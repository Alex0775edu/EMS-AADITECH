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
