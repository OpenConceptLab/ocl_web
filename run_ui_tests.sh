#!/bin/bash
# env=local browser=phantomjs OCL_WEB=~/workspace/ocl_web run_ui_tests.sh

if [ -z $OCL_WEB ]; then
    OCL_WEB=cd ~/ocl_web
fi

cd $OCL_WEB
nohup ./node_modules/protractor/bin/webdriver-manager update > nohup_ui_tests.out  2>&1 &

sleep 3
./node_modules/protractor/bin/protractor ./ocl_web/tests/ui_tests/conf.js --verbose
