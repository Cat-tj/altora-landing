"""Bangun katalog.html (barang dari principal resmi + jasa pemasangan) dari catalog_data.py.
Jalankan dari root repo:  python3 scripts/build_katalog.py && python3 scripts/apply_shell.py
Halaman /produk (aplikasi) dan portofolio sudah dihapus; skrip ini juga melepas blok produk di beranda bila masih ada."""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from urllib.parse import quote

root = pathlib.Path(__file__).resolve().parent.parent
WA = 'https://wa.me/6285190911170?text='

ICONS = {
    'doc': '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 15h6M9 18h4"/>',
    'folder': '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    'grid': '<rect height="16" rx="2" width="18" x="3" y="4"/><path d="M3 9h18M3 14h18M9 4v16M15 4v16"/>',
    'video': '<rect height="12" rx="2" width="13" x="3" y="6"/><path d="m16 10 5-3v10l-5-3z"/>',
    'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.2 3-5 6-5s5.4 1.8 6 5"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14.2c2.3.2 3.9 1.7 4.5 4.3"/>',
    'eye': '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/>',
    'key': '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2.5 2.5M14.5 8.5 17 11"/>',
    'truck': '<path d="M2.5 6.5h11v9h-11zM13.5 9.5h4l3 3.2v2.8h-7z"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'face': '<path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><circle cx="12" cy="10.5" r="2.6"/><path d="M8 17c.8-1.9 2.2-2.8 4-2.8s3.2.9 4 2.8"/>',
    'sensor': '<circle cx="12" cy="12" r="2.2"/><path d="M8.2 8.2a5.4 5.4 0 0 0 0 7.6M15.8 8.2a5.4 5.4 0 0 1 0 7.6M5.4 5.4a9.3 9.3 0 0 0 0 13.2M18.6 5.4a9.3 9.3 0 0 1 0 13.2"/>',
    'monitor': '<rect height="12" rx="2" width="18" x="3" y="4"/><path d="M9 20h6M12 16v4M7 12l3-3 2.5 2.5L17 7"/>',
    'cart': '<path d="M3 4h2.2l2.2 10.5h10.2L20 7.5H6.4"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
    'leaf': '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14Z"/><path d="M5 19 13 11"/>',
    'layers': '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    'chip': '<rect height="12" rx="2" width="12" x="6" y="6"/><path d="M9.5 9.5h5v5h-5zM9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    'signage': '<rect height="11" rx="1.5" width="18" x="3" y="3"/><path d="M12 14v7M8 21h8M7 7h6M7 10h10"/>',
    'satellite': '<path d="M4.5 13.5a6 6 0 0 0 6 6M4.5 9.5a10 10 0 0 0 10 10"/><circle cx="5" cy="19" r="1.4"/><path d="m13 4 3 3-3.5 3.5-3-3zM14.5 8.5 17 11M16 7l4-4"/>',
    'gauge': '<path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 17 4-5"/><circle cx="12" cy="17" r="1.3"/>',
}


e = lambda t: html.escape(t, quote=True)

def cart_btn(pid, name, meta, img, extra=''):
    return (f'<button class="cart-add {extra}" data-cart-id="{e(pid)}" data-cart-img="{e(img)}" data-cart-meta="{e(meta)}" '
            f'data-cart-name="{e(name)}" type="button"><span aria-hidden="true">+</span><span class="cart-add-label">Tambah ke keranjang</span></button>')

def icon(name):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[name]}</svg>'

from catalog_data import HW_CATS, HW_ITEMS, JASA

VIGI_ANCHOR = {'vigi-dome': 'dome', 'vigi-dome-ir': 'dome', 'vigi-turret': 'turret', 'vigi-bullet': 'bullet', 'vigi-aurora': 'bullet', 'vigi-ptz': 'pt',
               'vigi-panoramic': 'bullet', 'vigi-4g': 'pt', 'vigi-nvr': 'nvr', 'vigi-nvd': 'nvd', 'vigi-solar': 'solar', 'vigi-vms': 'net'}
SVC_LINK = {'konek': '/services/starlink-internet-satelit', 'kios': '/services/smart-display-kios'}

