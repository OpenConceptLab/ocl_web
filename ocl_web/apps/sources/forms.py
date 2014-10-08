# -*- coding: utf-8 -*-
"""
    Forms for sources.
"""
from django.utils.translation import ugettext as _
from django import forms

from libs.ocl import OCLapi
from apps.core import LOCALE_LIST


class SourceCreateForm(forms.Form):
    """
        source create form
    """
    required_css_class = 'required'

    short_name = forms.CharField(label=_('Source Short Name'), max_length=48, required=True,
      help_text=_('Short Name (e.g. ICD-10), Your new source will live at: https://OpenConceptLab.org/[OwnerType]/[Owner]/sources/<span id="source-name">[SourceName]</span>'))
    full_name = forms.CharField(label=_('Source Full Name'), max_length=48, required=True,
      help_text=_('Full Name (e.g. International Classification for Diseases v10)'))
    website = forms.URLField(label=_('Website'), required=False,
      help_text=_('Website (e.g. http://apps.who.int/classifications/icd10)'))
    source_type = forms.CharField(max_length=30, label=_('Source Type'), required=False)
    public_access = forms.ChoiceField(label=_('Public Access'), required=False, initial='View',
      choices=(('View', 'View (default)'), ('Edit', 'Edit'), ('None', 'None')))
    default_locale = forms.ChoiceField(choices=LOCALE_LIST, label=_('Locale'), required=True)
    supported_locales = forms.CharField(max_length=30, label=_('Supported Locales'), required=True)

    description = forms.CharField(max_length=80, label=_('Description'), required=False)

    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        source = self.initial['source']
        request = self.initial['request']
        api = OCLapi(request, debug=True)
        result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used.'))
        return concept_id


class SourceEditForm(SourceCreateForm):

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(SourceEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_name')


class SourceVersionAddForm(forms.Form):
    """
        TODO: Removed. Not used. Now json/angular.
        Add a source version form
    """
    required_css_class = 'required'

    id = forms.CharField(max_length=30, label=_('ID'), required=True)
    description = forms.CharField(max_length=80, label=_('Description'), required=False)
    released = forms.BooleanField(required=False, label=_('Released'))
