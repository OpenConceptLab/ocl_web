from django.core.management import BaseCommand
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Create ocl api as social app'

    def handle(self, *args, **options):
        SocialApp.objects.all().delete()
        SocialApp.objects.create(id=1, provider='OCL', name='OCL', key='OCL', secret='OCL', client_id='OCL')

