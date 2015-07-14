"""
OCL Organization Views
"""
import requests
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
from libs.ocl import OCLapi, OCLSearch

logger = logging.getLogger('oclweb')



class OrganizationReadBaseView(TemplateView):
    """
    Base class for Organization Read views.
    """

    def get_org_details(self, org_id):
        """
        Get the org details
        """
        api_org = OCLapi(self.request, debug=True)
        search_result_org = api_org.get('orgs', org_id)
        if search_result_org.status_code != 200:
            if search_result_org.status_code == 404:
                raise Http404
            else:
                search_result_org.raise_for_status()
        return search_result_org.json()

    def get_org_members(self, org_id):
        """
        Load members of this org
        """
        # TODO: Access issue, error if user is not super user??
        members = []
        api_members = OCLapi(self.request, debug=True)
        members_search_results = api_members.get('orgs', org_id, 'members')
        if members_search_results.status_code == 200:
            members = members_search_results.json()
        elif members_search_results.status_code != 404:
            #raise Exception(r.json())
            pass
        return members


# class OrganizationDetailView(OrganizationReadBaseView):
#     """
#     Organization details and source search view.
#     """

#     template_name = "orgs/org_detail.html"

#     def get_context_data(self, *args, **kwargs):
#         """Gets the org, then the sources of that org, and then the
#         concepts from each of those sources.
#         """

#         context = super(OrganizationDetailView, self).get_context_data(*args, **kwargs)
#         context['url_params'] = self.request.GET
#         context['selected_tab'] = 'Details'

#         # Determine the organization ID
#         # TODO: Make the org object self-aware like the source context (e.g. self.org_id)
#         org_id = self.kwargs.get('org')

#         # Prepare to search the sources in this org
#         # NOTE: Both are searched no matter what, but only one accepts search
#         # criteria/filters at a time
#         res_type = self.request.GET.get('resource_type')
#         print 'INPUT PARAMS %s: %s' % (self.request.method, self.request.GET)
#         print res_type
#         source_searcher = OCLSearch(
#             search_type=OCLSearch.SOURCE_TYPE, params=self.request.GET)

#         # Load the organization
#         org = self.get_org_details(org_id)
#         context['org'] = org

#         # Set about text for the organization
#         # TODO: Create a generic method for getting at extras
#         if 'extras' in org and isinstance(org['extras'], dict):
#             about = org['extras'].get('about', 'No about entry.')
#         else:
#             # TODO: If user has editing privileges, prompt them to create about entry
#             about = 'No about entry.'
#         context['about'] = about

#         # Load members of this org
#         members = self.get_org_members(org_id)
#         context['members'] = members

#         # Load the sources in this organization
#         api_sources = OCLapi(self.request, debug=True, facets=True)
#         search_result_sources = api_sources.get(
#             'orgs', org_id, 'sources', params=source_searcher.search_params)
#         if search_result_sources.status_code == requests.codes.not_found:
#             sources_response_json = {}
#             sources_facets_json = {}
#             sources_facets = {}
#             sources = []
#             sources_num_found = 0
#             sources_paginator = None
#             sources_current_page = 0
#         else:
#             sources_response_json = search_result_sources.json()
#             sources_facets_json = sources_response_json['facets']
#             sources_facets = source_searcher.process_facets('sources', sources_facets_json)
#             sources = sources_response_json['results']
#             if 'num_found' in search_result_sources.headers:
#                 try:
#                     sources_num_found = int(search_result_sources.headers['num_found'])
#                 except ValueError:
#                     sources_num_found = 0
#             else:
#                 sources_num_found = 0
#             sources_paginator = Paginator(range(sources_num_found), source_searcher.num_per_page)
#             sources_current_page = sources_paginator.page(source_searcher.current_page)

#         # TODO: Setup source filters based on the current search

#         # Select filters
#         # TODO: This is passing all parameters, but should pass only those relevant to sources
#         source_searcher.select_search_filters(self.request.GET)

#         # Set the context for the child sources
#         context['sources'] = sources
#         context['source_page'] = sources_current_page
#         context['source_pagination_url'] = self.request.get_full_path()
#         context['source_q'] = source_searcher.get_query()
#         context['source_facets'] = sources_facets

#         # Set debug context for sources
#         context['sources_request_url'] = api_sources.url
#         context['sources_search_params'] = source_searcher.search_params
#         context['sources_search_response_headers'] = search_result_sources.headers
#         context['sources_search_facets_json'] = sources_facets_json

#         # TODO: Sort is not setup correctly to work with both sources and collections
#         context['search_sort_options'] = source_searcher.get_sort_options()
#         context['search_sort'] = source_searcher.get_sort()

#         return context


