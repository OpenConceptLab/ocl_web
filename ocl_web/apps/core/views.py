"""
OCL Web Core Functionality
"""
# import requests
import logging

from django.core import cache
from django.http import HttpResponse
from django.views.generic.edit import View
from django.utils.translation import ugettext as _
from braces.views import JsonRequestResponseMixin

from libs.ocl import OclApi

logger = logging.getLogger('oclweb')
api = OclApi()


class UserOrOrgMixin(object):
    """
    Figure out if a view is called from a user or an organization "owner".
    """

    def get_args(self):
        """
        Helper method to determine resource ownership (user/org) and resource identifiers.

        Method will set the following based on the passed kwargs:
        :param self.from_user: sets to true/false depending on source type
        :param self.from_org: sets to true/false depending on source type
        :param self.user_id: sets to username if source is from user
        :param self.org_id: sets to org id if source is from org
        :param self.owner_type: sets to "users" or "orgs", good for calling API
        :param self.owner_id: sets to user id or org id, good for calling API
        :param self.source_id: sets to source ID if view URL has source part
        :param self.source_version_id: sets to source version ID if view URL contains it
        :param self.concept_id: sets to concept ID if view URL has concept part
        :param self.concept_version_id: sets to concept version if view URL has concept version part

        TODO(paynejd@gmail.com): Collections are not handled here
        """
        self.from_user = False
        self.from_org = False
        self.user_id = None
        self.org_id = None
        self.owner_type = None
        self.owner_id = None
        self.source_id = None
        self.source_version_id = None
        self.concept_id = None
        self.concept_version_id = None
        self.mapping_id = None
        self.proper_owner_type = None

        # Determine the owner type and set the owner ID
        self.org_id = self.kwargs.get('org')
        if self.org_id is None:
            self.user_id = self.kwargs.get('user')
            self.from_user = True
            self.owner_type = 'users'
            self.owner_id = self.user_id
            self.proper_owner_type = 'User'
        else:
            self.from_org = True
            self.owner_type = 'orgs'
            self.owner_id = self.org_id
            self.proper_owner_type = 'Organization'

        # Set the source, concept, and their versions
        self.source_id = self.kwargs.get('source')
        self.source_version_id = self.kwargs.get('source_version')
        # Set the source, concept, and their versions
        self.collection_id = self.kwargs.get('collection')
        self.collection_version_id = self.kwargs.get('collection_version')
        self.concept_id = self.kwargs.get('concept')
        self.concept_version_id = self.kwargs.get('concept_version')
        self.mapping_id = self.kwargs.get('mapping')
        self.mapping_version_id = self.kwargs.get('mapping_version')

    def args_string(self):
        """
        Debug method to return all args parsed as a printable string.
        """
        output_string = ''
        if self.org_id:
            output_string += 'org_id: %s  ' % self.org_id
        if self.user_id:
            output_string += 'user_id: %s  ' % self.user_id
        if self.owner_type:
            output_string += 'owner_type: %s  ' % self.owner_type
        if self.owner_id:
            output_string += 'owner_id: %s  ' % self.owner_id
        if self.source_id:
            output_string += 'source_id: %s  ' % self.source_id
        if self.source_version_id:
            output_string += 'source_version_id: %s  ' % self.source_version_id
        if self.concept_id:
            output_string += 'concept_id: %s  ' % self.concept_id
        if self.version_id:
            output_string += 'concept_version_id: %s  ' % self.version_id
        return output_string


class ExtraJsonView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
    Extra handling for org/user/source is different from concept...

    The extras field name IS the attribute name, the data is stored as a dictionary.
    So in this view, we translate the API style of data to be like descriptions and names.
    e.g.:

    API version:   {'price': 100}
    front end version: {extra_name: 'price', extra_value: 100}
    """

    def get_all_args(self):
        """
        Get all the input entities' identity, figure out whether this is a user owned
        sourced concept or an org owned sourced concept, and set self.owner_type, self.owner_id
        for easy interface to OCL API.
        """
        self.get_args()
        self.extra_id = self.kwargs.get('extra')

    def build_url(self, *args):
        """
        A tricky bit of code here. The extra maybe for
          * an org
          * a user,
          * a source (owned by org or user),
          * a concept
          ...etc...

        We will use what's given in the kwargs in the URL to figure out the
        corresponding OCL API url.
        """
        url_args = [self.owner_type, self.owner_id]  # either org or user
        if self.source_id is not None:
            url_args += ['sources', self.source_id]
        if self.concept_id is not None:
            url_args += ['concepts', self.concept_id]
        url_args.append('extras')
        if len(args) > 0:
            url_args += args
        return url_args

    def is_edit(self):
        """Return whether extra_id is set in instance
        """
        return self.extra_id is not None

    def get(self, request, *args, **kwargs):
        """Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OclApi(self.request, debug=True)

        result = api.get(*self.build_url())
        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        # Convert OCLAPI dictionary style data to a list of dictionary objects
        # so that we can use the same front end JS to work with extras.
        output_list = []
        for key, value in result.json().iteritems():
            output_list.append({'extra_name': key, 'extra_value': value})

        return self.render_json_response(output_list)

    def post(self, request, *args, **kwargs):
        """Post
        """

        self.get_all_args()

        # Convert back to OCLAPI format for extras, the dictionnary
        # key is the attribute name.
        data = {}
        fn = fv = None
        try:
            fn = self.request_json.get('extra_name')
            fv = self.request_json.get('extra_value')
            data[fn] = fv
        except KeyError:
            resp = {'message': _('Invalid input')}
            return self.render_bad_request_response(resp)

        api = OclApi(self.request, debug=True)
        if self.is_edit():
            result = api.put(*self.build_url(fn), **data)
            msg = _('Extra updated')
        else:
            result = api.put(*self.build_url(fn), **data)
            msg = _('Extra added')

        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)
        else:
            return self.render_json_response({'message': msg})

    def delete(self, request, *args, **kwargs):
        """Delete the specified item.
        """
        self.get_all_args()

        api = OclApi(self.request, debug=True)

        if not self.is_edit():  # i.e. has item UUID
            return self.render_bad_request_response({'message': 'key missing'})

        result = api.delete(*self.build_url(self.extra_id))

        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': _('extra deleted')})


