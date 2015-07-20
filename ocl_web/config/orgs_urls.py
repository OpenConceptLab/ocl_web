# -*- coding: utf-8 -*-
"""
URL Configuration for "/orgs/..." and all its children.

Regex expression not split across lines -- pylint warnings for long lines supressed
with "# pylint: disable=C0301"
"""

from __future__ import unicode_literals

from django.conf.urls import (patterns, url)
from apps.orgs.views import (
    OrganizationDetailsView, OrganizationAboutView, OrganizationSourcesView,
    OrganizationNewView, OrganizationEditView,
    OrganizationMemberAddView, OrganizationMemberRemoveView)
from apps.sources.views import (
    SourceDetailsView, SourceAboutView, SourceConceptsView, SourceMappingsView,
    SourceCreateView, SourceEditView, SourceVersionsView)
from apps.mappings.views import (MappingDetailsView)
from apps.concepts.views import (
    ConceptDetailsView, ConceptMappingsView, ConceptHistoryView,
    ConceptDetailView, ConceptCreateJsonView, ConceptRetireView, ConceptNewView,
    ConceptDescView, ConceptNameView, ConceptVersionListView, ConceptMappingView)
from apps.core.views import ExtraJsonView

# TODO(paynejd@gmail.com): Collections not implemented yet
#from apps.collections.views import (
#    CollectionDetailView, CollectionCreateView, CollectionEditView)

# TODO(paynejd@gmail.com): OLD -- remove after tested
#from apps.sources.views import (SourceDetailView, SourceVersionView)



