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
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        SmallInteger, Unicode, UnicodeText)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text


class Relationship(Base):
    __tablename__ = 'rel'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_id = Column(Integer, primary_key=True)

    last_updated = Column(DateTime, nullable=False,
                          server_default=text("(now() AT TIME ZONE 'UTC')"))
    master_revision_id = Column(
        Integer, ForeignKey('bookbrainz.revision.revision_id',
                            deferrable=True)
    )

    master_revision = relationship(
        'RelationshipRevision', foreign_keys=[master_revision_id],
        post_update=True
    )


class RelationshipType(Base):
    __tablename__ = 'rel_type'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_type_id = Column(Integer, primary_key=True)
    label = Column(Unicode(255), nullable=False, unique=True)

    parent_id = Column(
        Integer, ForeignKey('bookbrainz.rel_type.relationship_type_id',
                            deferrable=True)
    )

    child_order = Column(Integer, nullable=False, server_default=text('0'))

    description = Column(UnicodeText, nullable=False)
    template = Column(UnicodeText, nullable=False)

    deprecated = Column(Boolean, nullable=False, server_default=sql.false())


class RelationshipData(Base):
    __tablename__ = 'rel_data'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_data_id = Column(Integer, primary_key=True)

    relationship_type_id = Column(
        Integer, ForeignKey('bookbrainz.rel_type.relationship_type_id',
                            deferrable=True), nullable=False
    )

    entities = relationship('RelationshipEntity', backref='relationship_data')
    texts = relationship('RelationshipText', backref='relationship_data')

    relationship_type = relationship('RelationshipType')

    def diff(self, other):
        other_entities = getattr(other, 'entities', [])
        other_texts = getattr(other, 'texts', [])
        data = {
            'relationship_type': (self.relationship_type,
                                  getattr(other, 'relationship_type', None)),
            'entities': (
                [e for e in self.entities if e not in other_entities],
                [e for e in other_entities if e not in self.entities]
            ),
            'texts': (
                [e for e in self.texts if e not in other_texts],
                [e for e in other_texts if e not in self.texts]
            )
        }

        return {k: v for k, v in data.items() if v[0] != v[1]}


    @classmethod
    def create(cls, data):
        result = cls()

        if (('relationship_type' not in data) or
                ('relationship_type_id' not in data['relationship_type'])):
            return None

        result.relationship_type_id = \
            data['relationship_type']['relationship_type_id']

        for entity in data.get('entities', []):
            if ('entity_gid' not in entity) or ('position' not in entity):
                return None

            rel_entity = RelationshipEntity(entity_gid=entity['entity_gid'],
                                            position=entity['position'])
            result.entities.append(rel_entity)

        for text in data.get('text', []):
            if ('text' not in text) or ('position' not in text):
                return None

            rel_text = RelationshipText(text=text['text'],
                                        position=text['position'])
            result.texts.append(rel_text)

        # A relationship must have at least 2 parts
        if (len(result.entities) + len(result.texts)) < 2:
            return None

        return result


class RelationshipEntity(Base):
    __tablename__ = 'rel_entity'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_data_id = Column(
        Integer, ForeignKey('bookbrainz.rel_data.relationship_data_id',
                            deferrable=True), primary_key=True
    )
    position = Column(SmallInteger, primary_key=True)

    entity_gid = Column(
        UUID(as_uuid=True), ForeignKey('bookbrainz.entity.entity_gid',
                                       deferrable=True), nullable=False
    )

    entity = relationship('Entity')


class RelationshipText(Base):
    __tablename__ = 'rel_text'
    __table_args__ = {'schema': 'bookbrainz'}

    relationship_data_id = Column(
        Integer, ForeignKey('bookbrainz.rel_data.relationship_data_id',
                            deferrable=True), primary_key=True
    )
    position = Column(SmallInteger, primary_key=True)

    text = Column(UnicodeText, nullable=False)
