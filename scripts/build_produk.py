"""Bangun produk.html dari data PRODUCTS di bawah.
Jalankan dari root repo:  python3 scripts/build_produk.py && python3 scripts/apply_shell.py"""
import html, json, pathlib
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
}

GROUPS = [
    ('sdm', 'SDM & kehadiran', 'Kelola tim, jadwal, dan absensi tanpa rekap manual.'),
    ('aman', 'Keamanan & akses', 'Pantau area dan kendalikan akses dari infrastruktur yang sudah ada.'),
    ('lapangan', 'Armada, lahan & lapangan', 'Lihat kondisi kendaraan, lahan, sensor, dan lokasi dalam satu tampilan.'),
    ('segera', 'Segera hadir', 'Sedang disiapkan untuk retail, F&B, dan operasional multi-cabang.'),
]

PRODUCTS = [
    dict(id='teams', group='sdm', icon='users', tone='purple', name='Altora Teams', tagline='HRIS & People Operations',
         desc='Sistem kelola SDM: absensi GPS & selfie, shift kerja, pengajuan cuti/izin, reimbursement, dan payroll otomatis.',
         feats=['Absensi GPS & validasi', 'Shift & schedule builder', 'Cuti, izin & reimbursement', 'Payroll & portal karyawan'],
         cta='Coba Altora Teams', proof='/portfolio/altora-teams'),
    dict(id='attendance', group='sdm', icon='face', tone='pink', name='Altora Smart Attendance', tagline='Face recognition dari CCTV',
         desc='Absensi otomatis berbasis AI yang mengenali wajah dari kamera CCTV—tanpa antre di mesin absensi atau menempelkan kartu.',
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
    'sense': '62% 58%', 'farming': '62% 58%', 'command': '60% 62%', 'pos': '50% 58%', 'erp': '62% 58%',
}

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
            f'<div class="pd-actions"><a class="btn {"btn-outline" if p.get("soon") else "btn-purple"}" href="{WA}{quote(msg)}" rel="noopener" target="_blank">{e(p["cta"])} →</a>{proof}</div>'
            '</article>')

sections = []
for gid, title, lead in GROUPS:
    items = [p for p in PRODUCTS if p['group'] == gid]
    sections.append(f'<section class="pd-group" id="{gid}"><div class="pd-wrap"><div class="pd-group-head"><h2>{e(title)}</h2><p>{e(lead)}</p></div>'
                    f'<div class="pd-grid">{"".join(card(p) for p in items)}</div></div></section>')

chips = ''.join(f'<a href="#{gid}">{e(t)}</a>' for gid, t, _ in GROUPS)
ready = sum(1 for p in PRODUCTS if not p.get('soon'))

ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Produk Altora Indonesia',
      'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                           'item': {'@type': 'SoftwareApplication', 'name': p['name'], 'description': p['desc'],
                                    'applicationCategory': 'BusinessApplication', 'url': f'https://altora.id/produk#{p["id"]}',
                                    'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': 'https://altora.id/'}}}
                          for i, p in enumerate(PRODUCTS)]}

title = 'Produk Altora | HRIS, AI CCTV, Smart Access & Fleet Management'
desc = ('Produk siap pakai dari Altora Indonesia: Altora Teams (HRIS), Vision (AI CCTV), Pass (smart access), '
        'FMS (fleet management), Smart Attendance, Sense (IoT), dan Command Center.')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title><meta content="{e(desc)}" name="description"/><link href="https://altora.id/produk" rel="canonical"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="https://altora.id/produk" property="og:url"/><meta content="https://altora.id/assets/img/produk/vision.webp" property="og:image"/><link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v=20261011a"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header class="company-nav"><a class="project-brand" href="/"><img alt="Altora" src="/assets/img/altora-logo-icon-v2.svg"/><span>Altora</span></a></header>
<main class="pd-page">
<section class="pd-hero"><div class="pd-wrap">
<p class="eyebrow eyebrow-purple">Produk Altora</p>
<h1>Produk siap pakai untuk operasional yang perlu berjalan hari ini.</h1>
<p class="pd-lead">{ready} produk yang sudah dipakai di lapangan—dari HRIS dan absensi wajah sampai AI CCTV, smart access, dan fleet management. Bisa dipakai apa adanya atau disesuaikan dengan alur kerja Anda.</p>
<p class="pd-note">Foto produk adalah ilustrasi penggunaan aplikasi Altora.</p>
<nav aria-label="Kategori produk" class="pd-chips">{chips}</nav>
</div></section>
{"".join(sections)}
<section class="pd-compare"><div class="pd-wrap pd-compare-grid">
<div class="pd-compare-card"><p class="pd-kicker">Produk siap pakai</p><h3>Cocok jika kebutuhan Anda umum dan perlu cepat jalan.</h3><ul><li>Implementasi lebih cepat</li><li>Fitur inti sudah teruji di lapangan</li><li>Bisa dihubungkan ke perangkat yang sudah ada</li></ul></div>
<div class="pd-compare-card pd-compare-alt"><p class="pd-kicker">Software custom</p><h3>Cocok jika alur kerja Anda tidak muat di template.</h3><ul><li>Dibangun dari proses kerja nyata</li><li>Integrasi dengan sistem dan data lama</li><li>Bisa dimulai dari produk lalu dikembangkan</li></ul><a class="pd-link" href="/services/software-custom">Pelajari software custom</a></div>
</div></section>
<section class="pd-cta"><div class="pd-wrap pd-cta-inner"><div><h2>Belum yakin produk mana yang pas?</h2><p>Ceritakan kondisinya. Kami bantu memilih produk, kombinasi, atau pendekatan custom yang paling proporsional.</p></div><a class="btn btn-purple" href="/contact">Konsultasi kebutuhan →</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''
(root / 'produk.html').write_text(page, encoding='utf-8')
print('produk.html dibuat:', len(PRODUCTS), 'produk')
