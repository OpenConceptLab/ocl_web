#!/bin/bash -e

cd ocl_web 
source ocl/bin/activate 
pip install -r requirements.txt 
grunt serve &
