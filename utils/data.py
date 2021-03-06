# -*- coding: utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bbschema import *


def create_fixed(hostname, port, username, password, db_name):
    connection_string =\
        'postgresql://{}:{}@{}/{}'.format(username, password, hostname,
                                          db_name)

    engine = create_engine(connection_string, echo=True)
    Session = sessionmaker(bind=engine)

    session = Session()

    # Add User Types
    user_types = [
        UserType(label='Editor'),
        UserType(label='Bot'),
    ]
    session.add_all(user_types)

    # Create Bookworm user as a bot
    bot_type = session.query(UserType).filter_by(label=u'Bot').one()

    user = User(name="Bookworm", email="admin@bookbrainz.org",
                         password="", user_type_id=bot_type.user_type_id)
    session.add(user)

    # Create OAuth client for the frontend
    bookworm_user = session.query(User).filter_by(name=u'Bookworm').one()

    client = OAuthClient(owner_id=bookworm_user.user_id)
    session.add(client)

    # Add Publication Types
    publication_types = [
        PublicationType(label='Book'),
        PublicationType(label='Leaflet'),
        PublicationType(label='Newspaper'),
        PublicationType(label='Magazine'),
        PublicationType(label='Journal'),
    ]
    session.add_all(publication_types)

    # Add Creator Types
    creator_types = [
        CreatorType(label='Person'),
        CreatorType(label='Group'),
    ]
    session.add_all(creator_types)

    # Add Publisher Types - we probably need further research here
    publisher_types = [
        PublisherType(label='Publisher'),
        PublisherType(label='Distributor'),
    ]
    session.add_all(publisher_types)

    # Add Edition Formats
    edition_formats = [
        EditionFormat(label='Paperback'),
        EditionFormat(label='Hardcover'),
        EditionFormat(label='Mass Market Paperback'),
        EditionFormat(label='eBook'),
        EditionFormat(label='Library Binding'),
        EditionFormat(label='Audiobook'),
    ]
    session.add_all(edition_formats)

    # Add Edition Statuses
    edition_statuses = [
        EditionStatus(label='Official'),
        EditionStatus(label='Draft'),
    ]
    session.add_all(edition_statuses)

    # Add Work Types
    work_types = [
        WorkType(label='Novel'),
        WorkType(label='Short Story'),
        WorkType(label='Epic'),
        WorkType(label='Poem'),
        WorkType(label='Play'),
        WorkType(label='Article'),
        WorkType(label='Scientific Paper'),
        WorkType(label='Non-fiction'),
    ]
    session.add_all(work_types)

    identifier_types = [
        IdentifierType(
            label='MusicBrainz Release ID',
            description='UUID corresponding to a Release in MusicBrainz',
            detection_regex=r'musicbrainz\.org\/release\/([a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})',
            validation_regex=r'^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$',
            entity_type = 'Edition'
        ),
        IdentifierType(
            label='MusicBrainz Artist ID',
            description='UUID corresponding to an Artist in MusicBrainz',
            detection_regex=r'musicbrainz\.org\/artist\/([a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})',
            validation_regex=r'^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$',
            entity_type = 'Creator'
        ),
        IdentifierType(
            label='MusicBrainz Work ID',
            description='UUID corresponding to a Work in MusicBrainz',
            detection_regex=r'musicbrainz\.org\/work\/([a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12})',
            validation_regex=r'^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$',
            entity_type = 'Work'
        ),
        IdentifierType(
            label='Amazon ASIN',
            detection_regex=r'amazon\.*?\/(?:\.*?\/)*?(B\d{2}\w{7}|\d{9}[X\d])',
            validation_regex=r'^(?:B\d{2}\w{7}|\d{9}[X\d])$',
            description='ASIN of an edition available on Amazon',
            entity_type = 'Edition'
        ),
        IdentifierType(
            label='ISBN-13',
            description='13-digit International Standard Book Number',
            detection_regex=r'((?:\d-?){12}[X\d])',
            validation_regex=r'^(?:\d-?){12}[X\d]$',
            entity_type = 'Edition'
        ),
        IdentifierType(
            label='ISBN-10',
            description='10-digit International Standard Book Number',
            detection_regex=r'((?:\d-?){9}[X\d])',
            validation_regex=r'^(?:\d-?){9}[X\d]$',
            entity_type = 'Edition'
        )
    ]
    session.add_all(identifier_types)

    base_relationship_types = [
        RelationshipType(
            label='Worked on',
            description='Indicates that a creator worked on a work',
            template='{{{entities.[0]}}} worked on {{{entities.[1]}}}',
        ),
        RelationshipType(
            label='Illustrated',
            description='Indicates that a creator illustrated an edition',
            template='{{{entities.[0]}}} illustrated {{{entities.[1]}}}',
        ),
        RelationshipType(
            label='Edition',
            description='Represents the relationship between an edition and publication',
            template='{{{entities.[0]}}} is an edition of {{{entities.[1]}}}',
        ),
        RelationshipType(
            label='Publisher',
            description='Indicates that a publisher published an edition',
            template='{{{entities.[0]}}} published {{{entities.[1]}}}',
        ),
        RelationshipType(
            label='Editor',
            description='Indicates that a creator edited an edition',
            template='{{{entities.[0]}}} edited {{{entities.[1]}}}',
        ),
        RelationshipType(
            label='Inspiration',
            description='Indicates that one work was the inspiration for another work',
            template='{{{entities.[0]}}} was the inspiration for {{{entities.[1]}}}',
        ),
        RelationshipType(
            label='Parody',
            description='Indicates that one work was the inspiration for another work',
            template='{{{entities.[0]}}} was the inspiration for {{{entities.[1]}}}',
        ),
    ]

    creator_work_types = [
        RelationshipType(
            label='Authored',
            description='Indicates that a creator is the author of a work',
            template='{{{entities.[0]}}} authored {{{entities.[1]}}}',
            child_order=1,
        ),
        RelationshipType(
            label='Translated',
            description='Indicates that a creator translated a work',
            template='{{{entities.[0]}}} translated {{{entities.[1]}}} to {{{entities.[2]}}}',
            child_order=2,
        ),
    ]

    for t in creator_work_types:
        t.parent = base_relationship_types[0]

    session.add_all(base_relationship_types)
    session.add_all(creator_work_types)
    session.commit()


