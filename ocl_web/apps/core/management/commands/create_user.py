"""
Create test user.

Run this once before running e2e tests
"""
from optparse import make_option

from django.core.management import BaseCommand
from libs.ocl import OclApi

class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}

class Command(BaseCommand):
    """ manage.py Command 'create_sysadmin' """
    help = 'Create user'
    option_list = BaseCommand.option_list + (

        make_option('--username',
                    action='store',
                    dest='username',
                    default='test',
                    help='Username to be created'),
        make_option('--password',
                    action='store',
                    dest='password',
                    default='test123',
                    help='Password'),
        make_option('--superuser',
                    action='store_true',
                    dest='superuser',
                    default=False,
                    help='True, if superuser account'),
        make_option('--company_name',
                    action='store',
                    dest='company_name',
                    default='Open Concept Lab',
                    help='Company full name'),
        make_option('--location',
                    action='store',
                    dest='location',
                    default='Boston, MA, USA',
                    help='Location, e.g. Boston, MA, USA'),
    )

    def __init__(self):
        super(Command, self).__init__()

    def create_test_user(self):
        """ Creates the OCL sysadmin user """
        from users.models import User
        from allauth.account.models import EmailAddress

        print '==================================='


        print 'Creating "' + self.username + '" User'

        email = self.username + '@openconceptlab.org'

        user = None

        if User.objects.filter(username=self.username).count() > 0:
            user = User.objects.get(username=self.username)
            if self.superuser and not user.is_superuser:
                user.delete();
                user = None

        if user is None:
            if self.superuser:
                user = User.objects.create_superuser(self.username, email, self.password)
            else:
                user = User.objects.create_user(username=self.username)

        user.email = email
        user.set_password(self.password)
        user.first_name = 'none'
        user.last_name = 'none'
        user.save()

        if EmailAddress.objects.filter(user=user).count() > 0:
            email = EmailAddress.objects.get(user=user)
        else:
            email = EmailAddress.objects.create(user=user)

        email.email = user.email
        email.verified = True
        email.save()

        ocl = OclApi(admin=True)

        data = {
            "username": user.username,
            "name": user.first_name + ' ' + user.last_name,
            "email": user.email,
            'hashed_password': user.password,
            "company": self.company_name,
            "location": self.location,
            "preferred_locale": 'en'
        }

        result = ocl.create_user(data)

        if result.status_code == 201:
            print 'User "' + user.username + '" synced to API'
            print '==================================='
        elif result.status_code == 400:
            print 'User "' + user.username + '" exists in API, trying to reactivate...'
            # try reactivate for now, this is very not secure, #TODO
            result = ocl.reactivate_user(user.username)
            if result == 204:
                print 'User "' + user.username + '" reactivated in API'
            else:
                print 'Failed to reactivate user "' + user.username + '" in API. Server responded with ' + str(result.status_code)

            print '==================================='
        else:
            print 'Failed to sync user "' + user.username + '" to API. Server responded with ' + str(result.status_code)
            print '==================================='
            exit(1)

    def handle(self, *args, **options):

        self.location = options['location']
        self.company_name = options['company_name']
        self.username = options['username']
        self.password = options['password']
        self.superuser = options['superuser']

        self.create_test_user()
