from django.test import TestCase
from forms import CollectionCreateForm, CollectionEditForm, CollectionVersionAddForm
from unittest import skip


class CollectionCreateTest(TestCase):
    def test_when_all_valid_data_is_provided_then_new_collection_should_be_made(self):
        form_data = {
            'short_name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_when_shortName_is_not_provided_then_form_is_not_valid(self):
        form_data = {
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_when_FullName_is_not_provided_then_form_is_not_valid(self):
        form_data = {
            'short_name': 'col',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_when_defaultLocale_is_not_provided_then_form_is_not_valid(self):
        form_data = {
            'short_name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_when_defaultLocales_is_not_provided_then_form_is_not_valid(self):
        form_data = {
            'short_name': 'col',
            'full_name': 'collection',
            'collection_type': 'Dictionary',
            'public_access': 'Edit',
            'default_locale': 'en',
            'supported_locales': 'en'
        }
        form = CollectionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

class CollectionEditFormTest(TestCase):

    def test_when_edit_form_called_short_name_should_not_be_present(self):


        edit_form = CollectionEditForm()
        self.assertFalse(edit_form.fields.__contains__('short_name'))
        self.assertTrue(edit_form.fields.__contains__('full_name'))



