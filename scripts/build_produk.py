"""Bangun produk.html dari data PRODUCTS di bawah.
Jalankan dari root repo:  python3 scripts/build_produk.py && python3 scripts/apply_shell.py"""
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

GROUPS = [
    ('sdm', 'SDM & absensi', 'Absensi, jadwal, dan gaji tanpa rekap manual.'),
    ('aman', 'Keamanan & akses', 'CCTV pintar dan akses pintu digital.'),
    ('lapangan', 'Armada, lahan & sensor', 'Pantau kendaraan, lahan, dan sensor dari satu layar.'),
    ('data', 'Data & AI', 'AI dan pemetaan yang berjalan di server Anda sendiri.'),
    ('jualan', 'Jualan online', 'Website toko dan penjualan tiket milik usaha Anda sendiri.'),
    ('kerja', 'Kerja & kolaborasi privat', 'Dokumen, spreadsheet, dan rapat online di server Anda sendiri.'),
    ('bisnis', 'Toko & operasional bisnis', 'Diterapkan mengikuti proses usaha Anda, bisa mulai dari satu modul.'),
]

PRODUCTS = [
    dict(id='teams', group='sdm', icon='users', tone='purple', name='Altora Teams', tagline='HRIS & People Operations',
         desc='Sistem kelola SDM: absensi GPS & selfie, shift kerja, pengajuan cuti/izin, reimbursement, dan payroll otomatis.',
         feats=['Absensi GPS & validasi', 'Shift & schedule builder', 'Cuti, izin & reimbursement', 'Payroll & portal karyawan'],
         cta='Coba Altora Teams', proof='/portfolio/altora-teams'),
    dict(id='projek', group='sdm', icon='layers', tone='blue', name='Altora Projek', tagline='Manajemen proyek & tugas',
         desc='Proyek, tugas, tenggat, dan progres tim dalam satu tempat: papan kanban, kalender, timeline, dan laporan.',
         feats=['Tugas & penanggung jawab', 'Papan, daftar & kalender', 'Timeline & sprint', 'Laporan progres'],
         cta='Minta demo Altora Projek'),
    dict(id='office', group='kerja', icon='doc', tone='purple', name='Altora Office', tagline='Paket kerja kantor di server sendiri',
         desc='Word, Sheets, Docs, dan Meet dalam satu paket, berjalan di server atau cloud milik organisasi Anda.',
         feats=['Dokumen, spreadsheet & rapat', 'Satu akun untuk semua', 'Di server Anda sendiri', 'Bisa mulai dari satu divisi'],
         cta='Minta demo Altora Office'),
    dict(id='ticket', group='jualan', icon='signage', tone='purple', name='Altora Ticket', tagline='Website jual tiket acara',
         desc='Jual tiket acara dari website sendiri: kuota per jenis tiket, bukti transfer, tiket QR, dan check-in di pintu masuk.',
         feats=['Halaman acara & kuota tiket', 'Bukti transfer & persetujuan', 'Tiket QR per peserta', 'Check-in dari HP'],
         cta='Minta demo Altora Ticket'),
    dict(id='catalog', group='jualan', icon='cart', tone='blue', name='Altora Catalog', tagline='Website toko online siap pakai',
         desc='Toko online milik usaha sendiri: produk, varian, stok, keranjang, pembayaran transfer, pengiriman, dan nomor resi.',
         feats=['Katalog, varian & stok', 'Keranjang & transfer', 'Kirim atau ambil sendiri', 'Admin & laporan pesanan'],
         cta='Minta demo Altora Catalog'),
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
    dict(id='word', group='kerja', icon='doc', tone='blue', name='Altora Word', tagline='Pengolah dokumen privat',
         desc='Menulis dan menyunting dokumen Word di browser, tersimpan di server atau cloud milik organisasi Anda sendiri.',
         feats=['Buka & simpan .docx', 'Komentar & revisi', 'Template surat & laporan', 'Di server Anda sendiri'],
         cta='Minta demo Altora Word'),
    dict(id='docs', group='kerja', icon='folder', tone='purple', name='Altora Docs', tagline='Penyimpanan & berbagi dokumen privat',
         desc='Simpan, cari, dan bagikan dokumen dengan hak akses per orang dan per folder, di server Anda sendiri.',
         feats=['Folder & pencarian', 'Hak akses per folder', 'Riwayat versi', 'Di server Anda sendiri'],
         cta='Minta demo Altora Docs'),
    dict(id='sheets', group='kerja', icon='grid', tone='green', name='Altora Sheets', tagline='Spreadsheet privat',
         desc='Spreadsheet untuk rekap dan laporan yang bisa disunting bersama, dengan data tetap di server Anda.',
         feats=['Buka & simpan .xlsx', 'Rumus & grafik', 'Edit bersama', 'Di server Anda sendiri'],
         cta='Minta demo Altora Sheets'),
    dict(id='meet', group='kerja', icon='video', tone='pink', name='Altora Meet', tagline='Rapat video privat',
         desc='Rapat video antar kantor dan tim lapangan, termasuk rekamannya, berjalan di server Anda sendiri.',
         feats=['Ruang rapat & tamu', 'Berbagi layar & chat', 'Rekaman di server Anda', 'Dari browser & HP'],
         cta='Minta demo Altora Meet'),
    dict(id='pos', group='bisnis', icon='cart', tone='orange', name='Altora POS', tagline='Point of Sale & Kasir', status='custom',
         desc='Kasir modern untuk retail & F&B: pencatatan pesanan cepat, stok toko real-time, integrasi QRIS, dan laporan penjualan.',
         feats=['Kasir cepat retail & F&B', 'Stok & varian produk', 'Integrasi QRIS / EDC', 'Multi-cabang & laporan penjualan'],
         cta='Diskusikan kebutuhan kasir'),
    dict(id='erp', group='bisnis', icon='layers', tone='blue', name='Altora ERP', tagline='Enterprise Resource Planning', status='custom',
         desc='Sistem operasional terpadu: stok multi-gudang, purchasing, laporan keuangan, dan dashboard eksekutif multi-cabang.',
         feats=['Stok multi-gudang & transfer', 'Purchasing & portal supplier', 'Laporan keuangan & akuntansi', 'Dashboard operasional eksekutif'],
         cta='Diskusikan kebutuhan ERP'),
]

