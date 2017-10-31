import json
from unittest import TestCase
from unittest import skip
from apps.sources.forms import SourceDeleteForm
from django.contrib import messages
from mock import patch, MagicMock
from requests.models import Response
import views


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

    @patch('django.contrib.messages.add_message')
    @patch('libs.ocl.OclApi.delete')
    def test_whenDeleteSuccessfull_thenReturnSourceDeletedMessage(self, mock_delete, mock_message):
        colResponse = MagicMock(spec=Response, status_code=204)
        mock_delete.return_value=colResponse
        form = SourceDeleteForm()
        sourceDeleteView= views.SourceDeleteView()
        sourceDeleteView.request = FakeRequest()
        sourceDeleteView.kwargs = {
            'org': 'testOrgId',
        }

        sourceDeleteView.form_valid(form)
        mock_message.assert_called_once_with(sourceDeleteView.request, messages.INFO, ('Source Deleted'))

class SourceVersionEditJsonViewTest(TestCase):
    @patch('libs.ocl.OclApi.update_resource_version')
    def test_put(self, mock_update_resource_version):
        colResponse = MagicMock(spec=Response)
        colResponse.status_code=200
        colResponse.json.return_value = "foobar"
        mock_update_resource_version.return_value = colResponse
        sourceVersionEditView = views.SourceVersionEditJsonView()
        fake_request = FakeRequest()
        fake_request.body = json.dumps({'released':True})
        sourceVersionEditView.request = fake_request
        sourceVersionEditView.put(fake_request, {}, **{'org': 'org', 'source': 'sourceId', 'source_version': 'v1'})
        self.assertTrue(mock_update_resource_version.called)

