var UserSourcePage = function() {

    // user source locators
    this.newUserSrclink = element(by.id('new-user-source'));
    this.shortCode = $('#id_short_name');
    this.srcFullName = $('#id_full_name');
    this.supportedLocale = $('#id_supported_locales');
    this.customValidationSchema = $('#id_custom_validation_schema');
    this.createUsrSourceButton = element(by.buttonText('Create Source'));
    this.editUserSourceButton = element(by.id('edit-source'));
    this.updateUserSourceButton = element(by.id('update-source'));
    this.deleteSourceButton = element(by.id('delete-source'));
    this.confirmDeleteSourceButton = element(by.id('confirm-delete-source'));

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

    this.setCustomValidationSchema = function (custom_validation_schema) {
       this.customValidationSchema.sendKeys(custom_validation_schema)
    };

    this.clickCreateUsrSrcButton = function () {
       this.createUsrSourceButton.click();
    };

    this.createNewUsrSource = function (code, full_name, locale, custom_validation_schema){
        this.clickNewUsrSrcLink();
        this.setShortCode(code);
        this.setSrcFullName(full_name);
        this.setSupportedLocale(locale);
        this.setCustomValidationSchema(custom_validation_schema);
        this.clickCreateUsrSrcButton();
    };
};
module.exports = UserSourcePage;
