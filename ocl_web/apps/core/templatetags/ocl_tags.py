"""
    Custom template tags for OCL Web.

    TODO: The label tags could take an optional arg to not include the href,
    but not sure if we want that anyway.
"""
import re
import dateutil.parser
from django import template
from django.template.base import (Node, NodeList)
from libs.ocl import OclApi

register = template.Library()



# Number of characters to display in field tag - subtract 3 to account for the ellipses
TRUNCATE_LENGTH = 97


## Custom Date Filters

@register.filter
def smart_datetime(iso8601_dt):
    """
    Return a friendly date time display.
    Currently just localized, but eventually "two days ago", etc.
    """
    date_value = dateutil.parser.parse(iso8601_dt)
    return date_value.strftime('%c')


@register.filter
def smart_date(iso8601_dt):
    """
    Return a friendly date display.
    Currently just localized, but eventually "two days ago", etc.
    """
    date_value = dateutil.parser.parse(iso8601_dt)
    return date_value.strftime('%x')


## Custom Tags: RESOURCE LABELS

@register.inclusion_tag('includes/org_label_incl.html')
def org_label(org, label_size=None):
    """
    Independent org label, no breadcrumb. Ex:

        [:org-icon :org-id]

    :param org: OCL org resource
    :param label_size: No value is 'medium'; Acceptable values are 'small' or 'large'
    """
    return {'org':org, 'label_size':label_size}


@register.inclusion_tag('includes/user_label_incl.html')
def user_label(user, label_size=None):
    """
    Independent user label, no breadcrumb. Ex:

        [:user-icon :username]

    :param user: OCL user resource
    :param label_size: No value is 'medium'; Acceptable values are 'small' or 'large'
    """
    return {'user':user, 'label_size':label_size}


@register.inclusion_tag('includes/resource_owner_label_incl.html')
def resource_owner_label(resource, label_size=None):
    """
    Display an independent label (no breadcrumb) for the owner (a user or organization) of
    a resource, based on the "owner_type" and "owner". Ex:

        [:owner-type-icon :owner-id]

    :param resource: OCL resource with owner_type and owner attributes
    :param label_size: No value is 'medium'; Acceptable values are 'small' or 'large'
    """
    return {
        'resource_owner_type': resource['owner_type'],
        'resource_owner': resource['owner'],
        'label_size': label_size
    }

@register.inclusion_tag('includes/source_label_incl.html')
def source_label(source, label_size=None):
    """
    Displays independent source label (no breadcrumb). Ex:

        [:source-icon :source-short-name]

    :param source: OCL source
    :param label_size: No value is 'medium'; Acceptable values are 'small' or 'large'
    """
    return {
        'source':source,
        'label_size':label_size
    }

@register.inclusion_tag('includes/collection_label_incl.html')
def collection_label(collection, label_size=None):
    """
    Displays independent collection label (no breadcrumb). Ex:

        [:collection-icon :collection-short-name]

    :param collection: OCL Collection
    :param label_size: No value is 'medium'; Acceptable values are 'small' or 'large'
    """
    return {
        'collection':collection,
        'label_size':label_size
    }


@register.inclusion_tag('includes/concept_label_incl.html')
def concept_label(concept, label_size=None):
    """
    Displays independent concept label (no breadcrumb). Ex:

        [:concept-icon :concept-id]

    :param concept: (required) OCL concept
    :param label_size: (optional) No value is 'medium'; Acceptable values are 'small' or 'large'
    """
    return {
        'concept':concept,
        'label_size':label_size
    }


@register.inclusion_tag('includes/mapping_label_incl.html')
def mapping_label(mapping, label_size=None, display_breadcrumb=False, url=None):
    """
    Displays mapping label. Ex with no breadcrumb:

        [:mapping-icon :mapping-id :map-type]

    Example with breadcrumb:

        [:mapping-icon :owner / :source / :mapping-id :map-type]

    :param mapping: (required) OCL mapping
    :param label_size: (optional) No value is 'medium'; Acceptable values are 'small' or 'large'
    :param display_breadcrumb: (optional) Whether to display source breadcrumb
    """
    return {
        'mapping': mapping,
        'label_size': label_size,
        'display_breadcrumb': display_breadcrumb,
        'url': url
    }


@register.inclusion_tag('includes/mapping_from_concept_label_incl.html')
def mapping_from_concept_label(mapping, label_size=None):
    """
    Generates a breadcrumbed label for the from_concept of an OCL mapping.

    :param mapping: (required) OCL mapping
    :param label_size: (optional) Default value is 'medium'; accepts 'small' or 'large'
    """
    return {'mapping':mapping, 'label_size':label_size}


