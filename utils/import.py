#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (C) 2015  Ben Ockmore

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This module contains the functions necessary for importing BookBrainz data
from previously created dumps.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os
import shutil
import tarfile
import tempfile

import click
import psycopg2
import psycopg2.extensions

TABLE_RENAMES = {
    'user_sanitised': 'bookbrainz.user'
}


@click.command()
@click.argument('username')
@click.argument('database')
@click.option('--password', prompt=True, hide_input=True,
              help=('the password for the specified PostgreSQL user, prompted'
                    ' for if not provided in the command line'))
@click.option('--host', default='localhost',
              help='the hostname for the instance of PostgreSQL to connect to')
@click.option('--port', default=5432,
              help='the port for the instance of PostgreSQL to connect to')
@click.option('--keep-files/--delete-files', default=False,
              help="delete the imported files from the source directory")
@click.option('--tmp-dir', default=None,
              help='use DIR for temporary storage (default: /tmp)')
@click.option('--source', multiple=True, help='source files to import from')
def imp(username, database, password, **kwargs):
    """ Imports BookBrainz database dumps which have previously been stored
    in compressed tar archives. The user must provide the PostgreSQL USERNAME
    and PostgreSQL DATABASE to use, and will be prompted for a password.
    """

    start_time = datetime.datetime.now()
    sources = [os.path.abspath(s) for s in kwargs['source']]

    temp_dir = (None if kwargs['tmp_dir'] is None
                else os.path.abspath(kwargs['tmp_dir']))
    temp_output_dir = tempfile.mkdtemp(prefix='bbimport', dir=temp_dir)

    num_tables = 0

    for source in sources:
        archive = tarfile.open(source, 'r:bz2')
        archive.extractall(temp_output_dir)

    with psycopg2.connect(database=database, user=username, password=password,
                          host=kwargs['host'], port=kwargs['port']) as conn:
        conn.set_session(
            isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
        )
        with conn.cursor() as curs:
            curs.execute('SET CONSTRAINTS ALL DEFERRED')
            num_tables +=\
                import_directory(os.path.join(temp_output_dir, 'bbdump'), curs)
            set_sequence_values(curs)

    shutil.rmtree(temp_output_dir)
    if not kwargs['keep_files']:
        pass

    end_time = datetime.datetime.now()
    print("Imported {} tables in {}".format(num_tables, end_time - start_time))


def import_directory(source_dir, curs):
    """ Import BookBrainz tables from a directory containing dump files. """
    num_tables = 0
    for table in os.listdir(source_dir):
        with open(os.path.join(source_dir, table), 'rb') as f_obj:
            table = TABLE_RENAMES.get(table, table)
            print('Importing to {}...'.format(table))
            curs.copy_from(f_obj, table)
            num_tables += 1
    return num_tables

SEQUENCES = (
    ('bookbrainz.disambiguation_id_seq',
     'bookbrainz.disambiguation.disambiguation_id'),
    ('bookbrainz.edition_status_id_seq',
     'bookbrainz.edition_status.edition_status_id'),
    ('musicbrainz.language_id_seq', 'musicbrainz.language.id'),
    ('bookbrainz.work_type_id_seq',
     'bookbrainz.edition_status.edition_status_id'),
    ('bookbrainz.entity_data_id_seq',
     'bookbrainz.entity_data.entity_data_id'),
    ('bookbrainz.rel_type_id_seq',
     'bookbrainz.rel_type.relationship_type_id'),
    ('bookbrainz.annotation_id_seq',
     'bookbrainz.annotation.annotation_id'),
    ('bookbrainz.creator_type_id_seq',
     'bookbrainz.creator_type.creator_type_id'),
    ('musicbrainz.gender_id_seq', 'musicbrainz.gender.id'),
    ('bookbrainz.user_type_id_seq', 'bookbrainz.user_type.user_type_id'),
    ('bookbrainz.publisher_type_id_seq',
     'bookbrainz.publisher_type.publisher_type_id'),
    ('bookbrainz.publication_type_id_seq',
     'bookbrainz.publication_type.publication_type_id'),
    ('bookbrainz.user_id_seq', 'bookbrainz.user.user_id'),
    ('bookbrainz.alias_id_seq', 'bookbrainz.alias.alias_id'),
    ('bookbrainz.rel_tree_id_seq', 'bookbrainz.rel_data.relationship_data_id'),
    ('bookbrainz.revision_id_seq', 'bookbrainz.revision.revision_id'),
    ('bookbrainz.message_message_id_seq', 'bookbrainz.message.message_id'),
    ('bookbrainz.rel_id_seq', 'bookbrainz.rel.relationship_id'),
    ('bookbrainz.edit_note_id_seq',
     'bookbrainz.revision_note.revision_note_id'),
    ('bookbrainz.creator_credit_creator_credit_id_seq',
     'bookbrainz.creator_credit.creator_credit_id'),
    ('bookbrainz.identifier_type_identifier_type_id_seq',
     'bookbrainz.identifier_type.identifier_type_id'),
    ('bookbrainz.identifier_identifier_id_seq',
     'bookbrainz.identifier.identifier_id'),
    ('bookbrainz.edition_format_edition_format_id_seq',
     'bookbrainz.edition_format.edition_format_id')
)


def set_sequence_values(curs):
    """ Sets the next values of all sequences used for generation of
    autoincrement columns.
    """

    query_template =\
        "SELECT setval('{}', COALESCE((SELECT MAX({}) + 1 FROM {}), 1), false)"
    for sequence, column in SEQUENCES:
        table = '.'.join(column.split('.')[:-1])
        query = query_template.format(sequence, column, table)
        curs.execute(query)

if __name__ == "__main__":
    imp()
