"""JSON-LD untuk halaman tulisan-tangan + sinkron sameAs Altora ke semua halaman.
- contact, services, jasa-pembuatan-software-samarinda: blok JSON-LD bertanda data-schema="apply_schema", ditulis ulang tiap jalan.
- Setiap simpul ber-@id ORG_ID (beranda, halaman kota, layanan, dst.) mendapat sameAs dari site_data.SAME_AS.
Aman dijalankan berulang. Jalankan setelah apply_seo.py:  python3 scripts/apply_schema.py"""
import html, json, pathlib, re
from site_data import SITE, OFFICES, ORG_ID, SAME_AS, org, office_node

root = pathlib.Path(__file__).resolve().parent.parent
skip = ('leads/', 'outreach/', 'design/', 'partials/', 'ops/', 'content/', 'scripts/')
MARK = 'data-schema="apply_schema"'
LD_RE = re.compile(r'<script type="application/ld\+json"( data-schema="apply_schema")?>(.*?)</script>', re.S)


def head_text(s, pat):
    m = re.search(pat, s, re.S)
    return html.unescape(m.group(1)).strip() if m else ''


def services_list():
    out = []
    for f in sorted((root / 'services').glob('*.html')):
        s = f.read_text(encoding='utf-8')
        name = head_text(s, r'<title>([^<|]*)').strip()
        out.append((name, f'{SITE}/services/{f.stem}'))
    return out


def pages():
    offices = [office_node(o) for o in OFFICES]
    crumbs = lambda *items: {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}
    return {
        'contact.html': [org()] + offices + [
            {'@type': 'ContactPage', '@id': SITE + '/contact#halaman', 'url': SITE + '/contact', 'name': 'Konsultasi dengan Altora Indonesia',
             'inLanguage': 'id-ID', 'about': {'@id': ORG_ID}},
            crumbs(('Beranda', '/'), ('Konsultasi', '/contact'))],
        'services.html': [org(),
            {'@type': 'CollectionPage', '@id': SITE + '/services#halaman', 'url': SITE + '/services', 'name': 'Layanan Altora Indonesia',
             'inLanguage': 'id-ID', 'about': {'@id': ORG_ID},
             'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': i + 1, 'name': n, 'url': u} for i, (n, u) in enumerate(services_list())]}},
            crumbs(('Beranda', '/'), ('Layanan', '/services'))],
        'jasa-pembuatan-software-samarinda.html': [org(), office_node(next(o for o in OFFICES if o['hq'])),
            {'@type': 'Service', '@id': SITE + '/jasa-pembuatan-software-samarinda#layanan', 'name': 'Jasa pembuatan software Samarinda',
             'serviceType': 'Software custom', 'url': SITE + '/jasa-pembuatan-software-samarinda',
             'provider': {'@id': SITE + '/#kantor-samarinda'}, 'areaServed': {'@type': 'City', 'name': 'Samarinda'}},
            crumbs(('Beranda', '/'), ('Software house Samarinda', '/software-house-samarinda'), ('Jasa pembuatan software Samarinda', '/jasa-pembuatan-software-samarinda'))],
    }


def with_same_as(raw):
    """Tambahkan/ganti sameAs pada simpul ber-@id ORG_ID. Kembalikan None bila tidak ada perubahan."""
    try:
        data = json.loads(raw)
    except ValueError:
        return None
    changed = False

    def walk(o):
        nonlocal changed
        if isinstance(o, dict):
            if o.get('@id') == ORG_ID and len(o) > 1 and SAME_AS and o.get('sameAs') != SAME_AS:
                o['sameAs'] = list(SAME_AS); changed = True
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    return json.dumps(data, ensure_ascii=False) if changed else None


built = pages()
counts = dict(blok=0, sameAs=0)
for f in sorted(root.rglob('*.html')):
    rel = f.relative_to(root).as_posix()
    if rel.startswith(skip):
        continue
    s = f.read_text(encoding='utf-8'); orig = s
    if rel in built:
        # bs4 (build_services_hub) bisa menukar urutan atribut, jadi cocokkan kedua urutan agar idempoten
        s = re.sub(r'<script (?:type="application/ld\+json" ' + MARK + '|' + MARK + r' type="application/ld\+json")>.*?</script>', '', s, flags=re.S)
        block = f'<script type="application/ld+json" {MARK}>' + json.dumps({'@context': 'https://schema.org', '@graph': built[rel]}, ensure_ascii=False) + '</script>'
        s = s.replace('</head>', block + '</head>', 1)
        counts['blok'] += 1

    def sync(m):
        new = with_same_as(m.group(2))
        return m.group(0) if new is None else f'<script type="application/ld+json"{m.group(1) or ""}>{new}</script>'
    s2 = LD_RE.sub(sync, s)
    if s2 != s:
        counts['sameAs'] += 1; s = s2
    if s != orig:
        f.write_text(s, encoding='utf-8')
print(f"apply_schema: {counts['blok']} halaman diberi JSON-LD, sameAs disinkronkan di {counts['sameAs']} halaman"
      + ('' if SAME_AS else ' (SAME_AS di site_data.py masih kosong)'))
