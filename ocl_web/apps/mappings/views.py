"""
Views for OCL Mappings.
"""
#import requests
import logging

from django.shortcuts import redirect
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
import json

from .forms import (MappingNewForm, MappingEditForm, MappingRetireForm)
from braces.views import LoginRequiredMixin
from libs.ocl import OCLapi
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')



class MappingReadBaseView(TemplateView):
    """
    Base class for Mapping Read views.
    """

    def get_source_details(self, owner_type, owner_id, source_id, source_version_id=None):
        """
        Load source details from the API and return as dictionary.
        """
        # NOTE: This is not used by mappings view - remove?
        # TODO(paynejd@gmail.com): Load details from source version, if applicable (or remove?)
        # TODO(paynejd@gmail.com): Validate the input parameters
        api = OCLapi(self.request, debug=True)
        search_response = api.get(owner_type, owner_id, 'sources', source_id)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()
        return search_response.json()


    def get_mapping_details(self, owner_type, owner_id, source_id, mapping_id):
        """
        Load mapping details from the API and return as dictionary.
        """
        # TODO(paynejd@gmail.com): Validate the input parameters
        api = OCLapi(self.request, debug=True)
        search_response = api.get(
            owner_type, owner_id, 'sources', source_id, 'mappings', mapping_id)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()
        return search_response.json()



class MappingFormBaseView(FormView):
    """
    Base class for Mapping Form views.
    """

    def get_initial(self):
        """ Set the owner and source args for use in the form """

        data = super(MappingFormBaseView, self).get_initial()

        # Set owner type and identifiers using UserOrOrgMixin.get_args()
        self.get_args()
        data.update({
            'request': self.request,
            'from_user': self.from_user,
            'from_org': self.from_org,
            'user_id': self.user_id,
            'org_id': self.org_id,
            'owner_type': self.owner_type,
            'owner_id': self.owner_id,
            'source_id': self.source_id
        })
        return data



class MappingDetailsView(UserOrOrgMixin, MappingReadBaseView):
    """
    Mapping Details view.
    """
    template_name = "mappings/mapping_details.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the mapping details.
        """

        # Setup the context and args
        context = super(MappingDetailsView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the mapping details
        mapping = self.get_mapping_details(
            self.owner_type, self.owner_id, self.source_id, self.mapping_id)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Details'
        context['mapping'] = mapping

        return context



class MappingEditView(LoginRequiredMixin, UserOrOrgMixin, MappingFormBaseView):
    """
    Mapping Edit view.
    """
    #form_class = MappingEditForm
    template_name = "mappings/mapping_edit.html"

    def get_form_class(self):
        """
        A sneaky way to hook into the generic form processing view, to grep args
        from the URL, retrieve some application data and store them in the view.
        """
        self.get_args()
        self.source_id = self.kwargs.get('source')
        self.mapping_id = self.kwargs.get('mapping')

        api = OCLapi(self.request, debug=True)

        self.source = api.get(
            self.owner_type, self.org_id, 'sources', self.source_id).json()
        self.mapping = api.get(
            self.owner_type, self.org_id, 'sources', self.source_id,
            'mappings', self.mapping_id).json()

        return MappingEditForm


    def get_initial(self):
        """ Set the owner and source args for use in the form """
        data = super(MappingEditView, self).get_initial()
        data['source'] = self.source
        data['mapping'] = self.mapping
        data.update(self.mapping)
        return data


    def get_context_data(self, *args, **kwargs):
        """ Loads the mapping details. """

        # Setup the form context
        context = super(MappingEditView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # TODO: Load list of map types

        # Set the context
        context['kwargs'] = self.kwargs
        context['source'] = self.source
        context['mapping'] = self.mapping

        return context



class MappingNewView(LoginRequiredMixin, UserOrOrgMixin, MappingFormBaseView):
    """
    Mapping New view.
    """
    form_class = MappingNewForm
    template_name = "mappings/mapping_new.html"

    def get_context_data(self, *args, **kwargs):
        """ Loads the mapping details. """

        # Setup the form context
        context = super(MappingNewView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source that the new mapping will belong to
        api = OCLapi(self.request, debug=True)
        source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()

        # TODO: Load list of map types

        # Set the context
        context['kwargs'] = self.kwargs
        context['source'] = source

        return context


    def form_valid(self, form, *args, **kwargs):
        """ Submits the validated form data using the API: new mapping """

        # Prepare the data form submission, incl. renaming fields as needed
        mapping_destination = form.cleaned_data.get('is_internal_or_external')
        base_data = {
            'from_concept_url': form.cleaned_data.get('from_concept_url'),
            'map_type': form.cleaned_data.get('map_type', ''),
            'external_id': form.cleaned_data.get('external_id', '')
        }
        if mapping_destination == 'Internal':
            base_data['to_concept_url'] = form.cleaned_data.get('internal_to_concept_url')
        elif mapping_destination == 'External':
            base_data['to_source_url'] = form.cleaned_data.get('external_to_source_url')
            base_data['to_concept_code'] = form.cleaned_data.get('external_to_concept_code')
            base_data['to_concept_name'] = form.cleaned_data.get('external_to_concept_name')

        # Create the mapping
        api = OCLapi(self.request, debug=True)
        result = api.create_mapping(self.owner_type, self.owner_id, self.source_id, base_data)
        if result.ok:
            new_mapping_id = result.json()['id']
            messages.add_message(self.request, messages.INFO, _('Mapping created.'))
            if self.from_org:
                return redirect(reverse('mapping-home',
                                        kwargs={'org': self.owner_id,
                                                'source': self.source_id,
                                                'mapping': new_mapping_id}))
            else:
                return redirect(reverse('mapping-home',
                                        kwargs={'user': self.owner_id,
                                                'source': self.source_id,
                                                'mapping': new_mapping_id}))
        else:
            messages.add_message(
                self.request, messages.ERROR,
                _('Error: ' + result.content + '<br />POST data: ' + json.dumps(base_data)))
            logger.warning('Mapping create POST failed: %s' % result.content)
            return super(MappingNewView, self).form_invalid(form)



class MappingRetireView(LoginRequiredMixin, UserOrOrgMixin, MappingFormBaseView):
    """
    Mapping retire view
    """
    form_class = MappingRetireForm
    template_name = "mappings/mapping_retire.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the mapping details.
        """
        return
