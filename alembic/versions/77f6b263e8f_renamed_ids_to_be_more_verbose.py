"""Renamed IDs to be more verbose

Revision ID: 77f6b263e8f
Revises: 2cdc0539135
Create Date: 2015-03-09 22:02:09.621692

"""

# revision identifiers, used by Alembic.
revision = '77f6b263e8f'
down_revision = '2cdc0539135'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.alter_column('entity_data', 'id', new_column_name='entity_data_id', schema='bookbrainz')
    op.alter_column('rel_type', 'id', new_column_name='relationship_type_id', schema='bookbrainz')
    op.alter_column('user_type', 'id', new_column_name='user_type_id', schema='bookbrainz')
    op.alter_column('edition_status', 'id', new_column_name='edition_status_id', schema='bookbrainz')
    op.alter_column('work_type', 'id', new_column_name='work_type_id', schema='bookbrainz')
    op.alter_column('publication_type', 'id', new_column_name='publication_type_id', schema='bookbrainz')
    op.alter_column('entity', 'gid', new_column_name='entity_gid', schema='bookbrainz')
    op.alter_column('disambiguation', 'id', new_column_name='disambiguation_id', schema='bookbrainz')
    op.alter_column('creator_type', 'id', new_column_name='creator_type_id', schema='bookbrainz')
    op.alter_column('publisher_type', 'id', new_column_name='publisher_type_id', schema='bookbrainz')
    op.alter_column('annotation', 'id', new_column_name='annotation_id', schema='bookbrainz')
    op.alter_column('edition_data', 'id', new_column_name='entity_data_id', schema='bookbrainz')
    op.alter_column('creator_data', 'id', new_column_name='entity_data_id', schema='bookbrainz')
    op.alter_column('rel_tree', 'id', new_column_name='relationship_tree_id', schema='bookbrainz')
    op.alter_column('publisher_data', 'id', new_column_name='entity_data_id', schema='bookbrainz')
    op.alter_column('work_data', 'id', new_column_name='entity_data_id', schema='bookbrainz')
    op.alter_column('alias', 'id', new_column_name='alias_id', schema='bookbrainz')
    op.alter_column('publication_data', 'id', new_column_name='entity_data_id', schema='bookbrainz')
    op.alter_column('user', 'id', new_column_name='user_id', schema='bookbrainz')
    op.alter_column('entity_tree', 'id', new_column_name='entity_tree_id', schema='bookbrainz')
    op.alter_column('revision', 'id', new_column_name='revision_id', schema='bookbrainz')
    op.alter_column('edit', 'id', new_column_name='edit_id', schema='bookbrainz')
    op.alter_column('rel', 'id', new_column_name='relationship_id', schema='bookbrainz')
    op.alter_column('edit_note', 'id', new_column_name='edit_note_id', schema='bookbrainz')
    op.alter_column('entity_revision', 'id', new_column_name='revision_id', schema='bookbrainz')
    op.alter_column('rel_revision', 'id', new_column_name='revision_id', schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.alter_column('entity_data', 'entity_data_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('rel_type', 'relationship_type_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('user_type', 'user_type_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('edition_status', 'edition_status_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('work_type', 'work_type_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('publication_type', 'publication_type_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('entity', 'entity_gid', new_column_name='gid', schema='bookbrainz')
    op.alter_column('disambiguation', 'disambiguation_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('creator_type', 'creator_type_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('publisher_type', 'publisher_type_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('annotation', 'annotation_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('edition_data', 'entity_data_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('creator_data', 'entity_data_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('rel_tree', 'relationship_tree_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('publisher_data', 'entity_data_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('work_data', 'entity_data_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('alias', 'alias_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('publication_data', 'entity_data_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('user', 'user_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('entity_tree', 'entity_tree_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('revision', 'revision_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('edit', 'edit_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('rel', 'relationship_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('edit_note', 'edit_note_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('entity_revision', 'revision_id', new_column_name='id', schema='bookbrainz')
    op.alter_column('rel_revision', 'revision_id', new_column_name='id', schema='bookbrainz')
    ### end Alembic commands ###
