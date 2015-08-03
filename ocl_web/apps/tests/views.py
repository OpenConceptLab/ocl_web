"""
Test views
"""
from django.views.generic import TemplateView

class TestTagsView(TemplateView):
    """
    View to test resource tags
    """
    template_name = "tests/tags.html"
