var chromeCapabilities = {
    browserName: 'chrome'
};

var phantomJSCapabilities = {
    browserName: 'phantomjs',
    'phantomjs.binary.path': 'node_modules/phantomjs/bin/phantomjs'
};

var invalidBrowserCapabilities = {
    browserName: "Invalid Browser name provided: " + process.env.browser
};

function getBrowserCapabilities() {
    var desiredCapabilities;
    if ((process.env.browser === undefined) || (process.env.browser === "phantomjs")) {
        desiredCapabilities = phantomJSCapabilities;
    } else if (process.env.browser === "chrome") {
        desiredCapabilities = chromeCapabilities;
    } else {
        desiredCapabilities = invalidBrowserCapabilities;
    }
    console.log("-> Using " + desiredCapabilities.browserName + " browser for execution");
    return desiredCapabilities;
}

exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:4444/wd/hub',
    specs: ['./specs/organization_spec.js', './specs/collections_reference_spec.js', './specs/user_source_spec.js', './specs/collections_spec.js', './specs/user_source_validation_spec.js', './specs/concept_spec.js', './specs/search_spec.js'],
    capabilities: getBrowserCapabilities(),

    jasmineNodeOpts: {
        defaultTimeoutInterval: 100000,
        silent: true,
        print: function () {
        }
    },

    'onPrepare': function () {
        browser.driver.manage().window().setSize(1280, 1024);
        var SpecReporter = require('jasmine-spec-reporter');
        jasmine.getEnv().addReporter(new SpecReporter({displayStacktrace: 'all'}));
    }
};


