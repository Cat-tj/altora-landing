"""Bangun produk.html dari data PRODUCTS di bawah.
Jalankan dari root repo:  python3 scripts/build_produk.py && python3 scripts/apply_shell.py"""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from urllib.parse import quote

root = pathlib.Path(__file__).resolve().parent.parent
WA = 'https://wa.me/6285190911170?text='

ICONS = {
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

GROUPS = [
    ('sdm', 'SDM & absensi', 'Absensi, jadwal, dan gaji tanpa rekap manual.'),
    ('aman', 'Keamanan & akses', 'CCTV pintar dan akses pintu digital.'),
    ('lapangan', 'Armada, lahan & sensor', 'Pantau kendaraan, lahan, dan sensor dari satu layar.'),
    ('data', 'Data & AI', 'AI dan pemetaan yang berjalan di server Anda sendiri.'),
    ('segera', 'Segera hadir', 'Untuk toko, kafe, dan usaha dengan banyak cabang.'),
]

PRODUCTS = [
    dict(id='teams', group='sdm', icon='users', tone='purple', name='Altora Teams', tagline='HRIS & People Operations',
         desc='Sistem kelola SDM: absensi GPS & selfie, shift kerja, pengajuan cuti/izin, reimbursement, dan payroll otomatis.',
         feats=['Absensi GPS & validasi', 'Shift & schedule builder', 'Cuti, izin & reimbursement', 'Payroll & portal karyawan'],
         cta='Coba Altora Teams', proof='/portfolio/altora-teams'),
    dict(id='attendance', group='sdm', icon='face', tone='pink', name='Altora Smart Attendance', tagline='Face recognition dari CCTV',
         desc='Absensi otomatis berbasis AI yang mengenali wajah dari kamera CCTV. Tanpa antre di mesin absensi atau tempel kartu.',
         feats=['Face recognition dari CCTV', 'Check-in otomatis & timestamp', 'Integrasi ke HRIS & akses gedung', 'Audit log kehadiran'],
         cta='Konsultasi Smart Attendance', proof='/portfolio/smart-attendance'),
    dict(id='vision', group='aman', icon='eye', tone='green', name='Altora Vision', tagline='AI CCTV & Safety Analytics',
         desc='Deteksi kepatuhan APD, pengawasan area berbahaya, dan analitik pengunjung langsung dari jaringan CCTV yang sudah ada.',
         feats=['Deteksi APD & kepatuhan safety', 'Pengawasan zona terlarang', 'People & vehicle counting', 'Dashboard alert real-time'],
         cta='Konsultasi Altora Vision', proof='/portfolio/ai-safety-vision'),
    dict(id='pass', group='aman', icon='key', tone='blue', name='Altora Pass', tagline='Smart Access & Gate Control',
         desc='Akses pintu digital, smartlock, dan turnstile gate terintegrasi untuk kontrol masuk karyawan, tamu, serta kendaraan.',
         feats=['Smartlock & akses RFID / QR', 'Turnstile & barrier gate', 'Izin akses bertingkat', 'Log akses real-time'],
         cta='Tanya Altora Pass', proof='/portfolio/smartlock-akses-digital'),
    dict(id='fms', group='lapangan', icon='truck', tone='orange', name='Altora FMS', tagline='Fleet Management System',
         desc='Pantau armada, perjalanan, dan aktivitas kendaraan dalam satu tampilan yang mudah ditindaklanjuti.',
         feats=['Live vehicle tracking', 'Riwayat perjalanan & rute', 'Geofence & alert operasional', 'Dashboard & laporan armada'],
         cta='Konsultasi Altora FMS', proof='/portfolio/fleet-management'),
    dict(id='sense', group='lapangan', icon='sensor', tone='cyan', name='Altora Sense', tagline='IoT Monitoring & Safety Sensors',
         desc='Sensor untuk memantau asap, api, suhu, kelembapan, dan kondisi lapangan agar tim menerima alert saat diperlukan.',
         feats=['Deteksi asap & api', 'Monitoring suhu & kelembapan', 'Status perangkat & alert', 'Sensor gateway & dashboard'],
         cta='Konsultasi Altora Sense', proof='/portfolio/iot-monitoring-lahan'),
    dict(id='farming', group='lapangan', icon='leaf', tone='green', name='Altora Smart Farming', tagline='IoT Monitoring Lahan Pertanian',
         desc='Aplikasi pemantauan lahan dari sensor lapangan: kelembapan tanah, kondisi tanaman, suhu, dan kelembapan udara langsung di ponsel petugas.',
         feats=['Kelembapan tanah per petak', 'Status & kondisi tanaman', 'Suhu & kelembapan udara', 'Catatan field check'],
         cta='Konsultasi Smart Farming', proof='/portfolio/iot-monitoring-lahan'),
    dict(id='command', group='lapangan', icon='monitor', tone='purple', name='Altora Command', tagline='Command Center & Operations Monitoring',
         desc='Tampilan operasional terpusat untuk memantau CCTV AI, armada, sensor, dan status perangkat sesuai kebutuhan lokasi Anda.',
         feats=['Tampilan operasional terpadu', 'Monitoring CCTV, armada & sensor', 'Visibilitas alert & insiden', 'Setup command center custom'],
         cta='Diskusikan Command Center', proof='/services/iot-command-center'),
    dict(id='private-ai', group='data', icon='chip', tone='blue', name='Altora Private AI & GIS', tagline='AI on-premise & peta data spasial',
         desc='Asisten AI yang berjalan di server Anda sendiri, tanpa mengirim data ke cloud publik. Dilengkapi GIS untuk memetakan dan menganalisis data wilayah secara terpusat.',
         feats=['Model bahasa (LLM) on-premise / air-gapped', 'Membaca data internal yang sudah ada', 'GIS: peta & analisis data spasial', 'Server, enkripsi, backup & pelatihan tim'],
         cta='Konsultasi Private AI', proof='/services/private-ai-gis'),
    dict(id='pos', group='segera', icon='cart', tone='gray', name='Altora POS', tagline='Point of Sale & Kasir', soon=True,
         desc='Kasir modern untuk retail & F&B: pencatatan pesanan cepat, stok toko real-time, integrasi QRIS, dan laporan penjualan.',
         feats=['Kasir cepat retail & F&B', 'Stok & varian produk', 'Integrasi QRIS / EDC', 'Multi-cabang & laporan penjualan'],
         cta='Daftar info peluncuran'),
    dict(id='erp', group='segera', icon='layers', tone='gray', name='Altora ERP', tagline='Enterprise Resource Planning', soon=True,
         desc='Sistem operasional terpadu: stok multi-gudang, purchasing, laporan keuangan, dan dashboard eksekutif multi-cabang.',
         feats=['Stok multi-gudang & transfer', 'Purchasing & portal supplier', 'Laporan keuangan & akuntansi', 'Dashboard operasional eksekutif'],
         cta='Daftar info peluncuran'),
]

e = lambda t: html.escape(t, quote=True)

# Foto ilustrasi penggunaan per produk (assets/img/produk/<id>.webp, 800x1000 portrait).
# Nilai = object-position agar potongan 4:3 tetap fokus ke layar perangkat.
PHOTO_FOCUS = {
    'teams': '60% 62%', 'attendance': '75% 35%', 'vision': '60% 62%', 'pass': '60% 58%', 'fms': '55% 62%',
    'sense': '62% 58%', 'farming': '62% 58%', 'command': '60% 62%', 'pos': '50% 58%', 'erp': '62% 58%', 'private-ai': '50% 50%',
}

def cart_btn(pid, name, meta, img, extra=''):
    return (f'<button class="cart-add {extra}" data-cart-id="{e(pid)}" data-cart-img="{e(img)}" data-cart-meta="{e(meta)}" '
            f'data-cart-name="{e(name)}" type="button"><span aria-hidden="true">+</span><span class="cart-add-label">Tambah ke keranjang</span></button>')

def photo(p):
    pos = PHOTO_FOCUS.get(p['id'])
    if not pos:
        return ''
    alt = f'Ilustrasi penggunaan {p["name"]}: {p["tagline"]}'
    return (f'<figure class="pd-photo"><img alt="{e(alt)}" decoding="async" height="1000" loading="lazy" '
            f'src="/assets/img/produk/{p["id"]}.webp" style="object-position:{pos}" width="800"/></figure>')

def icon(name):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[name]}</svg>'

