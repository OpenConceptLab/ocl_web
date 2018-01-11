'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var conceptPage = require('../pages/concept_page');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;

const timeout = configuration.get('timeout');
const ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT = 'A concept must have at least one fully specified name';
const CONCEPT_MUST_HAVE_AT_LEAST_ONE_NAME = 'A concept must have at least one name';
const FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE = 'Concept fully specified name must be unique for same source and locale';
const SHORT_NAME_CANNOT_BE_PREFERRED = 'A short name cannot be marked as locale preferred';
const NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE = 'A concept may not have more than one fully specified name in any locale';
const NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE = 'A concept may not have more than one preferred name (per locale)';
const NON_SHORT_NAMES_MUST_BE_UNIQUE = 'All names except short names must be unique for a concept and locale';

function addNameDetailsToWarning(warning, name, locale, preferred) {
    return warning + ': ' + name + ' (locale: ' + locale + ', preferred: ' + (preferred ? 'yes' : 'no') + ')';
}

var ConceptBuilder = function () {

    var id;
    var nameAndSynonym;
    var nameText;
    var nameType;
    var localePreferred;
    var nameLocale;

    return {
        prepareConceptPage: function () {
            conceptPage.prepareToCreateConcept();
            return this;
        },

        addNamesAndSynonyms: function (count) {
            conceptPage.addNamesAndSynonyms(count);
            return this;
        },

        setId: function (id) {
            this.id = id;
            return this;
        },

        setNameText: function (nameText) {
            this.nameText = nameText;
            return this;
        },

        setNameType: function (nameType) {
            this.nameType = nameType;
            return this;
        },

        setLocalePreferred: function (localePreferred) {
            this.localePreferred = localePreferred;
            return this;
        },

        setNameLocale: function (nameLocale) {
            this.nameLocale = nameLocale;
            return this;
        },

        setNameAndSynonym: function (nameAndSynonym) {
            this.nameAndSynonym = nameAndSynonym;
            return this;
        },

        fillDescriptionField: function () {
            conceptPage.fillDescriptionField();
            return this;
        },

        deleteDescriptionArea: function () {
            conceptPage.deleteDescriptionArea();
            return this;
        },

        fillToFields: function () {
            conceptPage.setName(this.nameAndSynonym, this.nameText, this.nameType, this.localePreferred, this.nameLocale);
            conceptPage.setConceptId(this.id == undefined ? conceptPage.getRandomId() : this.id);
            return this;
        },

        build: function () {
            conceptPage.createConcept();
        }
    };
};

