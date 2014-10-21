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

"""This module specifies two structures to allow people to modify the data
contained in BookBrainz - Editor and Edit. Editors can make edits, which
are changes to the database."""

from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, ForeignKey, Boolean, Unicode, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import text

from bbschema.base import Base


class Edit(Base):

    __tablename__ = 'edit'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(UUID(as_uuid=True), primary_key=True)

    resource_gid = Column(UUID, ForeignKey('bookbrainz.resource.gid'), nullable=False)
    editor_id = Column(Integer, ForeignKey('bookbrainz.editor.id'), nullable=False)

    start_data = Column(JSON, nullable=False)
    end_data = Column(JSON, nullable=False)

    # Edit is editable by the editor until it gets applied - at which point
    # it will either update the entity or go into the waiting period for
    # approvals.
    applied = Column(Boolean, nullable=False, default=False)


class Editor(Base):

    __tablename__ = 'editor'
    __table_args__ = {'schema': 'bookbrainz'}


    id = Column(Integer, primary_key=True)

    reputation = Column(Integer, nullable=False)

    created = Column(DateTime, nullable=False)

    email = Column(Unicode(255), nullable=False)

    active = Column(Boolean, nullable=False)
    suspended = Column(Boolean, nullable=False)

class EditorLanguage(Base):

    __tablename__ = 'editor_language'
    __table_args__ = {'schema': 'bookbrainz'}

    editor_id = Column(Integer, ForeignKey('bookbrainz.editor.id'), primary_key=True)
    language = Column(Integer, ForeignKey('musicbrainz.language.id'), primary_key=True)
    fluency = Column(Enum('basic', 'intermediate', 'advanced', 'native', name='FLUENCY'), nullable=False)

