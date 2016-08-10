"""
File to test OCL users -- this is way out of date and does not work
"""
#Get list of user:
#http://65.99.230.144/v1/users/
from django.test import TestCase

from libs.ocl import OclApi
from users.models import User
from unittest import skip

class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}

class UserTestCase(TestCase):
    """ UserTestCase class """

    username = 'testuser996'
    password = 'pbkdf2_sha256$12000$txd3yUA9l4mv$88BDS8RweS3vGcrQtVdRKkcUcypHVsOZ/NczuPuyQxA='

    @skip("not a valid test case")
    def test_create_user(self):
        """ Test create OCL user """

#        ocl = OclApi(debug=True)
        ocl = OclApi(admin=True)

        username = 'testuser995'
        data = {
            "username":username,
            "name":"Test User995",
            "email":"testuser995@me.com",
            'hashed_password':"aaaaaa",
            "company":"Some Company",
            "location":"Eldoret, Kenya",
            "preferred_locale":"en,sw",
            "extras":{"my-field":"my-value"}
        }

        result = ocl.create_user(data)
        print 'create:', result.status_code
        print result.text
        print len(result.text)
        print result.json()
        if result.status_code == 400:
            # try reactivate
            print 'reactivate?'
            result = ocl.reactivate_user('blah') # username)
            print result.status_code # , result.json()
            print result.json()

        result = ocl.get_user_auth(username, 'aaaaaa')
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

    @skip("not a valid test case")
    def test_user_login(self):
        """ Note that password is hardcoded for now.
         """
        ocl = OclApi(admin=True, debug=True)

        user = User.objects.create_user(username=self.username)
        user.password = self.password
        user.save()

        result = ocl.get_user_auth(user.username, user.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

    @skip("not a valid test case")
    def test_user_update(self):
        """ Test user partial data update.
            Need to login first with hard coded password.
         """
        ocl = OclApi(admin=True, debug=True)

        user = User.objects.create_user(username=self.username)
        user.password = self.password
        user.save()

        result = ocl.get_user_auth(user.username, user.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        request = FakeRequest()
        ocl.save_auth_token(request, result.json())


        ocl = OclApi(request, debug=True)
        print ocl.get('users', user.username).json()

        data = {'company': 'company one'}
        result = ocl.post('user', **data)
        print result.status_code
        if len(result.text) > 0:
            print result.json()

    @skip("not a valid test case")
    def test_concept_create(self):
        """ Test concept create
            Need to login first with hard coded password.
         """
        ocl = OclApi(admin=True, debug=True)

        user = User.objects.create_user(username=self.username)
        user.password = self.password
        user.save()

        result = ocl.get_user_auth(user.username, user.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        request = FakeRequest()
        ocl.save_auth_token(request, result.json())


        ocl = OclApi(request, debug=True)
        org_id = 'TESTORG1'
        source_id = 'S1'


        data = {
            'id': 'CTEST001',
            'concept_class': 'Diagnosis',
            'datatype': 'String',
        }
        names = [{
            'name': 'concept name',
            'locale': 'en',
        }]
        result = ocl.create_concept('orgs', org_id, source_id, base_data=data, names=names)
        print result.status_code
        print result
        if len(result.text) > 0:
            print result.json()

    @skip("not a valid test case")
    def test_concept_names(self):
        """ Test concept names operations
            Need to login first with hard coded password.
         """
        ocl = OclApi(admin=True, debug=True)

        user = User.objects.create_user(username=self.username)
        user.password = self.password
        user.save()

        result = ocl.get_user_auth(user.username, user.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        request = FakeRequest()
        ocl.save_auth_token(request, result.json())


        ocl = OclApi(request, debug=True)
        org_id = 'TESTORG1'
        source_id = 'S1'
        concept_id = 'C2'

        result = ocl.get('orgs', org_id, 'sources', source_id, 'concepts', concept_id, 'names')
        print result.status_code
        print result
        if len(result.text) > 0:
            print result.json()

        # delete all names
