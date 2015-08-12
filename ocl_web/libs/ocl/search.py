""" Search helper for interfacing web with OCL API. """
from django.http import QueryDict
#from urllib import quote
import logging

logger = logging.getLogger('oclweb')


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

    def __str__(self):
        return "%s: %s [%s] %s" % (self.search_filter.search_filter_name,
                                   self.option_name,
                                   self.option_num,
                                   self.selected)

    def __unicode__(self):
        return u"%s: %s [%s] %s" % (self.search_filter.search_filter_name,
                                    self.option_name,
                                    self.option_num,
                                    self.selected)



class SearchFilter(object):
    """
    A specific search filter (e.g. Locale) and its options (e.g. English).

    options is a dictionary of SearchFilterOption instances
    """
    def __init__(self, search_filter_id='', search_filter_name=''):
        self.search_filter_id = search_filter_id      # unique ID for query etc
        self.search_filter_name = search_filter_name  # for display
        self.options = {}                             # a dictionary of search filter options

    def add_option(self, option_value='', option_name='', option_num=0, selected=False):
        """Add SearchFilterOption to the SearchFilter.
        """
        self.options[option_value] = SearchFilterOption(
            search_filter=self, option_value=option_value, option_name=option_name,
            option_num=option_num, selected=selected)

    def select_option(self, option_values):
        """Mark as selected the option(s) according to the value or list of string values passed.
        """
        if not isinstance(option_values, list):
            option_values = [option_values]
        for i in self.options:
            if self.options[i].option_value in option_values:
                self.options[i].selected = True

    def __str__(self):
        return "%s (%s): %s" % (self.search_filter_name,
                                self.search_filter_id,
                                [str(self.options[k]) for k in self.options.keys()])

    def __unicode__(self):
        return "%s (%s): %s" % (self.search_filter_name,
                                self.search_filter_id,
                                [str(self.options[k]) for k in self.options.keys()])



class SearchFilterList(object):
    """
    A list of SearchFilter isntances for a specific resource type (e.g. concept, source, etc.).
    """
    def __init__(self, resource_name=''):
        self.resource_name = resource_name
        self.search_filter_list = []

    def match_search_filter(self, search_filter_id):
        """
        Lookup a search filter by search_filter_id.

        :returns: Matched SearchFilter or None
        """
        matched_search_filters = filter(lambda f: f.search_filter_id == search_filter_id,
                                        self.search_filter_list)
        if len(matched_search_filters) == 0:
            return None
        else:
            return matched_search_filters[0]

    def add_search_filter(self, search_filter_id='', search_filter_name=''):
        """Add SearchFilter to the SearchFilterList.
        """
        search_filter = SearchFilter(search_filter_id, search_filter_name)
        self.search_filter_list.append(search_filter)
        return search_filter

    def __iter__(self):
        return self.search_filter_list.__iter__()

    def __str__(self):
        return 'Resource %s: %s\n\n' % (self.resource_name,
                                        [str(f) for f in self.search_filter_list])

    def __unicode__(self):
        return 'Resource %s: %s\n\n' % (self.resource_name,
                                        [str(f) for f in self.search_filter_list])



