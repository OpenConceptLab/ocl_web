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
        context['concepts'] -- All the concepts from the org.

        """

        context = super(OrganizationDetailView, self).get_context_data(*args, **kwargs)

        # TODO:  This request patten is duplicated across views.  Figure out how to
        # make DRY.
        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        org_path = "/v1/orgs/%s" % kwargs['org']
        org_url = host + org_path
        headers = {'Authorization': auth_token}

        org = requests.get(org_url, headers=headers).json()
        sources_url = org['sources_url']
        sources = requests.get(sources_url, headers=headers).json()
        concepts = []

        for source in sources:
            concept_url = source['url'] + "concepts/"
            results = requests.get(concept_url, headers=headers).json()
            concepts += results

        context['org'] = org
        context['concepts'] = concepts

        return context