def create_test(hostname, port, username, password, db_name):
    connection_string =\
        'postgresql://{}:{}@{}/{}'.format(username, password, hostname,
                                          db_name)

    engine = create_engine(connection_string, echo=True)
    Session = sessionmaker(bind=engine)

    session = Session()

    editor_type = session.query(UserType).filter_by(label=u'Editor').one()

    # Create a couple of users
    user1 = User(name="user1", email="user1@users.org",
                 password="", user_type_id=editor_type.user_type_id)
    user2 = User(name="user2", email="user1@users.org",
                 password="", user_type_id=editor_type.user_type_id)
    session.add_all([user1, user2])

    book_type = session.query(PublicationType).filter_by(label=u'Book').one()

    languages = [
        Language(name="Klingon", frequency=1),
        Language(name="Romulan", frequency=2),
        Language(name="Ferengi", frequency=0)
    ]
    session.add_all(languages)

    # Create some entities

    revision_jsons = [
        {
            'entity_gid': [],
            'publication_data': {
                'publication_type_id': book_type.publication_type_id
            },
            'annotation': u"Testing this entity, so don't actually use this.",
            'disambiguation': u'book by Natsuo Kirino',
            'aliases': [
                {
                    'name': u'アウト',
                    'sort_name': u'アウト',
                    'language_id': 1,
                    'default': True,
                    'primary': True
                },
                {
                    'name': u'Out',
                    'sort_name': u'Out',
                    'language_id': 1,
                    'default': True,
                    'primary': True
                },
                {
                    'name': u'Le quattro casalinghe di Tokyo',
                    'sort_name': u'Le quattro casalinghe di Tokyo',
                    'language_id': 1,
                    'default': True,
                    'primary': True
                },
                {
                    'name': u'De nachtploeg',
                    'sort_name': u'De nachtploeg',
                    'language_id': 1,
                    'default': True,
                    'primary': True
                }
            ]
        },
    ]

    for revision_json in revision_jsons:
        if 'publication_data' in revision_json:
            entity_data = PublicationData.create(revision_json, session)
            entity = Publication()

        revision = EntityRevision(user_id=user1.user_id)
        revision.entity = entity
        revision.entity_data = entity_data

        revision.entity.master_revision = revision

        session.add(revision)

    session.commit()