def card(p):
    msg = f'Halo Altora, saya tertarik dengan {p["name"]} ({p["tagline"]}).'
    if p.get('soon'):
        msg = f'Halo Altora, kabari saya saat {p["name"]} diluncurkan.'
    badge = '<span class="pd-badge pd-soon">Segera hadir</span>' if p.get('soon') else '<span class="pd-badge">Siap dipakai</span>'
    proof = f'<a class="pd-link" href="{p["proof"]}">Lihat implementasi</a>' if p.get('proof') else ''
    feats = ''.join(f'<li>{e(f)}</li>' for f in p['feats'])
    return (f'<article class="pd-card pd-{p["tone"]}{" is-soon" if p.get("soon") else ""}" id="{p["id"]}">'
            f'{photo(p)}<div class="pd-top"><span class="pd-icon">{icon(p["icon"])}</span>{badge}</div>'
            f'<h3>{e(p["name"])}</h3><p class="pd-tagline">{e(p["tagline"])}</p><p class="pd-desc">{e(p["desc"])}</p>'
            f'<ul class="pd-feats">{feats}</ul>'
            f'<div class="pd-actions"><a class="btn {"btn-outline" if p.get("soon") else "btn-purple"}" href="{WA}{quote(msg)}" rel="noopener" target="_blank">{e(p["cta"])} →</a>'
            + ('' if p.get('soon') else cart_btn(p['id'], p['name'], 'Aplikasi Altora', f"/assets/img/produk/{p['id']}.webp", 'cart-add-sm'))
            + f'{proof}</div>'
            '</article>')


