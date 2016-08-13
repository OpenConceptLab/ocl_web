from unittest import TestCase
from requests.exceptions import HTTPError
from requests.models import Response
from mock import Mock, patch, MagicMock
from django.contrib import messages
from apps.sources.forms import  SourceDeleteForm
from libs.ocl import OclApi, OclSearch, OclConstants
import views;
from unittest import skip

class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}
        self.GET = {}

class DeleteViewTest(TestCase):
    @patch('libs.ocl.OclApi.get')
    def test_getContextForSource_contextForSourceReceived(self, mock_get):
        colResponse = MagicMock(spec=Response)
        colResponse.json.return_value = "testSource"
        mock_get.return_value = colResponse
        sourceDeleteView = views.SourceDeleteView()
        sourceDeleteView.request = FakeRequest()
        sourceDeleteView.kwargs = {
            'source_id': 'testSourceId',
        }
        context = sourceDeleteView.get_context_data();
        self.assertEquals(context['source'],'testSource')

    @skip("need to fix this test case")
    @patch('libs.ocl.OclApi.delete')
    @patch('django.contrib.messages.api')
    def test_whenDeleteSuccessfull_thenReturnSourceDeletedMessage(self, mock_delete,mock_message):
        colResponse = MagicMock(spec=Response, status_code=204)
        mock_delete.return_value=colResponse
        form = SourceDeleteForm()
        sourceDeleteView= views.SourceDeleteView()
        sourceDeleteView.request = FakeRequest()
        sourceDeleteView.kwargs = {
            'org': 'testOrgId',
        }

        result=sourceDeleteView.form_valid(form)
        mock_message.add_message.asser_called_with("error","Error")
        print result
