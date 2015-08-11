"""
Views for OCL Mappings.
"""
import logging

from django.http import Http404
from django.views.generic import TemplateView

#from django.utils.translation import ugettext as _
#from django.core.urlresolvers import reverse
#from django.http import HttpResponseRedirect
#from django.views.generic.edit import FormView
#from django.contrib import messages
#from django.core.paginator import Paginator
#from braces.views import JsonRequestResponseMixin

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

        # Load the source that contains this mapping
        # TODO(paynejd): Source is only loaded because of funky custom tags - REMOVE IN THE FUTURE
        # NOTE: Testing if "if_can_change" tag can accept a mapping
        source = self.get_source_details(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id)

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Details'
        context['mapping'] = mapping
        context['source'] = source

        return context



class MappingEditView(UserOrOrgMixin, MappingReadBaseView):
    """
    Mapping Edit view.
    """
    template_name = "mappings/mapping_edit.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the mapping details.
        """
        return



class MappingNewView(UserOrOrgMixin, MappingReadBaseView):
    """
    Mapping New view.
    """
    template_name = "mappings/mapping_new.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the mapping details.
        """
        return


class MappingRetireView(UserOrOrgMixin, MappingReadBaseView):
    """
    Mapping retire view
    """

    template_name = "mappings/mapping_retire.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the mapping details.
        """
        return