describe('Concept', function () {
    var loginPage = new LoginPage();
    var logoutPage = new LogoutPage();
    var usrSrcPage = new UserSourcePage();
    var srcShortCode = '';
    var conceptBuilder = new ConceptBuilder();

    beforeAll(function () {
        loginPage.login();
        browser.ignoreSynchronization = true;
    });

    describe('Basic validation', function () {

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

        describe('Create', function () {
            it('same names with different locales should not get an error #238', function () {
                var names = conceptPage.getNamesAndSynonyms();

                conceptBuilder
                    .prepareConceptPage()
                    .setNameAndSynonym(names.first())
                    .setNameText(conceptPage.getRandomName())
                    .setLocalePreferred(false)
                    .setNameType('Short')
                    .setNameLocale("fr")
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setNameAndSynonym(names.last())
                    .setNameText(conceptPage.getRandomName())
                    .setLocalePreferred(false)
                    .setNameType('Fully Specified')
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            xit('should have combobox with values in concept mapping creation form', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setLocalePreferred(false)
                    .setNameType('Fully Specified')
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                conceptPage.clickMappings();
                var firstMapType = conceptPage.mapTypes.first();
                expect(firstMapType.getText()).not.toBeUndefined();
            });

            it('form should retain data after unsuccessful creation #352', function () {
                var expectedName = conceptPage.getRandomName();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(expectedName)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setLocalePreferred(true)
                    .setNameType('Short')
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(expectedName)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setLocalePreferred(true)
                    .setNameType('Short')
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getNameText(conceptPage.getNamesAndSynonyms().first())).toEqual(expectedName);
                expect(conceptPage.getNameType(conceptPage.getNamesAndSynonyms().first())).toContain('Short');
            });
        });

        describe('Concept Page', function () {
            it('add to collection button should add the concept to collection when user specifies', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setLocalePreferred(true)
                    .setNameType('Fully Specified')
                    .setNameLocale('en')
                    .fillDescriptionField()
                    .fillToFields()
                    .build();

                conceptPage.addConceptToFirstCollection();

                browser.wait(EC.visibilityOf(conceptPage.confirmButton), timeout);

                conceptPage.confirmWithoutCascade();

                browser.wait(EC.visibilityOf(conceptPage.alertBox), timeout);

                const alertBoxText = conceptPage.alertBox.getText();

                expect(alertBoxText).toEqual('Added the latest versions of concept to the collection. Future updates will not be added automatically.');
            });
        });


        describe('Edit', function () {
            it('deleting description field should not get error #341', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setLocalePreferred(true)
                    .setNameType('Fully Specified')
                    .setNameLocale('en')
                    .fillDescriptionField()
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();

                conceptPage.deleteDescriptionArea();
                conceptPage.updateConcept();
                expect(conceptPage.getStatus()).toEqual('Concept updated');
            });

            it('form should retain data after unsuccessful editing #352 ', function () {
                var expectedName = conceptPage.getRandomName();
                var conceptNameArea = conceptPage.getNamesAndSynonyms().first();
                var expectedNameType = 'Short';

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptNameArea)
                    .setNameText(expectedName)
                    .setLocalePreferred(false)
                    .setNameType("Fully Specified")
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

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

    describe('OpenMRS validations', function () {

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

        describe('Create', function () {

            it('with more than one preferred name should get an error (#241)', function () {

                conceptBuilder
                    .prepareConceptPage()
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setLocalePreferred(true)
                    .setNameType('Fully Specified')
                    .setNameLocale('fr')
                    .fillToFields();

                var randomName = conceptPage.getRandomName();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText(randomName)
                    .setLocalePreferred(true)
                    .setNameType('Fully Specified')
                    .setNameLocale('fr')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE, randomName, 'fr', true));
            });

            it('with short preferred name should get an error (#241)', function () {
                var names = conceptPage.getNamesAndSynonyms();
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(names.first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Fully Specified')
                    .setLocalePreferred(false)
                    .setNameLocale('fr')
                    .fillToFields()
                    .build();

                const randomName = conceptPage.getRandomName();
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(names.last())
                    .setNameText(randomName)
                    .setNameType('Short')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(SHORT_NAME_CANNOT_BE_PREFERRED, randomName, 'en', true));
            });

            it('with same preferred name in same source & locale should get an error (#242)', function () {
                var expectedName = 'sameName';

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, expectedName, 'en', true));

            });

            it('with same fully specified name in same source & locale should get an error (#242)', function () {

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('sameFullySpecified')
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("fr")
                    .fillToFields();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('requiredFullySpecified')
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("fr")
                    .fillToFields();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText('sameFullySpecified')
                    .setNameType("Fully Specified")
                    .setLocalePreferred(false)
                    .setNameLocale("fr")
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE, 'sameFullySpecified', 'fr', false));
            });

            it('deleting description field should not get error (#341)', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .deleteDescriptionArea()
                    .build();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            it('with more then one fully specified name in same source & locale should get an error (#335)', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields();

                const randomName = conceptPage.getRandomName();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText(randomName)
                    .setNameType('Fully Specified')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE, randomName, 'en', false));
            });

            it('without fully specified name should get an error (#335)', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Short')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('with more then one preferred name should get an error (#335)', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields();

                const randomName = conceptPage.getRandomName();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText(randomName)
                    .setNameType('Short')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE, randomName, 'en', true));
            });

            it('with preferred short name should get an error (#335)', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Fully Specified')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields();

                const randomName = conceptPage.getRandomName();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText(randomName)
                    .setNameType('Short')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(SHORT_NAME_CANNOT_BE_PREFERRED, randomName, 'en', true));
            });

            it('with 2 non-short names having the same text should get an error (#335)', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('sameText')
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText('sameText')
                    .setNameType('Fully Specified')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(NON_SHORT_NAMES_MUST_BE_UNIQUE);
            });

            it('with 2 non-short & short names having the same text should be created successfully (#335)', function () {

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .addNamesAndSynonyms(1)
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('sameText')
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields();

                conceptBuilder
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText('sameText')
                    .setNameType('Short')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getStatus()).toEqual('Concept created.');
            });

            it('form should retain data after unsuccessful creation #352', function () {
                var expectedName = conceptPage.getRandomName();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setNameType('Short')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setNameType('Short')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getNameText(conceptPage.getNamesAndSynonyms().first())).toEqual(expectedName);
                expect(conceptPage.getNameType(conceptPage.getNamesAndSynonyms().first())).toContain('Short');
            });

            it('order at least one fully specified name #342', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType('Short')
                    .setLocalePreferred(false)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('source validation order preferred and fully specified name should be unique #342', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('name33')
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('name33')
                    .setNameType('Fully Specified')
                    .setLocalePreferred(true)
                    .setNameLocale('en')
                    .fillToFields()
                    .build();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, 'name33', 'en', true));
            });
        });

        describe('Edit', function () {

            it('with more then one preferred and fully specified name should get an error #278', function () {

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText('name1')
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().last())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setNameText(names.first(), "name1");

                conceptPage.updateConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, 'name1', 'en', true));
            });

            it('order at least one fully specified name #342', function () {
                var expectedName = conceptPage.getRandomName();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(expectedName)
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();

                conceptPage.setName(conceptPage.getNamesAndSynonyms().first(), expectedName, 'Short', false);

                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(ONE_FULLY_SPECIFIED_NAME_PER_CONCEPT);
            });

            it('adding one preferred name should get an error #278', function () {

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                const randomName = conceptPage.getRandomName();
                conceptPage.setName(names.last(), randomName, "Short", true);

                conceptPage.updateConcept();

                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_PREFERRED_NAME_PER_LOCALE, randomName, 'en', true));
            });

            it('adding one preferred short name should get an error #278', function () {

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

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
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText("fullySpecified1")
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();

                conceptPage.addNamesAndSynonyms(1);

                var names = conceptPage.getNamesAndSynonyms();

                conceptPage.setName(names.last(), "fullySpecified1", "Fully Specified", false);

                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(NO_MORE_THAN_ONE_FULLY_SPECIFIED_PER_LOCALE, 'fullySpecified1', 'en', false));

            });

            it('deleting fully specified name should get corresponding error #338', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();
                conceptPage.deleteNameArea();
                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(CONCEPT_MUST_HAVE_AT_LEAST_ONE_NAME);
            });

            xit('deleting description field should not get error #341', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillDescriptionField()
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();
                conceptPage.deleteDescriptionArea();
                conceptPage.updateConcept();
                expect(conceptPage.getStatus()).toEqual('Concept updated');
            });

            it('source validation order preferred and fully specified name should be unique #342', function () {
                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText('name35')
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptBuilder
                    .prepareConceptPage()
                    .setId(conceptPage.getRandomId())
                    .setNameAndSynonym(conceptPage.getNamesAndSynonyms().first())
                    .setNameText(conceptPage.getRandomName())
                    .setNameType("Fully Specified")
                    .setLocalePreferred(true)
                    .setNameLocale("en")
                    .fillToFields()
                    .build();

                conceptPage.prepareToEditConcept();

                conceptPage.setNameText(conceptPage.getNamesAndSynonyms().first(), 'name35');

                conceptPage.updateConcept();
                expect(conceptPage.getError()).toEqual(addNameDetailsToWarning(FULLY_SPECIFIED_NAME_UNIQUE_PER_SOURCE_LOCALE, 'name35', 'en', true));
            });
        });
    });

    afterAll(function () {
        logoutPage.logout();
    });
});
