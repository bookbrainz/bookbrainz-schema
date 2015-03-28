"""Added user.gender_id FK.

Revision ID: 37754503f344
Revises: 442ccf5568ea
Create Date: 2015-03-28 18:13:33.306339

"""

# revision identifiers, used by Alembic.
revision = '37754503f344'
down_revision = '442ccf5568ea'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_foreign_key(u'user_gender_id_fkey', 'user', 'gender', ['gender_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint(u'user_gender_id_fkey', 'user', schema='bookbrainz', type_='foreignkey')
    ### end Alembic commands ###
