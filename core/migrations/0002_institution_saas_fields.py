# Generated manually for EMS upgrade

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='admin_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
