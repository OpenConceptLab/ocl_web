'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;
const baseUrl = configuration.get('baseUrl');
const username = configuration.get('username');
const timeout = configuration.get('timeout');

describe('OCL User Source Page', function () {
    var loginPage;
    var logoutPage;
    var usrSrcPage;
    var srcShortCode = '';

    beforeAll(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        usrSrcPage = new UserSourcePage();
        return browser.ignoreSynchronization = true;
    });

    it('should login', function () {
        loginPage.login();

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as ' + username + '.');
    });

    it('should create source', function () {
        srcShortCode = orgPage.getRandomShortCode();
        usrSrcPage.createNewUsrSource(
            data.src_code + srcShortCode,
            data.src_full_name,
            data.supported_locale
        );

        expect(orgPage.getStatus()).toEqual('Source created');
        expect((orgPage.customValidationSchema).getText()).toEqual('None')
    });

    it('should create concept', function () {
        orgPage.createNewConcept(data.concept_id + orgPage.getRandomId(), data.concept_name, 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);

        expect(orgPage.getStatus()).toEqual('Concept created.');

        element(by.linkText('  ' + data.src_code + srcShortCode)).click();
    });

    it('should create source version', function () {
        orgPage.createNewSourceVersion(data.id, data.description);

        browser.wait(EC.presenceOf(orgPage.status), timeout);
        expect(orgPage.getStatus()).toEqual('Source version created!');

        browser.refresh()
    });

    it('should release a user source version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Released'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), timeout);
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click()
    });

    it('should retire a user source version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Retired'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');

        browser.wait(EC.textToBePresentInElement(orgPage.retireLabel.get(1), 'Retired'), timeout);
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

        orgPage.notification.click()
    });

    it('should un-retire a user source version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Retired.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Un-Retired.');

        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), timeout);
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click()
    });

    it('should un-release a user source version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Released.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Un-Released.');

        orgPage.notification.click()
    });

    it('should delete a user source version', function () {
        orgPage.deleteSrcVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully removed source version.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully removed source version.');

        orgPage.notification.click();
    });

    xit('should add source concepts to collection', function () {
		
        browser.get(baseUrl + 'users/' + username + '/sources/' + data.src_code + srcShortCode + '/concepts/');

        usrSrcPage.addToCollection();
        browser.wait(EC.elementToBeClickable(usrSrcPage.confirmButton), timeout);
        usrSrcPage.confirmButton.click();

        browser.wait(EC.visibilityOf(usrSrcPage.addToCollectionResultInformation), timeout);
        expect(usrSrcPage.addToCollectionResultInformation.isDisplayed()).toBeTruthy();
    });

    xit('should show error modal when add source concepts to collection with error', function () {
        browser.get(baseUrl + 'users/' + username + '/sources/' + data.src_code + srcShortCode + '/concepts/');

        usrSrcPage.addToCollection();
        browser.wait(EC.elementToBeClickable(usrSrcPage.confirmButton), timeout);
        usrSrcPage.confirmButton.click();

        browser.wait(EC.visibilityOf(usrSrcPage.addToCollectionErrorModal), timeout);
        expect(usrSrcPage.addToCollectionResultInformation.isDisplayed()).toBeFalsy();
    });

    it('should logout', function () {
        logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });
});
