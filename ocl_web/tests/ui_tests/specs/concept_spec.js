'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var OrgPage = require('../pages/organization_page');
var UserSourcePage = require('../pages/user_source_page');
var ConceptEditPage = require('../pages/concept_edit_page');
var configuration = require('../utilities/configuration.js');
var EC = require('protractor').ExpectedConditions;

describe('Concept edits', function () {
    var loginPage;
    var logoutPage;
    var orgPage;
    var usrSrcPage;
    var conceptEditPage;
    var srcShortCode = '';


    beforeAll(function(){
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        orgPage = new OrgPage();
        usrSrcPage = new UserSourcePage();
        conceptEditPage = new ConceptEditPage();
        browser.ignoreSynchronization = true;

        // Login
        loginPage.visit();
        loginPage.login();

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


    it('should edit the concept 2, drop fully specified name and get an error', function() {
        element(by.id("edit-concept")).click();

        conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
        conceptEditPage.namesDiv.element(by.css('.name-type')).element(by.cssContainingText("option", "Short")).click();

        conceptEditPage.updateButton.click();

        expect(conceptEditPage.errorBox.getText()).toEqual('Concept requires at least one fully specified name');

        conceptEditPage.cancelUpdateButton.click();

    });

    it('should edit the concept 2, change the name to be same as concept 1 and get an error', function(done) {
        element(by.id("edit-concept")).click();

        conceptEditPage.fillInUpdateText("Update Concept " + orgPage.getRandomString(3));
        var nameInput = conceptEditPage.namesDiv.element(by.css('.name-content'));

        // PAIN!
        nameInput.sendKeys(protractor.Key.BACK_SPACE +  '1');
        conceptEditPage.updateButton.click();

        expect(conceptEditPage.errorBox.getText()).toEqual('Concept preferred name should be unique for same source and locale');

        conceptEditPage.cancelUpdateButton.click();
        done()
    });

    afterAll(function() {
        logoutPage.logout();
    });
});
