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
        collections_path = "/v1/orgs/%s/collections/" % kwargs['org']  # The org object should have this in the future.
        collections_url = host + collections_path
        collections = requests.get(collections_url, headers=headers).json()
        members_url = org['members_url']
        members = requests.get(members_url, headers=headers).json()

        mock_members = [
            {
                "username": "johnnytest",
                "name": "Johnny Test",
                "url": "http://65.99.230.144/v1/users/johnnytest/"
            },
            {
                "username": "bobbytest",
                "name": "Bobby Test",
                "url": "http://65.99.230.144/v1/users/bobbytest/"
            },
            {
                "username": "paynetest2",
                "name": "Jonathan Payne",
                "url": "http://65.99.230.144/v1/users/paynetest2/"
            }
        ]

        mock_collections = [
            {
                "type": "Collection",
                "uuid": "8d492ee0-c2cc-11de-8d13-0010c6dffd0f",
                "id": "Community-MCH",

                "shortCode": "Community-MCH",
                "name": "Community-MCH Core Dataset",
                "fullName": "Community Maternal-Child Health Core Dataset",
                "publicAccess": "View",
                "supportedLocales": "en,es",
                "website": "",
                "description": "",

                "owner": "MCL",
                "ownerType": "organization",
                "ownerUrl": "https://api.openconceptlab.org/v1/orgs/MCL",

                "url": "https://www.openconceptlab.org/v1/orgs/MCL/collections/Community-MCH",
                "versionsUrl": "https://www.openconceptlab.org/v1/orgs/MCL/collections/Community-MCH/versions",
                "conceptsUrl": "https://www.openconceptlab.org/v1/orgs/MCL/collections/Community-MCH/concepts",

                "versions": 4,
                "activeConcepts": 92,
                "stars": 17,

                "createdOn": "2008-01-14T04:33:35Z",
                "updatedOn": "2008-02-18T09:10:16Z"
            },
            {
                "type": "Collection",
                "uuid": "8d492ee0-c2cc-11de-8d13-0010c6dffd0f",
                "id": "Community-MCH",

                "shortCode": "Community-MCH",
                "name": "Community-MCH Core Dataset",
                "fullName": "Community Maternal-Child Health Core Dataset",
                "publicAccess": "View",
                "supportedLocales": "en,es",
                "website": "",
                "description": "",

                "owner": "MCL",
                "ownerType": "organization",
                "ownerUrl": "https://api.openconceptlab.org/v1/orgs/MCL",

                "url": "https://www.openconceptlab.org/v1/orgs/MCL/collections/Community-MCH",
                "versionsUrl": "https://www.openconceptlab.org/v1/orgs/MCL/collections/Community-MCH/versions",
                "conceptsUrl": "https://www.openconceptlab.org/v1/orgs/MCL/collections/Community-MCH/concepts",

                "versions": 4,
                "activeConcepts": 92,
                "stars": 17,

                "createdOn": "2008-01-14T04:33:35Z",
                "updatedOn": "2008-02-18T09:10:16Z"
            }
        ]

        context['org'] = org
        context['sources'] = sources
        context['collections'] = mock_collections
        context['members'] = mock_members
#        context['collections'] = collections  # Uncomment to add the real collections (whenever the API is ready)
#        context['members'] = members  # Uncomment to add the real collections (whenever the API is ready)

        return context
