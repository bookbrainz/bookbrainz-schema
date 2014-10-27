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

"""Specifies resources related to space and time - Events and Places."""

from sqlalchemy import (Column, Integer, String, DateTime, UnicodeText,
                        ForeignKey, Boolean, Unicode)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import text

from mbdata.types import Point

from .base import Base
from .resource import Resource


class Place(Resource):
    """A place represents a particular point in the world."""

    __tablename__ = 'place'
    __table_args__ = {'schema': 'bookbrainz'}

    gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.resource.gid'),
                 primary_key=True)

    primary_name = Column(UnicodeText, nullable=False)
    type_id = Column(Integer, ForeignKey('bookbrainz.place_type.id'))

    address = Column(UnicodeText)

    # Unfortunately, because MB uses Integer primary keys, this is an Int FK.
    area_id = Column(Integer, ForeignKey('musicbrainz.area.id'))

    coordinates = Column(Point)

    begin_event_gid = Column(UUID)
    end_event_gid = Column(UUID)

    __mapper_args__ = {
        'polymorphic_identity': 'pla',
    }


class PlaceType(Base):
    """Represents a type of place."""

    __tablename__ = 'place_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)


class Event(Resource):
    """An event represents a particular occaision where something significant
    happened, related to books.
    """

    __tablename__ = 'event'
    __table_args__ = {'schema': 'bookbrainz'}

    gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.resource.gid'),
                 primary_key=True)

    short_description = Column(Unicode(200), nullable=False)

    description = Column(UnicodeText)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    location = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.place.gid'))

    __mapper_args__ = {
        'polymorphic_identity': 'eve',
    }
