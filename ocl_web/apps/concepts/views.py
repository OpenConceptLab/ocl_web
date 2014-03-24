from django.views.generic import TemplateView
from django.conf import settings
import requests


class ConceptDetailView(TemplateView):
    template_name = "concepts/concept.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ConceptDetailView, self).get_context_data(*args, **kwargs)

        host = settings.API_HOST
        auth_token = settings.API_TOKEN
        full_path = host + uri_path
        headers = {'Authorization': auth_token}

        results = requests.get(full_path, headers=headers)
        context['results'] = results.json()

        import pdb; pdb.set_trace()
        return context




