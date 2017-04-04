'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var UserSourcePage = require('../pages/user_source_page.js');
var data = require('../fixtures/test_data.json');
var configuration = require('../utilities/configuration.js');
var searchPage = require('../pages/search_page.js');
var EC = require('protractor').ExpectedConditions;
const timeout = configuration.get('timeout');
const baseUrl = configuration.get('baseUrl');

describe('Search Page', function () {

    var loginPage,
        logoutPage,
        usrSrcPage;

    beforeAll(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        usrSrcPage = new UserSourcePage();
        loginPage.login();
        return browser.ignoreSynchronization = true;
    });

    afterAll(function () {
        logoutPage.logout();
    });

    it('should show at least one concept', function () {
        browser.get(baseUrl + 'search/?type=concepts&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show at least one mapping', function () {
        browser.get(baseUrl + 'search/?type=mappings&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show at least one source', function () {
        browser.get(baseUrl + 'search/?type=sources&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show at least one collection', function () {
        browser.get(baseUrl + 'search/?type=collections&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show at least one org', function () {
        browser.get(baseUrl + 'search/?type=orgs&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show at least one user', function () {
        browser.get(baseUrl + 'search/?type=users&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

});
