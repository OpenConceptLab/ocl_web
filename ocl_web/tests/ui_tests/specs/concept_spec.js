'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var OrgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var ConceptEditPage = require('../pages/concept_edit_page');
var ConceptCreatePage = require('../pages/concept_create_page');
var configuration = require('../utilities/configuration.js');

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

            expect(getErrorText()).toEqual('A concept must have at least one fully specified name (across all locales)');

            conceptEditPage.cancelUpdateButton.click();

        });

        it('should edit the concept 2, change the name to be same as concept 1 and get an error', function () {
            element(by.id("edit-concept")).click();

            conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
            var nameInput = conceptEditPage.namesDiv.element(by.css('.name-content'));

            // PAIN!
            nameInput.sendKeys(protractor.Key.BACK_SPACE + '1');
            conceptEditPage.updateButton.click();

            expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');

            conceptEditPage.cancelUpdateButton.click();
        });

        it('#238 concept create - same names with different locales should not get an error', function () {
            prepareToCreateConcept();

            setConceptId("29");
            addNamesAndSynonyms(1);

            var names = getNamesAndSynonyms();
            setName(names.first(), "en_fr_name", "Short", false, "French [fr]");
            setName(names.last(), "name2", "Fully Specified", false, "English [en]");

            element(by.model('description.description')).sendKeys("desc");
            createConcept();

            createConceptWithFullySpecifiedName("30", "en_fr_name")
            expect((orgPage.status).getText()).toEqual('Concept created.');
        });

        it('#342 concept create - basic validation order at least one fully specified name', function () {
            prepareToCreateConcept();
            setConceptId("32");
            setName(getNamesAndSynonyms().first(), "sdfsdf", "Short", true, "English [en]");
            element(by.model('description.description')).sendKeys("desc");
            createConcept();

            expect(getErrorText()).toEqual('A concept must have at least one fully specified name (across all locales)');
        });

        it('#342 concept create - source validation order preferred name should be unique', function () {
            createConceptWithFullySpecifiedName("33", "name33");
            createConceptWithFullySpecifiedName("34", "name33");

            expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');
        });

        it('#342 concept edit - basic validation order at least one fully specified name', function () {
            createConceptWithFullySpecifiedName("34", "askjhdsajkhdkjsahd");
            element(by.id("edit-concept")).click();

            conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
            setNameType(getNamesAndSynonyms().first(), 'Short')

            conceptEditPage.updateButton.click();
            expect(getErrorText()).toEqual('A concept must have at least one fully specified name (across all locales)');
        });

        it('#342 concept edit - source validation order preferred name should be unique', function () {
            createConceptWithFullySpecifiedName("35", "name35");
            createConceptWithFullySpecifiedName("36", "name36");
            element(by.id("edit-concept")).click();

            conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
            setNameText(getNamesAndSynonyms().first(), 'name35')

            conceptEditPage.updateButton.click();
            expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');
        });

        afterAll(function () {
            element(by.css('.resource-label.user')).click();
        });

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
        item.element(by.model('name.name')).clear().sendKeys(name);
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

    function setNameLocale(item, option) {
        if (option === undefined) {
            option = "English [en]"
        }
        item.element(by.model('name.locale')).element(by.cssContainingText("option", option)).click();
    }

    function setName(item, nameText, nameType, localePreferred, nameLocale) {
        setNameText(item, nameText);
        setNameType(item, nameType);
        setLocalePreferred(item, localePreferred);
        setNameLocale(item, nameLocale)
    }

    function createConcept() {
        conceptCreatePage.createButton.click();
    }

    function getErrorText() {
        return conceptCreatePage.errorBox.getText();
    }

    function createConceptWithFullySpecifiedName(id, name) {
        prepareToCreateConcept();
        setConceptId(id);
        setName(getNamesAndSynonyms().first(), name, "Fully Specified", true, "English [en]");
        element(by.model('description.description')).sendKeys("desc");
        createConcept();
    }

    describe('concept - openmrs validations', function () {

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

        describe('create with openmrs validation', function () {

            it('#241 concept create with more then one preferred name should get an error', function () {

                prepareToCreateConcept();
                setConceptId("1");
                addNamesAndSynonyms(1);

                var names = getNamesAndSynonyms();

                setNameText(names.first(), "name1");
                setLocalePreferred(names.first(), true);

                setNameText(names.last(), "name2");
                setLocalePreferred(names.last(), true);

                element(by.model('description.description')).sendKeys("desc");

                createConcept();

                expect(getErrorText()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#241 concept create with short preferred name should get an error', function () {

                prepareToCreateConcept();

                setConceptId("1");
                addNamesAndSynonyms(1);

                var names = getNamesAndSynonyms();
                setName(names.first(), "name1", "Fully Specified", false);
                setName(names.last(), "name2", "Short", true);

                element(by.model('description.description')).sendKeys("desc");

                createConcept();
                expect(getErrorText()).toEqual('A short name cannot be marked as locale preferred');
            });

            it('#241 concept create with more then one preferred name should get an error', function () {

                prepareToCreateConcept();

                setConceptId("1");
                addNamesAndSynonyms(1);

                getNamesAndSynonyms().each(function (item) {
                    setName(item, "name", "Fully Specified", true);
                });

                element(by.model('description.description')).sendKeys("desc");

                createConcept();
                expect(getErrorText()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#242 concept create with same preferred name in same source & locale should get an error', function () {

                createConceptWithFullySpecifiedName("2", "sameName");

                createConceptWithFullySpecifiedName("3", "sameName");

                expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');

            });

            it('#242 concept create with same fully specified name in same source & locale should get an error', function () {

                createConceptWithFullySpecifiedName("3", "sameFullySpecified");

                prepareToCreateConcept();

                setConceptId("4");

                addNamesAndSynonyms(1);

                var names = getNamesAndSynonyms();

                setName(names.first(), "requiredFullySpecified", "Fully Specified", true);
                setName(names.last(), "sameFullySpecified", "Fully Specified", false);

                element(by.model('description.description')).sendKeys("desc");

                createConcept();

                expect(getErrorText()).toEqual('A concept may not have more than one fully specified name in any locale');

            });

        });

        describe('concept edit with openmrs validation', function () {

            it('#278 concept edit with more then one preferred name should get an error', function () {

                createConceptWithFullySpecifiedName("21", "name1");

                createConceptWithFullySpecifiedName("22", "name2");

                element(by.id("edit-concept")).click();

                conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));

                var nameInput = conceptEditPage.namesDiv.element(by.css('.name-content'));

                nameInput.clear().sendKeys('name1');

                conceptEditPage.updateButton.click();

                expect(getErrorText()).toEqual('Concept preferred name must be unique for same source and locale');
            });

            it('#278 concept edit adding one preferred name should get an error', function () {

                createConceptWithFullySpecifiedName("25", "gdgdgdbgd");

                element(by.id("edit-concept")).click();

                conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));

                addNamesAndSynonyms(1);

                var names = element.all(by.repeater('name in names'));

                setName(names.last(), "bmvshdg", "Short", true);

                conceptEditPage.updateButton.click();

                expect(getErrorText()).toEqual('A concept may not have more than one preferred name (per locale)');
            });

            it('#278 concept edit adding one preferred short name should get an error', function () {

                createConceptWithFullySpecifiedName("24", "name24");

                element(by.id("edit-concept")).click();

                addNamesAndSynonyms(1);

                var names = getNamesAndSynonyms();
                setLocalePreferred(names.first(), false);

                setName(names.last(), "shortName", "Short", true);

                conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));

                conceptEditPage.updateButton.click();

                expect(getErrorText()).toEqual('A short name cannot be marked as locale preferred');
            });

            it('#278 concept edit with same fully specified name in same source & locale should get an error', function () {

                createConceptWithFullySpecifiedName("27", "fullySpecified1");
                createConceptWithFullySpecifiedName("28", "fullySpecified2");

                element(by.id("edit-concept")).click();

                addNamesAndSynonyms(1);

                var names = getNamesAndSynonyms();

                setName(names.last(), "fullySpecified1", "Fully Specified", false);

                conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
                conceptEditPage.updateButton.click();
                expect(getErrorText()).toEqual('A concept may not have more than one fully specified name in any locale');

            });

        });

    });

    afterAll(function () {
        logoutPage.logout();
    });
});



