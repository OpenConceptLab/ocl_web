'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var conceptPage = require('../pages/concept_page');
var configuration = require('../utilities/configuration.js');

describe('Concept', function () {
    var loginPage = new LoginPage();
    var logoutPage = new LogoutPage();
    var usrSrcPage = new UserSourcePage();
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
            srcShortCode = conceptPage.getRandomShortCode();
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
            conceptPage.prepareToEditConcept();

            conceptPage.namesDiv.element(by.css('.name-type')).element(by.cssContainingText("option", "Short")).click();

            conceptPage.updateButton.click();

            expect(conceptPage.getError()).toEqual('A concept must have at least one fully specified name (across all locales)');

            conceptPage.cancelUpdateButton.click();

        });

        it('should edit the concept 2, change the name to be same as concept 1 and get an error', function () {
            conceptPage.prepareToEditConcept();

            var nameInput = conceptPage.namesDiv.element(by.css('.name-content'));

            // PAIN!
            nameInput.sendKeys(protractor.Key.BACK_SPACE + '1');
            conceptPage.updateButton.click();

            expect(conceptPage.getError()).toEqual('Concept preferred name must be unique for same source and locale');

            conceptPage.cancelUpdateButton.click();
        });

        it('#238 concept create - same names with different locales should not get an error', function () {
            conceptPage.prepareToCreateConcept();

            conceptPage.addNamesAndSynonyms(1);

            var names = conceptPage.getNamesAndSynonyms();
            conceptPage.setName(names.first(), "en_fr_name", "Short", false, "French [fr]");
            conceptPage.setName(names.last(), "name2", "Fully Specified", false, "English [en]");

            conceptPage.fillDescriptionField();
            conceptPage.createConcept();

            conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "en_fr_name")
            expect(conceptPage.getStatus()).toEqual('Concept created.');
        });

        it('#342 concept create - basic validation order at least one fully specified name', function () {
            conceptPage.prepareToCreateConcept();
            conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Short", true, "English [en]");
            conceptPage.fillDescriptionField();
            conceptPage.createConcept();

            expect(conceptPage.getError()).toEqual('A concept must have at least one fully specified name (across all locales)');
        });

        it('#342 concept create - source validation order preferred name should be unique', function () {
            conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name33");
            conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name33");

            expect(conceptPage.getError()).toEqual('Concept preferred name must be unique for same source and locale');
        });

        it('#338 concept edit - deleting fully specified name should get corresponding error', function () {
            conceptPage.createConceptFullySpecifiedRandomly();
            conceptPage.prepareToEditConcept();

            conceptPage.deleteNameArea();

            conceptPage.updateButton.click();
            expect(conceptPage.getError()).toEqual('A concept must have at least one fully specified name (across all locales)');
        });

        it('#341 concept create - deleting description field should not get error', function () {
            conceptPage.prepareToCreateConcept();
            conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
            conceptPage.deleteDescriptionArea();
            conceptPage.createConcept();

            expect(conceptPage.getStatus()).toEqual('Concept created.');
        });

        it('#341 concept edit - deleting description field should not get error', function () {
            conceptPage.createConceptFullySpecifiedRandomly();
            conceptPage.prepareToEditConcept();

            conceptPage.deleteDescriptionArea();

            conceptPage.updateButton.click();
            expect(conceptPage.getStatus()).toEqual('Concept updated');
        });

        it('#342 concept edit - basic validation order at least one fully specified name', function () {
            conceptPage.createConceptFullySpecifiedRandomly();
            conceptPage.prepareToEditConcept();

            conceptPage.setNameType(conceptPage.getNamesAndSynonyms().first(), 'Short');

            conceptPage.updateButton.click();
            expect(conceptPage.getError()).toEqual('A concept must have at least one fully specified name (across all locales)');
        });

        it('#342 concept edit - source validation order preferred name should be unique', function () {
            conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name35");
            conceptPage.createConceptFullySpecifiedRandomly();
            conceptPage.prepareToEditConcept();

            conceptPage.setNameText(conceptPage.getNamesAndSynonyms().first(), 'name35');

            conceptPage.updateButton.click();
            expect(conceptPage.getError()).toEqual('Concept preferred name must be unique for same source and locale');
        });

        afterAll(function () {
            element(by.css('.resource-label.user')).click();
        });

    });



    describe('concept - openmrs validations', function () {

        beforeAll(function () {
            // Create Source with openMRS
            srcShortCode = orgPage.getRandomShortCode();
            usrSrcPage.createNewUsrSource(
                data.src_code + srcShortCode,
                data.src_full_name,
                data.supported_locale,
                'OpenMRS'
            );
        });

        describe('create with openmrs validation', function () {

            it('#241 concept create with more then one preferred name should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setNameText(names.first(), conceptPage.getRandomName());
                conceptPage.setLocalePreferred(names.first(), true);

                conceptPage.setNameText(names.last(), conceptPage.getRandomName());
                conceptPage.setLocalePreferred(names.last(), true);

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#241 concept create with short preferred name should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();
                conceptPage.setName(names.first(), conceptPage.getRandomName(), "Fully Specified", false);
                conceptPage.setName(names.last(), conceptPage.getRandomName(), "Short", true);

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();
                expect(conceptPage.getError()).toEqual('A short name cannot be marked as locale preferred');
            });

            it('#241 concept create with more then one preferred name should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);

                conceptPage.getNamesAndSynonyms().each(function (item) {
                    conceptPage.setName(item, conceptPage.getRandomName(), "Fully Specified", true);
                });

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();
                expect(conceptPage.getError()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#242 concept create with same preferred name in same source & locale should get an error', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "sameName");

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "sameName");

                expect(conceptPage.getError()).toEqual('Concept preferred name must be unique for same source and locale');

            });

            it('#242 concept create with same fully specified name in same source & locale should get an error', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "sameFullySpecified");

                conceptPage.prepareToCreateConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setName(names.first(), "requiredFullySpecified", "Fully Specified", true);
                conceptPage.setName(names.last(), "sameFullySpecified", "Fully Specified", false);

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('A concept may not have more than one fully specified name in any locale');

            });

            it('#341 concept create - deleting description field should not get error', function () {
                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                conceptPage.deleteDescriptionArea();
                conceptPage.createConcept();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            it('#335 concept create with more then one fully specified name in same source & locale should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), conceptPage.getRandomName(), "Fully Specified", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('A concept may not have more than one fully specified name in any locale');
            });

            it('#335 concept create without fully specified name should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('A concept must have at least one fully specified name (across all locales)');
            });

            it('#335 concept create with more then one preferred name should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), conceptPage.getRandomName(), "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#335 concept create with preferred short name should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", false, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), conceptPage.getRandomName(), "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('A short name cannot be marked as locale preferred');
            });

            it('#335 concept create with 2 non-short names having the same text should get an error', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), "sameText", "Fully Specified", true, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), "sameText", "Fully Specified", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual('All names except short names must unique for a concept and locale');
            });

            it('#335 concept create with 2 non-short & short names having the same text should be created successfully', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), "sameText", "Fully Specified", true, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), "sameText", "Short", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

        });

        describe('concept edit with openmrs validation', function () {

            it('#278 concept edit with more then one preferred name should get an error', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name1");

                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                var nameInput = conceptPage.namesDiv.element(by.css('.name-content'));

                nameInput.clear().sendKeys('name1');

                conceptPage.updateButton.click();

                expect(conceptPage.getError()).toEqual('Concept preferred name must be unique for same source and locale');
            });

            it('#278 concept edit adding one preferred name should get an error', function () {

                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = element.all(by.repeater('name in names'));

                conceptPage.setName(names.last(), conceptPage.getRandomName(), "Short", true);

                conceptPage.updateButton.click();

                expect(conceptPage.getError()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#278 concept edit adding one preferred short name should get an error', function () {

                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();
                conceptPage.setLocalePreferred(names.first(), false);

                conceptPage.setName(names.last(), conceptPage.getRandomName(), "Short", true);

                conceptPage.updateButton.click();

                expect(conceptPage.getError()).toEqual('A short name cannot be marked as locale preferred');
            });

            it('#278 concept edit with same fully specified name in same source & locale should get an error', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "fullySpecified1");
                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setName(names.last(), "fullySpecified1", "Fully Specified", false);

                conceptPage.updateButton.click();
                expect(conceptPage.getError()).toEqual('A concept may not have more than one fully specified name in any locale');

            });

            it('#341 concept edit - deleting description field should not get error', function () {
                conceptPage.createConceptFullySpecifiedRandomly();
                conceptPage.prepareToEditConcept();

                conceptPage.deleteDescriptionArea();

                conceptPage.updateButton.click();
                expect(conceptPage.getStatus()).toEqual('Concept updated');
            });

            it('#341 concept create without description - edit no ', function () {
                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                conceptPage.deleteDescriptionArea();

                conceptPage.createConcept();

                conceptPage.prepareToEditConcept();

                conceptPage.updateButton.click();
                expect(conceptPage.getStatus()).toEqual('Concept updated');
            });

        });

    });

    afterAll(function () {
        logoutPage.logout();
    });
});



