"""
Organization forms
"""
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from django import forms


class OrganizationNewForm(forms.Form):
    """
    Form to create a new organization
    """
    required_css_class = 'required'

    short_name = forms.CharField(
        label=_('Organization Short Name'),
        max_length=128,
        required=True,
        error_messages={'required': 'Please enter your name'},
        help_text=('Allowed characters are : Alphabets(a-z,A-Z), Numbers(0-9) and Hyphen(-) <br/>Your new organization will live at: '
                   'https://OpenConceptLab.com/orgs/'
                   '<span id="new_org_id" style="font-weight:bold;">[org-id]</span>/'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. WHO"}))
    name = forms.CharField(
        label=_('Organization Full Name'),
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "e.g. World Health Organization"}))
    website = forms.URLField(
        label=_('Website'),
        required=False,
        widget=forms.URLInput(attrs={'placeholder': "e.g. http://www.who.int/"}))
    company = forms.CharField(
        label=_('Company Name'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. World Health Organization"}))
    location = forms.CharField(
        label=_('Location'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. Geneva, Switzerland"}))


class OrganizationEditForm(OrganizationNewForm):
    """
    Form to edit an organization
    """

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. Django 1.6 lets you do this
            officially.
        """
        super(OrganizationEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_name')


class OrganizationMemberAddForm(forms.Form):
    """
    Form to add a member to an organization
    """
    required_css_class = 'required'

    member_username = forms.CharField(
        label="Member Username",
        max_length="128",
        widget=forms.TextInput(attrs={'placeholder': "Member Username"}))
