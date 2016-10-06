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

    def test_org_collection_version_json_edit_viewname_to_url(self):
        url = reverse('collection-version-json-edit', kwargs={"org": "org", "collection": "testcol", "collection_version": "v1"})
        self.assertEqual(url, '/orgs/org/collections/testcol/v1/json/edit/')

    def test_org_collection_version_edit_url_to_viewname(self):
        resolver = resolve('/orgs/org/collections/coll/v1/json/edit/')
        self.assertEqual(resolver.view_name, 'collection-version-json-edit')
        self.assertEqual(resolver.kwargs['org'], 'org')
        self.assertEqual(resolver.kwargs['collection'], 'coll')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')

    def test_org_source_version_json_edit_viewname_to_url(self):
        url = reverse('source-version-json-edit', kwargs={"org": "org", "source": "source", "source_version": "v1"})
        self.assertEqual(url, '/orgs/org/sources/source/v1/json/edit/')

    def test_org_source_version_edit_url_to_viewname(self):
        resolver = resolve('/orgs/org/sources/source/v1/json/edit/')
        self.assertEqual(resolver.view_name, 'source-version-json-edit')
        self.assertEqual(resolver.kwargs['org'], 'org')
        self.assertEqual(resolver.kwargs['source'], 'source')
        self.assertEqual(resolver.kwargs['source_version'], 'v1')

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


    def test_collections_references_viewname_to_url(self):
        url = reverse('collection-references', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/references/')

    def test_url_to_collections_references_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/references/')
        self.assertEqual(resolver.view_name, 'collection-references')

    def test_org_collection_references_delete_viewname_to_url(self):
        url = reverse('collection-references-delete', kwargs={"org": "org", "collection": "testcol"})
        self.assertEqual(url, '/orgs/org/collections/testcol/references/delete/')

    def test_org_collection_reference_delete_url_to_viewname(self):
        resolver = resolve('/orgs/org/collections/coll/references/delete/')
        self.assertEqual(resolver.view_name, 'collection-references-delete')
        self.assertEqual(resolver.kwargs['org'], 'org')
        self.assertEqual(resolver.kwargs['collection'], 'coll')

    def test_collections_delete_viewname_to_url(self):
        url = reverse('collection-delete', kwargs={'org': 'myorgs', 'collection': 'collection1'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/delete/')

    def test_url_to_collections_delete_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/delete/')
        self.assertEqual(resolver.view_name, 'collection-delete')

    def test_collections_version_delete_viewname_to_url(self):
        url = reverse('collection-version-delete', kwargs={'org': 'myorgs', 'collection': 'collection1','collection_version': 'testcolver'})
        self.assertEqual(url, '/orgs/myorgs/collections/collection1/testcolver/delete/')

    def test_url_to_collection_version_delete_viewname(self):
        resolver = resolve('/orgs/myorgs/collections/collection1/testcolver/delete/')
        self.assertEqual(resolver.view_name, 'collection-version-delete')

    def test_sources_delete_viewname_to_url(self):
        url = reverse('source-delete', kwargs={'org': 'myorgs', 'source': 'source1'})
        self.assertEqual(url, '/orgs/myorgs/sources/source1/delete/')

    def test_url_to_sources_delete_viewname(self):
        resolver = resolve('/orgs/myorgs/sources/source1/delete/')
        self.assertEqual(resolver.view_name, 'source-delete')

    def test_org_collection_references_viewname_to_url(self):
        url = reverse('collection-references', kwargs={"org": "testOrg", "collection": "collection1"})
        self.assertEqual(url, '/orgs/testOrg/collections/collection1/references/')

    def test_org_collection_references_url_to_viewname(self):
        resolver = resolve('/orgs/testOrg/collections/collection1/references/')
        self.assertEqual(resolver.view_name, 'collection-references')
        self.assertEqual(resolver.kwargs['org'], 'testOrg')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')

    def test_org_collection_addReferences_viewname_to_url(self):
        url = reverse('collection-addreference', kwargs={"org": "testOrg", "collection": "collection1"})
        self.assertEqual(url, '/orgs/testOrg/collections/collection1/references/new/')

    def test_org_collection_addReferences_url_to_viewname(self):
        resolver = resolve('/orgs/testOrg/collections/collection1/references/new/')
        self.assertEqual(resolver.view_name, 'collection-addreference')
        self.assertEqual(resolver.kwargs['org'], 'testOrg')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')

    def test_user_collection_version_home_url_to_viewname(self):
        resolver = resolve('/orgs/testOrg/collections/collection1/v1/')
        self.assertEqual(resolver.view_name, 'collection-version-home')
        self.assertEqual(resolver.kwargs['org'], 'testOrg')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')

    def test_user_collection_version_viewname_to_url(self):
        url = reverse('collection-version-home',
                      kwargs={"org": "testorg", "collection": "collection1", "collection_version": "v1"})
        self.assertEqual(url, '/orgs/testorg/collections/collection1/v1/')


    def test_collections_version_mappings_viewname_to_url(self):
        url = reverse('collection-mappings', kwargs={'org': 'testOrg', 'collection': 'collection1','collection_version':'v1'})
        self.assertEqual(url, '/orgs/testOrg/collections/collection1/v1/mappings/')

    def test_url_to_collections_version_mappings_viewname(self):
        resolver = resolve('/orgs/testOrg/collections/collection1/v1/mappings/')
        self.assertEqual(resolver.view_name, 'collection-mappings')
        self.assertEqual(resolver.kwargs['org'], 'testOrg')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')


    def test_collections_version_concepts_viewname_to_url(self):
        url = reverse('collection-version-concepts', kwargs={'org': 'testOrg', 'collection': 'collection1','collection_version':'v1'})
        self.assertEqual(url, '/orgs/testOrg/collections/collection1/v1/concepts/')

    def test_url_to_collections_version_concepts_viewname(self):
        resolver = resolve('/orgs/testOrg/collections/collection1/v1/concepts/')
        self.assertEqual(resolver.view_name, 'collection-version-concepts')
        self.assertEqual(resolver.kwargs['org'], 'testOrg')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')


    def test_collections_version_references_viewname_to_url(self):
        url = reverse('collection-version-references', kwargs={'org': 'testOrg', 'collection': 'collection1','collection_version':'v1'})
        self.assertEqual(url, '/orgs/testOrg/collections/collection1/v1/references/')

    def test_url_to_collections_version_references_viewname(self):
        resolver = resolve('/orgs/testOrg/collections/collection1/v1/references/')
        self.assertEqual(resolver.view_name, 'collection-version-references')
        self.assertEqual(resolver.kwargs['org'], 'testOrg')
        self.assertEqual(resolver.kwargs['collection'], 'collection1')
        self.assertEqual(resolver.kwargs['collection_version'], 'v1')

    def test_org_mapping_versions_mappings_to_viewname(self):
        resolver = resolve('/orgs/org1/sources/s1/mappings/m1/history/')
        self.assertEqual(resolver.view_name, 'mapping-versions')
        self.assertEqual(resolver.kwargs['org'], 'org1')
        self.assertEqual(resolver.kwargs['source'], 's1')
        self.assertEqual(resolver.kwargs['mapping'], 'm1')


    def test_org_mapping_versions_mappings_viewname_to_url(self):
        url = reverse('mapping-versions', kwargs={"org": "org1", "source": "s1","mapping":"m1"})
        self.assertEqual(url, '/orgs/org1/sources/s1/mappings/m1/history/')

    def test_org_mapping_version_mappings_to_viewname(self):
        resolver = resolve('/orgs/org1/sources/s1/mappings/m1/1/')
        self.assertEqual(resolver.view_name, 'mapping-version-home')
        self.assertEqual(resolver.kwargs['org'], 'org1')
        self.assertEqual(resolver.kwargs['source'], 's1')
        self.assertEqual(resolver.kwargs['mapping'], 'm1')
        self.assertEqual(resolver.kwargs['mapping_version'], '1')


    def test_org_mapping_version_mappings_viewname_to_url(self):
        url = reverse('mapping-version-home', kwargs={"org": "org1", "source": "s1","mapping":"m1","mapping_version":"1"})
        self.assertEqual(url, '/orgs/org1/sources/s1/mappings/m1/1/')

