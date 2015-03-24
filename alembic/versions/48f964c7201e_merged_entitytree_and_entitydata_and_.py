"""Merged EntityTree and EntityData, and changed relationship template field.

Revision ID: 48f964c7201e
Revises: 2a9ada265658
Create Date: 2015-03-24 21:26:47.943978

"""

# revision identifiers, used by Alembic.
revision = '48f964c7201e'
down_revision = '2a9ada265658'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

entity_types = postgresql.ENUM('Creator', 'Publication', 'Edition', 'Publisher', 'Work', name='entity_types', create_type=False)

def upgrade():
    entity_types.create(op.get_bind())
    op.rename_table('work_data_language', 'work_data__language', schema='bookbrainz')
    op.add_column('entity', sa.Column('_type', entity_types, nullable=False), schema='bookbrainz')

    # EntityTree -> Entity
    op.create_table('entity_data__alias',
    sa.Column('entity_data_id', sa.Integer(), nullable=False),
    sa.Column('alias_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['alias_id'], ['bookbrainz.alias.alias_id'], ),
    sa.ForeignKeyConstraint(['entity_data_id'], ['bookbrainz.entity_data.entity_data_id'], ),
    sa.PrimaryKeyConstraint('entity_data_id', 'alias_id'),
    schema='bookbrainz'
    )
    op.drop_table('entity_tree_alias', schema='bookbrainz')

    op.drop_constraint(u'entity_revision_entity_tree_id_fkey', 'entity_revision', schema='bookbrainz', type_='foreignkey')
    op.drop_table('entity_tree', schema='bookbrainz')

    op.add_column('entity_data', sa.Column('annotation_id', sa.Integer(), nullable=True), schema='bookbrainz')
    op.add_column('entity_data', sa.Column('default_alias_id', sa.Integer(), nullable=True), schema='bookbrainz')
    op.add_column('entity_data', sa.Column('disambiguation_id', sa.Integer(), nullable=True), schema='bookbrainz')
    op.create_foreign_key(u'entity_data_annotation_id_fkey', 'entity_data', 'annotation', ['annotation_id'], ['annotation_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_data_disambiguation_id_fkey', 'entity_data', 'disambiguation', ['disambiguation_id'], ['disambiguation_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_data_default_alias_id_fkey', 'entity_data', 'alias', ['default_alias_id'], ['alias_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.add_column('entity_revision', sa.Column('entity_data_id', sa.Integer(), nullable=False), schema='bookbrainz')
    op.create_foreign_key(u'entity_revision_entity_data_id_fkey', 'entity_revision', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.drop_column('entity_revision', 'entity_tree_id', schema='bookbrainz')
    op.alter_column('rel_type', 'forward_template', new_column_name='template', schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.alter_column('rel_type', 'template', new_column_name='forward_template', schema='bookbrainz')

    op.add_column('entity_revision', sa.Column('entity_tree_id', sa.INTEGER(), autoincrement=False, nullable=False), schema='bookbrainz')
    op.drop_constraint(u'entity_revision_entity_data_id_fkey', 'entity_revision', schema='bookbrainz', type_='foreignkey')
    op.drop_column('entity_revision', 'entity_data_id', schema='bookbrainz')
    op.drop_constraint(u'entity_data_default_alias_id_fkey', 'entity_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_data_disambiguation_id_fkey', 'entity_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_data_annotation_id_fkey', 'entity_data', schema='bookbrainz', type_='foreignkey')
    op.drop_column('entity_data', 'disambiguation_id', schema='bookbrainz')
    op.drop_column('entity_data', 'default_alias_id', schema='bookbrainz')
    op.drop_column('entity_data', 'annotation_id', schema='bookbrainz')
    op.drop_column('entity', '_type', schema='bookbrainz')

    op.create_table('entity_tree',
    sa.Column('entity_tree_id', sa.INTEGER(), nullable=False),
    sa.Column('annotation_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('disambiguation_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('data_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('default_alias_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['annotation_id'], [u'bookbrainz.annotation.annotation_id'], name=u'entity_tree_annotation_id_fkey'),
    sa.ForeignKeyConstraint(['data_id'], [u'bookbrainz.entity_data.entity_data_id'], name=u'entity_tree_data_id_fkey'),
    sa.ForeignKeyConstraint(['default_alias_id'], [u'bookbrainz.alias.alias_id'], name=u'entity_tree_default_alias_id_fkey'),
    sa.ForeignKeyConstraint(['disambiguation_id'], [u'bookbrainz.disambiguation.disambiguation_id'], name=u'entity_tree_disambiguation_id_fkey'),
    sa.PrimaryKeyConstraint('entity_tree_id', name=u'entity_tree_pkey'),
    schema='bookbrainz',
    postgresql_ignore_search_path=False
    )
    op.create_foreign_key(u'entity_revision_entity_tree_id_fkey', 'entity_revision', 'entity_tree', ['entity_tree_id'], ['entity_tree_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.create_table('entity_tree_alias',
    sa.Column('entity_tree_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('alias_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['alias_id'], [u'bookbrainz.alias.alias_id'], name=u'entity_tree_alias_alias_id_fkey'),
    sa.ForeignKeyConstraint(['entity_tree_id'], [u'bookbrainz.entity_tree.entity_tree_id'], name=u'entity_tree_alias_entity_tree_id_fkey'),
    sa.PrimaryKeyConstraint('entity_tree_id', 'alias_id', name=u'entity_tree_alias_pkey'),
    schema='bookbrainz'
    )
    op.drop_table('entity_data__alias', schema='bookbrainz')

    op.rename_table('work_data__language', 'work_data_language', schema='bookbrainz')
    entity_types.drop(op.get_bind())
    ### end Alembic commands ###
