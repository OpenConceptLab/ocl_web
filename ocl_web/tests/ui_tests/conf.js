exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:9515',
    // seleniumAddress: 'http://localhost:4444/wd/hub',
    specs: ['./specs/collections_spec.js'],//'./specs/organization_spec.js','./specs/user_source_spec.js'],
    capabilities: {
        'browserName': 'phantomjs'
        // 'browserName': 'chrome'

    },
    'onPrepare' : function () {
        browser.driver.manage().window().setSize(1280, 1024);
    },
    troubleshoot: true,
    baseUrl: 'http://showcase.openconceptlab.org/'
};
