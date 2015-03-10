schema
======

.. image:: https://travis-ci.org/BookBrainz/bookbrainz-schema.svg?branch=master
    :target: https://travis-ci.org/BookBrainz/bookbrainz-schema

This package contains the SQLAlchemy models mapping the BookBrainz database
schema to Python objects. It is likely to change considerably during the early
stages of development.

Installation
------------

First, install all of the required modules. You can do this with pip, as
follows:

    pip install -r requirements.txt

Then, run setup.py, to install the bbschema package:

    python setup.py install

You'll probably need to prefix these commands with "sudo" to get anywhere!

Testing
-------

To perform tests, you'll need to have a working installation of Postgresql.
Edit the config.py file in bbschema/ to accomodate your settings, after
creating a database to run the tests on. Then, execute the following commands:

    python setup.py bootstrap
    python setup.py test
