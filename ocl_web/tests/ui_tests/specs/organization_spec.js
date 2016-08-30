'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var OrgPage = require('../pages/organization_page');
var data = require('../fixtures/test_data.json');

describe('OCL Org Page', function () {
    var loginPage;
    var logoutPage;
    var orgPage;
    var id = '';

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        orgPage = new OrgPage();
    });

    it('should login', function () {
        loginPage.visit();
        loginPage.login(data.username,data.password);

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as awadhwa1.');
    });

    it('should create organization', function () {
        id = orgPage.getRandomString(5);
        orgPage.createNewOrg( data.org_short_code+id,
            data.org_name,
            data.website,
            data.company,
            data.org_location
        );

        expect((orgPage.status).getText()).toEqual('Organization Added');
    });

    it('should create source', function () {
        orgPage.createNewSource( data.src_code,
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

        element(by.linkText('  '+data.src_code)).click();
    });

    it('should create source version', function () {
        orgPage.createNewSourceVersion(data.id,
            data.description
        );

        expect((orgPage.status).getText()).toEqual('Source version created!');
    });

    it('should create concept', function () {
        orgPage.createNewConcept( data.concept_id+id,
            data.concept_name,
            data.name_type
        );

        expect((orgPage.status).getText()).toEqual('Concept created.');

        element(by.linkText('  '+data.src_code)).click();
    });

    it('should create a mapping', function () {
        var fromConceptURL= '/orgs/'+data.org_short_code+id+'/sources/HSTP-Indicators/concepts/C1.1.1.2-/';
        var toConceptURL = '/orgs/'+data.org_short_code+id+'/sources/HSTP-Indicators/concepts/C1.1.1.2-'+id+'/';

        orgPage.createNewMapping(
            fromConceptURL,
            'SAME-AS',
            toConceptURL
        );

        expect((orgPage.status).getText()).toEqual('Mapping created.');

        element(by.linkText('  '+data.org_short_code+id)).click();
    });

    it('should create collection under org', function () {
        orgPage.createNewOrgCollection( data.short_code+id,
            data.col_name,
            data.full_name,
            data.supported_locale
        );
        expect((orgPage.status).getText()).toEqual('Collection created');
    });

    it('should add a reference of concept to a collection', function () {
        var expression = '/orgs/'+data.org_short_code+id+'/sources/HSTP-Indicators/concepts/C1.1.1.2-/';
        orgPage.createNewConceptReference(expression);
        expect((orgPage.status).getText()).toEqual('Expression added.');
        // expect(element(by.linkText(' '+expression)).isPresent()).toBe(true);
    });

     it('should logout', function () {
         logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });

});
