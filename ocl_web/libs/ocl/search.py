"""
    Search helper for interfacing web with OCL API.

"""
import logging

logger = logging.getLogger('oclweb')


class FilterOption(object):
    """
        Defines a specific filter option
    """
    def __init__(self, filter=None, option_value='', option_name='', option_num=0, selected=False):
        self.filter = filter
        self.option_value = option_value
        self.option_name = option_name
        self.option_num = option_num
        self.selected = selected

    def __str__(self):
        return "%s: %s [%s] %s" % (self.filter.filter_name, self.option_name, self.option_num, self.selected)

    def __unicode__(self):
        return "%s: %s [%s] %s" % (self.filter.filter_name, self.option_name, self.option_num, self.selected)



class Filter(object):
    """
        A specific filter for searching OCL

        options is a dictionary of FilterOption instances
    """
    def __init__(self, filter_id='', filter_name=''):
        self.filter_id = filter_id  # unique ID for query etc
        self.filter_name = filter_name  # for display
        self.options = {}  # a dictionary of filter options

    def add_option(self, option_value='', option_name='', option_num=0, selected=False):
        self.options[option_value] = FilterOption(filter=self, option_value=option_value, 
            option_name=option_name, option_num=option_num, selected=selected)

    def select_option(self, option_value):
        """
        Mark as selected the option(s) according to the value or list of values passed.
        """
        # handle the case where option_value is a list of options
        if not isinstance(option_value, list):
            ls = [option_value]
        else:
            ls = option_value

        for i in self.options:
            if self.options[i].option_value in ls:
                self.options[i].selected = True

    def __str__(self):
        return "%s (%s): %s" % (self.filter_name, self.filter_id, [str(self.options[k]) for k in self.options.keys()] )

    def __unicode__(self):
        return "%s (%s): %s" % (self.filter_name, self.filter_id, [str(self.options[k]) for k in self.options.keys()] )



class FilterList(object):
    """
        A list of filter spec for a specific resource type (concept, source, etc)
    """
    def __init__(self, resource_name=''):
        self.resource_name = resource_name
        self.filter_list = []

    def match_filter(self, filter_id):
        """
        Lookup a filter by filter_id.

        :returns: Matched Filter or None
        """
        matched_filters = filter(lambda f: f.filter_id == filter_id, self.filter_list)
        if len(matched_filters) == 0:
            return None
        else:
            return matched_filters[0]

    def add_filter(self, filter_id='', filter_name=''):
        f = Filter(filter_id, filter_name)
        self.filter_list.append(f)
        return f

    def __iter__(self):
        return self.filter_list.__iter__()

    def __str__(self):
        return 'Resource %s: %s\n\n' % (self.resource_name, [str(f) for f in self.filter_list])

    def __unicode__(self):
        return 'Resource %s: %s\n\n' % (self.resource_name, [str(f) for f in self.filter_list])


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



def setup_filters():

    from apps.core.views import _get_concept_class_list
    from apps.core.views import _get_datatype_list
    from apps.core.views import _get_source_type_list
    from apps.core.views import _get_locale_list

    # concept filters
    filters = FilterList('concepts')
    f = filters.add_filter('concept_class', 'Concept Classes')
    f.options = turn_to_tuples(_get_concept_class_list())

    f = filters.add_filter('datatype', 'Datatypes')
    f.options = turn_to_tuples(_get_datatype_list())

    f = filters.add_filter('locale', 'Locale')
    f.options = turn_to_tuples(_get_locale_list())

    f = filters.add_filter('includeRetired', 'Include Retired')
    f.options = turn_to_tuples([{'code': u'1', 'name': 'Retired'}])
    concept_filters = filters

    # source filter
    filters = FilterList('sources')
    f = filters.add_filter('source_type', 'Source Types')
    f.options = turn_to_tuples(_get_source_type_list())

    f = filters.add_filter('language', 'Locale')
    f.options = _get_locale_list()
    source_filters = filters

    # collection filters
    filters = FilterList('collections')
    f = filters.add_filter('collection_type', 'Collection Types')
    f.options = turn_to_tuples([
                'Dictionary',
                'Interface Terminology',
                'Indicator Registry',
                'Reference',
                'External'
    ])

    f = filters.add_filter('language', 'Locale')
    f.options = _get_locale_list()
    collection_filters = filters

    # mapping filters
    filters = FilterList('mappings')
    f = filters.add_filter('collection_type', 'Collection Types')
    f.options = turn_to_tuples([
                'Dictionary',
                'Interface Terminology',
                'Indicator Registry',
                'Reference',
                'External'
    ])
    mapping_filters = filters

    user_filters = None
    org_filters = None

    return [user_filters, org_filters, source_filters, concept_filters,
            collection_filters, mapping_filters]



