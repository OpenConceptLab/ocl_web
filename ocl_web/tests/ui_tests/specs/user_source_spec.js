'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var OrgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');

describe('OCL User Source Page', function () {
    var loginPage;
    var logoutPage;
    var orgPage;
    var usrSrcPage;
    var srcShortCode = '';

     beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
         orgPage = new OrgPage();
         usrSrcPage = new UserSourcePage();
    });

    it('should login', function () {
        loginPage.visit();
        loginPage.login(data.username,data.password);

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as awadhwa1.');
    });

    it('should create source', function () {
        srcShortCode = orgPage.getRandomString(5);
        usrSrcPage.createNewUsrSource(data.src_code+srcShortCode,
            data.src_full_name,
            data.supported_locale
        );

        expect((orgPage.status).getText()).toEqual('Source created');
    });

    it('should create concept', function () {
        orgPage.createNewConcept( data.concept_id,
            data.concept_name,
            data.name_type
        );

        expect((orgPage.status).getText()).toEqual('Concept created.');

        element(by.linkText('  '+data.src_code+srcShortCode)).click();
    });

    it('should create source version', function () {
        orgPage.createNewSourceVersion(data.id,
            data.description
        );

        expect((orgPage.status).getText()).toEqual('Source version created!');
    });

    it('should release a user source version', function () {
        orgPage.releaseVersion();
        browser.sleep('500');

        expect(orgPage.releaseLabel.getText()).toEqual('Released');
        expect(orgPage.message.getText()).toEqual('Successfully Released.');

        browser.sleep('500');
        orgPage.message.click();
        browser.sleep('750');
    });

    it('should un-release a user source version', function () {
        orgPage.releaseVersion();
        browser.sleep('750');

        expect(orgPage.message.getText()).toEqual('Successfully Un-Released.');

        browser.sleep('500');
        orgPage.message.click();
        browser.sleep('500');
    });

    it('should logout', function () {
         logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });
});
