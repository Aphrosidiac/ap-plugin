#!/usr/bin/env python3
"""Check every colour inside every <svg> against BOTH theme grounds.

    python3 contrast.py <file.html> [--min 3.5]

SVG colours are literals, so they do not follow the page's theme tokens. A hue that reads
beautifully on the dark ground can be near-invisible on the light one, and you will not
notice because you only looked at one. This catches that before publishing, and suggests a
replacement from the balanced palette.
"""
import argparse, re, sys

LIGHT_GROUND = 'FFFFFF'   # .figbox surface, light theme
DARK_GROUND  = '1B1A16'   # .figbox surface, dark theme

PALETTE = {
    '#A57A12': 'gold',    '#1A85A2': 'cyan',  '#C4508F': 'magenta',
    '#3E9159': 'green',   '#CB5A57': 'red',   '#AE7C22': 'amber',
}


def lum(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    ch = []
    for i in (0, 2, 4):
        v = int(h[i:i + 2], 16) / 255
        ch.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def ratio(a, b):
    x, y = lum(a), lum(b)
    return round((max(x, y) + 0.05) / (min(x, y) + 0.05), 2)


def nearest(hex_):
    """Closest balanced palette entry by RGB distance."""
    h = hex_.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    best, bd = None, 1e9
    for p, name in PALETTE.items():
        q = p.lstrip('#')
        pr, pg, pb = (int(q[i:i + 2], 16) for i in (0, 2, 4))
        d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d < bd:
            best, bd = (p, name), d
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--min', type=float, default=3.5)
    a = ap.parse_args()

    src = open(a.file, encoding='utf-8').read()
    svgs = re.findall(r'<svg\b.*?</svg>', src, re.S)
    if not svgs:
        print('no <svg> found — nothing to check')
        return 0

    counts, fails = {}, []
    for svg in svgs:
        for hx in re.findall(r'#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b', svg):
            counts[hx.upper()] = counts.get(hx.upper(), 0) + 1

    print(f'{len(svgs)} svg block(s), {len(counts)} distinct colour(s), min ratio {a.min}\n')
    print(f'{"colour":<10}{"uses":>5}  {"on light":>9}{"on dark":>9}   verdict')
    print('-' * 62)
    for hx, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        L, D = ratio(hx, LIGHT_GROUND), ratio(hx, DARK_GROUND)
        ok = L >= a.min and D >= a.min
        known = ' (palette)' if hx in PALETTE else ''
        verdict = 'ok' + known if ok else ('FAILS light' if L < a.min else '') + ('FAILS dark' if D < a.min else '')
        print(f'{hx:<10}{n:>5}  {L:>9}{D:>9}   {verdict}')
        if not ok:
            fails.append((hx, n, L, D))

    if not fails:
        print('\nAll SVG colours legible on both grounds.')
        return 0

    print(f'\n{len(fails)} colour(s) need replacing:')
    for hx, n, L, D in fails:
        rep, name = nearest(hx)
        print(f'  {hx} ({n} uses, {L} light / {D} dark)  ->  {rep}  {name}')
    print('\n  sed -i "" ' + ' '.join(f'-e "s/{hx}/{nearest(hx)[0]}/g"' for hx, *_ in fails) + f' {a.file}')
    print('  (only inside <svg> — check the sed does not hit your CSS tokens)')
    return 1


if __name__ == '__main__':
    sys.exit(main())
