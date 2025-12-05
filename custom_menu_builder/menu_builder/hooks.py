from wagtail import hooks
from wagtail.snippets.models import register_snippet
from .models import Menu
from .admin import MenuAdmin


@hooks.register("register_admin_viewset")
def register_menu_admin():
    """Register Menu snippet admin with Wagtail."""
    return MenuAdmin()