from catalog_data import HW_CATS, HW_ITEMS

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

sections = []
for gid, title, lead in GROUPS:
    items = [p for p in PRODUCTS if p['group'] == gid]
    sections.append(f'<section class="pd-group" id="{gid}"><div class="pd-wrap"><div class="pd-group-head"><h2>{e(title)}</h2><p>{e(lead)}</p></div>'
                    f'<div class="pd-grid">{"".join(card(p) for p in items)}</div></div></section>')

chips = ('<a href="#software">Software</a>' + ''.join(f'<a class="pd-chip-sub" href="#{gid}">{e(t)}</a>' for gid, t, _ in GROUPS)
         + '<a href="#hardware">Hardware</a>')
hw_filters = '<button aria-pressed="true" data-filter="all" type="button">Semua</button>' + ''.join(f'<button aria-pressed="false" data-filter="{c}" type="button">{e(t)}</button>' for c, t in HW_CATS)
hardware_html = ('<section class="pd-block" id="hardware"><div class="pd-wrap"><div class="pd-block-head"><p class="eyebrow eyebrow-purple">Hardware</p>'
                 '<h2>Perangkat &amp; instalasi</h2>'
                 '<p>Kami bantu memilih tipe yang pas, lalu mengadakan, memasang, dan merawatnya. Spesifikasi perangkat principal diringkas dari katalog resminya.</p></div>'
                 '<div class="hwi-allvigi"><div><b>Katalog lengkap CCTV VIGI</b><br/><span>Semua model kamera, NVR, kit, decoder, solar, dan jaringan pendukung.</span></div><a class="btn btn-purple" href="/katalog-cctv-vigi">Lihat semua model VIGI →</a></div>'
                 f'<div aria-label="Filter kategori hardware" class="hwi-filter" role="group">{hw_filters}</div>'
                 f'<div class="hwi-grid">{"".join(hw_item(h) for h in HW_ITEMS)}</div>'
                 '<div class="hwi-more"><div class="hwi-more-logos"><img alt="TP-Link" src="/assets/img/partners/tplink-v2.png"/><img alt="Lenovo" src="/assets/img/partners/lenovo-v2.png"/><img alt="VIGI" src="/assets/img/partners/vigi-v2.png"/></div>'
                 '<div><b>Juga tersedia: jaringan TP-Link Omada dan perangkat Lenovo.</b><p>Switch PoE, access point, router 4G/5G, laptop, dan PC. Tipe kami sesuaikan dengan proyek Anda.</p></div>'
                 f'<a class="btn btn-purple" href="{WA}{quote("Halo Altora, saya ingin konsultasi perangkat CCTV/jaringan/komputer untuk proyek saya.")}" rel="noopener" target="_blank">Konsultasi perangkat →</a></div>'
                 '</div></section>')
