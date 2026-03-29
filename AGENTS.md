# AI Agent Guide

## Project Architecture
- Django project in `ems/` with multiple feature apps.
- Feature apps include `accounts`, `attendance`, `billing`, `classes`, `communications`, `core`, `dashboard`, `documents`, `exams`, `fees`, `institutions`, `materials`, `notices`, `notifications`, `reports`, `students`, `teachers`.
- Templates live in `templates/` and use Django template inheritance.
- Static assets live in `templates/static/` and are collected to `staticfiles/` for production.
- Entry points are `manage.py`, `ems/settings.py`, and `ems/urls.py`.
- AI integration is in `ai_services/` with a public chatbot endpoint.

## Coding Standards
- Follow PEP 8 for Python and keep Django conventions.
- Keep templates readable, use `{% url %}` and `{% static %}` helpers.
- Keep CSS in `templates/static/css/` and JS in `templates/static/js/`.
- Prefer small, composable functions and avoid duplicate logic.
- Use ASCII in source files unless a file already uses Unicode.

## Automation Workflow
- Run `python manage.py check` and `python manage.py test` before commits.
- Apply migrations after model changes.
- Run `python manage.py collectstatic --noinput` for production.
- Update docs when behaviors or setup steps change.

## Git Rules
- Use commit format `type(scope): description`.
- Keep commits scoped to one logical change.
- Avoid force-push and avoid rewriting history on shared branches.
- Do not commit secrets or local databases.

## Testing Instructions
- Local checks: `python manage.py check`.
- Tests: `python manage.py test`.
- Manual smoke:
  - Home page loads.
  - Login works.
  - Dashboard routes render for authenticated users.
  - Chatbot endpoint responds.

## Improvement Guidelines
- Prefer real data over placeholders.
- Keep SEO tags, sitemap, and robots rules updated.
- Keep UI responsive across mobile, tablet, desktop.
- Remove duplicate model or template logic when found.
- Document all new behavior in README and CHANGELOG.
