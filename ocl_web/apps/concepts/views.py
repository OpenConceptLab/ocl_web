"""
OCL Concept Views
"""

import requests
import logging

from django.views.generic import TemplateView
from django.views.generic.edit import (View, FormView)
from django.http import (HttpResponseRedirect, Http404)
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.core.paginator import Paginator

from braces.views import (LoginRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin)

from .forms import (ConceptNewForm, ConceptCreateForm, ConceptEditForm, ConceptRetireForm)
from libs.ocl import OCLapi, OCLSearch
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')



class ConceptReadBaseView(TemplateView):
    """
    Base class for Concept Read views.
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

    def get_concept_details(self, owner_type, owner_id, source_id, concept_id,
                            source_version_id=None, concept_version_id=None,
                            include_mappings=False, include_inverse_mappings=False):
        """
        Get the concept details.
        """

        # Setup request parameters
        params = {}
        if include_mappings:
            params['includeMappings'] = 'true'
            params['verbose'] = 'true'
        if include_inverse_mappings:
            params['includeInverseMappings'] = 'true'
            params['verbose'] = 'true'

        # TODO(paynejd@gmail.com): Validate input parameters
        api = OCLapi(self.request, debug=True)
        if source_version_id and concept_version_id:
            raise ValueError(
                'Must specify only a source version or a concept version. Both were specified.')
        elif source_version_id:
            search_response = api.get(
                owner_type, owner_id, 'sources', source_id, source_version_id,
                'concepts', concept_id,
                params=params)
        elif concept_version_id:
            search_response = api.get(
                owner_type, owner_id, 'sources', source_id,
                'concepts', concept_id, concept_version_id,
                params=params)
        else:
            search_response = api.get(
                owner_type, owner_id, 'sources', source_id,
                'concepts', concept_id,
                params=params)
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()
        return search_response.json()

    def get_concept_history(self, owner_type, owner_id, source_id, concept_id,
                            source_version_id=None, concept_version_id=None,
                            search_params=None):
        """
        Get the concept version history.
        """
        # TODO(paynejd@gmail.com): Validate input parameters
        # TODO(paynejd@gmail.com): source_version_id and concept_version_id not currently used

        # Create the searcher
        searcher = OCLSearch(search_type=OCLapi.CONCEPT_VERSION_TYPE, params=search_params)

        # Perform the search
        api = OCLapi(self.request, debug=True, facets=False)
        search_response = api.get(
            owner_type, owner_id, 'sources', source_id,
            'concepts', concept_id, 'versions')
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type='concept version', search_response=search_response,
            has_facets=False, search_params=search_params)

        return searcher



class ConceptDetailsView(UserOrOrgMixin, ConceptReadBaseView):
    """
    Concept details view.
    """
    template_name = "concepts/concept_details.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the concept details.
        """

        # Setup the context and args
        context = super(ConceptDetailsView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the concept details
        concept = self.get_concept_details(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id)

        # Load the source that contains this concept
        # TODO(paynejd@gmail.com): This is only loaded because of the funky implementation of the
        # owner and source label tags --- REMOVE IN THE FUTURE
        source = self.get_source_details(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id)

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Details'
        context['concept'] = concept
        context['source'] = source

        return context



class ConceptMappingsView(UserOrOrgMixin, ConceptReadBaseView):
    """
    Concept mappings view.
    """
    template_name = "concepts/concept_mappings.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the concept details.
        """

        # Setup the context and args
        context = super(ConceptMappingsView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the concept details
        concept = self.get_concept_details(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id,
            include_mappings=True, include_inverse_mappings=True)

        # Load the source that contains this concept
        # TODO(paynejd@gmail.com): This is only loaded because of the funky implementation of the
        # owner and source label tags --- REMOVE IN THE FUTURE
        source = self.get_source_details(
            self.owner_type, self.owner_id, self.source_id,
            source_version_id=self.source_version_id)

        # Process mappings
        mappings = concept['mappings'].copy()
        # TODO(paynejd@gmail.com): Do necessary processing of mappings here

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Mappings'
        context['concept'] = concept
        context['source'] = source
        context['mappings'] = mappings

        return context



class ConceptHistoryView(UserOrOrgMixin, ConceptReadBaseView):
    """
    Concept history view.
    """
    template_name = "concepts/concept_history.html"

    def get_context_data(self, *args, **kwargs):
        """
        Loads the concept details and its version history.
        """

        # Setup the context and args
        context = super(ConceptHistoryView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the concept details
        concept = self.get_concept_details(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id)

        # Load the concept version history
        searcher = self.get_concept_history(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Set the context
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'History'
        context['concept'] = concept
        context['concept_versions'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()

        return context



class ConceptNewView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """
    View to create new concept
    """

    form_class = ConceptNewForm
    template_name = "concepts/concept_new.html"

    def get_initial(self):
        """ Load some useful data into the context """

        data = super(ConceptNewView, self).get_initial()

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

    def get_context_data(self, *args, **kwargs):
        """
        Loads the context data for creating a new concept.
        """

        # Setup the context and args
        context = super(ConceptNewView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source that the new concept will belong to
        api = OCLapi(self.request, debug=True)
        source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()

        # Set the context
        context['source'] = source

        return context

    def form_valid(self, form, *args, **kwargs):
        """
        Validates the form data and submits if valid
        """
        # TODO(paynejd@gmail.com): Rename this method - it validates and submits form

        #org_id = form.cleaned_data.pop('short_name')

        # api = OCLapi(self.request, debug=True)

        # data = {
        #     'id': org_id,
        # }
        # data.update(form.cleaned_data)
        # print form.cleaned_data
        # print data
        # result = api.create_org(data)

        # # TODO:  Catch exceptions that will be raised by
        # # Ocl lib.
        # if result.ok:
        #     messages.add_message(self.request, messages.INFO, _('Concept Added'))
        #     return redirect(reverse('org-details', kwargs={'org': org_id}))

        # # TODO:  Add error messages from API to form.
        # else:
        #     return super(ConceptNewView, self).form_invalid(self, *args, **kwargs)




class ConceptCreateJsonView(UserOrOrgMixin, JsonRequestResponseMixin,
                            TemplateView):
    """
    A mix HTTP and ajax view for creating and editing concepts.
    on Get returns full HTML display page.
    create is handled via ajax post via angular.
    """

    def get(self, request, *args, **kwargs):
        """Get concept
        """

        self.get_args()
        data = {}
        print self.request.is_ajax()
        api = OCLapi(self.request, debug=True)
        source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()
        data['source'] = source

        if self.concept_id is not None:
            # edit
            concept = api.get(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'concepts', self.concept_id).json()
            data['concept'] = concept

            if request.is_ajax():
                return self.render_json_response(concept)

        if self.concept_id is None:
            return TemplateResponse(request, 'concepts/concept_create.html', data)
        else:
            return TemplateResponse(request, 'concepts/concept_edit.html', data)


    def get_success_url(self):
        """Get success URL
        """

        if self.from_org:
            return reverse("source-home",
                           kwargs={"org": self.org_id,
                                   'source': self.kwargs.get('source')})
        else:
            return reverse("source-home",
                           kwargs={"user": self.user_id,
                                   'source': self.kwargs.get('source')})


    def clean_concept_id(self, request, concept_id):
        """ concept ID must be unique
        """

        api = OCLapi(request, debug=True)
        result = api.get(
            self.owner_type, self.owner_id, 'sources', self.source_id,
            'concepts', concept_id)
        if result.status_code == 200:
            return _('This Concept ID is already used.')
        else:
            return None


    def add(self):
        """Create new concept
        """

        print self.request_json
        data = {}
        data['id'] = self.request_json.get('concept_id')
        msg = self.clean_concept_id(self.request, data['id'])
        if msg is not None:
            return self.render_bad_request_response({'message': msg})

        data['concept_class'] = self.request_json.get('concept_class')
        data['datatype'] = self.request_json.get('datatype')
        data['external_id'] = self.request_json.get('external_id')

        name = {}
        name['name'] = self.request_json.get('name')
        name['locale'] = self.request_json.get('locale')
        name['preferred'] = self.request_json.get('preferred_locale')
        name['name_type'] = self.request_json.get('name_type')
        names = [name]

        # TEMP for faster testing
        # return self.render_json_response({'message': _('Concept created')})

        api = OCLapi(self.request, debug=True)
        result = api.create_concept(
            self.owner_type, self.owner_id, self.source_id, data, names=names)
        if result.status_code != 201:
            logger.warning('Concept create POST failed: %s' % result.content)
            return self.render_bad_request_response({'message': result.content})
        else:
            # TODO: If successful, redirect browser to new concept details page
            return self.render_json_response({'message': _('Concept created!')})


    def edit(self):
        """Edit concept
        """

        data = {}
        data['concept_class'] = self.request_json.get('concept_class')
        data['datatype'] = self.request_json.get('datatype')
        data['external_id'] = self.request_json.get('external_id')
        data['update_comment'] = self.request_json.get('update_comment')
        print data
        # TEMP for faster testing
        # return self.render_json_response({'message': _('Concept updated')})

        api = OCLapi(self.request, debug=True)
        result = api.update_concept(
            self.owner_type, self.owner_id, self.source_id,
            self.concept_id, data)
        if result.status_code != requests.codes.ok:
            emsg = result.json().get('detail', 'Error')
            logger.warning('Concept update POST failed %s' % emsg)
            return self.render_bad_request_response({'message': emsg})
        else:
            # TODO: If successful, redirect browser to concept details page
            return self.render_json_response({'message': _('Concept updated!')})


    def post(self, *args, **kwargs):
        """Post create or new concept
        """

        self.get_args()
        print self.args_string()

        if self.concept_id is not None:
            return self.edit()
        else:
            return self.add()


class ConceptRetireView(UserOrOrgMixin, FormView):
    """View for retiring a concept. This is like a logical delete.
    """

    form_class = ConceptRetireForm
    template_name = "concepts/concept_retire.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ConceptRetireView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OCLapi(self.request, debug=True)
        source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()
        context['source'] = source
        concept = api.get(
            self.owner_type, self.owner_id, 'sources', self.source_id,
            'concepts', self.concept_id).json()
        context['concept'] = concept
        return context

    def get_success_url(self):
        if self.from_org:
            return reverse('concept-detail',
                           kwargs={"org": self.org_id,
                                   'source': self.source_id,
                                   'concept': self.concept_id})

        else:
            return reverse('concept-detail',
                           kwargs={"user": self.user_id,
                                   'source': self.source_id,
                                   'concept': self.concept_id})

    def form_valid(self, form, *args, **kwargs):

        self.get_args()
        print form.cleaned_data

        data = {'update_comment': form.cleaned_data['comment']}
        api = OCLapi(self.request, debug=True)
        result = api.delete(
            self.owner_type, self.owner_id, 'sources', self.source_id, 'concepts',
            self.concept_id, **data)
        print result
        if result.status_code != 204:
            print result.status_code
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        else:
            messages.add_message(self.request, messages.INFO, _('Concept retired'))
            return HttpResponseRedirect(self.get_success_url())


class ConceptCreateView(UserOrOrgMixin, FormView):
    """
        This is not used anymore. See the Json version.
    """
    form_class = ConceptCreateForm
    template_name = "concepts/concept_create.html"

    def get_success_url(self):
        if self.from_org:
            return reverse("source-home",
                           kwargs={"org": self.org_id,
                                   'source': self.kwargs.get('source')})
        else:
            return reverse("source-home",
                           kwargs={"user": self.user_id,
                                   'source': self.kwargs.get('source')})

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form
        """

        context = super(ConceptCreateView, self).get_context_data(*args, **kwargs)

        print 'get context...'

        self.get_args()
        source_id = self.kwargs.get('source')

        api = OCLapi(self.request, debug=True)
        print 'org id etc', self.org_id, self.from_org, source_id

        if self.from_org:
            source = api.get('orgs', self.org_id, 'sources', source_id).json()
        else:
            source = api.get('users', self.user_id, 'sources', source_id).json()

        context['source'] = source
        return context

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use
        """

        self.get_args()
        source_id = self.kwargs.get('source')

        api = OCLapi(self.request, debug=True)
        if self.from_org:
            source = api.get('orgs', self.org_id, 'sources', source_id).json()
        else:
            source = api.get('users', self.user_id, 'sources', source_id).json()

        data = {
            'source': source,
            'request': self.request,
        }
        return data

    def form_valid(self, form, *args, **kwargs):
        """Form validator
        """

        self.get_args()
        source_id = self.kwargs.get('source')

        print form.cleaned_data

        data = {}
        data['id'] = form.cleaned_data['concept_id']
        data['concept_class'] = form.cleaned_data['concept_class']
        data['datatype'] = form.cleaned_data['datatype']

        name = {}
        name['name'] = form.cleaned_data['name']
        name['name_type'] = form.cleaned_data['name_type']
        name['locale'] = form.cleaned_data['locale']
        name['preferred'] = form.cleaned_data['preferred_locale']
        names = [name]

        api = OCLapi(self.request, debug=True)
        if self.from_org:
            result = api.create_concept('orgs', self.org_id, source_id, data, names=names)
        else:
            result = api.create_concept('users', self.user_id, source_id, data, names=names)
        if result.status_code != 201:
            print result.status_code
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        else:
            print result.status_code
            print result.json()
            messages.add_message(self.request, messages.INFO, _('Concept Added'))
            return HttpResponseRedirect(self.get_success_url())


class ConceptEditView(UserOrOrgMixin, FormView):
    """
        This is not used anymore. See the Json version.
    """
    template_name = "concepts/concept_edit.html"

    def get_form_class(self):
        """ A sneaky way to hook into the generic form processing view, to
            grep arguments from the URL, retrieve some application data and store them
            in the view.
        """
        self.get_args()
        self.source_id = self.kwargs.get('source')
        self.concept_id = self.kwargs.get('concept')

        api = OCLapi(self.request, debug=True)

        if self.from_org:
            self.source = api.get('orgs', self.org_id, 'sources', self.source_id).json()
            self.concept = api.get(
                'orgs', self.org_id, 'sources', self.source_id,
                'concepts', self.concept_id).json()
        else:
            self.source = api.get('users', self.user_id, 'sources', self.source_id).json()
            self.concept = api.get(
                'users', self.user_id, 'sources', self.source_id,
                'concepts', self.concept_id).json()
        return ConceptEditForm

    def get_success_url(self):
        """Get success URL
        """
        if self.from_org:
            return reverse("concept-detail",
                           kwargs={"org": self.org_id,
                                   'source': self.kwargs.get('source'),
                                   'concept': self.concept_id})
        else:
            return reverse("concept-detail",
                           kwargs={"user": self.user_id,
                                   'source': self.kwargs.get('source'),
                                   'concept': self.concept_id})

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form
        """
        context = super(ConceptEditView, self).get_context_data(*args, **kwargs)

        self.get_args()

        context['source'] = self.source
        context['concept'] = self.concept
        return context

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        self.get_args()
        data = {
            'source': self.source,
            'concept': self.concept,
            'request': self.request,
        }
        data.update(self.concept)
        return data

    def form_valid(self, form, *args, **kwargs):

        self.get_args()

        data = form.cleaned_data

        api = OCLapi(self.request, debug=True)
        if self.from_org:
            result = api.update_concept('orgs', self.org_id, self.source_id, self.concept_id, data)
        else:
            result = api.update_concept(
                'users', self.user_id, self.source_id, self.concept_id, data)
        if result.status_code != requests.codes.ok:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        else:
            messages.add_message(self.request, messages.INFO, _('Concept updated'))
            return HttpResponseRedirect(self.get_success_url())


class ConceptDetailView(UserOrOrgMixin, TemplateView):
    """
    Display concept detail.
    """
    template_name = "concepts/concept_detail.html"

    def get_all_args(self):
        """ Get all input parameters for view.
        """
        self.get_args()

        api = OCLapi(self.request, debug=True)

        self.source = api.get_json(self.owner_type, self.owner_id, 'sources',
                                   self.source_id)
        self.concept = api.get_json(self.owner_type, self.owner_id, 'sources',
                                    self.source_id, 'concepts', self.concept_id)
        return

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form
        """
        self.get_all_args()
        context = super(ConceptDetailView, self).get_context_data(*args, **kwargs)

        context['source'] = self.source
        context['concept'] = self.concept
        return context


class ConceptVersionListView(CsrfExemptMixin, JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
    Return json concept versions.
    """

    def get_all_args(self):
        """ Get all input parameters for view.
        """
        self.get_args()
#        self.source_id = self.kwargs.get('source')
#        self.concept_id = self.kwargs.get('concept')

    def get(self, request, *args, **kwargs):
        """
            Return a list of versions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(self.owner_type, self.owner_id, 'sources', self.source_id,
                         'concepts', self.concept_id, 'versions')
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(result.json())


class ConceptItemView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """Interface to AngularJS concept description operations,
    supporting list, add, update and delete.
    """
    # override this, set to 'descriptions', 'names', etc
    item_name = None
    kwarg_name = None
    field_names = []
    optional = None

    def get_all_args(self):
        """
        Get all the input entities' identity, figure out whether this is a user owned
        sourced concept or an org owned sourced concept, and set self.owner_type, self.owner_id
        for easy interface to OCL API.
        """
        self.get_args()
        self.item_id = self.kwargs.get(self.kwarg_name)

    def is_edit(self):
        return self.item_id is not None

    def get(self, request, *args, **kwargs):
        """
            Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        if self.optional:
            result = api.get(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'concepts', self.concept_id, self.item_name, params=self.optional)
        else:
            result = api.get(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'concepts', self.concept_id, self.item_name)


        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(result.json())

    def post(self, request, *args, **kwargs):

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
            if self.item_name == 'mappings':
                result = api.put(
                    self.owner_type, self.owner_id, 'sources', self.source_id,
                    self.item_name, **data)
            else:
                result = api.put(
                    self.owner_type, self.owner_id, 'sources', self.source_id,
                    'concepts', self.concept_id, self.item_name, self.item_id, **data)
            msg = _('updated')
        else:
            if self.item_name == 'mappings':
                result = api.post(
                    self.owner_type, self.owner_id, 'sources', self.source_id,
                    self.item_name, **data)
            else:
                result = api.post(
                    self.owner_type, self.owner_id, 'sources', self.source_id,
                    'concepts', self.concept_id, self.item_name, **data)
            msg = _('added')

        if not result.ok:
            logger.warning('Update failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': msg})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified item.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)
        if self.is_edit():  # i.e. has item UUID
            result = api.delete(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'concepts', self.concept_id, self.item_name, self.item_id)
        if not result.ok:
            logger.warning('DEL failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response(
            {'message': _('deleted')})