e = lambda t: html.escape(t, quote=True)

# Ilustrasi per produk (assets/img/produk/<id>.webp, 800x1000 portrait).
# Nilai = object-position agar potongan 4:3 tetap fokus ke layar perangkat.
PHOTO_FOCUS = {
    # Ilustrasi dari scripts/build_produk_img.py dan tangkapan layar Ticket/Catalog: fokus ke jendela aplikasi.
    **{k: '50% 45%' for k in ('teams', 'attendance', 'vision', 'pass', 'fms', 'sense', 'farming', 'command', 'pos', 'erp', 'private-ai',
                             'projek', 'office', 'word', 'docs', 'sheets', 'meet')},
    'ticket': '50% 40%', 'catalog': '50% 40%',
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
    badge = ('<span class="pd-badge pd-soon">Segera hadir</span>' if p.get('soon') else '<span class="pd-badge pd-custom">Implementasi custom</span>' if p.get('status') == 'custom'
             else '<span class="pd-badge">Siap dipakai</span>')
    proof = f'<a class="pd-link" href="/produk/{p["id"]}">Detail produk →</a>'
    feats = ''.join(f'<li>{e(f)}</li>' for f in p['feats'])
    return (f'<article class="pd-card pd-{p["tone"]}{" is-soon" if p.get("soon") else ""}" id="{p["id"]}">'
            f'{photo(p)}<div class="pd-top"><span class="pd-icon">{icon(p["icon"])}</span>{badge}</div>'
            f'<h3><a class="pd-title-link" href="/produk/{p["id"]}">{e(p["name"])}</a></h3><p class="pd-tagline">{e(p["tagline"])}</p><p class="pd-desc">{e(p["desc"])}</p>'
            f'<ul class="pd-feats">{feats}</ul>'
            f'<div class="pd-actions"><a class="btn {"btn-outline" if p.get("soon") else "btn-purple"}" href="{WA}{quote(msg)}" rel="noopener" target="_blank">{e(p["cta"])} →</a>'
            + ('' if p.get('soon') else cart_btn(p['id'], p['name'], 'Aplikasi Altora', f"/assets/img/produk/{p['id']}.webp", 'cart-add-sm'))
            + f'{proof}</div>'
            '</article>')


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
                 '<div><b>Juga tersedia: jaringan TP-Link Omada dan model Lenovo lainnya.</b><p>Switch PoE, access point, router 4G/5G, serta laptop, PC, dan server dengan spesifikasi sesuai kebutuhan proyek Anda.</p></div>'
                 f'<a class="btn btn-purple" href="{WA}{quote("Halo Altora, saya ingin konsultasi perangkat CCTV/jaringan/komputer untuk proyek saya.")}" rel="noopener" target="_blank">Konsultasi perangkat →</a></div>'
                 '</div></section>')
