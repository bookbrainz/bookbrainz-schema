#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from sqlalchemy import create_engine

from bbschema.base import Base

engine = create_engine(sys.argv[1], echo=True)
Base.metadata.create_all(engine)
