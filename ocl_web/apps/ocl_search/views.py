# Basic search
# https://github.com/search?q=malaria&ref=cmdform
# Search by type (when sidebar is clicked)
# https://github.com/search?q=malaria&ref=cmdform&type=Code
import logging

from django.views.generic import TemplateView
from django.conf import settings
from django.core.paginator import Paginator
import urllib
import math

from libs.ocl import (OCLapi, OCLSearch)


logger = logging.getLogger('oclweb')


class HomeSearchView(TemplateView):

    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):

        search_type_names = {
            'concepts': 'concept',
            'mappings': 'mapping',
            'sources': 'source',
            'collections': 'collection',
            'orgs': 'organization',
            'users': 'user'
        }
        search_type_paths = {
            'concepts': 'concepts',
            'mappings': 'mappings',
            'sources': 'sources',
            'collections': 'collections',
            'orgs': 'orgs',
            'users': 'users'
        }
        search_type_int = {
            'concepts': OCLapi.CONCEPT_TYPE,
            'mappings': OCLapi.MAPPING_TYPE,
            'sources': OCLapi.SOURCE_TYPE,
            'collections': OCLapi.COLLECTION_TYPE,
            'orgs': OCLapi.ORG_TYPE,
            'users': OCLapi.USER_TYPE
        }

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Setup the resource count dictionary
        resource_count = {}
        for resource_type in search_type_names:
            resource_count[resource_type] = 0

        # Map resource_type string to INT
        search_type = self.request.GET.get('type', 'concepts')
        if search_type in search_type_int:
            resource_type = search_type_int[search_type]
        else:
            resource_type = OCLapi.CONCEPT_TYPE

        # Perform the primary search via the API
        searcher = OCLSearch(resource_type).parse(self.request.GET)
        api = OCLapi(self.request, debug=True)
        search_url = search_type_paths[search_type]
        search_response = api.get(search_url, params=searcher.search_params)
        search_results = search_response.json()
        num_found = int(search_response.headers['num_found'])

        # Set count for primary search type here, the rest is below
        resource_count[search_type] = num_found

        # Setup paginator and context for primary search
        pg = Paginator(range(num_found), searcher.num_per_page)
        context['page'] = pg.page(searcher.current_page)
        context['pagination_url'] = self.request.get_full_path()
        context['search_filters'] = searcher.get_filters()
        context['results'] = search_results
        context['search_type'] = search_type
        context['search_type_name'] = search_type_names[search_type]
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()

        # Perform the counter searches
        if search_response:
            for resource_type in search_type_names:
                
                # Skip this resource if the primary search type
                if resource_type == search_type:
                    continue

                # Need to apply search criteria to this url
                counter_search_url = search_type_paths[resource_type]
                count_response = api.head(counter_search_url, params=searcher.search_params)
                if 'num_found' in count_response.headers:
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                else:
                    resource_count[resource_type] = 0
        context['resource_count'] = resource_count

        # for debug display only
        context['search_params'] = searcher.search_params
        context['api_search_query'] = search_url
        context['search_response_headers'] = search_response.headers

        # to remove closing form tag in nav.html
        context['extend_nav_form'] = True  

        return context