'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var collectionPage = require('../pages/collections_page.js');
var orgPage = require('../pages/organization_page');
var data = require('../fixtures/test_data.json');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;

describe('OCL Collections Page', function () {

    var loginPage = new LoginPage();
    var logoutPage = new LogoutPage();
    var id = '';
    browser.ignoreSynchronization = true;

    beforeAll(function () {
        loginPage.visit();
        loginPage.login();
    });

    it('should create collection', function () {
        id = orgPage.getRandomId();
        collectionPage.createNewUserCollection(data.short_code + id,
            data.col_name,
            data.full_name,
            data.supported_locale
        );

        expect(collectionPage.getStatus()).toEqual('Collection created');
    });

    it('should create collection with openmrs validation schema', function () {
        collectionPage.userHomeLink.click();
        id = orgPage.getRandomId();
        collectionPage.createNewUserCollection(data.short_code + id,
            data.col_name,
            data.full_name,
            data.supported_locale,
            data.custom_validation_schema
        );
        expect(collectionPage.getStatus()).toEqual('Collection created');
    });

    it('should update collection to openmrs validation schema', function () {
        collectionPage.userHomeLink.click();
        id = orgPage.getRandomId();
        collectionPage.createNewUserCollection(data.short_code + id,
            data.col_name,
            data.full_name,
            data.supported_locale
        );

        collectionPage.clickEditIcon();
        collectionPage.setCustomValidationSchema(data.customValidationSchema);
        collectionPage.clickUpdateCollection();
        expect(collectionPage.getStatus()).toEqual('Collection updated');
    });

    it('should create collection version', function () {

        collectionPage.createNewCollectionVersion('V1', 'Version 1');

        expect((orgPage.status).getText()).toEqual('Collection version created!');
        browser.refresh();
    });

    it('should release a user collection version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Released'), 500);
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), 500);
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click();
    });

    it('should retire user collection version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Retired.'), 500);
        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');

        browser.wait(EC.textToBePresentInElement(orgPage.retireLabel.get(1), 'Retired'), 500);
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

        orgPage.notification.click();
    });

    it('should un-retire user collection version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Retired.'), 1000);
        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), 1000);

        orgPage.notification.click();
    });

    it('should un-release a user collection version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Released.'), 500);

        orgPage.notification.click();
    });

    it('should delete a user collection version', function () {
        orgPage.deleteCollectionVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully removed collection version.'), 1000);

        orgPage.notification.click();
    });

    it('should edit collection', function () {
        collectionPage.editCollection(data.col_desc, data.ext_id);

        expect(collectionPage.getStatus()).toEqual('Collection updated');
        expect((collectionPage.updatedDescValue).getText()).toContain('collection description');
        expect((collectionPage.updatedExtIdValue).getText()).toContain('1.1');
    });

    it('should delete collection', function () {
        collectionPage.deleteCollection();

        expect(collectionPage.getStatus()).toEqual('Collection Deleted');
    });

    it('should logout', function () {
        logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });
});