def hw_item(h):
    if h['img']:
        pic = f'<img alt="{e(h["name"])} — {e(h["brand"])}" loading="lazy" src="/assets/img/hardware/{h["img"]}.webp"/>'
    elif not h['logo']:
        pic = f'<span class="hwi-icon">{icon(h["icon"])}</span>'
    else:
        pic = f'<img alt="{e(h["brand"])}" class="hwi-logo-only" loading="lazy" src="/assets/img/partners/{h["logo"]}.png"/>'
    specs = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in h['specs'])
    msg = f'Halo Altora, saya ingin tahu lebih lanjut tentang {h["name"]} ({h["brand"]}).'
    return (f'<article class="hwi" data-cat="{h["cat"]}" id="{h["id"]}"><div class="hwi-pic">{pic}'
            + (f'<img alt="" class="hwi-brand" src="/assets/img/partners/{h["logo"]}.png"/>' if h['logo'] else '') + '</div>'
            f'<div class="hwi-body"><small>{e(h["brand"])}</small><h3>{e(h["name"])}</h3><p>{e(h["desc"])}</p>'
            f'<dl class="hwi-specs">{specs}</dl>'
            f'<div class="pd-actions">{cart_btn(h["id"], h["name"], h["brand"], f"/assets/img/hardware/{h['img']}.webp" if h['img'] else "")}'
            f'<a class="pd-link" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Tanya via WhatsApp</a>'
            + (f'<a class="pd-link" href="/katalog-cctv-vigi#{VIGI_ANCHOR.get(h["id"], "")}">Lihat semua model</a>' if h['brand'] == 'VIGI' else f'<a class="pd-link" href="{SVC_LINK.get(h["cat"], "/services/pengadaan-instalasi-maintenance")}">Instalasi & maintenance</a>') + '</div></div></article>')


def head(title, desc, url, ld, extra_css=''):
    return (f'<!DOCTYPE html>\n<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title>'
            f'<meta content="{e(desc)}" name="description"/><link href="https://altora.id{url}" rel="canonical"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/>'
            f'<meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="https://altora.id{url}" property="og:url"/>'
            '<meta content="https://altora.id/assets/img/altora-logo-600.png" property="og:image"/><link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/>'
            '<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>'
            '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>'
            '<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>'
            '<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>'
            f'<link rel="stylesheet" href="/assets/css/unify.css?v=20261019-katalog2"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>'
            '<body class="company-page"><header class="company-nav"></header>\n')

# ── /katalog: katalog belanja (aplikasi + perangkat, filter, keranjang, cetak) ──
def kat_jasa(j):
    jid, name, desc, inc, img, link = j
    return (f'<article class="hwi" data-cat="jasa" id="{jid}"><div class="hwi-pic hwi-pic-photo"><img alt="{e(name)}" loading="lazy" src="{img}"/></div>'
            f'<div class="hwi-body"><small>Jasa</small><h3>{e(name)}</h3><p>{e(desc)}</p>'
            '<div class="hwi-list"><b>Termasuk</b><ul>' + ''.join(f'<li>{e(x)}</li>' for x in inc) + '</ul></div>'
            f'<div class="pd-actions">{cart_btn(jid, name, "Jasa Altora", img)}<a class="pd-link" href="{link}">Detail jasa</a></div></div></article>')

# Pilihan "Cari apa?": tiap pilihan = kategori barang + id jasa/software yang relevan
VIEWS = [
    ('cctv', 'CCTV & keamanan', 'Kamera VIGI, NVR, tenaga surya, jasa pasang', '/assets/img/vigi/s385dps.webp',
     ['cctv'], ['jasa-pasang-cctv']),
    ('pengadaan', 'Pengadaan', 'Laptop, PC, server, perangkat resmi untuk kantor & instansi', '/assets/img/hardware/lenovo-thinkpad-t14.webp',
     ['laptop', 'computer', 'tablet', 'server'], ['jasa-pengadaan', 'jasa-server', 'jasa-kios-custom']),
    ('software', 'Website & aplikasi custom', 'Jasa pembuatan website dan aplikasi sesuai proses Anda', '/assets/img/hardware/lenovo-thinkpad-x1.webp',
     [], ['jasa-website', 'jasa-software']),
    ('jaringan', 'Jaringan & infrastruktur', 'WiFi, LAN, fiber, rak server, listrik', '/assets/img/hardware/hr-close-glass.webp',
     ['rack', 'fiber'], ['jasa-jaringan', 'jasa-fiber', 'jasa-listrik', 'jasa-it-support']),
    ('armada', 'GPS tracker', 'GPS tracker Teltonika, sensor, dan kamera kendaraan', '/assets/img/hardware/telt-fmc920.webp',
     ['gps'], ['jasa-gps']),
    ('internet', 'Starlink & internet', 'Kit Starlink, instalasi, off-grid', '/assets/img/hardware/starlink-v5.webp',
     ['konek'], ['jasa-starlink']),
    ('akses', 'Smartlock & akses', 'Kunci digital dan akses pintu', '/assets/img/hardware/smartlock.webp',
     ['akses'], []),
    ('display', 'Display, signage & kios', 'Videotron, IFP, kios layanan mandiri', '/assets/img/hardware/kios-k.webp',
     ['display', 'kios'], ['jasa-display', 'jasa-kios-custom']),
    ('jasa', 'Semua jasa', 'Pemasangan, instalasi, perawatan, pembuatan', '/assets/img/hardware/fas-fusion-splicer.webp',
     ['jasa'], []),
    ('barang', 'Semua barang', 'Seluruh perangkat di katalog', '/assets/img/hardware/hde-ifp.webp',
     [c for c, _ in HW_CATS], []),
]
views_json = json.dumps({k: {'t': t, 'cats': cats, 'ids': ids} for k, t, _, _, cats, ids in VIEWS}, ensure_ascii=False)
chooser = ''.join(f'<a class="kc-tile" data-view="{k}" href="#v-{k}"><span class="kc-pic"><img alt="" loading="lazy" src="{img}"/></span>'
                  f'<span class="kc-txt"><b>{e(t)}</b><small>{e(d)}</small></span></a>' for k, t, d, img, _, _ in VIEWS)
