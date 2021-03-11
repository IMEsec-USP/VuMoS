#!/bin/bash

until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# while :
# do 
# 	sleep 10000
# done

python -m scrapy crawl sqlsearch -o /dev/stdout:json
# python -m scrapy crawl sqlsearch -o output.json:json
