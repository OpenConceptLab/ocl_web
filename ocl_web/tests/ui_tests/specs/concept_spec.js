'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var OrgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var ConceptEditPage = require('../pages/concept_edit_page');
var ConceptCreatePage = require('../pages/concept_create_page');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;


describe('Concept', function () {
    var loginPage = new LoginPage();
    var logoutPage = new LogoutPage();
    var orgPage = new OrgPage();
    var usrSrcPage = new UserSourcePage();
    var conceptEditPage = new ConceptEditPage();
    var conceptCreatePage = new ConceptCreatePage();
    var srcShortCode = '';
    browser.ignoreSynchronization = true;

    beforeAll(function () {
        // Login
        loginPage.visit();
        loginPage.login();
    });

    describe('concept edit with basic validation', function () {

        beforeAll(function () {
            // Create Source
            srcShortCode = orgPage.getRandomString(5);
            usrSrcPage.createNewUsrSource(
                data.src_code + srcShortCode,
                data.src_full_name,
                data.supported_locale,
                'None'
            );

            // Create two concepts
            // Create concept 1
            orgPage.createNewConcept(data.concept_id + "1", data.concept_name + "1", data.concept_desc, data.key1, data.locale2);

            // Go back to source's page
            element(by.css(".resource-label.source")).click();

            //Create concept 2
            return orgPage.createNewConcept(data.concept_id + "2", data.concept_name + "2", data.concept_desc, data.key1, data.locale2);
        });

        it('should edit the concept 2, drop fully specified name and get an error', function () {
            element(by.id("edit-concept")).click();

            conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
            conceptEditPage.namesDiv.element(by.css('.name-type')).element(by.cssContainingText("option", "Short")).click();

            conceptEditPage.updateButton.click();

            expect(conceptEditPage.errorBox.getText()).toEqual('Concept requires at least one fully specified name');

            conceptEditPage.cancelUpdateButton.click();

        });

        it('should edit the concept 2, change the name to be same as concept 1 and get an error', function () {
            element(by.id("edit-concept")).click();

            conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
            var nameInput = conceptEditPage.namesDiv.element(by.css('.name-content'));

            // PAIN!
            nameInput.sendKeys(protractor.Key.BACK_SPACE + '1');
            conceptEditPage.updateButton.click();

            expect(conceptEditPage.errorBox.getText()).toEqual('Concept preferred name must be unique for same source and locale');

            conceptEditPage.cancelUpdateButton.click();
        });

        afterAll(function () {
            element(by.css('.resource-label.user')).click();
        });

    });


    describe('concept create with openmrs validation', function () {

        beforeAll(function () {
            // Create Source with openMRS
            srcShortCode = orgPage.getRandomString(5);
            usrSrcPage.createNewUsrSource(
                data.src_code + srcShortCode,
                data.src_full_name,
                data.supported_locale,
                'OpenMRS'
            );
        });

        function prepareToCreateConcept() {
            element(by.css(".resource-label.source")).click();
            orgPage.newConceptLink.click();
            orgPage.createConcept.click();
        }

        function setConceptId(id) {
            orgPage.conceptId.sendKeys(id);
        }

        function addNamesAndSynonyms(namesAndSynonymsNumber) {
            for (var i = 0; i < namesAndSynonymsNumber; i++) {
                orgPage.addNameSynonymLink.click();
            }
        }

        function getNamesAndSynonyms() {
            return element.all(by.repeater('name in names'));
        }

        function setNameText(item, name) {
            item.element(by.model('name.name')).sendKeys(name);
        }

        function setLocalePreferred(item, select) {
            item.element(by.model('name.locale_preferred')).isSelected().then(function (selected) {
                if ((!selected && select) || (selected && !select)) {
                    item.element(by.model('name.locale_preferred')).click();
                }
            });
        }

        function setNameType(item, option) {
            item.element(by.model('name.name_type')).element(by.cssContainingText("option", option)).click();
        }

        function setName(item, nameText, nameType, localePreferred) {
            setNameText(item, nameText);
            setNameType(item, nameType);
            setLocalePreferred(item, localePreferred);
        }

        function createConcept() {
            conceptCreatePage.createButton.click();
        }

        function getErrorText() {
            return conceptCreatePage.errorBox.getText();
        }

        it('#241 concept create with more then one preferred name should get an error', function () {

            prepareToCreateConcept();
            setConceptId("1");
            addNamesAndSynonyms(1);

            var names = getNamesAndSynonyms();

            setNameText(names.first(), "name1");
            setLocalePreferred(names.first(), true);

            setNameText(names.last(), "name2");
            setLocalePreferred(names.last(), true);

            createConcept();

            expect(getErrorText()).toEqual('Custom validation rules require a concept to have exactly one preferred name');
        });

        it('#241 concept create with short preferred name should get an error', function () {

            prepareToCreateConcept();

            setConceptId("1");
            addNamesAndSynonyms(1);

            var names = getNamesAndSynonyms();
            setName(names.first(), "name1", "Fully Specified", false);
            setName(names.last(), "name2", "Short", true);

            createConcept();
            expect(getErrorText()).toEqual('Custom validation rules require a preferred name to be different than a short name');
        });

        it('#241 concept create with more then one preferred name should get an error', function () {

            prepareToCreateConcept();

            setConceptId("1");
            addNamesAndSynonyms(1);

            getNamesAndSynonyms().each(function (item) {
                setName(item, "name", "Fully Specified", true);
            });

            createConcept();
            expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');
        });

        it('#241 concept create with unique short names should return success', function () {

            prepareToCreateConcept();

            setConceptId("1");
            addNamesAndSynonyms(2);

            var names = getNamesAndSynonyms();
            setName(names.first(), "name", "Fully Specified", true);

            names.each(function (item, index) {
                if (index > 0) {
                    setName(item, "shortName", "Short", false);
                }
            });

            element(by.model('description.description')).sendKeys("desc");
            createConcept();
            expect((orgPage.status).getText()).toEqual('Concept created.');
        });

        it('#242 concept create with same preferred name in same source & locale should get an error', function () {
            prepareToCreateConcept();

            setConceptId("2");

            setName(getNamesAndSynonyms().first(), "sameName", "Fully Specified", true);

            element(by.model('description.description')).sendKeys("desc");

            createConcept();

            prepareToCreateConcept();

            setConceptId("3");

            setName(getNamesAndSynonyms().first(), "sameName", "Fully Specified", true);

            createConcept();

            expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');

        });

        it('#242 concept create with same fully specified name in same source & locale should get an error', function () {

            prepareToCreateConcept();

            setConceptId("3");

            setName(getNamesAndSynonyms().first(), "sameFullySpecified", "Fully Specified", true);

            element(by.model('description.description')).sendKeys("desc");

            createConcept();

            prepareToCreateConcept();

            setConceptId("4");

            addNamesAndSynonyms(1);

            var names = getNamesAndSynonyms();

            setName(names.first(), "requiredFullySpecified", "Fully Specified", true);
            setName(names.last(), "sameFullySpecified", "Fully Specified", false);

            createConcept();

            expect(getErrorText()).toEqual('Custom validation rules require fully specified name should be unique for same locale and source');

        });


    });

    afterAll(function () {
        logoutPage.logout();
    });

});

