#!/usr/bin/env python2

from distutils.core import setup, Command
import unittest
import sys

class test_cmd(Command):
    description = "run automated tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import tests
        unittest.main(tests, argv=sys.argv[:-1])


class bootstrap(Command):
    description = "initialize database and fixed data"
    user_options = [
        ('notables', 'n', "don't create tables"),
        ('blank', 'b', "don't add test data")
    ]

    def initialize_options(self):
        self.blank = False
        self.notables = False

    def finalize_options(self):
        pass

    def run(self):
        import utils.create
        import utils.data
        from bbschema import config

        if not self.notables:
            utils.create.create_all(
                config.HOSTNAME, config.PORT, config.USERNAME, config.PASSWORD,
                config.DATABASE
            )

        utils.data.create_fixed(config.HOSTNAME, config.PORT, config.USERNAME,
                                config.PASSWORD, config.DATABASE)

        if not self.blank:
            utils.data.create_test(
                config.HOSTNAME, config.PORT, config.USERNAME, config.PASSWORD,
                config.DATABASE
            )


if __name__ == '__main__':
    cmd_classes = {
        'test': test_cmd,
        'bootstrap': bootstrap,
    }

    setup(
        cmdclass=cmd_classes,
        name='bbschema',
        version='1.0',
        description='Schema for the BookBrainz database',
        author='Ben Ockmore',
        author_email='ben.sput@gmail.com',
        url='https://bitbucket.org/bookbrainz/schema',
        packages=['bbschema'],
        requires=['sqlalchemy (>=0.9.7)', 'psycopg2 (>=2.5.4)'],
        provides=['bbschema'],
    )
