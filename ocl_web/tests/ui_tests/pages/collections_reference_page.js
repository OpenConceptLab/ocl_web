var BasePage = require('./base_page.js');
var EC = require('protractor').ExpectedConditions;
var id = '';
var conceptVersionUrl;
var conceptVersionNumber;
var mappingId;


var CollectionsReferencePage = function () {

    this.references = element(by.linkText('References'));
    this.addNewReferenceLink = element(by.id('add-reference'));
    this.singleReferences = element(by.id('add-single-tab'));
    this.expression = element(by.id('expression'));
    this.addSingleReferenceButton = element(by.id('add-single-reference'));
    this.addMultipleReferenceButton = element(by.id('add-multiple-references-button'));
    this.countOfReferences = element.all(by.css('a[title="Collection Reference"]'));

    this.successModal = element(by.css('.alert.alert-success'));
    this.warningModal = element(by.css('.alert.alert-warning'));
    this.duplicateErrorModal = element(by.css('.list-group-item.ng-binding.ng-scope'));
    this.conceptVersionUrl = element(by.css('.concept-version-url .field-label-value'));

    this.checkReference = $('#check-reference-1');
    this.checkAllReferences = $('#toggle-select-references');
    this.deleteLink = $('.delete-reference');
    this.warning = $('.ajs-warning');
    this.okButton = element(by.buttonText('OK'));
    this.organization = element(by.id('organization'));
    this.source = element(by.id('source'));
    this.sourceVersion = element(by.id('sourceVersion'));
    this.messageBox = element.all(by.className('ajs-message ajs-warning ajs-visible')).first();
    this.multipleReferencesTab = element(by.css('#addmultiplereftab > div:nth-child(2)'));
    this.conceptToSelect = element(by.css('#concepts > li:nth-child(1) > label > input'));
    this.mappingToSelect = element(by.css('#mappings > li:nth-child(1) > label > input'));
    this.mappingModalMessage = element(by.css('#mappingModal > div > div > div.modal-body > div'));
    this.mappingModalList = element.all(by.css('#mappingModal > div > div > div.modal-body > ul > li'));
    this.countOfMappingModal = element.all(by.id('mappingModal'));
    this.addReferenceModalErrorList = element.all(by.css('#addReferenceModalErrorList > li'));
    this.addReferenceModalSuccessList = element.all(by.css('#addReferenceModalSuccessList > li'));
    this.closeErrorModal = element(by.id('closeErrorModalButton'));

    this.createNewSingleReference = function (expression) {
        this.references.click();
        this.addNewReferenceLink.click();
        this.singleReferences.click();
        browser.wait(EC.visibilityOf(this.expression), 2000);
        this.expression.sendKeys(expression);
        return this.addSingleReferenceButton.click();
    };

    this.setCreateNewMultipleReferencesValues = function (organization, source, sourceVersion) {
        this.references.click();
        this.addNewReferenceLink.click();
        browser.wait(EC.elementToBeClickable(this.organization), 1000);
        this.organization.sendKeys(organization);

        browser.wait(EC.presenceOf(this.source.$('option[label="' + source + '"]')), 2000);
        this.source.sendKeys(source);

        browser.wait(EC.elementToBeClickable(this.sourceVersion.$('option[label="HEAD"]')), 7000);
        this.sourceVersion.sendKeys(sourceVersion);
    };

    this.createNewMultipleReferences = function (organization, source, sourceVersion) {
        this.setCreateNewMultipleReferencesValues(organization, source, sourceVersion);
        browser.wait(EC.visibilityOf(this.multipleReferencesTab), 4000);
        this.conceptToSelect.click();
        this.addMultipleReferenceButton.click();
    };

    this.createNewMultipleReferencesWithConcepts = function (organization, source, sourceVersion, conceptIdList) {
        this.setCreateNewMultipleReferencesValues(organization, source, sourceVersion);
        browser.wait(EC.visibilityOf(this.multipleReferencesTab), 1000);
        conceptIdList.forEach(function (conceptId) {
            element(by.css('#' + conceptId)).click();
        });
        this.addMultipleReferenceButton.click();
    };

    this.createNewMultipleReferencesWithConceptAndMapping = function (organization, source, sourceVersion, conceptId) {
        this.setCreateNewMultipleReferencesValues(organization, source, sourceVersion);
        browser.wait(EC.visibilityOf(this.multipleReferencesTab), 1000);
        element(by.css('#' + conceptId)).click();
        this.mappingToSelect.click();
        this.addMultipleReferenceButton.click();
    };

    this.deleteReference = function () {
        this.checkReference.click();
        this.deleteLink.click();
        browser.wait(EC.visibilityOf(this.okButton), 1000);
        this.okButton.click();
    };

    this.deleteAllReferences = function () {
        this.checkAllReferences.click();
        this.deleteLink.click();
        browser.wait(EC.visibilityOf(this.okButton), 2000);
        this.okButton.click();
    };
};

CollectionsReferencePage.prototype = BasePage;
module.exports = new CollectionsReferencePage();
