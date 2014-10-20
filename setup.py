#!/usr/bin/env python2

from distutils.core import setup

setup(name='bbschema',
      version='1.0',
      description='Schema for the BookBrainz database',
      author='Ben Ockmore',
      author_email='ben.sput@gmail.com',
      url='https://bitbucket.org/bookbrainz/schema',
      packages=['bbschema'],
      requires=['sqlalchemy (>=0.9.7)', 'psycopg2 (>=2.5.4)'],
      provides=['bbschema'],
)
