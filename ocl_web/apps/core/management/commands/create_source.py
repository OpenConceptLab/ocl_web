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
hl7_code
"""
from optparse import make_option
from django.core.management import BaseCommand, CommandError
from .importer import Importer


PUBLIC_ACCESS_VALUES = ('View', 'Edit', 'None')


class Command(BaseCommand):
    """ create_source manage.py command """

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
        self.importer = Importer()

    def create_source(
            self, org_id,
            source_id, external_id, short_code,
            name, full_name, source_type,
            public_access, default_locale, supported_locales,
            website, description, hl7_code):
        """ Create one source for the specified org """

        # some basic validation
        if public_access not in PUBLIC_ACCESS_VALUES:
            print 'public_access must be one of %s' % PUBLIC_ACCESS_VALUES
            return

        print '>%s<' % hl7_code

        print 'creating source %s for %s' % (source_id, org_id)

        data = {
            'org': org_id,
            'id': source_id,
            'external_id': external_id,
            'short_code': short_code,
            'name': name,
            'full_name': full_name,
            'source_type': source_type,

            'public_access': public_access,
            'default_locale': default_locale,
            'supported_locales': supported_locales,

            'website': website,
            'description': description,
        }

        if hl7_code != '':
            extras = {'hl7_code': hl7_code}
            data['extras'] = extras

        print data
        if self.importer.test_mode:
            print 'Just testing...'
            return
        result = self.importer.ocl.create_source('orgs', org_id, data)
        print result

    def handle_file(self):
        """ Load CSV from the file """
        self.importer.load_csv()
        for row in self.importer.reader:
            self.create_source(
                row['org'],
                row['short_code'],  # id
                row['external_id'],
                row['short_code'],
                row['short_code'],  # name
                row['full_name'],
                row['source_type'],

                row['public_access'],
                row['default_locale'],
                row['supported_locales'],

                row['website'],
                row['description'],
                row['hl7_code']
            )

    def handle(self, *args, **options):

        self.importer.get_args(args, options)

        if self.importer.filename is None:
            raise CommandError('--org_id or --csv is required.')

        self.importer.connect()

        if self.importer.filename:
            self.handle_file()
        else:
            # TBW
            # TODO: Command.handle:: self.create_source()
            pass
