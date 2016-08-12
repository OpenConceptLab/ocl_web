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



class CollectionCreateViewTest(TestCase):

    def test_getInitialViewOfOrgCol_initialViewWithDataSet(self):
        collectionCreateView = views.CollectionCreateView()
        collectionCreateView.request = FakeRequest()
        collectionCreateView.kwargs = {
            'org':'testOrgId',
        }
        data = collectionCreateView.get_initial();
        self.assertIsNone(data['user_id'], "for org col , user should be none")
        self.assertEquals(data['org_id'], 'testOrgId')
        self.assertFalse(data['from_user'])
        self.assertTrue(data['from_org'])
        self.assertEquals(data['request'], collectionCreateView.request)

    def test_getInitialViewOfUserCol_initialViewWithDataSet(self):
        collectionCreateView = views.CollectionCreateView()
        collectionCreateView.request = FakeRequest()
        collectionCreateView.kwargs = {
            'user':'testUserId',
        }
        data = collectionCreateView.get_initial();
        self.assertIsNone(data['org_id'],"for user col , org should be none")
        self.assertEquals(data['user_id'], 'testUserId')
        self.assertFalse(data['from_org'])
        self.assertTrue(data['from_user'])
        self.assertEquals(data['request'], collectionCreateView.request)

    @patch('libs.ocl.OclApi.get')
    def test_getContextForOrgCol_contextForOrgReceived(self, mock_get):
        colResponse = MagicMock(spec = Response)
        colResponse.json.return_value = "testOrg"
        mock_get.return_value = colResponse
        collectionCreateView = views.CollectionCreateView()
        collectionCreateView.request = FakeRequest()
        collectionCreateView.kwargs = {
            'org':'testOrgId',
        }
        context = collectionCreateView.get_context_data();
        self.assertEquals(context['org'], "testOrg")
        self.assertIsNone(context['ocl_user'])
        self.assertFalse(context['from_user'])
        self.assertTrue(context['from_org'])

    @patch('libs.ocl.OclApi.get')
    def test_getContextForOrgUser_contextForUserReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testUser"
        mock_get.return_value = colResponse
        collectionCreateView = views.CollectionCreateView()
        collectionCreateView.request = FakeRequest()
        collectionCreateView.kwargs = {
            'user': 'testUserId',
        }
        context = collectionCreateView.get_context_data();
        self.assertIsNone(context['org'])
        self.assertEquals(context['ocl_user'], "testUser")
        self.assertTrue(context['from_user'])
        self.assertFalse(context['from_org'])



