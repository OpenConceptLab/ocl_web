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

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Handle the search type
        search_type = self.request.GET.get('type', 'concepts')
        if search_type not in OCLSearch.resource_type_info:
            search_type = 'concepts'
        # change this to an object method
        resource_type = OCLSearch.resource_type_info[search_type]['int']
        search_type_name = OCLSearch.resource_type_info[search_type]['name']

        # Setup the searcher helper class
        searcher = OCLSearch(resource_type)

        # Parse requires that filters have been setup, but filters aren't setup until the 
        # request has been made because it is using facets --- need to separate out parsing of paramaters
        # and handling of facets before this actually works
        searcher.parse(self.request.GET)

        # Perform the primary search via the API
        has_facets = OCLSearch.resource_type_info[search_type]['facets']
        api = OCLapi(self.request, debug=True, facets=has_facets)
        search_response = api.get(search_type, params=searcher.search_params)
        if has_facets:
            search_response_json = search_response.json()
            search_facets_json = search_response_json['facets']
            search_facets = searcher.process_facets(search_type, search_facets_json)
            search_results = search_response_json['results']
        else:
            search_results = search_response.json()
            search_facets = {}
            search_facets_json = {}
        num_found = int(search_response.headers['num_found'])

        # Setup filters based on the current resource_type
        # NOTE: Facets should be processed separately from filters -- 
        #       Facets are what are returned by Solr, filters are what are displayed
        #       Some processing will be required to convert between the two
        # TODO: sort filters
        # TODO: add some other filters (e.g. Include Retired)

        # Select filters
        searcher.select_filters(searcher.search_params)

        # Setup paginator and context for primary search
        pg = Paginator(range(num_found), searcher.num_per_page)
        context['page'] = pg.page(searcher.current_page)
        context['pagination_url'] = self.request.get_full_path()
        #context['search_filter_lists'] = searcher.get_filters()
        context['results'] = search_results
        context['search_type'] = search_type
        context['search_type_name'] = search_type_name
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_facets'] = search_facets

        # Build URL parameters for switching to other resources
        allowed_other_resource_search_params = ['q', 'limit', 'debug']
        other_resource_search_params = {}
        for param in allowed_other_resource_search_params:
            if param in self.request.GET:
                other_resource_search_params[param] = self.request.GET.get(param)
        context['other_resource_search_params'] = ''
        if len(other_resource_search_params):
            context['other_resource_search_params'] = '&' + urllib.urlencode(other_resource_search_params)

        # Perform the counter searches for the other resources
        resource_count = {}
        for resource_type in OCLSearch.resource_type_info:
            if resource_type == search_type:
                # this search has already been performed, so just set value from above
                resource_count[search_type] = num_found
            else:
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
        context['search_facets_json'] = search_facets_json

        # to remove closing form tag in nav.html
        context['extend_nav_form'] = True  

        return context