"""Prototipe landing 'gedung yang dibangun': /preview-gedung (noindex).
Gedung isometrik digambar sebagai SVG statis dari kode ini; scroll menyalakan lantai demi lantai (assets/js/gedung.js).
Jalankan lewat scripts/build_all.sh (atau: python3 scripts/build_gedung.py && python3 scripts/apply_shell.py)."""
import html, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
CSS_VER = '20261016i'

# ── Proyeksi isometrik ──
CX, CY = 300, 560
C30, S30 = 0.866, 0.5


def p(x, y, z=0):
    return (round(CX + (x - y) * C30, 1), round(CY + (x + y) * S30 - z, 1))


def poly(pts, cls='', extra=''):
    d = ' '.join(f'{a},{b}' for a, b in pts)
    return f'<polygon class="{cls}" points="{d}"{extra}/>'


HALF = 80          # setengah lebar tapak gedung
FLOOR_H = 70       # tinggi per lantai
BASE_H = 22        # fondasi

# lantai: (judul label, warna kiri, warna kanan, warna atas)
FLOORS = [
    ('Fondasi · Perangkat lapangan', '#3A3F78', '#2A2F5E', '#4A4F8C'),
    ('Lantai 1 · Jaringan & server', '#5B3FC4', '#4A31A8', '#7C5CE8'),
    ('Lantai 2 · Aplikasi Altora', '#7C5CE8', '#6447D6', '#9C84F5'),
    ('Lantai 3 · AI & dashboard', '#9C84F5', '#8468E8', '#C2B2FF'),
    ('Atap · Klien & hasil', '#C2B2FF', '#A892F5', '#E4DCFF'),
]


def floor_z(i):
    zb = 0 if i == 0 else BASE_H + (i - 1) * FLOOR_H
    zt = BASE_H if i == 0 else zb + FLOOR_H
    if i == len(FLOORS) - 1:
        zt = zb + 30  # atap lebih tipis
    return zb, zt


def box(zb, zt, cl, cr, ct, h=HALF):
    left = poly([p(-h, h, zb), p(h, h, zb), p(h, h, zt), p(-h, h, zt)], 'fl-left', f' fill="{cl}"')
    right = poly([p(h, -h, zb), p(h, h, zb), p(h, h, zt), p(h, -h, zt)], 'fl-right', f' fill="{cr}"')
    top = poly([p(-h, -h, zt), p(h, -h, zt), p(h, h, zt), p(-h, h, zt)], 'fl-top', f' fill="{ct}"')
    return left + right + top


def windows(zb, zt, n=4, h=HALF):
    out = ''
    zl, zh = zb + 16, zt - 16
    span = 2 * h / n
    for k in range(n):
        a, b = -h + k * span + 8, -h + (k + 1) * span - 8
        out += poly([p(a, h, zl), p(b, h, zl), p(b, h, zh), p(a, h, zh)], 'win')
        out += poly([p(h, a, zl), p(h, b, zl), p(h, b, zh), p(h, a, zh)], 'win win-r')
    return out


def floor_svg(i):
    name, cl, cr, ct = FLOORS[i]
    zb, zt = floor_z(i)
    g = box(zb, zt, cl, cr, ct)
    if 0 < i < len(FLOORS) - 1:
        g += windows(zb, zt)
    if i == len(FLOORS) - 1:  # atap: papan nama + antena
        ax, ay = p(0, 0, zt)
        g += f'<line class="ant" x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay - 70}"/>'
        g += f'<circle class="ant-dot" cx="{ax}" cy="{ay - 74}" r="6"/>'
        lx, ly = p(-40, 80, zb + 6)
        rx, ry = p(40, 80, zb + 6)
        g += f'<text class="roof-name" x="{(lx + rx) / 2:.1f}" y="{(ly + ry) / 2 - 2:.1f}" transform="rotate(30 {(lx + rx) / 2:.1f} {(ly + ry) / 2:.1f})">ALTORA</text>'
    # label di kanan
    mx, my = p(HALF, HALF / 2, (zb + zt) / 2)
    g += (f'<g class="fl-tag"><line x1="{mx + 6}" y1="{my}" x2="{560}" y2="{my}"/>'
          f'<text x="566" y="{my + 4}">{e(name)}</text></g>')
    # riser data di sudut depan (menyambung ke lantai bawah)
    fx, fy_b = p(HALF, HALF, zb)
    _, fy_t = p(HALF, HALF, zt)
    if i > 0:
        g += f'<line class="riser" x1="{fx}" y1="{fy_b + 2}" x2="{fx}" y2="{fy_t}"/>'
    bx, by = p(-HALF, HALF, zb)
    _, byt = p(-HALF, HALF, zt)
    if i > 0:
        g += f'<line class="riser riser-b" x1="{bx}" y1="{by}" x2="{bx}" y2="{byt}"/>'
    return f'<g class="fl" data-i="{i}">{g}</g>'


