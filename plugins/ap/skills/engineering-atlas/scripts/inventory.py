#!/usr/bin/env python3
"""Inventory a codebase: every function, every HTTP endpoint with its role guards.

    python3 inventory.py --root <repo> --out <dir> [--src backend/src] [--quiet]

Writes functions.json and endpoints.json (compact, ready to embed in an artifact) and
prints a summary. Regex-based and deliberately so — it runs on any repo in a second with
no parse step. It is a starting point: read a couple of real route files and confirm the
endpoint count looks right before quoting it. If the project uses a convention this does
not know, extend PATTERNS rather than counting by hand.
"""
import argparse, json, os, re, sys
from collections import Counter

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '.next', '__pycache__', 'vendor',
             '.venv', 'venv', 'coverage', '.turbo', 'target', 'out', '.nuxt'}
SKIP_FILE = re.compile(r'\.(test|spec|d)\.[jt]sx?$|\.min\.js$')
EXTS = ('.ts', '.tsx', '.js', '.jsx', '.mjs', '.py', '.go', '.vue')

# name -> (kind, regex). Order matters: first match on a line wins per pattern set.
PATTERNS = [
    ('fn-export',    re.compile(r'^export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)', re.M)),
    ('const-export', re.compile(r'^export\s+const\s+(\w+)', re.M)),
    ('class-export', re.compile(r'^export\s+class\s+(\w+)', re.M)),
    ('fn-local',     re.compile(r'^(?:async\s+)?function\s+(\w+)', re.M)),
    ('fn-local',     re.compile(r'^const\s+(\w+)\s*=\s*(?:async\s*)?\(', re.M)),
    ('fn-py',        re.compile(r'^(?:async\s+)?def\s+(\w+)', re.M)),
    ('fn-py',        re.compile(r'^class\s+(\w+)', re.M)),
    ('fn-go',        re.compile(r'^func\s+(?:\([^)]*\)\s*)?(\w+)', re.M)),
]

# framework -> regex capturing (method, path) and optionally the options blob
ROUTE_PATTERNS = [
    # fastify.get('/x', { preHandler: … }, handler)   |  app.get('/x', handler)
    re.compile(r"""(?:fastify|app|router|server|r)\.(get|post|put|patch|delete|options|head)\(\s*
                   ['"`]([^'"`]*)['"`]\s*(?:,\s*(\{.*?\})\s*)?,\s*([A-Za-z0-9_.]+)""",
               re.S | re.X | re.I),
    # @app.get("/x")  /  @router.post("/x")   — FastAPI / Flask
    re.compile(r"""@(?:app|router|bp)\.(get|post|put|patch|delete)\(\s*['"]([^'"]*)['"]()()""", re.X),
]
ROLE_RE = re.compile(r'requireRole\(([^)]*)\)')
PREHANDLER_RE = re.compile(r'preHandler:\s*([A-Za-z0-9_]+)')


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith(EXTS) and not SKIP_FILE.search(fn):
                yield os.path.join(dirpath, fn)


def read(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        return ''


def functions(root):
    out = []
    for path in sorted(walk(root)):
        src = read(path)
        rel = os.path.relpath(path, root)
        seen = set()
        for kind, rx in PATTERNS:
            for m in rx.finditer(src):
                name = m.group(1)
                if name in seen:
                    continue
                seen.add(name)
                out.append({'f': rel, 'k': kind, 'n': name})
    return out


def endpoints(root, prefixes):
    """prefixes: {module_dir: url_prefix} discovered from a server/main file, or {}."""
    out = []
    for path in sorted(walk(root)):
        low = os.path.basename(path).lower()
        if not any(t in low for t in ('route', 'controller', 'handler', 'urls', 'api', 'main', 'app')):
            continue
        src = read(path)
        rel = os.path.relpath(path, root)
        mod = os.path.basename(os.path.dirname(path))
        pre = prefixes.get(mod, '')
        for rx in ROUTE_PATTERNS:
            for m in rx.finditer(src):
                meth, sub, opts, handler = (list(m.groups()) + [None] * 4)[:4]
                roles = []
                if opts:
                    rm = ROLE_RE.search(opts)
                    if not rm:
                        vm = PREHANDLER_RE.search(opts)
                        if vm:
                            rm = re.search(r'const\s+' + vm.group(1) + r'\s*=\s*requireRole\(([^)]*)\)', src)
                    if rm:
                        roles = [r.strip().strip('\'"') for r in rm.group(1).split(',') if r.strip()]
                full = (pre + sub).rstrip('/') or (pre or sub or '/')
                out.append({'m': meth.upper(), 'p': full, 'h': handler or '', 'mod': mod, 'r': roles, 'f': rel})
    # de-duplicate: the same route can be caught by two patterns
    seen, uniq = set(), []
    for e in out:
        key = (e['m'], e['p'], e['f'])
        if key not in seen:
            seen.add(key)
            uniq.append(e)
    return uniq


def find_prefixes(root):
    """Map a module directory name to its registered URL prefix, from a server entry file."""
    rx = re.compile(r"""register\(\s*(\w+)\s*,\s*\{\s*prefix:\s*['"`]([^'"`]+)['"`]""")
    imp = re.compile(r"""import\s+(\w+)\s+from\s+['"`].*?/([^/]+)/[^/'"`]+['"`]""")
    prefixes = {}
    for path in walk(root):
        base = os.path.basename(path)
        if base.split('.')[0] not in ('server', 'main', 'app', 'index'):
            continue
        src = read(path)
        var_to_mod = {m.group(1): m.group(2) for m in imp.finditer(src)}
        for m in rx.finditer(src):
            mod = var_to_mod.get(m.group(1))
            if mod:
                prefixes[mod] = m.group(2)
    return prefixes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--src', default=None, help='subdirectory to scan, e.g. backend/src')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    root = os.path.join(a.root, a.src) if a.src else a.root
    if not os.path.isdir(root):
        sys.exit(f'not a directory: {root}')
    os.makedirs(a.out, exist_ok=True)

    fns = functions(root)
    prefixes = find_prefixes(root)
    eps = endpoints(root, prefixes)

    for name, data in (('functions', fns), ('endpoints', eps)):
        with open(os.path.join(a.out, name + '.json'), 'w') as fh:
            json.dump(data, fh, separators=(',', ':'))

    if not a.quiet:
        print(f'root      {root}')
        print(f'functions {len(fns)}   ' + '  '.join(f'{k}:{v}' for k, v in Counter(x['k'] for x in fns).most_common()))
        print(f'endpoints {len(eps)}   ' + '  '.join(f'{k}:{v}' for k, v in Counter(x['m'] for x in eps).most_common()))
        print(f'modules   {len(set(x["mod"] for x in eps))}   prefixes resolved: {len(prefixes)}')
        ungated = sum(1 for e in eps if not e['r'])
        if eps:
            print(f'ungated   {ungated} endpoint(s) with no role list — worth a look')
        print(f'\nwrote {a.out}/functions.json and {a.out}/endpoints.json')
        print('\nCOUNTED (quote this definition alongside any number you publish):')
        print(f'  functions = named declarations in {len(set(x["f"] for x in fns))} source files under {os.path.relpath(root, a.root) or "."}')
        print( '              exported + module-local; tests, .d.ts, minified and node_modules excluded')
        print(f'  endpoints = server-side route registrations in {len(set(x["f"] for x in eps))} route files')
        print( '              client-side API wrappers are NOT counted; a path with 2 methods counts twice')
        if eps and not prefixes:
            print('note: no URL prefixes resolved — paths are relative. Check the server entry file.')


if __name__ == '__main__':
    main()
