#!/usr/bin/env python3
"""Structural check on a finished artifact before publishing.

    python3 validate.py <file.html>

Catches the errors that silently break a page: an unclosed tag that swallows half the
document, a TOC link pointing at a section that does not exist, a table outside its scroll
wrapper, a diagram with no accessible label.
"""
import re, sys
from html.parser import HTMLParser

VOID = {'br', 'hr', 'img', 'input', 'link', 'meta', 'source', 'path', 'rect', 'line',
        'circle', 'polygon', 'polyline', 'use', 'stop', 'ellipse', 'col', 'area', 'track'}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f'stray </{tag}> at line {self.getpos()[0]}')
            return
        if self.stack[-1][0] != tag:
            open_tag, pos = self.stack[-1]
            self.errors.append(f'</{tag}> at line {self.getpos()[0]} closes <{open_tag}> opened at line {pos[0]}')
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
        else:
            self.stack.pop()


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: validate.py <file.html>')
    path = sys.argv[1]
    src = open(path, encoding='utf-8').read()
    problems = []

    p = Balance()
    p.feed(src)
    problems += p.errors
    problems += [f'never closed: <{t}> opened at line {pos[0]}' for t, pos in p.stack[:8]]

    sections = re.findall(r'<section id="([^"]+)"', src)
    toc = re.findall(r'<a href="#([^"]+)"', src)
    for t in toc:
        if t not in sections:
            problems.append(f'TOC links #{t} but no <section id="{t}">')
    for s in sections:
        if s not in toc:
            problems.append(f'<section id="{s}"> is not in the TOC')

    svgs = re.findall(r'<svg\b[^>]*>', src)
    for s in svgs:
        if 'aria-label' not in s:
            problems.append('an <svg> has no aria-label')
        if 'viewBox' not in s:
            problems.append('an <svg> has no viewBox')

    figs = len(re.findall(r'<figure', src))
    caps = len(re.findall(r'<figcaption', src))
    if figs != caps:
        problems.append(f'{figs} <figure> but {caps} <figcaption>')

    bare = len(re.findall(r'<table', src)) - len(re.findall(r'class="tw', src))
    if bare > 0:
        problems.append(f'{bare} <table> not inside a .tw wrapper — the page will scroll sideways')

    for tag in ('<!doctype', '<html', '<head>', '<body>'):
        if tag in src.lower():
            problems.append(f'remove {tag} — the Artifact tool supplies the document skeleton')

    if not re.search(r'<title>.+</title>', src):
        problems.append('no <title> — the artifact will be named after the file')

    ids = re.findall(r'<marker\s+id="([^"]+)"', src)
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f'duplicate marker id(s) {sorted(dupes)} — arrows will point at the first definition')

    kb = len(src.encode()) / 1024
    print(f'{path}  ·  {kb:.0f} KB  ·  {len(sections)} sections  ·  {len(svgs)} diagrams  '
          f'·  {len(re.findall(r"<table", src))} tables')

    if problems:
        print(f'\n{len(problems)} problem(s):')
        for x in problems:
            print(f'  - {x}')
        return 1
    print('\nStructure OK.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