software_head = ('<section class="pd-block pd-block-sw" id="software"><div class="pd-wrap"><div class="pd-block-head"><p class="eyebrow eyebrow-purple">Software</p>'
                 '<h2>Aplikasi siap pakai</h2><p>Bisa langsung dipakai atau disesuaikan.</p></div></div></section>')
ready = sum(1 for p in PRODUCTS if not p.get('soon'))

# ── Sorotan produk (bento) di bawah hero ──
def _feat(pid, big=False):
    p = next(x for x in PRODUCTS if x['id'] == pid)
    feats = ''.join(f'<li>{e(f)}</li>' for f in p['feats'][:3 if big else 2])
    return (f'<a class="ph-feat{" ph-big" if big else ""} pd-{p["tone"]}" href="#{p["id"]}">'
            f'<span class="ph-photo"><img alt="" loading="{"eager" if big else "lazy"}" src="/assets/img/produk/{p["id"]}.webp" style="object-position:{PHOTO_FOCUS.get(p["id"], "50% 50%")}"/></span>'
            f'<span class="ph-body"><span class="ph-kicker">{e(p["tagline"])}</span><b>{e(p["name"])}</b>'
            f'<span class="ph-desc">{e(p["desc"])}</span><ul>{feats}</ul><span class="ph-more">Lihat detail →</span></span></a>')

HW_HL = [
    ('/katalog-cctv-vigi', '/assets/img/vigi/s385dps.webp', 'CCTV VIGI', '148 model kamera, NVR & solar', 'Katalog lengkap'),
    ('#starlink-v5', '/assets/img/hardware/starlink-v5.webp', 'Starlink', 'V5, Mini, Enterprise, Performance', 'Kit + instalasi'),
    ('#telt-fmc920', '/assets/img/hardware/telt-fmc920.webp', 'GPS Teltonika', 'Tracker, kamera & sensor armada', 'Telematika'),
    ('#smartlock', '/assets/img/hardware/smartlock.webp', 'Smartlock', 'Akses pintu via app, kartu, wajah', 'Kontrol akses'),
    ('#kios-k', '/assets/img/hardware/kios-k.webp', 'Kios & signage', 'Layanan mandiri & layar promosi', 'Smart display'),
    ('#hde-ifp', '/assets/img/hardware/hde-ifp.webp', 'Display HDe', 'Videotron & interactive panel', 'Ruang rapat'),
]
hw_tiles = ''.join(f'<a class="ph-hw" href="{u}"><span class="ph-hw-pic"><img alt="" loading="lazy" src="{img}"/></span>'
                   f'<span class="ph-hw-tag">{e(tag)}</span><b>{e(t)}</b><small>{e(sub)}</small></a>' for u, img, t, sub, tag in HW_HL)
n_vigi = 148
highlight_html = ('<section class="ph-wrap" aria-label="Produk unggulan"><div class="pd-wrap">'
                  '<div class="ph-head"><p class="eyebrow eyebrow-purple">Produk unggulan</p><h2>Paling banyak dipakai klien kami</h2></div>'
                  f'<div class="ph-bento">{_feat("vision", True)}{_feat("fms")}{_feat("teams")}</div>'
                  f'<div class="ph-stats"><div><b>{ready}</b><span>aplikasi siap pakai</span></div><div><b>148</b><span>model CCTV VIGI</span></div>'
                  '<div><b>7</b><span>kit Starlink</span></div><div><b>6</b><span>principal resmi</span></div></div>'
                  '<div class="ph-head ph-head-hw"><p class="eyebrow eyebrow-purple">Perangkat pilihan</p><h2>Hardware yang kami adakan dan pasang</h2></div>'
                  f'<div class="ph-hws">{hw_tiles}</div>'
                  '</div></section>')

ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Produk Altora Indonesia',
      'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                           'item': {'@type': 'SoftwareApplication', 'name': p['name'], 'description': p['desc'],
                                    'applicationCategory': 'BusinessApplication', 'url': f'https://altora.id/produk#{p["id"]}',
                                    'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': 'https://altora.id/'}}}
                          for i, p in enumerate(PRODUCTS)]}

