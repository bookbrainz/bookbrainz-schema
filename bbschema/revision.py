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
from bbschema.base import Base
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, SmallInteger,
                        UnicodeText)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select, text


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
    posted_at = Column(DateTime, nullable=False,
                       server_default=text("(now() AT TIME ZONE 'UTC')"))

    user = relationship('User')


class Revision(Base):
    __tablename__ = 'revision'
    __table_args__ = {'schema': 'bookbrainz'}

    revision_id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('bookbrainz.user.user_id'),
                     nullable=False)
    created_at = Column(DateTime, nullable=False,
                        server_default=text("(now() AT TIME ZONE 'UTC')"))

    parent_id = Column(Integer, ForeignKey('bookbrainz.revision.revision_id'))

    note = sqlalchemy.orm.column_property(
        select([RevisionNote.content]).where(
            RevisionNote.revision_id == revision_id
        ).order_by(RevisionNote.posted_at).limit(1)
    )

    notes = relationship('RevisionNote')
    user = relationship('User', backref='revisions')
    parent = relationship('Revision', backref='children',
                          remote_side=[revision_id])

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
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id')
    )

    entity = relationship('Entity', foreign_keys=[entity_gid],
                          backref='revisions')
    entity_data = relationship('EntityData')

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }


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
    relationship_data_id = Column(
        Integer, ForeignKey('bookbrainz.rel_data.relationship_data_id'),
        nullable=False
    )

    relationship = sqlalchemy.orm.relationship('Relationship',
                                               foreign_keys=[relationship_id])
    relationship_data = sqlalchemy.orm.relationship('RelationshipData')

    __mapper_args__ = {
        'polymorphic_identity': 2,
    }

    @classmethod
    def create(cls, user_id, relationship, relationship_data):
        if relationship is None or relationship_data is None:
            return None

        revision = cls()
        revision.user_id = user_id
        revision.relationship = relationship
        revision.relationship_data = relationship_data

        return revision
