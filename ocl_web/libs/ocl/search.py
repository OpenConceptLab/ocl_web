"""
    Search helper for interfacing web with OCL API.

    Work in progress...
"""
import logging




logger = logging.getLogger('oclweb')


class Filter(object):
    """
        A specific filter for searching OWL
    """
    def __init__(self, filter_id, name):
        self.filter_id = filter_id  # unique ID for query etc
        self.name = name  # for display
        self.options = []  # a select list of choices


class FilterList(object):
    """
        A list of filter spec for a specific resource type (concept, source, etc)
    """
    def __init__(self, resource_name):
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

    def add_filter(self, filter_id, filter_name):
        f = Filter(filter_id, filter_name)
        self.filter_list.append(f)
        return f

    def __iter__(self):
        return self.filter_list.__iter__()


def turn_to_pairs(values):
    """
    Temporary util to turn a list of values into a list of json friendly dictionary.
    Used to translate the concept_class_list type of lists to a code/name tuple
    list for used in filter.

    Once we clean up these lists to be all code/name pair this will go away.

    """
    return [{'code': v, 'name': v} for v in values]


def setup_filters():

    from apps.core.views import _get_concept_class_list
    from apps.core.views import _get_datatype_list
    from apps.core.views import _get_source_type_list
    from apps.core.views import _get_locale_list

    # concept filters
    filters = FilterList('concepts')
    f = filters.add_filter('concept_class', 'Concept Classes')
    f.options = turn_to_pairs(_get_concept_class_list())

    f = filters.add_filter('datatype', 'Datatypes')
    f.options = turn_to_pairs(_get_datatype_list())

    f = filters.add_filter('locale', 'Locale')
    f.options = _get_locale_list()
    concept_filters = filters

    # source filter
    filters = FilterList('sources')
    f = filters.add_filter('source_type', 'Source Types')
    f.options = turn_to_pairs(_get_source_type_list())

    f = filters.add_filter('language', 'Locale')
    f.options = _get_locale_list()
    source_filters = filters

    # collection filters
    filters = FilterList('collections')
    f = filters.add_filter('collection_type', 'Collection Types')
    f.options = turn_to_pairs([
                'Dictionary',
                'Interface Terminology',
                'Indicator Registry',
                'Reference',
    ])

    f = filters.add_filter('language', 'Locale')
    f.options = _get_locale_list()
    collection_filters = filters

    user_filters = None
    org_filters = None

    return [user_filters, org_filters, source_filters, concept_filters, collection_filters]


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
        self.resource_type = resource_type

        # one time initialization
        if self.filters is None:
            self.filters = setup_filters()

    def get_filters(self):
        return self.filters[self.resource_type]

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
        # sort results on one of the following fields: "name", "last_update" (default), "num_stars"

        # query text
        # q=    for name, full_name, desc in source
        if 'q' in params:
            q = params.pop('q')
            if len(q) == 1:
                search_params['q'] = q[0]
        # for source
        # source_type (optional) string - Filter results to a given source type, e.g. "dictionary", "reference"
        # language (optional) string - Filter results to those with a given language in their supported_locales, e.g. "en", "fr"

        for key in params.keys():
            print 'trying key:%s' % key
            f = self.get_filters().match_filter(key)
            if f:
                search_params[key] = params.pop(key)
                print 'add key %s = %s' % (key, search_params[key])

        from libs.ocl import OCLapi
        print 'Searcher %s params: %s' % (OCLapi.resource_type_name(self.resource_type), search_params)
        self.search_params = search_params
        return self
