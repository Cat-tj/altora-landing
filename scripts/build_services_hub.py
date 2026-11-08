"""Halaman /services (hub): hero, katalog 9 layanan dengan kartu seragam, dan teks pendukung.
Bagian lain halaman (masalah umum, lokasi, ajakan) tetap dari services.html. Jalankan setelah build_services.py."""
import html, pathlib
from bs4 import BeautifulSoup

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(t, quote=True)
CARDS = [
    ('software-custom', 'Software custom', 'Aplikasi & sistem internal', 'Aplikasi dan sistem internal untuk proses yang tidak cocok dengan software jadi.', '/assets/img/apps/office-project.webp'),
    ('web-custom', 'Web custom', 'Portal & dashboard', 'Portal, dashboard, dan aplikasi web yang dibuat dari nol sesuai proses Anda.', '/assets/img/apps/office-board.webp'),
    ('mobile-app-custom', 'Aplikasi mobile custom', 'Android & iOS', 'Aplikasi Android dan iOS untuk tim lapangan, pelanggan, atau mitra.', '/assets/img/services/mobile.webp'),
    ('ai-custom', 'AI custom', 'Asisten & otomasi', 'Asisten AI, otomasi dokumen, analisis data, dan visi komputer untuk proses bisnis.', '/assets/img/services/ai.webp'),
    ('private-ai', 'AI lokal', 'Di server sendiri', 'Model AI yang berjalan di server Anda, tanpa data keluar jaringan.', '/assets/img/services/private-ai.webp'),
    ('iot-custom', 'IoT custom', 'Sensor & perangkat', 'Dasbor, peringatan, dan integrasi untuk sensor dan perangkat lapangan.', '/assets/img/services/iot.webp'),
    ('tracking', 'Tracking', 'Armada & aset', 'Pelacakan kendaraan dan aset: posisi, riwayat perjalanan, geofence, dan laporan.', '/assets/img/services/tracking.webp'),
    ('website-seo', 'Website', 'Company profile & instansi', 'Company profile, website instansi, dan landing page yang cepat dan mudah diperbarui.', '/assets/img/services/website.webp'),
    ('seo', 'SEO', 'Mudah ditemukan', 'Audit, perbaikan on-page, dan SEO lokal agar website ditemukan di Google.', '/assets/img/services/seo.webp'),
]
HERO = '''<section class="svh-hero"><div class="ct-wrap svh-wrap"><div class="pg-copy">
<p class="eyebrow eyebrow-purple">Layanan</p><h1>Software, AI, website, dan SEO untuk bisnis dan instansi.</h1>
<p class="ct-lead">Ceritakan masalahnya, kami bantu pilih solusinya: aplikasi web dan mobile, AI, IoT dan tracking, website, SEO, atau gabungannya.</p>
<div class="svd-actions"><a class="btn btn-purple" href="/contact">Konsultasi gratis</a><a class="svd-link" href="#layanan">Lihat layanan ↓</a></div>
</div></div></section>'''


def catalogue():
    cards = ''.join(f'''<a class="svc2-card" href="/services/{slug}"><span class="svc2-pic"><img alt="{e(name)}" loading="lazy" src="{img}"/></span>
<span class="svc2-body"><span class="svc2-top"><i>{n:02d}</i><em>{e(tag)}</em></span><b>{e(name)}</b><span class="svc2-desc">{e(desc)}</span><strong>Pelajari layanan →</strong></span></a>'''
                    for n, (slug, name, tag, desc, img) in enumerate(CARDS, 1))
    return f'''<section class="svc2-sec" id="layanan"><div class="ct-wrap"><div class="svc2-head"><div><p class="eyebrow eyebrow-purple">Pilih layanan</p><h2>Sembilan layanan, satu proyek</h2></div>
<p>Bisa diambil satu per satu atau digabung dalam satu proyek.</p></div><div class="svc2-grid">{cards}</div></div></section>'''


p = root / 'services.html'
soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
main = soup.find('main')
old = main.find('section', class_=['services-hero-v2', 'svh-hero'])
old.replace_with(BeautifulSoup(HERO, 'html.parser'))
for cls in ('services-intro', 'services-catalogue', 'svc2-sec'):
    for s in main.find_all('section', class_=cls):
        s.decompose()
main.find('section', class_='svh-hero').insert_after(BeautifulSoup(catalogue(), 'html.parser'))
txt = str(soup)
txt = txt.replace('Altora Office, Teams, dan Control Center, lengkap dengan screenshot.', 'FieldOps, Store, Office, Teams, Word, Sheets, Slides, dan Control Center.')
txt = txt.replace('<li>Aplikasi custom</li><li>Website</li><li>SEO</li><li>Dashboard dan laporan</li>', '<li>Aplikasi web &amp; mobile</li><li>AI custom &amp; AI lokal</li><li>IoT &amp; tracking</li><li>Website &amp; SEO</li>')
p.write_text(txt, encoding='utf-8')
print('services.html: hub layanan dibangun')
