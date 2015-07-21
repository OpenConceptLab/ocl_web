"""
    Custom template tags for OCL Web.

    TODO: The label tags could take an optional arg to not include the href,
    but not sure if we want that anyway.
"""
import re
import dateutil.parser

from django import template
from django.template.base import (Node, NodeList)


from libs.ocl import OCLapi


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


@register.inclusion_tag('includes/org_label_incl.html')
def org_label(org, size=None):
    return {'org':org, 'size':size}


@register.inclusion_tag('includes/user_label_incl.html')
def user_label(user, size=None):
    return {'user':user, 'size':size}


@register.inclusion_tag('includes/source_owner_label_incl.html')
def source_owner_label(source, size=None):
    """
    Display a label for a source owner, which can be either a
    user or an organization.
    Note that this tag displays the *owner* of the source, not the source.

    :param source: is the OCL source object.
    """
    from_org = source.get('owner_type').lower() == 'organization'
    return {
        'from_org': from_org,
        'source': source,
        'size': size
    }

@register.inclusion_tag('includes/source_label_incl.html')
def source_label(source, size=None):
    """ Source label """
    return {'source':source, 'size':size}


@register.inclusion_tag('includes/concept_label_incl.html')
def concept_label(concept, size=None):
    """ Concept label """
    return {'concept':concept, 'size':size}


@register.inclusion_tag('includes/mapping_label_incl.html')
def mapping_label(mapping, size=None):
    return {'mapping':mapping, 'size':size}

@register.inclusion_tag('includes/mapping_from_concept_label_incl.html')
def mapping_from_concept_label(mapping, size=None):
    return {'mapping':mapping, 'size':size}

@register.inclusion_tag('includes/mapping_to_concept_label_incl.html')
def mapping_to_concept_label(mapping, size=None):
    return {'mapping':mapping, 'size':size}

@register.inclusion_tag('includes/field_display_incl.html')
def field_label(label, value, url=False, truncate=True, vertical=False, small=False):
    """
        Display a simple read only field value to user, like:

        field label text: field value

        See the include template for details.
        :param url: If true, displays value as an anchor tag
        :param truncate: If true (default), display text is truncated
        :param vertical: Default is a horizontal display using bootstrap grid divs. 
            Set vertical to true to display in a vertical layout instead.
    """
    TRUNCATE_LENGTH = 97      # 100 minus 3 for the ellipses
    url_string = ''
    if url:
        url_string = value
    value = u'%s' % value
    if truncate and len(value) > (TRUNCATE_LENGTH + 3):
        value = value[:TRUNCATE_LENGTH] + '...'
    return {
        'field_label': label,
        'field_value': value,
        'url_value': url_string,
        'is_url': url,
        'vertical': vertical,
        'small': small
    }


@register.inclusion_tag('includes/simple_pager_incl.html')
def simple_pager(page, name, url=None):
    """
        Display a simple pager with N-M of P {name}[<] [>]

        :param page: is a django paginator Page object.
        :param name: is for display the item's name.
        :url: is the GET url used to invoke the other page, usually
            includes query parameters.
    """

    if url:
        # Remove existing page GET parameters
        # Should use force_text, see django-bootstrap3...
        url = re.sub(r'\?page\=[^\&]+', '?', url)
        url = re.sub(r'\&page\=[^\&]+', '', url)
        # Append proper separator
        if '?' in url:
            url += '&'
        else:
            url += '?'

    return {
        'page': page,
        'name': name,
        'url': url,
    }


class IfCanChangeNode(Node):

    def __init__(self, nodelist_true, nodelist_false, obj_var):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.obj_var = template.Variable(obj_var)

    def render(self, context):
        # Init state storage
        try:
            obj = self.obj_var.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        user = context['user']
        can = False
        if obj.get('type') == 'Organization':
            can = user.is_authenticated()
            # TODO: Actually we need to check to see if this user/member
            # is an administrative member of this org. How?

        elif obj.get('owner_type') == 'Organization':
            # member can change
            # TODO: need a better API call to check for access
            api = OCLapi(context['request'], debug=True)
            results = api.get('orgs', obj.get('owner'), 'members',
                              user.username)
            if results.status_code == 204:
                can = True
            print 'ACCESS Check:', results.status_code

        else:
            # owned by a user
            can = True

        if can:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.tag('if_can_change')
def do_if_can_change(parser, token):
    """
    The ``{% if_can_change source_or_concept %}`` tag
    evaluates whether the current user have
    access to the specified object.

    If so, the block bracketed are output.

    ::

        {% if_can_change source %}

        {% endif_can_change %}


    """
    # {% if ... %}
    # NOTE: the obj_var can also be a source, org or concept
    obj_var = token.split_contents()[1]

    nodelist_true = parser.parse(('else', 'endif_can_change'))

    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_can_change',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return IfCanChangeNode(nodelist_true, nodelist_false, obj_var)


@register.filter(name='get')
def get(d, k):
    return d.get(k, None)