class ConceptDescView(ConceptItemView):
    item_name = 'descriptions'
    kwarg_name = 'description'
    field_names = ['description', 'description_type', 'external_id', 'locale', 'locale_preferred']


class ConceptNameView(ConceptItemView):
    item_name = 'names'
    kwarg_name = 'name'
    field_names = ['name', 'name_type', 'external_id', 'locale', 'locale_preferred']


class ConceptExtraView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """Concept extras handling is different from descriptions and names.
    So the view is similar to the ConceptItemView but not the same.

    The extras field name IS the attribute name, the data is stored as a dictionary.
    So in this view, we translate the API style of data to be like descriptions and names.
    e.g.:

    API version:   {'price': 100}
    front end version: {extra_name: 'price', extra_value: 100}
    """

    item_name = 'extras'  # used in calling API URL
    kwarg_name = 'extra'  # used in extracting unique ID from front end.

    def get_all_args(self):
        """
        Get all the input entities' identity, figure out whether this is a user owned
        sourced concept or an org owned sourced concept, and set self.owner_type, self.owner_id
        for easy interface to OCL API.
        """
        self.get_args()
        self.item_id = self.kwargs.get(self.kwarg_name)

    def is_edit(self):
        return self.item_id is not None

    def get(self, request, *args, **kwargs):
        """Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(self.owner_type, self.owner_id, 'sources', self.source_id,
                         'concepts', self.concept_id, self.item_name)
        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        # convert OCLAPI dictionary style data to a list of dictionary objects
        # so that we can use the same front end JS to work with extras.
        ls = []
        for k, v in result.json().iteritems():
            print k, v
            o = {'extra_name': k, 'extra_value': v}
            ls.append(o)

        return self.render_json_response(ls)

    def post(self, request, *args, **kwargs):

        self.get_all_args()

        # Convert back to OCLAPI format for extras, the dictionnary
        # key is the attribute name.
        data = {}
        fn = fv = None
        try:
            print 'request json:', self.request_json
            fn = self.request_json.get('extra_name')
            fv = self.request_json.get('extra_value')
            data[fn] = fv
        except KeyError:
            resp = {'message': _('Invalid input')}
            return self.render_bad_request_response(resp)

        api = OCLapi(self.request, debug=True)
        if self.is_edit():
            result = api.put(self.owner_type, self.owner_id, 'sources', self.source_id,
                             'concepts', self.concept_id, 'extras', fn,
                             **data)
            msg = _('Extra updated')
        else:
            result = api.put(self.owner_type, self.owner_id, 'sources', self.source_id,
                             'concepts', self.concept_id, 'extras', fn, **data)
            msg = _('Extra added')

        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)
        else:
            return self.render_json_response({'message': msg})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified item.
        """
        self.get_all_args()

        api = OCLapi(self.request, debug=True)
        self.item_id = None
        if not self.is_edit():  # i.e. has item UUID
            return self.render_bad_request_response({'message': 'key missing'})

        result = api.delete(self.owner_type, self.owner_id, 'sources', self.source_id,
                            'concepts', self.concept_id,
                            self.item_name, self.item_id)
        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': _('extra deleted')})


