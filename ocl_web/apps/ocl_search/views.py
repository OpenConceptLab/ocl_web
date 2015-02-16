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
            'sources': 'source',
            'collections': 'collection',
            'orgs': 'organization',
            'users': 'user'
        }
        search_type_paths = {
            'concepts': 'concepts',
            'sources': 'sources',
            'collections': 'collections',
            'orgs': 'orgs',
            'users': 'users'
        }

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Setup the resource count dictionary
        resource_count = {}
        for resource_type in search_type_names:
            resource_count[resource_type] = 0

        search_type = self.request.GET.get('type', 'concepts')

        # for now, map string to INT
        resource_type = OCLapi.CONCEPT_TYPE

        if search_type == 'orgs':
            resource_type = OCLapi.ORG_TYPE
        if search_type == 'users':
            resource_type = OCLapi.USER_TYPE
        if search_type == 'sources':
            resource_type = OCLapi.SOURCE_TYPE
        if search_type == 'concepts':
            resource_type = OCLapi.CONCEPT_TYPE
        if search_type == 'collections':
            resource_type = OCLapi.COLLECTION_TYPE

        searcher = OCLSearch(resource_type).parse(self.request.GET)

        # Perform the primary search via the API
        api = OCLapi(self.request, debug=True)
        search_url = search_type_paths[search_type]
        search_response = api.get(search_url, params=searcher.search_params)
        search_results = search_response.json()

        num_found = int(search_response.headers['num_found'])
        # header count for filtered search type set here, the rest is below
        resource_count[search_type] = num_found

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
                if resource_type == search_type:
                    continue
                # Need to apply search criteria to this url
                counter_search_url = search_type_paths[resource_type]
                count_response = api.head(counter_search_url)
                resource_count[resource_type] = int(count_response.headers['num_found'])

        context['resource_count'] = resource_count

        # for debug display only
        context['search_params'] = searcher.search_params
        context['api_search_query'] = search_url
        context['search_response_headers'] = search_response.headers

        context['extend_nav_form'] = True  # to remove closing form tag in nav.html
        return context


class OldHomeSearchView(TemplateView):
    """
    This is not used anymore.
    """
    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Defaults
        default_search_type = 'concepts'
        default_num_per_page = 5
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        page_url = '/search/'

        # Resolves search type to the API path
        search_type_paths = {
            'concepts': '/v1/concepts/',
            'sources': '/v1/sources/',
            'collections': '/v1/collections/',
            'orgs': '/v1/orgs/',
            'users': '/v1/users/'
        }
        search_type_paths = {
            'concepts': 'concepts/',
            'sources': 'sources/',
            'collections': 'collections/',
            'orgs': 'orgs/',
            'users': 'users/'
        }

        # Resolves search type to the English singular word form
        search_type_names = {
            'concepts': 'concept',
            'sources': 'source',
            'collections': 'collection',
            'orgs': 'organization',
            'users': 'user'
        }

        # URL parameters that can be passed on to the search API (excluding paging)
        allowed_api_parameters = {
            'concept_class': 'concept_class',
            'datatype': 'concept_class',
            'source_type': 'concept_class',
            'collection_type': 'concept_class',
            'locale': 'concept_class',
            'q': 'concept_class'
        }

        # Setup filters
        # Note: this should be automatically populated based on the data
        search_filter = {}
        search_filter['concepts'] = {}
        search_filter['concepts']['concept_class'] = {
            'filter_id': 'concept_class',
            'name': 'Concept Classes',
            'options': [
                'Anatomy',
                'Diagnosis',
                'Drug',
                'Finding',
                'Symptom',
                'Test',
                'Procedure',
                'Indicator',
                'Frequency',
                'Misc',
                'ConvSet',
                'Organism',
                'Question',
                'Program'
            ]
        }
        search_filter['concepts']['datatype'] = {
            'filter_id': 'datatype',
            'name': 'Datatypes',
            'options': [
                'Boolean',
                'Coded',
                'Complex',
                'Date',
                'Datetime',
                'Document',
                'None',
                'Numeric',
                'Rule',
                'Structured Numeric',
                'Text',
                'Time'
            ]
        }
        search_filter['sources'] = {}
        search_filter['sources']['source_type'] = {
            'filter_id': 'source_type',
            'name': 'Source Types',
            'options': [
                'Dictionary',
                'Interface Terminology',
                'Indicator Registry'
            ]
        }
        search_filter['sources']['locale'] = {
            'filter_id': 'locale',
            'name': 'Locales',
            'options': [
                'en', 'sw', 'fr', 'sp', 'ru'
            ]
        }
        search_filter['collections'] = {}
        search_filter['collections']['collection_type'] = {
            'filter_id': 'collection_type',
            'name': 'Collection Types',
            'options': [
                'Subset',
                'Starter Set'
            ]
        }
        search_filter['collections']['locale'] = {
            'filter_id': 'locale',
            'name': 'Locales',
            'options': [
                'en', 'sw', 'fr', 'sp', 'ru'
            ]
        }
        search_filter['users'] = {}
        search_filter['orgs'] = {}

        # Setup the resource count dictionary
        resource_count = {}
        for resource_type in search_type_names:
            resource_count[resource_type] = 0

        # Copy the GET parameters
        get_params = self.request.GET.copy()

        # Default search type if missing or invalid
        if 'type' in get_params and get_params['type'] in search_type_names:
            search_type = get_params['type']
            del get_params['type']
        else:
            search_type = default_search_type

        # Set parameters for primary search
        search_params = {
            'verbose': 'true'
        }
        # pagination parameters
        if 'page' in get_params:
            try:
                search_params['page'] = current_page = int(get_params['page'])
                del get_params['page']
            except:
                current_page = 1
        if 'limit' in self.request.GET:
            try:
                search_params['limit'] = num_per_page = int(self.request.GET['limit'])
            except:
                search_params['limit'] = num_per_page = default_num_per_page
        else:
            search_params['limit'] = num_per_page = default_num_per_page
        # all the other parameters
        for key in get_params.keys():
            if key in allowed_api_parameters:
                search_params[key] = get_params.pop(key)
                search_params[key] = self.request.GET[key]

        # Setup API request headers
        search_request_headers = {'Authorization': auth_token}

        # Setup primary search API URL
        search_url = host + search_type_paths[search_type]
        search_url = search_type_paths[search_type]
