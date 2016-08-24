describe('OCL Org Page', function () {

    it('should login', function () {
        var loginPage = new LoginPage();
        loginPage.visit();
        loginPage.login('awadhwa','root123');

        expect(element(by.linkText('awadhwa')).getText()).toEqual('awadhwa');
    });

    it('should create organization', function () {
        element(by.linkText('Create New Organization')).click();
        element(by.id('id_short_name')).sendKeys('testOrg2');
        element(by.id('id_name')).sendKeys('testOrg2');
        element(by.id('id_website')).sendKeys('http://testOrg2.com');
        element(by.id('id_company')).sendKeys('testOrg2');
        element(by.id('id_location')).sendKeys('Geneva');
        element(by.buttonText('Create Organization')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Organization Added');
    })

    it('should edit organization', function () {
        element(by.css('span.glyphicon-cog')).click();
        element(by.id('id_name')).sendKeys('Edited');
        element(by.buttonText('Update')).click();

        expect(element(by.className('alert-info')).getText()).toEqual('Organization updated.');
    })

     it('should logout', function () {
        element(by.linkText('Logout')).click();
        element(by.buttonText('Sign Out')).click();

        expect(element(by.className('alert-success')).getText()).toEqual('You have signed out.');
    });

});
