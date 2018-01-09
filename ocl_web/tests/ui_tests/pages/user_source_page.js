'use strict';

var EC = require('protractor').ExpectedConditions;

var UserSourcePage = function() {

    // user source locators
    this.newUserSrclink = element(by.id('new-user-source'));
    this.shortCode = $('#id_short_name');
    this.srcFullName = $('#id_full_name');
    this.defaultLocale = $('#id_default_locale');
    this.supportedLocale = $('#id_supported_locales');
    this.customValidationSchema = $('#id_custom_validation_schema');
    this.createUsrSourceButton = element(by.buttonText('Create Source'));
    this.editUserSourceButton = element(by.id('edit-source'));
    this.updateUserSourceButton = element(by.id('update-source'));
    this.deleteSourceButton = element(by.id('delete-source'));
    this.confirmDeleteSourceButton = element(by.id('confirm-delete-source'));
    this.checkAllReferences = element(by.id('toggle-select-references'));
    this.addToCollectionDropdownButton = element(by.id('add-to-collection-dropdown-button'));
    this.userCollection1 = element(by.id('user-collection-1'));
    this.addToCollectionSaveButton = element(by.css('#add-to-collection-dropdown .add-to-collection-save.btn.btn-primary.btn-block'));
    this.confirmModalCollectionName = element(by.id('collection-name'));
    this.confirmButton = element(by.id('confirm-modal'));
    this.addToCollectionResultInformation = element(by.id('add-to-collection-result-information'));
    this.addToCollectionErrorModal = element(by.id('add-to-collection-error'));

    this.failedValidationsPopup = element(by.id('failed-validations'));
    this.successMessage = element(by.css('.alert.alert-info'));

    this.clickNewUsrSrcLink = function () {
        this.newUserSrclink.click();
    };

    this.setShortCode = function (code) {
        this.shortCode.sendKeys(code);
    };

    this.setSrcFullName = function (full_name) {
        this.srcFullName.sendKeys(full_name);
    };

    this.setSupportedLocale = function (locale) {
       this.supportedLocale.sendKeys(locale)
    };

    this.setDefaultLocale = function (locale) {
       this.defaultLocale.sendKeys(locale)
    };

    this.setCustomValidationSchema = function (custom_validation_schema) {
        if (typeof custom_validation_schema !== 'undefined') {
            this.customValidationSchema.element(by.cssContainingText("option", custom_validation_schema)).click();
        }
    };

    this.clickCreateUsrSrcButton = function () {
       this.createUsrSourceButton.click();
    };

    this.createNewUsrSource = function (code, full_name, locale, custom_validation_schema){
        this.clickNewUsrSrcLink();
        this.setShortCode(code);
        this.setSrcFullName(full_name);
        this.setDefaultLocale('en');
        this.setSupportedLocale(locale);
        this.setCustomValidationSchema(custom_validation_schema);
        this.clickCreateUsrSrcButton();
    };

    this.addToCollection = function () {
        this.checkAllReferences.click();
        this.addToCollectionDropdownButton.click();
        this.userCollection1.click();
        this.addToCollectionSaveButton.click();
    };
};
module.exports = UserSourcePage;
