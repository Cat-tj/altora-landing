"""Periksa tautan internal (href/src) di semua halaman: laporkan yang menunjuk ke file yang tidak ada.
Jalankan: python3 scripts/check_links.py [--sumber]   (keluar kode 1 bila ada tautan putus)"""
import glob, os, re, sys, collections
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(root)
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(('design/', 'partials/', 'preview'))]
def exists(p):
    p = p.split('#')[0].split('?')[0]
    if p in ('', '/'): return True
    p = p.lstrip('/')
    return any(os.path.exists(c) for c in (p, p + '.html', p + '/index.html')) and not os.path.isdir(p) or os.path.isfile(p + '.html') or os.path.isfile(p)
bad = collections.defaultdict(set)
for f in files:
    h = open(f, errors='ignore').read()
    h = re.sub(r'<script[^>]*>.*?</script>', lambda m: m.group(0) if 'ld+json' in m.group(0) else '', h, flags=re.S)
    for u in re.findall(r'(?:href|src|content)="(/[^"]*)"', h):
        if u.startswith('//') or u.startswith('/api/'): continue
        if not exists(u): bad[u.split('#')[0].split('?')[0]].add(f)
for u in sorted(bad, key=lambda k: -len(bad[k])):
    print(f'{len(bad[u]):4d}  {u}' + ('   <- ' + ', '.join(sorted(bad[u])[:3]) if '--sumber' in sys.argv else ''))
print(f'\n{len(bad)} tujuan putus, dari {len(files)} halaman')
sys.exit(1 if bad else 0)
