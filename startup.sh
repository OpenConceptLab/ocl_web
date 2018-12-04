#!/bin/bash

if [ $SSH ] 
then 
sudo service ssh start 
fi

if [ ! -z "$WAIT_FOR" ] 
then
./wait-for-it.sh $WAIT_FOR
fi

hostip=$(ip route show | awk '/default/ {print $3}')

export CONFIG=${ENVIRONMENT^}

echo ""
echo "Host IP=${hostip}"
echo ""

python ocl_web/manage.py syncdb --noinput --configuration="${CONFIG}"

python ocl_web/manage.py migrate --configuration="${CONFIG}"

python ocl_web/manage.py create_user --username="root" --password="${ROOT_PASSWORD}" --superuser --configuration="${CONFIG}"

if [ "$IMPORT_DEMO_DATA" = "true" ]
then
python ocl_web/manage.py create_user --username="admin" --password="Admin123" --superuser --configuration="${CONFIG}"
fi

echo "Starting the server"
grunt serve
