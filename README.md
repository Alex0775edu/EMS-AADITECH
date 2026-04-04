# Education Management System (EMS)

A role-based, multi-institute Education Management System built with Django.  
This project supports school, college, university, and coaching workflows from one platform.

## 1. Features

- Role-based authentication (`ADMIN`, `TEACHER`, `STUDENT`, `INSTITUTE`)
- Login using `Institute ID`, `Email`, or `Username`
- Institute-wise data isolation
- Student and teacher management
- Course and assignment management
- Attendance management
  - Manual marking
  - Face attendance integration point (placeholder for OpenCV + `face_recognition`)
- Exam and performance reporting
- Fee tracking
- Notices and announcements
- Dashboard analytics with charts
- Traffic analytics (page views + logins)
- Forgot password flow (DOB verification + reset)

## 2. Tech Stack

- Backend: Django 5
- Database: MySQL (recommended), SQLite available in workspace
- Frontend: Django templates, Bootstrap, CSS, JavaScript
- AI Integration:
  - Chatbot endpoint (rule-based + OpenAI fallback)
  - Face attendance service hook

## 3. Documentation

- `AGENTS.md` for AI automation rules and workflow
- `CONTRIBUTING.md` for contributor setup and standards
- `CHANGELOG.md` for release notes
## 4. Project Structure

```text
ems/
|- accounts/        # Custom user model, auth, register/login/reset
|- attendance/      # Attendance models/views + face service
|- core/            # Institution model
|- dashboard/       # Main dashboards, analytics, reports, data hub
|- exams/           # Exam list/create
|- fees/            # Fee pages/routes
|- notices/         # Notice list/create
|- students/        # Student models/views
|- teachers/        # Teacher models/views
|- templates/       # HTML templates
|- static/          # CSS/JS/assets
|- ems/             # Django project settings/urls
|- manage.py
```

## 5. Core Data Model

- `core.Institution`: institute master entity
- `accounts.User`: custom auth model with role + institute mapping
- `students.Student`: student profile linked to user + institution
- `teachers.Teacher`: teacher profile linked to user + institution
- `attendance.Attendance`: daily attendance record per student
- `dashboard.Course`, `Assignment`, `FeePayment`, `StudentPerformance`, `ActivityLog`

## 6. Authentication & Role Behavior

### Login

- URL: `/accounts/login/`
- Accepts:
  - Institute ID
  - Email
  - Username
- Redirect by role:
  - `ADMIN` -> admin dashboard
  - `TEACHER` -> teacher dashboard
  - `STUDENT` -> student dashboard

### Access Control

- Admin/superuser can create users and manage institute data.
- Student role is restricted to read-only/self-scoped views for sensitive modules.
- Data is scoped by institution for non-superusers.

## 7. Main Routes

### Project URLs

- `/` home
- `/accounts/` auth module
- `/dashboard/` dashboard module
- `/analytics/` traffic analytics (admin)
- `/students/`, `/teachers/`, `/attendance/`, `/exams/`, `/fees/`, `/notices/`
- `/robots.txt` search engine directives
- `/sitemap.xml` sitemap listing public routes

### Dashboard URLs

- `/dashboard/` main dashboard
- `/dashboard/admin/`
- `/dashboard/teacher/`
- `/dashboard/student/`
- `/dashboard/students/`
- `/dashboard/teachers/`
- `/dashboard/courses/`
- `/dashboard/attendance/`
- `/dashboard/assignments/`
- `/dashboard/exams/`
- `/dashboard/fees/`
- `/dashboard/notices/`
- `/dashboard/reports/`
- `/dashboard/data-hub/`
- `/dashboard/chatbot/ask/`

### Attendance URLs

- `/attendance/mark/`
- `/attendance/report/`
- `/attendance/face-mark/`

## 8. Local Setup

## Prerequisites

- Python 3.11+
- MySQL server
- `pip` and virtual environment

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Database Configuration

Use environment variables (see `.env.example`).

- If `DATABASE_URL` or `DB_NAME` is set, Django uses that database.
- If nothing is set, it falls back to SQLite (`db.sqlite3`) for local dev.

For MySQL / PythonAnywhere set:

- `DB_ENGINE`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Superuser

```bash
python manage.py createsuperuser
```

## Run

```bash
python manage.py runserver 0.0.0.0:8000
```

Use `0.0.0.0` for phone testing on same Wi-Fi.

## 9. PythonAnywhere Deployment

1. Create a PythonAnywhere account and a MySQL database.
2. Set environment variables in the PythonAnywhere Web app:

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=yourusername$ems_db
DB_USER=yourusername
DB_PASSWORD=your_mysql_password
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_PORT=3306
```

3. On PythonAnywhere Bash console, run:

```bash
git clone <your-repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

4. In the Web tab, set the WSGI file to:

```python
from ems.wsgi import application
```

5. Configure static files in the Web tab:

```text
/static/  -> /home/yourusername/your-repo/staticfiles
/media/   -> /home/yourusername/your-repo/media
```

6. Reload the web app.

## 10. How Data Is Added

- Django Admin: `/admin/`
- Data Hub: `/dashboard/data-hub/` (admin/superuser only)
- Dedicated module forms (where allowed by role):
  - students
  - teachers
  - exams
  - notices
  - attendance

## 11. Password & Reset Flow

- User creation supports DOB-based default password format: `DDMMYYYY`
- Forgot password page: `/accounts/forgot-password/`
- Validation uses identifier + date of birth

## 12. AI Features

### Chatbot

- Endpoint: `POST /dashboard/chatbot/ask/`
- First tries rule-based answers (attendance, exams, assignments, study help)
- Can optionally fallback to OpenAI API if key configured

### Face Attendance

- File: `attendance/face_recognition_service.py`
- Current implementation is a placeholder
- Replace with real encoding/matching pipeline using OpenCV + `face_recognition`

## 13. Security Notes

- CSRF protection enabled via Django middleware/forms
- Role checks implemented in views
- Institution scoping for non-superusers
- Recommended production additions:
  - HTTPS
  - secure cookies
  - strict password policy
  - audit log hardening

## 14. Common Issues

### `NoReverseMatch`

- Verify URL names and namespaces in `urls.py`
- Use namespaced reverse in templates, e.g. `{% url 'attendance:mark_attendance' %}`

### `CSRF verification failed`

- Ensure every POST form has `{% csrf_token %}`
- Reload form page after login
- Keep cookies enabled

### `Unknown column ...`

- Model changed but migration not applied:
  - `python manage.py makemigrations`
  - `python manage.py migrate`

### Migration graph errors (`NodeNotFoundError`)

- Check missing migration dependency app
- Recreate/fix migration chain before migrate

## 15. Production Readiness Checklist

- Move secrets to environment variables
- Configure `ALLOWED_HOSTS`
- Use Gunicorn/Uvicorn + Nginx
- Configure static/media serving
- Add backup/restore strategy
- Add monitoring and error tracking

## 16. Roadmap

- Complete real face recognition attendance pipeline
- Add payment gateway for online fee collection
- Add downloadable PDF report cards and invoices
- Add advanced analytics and institute-level KPIs
- Add full test suite (unit + integration)
