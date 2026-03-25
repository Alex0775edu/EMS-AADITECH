import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_remove_institution_institution_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsletterSubscription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
