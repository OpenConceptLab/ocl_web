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



## Custom Date Filters

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


# TODO: Retire this if not in use
@register.filter(name='get')
def get(d, k):
    return d.get(k, None)



## Custom Tags: RESOURCE LABELS

@register.inclusion_tag('includes/org_label_incl.html')
def org_label(org, label_size=None):
    """
    Independent org label, no breadcrumb. Ex:
    
        [:org-icon :org-id]
    """
    return {'org':org, 'label_size':label_size}


@register.inclusion_tag('includes/user_label_incl.html')
def user_label(user, label_size=None):
    """
    Independent user label, no breadcrumb. Ex:
    
        [:user-icon :username]
    """
    return {'user':user, 'label_size':label_size}


@register.inclusion_tag('includes/resource_owner_label_incl.html')
def resource_owner_label(resource, label_size=None):
    """
    Display a independent label (no breadcrumb) for the owner (a user or organization) of
    a resource, based on the "owner_type" and "owner". Ex:
    
        [:owner-type-icon :owner-id]

    :param resource: OCL resource with owner_type and owner attributes
    :param label_size: Currently ignored
    """
    return {
        'resource_owner_type': resource['owner_type'],
        'resource_owner': resource['owner'],
        'label_size': label_size
    }

@register.inclusion_tag('includes/source_label_incl.html')
def source_label(source, label_size=None):
    """
    Displays indepdent source label (no breadcrumb). Ex:

        [:source-icon :source-short-name]

    :param source: OCL source
    :param label_size: Currently ignored
    """
    return {
        'source':source,
        'label_size':label_size
    }


@register.inclusion_tag('includes/source_label_incl.html')
def generic_source_label(owner_type=None, owner_id=None,
                         source_id=None, source_name=None,
                         display_breadcrumb=False,
                         label_size=None):
    """
    TODO: generic_source_label template is not implemented yet

    Displays source label with options. Example with no breadcrumb:

        [:source-icon :source-short-name]

    Example with breadcrumb:

        [:source-icon :owner-id / :source-id :source-name]

    :param owner_type: (required) "Organization" or "User"
    :param owner_id: (optional) ID of the resource owner
    :param source_id: (required) ID of the source
    :param source_name: (optional) Name of the source
    :param display_breadcrumb: (optional) Whether to display source breadcrumb
    :param label_size: (optional) Currently ignored
    """
    return {
        'owner_type':owner_type,
        'owner_id':owner_id,
        'source_id':source_id,
        'source_name':source_name,
        'display_breadcrumb': display_breadcrumb,
        'label_size':label_size
    }


@register.inclusion_tag('includes/concept_label_incl.html')
def concept_label(concept, label_size=None):
    """
    Displays independent concept label (no breadcrumb). Ex:

        [:concept-icon :concept-id]

    :param concept: (required) OCL concept
    :param label_size: (ignored) Currently ignored
    """
    return {
        'concept':concept,
        'label_size':label_size
    }


@register.inclusion_tag('includes/mapping_label_incl.html')
def mapping_label(mapping, label_size=None, display_breadcrumb=False):
    """
    Displays mapping label. Ex with no breadcrumb:

        [:mapping-icon :mapping-id :map-type]

    Example with breadcrumb:

        [:mapping-icon :owner / :source / :mapping-id :map-type]

    :param mapping: (required) OCL mapping
    :param label_size: (ignored) Currently ignored
    :param display_breadcrumb: (optional) Whether to display source breadcrumb
    """
    return {
        'mapping': mapping,
        'label_size': label_size,
        'display_breadcrumb': display_breadcrumb
    }


@register.inclusion_tag('includes/mapping_from_concept_label_incl.html')
def mapping_from_concept_label(mapping, label_size=None):
    return {'mapping':mapping, 'label_size':label_size}


@register.inclusion_tag('includes/mapping_to_concept_label_incl.html')
def mapping_to_concept_label(mapping, label_size=None):
    return {'mapping':mapping, 'label_size':label_size}


@register.inclusion_tag('includes/generic_resource_label_incl.html')
def generic_resource_label(
        resource_type='', resource_id=None, resource_name=None, resource_version_id=None,
        resource_url=None, resource_retired=False,
        owner_type=None, owner_id=None,
        source_id=None, source_version_id=None,
        label_size='', display_icon=True, display_breadcrumb=False):
    """
    If display_breadcrumb == false:
        [:resource-icon :resource-id]
    Else:
        [:resource-icon :resource-id :resource-name]
        [:resource-icon :resource-id :resource-name]
        [:resource-icon :resource-id :resource-name]
    """

    # TODO: Set the URL

    # Validate resource type and set the icon type
    resource_type = resource_type.lower()
    default_resource_icon = 'question-sign'
    resource_icons = {
        'concept': 'tag',
        'mapping': 'link',
        'source': 'th-list',
        'collection': 'tags',
        'org': 'home',
        'user': 'user',
        'source-version': 'asterisk'
    }
    if resource_type in resource_icons:
        resource_icon = resource_icons[resource_type]
    else:
        resource_icon = default_resource_icon

    # Determine label size
    css_size_class = ''
    if label_size.lower() == 'small':
        css_size_class = 'small'
    elif label_size.lower() == 'large':
        css_size_class = 'large'

    # Setup the breadcrumb
    breadcrumb_parts = []
    if display_breadcrumb:
        # owner
        breadcrumb_parts.append({'text':owner_id, 'display_as_version':false, 'focus':false})
        if source_id:
            breadcrumb_parts.append({'text':source_id, 'display_as_version':false, 'focus':false})
        if source_version_id:
            breadcrumb_parts.append({'text':source_version_id, 'display_as_version':true, 'focus':false})
        if resource_type in ('concept','mapping'):
            breadcrumb_parts.append({'text':resource_id, 'display_as_version':false, 'focus':false})
            if resource_version_id:
                breadcrumb_parts.append({'text':resource_version_id, 'display_as_version':true, 'focus':false})

    return {
        'resource_type':resource_type,
        'resource_id':resource_id,
        'resource_name':resource_name,
        'resource_url':resource_url,
        'resource_icon':resource_icon,
        'owner_type':owner_type,
        'owner_id':owner_id,
        'source_id':source_id,
        'source_version_id':source_version_id,
        'label_size':label_size,
        'css_size_class':css_size_class,
        'display_icon':display_icon,
        'display_breadcrumb':display_breadcrumb,
        'breadcrumb_parts':breadcrumb_parts,
    }



## Custom Tags: FIELD LABEL

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



## Custom Tags: PAGINATION

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



## Custom Tags: PERMISSION CHECKING

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
