"""Tulis partials/header.html dan partials/footer.html ke semua halaman publik.
Menu aktif (aria-current) ditentukan dari path halaman.
Jalankan dari root repo:  python3 scripts/apply_shell.py"""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
header_tpl = (root / 'partials/header.html').read_text(encoding='utf-8').strip()
footer = (root / 'partials/footer.html').read_text(encoding='utf-8').strip()
skip = ('id/', 'leads/', 'outreach/', 'design/', 'partials/', 'ops/')

def section_of(rel):
    route = '/' + rel[:-5]  # buang .html
    if route == '/index':
        return '/'
    for sec in ('/services', '/produk', '/portfolio', '/about', '/support', '/careers'):
        if route == sec or route.startswith(sec + '/'):
            return sec
    return None

def header_for(rel):
    sec = section_of(rel)
    h = header_tpl
    if sec:
        h = h.replace(f'data-section="{sec}" href', f'aria-current="page" data-section="{sec}" href')
    return h

changed = 0
for f in sorted(root.rglob('*.html')):
    rel = f.relative_to(root).as_posix()
    if rel.startswith(skip) or rel.startswith('google'):
        continue
    s = f.read_text(encoding='utf-8')
    new, n = re.subn(r'<header\b.*?</header>', lambda _: header_for(rel), s, count=1, flags=re.S)
    if n == 0:
        new = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + header_for(rel), new, count=1)
    new, n = re.subn(r'<footer\b.*?</footer>', lambda _: footer, new, count=1, flags=re.S)
    if n == 0:
        new = new.replace('</main>', '</main>' + footer, 1)
    if new != s:
        f.write_text(new, encoding='utf-8'); changed += 1
print(f'header & footer diterapkan ke {changed} halaman')