title = 'Produk Altora | Aplikasi, CCTV VIGI, Smartlock & Starlink'
desc = ('Aplikasi Altora untuk HRIS, AI CCTV, armada & private AI, plus kamera VIGI, smartlock, signage, kios, Starlink, dan perangkat Teltonika, HDe, HaganeRack.')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title><meta content="{e(desc)}" name="description"/><link href="https://altora.id/produk" rel="canonical"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="https://altora.id/produk" property="og:url"/><meta content="https://altora.id/assets/img/produk/vision.webp" property="og:image"/><link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v=20261014i"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header class="company-nav"><a class="project-brand" href="/"><img alt="Altora" src="/assets/img/altora-logo-icon-v2.svg"/><span>Altora</span></a></header>
<main class="pd-page">
<section class="pd-hero"><div class="pd-wrap">
<p class="eyebrow eyebrow-purple">Produk Altora</p>
<h1>Aplikasi dan perangkat untuk bisnis dan instansi.</h1>
<p class="pd-lead">{ready} aplikasi siap pakai, mulai dari absensi dan CCTV pintar sampai pemantauan armada. Ditambah perangkat dari principal resmi seperti VIGI, Teltonika, HDe, dan HaganeRack.</p>
<p class="pd-note">Foto produk adalah ilustrasi.</p>
<nav aria-label="Kategori produk" class="pd-chips">{chips}</nav>
</div></section>
{highlight_html}
{software_head}{"".join(sections)}
{hardware_html}
<section class="pd-compare"><div class="pd-wrap pd-compare-grid">
<div class="pd-compare-card"><p class="pd-kicker">Produk siap pakai</p><h3>Cocok kalau kebutuhan Anda umum dan ingin cepat jalan.</h3><ul><li>Lebih cepat dipasang</li><li>Fitur utama sudah dipakai klien lain</li><li>Bisa dihubungkan ke perangkat yang ada</li></ul></div>
<div class="pd-compare-card pd-compare-alt"><p class="pd-kicker">Software custom</p><h3>Cocok kalau proses Anda berbeda dari kebanyakan.</h3><ul><li>Dibuat mengikuti proses Anda</li><li>Bisa terhubung ke sistem lama</li><li>Bisa mulai dari produk, lalu dikembangkan</li></ul><a class="pd-link" href="/services/software-custom">Pelajari software custom</a></div>
</div></section>
<section class="pd-cta"><div class="pd-wrap pd-cta-inner"><div><h2>Belum yakin produk mana yang pas?</h2><p>Ceritakan kebutuhan Anda, kami bantu pilihkan.</p></div><a class="btn btn-purple" href="/contact">Konsultasi gratis</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="/assets/js/hw-filter.js?v=20261011"></script></body></html>
'''
(root / 'produk.html').write_text(page, encoding='utf-8')
print('produk.html dibuat:', len(PRODUCTS), 'produk')

# ── Grid produk ringkas di beranda (index.html, di antara penanda produk-ringkas) ──
def home_card(p):
    soon = '<span class="hp-soon">Segera hadir</span>' if p.get('soon') else ''
    pos = PHOTO_FOCUS.get(p['id'], '50% 50%')
    return (f'<a class="hp-card" href="/produk#{p["id"]}"><span class="hp-pic"><img alt="" loading="lazy" '
            f'src="/assets/img/produk/{p["id"]}.webp" style="object-position:{pos}"/>{soon}</span>'
            f'<b>{e(p["name"])}</b><small>{e(p["tagline"])}</small></a>')

cards = ''.join(home_card(p) for p in PRODUCTS)
dup = cards.replace('<a class="hp-card"', '<a aria-hidden="true" class="hp-card" tabindex="-1"')
home_grid = ('<!-- produk-ringkas:start --><div aria-label="Produk Altora" class="hp-marquee">'
             f'<div class="hp-marquee-track">{cards}{dup}</div></div>'
             '<div class="hp-actions"><a class="btn btn-purple" href="/produk">Produk kami</a>'
             '<span>Termasuk perangkat VIGI, Teltonika, HDe, HaganeRack, dan Fasser.</span></div><!-- produk-ringkas:end -->')
idx = root / 'index.html'
s = idx.read_text(encoding='utf-8')
s = re.sub(r'<!-- produk-ringkas:start -->.*?<!-- produk-ringkas:end -->', lambda _: home_grid, s, count=1, flags=re.S)
idx.write_text(s, encoding='utf-8')
print('beranda: grid produk ringkas diperbarui')
