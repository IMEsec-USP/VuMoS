#!/bin/bash
cd /home/alembic/

cp alembic/requirements.txt ./requirements.txt

echo "--------------------------"
echo "----- Installing Project Dependencies -----"
if [ -f installed_requirements.txt ]; then
  echo "----- Dependencies previously installed. Checking if we need to install again -----"
  DIFF=$(diff requirements.txt installed_requirements.txt) 
  if [ "$DIFF" != "" ] 
  then
    echo "----- Dependencies modified. Reinstalling -----"
    pip freeze | xargs pip uninstall -y
    pip install -r requirements.txt
    mv requirements.txt installed_requirements.txt
  else
    echo "----- Dependencies not modified -----"
  fi
else
  echo "----- No dependencies previously installed. Installing -----"
  pip install -r requirements.txt
  mv requirements.txt installed_requirements.txt
fi

echo "Start processing"

cd /home/alembic/alembic/

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
