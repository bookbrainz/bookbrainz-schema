# -*- coding: utf8 -*-

# Copyright (C) 2014  Ben Ockmore

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import (Column, Integer, String, DateTime, UnicodeText,
                        ForeignKey, Boolean, Unicode, Enum, Date)
from sqlalchemy.sql import text
import sqlalchemy.sql as sql
from sqlalchemy.orm import relationship

from bbschema.base import Base


class UserType(Base):
    __tablename__ = 'user_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)

    label = Column(Unicode(255), nullable=False)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(64), nullable=False, unique=True)
    email = Column(Unicode(255), nullable=False)
    reputation = Column(Integer, nullable=False, server_default=text('0'))
    bio = Column(UnicodeText)
    birth_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    active_at = Column(DateTime(timezone=True), server_default=sql.func.now())

    user_type_id = Column(Integer, ForeignKey('bookbrainz.user_type.id'),
                          nullable=False)
    gender_id = Column(Integer)
    country_id = Column(Integer)

    inactive = relationship('InactiveUser', uselist=False)
    suspended = relationship('SuspendedUser', uselist=False)
    editor_stats = relationship('EditorStats', uselist=False)


class InactiveUser(Base):
    __tablename__ = 'inactive_users'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, ForeignKey('bookbrainz.user.id'), primary_key=True)


class SuspendedUser(Base):
    __tablename__ = 'suspended_users'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, ForeignKey('bookbrainz.user.id'), primary_key=True)

    reason = Column(UnicodeText, nullable=False)


class EditorStats(Base):

    __tablename__ = 'editor_stats'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, ForeignKey('bookbrainz.user.id'),
                     primary_key=True)

    total_edits = Column(Integer, nullable=False, server_default=text('0'))
    total_revisions = Column(Integer, nullable=False, server_default=text('0'))
    edits_accepted = Column(Integer, nullable=False, server_default=text('0'))
    edits_rejected = Column(Integer, nullable=False, server_default=text('0'))
    edits_failed = Column(Integer, nullable=False, server_default=text('0'))
