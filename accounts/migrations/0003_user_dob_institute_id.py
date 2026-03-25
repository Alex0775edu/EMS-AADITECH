# Generated manually for EMS upgrade

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='institute_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
