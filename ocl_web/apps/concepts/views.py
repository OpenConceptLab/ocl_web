import requests
import logging

from django.views.generic import TemplateView
from django.views.generic.edit import View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse

from braces.views import (CsrfExemptMixin, JsonRequestResponseMixin)

from .forms import (ConceptCreateForm, ConceptEditForm, ConceptRetireForm)
from libs.ocl import OCLapi
from apps.core.views import UserOrOrgMixin

logger = logging.getLogger('oclweb')


class ConceptCreateJsonView(UserOrOrgMixin, JsonRequestResponseMixin,
                            TemplateView):
    """
    A mix HTTP and ajax view for creating and editing concepts.
    on Get returns full HTML display page.
    create is handled via ajax post via angular.
    """
    def get(self, request, *args, **kwargs):

        self.get_args()
        data = {}
        print self.request.is_ajax()
        api = OCLapi(self.request, debug=True)
        source = api.get(self.own_type, self.own_id, 'sources', self.source_id).json()
        data['source'] = source

        if self.concept_id is not None:
            # edit
            concept = api.get(self.own_type, self.own_id, 'sources', self.source_id, 'concepts', self.concept_id).json()
            data['concept'] = concept

            if request.is_ajax():
                return self.render_json_response(concept)

        if self.concept_id is None:
            return TemplateResponse(request, 'concepts/concept_create.html', data)
        else:
            return TemplateResponse(request, 'concepts/concept_edit.html', data)

    def get_success_url(self):
        if self.from_org:
            return reverse("source-detail",
                           kwargs={"org": self.org_id,
                                   'source': self.kwargs.get('source')})
        else:
            return reverse("source-detail",
                           kwargs={"user": self.user_id,
                                   'source': self.kwargs.get('source')})

    def clean_concept_id(self, request, concept_id):
        """ concept ID must be unique """

        api = OCLapi(request, debug=True)
        result = api.get(self.own_type, self.own_id, 'sources', self.source_id, 'concepts', concept_id)
        if result.status_code == 200:
            return _('This Concept ID is already used.')
        else:
            return None

    def add(self):
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
            self.own_type, self.own_id, self.source_id, data, names=names)
        if result.status_code != 201:
            logger.warning('Concept create POST failed %s' % result.content)
            return self.render_bad_request_response({'message': result.content})
        else:
            return self.render_json_response({'message': _('Concept created')})

    def edit(self):

        data = {}
        data['concept_class'] = self.request_json.get('concept_class')
        data['datatype'] = self.request_json.get('datatype')
        data['external_id'] = self.request_json.get('external_id')
        data['update_comment'] = self.request_json.get('update_comment')
        print data
        # TEMP for faster testing
        # return self.render_json_response({'message': _('Concept updated')})

        api = OCLapi(self.request, debug=True)
        result = api.update_concept(self.own_type, self.own_id, self.source_id, self.concept_id, data)
        if result.status_code != requests.codes.ok:
            emsg = result.json().get('detail', 'Error')
            logger.warning('Concept update POST failed %s' % emsg)
            return self.render_bad_request_response({'message': emsg})
        else:
            return self.render_json_response({'message': _('Concept updated')})

    def post(self, *args, **kwargs):
        """
            Handle actual creation or edit.
        """
        self.get_args()
        print self.args_string()

        if self.concept_id is not None:
            return self.edit()
        else:
            return self.add()


class ConceptRetireView(UserOrOrgMixin, FormView):
    """
    View for retiring a concept. This is like a logical delete.
    """
    form_class = ConceptRetireForm
    template_name = "concepts/concept_retire.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ConceptRetireView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OCLapi(self.request, debug=True)
        source = api.get(self.own_type, self.own_id, 'sources', self.source_id).json()
        context['source'] = source
        concept = api.get(self.own_type, self.own_id, 'sources', self.source_id, 'concepts', self.concept_id).json()
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
            self.own_type, self.own_id, 'sources', self.source_id, 'concepts',
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
        # moved to get_args
        # self.source_id = self.kwargs.get('source')
        # self.concept_id = self.kwargs.get('concept')

        api = OCLapi(self.request, debug=True)

        self.source = api.get_json(self.own_type, self.own_id, 'sources',
                                   self.source_id)
        self.concept = api.get_json(self.own_type, self.own_id, 'sources',
                                    self.source_id, 'concepts', self.concept_id)
        return

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
    optional = None

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

        if self.optional:
            result = api.get(self.own_type, self.own_id, 'sources', self.source_id,
               'concepts', self.concept_id, self.item_name, params=self.optional)
        else:
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
            msg = _('updated')
        else:
            result = api.post(self.own_type, self.own_id, 'sources', self.source_id,
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
            result = api.delete(self.own_type, self.own_id, 'sources', self.source_id,
                                'concepts', self.concept_id,
                                self.item_name, self.item_id)
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


class ConceptMappingView(ConceptItemView):
    item_name = 'mappings'
    kwarg_name = 'mapping'
    field_names = ['map_type', 'external_id', 'from_concept_url', 'to_concept_url']
    optional = {'includeInverseMappings': True}


class ConceptExtraView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
        Concept extras handling is different from descriptions and names. So the view
        is similar to the ConceptItemView but not the same.

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
            result = api.put(self.own_type, self.own_id, 'sources', self.source_id,
                             'concepts', self.concept_id, 'extras', fn,
                             **data)
            msg = _('Extra updated')
        else:
            result = api.put(self.own_type, self.own_id, 'sources', self.source_id,
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

        result = api.delete(self.own_type, self.own_id, 'sources', self.source_id,
                            'concepts', self.concept_id,
                            self.item_name, self.item_id)
        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': _('extra deleted')})
