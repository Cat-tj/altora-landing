"""Halaman /pengadaan: katalog pengadaan perangkat (CCTV VIGI, kit Starlink, jaringan & rak server, GPS tracker, display & kios,
laptop/PC/tablet/server) beserta jasa instalasinya. Data produk di pengadaan_data.py (diporting dari katalog situs saudara).
Aturan: tanpa harga (setiap kartu -> 'Minta penawaran' lewat WhatsApp), Altora bukan mitra resmi Starlink,
layanan perangkat kecil (CCTV rumahan, smart lock, smart home, IT support bulanan) hanya Samarinda, proyek perusahaan se-Kaltim.
Schema: CollectionPage + ItemList (tanpa Product/Offer, supaya tidak ada harga atau rating karangan), Service + OfferCatalog jasa, FAQPage.
Jalankan sebelum apply_shell.py (lihat build_all.sh)."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import OFFICES, ORG_ID, org, office_node
from pengadaan_data import PRODUCTS, VIGI_MODELS, IMG_SIZE

root = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://altora.id'
URL = '/pengadaan'
CSS_VER = '20261118a'
WA = 'https://wa.me/6285190911170?text='
IMG = '/assets/img/pengadaan/'
e = lambda t: html.escape(str(t), quote=True)
wa = lambda msg: WA + quote(msg)

TITLE = 'Pengadaan Perangkat: CCTV, Starlink, Jaringan & Laptop | Altora'
DESC = ('Pengadaan CCTV VIGI dan Dahua, kit Starlink, rak server, GPS Teltonika, display, dan laptop/PC/server Lenovo, '
        'lengkap dengan jasa instalasi di Kalimantan Timur.')
H1 = 'Pengadaan perangkat, sekaligus pemasangannya'
LEAD = ('CCTV VIGI dan Dahua, kit Starlink, jaringan dan rak server, GPS tracker, display, sampai laptop dan server. '
        'Kami sediakan barang resmi bergaransi, pasang di lokasi, dan rawat setelahnya untuk perusahaan dan instansi di Kalimantan Timur.')

ICONS = {
    'camera': '<path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/>',
    'sat': '<path d="M5 19 19 5"/><path d="M7 13a4 4 0 0 0 4 4M4 13a7 7 0 0 0 7 7"/><rect height="6" rx="1" transform="rotate(45 16 8)" width="8" x="12" y="5"/>',
    'rack': '<rect height="18" rx="1.5" width="14" x="5" y="3"/><path d="M5 8h14M5 13h14M5 18h14M8 5.5h.01M8 10.5h.01M8 15.5h.01"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'display': '<rect height="12" rx="2" width="18" x="3" y="4"/><path d="M9 20h6M12 16v4"/>',
    'laptop': '<rect height="10" rx="1.5" width="16" x="4" y="5"/><path d="M2 19h20"/>',
    'search': '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
    'tool': '<path d="M14 7a4 4 0 0 0-5 5l-5 5 3 3 5-5a4 4 0 0 0 5-5l-2.5 2.5-2-2z"/>',
    'bolt': '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    'wifi': '<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0"/><circle cx="12" cy="19.5" r="1"/>',
    'fiber': '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    'check': '<path d="m5 12 4 4 10-10"/>',
}
icon = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[n]}</svg>'
WA_ICON = ('<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12.05 2C6.6 2 2.16 6.44 2.16 11.89c0 1.75.46 3.45 1.33 4.95L2.06 22l5.3-1.39a9.86 9.86 0 0 0 4.69 1.19c5.45 0 9.89-4.44 '
           '9.89-9.89S17.5 2 12.05 2Zm5.42 12.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.18.2-.35.23-.65.08-.3-.15-1.25-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.14-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.91-2.21-.25-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.03 1.02-1.03 2.48s1.06 2.87 1.21 3.07c.15.2 2.1 3.2 5.08 4.49 2.48 1.07 2.99.86 3.53.8.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.18-1.42-.08-.12-.27-.2-.57-.35Z"/></svg>')

# (anchor, judul, ringkasan tile, ikon, merek, pengantar, foto tile, jasa (judul, isi, poin), tautan terkait)
CATS = [
    ('cctv', 'CCTV &amp; keamanan', 'Kamera, NVR, tenaga surya, smart lock', 'camera', 'VIGI by TP-Link · Dahua · mitra resmi',
     'Kamera VIGI dan Dahua untuk rumah, toko, kantor, gudang, dan site proyek, lengkap dengan NVR, tenaga surya, dan software pemantauan. '
     'Kirim denah atau foto lokasi, kami bantu hitung tipe dan jumlah kameranya.', 'vigi-turret-fullcolor.webp',
     ('Jasa pasang CCTV', 'Survei titik, pemasangan kamera dan NVR, sampai rekaman bisa dipantau dari HP.',
      ['Survei titik kamera', 'Kabel, tiang &amp; bracket', 'Setting NVR &amp; aplikasi HP', 'Analitik: APD/K3, perimeter, hitung orang']),
     [('/infrastruktur-hardware-kaltim', 'CCTV AI untuk perusahaan (Kaltim)'), ('/services/cctv', 'Pasang CCTV rumah &amp; toko (Samarinda)'),
      ('/cctv-tenaga-surya-samarinda', 'CCTV tenaga surya &amp; 4G'), ('/jual-cctv-samarinda', 'Jual CCTV Samarinda')]),
    ('starlink', 'Starlink &amp; internet', 'Kit Starlink, instalasi, off-grid', 'sat', 'Kit Starlink · khusus Kalimantan Timur',
     'Kit Starlink untuk rumah, kantor, site tambang, kebun, dan kapal di Kalimantan Timur yang tidak terjangkau fiber. '
     'Kami bantu pengadaan kitnya dan memasang sampai Wi-Fi menyala di titik yang dibutuhkan. Layanan kit Starlink hanya untuk wilayah Kalimantan Timur.', 'starlink-v5.webp',
     ('Instalasi Starlink &amp; off-grid', 'Pemasangan lengkap: mounting, kabel, Wi-Fi, dan panel surya untuk lokasi tanpa PLN.',
      ['Survei titik &amp; mounting', 'Tiang &amp; grounding anti-petir', 'Wi-Fi repeater / mesh', 'Failover dual-WAN', 'Panel surya &amp; baterai']),
     [('/infrastruktur-hardware-kaltim', 'Starlink untuk lokasi terpencil (Kaltim)'), ('/jual-starlink-samarinda', 'Kit Starlink Samarinda'),
      ('/jual-starlink-balikpapan', 'Kit Starlink Balikpapan'), ('/jual-starlink-berau', 'Kit Starlink Berau')]),
    ('jaringan', 'Jaringan &amp; infrastruktur', 'Rak server, data center, fiber optik', 'rack', 'HaganeRack · Fasser · mitra resmi',
     'Rak server, sistem pendingin data center, dan alat ukur fiber optik untuk ruang server, kantor, dan proyek jaringan. '
     'Kabel LAN, WiFi, dan listriknya juga kami kerjakan.', 'hr-close-glass.webp',
     ('Instalasi jaringan, fiber &amp; listrik', 'LAN, access point, fiber, rak server, wireless bridge antar gedung, dan kelistrikannya.',
      ['Kabel LAN &amp; switch PoE', 'WiFi merata &amp; wireless bridge', 'Fusion splicing &amp; laporan OTDR', 'Panel, MCB &amp; grounding', 'Dokumentasi jalur']),
     [('/infrastruktur-hardware-kaltim', 'Jaringan &amp; IoT untuk perusahaan (Kaltim)'), ('/services/iot-custom', 'IoT custom')]),
    ('gps', 'GPS tracker &amp; telematika', 'Tracker Teltonika, sensor, kamera kendaraan', 'pin', 'Teltonika · mitra resmi',
     'GPS tracker untuk mobil, motor, truk, alat berat, dan pekerja lapangan, ditambah sensor BBM, CAN, dan tekanan ban, serta kamera kabin.', 'telt-fmc920.webp',
     ('Pemasangan GPS tracker', 'Tracker, sensor BBM, TPMS, dan kamera di kendaraan dan alat berat.',
      ['Pilih perangkat per unit', 'Pemasangan rapi &amp; terkalibrasi', 'Akun platform pelacakan', 'Integrasi ke aplikasi armada']),
     [('/services/tracking', 'Tracking armada &amp; aset'), ('/industri/pertambangan', 'Solusi tambang')]),
    ('display', 'Display, signage &amp; kios', 'Videotron, interactive panel, kios layanan', 'display', 'HDe · mitra resmi',
     'Videotron, interactive flat panel, paket ruang rapat, digital signage, dan kios layanan mandiri untuk lobi, kelas, dan layanan publik.', 'hde-ifp.webp',
     ('Instalasi videotron, signage &amp; kios', 'Rangka, kelistrikan, pemasangan, dan pengaturan konten layar dan kios.',
      ['Hitung ukuran &amp; rangka', 'Pemasangan &amp; kalibrasi', 'Pengaturan konten', 'Kios custom: bodi, perangkat &amp; aplikasi']),
     [('/services/software-custom', 'Aplikasi kios &amp; antrean custom')]),
    ('komputer', 'Laptop, PC, tablet &amp; server', 'Untuk kantor, sekolah &amp; instansi', 'laptop', 'Lenovo · HDe · mitra resmi',
     'Laptop, PC, all-in-one, tablet, dan server untuk kantor, sekolah, dan instansi, siap pakai dengan instalasi dan garansi resmi. '
     'Cocok untuk pengadaan jumlah banyak.', 'lenovo-thinkpad-t14.webp',
     ('Pengadaan server &amp; komputer', 'Perangkat siap pakai: instalasi OS, jaringan, domain, dan backup, dengan garansi resmi.',
      ['Pilih spesifikasi sesuai beban', 'Instalasi OS, domain &amp; backup', 'Garansi resmi &amp; perawatan', 'Berita acara &amp; dokumentasi']),
     [('/services/it-support', 'IT support bulanan (Samarinda)'), ('/it-support-samarinda', 'IT support Samarinda')]),
]

VIGI_NAMES = {'dome': 'Kamera dome', 'bullet': 'Kamera bullet', 'turret': 'Kamera turret', 'pt': 'Pan tilt &amp; PTZ', 'fisheye': 'Fisheye',
              'nvr': 'NVR (perekam)', 'kit': 'Paket NVR + kamera', 'nvd': 'Video decoder', 'solar': 'Tenaga surya',
              'net': 'Switch PoE &amp; jaringan', 'acc': 'Aksesori'}

STEPS = [('Survei lokasi', 'Titik pemasangan, jalur kabel, listrik, dan sinyal dicek langsung.'),
         ('Rancangan &amp; penawaran', 'Daftar perangkat dan pekerjaan, ditulis jelas.'),
         ('Pengadaan barang', 'Barang resmi bergaransi dari principal dan distributor.'),
         ('Pemasangan &amp; konfigurasi', 'Dipasang rapi, diatur, dan diuji di lokasi.'),
         ('Serah terima', 'Uji bersama, pelatihan singkat, dan berita acara.'),
         ('Perawatan', 'Kunjungan berkala atau kontrak dengan SLA.')]

JASA = [
    ('search', 'Survei lokasi', 'Cek titik pemasangan, jalur kabel, sumber listrik, dan sinyal. Hasilnya jadi dasar rancangan dan penawaran.'),
    ('camera', 'Pasang CCTV &amp; NVR', 'Kamera, NVR, kabel, tiang, dan bracket, sampai rekaman langsung dan rekaman lama bisa dibuka dari HP.'),
    ('sat', 'Instalasi Starlink &amp; off-grid', 'Mounting, kabel, Wi-Fi repeater atau mesh, dan panel surya dengan baterai untuk lokasi tanpa PLN.'),
    ('tool', 'Mounting, tiang &amp; grounding', 'Tiang, bracket, dan grounding anti-petir supaya kamera dan terminal aman di lokasi terbuka.'),
    ('wifi', 'Jaringan LAN &amp; WiFi', 'Penarikan kabel, switch PoE, access point, rak, dan wireless bridge antar gedung, dengan dokumentasi jalur.'),
    ('fiber', 'Fiber optik', 'Penarikan dan terminasi kabel fiber, fusion splicing, dan pengujian OTDR dengan laporan hasil.'),
    ('bolt', 'Instalasi listrik', 'Titik baru, panel dan MCB, grounding, dan beban khusus untuk rumah, kantor, dan fasilitas, dengan garansi kerja.'),
    ('pin', 'GPS tracker &amp; sensor', 'Tracker, sensor BBM, TPMS, dan kamera kabin di kendaraan dan alat berat, lalu akun pelacakannya diatur.'),
    ('display', 'Videotron, signage &amp; kios', 'Hitung ukuran dan rangka, pemasangan, kalibrasi, dan pengaturan konten layar.'),
    ('gear', 'Konfigurasi perangkat', 'Laptop, PC, dan server siap pakai: OS, akun, domain, dan backup. NVR, router, dan VLAN diatur sesuai kebutuhan.'),
    ('link', 'Integrasi &amp; pelatihan', 'Menyambungkan perangkat ke sistem yang ada, misalnya CCTV ke dashboard atau GPS ke aplikasi armada, lalu melatih tim Anda.'),
    ('shield', 'Perawatan &amp; SLA', 'Kunjungan berkala, bantuan lewat WhatsApp, dan laporan perawatan. Bisa kontrak bulanan dengan SLA.'),
]

CHANNEL = ['Berstatus PKP', 'Terdaftar penyedia Inaproc/LKPP', 'Barang resmi bergaransi', 'Penawaran, faktur &amp; berita acara']

FAQ = [
    ('Apakah ada daftar harga?', 'Harga bergantung tipe, jumlah, dan lokasi pemasangan, jadi kami tidak memasang daftar harga. Kirim kebutuhan Anda lewat WhatsApp, kami balas dengan penawaran tertulis.'),
    ('Apakah bisa beli perangkat saja tanpa pemasangan?', 'Bisa. Perangkat bisa dibeli saja, atau sekaligus dengan pemasangan, konfigurasi, dan perawatan oleh tim kami.'),
    ('Apakah Altora mitra resmi Starlink?', 'Tidak. Altora bukan mitra resmi Starlink. Kami membantu pengadaan kit, survei lokasi, pemasangan, grounding, dan integrasi ke jaringan Anda. Starlink adalah merek dagang SpaceX.'),
    ('Apakah kit Starlink bisa dikirim ke luar Kalimantan Timur?', 'Tidak. Pengadaan dan pemasangan kit Starlink oleh Altora hanya untuk wilayah Kalimantan Timur: Samarinda, Balikpapan, Bontang, Berau, Kutai Kartanegara, Kutai Timur, Kutai Barat, Mahakam Ulu, Paser, Penajam Paser Utara, dan IKN.'),
    ('Merek apa saja yang tersedia?', 'Perangkat dari mitra resmi: CCTV VIGI by TP-Link dan Dahua, GPS tracker Teltonika, laptop, PC, dan server Lenovo, display HDe, rak server HaganeRack, dan alat fiber optik Fasser. Hikvision dan HiLook juga tersedia, begitu pula merek lain yang bisa dibahas sesuai kebutuhan proyek.'),
    ('Apakah bisa untuk pengadaan instansi?', 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara serah terima.'),
    ('Wilayah mana yang dilayani untuk pemasangan?', 'Proyek perusahaan dan instansi di Kalimantan Timur: Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya. Pasang CCTV rumahan, smart lock, smart home, dan IT support bulanan saat ini hanya Samarinda. Di luar Kalimantan Timur, perangkat selain kit Starlink bisa dikirim; pemasangan di lokasi kami bahas per proyek. Kit Starlink khusus Kalimantan Timur.'),
]


def pic(img, alt):
    if not img:
        return None
    w, h = IMG_SIZE[img]
    return f'<img alt="{e(alt)}" decoding="async" height="{h}" loading="lazy" src="{IMG}{img}" width="{w}"/>'


def card(p, cat_icon, hlevel):
    pid, brand, name, img, desc, specs = p
    im = pic(img, f'{name} {brand}') or f'<span class="pgd-noimg">{icon(cat_icon)}</span>'
    dl = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in specs)
    item = name if brand in name else f'{name} ({brand})'
    if brand == 'Starlink':
        item = f'kit {name}'
    msg = f'Halo Altora, saya ingin minta penawaran {item}.'
    return (f'<article class="pgd-card" id="p-{pid}"><div class="pgd-pic">{im}</div><div class="pgd-body">'
            f'<small class="pgd-brand">{e(brand)}</small><h{hlevel}>{e(name)}</h{hlevel}><p>{e(desc)}</p>'
            f'<dl class="pgd-specs">{dl}</dl>'
            f'<a class="pgd-ask" href="{wa(msg)}" rel="noopener" target="_blank">{WA_ICON}Minta penawaran</a></div></article>')


def count(key):
    return sum(len(l) for _, l in PRODUCTS[key])


def vigi_models():
    total = sum(len(l) for _, l in VIGI_MODELS)
    groups = ''.join(f'<div class="pgd-mgroup"><h4>{VIGI_NAMES.get(k, e(k))} <span>{len(l)}</span></h4><ul>'
                     + ''.join(f'<li><b>{e(n)}</b>{e(s)}</li>' for n, s in l) + '</ul></div>' for k, l in VIGI_MODELS)
    return (f'<details class="pgd-models"><summary><span>Lihat {total} model VIGI yang bisa kami sediakan</span></summary>'
            '<p class="pgd-models-key">Kode model: angka pertama 2 = dome, 3 = bullet, 4 = turret, 5 = pan tilt, 6 = fisheye; angka kedua = megapiksel. '
            'Akhiran I = inframerah, Z = zoom, S = ColorPro (malam berwarna), W = Wi-Fi. Ketersediaan tiap model kami konfirmasi saat Anda bertanya.</p>'
            f'<div class="pgd-mgrid">{groups}</div></details>')


def section(c):
    key, title, _, ico, brand, lead, _, (jt, jd, jpts), links = c
    groups = PRODUCTS[key]
    body = ''
    for sub, items in groups:
        cards = ''.join(card(p, ico, 4 if sub else 3) for p in items)
        body += (f'<h3 class="pgd-sub">{e(sub)}</h3>' if sub else '') + f'<div class="pgd-grid">{cards}</div>'
    if key == 'cctv':
        body += vigi_models()
        body += ('<div class="pgd-also"><div><b>Juga tersedia: Dahua, Hikvision, dan HiLook</b>'
                 '<p>Dahua adalah mitra resmi kami; Hikvision dan HiLook tersedia sesuai kebutuhan proyek. Tipe dan ketersediaannya kami konfirmasi lewat chat.</p></div>'
                 f'<a class="btn btn-purple" href="{wa("Halo Altora, saya ingin minta penawaran CCTV merek Dahua, Hikvision, atau HiLook. Kebutuhan saya: ")}" rel="noopener" target="_blank">Minta penawaran</a></div>')
    note = ''
    if key == 'starlink':
        note = '<p class="pgd-note">Wilayah layanan kit Starlink: Kalimantan Timur saja. Altora bukan mitra resmi Starlink; kami membantu pengadaan kit dan pemasangannya. Starlink adalah merek dagang SpaceX.</p>'
    if key == 'cctv':
        note = '<p class="pgd-note">Smart lock dan pasang CCTV untuk rumah atau toko saat ini khusus Samarinda. CCTV untuk perusahaan dan site proyek melayani Kalimantan Timur.</p>'
    pts = ''.join(f'<li>{icon("check")}{p}</li>' for p in jpts)
    rel = ''.join(f'<a href="{u}">{t}</a>' for u, t in links)
    msg = 'Halo Altora, saya ingin minta penawaran ' + re.sub('<[^>]+>', '', html.unescape(title)).lower() + ' beserta pemasangannya.'
    aside = (f'<aside class="pgd-side"><span class="pgd-ico">{icon(ico)}</span><h2>{title}</h2><p class="pgd-brandline">{brand}</p><p>{lead}</p>'
             f'<div class="pgd-jasa"><h3>{jt}</h3><p>{jd}</p><ul>{pts}</ul></div>'
             f'<a class="btn btn-white pgd-side-cta" href="{wa(msg)}" rel="noopener" target="_blank">Minta penawaran paket</a>'
             f'<nav aria-label="Halaman terkait" class="pgd-rel">{rel}</nav>{note}</aside>')
    return (f'<section class="pgd-cat" id="{key}"><div class="ct-wrap pgd-cat-grid">{aside}'
            f'<div class="pgd-items"><p class="pgd-count">{count(key)} produk</p>{body}</div></div></section>')


def page():
    shelf = ''.join(f'<a class="pgd-tile" href="#{k}"><span class="pgd-tile-pic">{pic(img, "")}</span>'
                    f'<span class="pgd-tile-txt"><b>{t}</b><small>{s}</small><em>{count(k)} produk</em></span></a>'
                    for k, t, s, _, _, _, img, _, _ in CATS)
    shelf += ('<a class="pgd-tile pgd-tile-jasa" href="#jasa-instalasi"><span class="pgd-tile-ico">' + icon('tool') + '</span>'
              '<span class="pgd-tile-txt"><b>Jasa instalasi</b><small>Survei, pemasangan, konfigurasi, perawatan</small></span></a>')
    chan = ''.join(f'<li>{icon("check")}{c}</li>' for c in CHANNEL)
    sections = ''.join(section(c) for c in CATS)
    steps = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in STEPS)
    jasa = ''.join(f'<article class="pgd-svc"><span class="pgd-ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in JASA)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    offices = ''.join(f'<li><b>{e(o["label"])}</b>{e(o["street"])}, {e(o["city"])}</li>' for o in OFFICES)
    hero_msg = 'Halo Altora, saya ingin minta penawaran pengadaan perangkat. Kebutuhan saya: '
    total = sum(count(k) for k, *_ in CATS)

    items, pos = [], 0
    for k, title, *_ in CATS:
        for _, lst in PRODUCTS[k]:
            for pid, brand, name, img, desc, _ in lst:
                pos += 1
                it = {'@type': 'ListItem', 'position': pos, 'name': f'{name} ({brand})' if brand not in name else name, 'url': f'{SITE}{URL}#p-{pid}'}
                if img:
                    it['image'] = SITE + IMG + img
                items.append(it)
    ld = {'@context': 'https://schema.org', '@graph': [org()] + [office_node(o) for o in OFFICES] + [
        {'@type': 'CollectionPage', '@id': SITE + URL + '#halaman', 'url': SITE + URL, 'name': 'Pengadaan perangkat Altora', 'description': DESC,
         'inLanguage': 'id-ID', 'about': {'@id': ORG_ID}, 'isPartOf': {'@id': SITE + '/#website'},
         'mainEntity': {'@type': 'ItemList', 'name': 'Katalog pengadaan perangkat', 'numberOfItems': len(items), 'itemListElement': items}},
        {'@type': 'Service', '@id': SITE + URL + '#jasa', 'name': 'Pengadaan dan instalasi perangkat', 'serviceType': 'Pengadaan perangkat IT, instalasi, dan perawatan',
         'description': DESC, 'url': SITE + URL, 'provider': {'@id': ORG_ID},
         'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Kalimantan Timur'}, {'@type': 'City', 'name': 'Samarinda'}, {'@type': 'City', 'name': 'Balikpapan'}],
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Jasa instalasi', 'itemListElement': [
             {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': html.unescape(t)}} for _, t, _ in JASA]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Layanan', 'item': SITE + '/services'},
            {'@type': 'ListItem', 'position': 3, 'name': 'Pengadaan perangkat', 'item': SITE + URL}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]}
    og = SITE + IMG + 'vigi-turret-fullcolor.webp'
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(TITLE)}</title><meta content="{e(DESC)}" name="description"/><link href="{SITE}{URL}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(TITLE)}" property="og:title"/><meta content="{e(DESC)}" property="og:description"/><meta content="{SITE}{URL}" property="og:url"/><meta content="{og}" property="og:image"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v=20261016i"/><link rel="stylesheet" href="/assets/css/pengadaan.css?v=b{CSS_VER}"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
<main class="ct-page pgd-page">
<section class="pgd-hero"><div class="ct-wrap pgd-hero-grid">
<div class="pgd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/beranda">Beranda</a><span>/</span><a href="/services">Layanan</a><span>/</span><span>Pengadaan perangkat</span></nav>
<p class="eyebrow eyebrow-purple">Pengadaan perangkat · Kalimantan Timur</p><h1>{e(H1)}</h1><p class="ct-lead">{e(LEAD)}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{wa(hero_msg)}" rel="noopener" target="_blank">Minta penawaran</a><a class="btn btn-white" href="#jasa-instalasi">Lihat jasa instalasi</a></div>
<ul class="pgd-channel" aria-label="Jalur pengadaan">{chan}</ul></div>
<nav aria-label="Kategori perangkat" class="pgd-shelf">{shelf}</nav>
</div></section>
<div class="pgd-intro ct-wrap"><p><b>{total} produk dalam {len(CATS)} kategori</b>, dari mitra resmi VIGI by TP-Link, Dahua, Teltonika, Lenovo, HDe, HaganeRack, dan Fasser, ditambah kit Starlink. Tanpa daftar harga: setiap produk punya tombol <b>Minta penawaran</b> yang membuka chat WhatsApp dengan nama produknya.</p></div>
{sections}
<section class="pgd-jasa-sec" id="jasa-instalasi"><div class="ct-wrap">
<div class="pgd-head"><h2>Jasa instalasi</h2><p>Barang yang kami sediakan juga kami pasang. Tim teknisi datang ke lokasi, dari survei sampai perawatan, dengan alur yang sama untuk setiap proyek.</p></div>
<ol class="pgd-steps">{steps}</ol>
<div class="pgd-svcs">{jasa}</div>
</div></section>
<section class="pgd-area"><div class="ct-wrap pgd-area-grid">
<div class="pgd-area-card"><h2>Kalimantan Timur</h2><p>Proyek perusahaan dan instansi: CCTV dengan AI, Starlink, jaringan dan rak server, GPS armada, display, dan pengadaan komputer di Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya.</p><a href="/infrastruktur-hardware-kaltim">Infrastruktur &amp; hardware Kaltim</a></div>
<div class="pgd-area-card"><h2>Khusus Samarinda</h2><p>Pasang CCTV rumah dan toko, smart lock, smart home, dan IT support bulanan untuk kantor saat ini hanya melayani Samarinda.</p><span class="pgd-area-links"><a href="/services/cctv">Pasang CCTV</a><a href="/services/smart-lock">Smart lock</a><a href="/services/smart-home">Smart home</a><a href="/services/it-support">IT support bulanan</a></span></div>
<div class="pgd-area-card pgd-area-office"><h2>Kantor kami</h2><ul>{offices}</ul><p>Di luar Kalimantan Timur, perangkat bisa dikirim. Pemasangan di lokasi kami bahas per proyek.</p></div>
</div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Kirim daftar kebutuhan Anda</h2><p>Tulis perangkat, jumlah, dan lokasinya. Kami balas dengan penawaran tertulis, termasuk pemasangan bila dibutuhkan.</p></div><a class="btn btn-purple" href="{wa(hero_msg)}" rel="noopener" target="_blank">Minta penawaran</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


if __name__ == '__main__':
    (root / 'pengadaan.html').write_text(page(), encoding='utf-8')
    from build_area import update_sitemap
    update_sitemap([URL])
    sm = root / 'sitemap.xml'
    t = sm.read_text(encoding='utf-8')
    t = re.sub(r'(<loc>' + re.escape(SITE + URL) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-11-18', t)
    sm.write_text(t, encoding='utf-8')
    print('halaman:', URL, sum(count(k) for k, *_ in CATS), 'produk')
