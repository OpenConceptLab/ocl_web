"""
    Create organization in system via command line.

    Setup is a little bit tricky:
    - you need to have a working OCL user created, via the web, stored
      on the same backend you are trying to create test data on.
      - e.g. point your local dev environment to api.dev.ocl.com and
        create a unique new user.

    -   then this tool will read your local django DB to get the auth info
        and create a lot of test/demo data under that user ID.

        manage.py create_org --username testusername --csv filename
        or
        manage.py create_org --username testusername --short_name sn
            --full_name=full_name --website=.....

    - The CSV file must have a header row.

    The column names must be:
    org_short_name
    org_full_name
    website
    company_name
    location

"""
from optparse import make_option
import os.path
import csv

from django.core.management import BaseCommand, CommandError

from libs.ocl import OCLapi

from users.models import User


class FakeRequest(object):
    def __init__(self):
        self.session = {}


class Command(BaseCommand):
    help = 'Create demo data'
    option_list = BaseCommand.option_list + (
        make_option('--username',
                    action='store',
                    dest='username',
                    default=None,
                    help='username for an existing user, e.g. demo1'),
        make_option('--short_name',
                    action='store',
                    dest='short_name',
                    default=None,
                    help='Organization short name e.g. OCL'),
        make_option('--full_name',
                    action='store',
                    dest='full_name',
                    default=None,
                    help='Organization full name e.g. Open Concept Lab'),
        make_option('--website',
                    action='store',
                    dest='website',
                    default=None,
                    help='Organization website'),
        make_option('--company_name',
                    action='store',
                    dest='company_name',
                    default=None,
                    help='Company full name'),
        make_option('--location',
                    action='store',
                    dest='location',
                    default=None,
                    help='Location, e.g. Boston, MA, USA'),
        make_option('--csv',
                    action='store',
                    dest='filename',
                    default=None,
                    help='CSV Filename'),
        make_option('--test',
                    action='store_true',
                    dest='test_mode',
                    default=False,
                    help='Test only, do not create data.'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.ocl = None
        self.username = None
        self.password = None
        self.web_host = os.environ['OCL_WEB_HOST']

    def load_user(self, username):
        """
            Load access info for specified username to create test data.
            :param username: is an existing user in the system.
        """
        user = User.objects.get(username=username)
        print user.password
        self.username = username
        self.password = user.password

    def login(self):
        """
            Perform a login for the user to get authenticated access
            for subsequence create calls.
        """
        self.ocl = OCLapi(admin=True, debug=True)

        result = self.ocl.get_user_auth(self.username, self.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        # now use a "normal" API interface, save the user's access permission
        self.request = FakeRequest()
        self.ocl.save_auth_token(self.request, result.json())
        self.ocl = OCLapi(self.request, debug=True)

    def create_org(self, short_name, full_name, website,
                   company_name, location):
        """ Create one org for our user """
        data = {
            'id': short_name,
            'name': full_name,
            'website': website,
            'company_name': company_name,
            'location': location,
        }
        print data

        if not self.test_mode:
            print 'creating org %s' % short_name
            result = self.ocl.create_org(data)
            print result

    def load_csv(self, filename):
        print filename
        f = open(filename, 'r')
        r = csv.DictReader(f)
        for row in r:
            self.create_org(row['org_short_name'], row['org_full_name'],
                            row['website'], row['company_name'],
                            row['location'])

    def handle(self, *args, **options):

        self.test_mode = options['test_mode']
        username = options['username']

        if username is None:
            raise CommandError('--username is required.')

        if self.test_mode:
            print 'Testing only...'

        self.short_name = options['short_name']
        self.full_name = options['full_name']
        self.company_name = options['company_name']
        self.website = options['website']
        self.location = options['location']
        self.filename = options['filename']

        if self.short_name is None and self.filename is None:
            raise CommandError('--short_name or --csv is required.')

        self.load_user(username)
        self.login()

        if self.filename:
            self.load_csv(self.filename)
        else:
            self.create_org(self.short_name, self.full_name,
                            self.website, self.company_name, self.location)
