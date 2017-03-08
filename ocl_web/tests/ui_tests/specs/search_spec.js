'use strict';

var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var data = require('../fixtures/test_data.json');
var configuration = require('../utilities/configuration.js');
var searchPage = require('../pages/search_page.js');
var EC = require('protractor').ExpectedConditions;
const timeout = 5000;
const baseUrl = configuration.get('baseUrl');

describe('Search Page', function () {

    var loginPage,
        logoutPage;

    beforeAll(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        loginPage.login();
        return browser.ignoreSynchronization = true;
    });

    afterAll(function () {
        logoutPage.logout();
    });

    it('should show least one concept', function () {
        browser.get(baseUrl + 'search/?type=concepts&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show least one mapping', function () {
        browser.get(baseUrl + 'search/?type=mappings&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show least one source', function () {
        browser.get(baseUrl + 'search/?type=sources&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show least one collection', function () {
        browser.get(baseUrl + 'search/?type=collections&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show least one org', function () {
        browser.get(baseUrl + 'search/?type=orgs&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

    it('should show least one user', function () {
        browser.get(baseUrl + 'search/?type=users&q=');

        expect(searchPage.searchResults.count()).toBeGreaterThan(0);
    });

});
