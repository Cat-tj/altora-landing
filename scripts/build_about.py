"""Halaman /about. Jalankan lewat scripts/build_all.sh."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, SITE, WA
from build_trust import CLIENTS, logo_tile, STATS
from site_data import OFFICES, one_line, maps_link, FACTS

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
P = '/assets/img/portfolio/'

DIVISIONS = [
    ('Bisnis & solusi', 'Konsultasi kebutuhan, desain solusi dan RAB, pengadaan, sampai manajemen proyek.', 'brief',
     ['Survei & konsultasi', 'RAB transparan', 'Manajemen proyek']),
    ('Hardware & IoT', 'Survei titik, pemasangan CCTV, sensor, GPS tracker, jaringan, dan kelistrikan oleh teknisi sendiri.', 'chip',
     ['CCTV & akses pintu', 'GPS & sensor', 'Jaringan & listrik']),
    ('Software & AI', 'Pengembangan web, aplikasi HP, sistem terintegrasi, sampai AI yang berjalan di server Anda.', 'code',
     ['Web & mobile app', 'Integrasi sistem', 'AI on-premise']),
]
VALUES = [('Integritas', 'Jujur pada klien, transparan pada hasil.'), ('Kolaborasi', 'Bekerja sebagai mitra, bukan sekadar vendor.'),
          ('Berdampak', 'Teknologi yang benar-benar dipakai setiap hari.'), ('Bertumbuh', 'Terus belajar mengikuti perkembangan teknologi.')]
MISSION = ['Solusi yang inovatif, bisa berkembang, dan mudah dipakai di web, desktop, maupun HP.',
           'Mutu lewat proses yang terstruktur dan terdokumentasi, dari survei sampai purnajual.',
           'Hubungan jangka panjang atas dasar kepercayaan.',
           'Menjadi pusat talenta teknologi di Kalimantan Timur.']
TIMELINE = [
    ('2019', 'Berdiri di Samarinda', 'Mulai dari pengembangan website dan aplikasi untuk kampus dan usaha lokal.'),
    ('Tumbuh', 'Masuk ke perangkat & IoT', 'CCTV, jaringan, GPS tracker, dan kios layanan, dipasang dan dirawat tim sendiri.'),
    ('2024', 'Badan usaha resmi & siap tender', 'Berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.'),
    ('Kini', 'Tiga kantor di Kalimantan Timur', 'Kantor pusat di Samarinda, dua cabang di Balikpapan, 50+ proyek selesai.'),
    ('2026', 'Membina talenta muda', 'Membimbing tim SMP Negeri 5 Balikpapan hingga Juara 2 Nasional Innovakids.'),
]
PARTNERS = [('tplink-v2', 'TP-Link'), ('vigi-v2', 'VIGI'), ('teltonika-v2', 'Teltonika'), ('lenovo-v2', 'Lenovo'),
            ('hde-v2', 'HDe'), ('haganerack-v2', 'HaganeRack'), ('fasser-v2', 'Fasser'), ('itk-v2', 'Institut Teknologi Kalimantan')]
GALLERY = [('/assets/img/services/team-podium-system-demo.png', 'Presentasi sistem di depan pengguna'),
           (P + 'hardware-field/serah-terima-raya-makmur.jpg', 'Serah terima perangkat di kelurahan'),
           (P + 'kiosk-samarinda/kiosk-workshop.jpg', 'Perakitan dan uji kios'),
           (P + 'pompy-coordination/malang-command-center-02.png', 'Rapat koordinasi proyek')]
ICO = {
    'brief': '<rect height="13" rx="2" width="18" x="3" y="7"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/>',
    'chip': '<rect height="12" rx="2" width="12" x="6" y="6"/><path d="M9.5 9.5h5v5h-5zM9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    'code': '<path d="m9 8-4 4 4 4M15 8l4 4-4 4M13 6l-2 12"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
}
ico = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICO[n]}</svg>'


def build():
    stats = ''.join(f'<div><b>{e(v)}</b><span>{e(k)}</span></div>' for v, k in STATS)
    divs = ''.join(f'<article class="ab-div"><span class="ab-div-ico">{ico(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p>'
                   '<ul>' + ''.join(f'<li>{e(x)}</li>' for x in pts) + '</ul></article>' for t, d, i, pts in DIVISIONS)
    tl = ''.join(f'<li><span class="ab-tl-year">{e(y)}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for y, t, d in TIMELINE)
    mission = ''.join(f'<li>{e(m)}</li>' for m in MISSION)
    values = ''.join(f'<div><b>{e(t)}</b><p>{e(d)}</p></div>' for t, d in VALUES)
    logos = ''.join(logo_tile(*c) for c in CLIENTS)
    partners = ''.join(f'<li><img alt="{e(n)}" loading="lazy" src="/assets/img/partners/{f}.png"/></li>' for f, n in PARTNERS)
    gallery = ''.join(f'<figure><img alt="{e(c)}" loading="lazy" src="{s}"/><figcaption>{e(c)}</figcaption></figure>' for s, c in GALLERY)
    offices = ''.join(f'<a class="ab-office" href="{e(maps_link(o))}" rel="noopener" target="_blank"><span class="ab-office-ico">{ico("pin")}</span>'
                      f'<span><small>{"Kantor pusat" if o["hq"] else "Cabang"}</small><b>{e(o["label"])}</b><span>{e(one_line(o))}</span><em>Buka di Google Maps →</em></span></a>' for o in OFFICES)
    msg = 'Halo Altora, saya ingin berdiskusi tentang kebutuhan teknologi kami.'
    body = f'''<main class="ct-page ab-page">
<section class="ab-hero"><div class="ct-wrap ab-hero-grid">
<div class="ab-hero-copy"><p class="eyebrow eyebrow-purple">Tentang Altora</p>
<h1>Kami merancang, memasang, dan merawat teknologi yang dipakai setiap hari.</h1>
<p class="ct-lead">Altora Indonesia berdiri sejak {FACTS["founded"]} di Samarinda, dengan cabang di Balikpapan. Kami membuat aplikasi, website, CCTV pintar, dan sistem armada, lalu mengadakan, memasang, dan merawat perangkatnya. Semua dikerjakan tim sendiri, jadi Anda selalu tahu siapa yang bertanggung jawab.</p>
<div class="ab-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Diskusi dengan tim kami</a><a class="pd-link" href="/portfolio">Lihat portofolio →</a></div></div>
<div class="ab-mosaic"><img alt="Tim Altora mempresentasikan sistem" class="ab-m1" src="{GALLERY[0][0]}"/><img alt="Serah terima perangkat" class="ab-m2" src="{GALLERY[1][0]}"/><img alt="Perakitan kios" class="ab-m3" src="{GALLERY[2][0]}"/></div>
</div></section>
<section class="ab-sec ab-stats-sec"><div class="ct-wrap"><div class="ts-stats">{stats}</div></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split">
<div><p class="eyebrow eyebrow-purple">Cara kami bekerja</p><h2>Tiga divisi, satu tim</h2><p class="ab-p">Tidak ada saling lempar tanggung jawab antarvendor. Dari survei pertama sampai dukungan setelah serah terima, semuanya ditangani tim yang sama.</p></div>
<div class="ab-divs">{divs}</div></div></section>
<section class="ab-sec ab-dark"><div class="ct-wrap ab-vm">
<div class="ab-vision"><p class="eyebrow">Visi</p><blockquote>Menjadi mitra strategis bisnis dan instansi dalam transformasi digital, dengan solusi AI, IoT, dan software yang membuat operasional lebih efisien.</blockquote>
<p class="eyebrow ab-mt">Misi</p><ol class="ab-mission">{mission}</ol></div>
<div><p class="eyebrow">Nilai kami</p><div class="ab-values">{values}</div></div></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split">
<div><p class="eyebrow eyebrow-purple">Perjalanan</p><h2>Dari Samarinda, untuk Kalimantan Timur</h2><p class="ab-p">Kami tumbuh bersama klien: mulai dari website dan aplikasi, lalu ke perangkat, IoT, dan AI yang terpasang di lapangan.</p></div>
<ol class="ab-tl">{tl}</ol></div></section>
<section class="ab-sec ab-soft"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Di lapangan</p><h2>Bukan mockup: tim kami di lokasi klien</h2></div><div class="ab-gallery">{gallery}</div></div></section>
<section class="ab-sec"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Klien</p><h2>Dipercaya oleh</h2><p class="ab-p">Sebagian klien mempercayakan lebih dari satu proyek. Dengan persetujuan klien, kami bisa memfasilitasi kontak referensi atau kunjungan lokasi.</p></div>
<ul class="tl-grid">{logos}</ul></div></section>
<section class="ab-sec ab-soft"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Partner</p><h2>Principal resmi & kolaborasi riset</h2><p class="ab-p">Perangkat asli dengan garansi resmi. Kami tetap memilihkan yang paling cocok, tanpa mengunci Anda pada satu merek.</p></div>
<ul class="ab-partners">{partners}</ul></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split ab-split-even">
<div class="ab-legal"><p class="eyebrow eyebrow-purple">Legalitas</p><h2>Resmi dan siap tender</h2>
<ul><li>Badan usaha resmi berstatus PKP</li><li>Terdaftar sebagai penyedia di Inaproc / LKPP</li><li>Kontrak, RAB, faktur pajak, dan berita acara di setiap proyek</li><li>Kolaborasi riset dengan Institut Teknologi Kalimantan</li></ul></div>
<div><p class="eyebrow eyebrow-purple">Kantor</p><h2>Datang ke kantor kami</h2><div class="ab-offices">{offices}</div></div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Siap mulai? Ceritakan kebutuhan Anda.</h2><p>Konsultasi dan survei lokasi gratis, tanpa kewajiban lanjut.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a></div></section>
</main>'''
    ld = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'Tentang Altora Indonesia', 'url': SITE + '/about',
          'mainEntity': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': SITE + '/', 'foundingDate': FACTS['founded'],
                         'foundingLocation': 'Samarinda', 'logo': SITE + '/assets/img/altora-logo-600.png'}}
    return shell('Tentang Altora Indonesia | Samarinda & Balikpapan',
                 'Altora Indonesia berdiri sejak 2019 di Samarinda dengan cabang di Balikpapan. Aplikasi, website, CCTV pintar, dan perangkat, dikerjakan satu tim.',
                 '/about', SITE + GALLERY[0][0], ld, body)


if __name__ == '__main__':
    (root / 'about.html').write_text(build(), encoding='utf-8')
    print('about.html dibuat')
