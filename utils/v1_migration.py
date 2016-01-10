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
            id, name, email, reputation, bio, birth_date, created_at,
            active_at, type_id, gender_id, area_id, password,
            revisions_applied, revisions_reverted, total_revisions
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
            user_id, language_id,
            proficiency::text::_bookbrainz.lang_proficiency
        FROM bookbrainz.user_language
    """)


def migrate_revisions(session):
    session.execute("""
        INSERT INTO _bookbrainz.revision (
            id, author_id, created_at, type
        ) SELECT
            r.revision_id, r.user_id, r.created_at,
            e._type::text::_bookbrainz.entity_type
        FROM bookbrainz.revision r
        LEFT JOIN bookbrainz.entity_revision er
            ON r.revision_id = er.revision_id
        LEFT JOIN bookbrainz.entity e
            ON e.entity_gid = er.entity_gid;
    """)

    session.execute("""
        INSERT INTO _bookbrainz.revision_parent (
            parent_id, child_id
        ) SELECT
            revision_id, parent_id
        FROM bookbrainz.revision
        WHERE parent_id IS NOT NULL;
    """)

    session.execute("""
        INSERT INTO _bookbrainz.note (
            id, author_id, revision_id, content, posted_at
        ) SELECT
            revision_note_id, user_id, revision_id, content, posted_at
        FROM bookbrainz.revision_note;
    """)


def limit_query(q, limit):
    offset = 0
    results = q.limit(limit).offset(offset).all()
    while results:
        for result in results:
            yield result
        offset += limit
        results = q.limit(limit).offset(offset).all()


def convert_date(date, precision):
    if date is None:
        return (None, None, None)
    else:
        if precision == 'DAY':
            return (date.year, date.month, date.day)
        elif precision == 'MONTH':
            return (date.year, date.month, None)
        else:
            return (date.year, None, None)


def insert_creator_data_and_revision(session, entity, revision, alias_set_id,
                                     identifier_set_id):
    data = revision.entity_data
    begin_year, begin_month, begin_day = \
        convert_date(data.begin_date, data.begin_date_precision)
    end_year, end_month, end_day = \
        convert_date(data.end_date, data.end_date_precision)

    result = session.execute(
        '''INSERT INTO _bookbrainz.creator_data (
            alias_set_id, identifier_set_id, annotation_id,
            disambiguation_id, begin_year, begin_month, begin_day, end_year,
            end_month, end_day, ended, gender_id, type_id
        ) VALUES (
            :alias_set_id, :identifier_set_id, :annotation_id,
            :disambiguation_id,  :begin_year, :begin_month, :begin_day,
            :end_year, :end_month, :end_day, :ended, :gender_id, :type_id
        ) RETURNING id''', {
            'alias_set_id': alias_set_id,
            'identifier_set_id': identifier_set_id,
            'annotation_id': data.annotation_id,
            'disambiguation_id': data.disambiguation_id,
            'begin_year': begin_year,
            'begin_month': begin_month,
            'begin_day': begin_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day,
            'ended': data.ended,
            'gender_id': data.gender_id,
            'type_id': data.creator_type_id
        }
    )
    data_id = result.fetchone()[0]

    session.execute(
        '''INSERT INTO _bookbrainz.creator_revision (
            id, bbid, data_id
        ) VALUES (
            :id, :bbid, :data_id
        )''', {
            'id': revision.revision_id,
            'bbid': entity.entity_gid,
            'data_id': data_id
        }
    )


def insert_edition_data_and_revision(session, entity, revision, alias_set_id,
                                     identifier_set_id):
    data = revision.entity_data

    result = session.execute(
        '''INSERT INTO _bookbrainz.edition_data (
            alias_set_id, identifier_set_id, annotation_id,
            disambiguation_id, publication_bbid, width, height, depth,
            weight, pages, format_id, status_id
        ) VALUES (
            :alias_set_id, :identifier_set_id, :annotation_id,
            :disambiguation_id, :publication_bbid, :width, :height,
            :depth, :weight, :pages, :format_id, :status_id
        ) RETURNING id''', {
            'alias_set_id': alias_set_id,
            'identifier_set_id': identifier_set_id,
            'annotation_id': data.annotation_id,
            'disambiguation_id': data.disambiguation_id,
            'publication_bbid': data.publication_gid,
            'width': data.width,
            'height': data.height,
            'depth': data.depth,
            'weight': data.weight,
            'pages': data.pages,
            'format_id': data.edition_format_id,
            'status_id': data.edition_status_id
        }
    )
    data_id = result.fetchone()[0]

    # Create a release event if release date is not NULL
    if data.release_date is not None:
        release_year, release_month, release_day = \
            convert_date(data.release_date, data.release_date_precision)
        result = session.execute(
            '''INSERT INTO _bookbrainz.release_event (
                "year", "month", "day"
            ) VALUES (
                :year, :month, :day
            ) RETURNING id
            ''', {
                'year': release_year,
                'month': release_month,
                'day': release_day
            }
        )

        release_event_id = result.fetchone()[0]
        session.execute(
            '''INSERT INTO _bookbrainz.release_event__edition_data (
                release_event_id, edition_data_id
            ) VALUES (
                :event_id, :data_id
            )
            ''', {
                'event_id': release_event_id,
                'data_id': data_id
            }
        )

    if data.language_id is not None:
        session.execute(
            '''INSERT INTO _bookbrainz.edition_data__language (
                data_id, language_id
            ) VALUES (
                :data_id, :language_id
            )
            ''', {
                'data_id': data_id,
                'language_id': data.language_id
            }
        )

    if data.publisher_gid is not None:
        session.execute(
            '''INSERT INTO _bookbrainz.edition_data__publisher (
                data_id, publisher_bbid
            ) VALUES (
                :data_id, :publisher_bbid
            )
            ''', {
                'data_id': data_id,
                'publisher_bbid': data.publisher_gid
            }
        )

    session.execute(
        '''INSERT INTO _bookbrainz.edition_revision (
            id, bbid, data_id
        ) VALUES (
            :id, :bbid, :data_id
        )''', {
            'id': revision.revision_id,
            'bbid': entity.entity_gid,
            'data_id': data_id
        }
    )


def insert_work_data_and_revision(session, entity, revision, alias_set_id,
                                  identifier_set_id):
    data = revision.entity_data

    result = session.execute(
        '''INSERT INTO _bookbrainz.work_data (
            alias_set_id, identifier_set_id, annotation_id,
            disambiguation_id, type_id
        ) VALUES (
            :alias_set_id, :identifier_set_id, :annotation_id,
            :disambiguation_id, :type_id
        ) RETURNING id''', {
            'alias_set_id': alias_set_id,
            'identifier_set_id': identifier_set_id,
            'annotation_id': data.annotation_id,
            'disambiguation_id': data.disambiguation_id,
            'type_id': data.work_type_id
        }
    )
    data_id = result.fetchone()[0]

    # Create a release event if release date is not NULL
    for language in data.languages:
        session.execute(
            '''INSERT INTO _bookbrainz.work_data__language (
                data_id, language_id
            ) VALUES (
                :data_id, :language_id
            )
            ''', {
                'data_id': data_id,
                'language_id': language.id
            }
        )

    session.execute(
        '''INSERT INTO _bookbrainz.work_revision (
            id, bbid, data_id
        ) VALUES (
            :id, :bbid, :data_id
        )''', {
            'id': revision.revision_id,
            'bbid': entity.entity_gid,
            'data_id': data_id
        }
    )


def insert_publisher_data_and_revision(session, entity, revision, alias_set_id,
                                       identifier_set_id):
    data = revision.entity_data
    begin_year, begin_month, begin_day = \
        convert_date(data.begin_date, data.begin_date_precision)
    end_year, end_month, end_day = \
        convert_date(data.end_date, data.end_date_precision)

    result = session.execute(
        '''INSERT INTO _bookbrainz.publisher_data (
            alias_set_id, identifier_set_id, annotation_id, disambiguation_id,
            begin_year, begin_month, begin_day, end_year, end_month, end_day,
            ended, type_id
        ) VALUES (
            :alias_set_id, :identifier_set_id, :annotation_id,
            :disambiguation_id, :begin_year, :begin_month, :begin_day,
            :end_year, :end_month, :end_day, :ended, :type_id
        ) RETURNING id''', {
            'alias_set_id': alias_set_id,
            'identifier_set_id': identifier_set_id,
            'annotation_id': data.annotation_id,
            'disambiguation_id': data.disambiguation_id,
            'begin_year': begin_year,
            'begin_month': begin_month,
            'begin_day': begin_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day,
            'ended': data.ended,
            'type_id': data.publisher_type_id
        }
    )
    data_id = result.fetchone()[0]

    session.execute(
        '''INSERT INTO _bookbrainz.publisher_revision (
            id, bbid, data_id
        ) VALUES (
            :id, :bbid, :data_id
        )''', {
            'id': revision.revision_id,
            'bbid': entity.entity_gid,
            'data_id': data_id
        }
    )



def insert_publication_data_and_revision(session, entity, revision,
                                         alias_set_id, identifier_set_id):
    data = revision.entity_data

    result = session.execute(
        '''INSERT INTO _bookbrainz.publication_data (
            alias_set_id, identifier_set_id, annotation_id, disambiguation_id,
            type_id
        ) VALUES (
            :alias_set_id, :identifier_set_id, :annotation_id,
            :disambiguation_id, :type_id
        ) RETURNING id''', {
            'alias_set_id': alias_set_id,
            'identifier_set_id': identifier_set_id,
            'annotation_id': data.annotation_id,
            'disambiguation_id': data.disambiguation_id,
            'type_id': data.publication_type_id
        }
    )
    data_id = result.fetchone()[0]

    session.execute(
        '''INSERT INTO _bookbrainz.publication_revision (
            id, bbid, data_id
        ) VALUES (
            :id, :bbid, :data_id
        )''', {
            'id': revision.revision_id,
            'bbid': entity.entity_gid,
            'data_id': data_id
        }
    )

def migrate_entities(session):
    session.execute("""
        INSERT INTO _bookbrainz.entity (
            bbid, type
        ) SELECT
            entity_gid, _type::text::_bookbrainz.entity_type
        FROM bookbrainz.entity
    """)

    # Leave master_revision_id NULL for now - they don't exist yet
    session.execute("""
        INSERT INTO _bookbrainz.creator_header (
            bbid
        ) SELECT
            entity_gid
        FROM bookbrainz.entity
        WHERE _type = 'Creator'
    """)

    session.execute("""
        INSERT INTO _bookbrainz.edition_header (
            bbid
        ) SELECT
            entity_gid
        FROM bookbrainz.entity
        WHERE _type = 'Edition'
    """)

    session.execute("""
        INSERT INTO _bookbrainz.publication_header (
            bbid
        ) SELECT
            entity_gid
        FROM bookbrainz.entity
        WHERE _type = 'Publication'
    """)

    session.execute("""
        INSERT INTO _bookbrainz.publisher_header (
            bbid
        ) SELECT
            entity_gid
        FROM bookbrainz.entity
        WHERE _type = 'Publisher'
    """)

    session.execute("""
        INSERT INTO _bookbrainz.work_header (
            bbid
        ) SELECT
            entity_gid
        FROM bookbrainz.entity
        WHERE _type = 'Work'
    """)

def migrate_entity_data(session):
    session.execute("""
        INSERT INTO _bookbrainz.annotation (
            id, content, last_revision_id
        ) SELECT DISTINCT ON(a.annotation_id)
            a.annotation_id, a.content, r.revision_id
        FROM bookbrainz.entity_revision er
        LEFT JOIN bookbrainz.revision r
            ON r.revision_id = er.revision_id
        LEFT JOIN bookbrainz.entity_data ed
            ON er.entity_data_id = ed.entity_data_id
        LEFT JOIN bookbrainz.annotation a
            ON ed.annotation_id = a.annotation_id
        WHERE a.annotation_id IS NOT NULL
        ORDER BY a.annotation_id, revision_id
    """)

    session.execute("""
        INSERT INTO _bookbrainz.disambiguation (
            id, comment
        ) SELECT
            disambiguation_id, COALESCE(comment, ''::text)
        FROM bookbrainz.disambiguation
    """)

    session.execute("""
        INSERT INTO _bookbrainz.alias (
            id, name, sort_name, language_id, "primary"
        ) SELECT
            alias_id, name, sort_name, language_id, "primary"
        FROM bookbrainz.alias
    """)

    session.execute("""
        INSERT INTO _bookbrainz.identifier (
            id, type_id, value
        ) SELECT
            identifier_id, identifier_type_id, value
        FROM bookbrainz.identifier
    """)

    # For each entity, go through all the entity and relationship revisions
    # Keep track of the aliases, identifiers and relationships on the
    # entity at all times
    # For each entity revision, create a new alias set, identifier_set and
    # relationship set, using the tracked aliases, identifier and
    # relationships
    entity_query = session.query(Entity)
    for entity in limit_query(entity_query, 100):
        print(entity)
        print('--------------')
        entity_revision_query = session.query(EntityRevision).\
            filter(EntityRevision.entity_gid == entity.entity_gid)
        relationship_revision_query = session.query(RelationshipRevision).\
            join(RelationshipData).\
            join(RelationshipEntity).\
            filter(RelationshipEntity.entity_gid == entity.entity_gid)

        all_revisions = (
            entity_revision_query.all() + relationship_revision_query.all()
        )

        all_revisions = sorted(all_revisions, key=lambda x: x.created_at)

        relationships = []
        aliases = []
        identifiers = []
        for revision in all_revisions:
            print('r{}'.format(revision.revision_id))
            if isinstance(revision, EntityRevision):
                aliases = revision.entity_data.aliases
                identifiers = revision.entity_data.identifiers
                default_alias = revision.entity_data.default_alias

                # Create alias set
                result = session.execute('''INSERT INTO _bookbrainz.alias_set (
                        default_alias_id
                    ) VALUES (
                        :default_id
                    ) RETURNING id
                ''', {"default_id": default_alias.alias_id if default_alias is not None else None})
                alias_set_id = result.fetchone()[0]

                for alias in aliases:
                    session.execute('''INSERT INTO _bookbrainz.alias_set__alias (
                            set_id, alias_id
                        ) VALUES (
                            :set_id, :alias_id
                        )
                    ''', {"set_id": alias_set_id, "alias_id": alias.alias_id})


                # Create identifier set
                result = session.execute('''INSERT INTO _bookbrainz.identifier_set
                    DEFAULT VALUES RETURNING id
                ''')
                identifier_set_id = result.fetchone()[0]

                # Add identifiers to set
                for identifier in identifiers:
                    session.execute('''INSERT INTO _bookbrainz.identifier_set__identifier (
                            set_id, identifier_id
                        ) VALUES (
                            :set_id, :identifier_id
                        )
                    ''', {"set_id": identifier_set_id, "identifier_id": identifier.identifier_id})

                # Create entity data
                if isinstance(revision.entity_data, CreatorData):
                    insert_creator_data_and_revision(
                        session, entity, revision, alias_set_id,
                        identifier_set_id
                    )
                elif isinstance(revision.entity_data, EditionData):
                    insert_edition_data_and_revision(
                        session, entity, revision, alias_set_id,
                        identifier_set_id
                    )
                elif isinstance(revision.entity_data, WorkData):
                    insert_work_data_and_revision(
                        session, entity, revision, alias_set_id,
                        identifier_set_id
                    )
                elif isinstance(revision.entity_data, PublisherData):
                    insert_publisher_data_and_revision(
                        session, entity, revision, alias_set_id,
                        identifier_set_id
                    )
                elif isinstance(revision.entity_data, PublicationData):
                    insert_publication_data_and_revision(
                        session, entity, revision, alias_set_id,
                        identifier_set_id
                    )
                else:
                    raise Error('Err... what?')

                # Create revision

        # Also need to make a new entity data row for each relationship
        # revision

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
    migrate_revisions(session)
    migrate_entities(session)
    migrate_entity_data(session)

    session.rollback()

if __name__ == "__main__":
    migrate()
