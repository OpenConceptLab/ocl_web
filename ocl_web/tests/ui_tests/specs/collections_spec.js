'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var CollectionPage = require('../pages/collections_page.js');

describe('OCL Collections Page', function () {

    var loginPage;
    var logoutPage;
    var collectionPage;

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        collectionPage = new CollectionPage();
    });

    it('should login', function () {
        loginPage.visit();
        loginPage.login('awadhwa','root123');

        expect(element(by.className('alert-success')).getText()).toEqual('Successfully signed in as awadhwa.');
    });

    it('should create collection', function () {
        collectionPage.createNewUserCollection('C1', 'col1', 'collection 1', 'en,es,fr');

        expect(element(by.className('alert-info')).getText()).toEqual('Collection created');
    });

    it('should edit collection', function () {
        collectionPage.editCollection('collection description', '123456');

        expect(element(by.className('alert-info')).getText()).toEqual('Collection updated');
        expect($('#id_coll_description').getText()).toContain('collection description');
        expect($('#id_coll_externalId').getText()).toContain('123456');
    });

    it('should delete collection', function () {
        collectionPage.deleteCollection();

        expect(element(by.className('alert-info')).getText()).toEqual('Collection Deleted');
    });

     it('should logout', function () {
         logoutPage.logout();

         expect(element(by.className('alert-success')).getText()).toEqual('You have signed out.');
     });

});

