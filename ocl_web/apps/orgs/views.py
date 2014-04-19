from django.views.generic import TemplateView
from django.conf import settings
import requests


class OrganizationDetailView(TemplateView):

    template_name = "orgs/org_detail.html"

    def get_context_data(self, *args, **kwargs):
        """Gets the org first, then the sources of that org, and then the
        concepts from each of those sources.

        Final context
        -------------
        context['org'] -- The org.
        context['sources']
        context['collections']
        context['members']

        """

        context = super(OrganizationDetailView, self).get_context_data(*args, **kwargs)

        # TODO:  This request patten is duplicated across views.  Figure out how to
        # make DRY.
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        org_path = "/v1/orgs/%s" % kwargs['org']
        org_url = host + org_path
        headers = {'Authorization': auth_token}

        # Get org details from API
        org = requests.get(org_url, headers=headers).json()

        # Get sources owned by the org
        sources_url = org['sources_url']
        sources = requests.get(sources_url, headers=headers).json()

        # Get collections owned by the org
        collections_path = "/v1/orgs/%s/collections/" % kwargs['org']  # The org object should have this in the future.
        collections_url = host + collections_path
        collections = requests.get(collections_url, headers=headers).json()

        # Get members of the org
        members_url = org['members_url']
        members = requests.get(members_url, headers=headers).json()

        # Get additional details for sources and collections (since currently not included in the list query)
        sources_detail = []
        for source in sources:
            source = requests.get(source['url'], headers=headers).json()
            sources_detail.append(source)
        collections_detail = []
        for collection in collections:
            collection = requests.get(collection['url'], headers=headers).json()
            collections_detail.append(collection)

        context['org'] = org
        context['sources'] = sources_detail
        context['collections'] = collections_detail
#       context['sources'] = sources
#       context['collections'] = collections  # Uncomment to add the real collections (whenever the API is ready)
        context['members'] = members  # Uncomment to add the real collections (whenever the API is ready)

        return context
