from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel, InlinePanel
from .models import Menu


class MenuAdmin(SnippetViewSet):
    model = Menu
    menu_label = 'Menus'
    menu_icon = 'list-ul'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'slug']
    search_fields = ['title', 'slug']
    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel('menu_items', label="Menu Items"),
    ]

