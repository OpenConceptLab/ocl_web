import requests

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import (TemplateView, View)
from django.views.generic.edit import FormView
from django.contrib import messages
from braces.views import (CsrfExemptMixin, JsonRequestResponseMixin)

from libs.ocl import OCLapi
from .forms import (SourceCreateForm, SourceEditForm, SourceVersionAddForm)
from apps.core.views import UserOrOrgMixin


class SourceDetailView(UserOrOrgMixin, TemplateView):

    template_name = "sources/source_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SourceDetailView, self).get_context_data(*args, **kwargs)

        self.get_args()

        api = OCLapi(self.request, debug=True)

        source = api.get(self.own_type, self.own_id, 'sources', self.source_id).json()
        concept_list = api.get(self.own_type, self.own_id, 'sources', self.source_id, 'concepts').json()

        context['source'] = source
        context['concepts'] = concept_list
        return context


class SourceVersionListView(CsrfExemptMixin, JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
    Return json source versions.
    """

    def get_all_args(self):
        """ Get all input parameters for view.
        """
        self.get_args()
        self.source_id = self.kwargs.get('source')

        if self.from_org:
            self.own_type = 'orgs'
            self.own_id = self.org_id
        else:
            self.own_type = 'users'
            self.own_id = self.user_id

    def get(self, request, *args, **kwargs):
        """
            Return a list of versions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(self.own_type, self.own_id, 'sources', self.source_id,
                         'versions', '?verbose=True')
        if not result.ok:
            print result
            return self.render_bad_request_response(result)

        return self.render_json_response(result.json())


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
            Source input is good, update API backend.
        """
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
        print result.status_code
        if len(result.text) > 0: print result.json()

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
        """ Trick to load initial data """
        self.get_args()
        api = OCLapi(self.request, debug=True)
        self.source_id = self.kwargs.get('source')
        if self.from_org:
            self.source = api.get('orgs', self.org_id, 'sources', self.source_id).json()
        else:
            self.source = api.get('users', self.user_id, 'sources', self.source_id).json()
        return SourceEditForm

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
        if len(result.text) > 0: print result.json()

        messages.add_message(self.request, messages.INFO, _('Source updated'))

        if self.from_org:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"org": self.org_id,
                                                        'source': self.source_id}))
        else:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"user": self.user_id,
                                                        'source': self.source_id}))


class SourceVersionAddView(UserOrOrgMixin, FormView):
    """
        Add a new source version.
    """
    template_name = "sources/source_version_add.html"

    def get_form_class(self):
        """ Trick to load initial data """
        self.get_args()
        api = OCLapi(self.request, debug=True)

        self.source = api.get(self.own_type, self.own_id, 'sources', self.source_id).json()
        return SourceVersionAddForm

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
        context = super(SourceVersionAddView, self).get_context_data(*args, **kwargs)

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
            result = api.create_source_version_by_org(self.org_id, self.source_id, data)
        else:
            result = api.create_source_version_by_user(self.user_id, self.source_id, data)
        print result
        if len(result.text) > 0: print result.json()

        if result.status_code != requests.codes.created:
            emsg = result.json().get('detail', 'Error')
            messages.add_message(self.request, messages.ERROR, emsg)
            return HttpResponseRedirect(self.request.path)

        messages.add_message(self.request, messages.INFO, _('Version Added'))
        if self.from_org:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"org": self.org_id,
                                                        'source': self.source_id}))
        else:
            return HttpResponseRedirect(reverse("source-detail",
                                                kwargs={"user": self.user_id,
                                                        'source': self.source_id}))

