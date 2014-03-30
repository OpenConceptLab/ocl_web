from django.views.generic import TemplateView
from django.conf import settings
import requests


class SourceDetailView(TemplateView):

    template_name = "sources/source_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(SourceDetailView, self).get_context_data(*args, **kwargs)

        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        source_path = "/v1/orgs/%s/sources/%s/" % (kwargs['org'], kwargs['source'])
        concept_path = "/v1/orgs/%s/sources/%s/concepts/" % (kwargs['org'], kwargs['source'])
        source_url = host + source_path
        concept_url = host + concept_path
        headers = {'Authorization': auth_token}

        source = requests.get(source_url, headers=headers).json()
        concepts = requests.get(concept_url, headers=headers).json()

        context['source'] = source
        context['concepts'] = concepts

        return context

