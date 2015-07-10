""" Search helper for interfacing web with OCL API. """
from django.http import QueryDict
#from urllib import quote
import logging

logger = logging.getLogger('oclweb')


class SearchFilterOption(object):
    """Defines a specific search filter option
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
        return "%s: %s [%s] %s" % (self.search_filter.search_filter_name,
                                   self.option_name,
                                   self.option_num,
                                   self.selected)



class SearchFilter(object):
    """A specific search filter for searching OCL

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
    """A list of filter spec for a specific resource type (concept, source, etc)
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



# TOOD(paynejd@gmail.com): Only setup_filters uses this -- possibly retire?
def turn_to_tuples(values):
    """
    Temporary util to turn a list of values into a list of json friendly dictionary.
    Used to translate the concept_class_list type of lists to a code/name tuple
    list for used in filter.

    Once we clean up these lists to be all code/name pair this will go away.

    """
    if isinstance(values[0], dict):
        # already a list of dictionary, just add "selected"
        for d in values:
            d['selected'] = False
        return values
    else:
        # input is a list of codes which are the same as values, split up into
        # code, value and selected dictionary
        return [{'code': v, 'name': v, 'selected': False} for v in values]



# TODO(paynejd@gmail.com): Replace with new facets/filter methodology
def setup_filters():
    """Sets up filters with static options. Deprecated.
    """
    from apps.core.views import _get_concept_class_list
    from apps.core.views import _get_datatype_list
    from apps.core.views import _get_source_type_list
    from apps.core.views import _get_locale_list

    # concept filters
    filters = SearchFilterList('concepts')
    f = filters.add_search_filter('concept_class', 'Concept Classes')
    f.options = turn_to_tuples(_get_concept_class_list())

    f = filters.add_search_filter('datatype', 'Datatypes')
    f.options = turn_to_tuples(_get_datatype_list())

    f = filters.add_search_filter('locale', 'Locale')
    f.options = turn_to_tuples(_get_locale_list())

    f = filters.add_search_filter('includeRetired', 'Include Retired')
    f.options = turn_to_tuples([{'code': u'1', 'name': 'Retired'}])
    concept_filters = filters

    # source filter
    filters = SearchFilterList('sources')
    f = filters.add_search_filter('source_type', 'Source Types')
    f.options = turn_to_tuples(_get_source_type_list())

    f = filters.add_search_filter('language', 'Locale')
    f.options = _get_locale_list()
    source_filters = filters

    # collection filters
    filters = SearchFilterList('collections')
    f = filters.add_search_filter('collection_type', 'Collection Types')
    f.options = turn_to_tuples(['Dictionary',
                                'Interface Terminology',
                                'Indicator Registry',
                                'Reference',
                                'External'])

    f = filters.add_search_filter('language', 'Locale')
    f.options = _get_locale_list()
    collection_filters = filters

    # mapping filters
    filters = SearchFilterList('mappings')
    f = filters.add_search_filter('collection_type', 'Collection Types')
    f.options = turn_to_tuples(['Dictionary',
                                'Interface Terminology',
                                'Indicator Registry',
                                'Reference',
                                'External'])
    mapping_filters = filters

    user_filters = None
    org_filters = None

    return [user_filters, org_filters, source_filters, concept_filters,
            collection_filters, mapping_filters]



class OCLSearch(object):
    """Helper to handle search query URL

    type=concepts|sources|collections|orgs|users
    page=N
    limit=N
    """

    # resource types
    USER_TYPE = 0
    ORG_TYPE = 1
    SOURCE_TYPE = 2
    CONCEPT_TYPE = 3
    COLLECTION_TYPE = 4
    MAPPING_TYPE = 5

    #defaults
    DEFAULT_NUM_PER_PAGE = 25
    DEFAULT_SEARCH_TYPE = 'concepts'

    search_filter_info = {
        'concepts': [
            {'id': 'source', 'display_name': 'Sources', 'facet': 'source'},
            {'id': 'conceptClass', 'display_name': 'Concept Classes', 'facet': 'conceptClass'},
            {'id': 'datatype', 'display_name': 'Datatype', 'facet': 'datatype'},
            {'id': 'includeRetired', 'display_name': 'Include Retired'},
            {'id': 'retired', 'display_name': 'Retired', 'facet': 'retired'},
            {'id': 'owner', 'display_name': 'Owner', 'facet': 'owner'},
            {'id': 'ownerType', 'display_name': 'Owner Type', 'facet': 'ownerType'},
            {'id': 'locale', 'display_name': 'Locale', 'facet': 'locale'}
        ],
        'mappings': [
            {'id': 'source', 'display_name': 'Sources', 'facet': 'source'},
            {'id': 'conceptClass', 'display_name': 'Concept Classes', 'facet': 'conceptClass'},
            {'id': 'datatype', 'display_name': 'Datatype', 'facet': 'datatype'},
            {'id': 'retired', 'display_name': 'Retired', 'facet': 'retired'},
            {'id': 'owner', 'display_name': 'Owner', 'facet': 'owner'},
            {'id': 'ownerType', 'display_name': 'Owner Type', 'facet': 'ownerType'},
            {'id': 'locale', 'display_name': 'Locale', 'facet': 'locale'}
        ],
        'source': [
            {'id': 'sourceType', 'display_name': 'Source Type', 'facet': 'sourceType'},
            {'id': 'owner', 'display_name': 'Owner', 'facet': 'owner'},
            {'id': 'ownerType', 'display_name': 'Owner Type', 'facet': 'ownerType'},
            {'id': 'locale', 'display_name': 'Locale', 'facet': 'locale'}
        ],
        'collections': [],
        'orgs': [],
        'users': []
    }

    resource_type_info = {
        'concepts': {'int': CONCEPT_TYPE, 'name': 'concept', 'facets': True},
        'mappings': {'int': MAPPING_TYPE, 'name': 'mapping', 'facets': True},
        'sources': {'int': SOURCE_TYPE, 'name': 'source', 'facets': True},
        'collections': {'int': COLLECTION_TYPE, 'name': 'collection', 'facets': True},
        'orgs': {'int': ORG_TYPE, 'name': 'organization', 'facets': False},
        'users': {'int': USER_TYPE, 'name': 'user', 'facets': False}
    }

    search_filter_list = None

    def __init__(self, search_type='', params=None):
        """
        :param search_type: string representation of one of the resource types
        """
        # outputs
        self.search_type = search_type
        self.num_per_page = self.DEFAULT_NUM_PER_PAGE
        self.current_page = None
        self.search_params = {}
        self.search_sort = None
        self.search_query = None

        # Optionally parse search parameters (i.e. GET request parameters)
        if params is not None:
            self.parse(params)


    @property
    def search_resource_id(self):
        """Get numeric resource identifier."""
        if self.search_type in self.resource_type_info:
            return self.resource_type_info[self.search_type]['int']
        else:
            return None


    @property
    def search_resource_name(self):
        """Get singular display name of the resource."""
        if self.search_type in self.resource_type_info:
            return self.resource_type_info[self.search_type]['name']
        else:
            return ''


    @property
    def search_resource_has_facets(self):
        """Get whether the set resource type supports facets."""
        if self.search_type in self.resource_type_info:
            return self.resource_type_info[self.search_type]['facets']
        else:
            return False


    # TODO: Retire this method - not used on global search but maybe on other searches
    def get_search_filters(self):
        """
        Get the search filters applicable for this search object type.
        The searfch filters returned will have state information of the current search criteria,
        i.e. checkboxes can stay checked.

        :returns: a list of SearchFilter object for constructing the HTML filter display.
        """
        return self.search_filter_list[self.search_type]


    # TODO: Develop roadmap to do this more generically
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


    # TODO: Develop roadmap to do this more generically
    def get_sort(self):
        """
        Returns the current sort option
        """
        return '' if self.search_sort is None else self.search_sort


    # TODO: Develop roadmap to do this more generically
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
        """Sets the selected attribute to true for the specified filter options.

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


    def parse(self, request_get):
        """
        Parse processes a request string, dictionary or QueryDict as
        the input/criteria for an OCL search. The parsed search inputs
        are saved in self.search_params

        :params request_get: request string, dictionary or QueryDict of
            search inputs/criteria
        :returns: None
        """

        search_params_dict = {}

        # Verbose - all searches should return resource details, so set verbose to true
        search_params_dict['verbose'] = 'true'

        # Get into QueryDict format if not already and make a copy
        print 'parsing:', request_get
        if isinstance(request_get, QueryDict):
            params = request_get.copy()
        else:
            params = QueryDict(request_get, mutable=True)

        # Determine the search type - gets the latest occurence of type
        if 'type' in params:
            if params['type'] in self.resource_type_info:
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
