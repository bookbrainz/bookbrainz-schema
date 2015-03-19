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

import sqlalchemy.orm
import sqlalchemy.sql as sql
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, SmallInteger,
                        Table, UnicodeText)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from .base import Base

from .entity import Entity, create_entity
from .entity_data import create_entity_data


class Revision(Base):
    __tablename__ = 'revision'
    __table_args__ = {'schema': 'bookbrainz'}

    revision_id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                     nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,
                        server_default=sql.func.now())

    parent_id = Column(Integer, ForeignKey('bookbrainz.revision.revision_id'))

    notes = relationship('RevisionNote')
    user = relationship('User', backref='revisions')
    parent = relationship('Revision', backref='children', remote_side=[revision_id])

    _type = Column(SmallInteger, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on': _type
    }


class EntityRevision(Revision):
    __tablename__ = 'entity_revision'
    __table_args__ = {'schema': 'bookbrainz'}

    revision_id = Column(
        Integer, ForeignKey('bookbrainz.revision.revision_id'),
        primary_key=True
    )

    entity_gid = Column(
        UUID(as_uuid=True), ForeignKey('bookbrainz.entity.entity_gid'),
        nullable=False
    )
    entity_data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        nullable=False
    )

    entity = relationship('Entity', foreign_keys=[entity_gid])
    entity_data = relationship('EntityData')

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }

    @classmethod
    def create(cls, user, revision_json):
        entity = create_entity(revision_json)

        if entity is None:
            return None

        entity_data = create_entity_data(revision_json)

        revision = cls()
        revision.user = user
        revision.entity = entity
        revision.entity_data = entity_data

        return revision

    @classmethod
    def update(cls, user, revision_json, session):
        try:
            entity = session.query(Entity).\
                filter_by(entity_gid=revision_json['entity_gid'][0]).one()
        except NoResultFound:
            return None

        if entity.master_revision_id is None:
            return None

        old_data = entity.master_revision.entity_data

        new_data = old_data.update(revision_json)

        if new_data == old_data:
            return None

        revision = cls()
        revision.user = user
        revision.entity = entity
        revision.entity_data = new_data

        return revision


class RelationshipRevision(Revision):
    __tablename__ = 'rel_revision'
    __table_args__ = {'schema': 'bookbrainz'}

    revision_id = Column(
        Integer, ForeignKey('bookbrainz.revision.revision_id'),
        primary_key=True
    )

    relationship_id = Column(
        Integer, ForeignKey('bookbrainz.rel.relationship_id'),
        nullable=False
    )
    relationship_tree_id = Column(
        Integer, ForeignKey('bookbrainz.rel_tree.relationship_tree_id'),
        nullable=False
    )

    relationship = sqlalchemy.orm.relationship('Relationship',
                                               foreign_keys=[relationship_id])
    relationship_tree = sqlalchemy.orm.relationship('RelationshipTree')

    __mapper_args__ = {
        'polymorphic_identity': 2,
    }


class RevisionNote(Base):
    __tablename__ = 'revision_note'
    __table_args__ = {'schema': 'bookbrainz'}

    revision_note_id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                     nullable=False)
    revision_id = Column(
        Integer, ForeignKey('bookbrainz.revision.revision_id'), nullable=False
    )
    content = Column(UnicodeText, nullable=False)
    posted_at = Column(DateTime(timezone=True), nullable=False,
                       server_default=sql.func.now())

    user = relationship('User')
