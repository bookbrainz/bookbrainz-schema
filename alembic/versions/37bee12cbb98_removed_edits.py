"""Removed edits.

Revision ID: 37bee12cbb98
Revises: 24c55a9cb996
Create Date: 2015-03-16 00:59:33.148066

"""

# revision identifiers, used by Alembic.
revision = '37bee12cbb98'
down_revision = '24c55a9cb996'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.rename_table('edit_note', 'revision_note', schema='bookbrainz')
    op.alter_column('revision_note', 'edit_note_id', new_column_name='revision_note_id', schema='bookbrainz')
    op.alter_column('revision_note', 'edit_id', new_column_name='revision_id', schema='bookbrainz')
    op.drop_constraint(u'edit_note_edit_id_fkey', 'revision_note', type_='foreignkey', schema='bookbrainz')
    op.create_foreign_key(u'edit_note_revision_id_fkey', 'revision_note', 'revision', ['revision_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'edit_revision_edit_id_fkey', 'edit_revision', type_='foreignkey', schema='bookbrainz')
    op.drop_table('edit', schema='bookbrainz')
    op.drop_table('edit_revision', schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.create_table('edit',
    sa.Column('edit_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], [u'bookbrainz.user.user_id'], name=u'edit_user_id_fkey'),
    sa.PrimaryKeyConstraint('edit_id', name=u'edit_pkey'),
    schema='bookbrainz'
    )
    op.create_table('edit_revision',
    sa.Column('edit_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('revision_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['edit_id'], [u'bookbrainz.edit.edit_id'], name=u'edit_revision_edit_id_fkey'),
    sa.ForeignKeyConstraint(['revision_id'], [u'bookbrainz.revision.revision_id'], name=u'edit_revision_revision_id_fkey'),
    sa.PrimaryKeyConstraint('edit_id', 'revision_id', name=u'edit_revision_pkey'),
    schema='bookbrainz'
    )

    op.drop_constraint(u'edit_note_revision_id_fkey', 'revision_note', type_='foreignkey', schema='bookbrainz')
    op.create_foreign_key(u'edit_note_edit_id_fkey', 'revision_note', 'edit', ['revision_id'], ['edit_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.alter_column('revision_note', 'revision_id', new_column_name='edit_id', schema='bookbrainz')
    op.alter_column('revision_note', 'revision_note_id', new_column_name='edit_note_id', schema='bookbrainz')
    op.rename_table('revision_note', 'edit_note', schema='bookbrainz')
    ### end Alembic commands ###
