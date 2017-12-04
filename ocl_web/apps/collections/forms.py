"""
Forms for collections.
"""
from django.utils.translation import ugettext as _
from django import forms

from libs.ocl import OclApi

from apps.core.views import _get_collection_type_list, _get_locale_list, _get_custom_validation_schema_list
from apps.core.fields import ComboBoxWidget, MultipleInputWidget


class CollectionCreateForm(forms.Form):
    """ collection create form """

    def __init__(self, *args, **kwargs):
        super(CollectionCreateForm, self).__init__(*args, **kwargs)
        # create widgets here to delay calls to api until initialization of the form
        self.fields['collection_type'].widget=ComboBoxWidget(data_list=[v for v in _get_collection_type_list()], name="collection_type_list")
        self.fields['default_locale'].widget=ComboBoxWidget(data_list=[[l['code'], l['name']] for l in _get_locale_list()], name="default_locale_list")
        self.fields['supported_locales'].widget=MultipleInputWidget(data_list=[l['name'] for l in _get_locale_list()], name="supported_locale_list")

    required_css_class = 'required'

    short_code = forms.CharField(
        label=_('Collection Short Code'),
        max_length=128,
        required=True,
        help_text=_('Allowed characters are : Alphabets(a-z,A-Z), Numbers(0-9) and Hyphen(-) <br/> '
                    'Your new collection will live at: https://www.openconceptlab.org'
                    '<span id="new_repository_base_url">[OwnerType]/[Owner]/collections/</span>'
                    '<span id="new_repository_id" style>[CollectionCode]</span>'),
        widget=forms.TextInput(attrs={'placeholder': "e.g. c80-practice-codes"}))

    name = forms.CharField(
        label=_('Collection Name'),
        max_length=128,
        required=True)

    full_name = forms.CharField(
        label=_('Collection Full Name'),
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. HL7 FHIR Practice Setting Code Value Set"}))

    website = forms.URLField(
        label=_('Website'),
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': "e.g. https://www.hl7.org/fhir/valueset-c80-practice-codes.html"}))

    collection_type = forms.CharField(
        label=_('Collection Type'),
        required=False,
        initial=_get_collection_type_list()[0],
        # widget defined in __init__
    )

    public_access = forms.ChoiceField(
        label=_('Public Access'),
        required=False,
        initial='View',
        choices=(('View', 'View (default)'), ('Edit', 'Edit'), ('None', 'None')))

    default_locale = forms.CharField(
        label=_('Default Locale'),
        required=True,
        # widget defined in __init__
    )

    supported_locales = forms.CharField(
        max_length=30,
        label=_('Supported Locales'),
        required=True,
        # widget defined in __init__
    )

    custom_validation_schema = forms.ChoiceField(
        label=('Custom Validation Schema'),
        choices=[(v,v) for v in _get_custom_validation_schema_list()],
        required=False
    )

    description = forms.CharField(
        max_length=512,
        label=_('Description'),
        required=False)

    external_id = forms.CharField(
        label=_('External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))

    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        collection = self.initial['collection']
        request = self.initial['request']
        api = OclApi(request, debug=True)
        result = api.get('orgs', collection['owner'], 'collections', collection['id'],
                         'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used.'))
        return concept_id


class CollectionDeleteForm(forms.Form):
    """ Form to delete a collection """
    required_css_class = 'required'


class CollectionEditForm(CollectionCreateForm):
    """ Form to edit collections """

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(CollectionEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_code')


class CollectionVersionAddForm(forms.Form):
    """ Form to add a collection version """

    required_css_class = 'required'
    id = forms.CharField(
        label=_('ID'),
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'width:480px;',
                   'placeholder': "Name this Collection version"}))

    description = forms.CharField(
        label=_('Description'),
        required=True,
        widget=forms.Textarea(attrs={'style': 'width:480px;',
                                     'rows': 5,
                                     'placeholder': 'Describe this Collection version'}))

    previous_version = forms.CharField(
        required=True,
        widget=forms.HiddenInput())

    version_external_id = forms.CharField(
        label=_('External ID'),
        required=False,
        widget=forms.TextInput(attrs={'style':'width:480px;',
                                      'placeholder': "e.g. UUID from external system"}))
    # released = forms.BooleanField(required=False, label=_('Released'))

class CollectionVersionsEditForm(CollectionVersionAddForm):
    """ Form to edit a collection version """
    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(CollectionVersionsEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('id')
        self.fields.pop('previous_version')

