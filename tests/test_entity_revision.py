from unittest import TestCase

from bbschema import (Entity, EntityRevision, Publication, PublicationData,
                      User, config)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestRelationshipViews(TestCase):

    def setUp(self):
        conn_string = 'postgres://{}:{}@{}/{}'.format(
            config.USERNAME, config.PASSWORD, config.HOSTNAME, config.DATABASE
        )
        self.engine = create_engine(conn_string)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_create_publication(self):
        user = self.session.query(User).filter_by(user_id=1).one()
        revision_json = {
            'entity_gid': [],
            'publication_type': {
                'publication_type_id': 1
            },
            'annotation': u"Testing this entity, so don't actually use this.",
            'disambiguation': u'A disambiguation.',
            'aliases': [
                {
                    'name': u'ABC',
                    'sort_name': u'CBA',
                    'language_id': 1,
                    'default': False,
                    'primary': True
                }
            ]
        }

        entity = Publication()
        entity_data = PublicationData.create(revision_json, self.session)

        rev = EntityRevision(user_id=user.user_id)
        rev.entity = entity
        rev.entity_data = entity_data

        self.session.add(rev)
        self.session.commit()

        entity = rev.entity
        entity_data = rev.entity_data

        # Check properties of entity
        self.assertEquals(entity.master_revision_id, None)

        annotation = entity_data.annotation
        disambiguation = entity_data.disambiguation
        aliases = entity_data.aliases

        # Check annotation
        self.assertEqual(annotation.content, u"Testing this entity, so don't actually use this.")

        # Check disambiguation
        self.assertEqual(disambiguation.comment, u'A disambiguation.')

        # Check aliases
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0].name, u'ABC')
        self.assertEqual(aliases[0].sort_name, u'CBA')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertEqual(aliases[0].primary, True)

        # Check properties of entity_tree
        self.assertEqual(entity_data.default_alias_id, None)

        # Check properties of publication_data
        self.assertEqual(entity_data.publication_type_id, 1)

        entity.master_revision = rev
        self.session.commit()

        return entity.entity_gid

    def test_update_publication(self):
        # Create entity
        entity_gid = self.test_create_publication()
        entity = self.session.query(Entity).\
            filter_by(entity_gid=entity_gid).one()

        prev_master_revision_id = entity.master_revision_id
        prev_alias_id = entity.master_revision.entity_data.aliases[0].alias_id

        # Now, update it
        user = self.session.query(User).filter_by(user_id=1).one()

        new_entity_data = entity.master_revision.entity_data.update({
            'entity_gid': [entity_gid],
            'annotation': u"Testing this entity, so do actually use this.",
            'disambiguation': u'A different disambiguation.',
            'aliases': [
                [prev_alias_id, {
                    'name': u'ABCD',
                    'sort_name': u'DCBA',
                    'language_id': 2,
                    'default': True,
                    'primary': True
                }]
            ]
        }, self.session)

        rev = EntityRevision(user_id=user.user_id)
        rev.entity = entity
        rev.entity_data = new_entity_data

        self.session.add(rev)
        self.session.commit()

        entity = rev.entity
        entity_data = rev.entity_data

        # Check properties of entity
        self.assertEquals(entity.master_revision_id, prev_master_revision_id)

        annotation = entity_data.annotation
        disambiguation = entity_data.disambiguation
        aliases = entity_data.aliases

        # Check annotation
        self.assertEqual(annotation.content, u"Testing this entity, so do actually use this.")

        # Check disambiguation
        self.assertEqual(disambiguation.comment, u'A different disambiguation.')

        # Check aliases
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0].name, u'ABCD')
        self.assertEqual(aliases[0].sort_name, u'DCBA')
        self.assertEqual(aliases[0].language_id, 2)
        self.assertEqual(aliases[0].primary, True)

        # Check properties of entity_tree
        self.assertEqual(entity_data.default_alias_id, aliases[0].alias_id)

        # Check properties of publication_data
        self.assertEqual(entity_data.publication_type_id, 1)
