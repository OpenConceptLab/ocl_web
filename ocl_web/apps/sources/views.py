from django.views.generic import TemplateView
from django.conf import settings
import requests


class SourceDetailView(TemplateView):

    template_name = "sources/source_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(SourceDetailView, self).get_context_data(*args, **kwargs)

        # Setup API calls
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        source_path = "/v1/orgs/%s/sources/%s/" % (kwargs['org'], kwargs['source'])
        concept_path = "/v1/orgs/%s/sources/%s/concepts/" % (kwargs['org'], kwargs['source'])
        source_url = host + source_path
        concept_url = host + concept_path
        requestHeaders = {'Authorization': auth_token}

        # API calls for source details and concepts
        source = requests.get(source_url, headers=requestHeaders).json()
        concepts = requests.get(concept_url, headers=requestHeaders).json()

        # Set the context
        context['source'] = source
        context['concepts'] = concepts

        return context

