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
    tables_imported = set()

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
            import_directory(os.path.join(temp_output_dir, 'bbdump'), curs)

    shutil.rmtree(temp_output_dir)
    if not kwargs['keep_files']:
        pass

    end_time = datetime.datetime.now()
    print("Imported {} tables in {}".format(num_tables, end_time - start_time))


def import_directory(source_dir, curs):
    for table in os.listdir(source_dir):
        with open(os.path.join(source_dir, table), 'rb') as f:
            table = TABLE_RENAMES.get(table, table)
            print('Importing to {}...'.format(table))
            curs.copy_from(f, table)

if __name__ == "__main__":
    imp()
