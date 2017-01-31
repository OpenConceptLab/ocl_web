#!/bin/bash -e

export RELEASE_VERSION=`date +"%Y%m%d%H%M%S"`
cd ../
tar -czf ocl_web$RELEASE_VERSION.tgz repo
scp ocl_web$RELEASE_VERSION.tgz root@$IP:/root/releases/
if ssh root@$IP "pkill -9 -f grunt"; then echo "killed grunt"; fi;
if ssh root@$IP "pkill -9 -f ocl_web"; then echo "killed ocl_web"; fi;
ssh root@$IP 'rm -rf ocl_web'
ssh root@$IP "tar -xzf releases/ocl_web$RELEASE_VERSION.tgz && mv repo ocl_web"
if ssh root@$IP "source ~/ocl_web/deploy/manage_releases.sh && clear_releases ~/releases/"; then echo "Removed old releases"; fi;
if [[ -z $PORT ]]
then
	PORT=80
fi
ssh root@$IP "DJANGO_CONFIGURATION=$ENV OCL_WEB_SOCKET_ADDRESS=0.0.0.0:$PORT ./ocl_web/run_server.sh $SETTINGS $TOKEN"
