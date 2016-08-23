exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:9515',
    specs: ['../ui_tests/specs/*.js'],
    capabilities: {
        'browserName': 'phantomjs'
    },
    baseUrl: 'http://showcase.openconceptlab.org'
};
