# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView

from django.conf import settings
import requests

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import UserForm

# Import the customized User model
from .models import User



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):

        context = super(UserDetailView, self).get_context_data(*args, **kwargs)

        # Setup API calls
        username = (kwargs["object"].username)
        host = settings.API_HOST
        auth_token = settings.API_TOKEN

        ocl_user_url = "%s/v1/users/%s/" % (host, username)
        ocl_user_orgs_url = ocl_user_url + "orgs/"
        ocl_user_sources_url = ocl_user_url + "sources/"
        ocl_user_collections_url = ocl_user_url + "collections/"
        requestHeaders = {'Authorization': auth_token}

        # API calls
        ocl_user = requests.get(ocl_user_url, headers=requestHeaders).json()
        ocl_user_orgs = requests.get(ocl_user_orgs_url, headers=requestHeaders).json()
        ocl_user_sources = requests.get(ocl_user_sources_url, headers=requestHeaders).json()
        ocl_user_collections = requests.get(ocl_user_collections_url, headers=requestHeaders).json()

        # Set the context
        context['ocl_user'] = ocl_user
        context['orgs'] = ocl_user_orgs
        context['sources'] = ocl_user_sources
        context['collections'] = ocl_user_collections

        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
            kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                    kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"