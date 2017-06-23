# -*- coding: utf-8 -*-
"""
Forms for mappings.
"""
from django.utils.translation import ugettext as _
from django import forms

from apps.core.views import _get_org_or_user_sources_list


class MappingRetireForm(forms.Form):
    """
    Mapping retirement form
    """
    required_css_class = 'required'

    comment = forms.CharField(
        label=_('Retire Reason'),
        required=True,
        widget=forms.Textarea(attrs={'rows':5,
                                     'placeholder':'Note the reason for retiring the mapping'}))



class MappingNewForm(forms.Form):
    """
    New mapping form - owner source is already set
    """
    required_css_class = 'required'

    # TODO(paynejd@gmail.com): Use dynamic resource selector for from_concept
    from_concept_url = forms.CharField(
        label=_('From Concept URL'),
        required=True,
        help_text=_('Copy/paste the relative URL of the concept in '
                    'OCL from which this mapping originates'),
        widget=forms.TextInput(
            attrs={'placeholder':"e.g. /orgs/MyOrg/sources/MySource/concepts/1234/"}))

    # TODO: Populate map_type dynamically
    map_type = forms.CharField(
        label=_('Map Type'),
        required=True,
        help_text=_('Enter the type of relationship between the concepts'),
        widget=forms.TextInput(attrs={'placeholder':"e.g. SAME-AS, NARROWER-THAN, BROADER-THAN"}))

    external_id = forms.CharField(
        label=_('Mapping External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))

    is_internal_or_external = forms.ChoiceField(
        choices=[('Internal', 'Internal'), ('External', 'External')],
        label=_('Mapping Target'),
        required=True,
        widget=forms.RadioSelect(attrs={'class':'radio-inline'}))

    # TODO(paynejd@gmail.com): Use dynamic resource selector for to_concept
    internal_to_concept_url = forms.CharField(
        label=_('To Concept URL'),
        required=False,
        help_text=_('Copy/paste the relative URL of a concept '
                    'stored in OCL to which this mapping points'),
        widget=forms.TextInput(attrs={'placeholder':"e.g. /orgs/CIEL/sources/CIEL/concepts/32/"}))

    # TODO(paynejd@gmail.com): Use dynamic resource selector for to_source
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


class MappingForkForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MappingForkForm, self).__init__(*args, **kwargs)
        print 'MappingForkForm args:   ', args
        print 'MappingForkForm kwargs: ', kwargs
        self.fields['sources'].choices = [(s, s['id']) for s in _get_org_or_user_sources_list(**kwargs)]

    sources = forms.ChoiceField(
        choices=[],
        label=_('source'),
        required=True
    )


class MappingEditForm(MappingNewForm):
    """
    Mapping edit form
    """
    update_comment = forms.CharField(
        label=_('Update Comment'),
        required=True,
        widget=forms.Textarea(attrs={'rows': 5,
                                     'placeholder': 'Note the reason for editing the mapping'}))

    def __init__(self, *args, **kwargs):
        """
        Dirty trick to delete one field for edit form. django 1.6 lets you do this officially.
        """
        super(MappingEditForm, self).__init__(*args, **kwargs)
        # TODO: Remove any fields during edit?
        #self.fields.pop('from_concept_url')
