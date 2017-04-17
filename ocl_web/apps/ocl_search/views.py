"""Views for OCL Global search

Examples:
https://openconceptlab.org/search?q=malaria
https://openconceptlab.org/search?q=oncology&type=sources
"""
import logging

from django.views.generic import TemplateView
from django.http import Http404
from django.core.paginator import Paginator
from django.utils.http import urlencode
from apps.core.utils import SearchStringFormatter
from libs.ocl import (OclApi, OclSearch, OclConstants)


logger = logging.getLogger('oclweb')


class GlobalSearchView(TemplateView):
    """ View for global OCL search """

    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):
        """ Set context for OCL global search """

        context = super(GlobalSearchView, self).get_context_data(*args, **kwargs)

        # Perform the primary search via the API
        original_search_string = self.request.GET.get('q', '')
        SearchStringFormatter.add_wildcard(self.request)

        searcher = OclSearch(params=self.request.GET)

        api = OclApi(
            self.request, debug=True,
            facets=OclConstants.resource_has_facets(searcher.search_type))

        search_response = api.get(searcher.search_type, params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the primary search results
        searcher.process_search_results(
            search_type=searcher.search_type,
            search_response=search_response,
            search_params=self.request.GET)

        # Setup paginator for primary search
        search_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_current_page = search_paginator.page(searcher.current_page)

        # Set context for primary search
        context['results'] = searcher.search_results
        context['page'] = search_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_type'] = searcher.search_type
        context['search_type_name'] = OclConstants.resource_display_name(searcher.search_type)
        context['search_type_icon'] = OclConstants.resource_display_icon(searcher.search_type)
        context['search_sort_option_defs'] = searcher.get_sort_option_definitions()
        context['search_sort'] = searcher.get_sort()
        context['search_filters'] = searcher.search_filter_list
        context['search_query'] = original_search_string
        context['hide_nav_search'] = True

        if self.request.user.is_authenticated() and searcher.search_type in ['concepts', 'mappings']:
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Build URL params for navigating to other resources
        other_resource_search_params = {}
        for param in OclSearch.TRANSFERRABLE_SEARCH_PARAMS:
            if param in self.request.GET:
                if param == 'q':
                    other_resource_search_params[param] = original_search_string
                else:
                    other_resource_search_params[param] = self.request.GET.get(param)

        # Encode the search parameters into a single URL-encoded string so that it can
        #   easily be appended onto URL links on the search page
        context['other_resource_search_params'] = ''
        if other_resource_search_params:
            context['other_resource_search_params'] = (
                '&' + urlencode(other_resource_search_params))

        # Perform the counter searches for the other resources
        resource_count = {}
        for resource_type in OclConstants.RESOURCE_TYPE_INFO:
            if resource_type == searcher.search_type:
                # Primary search has already been performed, so just set value from above
                resource_count[searcher.search_type] = searcher.num_found
            elif OclConstants.RESOURCE_TYPE_INFO[resource_type]['show_on_global_search']:
                # Get resource count applying transferrable search criteria
                count_response = api.head(resource_type, params=other_resource_search_params)
                if 'num_found' in count_response.headers:
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                else:
                    resource_count[resource_type] = 0
        context['resource_count'] = resource_count

        # Set debug variables
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_response_headers'] = search_response.headers
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context
