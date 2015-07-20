# -*- coding: utf8 -*-

from sqlalchemy import create_engine

from bbschema.base import Base

INCLUDED_TABLES = [
    'musicbrainz.language',
    'musicbrainz.gender'
]


def create_all(hostname, port, username, password, db_name):
    connection_string =\
        'postgresql://{}:{}@{}/{}'.format(username, password, hostname,
                                          db_name)
    engine = create_engine(connection_string, echo=True)
    tables = [t for name, t in Base.metadata.tables.items()
              if name.startswith('bookbrainz') or name in INCLUDED_TABLES]
    Base.metadata.create_all(engine, tables=tables)
