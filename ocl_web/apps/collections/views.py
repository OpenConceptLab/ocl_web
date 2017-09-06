"""
OCL Collection views
"""
import logging
import re
from urllib import urlencode

import requests
import simplejson as json
from django.http import HttpResponseBadRequest

from apps.collections.validation_messages import POSTED_HEAD_VERSION_OF_SOURCE, POSTED_NON_HEAD_VERSION_OF_SOURCE, \
    ENTERED_WITH_VERSION_NUMBER_FOR_CONCEPT, ENTERED_WITH_VERSION_NUMBER_FOR_MAPPING, \
    ENTERED_WITHOUT_VERSION_NUMBER_FOR_CONCEPT, ENTERED_WITHOUT_VERSION_NUMBER_FOR_MAPPING, EXPRESSIONS_SHOULD_EXIST
from apps.core.utils import SearchStringFormatter
from apps.core.views import UserOrOrgMixin
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import (HttpResponseRedirect, Http404)
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from libs.ocl import OclApi, OclSearch, OclConstants

from .forms import (CollectionCreateForm, CollectionEditForm,
                    CollectionDeleteForm, CollectionVersionAddForm, CollectionVersionsEditForm)

logger = logging.getLogger('oclweb')


class CollectionsBaseView(UserOrOrgMixin):
    def get_args(self):
        super(CollectionsBaseView, self).get_args()
        self.collection_id = self.kwargs.get('collection')
        self.collection_version_id = self.kwargs.get('collection_version')

    def get_collection_data(self, owner_type, owner_id, collection_id, field_name,
                            collection_version_id=None, search_params=None):

        searcher = OclSearch(search_type=field_name,
                             search_scope=OclConstants.SEARCH_SCOPE_RESTRICTED,
                             params=search_params)
        api = OclApi(self.request, debug=True, facets=True)

        if collection_version_id:
            search_response = api.get(
                owner_type, owner_id, 'collections', collection_id,
                collection_version_id, field_name,
                params=searcher.search_params)
        else:
            search_response = api.get(
                owner_type, owner_id, 'collections', collection_id, field_name,
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

    def get_collection_versions(self, owner_type, owner_id, collection_id, search_params=None):
        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_COLLECTION_VERSIONS,
                             search_scope=OclConstants.SEARCH_SCOPE_RESTRICTED,
                             params=search_params)

        api = OclApi(self.request, debug=True, facets=False)
        search_response = api.get(owner_type, owner_id, 'collections', collection_id, 'versions',
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


class CollectionReferencesView(CollectionsBaseView, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_references.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionReferencesView, self).get_context_data(*args, **kwargs)
        self.get_args()

        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'

        versions = self.get_collection_versions(
            self.owner_type, self.owner_id, self.collection_id,
            search_params={'limit': '0'})

        # Load the references in this collection, applying search parameters
        original_search_string = self.request.GET.get('q', '')
        # TODO: SearchStringFormatter.add_wildcard(self.request)
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'
        searcher = self.get_collection_data(
            self.owner_type, self.owner_id, self.collection_id, 'references',
            collection_version_id=self.collection_version_id,
            search_params=params)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        add_reference_warning = self.request.session.get('add_reference_warning', None)
        add_reference_success = self.request.session.get('add_reference_success', None)
        self.request.session['add_reference_success'] = None
        self.request.session['add_reference_warning'] = None

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
        context['selected_tab'] = 'References'
        context['collection'] = collection
        context['collection_version'] = self.collection_version_id
        context['collection_versions'] = versions.search_results
        context['selected_tab'] = 'References'
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_sort_option_defs'] = searcher.get_sort_option_definitions()
        context['search_sort'] = self.request.GET.get('search_sort', 'ASC')
        context['search_query'] = searcher.get_query()
        context['search_filters'] = searcher.search_filter_list

        # Set debug variables
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)
        context['collection_versions'] = versions.search_results

        context['warning'] = add_reference_warning
        context['success'] = add_reference_success

        return context


