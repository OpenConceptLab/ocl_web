'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');

describe('OCL Org Page', function () {
    var loginPage;
    var logoutPage;
    var orgShortCode = '';

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
    });

    it('should login', function () {
        var loginPage = new LoginPage();
        loginPage.visit();
        loginPage.login('awadhwa','root123');

        expect(element(by.className('alert-success')).getText()).toEqual('Successfully signed in as awadhwa.');
    });

    var getRandomString = function(length) {
        var string = '';
        var letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
        for (var i = 0; i < length; i++) {
            string += letters.charAt(Math.floor(Math.random() * letters.length));
        }
        return string;
    };

    it('should create organization', function () {
        element(by.linkText('Create New Organization')).click();
        orgShortCode = getRandomString(5);
        element(by.id('id_short_name')).sendKeys(orgShortCode);
        element(by.id('id_name')).sendKeys('Full name');
        element(by.id('id_website')).sendKeys('http://www.google.com/');
        element(by.id('id_company')).sendKeys('TW');
        element(by.id('id_location')).sendKeys('India');
        element(by.buttonText('Create Organization')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Organization Added');
    });

    it('should create collection under org', function () {
        element(by.linkText('Collections')).click();
        element(by.linkText(' New Collection')).click();
        element(by.id('id_short_code')).sendKeys('C1');
        element(by.id('id_name')).sendKeys('org col 1');
        element(by.id('id_full_name')).sendKeys('organization collection 1');
        element(by.id('id_supported_locales')).sendKeys('en');
        element(by.buttonText('Add')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Collection created');

        element(by.linkText('  '+orgShortCode)).click();
    });

    it('should create source', function () {
        element(by.linkText('Sources')).click();
        element(by.linkText(' New Source')).click();
        element(by.id('id_short_name')).sendKeys('S1');
        element(by.id('id_full_name')).sendKeys('source 1');
        element(by.id('id_supported_locales')).sendKeys('en');
        element(by.buttonText('Create Source')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Source created');
    });

    it('should create source version', function () {
        element(by.linkText('Versions')).click();
        element(by.linkText('New Source Version')).click();
        element(by.id('id_id')).sendKeys('v1');
        element(by.id('id_description')).sendKeys('version 1');
        element(by.buttonText('Create Source Version')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Source version created!');
    });

    it('should create concept', function () {
        element(by.linkText('Concepts')).click();
        element(by.linkText(' New Concept')).click();
        element(by.id('id_concept_id')).sendKeys('C1');
        element(by.id('id_name')).sendKeys('concept 1');
        element(by.id('id_name_type')).sendKeys('Fully_specified');
        element(by.buttonText('Create Concept')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Concept created.');
    });

     it('should logout', function () {
         var logoutPage = new LogoutPage();
         logoutPage.logout();

        expect(element(by.className('alert-success')).getText()).toEqual('You have signed out.');
    });

});
