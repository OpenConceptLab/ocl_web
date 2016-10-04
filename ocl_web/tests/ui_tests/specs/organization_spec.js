'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var OrgPage = require('../pages/organization_page');
var CollectionPage = require('../pages/collections_page.js');
var data = require('../fixtures/test_data.json');

describe('OCL Org Page', function () {
    var loginPage;
    var logoutPage;
    var orgPage;
    var collectionPage;
    var id = '';
    var mapping_id;

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        collectionPage = new CollectionPage();
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

    it('should release a org source version', function () {
        orgPage.releaseVersion();
        browser.sleep('750');

        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('750');
    });

    it('should retire org source version', function () {
        orgPage.retireVersion();
        browser.sleep('750');

        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should un-retire org source version', function () {
        orgPage.retireVersion();
        browser.sleep('500');

        expect(orgPage.notification.getText()).toEqual('Successfully Un-Retired.');
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should un-release a source version', function () {
        orgPage.releaseVersion();
        browser.sleep('750');

        expect(orgPage.notification.getText()).toEqual('Successfully Un-Released.');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should delete a source version', function () {
       orgPage.deleteSrcVersion();
       browser.sleep('750');

       expect(orgPage.notification.getText()).toEqual('Successfully removed source version.');

       browser.sleep('500');
       orgPage.notification.click();
        browser.sleep('500');
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

        // mapping_id = element(by.css('#mapping_id .row .field-label-value')).getText();
        // console.log(mapping_id);
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

    it('should create collection version', function () {

       collectionPage.createNewCollectionVersion('V1', 'version 1');

       expect((orgPage.status).getText()).toEqual('Collection version created!');
    });

    it('should release a collection version', function () {
        orgPage.releaseVersion();
        browser.sleep('750');

        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('750');
    });

    it('should retire org collection version', function () {
        orgPage.retireVersion();
         browser.sleep('750');

        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should un-retire org collection version', function () {
        orgPage.retireVersion();
        browser.sleep('750');

        expect(orgPage.notification.getText()).toEqual('Successfully Un-Retired.');
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should un-release a collection version', function () {
        orgPage.releaseVersion();
        browser.sleep('750');

        expect(orgPage.notification.getText()).toEqual('Successfully Un-Released.');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should delete org colection version', function () {
       orgPage.deleteCollectionVersion();
       browser.sleep('750');

       expect(orgPage.notification.getText()).toEqual('Successfully removed collection version.');

       browser.sleep('500');
       orgPage.notification.click();
        browser.sleep('500');
    });


    it('should add a reference of concept to a collection', function () {
        var concept_expression = '/orgs/'+data.org_short_code+id+'/sources/HSTP-Indicators/concepts/C1.1.1.2-/';
        orgPage.createNewReference(concept_expression);
    });

    // it('should add multiple reference', function () {
    //     element(by.linkText('References')).click();
    //     element(by.linkText('Add Multiple References')).click();
    //     element(by.cssContainingText('option', 'EthiopiaMoH-test-MlcaE')).click();
    //     element(by.cssContainingText('option', 'S1')).click();
    //     element(by.cssContainingText('option', 'S1-V2')).click();
    // });

    // it('should delete without selecting reference', function () {
    //     console.log(browser.getCurrentUrl());
    //     browser.pause();
    //     orgPage.deleteLink.click();
    //     browser.sleep('200');
    //
    //     expect(orgPage.warning.getText()).toEqual('Please select references!');
    //
    //     // browser.sleep('500');
    //     orgPage.warning.click();
    //     browser.sleep('500');
    // });

    // it('should delete a reference of concept from org collection', function () {
    //     orgPage.deleteReference();
    //
    //     expect(orgPage.notification.getText()).toEqual('Successfully removed.');
    //
    //     browser.sleep('500');
    //     orgPage.notification.click();
    //     browser.sleep('500');
    // });

    // it('should add a reference of mapping to a collection', function () {
    //     var mapping_expression = '/orgs/'+data.org_short_code+id+'/sources/HSTP-Indicators/mappings/'+mapping_id+'/';
    //     orgPage.createNewReference(mapping_expression);
    //     console.log(mapping_expression);
    //
    //     expect((orgPage.status).getText()).toEqual('Expression added.');
    //     // expect(element(by.linkText(' '+expression)).isPresent()).toBe(true);
    // });

     it('should logout', function () {
         logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });

});
