"""Views for OCL Global search

Examples:
https://github.com/search?q=malaria&ref=cmdform
https://github.com/search?q=malaria&ref=cmdform&type=Code
"""
import logging

from django.views.generic import TemplateView
from django.conf import settings
from django.core.paginator import Paginator
import urllib
#import math

from libs.ocl import (OCLapi, OCLSearch)


logger = logging.getLogger('oclweb')


class HomeSearchView(TemplateView):
    """View for global OCL search
    """

    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):
        """Set context for OCL global search_type
        """

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Setup the OCL Search helper class
        searcher = OCLSearch(params=self.request.GET)

        # Perform the primary search via the API
        api = OCLapi(self.request, debug=True, facets=searcher.search_resource_has_facets)
        search_response = api.get(searcher.search_type, params=searcher.search_params)
        if searcher.search_resource_has_facets:
            search_response_json = search_response.json()
            search_facets_json = search_response_json['facets']
            search_facets = searcher.process_facets(searcher.search_type, search_facets_json)
            search_results = search_response_json['results']
        else:
            search_results = search_response.json()
            search_facets_json = {}
            search_facets = {}

        # Process number of results found in primary search
        if 'num_found' in search_response.headers:
            try:
                num_found = int(search_response.headers['num_found'])
            except ValueError:
                num_found = 0
        else:
            num_found = 0

        # Setup filters based on the current search
        # NOTE: Facets should be processed separately from filters --
        #       Facets are what are returned by Solr, filters are what are displayed
        #       Some processing will be required to convert between the two
        # TODO: sort filters
        # TODO: add some other filters (e.g. Include Retired)

        # Select filters
        # TODO: Currently this is selecting the filters created only by the facets returned but this
        #       should change to select the actual filters
        searcher.select_filters(self.request.GET)

        # Setup paginator for primary search
        search_paginator = Paginator(range(num_found), searcher.num_per_page)
        search_current_page = search_paginator.page(searcher.current_page)

        # Set context for primary search
        context['page'] = search_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['results'] = search_results
        context['search_type'] = searcher.search_type
        context['search_type_name'] = searcher.search_resource_name
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_facets'] = search_facets

        # Build URL parameters for switching to other resources
        # TODO: should this use GET or search_params?
        allowed_params = ['q', 'limit', 'debug']
        other_resource_search_params = {}
        for param in allowed_params:
            if param in self.request.GET:
                other_resource_search_params[param] = self.request.GET.get(param)
        context['other_resource_search_params'] = ''
        if len(other_resource_search_params):
            context['other_resource_search_params'] = (
                '&' + urllib.urlencode(other_resource_search_params))

        # Perform the counter searches for the other resources
        resource_count = {}
        for resource_type in OCLSearch.resource_type_info:
            if resource_type == searcher.search_type:
                # this search has already been performed, so just set value from above
                resource_count[searcher.search_type] = num_found
            else:
                # Get resource count using same search criteria
                count_response = api.head(resource_type, params=other_resource_search_params)
                if 'num_found' in count_response.headers:
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                else:
                    resource_count[resource_type] = 0
        context['resource_count'] = resource_count

        # debug display variables
        context['get_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_response_headers'] = search_response.headers
        context['search_facets_json'] = search_facets_json

        # to remove closing form tag in nav.html
        context['extend_nav_form'] = True

        return context