@register.inclusion_tag('includes/mapping_to_concept_label_incl.html')
def mapping_to_concept_label(mapping, label_size=None):
    """
    Generates a breadcrumbed label for the to_concept of an OCL mapping.

    :param mapping: (required) OCL mapping
    :param label_size: (optional) Default value is 'medium'; accepts 'small' or 'large'
    """
    return {'mapping':mapping, 'label_size':label_size}


@register.inclusion_tag('includes/generic_resource_label_incl.html')
def generic_resource_label(
        resource_type='', resource_id=None, resource_name='',
        resource_version_id=None, resource_url=None, resource_retired=False,
        owner_type=None, owner_id=None,
        source_id=None, source_version_id=None,
        label_size='', display_icon=True, display_breadcrumb=False, empty_name_text=''):
    """
    Generates an OCL resource label based on the passed information.

    `resource_*` fields describe the resource for which the label is being generated,
    and are always applicable regardless of whether the breadcrumb is displayed.

    `owner_type`, `owner_id`, `source_id`, and `source_version_id` are only used
    to display breadcrumb information.

    If display_breadcrumb == true:
        Owner (Organization/User):
            (:icon :resource-id | :resource-name)
        Repository (Source/Collection):
            (:icon :owner_id / :resource-id | :resource-name)
        Versioned Repository:
            (:icon :owner_id / :resource-id [ :resource_version_id ] | :resource-name)
        Repository Version (no name when listing repo versions):
            (:icon :owner_id / :resource-id [ :resource_version_id ])
        Concept/Mapping:
            (:icon :owner_id / :source_id / :resource-id | :resource-name)
        Versioned Concept/Mapping:
            (:icon :owner_id / :source_id /:resource-id[:resource_ver_id]|:resource-name)
    Elif resource_id and resource_name:
        ( :icon :resource-id | :resource_name )
    Else:
        ( :icon :resource-id )
    """

    # Validate resource type and set the icon type
    resource_type = resource_type.lower()
    default_resource_icon = 'question-sign'
    resource_icons = {
        'concept': 'tag',
        'external_concept': 'tag',
        'mapping': 'link',
        'source': 'th-list',
        'collection': 'tags',
        'org': 'home',
        'user': 'user',
        'source_version': 'asterisk',
        'collection_version': 'asterisk',
        'repository_version': 'asterisk'
    }
    if resource_type in resource_icons:
        resource_icon = resource_icons[resource_type]
    else:
        resource_icon = default_resource_icon

    # Determine label size -- small, large, or nothing (which is medium)
    css_size_class = ''
    if not label_size or label_size.lower() not in ('small', 'large'):
        pass
    else:
        css_size_class = label_size.lower()

    # Setup the breadcrumb
    breadcrumb_parts = []
    if display_breadcrumb:
        if owner_id:
            breadcrumb_parts.append({
                'text': owner_id,
                'display_as_version': False,
                'focus': False
            })
        if source_id:
            breadcrumb_parts.append({
                'text': source_id,
                'display_as_version': False,
                'focus': False
            })
        if source_version_id:
            breadcrumb_parts.append({
                'text': source_version_id,
                'display_as_version': True,
                'focus': False
            })
        if resource_id:
            breadcrumb_parts.append({
                'text': resource_id,
                'display_as_version': False,
                'focus': False if resource_version_id else True
            })
        if resource_version_id:
            breadcrumb_parts.append({
                'text': resource_version_id,
                'display_as_version': True,
                'focus': True
            })
    elif resource_id and resource_name:
        breadcrumb_parts.append({
            'text': resource_id,
            'display_as_version': False,
            'focus': False if resource_version_id else True
        })
        if resource_version_id:
            breadcrumb_parts.append({
                'text': resource_version_id,
                'display_as_version': True,
                'focus': True
            })

    return {
        'resource_type':resource_type,
        'resource_id':resource_id,
        'resource_name':resource_name,
        'resource_url':resource_url,
        'resource_icon':resource_icon,
        'resource_retired':resource_retired,
        'owner_type':owner_type,
        'owner_id':owner_id,
        'source_id':source_id,
        'source_version_id':source_version_id,
        'label_size':label_size,
        'css_size_class':css_size_class,
        'display_icon':display_icon,
        'display_breadcrumb':display_breadcrumb,
        'breadcrumb_parts':breadcrumb_parts,
        'empty_name_text':empty_name_text
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
    url_string = ''
    if url:
        url_string = value
    value = u'%s' % value
    if truncate and len(value) > (TRUNCATE_LENGTH + 3):
        value = value[:TRUNCATE_LENGTH] + '...'
    id = convert_to_id(label)
    return {
        'field_label': label,
        'field_value': value,
        'url_value': url_string,
        'is_url': url,
        'vertical': vertical,
        'small': small,
        'id': id
    }

def convert_to_id(label):
    label = label.replace(' ', '_').lower()
    return "id_" + label


## Custom Tags: PAGINATION

@register.inclusion_tag('includes/simple_pager_incl.html')
def simple_pager(page, name, url=None, pager_size='', hide_xs=False):
    """
        Display a simple pager with N-M of P {name}[<] [>]

        :param page: is a django paginator Page object.
        :param name: is for display the item's name.
        :url: is the GET url used to invoke the other page, usually
            includes query parameters.
    """

    # Determine display size -- small, large, or nothing (which is medium)
    css_size_class = ''
    if not pager_size or pager_size.lower() not in ('small', 'large'):
        pass
    else:
        css_size_class = pager_size.lower()

    # Set next and previous URLs for the pager
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
        'pager_size': css_size_class,
        'hide_xs': bool(hide_xs)
    }



