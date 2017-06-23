# -*- coding: utf-8 -*-
"""
Forms for concepts.

# Preserving this method here as it may be useful later!
def clean_concept_id(self):
    #concept ID must be unique
    concept_id = self.cleaned_data['concept_id']
    source = self.initial['source']
    request = self.initial['request']
    api = OclApi(request, debug=True)
    result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
    if result.status_code == 200:
        raise forms.ValidationError(_('This Concept ID is already used in this source.'))
    return concept_id

"""
from django.utils.translation import ugettext as _
from django import forms
from django.forms.formsets import formset_factory

#from libs.ocl import OclApi
from apps.core.views import (_get_locale_list, _get_concept_class_list, _get_org_or_user_sources_list,
                             _get_datatype_list, _get_name_type_list, _get_description_type_list)
from libs.ocl import OclApi


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
        help_text=_('Enter the type of relationship between the concepts'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. SAME-AS, NARROWER-THAN, BROADER-THAN"}))

    is_internal_or_external = forms.ChoiceField(
        choices=[('Internal', 'Internal'), ('External', 'External')],
        label=_('Mapping Target'),
        required=True,
        widget=forms.RadioSelect(attrs={'class':'radio-inline'}))

    internal_to_concept_url = forms.CharField(
        label=_('To Concept URL'),
        required=False,
        help_text=_('Copy/paste the relative URL of a concept '
                    'stored in OCL to which this mapping points'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. /orgs/CIEL/sources/CIEL/concepts/32/"}))

    external_to_source_url = forms.CharField(
        label=_('To Source URL'),
        required=False,
        help_text=_('Copy/paste the relative URL of a source in '
                    'OCL with source type "External"'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. /orgs/IHTSDO/sources/SNOMED-CT/"}))

    external_to_concept_code = forms.CharField(
        label=_('To Concept Code'),
        required=False,
        help_text=_('Enter the name of the external concept code'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. A15.1"}))

    external_to_concept_name = forms.CharField(
        label=_('To Concept Name'),
        required=False,
        help_text=_('Enter the name of the external concept name'),
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. Tuberculosis of lung, confirmed by culture only"}))

    external_id = forms.CharField(
        label=_('Mapping External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))


class  ConceptNewForm(forms.Form):
    """
    Concept new form
    """

    def __init__(self, *args, **kwargs):
        super(ConceptNewForm, self).__init__(*args, **kwargs)

        self.fields['concept_class'].choices = [(cl, cl) for cl in _get_concept_class_list()]
        self.fields['datatype'].choices = [(d, d) for d in _get_datatype_list()]

    required_css_class = 'required'

    # TODO: Validate concept ID is unique
    concept_id = forms.CharField(
        label=_('Concept ID'),
        max_length=256,
        required=True,
        help_text=_('<small>Alphanumeric characters, hyphens and periods are allowed.<br/>'
                    'Your new concept will live at: '
                    '<span id="new_concept_base_url">/[owner-type]/[owner]/sources/'
                    '[source]/concepts/</span>'
                    '<span id="new_concept_id" style="font-weight:bold;">'
                    '[concept-id]</span>/</small>'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. A15.0"}))

    concept_class = forms.ChoiceField(
        choices=[],
        label=_('Concept Class'),
        required=True)

    datatype = forms.ChoiceField(
        choices=[],
        label=_('Datatype'),
        initial='None',
        required=True)

    external_id = forms.CharField(
        label=_('Concept External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))


class ConceptForkForm(forms.Form):
    original_concept_id = None

    def __init__(self, *args, **kwargs):
        super(ConceptForkForm, self).__init__(*args, **kwargs)
        self.fields['concept_id'].widget.attrs['placeholder'] = kwargs['initial']['original_concept_id']
        self.fields['sources'].choices = [(s, s['id']) for s in _get_org_or_user_sources_list(**kwargs)]

    # TODO: Validate concept ID is unique
    concept_id = forms.CharField(
        label=_('Concept ID'),
        max_length=256,
        required=True,
        help_text=_('<small>Alphanumeric characters, hyphens and periods are allowed.<br/>'
                    'Your fork concept will live at: '
                    '<span id="new_concept_base_url">/[owner-type]/[owner]/sources/'
                    '[source]/concepts/</span>'
                    '<span id="new_concept_id" style="font-weight:bold;">'
                    '[concept-id]</span>/</small>'),
        widget=forms.TextInput(attrs={'placeholder': original_concept_id}))

    sources = forms.ChoiceField(
        choices=[],
        label=_('source'),
        required=True
    )
    Fork_Mappings = forms.BooleanField(
        label=_('Fork mappings'),
        required=False
    )


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


# TODO: Resurrect ConceptNameForm
class ConceptNameForm(forms.Form):
    """
        Form for a single concept name.
    """

    def __init__(self, *args, **kwargs):
        super(ConceptNameForm, self).__init__(*args, **kwargs)
        self.fields['locale'].choices = [(l['code'], l['name']) for l in _get_locale_list()]

    required_css_class = 'required'

    name = forms.CharField(max_length=30, label=_('Name'), required=True)
    locale = forms.ChoiceField(
        choices=[],
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
