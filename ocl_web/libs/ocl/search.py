"""
    Search helper for interfacing web with OCL API.

    Work in progress...
"""


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

concept_filters = None


def setup_filters():
    concept_filters = FilterList('concepts')
    f = concept_filters.add_filter('concept_class', 'Concept Classes')
    f.options = [
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

    f = concept_filters.add_filter('datatype', 'Datatypes')
    f.options = [
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
    return concept_filters


class OCLSearch(object):
    """
        Helper to handle search query URL

        type=concepts|sources|collections|orgs|users
        page=N
        limit=N

    """

    DEFAULT_NUM_PER_PAGE = 5
    DEFAULT_SEARCH_TYPE = 'concepts'

    search_type_names = {
        'concepts': 'concept',
        'sources': 'source',
        'collections': 'collection',
        'orgs': 'organization',
        'users': 'user'
    }

    concept_filters = None

    def __init__(self):
        # outputs
        self.search_type = None
        self.num_per_page = None
        self.current_page = None
        self.search_params = None

        # one time initialization
        if self.concept_filters is None:
            self.concept_filters = setup_filters()

    def parse(self, request_get):
        # make a copy so that we can delete things from it
        params = request_get.copy()

        # search what object type?
        if 'type' in params and params['type'] in self.search_type_names:
            self.search_type = params['type']
            del params['type']
        else:
            self.search_type = self.DEFAULT_SEARCH_TYPE

        # paging
        if 'page' in params:
            try:
                self.current_page = int(params['page'])
                del params['page']
            except:
                # some problem with the page=N input
                self.current_page = 1
        else:
            self.current_page = 1

        if 'limit' in params:
            try:
                self.num_per_page = int(params['limit'])
            except:
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
            f = self.concept_filters.match_filter(key)
            if f:
                search_params[key] = params.pop(key)

        print 'resulting earch params:', search_params
        self.search_params = search_params
        return self


