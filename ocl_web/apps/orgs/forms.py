from django.utils.translation import ugettext as _
from django import forms


class OrganizationNewForm(forms.Form):

    short_name = forms.CharField(
        label=_('Organization Short Name'),
        max_length="128",
        required=True,
        help_text='Your new organization will live at: ' +
                  'https://OpenConceptLab.org/orgs/<span id="org-name">[OrganizationName]',
        widget=forms.TextInput(attrs={'placeholder': "e.g. WHO"}))
    full_name = forms.CharField(
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

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. Django 1.6 lets you do this
            officially.
        """
        super(OrganizationEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_name')


class OrganizationMemberAddForm(forms.Form):

    member_username = forms.CharField(
        label="Member Username",
        max_length="128",
        widget=forms.TextInput(attrs={'placeholder': "Member Username"}))
