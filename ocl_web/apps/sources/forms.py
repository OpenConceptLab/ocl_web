# -*- coding: utf-8 -*-
"""
Forms for sources.
"""
from django.utils.translation import ugettext as _
from django import forms

from libs.ocl import OclApi

from apps.core.views import _get_source_type_list, _get_locale_list, _get_custom_validation_schema_list



class SourceNewForm(forms.Form):
    """ source create form """

    def __init__(self, *args, **kwargs):
        super(SourceNewForm, self).__init__(*args, **kwargs)
        self.fields['default_locale'].choices = [(l['code'], l['name']) for l in _get_locale_list()]

    required_css_class = 'required'

    short_name = forms.CharField(
        label=_('Source Short Code'),
        max_length=128,
        required=True,
        help_text=_('Allowed characters are : Alphabets(a-z,A-Z), Numbers(0-9) and Hyphen(-) <br/> Your new source will live at: http://www.openconceptlab.org'
                    '<span id="new_repository_base_url">/[OwnerType]/[Owner]/sources/</span>'
                    '<span id="new_repository_id" style="font-weight:bold;">[SourceCode]</span>/'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. ICD-10"}))
    full_name = forms.CharField(
        label=_('Source Full Name'),
        max_length=256,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. International Classification for Diseases v10"}))
    website = forms.URLField(
        label=_('Website'),
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. http://apps.who.int/classifications/icd10/"}))
    source_type = forms.ChoiceField(
        choices=[(v, v) for v in _get_source_type_list()],
        label=_('Source Type'),
        required=False)
    public_access = forms.ChoiceField(
        label=_('Public Access'),
        required=False,
        initial='View',
        choices=(('View', 'View (default)'), ('Edit', 'Edit'), ('None', 'None')))
    default_locale = forms.ChoiceField(
        label=_('Default Locale'),
        choices=[],
        required=True)

    supported_locales = forms.CharField(
        max_length=30,
        label=_('Supported Locales'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "e.g. en,fr,es"}))
    custom_validation_schema = forms.ChoiceField(
        label=_('Custom Validation Schema'),
        choices=[(v, v) for v in _get_custom_validation_schema_list()],
        required=False)
    description = forms.CharField(
        max_length=512,
        label=_('Description'),
        required=False)
    external_id = forms.CharField(
        label=_('External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))
    allow_forking = forms.BooleanField(
        label=('Allow Forking'),
        required=False
    )

    # TODO(paynejd@gmail.com): Is this mis-named or not used?
    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        source = self.initial['source']
        request = self.initial['request']
        api = OclApi(request, debug=True)
        result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used.'))
        return concept_id



class SourceEditForm(SourceNewForm):
    """ Form to edit a source """

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(SourceEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_name')

class SourceDeleteForm(forms.Form):
    """ Form to delete a source """
    required_css_class = 'required'


class SourceVersionsNewForm(forms.Form):
    """ Form to create a new source version """
    required_css_class = 'required'

    id = forms.CharField(
        label=_('ID'),
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={'style':'width:480px;',
                   'placeholder': "Name this source version"}))

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={'style':'width:480px;',
                                     'rows':5,
                                     'placeholder':'Describe this source version'}))

    previous_version = forms.CharField(
        required=True,
        widget=forms.HiddenInput())


class SourceVersionsEditForm(SourceVersionsNewForm):
    """ Form to edit a source version """
    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(SourceVersionsEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('id')
        self.fields.pop('previous_version')


class SourceVersionsRetireForm(forms.Form):
    """ Form to retire a source version - empty form """
    # No form fields
