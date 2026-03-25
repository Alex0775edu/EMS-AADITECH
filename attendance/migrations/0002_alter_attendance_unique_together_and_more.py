# Restored migration file to match applied DB history.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='teacher_assignment',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='remarks',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent'), ('LEAVE', 'Leave')], max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'date')},
        ),
    ]
