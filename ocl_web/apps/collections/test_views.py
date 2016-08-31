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
from unittest import skip

class MyDict(dict):
    def __init__(self,name):
        self.username = name


class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}
        self.GET = {}
    def get_full_path(self):
        return '/foobar'

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

    @skip('TODO: test showing exception. not able to fix now. will come back')
    @patch('libs.ocl.OclApi.post')
    def test_validDataPassedfromOrg_formIsValid(self, mock_post):
        form_data = {
            'short_code': 'col',
            'name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        form.full_clean()
        colResponse = FakeResponse()
        colResponse.status_code=201
        mock_post.return_value = colResponse
        collectionCreateView = views.CollectionCreateView()
        collectionCreateView.request = FakeRequest()
        collectionCreateView.kwargs = {
            'org': 'testOrgId',
        }
        abc = collectionCreateView.form_valid(form)
        # print abc

class CollectionEditViewTest(TestCase):
    @patch('libs.ocl.OclApi.get')
    def test_getFromClass_getData(self, mock_get):
        collectionEditView=views.CollectionEditView()
        collectionEditView.request = FakeRequest()
        collectionEditView.kwargs = {
            'org': 'testOrgId',
        }

        collectionForm = collectionEditView.get_form_class()
        self.assertEquals(collectionForm.__name__, 'CollectionEditForm')

    @patch('libs.ocl.OclApi.get')
    def test_getContextForUserCol_contextForUserReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testUser"
        mock_get.return_value = colResponse
        collectionEditView = views.CollectionEditView()
        collectionEditView.request = FakeRequest()
        collectionEditView.collection = {'id':'mycolid'}
        collectionEditView.kwargs = {
            'user': 'testUserId',
        }
        context = collectionEditView.get_context_data();
        self.assertIsNone(context['org'])
        self.assertEquals(context['ocl_user'], "testUser")
        self.assertTrue(context['from_user'])
        self.assertFalse(context['from_org'])

    @patch('libs.ocl.OclApi.get')
    def test_getContextForOrgCol_contextForOrgReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testOrg"
        mock_get.return_value = colResponse
        collectionEditView = views.CollectionEditView()
        collectionEditView.request = FakeRequest()
        collectionEditView.collection = {'id': 'mycolid'}
        collectionEditView.kwargs = {
            'org': 'testOrgId',
        }
        context = collectionEditView.get_context_data();
        self.assertEquals(context['org'], "testOrg")
        self.assertIsNone(context['ocl_user'])
        self.assertFalse(context['from_user'])
        self.assertTrue(context['from_org'])

class CollectionDeleteViewTest(TestCase):
    @patch('libs.ocl.OclApi.get')
    def test_getContextForCol_contextForCollectionReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testCollection"
        mock_get.return_value = colResponse
        collectionDeleteView = views.CollectionDeleteView()
        collectionDeleteView.request = FakeRequest()
        collectionDeleteView.collection = {'id': 'mycolid'}
        collectionDeleteView.kwargs = {
            'collection_id': 'testColId',
        }
        context = collectionDeleteView.get_context_data();
        self.assertEquals(context['collection'],'testCollection')

    @skip("need to fix this test case")
    @patch('django.contrib.messages.api')
    @patch('libs.ocl.OclApi.delete')
    def test_whenDeleteSuccessfull_thenReturnCollectionDeletedMessage(self, mock_delete,mock_message):
        colResponse = MagicMock(spec=Response, status_code=204)
        mock_delete.return_value=colResponse
        form = CollectionDeleteForm()
        collectionDeleteView= views.CollectionDeleteView()
        collectionDeleteView.request = FakeRequest()
        collectionDeleteView.kwargs = {
            'org': 'testOrgId',
        }

        result=collectionDeleteView.form_valid(form)
        mock_message.add_message.asser_called_with("error","Error")
        print result


class CollectionAddReferenceViewTest(TestCase):

    @patch('libs.ocl.OclApi.get')
    def test_getContextForColReference_contextForCollectionReferenceReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testCollection"
        mock_get.return_value = colResponse
        collectionAddReferenceView = views.CollectionAddReferenceView()
        collectionAddReferenceView.request = FakeRequest()
        collectionAddReferenceView.collection = {'id': 'mycolid'}
        collectionAddReferenceView.kwargs = {
            'collection_id': 'testColId',
        }
        context = collectionAddReferenceView.get_context_data()
        self.assertEquals(context['collection'], 'testCollection')


class CollectionConceptViewTest(TestCase):

    @patch('libs.ocl.OclApi.get')
    def test_getContextForCollectionConcepts_contextRecieved(self, mock_get):
        conceptResponse = MagicMock(spec=Response)
        collection = ["Some Results"]
        conceptResponse.json.return_value = collection
        conceptResponse.status_code = 200
        conceptResponse.headers = []
        mock_get.return_value = conceptResponse

        collectionConceptsView = views.CollectionConceptsView()
        collectionConceptsView.request = FakeRequest()

        hash = {'collection': 'test', 'org': 'org1'}
        collectionConceptsView.kwargs = hash
        context = collectionConceptsView.get_context_data()

        self.assertEquals(context['url_params'], {})
        self.assertEquals(context['kwargs'], hash)
        self.assertEquals(context['selected_tab'], 'Concepts')
        self.assertEquals(context['results'], collection)
        self.assertEquals(context['pagination_url'], '/foobar')
        self.assertEquals(context['search_query'], '')
        self.assertEquals(context['search_filters'], None)
        self.assertEquals(context['search_sort_options'], ['Best Match', 'Last Update (Desc)', 'Last Update (Asc)', 'Name (Asc)', 'Name (Desc)'])
        self.assertEquals(context['search_sort'], '')
        self.assertEquals(context['search_facets_json'], None)

class CollectionMappingsViewTest(TestCase):

    @patch('libs.ocl.OclApi.get')
    def test_getContextForCollectionMappings_contextRecieved(self, mock_get):
        mappingResponse = MagicMock(spec=Response)
        collection = ["Some Results"]
        mappingResponse.json.return_value = collection
        mappingResponse.status_code = 200
        mappingResponse.headers = []
        mock_get.return_value = mappingResponse

        collectionMappingsView = views.CollectionMappingsView()
        collectionMappingsView.request = FakeRequest()

        hash = {'collection': 'test', 'org': 'org1'}
        collectionMappingsView.kwargs = hash
        context = collectionMappingsView.get_context_data()

        self.assertEquals(context['url_params'], {})
        self.assertEquals(context['kwargs'], hash)
        self.assertEquals(context['selected_tab'], 'Mappings')
        self.assertEquals(context['results'], collection)
        self.assertEquals(context['pagination_url'], '/foobar')
        self.assertEquals(context['search_query'], '')
        self.assertEquals(context['search_filters'], None)
        self.assertEquals(context['search_sort_options'], ['Best Match', 'Last Update (Desc)', 'Last Update (Asc)', 'Name (Asc)', 'Name (Desc)'])
        self.assertEquals(context['search_sort'], '')
        self.assertEquals(context['search_facets_json'], None)

class CollectionReferencesViewTest(TestCase):
    # todo improve below test case by testing vesrions too
    @patch('libs.ocl.OclApi.get')
    def test_getContextForCollectionReferences_contextRecieved(self, mock_get):
        referenceResponse = MagicMock(spec=Response)
        references = ["Some Results"]
        referenceResponse.json.return_value = references
        referenceResponse.status_code = 200
        referenceResponse.headers = []

        mock_get.return_value = referenceResponse

        collectionReferencesView = views.CollectionReferencesView()
        collectionReferencesView.request = FakeRequest()

        hash = {'collection': 'test', 'org': 'org1'}
        collectionReferencesView.kwargs = hash
        context = collectionReferencesView.get_context_data()

        self.assertEquals(context['kwargs'], hash)
        self.assertEquals(context['selected_tab'], 'References')
        self.assertEquals(context['collection'], references)


class CollectionVersionsNewViewTest(TestCase):

    @patch('libs.ocl.OclApi.get')
    def test_getContextForColVersion_contextForCollectionVersionReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testCollection"
        mock_get.return_value = colResponse
        collectionVersionNewView = views.CollectionVersionsNewView()
        collectionVersionNewView.request = FakeRequest()
        collectionVersionNewView.collection = {'id': 'mycolid'}
        collectionVersionNewView.kwargs = {
            'collection_id': 'testColId',
        }
        context = collectionVersionNewView.get_context_data()
        self.assertEquals(context['collection'], 'testCollection')

    @skip("need to fix this test case")
    @patch('django.contrib.messages.api')
    @patch('libs.ocl.OclApi.create_collection_version')
    def test_whenDeleteSuccessfull_thenReturnCollectionDeletedMessage(self, mock_create_version, mock_message):
        colResponse = MagicMock(spec=Response, status_code=204)
        mock_create_version.return_value = colResponse
        form_data = {
            'id': 'testv1',
            'description': 'testdescription',
        }
        form = CollectionVersionAddForm(form_data)
        form.full_clean()
        collectionNewVserionView = views.CollectionVersionsNewView()
        collectionNewVserionView.request = FakeRequest()
        collectionNewVserionView.kwargs = {
            'org': 'testOrgId',
        }

        result = collectionNewVserionView.form_valid(form)
        mock_message.add_message.asser_called_with("error", "Error")
        print result
