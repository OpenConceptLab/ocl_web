from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from .forms import (ConceptCreateForm, ConceptNameFormSet)


from libs.ocl import OCLapi


class ConceptDetailView(TemplateView):
    template_name = "concepts/concept.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ConceptDetailView, self).get_context_data(*args, **kwargs)

        fake_concept = dict(
            id="A15.1",
            conceptClass="Diagnosis",
            datatype="None",
            retired=False,
            source="ICD-10",
            owner="WHO",
            ownerType="Organization",
            displayName="Tuberculosis of lung, confirmed by culture only",
            displayLocale="en",
            versioned_object_url="http://65.99.230.144/v1/orgs/WHO/sources/ICD-10/concepts/A15.1/",
            url="http://65.99.230.144/v1/orgs/WHO/sources/ICD-10/concepts/A15.1/52957df350d61b2b63e18f88/",
            descriptions=[
                dict(
                    locale="en",
                    type=None,
                    name="Tuberculous bronchiectasis, fibrosis of lung, pneumonia, pneumothorax, confirmed by sputum microscopy with culture only",
                    localePreferred=False
                ),
                dict(
                    locale="fr",
                    type=None,
                    name="French definition!",
                    localePreferred=False
                )
            ],
            names=[
                dict(
                    locale="en",
                    type=None,
                    name="Tuberculosis of lung, confirmed by culture only",
                    localePreferred=True
                ),
                dict(
                    locale="fr",
                    type=None,
                    name="Tuberculose pulmonaire, confirmee par culture seulement",
                    localePreferred=False
                )
            ]
        )




        context['concept'] = fake_concept


        org_id = self.kwargs.get('org')
        source_id = self.kwargs.get('source')
        concept_id = self.kwargs.get('concept')

        api = OCLapi(self.request, debug=True)

        concept = api.get('orgs', org_id, 'sources', source_id, 'concepts', concept_id).json()
        context['concept'] = concept
        return context


class ConceptCreateView(FormView):

    form_class = ConceptCreateForm
    template_name = "concepts/concept_create.html"

    def get_success_url(self):
        return reverse("source-detail",
                    kwargs={"org": self.kwargs.get('org'),
                            'source': self.kwargs.get('source')})

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form
        """
        context = super(ConceptCreateView, self).get_context_data(*args, **kwargs)

        source_id = self.kwargs.get('source')
        org_id = self.kwargs.get('org')

        api = OCLapi(self.request, debug=True)

        source = api.get('orgs', org_id, 'sources', source_id).json()
        context['source'] = source
        return context

    def get_initial(self):
        """ Load some useful data, not really for form display but internal use """
        source_id = self.kwargs.get('source')
        org_id = self.kwargs.get('org')

        api = OCLapi(self.request, debug=True)

        source = api.get('orgs', org_id, 'sources', source_id).json()
        data = {
            'source': source,
            'request': self.request,
            }
        return data


    def form_valid(self, form, *args, **kwargs):

        source_id = self.kwargs.get('source')
        org_id = self.kwargs.get('org')

        print form.cleaned_data

        data = {}
        data['id'] = form.cleaned_data['concept_id']
        data['concept_class'] = form.cleaned_data['concept_class']
        data['datatype'] = form.cleaned_data['datatype']

        name = {}
        name['name'] = form.cleaned_data['name']
        name['locale'] = form.cleaned_data['locale']
        name['preferred'] = form.cleaned_data['preferred_locale']
        names = [name]

        api = OCLapi(self.request, debug=True)
        result = api.create_concept(org_id, source_id, data, names=names)
        print result.status_code
        print result.json()
        messages.add_message(self.request, messages.INFO, _('Concept Added'))
        return HttpResponseRedirect(self.get_success_url())


class ConceptNamesUpdateView(FormView):
    """
    Update or add names to a concept.
    """
    form_class = ConceptNameFormSet
    template_name = "concepts/concept_names.html"

    def get_success_url(self):
        return reverse("source-detail",
                    kwargs={"org": self.kwargs.get('org'),
                            'source': self.kwargs.get('source')})

    def get_context_data(self, *args, **kwargs):
        """ Supply related data for the add form
        """
        context = super(ConceptNamesUpdateView, self).get_context_data(*args, **kwargs)

        source_id = self.kwargs.get('source')
        org_id = self.kwargs.get('org')

        api = OCLapi(self.request, debug=True)

        source = api.get('orgs', org_id, 'sources', source_id).json()
        context['source'] = source

        context['formset'] = context['form']
        return context

    def get_initialx(self):
        """ Load some useful data, not really for form display but internal use """
        print self.kwargs
        source_id = self.kwargs.get('source')
        org_id = self.kwargs.get('org')

        api = OCLapi(self.request, debug=True)

        source = api.get('orgs', org_id, 'sources', source_id).json()
        data = {
            'source': source,
            'request': self.request,
            }
        return data


    def form_valid(self, form, *args, **kwargs):


        messages.add_message(self.request, messages.INFO, _('Concept Added'))
        return HttpResponseRedirect(self.get_success_url())

        org_id = form.cleaned_data.pop('short_name')
        name = form.cleaned_data.pop('full_name')



