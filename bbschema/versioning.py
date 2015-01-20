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

"""This module specifies two structures to allow people to modify the data
contained in BookBrainz - Editor and Edit. Editors can make edits, which
are changes to the database."""

import sqlalchemy.sql as sql
from bbschema.base import Base
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        SmallInteger, String, Table, Unicode, UnicodeText)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship
import sqlalchemy.orm
from sqlalchemy.sql import text

edit_revision_table = Table(
    'edit_revision', Base.metadata,
    Column('edit_id', Integer, ForeignKey('bookbrainz.edit.id'),
           primary_key=True),
    Column('revision_id', Integer, ForeignKey('bookbrainz.revision.id'),
           primary_key=True),
    schema='bookbrainz'
)


class Edit(Base):
    __tablename__ = 'edit'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('bookbrainz.user.id'), nullable=False)
    status = Column(Integer, nullable=False)

    user = relationship('User', backref='edits')
    edit_notes = relationship('EditNote')
    revisions = relationship('Revision', secondary=edit_revision_table,
                             backref='edits')


class Revision(Base):
    __tablename__ = 'revision'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('bookbrainz.user.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,
                        server_default=sql.func.now())

    user = relationship('User', backref='revisions')

    _type = Column(SmallInteger, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on': _type
    }


class EntityRevision(Revision):
    __tablename__ = 'entity_revision'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.revision.id'),
                primary_key=True)

    entity_gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.entity.gid'),
                        nullable=False)
    entity_tree_id = Column(
        Integer, ForeignKey('bookbrainz.entity_tree.id'), nullable=False
    )

    entity = relationship('Entity', foreign_keys=[entity_gid])
    entity_tree = relationship('EntityTree')

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }


class RelationshipRevision(Revision):
    __tablename__ = 'rel_revision'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.revision.id'),
                primary_key=True)

    relationship_id = Column(Integer, ForeignKey('bookbrainz.rel.id'),
                             nullable=False)
    relationship_tree_id = Column(
        Integer, ForeignKey('bookbrainz.rel_tree.id'), nullable=False
    )

    relationship = sqlalchemy.orm.relationship('Relationship', foreign_keys=[relationship_id])
    relationship_tree = sqlalchemy.orm.relationship('RelationshipTree')

    __mapper_args__ = {
        'polymorphic_identity': 2,
    }


class EditNote(Base):
    __tablename__ = 'edit_note'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('bookbrainz.user.id'),
                     nullable=False)
    edit_id = Column(Integer, ForeignKey('bookbrainz.edit.id'),
                     nullable=False)
    content = Column(UnicodeText, nullable=False)
    posted_at = Column(DateTime(timezone=True), nullable=False,
                       server_default=sql.func.now())

    user = relationship('User')
