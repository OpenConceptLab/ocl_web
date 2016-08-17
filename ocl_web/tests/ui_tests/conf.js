exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:9515',
    specs: ['home_spec.js'],
    capabilities: {
        'browserName': 'phantomjs'
    }
};
