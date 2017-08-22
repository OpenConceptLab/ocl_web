"""
OCL Resource Constants
"""

class OclConstants(object):
    """
    OCL Resource Constants
    """
    # RegEx Patterns
    ORG_PATTERN = '[a-zA-Z0-9\-]+'
    NAMESPACE_PATTERN = '[a-zA-Z0-9\-\.]+'
    CONCEPT_ID_PATTERN = '[a-zA-Z0-9\-\.\_]+'

    # Resource types
    RESOURCE_ID_USER = 0
    RESOURCE_ID_ORG = 1
    RESOURCE_ID_SOURCE = 2
    RESOURCE_ID_CONCEPT = 3
    RESOURCE_ID_COLLECTION = 4
    RESOURCE_ID_MAPPING = 5
    RESOURCE_ID_SOURCE_VERSION = 6
    RESOURCE_ID_CONCEPT_VERSION = 7
    RESOURCE_ID_COLLECTION_VERSION = 8
    RESOURCE_ID_MAPPING_VERSION = 9

    # Resource Names - SINGULAR
    RESOURCE_NAME_USER = 'user'
    RESOURCE_NAME_ORG = 'org'
    RESOURCE_NAME_SOURCE = 'source'
    RESOURCE_NAME_CONCEPT = 'concept'
    RESOURCE_NAME_COLLECTION = 'collection'
    RESOURCE_NAME_MAPPING = 'mapping'
    RESOURCE_NAME_SOURCE_VERSION = 'source_version'
    RESOURCE_NAME_COLLECTION_VERSION = 'collection_version'
    RESOURCE_NAME_CONCEPT_VERSION = 'concept_version'
    RESOURCE_NAME_MAPPING_VERSION = 'mapping_version'

    # Resource Names - PLURAL
    RESOURCE_NAME_USERS = 'users'
    RESOURCE_NAME_ORGS = 'orgs'
    RESOURCE_NAME_SOURCES = 'sources'
    RESOURCE_NAME_CONCEPTS = 'concepts'
    RESOURCE_NAME_COLLECTIONS = 'collections'
    RESOURCE_NAME_MAPPINGS = 'mappings'
    RESOURCE_NAME_SOURCE_VERSIONS = 'source_versions'
    RESOURCE_NAME_COLLECTION_VERSIONS = 'collection_versions'
    RESOURCE_NAME_CONCEPT_VERSIONS = 'concept_versions'
    RESOURCE_NAME_MAPPING_VERSIONS = 'mapping_versions'

    # Search scope - may need additional options in the future
    SEARCH_SCOPE_GLOBAL = 0      # Global search looks across owners and repositories
    SEARCH_SCOPE_RESTRICTED = 1  # Restricted search looks within an owner or repository

    # Define the search filters for each resource
    SEARCH_FILTER_INFO = {
        RESOURCE_NAME_CONCEPTS: [
            {
                'filter_id':'includeRetired',
                'filter_name':'Include Retired',
                'filter_widget':'checkboxes',
                'option_defs':[
                    {'option_value':'true', 'option_name':'Include Retired'},
                ],
                'attrs':{'show_zeroed_options':True, 'hide_numbers':True},
            },
            {
                'filter_id':'source',
                'filter_name':'Source',
                'filter_widget':'checkboxes',
                'facet_id':'source',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'conceptClass',
                'filter_name':'Concept Class',
                'filter_widget':'checkboxes',
                'facet_id':'conceptClass',
            },
            {
                'filter_id':'datatype',
                'filter_name':'Datatype',
                'filter_widget':'checkboxes',
                'facet_id':'datatype',
            },
            {
                'filter_id':'retired',
                'filter_name':'Retired',
                'filter_widget':'checkboxes',
                'facet_id':'retired',
                'minimized':True,
            },
            {
                'filter_id':'owner',
                'filter_name':'Concept Owner',
                'filter_widget':'checkboxes',
                'facet_id':'owner',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'locale',
                'filter_name':'Locale',
                'filter_widget':'checkboxes',
                'facet_id':'locale',
            },
            {
                'filter_id':'ownerType',
                'filter_name':'Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'ownerType',
                'minimized':True,
                'show_with_restricted_scope':False,
            },
        ],
        RESOURCE_NAME_MAPPINGS: [
            {
                'filter_id':'includeRetired',
                'filter_name':'Include Retired',
                'filter_widget':'include_retired',
                'option_defs':[
                    {'option_value':'true', 'option_name':'Include Retired'}
                ],
                'attrs':{'show_zeroed_options':True, 'hide_numbers':True},
            },
            {
                'filter_id':'mapType',
                'filter_name':'Map Type',
                'filter_widget':'checkboxes',
                'facet_id':'mapType'
            },
            {
                'filter_id':'source',
                'filter_name':'Mapping Source',
                'filter_widget':'checkboxes',
                'facet_id':'source',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'retired',
                'filter_name':'Retired',
                'filter_widget':'checkboxes',
                'facet_id':'retired',
                'minimized':True,
            },
            {
                'filter_id':'conceptOwner',
                'filter_name':'Concept Owner',
                'filter_widget':'checkboxes',
                'facet_id':'conceptOwner',
            },
            {
                'filter_id':'conceptSource',
                'filter_name':'Concept Source',
                'filter_widget':'checkboxes',
                'facet_id':'conceptSource',
            },
            {
                'filter_id':'conceptOwnerType',
                'filter_name':'Concept Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'conceptOwnerType',
                'minimized':True,
            },
            {
                'filter_id':'toConceptSource',
                'filter_name':'To Concept Source',
                'filter_widget':'checkboxes',
                'facet_id':'toConceptSource',
                'minimized':True,
            },
            {
                'filter_id':'toConceptOwner',
                'filter_name':'To Concept Owner',
                'filter_widget':'checkboxes',
                'facet_id':'toConceptOwner',
                'minimized':True,
            },
            {
                'filter_id':'toConceptOwnerType',
                'filter_name':'To Concept Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'toConceptOwnerType',
                'minimized':True,
            },
            {
                'filter_id':'fromConceptSource',
                'filter_name':'From Concept Source',
                'filter_widget':'checkboxes',
                'facet_id':'fromConceptSource',
                'minimized':True,
            },
            {
                'filter_id':'fromConceptOwnerType',
                'filter_name':'From Concept Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'fromConceptOwnerType',
                'minimized':True,
            },
            {
                'filter_id':'fromConceptOwner',
                'filter_name':'From Concept Owner',
                'filter_widget':'checkboxes',
                'facet_id':'fromConceptOwner',
                'minimized':True,
            },
            {
                'filter_id':'owner',
                'filter_name':'Mapping Owner',
                'filter_widget':'checkboxes',
                'facet_id':'owner',
                'minimized':True,
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'ownerType',
                'filter_name':'Mapping Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'ownerType',
                'minimized':True,
                'show_with_restricted_scope':False,
            },
        ],
        RESOURCE_NAME_SOURCES: [
            {
                'filter_id':'sourceType',
                'filter_name':'Source Type',
                'filter_widget':'checkboxes',
                'facet_id':'sourceType',
            },
            {
                'filter_id':'owner',
                'filter_name':'Owner',
                'filter_widget':'checkboxes',
                'facet_id':'owner',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'ownerType',
                'filter_name':'Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'ownerType',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'locale',
                'filter_name':'Supported Locale',
                'filter_widget':'checkboxes',
                'facet_id':'locale',
            },
        ],
        RESOURCE_NAME_COLLECTIONS: [
            {
                'filter_id':'collectionType',
                'filter_name':'Collection Type',
                'filter_widget':'checkboxes',
                'facet_id':'collectionType',
            },
            {
                'filter_id':'owner',
                'filter_name':'Owner',
                'filter_widget':'checkboxes',
                'facet_id':'owner',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'ownerType',
                'filter_name':'Owner Type',
                'filter_widget':'checkboxes',
                'facet_id':'ownerType',
                'show_with_restricted_scope':False,
            },
            {
                'filter_id':'locale',
                'filter_name':'Supported Locale',
                'filter_widget':'checkboxes',
                'facet_id':'locale',
            },
        ],
    }

    # Resource type definitions
    RESOURCE_TYPE_INFO = {
        RESOURCE_NAME_CONCEPTS:{
            'int':RESOURCE_ID_CONCEPT,
            'name':RESOURCE_NAME_CONCEPT,
            'display_name':'concept',
            'facets':True,
            'icon': 'glyphicon-tag',
            'show_on_global_search':True},
        RESOURCE_NAME_MAPPINGS:{
            'int':RESOURCE_ID_MAPPING,
            'name':RESOURCE_NAME_MAPPING,
            'display_name':'mapping',
            'facets':True,
            'icon': 'glyphicon-link',
            'show_on_global_search':True},
        RESOURCE_NAME_SOURCES:{
            'int':RESOURCE_ID_SOURCE,
            'name':RESOURCE_NAME_SOURCE,
            'display_name':'source',
            'facets':True,
            'icon': 'glyphicon-th-list',
            'show_on_global_search':True},
        RESOURCE_NAME_COLLECTIONS:{
            'int':RESOURCE_ID_COLLECTION,
            'name':RESOURCE_NAME_COLLECTION,
            'display_name':'collection',
            'facets':True,
            'icon': 'glyphicon-tags',
            'show_on_global_search':True},
        RESOURCE_NAME_ORGS:{
            'int':RESOURCE_ID_ORG,
            'name':RESOURCE_NAME_ORG,
            'display_name':'organization',
            'facets':False,
            'icon': 'glyphicon-home',
            'show_on_global_search':True},
        RESOURCE_NAME_USERS:{
            'int':RESOURCE_ID_USER,
            'name':RESOURCE_NAME_USER,
            'display_name':'user',
            'facets':False,
            'icon': 'glyphicon-user',
            'show_on_global_search':True},
        RESOURCE_NAME_SOURCE_VERSIONS:{
            'int':RESOURCE_ID_SOURCE_VERSION,
            'name':RESOURCE_NAME_SOURCE_VERSION,
            'display_name':'version',
            'facets':False,
            'icon': 'glyphicon-asterisk',
            'show_on_global_search':False},
        RESOURCE_NAME_COLLECTION_VERSIONS: {
            'int': RESOURCE_ID_COLLECTION_VERSION,
            'name': RESOURCE_NAME_COLLECTION_VERSION,
            'display_name': 'version',
            'facets': False,
            'icon': 'glyphicon-asterisk',
            'show_on_global_search':False},
        RESOURCE_NAME_CONCEPT_VERSIONS:{
            'int':RESOURCE_ID_CONCEPT_VERSION,
            'mnemonic':RESOURCE_NAME_CONCEPT_VERSION,
            'display_name':'concept version',
            'facets':False,
            'icon': 'glyphicon-th',
            'show_on_global_search':False},
        RESOURCE_NAME_MAPPING_VERSIONS:{
            'int':RESOURCE_ID_MAPPING_VERSION,
            'mnemonic':RESOURCE_NAME_MAPPING_VERSION,
            'display_name':'mapping version',
            'facets':False,
            'icon': 'glyphicon-th',
            'show_on_global_search':False},
    }


    # Ordered list of definitions for sort options
    # Currently the same list is applied to all resources
    SORT_OPTION_DEFINITIONS = [
        {
            'value': 'Best Match',
            'display': 'Best Match',
            'icon': 'glyphicon-sort'
        },
        {
            'value': 'Last Update (Desc)',
            'display': 'Last Update (Desc)',
            'icon': 'glyphicon-sort-by-attributes-alt'
        },
        {
            'value': 'Last Update (Asc)',
            'display': 'Last Update (Asc)',
            'icon': 'glyphicon-sort-by-attributes'
        },
        {
            'value': 'Name (Asc)',
            'display': 'Name (Asc)',
            'icon': 'glyphicon-sort-by-alphabet'
        },
        {
            'value': 'Name (Desc)',
            'display': 'Name (Desc)',
            'icon': 'glyphicon-sort-by-alphabet-alt'
        }
    ]

    @classmethod
    def resource_id(cls, resource_type):
        """Get numeric resource identifier."""
        if resource_type in cls.RESOURCE_TYPE_INFO:
            return cls.RESOURCE_TYPE_INFO[resource_type]['int']
        else:
            return None

    @classmethod
    def resource_display_name(cls, resource_type):
        """Get singular display name of the resource."""
        if resource_type in cls.RESOURCE_TYPE_INFO:
            return cls.RESOURCE_TYPE_INFO[resource_type]['display_name']
        else:
            return ''

    @classmethod
    def resource_display_icon(cls, resource_type):
        """Get singular display icon of the resource."""
        if resource_type in cls.RESOURCE_TYPE_INFO:
            return cls.RESOURCE_TYPE_INFO[resource_type]['icon']
        else:
            return ''

    @classmethod
    def resource_has_facets(cls, resource_type):
        """Get whether the set resource type supports facets."""
        if resource_type in cls.RESOURCE_TYPE_INFO:
            return cls.RESOURCE_TYPE_INFO[resource_type]['facets']
        else:
            return False
