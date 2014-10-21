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

"""This module provides classes related to the Work resource."""

from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from .base import Base
from .resource import Resource

class Work(Resource):
    """Work class, representing some work of literature."""

    __tablename__ = 'work'
    __table_args__ = {'schema': 'bookbrainz'}

    gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.resource.gid'),
                 primary_key=True)

    primary_name = Column(UnicodeText, nullable=False)

    type_id = Column(Integer, ForeignKey('bookbrainz.work_type.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'wor',
    }

class WorkType(Base):
    """Class which is used to represent different types of section."""

    __tablename__ = 'work_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)

class WorkWork(Base):
    """Class to represent the relationship between works and subworks."""

    __tablename__ = 'work_work'
    __table_args__ = {'schema': 'bookbrainz'}

    parent_gid = Column(UUID, ForeignKey('bookbrainz.work.gid'), primary_key=True)
    child_gid = Column(UUID, ForeignKey('bookbrainz.work.gid'), primary_key=True)
    position = Column(Integer, primary_key=True)

