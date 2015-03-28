"""Renamed relationship data and added user passwords.

Revision ID: 2e1023fcda0a
Revises: 48f964c7201e
Create Date: 2015-03-28 11:25:55.285196

"""

# revision identifiers, used by Alembic.
revision = '2e1023fcda0a'
down_revision = '48f964c7201e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Rename relationship tree to relationship data
    op.rename_table('rel_tree', 'rel_data', schema='bookbrainz')
    op.alter_column(
        'rel_data', 'relationship_tree_id',
        new_column_name='relationship_data_id', schema='bookbrainz'
    )

    op.alter_column(
        'rel_entity', 'relationship_tree_id',
        new_column_name='relationship_data_id', schema='bookbrainz'
    )

    op.alter_column(
        'rel_revision', 'relationship_tree_id',
        new_column_name='relationship_data_id', schema='bookbrainz'
    )

    op.alter_column(
        'rel_text', 'relationship_tree_id',
        new_column_name='relationship_data_id', schema='bookbrainz'
    )

    # Drop reverse templates
    op.drop_column('rel_type', 'reverse_template', schema='bookbrainz')

    # Add user password field (stores 'bytes' hashes)
    op.add_column('user', sa.Column('password', sa.Text(), nullable=False),
                  schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_column('user', 'password', schema='bookbrainz')

    op.add_column('rel_type', sa.Column('reverse_template', sa.TEXT(),
                  autoincrement=False, nullable=False), schema='bookbrainz')

    op.alter_column(
        'rel_text', 'relationship_data_id',
        new_column_name='relationship_tree_id', schema='bookbrainz'
    )
    op.alter_column(
        'rel_revision', 'relationship_data_id',
        new_column_name='relationship_tree_id', schema='bookbrainz'
    )

    op.alter_column(
        'rel_entity', 'relationship_data_id',
        new_column_name='relationship_tree_id', schema='bookbrainz'
    )

    op.alter_column(
        'rel_data', 'relationship_data_id',
        new_column_name='relationship_tree_id', schema='bookbrainz'
    )

    op.rename_table('rel_data', 'rel_tree', schema='bookbrainz')

    ### end Alembic commands ###
