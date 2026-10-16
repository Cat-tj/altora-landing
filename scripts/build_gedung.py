"""Prototipe landing 'halaman = gedung': /preview-gedung (noindex).
Alur: gedung utuh -> zoom in ke puncak, atap terangkat -> konten keluar dari tiap lantai (7 -> lobi) -> zoom out, footer di bawah gedung.
Gedung tampak depan digambar sebagai SVG dari kode ini; animasi di assets/js/gedung.js, gaya di assets/css/gedung.css.
Jalankan lewat scripts/build_all.sh (atau: python3 scripts/build_gedung.py && python3 scripts/apply_shell.py)."""
import html, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
CSS_VER = '20261016i'
WA = 'https://wa.me/6285190911170?text=Halo%20Altora%2C%20saya%20ingin%20konsultasi.'

# ── Gedung tampak depan (satuan SVG) ──
BW = 360            # lebar badan gedung
PIL = 14            # tebal pilar kiri/kanan
SLAB = 6            # tebal pelat lantai
FH = 60             # tinggi lantai
LOBBY = 80          # tinggi lobi
ROOF_Y = 70         # atap dari y=0 sampai 70
N = 7               # jumlah lantai


def floor_top(k):
    """y atas lantai k (7 = teratas, 1 = lobi)."""
    return ROOF_Y + (N - k) * FH


def floor_h(k):
    return LOBBY if k == 1 else FH


def building_svg(cls):
    g = []
    gy = floor_top(1) + LOBBY
    g.append(f'<rect class="b-ground" x="-220" y="{gy}" width="800" height="36" rx="4"/>')
    for tx in (-170, -110, 470, 530):
        g.append(f'<g class="b-tree"><rect x="{tx - 3}" y="{gy - 22}" width="6" height="22"/><circle cx="{tx}" cy="{gy - 32}" r="16"/></g>')
    for k in range(N, 0, -1):
        y, h = floor_top(k), floor_h(k)
        f = [f'<rect class="b-interior" x="0" y="{y}" width="{BW}" height="{h}"/>']
        glass = []
        if k == 1:
            glass.append(f'<rect class="b-glass" x="{PIL}" y="{y + SLAB}" width="{BW - 2 * PIL}" height="{h - SLAB}"/>')
            glass.append(f'<rect class="b-door" x="{BW / 2 - 34}" y="{y + 22}" width="68" height="{h - 22}" rx="3"/>')
            glass.append(f'<text class="b-lobby" x="{BW / 2}" y="{y + 17}">LOBI</text>')
        else:
            n, gap = 5, 6
            span = (BW - 2 * PIL - gap * (n + 1)) / n
            for i in range(n):
                x = PIL + gap + i * (span + gap)
                glass.append(f'<rect class="b-win" x="{x:.1f}" y="{y + SLAB + 8}" width="{span:.1f}" height="{h - SLAB - 16}" rx="2"/>')
        f.append(f'<g class="b-facade">{"".join(glass)}</g>')
        f.append(f'<rect class="b-pillar" x="0" y="{y}" width="{PIL}" height="{h}"/><rect class="b-pillar" x="{BW - PIL}" y="{y}" width="{PIL}" height="{h}"/>')
        f.append(f'<rect class="b-slab" x="0" y="{y}" width="{BW}" height="{SLAB}"/>')
        f.append(f'<text class="b-num" x="{PIL / 2}" y="{y + h / 2 + 4}">{k}</text>')
        g.append(f'<g class="b-floor" data-k="{k}">{"".join(f)}</g>')
    g.append('<g class="b-roof">'
             f'<rect class="b-parapet" x="-8" y="{ROOF_Y - 12}" width="{BW + 16}" height="12" rx="3"/>'
             f'<rect class="b-sign" x="{BW / 2 - 90}" y="{ROOF_Y - 52}" width="180" height="34" rx="8"/>'
             f'<text class="b-sign-t" x="{BW / 2}" y="{ROOF_Y - 29}">ALTORA</text>'
             f'<line class="b-ant" x1="{BW - 40}" y1="{ROOF_Y - 12}" x2="{BW - 40}" y2="{ROOF_Y - 66}"/><circle class="b-ant-dot" cx="{BW - 40}" cy="{ROOF_Y - 69}" r="5"/>'
             '</g>')
    return f'<svg class="{cls}" viewBox="-220 -10 800 {gy + 46}" aria-hidden="true">{"".join(g)}</svg>'


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
floors_html = ''
for k, kicker, title, text, links in FLOORS:
    ls = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in links)
    extra = ''
    if k == 2:
        extra = ('<div class="gf-stats"><div><b>2019</b><span>berdiri di Samarinda</span></div><div><b>50+</b><span>proyek selesai</span></div>'
                 '<div><b>13</b><span>tim inti</span></div><div><b>3</b><span>kantor di Kaltim</span></div></div>'
                 '<p class="gf-clients">Pemkot Samarinda · Pemkab Barito Utara · InJourney Airports · Universitas Mulawarman · Institut Teknologi Kalimantan · Adhi · Alba Aluminium · Labschool · 1Ci Enterprise · MBC Entertainment</p>')
    if k == 1:
        extra = f'<a class="btn btn-purple gf-cta" href="{WA}" rel="noopener" target="_blank">Chat WhatsApp</a>'
    floors_html += (f'<section class="gf" data-k="{k}"><div class="gf-hatch" aria-hidden="true"><i></i><i></i></div>'
                    f'<div class="gf-room"><div class="gf-copy"><p class="gf-kicker"><b>LT {k}</b>{e(kicker)}</p><h2>{e(title)}</h2><p>{e(text)}</p></div>'
                    f'<div class="gf-side"><div class="gf-links">{ls}</div>{extra}</div></div></section>')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Preview: Gedung Altora</title><meta content="noindex,nofollow" name="robots"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>
<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="/assets/css/gedung.css?v=11"/></head>
<body class="company-page gd-body"><header></header>
<main class="gd2">
<section class="gd-intro"><div class="gd-scene">
<div class="gd-hero"><p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>
<h1>Kami membangun sistem Anda, <span>lantai demi lantai.</span></h1>
<p>Scroll untuk masuk ke gedung kami ↓</p></div>
<div class="gd-bld">{building_svg('bld-svg')}</div><div class="gd-veil"></div>
</div></section>
<div class="gd-floors">{floors_html}</div>
<section class="gd-outro"><div class="gd-scene">
<div class="gd-veil"></div><div class="gd-bld gd-bld-out">{building_svg('bld-svg')}</div>
<div class="gd-outro-copy"><h2>Gedung kami terbuka untuk Anda.</h2><p>Kantor pusat di Samarinda, dua cabang di Balikpapan.</p></div>
</div></section>
<div class="gd-lift" aria-hidden="true"><span>▼</span><b>7</b></div>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="/assets/js/gedung.js?v=11"></script></body></html>
'''
(root / 'preview-gedung.html').write_text(page, encoding='utf-8')
print('preview-gedung.html dibuat')
