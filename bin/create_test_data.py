import sys
from sqlachemy import session_maker, create_engine

from base import Base

engine = create_engine(sys.argv[1], echo=True)
Base.metadata.bind(engine)

from bbschema import *

Session = session_maker()
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
user1 = User(name="user1", email="user1@users.org", user_type=editor_type)
user2 = User(name="user2", email="user1@users.org", user_type=editor_type)
session.add_all([user1, user2])
session.commit()

# Create an Edit or two
edit1 = Edit(user=user1, status=0)
edit2 = Edit(user=user1, status=0)
session.add_all((edit1, edit2))
session.commit()

# Create some entities (blank master revision for now)
entity1 = Entity()
entity2 = Entity()
entity3 = Entity()
session.add_all((entity1, entity2, entity3))
session.commit()

pub_data1 = PublicationData(publication_type=pub_type)
pub_data2 = PublicationData(publication_type=pub_type)
creator_data = CreatorData(creator_type=creator_type)
session.add_all([pub_data1, pub_data2, creator_data])

entity_tree1 = EntityTree(data=pub_data1)
entity_tree2 = EntityTree(data=pub_data2)
entity_tree3 = EntityTree(data=creator_data)
session.add_all([entity_tree1, entity_tree2, entity_tree3])
session.commit()

# Create some revisions
revision1 = EntityRevision(user=user1, entity_gid=entity1.gid,
                           entity_tree=entity_tree1)
revision2 = EntityRevision(user=user1, entity_gid=entity1.gid,
                           entity_tree=entity_tree2)
revision3 = EntityRevision(user=user1, entity_gid=entity1.gid,
                           entity_tree=entity_tree3)

revision1.edits = [edit1]
revision2.edits = [edit1]
revision3.edits = [edit2]
session.add_all([revision1, revision2, revision3])
session.commit()
