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

from sqlalchemy import (Column, Integer, String, DateTime, Unicode, UnicodeText,
                        ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from .base import Base
from .resource import Resource


class Edition(Resource):
    __tablename__ = 'edition'
    __table_args__ = {'schema': 'bookbrainz'}

    gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.resource.gid'),
                 primary_key=True)

    short_description = Column(Unicode(200), nullable=False)

    description = Column(UnicodeText)

    type_id = Column(Integer, ForeignKey('bookbrainz.edition_type.id'))

    work_gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.work.gid'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'edi',
    }


class EditionType(Base):
    __tablename__ = 'edition_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
