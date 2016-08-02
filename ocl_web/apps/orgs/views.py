"""
OCL Organization Views
"""
#import requests
import logging

from django.shortcuts import redirect
from django.http import Http404
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
from braces.views import JsonRequestResponseMixin

from .forms import (OrganizationNewForm, OrganizationEditForm)
from .forms import (OrganizationMemberAddForm)
from libs.ocl import OclApi, OclSearch, OclConstants

logger = logging.getLogger('oclweb')



class OrganizationReadBaseView(TemplateView):
    """
    Base class for Organization Read views.
    """

    def get_org_details(self, org_id):
        """
        Get the org details
        """
        api = OclApi(self.request, debug=True)
        search_result = api.get('orgs', org_id)
        if search_result.status_code != 200:
            if search_result.status_code == 404:
                raise Http404
            else:
                search_result.raise_for_status()
        return search_result.json()

    def get_org_members(self, org_id):
        """
        Load members of this org
        """
        # TODO(paynejd@gmail.com): Access issue, error if user is not super user??
        members = []
        api = OclApi(self.request, debug=True)
        search_results = api.get('orgs', org_id, 'members')
        if search_results.status_code == 200:
            members = search_results.json()
        elif search_results.status_code != 404:
            # TODO(paynejd@gmail.com): Confirm whether to pass or raise an exception here
            #raise Exception(r.json())
            pass
        return members

    def get_org_sources(self, org_id, search_params=None):
        """
        Load org sources from the API and return OclSearch instance with results
        """
        # TODO(paynejd@gmail.com): Validate the input parameters

        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_SOURCES, params=search_params)
        api = OclApi(self.request, debug=True, facets=True)
        search_response = api.get('orgs', org_id, 'sources', params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type, search_response=search_response,
            search_params=self.request.GET)

        return searcher

    def get_org_collections(self, org_id, search_params=None):
        """
        Load org sources from the API and return OclSearch instance with results
        """
        # TODO(paynejd@gmail.com): Validate the input parameters

        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_COLLECTIONS, params=search_params)
        api = OclApi(self.request, debug=True, facets=True)
        search_response = api.get('orgs', org_id, 'collections', params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type, search_response=search_response,
            search_params=self.request.GET)

        return searcher


class OrganizationDetailsView(OrganizationReadBaseView):
    """ Organization details view. """

    template_name = "orgs/org_details.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the organization details and its members.
        """

        # Set the context
        context = super(OrganizationDetailsView, self).get_context_data(*args, **kwargs)

        # Load the organization
        org_id = self.kwargs.get('org')
        org = self.get_org_details(org_id)

        # Load members of this org
        members = self.get_org_members(org_id)

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Details'
        context['org'] = org
        context['members'] = members

        return context



class OrganizationSourcesView(OrganizationReadBaseView):
    """ Organization Sources view """

    template_name = "orgs/org_sources.html"

    def get_context_data(self, *args, **kwargs):
        """ Load sources search results, facets/filters, etc. for the org """

        context = super(OrganizationSourcesView, self).get_context_data(*args, **kwargs)

        # Load the organization
        org_id = self.kwargs.get('org')
        org = self.get_org_details(org_id)

        # Load the sources in this org, applying search parameters
        searcher = self.get_org_sources(org_id, search_params=self.request.GET)
        search_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_current_page = search_paginator.page(searcher.current_page)

        # Set the context for the sources
        context['selected_tab'] = 'Sources'
        context['org'] = org
        context['sources'] = searcher.search_results
        context['source_page'] = search_current_page
        context['source_pagination_url'] = self.request.get_full_path()
        context['source_q'] = searcher.get_query()
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_filters'] = searcher.search_filter_list
        context['search_type'] = searcher.search_type
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context

class OrganizationCollectionsView(OrganizationReadBaseView):
    """ Organization Sources view """

    template_name = "orgs/org_collections.html"

    def get_context_data(self, *args, **kwargs):
        """ Load sources search results, facets/filters, etc. for the org """

        context = super(OrganizationCollectionsView, self).get_context_data(*args, **kwargs)

        # Load the organization
        org_id = self.kwargs.get('org')
        org = self.get_org_details(org_id)

        # Load the sources in this org, applying search parameters
        searcher = self.get_org_collections(org_id, search_params=self.request.GET)
        search_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_current_page = search_paginator.page(searcher.current_page)

        # Set the context for the collections
        context['selected_tab'] = 'Collections'
        context['org'] = org
        context['collections'] = searcher.search_results
        context['collection_page'] = search_current_page
        context['collection_pagination_url'] = self.request.get_full_path()
        context['collection_q'] = searcher.get_query()
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_filters'] = searcher.search_filter_list
        context['search_type'] = searcher.search_type
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context



class OrganizationAboutView(OrganizationReadBaseView):
    """
    Organization about page.
    """

    template_name = "orgs/org_about.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the org details and about text.
        """
        context = super(OrganizationAboutView, self).get_context_data(*args, **kwargs)

        # Load the organization
        org_id = self.kwargs.get('org')
        org = self.get_org_details(org_id)

        # Set about text
        about = None
        if 'extras' in org and isinstance(org['extras'], dict) and 'about' in org['extras']:
            about = org['extras'].get('about')
        context['about'] = about

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'About'
        context['org'] = org
        context['about'] = about

        return context



