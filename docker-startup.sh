#!/bin/bash

echo "from django.contrib.auth.models import User; from users.models import UserProfile; from orgs.models import Organization; UserProfile.objects.create(user=User.objects.create_superuser('root', 'root@example.com', '$ROOT_PWD'), organizations=map(lambda o: o.id, Organization.objects.filter(created_by='root')), mnemonic='root')" | python ocl_web/manage.py shell

python ocl_web/manage.py syncdb --noinput

python ocl_web/manage.py migrate 

echo "Starting the server"
grunt serve
