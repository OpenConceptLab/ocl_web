'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var collectionReferencePage = require('../pages/collections_reference_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;
const timeout = configuration.get('timeout');
const baseUrl = configuration.get('baseUrl');

describe('Collection Reference Page', function () {

    var loginPage,
        logoutPage,
        mappingId,
        conceptVersionUrl,
        conceptVersionNumber,
        id,
        mappingVersion,
        sourceId;

    beforeAll(function () {
        id = collectionReferencePage.id;
        conceptVersionUrl = collectionReferencePage.conceptVersionUrl;
        conceptVersionNumber = collectionReferencePage.conceptVersionNumber;
        mappingId = collectionReferencePage.mappindId;
        mappingVersion = 1;
        sourceId = data.src_code;
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        loginPage.login();
        return browser.ignoreSynchronization = true;
    });

    afterAll(function () {
        logoutPage.logout();
    });

    xit('add concept single reference without version number', function () {
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id);
        var expectedMessage = 'OCL does not support adding the HEAD version of concepts to the collection. Added the latest version instead: ' + sourceId + '-C1.1.1.2- version';
        var conceptExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-/';
        collectionReferencePage.createNewSingleReference(conceptExpression);
        browser.wait(EC.presenceOf(collectionReferencePage.warningModal), timeout);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(1);
        expect(collectionReferencePage.warningModal.getText()).toContain(expectedMessage);
    });

    xit('add concept single reference with version number', function () {
		
        collectionReferencePage.deleteReference();
        var expectedMessage = 'Added concept: ' + sourceId + '-C1.1.1.2- version ' + conceptVersionNumber;
        collectionReferencePage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout);

        expect(collectionReferencePage.countOfReferences.count()).toEqual(1);
        expect(collectionReferencePage.successModal.getText()).toEqual(expectedMessage);
    });

    xit('add mapping single reference without version number', function () {
		
        collectionReferencePage.deleteReference();
        var expectedMessage = 'OCL does not support adding the HEAD version of mapping to the collection. Added the latest version instead: ' + sourceId + '-' + mappingId + ' version 1';
        var mappingExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/mappings/' + mappingId + '/';
        collectionReferencePage.createNewSingleReference(mappingExpression);
        browser.wait(EC.presenceOf(collectionReferencePage.warningModal), timeout);
        expect(collectionReferencePage.warningModal.getText()).toContain(expectedMessage);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(1);
    });

    xit('add mapping single reference with version number', function () {
		
        collectionReferencePage.deleteReference();
        var expectedMessage = 'Added mapping: ' + sourceId + '-' + mappingId + ' version ' + mappingVersion;
        var mappingExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/mappings/' + mappingId + '/' + mappingVersion + '/';
        collectionReferencePage.createNewSingleReference(mappingExpression);
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(1);
        expect(collectionReferencePage.successModal.getText()).toEqual(expectedMessage)
    });


    xit('add duplicate concept expression should fail', function () {
		
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.deleteReference();
        var expectedMessage = conceptVersionUrl + ': ' + 'Concept or Mapping reference name must be unique in a collection.';

        collectionReferencePage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout);

        collectionReferencePage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.duplicateErrorModal), timeout);

        expect(collectionReferencePage.duplicateErrorModal.getText()).toEqual(expectedMessage);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(0);
    });

    xit('add duplicate mapping expression should fail', function () {
		
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.deleteReference();
        var mappingExpression = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/mappings/' + mappingId + '/' + mappingVersion + '/';
        var expectedMessage = mappingExpression + ': ' + 'Concept or Mapping reference name must be unique in a collection.';

        collectionReferencePage.createNewSingleReference(mappingExpression);
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout);

        collectionReferencePage.createNewSingleReference(mappingExpression);
        browser.wait(EC.presenceOf(collectionReferencePage.duplicateErrorModal), timeout);

        expect(collectionReferencePage.duplicateErrorModal.getText()).toEqual(expectedMessage);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(0);
    });

    xit('fully specified name within collection should be unique', function () {
		
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.deleteReference();

        collectionReferencePage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout);
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/');
        orgPage.createNewConcept(data.concept_id + id, data.concept_name, 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);

        var nonUniqueFullySpecifiedNameUrl = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-' + id + '/';
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.createNewSingleReference(nonUniqueFullySpecifiedNameUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.duplicateErrorModal), timeout);
        expect(collectionReferencePage.duplicateErrorModal.getText()).toContain('Concept fully specified name must be unique for same collection and locale.');
        expect(collectionReferencePage.countOfReferences.count()).toEqual(0);
    });

    xit('test preferred name within collection should be unique', function () {
		
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.deleteReference();

        collectionReferencePage.createNewSingleReference(conceptVersionUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout);
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/');

        orgPage.createNewConcept(data.concept_id + 'test', data.concept_name, 'None', data.concept_desc, data.key1, data.locale2);
        var nonUniqueFullySpecifiedNameUrl = '/orgs/' + data.org_short_code + id + '/sources/HSTP-Indicators/concepts/C1.1.1.2-' + 'test' + '/';
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.createNewSingleReference(nonUniqueFullySpecifiedNameUrl);
        browser.wait(EC.presenceOf(collectionReferencePage.duplicateErrorModal), timeout);

        expect(collectionReferencePage.duplicateErrorModal.getText()).toContain('Concept preferred name must be unique for same collection and locale.');
        expect(collectionReferencePage.countOfReferences.count()).toEqual(0);
    });

    xit('test when user selects HEAD version of source from dropdown in multiple references', function () {
		
        const organization = data.org_short_code + id;
        browser.get(baseUrl + 'orgs/' + organization + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.deleteAllReferences();
        collectionReferencePage.setCreateNewMultipleReferencesValues(organization, 'HSTP-Indicators', 'HEAD');
        browser.wait(EC.textToBePresentInElement(collectionReferencePage.messageBox, 'When HEAD version selected, the latest version of concepts and mappings are listed'), timeout);
    });

    xit('test when user adds HEAD version of source in multiple references then inform the user', function () {

        const organization = data.org_short_code + id;
        browser.get(baseUrl + 'orgs/' + organization + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.createNewMultipleReferences(organization, 'HSTP-Indicators', 'HEAD');
        browser.wait(EC.presenceOf(collectionReferencePage.warningModal), timeout);
        expect(collectionReferencePage.warningModal.getText()).toEqual('Added the latest versions of concepts/mappings to the collection. Future updates will not be added automatically.');
    });

    xit('then when user adds non-HEAD version of source in multiple references then inform for success', function () {
        const organization = data.org_short_code + id;
        browser.get(baseUrl + 'orgs/' + organization + '/sources/HSTP-Indicators/versions/');
        orgPage.createNewSourceVersion('nonHead', 'for testing');
        browser.get(baseUrl + 'orgs/' + organization + '/collections/' + data.short_code + id + '/references/');
        collectionReferencePage.deleteAllReferences();
        collectionReferencePage.createNewMultipleReferences(organization, 'HSTP-Indicators', 'nonHead');
        browser.wait(EC.presenceOf(collectionReferencePage.successModal), timeout + 4000);
        expect(collectionReferencePage.successModal.getText()).toEqual('Concepts/mappings are added to collection.');
    });

    xit('add concept multiple reference with related mappings', function () {

        const organization = data.org_short_code + id;
        const collectionShortCode = data.short_code + id + id;
        const conceptId = 'C1\\.1\\.1\\.2-' + id + id;

        browser.get(baseUrl + 'orgs/' + organization + '/');
        orgPage.createNewOrgCollection(
            collectionShortCode,
            data.col_name + id,
            data.full_name + id,
            data.supported_locale,
            data.custom_validation_schema
        );

        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + collectionShortCode);
        const expectedMessage = 'Related mappings stored in the same source are also added to collection.';
        collectionReferencePage.createNewMultipleReferencesWithConceptAndMapping(organization, sourceId, 'HEAD', conceptId);

        browser.wait(EC.presenceOf(collectionReferencePage.checkReference), timeout);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(2);
    });

    xit('add concept multiple reference with related mappings and get error modal', function () {

        const organization = data.org_short_code + id;
        const collectionShortCode = data.short_code + id + id;
        const conceptId1 = 'C1\\.1\\.1\\.2-' + id + id;
        const conceptId2 = 'C1\\.1\\.1\\.2-test';
        const conceptExpression = '/orgs/' + organization + '/sources/HSTP-Indicators/concepts/C1.1.1.2-test/';

        browser.get(baseUrl + 'orgs/' + organization + '/collections/' + collectionShortCode + '/references/');
        collectionReferencePage.deleteAllReferences();

        collectionReferencePage.createNewSingleReference(conceptExpression);

        browser.get(baseUrl + 'orgs/' + organization + '/collections/' + collectionShortCode);
        collectionReferencePage.createNewMultipleReferencesWithConcepts(organization, sourceId, 'HEAD', [conceptId1, conceptId2]);

        browser.wait(EC.presenceOf(collectionReferencePage.warningModal), timeout);
        expect(collectionReferencePage.addReferenceModalErrorList.count()).toEqual(1);
        expect(collectionReferencePage.addReferenceModalSuccessList.count()).toEqual(2);

        collectionReferencePage.closeErrorModal.click();
        browser.wait(EC.presenceOf(collectionReferencePage.checkReference), timeout);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(3);
    });

    xit('delete concept reference with related mappings', function () {

        const organization = data.org_short_code + id;
        const collectionShortCode = data.short_code + id + id;
        const conceptId = 'C1\\.1\\.1\\.2-' + id + id;

        browser.get(baseUrl + 'orgs/' + organization + '/collections/' + collectionShortCode + '/references/');
        collectionReferencePage.deleteAllReferences();
        browser.get(baseUrl + 'orgs/' + data.org_short_code + id + '/collections/' + collectionShortCode);
        collectionReferencePage.createNewMultipleReferencesWithConceptAndMapping(organization, sourceId, 'HEAD', conceptId);
        browser.wait(EC.presenceOf(collectionReferencePage.warningModal), timeout);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(2);
        collectionReferencePage.deleteReferenceBySpecificIndex('2');
        browser.wait(EC.invisibilityOf(collectionReferencePage.warningModal), timeout);
        expect(collectionReferencePage.countOfReferences.count()).toEqual(0);
    });
});
