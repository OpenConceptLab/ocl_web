from unittest import TestCase
import mock
from django.http import Http404
from django_extensions.db.fields import json
from requests.exceptions import HTTPError
from requests.models import Response
from django.http.request import HttpRequest
from mock import Mock, patch, MagicMock
from django.contrib import messages
from apps.collections.forms import CollectionCreateForm, CollectionEditForm, CollectionDeleteForm, \
    CollectionVersionAddForm
from libs.ocl import OclApi, OclSearch, OclConstants
import views

class MyDict(dict):
    def __init__(self,name):
        self.username = name


class FakeRequest(object):

    """ FakeRequest class """
    def __init__(self):
        self.session = {}
        self.GET = {}
        self.body = None
        self.user = MyDict('tempuser')

    def get_full_path(self):

        return '/foobar'

class FakeResponse(object):
    """ FakeRequest class """
    def __init__(self,data=None):
        self.session = {}
        self.GET = {}
        self.detail = data
        self.status_code = 200
        self.headers = {}
    def json(self):
        return {'detail': self.detail}
    def raise_for_status(self):
        raise HTTPError('error', response=self)


class MappingVersionsViewTest(TestCase):

    @patch('libs.ocl.OclApi.get')
    def test_getcontextData_contextDataRecievedWithMappingVersions(self, mock_get):
        search_response_mapping = FakeResponse()
        search_response_version = FakeResponse()

        mock_get.side_effect = [search_response_mapping, search_response_version]
        mapping = search_response_mapping.json()
        mappingVersion = search_response_version.json()

        mappingVersionsView = views.MappingVersionsView()
        id = 'someID'
        mappingVersionsView.kwargs = {'mapping_id': id}
        mappingVersionsView.request = FakeRequest()

        kwargs={'mapping_id': id}
        context = mappingVersionsView.get_context_data(**kwargs)

        self.assertEquals(context['kwargs'], kwargs)
        self.assertEquals(context['mapping'], mapping)
        self.assertEquals(context['mapping_versions'], mappingVersion)

        self.assertEquals(context['selected_tab'], 'History')

    @patch('libs.ocl.OclApi.get')
    def test_getcontextData_getMappingDetailsRaises404Exception_404ErrorReceived(self, mock_get):
        search_response_mapping = FakeResponse()
        search_response_mapping.status_code = 404
        search_response_version = FakeResponse()

        mock_get.side_effect = [search_response_mapping, search_response_version]

        mappingVersionsView = views.MappingVersionsView()
        id = 'someID'
        mappingVersionsView.kwargs = {'mapping_id': id}
        mappingVersionsView.request = FakeRequest()

        kwargs={'mapping_id': id}
        with self.assertRaises(Http404):
            mappingVersionsView.get_context_data(**kwargs)

    @patch('libs.ocl.OclApi.get')
    def test_getcontextData_getMappingVersionsRaises404Exception_404ErrorReceived(self, mock_get):
        search_response_mapping = FakeResponse()
        search_response_version = FakeResponse()
        search_response_version.status_code = 404

        mock_get.side_effect = [search_response_mapping, search_response_version]

        mappingVersionsView = views.MappingVersionsView()
        id = 'someID'
        mappingVersionsView.kwargs = {'mapping_id': id}
        mappingVersionsView.request = FakeRequest()

        kwargs={'mapping_id': id}
        with self.assertRaises(Http404):
            mappingVersionsView.get_context_data(**kwargs)



