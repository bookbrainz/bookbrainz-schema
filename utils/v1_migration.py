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

""" This module contains the functions necessary for migrating from v0.x of the
BookBrainz database to v1.x. There is no function to undo the operation,
therefore, it is advised that the database is backed up prior to running this
script.
"""

from __future__ import (absolute_import, division, print_function)

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bbschema import *


def migrate_types(session):
    session.execute("""
        INSERT INTO _bookbrainz.editor_type (
            id, label
        ) SELECT
            user_type_id, label
        FROM bookbrainz.user_type
    """)

    session.execute("""
        INSERT INTO _bookbrainz.publisher_type (
            id, label
        ) SELECT
            publisher_type_id, label
        FROM bookbrainz.publisher_type
    """)

    session.execute("""
        INSERT INTO _bookbrainz.creator_type (
            id, label
        ) SELECT
            creator_type_id, label
        FROM bookbrainz.creator_type
    """)

    session.execute("""
        INSERT INTO _bookbrainz.work_type (
            id, label
        ) SELECT
            work_type_id, label
        FROM bookbrainz.work_type
    """)

    session.execute("""
        INSERT INTO _bookbrainz.publication_type (
            id, label
        ) SELECT
            publication_type_id, label
        FROM bookbrainz.publication_type
    """)

    session.execute("""
        INSERT INTO _bookbrainz.edition_status (
            id, label
        ) SELECT
            edition_status_id, label
        FROM bookbrainz.edition_status
    """)

    session.execute("""
        INSERT INTO _bookbrainz.edition_format (
            id, label
        ) SELECT
            edition_format_id, label
        FROM bookbrainz.edition_format
    """)

    session.execute("""
        INSERT INTO _bookbrainz.identifier_type (
            id, label, description, detection_regex, validation_regex,
            display_template, entity_type, parent_id, child_order, deprecated
        ) SELECT
            identifier_type_id, label, description, detection_regex,
            validation_regex, 'Placeholder Template', 'Creator', parent_id,
            child_order, false
        FROM bookbrainz.identifier_type
    """)

    session.execute("""
        INSERT INTO _bookbrainz.relationship_type (
            id, label, description, display_template, source_entity_type,
            target_entity_type, parent_id, child_order, deprecated
        ) SELECT
            relationship_type_id, label, description, template, 'Creator',
            'Creator', parent_id, child_order, deprecated
        FROM bookbrainz.rel_type
    """)


def migrate_editors(session):
    session.execute("""
        INSERT INTO _bookbrainz.editor (
          id, name, email, reputation, bio, birth_date, created_at, active_at,
          type_id, gender_id, area_id, password, revisions_applied,
          revisions_reverted, total_revisions
        ) SELECT
          user_id, name, email, reputation, COALESCE(bio, ''::text),
          birth_date, created_at, active_at, user_type_id, gender_id, NULL,
          password, revisions_applied, revisions_reverted, total_revisions
        FROM bookbrainz.user
    """)

    session.execute("""
        INSERT INTO _bookbrainz.editor__language (
          editor_id, language_id, proficiency
        ) SELECT
          user_id, language_id, proficiency::text::_bookbrainz.lang_proficiency
        FROM bookbrainz.user_language
    """)


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
def migrate(username, database, password, **kwargs):
    """ Migrates the specified database from v0.x to v1.x, using the provided
    credentials and connections information.
    """

    connection_string =\
        'postgresql://{}:{}@{}:{}/{}'.format(
            username, password, kwargs['host'], kwargs['port'], database
        )

    engine = create_engine(connection_string, echo=True)
    Session = sessionmaker(bind=engine)

    session = Session()

    # Assume that the new schema exists in _bookbrainz

    migrate_types(session)
    migrate_editors(session)

    session.rollback()

if __name__ == "__main__":
    migrate()
