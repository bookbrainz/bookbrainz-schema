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

from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, ForeignKey, SMALLINT, CHAR, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, composite
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.sql as sql

from mbdata.types import PartialDate

from bbschema.base import Base


class AreaType(Base):
    __tablename__ = 'area_type'
    __table_args__ = {'schema': 'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Area(Base):
    __tablename__ = 'area'
    __table_args__ = {'schema': 'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    sort_name = Column(String, nullable=False)
    type_id = Column('type', Integer, ForeignKey('musicbrainz.area_type.id', name='area_fk_type'))
    edits_pending = Column(Integer, default=0, server_default=sql.text('0'), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    ended = Column(Boolean, default=False, server_default=sql.false(), nullable=False)
    comment = Column(String(255), default='', server_default=sql.text("''"), nullable=False)

    type = relationship('AreaType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class AreaGIDRedirect(Base):
    __tablename__ = 'area_gid_redirect'
    __table_args__ = {'schema': 'musicbrainz'}

    gid = Column(UUID, primary_key=True, nullable=False)
    redirect_id = Column('new_id', Integer, ForeignKey('musicbrainz.area.id', name='area_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Area', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def area(self):
        return self.redirect


class AreaAliasType(Base):
    __tablename__ = 'area_alias_type'
    __table_args__ = {'schema': 'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class AreaAlias(Base):
    __tablename__ = 'area_alias'
    __table_args__ = {'schema': 'musicbrainz'}

    id = Column(Integer, primary_key=True)
    area_id = Column('area', Integer, ForeignKey('musicbrainz.area.id', name='area_alias_fk_area'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, default=0, server_default=sql.text('0'), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey('musicbrainz.area_alias_type.id', name='area_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, default=False, server_default=sql.false(), nullable=False)
    ended = Column(Boolean, default=False, server_default=sql.false(), nullable=False)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    type = relationship('AreaAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class Language(Base):
    __tablename__ = 'language'
    __table_args__ = {'schema': 'musicbrainz'}

    id = Column(Integer, primary_key=True)
    iso_code_2t = Column(CHAR(3))
    iso_code_2b = Column(CHAR(3))
    iso_code_1 = Column(CHAR(2))
    name = Column(String(100), nullable=False)
    frequency = Column(Integer, default=0, server_default=sql.text('0'), nullable=False)
    iso_code_3 = Column(CHAR(3))
