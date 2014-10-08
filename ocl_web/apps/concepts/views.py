import requests

from django.views.generic import TemplateView
from django.views.generic.edit import View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from braces.views import (CsrfExemptMixin, JsonRequestResponseMixin)

from .forms import (ConceptCreateForm, ConceptEditForm)
from libs.ocl import OCLapi
from apps.core.views import UserOrOrgMixin


class ConceptCreateView(UserOrOrgMixin, FormView):

    form_class = ConceptCreateForm
    template_name = "concepts/concept_create.html"

    def get_success_url(self):
        if self.from_org:
            return reverse("source-detail",
                           kwargs={"org": self.org_id,
                                   'source': self.kwargs.get('source')})
        else:
            return reverse("source-detail",
                           kwargs={"user": self.user_id,
                                   'source': self.kwargs.get('source')})

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form
        """
        context = super(ConceptCreateView, self).get_context_data(*args, **kwargs)

        self.get_args()
        source_id = self.kwargs.get('source')

        api = OCLapi(self.request, debug=True)
        if self.from_org:
            source = api.get('orgs', self.org_id, 'sources', source_id).json()
        else:
            source = api.get('users', self.user_id, 'sources', source_id).json()

        context['source'] = source
        return context

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
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

        self.get_args()
        source_id = self.kwargs.get('source')

        print form.cleaned_data

        data = {}
        data['id'] = form.cleaned_data['concept_id']
        data['concept_class'] = form.cleaned_data['concept_class']
        data['datatype'] = form.cleaned_data['datatype']

        name = {}
        name['name'] = form.cleaned_data['name']
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
            self.concept = api.get('orgs', self.org_id, 'sources', self.source_id, 'concepts', self.concept_id).json()
        else:
            self.source = api.get('users', self.user_id, 'sources', self.source_id).json()
            self.concept = api.get('users', self.user_id, 'sources', self.source_id, 'concepts', self.concept_id).json()
        return ConceptEditForm

    def get_success_url(self):
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
            result = api.update_concept('users', self.user_id, self.source_id, self.concept_id, data)
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
        self.source_id = self.kwargs.get('source')
        self.concept_id = self.kwargs.get('concept')

        api = OCLapi(self.request, debug=True)

        if self.from_org:
            self.source = api.get_json('orgs', self.org_id, 'sources', self.source_id)
            self.concept = api.get_json('orgs', self.org_id, 'sources', self.source_id, 'concepts', self.concept_id)
        else:
            self.source = api.get('users', self.user_id, 'sources', self.source_id).json()
            self.concept = api.get('users', self.user_id, 'sources', self.source_id, 'concepts', self.concept_id).json()

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

        result = api.get(self.own_type, self.own_id, 'sources', self.source_id,
                         'concepts', self.concept_id, 'versions')
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(result.json())


class ConceptItemView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
        Interface to AngularJS concept description operations, supporting list, add, update and delete.
    """
    # override this, set to 'descriptions', 'names', etc
    item_name = None
    kwarg_name = None
    field_names = []

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
            Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(self.own_type, self.own_id, 'sources', self.source_id,
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
            result = api.put(self.own_type, self.own_id, 'sources', self.source_id,
                             'concepts', self.concept_id, self.item_name,
                             self.item_id, **data)
        else:
            result = api.post(self.own_type, self.own_id, 'sources', self.source_id,
                              'concepts', self.concept_id, self.item_name, **data)

        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(
            {'message': _('Description added')})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified item.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)
        if self.is_edit():  # i.e. has item UUID
            result = api.delete(self.own_type, self.own_id, 'sources', self.source_id,
                                'concepts', self.concept_id,
                                self.item_name, self.item_id)
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(
            {'message': _('Description deleted')})


class ConceptDescView(ConceptItemView):
    item_name = 'descriptions'
    kwarg_name = 'description'
    field_names = ['description', 'description_type', 'locale', 'locale_preferred']


class ConceptNameView(ConceptItemView):
    item_name = 'names'
    kwarg_name = 'name'
    field_names = ['name', 'name_type', 'locale', 'locale_preferred']


class ConceptExtraView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
        Concept extras handling is different from descriptions and names. So the view
        is similar to the ConceptItemView but not the same.

        The extras field name IS the attribute name, etc.
    """
    # override this, set to 'descriptions', 'names', etc
    item_name = 'extras'
    kwarg_name = 'extra'

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
            Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(self.own_type, self.own_id, 'sources', self.source_id,
                         'concepts', self.concept_id, self.item_name)
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        print result
        print result.json()
        return self.render_json_response(result.json())

    def post(self, request, *args, **kwargs):

        self.get_all_args()
        data = {}
        fn = fv = None
        try:
            print 'request json:', self.request_json
            fn = self.request_json.get('extra_name')
            fv = self.request_json.get('extra_value')
            data[fn] = fv
        except KeyError:
            resp = {u"message": _('Invalid input')}
            return self.render_bad_request_response(resp)

        return self.render_json_response(
            {'message': _('extra added')})

        api = OCLapi(self.request, debug=True)
        if self.is_edit():
            result = api.put(self.own_type, self.own_id, 'sources', self.source_id,
                             'concepts', self.concept_id, 'extras', fn,
                             **data)
        else:
            result = api.put(self.own_type, self.own_id, 'sources', self.source_id,
                              'concepts', self.concept_id, 'extras', fn, **data)

        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(
            {'message': _('extra added')})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified item.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)
        if self.is_edit():  # i.e. has item UUID
            result = api.delete(self.own_type, self.own_id, 'sources', self.source_id,
                                'concepts', self.concept_id,
                                self.item_name, self.item_id)
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(
            {'message': _('Description deleted')})

