from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from .views import OrganizationDetailView, OrganizationCreateView

__author__ = 'briandant'

urlpatterns = patterns('',
#    url(r'^$', OrganizationListView.as_view(), name='organization-list'),
    url(r'^new/$', OrganizationCreateView.as_view(), name='org-new'),
    url(r'^new/success/$', TemplateView.as_view(template_name='orgs/org_new_success.html'), name='org-new-success'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$', OrganizationDetailView.as_view(), name='org-detail'),
#    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/$', UserListView.as_view(), {'related_object_type': Organization, 'related_object_kwarg': 'org', 'related_object_attribute': 'members'}, name='organization-members'),
#    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/(?P<user>[a-zA-Z0-9\-]+)/$', OrganizationMemberView.as_view(), name='organization-member-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/', include('apps.sources.urls')),
#    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/', include('conceptcollections.urls')),
)
