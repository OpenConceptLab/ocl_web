#!/bin/bash

if [ $SSH ] 
then 
sudo service ssh start 
fi

if [ ! -z "$WAIT_FOR" ] 
then
./wait-for-it.sh $WAIT_FOR
fi

if [ -z $ENVIRONMENT ]
then 
export SETTINGS=local
export CONFIG=Local
elif [ "$ENVIRONMENT" = "qa" ]
then
export SETTINGS=local
export CONFIG=Local
else
export SETTINGS=$ENVIRONMENT
export CONFIG=${ENVIRONMENT^}
fi

hostip=$(ip route show | awk '/default/ {print $3}')

echo ""
echo "OCL_API_HOST=http://${hostip}:8000"
echo ""

export OCL_API_HOST="http://${hostip}:8000"

python ocl_web/manage.py syncdb --noinput

python ocl_web/manage.py migrate 

python ocl_web/manage.py create_test_user --username="root" --password="${ROOT_PASSWORD}"

echo "Starting the server"
grunt serve
