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

from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from bbschema.base import Base


class Resource(Base):
    """Resource class, from which all other resource models are derived."""

    __tablename__ = 'resource'
    __table_args__ = {'schema': 'bookbrainz'}

    gid = Column(UUID(as_uuid=True), primary_key=True)

    revision = Column(Integer, nullable=False, server_default=text('1'))

    edits_pending = Column(Integer, nullable=False, server_default=text('0'))

    last_updated = Column(DateTime, nullable=False,
                          server_default=text('(now() AT TIME ZONE \'utc\')'))

    comment = Column(UnicodeText, nullable=False, server_default='')

    # For inheritance and url redirection
    _type = Column(String(3))

    __mapper_args__ = {
        'polymorphic_identity': 'res',
        'polymorphic_on': _type
    }

class ResourceAlias(Base):
    """An alias, or alternative name, for some Resource."""

    __tablename__ = 'resource_alias'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)

    resource_gid = Column(UUID, ForeignKey('bookbrainz.resource.gid'), nullable=False)

    name = Column(UnicodeText, nullable=False)


class ResourceApproval(Base):
    """This class is used when an Editor approves a particular revision of a
    resource. It stores the Editor ID and Resource GID. Revision is not stored,
    because all approvals are cleared when the revision number changes."""

    __tablename__ = 'resource_approval'
    __table_args__ = {'schema': 'bookbrainz'}

    # Composite primary key on resource_gid and editor_id.
    resource_gid = Column(UUID(as_uuid=True), ForeignKey('bookbrainz.resource.gid'),
                          primary_key=True)

    editor_id = Column(Integer, ForeignKey('bookbrainz.editor.id'), primary_key=True)

