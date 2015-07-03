"""Added physical properties to editions.

Revision ID: 3f104ae31250
Revises: 37ad150a6b95
Create Date: 2015-06-25 12:07:36.389228

"""

# revision identifiers, used by Alembic.
revision = '3f104ae31250'
down_revision = '37ad150a6b95'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('edition_data', sa.Column('depth', sa.Integer(), nullable=True), schema='bookbrainz')
    op.add_column('edition_data', sa.Column('height', sa.Integer(), nullable=True), schema='bookbrainz')
    op.add_column('edition_data', sa.Column('pages', sa.Integer(), nullable=True), schema='bookbrainz')
    op.add_column('edition_data', sa.Column('weight', sa.Integer(), nullable=True), schema='bookbrainz')
    op.add_column('edition_data', sa.Column('width', sa.Integer(), nullable=True), schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_column('edition_data', 'width', schema='bookbrainz')
    op.drop_column('edition_data', 'weight', schema='bookbrainz')
    op.drop_column('edition_data', 'pages', schema='bookbrainz')
    op.drop_column('edition_data', 'height', schema='bookbrainz')
    op.drop_column('edition_data', 'depth', schema='bookbrainz')
    ### end Alembic commands ###
