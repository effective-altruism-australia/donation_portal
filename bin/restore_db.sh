#!/bin/bash

DB_NAME="donations"
BACKUP_FILE="backup.custom"

# Drop the existing database if it exists
dropdb -h localhost -U postgres $DB_NAME

# Create a new empty database
createdb -h localhost -U postgres $DB_NAME

# Restore the database
pg_restore -v -h localhost -U postgres -d $DB_NAME $BACKUP_FILE

echo "Restore completed for database: $DB_NAME"
