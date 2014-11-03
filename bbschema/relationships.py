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

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        UnicodeText, SmallInteger)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import sqlalchemy.sql as sql

from .base import Base


class Relationship(Base):

    __tablename__ = 'relationship'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('bookbrainz.relationship_type.id'))


class RelationshipType(Base):

    __tablename__ = 'relationship_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)

    parent_id = Column(Integer, ForeignKey('bookbrainz.relationship_type.id'))
    child_order = Column(Integer, server_default=sql.text('0'), nullable=False)

    description = Column(UnicodeText, nullable=False)
    link_template = Column(UnicodeText, nullable=False)
    reverse_link_template = Column(UnicodeText, nullable=False)
    long_link_template = Column(UnicodeText, nullable=False)

    deprecated = Column(Boolean, server_default=sql.false(), nullable=False)


class ResourceRelationship(Base):

    __tablename__ = 'resource_relationship'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_id = Column(Integer, ForeignKey('bookbrainz.relationship.id'),
                             primary_key=True)
    template_position = Column(SmallInteger, nullable=False, primary_key=True)

    resource_gid = Column(UUID(as_uuid=True),
                          ForeignKey('bookbrainz.resource.gid'))


class TextRelationship(Base):

    __tablename__ = 'text_relationship'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_id = Column(Integer, ForeignKey('bookbrainz.relationship.id'),
                             primary_key=True)
    template_position = Column(SmallInteger, nullable=False, primary_key=True)

    text = Column(UnicodeText)
