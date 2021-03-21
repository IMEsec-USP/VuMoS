#!/bin/bash

echo "Waiting for db..."

until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Migrating " $DB_USER-$DB_NAME
alembic upgrade head
if [ $? -eq 0 ]
then
  echo "Successfully migrated " $DB_USER-$DB_NAME
else
  echo "Error migrating " $DB_USER-$DB_NAME
  exit 1
fi
