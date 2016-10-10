var configuration = require('../utilities/configuration.js');

describe('OCL Home Page', function() {
  it('should have a title', function() {
    browser.get(configuration.get('baseUrl'));

    expect(browser.getTitle()).toEqual('Open Concept Lab');
  });
});
