# -*- coding: utf8 -*-

from sqlalchemy import create_engine

import bbschema


def create_all(hostname, port, username, password, db_name):
    connection_string =\
        'postgresql://{}:{}@{}/{}'.format(username, password, hostname,
                                          db_name)
    engine = create_engine(connection_string, echo=True)
    bbschema.create_all(engine)
