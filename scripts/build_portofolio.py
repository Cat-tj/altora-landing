"""Halaman /portofolio: proyek per kelompok (infrastruktur/IoT, AI, software, website) + daftar klien (teks saja).
Data di scripts/portofolio_data.py. Jalankan sebelum build_infra.py (lihat build_all.sh)."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import ORG_ID, org
from portofolio_data import GROUPS, PROJECTS, CLIENT_NAMES, BY, card, icon, e as esc, IMG

root = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://altora.id'
URL = '/portofolio'
CSS_VER = '20261016i'
PF_CSS = '/assets/css/portofolio.css?v=20261118a'
PF_JS = '/assets/js/portofolio.js?v=20261118a'
WA = 'https://wa.me/6285190911170?text='
MSG = 'Halo Altora, saya sudah melihat portofolio dan ingin membahas kebutuhan serupa.'
e = lambda t: html.escape(t, quote=True)
TITLE = 'Portofolio Proyek | Perangkat, AI, dan Software | Altora'
DESC = 'Proyek Altora Indonesia: CCTV AI, IoT, fleet management, absensi wajah, portal GIS, HRIS, dan website untuk pemerintahan, kampus, dan industri di Kaltim.'
LEAD = (f'{len(PROJECTS)} proyek perangkat, jaringan, AI, dan software untuk pemerintahan, kampus, industri, dan usaha di Kalimantan Timur. '
        'Data sensitif klien tidak ditampilkan.')
PROOF = [('AI', 'Vision & analytics'), ('IoT', 'Perangkat & lapangan'), ('Software', 'Workflow & data')]
FEATURED = ['pompy-batara', 'deteksi-apd-ai', 'fleet-management-tambang']   # tiga proyek berscreenshot yang paling relevan
HERO_SLUG = 'fleet-management-tambang'
TRUST = ['Diskusi awal gratis', 'Tanpa kewajiban lanjut', 'Tim lokal Kaltim']
KIND_LABEL = {'infra': 'Infrastruktur & IoT', 'ai': 'AI & vision', 'software': 'Software & data', 'web': 'Website'}
ICON_DOC = '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>'


def wa_url(msg):
    return WA + quote(msg)


def head_html(title, desc, url, img, ld):
    return (f'<!DOCTYPE html>\n<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title>'
            f'<meta content="{e(desc)}" name="description"/><link href="{SITE}{url}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/>'
            f'<meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(title)}" property="og:title"/>'
            f'<meta content="{e(desc)}" property="og:description"/><meta content="{SITE}{url}" property="og:url"/><meta content="{img}" property="og:image"/>'
            '<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>'
            '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>'
            '<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>'
            '<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>'
            f'<link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="{PF_CSS}"/>'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>\n')


def cta_html(msg):
    trust = ''.join(f'<li>{e(t)}</li>' for t in TRUST)
    return (f'<section class="pf-cta"><div aria-hidden="true" class="pf-dots"></div><div class="pf-wrap"><div class="pf-band pf-rv"><h2>Butuh sistem serupa?</h2>'
            f'<p>Ceritakan kebutuhan Anda. Diskusi awal gratis.</p><div class="pf-actions"><a class="pf-btn pf-btn-white" href="{wa_url(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a>'
            f'<a class="pf-btn pf-btn-outline" href="/contact">Kirim pesan</a></div><ul class="pf-trust">{trust}</ul></div></div></section>\n')


def tail_html():
    return f'</main>\n<footer></footer>\n<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="{PF_JS}"></script></body></html>\n'


def hero_media(p, alt=''):
    if p.get('img'):
        return f'<div class="pf-media"><img alt="{e(alt)}" decoding="async" fetchpriority="high" height="770" src="{IMG}{e(p["img"])}" width="1120"/></div>'
    return f'<div class="pf-media"><div class="pf-media-ph"><span class="pf-ico">{icon(p["icon"])}</span></div></div>'


def page():
    counts = {k: sum(1 for p in PROJECTS if p['group'] == k) for k, _, _ in GROUPS}
    filters = f'<button aria-pressed="true" class="is-active" data-filter="all" type="button">Semua <b>{len(PROJECTS)}</b></button>' + ''.join(
        f'<button aria-pressed="false" data-filter="{k}" type="button">{e(KIND_LABEL[k])} <b>{counts[k]}</b></button>' for k, _, _ in GROUPS)
    proof = ''.join(f'<div><b>{e(a)}</b><small>{e(b)}</small></div>' for a, b in PROOF)
    shots = ''.join(
        f'<a class="pf-shot pf-rv" href="/portofolio/{BY[k]["slug"]}"><img alt="{e(BY[k]["title"])}" decoding="async" height="375" loading="lazy" src="{IMG}{e(BY[k]["img"])}" width="500"/>'
        f'<span class="cap"><small>{e(BY[k]["client"])}</small><b>{e(BY[k]["title"])}</b></span></a>' for k in FEATURED)
    cards = ''.join(card(p, 'full') for p in PROJECTS)
    clients = ''.join(f'<li>{e(n)}</li>' for n in CLIENT_NAMES)
    msg = 'Halo Altora, saya sudah melihat portofolio dan ingin membahas kebutuhan serupa.'
    ld = {'@context': 'https://schema.org', '@graph': [org(),
        {'@type': 'CollectionPage', '@id': SITE + URL + '#halaman', 'url': SITE + URL, 'name': 'Portofolio proyek Altora Indonesia', 'description': DESC,
         'inLanguage': 'id-ID', 'about': {'@id': ORG_ID},
         'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(PROJECTS), 'itemListElement': [
             {'@type': 'ListItem', 'position': i, 'name': p['title'], 'url': f'{SITE}{URL}/{p["slug"]}'} for i, p in enumerate(PROJECTS, 1)]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Portofolio', 'item': SITE + URL}]}]}
    img = SITE + IMG + BY[HERO_SLUG]['img']
    return head_html(TITLE, DESC, URL, img, ld) + f"""<main class="pf-page" id="main">
