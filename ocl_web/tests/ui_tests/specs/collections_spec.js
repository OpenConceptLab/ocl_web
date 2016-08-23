'use strict';

var LoginPage = require('../pages/login_page.js');

describe('OCL Collections Page', function () {

    it('should login', function () {
        var loginPage = new LoginPage();
        loginPage.visit();
        loginPage.login('awadhwa','root123');

        expect(element(by.linkText('awadhwa')).getText()).toEqual('awadhwa');
    });

    it('should create collection', function () {
        element(by.linkText('New User Collection')).click();
        element(by.id('id_short_code')).sendKeys('C1');
        element(by.id('id_name')).sendKeys('Col 1');
        element(by.id('id_full_name')).sendKeys('Collection 1');
        element(by.id('id_supported_locales')).sendKeys('en,es,fr');
        element(by.buttonText('Add')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Collection created');
    })

    it('should edit collection', function () {
        element(by.css('span.glyphicon-cog')).click();
        element(by.id('id_description')).sendKeys('collection description');
        element(by.id('id_external_id')).sendKeys('123456');
        element(by.buttonText('Update')).click();
    })

    it('should delete collection', function () {
        element(by.css('span.glyphicon-cog')).click();
        element(by.css('span.glyphicon-trash')).click();
        element(by.buttonText('Delete')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Collection Deleted');
    })

    it('should logout', function () {
        element(by.linkText('Logout')).click();
        element(by.buttonText('Sign Out')).click();

        expect(element(by.className('alert-success')).getText()).toEqual('You have signed out.');
    });

});

