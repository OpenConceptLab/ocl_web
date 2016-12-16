'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var conceptPage = require('../pages/concept_page');
var configuration = require('../utilities/configuration.js');

var fs = require('fs');

function writeScreenShot(data, filename) {
    var stream = fs.createWriteStream(filename);
    stream.write(new Buffer(data, 'base64'));
    stream.end();
}


const ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT = 'A concept must have at least one fully specified name (across all locales)';
const PREFERRED_NAME_UNIQUE_PER_SOURCE_LOCALE = 'Concept preferred name must be unique for same source and locale';
const FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE = 'Concept fully specified name must be unique for same source and locale';
const SHORT_NAME_CANNOT_BE_PREFERRED = 'A short name cannot be marked as locale preferred';
const NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE = 'A concept may not have more than one fully specified name in any locale';
const NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE = 'A concept may not have more than one preferred name (per locale)';
const NON_SHORT_NAMES_MUST_BE_UNIQUE = 'All names except short names must be unique for a concept and locale';

function addNameDetailsToWarning(warning, name, locale, preferred) {
    return warning + ': ' + name + ' (locale: ' + locale + ', preferred: ' + (preferred ? 'yes' : 'no') + ')';
}

describe('Concept', function () {
    var loginPage = new LoginPage();
    var logoutPage = new LogoutPage();
    var usrSrcPage = new UserSourcePage();
    var srcShortCode = '';

    browser.ignoreSynchronization = true;

    beforeAll(function () {
        loginPage.login();
    });

    describe('// Basic validation //', function () {

        beforeAll(function () {
            // Create Source
            srcShortCode = conceptPage.getRandomShortCode();
            usrSrcPage.createNewUsrSource(
                data.src_code + srcShortCode,
                data.src_full_name,
                data.supported_locale,
                'None'
            );
        });

        describe('Create // ', function () {
            it('same names with different locales should not get an error #238', function () {
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

            it('deleting description field should not get error #341', function () {
                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                conceptPage.deleteDescriptionArea();
                conceptPage.createConcept();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            it('form should retain data after unsuccessful creation #352', function () {
                var expectedName = conceptPage.getRandomName();

                conceptPage.prepareToCreateConcept();
                conceptPage.setConceptId(expectedName);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, "Short", true, "English [en]");
                conceptPage.createConcept();

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setConceptId(expectedName);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getNameText(conceptPage.getNamesAndSynonyms().first())).toEqual(expectedName);
                expect(conceptPage.getNameType(conceptPage.getNamesAndSynonyms().first())).toContain('Short');
            });
        });


        describe('Edit //', function () {

            it('deleting description field should not get error #341', function () {
                conceptPage.createConceptFullySpecifiedRandomly();
                conceptPage.prepareToEditConcept();

                conceptPage.deleteDescriptionArea();

                conceptPage.updateConcept();
                expect(conceptPage.getStatus()).toEqual('Concept updated');
            });

            it('form should retain data after unsuccessful editing #352 ', function () {
                var expectedName = conceptPage.getRandomName();
                var conceptNameArea = conceptPage.getNamesAndSynonyms().first();
                var expectedNameType = 'Short';

                conceptPage.createConceptFullySpecifiedRandomly();
                conceptPage.prepareToEditConcept();
                conceptPage.fillInUpdateText('');
                conceptPage.setNameType(conceptNameArea, expectedNameType);
                conceptPage.setNameText(conceptNameArea, expectedName);
                conceptPage.updateConcept();

                expect(conceptPage.getNameText(conceptNameArea)).toEqual(expectedName);
                expect(conceptPage.getNameType(conceptNameArea)).toContain(expectedNameType);
            });
        });


        afterAll(function () {
            conceptPage.returnToHomePage();
        });

    });

    describe('// OpenMRS validations // ', function () {

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

        describe('Create // ', function () {

            it('with more than one preferred name should get an error (#241)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setNameText(names.first(), conceptPage.getRandomName());
                conceptPage.setLocalePreferred(names.first(), true);

                const randomName = conceptPage.getRandomName();
                conceptPage.setNameText(names.last(), randomName);
                conceptPage.setLocalePreferred(names.last(), true);

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE, randomName, 'ab', true));
            });

            it('with short preferred name should get an error (#241)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();
                conceptPage.setName(names.first(), conceptPage.getRandomName(), "Fully Specified", false);
                const randomName = conceptPage.getRandomName();
                conceptPage.setName(names.last(), randomName, "Short", true);

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();
                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(SHORT_NAME_CANNOT_BE_PREFERRED, randomName, 'en', true));
            });

            it('with same preferred name in same source & locale should get an error (#242)', function () {
                var expectedName = 'sameName';
                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), expectedName);
                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), expectedName);
                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE,expectedName,'en',true));

            });

            it('with same fully specified name in same source & locale should get an error (#242)', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "sameFullySpecified");

                conceptPage.prepareToCreateConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setName(names.first(), "requiredFullySpecified", "Fully Specified", true);
                conceptPage.setName(names.last(), "sameFullySpecified", "Fully Specified", false);

                conceptPage.fillDescriptionField();

                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE, 'sameFullySpecified', 'en', false));

            });

            it('deleting description field should not get error (#341)', function () {
                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                conceptPage.deleteDescriptionArea();
                conceptPage.createConcept();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            it('with more then one fully specified name in same source & locale should get an error (#335)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                const randomName = conceptPage.getRandomName();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), randomName, "Fully Specified", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE, randomName, 'en', false));
            });

            it('without fully specified name should get an error (#335)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Short", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('with more then one preferred name should get an error (#335)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", true, "English [en]");
                const randomName = conceptPage.getRandomName();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), randomName, "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE, randomName, 'en', true));
            });

            it('with preferred short name should get an error (#335)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Fully Specified", false, "English [en]");
                const randomName = conceptPage.getRandomName();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), randomName, "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(SHORT_NAME_CANNOT_BE_PREFERRED, randomName, 'en', true));
            });

            it('with 2 non-short names having the same text should get an error (#335)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), "sameText", "Fully Specified", true, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), "sameText", "Fully Specified", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(NON_SHORT_NAMES_MUST_BE_UNIQUE);
            });

            it('with 2 non-short & short names having the same text should be created successfully (#335)', function () {

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), "sameText", "Fully Specified", true, "English [en]");
                conceptPage.setName(conceptPage.getNamesAndSynonyms().last(), "sameText", "Short", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            it('form should retain data after unsuccessful creation #352', function () {
                var expectedName = conceptPage.getRandomName();

                conceptPage.prepareToCreateConcept();
                conceptPage.setConceptId(expectedName);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, "Short", true, "English [en]");
                conceptPage.createConcept();

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setConceptId(expectedName);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getNameText(conceptPage.getNamesAndSynonyms().first())).toEqual(expectedName);
                expect(conceptPage.getNameType(conceptPage.getNamesAndSynonyms().first())).toContain('Short');
            });

            it('order at least one fully specified name #342', function () {
                conceptPage.prepareToCreateConcept();
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), conceptPage.getRandomName(), "Short", false, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('source validation order preferred and fully specified name should be unique #342', function () {
                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name33");
                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name33");

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, 'name33', 'en', true));
            });
        });

        describe('Edit', function () {

            it('with more then one preferred and fully specified name should get an error #278', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name1");

                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setNameText(names.first(), "name1");

                conceptPage.updateConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, 'name1', 'en', true));
            });

            it('order at least one fully specified name #342', function () {
                var expectedName = conceptPage.getRandomName();
                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), expectedName);
                conceptPage.prepareToEditConcept();

                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, 'Short', false);

                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('adding one preferred name should get an error #278', function () {

                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                const randomName = conceptPage.getRandomName();
                conceptPage.setName(names.last(), randomName, "Short", true);

                conceptPage.updateConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE, randomName, 'en', true));
            });

            it('adding one preferred short name should get an error #278', function () {

                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();
                conceptPage.setLocalePreferred(names.first(), false);

                const randomName = conceptPage.getRandomName();
                conceptPage.setName(names.last(), randomName, "Short", true);

                conceptPage.updateConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(SHORT_NAME_CANNOT_BE_PREFERRED, randomName, 'en', true));
            });

            it('with same fully specified name in same source & locale should get an error #278', function () {

                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "fullySpecified1");
                conceptPage.createConceptFullySpecifiedRandomly();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setName(names.last(), "fullySpecified1", "Fully Specified", false);

                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE, 'fullySpecified1', 'en', false));

            });

            it('deleting fully specified name should get corresponding error #338', function () {
                conceptPage.createConceptFullySpecifiedRandomly();
                conceptPage.prepareToEditConcept();

                conceptPage.deleteNameArea();

                conceptPage.updateConcept();

                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('deleting description field should not get error #341', function () {
                conceptPage.createConceptFullySpecifiedRandomly();
                conceptPage.prepareToEditConcept();

                conceptPage.deleteDescriptionArea();

                conceptPage.updateConcept();
                expect(conceptPage.getStatus()).toEqual('Concept updated');
            });

            it('source validation order preferred and fully specified name should be unique #342', function () {
                conceptPage.createConceptWithFullySpecifiedName(conceptPage.getRandomId(), "name35");
                conceptPage.createConceptFullySpecifiedRandomly();
                conceptPage.prepareToEditConcept();

                conceptPage.setNameText(conceptPage.getNamesAndSynonyms().first(), 'name35');

                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, 'name35', 'en', true));
            });

            it('form should retain data after unsuccessful editing #352 ', function () {
                var expectedName = conceptPage.getRandomName();

                conceptPage.prepareToCreateConcept();
                conceptPage.setConceptId(expectedName);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, "Short", true, "English [en]");
                conceptPage.createConcept();

                conceptPage.prepareToCreateConcept();
                conceptPage.addNamesAndSynonyms(1);
                conceptPage.setConceptId(expectedName);
                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, "Short", true, "English [en]");
                conceptPage.fillDescriptionField();
                conceptPage.createConcept();

                expect(conceptPage.getNameText(conceptPage.getNamesAndSynonyms().first())).toEqual(expectedName);
                expect(conceptPage.getNameType(conceptPage.getNamesAndSynonyms().first())).toContain('Short');
            });
        });
    });

    afterAll(function () {
        logoutPage.logout();
    });
});