<section class="pf-hero"><div class="pf-wrap pf-split"><div class="pf-ph"><h1>Solusi yang <span class="pf-hl">nyata bekerja.</span></h1><p class="pf-lead">{e(LEAD)}</p><div class="pf-proof">{proof}</div>
<div class="pf-actions"><a class="pf-btn pf-btn-primary" href="{wa_url(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a></div></div>
<div class="pf-rv">{hero_media(BY[HERO_SLUG], 'Fleet management armada hauling')}</div></div></section>
<section class="pf-sec pf-sec-alt"><div class="pf-wrap"><div class="pf-head center pf-rv"><h2>Mulai dari bukti yang paling relevan.</h2><p class="pf-lead">Tiga proyek ini memperlihatkan bentuk kerja kami: data wilayah, keselamatan kerja berbasis AI, dan telematik armada.</p></div>
<div class="pf-shots">{shots}</div></div></section>
<section class="pf-sec"><div class="pf-wrap"><div class="pf-head center pf-rv"><h2>Eksplorasi proyek lainnya.</h2><p class="pf-lead">Pilih kategori untuk menyaring proyek.</p></div>
<div aria-label="Filter" class="pf-filters" role="group">{filters}</div>
<div class="pf-grid">{cards}</div></div></section>
<section class="pf-sec pf-sec-alt pf-sec-tight"><div class="pf-wrap"><div class="pf-head center pf-rv" style="margin-bottom:24px"><h2 style="font-size:clamp(1.5rem,1.2rem + 1.2vw,2rem)">Instansi dan perusahaan yang pernah bekerja sama</h2></div>
<ul class="pf-clients">{clients}</ul><p class="pf-note">Detail teknis dan data sensitif klien tidak ditampilkan. Untuk kebutuhan serupa, ceritakan lewat WhatsApp.</p></div></section>
""" + cta_html(msg) + tail_html()


def first_sentence(t):
    m = re.match(r'(.+?[.!?])(\s|$)', t)
    return m.group(1) if m else t


def short_desc(p):
    t = p['desc']
    if len(t) <= 155:
        return t
    s = first_sentence(t)
    return s if len(s) <= 155 else t[:152].rsplit(' ', 1)[0] + '...'


def detail(p):
    url = f'{URL}/{p["slug"]}'
    title = f'{p["title"]} | Portofolio Altora'
    if len(title) > 65:
        title = f'{p["title"].split(":")[0]} | Portofolio Altora'
    if len(title) > 65:
        title = f'{p["title"].split(":")[0]} | Altora'
    desc = short_desc(p)
    msg = f'Halo Altora, saya tertarik dengan sistem serupa "{p["title"]}".'
    ext = p.get('link') and p['link'][0].startswith('http')
    acts = f'<a class="pf-btn pf-btn-primary" href="{wa_url(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a>'
    if ext:
        acts += f'<a class="pf-btn pf-btn-ghost" href="{esc(p["link"][0])}" rel="noopener" target="_blank">Kunjungi situs ↗</a>'
    facts = f'<div><dt>Klien</dt><dd>{esc(p["client"])}</dd></div>'
    if p['year']:
        facts += f'<div><dt>Tahun</dt><dd>{esc(p["year"])}</dd></div>'
    facts += f'<div><dt>Teknologi</dt><dd>{esc(", ".join(p["tags"]))}</dd></div>'
    facts += f'<div><dt>Kategori</dt><dd>{esc(KIND_LABEL[p["group"]])}</dd></div>'
    if ext:
        host = p['link'][0].split('//', 1)[1].rstrip('/')
        facts += f'<div><dt>Situs langsung</dt><dd><a href="{esc(p["link"][0])}" rel="noopener" target="_blank">{esc(host)} ↗</a></dd></div>'
    mini = ''
    if p.get('link') and not ext:
        mini = (f'<div class="pf-mt"><a class="pf-mini" href="{esc(p["link"][0])}"><span class="pf-mi"><svg aria-hidden="true" viewBox="0 0 24 24">{ICON_DOC}</svg></span>'
                f'<span><b>{esc(p["link"][1].replace("Baca: ", ""))}</b><small>Artikel terkait</small></span></a></div>')
    same = [q for q in PROJECTS if q['group'] == p['group'] and q['slug'] != p['slug']]
    rest = [q for q in PROJECTS if q['group'] != p['group']]
    rel_cards = ''.join(card(q) for q in (same + rest)[:3])
    ld = {'@context': 'https://schema.org', '@graph': [org(),
        {'@type': 'WebPage', '@id': SITE + url + '#halaman', 'url': SITE + url, 'name': title, 'description': desc, 'inLanguage': 'id-ID',
         'isPartOf': {'@id': SITE + URL + '#halaman'}, 'about': {'@id': ORG_ID}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Portofolio', 'item': SITE + URL},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': SITE + url}]}]}
    img = SITE + IMG + (p['img'] if p.get('img') else BY[HERO_SLUG]['img'])
    return head_html(title, desc, url, img, ld) + f"""<main class="pf-page" id="main">
