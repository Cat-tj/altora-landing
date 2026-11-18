"""Bersihkan sitemap.xml. Jalankan terakhir di build_all.sh. Membuang entri yang:
- file halamannya sudah tidak ada,
- halamannya noindex (meta robots), atau
- path-nya dialihkan di _redirects (sitemap hanya boleh berisi URL final 200 yang boleh diindeks)."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
sm = root / 'sitemap.xml'; s = sm.read_text(encoding='utf-8')


def redirect_rules():
    rules = []
    for line in (root / '_redirects').read_text(encoding='utf-8').splitlines():
        parts = line.split('#', 1)[0].split()
        if len(parts) >= 3 and parts[2].startswith('30'):
            src = parts[0]
            rules.append(re.compile('^' + re.escape(src).replace(r'\*', '.*').replace(':splat', '') + '$'))
    return rules


RULES = redirect_rules()


def file_of(path):
    p = path.strip('/')
    for c in ((root / 'index.html') if not p else None, root / (p + '.html'), root / p / 'index.html'):
        if c is not None and c.is_file():
            return c
    return None


def reason(path):
    f = file_of(path)
    if f is None:
        return 'tidak ada'
    if re.search(r'<meta[^>]*content="[^"]*noindex[^"]*"[^>]*name="robots"|<meta[^>]*name="robots"[^>]*content="[^"]*noindex', f.read_text(encoding='utf-8')):
        return 'noindex'
    if path not in ('', '/') and any(r.match(path) for r in RULES):
        return 'dialihkan'
    return None


removed = []
def keep(m):
    loc = re.search(r'<loc>https://altora\.id([^<]*)</loc>', m.group(0))
    why = reason(loc.group(1)) if loc else None
    if why:
        removed.append(f'{loc.group(1)} ({why})'); return ''
    return m.group(0)


s = re.sub(r'\s*<url>.*?</url>', keep, s, flags=re.S)
sm.write_text(s, encoding='utf-8')
print(f'sitemap: {len(removed)} entri dibuang, {len(re.findall("<loc>", s))} tersisa' + (': ' + ', '.join(removed[:8]) if removed else ''))
