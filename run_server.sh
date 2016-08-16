#!/bin/bash -e

cd ocl_web
source ocl/bin/activate 
pip install -r requirements.txt 
export OCL_API_HOST='localhost:8000'
export OCL_API_TOKEN='showcase-token'
export OCL_ANON_API_TOKEN='showcase-token'
nohup grunt serve &
