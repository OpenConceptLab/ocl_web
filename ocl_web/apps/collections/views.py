"""
OCL Collection views
"""
import requests
import logging

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse,resolve, Resolver404
from django.http import (HttpResponseRedirect, Http404)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.paginator import Paginator


from libs.ocl import OclApi, OclSearch, OclConstants
from .forms import (CollectionCreateForm, CollectionEditForm, CollectionDeleteForm, CollectionAddReferenceForm, CollectionVersionAddForm)
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')


class CollectionsBaseView(UserOrOrgMixin):
    def get_args(self):
        super(CollectionsBaseView, self).get_args()
        self.collection_id = self.kwargs.get('collection')
        self.collection_version_id = self.kwargs.get('collection_version')

    def get_collection_data(self, owner_type, owner_id, collection_id, field_name,
                            collection_version_id=None, search_params=None):

        searcher = OclSearch(search_type=field_name, params=search_params)
        api = OclApi(self.request, debug=True, facets=True)

        if collection_version_id:
            search_response = api.get(
                owner_type, owner_id, 'collections', collection_id, collection_version_id, field_name,
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
            search_type=None, search_response=search_response,
            search_params=search_params)

        return searcher

    def get_collection_versions(self, owner_type, owner_id, collection_id, search_params=None):
        # Perform the search
        searcher = OclSearch(search_type=OclConstants.RESOURCE_NAME_COLLECTION_VERSIONS,
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
        data = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id,'references').json()
        collection = results.json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'References'
        context['collection'] = collection
        context['references'] = data.get('references')

        return context

class CollectionMappingsView(CollectionsBaseView, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_mappings.html"
    def get_context_data(self, *args, **kwargs):

        context = super(CollectionMappingsView, self).get_context_data(*args, **kwargs)
        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        searcher = self.get_collection_data(
            self.owner_type, self.owner_id, self.collection_id, OclConstants.RESOURCE_NAME_MAPPINGS,
            collection_version_id=self.collection_version_id,
            search_params=self.request.GET)

        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Mappings'
        context['collection'] = collection
        context['collection_version'] = self.collection_version_id
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_query'] = searcher.get_query()
        context['search_filters'] = searcher.search_filter_list
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context


class CollectionConceptsView(CollectionsBaseView, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_concepts.html"

    def get_context_data(self, *args, **kwargs):

        context = super(CollectionConceptsView, self).get_context_data(*args, **kwargs)
        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        searcher = self.get_collection_data(
            self.owner_type, self.owner_id, self.collection_id, OclConstants.RESOURCE_NAME_CONCEPTS,
            collection_version_id=self.collection_version_id,
            search_params=self.request.GET)

        search_results_paginator = Paginator(range(searcher.num_found), searcher.num_per_page)
        search_results_current_page = search_results_paginator.page(searcher.current_page)

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Concepts'
        context['collection'] = collection
        context['collection_version'] = self.collection_version_id
        context['results'] = searcher.search_results
        context['current_page'] = search_results_current_page
        context['pagination_url'] = self.request.get_full_path()
        context['search_query'] = searcher.get_query()
        context['search_filters'] = searcher.search_filter_list
        context['search_sort_options'] = searcher.get_sort_options()
        context['search_sort'] = searcher.get_sort()
        context['search_facets_json'] = searcher.search_facets
        context['search_filters_debug'] = str(searcher.search_filter_list)

        return context


class CollectionVersionsView(CollectionsBaseView, TemplateView):
    """ collection About view. """
    template_name = "collections/collection_versions.html"
    def get_context_data(self, *args, **kwargs):
        context = super(CollectionVersionsView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        # Load the source versions
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
        print form.cleaned_data

        self.get_args()

        data = form.cleaned_data
        short_code = data.pop('short_code')
        data['id'] = short_code

        api = OclApi(self.request, debug=True)
        result = api.post(self.owner_type, self.owner_id, 'collections', **data)
        if not result.status_code == requests.codes.created:
            emsg = result.json().get('detail', 'Error')
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


class CollectionAddReferenceView(UserOrOrgMixin, FormView):
    template_name = "collections/collection_add_reference.html"
    form_class = CollectionAddReferenceForm

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
                           kwargs={'org': self.org_id,'collection':self.collection_id})

        else:
            return reverse('collection-references',
                           kwargs={"username": self.request.user.username,'collection':self.collection_id})

    def form_valid(self, form, *args, **kwargs):
        """ Use validated form data to delete the collection"""

        self.get_args()
        data = form.cleaned_data
        # resolver = resolve(data)
        api = OclApi(self.request, debug=True)
        result = api.put(self.owner_type, self.owner_id, 'collections', self.collection_id, 'references', **data)

        if not result.status_code == requests.codes.all_good:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        messages.add_message(self.request, messages.INFO, _('Expression added.'))

        if self.from_org:
            return HttpResponseRedirect(reverse('collection-references',
                                                kwargs={'org': self.org_id,
                                                        'collection': self.collection_id}))
        else:
            return HttpResponseRedirect(reverse('collection-references',
                                                kwargs={'user': self.user_id,
                                                        'collection': self.collection_id}))

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
        self.collection = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id).json()
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
        print result
        if len(result.text) > 0:
            print result.json()

        messages.add_message(self.request, messages.INFO, _('Collection updated'))
        if self.from_org:
            return HttpResponseRedirect(reverse('collection-details',
                                                kwargs={'org': self.org_id,
                                                        'collection': self.collection_id}))
        else:
            return HttpResponseRedirect(reverse('collection-details',
                                                kwargs={'user': self.user_id,
                                                        'collection': self.collection_id}))
