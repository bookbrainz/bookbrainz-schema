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

"""This module provides a class, Entity, to represent people or organizations.
"""

from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from .base import Base
from .resource import Resource


class Entity(Resource):
    """Entity class, representing people and organisations."""

    __tablename__ = 'entity'
    __table_args__ = {'schema': 'bookbrainz'}

    gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.resource.gid'),
                 primary_key=True)

    primary_name = Column(UnicodeText, nullable=False)

    begin_event_gid = Column(UUID, ForeignKey('bookbrainz.event.gid'))
    end_event_gid = Column(UUID, ForeignKey('bookbrainz.event.gid'))

    __mapper_args__ = {
        'polymorphic_identity': 'ent',
    }
