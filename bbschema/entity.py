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
from bbschema.base import Base
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        UnicodeText)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text


class Entity(Base):
    """Resource class, from which all other resource models are derived."""

    __tablename__ = 'entity'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_gid = Column(UUID(as_uuid=True), primary_key=True,
                        server_default=text('public.uuid_generate_v4()'))

    last_updated = Column(DateTime, nullable=False,
                          server_default=text("(now() AT TIME ZONE 'UTC')"))
    master_revision_id = Column(
        Integer, ForeignKey('bookbrainz.entity_revision.revision_id',
                            use_alter=True, name='fk_master_revision_id')
    )
    _type = Column(
        Enum(
            'Creator', 'Publication', 'Edition', 'Publisher', 'Work',
            name='entity_types'
        ),
        nullable=False
    )

    master_revision = relationship(
        'EntityRevision', foreign_keys=[master_revision_id], post_update=True
    )

    __mapper_args__ = {
        'polymorphic_on': _type
    }


class Creator(Entity):
    __mapper_args__ = {
        'polymorphic_identity': 'Creator'
    }


class Publication(Entity):
    __mapper_args__ = {
        'polymorphic_identity': 'Publication'
    }


class Edition(Entity):
    __mapper_args__ = {
        'polymorphic_identity': 'Edition'
    }

    publication = relationship(
        'Publication',
        primaryjoin='Edition.master_revision_id == EntityRevision.revision_id',
        secondary='join(EntityRevision, EditionData, EntityRevision.entity_data_id == EditionData.entity_data_id)',
        secondaryjoin='EditionData.publication_gid == Publication.entity_gid',
        backref='editions'
    )


class Publisher(Entity):
    __mapper_args__ = {
        'polymorphic_identity': 'Publisher'
    }


class Work(Entity):
    __mapper_args__ = {
        'polymorphic_identity': 'Work'
    }


class EntityRedirect(Base):
    __tablename__ = 'entity_redirect'
    __table_args__ = {'schema': 'bookbrainz'}

    source_gid = Column(UUID(as_uuid=True), primary_key=True)
    target_gid = Column(
        UUID(as_uuid=True), ForeignKey('bookbrainz.entity.entity_gid'),
        nullable=False
    )


class Annotation(Base):
    __tablename__ = 'annotation'
    __table_args__ = {'schema': 'bookbrainz'}

    annotation_id = Column(Integer, primary_key=True)

    content = Column(UnicodeText, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        server_default=text("(now() AT TIME ZONE 'UTC')"))

    def copy(self):
        return Annotation(content=self.content, created_at=self.created_at)

    @classmethod
    def create(cls, revision_json):
        if (('annotation' not in revision_json) or
                (revision_json['annotation'] is None)):
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
        if (('disambiguation' not in revision_json) or
                (revision_json['disambiguation'] is None)):
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

    def update(self, alias_json):
        new = self.copy()

        if 'name' in alias_json:
            new.name = alias_json['name']
        if 'sort_name' in alias_json:
            new.sort_name = alias_json['sort_name']
        if 'language_id' in alias_json:
            new.language_id = alias_json['language_id']
        if 'primary' in alias_json:
            new.primary = alias_json['primary']

        return new


def create_aliases(revision_json):
    if 'aliases' not in revision_json:
        return ([], None)

    aliases = []
    default_alias = None
    for alias in revision_json['aliases']:
        aliases.append(Alias.create(alias))
        if alias.get('default', False):
            default_alias = aliases[-1]

    return (aliases, default_alias)


def update_aliases(aliases, default_alias_id, revision_json):
    if (('aliases' not in revision_json) or (revision_json['aliases'] is None)):
        return (aliases, None)

    # Create a dictionary, to make it easier look up aliases by ID
    alias_dict = dict((alias.alias_id, alias) for alias in aliases)

    new_aliases = []
    default_alias = None
    for alias_id, alias_json in revision_json['aliases']:
        if alias_json is None:
            del alias_dict[alias_id]
        else:
            if alias_id is None:
                new_aliases.append(Alias.create(alias_json))

                if alias_json.get('default', False):
                    default_alias = new_aliases[-1]
            else:
                alias_dict[alias_id] = alias_dict[alias_id].update(alias_json)
                if alias_json.get('default', False):
                    default_alias = alias_dict[alias_id]

    if default_alias is None:
        default_alias = alias_dict.get(default_alias_id, None)

    return (list(alias_dict.values()) + new_aliases, default_alias)
