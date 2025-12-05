# Mini CMS with Custom Menu Builder

A Wagtail-based mini CMS with a custom menu builder, featuring clean authentication pages and a white/grey theme.

## Features

- **Custom Menu Builder**: Create and manage hierarchical menus through Wagtail admin
- **Clean UI**: Modern white and grey theme for authentication pages
- **User Authentication**: Simple signup and login pages
- **Wagtail Integration**: Follows Wagtail best practices and structure

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the admin**:
   - Wagtail Admin: http://localhost:8000/admin/
   - Login Page: http://localhost:8000/login/
   - Signup Page: http://localhost:8000/signup/

## Usage

### Creating Menus

1. Log in to the Wagtail admin at `/admin/`
2. Navigate to **Snippets** → **Menus** in the admin sidebar
3. Click **Add Menu** to create a new menu
4. Fill in:
   - **Title**: Internal name for the menu (e.g., "Main Navigation")
   - **Slug**: URL-friendly identifier (e.g., "main-menu")
5. Add menu items by clicking **Add Menu Item**:
   - **Title**: Display text for the menu item
   - **Link URL**: Direct URL (e.g., `/about/`, `https://example.com`)
   - **Link Page**: Or select a Wagtail page
   - **Parent**: Select a parent item to create nested menus
   - **Open in new tab**: Check to open link in a new window
   - **CSS Class**: Additional CSS classes for custom styling

### Displaying Menus in Templates

Use the `render_menu` template tag to display menus in your Wagtail templates:

```django
{% load menu_tags %}

{% render_menu 'main-menu' %}
```

Or with a custom CSS class:

```django
{% render_menu 'main-menu' 'custom-menu-class' %}
```

### Menu Structure

- Menus support hierarchical structure (parent-child relationships)
- Top-level items are displayed in the main menu
- Child items appear in dropdown submenus on hover
- Menu items can link to either Wagtail pages or external URLs

## Project Structure

```
.
├── cms_project/          # Main Django project
│   ├── settings.py       # Django/Wagtail settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI configuration
├── menu_builder/         # Menu builder app
│   ├── models.py        # Menu and MenuItem models
│   ├── admin.py         # Wagtail admin configuration
│   ├── views.py         # Authentication views
│   ├── templatetags/    # Template tags for rendering menus
│   └── templates/       # App-specific templates
├── templates/           # Base templates
│   ├── base.html
│   └── menu_builder/    # Auth templates
├── static/              # Static files
│   └── css/
│       └── main.css     # Main stylesheet
└── requirements.txt     # Python dependencies
```

## Customization

### Styling

The white/grey theme is defined in `static/css/main.css`. You can customize:
- Colors and backgrounds
- Typography
- Spacing and layout
- Menu appearance

### Menu Rendering

Customize menu rendering by editing `templates/menu_builder/menu.html` or creating your own template.

## Wagtail Integration

This project follows Wagtail best practices:
- Uses `ClusterableModel` for menu items
- Uses `Orderable` for drag-and-drop ordering
- Integrates with Wagtail's snippet system
- Uses Wagtail's admin panels and viewsets
- Compatible with Wagtail's page system

## Development

### Adding New Features

1. Models should extend Wagtail's base classes when appropriate
2. Use Wagtail's admin panels for model configuration
3. Follow Wagtail's template tag conventions
4. Use Wagtail's snippet system for reusable content

## License

This project is open source and available for use.