#        if search_params:
#            search_url = search_url + '?' + urllib.urlencode(search_params)

        # Perform the primary search via the API
        # TODO: Improve the handling of search errors
        try:
            print 'search_url:', search_url
            print 'search_params', search_params
            print 'API GET'
            api = OCLapi(self.request, debug=True)
            search_response = api.get(search_url, params=search_params)
#            search_response = requests.get(url=search_url, headers=search_request_headers)
            search_results = search_response.json()
            search_response_headers = search_response.headers
        except:
            search_response = None
            search_results = []
            search_response_headers = None
            logger.exception('calling search API')

        # Setup pagination
        paginator_bar = []
        show_paginator_bar = False
        results_display_start = results_display_stop = 0
        num_pages = current_page = 0
        page_url_prev = ''
        page_url_next = ''
        if search_response:
            num_found = resource_count[search_type] = int(search_response_headers['num_found'])
            num_returned = int(search_response_headers['num_returned'])
            offset = int(search_response_headers['offset'])  # 0-index
            results_display_start = offset + 1  # 1-index
            results_display_stop = results_display_start + num_returned - 1  # 1-index
            num_pages = int(math.ceil(float(num_found) / num_per_page))  # 1-index
            current_page = int(math.ceil(float(offset + 1) / num_per_page))  # 1-index

            # Build previous page url
            if current_page > 1:
                page_params_prev = self.request.GET.copy()
                page_params_prev['page'] = current_page - 1
                page_url_prev = page_url + '?' + urllib.urlencode(page_params_prev)

            # Build next page url
            if current_page < num_pages:
                page_params_next = self.request.GET.copy()
                page_params_next['page'] = current_page + 1
                page_url_next = page_url + '?' + urllib.urlencode(page_params_next)

            # Build paginator bar
            if num_pages > 1:
                show_paginator_bar = True
                paginator_bar = self.buildPaginatorBar(base_url=page_url,
                    default_url_params=self.request.GET, num_pages=num_pages,
                    current_page=current_page)

        pagination = {
            'results_start_index': results_display_start,
            'results_stop_index': results_display_stop,
            'current_page': current_page,
            'total_pages': num_pages,
            'show_paginator_bar': show_paginator_bar,
            'paginator_bar': paginator_bar,
            'search_url_next_page': page_url_next,
            'search_url_prev_page': page_url_prev
        }

        # Perform the counter searches
        if search_response:
            for resource_type in search_type_names:
                if resource_type == search_type:
                    continue
#                counter_search_url = host + search_type_paths[resource_type]
                counter_search_url = search_type_paths[resource_type]

#                if search_params:
#                    counter_search_url = counter_search_url + '?' + urllib.urlencode(search_params)

                try:
#                    count_response = requests.head(url=counter_search_url, headers=search_request_headers)
                    count_response = api.head(counter_search_url, params=search_params)

                    resource_count[resource_type] = int(count_response.headers['num_found'])
                except:
                    resource_count[resource_type] = 0

        # Add data to the context
        context['search_filter'] = search_filter[search_type]
        context['search_params'] = search_params
        context['api_search_query'] = search_url
        context['results'] = search_results
        context['search_type'] = search_type
        context['search_type_name'] = search_type_names[search_type]
        context['search_response_headers'] = search_response_headers
        context['resource_count'] = resource_count
        context['pagination'] = pagination
        return context

    def buildPaginatorBar(self, base_url='', default_url_params={},
                          num_pages=1, current_page=1):
        paginator_bar = []
        for i in range(1, 3):
            if i <= num_pages:
                paginator_bar.append(self.buildPaginatorPage(base_url=base_url,
                    default_url_params=default_url_params, display=i, page_number=i,
                    current_page=current_page))
        if (current_page - 4) > 3:
            paginator_bar.append(self.buildPaginatorPage(display='...', disabled=True))
        for i in range(current_page - 4, current_page + 5):
            if i <= num_pages and i > 2:
                paginator_bar.append(self.buildPaginatorPage(base_url=base_url,
                    default_url_params=default_url_params, display=i, page_number=i,
                    current_page=current_page))
        if num_pages - 2 > current_page + 4 + 1:
            paginator_bar.append(self.buildPaginatorPage(display='...', disabled=True))
        for i in range(num_pages - 1, num_pages + 1):
            if i > current_page + 4:
                paginator_bar.append(self.buildPaginatorPage(base_url=base_url,
                    default_url_params=default_url_params, display=i, page_number=i,
                    current_page=current_page))
        return paginator_bar

    def buildPaginatorPage(self, base_url='', default_url_params=None, display='',
        page_number=None, current_page=None, disabled=False):
        paginator_page = {
            'display': display
        }
        if page_number is not None:
            paginator_page['page_num'] = page_number
            if page_number == current_page:
                paginator_page['current_page'] = True
        if disabled:
            paginator_page['disabled'] = True
        else:
            url_params = default_url_params.copy()
            if page_number is not None:
                url_params['page'] = page_number
            paginator_page['url'] = base_url + '?' + urllib.urlencode(url_params)
        return paginator_page
 
