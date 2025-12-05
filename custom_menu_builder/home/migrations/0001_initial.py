from django.db import migrations, models
import wagtail.fields
import wagtail.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("intro", wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]