def ground():
    G = 150
    plate = poly([p(-G, -G), p(G, -G), p(G, G), p(-G, G)], 'plate')
    grid = ''
    for k in range(-G + 40, G, 40):
        grid += f'<line class="grid" x1="{p(k, -G)[0]}" y1="{p(k, -G)[1]}" x2="{p(k, G)[0]}" y2="{p(k, G)[1]}"/>'
        grid += f'<line class="grid" x1="{p(-G, k)[0]}" y1="{p(-G, k)[1]}" x2="{p(G, k)[0]}" y2="{p(G, k)[1]}"/>'
    # perangkat di tanah + kabel data ke gedung
    devs = [('cctv', -125, 30), ('truck', -30, 130), ('dish', 128, -5), ('sensor', 75, 120)]
    out = ''
    for kind, x, y in devs:
        sx, sy = p(x, y)
        tx, ty = p(max(-HALF, min(HALF, x)), max(-HALF, min(HALF, y)))
        out += f'<path class="cable" d="M{sx},{sy} L{tx},{ty}"/>'
        if kind == 'cctv':
            out += (f'<g class="dev"><line x1="{sx}" y1="{sy}" x2="{sx}" y2="{sy - 46}" class="pole"/>'
                    f'<rect x="{sx - 2}" y="{sy - 54}" width="22" height="11" rx="3" class="cam"/><circle cx="{sx + 18}" cy="{sy - 48.5}" r="2.6" class="lens"/></g>')
        elif kind == 'truck':
            out += (f'<g class="dev"><rect x="{sx - 22}" y="{sy - 22}" width="28" height="18" rx="3" class="body"/><rect x="{sx + 6}" y="{sy - 17}" width="14" height="13" rx="3" class="cab"/>'
                    f'<circle cx="{sx - 14}" cy="{sy - 3}" r="4" class="wheel"/><circle cx="{sx + 12}" cy="{sy - 3}" r="4" class="wheel"/></g>')
        elif kind == 'dish':
            out += (f'<g class="dev"><line x1="{sx}" y1="{sy}" x2="{sx}" y2="{sy - 18}" class="pole"/>'
                    f'<ellipse cx="{sx}" cy="{sy - 26}" rx="16" ry="8" class="dish" transform="rotate(-20 {sx} {sy - 26})"/></g>')
        else:
            out += (f'<g class="dev"><rect x="{sx - 7}" y="{sy - 20}" width="14" height="20" rx="4" class="sensor"/>'
                    f'<path class="wave" d="M{sx + 12},{sy - 18} q6,6 0,12 M{sx + 17},{sy - 22} q10,10 0,20"/></g>')
    return f'<g class="ground">{plate}{grid}</g><g class="devs">{out}</g>'


def crane():
    mx, my = p(130, -130, 0)
    top = 70
    zz = ''.join(f'{mx - 6 if k % 2 else mx + 6},{my - k * 16} ' for k in range(int((my - top) / 16) + 1))
    jz = ''.join(f'{x},{top + (0 if k % 2 else 10)} ' for k, x in enumerate(range(int(mx + 50), int(CX - 70), -14)))
    return (f'<g class="crane"><line class="mast" x1="{mx - 6}" y1="{my}" x2="{mx - 6}" y2="{top}"/><line class="mast" x1="{mx + 6}" y1="{my}" x2="{mx + 6}" y2="{top}"/>'
            f'<polyline class="lattice" points="{zz.strip()}"/>'
            f'<line class="jib" x1="{mx + 50}" y1="{top}" x2="{CX - 70}" y2="{top}"/><line class="jib" x1="{mx + 50}" y1="{top + 10}" x2="{CX - 70}" y2="{top + 10}"/>'
            f'<polyline class="lattice" points="{jz.strip()}"/>'
            f'<rect class="cw" x="{mx + 30}" y="{top + 10}" width="22" height="16" rx="2"/><rect class="cab" x="{mx - 12}" y="{top + 12}" width="24" height="18" rx="3"/>'
            f'<line class="hook" x1="{CX}" y1="{top + 10}" x2="{CX}" y2="{top + 60}"/>'
            f'<rect class="hook-box" x="{CX - 8}" y="{top + 60}" width="16" height="10" rx="2"/></g>')


def blueprint():
    zt = floor_z(len(FLOORS) - 1)[1]
    h = HALF
    out = poly([p(-h, h, 0), p(h, h, 0), p(h, h, zt), p(-h, h, zt)], 'bp')
    out += poly([p(h, -h, 0), p(h, h, 0), p(h, h, zt), p(h, -h, zt)], 'bp')
    out += poly([p(-h, -h, zt), p(h, -h, zt), p(h, h, zt), p(-h, h, zt)], 'bp')
    for i in range(1, len(FLOORS)):
        zb = floor_z(i)[0]
        out += f'<polyline class="bp" points="{p(-h, h, zb)[0]},{p(-h, h, zb)[1]} {p(h, h, zb)[0]},{p(h, h, zb)[1]} {p(h, -h, zb)[0]},{p(h, -h, zb)[1]}"/>'
    return f'<g class="blueprint">{out}</g>'



