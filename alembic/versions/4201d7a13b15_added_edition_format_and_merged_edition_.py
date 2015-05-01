"""Added edition format and merged edition begin/end dates.

Revision ID: 4201d7a13b15
Revises: 5700c3a27fdc
Create Date: 2015-05-02 00:30:52.452387

"""

# revision identifiers, used by Alembic.
revision = '4201d7a13b15'
down_revision = '5700c3a27fdc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

date_precision = postgresql.ENUM('YEAR', 'MONTH', 'DAY', name='date_precision', create_type=False)

def upgrade():
    op.create_table('edition_format',
    sa.Column('edition_format_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('edition_format_id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )

    op.alter_column('edition_data', 'begin_date_precision', new_column_name='release_date_precision', schema='bookbrainz')
    op.alter_column('edition_data', 'begin_date', new_column_name='release_date', schema='bookbrainz')

    op.add_column('edition_data', sa.Column('edition_format_id', sa.Integer(), nullable=True), schema='bookbrainz')
    op.create_foreign_key(u'edition_data_edition_format_id_fkey', 'edition_data', 'edition_format', ['edition_format_id'], ['edition_format_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_column('edition_data', 'ended', schema='bookbrainz')
    op.drop_column('edition_data', 'end_date', schema='bookbrainz')
    op.drop_column('edition_data', 'end_date_precision', schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.add_column('edition_data', sa.Column('end_date_precision', date_precision, autoincrement=False, nullable=True), schema='bookbrainz')
    op.add_column('edition_data', sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=True), schema='bookbrainz')
    op.add_column('edition_data', sa.Column('ended', sa.BOOLEAN(), server_default=sa.text(u'false'), autoincrement=False, nullable=True), schema='bookbrainz')

    op.drop_constraint(u'edition_data_edition_format_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_column('edition_data', 'edition_format_id', schema='bookbrainz')

    op.alter_column('edition_data', 'release_date_precision', new_column_name='begin_date_precision', schema='bookbrainz')
    op.alter_column('edition_data', 'release_date', new_column_name='begin_date', schema='bookbrainz')

    op.drop_table('edition_format', schema='bookbrainz')
    ### end Alembic commands ###
