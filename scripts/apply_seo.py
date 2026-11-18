"""Pastikan tag dasar SEO ada di setiap halaman publik, lalu laporkan yang kurang.
Jalankan setelah semua build:  python3 scripts/apply_seo.py"""
import collections, html, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://altora.id'
DEFAULT_IMG = SITE + '/assets/img/altora-logo-600.png'
skip = ('id/', 'leads/', 'outreach/', 'design/', 'partials/', 'ops/', 'content/', 'scripts/', 'dist/', 'node_modules/')

ICONS = ('<link href="/favicon.ico" rel="icon" sizes="any"/>'
         '<link href="/assets/img/altora-logo-icon-v2.svg" rel="icon" type="image/svg+xml"/>'
         '<link href="/favicon-48.png" rel="icon" sizes="48x48" type="image/png"/>'
         '<link href="/apple-touch-icon.png" rel="apple-touch-icon"/>'
         '<link href="/site.webmanifest" rel="manifest"/>'
         '<meta content="#7C5CE8" name="theme-color"/>')


def meta(s, attr, key):
    m = re.search(rf'<meta[^>]*{attr}="{re.escape(key)}"[^>]*>', s)
    if not m:
        return None
    c = re.search(r'content="([^"]*)"', m.group(0))
    return html.unescape(c.group(1)) if c else ''


def add_head(s, tag):
    return s.replace('</head>', tag + '</head>', 1)


report = collections.defaultdict(list)
titles = collections.defaultdict(list)
for f in sorted(root.rglob('*.html')):
    rel = f.relative_to(root).as_posix()
    if rel.startswith(skip) or rel.startswith('google'):
        continue
    s = f.read_text(encoding='utf-8'); orig = s
    # ikon: hapus link ikon lama, pasang set lengkap
    s = re.sub(r'<link[^>]*rel="(?:icon|apple-touch-icon|manifest)"[^>]*/?>', '', s)
    s = re.sub(r'<meta[^>]*name="theme-color"[^>]*/?>', '', s)
    s = add_head(s, ICONS)
    noindex = 'noindex' in (meta(s, 'name', 'robots') or '')
    title = (re.search(r'<title>([^<]*)', s) or [None, ''])[1]
    desc = meta(s, 'name', 'description')
    canon = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"|<link[^>]*href="([^"]+)"[^>]*rel="canonical"', s)
    url = (canon.group(1) or canon.group(2)) if canon else None
    if not noindex:
        titles[html.unescape(title)].append(rel)
        if not desc: report['tanpa meta description'].append(rel)
        elif not 70 <= len(desc) <= 170: report[f'description {len(desc)} karakter'].append(rel)
        if not url: report['tanpa canonical'].append(rel)
        if len(html.unescape(title)) > 65: report['title > 65 karakter'].append(f'{rel} ({len(html.unescape(title))})')
        # Open Graph & Twitter
        if not meta(s, 'property', 'og:site_name'): s = add_head(s, '<meta content="Altora Indonesia" property="og:site_name"/>')
        if not meta(s, 'property', 'og:title'): s = add_head(s, f'<meta content="{html.escape(html.unescape(title))}" property="og:title"/>')
        if desc and not meta(s, 'property', 'og:description'): s = add_head(s, f'<meta content="{html.escape(desc)}" property="og:description"/>')
        if url and not meta(s, 'property', 'og:url'): s = add_head(s, f'<meta content="{url}" property="og:url"/>')
        if not meta(s, 'property', 'og:image'): s = add_head(s, f'<meta content="{DEFAULT_IMG}" property="og:image"/>')
        if not meta(s, 'name', 'twitter:card'): s = add_head(s, '<meta content="summary_large_image" name="twitter:card"/>')
        if len(re.findall(r'<h1[\s>]', s)) != 1: report['jumlah h1 bukan 1'].append(rel)
    if s != orig:
        f.write_text(s, encoding='utf-8')

dups = {t: p for t, p in titles.items() if len(p) > 1}
for t, p in dups.items():
    report['title kembar'].append(f'"{t}" -> {", ".join(p)}')
for k, v in report.items():
    print(f'[{k}] {len(v)}'); [print('   ', x) for x in v[:12]]
print('apply_seo selesai')
