"""
OCL Concept Views
"""
import re
import requests
import logging

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import (View, FormView)
from django.http import (HttpResponseRedirect, Http404)
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from apps.core.views import _get_locale_list, _get_name_type_list, _get_description_type_list, _get_map_type_list
import json
# from django.core.paginator import Paginator

from braces.views import (LoginRequiredMixin, JsonRequestResponseMixin)
# from braces.views importCsrfExemptMixin

from .forms import (ConceptNewForm, ConceptEditForm, ConceptNewMappingForm, ConceptRetireForm)
from libs.ocl import OclApi, OclSearch, OclConstants
from apps.core.views import UserOrOrgMixin
from itertools import chain

logger = logging.getLogger('oclweb')


class ConceptReadBaseView(TemplateView):
    """ Base class for Concept Read views. """

    def get_concept_details(self, owner_type, owner_id, source_id, concept_id,
                            source_version_id=None, concept_version_id=None,
                            include_mappings=False, include_inverse_mappings=False):
        """ Get the concept details. """
        # TODO(paynejd@gmail.com): Validate input parameters

        # Setup request parameters
        params = {}
        if include_mappings:
            params['includeMappings'] = 'true'
            params['verbose'] = 'true'
        if include_inverse_mappings:
            params['includeInverseMappings'] = 'true'
            params['verbose'] = 'true'

        # Perform the search
        api = OclApi(self.request, debug=True)
        if source_version_id and concept_version_id:
            raise ValueError(
                'Must specify only a source version or a concept version. Both were specified.')
        elif source_version_id:
            search_response = api.get(
                owner_type, owner_id,
                'sources', source_id, source_version_id,
                'concepts', concept_id,
                params=params)
        elif concept_version_id:
            search_response = api.get(
                owner_type, owner_id,
                'sources', source_id,
                'concepts', concept_id, concept_version_id,
                params=params)
        else:
            search_response = api.get(
                owner_type, owner_id,
                'sources', source_id,
                'concepts', concept_id,
                params=params)
        if search_response.status_code == 404:
            raise Http404(search_response.text)
        elif search_response.status_code != 200:
            search_response.raise_for_status()
        return search_response.json()

    def get_concept_history(self, owner_type, owner_id, source_id, concept_id,
                            search_params=None):
        """
        Get the concept version history.
        Note that source_version_id and concept_version_id are not applied here.
        """
        # TODO(paynejd@gmail.com): Validate input parameters

        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_CONCEPT_VERSIONS,
                             search_scope=OclConstants.SEARCH_SCOPE_RESTRICTED,
                             params=search_params)
        api = OclApi(self.request, debug=True, facets=False)
        search_response = api.get(
            owner_type, owner_id, 'sources', source_id,
            'concepts', concept_id, 'versions')
        if search_response.status_code == 404:
            raise Http404
        elif search_response.status_code != 200:
            search_response.raise_for_status()

        # Process the results
        searcher.process_search_results(
            search_type=searcher.search_type, search_response=search_response,
            search_params=search_params)

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

        api = OclApi(self.request, debug=True, facets=True)

        # Load the concept details
        concept = self.get_concept_details(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id,
            include_mappings=True, include_inverse_mappings=True)

        concept['has_direct_mappings'] = False
        concept['has_inverse_mappings'] = False
        if 'mappings' in concept and concept['mappings']:
            for mapping in concept['mappings']:
                if (self.proper_owner_type == mapping['to_source_owner_type'] and
                        self.owner_id == mapping['to_source_owner'] and
                        self.source_id == mapping['to_source_name'] and
                        self.concept_id == mapping['to_concept_code']):
                    mapping['is_inverse_mapping'] = True
                    concept['has_inverse_mappings'] = True
                    mapping['is_direct_mapping'] = False
                else:
                    mapping['is_direct_mapping'] = True
                    mapping['is_inverse_mapping'] = False
                    concept['has_direct_mappings'] = True
                if mapping['to_concept_url']:
                    mapping['is_internal_mapping'] = True
                    mapping['is_external_mapping'] = False
                else:
                    mapping['is_internal_mapping'] = False
                    mapping['is_external_mapping'] = True

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Details'
        context['concept'] = concept

        return context


