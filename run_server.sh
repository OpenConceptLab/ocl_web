#!/bin/bash

cd ocl_web
virtualenv ocl
source ocl/bin/activate
pip install -r requirements/local.txt
npm install
export OCL_API_HOST='localhost:8000'
export OCL_API_TOKEN=$1
export OCL_ANON_API_TOKEN=$1
nohup grunt serve > /dev/null 2>&1 &;
