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


class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}
        self.GET = {}

class OrgCollectionViewsTest(TestCase):

    def setUp(self):
        self.search_response = Response()
        self.search_response.status_code = 200

    @mock.patch.object(OclApi, 'get')
    def test_searchParamIsNoneAndResopnseCodeIs404_raised404Exception(self, mock_get):
        org_id = "my_orgs_id"
        self.search_response.status_code = 404
        mock_get.return_value = self.search_response

        orgReadBaseView = views.OrganizationReadBaseView()
        orgReadBaseView.request = None

        try:
            orgReadBaseView.get_org_collections(org_id, search_params=None)
            self.fail("this should never be called")
        except Http404:
            self.assertTrue(mock_get.called)
            pass

    @mock.patch.object(OclApi, 'get')
    def test_searchParamIsNoneAndResopnseCodeIs500_raisedHTTPError(self, mock_get):
        org_id = "my_orgs_id"
        self.search_response.status_code = 500
        mock_get.return_value = self.search_response

        orgReadBaseView = views.OrganizationReadBaseView()
        orgReadBaseView.request = None

        try:
            orgReadBaseView.get_org_collections(org_id, search_params=None)
            self.fail("this should never be called")
        except HTTPError:
            self.assertTrue(mock_get.called)
            pass


    @mock.patch.object(OclApi, 'get')
    @mock.patch.object(OclSearch, 'process_search_results')
    def test_searchParamIsNoneAndResopnseCodeIs200_shouldCallProcessSearchResults(self, mock_api_get, mock_process_search_results):
        org_id = "org_id"
        mock_api_get.return_value = self.search_response
        orgReadBaseView = views.OrganizationReadBaseView()
        orgReadBaseView.request = FakeRequest()

        searcher = orgReadBaseView.get_org_collections(org_id)

        self.assertTrue(mock_process_search_results.called)
        mock_process_search_results.assert_called_with('orgs', org_id, 'collections', params=searcher.search_params)

    @mock.patch.object(OclApi, 'get')
    def test_searchParamIsNoneAndResopnseCodeIs200_shouldReturnAllOrgCollections(self, mock_api_get):
        org_id = "org_id"
        # self.search_response.
        result = ['col1','col2','col3']
        response_mock  = MagicMock(spec=Response, status_code=200, headers={'content-type': "application/json"}
                                   , text=json.dumps({'status': True,"facets": {
                "dates": {},
                "fields": {},
                "queries": {}
            },"results": result
            }))
        response_mock.json.return_value = result
        mock_api_get.return_value = response_mock
        orgReadBaseView = views.OrganizationReadBaseView()
        orgReadBaseView.request = FakeRequest()

        searcher = orgReadBaseView.get_org_collections(org_id, search_params={'resourceFilter':'col'})
        self.assertEquals(searcher.search_results, result)





