var BasePage = require('./base_page.js');
var EC = require('protractor').ExpectedConditions;
var configuration = require('../utilities/configuration.js');
const timeout = configuration.get('timeout');

var OrganizationPage = function () {

    // create org locators
    this.orgTab = element(by.linkText('Organization Membership'));
    this.createNewOrgLink = element(by.id('new-organization'));
    this.shortCode = $('#id_short_name');
    this.name = $('#id_name');
    this.conceptName = element(by.model('name.name'));
    this.orgWebsite = $('#id_website');
    this.orgCompany = $('#id_company');
    this.orgLocation = $('#id_location');
    this.createOrgButton = element(by.buttonText('Create Organization'));
    this.customValidationSchema = $('#id_custom_validation_schema');

    this.source = element(by.id('source'));
    this.sourceVersion = element(by.id('sourceVersion'));
    this.messageBox = element.all(by.className('ajs-message ajs-warning ajs-visible')).first();
    this.conceptToSelect = element(by.css('#concepts > li:nth-child(1) > label > input'));
    this.multipleReferencesTab = element(by.css('#addmultiplereftab > div:nth-child(2)'));

    // create collection under org locators
    this.newOrgCollectionLink = element(by.linkText('Collections'));
    this.createNewCollection = element(by.linkText(' New Collection'));
    this.collShortCode = $('#id_short_code');
    this.fullName = $('#id_full_name');
    this.defaultLocale = $('#id_default_locale');
    this.supportedLocale = $('#id_supported_locales');
    this.addOrgCollectionButton = element(by.buttonText('Add'));


    // create source under org locators
    this.newOrgSourceLink = element(by.linkText('Sources'));
    this.createNewOrgSource = element(by.linkText(' New Source'));
    this.createSourceButton = element(by.buttonText('Create Source'));

    // create source version locators
    this.newSrcVersionLink = element(by.linkText('Versions'));
    this.createNewSrcVersion = element(by.linkText('New Source Version'));
    this.srcVersionId = $('#id_id');
    this.srcVersionDescription = $('#id_description');
    this.createSrcVersionButton = element(by.buttonText('Create Source Version'));

    // Release / Un-release version locators
    this.releaseButton = $('#id_release');
    this.notification = element.all(by.css('.ajs-success')).first();
    this.releaseLabel = $$('.label-primary.release-label');

    // Retire / Un-Retire version locators
    this.retireButton = $('.resource_retire');
    this.retireLabel = $$('.retire-label');

    this.checkReference = $('#check_reference');
    this.deleteLink = $('.delete-reference');
    this.warning = $('.ajs-warning');
    this.okButton = element(by.buttonText('OK'));

    // Delete version locators
    this.deleteSrcVersionIcon = element(by.css('.source_version_delete'));
    this.deleteColVersionIcon = element(by.css('.collection_version_delete'));

    // create concept locators
    this.conceptsLink = element(by.linkText('Concepts'));
    this.newConceptLink = element(by.linkText(' New Concept'));
    this.conceptId = $('#id_concept_id');
    this.createConceptButton = element(by.buttonText('Create Concept'));
    this.conceptClass = $('#id_concept_class');
    this.conceptDatatype = $('#id_datatype');
    this.select_name_locale = element(by.model('name.locale'));
    this.select_desc_locale = element(by.model('description.locale'));
    this.localePreferred = element(by.css('.name-locale-preferred'));
    this.nameType = element(by.css('.name-type'));
    this.conceptDesc = element(by.model('description.description'));
    this.key = element(by.model('extra.key'));
    this.addNameSynonymLink = $('#add-name-synonym');

    this.okButton = element(by.buttonText('OK'));

    //create mapping locators
    this.newMappingLink = element(by.linkText('Mappings'));
    this.createMapping = element(by.linkText(' New Mapping'));
    this.fromConcept = $('#id_from_concept_url');
    this.mapType = $('#map_type');
    this.toConcept = $('#id_internal_to_concept_url');
    this.createMappingButton = element(by.buttonText('Create Mapping'));

    this.setCustomValidationSchema = function (custom_validation_schema) {
        if (typeof custom_validation_schema !== 'undefined') {
            this.customValidationSchema.element(by.cssContainingText("option", custom_validation_schema)).click();
        }
    };


    this.createNewOrg = function (org_ShortCode, org_name, website, company, loc) {
        this.orgTab.click();
        this.createNewOrgLink.click();
        this.shortCode.sendKeys(org_ShortCode);
        this.name.sendKeys(org_name);
        this.orgWebsite.sendKeys(website);
        this.orgCompany.sendKeys(company);
        this.orgLocation.sendKeys(loc);
        this.createOrgButton.click();
    };

    this.createNewOrgCollection = function (short_code, coll_name, full_name, locale, customValidationSchema) {
        this.newOrgCollectionLink.click();
        this.createNewCollection.click();
        this.collShortCode.sendKeys(short_code);
        this.name.sendKeys(coll_name);
        this.fullName.sendKeys(full_name);
        this.setCustomValidationSchema(customValidationSchema);
        this.defaultLocale.sendKeys('en');
        this.supportedLocale.sendKeys(locale);
        this.addOrgCollectionButton.click();
    };

    this.createNewSource = function (src_shortCode, full_name, locale) {
        this.newOrgSourceLink.click();
        this.createNewOrgSource.click();
        this.shortCode.sendKeys(src_shortCode);
        this.fullName.sendKeys(full_name);
        this.defaultLocale.sendKeys('en');
        this.supportedLocale.sendKeys(locale);
        this.createSourceButton.click();
    };

    this.createNewSourceVersion = function (id, description) {
        this.newSrcVersionLink.click();
        this.createNewSrcVersion.click();
        this.srcVersionId.sendKeys(id);
        this.srcVersionDescription.sendKeys(description);
        this.createSrcVersionButton.click();
    };

    this.releaseVersion = function () {
        this.releaseButton.click();
    };

    this.retireVersion = function () {
        this.retireButton.click();
    };

    this.createNewConcept = function (id, name, nameType, desc, key, locale, localePreferred) {
        this.conceptsLink.click();
        this.newConceptLink.click();
        this.conceptId.sendKeys(id);
        this.conceptClass.sendKeys('Misc');
        this.conceptDatatype.sendKeys('None');
        this.select_name_locale.sendKeys(locale);
        this.conceptName.sendKeys(name);
        this.select_desc_locale.sendKeys(locale);
        this.conceptDesc.sendKeys(desc);
        this.nameType.sendKeys(nameType);
        this.localePreferred.sendKeys(localePreferred);
        this.key.sendKeys(key);
        this.createConceptButton.click();
    };

    this.createNewMapping = function (from_concept, map_type, to_concept) {
        this.newMappingLink.click();
        this.createMapping.click();
        this.fromConcept.sendKeys(from_concept);
        this.mapType.sendKeys(map_type);
        this.toConcept.sendKeys(to_concept);
        this.createMappingButton.click();
    };

    this.deleteSrcVersion = function () {
        var clickDelete = function () {
            this.deleteSrcVersionIcon.click();
            browser.wait(EC.visibilityOf(this.okButton), timeout);
            this.okButton.click();
        }.bind(this);

        browser.wait(EC.visibilityOf(this.deleteSrcVersionIcon), timeout).then(clickDelete, function () {
            //probably still processing...
            browser.refresh();
            browser.wait(EC.visibilityOf(this.deleteSrcVersionIcon, timeout)).then(clickDelete);
        }.bind(this));
    };

    this.deleteCollectionVersion = function () {
        var clickDelete = function() {
            this.deleteColVersionIcon.click();
            browser.wait(EC.visibilityOf(this.okButton), timeout);
            this.okButton.click();
        }.bind(this);

        browser.wait(EC.visibilityOf(this.deleteColVersionIcon), timeout).then(clickDelete, function() {
            //still processing...
            browser.refresh();
            browser.wait(EC.visibilityOf(this.deleteColVersionIcon), timeout).then(clickDelete);
        }.bind(this));
    };
};
OrganizationPage.prototype = BasePage;
module.exports = new OrganizationPage();
