# Basic search
#https://github.com/search?q=malaria&ref=cmdform

# Search by type (when sidebar is clicked)
#https://github.com/search?q=malaria&ref=cmdform&type=Code


from django.views.generic import TemplateView
from django.conf import settings
import requests
import urllib
import math


class HomeSearchView(TemplateView):

    template_name = "ocl_search/search.html"

    def get_context_data(self, *args, **kwargs):

        context = super(HomeSearchView, self).get_context_data(*args, **kwargs)

        # Defaults
        default_search_type = 'concepts'
        default_num_per_page = 2
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

        # Resolves search type to the English singular word form
        search_type_names = {
            'concepts': 'concept',
            'sources': 'source',
            'collections': 'collection',
            'orgs': 'organization',
            'users': 'user'
        }

        # Setup the resource count dictionary        
        resource_count = {}
        for resource_type in search_type_names:
            resource_count[resource_type] = 0

        # Default search type if missing or invalid
        if 'type' in self.request.GET and self.request.GET['type'] in search_type_names:
            search_type = self.request.GET['type']
        else:
            search_type = default_search_type

        # Set parameters for primary search
        search_params = {
            'verbose': 'true'
        }
        if 'q' in self.request.GET:
            search_params['q'] = self.request.GET['q']
        if 'page' in self.request.GET:
            try:
                search_params['page'] = current_page = int(self.request.GET['page'])
            except:
                current_page = 1
        if 'limit' in self.request.GET:
            try:
                search_params['limit'] = num_per_page = int(self.request.GET['limit'])
            except:
                search_params['limit'] = num_per_page = default_num_per_page
        else:
            search_params['limit'] = num_per_page = default_num_per_page

        # Setup API request headers
        search_request_headers = {'Authorization': auth_token}

        # Setup primary search API URL
        search_url = host + search_type_paths[search_type]
        if search_params:
            search_url = search_url + '?' + urllib.urlencode(search_params)

        # Perform the primary search via the API
        # TODO: Improve the handling of search errors
        try:
            search_response = requests.get(url=search_url, headers=search_request_headers)
            search_results = search_response.json()
            search_response_headers = search_response.headers
        except:
            search_response = None
            search_results = []
            search_response_headers = None

        # Setup pagination
        paginator_bar = []
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

            # HACK: Setup paginator bar
            x = 0
            while x < min(num_pages, 2):
                x = x + 1
                paginator_bar.append(x)
            if current_page > 3:
                paginator_bar.append('...')
            if current_page > 2:
                paginator_bar.append(current_page)
            if num_pages > 2 and current_page < (num_pages - 2):
                paginator_bar.append('...')
            if num_pages > 2 and current_page < (num_pages - 1):
                paginator_bar.append(num_pages - 1)
            if num_pages > 2 and current_page < num_pages:
                paginator_bar.append(num_pages)

        pagination = {
            'results_start_index': results_display_start,
            'results_stop_index': results_display_stop,
            'current_page': current_page,
            'total_pages': num_pages,
            'paginator_bar': paginator_bar,
            'search_url_next_page': page_url_next,
            'search_url_prev_page': page_url_prev
        }

        # Perform the counter searches
        if search_response:
            for resource_type in search_type_names:
                if resource_type == search_type:
                    continue
                counter_search_url = host + search_type_paths[resource_type]
                try:
                    count_response = requests.head(url=counter_search_url, headers=search_request_headers)
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                except:
                    resource_count[resource_type] = 0

        # Add data to the context
        context['api_search_query'] = search_url
        context['results'] = search_results
        context['search_type'] = search_type
        context['search_type_name'] = search_type_names[search_type]
        context['search_response_headers'] = search_response_headers
        context['resource_count'] = resource_count
        context['pagination'] = pagination

        return context
