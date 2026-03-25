from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mfa_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='consent_opt_in',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='preferences',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