software_head = ('<section class="pd-block pd-block-sw" id="software"><div class="pd-wrap"><div class="pd-block-head"><p class="eyebrow eyebrow-purple">Software</p>'
                 '<h2>Aplikasi siap pakai</h2><p>Bisa langsung dipakai atau disesuaikan.</p></div></div></section>')
ready = sum(1 for p in PRODUCTS if not p.get('soon'))


# ── Pencari solusi (3 pertanyaan) ──
FINDER_NEEDS = {
    'cctv': ('Keamanan & CCTV', [('/katalog-cctv-vigi', 'Katalog CCTV VIGI', '148 model kamera, NVR & solar'), ('/produk/vision', 'Altora Vision', 'AI deteksi APD & zona terlarang'), ('/cctv-tenaga-surya-{c}', 'CCTV tenaga surya & 4G', 'Untuk lokasi tanpa listrik')]),
    'absensi': ('Absensi & SDM', [('/produk/attendance', 'Altora Smart Attendance', 'Absensi wajah dari CCTV'), ('/produk/teams', 'Altora Teams', 'HRIS, cuti, lembur, payroll'), ('/absensi-face-recognition-{c}', 'Absensi wajah di kota Anda', 'Survei & pemasangan')]),
    'armada': ('Armada & kendaraan', [('/produk/fms', 'Altora FMS', 'GPS, BBM, CAN-Bus, TPMS'), ('/katalog#telt-fmc920', 'GPS tracker Teltonika', 'Perangkat telematika'), ('/gps-tracker-kendaraan-{c}', 'Pasang GPS tracker', 'Teknisi lokal')]),
    'internet': ('Internet di lokasi terpencil', [('/jual-starlink-{c}', 'Starlink + instalasi', 'V5, Mini, Enterprise, Performance'), ('/services/starlink-internet-satelit', 'Paket off-grid tenaga surya', 'Panel, baterai, Wi-Fi repeater'), ('/jasa-instalasi-jaringan-{c}', 'Jaringan & wireless bridge', 'Antar gedung & site')]),
    'akses': ('Akses pintu & gedung', [('/produk/pass', 'Altora Pass', 'Hak akses & riwayat'), ('/jual-smartlock-{c}', 'Smartlock & EM lock', 'Survei dan pasang'), ('/produk/attendance', 'Absensi + akses', 'Wajah membuka pintu')]),
    'layanan': ('Layanan publik & antrean', [('/mesin-kiosk-{c}', 'Kios layanan mandiri', 'Antrean & cetak dokumen'), ('/videotron-{c}', 'Videotron & signage', 'Informasi publik'), ('/industri/pemerintahan', 'Solusi pemerintahan', 'GIS, kios, CCTV kota')]),
    'display': ('Display & ruang rapat', [('/interactive-flat-panel-{c}', 'Interactive flat panel', 'Kelas & ruang rapat'), ('/videotron-{c}', 'Videotron indoor/outdoor', 'Aula, lobi, panggung'), ('/katalog#hde-mrs', 'Meeting recording system', 'Rekam rapat')]),
    'data': ('Data, peta & AI', [('/produk/private-ai', 'Altora Private AI & GIS', 'AI on-premise & peta wilayah'), ('/produk/command', 'Altora Command', 'Ruang kendali terpadu'), ('/services/software-custom', 'Software custom', 'Dashboard & integrasi')]),
    'kerja': ('Dokumen, rapat & proyek', [('/produk/office', 'Altora Office', 'Word, Sheets, Docs, Meet'), ('/produk/projek', 'Altora Projek', 'Tugas & progres proyek'), ('/produk/meet', 'Altora Meet', 'Rapat video privat')]),
    'jualan': ('Jualan online & tiket acara', [('/produk/catalog', 'Altora Catalog', 'Toko online milik sendiri'), ('/produk/ticket', 'Altora Ticket', 'Jual tiket & check-in QR'), ('/produk/pos', 'Altora POS', 'Kasir toko & F&B')]),
    'bisnis': ('Kasir, stok & keuangan', [('/produk/pos', 'Altora POS', 'Kasir retail & F&B'), ('/produk/erp', 'Altora ERP', 'Stok, pembelian, keuangan'), ('/jasa-pembuatan-aplikasi-{c}', 'Aplikasi custom', 'Sesuai proses Anda')]),
    'infra': ('Jaringan, server & IT', [('/it-support-{c}', 'IT support', 'Komputer, jaringan, server'), ('/rak-server-{c}', 'Rak server & data center', 'HaganeRack'), ('/alat-fiber-optik-{c}', 'Fiber optik', 'Splicing & alat ukur')]),
}
FINDER_IND = [('pertambangan', 'Tambang & industri berat'), ('pemerintahan', 'Pemerintahan & layanan publik'), ('pendidikan', 'Kampus & sekolah'), ('korporasi', 'Korporasi & dunia usaha')]
finder_data = json.dumps({k: v[1] for k, v in FINDER_NEEDS.items()}, ensure_ascii=False)
finder_html = ('<section class="fd-sec" id="cari-solusi"><div class="pd-wrap"><div class="fd-box">'
               '<div class="fd-head"><p class="eyebrow eyebrow-purple">Cari solusi</p><h2>Bingung mulai dari mana? Jawab 3 pertanyaan.</h2></div>'
               '<form class="fd-form" onsubmit="return false">'
               '<label>Sektor Anda<select name="ind">' + ''.join(f'<option value="{k}">{e(t)}</option>' for k, t in FINDER_IND) + '</select></label>'
               '<label>Yang paling dibutuhkan<select name="need">' + ''.join(f'<option value="{k}">{e(v[0])}</option>' for k, v in FINDER_NEEDS.items()) + '</select></label>'
               '<label>Lokasi<select name="city"><option value="samarinda">Samarinda</option><option value="balikpapan">Balikpapan</option><option value="samarinda">Kota lain di Kaltim</option></select></label>'
               '</form><div aria-live="polite" class="fd-result"></div>'
               f'<script type="application/json" id="fd-data">{finder_data}</script></div></div></section>')

