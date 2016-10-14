import mock
from libs.ocl import OclApi
from django.test import TestCase
from requests.exceptions import HTTPError
from forms import CollectionCreateForm, CollectionEditForm, CollectionVersionAddForm
from requests.models import Response


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


class CollectionCreateTest(TestCase):
    @mock.patch.object(OclApi, 'get')
    def test_when_all_valid_data_is_provided_then_new_collection_should_be_made(self, mock_get):
        form_data = {
            'short_code': 'col',
            'name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        response = Response()
        response.json = lambda: [{'locale': 'en', 'display_name': 'en'}]
        mock_get.return_value = response

        form = CollectionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    @mock.patch.object(OclApi, 'get')
    def test_when_shortName_is_not_provided_then_form_is_not_valid(self, mock_get):
        form_data = {
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @mock.patch.object(OclApi, 'get')
    def test_when_FullName_is_not_provided_then_form_is_not_valid(self, mock_get):
        form_data = {
            'name': 'col',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @mock.patch.object(OclApi, 'get')
    def test_when_defaultLocale_is_not_provided_then_form_is_not_valid(self, mock_get):
        form_data = {
            'name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    @mock.patch.object(OclApi, 'get')
    def test_when_defaultLocales_is_not_provided_then_form_is_not_valid(self, mock_get):
        form_data = {
            'short_code': 'col',
            'name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }

        response = Response()
        response.json = lambda: [{'locale': 'en', 'display_name': 'en'}]
        mock_get.return_value = response

        form = CollectionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

class CollectionEditFormTest(TestCase):

    @mock.patch.object(OclApi, 'get')
    def test_when_edit_form_called_short_name_should_not_be_present(self, mock_get):
        edit_form = CollectionEditForm()
        self.assertFalse(edit_form.fields.__contains__('short_code'))
        self.assertTrue(edit_form.fields.__contains__('name'))
        self.assertTrue(edit_form.fields.__contains__('full_name'))

class CollectionVersionAddFormTest(TestCase):

    def test_collectionVersionAddForm_containesOnlyId_formIsInvalid(self):
        form_data = {
            'id': 'v1.0',
        }
        form = CollectionVersionAddForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_collectionVersionAddForm_containesOnlyDescription_formIsInvalid(self):
        form_data = {
            'description': 'This is version 1.0',
        }
        form = CollectionVersionAddForm(data=form_data)
        self.assertFalse(form.is_valid())

    #TODO Testcases to check for different id inputs remaining

    def test_collectionVersionAddForm_containesBothIdAndDescription_version_missing_formIsValid(self):
        form_data = {
            'id': 'v1.1',
            'description': 'This is version 1.1',
        }
        form = CollectionVersionAddForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_collectionVersionAddForm_containesBothIdAndDescription_formIsValid(self):
        form_data = {
            'id': 'v1.1',
            'description': 'This is version 1.1',
            'previous_version': 'HEAD'
        }
        form = CollectionVersionAddForm(data=form_data)
        self.assertTrue(form.is_valid())
