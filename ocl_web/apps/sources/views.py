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
        headers = {'Authorization': auth_token}

        # API calls for source details and concepts
        source = requests.get(source_url, headers=headers).json()
        concepts = requests.get(concept_url, headers=headers).json()

        # Get additional details for concepts (since currently not included in list query)
        concepts_detail = []
        for concept in concepts:
            # this is a total hack to address a bug in how the API creates URLs
            concept_url = concept['url'].replace('INITIAL/','')
            # this part is a hack since the API doesn't let me customize the fields returned
            concept = requests.get(concept_url, headers=headers).json()
            concepts_detail.append(concept)

        context['source'] = source
        #context['concepts'] = concepts
        context['concepts'] = concepts_detail

        return context

