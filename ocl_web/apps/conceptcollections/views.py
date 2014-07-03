from django.views.generic import TemplateView
from django.conf import settings
import requests


class CollectionDetailView(TemplateView):

    template_name = "conceptcollections/conceptcollections_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(CollectionDetailView, self).get_context_data(*args, **kwargs)

        # Setup API calls
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        collection_path = "/v1/orgs/%s/collections/%s/" % (kwargs['org'], kwargs['collection'])
        concept_path = "/v1/orgs/%s/collections/%s/concepts/" % (kwargs['org'], kwargs['collection'])
        collection_url = host + collection_path
        concept_url = host + concept_path
        requestHeaders = {'Authorization': auth_token}

        # API calls for collection details and concepts
        collection = requests.get(collection_url, headers=requestHeaders).json()
        concepts = requests.get(concept_url, headers=requestHeaders).json()

        # Set the context
        context['collection'] = collection
        context['concepts'] = concepts

        return context

