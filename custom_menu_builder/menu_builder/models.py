from django.db import models
from django.core.exceptions import ValidationError
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable


class MenuItem(Orderable):
    """Individual menu item that can be nested"""
    menu = ParentalKey('Menu', related_name='menu_items', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255, help_text="Menu item title")
    link_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL for the menu item (e.g., /about/, https://example.com)"
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Link to a Wagtail page (optional)"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        help_text="Parent menu item (for nested menus)"
    )
    open_in_new_tab = models.BooleanField(default=False, help_text="Open link in new tab")
    css_class = models.CharField(
        max_length=255,
        blank=True,
        help_text="Additional CSS classes for styling"
    )
    
    panels = [
        FieldPanel('title'),
        FieldPanel('link_url'),
        FieldPanel('link_page'),
        FieldPanel('parent'),
        FieldPanel('open_in_new_tab'),
        FieldPanel('css_class'),
    ]
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    
    def __str__(self):
        return self.title
    
    def clean(self):
        """Validate that either link_url or link_page is provided"""
        if not self.link_url and not self.link_page:
            raise ValidationError("Either 'Link URL' or 'Link Page' must be provided.")
        if self.parent and self.parent == self:
            raise ValidationError("A menu item cannot be its own parent.")
    
    def get_url(self):
        """Get the URL for this menu item"""
        if self.link_page:
            return self.link_page.url
        return self.link_url or '#'
    
    def get_children(self):
        """Get child menu items"""
        return MenuItem.objects.filter(parent=self, menu=self.menu).order_by('sort_order')


class Menu(ClusterableModel):
    """Menu container that holds menu items"""
    title = models.CharField(
        max_length=255,
        unique=True,
        help_text="Internal name for this menu"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly identifier for this menu"
    )
    
    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel('menu_items', label="Menu Items"),
    ]
    
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_root_items(self):
        """Get top-level menu items (items without a parent)"""
        return self.menu_items.filter(parent__isnull=True).order_by('sort_order')

