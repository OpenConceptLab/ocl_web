from django.test import TestCase
from django.core.urlresolvers import reverse, resolve

class UserUrlsTest(TestCase):

    def test_user_new_collection_viewname_to_url(self):
        url = reverse('collection-new', kwargs={"user":"testuser"})
        self.assertEqual(url, '/users/testuser/collections/new/')

    def test_user_new_collection_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/new/')
        self.assertEqual(resolver.view_name, 'collection-new')
        self.assertEqual(resolver.kwargs['user'], 'testuser')

    def test_user_collection_details_viewname_to_url(self):
        url = reverse('collection-details', kwargs={"user":"testuser","collection":"testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/details/')

    def test_user_collection_details_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/details/')
        self.assertEqual(resolver.view_name, 'collection-details')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_collection_home_viewname_to_url(self):
        url = reverse('collection-home', kwargs={"user":"testuser","collection":"testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/')

    def test_user_collection_home_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/')
        self.assertEqual(resolver.view_name, 'collection-home')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_collection_edit_viewname_to_url(self):
        url = reverse('collection-edit', kwargs={"user":"testuser","collection":"testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/edit/')

    def test_user_collection_edit_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/edit/')
        self.assertEqual(resolver.view_name, 'collection-edit')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_collection_about_viewname_to_url(self):
        url = reverse('collection-about', kwargs={"user":"testuser","collection":"testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/about/')

    def test_user_collection_about_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/about/')
        self.assertEqual(resolver.view_name, 'collection-about')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_collection_versions_viewname_to_url(self):
        url = reverse('collection-versions', kwargs={"user":"testuser","collection":"testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/versions/')

    def test_user_collection_versions_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/versions/')
        self.assertEqual(resolver.view_name, 'collection-versions')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_collection_concepts_viewname_to_url(self):
        url = reverse('collection-concepts', kwargs={"user":"testuser","collection":"testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/concepts/')

    def test_user_collection_concepts_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/concepts/')
        self.assertEqual(resolver.view_name, 'collection-concepts')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')


    def test_user_collection_mappings_viewname_to_url(self):
        url = reverse('collection-mappings', kwargs={"user": "testuser", "collection": "testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/mappings/')


    def test_user_collection_mappings_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/mappings/')
        self.assertEqual(resolver.view_name, 'collection-mappings')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')


    def test_user_collection_sources_viewname_to_url(self):
        url = reverse('collection-sources', kwargs={"user": "testuser", "collection": "testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/sources/')


    def test_user_collection_sources_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/sources/')
        self.assertEqual(resolver.view_name, 'collection-sources')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')


    def test_user_collection_collections_viewname_to_url(self):
        url = reverse('collection-collections', kwargs={"user": "testuser", "collection": "testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/collections/')


    def test_user_collection_collections_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/collections/')
        self.assertEqual(resolver.view_name, 'collection-collections')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_collection_delete_viewname_to_url(self):
        url = reverse('collection-delete', kwargs={"user": "testuser", "collection": "testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/delete/')


    def test_user_collection_delete_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/delete/')
        self.assertEqual(resolver.view_name, 'collection-delete')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')

    def test_user_source_delete_viewname_to_url(self):
        url = reverse('source-delete', kwargs={"user": "testuser", "source": "testsource"})
        self.assertEqual(url, '/users/testuser/sources/testsource/delete/')

    def test_user_source_delete_url_to_viewname(self):
        resolver = resolve('/users/testuser/sources/testsource/delete/')
        self.assertEqual(resolver.view_name, 'source-delete')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['source'], 'testsource')
