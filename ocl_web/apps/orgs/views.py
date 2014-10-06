from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from .forms import (OrganizationCreateForm, OrganizationEditForm)

from libs.ocl import OCLapi


class OrganizationDetailView(TemplateView):

    template_name = "orgs/org_detail.html"

    def get_context_data(self, *args, **kwargs):
        """Gets the org first, then the sources of that org, and then the
        concepts from each of those sources.

        Final context
        -------------
        context['org']
        context['sources']
        context['collections']
        context['members']
        """

        context = super(OrganizationDetailView, self).get_context_data(*args, **kwargs)

        org_id = self.kwargs.get('org')

        api = OCLapi(self.request, debug=True)

        org = api.get('orgs', org_id).json()

        # Get sources owned by the org
        sources = api.get('orgs', org_id, 'sources', '?verbose=True').json()

        # Get collections owned by the org
        # The org object should have the URL in the future, like members_url.
        collections = api.get('orgs', org_id, 'collections', '?verbose=True').json()

        # TODO: access issue, error if user is not super user??
        members = []
        r = api.get('orgs', org_id, 'members')
        if r.status_code == 200:
            members = r.json()
        elif r.status_code != 404:
#            raise Exception(r.json())
            pass
        # Set the context

        context['org'] = org
        context['sources'] = sources
        context['collections'] = collections
        context['members'] = members

        return context


class OrganizationCreateView(FormView):

    form_class = OrganizationCreateForm
    template_name = "orgs/org_new.html"

    def form_valid(self, form, *args, **kwargs):

        org_id = form.cleaned_data.pop('short_name')

        api = OCLapi(self.request, debug=True)

        data = {
            'id': org_id,
        }
        data.update(form.cleaned_data)
        print form.cleaned_data
        print data
        result = api.create_org(data)

        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Organization Added'))
            return redirect(reverse('org-detail', kwargs={'org': org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationCreateView, self).form_invalid(self, *args, **kwargs)


class OrganizationEditView(FormView):

    template_name = 'orgs/org_edit.html'

    def get_form_class(self):
        """ Trick to do some initial lookup """
        self.org_id = self.kwargs.get('org')
        api = OCLapi(self.request, debug=True)
        self.org = api.get('orgs', self.org_id).json()
        return OrganizationEditForm

    def get_context_data(self, *args, **kwargs):

        context = super(OrganizationEditView, self).get_context_data(*args, **kwargs)
        context['org'] = self.org
        return context

    def get_initial(self):
        return self.org

    def form_valid(self, form, *args, **kwargs):

        api = OCLapi(self.request, debug=True)

        data = {}
        data.update(form.cleaned_data)
        result = api.update_org(self.org_id, data)
        # TODO:  Catch exceptions that will be raised by
        # Ocl lib.
        if result.ok:
            messages.add_message(self.request, messages.INFO, _('Organization updated.'))
            return redirect(reverse('org-detail', kwargs={'org': self.org_id}))

        # TODO:  Add error messages from API to form.
        else:
            return super(OrganizationEditView, self).form_invalid(self, *args, **kwargs)
