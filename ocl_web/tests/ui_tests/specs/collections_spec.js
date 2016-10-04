'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var CollectionPage = require('../pages/collections_page.js');
var OrgPage = require('../pages/organization_page');
var data = require('../fixtures/test_data.json');

describe('OCL Collections Page', function () {

    var loginPage;
    var logoutPage;
    var collectionPage;
    var orgPage;
    var id='';

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

    it('should create collection', function () {
        id = orgPage.getRandomString(2);
        collectionPage.createNewUserCollection( data.short_code+id,
            data.col_name,
            data.full_name,
            data.supported_locale
        );

        expect((collectionPage.status).getText()).toEqual('Collection created');
    });

    it('should create collection version', function () {

       collectionPage.createNewCollectionVersion('V1', 'Version 1');

       expect((orgPage.status).getText()).toEqual('Collection version created!');
    });

    it('should release a user collection version', function () {
        orgPage.releaseVersion();
        browser.sleep('500');

        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('750');
    });

    it('should retire user collection version', function () {
        orgPage.retireVersion();
        browser.sleep('500');

        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

         browser.sleep('500');
        orgPage.notification.click();
         browser.sleep('500');
    });

    it('should un-retire user collection version', function () {
        orgPage.retireVersion();
        browser.sleep('500');

        expect(orgPage.notification.getText()).toEqual('Successfully Un-Retired.');
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

         browser.sleep('500');
        orgPage.notification.click();
         browser.sleep('500');
    });

    it('should un-release a user collection version', function () {
        orgPage.releaseVersion();
        browser.sleep('500');

        expect(orgPage.notification.getText()).toEqual('Successfully Un-Released.');

        browser.sleep('500');
        orgPage.notification.click();
        browser.sleep('500');
    });

    it('should delete a user collection version', function () {
       orgPage.deleteVersion();
       browser.sleep('750');

       expect(orgPage.notification.getText()).toEqual('Successfully removed collection version.');
        browser.sleep('500');
       orgPage.notification.click();
    });

    it('should add a reference of concept to a collection', function () {
        var concept_expression = '/orgs/EthiopiaMOH/sources/HSTP-Indicators/concepts/1/';
        orgPage.createNewReference(concept_expression);
    });

    it('should edit collection', function () {
        collectionPage.editCollection(data.col_desc, data.ext_id);

        expect((collectionPage.status).getText()).toEqual('Collection updated');
        expect((collectionPage.updatedDescValue).getText()).toContain('collection description');
        expect((collectionPage.updatedExtIdValue).getText()).toContain('1.1');
    });

    it('should delete collection', function () {
        collectionPage.deleteCollection();

        expect((collectionPage.status).getText()).toEqual('Collection Deleted');
    });

     it('should logout', function () {
         logoutPage.logout();

         expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
     });

});

