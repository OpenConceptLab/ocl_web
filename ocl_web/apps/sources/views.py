"""
Views for OCL Sources and Source Versions.
"""
import requests
import logging

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, Http404)
from django.views.generic import (TemplateView, View)
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.paginator import Paginator
from braces.views import JsonRequestResponseMixin

from libs.ocl import OCLapi, OCLSearch
from .forms import (SourceCreateForm, SourceEditForm)
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')


class SourceDetailView(UserOrOrgMixin, TemplateView):
    """
    OCL Source detailed view.
    """

    template_name = "sources/source_detail.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the source then the concepts for the source
        """
        # TODO: Change each tab to a separate page (like GitHub)

        context = super(SourceDetailView, self).get_context_data(*args, **kwargs)
        context['get_params'] = self.request.GET
        print 'Source Detail INPUT PARAMS %s: %s' % (self.request.method, self.request.GET)

        # Adds identifying attributes to the instance
        # TODO: This is poorly named and kind of a hack -- fix it!
        self.get_args()

        # Load the source
        api = OCLapi(self.request, debug=True)
        # TODO: Change own_type and own_id to owner_type and owner_id
        source_search_results = api.get(self.own_type, self.own_id, 'sources', self.source_id)
        if source_search_results.status_code != 200:
            if source_search_results.status_code == 404:
                raise Http404
            else:
                source_search_results.raise_for_status()
        source = source_search_results.json()
        context['source'] = source

        # Set about text for the source
        if isinstance(source['extras'], dict):
            about = source['extras'].get('about', 'No about entry.')
        else:
            about = 'No about entry.'
        context['about'] = about

        # Load the concepts in this source
        api.include_facets = True
        concept_searcher = OCLSearch(search_type=OCLapi.CONCEPT_TYPE, params=self.request.GET)
        concept_search_results = api.get(
            self.own_type, self.own_id, 'sources', self.source_id,
            'concepts', params=concept_searcher.search_params)
        if concept_search_results.status_code != 200:
            if concept_search_results.status_code == 404:
                raise Http404
            else:
                concept_search_results.raise_for_status()
        concepts_response_json = concept_search_results.json()
        concepts_facets_json = concepts_response_json['facets']
        concepts_facets = concept_searcher.process_facets('concepts', concepts_facets_json)
        concepts = concepts_response_json['results']
        if 'num_found' in concept_search_results.headers:
            try:
                concepts_num_found = int(concept_search_results.headers['num_found'])
            except ValueError:
                concepts_num_found = 0
        else:
            concepts_num_found = 0
        concepts_paginator = Paginator(range(concepts_num_found), concept_searcher.num_per_page)
        concepts_current_page = concepts_paginator.page(concept_searcher.current_page)

        # TODO: Setup source filters based on the current search

        # Select concept filters
        # TODO: This is passing all parameters, but should pass only those relevant to concepts
        concept_searcher.select_search_filters(self.request.GET)

        # Set the context for the child concepts
        context['concepts'] = concepts
        context['concept_page'] = concepts_current_page
        context['concept_pagination_url'] = self.request.get_full_path()
        context['concept_q'] = concept_searcher.get_query()
        context['concept_facets'] = concepts_facets

        # TODO: Sort is not setup correctly to work with both concepts and mappings
        context['search_sort_options'] = concept_searcher.get_sort_options()
        context['search_sort'] = concept_searcher.get_sort()

        # TODO: Load the mappings in this source
        # TODO: Setup source filters based on the current search
        # TODO: Select mapping filters
        # TODO: Set the context for the child mappings

        # Load the source versions
        source_version_api = OCLapi(self.request, debug=True)
        source_version_search_results = source_version_api.get(
            self.own_type, self.own_id, 'sources', self.source_id,
            'versions')
        if source_version_search_results.status_code != 200:
            if source_version_search_results.status_code == 404:
                raise Http404
            else:
                source_version_search_results.raise_for_status()
        source_versions = source_version_search_results.json()
        context['source_versions'] = source_versions

        return context


class SourceCreateView(UserOrOrgMixin, FormView):
    """
    Create new source, either for an org or a user.
    """

    form_class = SourceCreateForm
    template_name = "sources/source_create.html"

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        self.get_args()

        data = {
            'org_id': self.org_id,
            'user_id': self.user_id,
            'from_org': self.from_org,
            'from_user': self.from_user,
            'request': self.request,
        }
        return data

    def get_context_data(self, *args, **kwargs):
        """

        """
        context = super(SourceCreateView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OCLapi(self.request, debug=True)
        org = ocl_user = None

        if self.from_org:
            org = api.get('orgs', self.org_id).json()
        else:
            ocl_user = api.get('users', self.user_id).json()
        # Set the context
        context['org'] = org
        context['ocl_user'] = ocl_user
        context['from_user'] = self.from_user
        context['from_org'] = self.from_org

        return context

    def form_valid(self, form):
        """
        Retrun whether source input is valid and then update API backend.
        """
        # TODO(paynejd@gmail.com): Rename class method -- it is submitting & validating the form

        print form.cleaned_data

        self.get_args()

        data = form.cleaned_data
        short_code = data.pop('short_name')
        data['short_code'] = short_code
        data['id'] = short_code
        data['name'] = short_code

        api = OCLapi(self.request, debug=True)
        if self.from_org:
            result = api.create_source_by_org(self.org_id, data)
        else:
            result = api.create_source_by_user(self.user_id, data)
        if not result.status_code == requests.codes.created:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        messages.add_message(self.request, messages.INFO, _('Source created'))

        if self.from_org:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"org": self.org_id,
                                                        'source': short_code}))
        else:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"user": self.user_id,
                                                        'source': short_code}))


class SourceEditView(UserOrOrgMixin, FormView):
    """
    Edit source, either for an org or a user.
    """
    template_name = "sources/source_edit.html"

    def get_form_class(self):
        """
        Trick to load initial data
        """
        self.get_args()
        api = OCLapi(self.request, debug=True)
        self.source_id = self.kwargs.get('source')
        if self.from_org:
            self.source = api.get('orgs', self.org_id, 'sources', self.source_id).json()
        else:
            self.source = api.get('users', self.user_id, 'sources', self.source_id).json()
        return SourceEditForm

    def get_initial(self):
        """
        Load some useful data, not really for form display but internal use
        """

        data = {
            'org_id': self.org_id,
            'user_id': self.user_id,
            'from_org': self.from_org,
            'from_user': self.from_user,
            'request': self.request,
        }
        data.update(self.source)
        # convert supported locales to string
        ls = self.source.get('supported_locales')
        if ls is None:
            data['supported_locales'] = ''
        else:
            data['supported_locales'] = ','.join(ls)

        return data

    def get_context_data(self, *args, **kwargs):
        context = super(SourceEditView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OCLapi(self.request, debug=True)
        org = ocl_user = None

        if self.from_org:
            org = api.get('orgs', self.org_id).json()
        else:
            ocl_user = api.get('users', self.user_id).json()
        # Set the context
        context['org'] = org
        context['ocl_user'] = ocl_user
        context['from_user'] = self.from_user
        context['from_org'] = self.from_org
        context['source'] = self.source

        return context

    def form_valid(self, form):
        """
        If Source input is valid, then update API backend.
        """
        # TODO(paynejd@gmail.com): Rename this class method -- it is validating & submitting form

        print form.cleaned_data

        self.get_args()

        data = form.cleaned_data

        api = OCLapi(self.request, debug=True)
        if self.from_org:
            result = api.update_source_by_org(self.org_id, self.source_id, data)
        else:
            result = api.update_source_by_user(self.user_id, self.source_id, data)
        print result
        if len(result.text) > 0:
            print result.json()

        messages.add_message(self.request, messages.INFO, _('Source updated'))

        if self.from_org:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"org": self.org_id,
                                                        'source': self.source_id}))
        else:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"user": self.user_id,
                                                        'source': self.source_id}))


class SourceVersionView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
    Handle source version list, add, update and delete via a JSON interface.

    TODO: use ConceptItemView if ConceptItemView is modified to use a list of args
        to specify the sub-path before item. concepts/CC/, but also the versions
        API does not use a keyword "versions", instead just append the version ID to the source
        ID.
    """
    # override this, set to 'descriptions', 'names', etc
    item_name = 'versions'
    kwarg_name = 'version'
    field_names = ['id', 'description', 'released']

    def get_all_args(self):
        """
        Get all the input entities' identity, figure out whether this is a user owned
        sourced concept or an org owned sourced concept, and set self.own_type, self.own_id
        for easy interface to OCL API.
        """
        self.get_args()
        self.item_id = self.kwargs.get(self.kwarg_name)

    def is_edit(self):
        return self.item_id is not None

    def get(self, request, *args, **kwargs):
        """
            Return a list of versions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(self.own_type, self.own_id, 'sources', self.source_id,
                         'versions', '?verbose=True')
        if not result.ok:
            logger.warning('GET error %s : %s' % (result.status_code, api.url))
            return self.render_bad_request_response(result)

        return self.render_json_response(result.json())

    def post(self, request, *args, **kwargs):
        """
            Create or edit a source version.
        """
        self.get_all_args()
        data = {}
        try:
            print 'request json:', self.request_json
            for n in self.field_names:
                # Skipping over fields that are not given -- exception is never thrown now...??
                v = self.request_json.get(n, None)
                if v is not None:
                    data[n] = v
        except KeyError:
            resp = {u"message": _('Invalid input')}
            return self.render_bad_request_response(resp)

        api = OCLapi(self.request, debug=True)
        if self.is_edit():
            # NOTE: updating a version URL does not have the keyword "versions",
            # rather, it is /owner/:owner/sources/:source/:version/
            result = api.put(self.own_type, self.own_id, 'sources', self.source_id,
                             self.item_id, **data)
            msg = _('Source Version updated!')
        else:
            result = api.post(self.own_type, self.own_id, 'sources', self.source_id,
                              'versions', **data)
            msg = _('Source Version created!')

        if not result.ok:
            logger.warning('Source Version POST error: %s' % result.status_code)
            return self.render_bad_request_response(result)

        return self.render_json_response({'message': msg})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified source version.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)
        if self.is_edit():  # i.e. has item UUID
            result = api.delete(self.own_type, self.own_id, 'sources',
                                self.source_id, self.item_id)
        if not result.ok:
            logger.warning('Source Version DELETE error: %s' % result.status_code)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': _('Source Version deleted!')})
