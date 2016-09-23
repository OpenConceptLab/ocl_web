var OrganizationPage = function() {

    // create org locators
    this.createNewOrgLink = element(by.linkText('Create New Organization'));
    this.shortCode = $('#id_short_name');
    this.name = $('#id_name');
    this.orgWebsite = $('#id_website');
    this.orgCompany = $('#id_company');
    this.orgLocation = $('#id_location');
    this.createOrgButton = element(by.buttonText('Create Organization'));
    this.status = $('.alert-info');

    // create collection under org locators
    this.newOrgCollectionLink = element(by.linkText('Collections'));
    this.createNewCollection = element(by.linkText(' New Collection'));
    this.collShortCode = $('#id_short_code');
    this.fullName = $('#id_full_name');
    this.supportedLocale = $('#id_supported_locales');
    this.addOrgCollectionButton = element(by.buttonText('Add'));

    // create reference locators
    this.references = element(by.linkText('References'));
    this.addNewReferenceLink = element(by.linkText(' Reference'));
    this.expression = $('#expression');
    this.addReferenceButton = element(by.buttonText('Add'));

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
    this.message = $('.ajs-success');
    this.releaseLabel = $$('.release-label');

    // Delete reference locators
    this.deleteLink = $('.delete-reference');
    this.warning = $('.ajs-warning');
    this.checkReference = $('#check_reference');
    this.okButton = element(by.buttonText('OK'));

    // create concept locators
    this.newConceptLink = element(by.linkText('Concepts'));
    this.createConcept = element(by.linkText(' New Concept'));
    this.conceptId = $('#id_concept_id');
    this.conceptNameType = $('#id_name_type');
    this.createConceptButton = element(by.buttonText('Create Concept'));

    //create mapping locators
    this.newMappingLink = element(by.linkText('Mappings'));
    this.createMapping = element(by.linkText(' New Mapping'));
    this.fromConcept = $('#id_from_concept_url');
    this.mapType = $('#id_map_type');
    this.toConcept = $('#id_internal_to_concept_url');
    this.createMappingButton = element(by.buttonText('Create Mapping'));

    // for random string as name of org
    this.getRandomString = function(length) {
        var string = '';
        var letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        for (var i = 0; i < length; i++) {
            string += letters.charAt(Math.floor(Math.random() * letters.length));
        }
        return string;
    };

    this.createNewOrg = function (org_ShortCode, org_name, website, company, loc ) {
        this.createNewOrgLink.click();
        this.shortCode.sendKeys(org_ShortCode);
        this.name.sendKeys(org_name);
        this.orgWebsite.sendKeys(website);
        this.orgCompany.sendKeys(company);
        this.orgLocation.sendKeys(loc);
        this.createOrgButton.click();
    };

    this.createNewOrgCollection = function (short_code, coll_name, full_name, locale ) {
        this.newOrgCollectionLink.click();
        this.createNewCollection.click();
        this.collShortCode.sendKeys(short_code);
        this.name.sendKeys(coll_name);
        this.fullName.sendKeys(full_name);
        this.supportedLocale.sendKeys(locale);
        this.addOrgCollectionButton.click();
    };

    this.createNewReference = function (expression) {
        this.references.click();
        this.addNewReferenceLink.click();
        this.expression.sendKeys(expression);
        this.addReferenceButton.click();
    };

    this.deleteReference = function () {
        this.checkReference.click();
        this.deleteLink.click();
        browser.sleep('250');
        this.okButton.click();
        browser.sleep('1000');
    };

    this.createNewSource = function (src_shortCode, full_name, locale) {
        this.newOrgSourceLink.click();
        this.createNewOrgSource.click();
        this.shortCode.sendKeys(src_shortCode);
        this.fullName.sendKeys(full_name);
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
      browser.sleep('750');
    };

    this.createNewConcept = function (id, name, name_type) {
        this.newConceptLink.click();
        this.createConcept.click();
        this.conceptId.sendKeys(id);
        this.name.sendKeys(name);
        this.conceptNameType.sendKeys(name_type);
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

    //
    // this.waitForAjax = function () {
    //     setInterval(function () {
    //         if ($.active == 0) {
    //             return;
    //         }
    //     }, 1000)
    // }
};
module.exports = OrganizationPage;
