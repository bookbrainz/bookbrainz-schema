# -*- coding: utf8 -*-

"""This module contains mappings for data shared with the MusicBrainz project,
which would either be too costly or just unnecessary to collect independently.
These mappings were copied directly from the mbdata project - I couldn't use
that directly due to the predefined Base class:

https://bitbucket.org/lalinsky/mbdata

The original license for these classes is included in the comment below.
"""

# Copyright (c) 2013 Lukas Lalinsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sqlalchemy.sql as sql
from bbschema.base import Base
from sqlalchemy import CHAR, Column, ForeignKey, Integer, Unicode, UnicodeText


class Gender(Base):
    __tablename__ = 'gender'
    __table_args__ = {'schema': 'musicbrainz'}

    gender_id = Column('id', Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent_id = Column(Integer, ForeignKey('musicbrainz.gender.id'))
    child_order = Column(Integer, nullable=False, server_default=sql.text('0'))
    description = Column(UnicodeText)


class Language(Base):
    __tablename__ = 'language'
    __table_args__ = {'schema': 'musicbrainz'}

    language_id = Column('id', Integer, primary_key=True)
    iso_code_2t = Column(CHAR(3))
    iso_code_2b = Column(CHAR(3))
    iso_code_1 = Column(CHAR(2))
    name = Column(Unicode(100), nullable=False)
    frequency = Column(Integer, nullable=False, server_default=sql.text('0'))
    iso_code_3 = Column(CHAR(3))
