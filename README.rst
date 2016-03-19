schema
======

.. image:: https://travis-ci.org/bookbrainz/bookbrainz-schema.svg?branch=master
    :target: https://travis-ci.org/bookbrainz/bookbrainz-schema

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

Importing Dumps
---------------

''Creating the Schema''
The first step in importing the BookBrainz dumps is to run the schema
creation script. This can be downloaded from the same location as the dumps.
This will create the necessary schemas and tables within a database you've
previously created. The commands to do this will be similar to the following
(with the necessary replacements):

    psql -U <pg_username> <bb_db> -c 'CREATE EXTENSION "uuid-ossp" SCHEMA public'

    psql -U <pg_username> <bb_db> -f <bbdump-structure download location>

Subsequently, download the data dumps, and import them using the
utils/import.py script. This script has a built-in help command. An example
usage of the script is:

    python import.py <pg_username> <bb_db> --source=<core_dump> --source=<derived_dump> --source=<editor_dump>

Note - at this stage, all three dumps must be provided to the import script.
After running this command, all the data will have been imported, and you should
be able to run queries against it and start an instance of the BookBrainz
web service.

Testing
-------

To perform tests, you'll need to have a working installation of Postgresql.
Edit the config.py file in bbschema/ to accomodate your settings, after
creating a database to run the tests on. Then, execute the following commands:

    python setup.py bootstrap

    python setup.py test
