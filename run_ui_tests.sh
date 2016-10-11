#!/bin/bash
# env=local browser=phantomjs OCL_WEB=~/workspace/ocl_web run_ui_tests.sh

if [ -z $OCL_WEB ]; then
    OCL_WEB=~/ocl_web
fi

cd $OCL_WEB

# create test user (username=testuser, password=test123)
python ocl_web/manage.py create_test_user --username=testuser --password=test123

CREATE_USER_RESULT=$?
if [[ $CREATE_USER_RESULT -ne 0 ]]; then
    exit 1
fi

nohup ./node_modules/protractor/bin/webdriver-manager update > nohup_ui_tests.out  2>&1 &

sleep 3
./node_modules/protractor/bin/protractor ./ocl_web/tests/ui_tests/conf.js --verbose
