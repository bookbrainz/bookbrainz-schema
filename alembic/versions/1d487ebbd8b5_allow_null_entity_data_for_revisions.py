"""Allow NULL entity data for revisions.

Revision ID: 1d487ebbd8b5
Revises: d7da5a26973
Create Date: 2015-07-08 14:05:50.704303

"""

# revision identifiers, used by Alembic.
revision = '1d487ebbd8b5'
down_revision = 'd7da5a26973'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(u'entity_revision', 'entity_data_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema=u'bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.alter_column(u'entity_revision', 'entity_data_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema=u'bookbrainz')
    ### end Alembic commands ###
