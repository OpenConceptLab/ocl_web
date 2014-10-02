import floppyforms

from django.utils.translation import ugettext as _
from django import forms


class OrganizationCreateForm(forms.Form):

    short_name = forms.CharField(
        label="Organization Short Name",
        max_length="48",
        help_text='Your organization will live at: ' +
                  'https://OpenConceptLab.org/orgs/<span id="org-name">[OrganizationName]',
        widget=forms.TextInput(attrs={'placeholder': "Short Name (e.g. WHO)"}))
    name = forms.CharField(
        label="Organization Full Name",
        max_length="48",
        widget=forms.TextInput(attrs={'placeholder': "Full Name (e.g. World Health Organization)"}))
    website = forms.URLField(
        label="Website",
        required=False,
        widget=forms.URLInput(attrs={'placeholder': "Website (e.g. http://www.who.int)"}))
    company = forms.CharField(
        label="Company Name",
        max_length="48",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Company name"}))
    location = forms.CharField(
        label=_('Location'),
        max_length="48",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "location"}))


class OrganizationEditForm(OrganizationCreateForm):

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(OrganizationEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_name')


class OrganizationCreateFormOldFormNotUsed(floppyforms.Form):

    short_name = floppyforms.CharField(
        label="Organization Short Name",
        max_length="48",
        widget=floppyforms.TextInput(
            attrs={'id': 'orgShortName',
                   'placeholder': "Short Name (e.g. WHO)",
                   'class': 'form-control'}))

    full_name = floppyforms.CharField(
        label="Organization Full Name",
        max_length="48",
        widget=floppyforms.TextInput(
            attrs={'id': 'orgFullName',
                   'placeholder': "Full Name (e.g. World Health Organization)",
                   'class': 'form-control'}))

    website = floppyforms.URLField(
        label="Website",
        required=False,
        widget=floppyforms.URLInput(
            attrs={'id': 'orgWebsite',
                   'placeholder': "Website (e.g. http://www.who.int)",
                   'class': 'form-control'}))

    @classmethod
    def submit(cls, data, *args, **kwargs):

        # utils.ocl_requests.post()
        # if not request.ok:
        # raise a Validation Error
        # else:
        # return True
        pass
