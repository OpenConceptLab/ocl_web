var BasePage = require('./base_page.js');
var chance = require('chance').Chance();

var ConceptPage = function() {
    this.createButton = element(by.css('.btn.btn-primary'));

    this.updateCommentTextArea = element(by.id("id_update_comment"));
    this.namesDiv= element(by.id("names-and-synonyms"));
    this.updateButton = element(by.id("update-concept"));
    this.cancelUpdateButton = element(by.id('cancel-update'));
    this.editLink = element(by.id("edit-concept"));
    this.descriptionField = element(by.model('description.description'));
    this.deleteDescriptionAreaButton = element(by.id("id-delete-description"));
    this.deleteNameAreaButton = element(by.id("id-delete-name"));

    this.conceptsLink = element(by.linkText('Concepts'));
    this.newConceptLink = element(by.linkText(' New Concept'));
    this.conceptId = $('#id_concept_id');
    this.addNameSynonymLink = $('#add-name-synonym');

    this.fillInUpdateText = function(updateMsg){
        this.updateCommentTextArea.sendKeys(updateMsg);
    };

    this.fillInUpdateTextRandomly = function(){
        this.fillInUpdateText("Update Concept " + chance.word({length: 4}));
    };

    this.clickEditConcept = function () {
        this.editLink.click();
    };

    this.fillDescriptionField = function () {
        this.descriptionField.sendKeys(chance.word({length: 4}))
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
        element(by.css(".resource-label.source")).click();
        this.conceptsLink.click();
        this.newConceptLink.click();
        this.setConceptId(this.getRandomId());
    };

    this.setConceptId = function (id) {
        this.conceptId.sendKeys(id);
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
        item.element(by.model('name.name_type')).element(by.cssContainingText("option", option)).click();
    };

    this.setNameLocale = function (item, option) {
        if (option === undefined) {
            option = "English [en]"
        }
        item.element(by.model('name.locale')).element(by.cssContainingText("option", option)).click();
    };

    this.setName = function (item, nameText, nameType, localePreferred, nameLocale) {
        this.setNameText(item, nameText);
        this.setNameType(item, nameType);
        this.setLocalePreferred(item, localePreferred);
        this.setNameLocale(item, nameLocale)
    };

    this.createConcept = function () {
        this.createButton.click();
    };

    this.updateConcept = function () {
        this.updateButton.click();
    };

    this.createConceptFullySpecifiedRandomly = function () {
        this.createConceptWithFullySpecifiedName(this.getRandomId(), this.getRandomName());
    };

    this.createConceptWithFullySpecifiedName = function (id, name) {
        this.prepareToCreateConcept();
        this.setConceptId(id);
        this.setName(this.getNamesAndSynonyms().first(), name, "Fully Specified", true, "English [en]");
        this.fillDescriptionField();
        this.createConcept();
    };
};

ConceptPage.prototype = BasePage;
module.exports = new ConceptPage();
