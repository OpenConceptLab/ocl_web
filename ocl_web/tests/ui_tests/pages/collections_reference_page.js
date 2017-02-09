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
    this.deleteLink = $('.delete-reference');
    this.warning = $('.ajs-warning');
    this.okButton = element(by.buttonText('OK'));
    this.organization = element(by.id('organization'));
    this.source = element(by.id('source'));
    this.sourceVersion = element(by.id('sourceVersion'));
    this.messageBox = element.all(by.className('ajs-message ajs-warning ajs-visible')).first();
    this.multipleReferencesTab = element(by.css('#addmultiplereftab > div:nth-child(2)'));
    this.conceptToSelect = element(by.css('#concepts > li:nth-child(1) > label > input'));

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
        this.organization.sendKeys(organization);
        browser.sleep(100);
        this.source.sendKeys(source);
        browser.sleep(100);
        this.sourceVersion.sendKeys(sourceVersion);
        browser.sleep(100);
    };

    this.createNewMultipleReferences = function (organization, source, sourceVersion) {
        this.setCreateNewMultipleReferencesValues(organization, source, sourceVersion);
        browser.wait(EC.visibilityOf(this.multipleReferencesTab), 500);
        this.conceptToSelect.click();
        this.addMultipleReferenceButton.click();
    };

    this.deleteReference = function () {
        this.checkReference.click();
        this.deleteLink.click();
        browser.wait(EC.visibilityOf(this.okButton), 500);
        this.okButton.click();
    };
};

CollectionsReferencePage.prototype = BasePage;
module.exports = new CollectionsReferencePage();
