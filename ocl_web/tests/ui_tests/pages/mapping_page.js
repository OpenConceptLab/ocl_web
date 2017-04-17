var BasePage = require('./base_page.js');
var EC = require('protractor').ExpectedConditions;
var configuration = require('../utilities/configuration.js');
const timeout = configuration.get('timeout');

var MappingPage = function () {

    this.addToCollectionDropDown = element(by.id('add-to-collection-dropdown-button'));
    this.firstCollection = element(by.id('user-collection-1'));
    this.addToCollectionSaveButton = element(by.css('#add-to-collection-dropdown > div > button'));
    this.confirmModalButton = element(by.id('confirm-modal'));
    this.firstSource = element(by.css('#source-1 > a > span.resource-label-id > span.resource-label-id-breadcrumb'));

    this.alertBox = element(by.id('concept-alert'));

    this.addMappingToFirstCollection = function () {
        browser.wait(EC.visibilityOf(this.addToCollectionDropDown), timeout);
        this.addToCollectionDropDown.click();
        this.firstCollection.click();
        this.addToCollectionSaveButton.click();
    };

    this.confirmModal = function () {
        this.confirmModalButton.click();
    };

    this.clickFirstSource = function () {
        this.firstSource.click();
    };

    this.getFirstSourceName = function () {
        return this.firstSource.getText();
    };
};

MappingPage.prototype = BasePage;
module.exports = new MappingPage();
