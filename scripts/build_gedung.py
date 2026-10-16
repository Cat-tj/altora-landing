"""Prototipe landing 'halaman = gedung', model "masuk ke layar": /preview-gedung (noindex).
Struktur halaman (semua konten adalah HTML biasa yang bisa di-scroll):
  adegan 3D intro  -> bagian lantai 7 -> adegan 3D -> bagian lantai 6 -> ... -> bagian lobi -> adegan 3D penutup -> footer
Setiap bagian diawali 'sampul' setinggi layar dan diakhiri 'penutup' setinggi layar. Di adegan 3D, layar di ruangan
menampilkan salinan sampul/penutup itu persis seukuran layar Anda, sehingga perpindahan 3D <-> halaman tidak terlihat.
Animasi: assets/js/gedung3d.js; gaya: assets/css/gedung.css.
Jalankan lewat scripts/build_all.sh (atau: python3 scripts/build_gedung.py && python3 scripts/apply_shell.py)."""
import html, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
CSS_VER = '20261016i'
WA = 'https://wa.me/6285190911170?text=Halo%20Altora%2C%20saya%20ingin%20konsultasi.'
P = '/assets/img/portfolio/'

ICON = {
    'app': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    'web': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    'ai': '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2"/><circle cx="12" cy="12" r="3"/>',
    'iot': '<circle cx="12" cy="12" r="2"/><path d="M8 8a6 6 0 0 0 0 8M16 8a6 6 0 0 1 0 8M5 5a10 10 0 0 0 0 14M19 5a10 10 0 0 1 0 14"/>',
    'box': '<path d="m12 3 9 5v8l-9 5-9-5V8z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    'truck': '<path d="M2.5 6.5h11v9h-11zM13.5 9.5h4l3 3.2v2.8h-7z"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'sat': '<path d="M4.5 13.5a6 6 0 0 0 6 6M4.5 9.5a10 10 0 0 0 10 10"/><circle cx="5" cy="19" r="1.4"/><path d="m13 4 3 3-3.5 3.5-3-3zM16 7l4-4"/>',
}
ico = lambda k: f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg>'


def rows(items):
    return '<div class="gs-list">' + ''.join(
        f'<a class="gs-row" href="{u}"><span class="gs-ic">{ico(i)}</span><span><b>{e(t)}</b><small>{e(d)}</small></span><em>→</em></a>' for u, i, t, d in items) + '</div>'


def split(img, alt, points, links):
    return ('<div class="gs-split"><figure><img alt="' + e(alt) + '" loading="lazy" src="' + img + '"/></figure><div class="gs-points">'
            + ''.join(f'<div><b>{e(t)}</b><p>{e(d)}</p></div>' for t, d in points)
            + '<div class="gs-links">' + ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in links) + '</div></div></div>')


