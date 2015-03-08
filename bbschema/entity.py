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

"""This module specifies a class, Resource, which is designed to be used as the
base class for all resource models specified in this package."""

import sqlalchemy.sql as sql
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        Table, UnicodeText)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from .base import Base
from .entity_data import entity_data_from_json


class Entity(Base):
    """Resource class, from which all other resource models are derived."""

    __tablename__ = 'entity'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_gid = Column(UUID(as_uuid=True), primary_key=True,
                        server_default=text('public.uuid_generate_v4()'))

    last_updated = Column(DateTime, nullable=False,
                          server_default=sql.func.now())
    master_revision_id = Column(
        Integer, ForeignKey('bookbrainz.entity_revision.revision_id',
                            use_alter=True, name='fk_master_revision_id')
    )

    master_revision = relationship(
        'EntityRevision', foreign_keys=[master_revision_id], post_update=True
    )


class EntityRedirect(Base):
    __tablename__ = 'entity_redirect'
    __table_args__ = {'schema': 'bookbrainz'}

    source_gid = Column(UUID(as_uuid=True), primary_key=True)
    target_gid = Column(
        UUID(as_uuid=True), ForeignKey('bookbrainz.entity.entity_gid'),
        nullable=False
    )


entity_tree_alias = Table(
    'entity_tree_alias', Base.metadata,
    Column(
        'entity_tree_id', Integer,
        ForeignKey('bookbrainz.entity_tree.entity_tree_id'), primary_key=True
    ),
    Column('alias_id', Integer, ForeignKey('bookbrainz.alias.alias_id'),
           primary_key=True),
    schema='bookbrainz'
)


class EntityTree(Base):
    __tablename__ = 'entity_tree'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_tree_id = Column(Integer, primary_key=True)

    annotation_id = Column(Integer,
                           ForeignKey('bookbrainz.annotation.annotation_id'))
    disambiguation_id = Column(
        Integer, ForeignKey('bookbrainz.disambiguation.disambiguation_id')
    )

    data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        nullable=False
    )

    default_alias_id = Column(Integer, ForeignKey('bookbrainz.alias.alias_id'))

    annotation = relationship('Annotation')
    disambiguation = relationship('Disambiguation')
    data = relationship('EntityData')
    aliases = relationship("Alias", secondary=entity_tree_alias)
    default_alias = relationship('Alias', foreign_keys=[default_alias_id])

    def __eq__(self, other):
        # Assume that other is an EntityTree
        for a, b in zip(self.aliases, other.aliases):
            if a != b:
                return False

        return (
            (self.annotation == other.annotation) and
            (self.disambiguation == other.disambiguation) and
            (self.data == other.data) and
            (self.default_alias == other.default_alias)
        )

    def set_default_alias(self, revision_json):
        raise NotImplementedError

    @classmethod
    def create(cls, revision_json):
        result = cls()
        result.data = entity_data_from_json(revision_json)
        result.annotation = Annotation.create(revision_json)
        result.disambiguation = Disambiguation.create(revision_json)
        result.aliases = create_aliases(revision_json)

        if result.aliases:
            result.set_default_alias(revision_json)

    def update(self, revision_json):
        # Create a new tree, copying the current tree.
        new_tree = self.copy()

        # Update the properties with the provided JSON.
        new_tree.data = self.data.update(revision_json)
        new_tree.annotation = self.annotation.update(revision_json)
        new_tree.disambiguation = self.disambiguation.update(revision_json)
        new_tree.aliases = update_aliases(self.aliases, revision_json)

        if new_tree.aliases:
            new_tree.set_default_alias(revision_json)

        # Now, return the new tree if anything was actually updated, or the old
        # tree if not.
        if self == new_tree:
            return self
        else:
            return new_tree

    def copy(self):
        return EntityTree(
            annotation_id=self.annotation_id,
            disambiguation_id=self.disambiguation_id,
            data_id=self.data_id,
            default_alias_id=self.default_alias_id
        )


class Annotation(Base):
    __tablename__ = 'annotation'
    __table_args__ = {'schema': 'bookbrainz'}

    annotation_id = Column(Integer, primary_key=True)

    content = Column(UnicodeText, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        server_default=sql.func.now())

    def copy(self):
        return Annotation(content=self.content, created_at=self.created_at)

    @classmethod
    def create(cls, revision_json):
        if 'annotation' not in revision_json:
            return None

        return cls(content=revision_json['annotation'])

    def update(self, revision_json):
        if 'annotation' not in revision_json:
            return self

        if self.content == revision_json['annotation']:
            return self

        new_annotation = self.copy()
        new_annotation.content = revision_json['annotation']

        return new_annotation


class Disambiguation(Base):
    __tablename__ = 'disambiguation'
    __table_args__ = {'schema': 'bookbrainz'}

    disambiguation_id = Column(Integer, primary_key=True)
    comment = Column(UnicodeText, nullable=False, server_default="")

    def copy(self):
        cls = type(self)
        return cls(comment=self.comment)

    @classmethod
    def create(cls, revision_json):
        if 'disambiguation' not in revision_json:
            return None

        return cls(comment=revision_json['disambiguation'])

    def update(self, revision_json):
        if 'disambiguation' not in revision_json:
            return self

        if self.comment == revision_json['disambiguation']:
            return self

        new_disambiguation = self.copy()
        new_disambiguation.comment = revision_json['disambiguation']

        return new_disambiguation


class Alias(Base):
    """An alias, or alternative name, for some Resource."""

    __tablename__ = 'alias'
    __table_args__ = {'schema': 'bookbrainz'}

    alias_id = Column(Integer, primary_key=True)

    name = Column(UnicodeText, nullable=False)
    sort_name = Column(UnicodeText, nullable=False)

    language_id = Column(Integer, ForeignKey('musicbrainz.language.id'))

    primary = Column(Boolean, nullable=False, server_default=text('false'))

    language = relationship('Language')

    def copy(self):
        return Alias(name=self.name, sort_name=self.sort_name,
                     language_id=self.language_id, primary=self.primary)

    def _update_from_json(self, data):
        self.name = data.get('name') or self.name
        self.sort_name = data.get('sort_name') or self.sort_name
        self.language_id = data.get('language_id') or self.language_id
        self.primary = data.get('primary') or self.primary

    @classmethod
    def create(cls, alias_json):
        return cls(
            name=alias_json['name'],
            sort_name=alias_json['sort_name'],
            language_id=alias_json.get('language_id'),
            primary=alias_json.get('primary', False)
        )


def create_aliases(revision_json):
    if 'aliases' not in revision_json:
        return []

    return [Alias.create(alias) for alias in revision_json['aliases']]


def update_aliases(aliases, revision_json):
    if 'aliases' not in revision_json:
        return aliases

    # Create a dictionary, to make it easier look up aliases by ID
    alias_dict = dict((alias.alias_id, alias) for alias in aliases)

    new_aliases = []
    for alias_id, alias_json in revision_json['aliases']:
        if alias_id is None:
            new_aliases.append(Alias.create(alias_json))
        elif alias_json is None:
            del alias_dict[alias_id]
        else:
            alias_dict[alias_id].update(alias_json)

    return list(alias_dict.values()) + new_aliases
