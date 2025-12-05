from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(help_text="Internal name for this menu", max_length=255, unique=True)),
                ("slug", models.SlugField(help_text="URL-friendly identifier for this menu", unique=True)),
            ],
            options={
                "verbose_name": "Menu",
                "verbose_name_plural": "Menus",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                ("title", models.CharField(help_text="Menu item title", max_length=255)),
                (
                    "link_url",
                    models.CharField(
                        blank=True,
                        help_text="URL for the menu item (e.g., /about/, https://example.com)",
                        max_length=500,
                    ),
                ),
                (
                    "open_in_new_tab",
                    models.BooleanField(default=False, help_text="Open link in new tab"),
                ),
                (
                    "css_class",
                    models.CharField(blank=True, help_text="Additional CSS classes for styling", max_length=255),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        help_text="Link to a Wagtail page (optional)",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "menu",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="menu_builder.menu",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="Parent menu item (for nested menus)",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="menu_builder.menuitem",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "verbose_name": "Menu Item",
                "verbose_name_plural": "Menu Items",
            },
            bases=(wagtail.models.Orderable, models.Model),
        ),
    ]

