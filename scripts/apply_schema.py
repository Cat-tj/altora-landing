"""JSON-LD entitas Altora untuk seluruh situs. Aman dijalankan berulang. Jalankan setelah apply_seo.py:  python3 scripts/apply_schema.py
1. Halaman tulisan-tangan (beranda, contact, services, jasa-pembuatan-software-samarinda): blok JSON-LD bertanda
   data-schema="apply_schema" ditulis ulang setiap jalan. Beranda memuat Organization lengkap (org_full) + kantor + WebSite + FAQPage.
2. Setiap simpul ber-@id ORG_ID diseragamkan dengan site_data.org() (nilai sama di semua halaman, termasuk sameAs),
   jadi tidak ada data Organization yang saling bertentangan antarhalaman.
3. Simpul halaman (WebPage, BlogPosting, CollectionPage, ...) diberi publisher {"@id": ORG_ID}; halaman indeks yang belum
   punya simpul halaman diberi blok WebPage kecil bertanda data-schema="apply_schema-page"."""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import SITE, OFFICES, ORG_ID, SAME_AS, HOME_FAQ, org, org_full, office_node, office_id

root = pathlib.Path(__file__).resolve().parent.parent
skip = ('leads/', 'outreach/', 'design/', 'partials/', 'ops/', 'content/', 'scripts/', 'dist/', 'node_modules/')
MARK = 'data-schema="apply_schema"'
PMARK = 'data-schema="apply_schema-page"'
LD_RE = re.compile(r'<script type="application/ld\+json"( data-schema="apply_schema(?:-page)?")?>(.*?)</script>', re.S)
PAGE_TYPES = {'WebPage', 'AboutPage', 'ContactPage', 'CollectionPage', 'FAQPage', 'BlogPosting', 'Article', 'Blog', 'ItemPage'}
PUBLISHER_TYPES = {'WebPage', 'AboutPage', 'ContactPage', 'CollectionPage', 'BlogPosting', 'Article', 'Blog', 'ItemPage'}
ORG_REF = {'@id': ORG_ID}


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


def faq_page(items, pid):
    return {'@type': 'FAQPage', '@id': pid, 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def pages():
    offices = [office_node(o) for o in OFFICES]
    crumbs = lambda *items: {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}
    home = [org_full()] + offices + [
        {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Altora Indonesia', 'alternateName': 'Altora',
         'inLanguage': 'id-ID', 'publisher': ORG_REF},
        {'@type': 'WebPage', '@id': SITE + '/#halaman', 'url': SITE + '/', 'name': 'Altora Indonesia | Software House Samarinda & Balikpapan',
         'inLanguage': 'id-ID', 'isPartOf': {'@id': SITE + '/#website'}, 'about': ORG_REF, 'publisher': ORG_REF},
        faq_page(HOME_FAQ, SITE + '/#faq')]
    hq = next(o for o in OFFICES if o['hq'])
    return {
        'index.html': home,
        'beranda.html': home,
        'contact.html': [org_full()] + offices + [
            {'@type': 'ContactPage', '@id': SITE + '/contact#halaman', 'url': SITE + '/contact', 'name': 'Konsultasi dengan Altora Indonesia',
             'inLanguage': 'id-ID', 'about': ORG_REF, 'publisher': ORG_REF},
            crumbs(('Beranda', '/'), ('Konsultasi', '/contact'))],
        'services.html': [org(),
            {'@type': 'CollectionPage', '@id': SITE + '/services#halaman', 'url': SITE + '/services', 'name': 'Layanan Altora Indonesia',
             'inLanguage': 'id-ID', 'about': ORG_REF, 'publisher': ORG_REF,
             'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': i + 1, 'name': n, 'url': u} for i, (n, u) in enumerate(services_list())]}},
            crumbs(('Beranda', '/'), ('Layanan', '/services'))],
        'jasa-pembuatan-software-samarinda.html': [org(), office_node(hq),
            {'@type': 'WebPage', '@id': SITE + '/jasa-pembuatan-software-samarinda#halaman', 'url': SITE + '/jasa-pembuatan-software-samarinda',
             'name': 'Jasa pembuatan software Samarinda', 'inLanguage': 'id-ID', 'publisher': ORG_REF},
            {'@type': 'Service', '@id': SITE + '/jasa-pembuatan-software-samarinda#layanan', 'name': 'Jasa pembuatan software Samarinda',
             'serviceType': 'Software custom', 'url': SITE + '/jasa-pembuatan-software-samarinda',
             'provider': {'@id': office_id(hq)}, 'areaServed': {'@type': 'City', 'name': 'Samarinda'}},
            crumbs(('Beranda', '/'), ('Software house Samarinda', '/software-house-samarinda'), ('Jasa pembuatan software Samarinda', '/jasa-pembuatan-software-samarinda'))],
    }


