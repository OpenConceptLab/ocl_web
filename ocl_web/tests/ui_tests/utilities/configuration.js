'use strict';

function getTestExecutionEnvironment() {
    var envName = process.env.env ? process.env.env : "showcase";
    console.log("--> Running specs against environment: " + envName);
    return envName;
}

function Configuration() {
    var envConfig = require('../config/env.json');
    var testExecutionEnvironment = getTestExecutionEnvironment();
    this.env = envConfig[testExecutionEnvironment];
    this.env["env"] = testExecutionEnvironment;
    this.env["username"] = process.env.username ? process.env.username : "test";
    this.env["password"] = process.env.password ? process.env.password : "test123";
    this.env["timeout"] = process.env.timeout ? process.env.timeout : 5000;
}

var Configurations = new Configuration();

Configurations.get = function (param) {
    return this.env[param];
};

module.exports = Configurations;
