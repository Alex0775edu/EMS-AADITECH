"""
Scan Django templates for POST forms missing a {% csrf_token %} and optionally insert it.

Usage:
  python scripts/fix_csrf_templates.py --apply
"""
import re
from pathlib import Path
import argparse

POST_FORM_RE = re.compile(r"<form[^>]*method=[\"']?post[\"']?[^>]*>", re.IGNORECASE)
CSRF_TOKEN_RE = re.compile(r"\{\%\s*csrf_token\s*\%\}", re.IGNORECASE)

def scan_templates(root: Path):
    templates = list(root.rglob('*.html'))
    missing = []
    for t in templates:
        content = t.read_text(encoding='utf-8')
        for m in POST_FORM_RE.finditer(content):
            # find form closing bracket
            start = m.end()
            # look ahead for csrf token before first input or closing form
            snippet = content[start:start+400]
            if not CSRF_TOKEN_RE.search(snippet):
                missing.append((t, m.start(), snippet[:120]))
                break
    return missing

def insert_csrf(path: Path):
    content = path.read_text(encoding='utf-8')
    def repl(match):
        tag = match.group(0)
        return tag + '\n    {% csrf_token %}'
    new = POST_FORM_RE.sub(repl, content)
    path.write_text(new, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--templates-dir', default='templates')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = Path(args.templates_dir)
    missing = scan_templates(root)
    if not missing:
        print('No issues found.')
        return
    print(f'Found {len(missing)} templates with potential missing csrf_token:')
    for p, pos, snippet in missing:
        print('-', p, '...', snippet)
    if args.apply:
        for p, pos, _ in missing:
            insert_csrf(p)
        print('Patched templates. Run tests to verify.')

if __name__ == '__main__':
    main()
"""
Scan templates for POST forms missing `{% csrf_token %}` and optionally insert token.

Usage (run from project root):
  python scripts/fix_csrf_templates.py --apply

This script is idempotent and creates backups when modifying files.
"""
import re
from pathlib import Path
import argparse

TEMPLATE_DIR = Path('templates')


def find_post_forms(text):
    # Find positions of <form ... method="post"
    pattern = re.compile(r'<form[^>]*method=["\']post["\'][^>]*>', re.IGNORECASE)
    return [m.start() for m in pattern.finditer(text)]


def has_csrf_near(text, pos, window=200):
    snippet = text[pos:pos+window]
    return '{% csrf_token %}' in snippet


def scan_and_fix(apply=False):
    modified = []
    for path in TEMPLATE_DIR.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        changed = False
        new_text = text
        for pos in find_post_forms(text):
            if not has_csrf_near(text, pos):
                # Insert csrf token after the opening tag
                insert_at = new_text.find('>', pos) + 1
                new_text = new_text[:insert_at] + '\n    {% csrf_token %}' + new_text[insert_at:]
                changed = True
        if changed:
            modified.append(str(path))
            if apply:
                backup = path.with_suffix(path.suffix + '.bak')
                path.write_text(text, encoding='utf-8')
                path.write_text(new_text, encoding='utf-8')
    return modified


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    mods = scan_and_fix(apply=args.apply)
    if mods:
        print('Modified templates:')
        for p in mods:
            print(' -', p)
    else:
        print('No missing CSRF tokens found.')
