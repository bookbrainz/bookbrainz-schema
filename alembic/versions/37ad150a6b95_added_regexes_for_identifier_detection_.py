"""Added regexes for identifier detection/validation.

Revision ID: 37ad150a6b95
Revises: 4201d7a13b15
Create Date: 2015-05-06 22:46:37.972539

"""

# revision identifiers, used by Alembic.
revision = '37ad150a6b95'
down_revision = '4201d7a13b15'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('identifier_type', sa.Column('detection_regex', sa.UnicodeText(), nullable=True), schema='bookbrainz')
    op.add_column('identifier_type', sa.Column('validation_regex', sa.UnicodeText(), nullable=False), schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_column('identifier_type', 'validation_regex', schema='bookbrainz')
    op.drop_column('identifier_type', 'detection_regex', schema='bookbrainz')
    ### end Alembic commands ###
