#!/usr/bin/env python2

from distutils.core import setup, Command
import unittest
import tests
import sys

class test_cmd(Command):
    description = "run automated tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        unittest.main(tests, argv=sys.argv[:-1])

if __name__ == '__main__':
    cmd_classes = {
        'test': test_cmd,
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
