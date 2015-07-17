# -*- coding: utf-8 -*-
"""
    Forms for concepts.
"""
from django.utils.translation import ugettext as _
from django import forms
from django.forms.formsets import formset_factory

from libs.ocl import OCLapi
from apps.core.views import (_get_locale_list, _get_concept_class_list, _get_datatype_list)


class ConceptRetireForm(forms.Form):
    """
        Concept retirement form
    """
    required_css_class = 'required'

    comment = forms.CharField(
        label=_('Retire Reason'),
        required=False)


class ConceptNewForm(forms.Form):
    """
    Concept new form
    """
    # TODO(paynejd@gmail.com): Populate all dropdowns dynamically

    required_css_class = 'required'

    # TODO: Validate concept ID is unique
    concept_id = forms.CharField(
        label=_('Concept ID'),
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "e.g. A15.0"}))

    # TODO: Populate this dynamically
    concept_class = forms.ChoiceField(
        choices=[(v, v) for v in _get_concept_class_list()],
        label=_('Concept Class'),
        required=True)

    # TODO: Populate this dynamically
    datatype = forms.ChoiceField(
        choices=[(v, v) for v in _get_datatype_list()],
        label=_('Datatype'),
        initial='None',
        required=True)

    # TODO: Put locale, name, and name_type on the same row

    # TODO: Populate this dynamically
    locale = forms.ChoiceField(
        label=_('Name Locale'),
        required=True,
        choices=[(d['code'], d['name']) for d in _get_locale_list()])

    name = forms.CharField(
        label=_('Name'),
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "e.g. Tuberculosis of lung, confirmed by sputum microscopy with or without culture"}))

    # TODO: Populate this dynamically
    name_type = forms.CharField(
        label=_('Name Type'),
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "e.g. FULLY_SPECIFIED"}))

    # TODO: Put locale, description, and description_type on the same row

    description = forms.CharField(
        label=_('Description'),
        max_length=1024,
        required=False)
    description_type = forms.CharField(
        label=_('Description Type'),
        max_length=128,
        required=False)

    # TODO: The first name is always the preferred name
    #preferred_locale = forms.BooleanField(
    #    label=_('Preferred Locale'), required=False, initial=False)

    external_id = forms.CharField(
        label=_('Concept External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))



class ConceptCreateForm(forms.Form):
    """
        Concept create form
    """
    required_css_class = 'required'

    concept_id = forms.CharField(
        label=_('Concept ID'), 
        max_length=256, 
        required=True)
    concept_class = forms.CharField(
        label=_('Concept Class'), 
        required=True)
    datatype = forms.CharField(
        label=_('Datatype'), 
        required=False)
    name = forms.CharField(
        label=_('Name'),
        max_length=256,
        required=True)
    locale = forms.ChoiceField(
        label=_('Name Locale'), 
        choices=[(d['code'], d['name']) for d in _get_locale_list()], 
        required=True)
    preferred_locale = forms.BooleanField(
        label=_('Preferred Locale'), 
        required=False, 
        initial=False)

    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        source = self.initial['source']
        request = self.initial['request']
        api = OCLapi(request, debug=True)
        result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used in this source.'))
        return concept_id


class ConceptEditForm(ConceptCreateForm):
    """
        Concept edit form
    """
    update_comment = forms.CharField(max_length=90, label=_('Update Comment'), required=False)

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(ConceptEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('concept_id')
        self.fields.pop('name')
        self.fields.pop('locale')
        self.fields.pop('preferred_locale')


class ConceptNameForm(forms.Form):
    """
        Form for a single concept name.
    """
    required_css_class = 'required'

    name = forms.CharField(max_length=30, label=_('Name'), required=True)
    locale = forms.ChoiceField(
        choices=[(d['code'], d['name']) for d in _get_locale_list()], label=_('Locale'), required=True)
    preferred_locale = forms.BooleanField(label=_('Preferred Locale'), required=False, initial=False)
    name_type = forms.CharField(max_length=30, label=_('Name Datatype'), required=False)

ConceptNameFormSet = formset_factory(ConceptNameForm, extra=3)