cat_names = dict(HW_CATS, jasa='Jasa')
cat_json = json.dumps(cat_names, ensure_ascii=False)
kat_ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Katalog Altora Indonesia', 'numberOfItems': len(HW_ITEMS) + len(JASA)}
katalog_page = head('Katalog Altora | Perangkat & Jasa', 'Katalog Altora: CCTV VIGI, GPS, Starlink, smartlock, laptop & server Lenovo, display, jaringan, dan jasa pemasangan. Tambah ke keranjang, kirim via WhatsApp.', '/katalog', kat_ld) + f"""<main class="pd-page kt-page">
<section class="pd-hero kt-hero"><div class="pd-wrap">
<div class="kt-bar"><p class="eyebrow eyebrow-purple">Katalog</p><button class="btn btn-outline kt-print" onclick="window.print()" type="button">Cetak / simpan PDF</button></div>
<h1>Anda sedang mencari apa?</h1>
<p class="pd-lead">Pilih kebutuhan Anda, kami tampilkan perangkat dan jasa yang relevan. Tambahkan ke keranjang, lalu kirim lewat WhatsApp untuk penawaran.</p>
<nav aria-label="Pilih kebutuhan" class="kc-grid">{chooser}</nav>
</div></section>
<section class="pd-block kt-results" hidden="" id="hasil"><div class="pd-wrap">
<div class="kr-head"><a class="kr-back" href="#">← Ganti pilihan</a><h2 class="kr-title"></h2><span class="kr-count"></span></div>
<div aria-label="Saring" class="hwi-filter kr-sub" role="group"></div>
<div class="hwi-allvigi kr-vigi" hidden=""><div><b>Katalog lengkap CCTV VIGI</b><br/><span>148 model kamera, NVR, kit, decoder, solar, dan jaringan pendukung.</span></div><a class="btn btn-purple" href="/katalog-cctv-vigi">Lihat semua model VIGI →</a></div>
<div class="hwi-grid">{"".join(hw_item(h) for h in HW_ITEMS)}{"".join(kat_jasa(j) for j in JASA)}</div>
<div class="hwi-more"><div><b>Tidak menemukan yang dicari?</b><p>Kami juga mengadakan perangkat lain sesuai spesifikasi proyek Anda: jaringan TP-Link Omada, model Lenovo lainnya, dan perangkat khusus.</p></div>
<a class="btn btn-purple" href="{WA}{quote("Halo Altora, saya mencari perangkat/jasa yang tidak ada di katalog.")}" rel="noopener" target="_blank">Tanya via WhatsApp →</a></div>
</div></section>
</main>
<footer></footer>
<script id="kc-views" type="application/json">{views_json}</script><script id="kc-cats" type="application/json">{cat_json}</script>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="/assets/js/hw-filter.js?v=20261014d"></script></body></html>
"""
(root / 'katalog.html').write_text(katalog_page, encoding='utf-8')
print('katalog.html dibuat')

# ── Blok grid produk di beranda (aplikasi) sudah tidak dipakai: lepas bila masih ada ──
idx = root / 'index.html'
s = idx.read_text(encoding='utf-8')
s = re.sub(r'<!-- produk-ringkas:start -->.*?<!-- produk-ringkas:end -->', '', s, flags=re.S)
idx.write_text(s, encoding='utf-8')
