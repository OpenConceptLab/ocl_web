'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var CollectionPage = require('../pages/collections_page.js');
var OrgPage = require('../pages/organization_page');
var data = require('../fixtures/test_data.json');

describe('OCL Collections Page', function () {

    var loginPage;
    var logoutPage;
    var collectionPage;
    var orgPage;
    var id='';

    beforeEach(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        collectionPage = new CollectionPage();
        orgPage = new OrgPage();
    });

    it('should login', function () {
        loginPage.visit();
        loginPage.login(data.username,data.password);

        expect((loginPage.loginStatus).getText()).toEqual('Successfully signed in as awadhwa1.');
    });

    it('should create collection', function () {
        id = orgPage.getRandomString(2);
        collectionPage.createNewUserCollection( data.short_code+id,
            data.col_name,
            data.full_name,
            data.supported_locale
        );

        expect((collectionPage.status).getText()).toEqual('Collection created');
    });

    it('should edit collection', function () {
        collectionPage.editCollection(data.col_desc, data.ext_id);

        expect((collectionPage.status).getText()).toEqual('Collection updated');
        expect((collectionPage.updatedDescValue).getText()).toContain('collection description');
        expect((collectionPage.updatedExtIdValue).getText()).toContain('1.1');
    });

    // it('should delete collection', function () {
    //     collectionPage.deleteCollection();
    //
    //     expect((collectionPage.status).getText()).toEqual('Collection Deleted');
    // });

     it('should logout', function () {
         logoutPage.logout();

         expect((loginPage.loginStatus).getText()).toEqual('You have signed out.');
     });

});

