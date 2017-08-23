#!/bin/bash

pip install -r requirements/local.txt

python ocl_web/manage.py test
