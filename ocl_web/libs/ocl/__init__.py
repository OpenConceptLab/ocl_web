# Python
import os

# Django
from django.conf import settings

# Third Party
import requests
import simplejson as json

# Ours
from api_resource import ApiResource
from collection import Collection
from concept import Concept
from concept_class import ConceptClass
from concept_data_type import ConceptDataType
from concept_list import ConceptList
from map_type import MapType
from mapping import Mapping
from source import Source
from star import Star
from user import User

SESSION_TOKEN_KEY = 'API_USER_TOKEN'


class OCLapi(object):
    """ Interface to the OCL API backend.
        Handles all the authentication and formating.
        Also contain helper and utility functions.
    """

    def __init__(self, request=None, debug=False, admin=False):
        """
        :param admin: optional, if set to True, access API as admin user. Needed for create_user.
        :param request: gives the API access to the current active session, to get Authorization etc.
        """
        self.debug = debug
        self.host = settings.API_HOST  # backend location
        self.headers = {'Content-Type': 'application/json'}

        # The admin api key should only be used for admin functions (duh)
        self.admin_api_key = os.environ.get('OCL_API_TOKEN', None)

        if admin:
            self.headers['Authorization'] = 'Token %s' % self.admin_api_key
        else:
            if request:
                # Todo: the KEY constant needs to be somewhere else
                key = request.session.get(SESSION_TOKEN_KEY)
                self.headers['Authorization'] = 'Token %s' % key

    def post(self, type_name, *args, **kwargs):
        """ Issue Post request to API.

            :param type_name: is a string specifying the type of the object according
                                to the API.
        """                                
        url = '%s/v1/%s/' % (self.host, type_name)
        if len(args) > 0:
            url = url + '/'.join(args) + '/'
        if self.debug:
            print 'POST %s %s %s' % (url, json.dumps(kwargs), self.headers)

        results = requests.post(url, data=json.dumps(kwargs),
                                headers=self.headers)
        return results

    def delete(self, type_name, object_id, **kwargs):
        """ Issue delete request to API.

            :param type_name: is a string specifying the type of the object according
                                to the API.
            :param object_id: is a string identifying the object for deletion.

        """                                
        url = '%s/v1/%s/%s/' % (self.host, type_name, object_id)

        if self.debug:
            print 'DELETE %s %s %s' % (url, json.dumps(kwargs), self.headers)
            return None

        results = requests.delete(url, data=json.dumps(kwargs),
                                headers=self.headers)
        return results

    def put(self, type_name, **kwargs):
        """ Issue delete request to API.

            :param type_name: is a string specifying the type of the object according
                                to the API.
        """                                
        url = '%s/v1/%s/' % (self.host, type_name)

        if self.debug:
            print 'PUT %s %s %s' % (url, json.dumps(kwargs), self.headers)
            return None

        results = requests.put(url, data=json.dumps(kwargs),
                                headers=self.headers)
        return results

    def get(self, type_name, *args, **kwargs):
        """ Issue get request to API.

            :param type_name: is a string specifying the type of the object according
                                to the API.
        """                                
        url = '%s/v1/%s/' % (self.host, type_name)
        if len(args) > 0:
            url = url + '/'.join(args) + '/'
        if self.debug:
            print 'GET %s %s %s' % (url, json.dumps(kwargs), self.headers)

        results = requests.get(url, data=json.dumps(kwargs),
                                headers=self.headers)
        return results

    def save_auth_token(self, request, json_data):
        """ Save API user token into session table for online use.

            :param request: is the django http request
            :param api_json_data: contains the backend auth token.
        """
        request.session[SESSION_TOKEN_KEY] = json_data['token']

    def create_user(self, **kwargs):
        """ Create a user in the system. This call is a bit special because
            users need to be created using admin credentials.
            :param **kwargs: is a dictionary of all the data fields.

            :returns: ??
        """
        result = self.post('users', **kwargs)
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
        result = self.post('users/login', username=username,
            password=password)
        return result

    def sync_password(self, user):
        """
        sync password with backend
        """
        result = self.post('users/%s/' % user.username, hashed_password=user.password)
        return result


    def create_concept(self, org_id, source_id, base_data, names=[], descriptions=[], extras=[]):
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

        result = self.post('orgs', org_id, 'sources', source_id, 'concepts', **data)
        return result

    def create_org(self, base_data, extras=[]):
        """
        """
        data = {}
        data.update(base_data)
        result = self.post('orgs', **data)
        return result

    def create_source_by_org(self, org_id, base_data, extras=[]):
        """
        """
        data = {}
        data.update(base_data)
        result = self.post('orgs', org_id, 'sources', **data)
        return result

    def create_source_by_me(self, base_data, extras=[]):
        """
        """
        data = {}
        data.update(base_data)
        result = self.post('users', 'sources', **data)
        return result



api_key = os.environ.get('OCL_API_TOKEN', None)
host = settings.API_HOST


def object_hooker(dct):
    class_names = {
        'OclMapType': MapType,
        'OclConcept': Concept,
        'OclConceptClass': ConceptClass,
        'OclConceptList': ConceptList,
        'OclConceptDataType': ConceptDataType,
        'OclCollection': Collection,
        'OclMapping': Mapping,
        'OclSource': Source,
        'OclStar': Star,
        'OclUser': User
    }

    if '__type__' in dct:
        class_name = dct['__type__']
        try:
            # Instantiate class based on value in the variable
            x = class_names[class_name]()
            x.set_values(dct)
            return x
        except KeyError:
            # handle error - Class is not defined
            pass
    return dct


class APIRequestor(object):

    def __init__(self, api_key=api_key):
        self.api_key = api_key
        self.headers = {'Authorization': 'Token %s' % api_key}
        self.headers['Content-Type'] = 'application/json'
        self.host = host

    def instance_url(self, cls):

        return '/v1/%ss/' % cls.__name__.lower()

    def post(self, url, **kwargs):

        results = requests.post(
            self.host + url,
            data=json.dumps(kwargs),
            headers=self.headers)

        return results


class Org(object):
    """ Not used anymore """

    @classmethod
    def create(cls, org_id, name, **kwargs):

        requestor = APIRequestor(api_key=api_key)
        url = requestor.instance_url(cls)
        results = requestor.post(url, id=org_id, name=name, **kwargs)

        # TODO: Raise bad requests here?  Yes, via Exceptions.
        # TODO: Return the org in a leaner format?
        return results
