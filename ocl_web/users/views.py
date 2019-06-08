"""OCL Users
"""

import simplejson as json

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import ListView
from django.contrib import messages


# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from django.views.generic import View

from .forms import UserForm

# Import the customized User model
from .models import User
from libs.ocl import OclApi
from django.http import HttpResponse



class UserDetailView(LoginRequiredMixin, DetailView):
    """OCL Users Detail view
    """

    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        """Set the context for OCL user
        """

        context = super(UserDetailView, self).get_context_data(*args, **kwargs)

        # Setup API calls
        username = (kwargs["object"].username)
        api = OclApi(self.request, debug=True)

        # Set the limit of records for standard display
        # TODO(paynejd@gmail.com): Create page for each user resource list to handle > than limit
        limit = 20

        ocl_user = api.get('users', username).json()
        ocl_user_orgs = api.get('users', username, 'orgs', params={'limit':limit}).json()
        ocl_user_sources = api.get('users', username, 'sources', params={'limit':limit}).json()
        ocl_user_collections = api.get('users', username, 'collections', params={'limit':limit}).json()

        # Set the selected tab
        default_tab = 'repositories'
        if 'tab' in self.request.GET:
            selected_tab = self.request.GET.get('tab').lower()
            if selected_tab not in ('repositories', 'organizations'):
                selected_tab = default_tab
        else:
            selected_tab = default_tab

        # Set the context
        context['ocl_user'] = ocl_user
        context['orgs'] = ocl_user_orgs
        context['sources'] = ocl_user_sources
        context['collections'] = ocl_user_collections
        context['selected_tab'] = selected_tab

        if self.request.user.username == username:
            context['api_token'] = api.api_key
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """User Redirect View
    """

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, FormView):
    """Update a user profile, need to update both web side and API side.
    """

    form_class = UserForm
    template_name = 'users/user_form.html'

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.kwargs.get('username')})

    def get_initial(self):
        user = User.objects.get(username=self.kwargs.get('username'))
        api = OclApi(self.request)
        result = api.get('users', user.username)
        api_user = result.json()
        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        data.update(api_user)
        return data

    def form_valid(self, form):
        """
            User entry is good, update both web database and backend.
        """
        print form.cleaned_data
        # only pass updatable fields to backend
        field_names = ('first_name', 'last_name', 'company', 'location')
        data = dict([(k, v) for k, v in form.cleaned_data.iteritems() if k in field_names])
        api = OclApi(self.request)
        result = api.post('user', **data)
        print result.status_code
        if len(result.text) > 0:
            print result.json()

        messages.add_message(self.request, messages.INFO, _('User updated'))
        return HttpResponseRedirect(self.get_success_url())


class UserListView(LoginRequiredMixin, ListView):
    """User List View
    """

    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserJsonView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse(status=401)
        api = OclApi(self.request, debug=True)
        result = api.get('users', params={'limit': '0'})
        return HttpResponse(json.dumps(result.json()), content_type="application/json")


class UserSourcesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get("user")
        if not (request.user.is_staff or request.user.username == username):
            return HttpResponse(status=401)
        api = OclApi(self.request, debug=True)
        result = api.get('users', username, "sources", params={'limit': '0'})
        return HttpResponse(json.dumps(result.json()), content_type="application/json")

class UserCollectionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        username = kwargs.get("user")
        if not (request.user.is_staff or request.user.username == username):
            return HttpResponse(status=401)
        api = OclApi(self.request, debug=True)
        result = api.get('users', username, "collections", params={'limit': '0'})
        return HttpResponse(json.dumps(result.json()), content_type="application/json")
