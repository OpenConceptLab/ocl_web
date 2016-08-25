var CollectionsPage = function() {

    // create collection locators
    this.newUserCollection = element(by.linkText('New User Collection'));
    this.shortCode = $('#id_short_code');
    this.col_name = $('#id_name');
    this.fullName = $('#id_full_name');
    this.supportedLocale = $('#id_supported_locales');
    this.addCollectionButton = element(by.buttonText('Add'));

    // edit collection locators
    this.editIcon = element(by.css('span.glyphicon-cog'));
    this.description = $('#id_description');
    this.externalId = $('#id_external_id');
    this.updateCollectionButton = element(by.buttonText('Update'));

    // delete collection locators
    this.deleteIcon = element(by.css('span.glyphicon-trash'));
    this.deleteButton = element(by.buttonText('Delete'));

    this.setShortCode = function (code) {
        this.shortCode.sendKeys(code);
    };

    this.setColName = function (name) {
        this.col_name.sendKeys(name);
    };

    this.setFullName = function (full_name) {
        this.fullName.sendKeys(full_name);
    };

    this.setSupportedLocale = function (locale) {
        this.supportedLocale.sendKeys(locale)
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

    this.createNewUserCollection = function (short_code, name, full_name, locale) {
        this.clickNewCollection();
        this.setShortCode(short_code);
        this.setColName(name);
        this.setFullName(full_name);
        this.setSupportedLocale(locale);
        this.clickAddCollection();
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
    };
};
module.exports = CollectionsPage;
