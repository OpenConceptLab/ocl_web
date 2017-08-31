'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var orgPage = require('../pages/organization_page');
var collectionPage = require('../pages/collections_page.js');
var collectionReferencePage = require('../pages/collections_reference_page.js');
var data = require('../fixtures/test_data.json');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;
const timeout = configuration.get('timeout');

describe('OCL Org Page', function () {
    const baseUrl = configuration.get('baseUrl');
    var loginPage;
    var logoutPage;
    var mappingId;
    var id = '';

    beforeAll(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        loginPage.login();
        return browser.ignoreSynchronization = true;
    });

    afterAll(function () {
        logoutPage.logout();
    });

    it('should create organization', function () {
        id = orgPage.getRandomId();
        collectionReferencePage.id = id;
        orgPage.createNewOrg(data.org_short_code + id, data.org_name, data.website, data.company, data.org_location);

        expect(orgPage.getStatus()).toEqual('Organization Added');
    });

    it('should create source', function () {
        orgPage.createNewSource(data.src_code, data.src_full_name, data.supported_locale);

        expect(orgPage.getStatus()).toEqual('Source created');
    });

    it('should create source version', function () {
        orgPage.createNewSourceVersion(data.id, data.description);

        browser.wait(EC.presenceOf(orgPage.status), timeout);

        expect(orgPage.getStatus()).toEqual('Source version created!');
        browser.refresh();

    });

    it('should release a org source version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Released'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), timeout);
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click();
    });

    it('should retire org source version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Retired.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');

        browser.wait(EC.textToBePresentInElement(orgPage.retireLabel.get(1), 'Retired'), timeout);
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

        orgPage.notification.click();
    });

    it('should un-retire org source version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Retired.'), timeout);
        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), timeout);

        orgPage.notification.click();
    });

    it('should un-release a source version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Released.'), timeout);

        orgPage.notification.click();
    });

    it('should delete a source version', function () {
        orgPage.deleteSrcVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully removed source version.'), timeout);

        orgPage.notification.click();
    });

    xit('should create concept', function () {
		
        orgPage.createNewConcept(data.concept_id, data.concept_name, 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);
        collectionReferencePage.conceptVersionUrl.getText().then(function (versionUrl) {
            collectionReferencePage.conceptVersionUrl = versionUrl;
            collectionReferencePage.conceptVersionNumber = versionUrl.toString().split('/')[7];
        });

        browser.wait(EC.presenceOf(orgPage.status), timeout);
        expect(orgPage.getStatus()).toEqual('Concept created.');

        element(by.linkText('  ' + data.src_code)).click();
    });

    xit('should create a mapping', function () {
	
        orgPage.createNewConcept(data.concept_id + id, data.concept_name, 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);

        element(by.linkText('  ' + data.src_code)).click();

        orgPage.createNewConcept(data.concept_id + id + id, data.concept_name + ' second', 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);

        element(by.linkText('  ' + data.src_code)).click();

        var fromConceptURL = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-' + id + id + '/';
        var toConceptURL = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-' + id + '/';

        orgPage.createNewMapping(
            fromConceptURL,
            'SAME-AS',
            toConceptURL
        );

        expect(orgPage.getStatus()).toEqual('Mapping created.');


        element(by.css('#mapping_id .row .field-label-value')).getText().then(function (value) {
            mappingId = value;
            collectionReferencePage.mappindId = mappingId;
        });

        element(by.linkText('  ' + data.org_short_code + id)).click();
    });

    it('should create collection under org', function () {
        // REMOVE THIS LINE BELOW WHEN YOU UNCOMMENT
        element(by.linkText('  ' + data.org_short_code + id)).click();
        orgPage.createNewOrgCollection(data.short_code + id,
            data.col_name,
            data.full_name,
            data.supported_locale,
            data.custom_validation_schema
        );

        expect(orgPage.getStatus()).toEqual('Collection created');
    });

    it('should create collection version', function () {
        collectionPage.createNewCollectionVersion('V1', 'version 1');
        expect(orgPage.getStatus()).toEqual('Collection version created!');
    });

    it('should release a collection version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Released'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Released.');

        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), timeout);
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click();
    });

    it('should retire org collection version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Retired.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Retired.');

        browser.wait(EC.textToBePresentInElement(orgPage.retireLabel.get(1), 'Retired'), timeout);
        expect(orgPage.retireLabel.get(1).getText()).toEqual('Retired');

        orgPage.notification.click();
    });

    it('should un-retire org collection version', function () {
        orgPage.retireVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Retired.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Un-Retired.');

        browser.wait(EC.textToBePresentInElement(orgPage.releaseLabel.get(1), 'Released'), timeout);
        expect(orgPage.releaseLabel.get(1).getText()).toEqual('Released');

        orgPage.notification.click();
    });

    it('should un-release a collection version', function () {
        orgPage.releaseVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully Un-Released.'), timeout);
        expect(orgPage.notification.getText()).toEqual('Successfully Un-Released.');

        orgPage.notification.click();
    });

    it('should delete org colection version', function () {
        orgPage.deleteCollectionVersion();

        browser.wait(EC.textToBePresentInElement(orgPage.notification, 'Successfully removed collection version.'), timeout);

        orgPage.notification.click();
    });
});
