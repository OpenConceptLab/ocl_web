"""
Create sysadmin user.

Run this onces at system generation time.
"""
from optparse import make_option

from django.core.management import BaseCommand
#from django.core.management import CommandError

from libs.ocl import OclApi


class Command(BaseCommand):
    """ manage.py Command 'create_sysadmin' """
    help = 'Create sysadmin user'
    option_list = BaseCommand.option_list + (

        make_option('--test',
                    action='store_true',
                    dest='test_mode',
                    default=False,
                    help='Test only, do not create data.'),
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

    def create_sysadmin_user(self):
        """ Creates the OCL sysadmin user """

        from users.models import User
        sysadmin = User.objects.create_superuser(
            'sysadmin', 'paynejd+sysadmin@gmail.com', 'password')
        sysadmin.first_name = 'System'
        sysadmin.last_name = 'Administrator'
        sysadmin.save()

        ocl = OclApi(admin=True)
        data = {
            "username": sysadmin.username,
            "name": "System Administrator",
            "email": sysadmin.email,
            'hashed_password': sysadmin.password,
            "company": self.company_name,
            "location": self.location,
            "preferred_locale": 'en',
        }

        result = ocl.create_user(data)
        self.stdout.write('Sysadmin user created, result:' + str(result.status_code))

    def handle(self, *args, **options):

        self.location = options['location']
        self.company_name = options['company_name']
        self.test_mode = options['test_mode']

        if self.test_mode:
            return

        self.create_sysadmin_user()
