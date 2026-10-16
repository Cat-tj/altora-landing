"""Prototipe landing 'halaman = gedung': /preview-gedung (noindex).
Alur: gedung utuh -> zoom in ke puncak, atap terangkat -> konten keluar dari tiap lantai (7 -> lobi) -> zoom out, footer di bawah gedung.
Gedung tampak depan digambar sebagai SVG dari kode ini; animasi di assets/js/gedung.js, gaya di assets/css/gedung.css.
Jalankan lewat scripts/build_all.sh (atau: python3 scripts/build_gedung.py && python3 scripts/apply_shell.py)."""
import html, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
CSS_VER = '20261016i'
WA = 'https://wa.me/6285190911170?text=Halo%20Altora%2C%20saya%20ingin%20konsultasi.'

# ── Gedung 3D (CSS 3D: setiap lantai = kotak dengan sisi depan, samping, belakang) ──
W3, D3, FH3, LOBBY3, N = 240, 170, 58, 74, 7
TOTAL3 = LOBBY3 + (N - 1) * FH3
LIT = {7: (60, 130), 6: (130,), 5: (20, 170), 4: (95,), 3: (60, 165), 2: (20, 130), 1: ()}


def building3d(cls=''):
    """Setiap lantai = kotak terbuka di atas: pelat lantai, dinding luar depan & kanan (berjendela),
    dinding dalam belakang & kiri (terlihat saat atap/lantai di atasnya dikupas)."""
    fl = ''
    for k in range(1, N + 1):
        h = LOBBY3 if k == 1 else FH3
        y = 0 if k == 1 else LOBBY3 + (k - 2) * FH3
        lit = ''.join(f'<b style="left:{x}px"></b>' for x in LIT[k])
        lit_r = ''.join(f'<b style="left:{round(x * D3 / W3)}px"></b>' for x in LIT[k][:1])
        fl += (f'<div class="bx3-floor{" bx3-lobby" if k == 1 else ""}" data-k="{k}" style="--y:{y}px;--h:{h}px">'
               '<i class="fc fc-plate"></i>'
               f'<i class="fc fc-front">{lit}{"<em>LOBI</em><s></s>" if k == 1 else ""}</i><i class="fc fc-right">{lit_r}</i>'
               '<i class="fc fc-backin"></i><i class="fc fc-leftin"></i>'
               '</div>')
    return (f'<div class="bx3 {cls}" style="--W:{W3}px;--D:{D3}px;--T:{TOTAL3}px"><div class="bx3-world">'
            '<div class="bx3-ground"></div>'
            f'{fl}'
            '<div class="bx3-roof"><i class="bx3-roof-plane"></i><i class="bx3-sign">ALTORA</i></div>'
            '</div></div>')