## Custom Tags: PERMISSION CHECKING

class IfCanChangeNode(Node):
    """
    Class to support permission checking tags

    Works with orgs, users, or resources that contain "owner" and "owner_type" fields.
    Meaning sources, concepts, mappings are fine, but not extras, concept names/descriptions,
    source versions, etc.
    """

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
        has_access = False
        if not user.is_authenticated():
            # User must be authenticated if checking for access
            has_access = False

        elif obj.get('type') == 'Organization':     # pylint: disable=E1101
            # If org, authenticated user can access only if they are a member of the org
            api = OclApi(context['request'], debug=True)
            results = api.get('orgs', obj.get('id'), 'members', user.username)  # pylint: disable=E1101
            if results.status_code == 204:
                has_access = True
            print 'ACCESS Check on org:', results.status_code

        elif obj.get('type') == 'User':     # pylint: disable=E1101
            # If user, authenticated user can access only if they are that user
            if user.username == obj.get('username'):    # pylint: disable=E1101
                has_access = True

        elif obj.get('owner_type') == 'Organization':       # pylint: disable=E1101
            # If resource is owned by an org, then user must be a member of the org
            api = OclApi(context['request'], debug=True)
            results = api.get('orgs', obj.get('owner'), 'members', user.username)       # pylint: disable=E1101
            if results.status_code == 204:
                has_access = True
            print 'ACCESS Check on ' + obj.get('type') + ':', results.status_code       # pylint: disable=E1101

        elif obj.get('owner_type') == 'User':       # pylint: disable=E1101
            # If resource is owned by a user, then authenticated user must own the resource
            if obj.get('owner') == user.username:       # pylint: disable=E1101
                has_access = True

        if has_access:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)



@register.tag('if_can_change')
def do_if_can_change(parser, token):
    """
    The ``{% if_can_change ocl_resource %}`` tag evaluates whether the current user has access
    to the specified OCL resource.

    The OCL resource can be an org, user, or any resource that contains "owner" and "owner_type"
    fields. Meaning sources, source versions, concepts, mappings are fine, but not extras,
    concept names/descriptions, concept versions, etc.

    ::
        {% if_can_change ocl_resource %}

        {% endif_can_change %}
    """
    # NOTE: the obj_var can also be a source, org, mapping or concept
    obj_var = token.split_contents()[1]

    nodelist_true = parser.parse(('else', 'endif_can_change'))

    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_can_change',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return IfCanChangeNode(nodelist_true, nodelist_false, obj_var)

@register.inclusion_tag('includes/select_all_toggle_incl.html')
def select_all_toggle(checkbox_css_selector, data_table_rows_id):
    return {
        'checkbox_css_selector': checkbox_css_selector,
        'data_table_rows_id': data_table_rows_id
    }

@register.inclusion_tag('includes/add_to_collection_dropdown.html')
def add_to_collection_dropdown(collections):
    return {
        'collections': collections
    }

@register.inclusion_tag('includes/add_to_collection_confirm_modal.html')
def add_to_collection_confirm_modal(show_cascade_option=False, reference_type=''):
    return {
        'show_cascade_option': show_cascade_option or reference_type == 'concepts'
    }

@register.inclusion_tag('includes/search_result_checkbox.html')
def search_result_checkbox(index, url):
    return {
        'index': index,
        'url': url
    }

@register.inclusion_tag('includes/add_to_collection_result_information.html')
def add_to_collection_result_information():
    return {}
