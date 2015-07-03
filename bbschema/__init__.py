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

from .base import Base

from .entity import (Entity, EntityRedirect,
                     Annotation, Disambiguation, Alias, Creator, Publication,
                     Edition, Publisher, Work, Identifier, IdentifierType)
from .user import (User, UserType, InactiveUser, SuspendedUser, OAuthClient,
                   Message, MessageReceipt, UserLanguage)
from .entity_data import (EntityData, PublicationData, PublicationType,
                          CreatorData, CreatorType, PublisherData,
                          PublisherType, EditionData, EditionStatus,
                          EditionFormat, WorkData, WorkType, CreatorCredit,
                          CreatorCreditName)
from .musicbrainz import Gender, Language
from .revision import (Revision, EntityRevision, RelationshipRevision,
                       RevisionNote)

from .relationships import (Relationship, RelationshipType, RelationshipData,
                            RelationshipEntity, RelationshipText)


def create_all(engine):
    Base.metadata.create_all(engine)
