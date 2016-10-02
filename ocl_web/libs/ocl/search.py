"""
Search helper for interfacing web with OCL API.
"""
from django.http import QueryDict
import logging
from .constants import OclConstants


logger = logging.getLogger('oclweb')



## SEARCH FILTER CLASSES

class SearchFilterOption(object):
    """
    Defines a specific search filter option (e.g. English).
    """
    def __init__(
            self, search_filter=None, option_value='',
            option_name='', option_num=0, selected=False):
        self.search_filter = search_filter
        self.option_value = option_value
        self.option_name = option_name
        self.option_num = option_num
        self.selected = selected

    def __repr__(self):
        return "%r: %r [%r] %r" % (self.search_filter.filter_name,
                                   self.option_name,
                                   self.option_num,
                                   self.selected)

class SearchFilter(object):
    """
    A specific search filter (e.g. Locale) and its options (e.g. English).

    options is a dictionary of SearchFilterOption instances
    """
    def __init__(self, filter_id='', filter_name='', filter_widget='',
                 option_defs=None, facet_id='', facet_results=None,
                 minimized=False, attrs=None):

        self.filter_id = filter_id          # unique ID for query etc
        self.filter_name = filter_name      # for display
        self.filter_widget = filter_widget
        self.facet_id = facet_id
        self.facet_results = facet_results
        self.minimized = minimized
        if not attrs:
            attrs = {}
        self.attrs = attrs
        self.option_defs = option_defs
        self.options = []                   # list of search filter options

        if option_defs:
            self.build_options(option_defs=option_defs)

        if facet_results:
            self.build_options_from_facets(facet_results=facet_results)


    def build_options(self, option_defs=None):
        """ Creates filter options from option definitions """
        for option_def in option_defs:
            self.add_option(**option_def)


    def build_options_from_facets(self, facet_results=None):
        """ Creates filter options using the facet results """
        for facet_option in facet_results:
            facet_option_name = facet_option[0]
            facet_option_num = facet_option[1]
            self.add_option(option_value=facet_option_name,
                            option_name=facet_option_name,
                            option_num=facet_option_num)


    def add_option(self, option_value='', option_name='', option_num=0, selected=False):
        """ Add SearchFilterOption to the SearchFilter. """
        self.options.append(SearchFilterOption(
            search_filter=self, option_value=option_value, option_name=option_name,
            option_num=option_num, selected=selected))


    def select_option(self, option_values):
        """
        Mark option(s) as selected according to the value or list of string values passed.
        :param option_values: Value or list of values to select
        """
        if not isinstance(option_values, list):
            option_values = [option_values]
        for opt in self.options:
            if opt.option_value in option_values:
                opt.selected = True

    def __repr__(self):
        return "%r (%r):\n%r" % (self.filter_name, self.filter_id,
                                 [str(opt) for opt in self.options])

class SearchFilterList(object):
    """
    A list of SearchFilter isntances for a specific resource type (e.g. concept, source, etc.).
    """

    def __init__(self, resource_name=''):
        self.resource_name = resource_name
        self.search_filter_list = []


    def match_search_filter(self, filter_id):
        """
        Lookup a search filter by filter_id.

        :returns: Matched SearchFilter or None
        """
        if self.search_filter_list:
            matched_search_filters = filter(lambda f: f.filter_id == filter_id,
                                            self.search_filter_list)
            if matched_search_filters and len(matched_search_filters) > 0:
                return matched_search_filters[0]
        return None


    # TODO(paynejd): Retire this after full implementation of self.add_filter
    def add_search_filter(self, filter_id='', filter_name=''):
        """Create & return new SearchFilter using passed kwargs, add to the SearchFilterList"""
        search_filter = SearchFilter(filter_id, filter_name)
        self.search_filter_list.append(search_filter)
        return search_filter


    def add_filter(self, search_filter):
        """ Add SearchFilter to this SearchFilterList """
        self.search_filter_list.append(search_filter)

    def __iter__(self):
        return self.search_filter_list.__iter__()

    def __repr__(self):
        return 'Resource %r: %r\n\n' % (self.resource_name,
                                        [str(f) for f in self.search_filter_list])



