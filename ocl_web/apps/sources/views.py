from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages

from libs.ocl import OCLapi
from .forms import (SourceCreateForm, SourceEditForm)
from apps.core.views import UserOrOrgMixin


class SourceDetailView(UserOrOrgMixin, TemplateView):

    template_name = "sources/source_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SourceDetailView, self).get_context_data(*args, **kwargs)

        self.get_args()
        source_id = self.kwargs.get('source')

        api = OCLapi(self.request, debug=True)

        if self.from_org:
            source = api.get('orgs', self.org_id, 'sources', source_id).json()
            concept_list = api.get('orgs', self.org_id, 'sources', source_id, 'concepts').json()
        else:
            source = api.get('users', self.user_id, 'sources', source_id).json()
            concept_list = api.get('users', self.user_id, 'sources', source_id, 'concepts').json()

        context['source'] = source
        context['concepts'] = concept_list
        return context


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
