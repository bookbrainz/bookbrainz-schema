import copy
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from bbschema import config

from bbschema.entity import create_aliases, Alias


class TestAliases(TestCase):
    def setUp(self):
        conn_string = 'postgres://{}:{}@{}/{}'.format(
            config.USERNAME, config.PASSWORD, config.HOSTNAME, config.DATABASE
        )
        self.engine = create_engine(conn_string)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    GOOD_DATA_SINGLE = {
        'aliases': [
            {
                'name': 'test',
                'sort_name': 'test_sort',
                'language_id': 1,
                'primary': True
            }
        ]
    }

    def test_alias__eq__(self):
        alias1 = Alias(name='test', sort_name='test_sort', language_id=1, primary=False)
        alias2 = Alias(name='test', sort_name='test_sort', language_id=1, primary=False)

        self.assertTrue(alias1 == alias2)
        self.assertFalse(alias1 == None)
        self.assertFalse(None == alias2)

    def test_create_alias_single(self):
        aliases, default_alias = create_aliases(self.GOOD_DATA_SINGLE)
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertEqual(aliases[0], default_alias)

    def test_create_alias_empty(self):
        aliases, default_alias = create_aliases({'aliases': []})
        self.assertEqual(len(aliases), 0)
        self.assertEqual(default_alias, None)

    def test_create_alias_missing_name(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        del bad_data['aliases'][0]['name']
        aliases, default_alias = create_aliases(bad_data)
        self.assertEqual(len(aliases), 0)
        self.assertEqual(default_alias, None)
