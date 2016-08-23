#!/bin/bash

cd ocl_web
virtualenv ocl
source ocl/bin/activate
pip install -r ../requirements/$1.txt
npm install
export OCL_API_HOST='http://localhost:8000'
export OCL_API_TOKEN=$2
export OCL_ANON_API_TOKEN=$2
nohup grunt serve > nohup.out 2>&1 &
