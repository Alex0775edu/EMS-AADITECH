# Restored migration file to match applied DB history.

import django.db.models.deletion
from django.core.exceptions import FieldDoesNotExist
from django.db import migrations, models


class SafeRemoveField(migrations.RemoveField):
    """Remove a field only if it exists in the migration state/database."""

    def state_forwards(self, app_label, state):
        model_key = (app_label, self.model_name_lower)
        model_state = state.models.get(model_key)
        if not model_state:
            return
        field_names = {name for name, _ in model_state.fields}
        if self.name not in field_names:
            return
        super().state_forwards(app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        from_model = from_state.apps.get_model(app_label, self.model_name)
        try:
            from_model._meta.get_field(self.name)
        except FieldDoesNotExist:
            return
        super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        to_model = to_state.apps.get_model(app_label, self.model_name)
        try:
            to_model._meta.get_field(self.name)
        except FieldDoesNotExist:
            return
        super().database_backwards(app_label, schema_editor, from_state, to_state)


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        SafeRemoveField(
            model_name='attendance',
            name='teacher_assignment',
        ),
        SafeRemoveField(
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
