describe('OCL Home Page', function() {
  it('should have a title', function() {
    browser.get('http://localhost:7000');

    expect(browser.getTitle()).toEqual('Open Concept Lab');
  });
});
