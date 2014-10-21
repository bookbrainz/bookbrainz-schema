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

from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, ForeignKey, Boolean, Unicode
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import text

from .base import Base
from .resource import Resource

class Event(Resource)
