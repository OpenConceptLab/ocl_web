# -*- coding: utf-8 -*-
"""
Forms for concepts.

# Preserving this method here as it may be useful later!
def clean_concept_id(self):
    #concept ID must be unique
    concept_id = self.cleaned_data['concept_id']
    source = self.initial['source']
    request = self.initial['request']
    api = OCLapi(request, debug=True)
    result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
    if result.status_code == 200:
        raise forms.ValidationError(_('This Concept ID is already used in this source.'))
    return concept_id

"""
from django.utils.translation import ugettext as _
from django import forms
from django.forms.formsets import formset_factory

#from libs.ocl import OCLapi
from apps.core.views import (_get_locale_list, _get_concept_class_list, _get_datatype_list)


class ConceptRetireForm(forms.Form):
    """
    Concept retirement form
    """
    required_css_class = 'required'

    comment = forms.CharField(
        label=_('Retire Reason'),
        required=True,
        widget=forms.Textarea(attrs={'rows':5,
                                     'placeholder':'Note the reason for retiring the concept'}))



class ConceptNewMappingForm(forms.Form):
    """
    New concept mapping form -- from_mapping is already set
    """
    required_css_class = 'required'

    map_type = forms.CharField(
        label=_('Map Type'),
        required=True,
        help_text=_('<small>Enter the type of relationship between the concepts</small>'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. SAME-AS, NARROWER-THAN, BROADER-THAN"}))

    is_internal_or_external = forms.ChoiceField(
        choices=['Internal', 'External'],
        label=_('To Concept Type'),
        required=True,
        widget=forms.RadioSelect())

    internal_to_concept_url = forms.CharField(
        label=_('To Concept Url'),
        required=False,
        help_text=_('<small>Copy/paste the URL of a concept stored in OCL</small>'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. /orgs/CIEL/sources/CIEL/concepts/32/"}))

    external_source_url = forms.CharField(
        label=_('To Source Url'),
        required=False,
        help_text=_('<small>Copy/paste the URL of a source in '
                    'OCL with source type "External"</small>'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. /orgs/IHTSDO/sources/SNOMED-CT/"}))

    external_concept_code = forms.CharField(
        label=_('To Concept Code'),
        required=False,
        help_text=_('<small>Enter the name of the external concept code</small>'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. A15.1"}))

    external_concept_name = forms.CharField(
        label=_('To Concept Code'),
        required=False,
        help_text=_('<small>Enter the name of the external concept name</small>'),
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. Tuberculosis of lung, confirmed by culture only"}))

    external_id = forms.CharField(
        label=_('Mapping External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))



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
        help_text=_('<small>Your new concept will live at: http://www.openconceptlab.com'
                    '<span id="new_concept_base_url">/[owner-type]/[owner]/sources/'
                    '[source]/concepts/</span>'
                    '<span id="new_concept_id" style="font-weight:bold;">'
                    '[concept-id]</span>/</small>'),
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
        help_text=_('<small>Choose the locale for the initial name and description</small>'),
        choices=[(d['code'], d['name']) for d in _get_locale_list()])

    name = forms.CharField(
        label=_('Name'),
        max_length=256,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. Tuberculosis of lung, confirmed by sputum microscopy with or without culture"}))

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

    # TODO: Populate this dynamically
    description_type = forms.CharField(
        label=_('Description Type'),
        max_length=128,
        required=False)

    external_id = forms.CharField(
        label=_('Concept External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))



class ConceptEditForm(ConceptNewForm):
    """
    Concept edit form
    """

    update_comment = forms.CharField(
        label=_('Update Comment'),
        required=True,
        widget=forms.Textarea(attrs={'rows':5,
                                     'placeholder':'Note the reason for editing the concept'}))

    def __init__(self, *args, **kwargs):
        """
        Dirty trick to delete one field for edit form. django 1.6 lets you do this officially.
        """
        super(ConceptEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('concept_id')
        self.fields.pop('locale')
        self.fields.pop('name')
        self.fields.pop('name_type')
        self.fields.pop('description')
        self.fields.pop('description_type')



# TODO: Resurrect ConceptNameForm
class ConceptNameForm(forms.Form):
    """
        Form for a single concept name.
    """
    required_css_class = 'required'

    name = forms.CharField(max_length=30, label=_('Name'), required=True)
    locale = forms.ChoiceField(
        choices=[(d['code'], d['name']) for d in _get_locale_list()],
        label=_('Locale'),
        required=True)

    preferred_locale = forms.BooleanField(
        label=_('Preferred Locale'),
        required=False,
        initial=False)
    name_type = forms.CharField(
        max_length=30,
        label=_('Name Datatype'),
        required=False)

ConceptNameFormSet = formset_factory(ConceptNameForm, extra=3)
