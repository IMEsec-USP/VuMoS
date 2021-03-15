#!/bin/sh

# copy all requirements to one file
cp requirements.txt all_requirements.txt
sed -i -e '$a\' all_requirements.txt
cat commons/requirements.txt >> all_requirements.txt

echo "--------------------------"
echo "----- Installing Project Dependencies -----"
if [ -f installed_requirements.txt ]; then
  echo "----- Dependencies previously installed. Checking if we need to install again -----"
  DIFF=$(diff all_requirements.txt installed_requirements.txt) 
  if [ "$DIFF" != "" ] 
  then
    echo "----- Dependencies modified. Reinstalling -----"
    pip freeze | xargs pip uninstall -y
    pip install -r all_requirements.txt
    mv all_requirements.txt installed_requirements.txt
  else
    echo "----- Dependencies not modified -----"
  fi
else
  echo "----- No dependencies previously installed. Installing -----"
  pip install -r all_requirements.txt
  mv all_requirements.txt installed_requirements.txt
fi

until PGPASSWORD=$DB_PASS psql -h "$DB_HOST" -U "postgres" -c '\q';
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Start processing"

python3 main.py
