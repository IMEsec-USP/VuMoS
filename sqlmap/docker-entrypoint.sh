#!/bin/bash

echo "Start processing"

echo "Waiting for db..."

until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

