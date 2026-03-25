import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('students', '0001_initial'),
        ('teachers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='short_description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='course',
            name='cover_image',
            field=models.FileField(blank=True, null=True, upload_to='courses/covers/'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='language',
            field=models.CharField(default='English', max_length=40),
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.CharField(
                choices=[
                    ('BEGINNER', 'Beginner'),
                    ('INTERMEDIATE', 'Intermediate'),
                    ('ADVANCED', 'Advanced'),
                ],
                default='BEGINNER',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='course',
            name='rating_average',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='rating_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('is_published', models.BooleanField(default=False)),
                ('release_at', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='dashboard.course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('lesson_type', models.CharField(
                    choices=[
                        ('VIDEO', 'Video'),
                        ('PDF', 'PDF'),
                        ('QUIZ', 'Quiz'),
                        ('LIVE', 'Live'),
                        ('TEXT', 'Text'),
                    ],
                    default='VIDEO',
                    max_length=20,
                )),
                ('content_url', models.URLField(blank=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='courses/lessons/')),
                ('duration_minutes', models.PositiveSmallIntegerField(default=0)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('is_preview', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='dashboard.module')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[
                        ('ACTIVE', 'Active'),
                        ('COMPLETED', 'Completed'),
                        ('DROPPED', 'Dropped'),
                    ],
                    default='ACTIVE',
                    max_length=20,
                )),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('progress_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='dashboard.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_enrollments', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='LessonProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('last_position_seconds', models.PositiveIntegerField(default=0)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_progress', to='dashboard.courseenrollment')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress_records', to='dashboard.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('review', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='dashboard.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_reviews', to='students.student')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='assignments/submissions/')),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(
                    choices=[
                        ('SUBMITTED', 'Submitted'),
                        ('GRADED', 'Graded'),
                        ('LATE', 'Late'),
                        ('RESUBMITTED', 'Resubmitted'),
                    ],
                    default='SUBMITTED',
                    max_length=20,
                )),
                ('grade', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('feedback', models.TextField(blank=True)),
                ('plagiarism_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='dashboard.assignment')),
                ('graded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_submissions', to='students.student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together={('course', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='lessonprogress',
            unique_together={('enrollment', 'lesson')},
        ),
        migrations.AlterUniqueTogether(
            name='coursereview',
            unique_together={('course', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='assignmentsubmission',
            unique_together={('assignment', 'student')},
        ),
    ]
