var LogoutPage = function() {

    this.logoutButton = element(by.css('a[title="Sign Out"]'));
    this.signoutButton = element(by.buttonText('Sign Out'));

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
