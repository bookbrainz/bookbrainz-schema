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

from bbschema.base import Base
from bbschema.entity import (Annotation, Disambiguation, create_aliases,
                             update_aliases)
from sqlalchemy import (Boolean, Column, Date, Enum, ForeignKey, Integer,
                        Table, UnicodeText)
from sqlalchemy.orm import relationship

ENTITY_DATA__ALIAS = Table(
    'entity_data__alias', Base.metadata,
    Column(
        'entity_data_id', Integer,
        ForeignKey('bookbrainz.entity_data.entity_data_id'), primary_key=True
    ),
    Column('alias_id', Integer, ForeignKey('bookbrainz.alias.alias_id'),
           primary_key=True),
    schema='bookbrainz'
)

WORK_DATA__LANGUAGE = Table(
    'work_data__language', Base.metadata,
    Column(
        'work_data_id', Integer,
        ForeignKey('bookbrainz.work_data.entity_data_id'), primary_key=True
    ),
    Column(
        'language_id', Integer, ForeignKey('musicbrainz.language.id'),
        primary_key=True
    ),
    schema='bookbrainz'
)


class EntityData(Base):
    __tablename__ = 'entity_data'
    __table_args__ = {'schema': 'bookbrainz'}

    _type = Column(Integer, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on': _type
    }

    entity_data_id = Column(Integer, primary_key=True)

    annotation_id = Column(Integer,
                           ForeignKey('bookbrainz.annotation.annotation_id'))
    disambiguation_id = Column(
        Integer, ForeignKey('bookbrainz.disambiguation.disambiguation_id')
    )
    default_alias_id = Column(Integer, ForeignKey('bookbrainz.alias.alias_id'))

    annotation = relationship('Annotation')
    disambiguation = relationship('Disambiguation')
    aliases = relationship("Alias", secondary=ENTITY_DATA__ALIAS)
    default_alias = relationship('Alias', foreign_keys=[default_alias_id])

    def __eq__(self, other):
        # Assume that other is an EntityData
        for left, right in zip(self.aliases, other.aliases):
            if left != right:
                return False

        return (
            (self.annotation == other.annotation) and
            (self.disambiguation == other.disambiguation) and
            (self.default_alias == other.default_alias)
        )

    @classmethod
    def create(cls, revision_json):
        new_data = cls()

        new_data.annotation = Annotation.create(revision_json)
        new_data.disambiguation = Disambiguation.create(revision_json)
        new_data.aliases, default_alias = create_aliases(revision_json)

        if default_alias is not None:
            new_data.default_alias = default_alias

        return new_data

    def update(self, revision_json):
        # Create a new EntityData, copying the current data.
        new_data = self.copy()

        new_data.annotation = self.annotation.update(revision_json)
        new_data.disambiguation = self.disambiguation.update(revision_json)
        new_data.aliases, default_alias =\
            update_aliases(self.aliases, self.default_alias_id, revision_json)

        if default_alias is not None:
            new_data.default_alias = default_alias

        return new_data

    def copy(self):
        copied_data = type(self)(
            annotation_id=self.annotation_id,
            disambiguation_id=self.disambiguation_id,
            default_alias_id=self.default_alias_id
        )
        copied_data.aliases = self.aliases

        return copied_data


class PublicationData(EntityData):
    __tablename__ = 'publication_data'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        primary_key=True
    )

    publication_type_id = Column(
        Integer, ForeignKey('bookbrainz.publication_type.publication_type_id')
    )

    publication_type = relationship('PublicationType')

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }

    def __eq__(self, other):
        if (self.publication_type_id == other.publication_type_id and
                super(PublicationData, self).__eq__(other)):
            return True

        return False

    @classmethod
    def create(cls, json):
        new_data = super(PublicationData, cls).create(json)

        new_data.publication_type_id = json.get('publication_type', {}).get('publication_type_id')

        return new_data

    def update(self, revision_json):
        new_data = super(PublicationData, self).update(revision_json)

        data_json = revision_json.get('publication_data', {})
        if 'publication_type_id' in data_json:
            new_data.publication_type_id = data_json['publication_type_id']

        if new_data == self:
            return self
        else:
            return new_data

    def copy(self):
        copied_data = super(PublicationData, self).copy()

        copied_data.publication_type_id = self.publication_type_id

        return copied_data


