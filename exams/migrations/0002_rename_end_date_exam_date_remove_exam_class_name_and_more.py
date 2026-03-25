# Restored migration file to match applied DB history.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='end_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='description',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='section',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='marks',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='examsubject',
            name='subject',
        ),
        migrations.AddField(
            model_name='examsubject',
            name='subject',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='marks',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='marks_obtained',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='marks',
            unique_together=set(),
        ),
    ]
