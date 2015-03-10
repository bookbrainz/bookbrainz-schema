# -*- coding: utf8 -*-

from sqlalchemy import create_engine

from bbschema.base import Base


def create_all(hostname, port, username, password, db_name):
    connection_string =\
        'postgresql://{}:{}@{}/{}'.format(username, password, hostname,
                                          db_name)
    engine = create_engine(connection_string, echo=True)
    Base.metadata.create_all(engine)
