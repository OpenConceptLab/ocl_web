import requests

from django.shortcuts import redirect
from django.http import Http404
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from braces.views import LoginRequiredMixin
from braces.views import (CsrfExemptMixin, JsonRequestResponseMixin)

from .forms import (OrganizationCreateForm, OrganizationEditForm)
from .forms import (OrganizationMemberAddForm)
from libs.ocl import OCLapi, OCLSearch


class OrganizationDetailView(TemplateView):
    """
    Organization details and source search view.
    """

    template_name = "orgs/org_detail.html"

    def get_context_data(self, *args, **kwargs):
        """Gets the org first, then the sources of that org, and then the
        concepts from each of those sources.

        Final context
        -------------
        context['org']
        context['sources']
        context['collections']
        context['members']
        """
        # TODO: Change page so that only one tab loaded at a time

        context = super(OrganizationDetailView, self).get_context_data(*args, **kwargs)

        # Determine the organization ID
        org_id = self.kwargs.get('org')

        # Prepare to search the sources and collections in this org
        # BUG: OCLSearch.parse() fails if no URL parameters are passed
        # NOTE: Both are searched no matter what, but only one accepts search criteria/filters at a time
        res_type = self.request.GET.get('resource_type')
        print 'INPUT PARAMS %s: %s' % (self.request.method, self.request.GET)
        print res_type
        if res_type == 'source':
            source_searcher = OCLSearch(search_type=OCLSearch.SOURCE_TYPE, params=self.request.GET)
            collection_searcher = OCLSearch(search_type=OCLSearch.COLLECTION_TYPE, params={})
        elif res_type == 'collection':
            source_searcher = OCLSearch(search_type=OCLSearch.SOURCE_TYPE, params={})
            collection_searcher = OCLSearch(search_type=OCLSearch.COLLECTION_TYPE, params=self.request.GET)
        else:
            # Still pass down paging parameters
            source_searcher = OCLSearch(search_type=OCLSearch.SOURCE_TYPE, params=self.request.GET)
            collection_searcher = OCLSearch(search_type=OCLSearch.COLLECTION_TYPE, params=self.request.GET)

        # Load the organization
        api = OCLapi(self.request, debug=True)
        search_result_org = api.get('orgs', org_id)
        if search_result_org.status_code != 200:
            if search_result_org.status_code == 404:
                raise Http404
            else:
                search_result_org.raise_for_status()
        org = search_result_org.json()

        # Set org about text
        # TODO: Need a more generic method for getting at extras
        if 'extras' in org and isinstance(org['extras'], dict):
            about = org['extras'].get('about', 'No about entry.')
        else:
            # TODO: If user has editing privileges to this org, then prompt them to create an about entry
            about = 'No about entry.'

        # Load the sources in this org
        api.include_facets = True
        search_result_sources = api.get('orgs', org_id, 'sources', params=source_searcher.search_params)
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
            # BUG: If num_found is not present or if sources_num_found is 0, that may cause paginator error
            if 'num_found' in search_result_sources.headers:
                try:
                    sources_num_found = int(search_result_sources.headers['num_found'])
                except ValueError:
                    sources_num_found = 0
            else:
                sources_num_found = 0
            sources_paginator = Paginator(range(num_found), source_searcher.num_per_page)
            sources_current_page = sources_paginator.page(source_searcher.current_page)

        # TODO: Setup source filters based on the current search

        # Select filters
        # TODO: This is passing all parameters, but should pass only those relevant to sources
        source_searcher.select_filters(self.request.GET)

        # Set the context for the child sources
        context['sources'] = sources
        context['source_page'] = sources_current_page
        context['source_pagination_url'] = self.request.get_full_path()
        context['source_q'] = source_searcher.get_query()
        context['source_facets'] = source_facets

        # TODO: Sort is not setup correctly to work with both sources and collections
        context['search_sort_options'] = source_searcher.get_sort_options()
        context['search_sort'] = source_searcher.get_sort()

        # Load the collections in this org
        # TODO: Collections not implemented yet
        #api.include_facets = True
        #search_result_collections = api.get('orgs', org_id, 'collections', params=collection_searcher.search_params)
        # if search_result_collections.status_code == requests.codes.not_found:
        #     collections = []
        #     num_found = 0
        #     context['collection_page'] = 0
        # else:
        #     collections = search_result_collections.json()
        #     num_found = int(search_result_collections.headers['num_found'])
        #     pg = Paginator(range(num_found), collection_searcher.num_per_page)
        #     context['collection_page'] = pg.page(collection_searcher.current_page)
        #
        # Set the context for the child collections
        #context['collection_pagination_url'] = self.request.get_full_path()
        #context['collections'] = collections
        #context['collection_filters'] = collection_searcher.get_filters()

        # Load members of this org
        # TODO: Access issue, error if user is not super user??
        members = []
        r = api.get('orgs', org_id, 'members')
        if r.status_code == 200:
            members = r.json()
        elif r.status_code != 404:
            #raise Exception(r.json())
            pass

        # Set the context
        context['org'] = org
        context['members'] = members
        context['about'] = about
        return context


class OrganizationCreateView(LoginRequiredMixin, FormView):

    form_class = OrganizationCreateForm
    template_name = "orgs/org_new.html"

    def form_valid(self, form, *args, **kwargs):

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
            return redirect(reverse('org-detail', kwargs={'org': org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationCreateView, self).form_invalid(self, *args, **kwargs)


class OrganizationEditView(FormView):

    template_name = 'orgs/org_edit.html'

    def get_form_class(self):
        """ Trick to do some initial lookup """
        self.org_id = self.kwargs.get('org')
        api = OCLapi(self.request, debug=True)
        self.org = api.get('orgs', self.org_id).json()
        return OrganizationEditForm

    def get_context_data(self, *args, **kwargs):

        context = super(OrganizationEditView, self).get_context_data(*args, **kwargs)
        context['org'] = self.org
        return context

    def get_initial(self):
        return self.org

    def form_valid(self, form, *args, **kwargs):

        api = OCLapi(self.request, debug=True)

        data = {}
        data.update(form.cleaned_data)
        result = api.update_org(self.org_id, data)
        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Organization updated.'))
            return redirect(reverse('org-detail', kwargs={'org': self.org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationEditView, self).form_invalid(form)


class OrganizationMemberAddView(LoginRequiredMixin, FormView):

    form_class = OrganizationMemberAddForm
    template_name = "orgs/org_member_add.html"

    def get_org(self):
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
        """
        context = super(OrganizationMemberAddView, self).get_context_data(*args, **kwargs)
        context['org'] = self.org
        return context

    def form_valid(self, form, *args, **kwargs):
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
            return redirect(reverse('org-detail', kwargs={'org': self.org['id']}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationMemberAddView, self).form_invalid(form)


class OrganizationMemberRemoveView(LoginRequiredMixin,
                                   JsonRequestResponseMixin, View):

    def post(self, *args, **kwargs):
        self.org_id = self.kwargs.get('org')
        self.username = self.kwargs.get('username')

        api = OCLapi(self.request, debug=True)
        result = api.delete('orgs', self.org_id, 'members', self.username)

        return self.render_json_response({'message':'Member removed'})
        if result.status_code == 204:
            return self.render_json_response({'message':'Member removed'})

        else:
            return self.render_bad_request_response({'message': result.status_code})