class PublicationType(Base):
    __tablename__ = 'publication_type'
    __table_args__ = {'schema': 'bookbrainz'}

    publication_type_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class CreatorData(EntityData):
    __tablename__ = 'creator_data'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        primary_key=True
    )

    begin_date = Column(Date)
    begin_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    end_date = Column(Date)
    end_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    ended = Column(Boolean, server_default='false')

    country_id = Column(Integer)
    gender_id = Column(Integer, ForeignKey('musicbrainz.gender.id'))
    creator_type_id = Column(
        Integer, ForeignKey('bookbrainz.creator_type.creator_type_id')
    )

    gender = relationship('Gender')
    creator_type = relationship('CreatorType')

    __mapper_args__ = {
        'polymorphic_identity': 2,
    }

    def __eq__(self, other):
        if (self.begin_date == other.begin_date and
                self.begin_date_precision == other.begin_date_precision and
                self.end_date == other.end_date and
                self.end_date_precision == other.end_date_precision and
                self.ended == other.ended and
                self.country_id == other.country_id and
                self.gender_id == other.gender_id and
                self.creator_type_id == other.creator_type_id and
                super(CreatorData, self).__eq__(other)):
            return True

        return False

    @classmethod
    def create(cls, json):
        new_data = super(CreatorData, cls).create(json)

        new_data.begin_date = json.get('begin_date')
        new_data.begin_date_precision = json.get('begin_date_precision')
        new_data.end_date = json.get('end_date')
        new_data.end_date_precision = json.get('end_date_precision')
        new_data.ended = json.get('ended', False)
        new_data.country_id = json.get('country_id')
        new_data.gender_id = json.get('gender.gender_id')
        new_data.creator_type_id = json.get('creator_type', {}).get('creator_type_id')

        return new_data

    def update(self, revision_json):
        new_data = super(CreatorData, self).update(revision_json)

        data_json = revision_json.get('creator_data', {})
        if 'begin_date' in data_json:
            new_data.begin_date = data_json['begin_date']
        if 'begin_date_precision' in data_json:
            new_data.begin_date_precision = data_json['begin_date_precision']
        if 'end_date' in data_json:
            new_data.end_date = data_json['end_date']
        if 'end_date_precision' in data_json:
            new_data.end_date_precision = data_json['end_date_precision']
        if 'ended' in data_json:
            new_data.ended = data_json['ended']
        if 'county_id' in data_json:
            new_data.country_id = data_json['country_id']
        if 'gender_id' in data_json:
            new_data.gender_id = data_json['gender_id']
        if 'creator_type_id' in data_json:
            new_data.creator_type_id = data_json['creator_type_id']

        if new_data == self:
            return self
        else:
            return new_data

    def copy(self):
        copied_data = super(CreatorData, self).copy()

        copied_data.begin_date = self.begin_date,
        copied_data.begin_date_precision = self.begin_date_precision,
        copied_data.end_date = self.end_date,
        copied_data.end_date_precision = self.end_date_precision,
        copied_data.ended = self.ended,
        copied_data.county_id = self.country_id,
        copied_data.gender_id = self.gender_id,
        copied_data.creator_type_id = self.creator_type_id

        return copied_data


class CreatorType(Base):
    __tablename__ = 'creator_type'
    __table_args__ = {'schema': 'bookbrainz'}

    creator_type_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class PublisherData(EntityData):
    __tablename__ = 'publisher_data'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        primary_key=True
    )

    begin_date = Column(Date)
    begin_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    end_date = Column(Date)
    end_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    ended = Column(Boolean, server_default='false')

    country_id = Column(Integer)
    publisher_type_id = Column(
        Integer, ForeignKey('bookbrainz.publisher_type.publisher_type_id')
    )

    publisher_type = relationship('PublisherType')

    __mapper_args__ = {
        'polymorphic_identity': 3,
    }

    def copy(self):
        copied_data = super(CreatorData, self).copy()

        copied_data.begin_date = self.begin_date
        copied_data.begin_date_precision = self.begin_date_precision
        copied_data.end_date = self.end_date
        copied_data.end_date_precision = self.end_date_precision
        copied_data.ended = self.ended
        copied_data.country_id = self.country_id
        copied_data.publisher_type_id = self.publisher_type_id

        return copied_data


class PublisherType(Base):
    __tablename__ = 'publisher_type'
    __table_args__ = {'schema': 'bookbrainz'}

    publisher_type_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class EditionData(EntityData):
    __tablename__ = 'edition_data'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        primary_key=True
    )

    # TODO: Implement creator credits, and add a FK here.

    begin_date = Column(Date)
    begin_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    end_date = Column(Date)
    end_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    ended = Column(Boolean, server_default='false')

    # TODO: add script ID, when that's replicated from MB

    country_id = Column(Integer)
    language_id = Column(Integer, ForeignKey('musicbrainz.language.id'))
    edition_status_id = Column(
        Integer, ForeignKey('bookbrainz.edition_status.edition_status_id')
    )

    language = relationship('Language')
    edition_status = relationship('EditionStatus')

    __mapper_args__ = {
        'polymorphic_identity': 4,
    }

    def copy(self):
        copied_data = super(CreatorData, self).copy()

        copied_data.begin_date = self.begin_date
        copied_data.begin_date_precision = self.begin_date_precision
        copied_data.end_date = self.end_date
        copied_data.end_date_precision = self.end_date_precision
        copied_data.ended = self.ended
        copied_data.edition_status_id = self.edition_status_id
        copied_data.country_id = self.country_id
        copied_data.language_id = self.language_id

        return copied_data


class EditionStatus(Base):
    __tablename__ = 'edition_status'
    __table_args__ = {'schema': 'bookbrainz'}

    edition_status_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class WorkData(EntityData):
    __tablename__ = 'work_data'
    __table_args__ = {'schema': 'bookbrainz'}

    entity_data_id = Column(
        Integer, ForeignKey('bookbrainz.entity_data.entity_data_id'),
        primary_key=True
    )

    work_type_id = Column(Integer,
                          ForeignKey('bookbrainz.work_type.work_type_id'))

    work_type = relationship('WorkType')
    languages = relationship('Language', secondary=WORK_DATA__LANGUAGE)

    __mapper_args__ = {
        'polymorphic_identity': 5,
    }

    def copy(self):
        copied_data = super(CreatorData, self).copy()

        copied_data.work_type_id = self.work_type_id
        copied_data.languages = self.languages

        return copied_data


class WorkType(Base):
    __tablename__ = 'work_type'
    __table_args__ = {'schema': 'bookbrainz'}

    work_type_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)
