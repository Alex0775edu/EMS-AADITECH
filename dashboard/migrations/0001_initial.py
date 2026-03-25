# Generated manually for EMS upgrade

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_institution_saas_fields'),
        ('students', '0001_initial'),
        ('teachers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=10)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True)),
                ('credits', models.PositiveSmallIntegerField(default=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='core.institution')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='teachers.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('message', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='core.institution')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='assignments/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='dashboard.course')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='core.institution')),
            ],
        ),
        migrations.CreateModel(
            name='FeePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('PARTIAL', 'Partial')], default='PENDING', max_length=20)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_payments', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('remarks', models.CharField(blank=True, max_length=200)),
                ('graded_at', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_records', to='dashboard.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_records', to='students.student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='studentperformance',
            unique_together={('student', 'course')},
        ),
    ]
