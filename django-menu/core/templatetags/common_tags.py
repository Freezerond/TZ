from django import template
from core.models import *
register = template.Library()


@register.inclusion_tag('templatetags/menu.html', takes_context=True, name='parent_items')
def get_parent_items(context):
    menu_items = MenuItem.objects.filter(parent__isnull=True)
    return {
        "menu_items": menu_items,
    }


@register.inclusion_tag('templatetags/all_items.html', takes_context=True, name='all')
def get_items(context):
    menu_items = MenuItem.objects.filter(level=0)
    return {
        "menu_items": menu_items,
    }