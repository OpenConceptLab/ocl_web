"""
Base for importing objects into OCL.
"""
#from optparse import make_option
import os.path
import csv

#from django.core.management import BaseCommand
from django.core.management import CommandError

from libs.ocl import OclApi

from users.models import User


class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}


class Importer(object):
    """ Importer class for importing objects into OCL """

    def __init__(self):
        self.ocl = None
        self.username = None
        self.password = None
        self.web_host = os.environ['OCL_WEB_HOST']

    def load_user(self):
        """
            Load access info for specified username to create test data.
            :param username: is an existing user in the system.
        """
        user = User.objects.get(username=self.username)
        print user.password
        self.password = user.password

    def login(self):
        """
            Perform a login for the user to get authenticated access
            for subsequence create calls.
        """
        self.ocl = OclApi(admin=True, debug=True)

        result = self.ocl.get_user_auth(self.username, self.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        # now use a "normal" API interface, save the user's access permission
        self.request = FakeRequest()
        self.ocl.save_auth_token(self.request, result.json())
        self.ocl = OclApi(self.request, debug=True)

    def connect(self):
        """ Login to OCL """
        self.load_user()
        self.login()

    def load_csv(self):
        """ Load data from CSV file and save to self.reader """
        print 'Loading from %s...' % self.filename
        f = open(self.filename, 'r')
        self.reader = csv.DictReader(f)

    def get_args(self, args, options):
        """
        Pick up common arguments like CSV file path and username
        """
        print args, options
        self.test_mode = options['test_mode']
        self.username = options['username']
        self.filename = options['filename']

        if self.username is None:
            raise CommandError('--username is required.')

        if self.test_mode:
            print 'Testing only...'
