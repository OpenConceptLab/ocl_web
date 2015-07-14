import requests
import logging

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, Http404)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.paginator import Paginator
from braces.views import JsonRequestResponseMixin


from libs.ocl import OCLapi, OCLSearch
from .forms import (CollectionCreateForm, CollectionEditForm)
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')


class CollectionDetailView(UserOrOrgMixin, TemplateView):

    template_name = "collections/collection_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(*args, **kwargs)

        self.get_args()

        print 'INPUT PARAMS %s: %s' % (self.request.method, self.request.GET)
        searcher = OCLSearch(OCLapi.COLLECTION_TYPE, params=self.request.GET)

        api = OCLapi(self.request, debug=True)

        results = api.get(self.owner_type, self.owner_id, 'collections', self.collection_id)
        if results.status_code != 200:
            if results.status_code == 404:
                raise Http404
            else:
                results.raise_for_status()
        concept = results.json()

        results = api.get(self.owner_type, self.owner_id, 'sources', self.source_id, 'concepts',
                          params=searcher.search_params)
        if results.status_code != 200:
            if results.status_code == 404:
                raise Http404
            else:
                results.raise_for_status()

        concept_list = results.json()
        context['source'] = source
        context['concepts'] = concept_list

        #context['search_filters'] = searcher.get_search_filters()
        num_found = int(results.headers['num_found'])
        pg = Paginator(range(num_found), searcher.num_per_page)
        context['page'] = pg.page(searcher.current_page)
        context['pagination_url'] = self.request.get_full_path()
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
            collection input is good, update API backend.
        """
        print form.cleaned_data

        self.get_args()

        data = form.cleaned_data
        short_code = data.pop('short_name')
        data['short_code'] = short_code
        data['id'] = short_code
        data['name'] = short_code

        api = OCLapi(self.request, debug=True)
        result = api.post(self.owner_type, self.owner_id, 'collections', **data)
        if not result.status_code == requests.codes.created:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        messages.add_message(self.request, messages.INFO, _('Collection created'))

        if self.from_org:
            return HttpResponseRedirect(reverse("collection-detail",
                                                kwargs={"org": self.org_id,
                                                        'source': short_code}))
        else:
            return HttpResponseRedirect(reverse("collection-detail",
                                                kwargs={"user": self.user_id,
                                                        'source': short_code}))


class CollectionEditView(UserOrOrgMixin, FormView):
    """
        Edit source, either for an org or a user.
    """
    template_name = "Collections/Collection_edit.html"

    def get_form_class(self):
        """ Trick to load initial data """
        self.get_args()
        api = OCLapi(self.request, debug=True)
        self.source_id = self.kwargs.get('source')
        if self.from_org:
            self.source = api.get('orgs', self.org_id, 'sources', self.source_id).json()
        else:
            self.source = api.get('users', self.user_id, 'sources', self.source_id).json()
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
        data.update(self.source)
        data['supported_locales'] = ','.join(self.source['supported_locales'])
        return data

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionEditView, self).get_context_data(*args, **kwargs)

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
            Source input is good, update API backend.
        """
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


class OldCollectionDetailView(TemplateView):

    template_name = "conceptcollections/conceptcollections_detail.html"

    def get_context_data(self, *args, **kwargs):

        context = super(OldCollectionDetailView, self).get_context_data(*args, **kwargs)

        # Setup API calls
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        collection_path = "/v1/orgs/%s/collections/%s/" % (kwargs['org'], kwargs['collection'])
        concept_path = "/v1/orgs/%s/collections/%s/concepts/" % (kwargs['org'], kwargs['collection'])
        collection_url = host + collection_path
        concept_url = host + concept_path
        requestHeaders = {'Authorization': auth_token}

        # API calls for collection details and concepts
        collection = requests.get(collection_url, headers=requestHeaders).json()
        concepts = requests.get(concept_url, headers=requestHeaders).json()

        # Set the context
        context['collection'] = collection
        context['concepts'] = concepts

        return context

