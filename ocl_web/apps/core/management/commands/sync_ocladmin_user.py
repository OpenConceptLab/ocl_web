import os

from django.conf import settings
from django.core.management import BaseCommand
from libs.ocl import OclApi

PASSWORD = os.environ.get('OCL_API_TOKEN', 'OclAdm1n@123')


class Command(BaseCommand):
    help = 'Upsert OClAdmin user'

    def handle(self, *args, **options):
        from users.models import User
        from allauth.account.models import EmailAddress

        username = settings.API_SUPERUSER_USERNAME

        if not PASSWORD:
            print "PASSWORD not there for ocladmin superuser"
            return

        user = User.objects.filter(username=username).first()
        if not user:
            user = User()
            user.username = username
            user.email = "ocladmin@openconceptlab.org"
            user.set_password(PASSWORD)
            user.first_name = 'ocl'
            user.last_name = 'admin'
            user.is_superuser = True
            user.is_staff = True
            user.save()
            if EmailAddress.objects.filter(user=user).count() > 0:
                email = EmailAddress.objects.get(user=user)
            else:
                email = EmailAddress.objects.create(user=user)

            email.email = user.email
            email.verified = True
            email.save()

        ocl = OclApi(debug=True)
        result = ocl.get_user_auth(username, PASSWORD, hashed=False)
        token = result.json()['token']

        user.sync_token(token)


