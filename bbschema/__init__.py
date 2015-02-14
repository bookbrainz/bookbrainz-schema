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

from .entity import (Entity, EntityRedirect, EntityTree, EntityData,
                     Annotation, Disambiguation, Alias)
from .user import (User, UserType, InactiveUser, SuspendedUser, EditorStats,
                   OAuthClient)
from .entities import (PublicationData, PublicationType, CreatorData,
                       CreatorType, PublisherData, PublisherType, EditionData,
                       EditionStatus, WorkData, WorkType)
from .versioning import (Edit, Revision, EntityRevision, RelationshipRevision,
                         EditNote)
from .musicbrainz import (Gender, Language)
from .relationships import (Relationship, RelationshipType, RelationshipTree,
                            RelationshipEntity, RelationshipText)

import base


def create_all(engine):
    base.Base.metadata.create_all(engine)
