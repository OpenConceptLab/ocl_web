var LoginPage = function() {

  this.username = $('#id_login');
  this.password = $('#id_password');
  this.signinLink = element(by.linkText('Sign In'));
  this.loginButton = element(by.buttonText('Sign In'));

  this.visit = function() {
    browser.get('/');
  };

  this.signin = function () {
      this.signinLink.click();
  };

  this.setUsername = function(username) {
    this.username.clear();
    this.username.sendKeys(username);
  };

  this.setPassword = function(password){
    this.password.clear();
    this.password.sendKeys(password);
  };

  this.login = function() {
    this.loginButton.click();
  };

   this.login = function(username, password) {
    this.signinLink.click();
    this.setUsername(username);
    this.setPassword(password);
    this.login();
  };
};
module.exports = LoginPage;
