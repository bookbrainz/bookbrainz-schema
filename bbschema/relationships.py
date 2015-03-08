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

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        UnicodeText, SmallInteger, Unicode)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
import sqlalchemy.sql as sql

from .base import Base


class Relationship(Base):
    __tablename__ = 'rel'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_id = Column(Integer, primary_key=True)

    last_updated = Column(DateTime, nullable=False,
                          server_default=sql.func.now())
    master_revision_id = Column(Integer,
                                ForeignKey('bookbrainz.revision.revision_id'))

    master_revision = relationship(
        'RelationshipRevision', foreign_keys=[master_revision_id],
        post_update=True
    )


class RelationshipType(Base):
    __tablename__ = 'rel_type'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_type_id = Column(Integer, primary_key=True)
    label = Column(Unicode(255), nullable=False, unique=True)

    parent_id = Column(Integer,
                       ForeignKey('bookbrainz.rel_type.relationship_type_id'))
    child_order = Column(Integer, nullable=False, server_default=text('0'))

    description = Column(UnicodeText, nullable=False)
    forward_template = Column(UnicodeText, nullable=False)
    reverse_template = Column(UnicodeText, nullable=False)

    deprecated = Column(Boolean, nullable=False, server_default=sql.false())


class RelationshipTree(Base):
    __tablename__ = 'rel_tree'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_tree_id = Column(Integer, primary_key=True)

    relationship_type_id = Column(
        Integer, ForeignKey('bookbrainz.rel_type.relationship_type_id'),
        nullable=False
    )

    entities = relationship('RelationshipEntity', backref='relationship_tree')
    texts = relationship('RelationshipText', backref='relationship_tree')

    relationship_type = relationship('RelationshipType')


class RelationshipEntity(Base):
    __tablename__ = 'rel_entity'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_tree_id = Column(
        Integer, ForeignKey('bookbrainz.rel_tree.relationship_tree_id'),
        primary_key=True
    )
    position = Column(SmallInteger, primary_key=True)

    entity_gid = Column(
        UUID(as_uuid=True), ForeignKey('bookbrainz.entity.entity_gid'),
        nullable=False
    )

    entity = relationship('Entity')


class RelationshipText(Base):
    __tablename__ = 'rel_text'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_tree_id = Column(
        Integer, ForeignKey('bookbrainz.rel_tree.relationship_tree_id'),
        primary_key=True
    )
    position = Column(SmallInteger, primary_key=True)

    text = Column(UnicodeText, nullable=False)
