"""
    This is the central interface to the OCL API.
"""
import os
import logging
import requests
import simplejson as json

from django.conf import settings

# for others to import via this module
from .search import OCLSearch


SESSION_TOKEN_KEY = 'API_USER_TOKEN'


class OCLapi(object):
    """ Interface to the OCL API backend.
        Handles all the authentication and formating.
        Also contain helper and utility functions.

        :logging: This class outputs debug level information to the "oclapi" logger.
    """
    # resource types
    USER_TYPE = 0
    ORG_TYPE = 1
    SOURCE_TYPE = 2
    CONCEPT_TYPE = 3
    COLLECTION_TYPE = 4
    MAPPING_TYPE = 5
    SOURCE_VERSION_TYPE = 6

    logger = logging.getLogger('oclapi')

    def debug_result(self, results):
        """
        Some serious debug output.
        """
        self.logger.debug('API %s' % (results.request.path_url))
        self.logger.debug('%s RESULT: %s' % (
            results.request.method, results.status_code))
        if results.status_code == requests.codes.server_error:
            self.logger.error(results.content)

        elif len(results.content) > 0:
            try:
                self.logger.debug('%s JSON: %s' % (results.request.method,
                                  json.dumps(results.json(),
                                             sort_keys=True, indent=4,
                                             separators=(',', ': '))))
            except json.JSONDecodeError:
                self.logger.error('JSON: Error decoding it: %s' % results.content[:40])
        else:
                self.logger.debug('%s no content.' % results.request.method)

    @classmethod
    def resource_type_name(cls, type_id):
        if type_id == cls.USER_TYPE:
            return 'User Type'
        if type_id == cls.ORG_TYPE:
            return 'Organization Type'
        if type_id == cls.SOURCE_TYPE:
            return 'Souce Type'
        if type_id == cls.CONCEPT_TYPE:
            return 'Concept Type'
        if type_id == cls.COLLECTION_TYPE:
            return 'Collection Type'
        if type_id == cls.MAPPING_TYPE:
            return 'Mapping Type'
        return 'Unknown type'

    def __init__(self, request=None, debug=False, admin=False, facets=False):
        """
        :param request: gives the API access to the current active session,
            to get Authorization etc.
        :param admin: optional, if set to True, access API as admin user.
            Needed for create_user.
        :param facets: optional, if set to True, API returns faceted search
            information instead of clean JSON results. Note that faceted
            results are only applicable on certain list requests, and this
            argument is ignored otherwise.
        """
        self.status_code = None
        self.debug = debug
        self.host = settings.API_HOST  # backend location
        self.headers = {'Content-Type': 'application/json'}

        # The admin api key should only be used for admin functions (duh)
        self.admin_api_key = os.environ.get('OCL_API_TOKEN', None)
        self.anon_api_key = os.environ.get('OCL_ANON_API_TOKEN', None)
        self.url = None
        self.api_key = None
        self.include_facets = facets

        if admin:
            self.headers['Authorization'] = 'Token %s' % self.admin_api_key
        else:
            if request:
                # Todo: the KEY constant needs to be somewhere else
                key = request.session.get(SESSION_TOKEN_KEY, self.anon_api_key)
                self.api_key = request.session.get(SESSION_TOKEN_KEY, None)
                self.headers['Authorization'] = 'Token %s' % key

    @property
    def include_facets(self):
        if 'includeFacets' in self.headers:
            return true
        else:
            return false

    @include_facets.setter
    def include_facets(self, include_facets_bool):
        if include_facets_bool:
            self.headers['includeFacets'] = 'true'
        elif 'includeFacets' in self.headers:
            del(self.headers['includeFacets'])

    def post(self, type_name, *args, **kwargs):
        """ Issue Post request to API.

            :param type_name: is a string specifying the type of the object
                              according to the API.
            :param *args: The rest of the positional arguments will be appended
                          to the post URL
            :param *kwargs: all the keyword arguments will become post data.

            :returns: response object from requests.
        """
        url = '%s/%s/' % (self.host, type_name)
        if len(args) > 0:
            url = url + '/'.join(args) + '/'
        if self.debug:
            self.logger.debug('POST %s %s %s' % (url, json.dumps(kwargs),
                                                 self.headers))

        results = requests.post(url, data=json.dumps(kwargs),
                                headers=self.headers)
        self.status_code = results.status_code
        if self.debug:
            self.debug_result(results)
        return results

    def delete(self, *args, **kwargs):
        """ Issue delete request to API.

        """
        url = '%s/' % (self.host)
        if len(args) > 0:
            url = url + '/'.join(args) + '/'
        if self.debug:
            self.logger.debug('DELETE %s %s %s' % (url, json.dumps(kwargs),
                                                   self.headers))

        results = requests.delete(url, data=json.dumps(kwargs),
                                  headers=self.headers)
        self.status_code = results.status_code
        return results

    def put(self, type_name, *args, **kwargs):
        """ Issue delete request to API.

            :param type_name: is a string specifying the type of the object
                              according to the API.
        """
        url = '%s/%s/' % (self.host, type_name)
        if len(args) > 0:
            url = url + '/'.join(args) + '/'

        if self.debug:
            self.logger.debug('PUT %s %s %s' % (url, json.dumps(kwargs),
                                                self.headers))

        results = requests.put(url, data=json.dumps(kwargs),
                               headers=self.headers)
        self.status_code = results.status_code
        if self.debug:
            self.debug_result(results)
        return results

    def head(self, *args, **kwargs):
        """ Issue HEAD request to API.

            :param *args: All positional arguments are appended to the request URL.
            :param **kwargs: These are not used at the moment, since this is a get request TODO
            :returns: requests.response object.

        """
        self.url = '%s/' % (self.host)
        if len(args) > 0:
            self.url = self.url + '/'.join(args) + '/'
        if self.debug:
            self.logger.debug('HEAD %s %s %s' % (self.url, json.dumps(kwargs), self.headers))

        # look for optional keyword argument params for constructing URL param
        # i.e. ?f1=v1&f2=v2
        params = kwargs.get('params')

        results = requests.head(self.url, params=params,
                                headers=self.headers)
        self.status_code = results.status_code
        if self.debug:
            self.debug_result(results)
        return results

    def get(self, *args, **kwargs):
        """ Issue get request to API.

            :param *args: All positional arguments are appended to the request URL.
                Note: To pass query parameters to the GET function, use a params={k:v} keyword argument.
            :param **kwargs: These are not used at the moment, since this is a get request TODO
            :returns: requests.response object.

        """
        # Build the URL
        self.url = '%s/' % (self.host)
        if len(args) > 0:
            self.url = self.url + '/'.join(args)
        if self.url[-1] != '/':
            self.url += '/'

        # Look for optional keyword argument params for constructing URL param e.g. ?f1=v1&f2=v2
        params = kwargs.get('params')

        if self.debug:
            self.logger.debug('GET %s %s %s' % (self.url, params, self.headers))

        results = requests.get(self.url, params=params, headers=self.headers)

        self.status_code = results.status_code
        if self.debug:
            self.debug_result(results)
        return results

    def get_json(self, *args):
        """ Smarter GET request when you really want a json object back.

            Note: This is experimental -- not sure if this is the right abstraction.

            :param *args: All positional arguments are appended to the request URL.
            :returns: json string or None if error.
            :exception: Will raise exception if response status code is not 200.
        """
        results = self.get(*args)
        if results.status_code != requests.codes.ok:
            results.raise_for_status()
        if len(results.content) > 0:
            return results.json()
        else:
            return None

    def get_by_url(self, url, **kwargs):
        """ Issue get request to API.

            :param url: is a string specifying the request url. Useful
                for urls contained in OCL response data like members_url.
        """
        url = '%s/%s' % (self.host, url)

        if self.debug:
            self.logger.debug('GET %s %s %s' % (url, json.dumps(kwargs), self.headers))

        results = requests.get(url, data=json.dumps(kwargs),
                               headers=self.headers)
        return results

    def save_auth_token(self, request, json_data):
        """ Save API user token into session table for online use.

            :param request: is the django http request
            :param api_json_data: contains the backend auth token.
        """
        request.session[SESSION_TOKEN_KEY] = json_data['token']

    def create_user(self, data):
        """ Create a user in the system. This call is a bit special because
            users need to be created using admin credentials.
            :param data: is a dictionary of all the data fields.

            :returns: requests.reponse object
        """
        result = self.post('users', **data)
        return result

    def delete_user(self, username):
        """ Delete a user in the system, actually just deactivates her.
            delete users needs admin credentials.
            :param username: is a string specifying the username.

            :returns: ??
        """
        result = self.delete('users', username)
        return result

    def reactivate_user(self, username):
        """ Delete a user in the system, actually just deactivates her.
            delete users needs admin credentials.
            :param username: is a string specifying the username.

            :returns: ??
        """
        result = self.put('users/%s/reactivate/' % username)
        return result

    def get_user_auth(self, username, password):
        """ Get the user AUTH token for the specified user.
            :param username: is a string containing the user name.

            :returns: ??
        """
        result = self.post('users', 'login', username=username, password=password)
        return result

    def sync_password(self, user):
        """
        sync password with backend
        """
        result = self.post('users/%s/' % user.username, hashed_password=user.password)
        return result

    def create_concept(self, source_owner_type, source_owner_id, source_id, base_data,
                       names=[], descriptions=[], extras=[]):
        """ Create a concept.
            NOTE: currently add by org+source, but there are other options... TODO

            :param org_id: is the ID of the owner org
            :param source_id: is the ID of the owner source
            :param base_data: is a dictionary of all the data fields
            :param names: is a list of dictionary of name fields, optional.
            :param descriptions: is a list of dictionary of name fields, optional.
            :param extras: is a list of dictionary of name fields, optional.

            :returns: POST result from requests package.
        """
        data = {}
        data.update(base_data)

        list_data = []
        for n in names:
            list_data.append(n)
        if len(list_data) > 0:
            data['names'] = list_data

        list_data = []
        for d in descriptions:
            list_data.append(d)
        if len(list_data) > 0:
            data['descriptions'] = list_data

        list_data = []
        for e in extras:
            list_data.append(e)
        if len(list_data) > 0:
            data['extras'] = list_data

        result = self.post(
            source_owner_type, source_owner_id, 'sources', source_id,
            'concepts', **data)
        return result

    def update_concept(self, source_owner_type, source_owner_id, source_id,
                       concept_id, base_data,
                       names=[], descriptions=[], extras=[]):
        """ Update a concept.
            NOTE: currently add by org+source, but there are other options... TODO

            :param org_id: is the ID of the owner org
            :param source_id: is the ID of the owner source
            :param base_data: is a dictionary of all the data fields
            :param names: is a list of dictionary of name fields, optional.
            :param descriptions: is a list of dictionary of name fields, optional.
            :param extras: is a list of dictionary of name fields, optional.

            :returns: POST result from requests package.
        """
        data = {}
        data.update(base_data)

        list_data = []
        for n in names:
            list_data.append(n)
        if len(list_data) > 0:
            data['names'] = list_data

        list_data = []
        for d in descriptions:
            list_data.append(d)
        if len(list_data) > 0:
            data['descriptions'] = list_data

        list_data = []
        for e in extras:
            list_data.append(e)
        if len(list_data) > 0:
            data['extras'] = list_data

        # TODO: Why doesn't POST work?
        result = self.put(
            source_owner_type, source_owner_id, 'sources', source_id,
            'concepts', concept_id, **data)
        return result

    def create_org(self, base_data, extras=[]):
        """
            Create organization

            :param base_data: is a dictionary of fields.

            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('orgs', **data)
        return result

    def update_org(self, org_id, base_data, extras=[]):
        """
            Update organization

            :param org_id: is the ID for the organization being updated.
            :param base_data: is a dictionary of fields.

            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('orgs', org_id, **data)
        return result

    def create_source_by_org(self, org_id, base_data, extras=[]):
        """
            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('orgs', org_id, 'sources', **data)
        return result

    def create_source_by_user(self, user_id, base_data, extras=[]):
        """
            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('users', user_id, 'sources', **data)
        return result

    def create_source_by_me(self, base_data, extras=[]):
        """
            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('users', 'sources', **data)
        return result

    def update_source_by_org(self, org_id, source_id, base_data, extras=[]):
        """
            update source owned by org.

            :param org_id: is the org owner of this wource.
            :param base_data: is a dictionary of fields.

            :returns: response object.
        """
        data = {}
        data.update(base_data)
        # TODO: Why doesn't POST work?
        result = self.put('orgs', org_id, 'sources', source_id, **data)
        return result

    def update_source_by_user(self, username, source_id, base_data, extras=[]):
        """
            Update source owned by user.

            :param username: is the user owner of this wource.
            :param base_data: is a dictionary of fields.

            :returns: response object.
        """
        data = {}
        data.update(base_data)
        # TODO: Why doesn't POST work?
        result = self.put('users', username, 'sources', source_id, **data)
        return result

    def create_source_version_by_org(self, org_id, source_id, base_data):
        """
            create a new source version owned by org.

            :param org_id: is the org owner of this wource.
            :param base_data: is a dictionary of fields.

            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('orgs', org_id, 'sources', source_id,
                           'versions', **data)
        return result

    def create_source_version_by_user(self, username, source_id, base_data):
        """
            create a new source version owned by user.

            :param username: is the user owner of this wource.
            :param base_data: is a dictionary of fields.

            :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.post('users', username, 'sources', source_id,
                           'versions', **data)
        return result

    def create_mapping(self, source_owner_type, source_owner_id, source_id,
                       concept_id, data):
        """ Create a concept mapping

            :param source_owner_type: is a string of either 'org' or 'user'
            :param source_owner_id: is the ID of the owner org or user
            :param source_id: is the ID of the owner source
            :param concept_id: is the concept ID of the source concept
            :param data: is a dictionary of all the data fields

            :returns: POST result from requests package.
        """
        result = self.post(source_owner_type, source_owner_id,
                           'sources', source_id, 'concepts', concept_id,
                           'mappings', **data)
        return result
