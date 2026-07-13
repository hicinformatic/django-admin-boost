"""Template tags for django_boosted."""

from django import template

from django_boosted.admin.index import get_index_views

register = template.Library()


@register.simple_tag(takes_context=True)
def boosted_index_views(context):
    """Return the admin index panel entries visible to the current user."""
    return get_index_views(context.get("request"))


@register.filter
def getattr_filter(obj, attr_name):
    """Get attribute from object dynamically."""
    return getattr(obj, attr_name, None)


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary dynamically."""
    if dictionary is None:
        return None
    return dictionary.get(key)