class OrganizationDetailsView(OrganizationReadBaseView):
    """
    Organization details view.
    """

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
    """
    Organization Sources view
    """

    template_name = "orgs/org_sources.html"

    def get_context_data(self, *args, **kwargs):
        """
        Load sources search results, facets/filters, etc. for the org
        """
        context = super(OrganizationSourcesView, self).get_context_data(*args, **kwargs)

        # Load the organization
        org_id = self.kwargs.get('org')
        org = self.get_org_details(org_id)

        # Load the sources in this organization
        source_searcher = OCLSearch(
            search_type=OCLSearch.SOURCE_TYPE, params=self.request.GET)
        api_sources = OCLapi(self.request, debug=True, facets=True)
        search_result_sources = api_sources.get(
            'orgs', org_id, 'sources', params=source_searcher.search_params)
        if search_result_sources.status_code == requests.codes.not_found:
            sources_response_json = {}
            sources_facets_json = {}
            sources_facets = {}
            sources = []
            sources_num_found = 0
            sources_paginator = None
            sources_current_page = 0
        else:
            sources_response_json = search_result_sources.json()
            sources_facets_json = sources_response_json['facets']
            sources_facets = source_searcher.process_facets('sources', sources_facets_json)
            sources = sources_response_json['results']
            if 'num_found' in search_result_sources.headers:
                try:
                    sources_num_found = int(search_result_sources.headers['num_found'])
                except ValueError:
                    sources_num_found = 0
            else:
                sources_num_found = 0
            sources_paginator = Paginator(range(sources_num_found), source_searcher.num_per_page)
            sources_current_page = sources_paginator.page(source_searcher.current_page)

        # TODO: Setup source filters based on the current search

        # Select filters
        # TODO: This is passing all parameters, but should pass only those relevant to sources
        source_searcher.select_search_filters(self.request.GET)

        # Set the context for the sources
        context['sources'] = sources
        context['source_page'] = sources_current_page
        context['source_pagination_url'] = self.request.get_full_path()
        context['source_q'] = source_searcher.get_query()
        context['source_facets'] = sources_facets
        context['search_sort_options'] = source_searcher.get_sort_options()
        context['search_sort'] = source_searcher.get_sort()

        # Set debug context
        context['url_params'] = self.request.GET
        context['sources_request_url'] = api_sources.url
        context['sources_search_params'] = source_searcher.search_params
        context['sources_search_response_headers'] = search_result_sources.headers
        context['sources_search_facets_json'] = sources_facets_json

        # Set the context for the org and template
        context['selected_tab'] = 'Sources'
        context['org'] = org

        return context


class OrganizationCollectionsView(OrganizationReadBaseView):
    """
    Organization Collections List view
    """

    template_name = "orgs/org_collections.html"

    def get_context_data(self, *args, **kwargs):
        """
        Load collection search results, facets/filters, etc. for the org
        """
        context = super(OrganizationCollectionsView, self).get_context_data(*args, **kwargs)

        # TODO(paynejd@gmail.com): Implement collections view

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Collections'
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

        # Set about text for the organization
        if 'extras' in org and isinstance(org['extras'], dict):
            about = org['extras'].get('about', 'No about entry.')
        else:
            # TODO: If user has editing privileges, prompt them to create about entry
            about = 'No about entry.'

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'About'
        context['org'] = org
        context['about'] = about

        return context



class OrganizationNewView(LoginRequiredMixin, FormView):
    """View to create new organization"""

    form_class = OrganizationNewForm
    template_name = "orgs/org_new.html"

    def form_valid(self, form, *args, **kwargs):
        """
        Validates the form data and submits if valid
        """
        # TODO(paynejd@gmail.com): Rename this method - it validates and submits form

        org_id = form.cleaned_data.pop('short_name')

        api = OCLapi(self.request, debug=True)

        data = {
            'id': org_id,
        }
        data.update(form.cleaned_data)
        print form.cleaned_data
        print data
        result = api.create_org(data)

        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Organization Added'))
            return redirect(reverse('org-details', kwargs={'org': org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationCreateView, self).form_invalid(self, *args, **kwargs)



class OrganizationEditView(FormView):
    """
    View to edit organization
    """

    template_name = 'orgs/org_edit.html'

    def get_form_class(self):
        """ Trick to do some initial lookup """
        self.org_id = self.kwargs.get('org')
        api = OCLapi(self.request, debug=True)
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
        # TODO(paynejd@gmail.com): Rename this method - it validates and submits form

        api = OCLapi(self.request, debug=True)

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
        api = OCLapi(self.request, debug=True)
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
        # TODO(paynejd@gmail.com): Rename this method - it validates and submits form

        print args
        print kwargs
        self.get_org()
        new_username = form.cleaned_data.pop('member_username')

        api = OCLapi(self.request, debug=True)

        result = api.put('orgs', self.org['id'], 'members', new_username)

        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.status_code == 204:
            messages.add_message(self.request, messages.INFO, _('Member Added'))
            return redirect(reverse('org-details', kwargs={'org': self.org['id']}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationMemberAddView, self).form_invalid(form)


class OrganizationMemberRemoveView(LoginRequiredMixin,
                                   JsonRequestResponseMixin, View):
    """
    View to remove member from organization
    """

    def post(self, *args, **kwargs):
        """Posts member removal request to API"""
        self.org_id = self.kwargs.get('org')
        self.username = self.kwargs.get('username')

        api = OCLapi(self.request, debug=True)
        result = api.delete('orgs', self.org_id, 'members', self.username)

        return self.render_json_response({'message':'Member removed'})

        # TODO(paynejd@gmail.com): Retire unreachable code?
        #if result.status_code == 204:
        #    return self.render_json_response({'message':'Member removed'})
        #else:
        #    return self.render_bad_request_response({'message': result.status_code})
