var LogoutPage = function() {

    this.logoutButton = element(by.linkText('Sign Out'));
    this.signoutButton = element(by.buttonText('Sign Out'));
    //this.logoutStatus = element(by.className('alert-success')).getText();

    this.clickLogout = function () {
        this.logoutButton.click();
    };

    this.clickSignout = function () {
        this.signoutButton.click();
    };

    this.logout = function () {
        this.clickLogout();
        this.clickSignout();
    };
};
module.exports = LogoutPage;
