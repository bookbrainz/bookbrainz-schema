import copy
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from bbschema import config

from bbschema.entity import create_aliases, Alias, update_aliases


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
                'name': u'test',
                'sort_name': u'test_sort',
                'language_id': 1,
                'primary': True
            }
        ]
    }

    GOOD_DATA_SINGLE_UPDATE = {
        'aliases': [
            [
                0,
                {
                    'name': u'tested',
                    'sort_name': u'tested_sort',
                    'language_id': 2,
                    'primary': False
                }
            ]
        ]
    }

    def _assert_no_aliases(self, aliases, default_alias):
        self.assertEqual(len(aliases), 0)
        self.assertIs(default_alias, None)

    def _assert_alias_equal(self, alias, name, sort_name, language_id, primary):
        self.assertEqual(alias.name, name)
        self.assertEqual(alias.sort_name, sort_name)
        self.assertEqual(alias.language_id, language_id)
        self.assertEqual(alias.primary, primary)


    def test_alias__eq__(self):
        alias1 = Alias(name='test', sort_name='test_sort',
                       language_id=1, primary=True)
        alias2 = Alias(name='test', sort_name='test_sort',
                       language_id=1, primary=True)

        self.assertTrue(alias1 == alias2)
        self.assertFalse(alias1 == None)
        self.assertFalse(None == alias2)

    def test_create_alias_single(self):
        aliases, default_alias = create_aliases(self.GOOD_DATA_SINGLE)
        self.assertEqual(len(aliases), 1)
        self._assert_alias_equal(aliases[0], u'test', u'test_sort', 1, True)
        self.assertIs(default_alias, aliases[0])

    def test_create_alias_empty(self):
        aliases, default_alias = create_aliases({'aliases': []})
        self._assert_no_aliases(aliases, default_alias)

    def test_create_alias_missing_name(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        del bad_data['aliases'][0]['name']
        aliases, default_alias = create_aliases(bad_data)
        self._assert_no_aliases(aliases, default_alias)

    def test_create_alias_numeric_name(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        bad_data['aliases'][0]['name'] = 2
        aliases, default_alias = create_aliases(bad_data)
        self._assert_no_aliases(aliases, default_alias)

    def test_create_alias_missing_sort_name(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        del bad_data['aliases'][0]['sort_name']
        aliases, default_alias = create_aliases(bad_data)
        self._assert_no_aliases(aliases, default_alias)

    def test_create_alias_numeric_sort_name(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        bad_data['aliases'][0]['sort_name'] = 2
        aliases, default_alias = create_aliases(bad_data)
        self._assert_no_aliases(aliases, default_alias)

    def test_create_alias_missing_language(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        del bad_data['aliases'][0]['language_id']
        aliases, default_alias = create_aliases(bad_data)
        self.assertEqual(len(aliases), 1)
        self._assert_alias_equal(aliases[0], u'test', u'test_sort', None, True)
        self.assertIs(default_alias, aliases[0])

    def test_create_alias_invalid_language(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        bad_data['aliases'][0]['language_id'] = 0
        aliases, default_alias = create_aliases(bad_data)
        self.assertEqual(len(aliases), 0)
        self.assertIs(default_alias, None)

    def test_create_alias_textual_language(self):
        bad_data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        bad_data['aliases'][0]['language_id'] = "bob"
        aliases, default_alias = create_aliases(bad_data)
        self.assertEqual(len(aliases), 0)
        self.assertIs(default_alias, None)

    def test_create_alias_primary_false(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        data['aliases'][0]['primary'] = False
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_create_alias_primary_none(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        data['aliases'][0]['primary'] = None
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 0)
        self.assertIs(default_alias, None)

    def test_create_alias_primary_missing(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        del data['aliases'][0]['primary']
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_create_alias_primary_textual(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        data['aliases'][0]['primary'] = "bob"
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 0)
        self.assertEqual(default_alias, None)

    def test_create_alias_primary_numeric(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        data['aliases'][0]['primary'] = 500
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 0)
        self.assertIs(default_alias, None)

    def test_create_alias_single_default(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        data['aliases'].append(data['aliases'][0])
        data['aliases'][1]['default'] = True
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 2)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[1])

    def test_create_alias_multiple_default(self):
        data = copy.deepcopy(self.GOOD_DATA_SINGLE)
        data['aliases'].append(data['aliases'][0])
        data['aliases'][0]['default'] = True
        data['aliases'][1]['default'] = True
        aliases, default_alias = create_aliases(data)
        self.assertEqual(len(aliases), 2)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[1])

    def test_update_alias_single_nop(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['name'] = u'test'
        data['aliases'][0][1]['sort_name'] = u'test_sort'
        data['aliases'][0][1]['language_id'] = 1
        data['aliases'][0][1]['primary'] = True
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertIs(default_alias, alias)

    def test_update_alias_single_change_all(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIsNot(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'tested')
        self.assertEqual(aliases[0].sort_name, u'tested_sort')
        self.assertEqual(aliases[0].language_id, 2)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_missing_name(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        del data['aliases'][0][1]['name']
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIsNot(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'tested_sort')
        self.assertEqual(aliases[0].language_id, 2)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_numeric_name(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['name'] = 2
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_missing_sort_name(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        del data['aliases'][0][1]['sort_name']
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIsNot(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'tested')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 2)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_numeric_sort_name(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['sort_name'] = 2
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_missing_language(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        del data['aliases'][0][1]['language_id']
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIsNot(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'tested')
        self.assertEqual(aliases[0].sort_name, u'tested_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_invalid_language(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['language_id'] = 0
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_textual_language(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['language_id'] = 'bob'
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_primary_false(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['primary'] = False
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIsNot(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'tested')
        self.assertEqual(aliases[0].sort_name, u'tested_sort')
        self.assertEqual(aliases[0].language_id, 2)
        self.assertFalse(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_primary_none(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['primary'] = None
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_primary_missing(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        del data['aliases'][0][1]['primary']
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIsNot(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'tested')
        self.assertEqual(aliases[0].sort_name, u'tested_sort')
        self.assertEqual(aliases[0].language_id, 2)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_primary_textual(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['primary'] = 'bob'
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])

    def test_update_alias_primary_numeric(self):
        alias = Alias(name=u'test', sort_name=u'test_sort',
                       language_id=1, primary=True)
        self.session.add(alias)
        self.session.commit()

        data = copy.deepcopy(self.GOOD_DATA_SINGLE_UPDATE)
        data['aliases'][0][0] = alias.alias_id
        data['aliases'][0][1]['primary'] = 2
        aliases, default_alias = update_aliases([alias], alias.alias_id, data)
        self.assertEqual(len(aliases), 1)
        self.assertIs(aliases[0], alias)
        self.assertEqual(aliases[0].name, u'test')
        self.assertEqual(aliases[0].sort_name, u'test_sort')
        self.assertEqual(aliases[0].language_id, 1)
        self.assertTrue(aliases[0].primary)
        self.assertIs(default_alias, aliases[0])
