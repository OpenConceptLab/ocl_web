var configuration = require('../utilities/configuration.js');

var LoginPage = function() {

  this.username = $('#id_login');
  this.password = $('#id_password');
  this.signinLink = element(by.linkText('Sign In'));
  this.loginButton = element(by.buttonText('Sign In'));
  this.loginStatus = $('.alert-success');

  this.visit = function() {
    browser.get(configuration.get('baseUrl'));
  };

  this.signIn = function () {
      this.signinLink.click();
  };

  this.setUsername = function() {
    this.username.clear();
    this.username.sendKeys(configuration.get("username"));
  };

  this.setPassword = function(){
    this.password.clear();
    this.password.sendKeys(configuration.get("password"));
  };

  this.clickLogin = function() {
    this.loginButton.click();
  };

  this.login = function() {
    this.visit();
    this.signIn();
    this.setUsername();
    this.setPassword();
    this.clickLogin();
  };
};
module.exports = LoginPage;