class OCLSearch(object):
    """
        Helper to handle search query URL

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

    DEFAULT_NUM_PER_PAGE = 25
    DEFAULT_SEARCH_TYPE = 'concepts'

    resource_type_info = {
        'concepts': { 'int': CONCEPT_TYPE, 'name': 'concept', 'facets': True },
        'mappings': { 'int': MAPPING_TYPE, 'name': 'mapping', 'facets': True },
        'sources': { 'int': SOURCE_TYPE, 'name': 'source', 'facets': True },
        'collections': { 'int': COLLECTION_TYPE, 'name': 'collection', 'facets': True },
        'orgs': { 'int': ORG_TYPE, 'name': 'organization', 'facets': False },
        'users': { 'int': USER_TYPE, 'name': 'user', 'facets': False }
    }

    filter_list = None

    def __init__(self, resource_type='', params=None):
        """
        :param resource_type: is a resource type from OCLapi.resource_types
        """
        # outputs
        self.search_type = None
        self.num_per_page = None
        self.current_page = None
        self.search_params = None
        self.search_sort = None
        self.q = None
        self.resource_type = resource_type

        # one time initialization
        #if self.filter_list is None:
        #    self.filter_list = setup_filters()

        # parse search parameters (i.e. GET request parameters)
        if (params):
            self.parse(params)


    # TODO: Planning to retire this method
    def get_filters(self):
        """
        Get the appropriate filters applicable for this search object type.
        The filters returned will have state information of the current search criteria,
        i.e. checkboxes can stay checked.

        :returns: a list of Filter object for constructing the HTML filter display.
        """
        return self.filter_list[self.resource_type]


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
        return '' if self.q is None else self.q


    def process_facets(self, resource_type='', facets=None):
        """
        :params resource_type: Resource type
        :params facets: Dictionary of the form { 'fields':{ } }
        :returns: FilterList
        """
        if isinstance(facets, dict) and 'fields' in facets and isinstance(facets['fields'], dict):
            fl = FilterList(resource_name=resource_type)
            for facet in facets['fields']:
                # TODO: Need method to convert field name to display name
                facet_display_name = facet
                f = fl.add_filter(filter_id=facet, filter_name=facet_display_name)
                for facet_option in facets['fields'][facet]:
                    facet_option_name = facet_option[0]
                    facet_option_num = facet_option[1]                    
                    f.add_option(option_value=facet_option_name, option_name=facet_option_name, option_num=facet_option_num)
        self.filter_list = fl
        return fl


    def select_filters(self, params):
        print 'Selecting filters...'
        if isinstance(self.filter_list, FilterList):
            for key in params.keys():
                print 'Attempting to select filter: %s = %s' % (key, params[key])
                matched_filter = self.filter_list.match_filter(key)
                if matched_filter:
                    matched_filter.select_option(params[key])
                print '\tMatched filter:', matched_filter


    def parse(self, request_get):

        search_params = {}

        # Verbose - all searches should return resource details, so set verbose to true
        search_params['verbose'] = 'true'

        # make a copy of the parameters so that we can delete entries from it
        print 'parsing:', request_get
        if request_get is None:
            params = {}
        else:
            params = request_get.copy()

        # determine the search type
        if 'type' in params:
            if params['type'] in self.resource_type_info:
                self.search_type = params['type']
            else:
                self.search_type = self.DEFAULT_SEARCH_TYPE
            del params['type']
        else:
            self.search_type = self.DEFAULT_SEARCH_TYPE
        print 'search type:', self.search_type

        # paging
        if 'page' in params:
            try:
                self.current_page = int(params['page'])
            except ValueError:
                self.current_page = 1
            del params['page']
        else:
            self.current_page = 1
        search_params['page'] = self.current_page
        print 'page:', self.current_page

        # limit
        if 'limit' in params:
            try:
                self.num_per_page = int(params['limit'])
            except ValueError:
                self.num_per_page = self.DEFAULT_NUM_PER_PAGE
            del params['limit']
        else:
            self.num_per_page = self.DEFAULT_NUM_PER_PAGE
        search_params['limit'] = self.num_per_page
        print 'limit:', self.num_per_page
 
        # sort - sortAsc/sortDesc (optional) string
        sort_direction = None
        sort_value = None
        if 'sort' in params:
            # convert sort parameter into string format if a list
            raw_search_sort = params.pop('sort')
            if isinstance(raw_search_sort, basestring):            
                self.search_sort = raw_search_sort
            elif all(isinstance(item, basestring) for item in raw_search_sort):
                self.search_sort = ' '.join(raw_search_sort)
            else:
                self.search_sort = ''

            # process sort
            p = self.search_sort.lower()
            if 'asc' in p:
                sort_direction = 'sortAsc'
            elif 'desc' in p:
                sort_direction = 'sortDesc'
            if 'last update' in p:
                sort_value = 'last_update'
            elif 'name' in p:
                sort_value = 'name'
            if sort_direction and sort_value:
                search_params[sort_direction] = sort_value
        print 'sort:', self.search_sort, sort_direction, ':', sort_value

        # query text
        if 'q' in params:
            q = params.pop('q')
            if isinstance(q, basestring):
                self.q = q
            elif all(isinstance(item, basestring) for item in q):
                self.q = ' '.join(q)
            else:
                self.q = ''
            search_params['q'] = self.q
        print 'q:', self.q

        # Apply facets/filters - everything that's left should be a filter/facet
        # Note: currently not doing any thatranslation of filter values
        for key in params.keys():
            value = params.pop(key)
            # TODO: any processing that needs to happen should go here
            search_params[key] = value
            print 'filter [%s] = %s' % (key, value)

        self.search_params = search_params
        print 'Searcher %s params: %s' % (self.resource_type, search_params)
