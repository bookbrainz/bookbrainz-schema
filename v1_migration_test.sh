psql -U bookbrainz bookbrainz -c "DROP SCHEMA bookbrainz CASCADE; CREATE SCHEMA bookbrainz AUTHORIZATION bookbrainz;"
psql -U bookbrainz bookbrainz -f ../bookbrainz-sql/schemas/bookbrainz.sql
psql -U bookbrainz bookbrainz -f ../bookbrainz-sql/scripts/create_triggers.sql
psql -U bookbrainz bookbrainz -c "ALTER SCHEMA bookbrainz RENAME TO _bookbrainz; ALTER SCHEMA __bookbrainz RENAME TO bookbrainz;"
./utils/v1_migration.py bookbrainz bookbrainz --password=bookbrainz
psql -U bookbrainz bookbrainz -c "ALTER SCHEMA bookbrainz RENAME TO __bookbrainz; ALTER SCHEMA _bookbrainz RENAME TO bookbrainz;"
