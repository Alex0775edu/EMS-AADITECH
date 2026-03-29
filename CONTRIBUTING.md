# Contributing Guide

Thanks for contributing to AaDiTeCh EMS.

## Quick Start
1. Create a virtual environment: `python -m venv .venv`
2. Activate: `.venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Branching
- Create a branch per change: `feat/...`, `fix/...`, `docs/...`.
- Keep changes focused and small.

## Commit Messages
Use `type(scope): description`.

Examples:
- `fix(auth): resolve login validation bug`
- `feat(ui): improve course card design`
- `docs(readme): improve setup guide`

## Testing
Run:
- `python manage.py check`
- `python manage.py test`

## Code Style
- Follow PEP 8 for Python.
- Keep HTML templates readable with consistent indentation.
- Keep CSS in `templates/static/css/` and JS in `templates/static/js/`.

## Security
- Do not commit secrets or credentials.
- Use `.env` for local secrets and `.env.example` for documentation.

## Pull Requests
Include:
- Summary of changes
- Files touched
- Testing performed
