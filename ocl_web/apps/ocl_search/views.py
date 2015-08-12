"""Views for OCL Global search

Examples:
https://github.com/search?q=malaria&ref=cmdform
https://github.com/search?q=malaria&ref=cmdform&type=Concept
"""
import logging

from django.views.generic import TemplateView
from django.http import Http404
from django.core.paginator import Paginator
import urllib
from libs.ocl import (OclApi, OclSearch)


logger = logging.getLogger('oclweb')


class GlobalSearchView(TemplateView):
    """ View for global OCL search """

    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):
        """ Set context for OCL global search_type """

        context = super(GlobalSearchView, self).get_context_data(*args, **kwargs)

        # Setup the OCL Search helper class
        searcher = OclSearch(params=self.request.GET)

        # Perform the primary search via the API
        api = OclApi(self.request, debug=True, facets=searcher.search_resource_has_facets)
        search_response = api.get(searcher.search_type, params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the primary search results
        searcher.process_search_results(
            search_type=searcher.search_type, search_response=search_response,
            has_facets=searcher.search_resource_has_facets, search_params=searcher.search_params)

        #if searcher.search_resource_has_facets:
        #    search_response_json = search_response.json()
        #    search_facets_json = search_response_json['facets']
        #    search_facets = searcher.process_facets(searcher.search_type, search_facets_json)
        #    search_results = search_response_json['results']
        #else:
        #    search_results = search_response.json()
        #    search_facets_json = {}
        #    search_facets = {}

        # Process number of results found in primary search
        #if 'num_found' in search_response.headers:
        #    try:
        #        num_found = int(search_response.headers['num_found'])
        #    except ValueError:
        #        num_found = 0
        #else:
        #    num_found = 0

        # Setup filters based on the current search
        # NOTE: Facets should be processed separately from filters --
        #       Facets are what are returned by Solr, filters are what are displayed
        #       Some processing will be required to convert between the two
        # TODO: sort filters
        # TODO: add some other filters (e.g. Include Retired)

        # Select filters
        # TODO: Currently this is selecting the filters created only by the facets returned but this
        #       should change to select the actual filters
        #searcher.select_search_filters(self.request.GET)

        # Setup paginator for primary search
        search_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_current_page = search_paginator.page(searcher.current_page)

        # Set context for primary search
        context['page'] = search_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['results'] = searcher.search_results
        context['search_type'] = searcher.search_type
        context['search_type_name'] = searcher.search_resource_name
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_facets'] = searcher.search_filter_list

        # Build URL params for navigating to other resources
        other_resource_search_params = {}
        for param in OclSearch.TRANSFERRABLE_SEARCH_PARAMS:
            if param in self.request.GET:
                other_resource_search_params[param] = self.request.GET.get(param)
        context['other_resource_search_params'] = ''
        if other_resource_search_params:
            context['other_resource_search_params'] = (
                '&' + urllib.urlencode(other_resource_search_params))

        # Perform the counter searches for the other resources
        resource_count = {}
        for resource_type in OclSearch.RESOURCE_TYPE_INFO:
            if resource_type == searcher.search_type:
                # Primary search has already been performed, so just set value from above
                resource_count[searcher.search_type] = searcher.num_found
            else:
                # Get resource count applying transferrable search criteria
                count_response = api.head(resource_type, params=other_resource_search_params)
                if 'num_found' in count_response.headers:
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                else:
                    resource_count[resource_type] = 0
        context['resource_count'] = resource_count

        # Set debug variables
        context['get_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_response_headers'] = search_response.headers
        #context['search_facets_json'] = search_facets_json

        # Set to remove closing form tag in nav.html -- retire in the future
        context['extend_nav_form'] = True

        return context
