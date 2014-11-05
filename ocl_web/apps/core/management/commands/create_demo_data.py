"""
    A very useful demo data creator.

    Setup is a little bit tricky:
    - you need to have a working OCL user created, via the web, stored
      on the same backend you are trying to create test data on.
      - e.g. point your local dev environment to api.dev.ocl.com and
        create a unique new user.

    -   then this tool will read your local django DB to get the auth info
        and create a lot of test/demo data under that user ID.

        manage.py create_demo_data --username testusername --create

"""
from optparse import make_option
import os.path
import json
import random
import requests

from django.core.management import BaseCommand, CommandError

from libs.ocl import OCLapi
from apps.core.views import _get_concept_class_list
from apps.core.views import _get_datatype_list
from apps.core.views import _get_source_type_list
from apps.core.views import _get_locale_list

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
                    help='username for an existing user'),
        make_option('--create',
                    action='store_true',
                    dest='create_mode',
                    default=False,
                    help='Create data.'),
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

    def signup(self):
        """
            Signup a new user via the web interface.

            Not ready for use yet.
        """
        url = self.web_host + '/accounts/signup/'
        results = requests.get(url)
        csrf = results.cookies['csrftoken']
        cookies = {'csrftoken': csrf}
        headers = {'X-CSRFToken': csrf}
        d = {
            'csrfmiddlewaretoken': csrf,
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': '',
            'password2': '',
            'email': '',
        }
        results = requests.post(
            url,
            data=json.dumps(d), cookies=cookies, headers=headers)
        print results

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

    def create_orgs(self):
        """ Create one test org for our user """
        self.ORG_ID = 'Health01'
        data = {
            'id': self.ORG_ID,
            'name': 'Health Org 01',
            'website': 'http://www.health01.org',
            'location': 'Boston, MA, USA'
        }
        result = self.ocl.create_org(data)
        print result

    def create_sources(self):
        self.ORG_ID = 'Health01'
        source_type_list = _get_source_type_list()
        for n in range(1, 21):
            n = 'HS01%d' % n
            data = {
                'short_code': n,
                'name': n,
                'id': n,
                'source_type': random.choice(source_type_list)
            }
            result = self.ocl.create_source_by_org(self.ORG_ID, data)
            print result

    def create_concepts(self):

        concept_class_list = _get_concept_class_list()
        datatype_list = _get_datatype_list()
        locale_list = [c for c, n in _get_locale_list()]

        self.ORG_ID = 'Health01'
        for s in range(1, 21):
            sid = 'HS01%d' % s
            for c in range(1, 21):
                data = {
                    'id': 'HS01-S%d-C%d' % (s, c),
                    'concept_class': random.choice(concept_class_list),
                    'datatype': random.choice(datatype_list),
                }
                lc = random.choice(locale_list)
                name = {
                    'name': 'Concept HS01 Source %d C%d' % (s, c),
                    'locale': lc,
                    'preferred': lc,
                }
                result = self.ocl.create_concept(
                    'orgs', self.ORG_ID, sid,
                    data, names=[name])
                print result

    def update_concepts(self):

        concept_class_list = _get_concept_class_list()
        datatype_list = _get_datatype_list()
        locale_list = [c for c, n in _get_locale_list()]

        self.ORG_ID = 'Health01'
        for s in range(1, 21):
            sid = 'HS01%d' % s
            for c in range(1, 21):
                concept_id = 'HS01-S%d-C%d' % (s, c)
                data = {

                    'concept_class': random.choice(concept_class_list),
                    'datatype': random.choice(datatype_list),
                    'update_comment': 'testing update',
                }

                result = self.ocl.update_concept(
                    'orgs', self.ORG_ID, sid, concept_id,
                    data)
                print result

    def add_concept_data(self):
        """ Add names and descriptions """
        concept_class_list = _get_concept_class_list()
        datatype_list = _get_datatype_list()
        locale_list = [c for c, n in _get_locale_list()]

        self.ORG_ID = 'Health01'
        for s in range(1, 21):
            sid = 'HS01%d' % s
            for c in range(1, 21):
                concept_id = 'HS01-S%d-C%d' % (s, c)

                for v in ['one', 'two', 'three']:
                    data = {
                        'name': '%s variant %s' % (concept_id, v),
                        'locale': random.choice(locale_list),
                        }

                    result = self.ocl.post(
                        'orgs', self.ORG_ID, 'sources', sid,
                        'concepts', concept_id, 'names', **data)
                    print result

                    data = {
                        'description': 'description for %s variant %s' % (concept_id, v),
                        'locale': random.choice(locale_list),
                        }

                    result = self.ocl.post(
                        'orgs', self.ORG_ID, 'sources', sid,
                        'concepts', concept_id, 'descriptions', **data)
                    print result

    def handle(self, *args, **options):

        create_mode = options['create_mode']
        username = options['username']
        if create_mode:
            if username is None:
                raise CommandError('--username is required.')

            self.load_user(username)
            self.login()

            self.create_orgs()
            self.create_sources()
            self.create_concepts()
            self.add_concept_data()
            self.update_concepts()
