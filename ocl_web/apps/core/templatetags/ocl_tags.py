"""
    Custom template tags for OCL Web.
"""
import dateutil.parser

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

register = template.Library()

@register.filter
def smart_datetime(iso8601_dt):
    """
        Return a friendly date time display.
        Currently just localized, but eventually "two days ago", etc.
    """
    dt = dateutil.parser.parse(iso8601_dt)
    return dt.strftime('%c')

@register.filter
def smart_date(iso8601_dt):
    """
        Return a friendly date display.
        Currently just localized, but eventually "two days ago", etc.
    """
    dt = dateutil.parser.parse(iso8601_dt)
    return dt.strftime('%x')
