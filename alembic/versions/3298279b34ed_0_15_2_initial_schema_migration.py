"""0.15.2: Initial schema migration

Revision ID: 3298279b34ed
Revises:
Create Date: 2015-03-13 21:22:59.700995

"""

# revision identifiers, used by Alembic.
revision = '3298279b34ed'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

lang_proficiency = postgresql.ENUM('BASIC', 'INTERMEDIATE', 'ADVANCED', 'NATIVE', name='lang_proficiency', create_type=False)
date_precision = postgresql.ENUM('YEAR', 'MONTH', 'DAY', name='date_precision', create_type=False)

def upgrade():
    lang_proficiency.create(op.get_bind())
    date_precision.create(op.get_bind())
    op.create_table('disambiguation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.UnicodeText(), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('edition_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )
    op.create_table('language',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('iso_code_2t', sa.CHAR(length=3), nullable=True),
    sa.Column('iso_code_2b', sa.CHAR(length=3), nullable=True),
    sa.Column('iso_code_1', sa.CHAR(length=2), nullable=True),
    sa.Column('name', sa.Unicode(length=100), nullable=False),
    sa.Column('frequency', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('iso_code_3', sa.CHAR(length=3), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='musicbrainz'
    )
    op.create_table('work_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )
    op.create_table('entity',
    sa.Column('gid', postgresql.UUID(as_uuid=True), server_default=sa.text(u'public.uuid_generate_v4()'), nullable=False),
    sa.Column('last_updated', sa.DateTime(), server_default=sa.text(u'now()'), nullable=False),
    sa.Column('master_revision_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['master_revision_id'], ['bookbrainz.entity_revision.id'], name='fk_master_revision_id', use_alter=True),
    sa.PrimaryKeyConstraint('gid'),
    schema='bookbrainz'
    )
    op.create_table('entity_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('_type', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('rel_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.Unicode(length=255), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('child_order', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=False),
    sa.Column('forward_template', sa.UnicodeText(), nullable=False),
    sa.Column('reverse_template', sa.UnicodeText(), nullable=False),
    sa.Column('deprecated', sa.Boolean(), server_default=sa.text(u'false'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['bookbrainz.rel_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )
    op.create_table('annotation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.UnicodeText(), server_default='', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text(u'now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('creator_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )
    op.create_table('gender',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('child_order', sa.Integer(), server_default=sa.text(u'0'), nullable=0),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['musicbrainz.gender.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='musicbrainz'
    )
    op.create_table('user_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.Unicode(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('publisher_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )
    op.create_table('publication_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('label'),
    schema='bookbrainz'
    )
    op.create_table('entity_redirect',
    sa.Column('source_gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('target_gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['target_gid'], ['bookbrainz.entity.gid'], ),
    sa.PrimaryKeyConstraint('source_gid'),
    schema='bookbrainz'
    )
    op.create_table('publication_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publication_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.entity_data.id'], ),
    sa.ForeignKeyConstraint(['publication_type_id'], ['bookbrainz.publication_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('creator_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin_date', sa.Date(), nullable=True),
    sa.Column('begin_date_precision', date_precision, nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('end_date_precision', date_precision, nullable=True),
    sa.Column('ended', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('creator_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_type_id'], ['bookbrainz.creator_type.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['musicbrainz.gender.id'], ),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.entity_data.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('publisher_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin_date', sa.Date(), nullable=True),
    sa.Column('begin_date_precision', date_precision, nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('end_date_precision', date_precision, nullable=True),
    sa.Column('ended', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('publisher_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.entity_data.id'], ),
    sa.ForeignKeyConstraint(['publisher_type_id'], ['bookbrainz.publisher_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=64), nullable=False),
    sa.Column('email', sa.Unicode(length=255), nullable=False),
    sa.Column('reputation', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('bio', sa.UnicodeText(), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=False),
    sa.Column('active_at', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=False),
    sa.Column('user_type_id', sa.Integer(), nullable=False),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_type_id'], ['bookbrainz.user_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='bookbrainz'
    )
    op.create_table('alias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.Column('sort_name', sa.UnicodeText(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('primary', sa.Boolean(), server_default=sa.text(u'false'), nullable=False),
    sa.ForeignKeyConstraint(['language_id'], ['musicbrainz.language.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('edition_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin_date', sa.Date(), nullable=True),
    sa.Column('begin_date_precision', date_precision, nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('end_date_precision', date_precision, nullable=True),
    sa.Column('ended', sa.Boolean(), server_default='false', nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('edition_status_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['edition_status_id'], ['bookbrainz.edition_status.id'], ),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.entity_data.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['musicbrainz.language.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('work_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.entity_data.id'], ),
    sa.ForeignKeyConstraint(['work_type_id'], ['bookbrainz.work_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('rel_tree',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('relationship_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['relationship_type_id'], ['bookbrainz.rel_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('editor_stats',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total_edits', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('total_revisions', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('edits_accepted', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('edits_rejected', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.Column('edits_failed', sa.Integer(), server_default=sa.text(u'0'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    schema='bookbrainz'
    )
    op.create_table('revision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=False),
    sa.Column('_type', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('rel_entity',
    sa.Column('relationship_tree_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.SmallInteger(), nullable=False),
    sa.Column('entity_gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['entity_gid'], ['bookbrainz.entity.gid'], ),
    sa.ForeignKeyConstraint(['relationship_tree_id'], ['bookbrainz.rel_tree.id'], ),
    sa.PrimaryKeyConstraint('relationship_tree_id', 'position'),
    schema='bookbrainz'
    )
    op.create_table('work_data_language',
    sa.Column('work_gid', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['language_id'], ['musicbrainz.language.id'], ),
    sa.ForeignKeyConstraint(['work_gid'], ['bookbrainz.work_data.id'], ),
    sa.PrimaryKeyConstraint('work_gid', 'language_id'),
    schema='bookbrainz'
    )
    op.create_table('oauth_client',
    sa.Column('client_id', postgresql.UUID(as_uuid=True), server_default=sa.text(u'public.uuid_generate_v4()'), nullable=False),
    sa.Column('client_secret', postgresql.UUID(as_uuid=True), server_default=sa.text(u'public.uuid_generate_v4()'), nullable=False),
    sa.Column('is_confidential', sa.Boolean(), server_default=sa.text(u'false'), nullable=False),
    sa.Column('_redirect_uris', sa.UnicodeText(), server_default='', nullable=False),
    sa.Column('_default_scopes', sa.UnicodeText(), server_default='', nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('client_id'),
    schema='bookbrainz'
    )
    op.create_index(op.f('ix_bookbrainz_oauth_client_client_secret'), 'oauth_client', ['client_secret'], unique=True, schema='bookbrainz')
    op.create_table('editor_language',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('proficiency', lang_proficiency, nullable=False),
    sa.ForeignKeyConstraint(['language_id'], ['musicbrainz.language.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'language_id'),
    schema='bookbrainz'
    )
    op.create_table('entity_tree',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('annotation_id', sa.Integer(), nullable=True),
    sa.Column('disambiguation_id', sa.Integer(), nullable=True),
    sa.Column('data_id', sa.Integer(), nullable=False),
    sa.Column('default_alias_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['annotation_id'], ['bookbrainz.annotation.id'], ),
    sa.ForeignKeyConstraint(['data_id'], ['bookbrainz.entity_data.id'], ),
    sa.ForeignKeyConstraint(['default_alias_id'], ['bookbrainz.alias.id'], ),
    sa.ForeignKeyConstraint(['disambiguation_id'], ['bookbrainz.disambiguation.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('suspended_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    schema='bookbrainz'
    )
    op.create_table('message',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('subject', sa.Unicode(length=255), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['sender_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('message_id'),
    schema='bookbrainz'
    )
    op.create_table('inactive_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    schema='bookbrainz'
    )
    op.create_table('edit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('rel_text',
    sa.Column('relationship_tree_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.SmallInteger(), nullable=False),
    sa.Column('text', sa.UnicodeText(), nullable=False),
    sa.ForeignKeyConstraint(['relationship_tree_id'], ['bookbrainz.rel_tree.id'], ),
    sa.PrimaryKeyConstraint('relationship_tree_id', 'position'),
    schema='bookbrainz'
    )
    op.create_table('entity_revision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity_gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('entity_tree_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['entity_gid'], ['bookbrainz.entity.gid'], ),
    sa.ForeignKeyConstraint(['entity_tree_id'], ['bookbrainz.entity_tree.id'], ),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.revision.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('entity_tree_alias',
    sa.Column('entity_tree_id', sa.Integer(), nullable=False),
    sa.Column('alias_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['alias_id'], ['bookbrainz.alias.id'], ),
    sa.ForeignKeyConstraint(['entity_tree_id'], ['bookbrainz.entity_tree.id'], ),
    sa.PrimaryKeyConstraint('entity_tree_id', 'alias_id'),
    schema='bookbrainz'
    )
    op.create_table('edit_revision',
    sa.Column('edit_id', sa.Integer(), nullable=False),
    sa.Column('revision_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['edit_id'], ['bookbrainz.edit.id'], ),
    sa.ForeignKeyConstraint(['revision_id'], ['bookbrainz.revision.id'], ),
    sa.PrimaryKeyConstraint('edit_id', 'revision_id'),
    schema='bookbrainz'
    )
    op.create_table('message_receipt',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['bookbrainz.message.message_id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('message_id', 'recipient_id'),
    schema='bookbrainz'
    )
    op.create_table('rel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), server_default=sa.text(u'now()'), nullable=False),
    sa.Column('master_revision_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['master_revision_id'], ['bookbrainz.revision.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('edit_note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('edit_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=False),
    sa.Column('posted_at', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=False),
    sa.ForeignKeyConstraint(['edit_id'], ['bookbrainz.edit.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['bookbrainz.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    op.create_table('rel_revision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('relationship_id', sa.Integer(), nullable=False),
    sa.Column('relationship_tree_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['bookbrainz.revision.id'], ),
    sa.ForeignKeyConstraint(['relationship_id'], ['bookbrainz.rel.id'], ),
    sa.ForeignKeyConstraint(['relationship_tree_id'], ['bookbrainz.rel_tree.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='bookbrainz'
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rel_revision', schema='bookbrainz')
    op.drop_table('edit_note', schema='bookbrainz')
    op.drop_table('rel', schema='bookbrainz')
    op.drop_table('message_receipt', schema='bookbrainz')
    op.drop_table('edit_revision', schema='bookbrainz')
    op.drop_table('entity_tree_alias', schema='bookbrainz')
    op.drop_table('entity_revision', schema='bookbrainz')
    op.drop_table('rel_text', schema='bookbrainz')
    op.drop_table('edit', schema='bookbrainz')
    op.drop_table('inactive_users', schema='bookbrainz')
    op.drop_table('message', schema='bookbrainz')
    op.drop_table('suspended_users', schema='bookbrainz')
    op.drop_table('entity_tree', schema='bookbrainz')
    op.drop_table('editor_language', schema='bookbrainz')
    op.drop_index(op.f('ix_bookbrainz_oauth_client_client_secret'), table_name='oauth_client', schema='bookbrainz')
    op.drop_table('oauth_client', schema='bookbrainz')
    op.drop_table('work_data_language', schema='bookbrainz')
    op.drop_table('rel_entity', schema='bookbrainz')
    op.drop_table('revision', schema='bookbrainz')
    op.drop_table('editor_stats', schema='bookbrainz')
    op.drop_table('rel_tree', schema='bookbrainz')
    op.drop_table('work_data', schema='bookbrainz')
    op.drop_table('edition_data', schema='bookbrainz')
    op.drop_table('alias', schema='bookbrainz')
    op.drop_table('user', schema='bookbrainz')
    op.drop_table('publisher_data', schema='bookbrainz')
    op.drop_table('creator_data', schema='bookbrainz')
    op.drop_table('publication_data', schema='bookbrainz')
    op.drop_table('entity_redirect', schema='bookbrainz')
    op.drop_table('publication_type', schema='bookbrainz')
    op.drop_table('publisher_type', schema='bookbrainz')
    op.drop_table('user_type', schema='bookbrainz')
    op.drop_table('gender', schema='musicbrainz')
    op.drop_table('creator_type', schema='bookbrainz')
    op.drop_table('annotation', schema='bookbrainz')
    op.drop_table('rel_type', schema='bookbrainz')
    op.drop_table('entity_data', schema='bookbrainz')
    op.drop_table('entity', schema='bookbrainz')
    op.drop_table('work_type', schema='bookbrainz')
    op.drop_table('language', schema='musicbrainz')
    op.drop_table('edition_status', schema='bookbrainz')
    op.drop_table('disambiguation', schema='bookbrainz')
    lang_proficiency.drop(op.get_bind())
    date_precision.drop(op.get_bind())
    ### end Alembic commands ###
