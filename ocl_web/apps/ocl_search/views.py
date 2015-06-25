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

        search_type_info = {
            'concepts': { 'int': OCLapi.CONCEPT_TYPE, 'name': 'concept', 'facets': True },
            'mappings': { 'int': OCLapi.MAPPING_TYPE, 'name': 'mapping', 'facets': True },
            'sources': { 'int': OCLapi.SOURCE_TYPE, 'name': 'source', 'facets': True },
            'collections': { 'int': OCLapi.COLLECTION_TYPE, 'name': 'collection', 'facets': True },
            'orgs': { 'int': OCLapi.ORG_TYPE, 'name': 'organization', 'facets': False },
            'users': { 'int': OCLapi.USER_TYPE, 'name': 'user', 'facets': False }
        }

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Setup the resource count dictionary
        resource_count = {}
        for resource_type in search_type_info:
            resource_count[resource_type] = 0

        # Map resource_type string to integer
        search_type = self.request.GET.get('type', 'concepts')
        if search_type in search_type_info:
            resource_type = search_type_info[search_type]['int']
        else:
            resource_type = OCLapi.CONCEPT_TYPE

        # Perform the primary search via the API
        searcher = OCLSearch(resource_type).parse(self.request.GET)
        api = OCLapi(self.request, debug=True, facets=search_type_info[search_type]['facets'])
        search_response = api.get(search_type, params=searcher.search_params)
        if search_type_info[search_type]['facets']:
            search_response_json = search_response.json()
            search_facets = search_response_json['facets']
            search_results = search_response_json['results']
            search_response_json = ''
        else:
            search_results = search_response.json()
            search_facets = {}
        num_found = int(search_response.headers['num_found'])

        # Set count for primary search type here, the rest is below
        resource_count[search_type] = num_found

        # Setup paginator and context for primary search
        pg = Paginator(range(num_found), searcher.num_per_page)
        context['page'] = pg.page(searcher.current_page)
        context['pagination_url'] = self.request.get_full_path()
        context['search_filter_lists'] = searcher.get_filters()
        context['results'] = search_results
        context['search_type'] = search_type
        context['search_type_name'] = search_type_info[search_type]['name']
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()

        # Build URL parameters for switching to other resources
        allowed_other_resource_search_params = ['q', 'limit', 'debug']
        other_resource_search_params = {}
        for param in allowed_other_resource_search_params:
            if param in self.request.GET:
                other_resource_search_params[param] = self.request.GET.get(param)
        context['other_resource_search_params'] = ''
        if len(other_resource_search_params):
            context['other_resource_search_params'] = '&' + urllib.urlencode(other_resource_search_params)

        # Perform the counter searches
        if search_response:
            for resource_type in search_type_info:                
                # Skip this resource if the primary search type (already calculated above)
                if resource_type == search_type:
                    continue

                # Get resource count using same search criteria
                count_response = api.head(resource_type, params=other_resource_search_params)
                if 'num_found' in count_response.headers:
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                else:
                    resource_count[resource_type] = 0
        context['resource_count'] = resource_count

        # debug display variables
        context['search_params'] = searcher.search_params
        context['search_response_headers'] = search_response.headers
        context['search_facets'] = search_facets

        # to remove closing form tag in nav.html
        context['extend_nav_form'] = True  

        return context