#!/usr/bin/env python3
"""Edit HTML files:
  - Add Beranda home button (far right of navigation-top)
  - Aktb*: ensure js/book-names.js is active
  - Cerito dan*: switch to js/book-names-2.js
  - Cerito dan-01-GLO-001.html: strip navigation to Beranda only
"""

import os

DIR = os.path.dirname(os.path.abspath(__file__))
BERANDA = "  <span class=\"button\"><a href='index.html' title='Beranda'>&nbsp;&nbsp;Beranda&nbsp;&nbsp;</a></span>\n"
NAV_OPEN = '<div class="navigation-top">'
NAV_CLOSE = '</div>'


def find_nav_close(content, after_open):
    """Return index of </div> closing navigation-top, skipping any inside comments."""
    pos = after_open
    while pos < len(content):
        close = content.find(NAV_CLOSE, pos)
        if close == -1:
            return -1
        snippet = content[after_open:close]
        if snippet.count('<!--') == snippet.count('-->'):
            return close
        pos = close + 1
    return -1


def process(filepath, filename):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    orig = content

    # Fix book-names script reference
    if filename.startswith('Aktb'):
        content = content.replace(
            "<!-- <script type='text/javascript' src='js/book-names.js'></script> -->",
            "<script type='text/javascript' src='js/book-names.js'></script>",
        )
    elif filename.startswith('Cerito dan'):
        # Longer match first so the substring match doesn't corrupt the comment
        content = content.replace(
            "<!-- <script type='text/javascript' src='js/book-names.js'></script> -->",
            "<script type='text/javascript' src='js/book-names-2.js'></script>",
        )
        # Also uncomment if book-names-2.js ended up commented (prior partial run)
        content = content.replace(
            "<!-- <script type='text/javascript' src='js/book-names-2.js'></script> -->",
            "<script type='text/javascript' src='js/book-names-2.js'></script>",
        )
        content = content.replace(
            "<script type='text/javascript' src='js/book-names.js'></script>",
            "<script type='text/javascript' src='js/book-names-2.js'></script>",
        )
        # Swap to stories menu (only active tag, GLO's commented-out version left alone)
        content = content.replace(
            "<script type='text/javascript' src='js/app-builder-menus.js'></script>",
            "<script type='text/javascript' src='js/app-builder-menus-stories.js'></script>",
        )

    # Update navigation-top
    start = content.find(NAV_OPEN)
    if start != -1:
        after_open = start + len(NAV_OPEN)
        end = find_nav_close(content, after_open)
        if end != -1:
            inner = content[after_open:end]
            has_beranda = "title='Beranda'" in inner or 'title="Beranda"' in inner

            if filename == 'Cerito dan-01-GLO-001.html':
                # Keep Beranda only; replace inner content unconditionally if not already clean
                want = "\n" + BERANDA
                if inner != want:
                    content = content[:after_open] + want + content[end:]
            else:
                if not has_beranda:
                    content = content[:end] + BERANDA + content[end:]

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


changed = 0
for name in sorted(os.listdir(DIR)):
    if not name.endswith('.html'):
        continue
    if process(os.path.join(DIR, name), name):
        print(f"  updated: {name}")
        changed += 1

print(f"\n{changed} file(s) updated.")