class ConceptMappingsView(FormView, UserOrOrgMixin,
                          ConceptReadBaseView):
    """
    View for seeing all mappings for the current concept,
    and creating a new mapping with this as the from_concept.
    """

    form_class = ConceptNewMappingForm
    template_name = "concepts/concept_mappings.html"

    def get_initial(self):
        """ Set the owner and source args for use in the form """

        data = super(ConceptMappingsView, self).get_initial()

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
        """ Loads the concept details. """

        # Setup the context and args
        context = super(ConceptMappingsView, self).get_context_data(*args, **kwargs)
        self.get_args()

        api = OclApi(self.request, debug=True, facets=True)

        # Load the concept details
        concept = self.get_concept_details(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id,
            include_mappings=True, include_inverse_mappings=True)

        # Process mappings relative to current concept
        # TODO(paynejd@gmail.com): Move processing code to concept/mapping class objects
        mappings = {
            'Direct Internal Mapping': [],
            'Direct External Mapping': [],
            'Inverse Mapping': [],
            'Linked Answer': [],
            'Linked Question': [],
            'Set Member': [],
            'Set Parent': [],
            'Other': [],
        }
        if 'mappings' in concept and concept['mappings']:
            for mapping in concept['mappings']:
                mapping['is_direct_mapping'] = False
                mapping['is_inverse_mapping'] = False
                mapping['is_internal_mapping'] = False
                mapping['is_external_mapping'] = False
                mapping['mapping_category'] = None
                mapping['to_url'] = None
                mapping['from_url'] = None
                mapping['mapping_url'] = None

                # TODO: Set the mapping_url
                mapping_url_args = {}
                if mapping['owner_type'] == 'Organization':
                    mapping_url_args['org'] = mapping['owner']
                else:
                    mapping_url_args['user'] = mapping['owner']
                mapping_url_args['source'] = mapping['source']
                mapping_url_args['mapping'] = mapping['id']
                mapping['mapping_url'] = reverse('mapping-home', kwargs=mapping_url_args)

                # this concept == from_concept
                if (self.proper_owner_type == mapping['from_source_owner_type'] and
                            self.owner_id == mapping['from_source_owner'] and
                            self.source_id == mapping['from_source_name'] and
                            self.concept_id == mapping['from_concept_code']):

                    # Setup the arguments to reverse to_concept URL - URL reversed in next block
                    to_concept_url_args = {}
                    if mapping['to_source_owner_type'] == 'Organization':
                        to_concept_url_args['org'] = mapping['to_source_owner']
                    else:
                        to_concept_url_args['user'] = mapping['to_source_owner']
                    to_concept_url_args['source'] = mapping['to_source_name']

                    # Set mapping attributes relative to the current concept
                    mapping['is_direct_mapping'] = True
                    if mapping['to_concept_url']:
                        mapping['is_internal_mapping'] = True
                        to_concept_url_args['concept'] = mapping['to_concept_code']
                        mapping['to_url'] = reverse('concept-home', kwargs=to_concept_url_args)
                    else:
                        mapping['is_external_mapping'] = True
                        mapping['to_url'] = reverse('source-home', kwargs=to_concept_url_args)

                    # Determine the mapping category relative to current concept
                    if mapping['map_type'] == 'Q-AND-A':
                        mapping['mapping_category'] = 'Linked Answer'
                        mappings['Linked Answer'].append(mapping)
                    elif mapping['map_type'] == 'CONCEPT-SET':
                        mapping['mapping_category'] = 'Set Member'
                        mappings['Set Member'].append(mapping)
                    elif mapping['to_concept_url']:
                        mapping['mapping_category'] = 'Direct Internal Mapping'
                        mappings['Direct Internal Mapping'].append(mapping)
                    else:
                        mapping['mapping_category'] = 'Direct External Mapping'
                        mappings['Direct External Mapping'].append(mapping)

                # this concept == to_concept (internal mapping)
                elif (self.proper_owner_type == mapping['to_source_owner_type'] and
                              self.owner_id == mapping['to_source_owner'] and
                              self.source_id == mapping['to_source_name'] and
                              self.concept_id == mapping['to_concept_code']):

                    # Setup the arguments to reverse from_concept URL - which must be in OCL
                    from_concept_url_args = {}
                    if mapping['from_source_owner_type'] == 'Organization':
                        from_concept_url_args['org'] = mapping['from_source_owner']
                    else:
                        from_concept_url_args['user'] = mapping['from_source_owner']
                    from_concept_url_args['source'] = mapping['from_source_name']
                    from_concept_url_args['concept'] = mapping['from_concept_code']
                    mapping['from_url'] = reverse('concept-home', kwargs=from_concept_url_args)

                    # Set mapping attributes relative to the current concept
                    mapping['is_inverse_mapping'] = True
                    mapping['is_internal_mapping'] = True

                    # Determine the mapping category
                    if mapping['map_type'] == 'Q-AND-A':
                        mapping['mapping_category'] = 'Linked Question'
                        mappings['Linked Question'].append(mapping)
                    elif mapping['map_type'] == 'CONCEPT-SET':
                        mapping['mapping_category'] = 'Set Parent'
                        mappings['Set Parent'].append(mapping)
                    else:
                        mapping['mapping_category'] = 'Inverse Mapping'
                        mappings['Inverse Mapping'].append(mapping)

                # this concept != from_concept or to_concept! something's wrong
                else:
                    mapping['mapping_category'] = 'Other'
                    mappings['Other'].append(mapping)

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Mappings'
        context['concept'] = concept
        context['mappings'] = mappings
        context['form'] = ConceptNewMappingForm()
        context['map_types'] = _get_map_type_list()

        return context

    def form_valid(self, form, *args, **kwargs):
        """ Submits the validated form data: A new Concept Mapping """

        # Prepare the data form submission, incl. renaming fields as needed
        mapping_destination = form.cleaned_data.get('is_internal_or_external')
        from_concept_url = ('/' + self.owner_type + '/' + self.owner_id + '/sources/' +
                            self.source_id + '/concepts/' + self.concept_id + '/')
        base_data = {
            'from_concept_url': from_concept_url,
            'map_type': form.cleaned_data.get('map_type', ''),
            'external_id': form.cleaned_data.get('external_id', '')
        }
        if mapping_destination == 'Internal':
            base_data['to_concept_url'] = form.cleaned_data.get('internal_to_concept_url')
            # TODO: move regex validation to form
            user_concept_format = r'^/users/(' + OclConstants.NAMESPACE_PATTERN + ')/sources/(' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(' + OclConstants.CONCEPT_ID_PATTERN + ')/$'
            org_concept_format = r'^/orgs/(' + OclConstants.ORG_PATTERN + ')/sources/(' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(' + OclConstants.CONCEPT_ID_PATTERN + ')/$'
            if not (re.compile(user_concept_format).match(base_data['to_concept_url']) or
                        re.compile(org_concept_format).match(base_data['to_concept_url'])):
                emsg = 'Invalid format of "To Concept URL" \'%s\'. valid url format is /[orgs or users]/[:org or :user]/sources/:source/concepts/:concept/' % \
                       base_data['to_concept_url']
                messages.add_message(self.request, messages.ERROR, emsg)
                return super(ConceptMappingsView, self).form_invalid(form)
        elif mapping_destination == 'External':
            base_data['to_source_url'] = form.cleaned_data.get('external_to_source_url')
            base_data['to_concept_code'] = form.cleaned_data.get('external_to_concept_code')
            base_data['to_concept_name'] = form.cleaned_data.get('external_to_concept_name')

        # Create the mapping
        api = OclApi(self.request, debug=True)
        result = api.create_mapping(self.owner_type, self.owner_id, self.source_id, base_data)
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Mapping created.'))
            if self.from_org:
                return redirect(reverse('concept-mappings',
                                        kwargs={'org': self.owner_id,
                                                'source': self.source_id,
                                                'concept': self.concept_id}))
            else:
                return redirect(reverse('concept-mappings',
                                        kwargs={'user': self.owner_id,
                                                'source': self.source_id,
                                                'concept': self.concept_id}))
        else:
            emsg = result.json().get('errors', 'Error: ' + result.content)
            messages.add_message(self.request, messages.ERROR, emsg)
            logger.warning('Mapping create POST failed: %s' % result.content)
            return super(ConceptMappingsView, self).form_invalid(form)