class OclSearch(object):
    """
    Helper to handle search queries and processing of search results.
    """

    # Resource types
    # TODO(paynejd@gmail.com): Resource type constants are duplicated in OclApi
    # TODO(paynejd@gmail.com): Standardized resource type representation
    # NOTE: Code uses mixture of integers (ORG_TYPE=1), singular text ('org'), and plural ('orgs')
    USER_TYPE = 0
    ORG_TYPE = 1
    SOURCE_TYPE = 2
    CONCEPT_TYPE = 3
    COLLECTION_TYPE = 4
    MAPPING_TYPE = 5
    SOURCE_VERSION_TYPE = 6
    CONCEPT_VERSION_TYPE = 7

    # Default search values
    DEFAULT_NUM_PER_PAGE = 25
    DEFAULT_SEARCH_TYPE = 'concepts'

    # List of URL parameters that are transferred between searches of different resource types
    # NOTE: This is used to build the resource links on the global search page
    TRANSFERRABLE_SEARCH_PARAMS = ['q', 'limit', 'debug']

    # Search filter definitions for each resource
    SEARCH_FILTER_INFO = {
        'concepts': [
            {'id':'source', 'display_name':'Source', 'filter_widget':'checkboxes', 'facet':'source'},
            {'id':'conceptClass', 'display_name':'Concept Class', 'filter_widget':'checkboxes', 'facet':'conceptClass'},
            {'id':'datatype', 'display_name':'Datatype', 'filter_widget':'checkboxes', 'facet':'datatype'},
            {'id':'includeRetired', 'display_name':'Include Retired''filter_widget':'include_retired'},
            {'id':'retired', 'display_name':'Retired', 'filter_widget':'checkboxes', 'filter_widget':'checkboxes', 'facet':'retired', 'minimized':True},
            {'id':'owner', 'display_name':'Concept Owner', 'filter_widget':'checkboxes', 'filter_widget':'checkboxes', 'facet':'owner'},
            {'id':'locale', 'display_name':'Locale', 'filter_widget':'checkboxes', 'filter_widget':'checkboxes', 'facet':'locale'},
            {'id':'ownerType', 'display_name':'Owner Type', 'filter_widget':'checkboxes', 'filter_widget':'checkboxes', 'facet':'ownerType', 'minimized':True},
        ],
        'mappings': [
            {'id':'mapType', 'display_name':'Map Type', 'filter_widget':'checkboxes', 'facet':'mapType'},
            {'id':'source', 'display_name':'Mapping Source', 'filter_widget':'checkboxes', 'facet':'source'},
            {'id':'includeRetired', 'display_name':'Include Retired', 'filter_widget':'include_retired'},
            {'id':'retired', 'display_name':'Retired', 'filter_widget':'checkboxes', 'facet':'retired', 'minimized':True},
            {'id':'conceptOwner', 'display_name':'Concept Owner', 'filter_widget':'checkboxes', 'facet':'conceptOwner'},
            {'id':'conceptSource', 'display_name':'Concept Source', 'filter_widget':'checkboxes', 'facet':'conceptSource'},
            {'id':'conceptOwnerType', 'display_name':'Concept Owner Type', 'filter_widget':'checkboxes', 'facet':'conceptOwnerType', 'minimized':True},
            {'id':'toConceptSource', 'display_name':'To Concept Source', 'filter_widget':'checkboxes', 'facet':'toConceptSource', 'minimized':True},
            {'id':'toConceptOwner', 'display_name':'To Concept Owner', 'filter_widget':'checkboxes', 'facet':'toConceptOwner', 'minimized':True},
            {'id':'toConceptOwnerType', 'display_name':'To Concept Owner Type', 'filter_widget':'checkboxes', 'facet':'toConceptOwnerType', 'minimized':True},
            {'id':'fromConceptSource', 'display_name':'From Concept Source', 'filter_widget':'checkboxes', 'facet':'fromConceptSource', 'minimized':True},
            {'id':'fromConceptOwnerType', 'display_name':'From Concept Owner Type', 'filter_widget':'checkboxes', 'facet':'fromConceptOwnerType', 'minimized':True},
            {'id':'fromConceptOwner', 'display_name':'From Concept Owner', 'filter_widget':'checkboxes', 'facet':'fromConceptOwner', 'minimized':True},
            {'id':'owner', 'display_name':'Mapping Owner', 'filter_widget':'checkboxes', 'facet':'owner', 'minimized':True},
            {'id':'ownerType', 'display_name':'Mapping Owner Type', 'filter_widget':'checkboxes', 'facet':'ownerType', 'minimized':True},
        ],
        'sources': [
            {'id':'sourceType', 'display_name':'Source Type', 'filter_widget':'checkboxes', 'facet':'sourceType'},
            {'id':'owner', 'display_name':'Owner', 'filter_widget':'checkboxes', 'facet':'owner'},
            {'id':'ownerType', 'display_name':'Owner Type', 'filter_widget':'checkboxes', 'facet':'ownerType'},
            {'id':'locale', 'display_name':'Supported Locale', 'filter_widget':'checkboxes', 'facet':'locale'},
        ],
        'collections': [],
        'orgs': [],
        'users': [],
        'source_versions': [],
        'concept_versions': [],
    }

    # Resource type definitions
    RESOURCE_TYPE_INFO = {
        'concepts': {'int':CONCEPT_TYPE, 'name':'concept', 'facets':True},
        'mappings': {'int':MAPPING_TYPE, 'name':'mapping', 'facets':True},
        'sources': {'int':SOURCE_TYPE, 'name':'source', 'facets':True},
        'collections': {'int':COLLECTION_TYPE, 'name':'collection', 'facets':True},
        'orgs': {'int':ORG_TYPE, 'name':'organization', 'facets':False},
        'users': {'int':USER_TYPE, 'name':'user', 'facets':False},
        'source_versions': {'int':SOURCE_VERSION_TYPE, 'name':'version', 'facets':False},
        'concept_versions': {'int':CONCEPT_VERSION_TYPE, 'name':'concept version', 'facets':False},
    }


    def __init__(self, search_type='', params=None):
        """
        :param search_type: Plural text of OCL resource (e.g. 'concepts', 'sources', 'users')
        :param params: dictionary, QueryDict, or string of search params
        """
        # outputs
        self.search_type = search_type
        self.num_per_page = self.DEFAULT_NUM_PER_PAGE
        self.current_page = None
        self.search_params = {}
        self.search_sort = None
        self.search_query = None
        self.search_filter_list = None
        self.search_results = None
        self.num_found = None

        # Optionally parse search parameters (i.e. GET request parameters)
        if params is not None:
            self.parse_search_request(params)

    @property
    def search_resource_id(self):
        """Get numeric resource identifier."""
        if self.search_type in self.RESOURCE_TYPE_INFO:
            return self.RESOURCE_TYPE_INFO[self.search_type]['int']
        else:
            return None

    @property
    def search_resource_name(self):
        """Get singular display name of the resource."""
        if self.search_type in self.RESOURCE_TYPE_INFO:
            return self.RESOURCE_TYPE_INFO[self.search_type]['name']
        else:
            return ''

    @property
    def search_resource_has_facets(self):
        """Get whether the set resource type supports facets."""
        if self.search_type in self.RESOURCE_TYPE_INFO:
            return self.RESOURCE_TYPE_INFO[self.search_type]['facets']
        else:
            return False

    # TODO(paynejd@gmail.com): Use OclSearch.get_search_filters to create SearchFilterList
    def get_search_filters(self):
        """
        Get the search filters applicable for this search object type.
        The searfch filters returned will have state information of the current search criteria,
        i.e. checkboxes can stay checked.

        :returns: a list of SearchFilter object for constructing the HTML filter display.
        """
        return self.search_filter_list[self.search_type]

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
        """
        Returns the current sort option
        """
        return '' if self.search_sort is None else self.search_sort


    def get_query(self):
        """
        Returns the current query string
        """
        return '' if self.search_query is None else self.search_query

    def process_facets(self, resource_type='', facets=None):
        """
        Processes facets into a SearchFilterList object as returned by a Solr search.

        :params resource_type: Resource type
        :params facets: Dictionary of the form { 'fields':{ } }
        :returns: SearchFilterList
        """
        filter_list = None
        if isinstance(facets, dict) and 'fields' in facets and isinstance(facets['fields'], dict):
            filter_list = SearchFilterList(resource_name=resource_type)
            for facet in facets['fields']:
                # TODO: Need method to convert field name to display name
                facet_display_name = facet
                search_filter = filter_list.add_search_filter(
                    search_filter_id=facet, search_filter_name=facet_display_name)
                for facet_option in facets['fields'][facet]:
                    facet_option_name = facet_option[0]
                    facet_option_num = facet_option[1]
                    search_filter.add_option(option_value=facet_option_name,
                                             option_name=facet_option_name,
                                             option_num=facet_option_num)
        self.search_filter_list = filter_list
        return filter_list

    def select_search_filters(self, params):
        """
        Sets the selected attribute to true for the specified filter options.

        Filter options must be specified in the URL parameter format.
        """
        print 'Selecting search filters...'
        if isinstance(self.search_filter_list, SearchFilterList):
            for key in params.keys():
                print 'Attempting to select search filter: %s = %s' % (key, params.getlist(key))
                matched_search_filter = self.search_filter_list.match_search_filter(key)
                if matched_search_filter:
                    matched_search_filter.select_option(params.getlist(key))
                print '\tMatched search filter:', matched_search_filter


    def process_search_results(self, search_type=None, search_response=None,
                               has_facets=False, search_params=None):
        """
        Processes the search results and saves to the searcher in
        self.search_results, and self.num_found. If has_facets is set to True,
        processes facets, selects options from search_params, and saves to
        self.search_filter_list.
        """
        search_response_json = search_response.json()

        # Create the filter lists based on the returned facets
        # TODO(paynejd@gmail.com): Create filter list based on filter definitions and
        # populate the filter options based on the facets
        if has_facets and 'facets' in search_response_json:
            self.process_facets(search_type, search_response_json['facets'])
            self.select_search_filters(search_params)

        # Get the resources from the search results -- if facets were returned,
        # then results live under the 'results' dictionary item. If no facets,
        # then the results are the full JSON response
        self.search_results = None
        if has_facets and 'results' in search_response_json:
            self.search_results = search_response_json['results']
        elif not has_facets:
            self.search_results = search_response_json

        # Process num_found
        self.num_found = 0
        if 'num_found' in search_response.headers:
            try:
                self.num_found = int(search_response.headers['num_found'])
            except ValueError:
                self.num_found = 0


    def parse_search_request(self, request_get):
        """
        Parse processes a request string, dictionary or QueryDict as the input/criteria for an
        OCL search. The parsed search inputs are saved in self.search_params

        :params request_get: request string, dictionary or QueryDict of search inputs/criteria
        :returns: None
        """

        search_params_dict = {}

        # Verbose - all searches return full resource details, so set verbose to true
        search_params_dict['verbose'] = 'true'

        # Get into QueryDict format if not already and make a copy
        print 'parsing:', request_get
        if isinstance(request_get, QueryDict):
            params = request_get.copy()
        elif isinstance(request_get, basestring):
            params = QueryDict(request_get, mutable=True)
        elif isinstance(request_get, dict):
            params = QueryDict('', mutable=True)
            params.update(request_get)
        else:
            raise TypeError('Expected QueryDict, dict, or str, but ' + str(request_get) + ' passed')

        # Determine the search type - gets the latest occurence of type
        if 'type' in params:
            if params['type'] in self.RESOURCE_TYPE_INFO:
                self.search_type = params['type']
            else:
                self.search_type = self.DEFAULT_SEARCH_TYPE
            del params['type']
        else:
            self.search_type = self.DEFAULT_SEARCH_TYPE
        print 'search type:', self.search_type

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
        print 'page:', self.current_page

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
        print 'limit:', self.num_per_page

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
        print 'sort:', self.search_sort, sort_direction, ':', sort_field

        # Query text
        if 'q' in params:
            self.search_query = params.get('q')
            del params['q']
            search_params_dict['q'] = self.search_query
        print 'q:', self.search_query

        # Apply facets/filters - everything that's left should be a filter/facet
        # NOTE: Quoting and URL encoding parameters before passing on to API
        for search_filter_key in params.keys():
            search_filter_value = map(lambda x: '"'+x+'"' if ' ' in x else x,
                                      params.pop(search_filter_key))
            search_params_dict[search_filter_key] = ','.join(search_filter_value)
            print 'search filter [%s] = %s' % (search_filter_key,
                                               search_params_dict[search_filter_key])

        self.search_params = search_params_dict
        print 'Searcher %s params: %s' % (self.search_type, search_params_dict)
