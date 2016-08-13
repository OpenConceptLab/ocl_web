from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
class OrgUrlsTest(TestCase):

    def test_collection_new_viewname_to_url(self):
        url = reverse('collection-new', kwargs={'org':'myorgs'})
        self.assertEqual(url, '/orgs/myorgs/collections/new/')

    def test_url_to_collection_new_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/new/')
        self.assertEqual(resolver.view_name, 'collection-new')

    def test_collection_home_viewname_to_url(self):
        url = reverse('collection-home', kwargs={'org': 'myorgs', 'collection':'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/')

    def test_url_to_collection_home_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/')
        self.assertEqual(resolver.view_name, 'collection-home')

    def test_org_collections_viewname_to_url(self):
        url = reverse('org-collections', kwargs={'org': 'myorgs'})
        self.assertEqual(url,'/orgs/myorgs/collections/')

    def test_url_to_org_collections_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/')
        self.assertEqual(resolver.view_name,'org-collections')

    def test_collections_details_viewname_to_url(self):
        url = reverse('collection-details', kwargs={'org': 'myorgs','collection':'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/details/')

    def test_url_to_collections_details_viewname(self):
        resolver=resolve('/orgs/myorgs/collections/collection1/details/')
        self.assertEqual(resolver.view_name,'collection-details')

    def test_collections_edit_viewname_to_url(self):
        url = reverse('collection-edit', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/edit/')

    def test_url_to_collections_edit_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/edit/')
        self.assertEqual(resolver.view_name,'collection-edit')

    def test_collections_about_viewname_to_url(self):
        url = reverse('collection-about', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/about/')

    def test_url_to_collections_about_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/about/')
        self.assertEqual(resolver.view_name, 'collection-about')

    def test_collections_versions_viewname_to_url(self):
        url = reverse('collection-versions', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/versions/')

    def test_url_to_collections_versions_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/versions/')
        self.assertEqual(resolver.view_name, 'collection-versions')

    def test_collections_concepts_viewname_to_url(self):
        url = reverse('collection-concepts', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/concepts/')

    def test_url_to_collections_concepts_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/concepts/')
        self.assertEqual(resolver.view_name, 'collection-concepts')

    def test_collections_mappings_viewname_to_url(self):
        url = reverse('collection-mappings', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/mappings/')

    def test_url_to_collections_mappings_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/mappings/')
        self.assertEqual(resolver.view_name, 'collection-mappings')


    def test_collections_sources_viewname_to_url(self):
        url = reverse('collection-sources', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/sources/')


    def test_url_to_collections_sources_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/sources/')
        self.assertEqual(resolver.view_name, 'collection-sources')

    def test_collections_collections_viewname_to_url(self):
        url = reverse('collection-collections', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/collections/')

    def test_url_to_collections_collections_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/collections/')
        self.assertEqual(resolver.view_name, 'collection-collections')

    def test_collections_delete_viewname_to_url(self):
        url = reverse('collection-delete', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/delete/')

    def test_url_to_collections_delete_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/delete/')
        self.assertEqual(resolver.view_name, 'collection-delete')

    def test_sources_delete_viewname_to_url(self):
        url = reverse('source-delete', kwargs={'org': 'myorgs', 'source': 'source1'})
        self.assertEqual(url, '/orgs/myorgs/sources/source1/delete/')

    def test_url_to_sources_delete_viewname(self):
        resolver = resolve('/orgs/myorgs/sources/source1/delete/')
        self.assertEqual(resolver.view_name, 'source-delete')

