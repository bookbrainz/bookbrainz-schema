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
    session.add(user_types)

    # Add Publication Types
    publication_types = [
        PublicationType(label='Book'),
        PublicationType(label='Leaflet'),
        PublicationType(label='Newspaper'),
        PublicationType(label='Magazine'),
        PublicationType(label='Journal'),
    ]
    session.add(publication_types)

    # Add Creator Types
    creator_types = [
        CreatorType(label='Person'),
        CreatorType(label='Group'),
    ]
    session.add(creator_types)

    # Add Publisher Types - we probably need further research here
    publisher_types = [
        PublisherType(label='Publisher'),
        PublisherType(label='Distributor'),
    ]
    session.add(publisher_types)

    # Add Edition Statuses
    edition_statuses = [
        EditionStatus(label='Official'),
        EditionStatus(label='Draft'),
    ]
    session.add(edition_statuses)

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
    session.add(work_types)

    base_relationship_types = [
        RelationshipType(
            label='Worked on',
            description='Indicates that a creator worked on a work',
            template='{{{entities.0}}} worked on {{{entities.1}}}'
        ),
        RelationshipType(
            label='Illustrated',
            description='Indicates that a creator illustrated an edition',
            template='{{{entities.0}}} illustrated {{{entities.1}}}'
        ),
        RelationshipType(
            label='Edition',
            description='Represents the relationship between an edition and publication',
            template='{{{entities.0}}} is an edition of {{{entities.1}}}'
        ),
        RelationshipType(
            label='Publisher',
            description='Indicates that a publisher published an edition',
            template='{{{entities.0}}} published {{{entities.1}}}'
        ),
        RelationshipType(
            label='Editor',
            description='Indicates that a creator edited an edition',
            template='{{{entities.0}}} edited {{{entities.1}}}',
        ),
        RelationshipType(
            label='Inspiration',
            description='Indicates that one work was the inspiration for another work',
            template='{{{entities.0}}} was the inspiration for {{{entities.1}}}',
        ),
        RelationshipType(
            label='Parody',
            description='Indicates that one work was the inspiration for another work',
            template='{{{entities.0}}} was the inspiration for {{{entities.1}}}',
        ),
    ]

    creator_work_types = [
        RelationshipType(
            label='Authored',
            description='Indicates that a creator is the author of a work',
            template='{{{entities.0}}} authored {{{entities.1}}}',
            child_order=1,
        ),
        RelationshipType(
            label='Translated',
            description='Indicates that a creator translated a work',
            template='{{{entities.0}}} translated {{{entities.1}}} to {{{entities.2}}}',
            child_order=2,
        ),
    ]

    for t in creator_work_types:
        t.parent = relationship_types[0]

    session.add(base_relationship_types)
    session.add(creator_work_types)


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
                 user_type_id=editor_type.user_type_id)
    user2 = User(name="user2", email="user1@users.org",
                 user_type_id=editor_type.user_type_id)
    session.add_all([user1, user2])

    book_type = session.query(PublicationType).filter_by(label=u'Book').one()

    # Create some entities
    revision1 = EntityRevision.create(user, {
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
    })

    # Make an edit
    edit1 = Edit(user_id=user1.user_id, status=0)
    revision1.edits = [edit1]

    revision1.entity.master_revision = revision1

    session.add(revision1)
    session.commit()