class CollectionMappingsView(CollectionsBaseView, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_mappings.html"

    def get_context_data(self, *args, **kwargs):
        """ Loads the mappings that are in the collection. """

        # Setup the context and args
        context = super(CollectionMappingsView, self).get_context_data(*args, **kwargs)
        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()
        # to fetch all , set limit to 0
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'

        versions = self.get_collection_versions(
            self.owner_type, self.owner_id, self.collection_id,
            search_params={'limit': '0'})

        # Load the mappings in this collection, applying search parameters
        original_search_string = self.request.GET.get('q', '')
        # TODO: SearchStringFormatter.add_wildcard(self.request)
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'
        searcher = self.get_collection_data(
            self.owner_type, self.owner_id, self.collection_id,
            OclConstants.RESOURCE_NAME_MAPPINGS,
            collection_version_id=self.collection_version_id,
            search_params=params)

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
        context['selected_tab'] = 'Mappings'
        context['collection'] = collection
        context['collection_version'] = self.collection_version_id
        context['collection_versions'] = versions.search_results
        context['selected_tab'] = 'Mappings'
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_sort_option_defs'] = searcher.get_sort_option_definitions()
        context['search_sort'] = searcher.get_sort()
        context['search_query'] = searcher.get_query()
        context['search_filters'] = searcher.search_filter_list

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        # Set debug variables
        context['url_params'] = self.request.GET
        context['search_params'] = searcher.search_params
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)
        context['collection_versions'] = versions.search_results

        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.get_args()

            searcher = self.get_collection_data(
                self.owner_type, self.owner_id, self.collection_id,
                OclConstants.RESOURCE_NAME_MAPPINGS,
                collection_version_id=self.collection_version_id,
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
        return super(CollectionMappingsView, self).get(self, *args, **kwargs)


class CollectionConceptsView(CollectionsBaseView, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_concepts.html"

    def get_context_data(self, *args, **kwargs):
        """ Loads the concepts that are in the collection. """

        # Setup the context and args
        context = super(CollectionConceptsView, self).get_context_data(*args, **kwargs)
        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'

        # to fetch all , set limit to 0
        versions = self.get_collection_versions(
            self.owner_type, self.owner_id, self.collection_id,
            search_params={'limit': '0'})

        # Load the concepts in this collection, applying search parameters
        original_search_string = self.request.GET.get('q', '')
        # TODO: SearchStringFormatter.add_wildcard(self.request)
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'
        searcher = self.get_collection_data(
            self.owner_type, self.owner_id, self.collection_id, OclConstants.RESOURCE_NAME_CONCEPTS,
            collection_version_id=self.collection_version_id,
            search_params=params)

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
        context['selected_tab'] = 'Concepts'
        context['collection'] = collection
        context['collection_version'] = self.collection_version_id
        context['collection_versions'] = versions.search_results
        context['selected_tab'] = 'Concepts'
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_sort_option_defs'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_query'] = self.search_string if hasattr(self, 'search_string') else ''
        context['search_filters'] = searcher.search_filter_list
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)
        context['collection_versions'] = versions.search_results

        if self.request.user.is_authenticated():
            context['all_collections'] = api.get_all_collections_for_user(self.request.user.username)

        return context

    def get(self, request, *args, **kwargs):
        self.search_string = request.GET.get('q', '')
        SearchStringFormatter.add_wildcard(request)

        if request.is_ajax():
            self.get_args()
            # Load the concepts in this collection, applying search parameters
            searcher = self.get_collection_data(
                self.owner_type, self.owner_id, self.collection_id,
                OclConstants.RESOURCE_NAME_CONCEPTS,
                collection_version_id=self.collection_version_id,
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
        return super(CollectionConceptsView, self).get(self, *args, **kwargs)


class CollectionVersionsView(CollectionsBaseView, TemplateView):
    """ collection About view. """
    template_name = "collections/collection_versions.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionVersionsView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        # Load the collection versions
        params = self.request.GET.copy()
        params['verbose'] = 'true'
        params['limit'] = '10'
        searcher = self.get_collection_versions(
            self.owner_type, self.owner_id, self.collection_id,
            search_params=params)
        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        for collection_version in searcher.search_results:
            if '_ocl_processing' in collection_version and collection_version['_ocl_processing']:
                collection_version['is_processing'] = 'True'

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['selected_tab'] = 'Versions'
        context['collection'] = collection
        context['collection_versions'] = searcher.search_results

        return context

    def get(self, request, *args, **kwargs):
        self.get_args()
        if request.is_ajax():
            api = OclApi(self.request, debug=True)
            result = api.get(self.owner_type, self.owner_id, 'collections',
                             kwargs.get('collection'), 'versions', params={'limit': '0'})
            return HttpResponse(json.dumps(result.json()), content_type="application/json")
        return super(CollectionVersionsView, self).get(self, *args, **kwargs)


class CollectionAboutView(CollectionsBaseView, TemplateView):
    """ Collection About view. """
    template_name = "collections/collection_about.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionAboutView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()
        about = None
        if ('extras' in collection and isinstance(collection['extras'], dict) and
                    'about' in collection['extras']):
            about = collection['extras'].get('about')

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'About'
        context['collection'] = collection
        context['about'] = about

        return context


class CollectionDetailView(CollectionsBaseView, TemplateView):
    """ Collection detail views """

    template_name = "collections/collection_details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)

        if results.status_code != 200:
            if results.status_code == 404:
                raise Http404
            else:
                results.raise_for_status()
        collection = results.json()

        context['kwargs'] = self.kwargs
        context['collection'] = collection
        context['selected_tab'] = 'Details'
        return context


class CollectionCreateView(CollectionsBaseView, FormView):
    """
        Create new Collection, either for an org or a user.
    """
    form_class = CollectionCreateForm
    template_name = "collections/collection_create.html"

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
        context = super(CollectionCreateView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OclApi(self.request, debug=True)
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
            collection input is good, update API backend.
        """
        self.get_args()

        data = form.cleaned_data
        short_code = data.pop('short_code')
        data['id'] = short_code
        if re.compile('^' + OclConstants.ORG_PATTERN + '$').match(short_code):
            api = OclApi(self.request, debug=True)
            result = api.post(self.owner_type, self.owner_id, 'collections', **data)
            if not result.status_code == requests.codes.created:
                emsg = result.json().get('detail', None)
                if not emsg:
                    for msg in result.json().get('__all__'):
                        messages.add_message(self.request, messages.ERROR, msg)
                else:
                    messages.add_message(self.request, messages.ERROR, emsg)
                return HttpResponseRedirect(self.request.path)

            messages.add_message(self.request, messages.INFO, _('Collection created'))

            if self.from_org:
                return HttpResponseRedirect(reverse("collection-home",
                                                    kwargs={"org": self.org_id,
                                                            'collection': short_code}))
            else:
                return HttpResponseRedirect(reverse("collection-home",
                                                    kwargs={"user": self.user_id,
                                                            'collection': short_code}))
        else:
            validator_template = ' Short Code \'%s\' is not valid. Allowed characters are : Alphabets(a-z,A-Z), Numbers(0-9) and Hyphen(-) '
            messages.add_message(self.request, messages.ERROR, validator_template % short_code)
            return HttpResponseRedirect(self.request.path)


class CollectionAddReferenceView(CollectionsBaseView, TemplateView):
    template_name = "collections/collection_add_reference.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionAddReferenceView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()
        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['collection'] = collection

        return context

    def get_success_url(self):
        """ Return URL for redirecting browser """
        if self.from_org:
            return reverse('collection-references',
                           kwargs={'org': self.org_id, 'collection': self.collection_id})

        else:
            return reverse(
                'collection-references',
                kwargs={"user": self.request.user.username, 'collection': self.collection_id})

    def post(self, request, *args, **kwargs):
        self.get_args()
        data = json.loads(request.body)
        api = OclApi(self.request, debug=True)

        if self.adding_single_reference(data) and not data['expressions']:
            return HttpResponseBadRequest(json.dumps({
                'errors': ('%s' % EXPRESSIONS_SHOULD_EXIST)
            }))

        result = api.put(
            self.owner_type,
            self.owner_id,
            'collections',
            self.collection_id,
            'references',
            data=data,
            params={'cascade': request.GET.get('cascade', 'sourcemappings')}
        )

        results = result.json()
        errors = results if result.status_code == requests.codes.bad else None

        added_result_count = len(filter(lambda result: result['added'], results))

        if added_result_count > 0 and self.show_warning(request.GET.get('warning', 'hide')):
            self.add_version_warning_to_session(data, request, results)

        return HttpResponse(
            json.dumps({
                'update_results': results,
                'success_url': self.get_success_url(),
                'errors': errors,
            }),
            content_type="application/json"
        )

    def add_version_warning_to_session(self, data, request, results):
        if self.adding_single_reference(data):
            # Version Information is getting from api but it isn't getting from form
            expression_from_form = data['expressions'][0]
            expression_from_api = results[0]['expression']
            self.send_message_by_version_information_for_single_reference(request, expression_from_form,
                                                                          expression_from_api)
        else:
            self.send_message_by_source_version_information_for_multiple_reference(request, data)

    def adding_head_version(self, data):
        return data['uri'].split('/')[5] == 'HEAD'

    def adding_single_reference(self, data):
        return data.has_key('expressions')

    def show_warning(self, flag):
        return flag == 'show'

    def version_specified(self, expression):
        return len(expression.split('/')) == 9

    def get_reference_type_in_expression(self, expression):
        return expression.split('/')[5]

    def get_source_in_expression(self, expression):
        return expression.split('/')[4]

    def get_mnemonic_in_expression(self, expression):
        return expression.split('/')[6]

    def get_version_information_in_expression(self, expression):
        return expression.split('/')[7]

    def added_without_version_information_warning_message_by_reference_type(self, reference_type, source, mnemonic, version_number):
        if reference_type == 'concepts':
            return ENTERED_WITHOUT_VERSION_NUMBER_FOR_CONCEPT.format(source, mnemonic, version_number)
        else:
            return ENTERED_WITHOUT_VERSION_NUMBER_FOR_MAPPING.format(source, mnemonic, version_number)

    def added_with_version_information_success_message_by_reference_type(self, reference_type, source, mnemonic, version_number):
        if reference_type == 'concepts':
            return ENTERED_WITH_VERSION_NUMBER_FOR_CONCEPT.format(source, mnemonic, version_number)
        else:
            return ENTERED_WITH_VERSION_NUMBER_FOR_MAPPING.format(source, mnemonic, version_number)

    def send_message_by_version_information_for_single_reference(self, request, expression_from_form, expression_from_api):
        reference_type = self.get_reference_type_in_expression(expression_from_api)
        mnemonic = self.get_mnemonic_in_expression(expression_from_api)
        source = self.get_source_in_expression(expression_from_api)
        version_number = self.get_version_information_in_expression(expression_from_api)

        if self.version_specified(expression_from_form):
            request.session['add_reference_success'] = self.added_with_version_information_success_message_by_reference_type(reference_type, source, mnemonic, version_number)
        else:
            request.session['add_reference_warning'] = self.added_without_version_information_warning_message_by_reference_type(reference_type, source, mnemonic,
                                                                                                                                version_number)

    def send_message_by_source_version_information_for_multiple_reference(self, request, data):
        if self.adding_head_version(data):
            request.session['add_reference_warning'] = POSTED_HEAD_VERSION_OF_SOURCE
        else:
            request.session['add_reference_success'] = POSTED_NON_HEAD_VERSION_OF_SOURCE


class CollectionReferencesDeleteView(CollectionsBaseView, TemplateView):
    def delete(self, request, *args, **kwargs):
        self.get_args()
        references = request.GET.get('references').split(',')
        cascade_mappings_flag = request.GET.get('cascade', 'sourcemappings')
        api = OclApi(self.request, debug=True)
        data = {'references': references, 'cascade': cascade_mappings_flag}
        res = api.delete(self.owner_type, self.owner_id, 'collections',
                         self.collection_id, 'references', **data)
        return HttpResponse(res.content, status=200)


class CollectionDeleteView(CollectionsBaseView, FormView):
    """
    View for deleting Collection.
    """

    template_name = "collections/collection_delete.html"
    form_class = CollectionDeleteForm

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionDeleteView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()
        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['collection'] = collection

        return context

    def get_success_url(self):
        """ Return URL for redirecting browser """
        if self.collection_version_id:
            if self.from_org:
                return reverse('collection-details',
                               kwargs={'org': self.org_id,
                                       'collection': self.collection_id})
            else:
                return reverse('collection-details',
                               kwargs={'user': self.user_id,
                                       'collection': self.collection_id})
        else:
            if self.from_org:
                return reverse('org-collections',
                               kwargs={'org': self.org_id})

            else:
                return reverse('users:detail',
                               kwargs={"username": self.request.user.username})

    def form_valid(self, form, *args, **kwargs):
        """ Use validated form data to delete the collection"""

        self.get_args()

        api = OclApi(self.request, debug=True)
        if self.collection_version_id:
            result = api.delete(self.owner_type, self.owner_id, 'collections',
                                self.collection_id, self.collection_version_id, **kwargs)
        else:
            result = api.delete(
                self.owner_type, self.owner_id, 'collections', self.collection_id, **kwargs)
        if result.status_code != 204:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        else:
            messages.add_message(self.request, messages.INFO, _('Collection Deleted'))

            return HttpResponseRedirect(self.get_success_url())


class CollectionEditView(CollectionsBaseView, FormView):
    """ Edit collection, either for an org or a user. """
    template_name = "collections/collection_edit.html"

    def get_form_class(self):
        """ Trick to load initial data """
        self.get_args()
        api = OclApi(self.request, debug=True)
        self.collection = api.get(self.owner_type, self.owner_id, 'collections',
                                  self.collection_id).json()
        return CollectionEditForm

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        data = {
            'org_id': self.org_id,
            'user_id': self.user_id,
            'from_org': self.from_org,
            'from_user': self.from_user,
            'request': self.request,
        }
        data.update(self.collection)
        # convert supported locales to string
        supported_locale_list = self.collection.get('supported_locales')
        if supported_locale_list is None:
            data['supported_locales'] = ''
        else:
            data['supported_locales'] = ','.join(supported_locale_list)

        return data

    def get_context_data(self, *args, **kwargs):
        """ Get collection details for the edit form """
        context = super(CollectionEditView, self).get_context_data(*args, **kwargs)
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
        context['collection'] = self.collection

        return context

    def form_valid(self, form):
        """ If Collection input is valid, then update API backend. """
        self.get_args()

        # Submit updated collection data to the API
        data = form.cleaned_data
        api = OclApi(self.request, debug=True)
        result = api.update_collection(self.owner_type, self.owner_id, self.collection_id, data)

        messages.add_message(self.request, messages.INFO, _('Collection updated'))
        if self.from_org:
            return HttpResponseRedirect(reverse('collection-details',
                                                kwargs={'org': self.org_id,
                                                        'collection': self.collection_id}))
        else:
            return HttpResponseRedirect(reverse('collection-details',
                                                kwargs={'user': self.user_id,
                                                        'collection': self.collection_id}))


class CollectionVersionsNewView(CollectionsBaseView, UserOrOrgMixin, FormView):
    form_class = CollectionVersionAddForm
    template_name = "collections/collection_versions_new.html"

    def get_initial(self):
        super(CollectionVersionsNewView, self).get_initial()
        self.get_args()

        api = OclApi(self.request, debug=True)
        # collection_version = None
        if self.from_org:
            collection_version = api.get('orgs', self.org_id, 'collections', self.collection_id,
                                         'versions', params={'limit': 1}).json()
        else:
            collection_version = api.get('users', self.user_id, 'collections', self.collection_id,
                                         'versions', params={'limit': 1}).json()

        data = {
            'request': self.request,
            'from_user': self.from_user,
            'from_org': self.from_org,
            'user_id': self.user_id,
            'org_id': self.org_id,
            'owner_type': self.owner_type,
            'owner_id': self.owner_id,
            'collection_id': self.collection_id,
            'previous_version': collection_version[0]['id'],
            'released': False
        }
        return data

    def get_context_data(self, *args, **kwargs):

        context = super(CollectionVersionsNewView, self).get_context_data(*args, **kwargs)
        self.get_args()

        api = OclApi(self.request, debug=True)
        # collection = None
        if self.from_org:
            collection = api.get('orgs', self.org_id, 'collections', self.collection_id).json()
        else:
            collection = api.get('users', self.user_id, 'collections', self.collection_id).json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['collection'] = collection

        return context

    def form_valid(self, form):
        self.get_args()

        # Submit the new collection version
        data = form.cleaned_data
        api = OclApi(self.request, debug=True)
        result = api.create_collection_version(self.owner_type, self.owner_id,
                                               self.collection_id, data)
        if result.status_code == requests.codes.created:
            messages.add_message(self.request, messages.INFO, _('Collection version created!'))
            if self.from_org:
                return HttpResponseRedirect(reverse('collection-versions',
                                                    kwargs={'org': self.org_id,
                                                            'collection': self.collection_id}))
            else:
                return HttpResponseRedirect(reverse('collection-versions',
                                                    kwargs={'user': self.user_id,
                                                            'collection': self.collection_id}))
        else:
            error_msg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, error_msg)
            return HttpResponseRedirect(self.request.path)


class CollectionVersionEditView(LoginRequiredMixin, UserOrOrgMixin, FormView):
    """ View to edit collection version """
    form_class = CollectionVersionsEditForm
    template_name = "collections/collection_versions_edit.html"

    def get_form_class(self):
        """ Trick to load initial form data """
        self.get_args()
        api = OclApi(self.request, debug=True)
        self.collection_version = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id,
                                          self.collection_version_id).json()
        return CollectionVersionsEditForm

    def get_initial(self):
        """ Load initial form data """
        data = {
            'org_id': self.org_id,
            'user_id': self.user_id,
            'from_org': self.from_org,
            'from_user': self.from_user,
            'collection_id': self.collection_id,
            'collection_version_id': self.collection_version_id,
            'request': self.request,
        }
        data.update(self.collection_version)
        return data

    def get_context_data(self, *args, **kwargs):
        """ Load context data needed for the view """
        context = super(CollectionVersionEditView, self).get_context_data(*args, **kwargs)
        context['kwargs'] = self.kwargs
        context['collection_version'] = self.collection_version
        return context

    def form_valid(self, form):
        """ If form data is valid, then update API backend. """
        self.get_args()

        # Submit updated collection version description to the API
        data = {
            'description':form.cleaned_data.get('description'),
            'version_external_id':form.cleaned_data.get('version_external_id')
        }
        api = OclApi(self.request, debug=True)
        result = api.update_resource_version(self.owner_type, self.owner_id, self.collection_id,
                                             self.collection_version_id, 'collections', data)

        # Check if successful
        if result.status_code == requests.codes.ok:
            messages.add_message(self.request, messages.INFO, _('Collection version updated'))
            if self.from_org:
                return HttpResponseRedirect(reverse('collection-versions',
                                                    kwargs={'org': self.org_id,
                                                            'collection': self.collection_id}))
            else:
                return HttpResponseRedirect(reverse('collection-versions',
                                                    kwargs={'user': self.user_id,
                                                            'collection': self.collection_id}))
        else:
            emsg = result.text
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)


class CollectionVersionEditJsonView(CollectionsBaseView, TemplateView):
    def put(self, request, *args, **kwargs):
        self.get_args()
        api = OclApi(self.request, debug=True)
        data = json.loads(request.body)
        res = api.update_resource_version(self.owner_type,
                                          self.owner_id,
                                          self.collection_id,
                                          self.collection_version_id,
                                          'collections',
                                          data)
        return HttpResponse(res.content, status=200)


class CollectionVersionDeleteView(CollectionsBaseView, View):
    """ collection version delete view"""

    def delete(self, request, *args, **kwargs):
        self.get_args()
        api = OclApi(self.request, debug=True)

        if request.is_ajax():
            result = api.delete(
                self.owner_type,
                self.owner_id,
                'collections',
                self.collection_id,
                self.collection_version_id,
                **kwargs
            )

            return HttpResponse(
                json.dumps({}),
                content_type="application/json"
            )
        return super(CollectionVersionDeleteView, self).delete(self, *args, **kwargs)
