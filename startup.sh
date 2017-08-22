#!/bin/bash

python ocl_web/manage.py syncdb --noinput

python ocl_web/manage.py migrate 

echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('root', 'paynejd@gmail.com', '${ROOT_PASSWORD}') if (User.objects.filter(username='root').count() < 1) else None" | python ocl_web/manage.py shell

echo "Starting the server"
grunt serve
