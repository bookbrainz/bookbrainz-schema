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
from sqlalchemy import (Boolean, Column, Date, Enum, ForeignKey, Integer,
                        Table, UnicodeText)
from sqlalchemy.orm import relationship


work_data_language_table = Table(
    'work_data_language', Base.metadata,
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

    entity_data_id = Column(Integer, primary_key=True)

    # For inheritance and url redirection
    _type = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 0,
        'polymorphic_on': _type
    }



def entity_data_from_json(data):
    TYPE_MAP = {
        'publication_data': PublicationData,
        'creator_data': CreatorData
    }

    for k, v in TYPE_MAP.items():
        if k in data:
            return v.from_json(data)


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

    def copy(self):
        return PublicationData(publication_type_id=self.publication_type_id)


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

    def copy(self):
        return CreatorData(
            begin_date=self.begin_date,
            begin_date_precision=self.begin_date_precision,
            end_date=self.end_date,
            end_date_precision=self.end_date_precision,
            ended=self.ended,
            county_id=self.country_id,
            gender_id=self.gender_id,
            creator_type_id=self.creator_type_id
        )


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
        return PublisherData(
            begin_date=self.begin_date,
            begin_date_precision=self.begin_date_precision,
            end_date=self.end_date,
            end_date_precision=self.end_date_precision,
            ended=self.ended,
            country_id=self.country_id,
            publisher_type_id=self.publisher_type_id,
        )


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
        return EditionData(
            begin_date=self.begin_date,
            begin_date_precision=self.begin_date_precision,
            end_date=self.end_date,
            end_date_precision=self.end_date_precision,
            ended=self.ended,
            edition_status_id=self.edition_status_id,
            country_id=self.country_id,
            language_id=self.language_id,
        )


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
    languages = relationship('Language', secondary=work_data_language_table)

    __mapper_args__ = {
        'polymorphic_identity': 5,
    }

    def copy(self):
        result = WorkData(
            work_type_id=self.work_type_id,
        )

        # Copy languages
        result.languages = self.languages

        return result


class WorkType(Base):
    __tablename__ = 'work_type'
    __table_args__ = {'schema': 'bookbrainz'}

    work_type_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)
