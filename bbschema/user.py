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

import sqlalchemy.sql as sql
from bbschema.base import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, Text, Unicode, UnicodeText)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text


class UserType(Base):
    __tablename__ = 'user_type'
    __table_args__ = {'schema': 'bookbrainz'}

    user_type_id = Column(Integer, primary_key=True)

    label = Column(Unicode(255), nullable=False)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, primary_key=True)

    name = Column(Unicode(64), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Unicode(255), nullable=False)
    reputation = Column(Integer, nullable=False, server_default=text('0'))

    bio = Column(UnicodeText)
    birth_date = Column(Date)

    created_at = Column(DateTime, nullable=False,
                        server_default=sql.func.now())
    active_at = Column(DateTime, nullable=False,
                       server_default=sql.func.now())

    user_type_id = Column(
        Integer, ForeignKey('bookbrainz.user_type.user_type_id'),
        nullable=False
    )

    gender_id = Column(Integer, ForeignKey('musicbrainz.gender.id'))
    country_id = Column(Integer)

    total_revisions = Column(Integer, nullable=False, server_default=text('0'))
    revisions_applied = Column(Integer, nullable=False,
                               server_default=text('0'))
    revisions_reverted = Column(Integer, nullable=False,
                                server_default=text('0'))

    inactive = relationship('InactiveUser', uselist=False)
    suspended = relationship('SuspendedUser', uselist=False)
    languages = relationship('UserLanguage', backref='user')
    user_type = relationship('UserType')
    gender = relationship('Gender')


class InactiveUser(Base):
    __tablename__ = 'inactive_users'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                     primary_key=True)


class SuspendedUser(Base):
    __tablename__ = 'suspended_users'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                     primary_key=True)

    reason = Column(UnicodeText, nullable=False)


class UserLanguage(Base):
    __tablename__ = 'user_language'
    __table_args__ = {'schema': 'bookbrainz'}

    user_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                     primary_key=True)
    language_id = Column(Integer, ForeignKey('musicbrainz.language.id'),
                         primary_key=True)

    proficiency = Column(
        Enum('BASIC', 'INTERMEDIATE', 'ADVANCED', 'NATIVE',
             name='lang_proficiency'),
        nullable=False
    )

    language = relationship("Language")


class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {'schema': 'bookbrainz'}

    message_id = Column(Integer, primary_key=True)

    sender_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                       nullable=True)

    subject = Column(Unicode(255), nullable=False)
    content = Column(UnicodeText, nullable=False)

    sender = relationship('User')


class MessageReceipt(Base):

    __tablename__ = 'message_receipt'
    __table_args__ = {'schema': 'bookbrainz'}

    message_id = Column(Integer, ForeignKey('bookbrainz.message.message_id'),
                        primary_key=True)
    recipient_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                          primary_key=True)

    archived = Column(Boolean, nullable=False, default=False)

    message = relationship('Message', backref='receipts')
    recipient = relationship('User')


class OAuthClient(Base):
    __tablename__ = 'oauth_client'
    __table_args__ = {'schema': 'bookbrainz'}

    client_id = Column(UUID(as_uuid=True), primary_key=True,
                       server_default=text('public.uuid_generate_v4()'))

    client_secret = Column(
        UUID(as_uuid=True), unique=True, index=True, nullable=False,
        server_default=text('public.uuid_generate_v4()')
    )
    is_confidential = Column(Boolean, nullable=False,
                             server_default=sql.false())
    _redirect_uris = Column(UnicodeText, nullable=False, server_default='')
    _default_scopes = Column(UnicodeText, nullable=False, server_default='')

    # creator of the client, not required
    owner_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                      nullable=False)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return ''

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []
