"""Halaman /portofolio: proyek per kelompok (infrastruktur/IoT, AI, software, website) + daftar klien (teks saja).
Data di scripts/portofolio_data.py. Jalankan sebelum build_infra.py (lihat build_all.sh)."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import ORG_ID, org
from portofolio_data import GROUPS, PROJECTS, CLIENT_NAMES, card

root = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://altora.id'
URL = '/portofolio'
CSS_VER = '20261016i'
PF_CSS = '/assets/css/portofolio.css?v=20261118'
WA = 'https://wa.me/6285190911170?text='
MSG = 'Halo Altora, saya sudah melihat portofolio dan ingin membahas kebutuhan serupa.'
e = lambda t: html.escape(t, quote=True)
TITLE = 'Portofolio Proyek | Perangkat, AI, dan Software | Altora'
DESC = 'Proyek Altora Indonesia: CCTV AI, IoT, fleet management, absensi wajah, portal GIS, HRIS, dan website untuk pemerintahan, kampus, dan industri di Kaltim.'
H1 = 'Portofolio proyek'
LEAD = 'Perangkat, jaringan, AI, dan software yang sudah kami pasang dan kerjakan untuk pemerintahan, kampus, industri, dan usaha di Kalimantan Timur.'


def page():
    nav = ''.join(f'<li><a href="#{k}">{e(t)} <span>{sum(1 for p in PROJECTS if p["group"] == k)}</span></a></li>' for k, t, _ in GROUPS)
    sections = ''
    for k, t, d in GROUPS:
        cards = ''.join(card(p) for p in PROJECTS if p['group'] == k)
        sections += (f'<section class="svd-sec pf-group" id="{k}"><div class="bl-wrap"><div class="pf-group-head"><h2>{e(t)}</h2><p>{e(d)}</p></div>'
                     f'<div class="pf-grid">{cards}</div></div></section>\n')
    clients = ''.join(f'<li>{e(n)}</li>' for n in CLIENT_NAMES)
    wa = WA + quote(MSG)
    ld = {'@context': 'https://schema.org', '@graph': [org(),
        {'@type': 'CollectionPage', '@id': SITE + URL + '#halaman', 'url': SITE + URL, 'name': 'Portofolio proyek Altora Indonesia', 'description': DESC,
         'inLanguage': 'id-ID', 'about': {'@id': ORG_ID},
         'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(PROJECTS), 'itemListElement': [
             {'@type': 'ListItem', 'position': i, 'name': p['title'], 'url': f'{SITE}{URL}#{p["slug"]}'} for i, p in enumerate(PROJECTS, 1)]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Portofolio', 'item': SITE + URL}]}]}
    img = SITE + '/assets/img/portofolio/fleet-management-tambang.webp'
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(TITLE)}</title><meta content="{e(DESC)}" name="description"/><link href="{SITE}{URL}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(TITLE)}" property="og:title"/><meta content="{e(DESC)}" property="og:description"/><meta content="{SITE}{URL}" property="og:url"/><meta content="{img}" property="og:image"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="{PF_CSS}"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
<main class="bl-page svd-page">
<section class="bl-index-head"><div class="bl-wrap">
<nav aria-label="Breadcrumb" class="bl-crumb"><a href="/">Beranda</a><span>/</span><span>Portofolio</span></nav>
<p class="eyebrow eyebrow-purple">Portofolio</p><h1>{e(H1)}</h1><p class="bl-lead">{e(LEAD)}</p>
<ul class="pf-nav">{nav}</ul>
<div class="pf-actions"><a class="btn btn-purple" href="{wa}" rel="noopener" target="_blank">Konsultasi gratis</a></div>
</div></section>
{sections}<section class="svd-sec"><div class="bl-wrap"><div class="pf-group-head"><h2>Instansi dan perusahaan yang pernah bekerja sama</h2></div>
<ul class="pf-clients">{clients}</ul>
<p class="pf-note">Detail teknis dan data sensitif klien tidak ditampilkan. Untuk kebutuhan serupa, ceritakan lewat WhatsApp.</p></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Punya kebutuhan serupa?</h2><p>Ceritakan lokasi dan kebutuhan Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{wa}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


if __name__ == '__main__':
    (root / 'portofolio.html').write_text(page(), encoding='utf-8')
    from build_area import update_sitemap
    update_sitemap([URL])
    sm = root / 'sitemap.xml'
    t = sm.read_text(encoding='utf-8')
    t = re.sub(r'(<loc>' + re.escape(SITE + URL) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-11-18', t)
    sm.write_text(t, encoding='utf-8')
    print('halaman:', URL)
