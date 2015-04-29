"""Added identifiers, and additional Edition fields.

Revision ID: 5700c3a27fdc
Revises: 37754503f344
Create Date: 2015-04-30 00:39:46.616375

"""

# revision identifiers, used by Alembic.
revision = '5700c3a27fdc'
down_revision = '37754503f344'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

entity_types = postgresql.ENUM('Creator', 'Publication', 'Edition', 'Publisher', 'Work', name='entity_types', create_type=False)

def upgrade():
    op.create_table('creator_credit',
    sa.Column('creator_credit_id', sa.Integer(), nullable=False),
    sa.Column('begin_phrase', sa.UnicodeText(), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('creator_credit_id'),
    schema='bookbrainz'
    )
    op.create_table('identifier_type',
    sa.Column('identifier_type_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.Unicode(length=255), nullable=False),
    sa.Column('entity_type', entity_types, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('child_order', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['bookbrainz.identifier_type.identifier_type_id'], ),
    sa.PrimaryKeyConstraint('identifier_type_id'),
    schema='bookbrainz'
    )
    op.create_table('creator_credit_name',
    sa.Column('creator_credit_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.SmallInteger(), autoincrement=False, nullable=False),
    sa.Column('creator_gid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('name', sa.Unicode(), nullable=False),
    sa.Column('join_phrase', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['creator_credit_id'], ['bookbrainz.creator_credit.creator_credit_id'], ),
    sa.ForeignKeyConstraint(['creator_gid'], ['bookbrainz.entity.entity_gid'], ),
    sa.PrimaryKeyConstraint('creator_credit_id', 'position'),
    schema='bookbrainz'
    )
    op.create_table('identifier',
    sa.Column('identifier_id', sa.Integer(), nullable=False),
    sa.Column('identifier_type_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['identifier_type_id'], ['bookbrainz.identifier_type.identifier_type_id'], ),
    sa.PrimaryKeyConstraint('identifier_id'),
    schema='bookbrainz'
    )
    op.create_table('entity_data__identifier',
    sa.Column('entity_data_id', sa.Integer(), nullable=False),
    sa.Column('identifier_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['entity_data_id'], ['bookbrainz.entity_data.entity_data_id'], ),
    sa.ForeignKeyConstraint(['identifier_id'], ['bookbrainz.identifier.identifier_id'], ),
    sa.PrimaryKeyConstraint('entity_data_id', 'identifier_id'),
    schema='bookbrainz'
    )

    op.add_column(u'edition_data', sa.Column('creator_credit_id', sa.Integer(), nullable=True), schema=u'bookbrainz')
    op.add_column(u'edition_data', sa.Column('publication_gid', postgresql.UUID(as_uuid=True), nullable=False), schema=u'bookbrainz')
    op.add_column(u'edition_data', sa.Column('publisher_gid', postgresql.UUID(as_uuid=True), nullable=True), schema=u'bookbrainz')
    op.create_foreign_key(u'edition_data_creator_credit_id_fkey', 'edition_data', 'creator_credit', ['creator_credit_id'], ['creator_credit_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_publication_gid_fkey', 'edition_data', 'entity', ['publication_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_publisher_gid_fkey', 'edition_data', 'entity', ['publisher_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint(u'edition_data_publisher_gid_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_publication_gid_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_creator_credit_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_column(u'edition_data', 'publisher_gid', schema=u'bookbrainz')
    op.drop_column(u'edition_data', 'publication_gid', schema=u'bookbrainz')
    op.drop_column(u'edition_data', 'creator_credit_id', schema=u'bookbrainz')

    op.drop_table('entity_data__identifier', schema='bookbrainz')
    op.drop_table('identifier', schema='bookbrainz')
    op.drop_table('creator_credit_name', schema='bookbrainz')
    op.drop_table('identifier_type', schema='bookbrainz')
    op.drop_table('creator_credit', schema='bookbrainz')
    ### end Alembic commands ###
