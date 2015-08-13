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

from django.core.management import BaseCommand, CommandError

from .importer import Importer


class Command(BaseCommand):
    """ create_org manage.py Command """

    help = 'Create demo data'
    option_list = BaseCommand.option_list + (
        make_option('--username',
                    action='store',
                    dest='username',
                    default=None,
                    help='username for an existing user, e.g. demo1'),
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
    )

    def __init__(self):
        super(Command, self).__init__()
        self.importer = Importer()

    def create_org(self, short_name, full_name, website,
                   company_name, location):
        """ Create one org for our user """
        data = {
            'id': short_name,
            'name': full_name,
            'website': website,
            'company': company_name,
            'location': location,
        }
        print data

        if not self.importer.test_mode:
            print 'creating org %s' % short_name
            result = self.importer.ocl.create_org(data)
            print result

    def handle_file(self):
        """ Load from CSV """
        self.importer.load_csv()
        for row in self.importer.reader:
            self.create_org(row['org_short_name'], row['org_full_name'],
                            row['website'], row['company_name'],
                            row['location'])

    def handle(self, *args, **options):

        self.importer.get_args(args, options)

        self.short_name = options['short_name']
        self.full_name = options['full_name']
        self.company_name = options['company_name']
        self.website = options['website']
        self.location = options['location']

        if self.short_name is None and self.importer.filename is None:
            raise CommandError('--short_name or --csv is required.')

        self.importer.connect()

        if self.importer.filename:
            self.handle_file()
        else:
            self.create_org(self.short_name, self.full_name,
                            self.website, self.company_name, self.location)
