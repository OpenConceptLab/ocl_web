var BasePage = require('./base_page.js');
var chance = require('chance').Chance();

var ConceptPage = function () {
    this.createButton = element(by.css('.btn.btn-primary'));

    this.updateCommentTextArea = element(by.id("id_update_comment"));
    this.updateButton = element(by.id("update-concept"));
    this.editLink = element(by.id("edit-concept"));
    this.descriptionField = element(by.model('description.description'));
    this.descriptionTypeField = element(by.model('description.description_type'));
    this.deleteDescriptionAreaButton = element(by.id("id-delete-description"));
    this.deleteNameAreaButton = element(by.id("id-delete-name"));

    this.conceptsLink = element(by.linkText('Concepts'));
    this.newConceptLink = element(by.id('id-new-concept'));
    this.conceptId = $('#id_concept_id');
    this.addNameSynonymLink = $('#add-name-synonym');
    this.conceptClass = $('#id_concept_class');
    this.conceptDatatype = $('#id_datatype');

    this.parentSourceLink = element(by.css(".resource-label.source"));

    this.mapTypes = element.all(by.css('#map_type option'));
    this.mappingsButton = element(by.id('mappings_link'));

    this.addToCollectionDropDown = element(by.id('add-to-collection-dropdown-button'));
    this.firstCollectionToBeAdded = element(by.id('user-collection-1'));
    this.addToCollectionSaveButton = element(by.css('#add-to-collection-dropdown > div > button'));
    this.confirmButton = element(by.id('confirm-modal'));
    this.cascadeCheckbox = element(by.id('cascade-mappings'));

    this.alertBox = element(by.id('concept-alert'));

    this.fillInUpdateText = function (updateMsg) {
        this.updateCommentTextArea.clear().sendKeys(updateMsg);
    };

    this.fillInUpdateTextRandomly = function () {
        this.fillInUpdateText("Update Concept " + chance.word({length: 4}));
    };

    this.addConceptToFirstCollection = function () {
        this.addToCollectionDropDown.click();
        this.firstCollectionToBeAdded.click();
        this.addToCollectionSaveButton.click();
    };

    this.clickConfirmModal = function () {
        this.confirmButton.click();
    };

    this.clickCascadeCheckbox = function () {
        this.cascadeCheckbox.click();
    };

    this.confirmWithoutCascade = function () {
        this.clickCascadeCheckbox();
        this.clickConfirmModal();
    };

    this.clickEditConcept = function () {
        this.editLink.click();
    };

    this.clickMappings = function () {
        this.mappingsButton.click();
    };

    this.fillDescriptionField = function () {
        this.descriptionField.sendKeys(chance.word({length: 4}));
        this.descriptionTypeField.sendKeys('None');
    };

    this.clearDescriptionField = function () {
        this.descriptionField.clear().sendKeys("");
    };

    this.deleteDescriptionArea = function () {
        this.deleteDescriptionAreaButton.click();
    };

    this.deleteNameArea = function () {
        this.deleteNameAreaButton.click();
    };

    this.prepareToEditConcept = function () {
        this.clickEditConcept();
        this.fillInUpdateTextRandomly();
    };

    this.prepareToCreateConcept = function () {
        this.parentSourceLink.click();
        this.conceptsLink.click();
        this.newConceptLink.click();
        this.setConceptId(this.getRandomId());
        this.conceptClass.sendKeys('Misc');
        this.conceptDatatype.sendKeys('None');
    };

    this.setConceptId = function (id) {
        this.conceptId.clear().sendKeys(id);
    };

    this.addNamesAndSynonyms = function (namesAndSynonymsNumber) {
        for (var i = 0; i < namesAndSynonymsNumber; i++) {
            this.addNameSynonymLink.click();
        }
    };

    this.getNamesAndSynonyms = function () {
        return element.all(by.repeater('name in names'));
    };

    this.setNameText = function (item, name) {
        item.element(by.model('name.name')).clear().sendKeys(name);
    };

    this.getNameText = function (item) {
        return item.element(by.model('name.name')).getAttribute('value');
    };

    this.getNameType = function (item) {
        return item.element(by.model('name.name_type')).getAttribute('value');
    };

    this.setLocalePreferred = function (item, select) {
        item.element(by.model('name.locale_preferred')).isSelected().then(function (selected) {
            if ((!selected && select) || (selected && !select)) {
                item.element(by.model('name.locale_preferred')).click();
            }
        });
    };

    this.setNameType = function (item, option) {
        item.element(by.model('name.name_type')).clear().sendKeys(option);
    };

    this.setNameLocale = function (item, option) {
        if (option === undefined) {
            option = "en"
        }
        item.element(by.model('name.locale')).clear().sendKeys(option);
    };

    this.setName = function (item, nameText, nameType, localePreferred, nameLocale) {
        this.setNameText(item, nameText);
        this.setNameType(item, nameType);
        this.setLocalePreferred(item, localePreferred);
        this.setNameLocale(item, nameLocale);
    };

    this.createConcept = function () {
        this.createButton.click();
    };

    this.updateConcept = function () {
        this.updateButton.click();
    };

    this.createConceptWithFullySpecifiedName = function (id, name) {
        this.prepareToCreateConcept();
        this.setConceptId(id);
        this.setName(this.getNamesAndSynonyms().first(), name, "Fully Specified", true, "en");
        this.fillDescriptionField();
        this.createConcept();
    };
};

ConceptPage.prototype = BasePage;
module.exports = new ConceptPage();
