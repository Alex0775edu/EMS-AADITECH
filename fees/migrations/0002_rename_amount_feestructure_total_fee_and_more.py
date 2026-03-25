# Restored migration file to match applied DB history.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0001_initial'),
        ('students', '0001_initial'),
        ('core', '0002_institution_saas_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
        migrations.RemoveField(
            model_name='feetransaction',
            name='fee_structure',
        ),
        migrations.RemoveField(
            model_name='feetransaction',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='feetransaction',
            name='status',
        ),
        migrations.RemoveField(
            model_name='feestructure',
            name='fee_head',
        ),
        migrations.RemoveField(
            model_name='feestructure',
            name='frequency',
        ),
        migrations.RenameField(
            model_name='feestructure',
            old_name='amount',
            new_name='total_fee',
        ),
        migrations.RenameField(
            model_name='feetransaction',
            old_name='amount_paid',
            new_name='amount',
        ),
        migrations.AddField(
            model_name='feestructure',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='feetransaction',
            name='transaction_type',
            field=models.CharField(choices=[('CREDIT', 'Credit'), ('DEBIT', 'Debit')], default='CREDIT', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='class_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='feestructure',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.institution'),
        ),
        migrations.AlterField(
            model_name='feetransaction',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
    ]
