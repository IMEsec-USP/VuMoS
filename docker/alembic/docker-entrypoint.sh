#!/bin/bash
echo "----- Image version: -----"
cat ../version.txt
echo "--------------------------"
echo "----- Installing Project Dependencies -----"
if [ ! -d lib ]; then
  mkdir lib
fi

# requirements.txt is only available in dev environment. In prod we just skip this
if [ -f requirements.txt ]; then
  cd lib
  if [ -f requirements.txt ];then
    rm requirements.txt
  fi
  cp ../requirements.txt .

  if [ -f installed_requirements.txt ]; then
    echo "----- Dependencies previously installed. Checking if we need to install again -----"
    DIFF=$(diff requirements.txt installed_requirements.txt) 
    if [ "$DIFF" != "" ] 
    then
      echo "----- Dependencies modified. Reinstalling -----"
	  rm -rf *
	  cp ../requirements.txt .
	  pip install -r requirements.txt -t . --extra-index-url=https://pip.e-deploy.com.br --cache-dir=/var/cache/pip || exit 1
	  mv requirements.txt installed_requirements.txt
    else
      echo "----- Dependencies not modified -----"
    fi
  else
    echo "----- No dependencies previously installed. Installing -----"
    pip install -r requirements.txt -t . --extra-index-url=https://pip.e-deploy.com.br --cache-dir=/var/cache/pip || exit 1
    mv requirements.txt installed_requirements.txt
  fi
  cd ..
else
  echo "----- Production environment, libraries already installed -----"
fi

if [ ! -z $LOG_CONFIG_JSON_BASE64 ];then
  echo $LOG_CONFIG_JSON_BASE64 | base64 -d > ./config/log-config.json
fi

echo "Start processing"
IFS=';' read -r -a ALL_CLIENT_DB_INFO_ARRAY <<< "$ALL_CLIENT_DB_INFO"
for CLIENT_INFO in "${ALL_CLIENT_DB_INFO_ARRAY[@]}"
do
  echo "Processing client"
  IFS=',' read -r -a DB_INFO <<< "$CLIENT_INFO"
  export DB_HOST=${DB_INFO[0]}
  export DB_PORT=${DB_INFO[1]}
  export DB_USER=${DB_INFO[2]}
  export DB_PASS=${DB_INFO[3]}
  export DB_NAME=${DB_INFO[4]}
  echo "Migrating " $DB_USER-$DB_NAME
  alembic --config ./config/alembic.ini upgrade head
  if [ $? -eq 0 ]
  then
    echo "Successfully migrated " $DB_USER-$DB_NAME
  else
    echo "Error migrating " $DB_USER-$DB_NAME
    exit 1
  fi
done
echo "No more clients to migrate"
