from django.test import TestCase
from forms import OrganizationNewForm
from unittest import skip


class OrganizationNewFormTest(TestCase):
    def test_when_required_fields_provided_then_form_is_valid(self):
        form_data = {
            'short_name': 'testshort',
            'name': 'test full name'
        }
        form = OrganizationNewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_when_all_required_fields_missing_form_is_invalid(self):
        form_data = {
            'something': 'something'
        }
        form = OrganizationNewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_when_required_short_name_field_missing_form_is_invalid(self):
        form_data = {
            'name': 'test full name'
        }
        form = OrganizationNewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_when_required_name_field_missing_form_is_invalid(self):
        form_data = {
            'short_name': 'testshort'
        }
        form = OrganizationNewForm(data=form_data)
        self.assertFalse(form.is_valid())

