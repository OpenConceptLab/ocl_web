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

        # Default search type to 'concepts' if missing or invalid
        if 'type' in self.request.GET and self.request.GET['type'] in search_type_names:
            search_type = self.request.GET['type']
        else:
            search_type = 'concepts'

        # Grab API settings
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        num_per_page = 2

        # Setup the primary search
        search_params = {}
        search_params['limit'] = num_per_page
        search_params['verbose'] = 'true'
        if 'q' in self.request.GET:
            search_params['q'] = self.request.GET['q']
        search_url = host + search_type_paths[search_type]
        if 'page' in self.request.GET:
            try:
                search_params['page'] = int(self.request.GET['page'])
            except:
                pass
        if search_params:
            search_url = search_url + '?' + urllib.urlencode(search_params)
        request_headers = {'Authorization': auth_token}

        # Perform the primary search using the API
        try:
            response = requests.get(url=search_url, headers=request_headers)
            results = response.json()
            response_headers = response.headers
        except:
            response = None
            results = []
            response_headers = None

        # Setup pagination
        resource_count = {}
        if response:
            num_found = resource_count[search_type] = int(response_headers['num_found'])
            num_returned = int(response_headers['num_returned'])
            offset = int(response_headers['offset'])
            results_display_start = offset + 1
            results_display_stop = results_display_start + num_returned - 1
            num_pages = int(math.ceil(float(num_found) / num_per_page))
            current_page = int(math.ceil(float(offset + 1) / num_per_page))

            # HACK: Setting up paginator
            pages = []
            x = 0
            while x < min(num_pages, 2):
                x = x + 1
                pages.append(x)
            if current_page > 3:
                pages.append('...')
            if current_page > 2:
                pages.append(current_page)
            if num_pages > 2 and current_page < (num_pages - 2):
                pages.append('...')
            if num_pages > 2 and current_page < (num_pages - 1):
                pages.append(num_pages - 1)
            if num_pages > 2 and current_page < num_pages:
                pages.append(num_pages)

        else:
            resource_count[search_type] = -1
            results_display_start = results_display_stop = 0
            num_pages = current_page = 0
        pagination = {
            'start': results_display_start,
            'stop': results_display_stop,
            'currentPage': current_page,
            'totalPages': num_pages,
            'pages': pages,
            'urlNext': '',
            'urlPrevious': ''
        }

        # Perform the counter searches
        if response:
            for resource_type in search_type_names:
                if resource_type == search_type:
                    continue
                counter_search_url = host + search_type_paths[resource_type]
                try:
                    count_response = requests.head(url=counter_search_url, headers=request_headers)
                    resource_count[resource_type] = int(count_response.headers['num_found'])
                except:
                    resource_count[resource_type] = -1

        # Add data to the context
        context['apiSearchQuery'] = search_url
        context['results'] = results
        context['searchType'] = search_type
        context['searchTypeName'] = search_type_names[search_type]
        context['responseHeaders'] = response_headers
        context['resourceCount'] = resource_count
        context['pagination'] = pagination

        return context
