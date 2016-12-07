'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;

describe('OCL User Source Page', function () {
    var loginPage;
    var logoutPage;
    var usrSrcPage;
    var srcShortCode = '';

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        usrSrcPage = new UserSourcePage();
        return browser.ignoreSynchronization = true;
    });

    it('should login', function () {
        loginPage.login();

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as ' + configuration.get("username") + '.');
    });

    it('should create source with OpenMRS validation', function () {
        srcShortCode = orgPage.getRandomShortCode();
        usrSrcPage.createNewUsrSource(
            data.src_code + srcShortCode,
            data.src_full_name,
            data.supported_locale,
            data.custom_validation_schema
        );

        expect(orgPage.getStatus()).toEqual('Source created');
        expect((orgPage.customValidationSchema).getText()).toEqual('OpenMRS')
    });

    it('should logout', function () {
        logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });

    });