urlpatterns = patterns(
    '',

    ## ORGANIZATION

    # /orgs/new/ - create new org
    url(r'^new/$', OrganizationNewView.as_view(), name='org-new'),

    # /orgs/:org/ - points to /orgs/:org/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$',
        OrganizationDetailsView.as_view(), name='org-home'),

    # /orgs/:org/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/edit/$',
        OrganizationEditView.as_view(), name='org-edit'),

    # /orgs/:org/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/details/$',
        OrganizationDetailsView.as_view(), name='org-details'),

    # /orgs/:org/about/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/about/$',
        OrganizationAboutView.as_view(), name='org-about'),

    # /orgs/:org/sources/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/$',
        OrganizationSourcesView.as_view(), name='org-sources'),

    # /orgs/:org/collections/
    # TODO(paynejd@gmail.com): Activate /orgs/:org/collections/ after implemented
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/$',
    #    OrganizationCollectionsView.as_view(), name='org-collections'),


    ## ORGANIZATION MEMBERS

    # /orgs/:org/members/add/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/add/$',
        OrganizationMemberAddView.as_view(), name='org-member-add'),

    # /orgs/:org/members/remove/:username/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/remove/(?P<username>[a-zA-Z0-9\-\.]+)/$',
        OrganizationMemberRemoveView.as_view(), name='org-member-remove'),


    ## SOURCES CORE

    # /orgs/:org/sources/new/ - create new source
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/new/$',
        SourceCreateView.as_view(), name='source-create-for-org'),

    # /orgs/:org/sources/:source/ - points to /orgs/:org/sources/:source/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$',
        SourceDetailsView.as_view(), name='source-home'),

    # /orgs/:org/sources/:source/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
        SourceEditView.as_view(), name='source-edit'),

    # /orgs/:org/sources/:source/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/details/$',
        SourceDetailsView.as_view(), name='source-details'),

    # /orgs/:org/sources/:source/about/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/about/$',
        SourceAboutView.as_view(), name='source-about'),

    # /orgs/:org/sources/:source/concepts/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/$',
        SourceConceptsView.as_view(), name='source-concepts'),

    # /orgs/:org/sources/:source/:version/concepts/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/concepts/$',    # pylint: disable=C0301
        SourceConceptsView.as_view(), name='source-version-concepts'),

    # /orgs/:org/sources/:source/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/$',
        SourceMappingsView.as_view(), name='source-mappings'),

    # /orgs/:org/sources/:source/:version/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        SourceMappingsView.as_view(), name='source-version-mappings'),

    # /orgs/:org/sources/:source/versions/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
        SourceVersionsView.as_view(), name='source-versions'),


    # /orgs/:org/sources/:source/versions/ - JSON ONLY - Angular
    # TODO(paynejd@gmail.com): Overwritten- old source versions will fail now
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
    #    SourceVersionView.as_view(), name='source-version-cl'),

    # /orgs/:org/sources/:source/versions/:source-version/ - JSON ONLY - Angular
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/(?P<version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    SourceVersionView.as_view(), name='source-version-ud'),

    # /orgs/:org/sources/:source/extras/ - JSON ONLY - Angular
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/$',
    #    ExtraJsonView.as_view(), name='source-extra'),

    # /orgs/:org/sources/:source/extras/:extra/ - JSON ONLY - Angular
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ExtraJsonView.as_view(), name='source-extra-add'),


    ## COLLECTIONS

    # TODO(paynejd@gmail.com): collections URLs
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/$',
    #    CollectionDetailView.as_view(), name='collection-detail'),
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/$',
    #    CollectionCreateView.as_view(), name='collection-create-for-org'),
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
    #    SourceEditView.as_view(), name='collection-edit'),


    ## CONCEPTS

    # /orgs/:org/sources/:source/concepts/new/ - create new concept
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/new/$',
        ConceptNewView.as_view(), name='concept-new-for-org'),

    # New concept: /orgs/:org/sources/:source/create/ - RETIRE
    # TODO(paynejd@gmail.com): Retire this - replaced by above
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$',
    #    ConceptCreateJsonView.as_view(), name='concept-create-for-org'),

    # /orgs/:org/sources/:source/concepts/:concept/ - points to concept details
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-home'),

    # /orgs/:org/sources/:source/concepts/:concept/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-details'),

    # /orgs/:org/sources/:source/concepts/:concept/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-mappings'),

    # /orgs/:org/sources/:source/concepts/:concept/history/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-history'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/ - points to concept details
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-home'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-details'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-version-mappings'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/history/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-version-history'),




    # /orgs/:org/sources/:source/concepts/:concept/edit/ - MODIFY
    # TODO(paynejd@gmail.com): This page is going to need to be completely rewritten - point to different view
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        ConceptCreateJsonView.as_view(), name='concept-edit'),

    # /orgs/:org/sources/:source/concepts/:concept/retire/ - UNKNOWN
    # TODO(paynejd@gmail.com): Confirm that this is actually used
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        ConceptRetireView.as_view(), name='concept-retire'),

    # /orgs/:org/sources/:source/concepts/:concept/versions/ - RETIRE
    # TODO(paynejd@gmail.com): Retire this - replaced by 'history' tab above
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/versions/$',    # pylint: disable=C0301
        ConceptVersionListView.as_view(), name='concept-version-list'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/versions/ - RETIRE
    # TODO(paynejd@gmail.com): This looks screwy - I think that this was not actually implemented
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/versions/$',    # pylint: disable=C0301
        ConceptVersionListView.as_view(), name='concept-version-list'),




    ## CONCEPT NAMES

    # /orgs/:org/sources/:source/concepts/:concept/names/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/names/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/names/:concept-name/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-ud'),


    ## CONCEPT DESCRIPTIONS

    # /orgs/:org/sources/:source/concepts/:concept/descriptions/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/descriptions/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/descriptions/:description/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-ud'),


    ## MAPPINGS

    # /orgs/:org/sources/:source/mappings/:mapping/ - ??
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-home'),

    # /orgs/:org/sources/:source/mappings/:mapping/ - ??
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-details'),

    # TODO(paynejd@gmail.com): Below Mapping URLs are not implemented correctly

    # /orgs/:org/sources/:source/concepts/:concept/mappings/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='concept-mapping-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/mappings/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='concept-mapping-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/mappings/:mapping/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='concept-mapping-ud'),

    # /orgs/:org/sources/:source/mappings/:mapping/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='mapping-ud'),


    ## CONCEPT EXTRAS

    # /orgs/:org/sources/:source/concepts/:concept/extras/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/extras/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /orgs/:org/sources/:source/concepts/:concept/extras/:extra/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra-add'),


    # IMPORTANT: we have to move this to the end because the version value - RETIRE
    # can be misinterpreted as /names/ /descriptions/ etc et. Not great URL design
    # TODO(paynejd@gmail.com): This is blocked by items above -- make sure everything works!
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ConceptDetailView.as_view(), name='concept-details'),
)
