#!/bin/bash

echo "Removing selenium before update"
rm -rf ./node_modules/protractor/node_modules/webdriver-manager/selenium

echo "Updating web driver manager"
nohup ./node_modules/protractor/bin/webdriver-manager clean
nohup ./node_modules/protractor/bin/webdriver-manager update

echo "Starting server"
nohup  ./node_modules/protractor/bin/webdriver-manager start --standalone > nohup_tests.out 2>&1 &

sleep 10

./node_modules/protractor/bin/protractor ./ocl_web/tests/ui_tests/conf.js --verbose