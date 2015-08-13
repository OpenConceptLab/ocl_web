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

from libs.ocl import OclApi
from apps.core.views import _get_concept_class_list
from apps.core.views import _get_datatype_list
from apps.core.views import _get_source_type_list
from apps.core.views import _get_locale_list

from users.models import User


class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}


class Command(BaseCommand):
    """ manage.py Command 'create_demo_data' """
    help = 'Create demo data'
    option_list = BaseCommand.option_list + (
        make_option('--username',
                    action='store',
                    dest='username',
                    default=None,
                    help='username for an existing user, e.g. demo1'),
        make_option('--org_id',
                    action='store',
                    dest='org_id',
                    default=None,
                    help='Organization ID, e.g. HLTH01'),
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
        self.ORG_ID = None
        self.locale_list = [d['code'] for d in _get_locale_list()]
        self.source_type_list = _get_source_type_list()
        self.concept_class_list = _get_concept_class_list()
        self.datatype_list = _get_datatype_list()

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
        self.ocl = OclApi(admin=True, debug=True)

        result = self.ocl.get_user_auth(self.username, self.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        # now use a "normal" API interface, save the user's access permission
        self.request = FakeRequest()
        self.ocl.save_auth_token(self.request, result.json())
        self.ocl = OclApi(self.request, debug=True)

    def make_source_name(self, n):
        """
            Create source name.

            :param n: is a number.
            :returns: a source name based on the ORG_ID and n.
        """
        return '%sS%d' % (self.ORG_ID, n)

    def make_concept_id(self, s, c):
        """
            Create concept_id

            :param s: is a number, for source
            :param c: is a number, for concept
            :returns: a source name based on the ORG_ID,s and c.
        """
        return '%s-S%d-C%d' % (self.ORG_ID, s, c)

    def create_orgs(self):
        """ Create one test org for our user """
        data = {
            'id': self.ORG_ID,
            'name': 'Health Org %s' % self.ORG_ID,
            'website': 'http://www.health%s.org' % self.ORG_ID,
            'location': 'Boston, MA, USA'
        }
        print 'creating org %s' % self.ORG_ID
        result = self.ocl.create_org(data)
        print result

    def create_sources(self):
        """ Create sources for demo data """

        for n in range(1, 11):
            n = self.make_source_name(n)
            data = {
                'short_code': n,
                'name': n,
                'id': n,
                'source_type': random.choice(self.source_type_list)
            }
            print 'creating source %s' % n
            result = self.ocl.create_source('orgs', self.ORG_ID, data)
            print result

    def create_concepts(self):
        """ Create concepts for demo data """

        for s in range(1, 11):
            sid = self.make_source_name(s)
            for c in range(1, 21):
                concept_id = self.make_concept_id(s, c)

                data = {
                    'id': concept_id,
                    'concept_class': random.choice(self.concept_class_list),
                    'datatype': random.choice(self.datatype_list),
                }
                lc = random.choice(self.locale_list)
                name = {
                    'name': 'Concept %s Source %d C%d' % (self.ORG_ID, s, c),
                    'locale': lc,
                    'preferred': lc,
                }
                print 'creating concept %s' % concept_id
                result = self.ocl.create_concept(
                    'orgs', self.ORG_ID, sid,
                    data, names=[name])
                print result

    def update_concepts(self):
        """ Update concepts for demo data -- WHEN IS THIS USED? """

        for s in range(1, 11):
            sid = self.make_source_name(s)
            for c in range(1, 21):
                concept_id = self.make_concept_id(s, c)
                data = {

                    'concept_class': random.choice(self.concept_class_list),
                    'datatype': random.choice(self.datatype_list),
                    'update_comment': 'testing update',
                }

                print 'updating concept %s' % concept_id
                result = self.ocl.update_concept(
                    'orgs', self.ORG_ID, sid, concept_id,
                    data)
                print result

    def add_concept_data(self):
        """ Add names and descriptions """

        for s in range(1, 11):
            sid = self.make_source_name(s)
            for c in range(1, 21):
                concept_id = self.make_concept_id(s, c)

                for v in ['one', 'two', 'three']:
                    data = {
                        'name': '%s variant %s' % (concept_id, v),
                        'locale': random.choice(self.locale_list),
                    }

                    print 'adding name %s' % data['name']
                    result = self.ocl.post(
                        'orgs', self.ORG_ID, 'sources', sid,
                        'concepts', concept_id, 'names', **data)
                    print result

                    data = {
                        'description': 'description for %s variant %s' % (concept_id, v),
                        'locale': random.choice(self.locale_list),
                    }

                    print 'adding desc %s' % data['description']
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

            self.ORG_ID = options['org_id']
            if self.ORG_ID is None:
                raise CommandError('--org_id is required.')

            self.load_user(username)
            self.login()

            self.create_orgs()
            self.create_sources()
            self.create_concepts()
            self.add_concept_data()
            self.update_concepts()
