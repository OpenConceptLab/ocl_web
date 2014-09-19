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


class OCLapi(object):
    """ Interface to the OCL API backend.
        Handles all the authentication and formating.
        Also contain helper and utility functions.
    """

    def __init__(self, debug=False):

        self.debug = debug
        self.host = settings.API_HOST  # backend location
        self.headers = {'Content-Type': 'application/json'}

        # The admin api key should only be used for admin functions (duh)
        self.admin_api_key = os.environ.get('OCL_API_TOKEN', None)

        self.headers['Authorization'] = 'Token %s' % self.admin_api_key


    def post(self, type_name, **kwargs):
        """ Issue Post request to API.

            :param type_name: is a string specifying the type of the object according
                                to the API.
        """                                
        url = '%s/v1/%s/' % (self.host, type_name)

        if self.debug:
            print 'POST %s %s %s' % (url, json.dumps(kwargs), self.headers)
            return None

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
        result = self.post('users/login/', username=username,
            password=password)
        return result


api_key = os.environ.get('OCL_API_TOKEN', None)
host = settings.API_HOST


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

    @classmethod
    def create(cls, org_id, name, **kwargs):

        requestor = APIRequestor(api_key=api_key)
        url = requestor.instance_url(cls)
        results = requestor.post(url, id=org_id, name=name, **kwargs)

        # TODO: Raise bad requests here?  Yes, via Exceptions.
        # TODO: Return the org in a leaner format?
        return results
