from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.contrib import messages

import requests

from libs.ocl import OCLapi
from .forms import SourceCreateForm

class SourceDetailView(TemplateView):

    template_name = "sources/source_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SourceDetailView, self).get_context_data(*args, **kwargs)

        # Setup API calls
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        source_path = "/v1/orgs/%s/sources/%s/" % (kwargs['org'], kwargs['source'])
        concept_path = "/v1/orgs/%s/sources/%s/concepts/" % (kwargs['org'], kwargs['source'])
        source_url = host + source_path
        concept_url = host + concept_path
        requestHeaders = {'Authorization': auth_token}

        # API calls for source details and concepts
        source = requests.get(source_url, headers=requestHeaders).json()
        concepts = requests.get(concept_url, headers=requestHeaders).json()

        # Set the context
        context['source'] = source
        context['concepts'] = concepts

        return context

class SourceCreateView(FormView):
    """
        Create new source, either for an org or a user.
    """
    form_class = SourceCreateForm
    template_name = "sources/source_create.html"

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        org_id = self.kwargs.get('org')

        data = {
            'org_id': org_id,
            'request': self.request,
            }
        return data

    def get_context_data(self, *args, **kwargs):
        context = super(SourceCreateView, self).get_context_data(*args, **kwargs)

        org_id = self.kwargs.get('org')
        api = OCLapi(self.request, debug=True)

        org = api.get('orgs', org_id).json()
        print org
        # Set the context
        context['org'] = org
        return context

    def form_valid(self, form):
        """
            Source input is good, update API backend.
        """
        print form.cleaned_data

        org_id = form.initial.get('org_id')
        data = form.cleaned_data
        short_code = data.pop('short_name')
        data['short_code'] = short_code
        data['id'] = short_code
        data['name'] = short_code

        api = OCLapi(self.request, debug=True)
        result = api.create_source_by_org(org_id, data)
        print result.status_code
        if len(result.text) > 0: print result.json()

        messages.add_message(self.request, messages.INFO, _('Source created'))
        return HttpResponseRedirect(reverse("source-detail",
           kwargs={"org": org_id,
                  'source': short_code}))

