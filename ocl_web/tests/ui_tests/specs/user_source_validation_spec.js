'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var ConceptPage = require('../pages/concept_page');
var configuration = require('../utilities/configuration.js');
const baseUrl = configuration.get('baseUrl');
const username = configuration.get('username');
const timeout = configuration.get('timeout');

describe('OCL User Source Validation Page', function () {
    var loginPage;
    var logoutPage;
    var usrSrcPage;
    var srcShortCode = '';
    var conceptPage = '';

    beforeAll(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        usrSrcPage = new UserSourcePage();
        conceptPage = ConceptPage;
        loginPage.login();
        return browser.ignoreSynchronization = true;
    });

    afterAll(function () {
        logoutPage.logout();
    });

    it('should create source with OpenMRS validation', function () {
        srcShortCode = orgPage.getRandomShortCode();
        usrSrcPage.createNewUsrSource(
            data.src_code + srcShortCode,
            data.src_full_name,
            data.supported_locale,
            data.custom_validation_schema
        );

        expect(orgPage.getStatus()).toEqual('Source created');
        expect((orgPage.customValidationSchema).getText()).toEqual('OpenMRS')
    });

    describe('when changing schema from None to OpenMRS', function(){
        var concept1Id = 'Concept1';
        var concept2Id = 'Concept2';

        var basicValidationSourceId = data.src_code + srcShortCode + orgPage.getRandomShortCode();

        beforeAll(function(){
            var userNewSourcePath = baseUrl + 'users/' + username;
            browser.get(userNewSourcePath);

            // create a basic validation source
            usrSrcPage.createNewUsrSource(
                basicValidationSourceId,
                data.src_full_name,
                data.supported_locale
            );

            conceptPage.createConceptWithFullySpecifiedName(concept1Id, 'Grip');
            conceptPage.createConceptWithFullySpecifiedName(concept2Id, 'Grip');

            conceptPage.parentSourceLink.click();

        });

        afterAll(function(){
            var basicSourceEditURL = baseUrl + 'users/' + username + '/sources/' + basicValidationSourceId + '/edit/';
            browser.get(basicSourceEditURL);
            usrSrcPage.deleteSourceButton.click();
            usrSrcPage.confirmDeleteSourceButton.click();

            element(by.css('.ajs-button.ajs-ok')).click();

        });

        it('should display list of failed validations given invalid concepts', function(){
            usrSrcPage.editUserSourceButton.click();
            usrSrcPage.setCustomValidationSchema(data.custom_validation_schema);
            usrSrcPage.updateUserSourceButton.click();

            expect(usrSrcPage.failedValidationsPopup.isDisplayed()).toBeTruthy()
        });

        it('should display number of failed concepts on the title', function(){
            var title = usrSrcPage.failedValidationsPopup.element(by.css('.modal-title'));
            expect(title.getText()).toEqual('2 concepts failed validation against OpenMRS');
        });

        it('should contain two errors given two invalid concepts', function(){
            var tableRows = usrSrcPage.failedValidationsPopup
                .element(by.tagName('tbody'))
                .all(by.tagName('tr'));

            expect(tableRows.count()).toBe(2);

        });

        it('should have a download as csv button', function(){
            var downloadCSVButton = usrSrcPage.failedValidationsPopup
                .element(by.linkText('Download as CSV'));

            expect(downloadCSVButton.isDisplayed).toBeTruthy();
            element(by.id('close-modal')).click()

        });


        xit('should succeed when an invalid concept is fixed', function(){
            var concept1EditUrl = baseUrl + 'users/' + username + '/sources/' + basicValidationSourceId + '/concepts/' + concept1Id + '/edit/';

            browser.get(concept1EditUrl);

            conceptPage.setNameText(conceptPage.getNamesAndSynonyms().first(), 'NewGrip');
            conceptPage.fillInUpdateTextRandomly();
            conceptPage.updateConcept();
            expect(conceptPage.getStatus()).toEqual('Concept updated');

            // Go back to source edit
            conceptPage.parentSourceLink.click();
            usrSrcPage.editUserSourceButton.click();
            usrSrcPage.setCustomValidationSchema(data.custom_validation_schema);
            usrSrcPage.updateUserSourceButton.click();

            expect(usrSrcPage.successMessage.getText()).toEqual('Source updated')
        })
    });

});