def _get_concept_class_list():
    """Return a list of concept classes.

    This is a temporary function. Should get this data from the database.
    currently from OpenMRS dataset 2014/10/19
    """
    response = api.get('orgs', 'OCL', 'sources', 'Classes', 'concepts', params={'limit': 0})
    return [] if response.status_code == 404 else [concept_class['id'] for concept_class in response.json()]


def _get_datatype_list():
    """Return a list of datatypes.

    Currently from OpenMRS dataset 2014/10/19
    """
    response = api.get('orgs', 'OCL', 'sources', 'Datatypes', 'concepts', params={'limit': 0})
    return [datatype['id'] for datatype in response.json()]


# TODO(paynejd@gmail.com): Retire this and replace with values stored in OCL
def _get_source_type_list():
    """Return a list of source types
    """
    return [
        'Dictionary',
        'Interface Terminology',
        'Indicator Registry',
        'External'
    ]


def _get_custom_validation_schema_list():
    return [
        'None',
        'OpenMRS',
    ]


# TODO(paynejd@gmail.com): Retire this and replace with values stored in OCL
def _get_collection_type_list():
    """Return a list of collection types
    """
    return [
        'Subset',
        'Value Set',
        'Dictionary',
        'Interface Terminology',
        'Indicator Registry'
    ]


locale_list = []

def _get_locale_list():
    """Return a list of locales only for those having 2-letter codes
    """
    local_cache = cache.get_cache('default')
    locale_list_in_cache = local_cache.get('locale')

    if locale_list_in_cache:
        return locale_list_in_cache

    response = api.get('orgs', 'OCL', 'sources', 'Locales', 'concepts', params={'limit': 0})

    if response.status_code == 404:
        locale_list = [{'code': 'en', 'name': 'en - English'}]
        return locale_list

    locale_list = [
        {
            'code': locale['locale'],
            'name': locale['display_name'] + ' [' + locale['locale'] + ']'
        }
        for locale in response.json() if locale['locale']
        ]
    locale_list.sort()

    day_time_as_minutes = 24 * 60 * 60

    local_cache.set('locale', locale_list, day_time_as_minutes)
    return locale_list


def _get_name_type_list():
    response = api.get('orgs', 'OCL', 'sources', 'NameTypes', 'concepts', params={'limit': 0})
    return [] if response.status_code == 404 else [name_type['display_name'] for name_type in response.json()]


def _get_description_type_list():
    response = api.get('orgs', 'OCL', 'sources', 'DescriptionTypes', 'concepts', params={'limit': 0})
    return [] if response.status_code == 404 else [description_type['display_name'] for description_type in response.json()]


def _get_map_type_list():
    response = api.get('orgs', 'OCL', 'sources', 'MapTypes', 'concepts', params={'limit': 0})
    return [] if response.status_code == 404 else [description_type['display_name'] for description_type in response.json()]


# TODO(paynejd@gmail.com): Retire this and replace with values stored in OCL
class GetOptionListView(JsonRequestResponseMixin, View):
    """Utility to get a list of valid options for attributes for
    different resource types for the front end.

    TODO: Get this from the database

    :returns: json list of either strings, or dictionaries in
        case of locales.
    """

    def get(self, request, *args, **kwargs):
        """Return a list of descriptions as json.
        """
        option_type = self.kwargs['type']
        if option_type == 'concept_classes':
            return self.render_json_response(_get_concept_class_list())
        if option_type == 'datatypes':
            return self.render_json_response(_get_datatype_list())
        if option_type == 'map_types':
            return self.render_json_response(_get_map_type_list())
        if option_type == 'locales':
            return self.render_json_response(_get_locale_list())


class GetStatsView(View):
    """Utility views to get basic statistics to monitoring services.
    """

    def get(self, request, *args, **kwargs):
        """Return a ... number !
        """
        key = self.kwargs['key']
        cnt = 0

        api = OclApi(self.request, debug=True)
        if key == 'concepts':
            response = api.head('concepts')
            cnt = response.headers.get('num_found')
        if key == 'users':
            response = api.head('users')
            cnt = response.headers.get('num_found')
        if key == 'orgs':
            response = api.head('orgs')
            cnt = response.headers.get('num_found')
        if key == 'sources':
            response = api.head('sources')
            cnt = response.headers.get('num_found')

        return HttpResponse(cnt)