# ── isi tiap lantai (dari atas ke bawah) ──
SECTIONS = [
    dict(k=7, room='Ruang meeting', kicker='Layanan', title='Yang kami bangun untuk Anda',
         lead='Aplikasi, website, CCTV pintar, jaringan, sampai pengadaan perangkat. Satu tim dari konsultasi sampai perawatan.',
         img=P + 'meeting.jpg',
         body=rows([('/services/software-custom', 'app', 'Aplikasi & sistem internal', 'Absensi, approval, HRIS, dan laporan internal di web dan HP.'),
                    ('/services/website-seo', 'web', 'Website & SEO', 'Company profile, website instansi, dan landing page yang mudah ditemukan.'),
                    ('/services/software-custom', 'link', 'Integrasi sistem', 'Menghubungkan aplikasi dan perangkat yang selama ini berjalan sendiri.'),
                    ('/services/ai-cctv', 'ai', 'AI & CCTV pintar', 'Deteksi APD, absensi wajah, dan alert area terlarang dari kamera.'),
                    ('/services/iot-command-center', 'iot', 'IoT & ruang kendali', 'Sensor, smartlock, dan command center yang terhubung.'),
                    ('/services/pengadaan-instalasi-maintenance', 'box', 'Pengadaan & instalasi', 'Server, komputer, CCTV, dan jaringan dari principal resmi.'),
                    ('/services/fleet-management-service', 'truck', 'Armada & GPS tracker', 'Posisi, BBM, dan perilaku pengemudi dalam satu dashboard.'),
                    ('/services/starlink-internet-satelit', 'sat', 'Starlink & internet site', 'Internet satelit untuk site, kebun, dan lokasi terpencil.')])
              + '<div class="gs-strip">' + ''.join(f'<figure><img alt="{e(c)}" loading="lazy" src="{s}"/><figcaption>{e(c)}</figcaption></figure>' for s, c in [
                  (P + 'unmul-infrastructure/cable-cctv-installation.png', 'Instalasi CCTV & jaringan, Universitas Mulawarman'),
                  (P + 'hardware-field/kiosk-baqa-service.jpg', 'Kios layanan di kantor kelurahan Samarinda'),
                  (P + 'fms.jpg', 'Dashboard armada hauling')]) + '</div>'),
    dict(k=6, room='Ruang direksi', kicker='AI & ruang kendali', title='Keputusan dari satu layar',
         lead='AI mengenali pelanggaran APD dari CCTV, asisten AI berjalan di server Anda sendiri, dan pimpinan memantau semuanya dari satu tempat.',
         img=P + 'safety.jpg',
         body=split(P + 'safety.jpg', 'Deteksi APD dari CCTV',
                    [('Altora Vision', 'Helm, rompi, dan zona terlarang terdeteksi otomatis, lengkap dengan foto kejadian.'),
                     ('Private AI & GIS', 'Asisten AI dan peta data wilayah yang berjalan di server Anda, tanpa cloud publik.'),
                     ('Altora Command', 'CCTV, armada, dan sensor dalam satu ruang kendali dengan video wall.')],
                    [('/produk/vision', 'Altora Vision'), ('/produk/private-ai', 'Private AI & GIS'), ('/produk/command', 'Altora Command')])),
    dict(k=5, room='Ruang karyawan', kicker='Aplikasi Altora', title='Siap dipakai tim Anda',
         lead='SDM, tugas, dokumen, rapat, armada, dan akses pintu. Pakai satu, atau gabungkan semuanya.',
         img='/assets/img/produk/teams.webp',
         body='<div class="gs-apps">' + ''.join(
             f'<a href="/produk/{k}"><img alt="" loading="lazy" src="/assets/img/produk/{k}.webp"/><b>{e(n)}</b><small>{e(t)}</small></a>' for k, n, t in [
                 ('teams', 'Altora Teams', 'Absensi, cuti, lembur, payroll'), ('projek', 'Altora Projek', 'Tugas & progres proyek'),
                 ('office', 'Altora Office', 'Dokumen, spreadsheet, rapat'), ('fms', 'Altora FMS', 'Armada & BBM'),
                 ('attendance', 'Smart Attendance', 'Absensi wajah dari CCTV'), ('pass', 'Altora Pass', 'Akses pintu digital')]) + '</div>'),
    dict(k=4, room='Ruang server', kicker='Jaringan & server', title='Jalur data yang rapi',
         lead='LAN, WiFi, fiber optik, rak server, sampai Starlink untuk site terpencil. Dipasang, diuji, dan didokumentasikan.',
         img=P + 'unmul-infrastructure/network-rack.png',
         body=split(P + 'unmul-infrastructure/network-rack.png', 'Rak jaringan',
                    [('Jaringan kabel & WiFi', 'Sinyal merata, kabel rapi, dan dokumentasi jalur diserahkan setelah selesai.'),
                     ('Rak & ruang server', 'Close rack HaganeRack, penataan perangkat, dan pendinginan.'),
                     ('Internet untuk site', 'Starlink dan wireless bridge untuk lokasi tanpa jaringan kabel.')],
                    [('/jasa-instalasi-jaringan-samarinda', 'Instalasi jaringan'), ('/katalog#cat-rack', 'Rak server'), ('/katalog#cat-konek', 'Starlink')])),
    dict(k=3, room='Ruang keamanan', kicker='Perangkat lapangan', title='Mata dan telinga di lokasi',
         lead='Kamera CCTV VIGI, GPS tracker Teltonika, smartlock, Starlink, dan kios layanan dari principal resmi.',
         img='/assets/img/vigi/s385dps.webp',
         body='<div class="gs-gear">' + ''.join(
             f'<a href="{u}"><img alt="" loading="lazy" src="{s}"/><b>{e(n)}</b></a>' for u, s, n in [
                 ('/katalog-cctv-vigi', '/assets/img/vigi/s385dps.webp', 'CCTV VIGI'), ('/katalog#cat-gps', '/assets/img/hardware/telt-fmc920.webp', 'GPS tracker Teltonika'),
                 ('/katalog#cat-konek', '/assets/img/hardware/starlink-v5.webp', 'Starlink'), ('/katalog#cat-akses', '/assets/img/hardware/smartlock.webp', 'Smartlock'),
                 ('/katalog#cat-kios', '/assets/img/hardware/kios-k.webp', 'Kios layanan'), ('/katalog#cat-rack', '/assets/img/hardware/hr-close-glass.webp', 'Rak server')]) + '</div>'
              + '<div class="gs-links gs-center"><a class="btn btn-purple" href="/katalog">Buka katalog</a></div>'),
    dict(k=2, room='Klien kami', kicker='Klien & bukti', title='Sudah berdiri di banyak tempat',
         lead='Pemerintah daerah, kampus, dan perusahaan di Kalimantan Timur mempercayakan sistemnya kepada kami.',
         img=P + 'unmul-infrastructure/cable-cctv-installation.png',
         body='<div class="gs-logos">' + ''.join(f'<span><img alt="{e(n)}" loading="lazy" src="/assets/img/clients/{f}"/></span>' for f, n in [
                 ('samarinda.png', 'Pemkot Samarinda'), ('barito.png', 'Pemkab Barito Utara'), ('injourney.png', 'InJourney Airports'),
                 ('unmul.png', 'Universitas Mulawarman'), ('itk.png', 'Institut Teknologi Kalimantan'), ('adhi.png', 'Adhi')])
              + ''.join(f'<span class="gs-word">{e(n)}</span>' for n in ['Alba Aluminium', 'Labschool', '1Ci Enterprise', 'MBC Entertainment']) + '</div>'
              + '<div class="gs-stats"><div><b>2019</b><span>berdiri di Samarinda</span></div><div><b>50+</b><span>proyek selesai</span></div><div><b>13</b><span>tim inti in-house</span></div><div><b>3</b><span>kantor di Kaltim</span></div></div>'
              + '<div class="gs-links gs-center"><a href="/portfolio">Lihat portofolio</a><a href="/blog">Artikel & cerita</a></div>'),
    dict(k=1, room='Lobi', kicker='Lobi', title='Selamat datang di Altora',
         lead='Ceritakan kebutuhan Anda. Diskusi awal gratis, lalu kami susun rencana dan jadwalnya bersama.',
         img=P + 'hardware-field/kiosk-baqa-service.jpg',
         body='<div class="gs-contact"><a class="btn btn-purple" href="' + WA + '" rel="noopener" target="_blank">Chat WhatsApp</a><a class="btn btn-white" href="/contact">Kirim email</a></div>'
              '<div class="gs-offices"><div><b>Kantor pusat Samarinda</b><p>Perum Graha Indah Blok A13, Air Putih, Samarinda Ulu</p></div>'
              '<div><b>Cabang Balikpapan Utara</b><p>Jl. Soekarno Hatta, Muara Rapak, Balikpapan Utara</p></div>'
              '<div><b>Cabang Balikpapan Pasar Baru</b><p>Pasar Baru, Balikpapan</p></div></div>'),
]
ROOM_OF = {s['k']: s['room'] for s in SECTIONS}