# CLEAN
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

        api = OclApi(self.request, debug=True, facets=True)

        # Load the concept details
        concept = self.get_concept_details(
            self.owner_type, self.owner_id, self.source_id, self.concept_id,
            source_version_id=self.source_version_id, concept_version_id=self.concept_version_id)

        # Load the concept version history
        searcher = self.get_concept_history(
            self.owner_type, self.owner_id, self.source_id, self.concept_id)
        # search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        # search_results_current_page = search_results_paginator.page(searcher.current_page)

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'History'
        context['concept'] = concept
        context['concept_versions'] = searcher.search_results
        # context['current_page'] = search_results_current_page
        # context['pagination_url'] = self.request.get_full_path()

        return context


# CLEAN
class ConceptNewView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """
    View to create new concept
    """
    form_class = ConceptNewForm
    template_name = "concepts/concept_new.html"

    def get_initial(self):
        """ Set the owner and source args for use in the form """

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
        """ Loads the context data for creating a new concept. """

        # Setup the form context
        context = super(ConceptNewView, self).get_context_data(*args, **kwargs)
        self.get_args()

        # Load the source that the new concept will belong to
        api = OclApi(self.request, debug=True)
        source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()

        # TODO: Load list of names types
        # TODO: Load list of description types
        # TODO: Load list of locales
        # TODO: Load list of datatypes
        # TODO: Load list of concept classes

        # Set the context
        context['kwargs'] = self.kwargs
        context['source'] = source
        context['locales'] = json.dumps(_get_locale_list())
        context['name_types'] = json.dumps(_get_name_type_list())
        context['description_types'] = json.dumps(_get_description_type_list())

        names = [
            {'name': '', 'locale': source['default_locale'], 'locale_preferred': True, 'name_type': 'Fully Specified'}]

        descriptions = [{'description': '', 'locale': source['default_locale'], 'locale_preferred': True,
                         'description_type': 'None'}]

        extras = [{'key': '', 'value': ''}]

        if self.request.method == 'POST':
            names = json.loads(self.request.POST.get('names'))
            descriptions = json.loads(self.request.POST.get('descriptions'))
            extras = json.loads(self.request.POST.get('extras'))

        context['names'] = json.dumps(names)
        context['descriptions'] = json.dumps(descriptions)
        context['extras'] = json.dumps(extras)

        return context

    def form_valid(self, form, *args, **kwargs):
        """ Submits the validated form data: A new Concept """

        # Prepare the data for submission, incl. renaming fields as needed
        concept_id = form.cleaned_data.pop('concept_id')
        base_data = {
            'id': concept_id,
            'concept_class': form.cleaned_data.get('concept_class'),
            'datatype': form.cleaned_data.get('datatype'),
            'external_id': form.cleaned_data.get('external_id', '')
        }

        names = json.loads(
            self.request.POST.get('names', [])
        )
        try:
            descriptions = json.loads(self.request.POST.get('descriptions', []))
        except ValueError:
            descriptions = None

        extras = {}
        if 'extras' in self.request.POST:
            extras_dict_list = json.loads(self.request.POST.get('extras'))
            for item in extras_dict_list:
                if item['key']:
                    extras[item['key']] = item['value']

        # Create new concept using the API
        api = OclApi(self.request, debug=True)
        result = api.create_concept(
            self.owner_type, self.owner_id, self.source_id, base_data,
            names=names, descriptions=descriptions, extras=extras)

        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Concept created.'))
            if self.from_org:
                return redirect(reverse('concept-details',
                                        kwargs={'org': self.owner_id,
                                                'source': self.source_id,
                                                'concept': concept_id}))
            else:
                return redirect(reverse('concept-details',
                                        kwargs={'user': self.owner_id,
                                                'source': self.source_id,
                                                'concept': concept_id}))
        else:
            errors = list(chain.from_iterable(json.loads(result.content).values()))
            messages.add_message(self.request, messages.ERROR,
                                 _("\n".join(errors)))
            logger.warning('Concept create POST failed: %s' % result.content)
            return super(ConceptNewView, self).form_invalid(form)


