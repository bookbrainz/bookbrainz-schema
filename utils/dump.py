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

""" This module contains the functions necessary for dumping BookBrainz data
from the database to files, and optionally compressing those files.
"""

from __future__ import print_function

import os

import click
import psycopg2
import psycopg2.extensions

GROUPS = {
    'core': [
        ('bookbrainz', [
            'alias',
            'creator_credit',
            'creator_credit_name',
            'creator_data',
            'creator_type',
            'creator_data',
            'disambiguation',
            'edition_data',
            'edition_format',
            'edition_status',
            'entity',
            'entity_data',
            'entity_data__alias',
            'entity_data__identifier',
            'entity_redirect',
            'entity_revision',
            'identifier',
            'identifier_type',
            'publication_data',
            'publication_type',
            'publisher_data',
            'publisher_type',
            'rel',
            'rel_data',
            'rel_entity',
            'rel_revision',
            'rel_text',
            'rel_type',
            'revision',
            'user_language',
            'user_type',
            'work_data',
            'work_data__language',
            'work_type'
        ]),
        ('musicbrainz', [
            'language',
            'gender'
        ])
    ],
    'derived': [
        ('bookbrainz', [
            'annotation',
            'revision_note'
        ])
    ],
    'editor': [
        (None, [
            'user_sanitised'
        ])
    ],
    'private': [
        ('bookbrainz', [
            'inactive_users',
            'message',
            'message_receipt',
            'oauth_client',
            'suspended_users',
            'user'
        ])
    ]
}

TEMPORARIES = [
    """
        SELECT
            user_id, name,
            'bookbrainz' AS password,
            '' AS email,
            reputation,
            NULL as bio,
            NULL as birth_date,
            created_at, active_at, user_type_id,
            NULL as gender_id,
            NULL as country_id,
            total_revisions, revisions_applied, revisions_reverted
        INTO TEMPORARY user_sanitised
        FROM bookbrainz.user
    """
]


@click.command()
@click.argument('username')
@click.argument('database')
@click.option('--password', prompt=True, hide_input=True)
@click.option('--host', default='localhost')
@click.option('--port', default=5432)
@click.option('--compress/--no-compress', default=False)
@click.option('--output-dir', default='.')
@click.option('--tmp-dir', default='/tmp')
@click.option('--keep-files/--delete-files', default=False)
def dump(username, database, password, **kwargs):
    """ Dumps the bookbrainz data from the specified database into files. """
    compress = kwargs['compress']
    output_dir = os.path.abspath(kwargs['output_dir'])

    with psycopg2.connect(database=database, user=username, password=password,
                          host=kwargs['host'], port=kwargs['port']) as conn:
        conn.set_session(
            isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
        )
        with conn.cursor() as curs:
            create_temporaries(curs)
            for group in GROUPS.keys():
                print("Dumping Group {}...".format(group))
                dump_group(curs, output_dir, group)


def create_temporaries(cursor):
    for temporary in TEMPORARIES:
        cursor.execute(temporary)


def dump_group(cursor, output_dir, group):
    schemas = GROUPS[group]
    for schema, tables in schemas:
        for table in tables:
            dump_table(cursor, output_dir, schema, table)


def dump_table(cursor, output_dir, schema, table):
    qualified_name = (schema + '.' + table) if schema is not None else table
    print("\tDumping Table {}...".format(qualified_name))
    with open(os.path.join(output_dir, table), 'wb') as f:
        cursor.copy_to(f, qualified_name)

if __name__ == "__main__":
    dump()
