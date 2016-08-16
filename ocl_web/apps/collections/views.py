"""
OCL Collection views
"""
import requests
import logging

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, Http404)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.paginator import Paginator


from libs.ocl import OclApi, OclSearch, OclConstants
from .forms import (CollectionCreateForm, CollectionEditForm, CollectionDeleteForm)
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')

class CollectionReferencesView(UserOrOrgMixin, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_references.html"
    def get_context_data(self, *args, **kwargs):
        context = super(CollectionReferencesView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'References'
        context['collection'] = collection

        return context
class CollectionMappingsView(UserOrOrgMixin, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_mappings.html"
    def get_context_data(self, *args, **kwargs):
        context = super(CollectionMappingsView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Mappings'
        context['collection'] = collection

        return context

class CollectionConceptsView(UserOrOrgMixin, TemplateView):
    """ collection concept view. """
    template_name = "collections/collection_concepts.html"
    def get_context_data(self, *args, **kwargs):
        context = super(CollectionConceptsView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Concepts'
        context['collection'] = collection

        return context


class CollectionVersionsView(UserOrOrgMixin, TemplateView):
    """ collection About view. """
    template_name = "collections/collection_versions.html"
    def get_context_data(self, *args, **kwargs):
        context = super(CollectionVersionsView, self).get_context_data(*args, **kwargs)

        self.get_args()
        api = OclApi(self.request, debug=True)
        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        collection = results.json()

        # Set the context
        context['kwargs'] = self.kwargs
        context['url_params'] = self.request.GET
        context['selected_tab'] = 'Versions'
        context['collection'] = collection

        return context

class CollectionAboutView(UserOrOrgMixin, TemplateView):
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


class CollectionDetailView(UserOrOrgMixin, TemplateView):
    """ Collection detail views """

    template_name = "collections/collection_details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(*args, **kwargs)

        self.get_args()

        searcher = OclSearch(OclConstants.RESOURCE_NAME_COLLECTIONS, params=self.request.GET)

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


class CollectionCreateView(UserOrOrgMixin, FormView):
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


class CollectionDeleteView(UserOrOrgMixin, FormView):
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


class CollectionEditView(UserOrOrgMixin, FormView):
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
