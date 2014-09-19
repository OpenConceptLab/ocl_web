#Get list of user:
#http://65.99.230.144/v1/users/
from django.test import TestCase

from libs.ocl import OCLapi

class UserTestCase(TestCase):

    def test_create_user(self):

#        ocl = OCLapi(debug=True)
        ocl = OCLapi()

        username = 'testuser998'
        data = {
                "username": username,
                "name": "Test User998",
                "email": "testuser998@me.com",
                'hashed_password': "aaaaaa",
                "company": "Some Company",
                "location": "Eldoret, Kenya",
                "preferred_locale": "en,sw",
                "extras": { "my-field": "my-value" }
                }

        result = ocl.create_user(**data)
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
        if len(result.text) > 0: print result.json()

#        result = ocl.delete_user(username)
#        print result
#        print result, result.status_code, # result.json()

#        result = ocl.reactivate_user(username)
#        print result
