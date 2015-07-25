"""Switched to using mbdata models directly.

Revision ID: d7da5a26973
Revises: 3f104ae31250
Create Date: 2015-07-04 00:11:17.804193

"""

# revision identifiers, used by Alembic.
revision = 'd7da5a26973'
down_revision = '37ad150a6b95'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_constraint(u'gender_parent_id_fkey', 'gender', schema='musicbrainz', type_='foreignkey')
    op.alter_column(u'gender', 'parent_id', new_column_name='parent', schema=u'musicbrainz')
    op.create_foreign_key('gender_fk_parent', 'gender', 'gender', ['parent'], ['id'], source_schema='musicbrainz', referent_schema='musicbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint('gender_fk_parent', 'gender', schema='musicbrainz', type_='foreignkey')
    op.alter_column(u'gender', 'parent', new_column_name='parent_id', schema=u'musicbrainz')
    op.create_foreign_key(u'gender_parent_id_fkey', 'gender', 'gender', ['parent_id'], ['id'], source_schema='musicbrainz', referent_schema='musicbrainz')
    ### end Alembic commands ###
