'use strict';

var BasePage = require('./base_page.js');
var EC = require('protractor').ExpectedConditions;

var SearchPage = function () {

    this.searchResults = element.all(by.css('#data-table-rows > div'));

};

SearchPage.prototype = BasePage;
module.exports = new SearchPage();
