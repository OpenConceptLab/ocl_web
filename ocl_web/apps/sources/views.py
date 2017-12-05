"""
Views for OCL Sources and Source Versions.
"""
import re
import requests
import logging
import json
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, Http404, QueryDict)
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
from libs.ocl import OclApi, OclSearch, OclConstants
from simplejson import JSONDecodeError

from .forms import (
    SourceNewForm, SourceEditForm,
    SourceVersionsNewForm, SourceVersionsEditForm, SourceVersionsRetireForm, SourceDeleteForm)
from apps.core.views import UserOrOrgMixin
from apps.core.utils import SearchStringFormatter
from django.utils.http import urlencode

logger = logging.getLogger('oclweb')



class SourceReadBaseView(TemplateView):
    """ Base class for Source Read views. """

    def get_source_details(self, owner_type, owner_id, source_id, source_version_id=None):
        """ Load source details from the API and return as dictionary. """
        # TODO(paynejd@gmail.com): Load details from source version, if applicable (or remove?)
        # TODO(paynejd@gmail.com): Validate the input parameters

        api = OclApi(self.request, debug=True)
        search_response = api.get(owner_type, owner_id, 'sources', source_id)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()
        return search_response.json()

    def get_source_versions(self, owner_type, owner_id, source_id, search_params=None):
        """
        Load source versions from the API and return OclSearch instance with results.
        """
        # TODO(paynejd@gmail.com): Validate the input parameters

        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_SOURCE_VERSIONS,
                             search_scope=OclConstants.SEARCH_SCOPE_RESTRICTED,
                             params=search_params)

        api = OclApi(self.request, debug=True, facets=False)
        search_response = api.get(owner_type, owner_id, 'sources', source_id, 'versions',
                                  params=searcher.search_params)

        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type, search_response=search_response,
            search_params=search_params)

        return searcher

    def get_source_concepts(self, api_client, owner_type, owner_id, source_id,
                            source_version_id=None, search_params=None):
        """
        Load source concepts from the API and return OclSearch instance with results.
        """

        # Perform the search, applying source_version_id if not None
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_CONCEPTS,
                             search_scope=OclConstants.SEARCH_SCOPE_RESTRICTED,
                             params=search_params)

        if source_version_id:
            search_response = api_client.get(
                owner_type, owner_id, 'sources', source_id, source_version_id, 'concepts',
                params=searcher.search_params)
        else:
            search_response = api_client.get(
                owner_type, owner_id, 'sources', source_id, 'concepts',
                params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type,
            search_response=search_response,
            search_params=search_params)

        return searcher

    def get_source_mappings(self, owner_type, owner_id, source_id,
                            source_version_id=None, search_params=None):
        """
        Load source mappings from the API and return OclSearch instance with results.
        """

        # Perform the search, applying source_version_id if not None
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_MAPPINGS,
                             search_scope=OclConstants.SEARCH_SCOPE_RESTRICTED,
                             params=search_params)
        api = OclApi(self.request, debug=True, facets=True)
        if source_version_id:
            search_response = api.get(
                owner_type, owner_id, 'sources', source_id, source_version_id, 'mappings',
                params=searcher.search_params)
        else:
            search_response = api.get(
                owner_type, owner_id, 'sources', source_id, 'mappings',
                params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type,
            search_response=search_response,
            search_params=search_params)

        return searcher

    def get_source_extrefs(self, owner_type, owner_id, source_id,
                           source_version_id=None, search_params=None):
        """
        Load external mappings that reference this source from the API, return OclSearch instance.
        """

        # Get search_params into a mutable QueryDict format so that we can add values
        if isinstance(search_params, QueryDict):
            params = search_params.copy()
        elif isinstance(search_params, basestring):
            params = QueryDict(search_params, mutable=True)
        elif isinstance(search_params, dict) or not search_params:
            params = QueryDict('', mutable=True)
            params.update(search_params)
        else:
            raise TypeError('Expected QueryDict, dict, or str.' + str(search_params) + ' passed.')

        # Add additional search params for the extref mappings search
        new_params = {}
        new_params['toConceptOwnerType'] = 'Organization' if owner_type == 'orgs' else 'User'
        new_params['toConceptOwner'] = self.owner_id
        new_params['toConceptSource'] = self.source_id
        params.update(new_params)

        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_MAPPINGS,
                             search_scope=OclConstants.SEARCH_SCOPE_GLOBAL,
                             params=params)
        api = OclApi(self.request, debug=True, facets=True)
        search_response = api.get('mappings', params=searcher.search_params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type, search_response=search_response,
            search_params=search_params)

        # TODO: Post-processing on external references results goes here
        # Maybe remove toConceptOwnerType, toConceptOwner, toConceptSource facets

        return searcher



