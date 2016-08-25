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

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as awadhwa.');
    });

    it('should create collection', function () {
        collectionPage.createNewUserCollection( 'WHO',
            'Woreda Health Office',
            'Woreda Health Office Collection',
            'en,es,fr'
        );

        expect((collectionPage.status).getText()).toEqual('Collection created');
    });

    it('should edit collection', function () {
        collectionPage.editCollection('collection description', '1.1');

        expect((collectionPage.status).getText()).toEqual('Collection updated');
        expect((collectionPage.updatedDescValue).getText()).toContain('collection description');
        expect((collectionPage.updatedExtIdValue).getText()).toContain('1.1');
    });

    it('should delete collection', function () {
        collectionPage.deleteCollection();

        expect((collectionPage.status).getText()).toEqual('Collection Deleted');
    });

     it('should logout', function () {
         logoutPage.logout();

         expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
     });

});

