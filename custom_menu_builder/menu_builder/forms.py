from django import forms
from .models import Menu, MenuItem


class MenuForm(forms.ModelForm):
    """Form for creating and editing menus"""
    
    class Meta:
        model = Menu
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter menu title (e.g., Main Navigation)'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter menu slug (e.g., main-menu)'
            }),
        }
        labels = {
            'title': 'Menu Title',
            'slug': 'Menu Slug',
        }
        help_texts = {
            'title': 'Internal name for this menu',
            'slug': 'URL-friendly identifier (lowercase, no spaces)',
        }
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            slug = slug.lower().strip()
            # Replace spaces with hyphens
            slug = slug.replace(' ', '-')
            # Remove invalid characters
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return slug


class MenuItemForm(forms.ModelForm):
    """Form for creating and editing menu items"""
    
    class Meta:
        model = MenuItem
        fields = ['title', 'link_url', 'parent', 'open_in_new_tab']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter menu item title'
            }),
            'link_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL (e.g., /about/, https://example.com)'
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control'
            }),
            'open_in_new_tab': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
        labels = {
            'title': 'Menu Item Title',
            'link_url': 'Link URL',
            'parent': 'Parent Menu Item',
            'open_in_new_tab': 'Open in New Tab',
        }
        help_texts = {
            'title': 'Display text for the menu item',
            'link_url': 'Direct URL (e.g., /about/, https://example.com)',
            'parent': 'Select parent item for nested menus (optional)',
            'open_in_new_tab': 'Open link in a new browser tab',
        }
    
    def __init__(self, *args, **kwargs):
        menu = kwargs.pop('menu', None)
        super().__init__(*args, **kwargs)
        
        if menu:
            # Filter parent choices to only items from this menu
            self.fields['parent'].queryset = MenuItem.objects.filter(menu=menu)
            # Exclude self if editing
            if self.instance and self.instance.pk:
                self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk=self.instance.pk)
            
        # Make fields optional
        self.fields['link_url'].required = True
        self.fields['parent'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        link_url = cleaned_data.get('link_url')
        
        if not link_url:
            raise forms.ValidationError("'Link URL' is required.")
        
        return cleaned_data

