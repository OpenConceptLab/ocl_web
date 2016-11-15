#!/bin/bash -e

cd ocl_web
virtualenv ocl
source ocl/bin/activate
pip install -r requirements/$1.txt
npm cache clean
npm install
export OCL_API_HOST='http://localhost:8000'
export OCL_API_TOKEN=$2
export OCL_ANON_API_TOKEN=$2
nohup grunt serve > nohup.out 2>&1 &
echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('admin', 'paynejd@gmail.com', 'Root123') if (User.objects.filter(username='admin').count() < 1) else None" | python ocl_web/manage.py shell
