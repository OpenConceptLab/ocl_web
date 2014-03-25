from django.views.generic import TemplateView
from django.conf import settings


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

        return context




