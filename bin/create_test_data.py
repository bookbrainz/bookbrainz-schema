#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(sys.argv[1], echo=True)

from bbschema import *

Session = sessionmaker(bind=engine)
session = Session()

# Create User, Publication and Creator Types
editor_type = UserType(label='Editor')
session.add(editor_type)
session.commit()

pub_type = PublicationType(label='Book')
session.add(pub_type)
session.commit()

creator_type = CreatorType(label='Author')
session.add(creator_type)
session.commit()

# Create a couple of users
user1 = User(name="user1", email="user1@users.org", user_type_id=editor_type.id)
user2 = User(name="user2", email="user1@users.org", user_type_id=editor_type.id)
session.add_all([user1, user2])
session.commit()

# Create an Edit or two
edit1 = Edit(user_id=user1.id, status=0)
edit2 = Edit(user_id=user1.id, status=0)
session.add_all((edit1, edit2))
session.commit()

# Create some entities (blank master revision for now)
entity1 = Entity()
entity2 = Entity()
entity3 = Entity()
session.add_all((entity1, entity2, entity3))
session.commit()

# Make some data
pub_data1 = PublicationData(publication_type_id=pub_type.id)
pub_data2 = PublicationData(publication_type_id=pub_type.id)
creator_data = CreatorData(creator_type_id=creator_type.id)
session.add_all([pub_data1, pub_data2, creator_data])

entity_tree1 = EntityTree()
entity_tree1.data = pub_data1
entity_tree2 = EntityTree()
entity_tree2.data = pub_data2
entity_tree3 = EntityTree()
entity_tree3.data = creator_data

# Now some aliases, annotations and disambiguations
entity1_alias1 = Alias(name='アウト', sort_name='アウト')
entity1_alias2 = Alias(name='Out', sort_name='Out')
entity1_alias3 = Alias(name='Le quattro casalinghe di Tokyo', sort_name='Le quattro casalinghe di Tokyo')
entity1_alias4 = Alias(name='De nachtploeg', sort_name='De nachtploeg')
entity_tree1.aliases.extend([entity1_alias1, entity1_alias2, entity1_alias3, entity1_alias4])

entity2_alias1 = Alias(name='桐野 夏生', sort_name='桐野 夏生')
entity2_alias2 = Alias(name='Natsuo Kirino', sort_name='Kirino, Natsuo')
entity_tree2.aliases.extend([entity2_alias1, entity2_alias2])

entity3_alias1 = Alias(name='Stephen Snyder', sort_name='Snyder, Stephen')
entity_tree3.aliases.append(entity3_alias1)

# And a disambiguation
entity1_disambig = Disambiguation(comment='book by Natsuo Kirino')
entity_tree1.disambiguation = entity1_disambig

session.add_all([entity_tree1, entity_tree2, entity_tree3])
session.commit()

# Create some revisions
revision1 = EntityRevision(user_id=user1.id, entity_gid=entity1.gid,
                           entity_tree_id=entity_tree1.id)
revision2 = EntityRevision(user_id=user1.id, entity_gid=entity2.gid,
                           entity_tree_id=entity_tree2.id)
revision3 = EntityRevision(user_id=user1.id, entity_gid=entity3.gid,
                           entity_tree_id=entity_tree3.id)

revision1.edits = [edit1]
revision2.edits = [edit1]
revision3.edits = [edit2]

entity1.master_revision = revision1
entity2.master_revision = revision2
entity3.master_revision = revision3
session.add_all([revision1, revision2, revision3])
session.commit()