# ── Sorotan produk (bento) di bawah hero ──
def _feat(pid, big=False):
    p = next(x for x in PRODUCTS if x['id'] == pid)
    feats = ''.join(f'<li>{e(f)}</li>' for f in p['feats'][:3 if big else 2])
    return (f'<a class="ph-feat{" ph-big" if big else ""} pd-{p["tone"]}" href="/produk/{p["id"]}">'
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

from build_apps import APPS

def head(title, desc, url, ld, extra_css=''):
    return (f'<!DOCTYPE html>\n<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title>'
            f'<meta content="{e(desc)}" name="description"/><link href="https://altora.id{url}" rel="canonical"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/>'
            f'<meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="https://altora.id{url}" property="og:url"/>'
            '<meta content="https://altora.id/assets/img/produk/vision.webp" property="og:image"/><link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/>'
            '<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>'
            '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>'
            '<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>'
            '<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>'
            f'<link rel="stylesheet" href="/assets/css/unify.css?v=20261019-katalog2"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>'
            '<body class="company-page"><header class="company-nav"></header>\n')

# ── /produk: halaman pengetahuan ──
KN_GROUPS = [('Keamanan & akses', ['vision', 'attendance', 'pass']), ('SDM, proyek & operasional', ['teams', 'projek', 'pos', 'erp']),
             ('Armada, lahan & sensor', ['fms', 'sense', 'farming']), ('Pusat kendali & data', ['command', 'private-ai']),
             ('Jualan online', ['ticket', 'catalog']),
             ('Kerja & kolaborasi privat', ['office', 'word', 'docs', 'sheets', 'meet'])]

def kn_app(k):
    a = APPS[k]
    st = '<span class="kn-st">Siap dipakai</span>' if a['status'] == 'ready' else '<span class="kn-st kn-custom">Implementasi custom</span>'
    return (f'<a class="kn-app" href="/produk/{k}"><span class="kn-pic"><img alt="" loading="lazy" src="/assets/img/produk/{k}.webp"/></span>'
            f'<span class="kn-body"><span class="kn-top"><small>{e(a["tag"])}</small>{st}</span><b>{e(a["name"])}</b>'
            f'<span class="kn-what">{e(a["lead"])}</span><span class="kn-solve"><em>Menyelesaikan:</em> {e(a["pains"][0])}</span>'
            f'<span class="kn-more">Pelajari {e(a["name"])} →</span></span></a>')

HW_KNOW = [
    ('cctv', 'CCTV VIGI', '/assets/img/vigi/s385dps.webp', 'Kamera, perekam (NVR), dan tenaga surya. Dasar untuk keamanan dan Altora Vision.', 'Dome, bullet, turret, pan tilt, 4G, NVR, solar', '/katalog-cctv-vigi'),
    ('gps', 'GPS & telematika', '/assets/img/hardware/telt-fmc920.webp', 'Perangkat Teltonika di kendaraan yang mengirim posisi dan data mesin ke Altora FMS.', 'Tracker, sensor BBM, TPMS, kamera ADAS', '/katalog#cat-gps'),
    ('konek', 'Starlink', '/assets/img/hardware/starlink-v5.webp', 'Internet satelit agar site terpencil tetap terhubung untuk CCTV, GPS, dan aplikasi.', 'V5, Mini, Enterprise, Performance', '/katalog#cat-konek'),
    ('akses', 'Smartlock & akses', '/assets/img/hardware/smartlock.webp', 'Kunci pintu digital yang dikelola Altora Pass, bisa terhubung ke absensi.', 'Smart handle, EM lock, doorcam', '/katalog#cat-akses'),
    ('kios', 'Kios & signage', '/assets/img/hardware/kios-k.webp', 'Layanan mandiri dan layar informasi untuk instansi, kampus, dan retail.', 'Kios-K, digital signboard', '/katalog#cat-kios'),
    ('display', 'Display & ruang rapat', '/assets/img/hardware/hde-ifp.webp', 'Videotron, interactive flat panel, dan sistem rekam rapat untuk kelas dan kantor.', 'Videotron, IFP, meeting recording', '/katalog#cat-display'),
    ('rack', 'Rak & data center', '/assets/img/hardware/hr-close-glass.webp', 'Rumah untuk server dan perangkat jaringan, termasuk server Private AI.', 'Close rack, wallmount, cooling', '/katalog#cat-rack'),
    ('fiber', 'Fiber optik', '/assets/img/hardware/fas-fusion-splicer.webp', 'Alat sambung dan ukur untuk jaringan fiber kampus, gedung, dan ISP.', 'OTDR, fusion splicer, power meter', '/katalog#cat-fiber'),
    ('laptop', 'Laptop, PC, tablet & server', '/assets/img/hardware/lenovo-thinkpad-t14.webp', 'Lenovo ThinkPad, ThinkCentre AIO, Tab, hingga server ThinkSystem untuk kantor dan instansi.', 'Laptop, AIO, tablet, server, workstation', '/katalog#cat-laptop'),
]
hw_know = ''.join(f'<a class="kn-hw" href="{u}"><span class="kn-hw-pic"><img alt="" loading="lazy" src="{img}"/></span><b>{e(t)}</b><span>{e(d)}</span><small>{e(ex)}</small><em>Lihat di katalog →</em></a>'
                  for _, t, img, d, ex, u in HW_KNOW)
kn_groups = ''.join(f'<div class="kn-group"><h3>{e(g)}</h3><div class="kn-apps">{"".join(kn_app(k) for k in ks)}</div></div>' for g, ks in KN_GROUPS)
flow = ('<div class="kn-flow">'
        '<div class="kn-step"><span>1</span><b>Perangkat di lapangan</b><p>Kamera, GPS tracker, sensor, smartlock, dan kios menangkap kejadian nyata.</p></div>'
        '<div class="kn-arrow" aria-hidden="true"></div>'
        '<div class="kn-step"><span>2</span><b>Aplikasi Altora</b><p>Data diolah: AI mengenali pelanggaran, absensi tercatat, armada terlacak.</p></div>'
        '<div class="kn-arrow" aria-hidden="true"></div>'
        '<div class="kn-step"><span>3</span><b>Dashboard & keputusan</b><p>Pimpinan melihat ringkasan, tim menerima alert, laporan terkirim otomatis.</p></div></div>')
ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Produk Altora Indonesia',
      'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'https://altora.id/produk/{k}', 'name': a['name']} for i, (k, a) in enumerate(APPS.items())]}
produk_page = head('Produk Altora | Kenali Aplikasi & Perangkat Kami', 'Kenali produk Altora: aplikasi AI CCTV, HRIS, absensi wajah, fleet management, dan smart access, plus perangkat CCTV, GPS, Starlink, hingga data center.', '/produk', ld) + f"""<main class="pd-page kn-page">
<section class="pd-hero kn-hero"><div class="pd-wrap">
<p class="eyebrow eyebrow-purple">Produk Altora</p>
<h1>Kenali produk kami: dari perangkat di lapangan sampai keputusan di dashboard.</h1>
<p class="pd-lead">Altora menggabungkan aplikasi dan perangkat yang saling terhubung. Ambil satu produk untuk mulai, atau rangkai beberapa menjadi satu sistem.</p>
<div class="kn-hero-actions"><a class="btn btn-purple" href="/katalog">Buka katalog</a><a class="pd-link" href="#cari-solusi">Cari solusi untuk saya</a></div>
{flow}
</div></section>
{finder_html}
<section class="kn-sec" id="aplikasi"><div class="pd-wrap"><div class="kn-head"><p class="eyebrow eyebrow-purple">Aplikasi</p><h2>Aplikasi Altora dan masalah yang diselesaikannya</h2>
<p>Setiap aplikasi bisa dipakai sendiri, atau digabung. Klik untuk melihat fitur, tampilan, dan cara mulai.</p></div>{kn_groups}</div></section>
<section class="kn-sec kn-sec-alt" id="perangkat"><div class="pd-wrap"><div class="kn-head"><p class="eyebrow eyebrow-purple">Perangkat</p><h2>Perangkat yang kami adakan, pasang, dan rawat</h2>
<p>Dari principal resmi. Kami pilihkan tipe yang cocok dengan lokasi Anda, lalu pastikan terhubung dengan aplikasinya.</p></div><div class="kn-hws">{hw_know}</div></div></section>
<section class="pd-compare"><div class="pd-wrap pd-compare-grid">
<div class="pd-compare-card"><p class="pd-kicker">Produk siap pakai</p><h3>Cocok kalau kebutuhan Anda umum dan ingin cepat jalan.</h3><ul><li>Lebih cepat dipasang</li><li>Fitur utama sudah dipakai klien lain</li><li>Bisa dihubungkan ke perangkat yang ada</li></ul></div>
<div class="pd-compare-card pd-compare-alt"><p class="pd-kicker">Software custom</p><h3>Cocok kalau proses Anda berbeda dari kebanyakan.</h3><ul><li>Dibuat mengikuti proses Anda</li><li>Bisa terhubung ke sistem lama</li><li>Bisa mulai dari produk, lalu dikembangkan</li></ul><a class="pd-link" href="/services/software-custom">Pelajari software custom</a></div>
</div></section>
<section class="pd-cta"><div class="pd-wrap pd-cta-inner"><div><h2>Sudah tahu yang dibutuhkan?</h2><p>Pilih produk di katalog, masukkan ke keranjang, lalu kirim lewat WhatsApp.</p></div><a class="btn btn-purple" href="/katalog">Buka katalog</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="/assets/js/finder.js?v=20261014"></script></body></html>
"""
(root / 'produk.html').write_text(produk_page, encoding='utf-8')

# ── /katalog: katalog belanja (aplikasi + perangkat, filter, keranjang, cetak) ──
def kat_app(k):
    a = APPS[k]
    msg = f'Halo Altora, saya tertarik dengan {a["name"]}.'
    return (f'<article class="hwi" data-cat="app" id="{k}"><div class="hwi-pic hwi-pic-photo"><img alt="{e(a["name"])}" loading="lazy" src="/assets/img/produk/{k}.webp" style="object-position:50% 52%"/></div>'
            f'<div class="hwi-body"><small>Aplikasi Altora</small><h3>{e(a["name"])}</h3><p>{e(a["tag"])}</p>'
            '<div class="hwi-list"><b>Fitur utama</b><ul>' + ''.join(f'<li>{e(t)}</li>' for t, _ in a['feats'][:3]) + '</ul></div>'
            f'<div class="pd-actions">{cart_btn(k, a["name"], "Aplikasi Altora", f"/assets/img/produk/{k}.webp")}'
            f'<a class="pd-link" href="/produk/{k}">Detail aplikasi</a></div></div></article>')

def kat_jasa(j):
    jid, name, desc, inc, img, link = j
    return (f'<article class="hwi" data-cat="jasa" id="{jid}"><div class="hwi-pic hwi-pic-photo"><img alt="{e(name)}" loading="lazy" src="{img}"/></div>'
            f'<div class="hwi-body"><small>Jasa</small><h3>{e(name)}</h3><p>{e(desc)}</p>'
            '<div class="hwi-list"><b>Termasuk</b><ul>' + ''.join(f'<li>{e(x)}</li>' for x in inc) + '</ul></div>'
            f'<div class="pd-actions">{cart_btn(jid, name, "Jasa Altora", img)}<a class="pd-link" href="{link}">Detail jasa</a></div></div></article>')

# Pilihan "Cari apa?": tiap pilihan = kategori barang + id jasa/software yang relevan
VIEWS = [
    ('cctv', 'CCTV & keamanan', 'Kamera VIGI, NVR, AI CCTV, jasa pasang', '/assets/img/vigi/s385dps.webp',
     ['cctv'], ['jasa-pasang-cctv', 'jasa-ai-cctv', 'vision', 'attendance']),
    ('pengadaan', 'Pengadaan', 'Laptop, PC, server, perangkat resmi untuk kantor & instansi', '/assets/img/portfolio/hardware-field/kiosk-pampang-install.jpg',
     ['laptop', 'computer', 'tablet', 'server'], ['jasa-pengadaan', 'jasa-server', 'jasa-kios-custom']),
    ('software', 'Software & aplikasi', 'Aplikasi Altora, website, dan aplikasi custom', '/assets/img/produk/teams.webp',
     ['app'], ['jasa-website', 'jasa-software', 'jasa-iot']),
    ('jaringan', 'Jaringan & infrastruktur', 'WiFi, LAN, fiber, rak server, listrik', '/assets/img/portfolio/unmul-infrastructure/network-rack.png',
     ['rack', 'fiber'], ['jasa-jaringan', 'jasa-fiber', 'jasa-listrik', 'jasa-it-support']),
    ('komputer', 'Komputer & laptop', 'Lenovo ThinkPad, AIO, tablet, server', '/assets/img/hardware/lenovo-thinkpad-t14.webp',
     ['laptop', 'computer', 'tablet', 'server'], ['jasa-server']),
    ('armada', 'GPS & armada', 'GPS tracker Teltonika, sensor, Altora FMS', '/assets/img/hardware/telt-fmc920.webp',
     ['gps'], ['jasa-gps', 'fms']),
    ('internet', 'Starlink & internet', 'Kit Starlink, instalasi, off-grid', '/assets/img/hardware/starlink-v5.webp',
     ['konek'], ['jasa-starlink']),
    ('akses', 'Smartlock & akses', 'Kunci digital, akses pintu, absensi', '/assets/img/hardware/smartlock.webp',
     ['akses'], ['pass', 'attendance']),
    ('display', 'Display, signage & kios', 'Videotron, IFP, kios layanan mandiri', '/assets/img/hardware/kios-k.webp',
     ['display', 'kios'], ['jasa-display', 'jasa-kios-custom']),
    ('jasa', 'Semua jasa', 'Pemasangan, instalasi, perawatan, pembuatan', '/assets/img/services/team-podium-system-demo.png',
     ['jasa'], []),
    ('barang', 'Semua barang', 'Seluruh perangkat di katalog', '/assets/img/hardware/hde-ifp.webp',
     [c for c, _ in HW_CATS], []),
]
views_json = json.dumps({k: {'t': t, 'cats': cats, 'ids': ids} for k, t, _, _, cats, ids in VIEWS}, ensure_ascii=False)
chooser = ''.join(f'<a class="kc-tile" data-view="{k}" href="#v-{k}"><span class="kc-pic"><img alt="" loading="lazy" src="{img}"/></span>'
                  f'<span class="kc-txt"><b>{e(t)}</b><small>{e(d)}</small></span></a>' for k, t, d, img, _, _ in VIEWS)
cat_names = dict(HW_CATS, app='Software', jasa='Jasa')
cat_json = json.dumps(cat_names, ensure_ascii=False)
kat_ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Katalog Altora Indonesia', 'numberOfItems': len(APPS) + len(HW_ITEMS) + len(JASA)}
katalog_page = head('Katalog Altora | Barang, Jasa & Software', 'Katalog Altora: CCTV VIGI, GPS, Starlink, smartlock, laptop & server Lenovo, display, jaringan, jasa pemasangan, dan software. Tambah ke keranjang, kirim via WhatsApp.', '/katalog', kat_ld) + f"""<main class="pd-page kt-page">
<section class="pd-hero kt-hero"><div class="pd-wrap">
<div class="kt-bar"><p class="eyebrow eyebrow-purple">Katalog</p><button class="btn btn-outline kt-print" onclick="window.print()" type="button">Cetak / simpan PDF</button></div>
<h1>Anda sedang mencari apa?</h1>
<p class="pd-lead">Pilih kebutuhan Anda, kami tampilkan barang, jasa, dan software yang relevan. Tambahkan ke keranjang, lalu kirim lewat WhatsApp untuk penawaran.</p>
<nav aria-label="Pilih kebutuhan" class="kc-grid">{chooser}</nav>
</div></section>
<section class="pd-block kt-results" hidden="" id="hasil"><div class="pd-wrap">
<div class="kr-head"><a class="kr-back" href="#">← Ganti pilihan</a><h2 class="kr-title"></h2><span class="kr-count"></span></div>
<div aria-label="Saring" class="hwi-filter kr-sub" role="group"></div>
<div class="hwi-allvigi kr-vigi" hidden=""><div><b>Katalog lengkap CCTV VIGI</b><br/><span>148 model kamera, NVR, kit, decoder, solar, dan jaringan pendukung.</span></div><a class="btn btn-purple" href="/katalog-cctv-vigi">Lihat semua model VIGI →</a></div>
<div class="hwi-grid">{"".join(hw_item(h) for h in HW_ITEMS)}{"".join(kat_jasa(j) for j in JASA)}{"".join(kat_app(k) for k in APPS)}</div>
<div class="hwi-more"><div><b>Tidak menemukan yang dicari?</b><p>Kami juga mengadakan perangkat lain sesuai spesifikasi proyek Anda: jaringan TP-Link Omada, model Lenovo lainnya, dan perangkat khusus.</p></div>
<a class="btn btn-purple" href="{WA}{quote("Halo Altora, saya mencari perangkat/jasa yang tidak ada di katalog.")}" rel="noopener" target="_blank">Tanya via WhatsApp →</a></div>
</div></section>
</main>
<footer></footer>
<script id="kc-views" type="application/json">{views_json}</script><script id="kc-cats" type="application/json">{cat_json}</script>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="/assets/js/hw-filter.js?v=20261014d"></script></body></html>
"""
(root / 'katalog.html').write_text(katalog_page, encoding='utf-8')
print('produk.html (pengetahuan) & katalog.html dibuat')

# ── Grid produk ringkas di beranda (index.html, di antara penanda produk-ringkas) ──
def home_card(p):
    soon = '<span class="hp-soon">Custom</span>' if p.get('status') == 'custom' else ''
    pos = PHOTO_FOCUS.get(p['id'], '50% 50%')
    return (f'<a class="hp-card" href="/produk/{p["id"]}"><span class="hp-pic"><img alt="" loading="lazy" '
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