# TODO(paynejd@gmail.com): Retire ConceptCreateJsonView ASAP
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
        api = OclApi(self.request, debug=True)
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

        api = OclApi(request, debug=True)
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
        name['description'] = self.request_json.get('description')
        name['locale'] = self.request_json.get('locale')
        name['preferred'] = self.request_json.get('preferred_locale')
        name['description_type'] = self.request_json.get('description_type')
        names = [name]

        # TEMP for faster testing
        # return self.render_json_response({'message': _('Concept created')})

        api = OclApi(self.request, debug=True)
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

        api = OclApi(self.request, debug=True)
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


# CLEAN
class ConceptRetireView(UserOrOrgMixin, FormView):
    """
    View for retiring a concept.
    """

    form_class = ConceptRetireForm
    template_name = "concepts/concept_retire.html"

    def get_context_data(self, *args, **kwargs):
        """ Set context data for retiring the concept """
        context = super(ConceptRetireView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OclApi(self.request, debug=True)
        source = api.get(self.owner_type, self.owner_id, 'sources', self.source_id).json()
        concept = api.get(
            self.owner_type, self.owner_id, 'sources', self.source_id,
            'concepts', self.concept_id).json()
        context['source'] = source
        context['concept'] = concept
        context['kwargs'] = self.kwargs
        return context

    def get_success_url(self):
        """ Return URL for redirecting browser """
        if self.from_org:
            return reverse('concept-details',
                           kwargs={'org': self.org_id,
                                   'source': self.source_id,
                                   'concept': self.concept_id})

        else:
            return reverse('concept-details',
                           kwargs={'user': self.user_id,
                                   'source': self.source_id,
                                   'concept': self.concept_id})

    def form_valid(self, form, *args, **kwargs):
        """ Use validated form data to retire the concept """

        self.get_args()
        data = {'update_comment': form.cleaned_data['comment']}
        api = OclApi(self.request, debug=True)
        result = api.delete(
            self.owner_type, self.owner_id, 'sources', self.source_id, 'concepts',
            self.concept_id, **data)
        if result.status_code != 204:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        else:
            messages.add_message(self.request, messages.INFO, _('Concept retired'))
            return HttpResponseRedirect(self.get_success_url())


# CLEAN
class ConceptEditView(UserOrOrgMixin, FormView):
    """
    View to edit core concept data (class, datatype, external-id)
    """

    template_name = "concepts/concept_edit.html"

    def get_form_class(self):
        """
        A sneaky way to hook into the generic form processing view, to grep args
        from the URL, retrieve some application data and store them in the view.
        """
        self.get_args()
        self.source_id = self.kwargs.get('source')
        self.concept_id = self.kwargs.get('concept')

        api = OclApi(self.request, debug=True)

        if self.from_org:
            self.source = api.get(
                self.owner_type, self.org_id, 'sources', self.source_id).json()
            self.concept = api.get(
                self.owner_type, self.org_id, 'sources', self.source_id,
                'concepts', self.concept_id).json()
        else:
            self.source = api.get(
                self.owner_type, self.user_id, 'sources', self.source_id).json()
            self.concept = api.get(
                self.owner_type, self.user_id, 'sources', self.source_id,
                'concepts', self.concept_id).json()

        return ConceptEditForm

    def get_success_url(self):
        """ Get success URL """
        if self.from_org:
            return reverse("concept-details",
                           kwargs={"org": self.org_id,
                                   'source': self.kwargs.get('source'),
                                   'concept': self.concept_id})
        else:
            return reverse("concept-details",
                           kwargs={"user": self.user_id,
                                   'source': self.kwargs.get('source'),
                                   'concept': self.concept_id})

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form """
        context = super(ConceptEditView, self).get_context_data(*args, **kwargs)

        self.concept['names'] = json.dumps(self.concept['names'])
        self.concept['descriptions'] = json.dumps(self.concept['descriptions'])

        self.get_args()
        temp = []
        if 'extras' in self.concept and self.concept['extras']:
            for key, value in self.concept.get('extras').iteritems():
                temp.append({'key': key, 'value': value})
            self.concept['extras'] = temp

        if self.request.method == 'POST':
            self.concept['names'] = self.request.POST.get('names')
            self.concept['descriptions'] = self.request.POST.get('descriptions')
            temp = json.loads(self.request.POST.get('extras'))

        context['kwargs'] = self.kwargs
        context['source'] = self.source
        context['concept'] = self.concept
        context['extras'] = json.dumps(temp)
        context['locales'] = json.dumps(_get_locale_list())
        context['name_types'] = json.dumps(_get_name_type_list())
        context['description_types'] = json.dumps(_get_description_type_list())

        return context

    def get_initial(self):
        """
        Load some useful data, not really for form display but internal use
        """
        self.get_args()
        data = {
            'source': self.source,
            'concept': self.concept,
            'request': self.request,
        }

        if self.concept['names']:
            data.update(self.concept['names'][0] if self.concept['names'] else {})
            data.update({
                'name_locale_preferred': data.pop('locale_preferred', False),
                'name_type': data.pop('name_type', None),
                'name_locale': data.pop('locale', None)
            })

        if self.concept['descriptions']:
            data.update(self.concept['descriptions'][0] if self.concept['descriptions'] else {})
            data.update({
                'description_locale_preferred': data.pop('locale_preferred', False),
                'description_type': data.pop('description_type', None),
                'description_locale': data.pop('locale', None)
            })

        data.update(self.concept)
        return data

    def form_valid(self, form, *args, **kwargs):
        """ Submit the edited concept data using the API """

        self.get_args()

        data = form.cleaned_data
        extras = {}
        if 'extras' in self.request.POST:
            extras_dict_list = json.loads(self.request.POST.get('extras'))
            for item in extras_dict_list:
                extras[item['key']] = item['value']
        data['extras'] = extras
        api = OclApi(self.request, debug=True)

        names = json.loads(
            self.request.POST.get('names', [])
        )

        try:
            descriptions = json.loads(self.request.POST.get('descriptions', []))
        except ValueError:
            descriptions = None

        if self.from_org:
            result = api.update_concept('orgs', self.org_id, self.source_id, self.concept_id, data, names, descriptions)
        else:
            result = api.update_concept(
                'users', self.user_id, self.source_id, self.concept_id, data, names, descriptions)
        if result.status_code != requests.codes.ok:
            data = result.json()
            emsg = data.get('detail')
            if not emsg:
                error_fields = data.keys()
                if 'non_field_errors' in error_fields:
                    error_fields.remove('non_field_errors')
                emsg = data[error_fields[0]][0]
            messages.add_message(self.request, messages.ERROR, emsg or 'Error')
            return super(ConceptEditView, self).form_invalid(form)
        else:
            messages.add_message(self.request, messages.INFO, _('Concept updated'))
            return HttpResponseRedirect(self.get_success_url())


# TODO(paynejd): Recreate ConceptItemView, ConceptDescView, ConceptNameView, and ConceptExtraView
# Currently, these are only used for fetching the JSON of concept names, descriptions, and extras
# They formerly handled Angular requests. Modify so that they support edits in the old Django way.

# TODO(paynejd): Resurrect ConceptItemView
class ConceptItemView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
    Interface to AngularJS concept description operations,
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
        """ Returns whether concept item is being edited or is new using self.item_id """
        return self.item_id is not None

    def get(self, request, *args, **kwargs):
        """
            Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OclApi(self.request, debug=True)

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
        """ Post the data """

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

        api = OclApi(self.request, debug=True)
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
        api = OclApi(self.request, debug=True)
        if self.is_edit():  # i.e. has item UUID
            result = api.delete(
                self.owner_type, self.owner_id, 'sources', self.source_id,
                'concepts', self.concept_id, self.item_name, self.item_id)
        if not result.ok:
            logger.warning('DEL failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response(
            {'message': _('deleted')})


# TODO(paynejd): Resurrect ConceptDescView
class ConceptDescView(ConceptItemView):
    """ Concept description view """
    item_name = 'descriptions'
    kwarg_name = 'description'
    field_names = ['description', 'description_type', 'external_id', 'locale', 'locale_preferred']


# TODO(paynejd): Resurrect ConceptNameView
class ConceptNameView(ConceptItemView):
    """ Concept name view """
    item_name = 'names'
    kwarg_name = 'name'
    field_names = ['name', 'name_type', 'external_id', 'locale', 'locale_preferred']


# TODO(paynejd): Resurrect ConceptExtraView
class ConceptExtraView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
    Concept extras handling is different from descriptions and names.
    So the view is similar to the ConceptItemView, but not the same.

    The extras field name IS the attribute name, the data is stored as a dictionary.
    So in this view, we translate the API style of data to be like descriptions and names.
    e.g.:

    API version:   {'price': 100}
    front-end version: {extra_name: 'price', extra_value: 100}
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
        """ Returns whether extra is being edited or is new using self.item_id """
        return self.item_id is not None

    def get(self, request, *args, **kwargs):
        """Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OclApi(self.request, debug=True)

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
        """ Post the form data """

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

        api = OclApi(self.request, debug=True)
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

        api = OclApi(self.request, debug=True)
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

# TODO(paynejd): Replace ConceptMappingView with Mapping*Views
# TODO(paynejd): Allow some mapping operations from the Concept Mappings page
# class ConceptMappingView(JsonRequestResponseMixin, UserOrOrgMixin, View):
#     """
#     Interface to front end json Mappings operations, supporting list, add, update and delete.
#     """
#     field_names = ['map_type', 'external_id', 'from_concept_url', 'to_concept_url',
#                    'to_source_url', 'to_concept_code', 'to_concept_name']

#     def get_all_args(self):
#         """
#         Get all the input entities' identity, figure out whether this is a user owned
#         sourced concept or an org owned sourced concept, and set self.owner_type, self.owner_id
#         for easy interface to OCL API.
#         """
#         self.get_args()
#         self.item_id = self.kwargs.get('mapping')

#     def is_edit(self):
#         return self.item_id is not None

#     def get(self, request, *args, **kwargs):
#         """
#             Return a list of mappings as json.
#         """
#         self.get_all_args()
#         api = OclApi(self.request, debug=True)

#         # Note: value must be lowercase string "true", not boolean
#         result = api.get(self.owner_type, self.owner_id, 'sources', self.source_id,
#                          'concepts', self.concept_id, 'mappings',
#                          params={'includeInverseMappings': 'true'})
#         if not result.ok:
#             print result
#             return self.render_bad_request_response(result)

#         return self.render_json_response(result.json())

#     def post(self, request, *args, **kwargs):
#         """
#         Post a new mapping
#         """

#         self.get_all_args()
#         data = {}
#         try:
#             print 'request json:', self.request_json
#             for n in self.field_names:
#                 # Skipping over fields that are not given -- exception is never thrown now...??
#                 v = self.request_json.get(n, None)
#                 if v is not None:
#                     data[n] = v
#         except KeyError:
#             resp = {u"message": _('Invalid input')}
#             return self.render_bad_request_response(resp)

#         api = OclApi(self.request, debug=True)
#         if self.is_edit():
#             # Somehow we get more data fields from the lookup  then
#             # what the update will accept
#             if data['to_concept_url']:
#                 data.pop('to_source_url', None)
#                 data.pop('to_concept_code', None)
#                 data.pop('to_concept_name', None)

#             result = api.put(
#                 self.owner_type, self.owner_id, 'sources', self.source_id,
#                 'mappings', self.item_id, **data)
#             msg = _('updated')
#         else:
#             result = api.post(
#                 self.owner_type, self.owner_id, 'sources', self.source_id,
#                 'mappings', **data)
#             msg = _('added')

#         if not result.ok:
#             logger.warning('Update failed %s' % result.content)
#             return self.render_bad_request_response(result.content)

#         return self.render_json_response({'message': msg})

#     def delete(self, request, *args, **kwargs):
#         """
#         Delete the specified item.
#         """
#         self.get_all_args()
#         api = OclApi(self.request, debug=True)
#         if self.is_edit():  # i.e. has item UUID
#             result = api.delete(self.owner_type, self.owner_id, 'sources', self.source_id,
#                                 'mappings', self.item_id)
#         if not result.ok:
#             logger.warning('DEL failed %s' % result.content)
#             return self.render_bad_request_response(result.content)

#         return self.render_json_response(
#             {'message': _('deleted')})
