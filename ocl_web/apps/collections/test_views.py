from unittest import TestCase
import mock
from django.http import Http404
from django_extensions.db.fields import json
from requests.exceptions import HTTPError
from requests.models import Response
from django.http.request import HttpRequest
from mock import Mock, patch, MagicMock
from libs.ocl import OclApi, OclSearch, OclConstants
import views;
from unittest import skip

class MyDict(dict):
    def __init__(self,name):
        self.username = name


class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}
        self.GET = {}

class FakeResponse(object):
    """ FakeRequest class """
    def __init__(self,data=None):
        self.session = {}
        self.GET = {}
        self.detail = data
        self.status_code = 200
    def json(self):
        return {'detail': self.detail}
    def raise_for_status(self):
        raise HTTPError('error', response=self)

class CollectionDetailViewTest(TestCase):

    def setUp(self):
        self.get_response = FakeResponse()

    @mock.patch.object(OclApi, 'get')
    def test_getCollectionContext_404ErrorReceived_raised404Exception(self, mock_get):
        coll_id = "my_coll_id"
        kwargs = {'collection_id':coll_id,'org':None}

        self.get_response.status_code = 404
        mock_get.return_value = self.get_response

        collectionDetailView = views.CollectionDetailView()
        collectionDetailView.request = FakeRequest()
        collectionDetailView.kwargs = {}

        try:
            collectionDetailView.get_context_data(**kwargs)
            self.fail("this should never be called")
        except Http404:
            self.assertTrue(mock_get.called)
            pass

    @mock.patch.object(OclApi, 'get')
    def test_getCollectionContext_500ErrorReceived_raised404Exception(self, mock_get):
        coll_id = "my_coll_id"
        kwargs = {'collection_id': coll_id, 'org': None}

        self.get_response.status_code = 500
        mock_get.return_value = self.get_response

        collectionDetailView = views.CollectionDetailView()
        collectionDetailView.request = FakeRequest()
        collectionDetailView.kwargs = {}

        try:
            collectionDetailView.get_context_data(**kwargs)
            self.fail("this should never be called")
        except HTTPError:
            self.assertTrue(mock_get.called)
            pass


    @patch('libs.ocl.OclApi.get')
    def test_getContextData_contextDataReceivedWithCollectionDetail(self, mock_get):

        colResponse = FakeResponse('mycoldetail')

        mock_get.return_value = colResponse

        collectionDetailView = views.CollectionDetailView()
        collectionDetailView.request = FakeRequest()
        collectionDetailView.kwargs = {'extra':'extra'}

        kwargs = {'object': MyDict('Jon')}
        context = collectionDetailView.get_context_data(**kwargs)
        self.assertEquals(context['collection'], colResponse.json())
        self.assertEquals(context['selected_tab'], 'Details')





