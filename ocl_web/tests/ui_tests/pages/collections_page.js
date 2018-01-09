var BasePage = require('./base_page.js');

var CollectionsPage = function() {

    // create collection locators
    this.newUserCollection = element(by.id('new-user-collection'));
    this.shortCode = $('#id_short_code');
    this.collName = $('#id_name');
    this.fullName = $('#id_full_name');
    this.defaultLocale = $('#id_default_locale');
    this.supportedLocale = $('#id_supported_locales');
    this.customValidationSchema = $('#id_custom_validation_schema');
    this.addCollectionButton = element(by.buttonText('Add'));

    // create collection version locators
    this.versionTab = element(by.linkText('Versions'));
    this.createVersionLink = element(by.linkText('New Collection Version'));
    this.versionId = $('#id_id');
    this.versionDescription = $('#id_description');
    this.createColVersionButton = element(by.buttonText('Create Collection Version'));

    // edit collection locators
    this.editIcon = element(by.css('span.glyphicon-pencil'));
    this.description = $('#id_description');
    this.externalId = $('#id_external_id');
    this.updateCollectionButton = element(by.buttonText('Update'));
    this.updatedDescValue = $('#id_coll_description');
    this.updatedExtIdValue = $('#id_coll_externalId');

    // delete collection locators
    this.deleteIcon = element(by.css('span.glyphicon-trash'));
    this.deleteButton = element(by.buttonText('Delete'));
    this.deleteConfirm = element(by.buttonText('Yes'));

    this.setShortCode = function (code) {
        this.shortCode.sendKeys(code);
    };

    this.setCollName = function (name) {
        this.collName.sendKeys(name);
    };

    this.setFullName = function (full_name) {
        this.fullName.sendKeys(full_name);
    };

    this.setDefaultLocale = function (locale) {
        this.supportedLocale.sendKeys(locale)
    };

    this.setSupportedLocale = function (locale) {
        this.defaultLocale.sendKeys(locale)
    };

    this.setCustomValidationSchema = function (custom_validation_schema) {
       this.customValidationSchema.sendKeys(custom_validation_schema)
    };

    this.setDescription = function (description) {
        this.description.sendKeys(description);
    };

    this.setExternalId = function (id) {
        this.externalId.sendKeys(id);
    };

    this.clickNewCollection = function () {
        this.newUserCollection.click();
    };

    this.clickAddCollection = function () {
        this.addCollectionButton.click();
    };

    this.clickUpdateCollection = function () {
        this.updateCollectionButton.click();
    };

    this.clickDeleteCollection = function () {
        this.deleteButton.click();
    };

    this.clickEditIcon = function () {
        this.editIcon.click();
    };

    this.clickDeleteIcon = function () {
        this.deleteIcon.click();
    };

    this.createNewUserCollection = function (short_code, name, full_name, locale, custom_validation_schema) {
        this.clickNewCollection();
        this.setShortCode(short_code);
        this.setCollName(name);
        this.setFullName(full_name);
        this.setDefaultLocale('en');
        this.setSupportedLocale(locale);
        this.clickAddCollection();
        this.setCustomValidationSchema(custom_validation_schema);
    };

    this.createNewCollectionVersion = function (id, description) {
        this.versionTab.click();
        this.createVersionLink.click();
        this.versionId.sendKeys(id);
        this.versionDescription.sendKeys(description);
        this.createColVersionButton.click();
    };

    this.editCollection = function (description, id) {
        this.clickEditIcon();
        this.setDescription(description);
        this.setExternalId(id);
        this.clickUpdateCollection();
    };

    this.deleteCollection = function () {
        this.clickEditIcon();
        this.clickDeleteIcon();
        this.clickDeleteCollection();
        this.deleteConfirm.click();
    };

};
CollectionsPage.prototype = BasePage;
module.exports = new CollectionsPage();
