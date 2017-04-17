var LoginPage = require('../pages/login_page.js');
var LogoutPage = require('../pages/logout_page.js');
var configuration = require('../utilities/configuration.js');
var data = require('../fixtures/test_data.json');
var orgPage = require('../pages/organization_page');
var mappingPage = require('../pages/mapping_page');
const timeout = configuration.get('timeout');
var EC = require('protractor').ExpectedConditions;

describe('Go to the Mapping', function () {
    const baseUrl = configuration.get('baseUrl');
    var loginPage;
    var logoutPage;

    beforeAll(function () {
        loginPage = new LoginPage();
        logoutPage = new LogoutPage();
        loginPage.login();
        return browser.ignoreSynchronization = true;
    });

    afterAll(function () {
        logoutPage.logout();
    });

    it('should add a mapping to a collection', function () {
        mappingPage.getFirstSourceName().then(function (text) {
            var parts = text.split('/');
            var userName = parts[0].trim();
            var sourceName = parts[1].trim();

            mappingPage.clickFirstSource();

            var firstId = orgPage.getRandomId();
            orgPage.createNewConcept(data.concept_id + firstId, data.concept_name, 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);

            element(by.linkText('  ' + sourceName)).click();

            var secondId = orgPage.getRandomId();
            orgPage.createNewConcept(data.concept_id + secondId, data.concept_name + ' second', 'Fully Specified', data.concept_desc, data.key1, data.locale2, true);

            element(by.linkText('  ' + sourceName)).click();

            var fromConceptURL = '/users/' + userName + '/sources/' + sourceName + '/concepts/' + data.concept_id + firstId + '/';
            var toConceptURL = '/users/' + userName + '/sources/' + sourceName + '/concepts/' + data.concept_id + secondId + '/';

            orgPage.createNewMapping(
                fromConceptURL,
                'SAME-AS',
                toConceptURL
            );

            mappingPage.addMappingToFirstCollection();

            browser.wait(EC.visibilityOf(mappingPage.confirmModalButton), timeout);

            mappingPage.confirmModal();

            browser.wait(EC.visibilityOf(mappingPage.alertBox), timeout);
        });
    });
});
