'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var orgPage = require('../pages/organization_page');
var collectionPage = require('../pages/collections_page.js');
var data = require('../fixtures/test_data.json');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;
var timeout = 5000;

var fs = require('fs');

function writeScreenShot(data, filename) {
    var stream = fs.createWriteStream(filename);
    stream.write(new Buffer(data, 'base64'));
    stream.end();
}

describe('OCL Org Page', function () {
    const baseUrl = configuration.get('baseUrl');
    var mappingVersion = 1;
    var loginPage;
    var logoutPage;
    var id = '';
    var conceptVersionUrl;
    var conceptVersionNumber;
    var mappingId;


    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        return browser.ignoreSynchronization = true;
    });

    it('should login', function () {
        loginPage.login();

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as ' + configuration.get("username") + '.');
    });

    it('should create organization', function () {
        id = orgPage.getRandomId();
        orgPage.createNewOrg(data.org_short_code + id, data.org_name, data.website, data.company, data.org_location);

        expect(orgPage.getStatus()).toEqual('Organization Added');
    });

    it('should create source', function () {
        orgPage.createNewSource(data.src_code, data.src_full_name, data.supported_locale);

        expect(orgPage.getStatus()).toEqual('Source created');
    });

    it('should create concept', function () {
        orgPage.createNewConcept(data.concept_id + id, data.concept_name, data.concept_desc, data.key1, data.locale1);

        browser.wait(EC.presenceOf(orgPage.status), timeout);
        expect(orgPage.getStatus()).toEqual('Concept created.');

        element(by.linkText('  ' + data.src_code)).click();
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

    it('should create concept', function () {

        orgPage.createNewConcept(data.concept_id, data.concept_name, data.concept_desc, data.key1, data.locale2);
        orgPage.conceptVersionUrl.getText().then(function (versionUrl) {
            conceptVersionUrl = versionUrl;
            conceptVersionNumber = versionUrl.toString().split('/')[7];
        });

        browser.wait(EC.presenceOf(orgPage.status), timeout);
        expect(orgPage.getStatus()).toEqual('Concept created.');

        element(by.linkText('  ' + data.src_code)).click();
    });

    it('should create a mapping', function () {
        var fromConceptURL = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-/';
        var toConceptURL = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-' + id + '/';

        orgPage.createNewMapping(
            fromConceptURL,
            'SAME-AS',
            toConceptURL
        );

        expect(orgPage.getStatus()).toEqual('Mapping created.');


        element(by.css('#mapping_id .row .field-label-value')).getText().then(function (value) {
            mappingId = value;
        });

        element(by.linkText('  ' + data.org_short_code + id)).click();
    });

    it('should create collection under org', function () {
        // REMOVE THIS LINE BELOW WHEN YOU UNCOMMENT
        element(by.linkText('  ' + data.org_short_code + id)).click();
        orgPage.createNewOrgCollection(data.short_code + id,
            data.col_name,
            data.full_name,
            data.supported_locale
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
        expect(orgPage.notification.getText()).toEqual('Successfully removed collection version.');

        orgPage.notification.click();
    });

    it('add concept single reference without version number', function () {
        var expectedMessage = 'Does not support adding the HEAD version of concepts to the collection. Added the latest version instead: C1.1.1.2- version';
        var conceptExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-/';
        orgPage.createNewSingleReference(conceptExpression).then(function () {
            browser.takeScreenshot().then(function (data) {
                writeScreenShot(data, 'single-reference.png')
            })
        });
        browser.wait(EC.presenceOf(orgPage.warningModal), timeout);
        expect(orgPage.countOfReferences.count()).toEqual(1);
        expect(orgPage.warningModal.getText()).toContain(expectedMessage);
    });

    it('add concept single reference with version number', function () {
        orgPage.deleteReference();
        var expectedMessage = 'Added concept: C1.1.1.2- version ' + conceptVersionNumber;
        orgPage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(orgPage.successModal), timeout);

        expect(orgPage.countOfReferences.count()).toEqual(1);
        expect(orgPage.successModal.getText()).toEqual(expectedMessage);
    });

    // it('add mapping single reference without version number', function () {
    //     orgPage.deleteReference();
    //     var expectedMessage = 'Does not support adding the HEAD version of mapping to the collection. Added the latest version instead: ' + mappingId + ' version 1';
    //     var mappingExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/mappings/' + mappingId + '/';
    //     orgPage.createNewSingleReference(mappingExpression);
    //     browser.wait(EC.presenceOf(orgPage.warningModal), timeout);
    //     expect(orgPage.warningModal.getText()).toContain(expectedMessage);
    //     expect(orgPage.countOfReferences.count()).toEqual(1);
    // });

    // it('add mapping single reference with version number', function () {
    //     orgPage.deleteReference();
    //     var expectedMessage = 'Added mapping: ' + mappingId + ' version ' + mappingVersion;
    //     var mappingExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/mappings/' + mappingId + '/' + mappingVersion + '/';
    //     orgPage.createNewSingleReference(mappingExpression);
    //     browser.wait(EC.presenceOf(orgPage.successModal), timeout);
    //     expect(orgPage.countOfReferences.count()).toEqual(1);
    //     expect(orgPage.successModal.getText()).toEqual(expectedMessage)
    // });


    it('add duplicate concept expression should fail', function () {
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        orgPage.deleteReference();
        var expectedMessage = conceptVersionUrl + ': ' + 'Concept or Mapping reference name must be unique in a collection.';

        orgPage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(orgPage.successModal), timeout);

        orgPage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(orgPage.duplicateErrorModal), timeout);

        expect(orgPage.duplicateErrorModal.getText()).toEqual(expectedMessage);
        expect(orgPage.countOfReferences.count()).toEqual(0);
    });

    it('add duplicate mapping expression should fail', function () {
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        orgPage.deleteReference();
        var mappingExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/mappings/' + mappingId + '/' + mappingVersion + '/';
        var expectedMessage = mappingExpression + ': ' + 'Concept or Mapping reference name must be unique in a collection.';

        orgPage.createNewSingleReference(mappingExpression);
        browser.wait(EC.presenceOf(orgPage.successModal), timeout);
        orgPage.createNewSingleReference(mappingExpression);
        browser.wait(EC.presenceOf(orgPage.duplicateErrorModal), timeout);
        expect(orgPage.duplicateErrorModal.getText()).toEqual(expectedMessage);
        expect(orgPage.countOfReferences.count()).toEqual(0);
    });

    it('should logout', function () {
        logoutPage.logout();

        expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
    });
});
