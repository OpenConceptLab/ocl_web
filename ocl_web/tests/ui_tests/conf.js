exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:9515',
<<<<<<< HEAD
    specs: ['../ui_tests/specs/*.js'],
=======
    specs: ['home_spec.js','collections_spec.js'],
>>>>>>> 6ccf9866724af8a402675f84b2bc4aa7417a2460
    capabilities: {
        'browserName': 'phantomjs'
    },
    baseUrl: 'http://showcase.openconceptlab.org'
};
