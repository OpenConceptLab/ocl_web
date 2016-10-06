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

    def test_user_collection_references_viewname_to_url(self):
        url = reverse('collection-references', kwargs={"user": "testuser", "collection": "testcol"})
        self.assertEqual(url, '/users/testuser/collections/testcol/references/')

    def test_user_collection_version_json_edit_viewname_to_url(self):
        url = reverse('collection-version-json-edit', kwargs={"user": "testuser", "collection": "testcol", "collection_version": "v1"})
        self.assertEqual(url, '/users/testuser/collections/testcol/v1/json/edit/')

    def test_user_collection_version_edit_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/coll/v1/json/edit/')
        self.assertEqual(resolver.view_name, 'collection-version-json-edit')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'coll')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')

    def test_user_source_version_json_edit_viewname_to_url(self):
        url = reverse('source-version-json-edit', kwargs={"user": "testuser", "source": "source", "source_version": "v1"})
        self.assertEqual(url, '/users/testuser/sources/source/v1/json/edit/')

    def test_user_source_version_edit_url_to_viewname(self):
        resolver = resolve('/users/testuser/sources/source/v1/json/edit/')
        self.assertEqual(resolver.view_name, 'source-version-json-edit')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['source'], 'source')
        self.assertEqual(resolver.kwargs['source_version'], 'v1')

    def test_user_collection_references_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/references/')
        self.assertEqual(resolver.view_name, 'collection-references')
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

    def test_user_collection_version_delete_viewname_to_url(self):
        url = reverse('collection-version-delete', kwargs={"user": "testuser", "collection": "testcol","collection_version":"testcolver"})
        self.assertEqual(url, '/users/testuser/collections/testcol/testcolver/delete/')


    def test_user_collection_version_delete_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/testcol/testcolver/delete/')
        self.assertEqual(resolver.view_name, 'collection-version-delete')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'testcol')
        self.assertEqual(resolver.kwargs['collection_version'], 'testcolver')

    def test_user_source_delete_viewname_to_url(self):
        url = reverse('source-delete', kwargs={"user": "testuser", "source": "testsource"})
        self.assertEqual(url, '/users/testuser/sources/testsource/delete/')

    def test_user_source_delete_url_to_viewname(self):
        resolver = resolve('/users/testuser/sources/testsource/delete/')
        self.assertEqual(resolver.view_name, 'source-delete')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['source'], 'testsource')

    def test_user_collection_references_viewname_to_url(self):
        url = reverse('collection-references', kwargs={"user": "testuser", "collection": "collection1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/references/')

    def test_user_collection_references_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/references/')
        self.assertEqual(resolver.view_name, 'collection-references')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')

    def test_user_collection_addReferences_viewname_to_url(self):
        url = reverse('collection-addreference', kwargs={"user": "testuser", "collection": "collection1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/references/new/')

    def test_user_collection_addReferences_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/references/new/')
        self.assertEqual(resolver.view_name, 'collection-addreference')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')

    def test_user_collection_add_version_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/versions/new/')
        self.assertEqual(resolver.view_name, 'collection-version-new')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')

    def test_user_collection_add_version_viewname_to_url(self):
        url = reverse('collection-version-new', kwargs={"user": "testuser", "collection": "collection1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/versions/new/')

    def test_user_collection_version_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/versions/')
        self.assertEqual(resolver.view_name, 'collection-versions')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')

    def test_user_collection_version_viewname_to_url(self):
        url = reverse('collection-versions', kwargs={"user": "testuser", "collection": "collection1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/versions/')


    def test_user_collection_version_home_url_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/v1/')
        self.assertEqual(resolver.view_name, 'collection-version-home')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')


    def test_user_collection_version_viewname_to_url(self):
        url = reverse('collection-version-home', kwargs={"user": "testuser", "collection": "collection1","collection_version":"v1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/v1/')


    def test_user_collection_version_concepts_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/v1/concepts/')
        self.assertEqual(resolver.view_name, 'collection-version-concepts')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')


    def test_user_collection_version_concepts_viewname_to_url(self):
        url = reverse('collection-version-concepts', kwargs={"user": "testuser", "collection": "collection1","collection_version":"v1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/v1/concepts/')


    def test_user_collection_version_mappings_to_viewname(self):
        resolver = resolve('/users/testuser/collections/collection1/v1/mappings/')
        self.assertEqual(resolver.view_name, 'collection-mappings')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')


    def test_user_collection_version_mappings_viewname_to_url(self):
        url = reverse('collection-mappings', kwargs={"user": "testuser", "collection": "collection1","collection_version":"v1"})
        self.assertEqual(url, '/users/testuser/collections/collection1/v1/mappings/')

    def test_user_mapping_versions_mappings_to_viewname(self):
        resolver = resolve('/users/testuser/sources/s1/mappings/m1/history/')
        self.assertEqual(resolver.view_name, 'mapping-versions')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['source'], 's1')
        self.assertEqual(resolver.kwargs['mapping'], 'm1')


    def test_user_mapping_versions_mappings_viewname_to_url(self):
        url = reverse('mapping-versions', kwargs={"user": "testuser", "source": "s1","mapping":"m1"})
        self.assertEqual(url, '/users/testuser/sources/s1/mappings/m1/history/')

    def test_user_mapping_version_mappings_to_viewname(self):
        resolver = resolve('/users/testuser/sources/s1/mappings/m1/1/')
        self.assertEqual(resolver.view_name, 'mapping-version-home')
        self.assertEqual(resolver.kwargs['user'], 'testuser')
        self.assertEqual(resolver.kwargs['source'], 's1')
        self.assertEqual(resolver.kwargs['mapping'], 'm1')
        self.assertEqual(resolver.kwargs['mapping_version'], '1')


    def test_user_mapping_version_mappings_viewname_to_url(self):
        url = reverse('mapping-version-home', kwargs={"user": "testuser", "source": "s1","mapping":"m1","mapping_version":"1"})
        self.assertEqual(url, '/users/testuser/sources/s1/mappings/m1/1/')

