"""
This is the central interface to the OCL API.
"""
import os
import logging
import requests
import simplejson as json

from django.conf import settings
from .search import OclSearch
from .constants import OclConstants


SESSION_TOKEN_KEY = 'API_USER_TOKEN'


class OclApi(object):
    """
    Interface to the OCL API backend.
    Handles all the authentication and formating.
    Also contain helper and utility functions.
    :logging: This class outputs debug level information to the "oclapi" logger.
    """

    logger = logging.getLogger('oclapi')


    def __init__(self, request=None, debug=False, admin=False, facets=False):
        """
        :param request: gives API access to the current active session, to get Authorization etc.
        :param admin: optional, if set to True, access API as admin user. Needed for create_user.
        :param facets: optional, if set to True, API returns faceted search information instead
                       of clean JSON results. Note that faceted results are only applicable on
                       certain list requests, and this argument is ignored otherwise.
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

    @property
    def include_facets(self):
        """ Return whether 'includeFacets' is set in the request headers """
        if 'includeFacets' in self.headers:
            return True
        else:
            return False


    @include_facets.setter
    def include_facets(self, include_facets_bool):
        """ Set whether 'includeFacets' is included in the request header """
        if include_facets_bool:
            self.headers['includeFacets'] = 'true'
        elif 'includeFacets' in self.headers:
            del self.headers['includeFacets']


    def post(self, type_name, *args, **kwargs):
        """
        Issue POST request to API.
        :param type_name: is a string specifying the type of the object according to the API.
        :param *args: The rest of the positional arguments will be appended to the post URL
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
        """
        Issue delete request to API.
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
        """
        Issue delete request to API.
        :param type_name: is a string specifying the type of the object according to the API.
        """
        url = '%s/%s/' % (self.host, type_name)
        if len(args) > 0:
            url = url + '/'.join(args) + '/'

        if self.debug:
            self.logger.debug('PUT %s %s %s' % (url, json.dumps(kwargs),
                                                self.headers))

        params = kwargs.get('params')

        results = requests.put(url, data=json.dumps(kwargs),
                               headers=self.headers, params=params)
        self.status_code = results.status_code
        if self.debug:
            self.debug_result(results)
        return results


    def head(self, *args, **kwargs):
        """
        Issue HEAD request to API.
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
        """
        Issue get request to API.
        :param *args: All positional arguments are appended to the request URL.
            Note: To pass query parameters to the GET function,
            use a params={k:v} keyword argument.
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


    # TODO: Retire get_json?
    def get_json(self, *args):
        """
        Smarter GET request when you really want a json object back.
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


    # TODO: Retire get_by_url?
    def get_by_url(self, url, **kwargs):
        """
        Issue get request to API.
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
        """
        Save API user token into session table for online use.
        :param request: is the django http request
        :param api_json_data: contains the backend auth token.
        """
        request.session[SESSION_TOKEN_KEY] = json_data['token']


    def create_user(self, data):
        """
        Create a user in the system. This call is a bit special because
        users need to be created using admin credentials.
        :param data: is a dictionary of all the data fields.
        :returns: requests.reponse object
        """
        result = self.post('users', **data)
        return result


    def delete_user(self, username):
        """
        Delete a user in the system, actually just deactivates her.
        delete users needs admin credentials.
        :param username: is a string specifying the username.
        :returns: ??
        """
        result = self.delete('users', username)
        return result


    def reactivate_user(self, username):
        """
        Delete a user in the system, actually just deactivates her.
        delete users needs admin credentials.
        :param username: is a string specifying the username.
        :returns: ??
        """
        result = self.put('users/%s/reactivate/' % username)
        return result


    def get_user_auth(self, username, password):
        """
        Get the user AUTH token for the specified user.
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

    def extract_names(self, names):
        if names is None:
            return []
        return names

    def extract_descriptions(self, descriptions):
        if descriptions is None:
            return None
        if len(descriptions) is 1 and not descriptions[0]['description']:
            return None
        return descriptions

    def create_concept(self, source_owner_type, source_owner_id, source_id, base_data,
                       names=[], descriptions=[], extras=None):
        """
        Create a concept.
        :param source_owner_type: 'orgs' or 'users'
        :param source_owner_id: ID of org/user owner
        :param source_id: is the ID of the owner source
        :param base_data: is a dictionary of all the data fields
        :param names: is a list of dictionary of name fields, optional.
        :param descriptions: is a list of dictionary of name fields, optional.
        :param extras: is a dictionary of name fields, optional.
        :returns: POST result from requests package.
        """
        data = {}
        data.update(base_data)

        data['names'] = self.extract_names(names)
        data['descriptions'] = self.extract_descriptions(descriptions)

        if extras:
            data['extras'] = extras
        result = self.post(
            source_owner_type, source_owner_id, 'sources', source_id,
            'concepts', **data)
        return result

    def update_concept(self, source_owner_type, source_owner_id, source_id,
                       concept_id, base_data,
                       names=[], descriptions=[], extras=[]):
        """
        Update a concept.
        NOTE: currently add by org+source, but there are other options... TODO
        :param source_owner_type: 'orgs' or 'users'
        :param source_owner_id: ID of org/user owner
        :param source_id: is the ID of the owner source
        :param concept_id: is the ID of the owner source
        :param base_data: is a dictionary of all the data fields
        :param names: is a list of dictionary of name fields, optional.
        :param descriptions: is a list of dictionary of name fields, optional.
        :param extras: is a list of dictionary of name fields, optional.
        :returns: POST result from requests package.
        """
        data = {}
        data.update(base_data)

        data['names'] = self.extract_names(names)
        data['descriptions'] = self.extract_descriptions(descriptions)

        list_data = []
        for extra in extras:
            list_data.append(extra)
        if len(list_data) > 0:
            data['extras'] = list_data

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


    def create_source(self, owner_type, owner_id, base_data, extras=[]):
        """
        Create source.
        :param owner_type: 'orgs' or 'users'
        :param owner_id: ID of the org/user/ owner
        :param base_data: Dictionary of fields for the new source version
        :param extras: Extras to save to the resource
        :returns: response object

        TODO(paynejd): create_sources extras not implemented
        """
        data = {}
        data.update(base_data)
        result = self.post(owner_type, owner_id, 'sources', **data)
        return result


    def update_source(self, owner_type, owner_id, source_id, base_data, extras=[]):
        """
        Update source owned by org.
        :param owner_type: 'orgs' or 'users'
        :param owner_id: ID of the org/user/ owner
        :param base_data: is a dictionary of fields.
        :param extras: Extras to save to the resource
        :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.put(owner_type, owner_id, 'sources', source_id, **data)
        return result


    def create_source_version(self, owner_type, org_id, source_id, base_data):
        """
        Create a new source version.
        :param owner_type: 'orgs' or 'users'
        :param owner_id: ID of the org/user/ owner
        :param source_id: ID of the source
        :param base_data: Dictionary of fields for the new source version
        :returns: response object
        """
        data = {}
        data.update(base_data)
        result = self.post(owner_type, org_id, 'sources', source_id, 'versions', **data)
        return result


    def update_resource_version(self, owner_type, owner_id,
                                resource_id, version_id, resource_type, base_data):
        """
        Update source version. Limits update to only the description and released fields for now.
        :param owner_type: 'orgs' or 'users'
        :param owner_id: ID of the org/user owner
        :param resource_id: ID of the source/collection
        :param version_id: ID of the source/collection_version
        :param resource_type: 'source' or 'collection'
        :param base_data: Dictionary of fields to update
        :returns: response object
        """
        data = {}
        if 'description' in base_data:
            data['description'] = base_data['description']
        if 'released' in base_data:
            data['released'] = base_data['released']
        if 'retired' in base_data:
            data['retired'] = base_data['retired']
        result = self.put(owner_type, owner_id, resource_type, resource_id, version_id, **data)
        return result


    def update_collection(self, owner_type, owner_id, collection_id, base_data, extras=[]):
        """
        Update collection.
        :param owner_type: 'orgs' or 'users'
        :param owner_id: ID of the org/user/ owner
        :param base_data: is a dictionary of fields.
        :param extras: Extras to save to the resource
        :returns: response object.
        """
        data = {}
        data.update(base_data)
        result = self.put(owner_type, owner_id, 'collections', collection_id, **data)
        return result

    def create_mapping_from_concept(self, source_owner_type, source_owner_id,
                                    source_id, from_concept_id, data):
        """
        Create a concept mapping from the specified concept

        The 'from_concept_url' is automatically set using the provided source_owner_type,
        'source_owner_id', 'source_id', and 'from_concept_id'. If the from_concept is not
        stored in the provided source, use create_mapping().

        :param source_owner_type: Either 'orgs' or 'users'
        :param source_owner_id: ID of the owner org/user
        :param source_id: ID of the source that will own the new mapping
        :param from_concept_id: ID of the from-concept
        :param data: A dictionary of all the data fields to POST
        :returns: POST result from requests package.
        """
        data['from_concept_url'] = ('/' + source_owner_type + '/' + source_owner_id +
                                    '/sources/' + source_id + '/concepts/' +
                                    from_concept_id + '/')
        return self.create_mapping(source_owner_type, source_owner_id, source_id, data)


    def create_mapping(self, source_owner_type, source_owner_id, source_id, data):
        """
        Create a mapping

        'from_concept_url' and 'map-type' are required fields in the data dictionary.
        If internal mapping, must include 'to_concept_url'. If external mapping, must
        include 'to_source_url' and 'to_concept_code'. Refer to API documentation
        for details and other optional fields.

        :param source_owner_type: Either 'orgs' or 'users'
        :param source_owner_id: ID of the owner org/user (e.g. "WHO")
        :param source_id: ID of the source that will own the new mapping (e.g. "ICD-10")
        :param data: A dictionary of all the data fields to POST
        :returns: POST result from requests package.
        """
        result = self.post(source_owner_type, source_owner_id,
                           'sources', source_id, 'mappings', **data)
        return result


    def update_mapping(self, source_owner_type, source_owner_id, source_id, mapping_id, data):
        """
        Update a mapping

        TODO: Unclear what happens if changing between internal/external -- consider only
        allowing updates to external_id, map_type, to_concept_name, and extras.

        :param source_owner_type: Either 'orgs' or 'users'
        :param source_owner_id: ID of the owner org/user (e.g. "WHO")
        :param source_id: ID of the source that will own the new mapping (e.g. "ICD-10")
        :param mapping_id: ID of the mapping to update
        :param data: A dictionary of all the data fields to POST
        :returns: POST result from requests package.
        """
        result = self.put(source_owner_type, source_owner_id,
                          'sources', source_id, 'mappings', mapping_id, **data)
        return result


    def create_collection_version(self, owner_type, org_id, collection_id, base_data):

        data = {}
        data.update(base_data)
        result = self.post(owner_type, org_id, 'collections', collection_id, 'versions', **data)
        return result

    def get_all_collections_for_user(self, username):
        return self.get_user_collections(username) + self.get_user_org_collections(username)

    def get_user_collections(self, username):
        user_collection_search_results = \
            self.get('users', username, 'collections', params={'limit': 0}).json()['results']


    def get_user_org_collections(self, username):
        user_orgs = self.get('users', username, 'orgs', params={'limit': 0}).json()
        all_org_collections = []

        for org in user_orgs:
            org_collections = self.get('orgs', org['id'], 'collections', params={'limit': 0}).json()['results']
            all_org_collections += org_collections

        return all_org_collections if len(all_org_collections) > 0 else []

