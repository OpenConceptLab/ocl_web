#!/bin/bash
# env=local browser=phantomjs OCL_WEB=~/workspace/ocl_web run_ui_tests.sh

if [ -z $OCL_WEB ]; then OCL_WEB=~/ocl_web; fi

cd $OCL_WEB

echo "Removing selenium before update"
rm -rf ./node_modules/protractor/node_modules/webdriver-manager/selenium

echo "Updating web driver manager"
nohup ./node_modules/protractor/bin/webdriver-manager update

echo "Starting server"
nohup  ./node_modules/protractor/bin/webdriver-manager start --standalone > nohup.out 2>&1 &

sleep 3

./node_modules/protractor/bin/protractor ./ocl_web/tests/ui_tests/conf.js --verbose