class ConceptMappingView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
        Interface to front end json Mappings operations, supporting list, add, update and delete.

    """
    field_names = ['map_type', 'external_id', 'from_concept_url', 'to_concept_url',
                   'to_source_url', 'to_concept_code', 'to_concept_name']

    def get_all_args(self):
        """
        Get all the input entities' identity, figure out whether this is a user owned
        sourced concept or an org owned sourced concept, and set self.owner_type, self.owner_id
        for easy interface to OCL API.
        """
        self.get_args()
        self.item_id = self.kwargs.get('mapping')

    def is_edit(self):
        return self.item_id is not None

    def get(self, request, *args, **kwargs):
        """
            Return a list of mappings as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        # Note: value must be lowercase string "true", not boolean
        result = api.get(self.owner_type, self.owner_id, 'sources', self.source_id,
                         'concepts', self.concept_id, 'mappings',
                         params={'includeInverseMappings': 'true'})
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(result.json())

    def post(self, request, *args, **kwargs):
        """
        Post a new mapping
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
            # Somehow we get more data fields from the lookup  then
            # what the update will accept
            if data['to_concept_url']:
                data.pop('to_source_url', None)
                data.pop('to_concept_code', None)
                data.pop('to_concept_name', None)

            result = api.put(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'mappings', self.item_id, **data)
            msg = _('updated')
        else:
            result = api.post(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'mappings', **data)
            msg = _('added')

        if not result.ok:
            logger.warning('Update failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': msg})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified item.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)
        if self.is_edit():  # i.e. has item UUID
            result = api.delete(self.owner_type, self.owner_id, 'sources', self.source_id,
                                'mappings', self.item_id)
        if not result.ok:
            logger.warning('DEL failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response(
            {'message': _('deleted')})
