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

from .entity import EntityData

work_data_language_table = Table(
    'work_data_language', Base.metadata,
    Column('work_gid', Integer, ForeignKey('bookbrainz.work_data.id'),
           primary_key=True),
    Column('language_id', Integer, ForeignKey('musicbrainz.language.id'),
           primary_key=True),
    schema='bookbrainz'
)


class PublicationData(EntityData):
    __tablename__ = 'publication_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'),
                primary_key=True)
    publication_type_id = Column(Integer,
                                 ForeignKey('bookbrainz.publication_type.id'))

    publication_type = relationship('PublicationType')

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }

    @classmethod
    def copy(cls, other):
        return cls(publication_type_id=other.publication_type_id)


class PublicationType(Base):
    __tablename__ = 'publication_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class CreatorData(EntityData):
    __tablename__ = 'creator_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'),
                primary_key=True)

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
    creator_type_id = Column(Integer, ForeignKey('bookbrainz.creator_type.id'))

    gender = relationship('Gender')
    creator_type = relationship('CreatorType')

    __mapper_args__ = {
        'polymorphic_identity': 2,
    }

    @classmethod
    def copy(cls, other):
        return cls(
            begin_date=other.begin_date,
            begin_date_precision=other.begin_date_precision,
            end_date=other.end_date,
            end_date_precision=other.end_date_precision,
            ended=other.ended,
            county_id=other.country_id,
            gender_id=other.gender_id,
            creator_type_id=other.creator_type_id
        )


class CreatorType(Base):
    __tablename__ = 'creator_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class PublisherData(EntityData):
    __tablename__ = 'publisher_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'),
                primary_key=True)

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
    publisher_type_id = Column(Integer,
                               ForeignKey('bookbrainz.publisher_type.id'))

    publisher_type = relationship('PublisherType')

    __mapper_args__ = {
        'polymorphic_identity': 3,
    }

    @classmethod
    def copy(cls, other):
        return cls(
            begin_date=other.begin_date,
            begin_date_precision=other.begin_date_precision,
            end_date=other.end_date,
            end_date_precision=other.end_date_precision,
            ended=other.ended,
            country_id=other.country_id,
            publisher_type_id=other.publisher_type_id,
        )


class PublisherType(Base):
    __tablename__ = 'publisher_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class EditionData(EntityData):
    __tablename__ = 'edition_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'),
                primary_key=True)

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
    edition_status_id = Column(Integer,
                               ForeignKey('bookbrainz.edition_status.id'))

    language = relationship('Language')
    edition_status = relationship('PublisherType')

    __mapper_args__ = {
        'polymorphic_identity': 4,
    }

    @classmethod
    def copy(cls, other):
        return cls(
            begin_date=other.begin_date,
            begin_date_precision=other.begin_date_precision,
            end_date=other.end_date,
            end_date_precision=other.end_date_precision,
            ended=other.ended,
            edition_status_id=other.edition_status_id,
            country_id=other.country_id,
            language_id=other.language_id,
        )


class EditionStatus(Base):
    __tablename__ = 'edition_status'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class WorkData(EntityData):
    __tablename__ = 'work_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'),
                primary_key=True)

    work_type_id = Column(Integer, ForeignKey('bookbrainz.work_type.id'))

    work_type = relationship('WorkType')
    languages = relationship('Language', secondary=work_data_language_table)

    __mapper_args__ = {
        'polymorphic_identity': 5,
    }

    @classmethod
    def copy(cls, other):
        result = cls(
            work_type_id=other.work_type_id,
        )

        # Copy languages
        result.languages = other.languages

        return result


class WorkType(Base):
    __tablename__ = 'work_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)
