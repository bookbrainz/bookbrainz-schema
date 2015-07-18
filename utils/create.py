# -*- coding: utf8 -*-

from sqlalchemy import create_engine

from bbschema.base import Base


def create_all(hostname, port, username, password, db_name):
    connection_string =\
        'postgresql://{}:{}@{}/{}'.format(username, password, hostname,
                                          db_name)
    engine = create_engine(connection_string, echo=True)
    tables = [t for t in Base.metadata.tables.values() if t.schema == 'bookbrainz' or (t.schema == 'musicbrainz' and t.name in ['gender', 'language'])]
    Base.metadata.create_all(engine, tables=tables)
