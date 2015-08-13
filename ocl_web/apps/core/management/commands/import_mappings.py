"""
Import mappings via API.

    The input file format is a record per line, each line in the form:
    mapping_name sorce_concept_id [list of dest_concept_id]

    manage.py import_mappings input_file_name

    File Example:

q_and_a 985 1173 1152 5254 1150 6046 5526 968
q_and_a 986 987 988 989 5622
concept_set 1010 1006 1007 1008 1298 1009
concept_set 1019 21 678 679 729 851 1015 1016 1017 1018
q_and_a 1030 1138 664 703 1304
q_and_a 1031 1311 1312 1313 1314 1315 1316 1317 1304

"""
from optparse import make_option
import os.path

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
    """ manage.py Command 'import_mappings' """
    help = 'Import mappigs'
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
                    help='Organization ID, e.g. OMRS'),
        make_option('--source_id',
                    action='store',
                    dest='source_id',
                    default=None,
                    help='Source ID, e.g. OMRS'),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.ocl = None
        self.username = None
        self.password = None
        self.api_host = os.environ['OCL_API_HOST']
        self.web_host = os.environ['OCL_WEB_HOST']
        self.ORG_ID = None
        self.SOURCE_ID = None
        self.locale_list = [d['code'] for d in _get_locale_list()]
        self.source_type_list = _get_source_type_list()
        self.concept_class_list = _get_concept_class_list()
        self.datatype_list = _get_datatype_list()

    def load_user(self, username):
        """
            Load access info for specified username to create data.
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
        self.ocl = OclApi(admin=True, debug=True)

        result = self.ocl.get_user_auth(self.username, self.password)
        print 'get auth:', result.status_code
        if len(result.text) > 0:
            print result.json()

        # now use a "normal" API interface, save the user's access permission
        self.request = FakeRequest()
        self.ocl.save_auth_token(self.request, result.json())
        self.ocl = OclApi(self.request, debug=True)


    def create_mapping(self, fields):
        """
        Create mappings from fields.

        :param fields: is a list in the form of mapping_name, src_id, dest_id+

        NOTE: The API URL path version is hard coded TBW
        """
        map_type = fields[0]
        source_cid = fields[1]

        if map_type == 'internal':
            map_type, code, source = fields[2].split(',')
            print map_type, code, source
            data = {
                'map_type': map_type,
                'to_source_code': source,
                'to_concept_code': code,
            }
            result = self.ocl.create_mapping_from_concept(
                'orgs', self.ORG_ID, self.SOURCE_ID, source_cid, data)
            print result
            return

        for dest_id in fields[2:]:
            data = {
                'map_type': map_type,
                'to_concept_url': '%s/v1/orgs/%s/sources/%s/concepts/%s/' % (self.api_host,
                                                                             self.ORG_ID,
                                                                             self.SOURCE_ID,
                                                                             dest_id),
                'to_concept_url': '/orgs/%s/sources/%s/concepts/%s/' % (self.ORG_ID,
                                                                        self.SOURCE_ID,
                                                                        dest_id),
            }
            result = self.ocl.create_mapping_from_concept(
                'orgs', self.ORG_ID, self.SOURCE_ID, source_cid, data)
            print result

    def load_mappings(self):
        """ Load mappings from file """
        for line in self.input:
            fields = line.split()
            self.create_mapping(fields)

    def handle(self, *args, **options):

        if len(args) != 1:
            raise CommandError('mapping input text file is required.')

        username = options['username']

        if username is None:
            raise CommandError('--username is required.')

        self.ORG_ID = options['org_id']
        if self.ORG_ID is None:
            raise CommandError('--org_id is required.')

        self.SOURCE_ID = options['source_id']
        if self.SOURCE_ID is None:
            raise CommandError('--source_id is required.')

        input_file = args[0]
        if not os.path.exists(input_file):
            raise CommandError('Could not find input file %s' % input_file)

        try:
            self.input = open(input_file, 'rb')
            # get total record count
            self.total = sum(1 for line in self.input)
            self.input.seek(0)
        except IOError:
            raise CommandError('Could not open input file %s' % input_file)

        self.load_user(username)
        self.login()

        self.load_mappings()
