"""Removed user/editor inconsistency.

Revision ID: 442ccf5568ea
Revises: 2e1023fcda0a
Create Date: 2015-03-28 16:20:09.037523

"""

# revision identifiers, used by Alembic.
revision = '442ccf5568ea'
down_revision = '2e1023fcda0a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.rename_table('editor_language', 'user_language', schema='bookbrainz')

    op.drop_table('editor_stats', schema='bookbrainz')

    op.add_column('user', sa.Column('revisions_accepted', sa.Integer(), server_default=sa.text(u'0'), nullable=False), schema='bookbrainz')
    op.add_column('user', sa.Column('revisions_rejected', sa.Integer(), server_default=sa.text(u'0'), nullable=False), schema='bookbrainz')
    op.add_column('user', sa.Column('total_revisions', sa.Integer(), server_default=sa.text(u'0'), nullable=False), schema='bookbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_column('user', 'total_revisions', schema='bookbrainz')
    op.drop_column('user', 'revisions_rejected', schema='bookbrainz')
    op.drop_column('user', 'revisions_accepted', schema='bookbrainz')

    op.create_table('editor_stats',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_edits', sa.INTEGER(), server_default=sa.text(u'0'), autoincrement=False, nullable=False),
    sa.Column('total_revisions', sa.INTEGER(), server_default=sa.text(u'0'), autoincrement=False, nullable=False),
    sa.Column('edits_accepted', sa.INTEGER(), server_default=sa.text(u'0'), autoincrement=False, nullable=False),
    sa.Column('edits_rejected', sa.INTEGER(), server_default=sa.text(u'0'), autoincrement=False, nullable=False),
    sa.Column('edits_failed', sa.INTEGER(), server_default=sa.text(u'0'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], [u'bookbrainz.user.user_id'], name=u'editor_stats_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', name=u'editor_stats_pkey'),
    schema='bookbrainz'
    )

    op.rename_table('user_language', 'editor_language', schema='bookbrainz')
    ### end Alembic commands ###
