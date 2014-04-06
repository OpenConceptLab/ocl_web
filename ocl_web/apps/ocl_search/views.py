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

        # Resolves search type to the API path
        SEARCH_TYPE_PATHS = {
            'concepts': '/v1/concepts/',
            'sources': '/v1/sources/',
            'collections': '/v1/collections/',
            'orgs': '/v1/orgs/',
            'users': '/v1/users/'
        }

        # Resolves search type to the English singular word form
        searchTypeNames = {
            'concepts': 'concept',
            'sources': 'source',
            'collections': 'collection',
            'orgs': 'organization',
            'users': 'user'
        }

        # Default search type to 'concepts' if not valid
        try:
            uri_path = SEARCH_TYPE_PATHS[self.request.GET['type']]
            searchType = self.request.GET['type']
        except KeyError:  # Either there is no 'type' in GET, or we don't support what was sent in.
            uri_path = SEARCH_TYPE_PATHS['concepts']
            searchType = 'concepts'

        # Perform the search using the API
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        full_path = host + uri_path
        headers = {'Authorization': auth_token}
        results = requests.get(full_path, headers=headers).json()

        # Load full resource details (since many required fields are not currently included in the list query)
        # NOTE: This is a temporary fix until the API supports field selection as a GET parameter
        if (searchType in ['sources', 'collections', 'orgs', 'users']):
            results_detail = []
            for result_summary in results:
                result_detail = requests.get(result_summary['url'], headers=headers).json()
                results_detail.append(result_detail)
            results = results_detail

        # Add data to the context
        context['results'] = results
        context['searchType'] = searchType
        context['searchTypeName'] = searchTypeNames[searchType]

        return context
