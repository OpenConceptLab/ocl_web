"""
Test views
"""
import requests

from django.views.generic import (TemplateView, View)

class TestTagsView(TemplateView):
	"""
    View to test resource tags
    """
    template_name = "tests/tags.html"

    def get_context_data(self, *args, **kwargs):
    	""" Do nothing for now """
    	return {}