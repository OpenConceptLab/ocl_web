var chance = require('chance').Chance();

var BasePage = function() {
    this.errorBox = element(by.css('.alert-error'));
    this.status = $('.alert-info');
    this.userHomeLink = element(by.css('.resource-label.user'));

    this.returnToHomePage = function () {
        this.userHomeLink.click();
    };

     this.getError = function() {
        return this.errorBox.getText();
    };

    this.getStatus = function() {
        return this.status.getText();
    };

    this.getRandomId = function() {
        return chance.word({length: 6})
    };

    this.getRandomName = function() {
        return chance.word({length: 10});
    };

    this.getRandomShortCode = function () {
        return chance.word({length: 5});
    };
};

module.exports = new BasePage();
