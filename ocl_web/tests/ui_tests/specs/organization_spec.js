'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var OrgPage = require('../pages/organization_page');
var data = require('../data/test_data.json');

describe('OCL Org Page', function () {
    var loginPage;
    var logoutPage;
    var orgPage;
    var orgShortCode = '';

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        orgPage = new OrgPage();
    });

    it('should login', function () {
        var loginPage = new LoginPage();
        loginPage.visit();
        loginPage.login(data.username,data.password);

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as awadhwa.');
    });

    it('should create organization', function () {
        orgShortCode = orgPage.getRandomString(5);
        orgPage.createNewOrg( orgShortCode,
            data.org_name,
            data.website,
            data.company,
            data.location
        );
        expect((orgPage.status).getText()).toEqual('Organization Added');
    });

    it('should create collection under org', function () {
        orgPage.createNewOrgCollection( data.short_code,
            data.col_name,
            data.full_name,
            data.supported_locale
        );
        expect((orgPage.status).getText()).toEqual('Collection created');

        element(by.linkText('  '+orgShortCode)).click();
    });

    it('should create source', function () {
        orgPage.createNewSource( data.src_code,
            data.src_full_name,
            data.supported_locale
        );

        expect((orgPage.status).getText()).toEqual('Source created');
    });

    it('should create source version', function () {
        orgPage.createNewSourceVersion(data.id,
            data.description
        );

        expect((orgPage.status).getText()).toEqual('Source version created!');
    });

    it('should create concept', function () {
        orgPage.createNewConcept( data.concept_id,
            data.concept_name,
            data.name_type
        );

        expect((orgPage.status).getText()).toEqual('Concept created.');
    });

     it('should logout', function () {
         logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });

});
