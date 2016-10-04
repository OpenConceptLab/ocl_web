exports.config = {
    framework: 'jasmine',

    // this is config to run in headless mode
    seleniumAddress: 'http://localhost:9515',
    capabilities: {
        'browserName': 'phantomjs'
    },

    // Uncomment below 3 lines and comment headless mode config above to run in Chrome browser
    //     seleniumAddress: 'http://localhost:4444/wd/hub',
    //     capabilities: {
    //         'browserName': 'chrome'
    //     },
    specs: ['./specs/organization_spec.js','./specs/user_source_spec.js','./specs/collections_spec.js'],

    'onPrepare' : function () {
        browser.driver.manage().window().setSize(1280, 1024);
    },
    troubleshoot: true,
    baseUrl: 'http://showcase.openconceptlab.org/'
};
