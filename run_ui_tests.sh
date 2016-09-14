#!/bin/bash

cd ~/ocl_web
nohup ./node_modules/protractor/bin/webdriver-manager start > nohup_ui_tests.out  2>&1 &
sleep 3
./node_modules/protractor/bin/protractor ./ocl_web/tests/ui_tests/conf.js
