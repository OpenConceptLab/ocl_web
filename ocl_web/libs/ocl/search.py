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

        :returns: FilterSpec or None
        """
        r = filter(lambda f: f.filter_id == filter_id, self.filter_list)
        if len(r) == 0:
            return None
        else:
            return r[0]

    def add_filter(self, filter_id='', filter_name=''):
        f = Filter(filter_id, filter_name)
        self.filter_list.append(f)
        return f

    def __iter__(self):
        return self.filter_list.__iter__()

    def __str__(self):
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

    DEFAULT_NUM_PER_PAGE = 25
    DEFAULT_SEARCH_TYPE = 'concepts'

    search_type_names = {
        'concepts': 'concept',
        'sources': 'source',
        'collections': 'collection',
        'orgs': 'organization',
        'users': 'user'
    }

    filters = None

    def __init__(self, resource_type):
        """
        :param resource_type: is a resource type from OCLapi.resource_types
        """
        # outputs
        self.search_type = None
        self.num_per_page = None
        self.current_page = None
        self.search_params = None
        self.search_sort = None
        self.resource_type = resource_type
        self.q = None

        # one time initialization
        if self.filters is None:
            self.filters = setup_filters()

    def get_filters(self):
        """
        Get the appropriate filters applicable for this search object type.
        The filters returned will have state information of the current search criteria,
        i.e. checkboxes can stay checked.

        :returns: a list of Filter object for constructing the HTML filter display.
        """
        return self.filters[self.resource_type]


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


    def process_facets(self, search_type, facets):
        """
        :params facets: Dictionary of the form { 'fields':{ } }
        :returns: FilterList
        """
        if isinstance(facets, dict) and 'fields' in facets and isinstance(facets['fields'], dict):
            fl = FilterList(resource_name=search_type)
            for facet in facets['fields']:
                # TODO: Need method to convert field name to display name
                facet_display_name = facet
                f = fl.add_filter(filter_id=facet, filter_name=facet_display_name)
                for facet_option in facets['fields'][facet]:
                    facet_option_name = facet_option[0]
                    facet_option_num = facet_option[1]                    
                    f.add_option(option_value=facet_option_name, option_name=facet_option_name, option_num=facet_option_num)
        return fl


    def parse(self, request_get):

        print 'parsing:', request_get
        if request_get is None:
            params = {}
        else:
            # make a copy so that we can delete things from it
            params = request_get.copy()

        # search what object type?
        if 'type' in params:
            if params['type'] in self.search_type_names:
                self.search_type = params['type']
                del params['type']
            else:
                self.search_type = self.DEFAULT_SEARCH_TYPE

        # paging
        if 'page' in params:
            try:
                print 'getting page'
                self.current_page = int(params['page'])
                print 'getting page', self.current_page
                del params['page']
            except ValueError:
                # some problem with the page=N input
                self.current_page = 1
        else:
            self.current_page = 1

        if 'limit' in params:
            try:
                self.num_per_page = int(params['limit'])
            except ValueError:
                self.num_per_page = self.DEFAULT_NUM_PER_PAGE
        else:
            self.num_per_page = self.DEFAULT_NUM_PER_PAGE

        search_params = {}
        search_params['limit'] = self.num_per_page
        search_params['page'] = self.current_page
        search_params['verbose'] = 'true'

        # sort
        # sortAsc/sortDesc (optional) string
        # sort results on one of the following fields: "name", "last_update"
        # (default), "num_stars"
        sort_key = None
        sort_value = None
        if 'sort' in params:
            self.search_sort = params['sort']
            p = self.search_sort.lower()
            if 'asc' in p:
                sort_key = 'sortAsc'
            elif 'desc' in p:
                sort_key = 'sortDesc'
            if 'last update' in p:
                sort_value = 'last_update'
            if 'name' in p:
                sort_value = 'name'
            if sort_key and sort_value:
                search_params[sort_key] = sort_value

        # query text
        # q=    for name, full_name, desc in source
        if 'q' in params:
            q = params.pop('q')
            if len(q) == 1:
                self.q = q[0]
                search_params['q'] = self.q

        # for source
        # source_type (optional) string - Filter results to a given source type
        # e.g. "dictionary", "reference"
        # language (optional) string - Filter results to those with a given
        # language in their supported_locales, e.g. "en", "fr"

        for key in params.keys():
            print 'trying key:%s' % key
            f = None
            if self.get_filters():
                f = self.get_filters().match_filter(key)
                if f:
                    v = params.pop(key)
                    # set this option as selected
                    f.select_option(v)
                    search_params[key] = v
                    print 'add key %s = %s' % (key, v)
                    print f
        from libs.ocl import OCLapi
        print 'Searcher %s params: %s' % (OCLapi.resource_type_name(self.resource_type), search_params)
        self.search_params = search_params
        return self
