"""Added parent to revisions.

Revision ID: 2a9ada265658
Revises: 37bee12cbb98
Create Date: 2015-03-16 22:24:51.006795

"""

# revision identifiers, used by Alembic.
revision = '2a9ada265658'
down_revision = '37bee12cbb98'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('revision', sa.Column('parent_id', sa.Integer(), nullable=True), schema='bookbrainz')
    op.create_foreign_key(None, 'revision', 'revision', ['parent_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint(None, 'revision', schema='bookbrainz', type_='foreignkey')
    op.drop_column('revision', 'parent_id', schema='bookbrainz')
    ### end Alembic commands ###