# ── Isi tiap lantai (dari atas ke bawah) ──
FLOORS = [
    (7, 'Layanan', 'Yang kami bangun untuk Anda', 'Aplikasi, website, CCTV pintar, jaringan, sampai pengadaan perangkat. Satu tim dari konsultasi sampai perawatan.',
     [('/services/software-custom', 'Aplikasi & sistem internal'), ('/services/website-seo', 'Website & SEO'), ('/services/ai-cctv', 'AI & CCTV pintar'),
      ('/services/iot-command-center', 'IoT & akses pintar'), ('/services/pengadaan-instalasi-maintenance', 'Pengadaan & instalasi'),
      ('/services/fleet-management-service', 'Armada & GPS tracker'), ('/services/starlink-internet-satelit', 'Starlink & internet site')]),
    (6, 'Aplikasi Altora', 'Siap dipakai tim Anda', 'SDM di Altora Teams, tugas di Altora Projek, dokumen dan rapat di Altora Office, armada di Altora FMS, dan CCTV pintar di Altora Vision.',
     [('/produk/teams', 'Altora Teams'), ('/produk/projek', 'Altora Projek'), ('/produk/office', 'Altora Office'), ('/produk/fms', 'Altora FMS'),
      ('/produk/vision', 'Altora Vision'), ('/produk/pass', 'Altora Pass')]),
    (5, 'AI & ruang kendali', 'Keputusan dari satu layar', 'AI mengenali pelanggaran APD dari CCTV, asisten AI berjalan di server Anda sendiri, dan pimpinan memantau semuanya dari ruang kendali.',
     [('/produk/private-ai', 'Private AI & GIS'), ('/produk/command', 'Command center'), ('/produk/attendance', 'Absensi wajah')]),
    (4, 'Jaringan & server', 'Jalur data yang rapi', 'LAN, WiFi, fiber optik, rak server, sampai Starlink untuk site terpencil. Dipasang, diuji, dan didokumentasikan.',
     [('/jasa-instalasi-jaringan-samarinda', 'Instalasi jaringan'), ('/katalog#cat-rack', 'Rak server'), ('/katalog#cat-konek', 'Starlink'), ('/katalog#cat-fiber', 'Fiber optik')]),
    (3, 'Perangkat lapangan', 'Mata dan telinga di lokasi', 'Kamera CCTV VIGI, GPS tracker Teltonika, sensor, smartlock, dan kios layanan dari principal resmi.',
     [('/katalog-cctv-vigi', 'Katalog CCTV VIGI'), ('/katalog#cat-gps', 'GPS tracker'), ('/katalog#cat-akses', 'Smartlock'), ('/katalog', 'Semua katalog')]),
    (2, 'Klien & bukti', 'Sudah berdiri di banyak tempat', 'Pemerintah daerah, kampus, dan perusahaan di Kalimantan Timur mempercayakan sistemnya kepada kami.',
     [('/portfolio', 'Lihat portofolio'), ('/blog', 'Artikel & cerita'), ('/about', 'Tentang Altora')]),
    (1, 'Lobi', 'Selamat datang di Altora', 'Ceritakan kebutuhan Anda. Diskusi awal gratis, lalu kami susun rencana dan jadwalnya bersama.',
     [('/contact', 'Kirim email'), ('/support', 'Butuh bantuan teknis')]),
]
cards = ''
for k, kicker, title, text, links in FLOORS:
    ls = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in links)
    extra = ''
    if k == 2:
        extra = ('<div class="gc-stats"><div><b>2019</b><span>berdiri di Samarinda</span></div><div><b>50+</b><span>proyek selesai</span></div>'
                 '<div><b>13</b><span>tim inti</span></div><div><b>3</b><span>kantor di Kaltim</span></div></div>')
    if k == 1:
        extra = f'<a class="btn btn-purple gc-cta" href="{WA}" rel="noopener" target="_blank">Chat WhatsApp</a>'
    cards += (f'<article class="gc" data-k="{k}"><p class="gc-kicker">{e(kicker)}</p><h2>{e(title)}</h2><p class="gc-text">{e(text)}</p>'
              f'<div class="gc-links">{ls}</div>{extra}</article>')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Preview: Gedung Altora</title><meta content="noindex,nofollow" name="robots"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>
<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="/assets/css/gedung.css?v=60"/></head>
<body class="company-page gd-body"><header></header>
<main class="gd2">
<section class="gd-story"><div class="gd-stage">
<div class="gd-hero"><p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>
<h1>Kami membangun sistem Anda, <span>lantai demi lantai.</span></h1>
<p>Scroll untuk masuk ke gedung kami ↓</p></div>
{building3d('bx3-in')}
<div class="gd-cards">{cards}</div>
<div class="gd-outro-copy"><h2>Gedung kami terbuka untuk Anda.</h2><p>Kantor pusat di Samarinda, dua cabang di Balikpapan.</p></div>
</div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}}}</script><script type="module" src="/assets/js/gedung3d.js?v=8"></script></body></html>
'''
(root / 'preview-gedung.html').write_text(page, encoding='utf-8')
print('preview-gedung.html dibuat')