def section(s):
    k = s['k']
    nxt = f'Turun ke lantai {k - 1} · {ROOM_OF[k - 1]}' if k > 1 else 'Keluar dari gedung'
    return (f'<section class="gs" data-k="{k}" id="lantai-{k}">'
            f'<div class="gs-cover" data-face="cover"><div class="gs-cover-in"><div class="gs-cover-copy"><p class="gs-kicker"><span>Lantai {k}</span>{e(s["kicker"])}</p>'
            f'<h2>{e(s["title"])}</h2><p class="gs-lead">{e(s["lead"])}</p><p class="gs-hint">Scroll ↓</p></div>'
            f'<figure class="gs-cover-pic"><img alt="" src="{s["img"]}"/></figure></div></div>'
            f'<div class="gs-body"><div class="gs-wrap">{s["body"]}</div></div>'
            f'<div class="gs-close" data-face="close"><div><p class="gs-kicker"><span>Lantai {k}</span>selesai</p><h3>{e(nxt)}</h3><p class="gs-arrow">↓</p></div></div>'
            '</section>')


body = ('<div class="gd-scene" data-scene="intro" data-to="7"><div class="gd-scene-in"><div class="gd-hero"><p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>'
        '<h1>Kami membangun sistem Anda, <span>lantai demi lantai.</span></h1><p>Scroll untuk masuk ke gedung kami ↓</p></div></div></div>')
for i, s in enumerate(SECTIONS):
    body += section(s)
    nxt = SECTIONS[i + 1]['k'] if i + 1 < len(SECTIONS) else 0
    body += (f'<div class="gd-scene" data-from="{s["k"]}" data-to="{nxt}"><div class="gd-scene-in">'
             + ('<div class="gd-outro-copy"><h2>Gedung kami terbuka untuk Anda.</h2><p>Kantor pusat di Samarinda, dua cabang di Balikpapan.</p></div>' if not nxt else '')
             + '</div></div>')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Preview: Gedung Altora</title><meta content="noindex,nofollow" name="robots"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>
<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="/assets/css/gedung-scenes.css?v=1"/></head>
<body class="company-page gd-body"><header></header>
<main class="gd2">
{body}
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}}}</script><script type="module" src="/assets/js/gedung3d.js?v=106"></script></body></html>
'''
(root / 'preview-gedung.html').write_text(page, encoding='utf-8')
print('preview-gedung.html dibuat')
