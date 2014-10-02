# -*- coding: utf-8 -*-
"""
    urls that starts with "users"
"""
from django.conf.urls import patterns, url

from users.views import (UserListView, UserRedirectView, UserDetailView, UserUpdateView)
from apps.sources.views import (SourceDetailView, SourceCreateView, SourceEditView)
from apps.concepts.views import (ConceptDetailView, ConceptCreateView, ConceptEditView)
from apps.concepts.views import (ConceptNamesUpdateView, ConceptNameAddView)

urlpatterns = patterns('',
    # URL pattern for the UserListView
#    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/', include('apps.sources.urls')),


    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/$', SourceCreateView.as_view(), name='source-create-for-user'),
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$', SourceDetailView.as_view(), name='source-detail'),
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$', SourceEditView.as_view(), name='source-edit'),


    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$', ConceptCreateView.as_view(), name='concept-create-for-user'),

    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptNameAddView.as_view(), name='concept-detail'),
#    url(r'^update/names/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptNamesUpdateView.as_view(), name='concept-names-update'),
#    url(r'^detail/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/name/add/$', ConceptNameAddView.as_view(), name='concept-name-add'),

    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$', ConceptEditView.as_view(), name='concept-edit'),

    url(
        regex=r'^$',
        view=UserListView.as_view(),
        name='list'
    ),
    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=UserRedirectView.as_view(),
        name='redirect'
    ),
    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<username>[\w\-_]+)/$',
        view=UserDetailView.as_view(),
        name='detail'
    ),
    # URL pattern for the UserUpdateView
    url(
        regex=r'^update/(?P<username>[\w\-_]+)/$',
        view=UserUpdateView.as_view(),
        name='update'
    ),
)
