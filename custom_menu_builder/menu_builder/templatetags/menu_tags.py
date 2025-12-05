from django import template
from menu_builder.models import Menu

register = template.Library()


@register.inclusion_tag('menu_builder/menu.html', takes_context=True)
def render_menu(context, menu_slug, css_class=''):
    """
    Template tag to render a menu
    
    Usage: {% render_menu 'main-menu' %}
    Usage: {% render_menu 'main-menu' 'custom-class' %}
    """
    try:
        menu = Menu.objects.get(slug=menu_slug)
        root_items = menu.get_root_items()
    except Menu.DoesNotExist:
        root_items = []
    
    return {
        'menu': menu if 'menu' in locals() else None,
        'menu_items': root_items,
        'css_class': css_class,
        'request': context.get('request'),
    }


@register.simple_tag
def get_menu(menu_slug):
    """Get a menu object by slug"""
    try:
        return Menu.objects.get(slug=menu_slug)
    except Menu.DoesNotExist:
        return None

