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

    def post(self, url, params):

        json_params = json.dumps(params)
        import pdb; pdb.set_trace()
        return requests.post(self.host + url, params=json_params, headers=self.headers)


class Org(object):

    @classmethod
    def create(cls, short_name, full_name, website):

        requestor = APIRequestor(api_key=api_key)
        url = requestor.instance_url(cls)
        results = requestor.post(
            url,
            {'id': short_name,
             'name': full_name,
             'website': website})

        return results

        # Return the org
        # Return the response object as Python






