'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var OrgPage = require('../pages/organization_page');

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
        loginPage.login('awadhwa','root123');

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as awadhwa.');
    });

    it('should create organization', function () {
        orgShortCode = orgPage.getRandomString(5);
        orgPage.createNewOrg( orgShortCode,
            'EthiopiaMoh',
            'www.moh.gov.et',
            'Ministry Of Health',
            'Ethiopia'
        );
        expect((orgPage.status).getText()).toEqual('Organization Added');
    });

    it('should create collection under org', function () {
        orgPage.createNewOrgCollection( 'WHO',
            'Woreda Health Office',
            'Woreda Health Office Collection',
            'en,es,fr'
        );
        expect((orgPage.status).getText()).toEqual('Collection created');

        element(by.linkText('  '+orgShortCode)).click();
    });

    it('should create source', function () {
        orgPage.createNewSource( 'WHS',
            'Census/World Health Statistics',
            'en,es'
        );

        expect((orgPage.status).getText()).toEqual('Source created');
    });

    it('should create source version', function () {
        orgPage.createNewSourceVersion('V1',
            'Version 1'
        );

        expect((orgPage.status).getText()).toEqual('Source version created!');
    });

    it('should create concept', function () {
        orgPage.createNewConcept( 'C1',
            'Life Expectancy at Birth (years)',
            'Fully Specified'
        );

        expect((orgPage.status).getText()).toEqual('Concept created.');
    });

     it('should logout', function () {
         logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });

});