def types(o):
    t = o.get('@type')
    return set(t if isinstance(t, list) else [t]) if t else set()


def normalize(raw):
    """Seragamkan simpul Organization Altora dan tambahkan publisher. Kembalikan (json_baru|None, ada_simpul_halaman)."""
    try:
        data = json.loads(raw)
    except ValueError:
        return None, False
    base = org()
    state = dict(changed=False, page=False)

    def walk(o):
        if isinstance(o, dict):
            ts = types(o)
            if ts & PAGE_TYPES:
                state['page'] = True
            if ts & PUBLISHER_TYPES and 'publisher' not in o:
                o['publisher'] = dict(ORG_REF); state['changed'] = True
            if o.get('@id') == ORG_ID and len(o) > 1:
                for k, v in base.items():
                    if o.get(k) != v:
                        o[k] = v; state['changed'] = True
                if 'sameAs' in o and not SAME_AS:
                    del o['sameAs']; state['changed'] = True
            for k, v in list(o.items()):
                # Organization Altora tanpa @id (versi lama) -> rujukan ke entitas tunggal
                if isinstance(v, dict) and 'Organization' in types(v) and v.get('name') in ('Altora Indonesia', 'Tim Altora Indonesia') and '@id' not in v:
                    o[k] = dict(ORG_REF); state['changed'] = True
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(data)
    return (json.dumps(data, ensure_ascii=False) if state['changed'] else None), state['page']


def insert_head(s, block):
    """Sisipkan blok di posisi tetap (sebelum set ikon dari apply_seo, atau sebelum </head>) supaya hasil build stabil."""
    i = s.find('<link href="/favicon.ico" rel="icon"')
    j = s.find('</head>')
    pos = i if 0 <= i < j else j
    return s[:pos] + block + s[pos:]


def meta(s, name):
    m = re.search(rf'<meta[^>]*name="{name}"[^>]*>', s)
    c = re.search(r'content="([^"]*)"', m.group(0)) if m else None
    return html.unescape(c.group(1)) if c else ''


if __name__ == '__main__':
    built = pages()
    counts = dict(blok=0, norm=0, page=0)
    for f in sorted(root.rglob('*.html')):
        rel = f.relative_to(root).as_posix()
        if rel.startswith(skip) or rel.startswith('google'):
            continue
        s = f.read_text(encoding='utf-8'); orig = s
        if rel in built:
            # bs4 (build_services_hub) bisa menukar urutan atribut, jadi cocokkan kedua urutan agar idempoten
            s = re.sub(r'<script (?:type="application/ld\+json" ' + MARK + '|' + MARK + r' type="application/ld\+json")>.*?</script>', '', s, flags=re.S)
            if rel in ('index.html', 'beranda.html'):
                # blok lama tulisan-tangan beranda (Organization tanpa penanda) diganti blok bertanda
                s = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*?"@id": "https://altora\.id/#organization"(?:(?!</script>).)*?</script>', '', s, flags=re.S)
            block = f'<script type="application/ld+json" {MARK}>' + json.dumps({'@context': 'https://schema.org', '@graph': built[rel]}, ensure_ascii=False) + '</script>'
            s = insert_head(s, block)
            counts['blok'] += 1
        s = re.sub(r'<script type="application/ld\+json" ' + PMARK + r'>.*?</script>', '', s, flags=re.S)
        has_page = [False]

        def sync(m):
            new, page = normalize(m.group(2))
            has_page[0] = has_page[0] or page
            if new is None or m.group(1):   # blok bertanda apply_schema sudah dibangun dari org()/org_full()
                return m.group(0)
            return f'<script type="application/ld+json">{new}</script>'
        s2 = LD_RE.sub(sync, s)
        if s2 != s:
            counts['norm'] += 1; s = s2
        canon = re.search(r'<link href="([^"]+)" rel="canonical"', s)
        if not has_page[0] and 'noindex' not in meta(s, 'robots') and canon:
            node = {'@context': 'https://schema.org', '@type': 'WebPage', '@id': canon.group(1) + '#halaman', 'url': canon.group(1),
                    'name': head_text(s, r'<title>([^<]*)'), 'inLanguage': 'id-ID', 'isPartOf': {'@id': SITE + '/#website'}, 'publisher': ORG_REF}
            if meta(s, 'description'):
                node['description'] = meta(s, 'description')
            s = insert_head(s, f'<script type="application/ld+json" {PMARK}>' + json.dumps(node, ensure_ascii=False) + '</script>')
            counts['page'] += 1
        if s != orig:
            f.write_text(s, encoding='utf-8')
    print(f"apply_schema: {counts['blok']} blok halaman tulisan-tangan, {counts['norm']} halaman diseragamkan, {counts['page']} blok WebPage"
          + ('' if SAME_AS else ' (SAME_AS di site_data.py masih kosong)'))
