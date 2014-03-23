# Basic search
#https://github.com/search?q=malaria&ref=cmdform

# Search by type (when sidebar is clicked)
#https://github.com/search?q=malaria&ref=cmdform&type=Code


from django.views.generic import TemplateView
from django.conf import settings
import requests


class HomeSearchView(TemplateView):

    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        SEARCH_TYPE_PATHS = {
            'concepts': '/v1/orgs/WHO/sources/ICD-10/concepts/',
            'sources': '/v1/orgs/WHO/sources/',
            'orgs': '/v1/orgs/',
            'users': '/v1/users/'}

        try:
            uri_path = SEARCH_TYPE_PATHS[self.request.GET['type']]
        except KeyError:  # Either there is no 'type' in GET, or we don't support what was sent in.
            uri_path = SEARCH_TYPE_PATHS['concepts']

        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        full_path = host + uri_path
        headers = {'Authorization': auth_token}

        results = requests.get(full_path, headers=headers)
        context['results'] = results.json()

        return context