class OrganizationNewView(LoginRequiredMixin, FormView):
    """
    View to create new organization
    """

    form_class = OrganizationNewForm
    template_name = "orgs/org_new.html"

    def form_valid(self, form, *args, **kwargs):
        """
        Submits the validated form data
        """

        api = OclApi(self.request, debug=True)

        # Prepare form data for submission, incl. renaming fields as necessary
        org_id = form.cleaned_data.pop('short_name')
        data = {
            'id': org_id,
        }
        data.update(form.cleaned_data)
        print form.cleaned_data
        print data
        result = api.create_org(data)

        # TODO:  Catch exceptions that will be raised by Ocl lib.
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Organization Added'))
            return redirect(reverse('org-details', kwargs={'org': org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationNewView, self).form_invalid(self, *args, **kwargs)



# TODO: Implement OrganizationRetireView
class OrganizationRetireView(FormView):
    """
    View to retire organization
    """
    template_name = 'orgs/org_retire.html'



class OrganizationEditView(FormView):
    """
    View to edit organization
    """

    template_name = 'orgs/org_edit.html'

    def get_form_class(self):
        """ Trick to do some initial lookup """
        self.org_id = self.kwargs.get('org')
        api = OclApi(self.request, debug=True)
        self.org = api.get('orgs', self.org_id).json()
        return OrganizationEditForm

    def get_context_data(self, *args, **kwargs):
        """
        Returns the context data for the view
        """
        context = super(OrganizationEditView, self).get_context_data(*args, **kwargs)
        context['org'] = self.org
        return context

    def get_initial(self):
        return self.org

    def form_valid(self, form, *args, **kwargs):
        """
        Validates the form data and submits if valid
        """

        api = OclApi(self.request, debug=True)

        data = {}
        data.update(form.cleaned_data)
        result = api.update_org(self.org_id, data)
        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Organization updated.'))
            return redirect(reverse('org-details', kwargs={'org': self.org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationEditView, self).form_invalid(form)



# TODO(paynejd): OrganizationMemberAddView only half works -- fix this
class OrganizationMemberAddView(LoginRequiredMixin, FormView):
    """
    View to add member to organization
    """

    form_class = OrganizationMemberAddForm
    template_name = "orgs/org_member_add.html"

    def get_org(self):
        """
        Load the organization
        """
        self.org_id = self.kwargs.get('org')
        api = OclApi(self.request, debug=True)
        self.org = api.get('orgs', self.org_id).json()

    def get_initial(self):
        """ Trick to do some initial lookup """
        self.get_org()
        data = super(OrganizationMemberAddView, self).get_initial()
        return data

    def get_context_data(self, *args, **kwargs):
        """
        Returns context data for the view
        """
        context = super(OrganizationMemberAddView, self).get_context_data(*args, **kwargs)
        context['org'] = self.org
        return context

    def form_valid(self, form, *args, **kwargs):
        """
        Validates the form data and submits if valid
        """
        print args
        print kwargs
        self.get_org()
        new_username = form.cleaned_data.pop('member_username')

        api = OclApi(self.request, debug=True)

        result = api.put('orgs', self.org['id'], 'members', new_username)

        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.status_code == 204:
            messages.add_message(self.request, messages.INFO, _('Member Added'))
            return redirect(reverse('org-details', kwargs={'org': self.org['id']}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationMemberAddView, self).form_invalid(form)



# TODO(paynejd): OrganizationMemberRemoveView only half works -- fix this
class OrganizationMemberRemoveView(LoginRequiredMixin,
                                   JsonRequestResponseMixin, View):
    """
    View to remove member from organization
    """

    def post(self, *args, **kwargs):
        """Posts member removal request to API"""
        self.org_id = self.kwargs.get('org')
        self.username = self.kwargs.get('username')

        api = OclApi(self.request, debug=True)
        result = api.delete('orgs', self.org_id, 'members', self.username)

        return self.render_json_response({'message':'Member removed'})

        # TODO(paynejd@gmail.com): Retire unreachable code?
        #if result.status_code == 204:
        #    return self.render_json_response({'message':'Member removed'})
        #else:
        #    return self.render_bad_request_response({'message': result.status_code})