class SourceDetailsView(UserOrOrgMixin, SourceReadBaseView):
    """ Source Details view. """
    template_name = "sources/source_details.html"

    def get_context_data(self, *args, **kwargs):
        """ Loads the source details. """

        # Setup the context and args
        context = super(SourceDetailsView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source details
        source = self.get_source_details(self.owner_type, self.owner_id, self.source_id)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Details'
        context['source'] = source

        return context



class SourceAboutView(UserOrOrgMixin, SourceReadBaseView):
    """ Source About view. """
    template_name = "sources/source_about.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the source details and about info.
        """

        # Setup the context and args
        context = super(SourceAboutView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source details
        source = self.get_source_details(self.owner_type, self.owner_id, self.source_id)

        # Set about text
        about = None
        if ('extras' in source and isinstance(source['extras'], dict) and
                'about' in source['extras']):
            about = source['extras'].get('about')

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'About'
        context['source'] = source
        context['about'] = about

        return context



class SourceConceptsView(UserOrOrgMixin, SourceReadBaseView):
    """ Source Concepts view. """
    template_name = "sources/source_concepts.html"

    def get_context_data(self, *args, **kwargs):
        """ Loads the concepts that are in the source. """

        # Setup the context and args
        context = super(SourceConceptsView, self).get_context_data(*args, **kwargs)
        self.get_args()
        api = OclApi(self.request, debug=True, facets=True)

        # Load the source details
        source = self.get_source_details(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id)

        # Load the concepts in this source, applying search parameters
        original_search_string = self.request.GET.get('q', '')
        # TODO: SearchStringFormatter.add_wildcard(self.request)
        searcher = self.get_source_concepts(
            api, self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id,
            search_params=self.request.GET)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Load the source versions
        source_version_searcher = self.get_source_versions(
            self.owner_type, self.owner_id, self.source_id,
            search_params={'limit': '0'})

        # Build URL params
        transferrable_search_params = {}
        for param in OclSearch.TRANSFERRABLE_SEARCH_PARAMS:
            if param in self.request.GET:
                if param == 'q':
                    transferrable_search_params[param] = original_search_string
                else:
                    transferrable_search_params[param] = self.request.GET.get(param)

        # Encode the search parameters into a single URL-encoded string so that it can
        #   easily be appended onto URL links on the search page
        context['transferrable_search_params'] = ''
        if transferrable_search_params:
            context['transferrable_search_params'] = urlencode(transferrable_search_params)

        # Set the context
        context['kwargs'] = self.kwargs
        context['source'] = source
        context['source_version'] = self.source_version_id
        context['source_versions'] = source_version_searcher.search_results
        context['selected_tab'] = 'Concepts'
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_sort_option_defs'] = searcher.get_sort_option_definitions()
        context['search_sort'] = searcher.get_sort()
        context['search_query'] = original_search_string
        context['search_filters'] = searcher.search_filter_list

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Set debug variables
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context

    def get(self, request, *args, **kwargs):
        self.search_string = request.GET.get('q', '')
        SearchStringFormatter.add_wildcard(request)

        if request.is_ajax():
            self.get_args()
            api = OclApi(self.request, debug=True, facets=True)
            # Load the concepts in this source, applying search parameters
            searcher = self.get_source_concepts(
                api, self.owner_type, self.owner_id, self.source_id,
                source_version_id=self.source_version_id,
                search_params=self.request.GET
            )

            response = {
                'items': searcher.search_results,
                'per_page': searcher.num_per_page,
                'total': searcher.num_found,
            }

            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )
        return super(SourceConceptsView, self).get(self, *args, **kwargs)



class SourceMappingsView(UserOrOrgMixin, SourceReadBaseView):
    """ Source Mappings view. """
    template_name = "sources/source_mappings.html"

    def get_context_data(self, *args, **kwargs):
        """ Loads the mappings that are in the source. """

        # Setup the context and args
        context = super(SourceMappingsView, self).get_context_data(*args, **kwargs)
        self.get_args()
        api = OclApi(self.request, debug=True, facets=True)

        # Load the source details
        source = self.get_source_details(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id)

        # Load the mappings in this source, applying search parameters
        original_search_string = self.request.GET.get('q', '')
        # TODO: SearchStringFormatter.add_wildcard(self.request)
        searcher = self.get_source_mappings(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id,
            search_params=self.request.GET)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Load the source versions
        source_version_searcher = self.get_source_versions(
            self.owner_type, self.owner_id, self.source_id,
            search_params={'limit': '0'})

        # Build URL params
        transferrable_search_params = {}
        for param in OclSearch.TRANSFERRABLE_SEARCH_PARAMS:
            if param in self.request.GET:
                if param == 'q':
                    transferrable_search_params[param] = original_search_string
                else:
                    transferrable_search_params[param] = self.request.GET.get(param)

        # Encode the search parameters into a single URL-encoded string so that it can
        #   easily be appended onto URL links on the search page
        context['transferrable_search_params'] = ''
        if transferrable_search_params:
            context['transferrable_search_params'] = urlencode(transferrable_search_params)

        # Set the context
        context['kwargs'] = self.kwargs
        context['source'] = source
        context['source_version'] = self.source_version_id
        context['source_versions'] = source_version_searcher.search_results
        context['selected_tab'] = 'Mappings'
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_sort_option_defs'] = searcher.get_sort_option_definitions()
        context['search_sort'] = searcher.get_sort()
        context['search_query'] = original_search_string
        context['search_filters'] = searcher.search_filter_list

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Set debug variables
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.get_args()

            searcher = self.get_source_mappings(
                self.owner_type, self.owner_id, self.source_id,
                source_version_id=self.source_version_id,
                search_params=self.request.GET
            )

            response = {
                'items': searcher.search_results,
                'per_page': searcher.num_per_page,
                'total': searcher.num_found,
            }

            return HttpResponse(
                json.dumps(response),
                content_type="application/json"
            )
        return super(SourceMappingsView, self).get(self, *args, **kwargs)



class SourceExternalReferencesView(UserOrOrgMixin, SourceReadBaseView):
    """ Source External References view. """
    template_name = "sources/source_extrefs.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads all external mappings that point to a concept code in this source.
        """

        # Setup the context and args
        context = super(SourceExternalReferencesView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source details
        source = self.get_source_details(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id)

        # Load external mappings that point to this source, applying search criteria
        original_search_string = self.request.GET.get('q', '')
        # TODO: SearchStringFormatter.add_wildcard(self.request)
        searcher = self.get_source_extrefs(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id, search_params=self.request.GET)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Build URL params
        transferrable_search_params = {}
        for param in OclSearch.TRANSFERRABLE_SEARCH_PARAMS:
            if param in self.request.GET:
                if param == 'q':
                    transferrable_search_params[param] = original_search_string
                else:
                    transferrable_search_params[param] = self.request.GET.get(param)

        # Encode the search parameters into a single URL-encoded string so that it can
        #   easily be appended onto URL links on the search page
        context['transferrable_search_params'] = ''
        if transferrable_search_params:
            context['transferrable_search_params'] = urlencode(transferrable_search_params)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['selected_tab'] = 'External References'
        context['source'] = source
        context['source_version'] = self.source_version_id
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_query'] = searcher.get_query()
        context['search_filters'] = searcher.search_filter_list
        context['search_sort_option_defs'] = searcher.get_sort_option_definitions()
        context['search_sort'] = searcher.get_sort()
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context



class SourceVersionsView(UserOrOrgMixin, SourceReadBaseView):
    """ Source Versions view. """
    template_name = "sources/source_versions.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the source versions.
        """

        # Setup the context and args
        context = super(SourceVersionsView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source details
        source = self.get_source_details(self.owner_type, self.owner_id, self.source_id)

        # Load the source versions
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'
        searcher = self.get_source_versions(
            self.owner_type, self.owner_id, self.source_id,
            search_params=params)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Set the context
        context['kwargs'] = self.kwargs
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Versions'
        context['source'] = source
        context['source_versions'] = searcher.search_results

        return context

    def get(self, request, *args, **kwargs):
        self.get_args()
        if request.is_ajax():
            api = OclApi(self.request, debug=True)
            result = api.get(self.owner_type, self.owner_id, 'sources', kwargs.get('source'),
                             'versions', params={'limit': '0'})
            return HttpResponse(json.dumps(result.json()), content_type="application/json")
        return super(SourceVersionsView, self).get(self, *args, **kwargs)



class SourceVersionsNewView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """ View to Create new source version """
    form_class = SourceVersionsNewForm
    template_name = "sources/source_versions_new.html"

    def get_initial(self):
        """ Load initial form data """
        context = super(SourceVersionsNewView, self).get_initial()
        self.get_args()

        # Load the most recent source version
        api = OclApi(self.request, debug=True)
        source_version = None
        if self.from_org:
            source_version = api.get('orgs', self.org_id, 'sources', self.source_id,
                                     'versions', params={'limit':1}).json()
        else:
            source_version = api.get('users', self.user_id, 'sources', self.source_id,
                                     'versions', params={'limit':1}).json()

        data = {
            'request': self.request,
            'from_user': self.from_user,
            'from_org': self.from_org,
            'user_id': self.user_id,
            'org_id': self.org_id,
            'owner_type': self.owner_type,
            'owner_id': self.owner_id,
            'source_id': self.source_id,
            'previous_version': source_version[0]['id'],
            'released': False
        }
        return data


    def get_context_data(self, *args, **kwargs):
        """
        Load context data needed for the view
        """
        context = super(SourceVersionsNewView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source
        api = OclApi(self.request, debug=True)
        source = None
        if self.from_org:
            source = api.get('orgs', self.org_id, 'sources', self.source_id).json()
        else:
            source = api.get('users', self.user_id, 'sources', self.source_id).json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['source'] = source

        return context


    def form_valid(self, form):
        """
        Submits the form to the API
        """
        self.get_args()

        # Submit the new source version
        data = form.cleaned_data
        api = OclApi(self.request, debug=True)
        result = api.create_source_version(self.owner_type, self.owner_id, self.source_id, data)
        if result.status_code == requests.codes.created:
            messages.add_message(self.request, messages.INFO, _('Source version created!'))
            if self.from_org:
                return HttpResponseRedirect(reverse('source-versions',
                                                    kwargs={'org': self.org_id,
                                                            'source': self.source_id}))
            else:
                return HttpResponseRedirect(reverse('source-versions',
                                                    kwargs={'user': self.user_id,
                                                            'source': self.source_id}))
        else:
            error_msg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, error_msg)
            return HttpResponseRedirect(self.request.path)



class SourceVersionsEditView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """ View to edit source version """
    form_class = SourceVersionsEditForm
    template_name = "sources/source_versions_edit.html"

    def get_form_class(self):
        """ Trick to load initial form data """
        self.get_args()
        api = OclApi(self.request, debug=True)
        self.source_version = api.get(self.owner_type, self.owner_id, 'sources', self.source_id,
                                      self.source_version_id).json()
        return SourceVersionsEditForm

    def get_initial(self):
        """ Load initial form data """
        data = {
            'org_id': self.org_id,
            'user_id': self.user_id,
            'from_org': self.from_org,
            'from_user': self.from_user,
            'source_id': self.source_id,
            'source_version_id': self.source_version_id,
            'request': self.request,
        }
        data.update(self.source_version)
        return data

    def get_context_data(self, *args, **kwargs):
        """ Load context data needed for the view """
        context = super(SourceVersionsEditView, self).get_context_data(*args, **kwargs)
        context['kwargs'] = self.kwargs
        context['source_version'] = self.source_version
        return context

    def form_valid(self, form):
        """ If form data is valid, then update API backend. """
        self.get_args()

        # Submit updated source version description to the API

        data = {
            'description':form.cleaned_data.get('description'),
            'version_external_id':form.cleaned_data.get('version_external_id')
        }

        api = OclApi(self.request, debug=True)
        result = api.update_resource_version(self.owner_type, self.owner_id, self.source_id,
                                             self.source_version_id, 'sources', data)

        # Check if successful
        if result.status_code == requests.codes.ok:
            messages.add_message(self.request, messages.INFO, _('Source version updated'))
            if self.from_org:
                return HttpResponseRedirect(reverse('source-versions',
                                                    kwargs={'org': self.org_id,
                                                            'source': self.source_id}))
            else:
                return HttpResponseRedirect(reverse('source-versions',
                                                    kwargs={'user': self.user_id,
                                                            'source': self.source_id}))
        else:
            emsg = result.text
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)



class SourceVersionsRetireView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """ View to retire source version """
    form_class = SourceVersionsRetireForm
    template_name = "sources/source_versions_retire.html"

    def get_initial(self):
        """ Load initial form data """
        pass



class SourceNewView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """ View to create new source """
    form_class = SourceNewForm
    template_name = "sources/source_create.html"

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        self.get_args()

        data = {
            'request': self.request,
            'from_user': self.from_user,
            'from_org': self.from_org,
            'user_id': self.user_id,
            'org_id': self.org_id,
            'owner_type': self.owner_type,
            'owner_id': self.owner_id
        }
        return data

    def get_context_data(self, *args, **kwargs):
        """
        Return org details
        """
        context = super(SourceNewView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OclApi(self.request, debug=True)
        org = ocl_user = None

        if self.from_org:
            org = api.get('orgs', self.org_id).json()
        else:
            ocl_user = api.get('users', self.user_id).json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['org'] = org
        context['ocl_user'] = ocl_user
        context['from_user'] = self.from_user
        context['from_org'] = self.from_org

        return context

    def form_valid(self, form):
        """
        Return whether source input is valid and then update API backend.
        """
        self.get_args()

        data = form.cleaned_data
        short_code = data.pop('short_name')
        data['short_code'] = short_code
        data['id'] = short_code
        data['name'] = short_code
        if re.compile('^' + OclConstants.ORG_PATTERN + '$').match(short_code):
            api = OclApi(self.request, debug=True)
            result = api.create_source(self.owner_type, self.owner_id, data)
            if result.status_code == requests.codes.created:
                messages.add_message(self.request, messages.INFO, _('Source created'))
                if self.from_org:
                    return HttpResponseRedirect(reverse("source-home",
                                                        kwargs={"org": self.org_id,
                                                                'source': short_code}))
                else:
                    return HttpResponseRedirect(reverse("source-home",
                                                        kwargs={"user": self.user_id,
                                                                'source': short_code}))
            else:
                emsg = result.json().get('detail', None)
                if not emsg:
                    for msg in result.json().get('__all__'):
                        messages.add_message(self.request, messages.ERROR, msg)
                else:
                    messages.add_message(self.request, messages.ERROR, emsg)
                return HttpResponseRedirect(self.request.path)
        else:
            validator_template = ' Short Code \'%s\' is not valid. Allowed characters are : Alphabets(a-z,A-Z), Numbers(0-9) and Hyphen(-) '
            messages.add_message(self.request, messages.ERROR, validator_template % short_code)
            return HttpResponseRedirect(self.request.path)



class SourceEditView(UserOrOrgMixin, FormView):
    """ Edit source, either for an org or a user. """
    template_name = "sources/source_edit.html"
    failed_concept_validations = []

    def get_form_class(self):
        """ Trick to load initial data """
        self.get_args()
        api = OclApi(self.request, debug=True)
        self.source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()
        return SourceEditForm

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        data = {
            'org_id': self.org_id,
            'user_id': self.user_id,
            'from_org': self.from_org,
            'from_user': self.from_user,
            'request': self.request,
        }
        data.update(self.source)
        # convert supported locales to string
        supported_locale_list = self.source.get('supported_locales')
        if supported_locale_list is None:
            data['supported_locales'] = ''
        else:
            data['supported_locales'] = ','.join(supported_locale_list)

        return data

    def get_context_data(self, *args, **kwargs):
        """ Get source details for the edit form """
        context = super(SourceEditView, self).get_context_data(*args, **kwargs)
        self.get_args()

        api = OclApi(self.request, debug=True)
        org = ocl_user = None
        if self.from_org:
            org = api.get('orgs', self.org_id).json()
        else:
            ocl_user = api.get('users', self.user_id).json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['org'] = org
        context['ocl_user'] = ocl_user
        context['from_user'] = self.from_user
        context['from_org'] = self.from_org
        context['source'] = self.source
        context['failed_concept_validations'] = self.failed_concept_validations

        return context

    def form_valid(self, form):
        """ If Source input is valid, then update API backend. """
        self.get_args()

        # Submit updated source data to the API
        data = form.cleaned_data
        api = OclApi(self.request, debug=True)
        result = api.update_source(self.owner_type, self.owner_id, self.source_id, data)
        print result

        if len(result.text) > 0:
            print result.json()

        if result.status_code <= 201:
            messages.add_message(self.request, messages.INFO, _('Source updated'))
            if self.from_org:
                return HttpResponseRedirect(reverse('source-details',
                                                    kwargs={'org': self.org_id,
                                                            'source': self.source_id}))
            else:
                return HttpResponseRedirect(reverse('source-details',
                                                    kwargs={'user': self.user_id,
                                                            'source': self.source_id}))
        else:
            try:
                self.failed_concept_validations = result.json().get('failed_concept_validations', None)
                messages.add_message(self.request, messages.ERROR, _('Some concepts failed validation'))

            except JSONDecodeError as error:
                messages.add_message(self.request, messages.ERROR, _(error))

            return super(SourceEditView, self).form_invalid(form)



class SourceDeleteView(UserOrOrgMixin, FormView):
    """
    View for deleting Source.
    """

    template_name = "sources/source_delete.html"
    form_class = SourceDeleteForm

    def get_context_data(self, *args, **kwargs):
        context = super(SourceDeleteView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'sources', self.source_id)
        source = results.json()
        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['source'] = source

        return context

    def get_success_url(self):
        """ Return URL for redirecting browser """
        if self.from_org:
            return reverse('org-sources',
                           kwargs={'org': self.org_id})

        else:
            return reverse('users:detail',
                           kwargs={"username": self.request.user.username})

    def form_valid(self, form, *args, **kwargs):
        """ Use validated form data to delete the source"""

        self.get_args()

        api = OclApi(self.request, debug=True)
        result = api.delete(
            self.owner_type, self.owner_id, 'sources', self.source_id, **kwargs)

        if result.status_code != 204:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        else:
            messages.add_message(self.request, messages.INFO, _('Source Deleted'))
            return HttpResponseRedirect(self.get_success_url())



class SourceVersionEditJsonView(UserOrOrgMixin, TemplateView):
    def put(self, request, *args, **kwargs):
        api = OclApi(self.request, debug=True)
        data = json.loads(request.body)

        if 'org' in kwargs:
            owner_type = 'orgs'
            owner_id = kwargs['org']
        else:
            owner_type = 'users'
            owner_id = kwargs['user']

        res = api.update_resource_version(owner_type,
                                          owner_id,
                                          kwargs['source'],
                                          kwargs['source_version'],
                                          'sources',
                                          data)
        return HttpResponse(res.content, status=res.status_code)



class SourceVersionDeleteView(UserOrOrgMixin, TemplateView):
    """ source version delete view"""

    def delete(self, request, *args, **kwargs):
        self.get_args()
        api = OclApi(self.request, debug=True)

        if request.is_ajax():
            result = api.delete(
                self.owner_type,
                self.owner_id,
                'sources',
                self.source_id,
                self.source_version_id,
                **kwargs
            )

            return HttpResponse(
                json.dumps({}),
                content_type="application/json"
            )
        return super(SourceVersionDeleteView, self).delete(self, *args, **kwargs)