<section class="pf-hero"><div class="pf-wrap pf-split"><div class="pf-ph"><nav aria-label="Breadcrumb" class="pf-crumb"><a href="/">Beranda</a><a href="{URL}">Portofolio</a><span>{esc(p['title'])}</span></nav>
<h1>{esc(p['title'])}</h1><p class="pf-lead">{esc(first_sentence(p['desc']))}</p><div class="pf-actions">{acts}</div></div>
<div class="pf-rv">{hero_media(p, p['title'])}</div></div></section>
<section class="pf-sec pf-sec-alt"><div class="pf-wrap pf-split top"><div class="pf-split-copy pf-rv"><h2>Tentang proyek ini</h2><p class="pf-lead">{esc(p['desc'])}</p></div>
<div class="pf-rv"><dl class="pf-facts">{facts}</dl>{mini}</div></div></section>
<section class="pf-sec"><div class="pf-wrap"><div class="pf-head center pf-rv"><h2>Eksplorasi proyek lainnya.</h2></div><div class="pf-grid">{rel_cards}</div>
<p class="pf-note"><a href="{URL}" style="color:#5B3FC4;font-weight:700">Lihat semua portofolio →</a></p></div></section>
""" + cta_html(msg) + tail_html()


if __name__ == '__main__':
    (root / 'portofolio.html').write_text(page(), encoding='utf-8')
    (root / 'portofolio').mkdir(exist_ok=True)
    for p in PROJECTS:
        (root / 'portofolio' / f'{p["slug"]}.html').write_text(detail(p), encoding='utf-8')
    urls = [URL] + [f'{URL}/{p["slug"]}' for p in PROJECTS]
    from build_area import update_sitemap
    update_sitemap(urls)
    sm = root / 'sitemap.xml'
    t = sm.read_text(encoding='utf-8')
    for u in urls:
        t = re.sub(r'(<loc>' + re.escape(SITE + u) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-11-18', t)
    sm.write_text(t, encoding='utf-8')
    print('halaman:', URL, '+', len(PROJECTS), 'detail')
