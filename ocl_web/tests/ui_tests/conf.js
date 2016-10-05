
    var chromeCapabilities = {
        browserName: 'chrome'
    };

    var phantomJSCapabilities = {
        browserName: 'phantomjs'
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
        seleniumPort: 4444,
        specs: ['./specs/organization_spec.js','./specs/user_source_spec.js','./specs/collections_spec.js'],
        capabilities: getBrowserCapabilities(),

        'onPrepare' : function () {
            browser.driver.manage().window().setSize(1280, 1024);
        }
    };


