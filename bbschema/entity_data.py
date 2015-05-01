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
from bbschema.entity import (Annotation, Disambiguation, Creator, Publication,
                             Publisher, create_aliases, update_aliases)
from bbschema.musicbrainz import Language
from sqlalchemy import (Boolean, Column, Date, Enum, ForeignKey, Integer,
                        SmallInteger, Table, Unicode, UnicodeText,
                        UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

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

ENTITY_DATA__IDENTIFIER = Table(
    'entity_data__identifier', Base.metadata,
    Column(
        'entity_data_id', Integer,
        ForeignKey('bookbrainz.entity_data.entity_data_id'), primary_key=True,
        nullable=False
    ),
    Column(
        'identifier_id', Integer,
        ForeignKey('bookbrainz.identifier.identifier_id'), primary_key=True,
        nullable=False
    ),
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


class Identifier(Base):
    __tablename__ = 'identifier'
    __table_args__ = {'schema': 'bookbrainz'}

    identifier_id = Column(Integer, primary_key=True)
    identifier_type_id = Column(
        Integer, ForeignKey('bookbrainz.identifier_type.identifier_type_id'),
        nullable=False
    )

    value = Column(UnicodeText, nullable=False)

    identifier_type = relationship('IdentifierType')

    @classmethod
    def create(cls, data, session):
        new_identifier = cls()

        new_identifier.identifier_type_id =\
            data.get('identifier_type', {}).get('identifier_type_id')

        new_identifier.value = data.get('value')

        return new_identifier


class IdentifierType(Base):
    __tablename__ = 'identifier_type'
    __table_args__ = {'schema': 'bookbrainz'}

    identifier_type_id = Column(Integer, primary_key=True)
    label = Column(Unicode(255), nullable=False)

    entity_type = Column(
        Enum(
            'Creator', 'Publication', 'Edition', 'Publisher', 'Work',
            name='entity_types'
        ),
        nullable=False
    )

    parent_id = Column(
        Integer, ForeignKey('bookbrainz.identifier_type.identifier_type_id')
    )

    child_order = Column(Integer, nullable=False, server_default=text('0'))
    description = Column(UnicodeText, nullable=False)

    parent = relationship('IdentifierType')

    UniqueConstraint('label', 'entity_type')


class CreatorCredit(Base):
    __tablename__ = 'creator_credit'
    __table_args__ = {'schema': 'bookbrainz'}

    creator_credit_id = Column(Integer, primary_key=True)
    begin_phrase = Column(UnicodeText, nullable=False, server_default='')

    names = relationship('CreatorCreditName', backref='creator_credit')

    @classmethod
    def create(cls, data, session):
        new_credit = cls()

        new_credit.begin_phrase = data.get('begin_phrase', '')

        for name_data in data.get('names', []):
            name = CreatorCreditName.create(name_data, session)

            name.creator_credit_id = new_credit.creator_credit_id
            new_credit.names.append(name)

        return new_credit


class CreatorCreditName(Base):
    __tablename__ = 'creator_credit_name'
    __table_args__ = {'schema': 'bookbrainz'}

    creator_credit_id = Column(
        Integer, ForeignKey('bookbrainz.creator_credit.creator_credit_id'),
        primary_key=True
    )

    position = Column(SmallInteger, primary_key=True, autoincrement=False)

    creator_gid = Column(
        UUID(as_uuid=True), ForeignKey('bookbrainz.entity.entity_gid')
    )

    name = Column(Unicode, nullable=False)
    join_phrase = Column(UnicodeText, nullable=False)

    creator = relationship('Creator')

    @classmethod
    def create(cls, data, session):
        new_name = cls()

        new_name.position = data.get('position')
        new_name.name = data.get('name')
        new_name.join_phrase = data.get('join_phrase')

        creator = session.query(Creator).get(data.get('creator_gid'))
        new_name.creator = creator

        return new_name


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
    aliases = relationship("Alias", secondary=ENTITY_DATA__ALIAS,
                           backref='data')
    default_alias = relationship('Alias', foreign_keys=[default_alias_id])

    identifiers = relationship('Identifier', secondary=ENTITY_DATA__IDENTIFIER,
                               backref='data')

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
    def create(cls, data, session):
        new_data = cls()

        new_data.annotation = Annotation.create(data)
        new_data.disambiguation = Disambiguation.create(data)
        new_data.aliases, default_alias = create_aliases(data)

        if default_alias is not None:
            new_data.default_alias = default_alias

        for identifier_data in data.get('identifiers', []):
            identifier = Identifier.create(identifier_data, session)
            new_data.identifiers.append(identifier)

        return new_data

    def update(self, data, session):
        # Create a new EntityData, copying the current data.
        new_data = self.copy()

        if self.annotation is not None:
            new_data.annotation = self.annotation.update(data)
        else:
            new_data.annotation = Annotation.create(data)

        if self.disambiguation is not None:
            new_data.disambiguation = self.disambiguation.update(data)
        else:
            new_data.disambiguation = Disambiguation.create(data)

        new_data.aliases, default_alias =\
            update_aliases(self.aliases, self.default_alias_id, data)

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
    def create(cls, data, session):
        new_data = super(PublicationData, cls).create(data, session)

        new_data.publication_type_id =\
            data.get('publication_type', {}).get('publication_type_id')

        return new_data

    def update(self, data, session):
        new_data = super(PublicationData, self).update(data, session)

        if (('publication_type' in data) and
                ('publication_type_id' in data['publication_type'])):
            new_data.publication_type_id =\
                data['publication_type']['publication_type_id']

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
    def create(cls, data, session):
        new_data = super(CreatorData, cls).create(data, session)

        new_data.begin_date = data.get('begin_date')
        new_data.begin_date_precision = data.get('begin_date_precision')
        new_data.end_date = data.get('end_date')
        new_data.end_date_precision = data.get('end_date_precision')
        new_data.ended = data.get('ended', False)
        new_data.country_id = data.get('country_id')
        new_data.gender_id = data.get('gender', {}).get('gender_id')
        new_data.creator_type_id =\
            data.get('creator_type', {}).get('creator_type_id')

        return new_data

    def update(self, data, session):
        new_data = super(CreatorData, self).update(data, session)

        if 'begin_date' in data:
            new_data.begin_date = data['begin_date']
        if 'begin_date_precision' in data:
            new_data.begin_date_precision = data['begin_date_precision']
        if 'end_date' in data:
            new_data.end_date = data['end_date']
        if 'end_date_precision' in data:
            new_data.end_date_precision = data['end_date_precision']
        if 'ended' in data:
            new_data.ended = data['ended']
        if 'country_id' in data:
            new_data.country_id = data['country_id']
        if 'gender_id' in data:
            new_data.gender_id = data['gender_id']
        if (('creator_type' in data) and
                ('creator_type_id' in data['creator_type'])):
            new_data.creator_type_id = data['creator_type']['creator_type_id']

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

    def __eq__(self, other):
        if (self.begin_date == other.begin_date and
                self.begin_date_precision == other.begin_date_precision and
                self.end_date == other.end_date and
                self.end_date_precision == other.end_date_precision and
                self.ended == other.ended and
                self.country_id == other.country_id and
                self.publisher_type_id == other.publisher_type_id and
                super(PublisherData, self).__eq__(other)):
            return True

        return False

    @classmethod
    def create(cls, data, session):
        new_data = super(PublisherData, cls).create(data, session)

        new_data.begin_date = data.get('begin_date')
        new_data.begin_date_precision = data.get('begin_date_precision')
        new_data.end_date = data.get('end_date')
        new_data.end_date_precision = data.get('end_date_precision')
        new_data.ended = data.get('ended', False)
        new_data.country_id = data.get('country_id')
        new_data.publisher_type_id =\
            data.get('publisher_type', {}).get('publisher_type_id')

        return new_data

    def update(self, data, session):
        new_data = super(PublisherData, self).update(data, session)

        if 'begin_date' in data:
            new_data.begin_date = data['begin_date']
        if 'begin_date_precision' in data:
            new_data.begin_date_precision = data['begin_date_precision']
        if 'end_date' in data:
            new_data.end_date = data['end_date']
        if 'end_date_precision' in data:
            new_data.end_date_precision = data['end_date_precision']
        if 'ended' in data:
            new_data.ended = data['ended']
        if 'country_id' in data:
            new_data.country_id = data['country_id']
        if (('publisher_type' in data) and
                ('publisher_type_id' in data['publisher_type'])):
            new_data.publisher_type_id =\
                data['publisher_type']['publisher_type_id']

        if new_data == self:
            return self
        else:
            return new_data

    def copy(self):
        copied_data = super(PublisherData, self).copy()

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

    publication_gid = Column(
        UUID(as_uuid=True), ForeignKey(Publication.entity_gid)
    )

    creator_credit_id = Column(
        Integer, ForeignKey('bookbrainz.creator_credit.creator_credit_id')
    )

    release_date = Column(Date)
    release_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )

    # TODO: add script ID, when that's replicated from MB

    country_id = Column(Integer)
    language_id = Column(Integer, ForeignKey('musicbrainz.language.id'))
    edition_format_id = Column(
        Integer, ForeignKey('bookbrainz.edition_format.edition_format_id')
    )
    edition_status_id = Column(
        Integer, ForeignKey('bookbrainz.edition_status.edition_status_id')
    )

    publisher_gid = Column(
        UUID(as_uuid=True), ForeignKey(Publisher.entity_gid)
    )

    publication = relationship('Publication', foreign_keys=[publication_gid])
    creator_credit = relationship('CreatorCredit')
    language = relationship('Language')
    edition_format = relationship('EditionFormat')
    edition_status = relationship('EditionStatus')
    publisher = relationship('Publisher', foreign_keys=[publisher_gid])

    __mapper_args__ = {
        'polymorphic_identity': 4,
    }

    def __eq__(self, other):
        if (self.release_date == other.release_date and
                self.release_date_precision == other.release_date_precision and
                self.country_id == other.country_id and
                self.edition_format_id == other.edition_format_id and
                self.edition_status_id == other.edition_status_id and
                self.language_id == other.language_id and
                super(EditionData, self).__eq__(other)):
            return True

        return False

    @classmethod
    def create(cls, data, session):
        new_data = super(EditionData, cls).create(data, session)

        publication_gid = data.get('publication_gid')
        if publication_gid is None:
            return None

        publication =\
            session.query(Publication).get(data.get('publication_gid'))
        new_data.publication = publication

        new_data.creator_credit =\
            CreatorCredit.create(data.get('creator_credit'), session)

        new_data.release_date = data.get('release_date')
        new_data.release_date_precision = data.get('release_date_precision')
        new_data.country_id = data.get('country_id')
        new_data.language_id =\
            data.get('language', {}).get('language_id')
        new_data.edition_format_id =\
            data.get('edition_format', {}).get('edition_format_id')
        new_data.edition_status_id =\
            data.get('edition_status', {}).get('edition_status_id')

        publisher_gid = data.get('publisher_gid')
        if publisher_gid is not None:
            publisher =\
                session.query(Publisher).get()

            new_data.publisher = publisher

        return new_data

    def update(self, data, session):
        new_data = super(EditionData, self).update(data, session)

        if 'release_date' in data:
            new_data.release_date = data['release_date']
        if 'release_date_precision' in data:
            new_data.release_date_precision = data['release_date_precision']
        if 'country_id' in data:
            new_data.country_id = data['country_id']
        if (('edition_format' in data) and
                ('edition_format' in data['edition_format_id'])):
            new_data.edition_format_id =\
                data['edition_format']['edition_format_id']
        if (('edition_status' in data) and
                ('edition_status' in data['edition_status_id'])):
            new_data.edition_status_id =\
                data['edition_status']['edition_status_id']
        if (('language' in data) and
                ('language_id' in data['language'])):
            new_data.language_id = data['language']['language_id']

        if new_data == self:
            return self
        else:
            return new_data

    def copy(self):
        copied_data = super(EditionData, self).copy()

        copied_data.release_date = self.release_date
        copied_data.release_date_precision = self.release_date_precision
        copied_data.edition_format_id = self.edition_format_id
        copied_data.edition_status_id = self.edition_status_id
        copied_data.country_id = self.country_id
        copied_data.language_id = self.language_id

        return copied_data


class EditionFormat(Base):
    __tablename__ = 'edition_format'
    __table_args__ = {'schema': 'bookbrainz'}

    edition_format_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


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

    def __eq__(self, other):
        if (self.work_type_id == other.work_type_id and
                self.languages == other.languages and
                super(WorkData, self).__eq__(other)):
            return True

        return False

    @classmethod
    def create(cls, data, session):
        new_data = super(WorkData, cls).create(data, session)

        new_data.begin_date = data.get('begin_date')
        new_data.begin_date_precision = data.get('begin_date_precision')
        new_data.end_date = data.get('end_date')
        new_data.end_date_precision = data.get('end_date_precision')
        new_data.ended = data.get('ended', False)
        new_data.country_id = data.get('country_id')
        new_data.language_id = data.get('language_id')
        new_data.work_type_id =\
            data.get('work_type', {}).get('work_type_id')

        for language_data in data.get('languages', []):
            language_id = language_data['language_id']
            language = session.query(Language).get(language_id)
            if language is not None:
                new_data.languages.append(language)

        return new_data

    def update(self, data, session):
        new_data = super(WorkData, self).update(data, session)

        if 'begin_date' in data:
            new_data.begin_date = data['begin_date']
        if 'begin_date_precision' in data:
            new_data.begin_date_precision = data['begin_date_precision']
        if 'end_date' in data:
            new_data.end_date = data['end_date']
        if 'end_date_precision' in data:
            new_data.end_date_precision = data['end_date_precision']
        if 'ended' in data:
            new_data.ended = data['ended']
        if 'country_id' in data:
            new_data.country_id = data['country_id']
        if (('work_type' in data) and
                ('work_type_id' in data['work_type'])):
            new_data.work_type_id = data['work_type']['work_type_id']

        if 'languages' in data:
            languages = data['languages']
            removed_language_ids = [old for old, new in languages if new is None]
            added_language_ids = [new for old, new in languages if old is None]
            new_data.languages = [x for x in new_data.languages if x.language_id not in removed_language_ids]

            for language_id in added_language_ids:
                language = session.query(Language).get(language_id)
                if language is not None:
                    new_data.languages.append(language)

        if new_data == self:
            return self
        else:
            return new_data

    def copy(self):
        copied_data = super(WorkData, self).copy()

        copied_data.work_type_id = self.work_type_id
        copied_data.languages = self.languages

        return copied_data


class WorkType(Base):
    __tablename__ = 'work_type'
    __table_args__ = {'schema': 'bookbrainz'}

    work_type_id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)
