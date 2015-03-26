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

from .entity import (Entity, EntityRedirect,
                     Annotation, Disambiguation, Alias, Creator, Publication,
                     Edition, Publisher, Work)
from .user import (User, UserType, InactiveUser, SuspendedUser, EditorStats,
                   OAuthClient, Message, MessageReceipt, EditorLanguage)
from .entity_data import (EntityData, PublicationData, PublicationType,
                          CreatorData, CreatorType, PublisherData,
                          PublisherType, EditionData, EditionStatus, WorkData,
                          WorkType)
from .revision import (Revision, EntityRevision, RelationshipRevision,
                       RevisionNote)
from .musicbrainz import (Gender, Language)
from .relationships import (Relationship, RelationshipType, RelationshipData,
                            RelationshipEntity, RelationshipText)

from . import base


def create_all(engine):
    base.Base.metadata.create_all(engine)