svg = (f'<svg class="gd-svg" viewBox="60 40 700 640" role="img" aria-label="Ilustrasi gedung Altora: fondasi perangkat, jaringan, aplikasi, AI, dan atap klien">'
       f'{ground()}{blueprint()}{crane()}' + ''.join(floor_svg(i) for i in range(len(FLOORS))) + '</svg>')

WA = 'https://wa.me/6285190911170?text=Halo%20Altora%2C%20saya%20ingin%20konsultasi.'
SECTIONS = [
    (0, 'Fondasi', 'Perangkat di lapangan', 'Semua dimulai dari yang menangkap kejadian nyata: kamera CCTV VIGI, GPS tracker Teltonika di kendaraan, sensor, smartlock, dan kios layanan.',
     [('/katalog-cctv-vigi', 'CCTV VIGI'), ('/katalog#cat-gps', 'GPS tracker'), ('/katalog#cat-akses', 'Smartlock'), ('/katalog#cat-kios', 'Kios layanan')]),
    (1, 'Lantai 1', 'Jaringan, server & internet', 'Data dari lapangan mengalir lewat jaringan yang rapi: LAN, WiFi, fiber optik, rak server, sampai Starlink untuk site terpencil.',
     [('/services/pengadaan-instalasi-maintenance', 'Jaringan & server'), ('/services/starlink-internet-satelit', 'Starlink'), ('/katalog#cat-rack', 'Rak server')]),
    (2, 'Lantai 2', 'Aplikasi Altora', 'Di sini data diolah menjadi pekerjaan: absensi dan SDM di Altora Teams, tugas di Altora Projek, dokumen dan rapat di Altora Office, armada di Altora FMS.',
     [('/produk/teams', 'Altora Teams'), ('/produk/projek', 'Altora Projek'), ('/produk/office', 'Altora Office'), ('/produk/fms', 'Altora FMS'), ('/produk/vision', 'Altora Vision')]),
    (3, 'Lantai 3', 'AI & dashboard', 'AI mengenali pelanggaran APD dari CCTV, asisten AI berjalan di server Anda sendiri, dan pimpinan melihat semuanya dari satu ruang kendali.',
     [('/produk/private-ai', 'Private AI & GIS'), ('/produk/command', 'Command center'), ('/services/ai-cctv', 'AI CCTV')]),
    (4, 'Atap', 'Dipakai klien kami', 'Gedung yang sama sudah berdiri untuk pemerintah daerah, kampus, dan perusahaan di Kalimantan Timur, dari Pemkot Samarinda sampai Universitas Mulawarman.',
     [('/portfolio', 'Lihat portofolio'), ('/about', 'Tentang Altora')]),
]
secs = ''
for i, kicker, title, text, links in SECTIONS:
    ls = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in links)
    extra = ''
    if i == 4:
        extra = ('<div class="gd-stats"><div><b>2019</b><span>berdiri</span></div><div><b>50+</b><span>proyek</span></div>'
                 '<div><b>13</b><span>tim inti</span></div><div><b>3</b><span>kantor</span></div></div>'
                 f'<a class="btn btn-purple" href="{WA}" rel="noopener" target="_blank">Mulai bangun bersama kami</a>')
    secs += (f'<section class="gd-sec" data-floor="{i}"><p class="gd-kicker"><span>{e(kicker)}</span></p><h2>{e(title)}</h2>'
             f'<p class="gd-text">{e(text)}</p><div class="gd-links">{ls}</div>{extra}</section>')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Preview: Gedung Altora</title><meta content="noindex,nofollow" name="robots"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>
<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>
<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="/assets/css/gedung.css?v=3"/></head>
<body class="company-page gd-body"><header></header>
<main class="gd-page" data-level="-1">
<div class="gd-layout">
<div class="gd-flow">
<section class="gd-sec gd-hero" data-floor="-1"><p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>
<h1>Kami membangun sistem Anda, <span>lantai demi lantai.</span></h1>
<p class="gd-text">Dari perangkat di lapangan sampai keputusan di dashboard. Setiap lantai saling terhubung, dikerjakan oleh satu tim.</p>
<div class="gd-actions"><a class="btn btn-purple" href="{WA}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="gd-scroll" href="#mulai">Scroll untuk membangun ↓</a></div></section>
<div id="mulai"></div>
{secs}
</div>
<div class="gd-stage" aria-hidden="false"><div class="gd-stage-inner">{svg}<div class="gd-progress"><span></span></div></div></div>
</div>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script><script defer="" src="/assets/js/gedung.js?v=3"></script></body></html>
'''
(root / 'preview-gedung.html').write_text(page, encoding='utf-8')
print('preview-gedung.html dibuat')
