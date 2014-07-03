from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
import requests
from .forms import OrganizationCreateForm
from libs import ocl


class OrganizationDetailView(TemplateView):

    template_name = "orgs/org_detail.html"

    def get_context_data(self, *args, **kwargs):
        """Gets the org first, then the sources of that org, and then the
        concepts from each of those sources.

        Final context
        -------------
        context['org']
        context['sources']
        context['collections']
        context['members']
        """

        context = super(OrganizationDetailView, self).get_context_data(*args, **kwargs)

        # TODO:  This request patten is duplicated across views.  Figure out how to
        # make DRY:  utils.ocl_requests.get()

        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        org_path = "/v1/orgs/%s" % kwargs['org']
        org_url = host + org_path
        requestHeaders = {'Authorization': auth_token}

        # Get org details from API
        org = requests.get(org_url, headers=requestHeaders).json()

        # Get sources owned by the org
        sources_url = org['sources_url']
        sources = requests.get(sources_url, headers=requestHeaders).json()

        # Get collections owned by the org
        collections_path = "/v1/orgs/%s/collections/" % kwargs['org']  # The org object should have this in the future.
        collections_url = host + collections_path
        collections = requests.get(collections_url, headers=requestHeaders).json()

        # Get members of the org
        members_url = org['members_url']
        members = requests.get(members_url, headers=requestHeaders).json()

        # Get additional details for sources and collections (since currently not included in the list query)
        sources_detail = []
        for source in sources:
            source = requests.get(source['url'], headers=requestHeaders).json()
            sources_detail.append(source)
        collections_detail = []
        for collection in collections:
            collection = requests.get(collection['url'], headers=requestHeaders).json()
            collections_detail.append(collection)

        context['org'] = org
        context['sources'] = sources_detail
        context['collections'] = collections_detail
        context['members'] = members

        return context

class OrganizationCreateView(FormView):

    form_class = OrganizationCreateForm
    template_name = "orgs/org_new.html"

    def form_valid(self, form, *args, **kwargs):

        org_id = form.cleaned_data.pop('short_name')
        name = form.cleaned_data.pop('full_name')

        results = ocl.Org.create(org_id, name, **form.cleaned_data)

        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if results.ok:
            return redirect("org-new-success")

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationCreateView, self).form_invalid(self, *args, **kwargs)