## OCL SEARCH CLASS

class OclSearch(object):
    """
    Helper to handle search queries and processing of search results.
    """

    # Default search values
    DEFAULT_NUM_PER_PAGE = 25
    DEFAULT_SEARCH_TYPE = 'concepts'

    # List of URL parameters that are transferred between searches of different resource types
    # NOTE: This is used to build the resource links on the global search page
    TRANSFERRABLE_SEARCH_PARAMS = ['q', 'limit', 'debug']


    def __init__(self, search_type=None, search_scope=None, params=None):
        """
        :param search_type: Plural of OCL resource name (e.g. 'concepts', 'sources', 'users')
        :param params: dictionary, QueryDict, or string of search params
        """
        # outputs
        self.search_type = search_type
        self.search_scope = search_scope if search_scope else OclConstants.SEARCH_SCOPE_GLOBAL
        self.num_per_page = self.DEFAULT_NUM_PER_PAGE
        self.current_page = None
        self.search_params = {}
        self.search_sort = None
        self.search_query = None
        self.search_facets = None
        self.search_filter_list = None
        self.search_results = None
        self.num_found = None

        # Optionally parse search parameters (i.e. GET request parameters)
        if params is not None:
            self.parse_search_request(params, search_type=search_type)

    # TODO(paynejd@gmail.com): Develop plan to handle search sort options better
    def get_sort_options(self):
        """
        :returns: a list of sort options.
        """
        return [
            'Best Match',
            'Last Update (Desc)',
            'Last Update (Asc)',
            'Name (Asc)',
            'Name (Desc)',
        ]

    def get_sort(self):
        """ Returns the current sort option """
        return '' if self.search_sort is None else self.search_sort

    def get_query(self):
        """ Returns the current query string """
        return '' if self.search_query is None else self.search_query

    def build_filters(self, resource_type, facets=None):
        """
        Builds search filters using filter definitions and facets.
        """
        self.search_filter_list = None
        if resource_type not in OclConstants.SEARCH_FILTER_INFO:
            return
        filter_list = SearchFilterList(resource_name=resource_type)
        for filter_definition in OclConstants.SEARCH_FILTER_INFO[resource_type]:
            # Optionally skip this filter if restricted scope search
            # (See filter definitions in OclConstants for settings for each resource)
            if (self.search_scope == OclConstants.SEARCH_SCOPE_RESTRICTED and
                    'show_with_restricted_scope' in filter_definition and
                    not filter_definition['show_with_restricted_scope']):
                continue

            # Apply the facets returned by the API to the filter definition
            try:
                if (facet and 'facet_id' in filter_definition and
                        filter_definition['facet_id'] in facets):
                    filter_definition['facet_results'] = facets[filter_definition['facet_id']]
                else:
                    filter_definition['facet_results'] = None
            except TypeError:
                filter_definition['facet_results'] = None

            # Create a new FilterDefinition with its facet results, if applicable
            search_filter = SearchFilter(**filter_definition)

            # Do anything that needs to be done to the filter here
            filter_list.add_filter(search_filter)
        self.search_filter_list = filter_list

    def select_search_filters(self, params):
        """
        Sets the selected attribute to true for the specified filter options.

        Filter options must be specified in the URL parameter format.
        """
        if isinstance(self.search_filter_list, SearchFilterList):
            for key in params.keys():
                matched_search_filter = self.search_filter_list.match_search_filter(key)
                if matched_search_filter:
                    matched_search_filter.select_option(params.getlist(key))

    def process_search_results(self, search_type=None, search_response=None,
                               search_params=None, create_filters=True):
        """
        Processes the search results and saves to the searcher in self.search_results and
        self.num_found. If the results contains facets, they are saved to self.search_facets.
        If create_filters is set to True, filters are created and saved to
        self.search_filter_list, taking into account facets as defined by the resource type.
        """

        # Get search results as JSON - for now, passing on exceptions if invalid
        search_response_json = search_response.json()

        # Get the resources from the search results -- If facets were returned,
        # then results live under the 'results' dictionary item. If no facets,
        # then the results are the full JSON response.
        self.search_results = None
        self.search_facets = None
        if 'results' in search_response_json and 'facets' in search_response_json:
            self.search_results = search_response_json['results']
            self.search_facets = search_response_json['facets']['fields']
        else:
            self.search_results = search_response_json

        # Process num_found
        self.num_found = 0
        if 'num_found' in search_response.headers:
            try:
                self.num_found = int(search_response.headers['num_found'])
            except ValueError:
                self.num_found = 0

        # Build filters, sending any facets that were returned
        if create_filters and search_type in OclConstants.SEARCH_FILTER_INFO:
            self.build_filters(search_type, facets=self.search_facets)

        # Select filters based on the search parameters
        self.select_search_filters(search_params)


    def parse_search_request(self, request_get, search_type=None):
        """
        Processes a request string, dict or QueryDict as the input/criteria for an OCL search.
        The parsed search inputs are saved in self.search_params. Set search_type if type=...
        not included in request_get and search_type != DEFAULT_SEARCH_TYPE. type=... in
        request_get takes priority over search_type attribute.

        :params request_get: request string, dictionary or QueryDict of search inputs/criteria
        :params search_type: Plural name of search_type (e.g. 'concepts', 'sources')
        :returns: None
        """

        search_params_dict = {}

        # Verbose - all searches return full resource details, so set verbose to true
        search_params_dict['verbose'] = 'true'

        # Get into QueryDict format if not already and make a copy
        if isinstance(request_get, QueryDict):
            params = request_get.copy()
        elif isinstance(request_get, basestring):
            params = QueryDict(request_get, mutable=True)
        elif isinstance(request_get, dict):
            params = QueryDict('', mutable=True)
            params.update(request_get)
        else:
            raise TypeError('Expected QueryDict, dict, or str.' + str(request_get) + ' passed.')

        # Determine the search type - gets the latest occurence of type
        if 'type' in params and params['type'] in OclConstants.RESOURCE_TYPE_INFO:
            self.search_type = params['type']
        elif search_type and search_type in OclConstants.RESOURCE_TYPE_INFO:
            self.search_type = search_type
        else:
            self.search_type = self.DEFAULT_SEARCH_TYPE
        if 'type' in params:
            del params['type']

        # Paging - gets the latest occurence of type
        if 'page' in params:
            try:
                self.current_page = int(params['page'])
            except ValueError:
                self.current_page = 1
            del params['page']
        else:
            self.current_page = 1
        search_params_dict['page'] = self.current_page

        # Limit - gets the latest occurence of type
        if 'limit' in params:
            try:
                self.num_per_page = int(params['limit'])
            except ValueError:
                self.num_per_page = self.DEFAULT_NUM_PER_PAGE
            del params['limit']
        else:
            self.num_per_page = self.DEFAULT_NUM_PER_PAGE
        search_params_dict['limit'] = self.num_per_page

        # Sort - gets the latest occurence of sort
        sort_direction = None
        sort_field = None
        if 'sort' in params:
            self.search_sort = params.get('sort', '')
            sort = self.search_sort.lower()
            del params['sort']
            if 'asc' in sort:
                sort_direction = 'sortAsc'
            elif 'desc' in sort:
                sort_direction = 'sortDesc'
            if 'last update' in sort:
                sort_field = 'last_update'
            elif 'name' in sort:
                sort_field = 'name'
            if sort_direction and sort_field:
                search_params_dict[sort_direction] = sort_field

        # Query text
        if 'q' in params:
            self.search_query = params.get('q')
            del params['q']
            search_params_dict['q'] = self.search_query

        # Apply facets/filters - everything that's left should be a filter/facet
        # NOTE: Quoting and URL encoding parameters before passing on to API
        for search_filter_key in params.keys():
            search_filter_value = map(lambda x: '"'+x+'"' if ' ' in x else x,
                                      params.pop(search_filter_key))
            search_params_dict[search_filter_key] = ','.join(search_filter_value)

        self.search_params = search_params_dict
