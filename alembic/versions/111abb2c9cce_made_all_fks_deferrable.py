"""Made all FKs deferrable.

Revision ID: 111abb2c9cce
Revises: 1d487ebbd8b5
Create Date: 2015-07-19 10:32:13.328483

"""

# revision identifiers, used by Alembic.
revision = '111abb2c9cce'
down_revision = '1d487ebbd8b5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint(u'alias_language_id_fkey', 'alias', type_='foreignkey')
    op.create_foreign_key(u'alias_language_id_fkey', 'alias', 'language', ['language_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')

    op.drop_constraint(u'creator_credit_name_creator_credit_id_fkey', 'creator_credit_name', type_='foreignkey')
    op.drop_constraint(u'creator_credit_name_creator_gid_fkey', 'creator_credit_name', type_='foreignkey')
    op.create_foreign_key(u'creator_credit_name_creator_credit_id_fkey', 'creator_credit_name', 'creator_credit', ['creator_credit_id'], ['creator_credit_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'creator_credit_name_creator_gid_fkey', 'creator_credit_name', 'entity', ['creator_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'creator_data_id_fkey', 'creator_data', type_='foreignkey')
    op.drop_constraint(u'creator_data_gender_id_fkey', 'creator_data', type_='foreignkey')
    op.drop_constraint(u'creator_data_creator_type_id_fkey', 'creator_data', type_='foreignkey')
    op.create_foreign_key(u'creator_data_creator_type_id_fkey', 'creator_data', 'creator_type', ['creator_type_id'], ['creator_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'creator_data_gender_id_fkey', 'creator_data', 'gender', ['gender_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')
    op.create_foreign_key(u'creator_data_entity_data_id_fkey', 'creator_data', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'edition_data_publisher_gid_fkey', 'edition_data', type_='foreignkey')
    op.drop_constraint(u'edition_data_id_fkey', 'edition_data', type_='foreignkey')
    op.drop_constraint(u'edition_data_language_id_fkey', 'edition_data', type_='foreignkey')
    op.drop_constraint(u'edition_data_creator_credit_id_fkey', 'edition_data', type_='foreignkey')
    op.drop_constraint(u'edition_data_publication_gid_fkey', 'edition_data', type_='foreignkey')
    op.drop_constraint(u'edition_data_edition_status_id_fkey', 'edition_data', type_='foreignkey')
    op.drop_constraint(u'edition_data_edition_format_id_fkey', 'edition_data', type_='foreignkey')
    op.create_foreign_key(u'edition_data_publication_gid_fkey', 'edition_data', 'entity', ['publication_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_edition_status_id_fkey', 'edition_data', 'edition_status', ['edition_status_id'], ['edition_status_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_language_id_fkey', 'edition_data', 'language', ['language_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')
    op.create_foreign_key(u'edition_data_creator_credit_id_fkey', 'edition_data', 'creator_credit', ['creator_credit_id'], ['creator_credit_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_edition_format_id_fkey', 'edition_data', 'edition_format', ['edition_format_id'], ['edition_format_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_entity_data_id_fkey', 'edition_data', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'edition_data_publisher_gid_fkey', 'edition_data', 'entity', ['publisher_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'fk_master_revision_id', 'entity', type_='foreignkey')
    op.create_foreign_key(u'fk_master_revision_id', 'entity', 'entity_revision', ['master_revision_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'entity_data_disambiguation_id_fkey', 'entity_data', type_='foreignkey')
    op.drop_constraint(u'entity_data_default_alias_id_fkey', 'entity_data', type_='foreignkey')
    op.drop_constraint(u'entity_data_annotation_id_fkey', 'entity_data', type_='foreignkey')
    op.create_foreign_key(u'entity_data_annotation_id_fkey', 'entity_data', 'annotation', ['annotation_id'], ['annotation_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_data_disambiguation_id_fkey', 'entity_data', 'disambiguation', ['disambiguation_id'], ['disambiguation_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_data_default_alias_id_fkey', 'entity_data', 'alias', ['default_alias_id'], ['alias_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'entity_data__alias_entity_data_id_fkey', 'entity_data__alias', type_='foreignkey')
    op.drop_constraint(u'entity_data__alias_alias_id_fkey', 'entity_data__alias', type_='foreignkey')
    op.create_foreign_key(u'entity_data__alias_entity_data_id_fkey', 'entity_data__alias', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_data__alias_alias_id_fkey', 'entity_data__alias', 'alias', ['alias_id'], ['alias_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'entity_data__identifier_identifier_id_fkey', 'entity_data__identifier', type_='foreignkey')
    op.drop_constraint(u'entity_data__identifier_entity_data_id_fkey', 'entity_data__identifier', type_='foreignkey')
    op.create_foreign_key(u'entity_data__identifier_identifier_id_fkey', 'entity_data__identifier', 'identifier', ['identifier_id'], ['identifier_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_data__identifier_entity_data_id_fkey', 'entity_data__identifier', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'entity_redirect_target_gid_fkey', 'entity_redirect', type_='foreignkey')
    op.create_foreign_key(u'entity_redirect_target_gid_fkey', 'entity_redirect', 'entity', ['target_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'entity_revision_id_fkey', 'entity_revision', type_='foreignkey')
    op.drop_constraint(u'entity_revision_entity_data_id_fkey', 'entity_revision', type_='foreignkey')
    op.drop_constraint(u'entity_revision_entity_gid_fkey', 'entity_revision', type_='foreignkey')
    op.create_foreign_key(u'entity_revision_revision_id_fkey', 'entity_revision', 'revision', ['revision_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_revision_entity_gid_fkey', 'entity_revision', 'entity', ['entity_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'entity_revision_entity_data_id_fkey', 'entity_revision', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'identifier_identifier_type_id_fkey', 'identifier', type_='foreignkey')
    op.create_foreign_key(u'identifier_identifier_type_id_fkey', 'identifier', 'identifier_type', ['identifier_type_id'], ['identifier_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'identifier_type_parent_id_fkey', 'identifier_type', type_='foreignkey')
    op.create_foreign_key(u'identifier_type_parent_id_fkey', 'identifier_type', 'identifier_type', ['parent_id'], ['identifier_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'inactive_users_user_id_fkey', 'inactive_users', type_='foreignkey')
    op.create_foreign_key(u'inactive_users_user_id_fkey', 'inactive_users', 'user', ['user_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'message_sender_id_fkey', 'message', type_='foreignkey')
    op.create_foreign_key(u'message_sender_id_fkey', 'message', 'user', ['sender_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'message_receipt_message_id_fkey', 'message_receipt', type_='foreignkey')
    op.drop_constraint(u'message_receipt_recipient_id_fkey', 'message_receipt', type_='foreignkey')
    op.create_foreign_key(u'message_receipt_message_id_fkey', 'message_receipt', 'message', ['message_id'], ['message_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'message_receipt_recipient_id_fkey', 'message_receipt', 'user', ['recipient_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'oauth_client_owner_id_fkey', 'oauth_client', type_='foreignkey')
    op.create_foreign_key(u'oauth_client_owner_id_fkey', 'oauth_client', 'user', ['owner_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'publication_data_publication_type_id_fkey', 'publication_data', type_='foreignkey')
    op.drop_constraint(u'publication_data_id_fkey', 'publication_data', type_='foreignkey')
    op.create_foreign_key(u'publication_data_id_fkey', 'publication_data', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'publication_data_publication_type_id_fkey', 'publication_data', 'publication_type', ['publication_type_id'], ['publication_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'publisher_data_id_fkey', 'publisher_data', type_='foreignkey')
    op.drop_constraint(u'publisher_data_publisher_type_id_fkey', 'publisher_data', type_='foreignkey')
    op.create_foreign_key(u'publisher_data_publisher_type_id_fkey', 'publisher_data', 'publisher_type', ['publisher_type_id'], ['publisher_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'publisher_entity_data_id_fkey', 'publisher_data', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'rel_master_revision_id_fkey', 'rel', type_='foreignkey')
    op.create_foreign_key(u'rel_master_revision_id_fkey', 'rel', 'revision', ['master_revision_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'rel_tree_relationship_type_id_fkey', 'rel_data', type_='foreignkey')
    op.create_foreign_key(u'rel_tree_relationship_type_id_fkey', 'rel_data', 'rel_type', ['relationship_type_id'], ['relationship_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'rel_entity_entity_gid_fkey', 'rel_entity', type_='foreignkey')
    op.drop_constraint(u'rel_entity_relationship_tree_id_fkey', 'rel_entity', type_='foreignkey')
    op.create_foreign_key(u'rel_entity_relationship_tree_id_fkey', 'rel_entity', 'rel_data', ['relationship_data_id'], ['relationship_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'rel_entity_entity_gid_fkey', 'rel_entity', 'entity', ['entity_gid'], ['entity_gid'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'rel_revision_relationship_id_fkey', 'rel_revision', type_='foreignkey')
    op.drop_constraint(u'rel_revision_id_fkey', 'rel_revision', type_='foreignkey')
    op.drop_constraint(u'rel_revision_relationship_tree_id_fkey', 'rel_revision', type_='foreignkey')
    op.create_foreign_key(u'rel_revision_relationship_data_id_fkey', 'rel_revision', 'rel_data', ['relationship_data_id'], ['relationship_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'rel_revision_relationship_id_fkey', 'rel_revision', 'rel', ['relationship_id'], ['relationship_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'rel_revision_id_fkey', 'rel_revision', 'revision', ['revision_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'rel_text_relationship_tree_id_fkey', 'rel_text', type_='foreignkey')
    op.create_foreign_key(u'rel_text_relationship_data_id_fkey', 'rel_text', 'rel_data', ['relationship_data_id'], ['relationship_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'rel_type_parent_id_fkey', 'rel_type', type_='foreignkey')
    op.create_foreign_key(u'rel_type_parent_id_fkey', 'rel_type', 'rel_type', ['parent_id'], ['relationship_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'revision_parent_id_fkey', 'revision', type_='foreignkey')
    op.drop_constraint(u'revision_user_id_fkey', 'revision', type_='foreignkey')
    op.create_foreign_key(u'revision_user_id_fkey', 'revision', 'user', ['user_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'revision_parent_id_fkey', 'revision', 'revision', ['parent_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'edit_note_revision_id_fkey', 'revision_note', type_='foreignkey')
    op.drop_constraint(u'edit_note_user_id_fkey', 'revision_note', type_='foreignkey')
    op.create_foreign_key(u'revision_note_user_id_fkey', 'revision_note', 'user', ['user_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'revision_note_revision_id_fkey', 'revision_note', 'revision', ['revision_id'], ['revision_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'suspended_users_user_id_fkey', 'suspended_users', type_='foreignkey')
    op.create_foreign_key(u'suspended_users_user_id_fkey', 'suspended_users', 'user', ['user_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'user_gender_id_fkey', 'user', type_='foreignkey')
    op.drop_constraint(u'user_user_type_id_fkey', 'user', type_='foreignkey')
    op.create_foreign_key(u'user_user_type_id_fkey', 'user', 'user_type', ['user_type_id'], ['user_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'user_gender_id_fkey', 'user', 'gender', ['gender_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')

    op.drop_constraint(u'editor_language_language_id_fkey', 'user_language', type_='foreignkey')
    op.drop_constraint(u'editor_language_user_id_fkey', 'user_language', type_='foreignkey')
    op.create_foreign_key(u'editor_language_user_id_fkey', 'user_language', 'user', ['user_id'], ['user_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'editor_language_language_id_fkey', 'user_language', 'language', ['language_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')

    op.drop_constraint(u'work_data_id_fkey', 'work_data', type_='foreignkey')
    op.drop_constraint(u'work_data_work_type_id_fkey', 'work_data', type_='foreignkey')
    op.create_foreign_key(u'work_data_work_type_id_fkey', 'work_data', 'work_type', ['work_type_id'], ['work_type_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'work_entity_data_id_fkey', 'work_data', 'entity_data', ['entity_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')

    op.drop_constraint(u'work_data_language_work_gid_fkey', 'work_data__language', type_='foreignkey')
    op.drop_constraint(u'work_data_language_language_id_fkey', 'work_data__language', type_='foreignkey')
    op.create_foreign_key(u'work_data_language_work_data_id_fkey', 'work_data__language', 'work_data', ['work_data_id'], ['entity_data_id'], source_schema='bookbrainz', referent_schema='bookbrainz')
    op.create_foreign_key(u'work_data_language_language_id_fkey', 'work_data__language', 'language', ['language_id'], ['id'], source_schema='bookbrainz', referent_schema='musicbrainz')
    ### end Alembic commands ###


def downgrade():
    op.drop_constraint(u'work_data_language_language_id_fkey', 'work_data__language', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'work_data_language_work_data_id_fkey', 'work_data__language', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'work_data_language_language_id_fkey', 'work_data__language', 'language', ['language_id'], ['id'], referent_schema='musicbrainz')
    op.create_foreign_key(u'work_data_language_work_gid_fkey', 'work_data__language', 'work_data', ['work_data_id'], ['entity_data_id'])

    op.drop_constraint(u'work_entity_data_id_fkey', 'work_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'work_data_work_type_id_fkey', 'work_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'work_data_work_type_id_fkey', 'work_data', 'work_type', ['work_type_id'], ['work_type_id'])
    op.create_foreign_key(u'work_data_id_fkey', 'work_data', 'entity_data', ['entity_data_id'], ['entity_data_id'])

    op.drop_constraint(u'editor_language_language_id_fkey', 'user_language', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'editor_language_user_id_fkey', 'user_language', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'editor_language_user_id_fkey', 'user_language', 'user', ['user_id'], ['user_id'])
    op.create_foreign_key(u'editor_language_language_id_fkey', 'user_language', 'language', ['language_id'], ['id'], referent_schema='musicbrainz')

    op.drop_constraint(u'user_gender_id_fkey', 'user', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'user_user_type_id_fkey', 'user', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'user_user_type_id_fkey', 'user', 'user_type', ['user_type_id'], ['user_type_id'])
    op.create_foreign_key(u'user_gender_id_fkey', 'user', 'gender', ['gender_id'], ['id'], referent_schema='musicbrainz')

    op.drop_constraint(u'suspended_users_user_id_fkey', 'suspended_users', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'suspended_users_user_id_fkey', 'suspended_users', 'user', ['user_id'], ['user_id'])

    op.drop_constraint(u'revision_note_revision_id_fkey', 'revision_note', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'revision_note_user_id_fkey', 'revision_note', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'edit_note_user_id_fkey', 'revision_note', 'user', ['user_id'], ['user_id'])
    op.create_foreign_key(u'edit_note_revision_id_fkey', 'revision_note', 'revision', ['revision_id'], ['revision_id'])

    op.drop_constraint(u'revision_parent_id_fkey', 'revision', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'revision_user_id_fkey', 'revision', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'revision_user_id_fkey', 'revision', 'user', ['user_id'], ['user_id'])
    op.create_foreign_key(u'revision_parent_id_fkey', 'revision', 'revision', ['parent_id'], ['revision_id'])

    op.drop_constraint(u'rel_type_parent_id_fkey', 'rel_type', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'rel_type_parent_id_fkey', 'rel_type', 'rel_type', ['parent_id'], ['relationship_type_id'])

    op.drop_constraint(u'rel_text_relationship_data_id_fkey', 'rel_text', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'rel_text_relationship_tree_id_fkey', 'rel_text', 'rel_data', ['relationship_data_id'], ['relationship_data_id'])

    op.drop_constraint(u'rel_revision_id_fkey', 'rel_revision', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'rel_revision_relationship_id_fkey', 'rel_revision', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'rel_revision_relationship_data_id_fkey', 'rel_revision', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'rel_revision_relationship_tree_id_fkey', 'rel_revision', 'rel_data', ['relationship_data_id'], ['relationship_data_id'])
    op.create_foreign_key(u'rel_revision_id_fkey', 'rel_revision', 'revision', ['revision_id'], ['revision_id'])
    op.create_foreign_key(u'rel_revision_relationship_id_fkey', 'rel_revision', 'rel', ['relationship_id'], ['relationship_id'])

    op.drop_constraint(u'rel_entity_entity_gid_fkey', 'rel_entity', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'rel_entity_relationship_tree_id_fkey', 'rel_entity', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'rel_entity_relationship_tree_id_fkey', 'rel_entity', 'rel_data', ['relationship_data_id'], ['relationship_data_id'])
    op.create_foreign_key(u'rel_entity_entity_gid_fkey', 'rel_entity', 'entity', ['entity_gid'], ['entity_gid'])

    op.drop_constraint(u'rel_tree_relationship_type_id_fkey', 'rel_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'rel_tree_relationship_type_id_fkey', 'rel_data', 'rel_type', ['relationship_type_id'], ['relationship_type_id'])

    op.drop_constraint(u'rel_master_revision_id_fkey', 'rel', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'rel_master_revision_id_fkey', 'rel', 'revision', ['master_revision_id'], ['revision_id'])

    op.drop_constraint(u'publisher_entity_data_id_fkey', 'publisher_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'publisher_data_publisher_type_id_fkey', 'publisher_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'publisher_data_publisher_type_id_fkey', 'publisher_data', 'publisher_type', ['publisher_type_id'], ['publisher_type_id'])
    op.create_foreign_key(u'publisher_data_id_fkey', 'publisher_data', 'entity_data', ['entity_data_id'], ['entity_data_id'])

    op.drop_constraint(u'publication_data_publication_type_id_fkey', 'publication_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'publication_data_id_fkey', 'publication_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'publication_data_id_fkey', 'publication_data', 'entity_data', ['entity_data_id'], ['entity_data_id'])
    op.create_foreign_key(u'publication_data_publication_type_id_fkey', 'publication_data', 'publication_type', ['publication_type_id'], ['publication_type_id'])

    op.drop_constraint(u'oauth_client_owner_id_fkey', 'oauth_client', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'oauth_client_owner_id_fkey', 'oauth_client', 'user', ['owner_id'], ['user_id'])

    op.drop_constraint(u'message_receipt_recipient_id_fkey', 'message_receipt', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'message_receipt_message_id_fkey', 'message_receipt', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'message_receipt_recipient_id_fkey', 'message_receipt', 'user', ['recipient_id'], ['user_id'])
    op.create_foreign_key(u'message_receipt_message_id_fkey', 'message_receipt', 'message', ['message_id'], ['message_id'])

    op.drop_constraint(u'message_sender_id_fkey', 'message', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'message_sender_id_fkey', 'message', 'user', ['sender_id'], ['user_id'])

    op.drop_constraint(u'inactive_users_user_id_fkey', 'inactive_users', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'inactive_users_user_id_fkey', 'inactive_users', 'user', ['user_id'], ['user_id'])

    op.drop_constraint(u'identifier_type_parent_id_fkey', 'identifier_type', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'identifier_type_parent_id_fkey', 'identifier_type', 'identifier_type', ['parent_id'], ['identifier_type_id'])

    op.drop_constraint(u'identifier_identifier_type_id_fkey', 'identifier', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'identifier_identifier_type_id_fkey', 'identifier', 'identifier_type', ['identifier_type_id'], ['identifier_type_id'])

    op.drop_constraint(u'entity_revision_entity_data_id_fkey', 'entity_revision', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_revision_entity_gid_fkey', 'entity_revision', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_revision_revision_id_fkey', 'entity_revision', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'entity_revision_entity_gid_fkey', 'entity_revision', 'entity', ['entity_gid'], ['entity_gid'])
    op.create_foreign_key(u'entity_revision_entity_data_id_fkey', 'entity_revision', 'entity_data', ['entity_data_id'], ['entity_data_id'])
    op.create_foreign_key(u'entity_revision_id_fkey', 'entity_revision', 'revision', ['revision_id'], ['revision_id'])

    op.drop_constraint(u'entity_redirect_target_gid_fkey', 'entity_redirect', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'entity_redirect_target_gid_fkey', 'entity_redirect', 'entity', ['target_gid'], ['entity_gid'])

    op.drop_constraint(u'entity_data__identifier_entity_data_id_fkey', 'entity_data__identifier', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_data__identifier_identifier_id_fkey', 'entity_data__identifier', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'entity_data__identifier_entity_data_id_fkey', 'entity_data__identifier', 'entity_data', ['entity_data_id'], ['entity_data_id'])
    op.create_foreign_key(u'entity_data__identifier_identifier_id_fkey', 'entity_data__identifier', 'identifier', ['identifier_id'], ['identifier_id'])

    op.drop_constraint(u'entity_data__alias_alias_id_fkey', 'entity_data__alias', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_data__alias_entity_data_id_fkey', 'entity_data__alias', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'entity_data__alias_alias_id_fkey', 'entity_data__alias', 'alias', ['alias_id'], ['alias_id'])
    op.create_foreign_key(u'entity_data__alias_entity_data_id_fkey', 'entity_data__alias', 'entity_data', ['entity_data_id'], ['entity_data_id'])

    op.drop_constraint(u'entity_data_default_alias_id_fkey', 'entity_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_data_disambiguation_id_fkey', 'entity_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'entity_data_annotation_id_fkey', 'entity_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'entity_data_annotation_id_fkey', 'entity_data', 'annotation', ['annotation_id'], ['annotation_id'])
    op.create_foreign_key(u'entity_data_default_alias_id_fkey', 'entity_data', 'alias', ['default_alias_id'], ['alias_id'])
    op.create_foreign_key(u'entity_data_disambiguation_id_fkey', 'entity_data', 'disambiguation', ['disambiguation_id'], ['disambiguation_id'])

    op.drop_constraint('fk_master_revision_id', 'entity', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'fk_master_revision_id', 'entity', 'entity_revision', ['master_revision_id'], ['revision_id'])

    op.drop_constraint(u'edition_data_publisher_gid_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_entity_data_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_edition_format_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_creator_credit_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_language_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_edition_status_id_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'edition_data_publication_gid_fkey', 'edition_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'edition_data_edition_format_id_fkey', 'edition_data', 'edition_format', ['edition_format_id'], ['edition_format_id'])
    op.create_foreign_key(u'edition_data_edition_status_id_fkey', 'edition_data', 'edition_status', ['edition_status_id'], ['edition_status_id'])
    op.create_foreign_key(u'edition_data_publication_gid_fkey', 'edition_data', 'entity', ['publication_gid'], ['entity_gid'])
    op.create_foreign_key(u'edition_data_creator_credit_id_fkey', 'edition_data', 'creator_credit', ['creator_credit_id'], ['creator_credit_id'])
    op.create_foreign_key(u'edition_data_language_id_fkey', 'edition_data', 'language', ['language_id'], ['id'], referent_schema='musicbrainz')
    op.create_foreign_key(u'edition_data_id_fkey', 'edition_data', 'entity_data', ['entity_data_id'], ['entity_data_id'])
    op.create_foreign_key(u'edition_data_publisher_gid_fkey', 'edition_data', 'entity', ['publisher_gid'], ['entity_gid'])

    op.drop_constraint(u'creator_data_entity_data_id_fkey', 'creator_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'creator_data_gender_id_fkey', 'creator_data', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'creator_data_creator_type_id_fkey', 'creator_data', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'creator_data_creator_type_id_fkey', 'creator_data', 'creator_type', ['creator_type_id'], ['creator_type_id'])
    op.create_foreign_key(u'creator_data_gender_id_fkey', 'creator_data', 'gender', ['gender_id'], ['id'], referent_schema='musicbrainz')
    op.create_foreign_key(u'creator_data_id_fkey', 'creator_data', 'entity_data', ['entity_data_id'], ['entity_data_id'])

    op.drop_constraint(u'creator_credit_name_creator_gid_fkey', 'creator_credit_name', schema='bookbrainz', type_='foreignkey')
    op.drop_constraint(u'creator_credit_name_creator_credit_id_fkey', 'creator_credit_name', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'creator_credit_name_creator_gid_fkey', 'creator_credit_name', 'entity', ['creator_gid'], ['entity_gid'])
    op.create_foreign_key(u'creator_credit_name_creator_credit_id_fkey', 'creator_credit_name', 'creator_credit', ['creator_credit_id'], ['creator_credit_id'])

    op.drop_constraint(u'alias_language_id_fkey', 'alias', schema='bookbrainz', type_='foreignkey')
    op.create_foreign_key(u'alias_language_id_fkey', 'alias', 'language', ['language_id'], ['id'], referent_schema='musicbrainz')
    ### end Alembic commands ###
