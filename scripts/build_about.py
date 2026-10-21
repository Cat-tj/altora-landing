"""Halaman /about. Jalankan lewat scripts/build_all.sh."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, SITE, WA
from build_trust import STATS
from site_data import OFFICES, one_line, maps_link

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
WORK = [
    ('Software custom & website', 'Aplikasi web dan HP, sistem internal, dan website yang disusun mengikuti proses kerja Anda.', 'code',
     ['Aplikasi web & mobile', 'Integrasi dengan sistem yang ada', 'Website & SEO']),
    ('Pengadaan hardware', 'Pengadaan perangkat dari principal resmi: CCTV, jaringan, komputer, kios, display, rak server, dan internet satelit.', 'chip',
     ['Pilih tipe yang sesuai', 'Pemasangan oleh teknisi', 'Garansi resmi & perawatan']),
]
VALUES = [('Jelas', 'Lingkup, jadwal, dan tanggung jawab ditulis sejak awal.'), ('Terbuka', 'Progres ditunjukkan bertahap, bukan hanya di akhir.'),
          ('Bertanggung jawab', 'Satu penanggung jawab dari survei sampai serah terima.'), ('Berkelanjutan', 'Dukungan tetap ada setelah sistem dipakai.')]
STEPS = [('Konsultasi', 'Memahami kebutuhan dan tujuan Anda. Gratis.'), ('Survei & rancangan', 'Cek lokasi atau alur kerja, lalu susun solusi.'),
         ('Penawaran', 'Proposal dan rencana kerja tertulis.'), ('Pengerjaan', 'Pengembangan aplikasi atau pemasangan perangkat.'),
         ('Serah terima & dukungan', 'Pelatihan pengguna dan dukungan setelah dipakai.')]
PARTNERS = [('tplink-v2', 'TP-Link'), ('vigi-v2', 'VIGI'), ('teltonika-v2', 'Teltonika'), ('lenovo-v2', 'Lenovo'),
            ('hde-v2', 'HDe'), ('haganerack-v2', 'HaganeRack'), ('fasser-v2', 'Fasser')]
MOSAIC = ['/assets/img/hardware/lenovo-thinkpad-t14.webp', '/assets/img/vigi/c340i.webp', '/assets/img/hardware/hr-close-glass.webp']
ICO = {
    'brief': '<rect height="13" rx="2" width="18" x="3" y="7"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/>',
    'chip': '<rect height="12" rx="2" width="12" x="6" y="6"/><path d="M9.5 9.5h5v5h-5zM9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    'code': '<path d="m9 8-4 4 4 4M15 8l4 4-4 4M13 6l-2 12"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
}
ico = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICO[n]}</svg>'


def build():
    stats = ''.join(f'<div><b>{e(v)}</b><span>{e(k)}</span></div>' for v, k in STATS)
    work = ''.join(f'<article class="ab-div"><span class="ab-div-ico">{ico(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p>'
                   '<ul>' + ''.join(f'<li>{e(x)}</li>' for x in pts) + '</ul></article>' for t, d, i, pts in WORK)
    steps = ''.join(f'<li><span class="ab-tl-year">{n}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for n, (t, d) in enumerate(STEPS, 1))
    values = ''.join(f'<div><b>{e(t)}</b><p>{e(d)}</p></div>' for t, d in VALUES)
    partners = ''.join(f'<li><img alt="{e(n)}" loading="lazy" src="/assets/img/partners/{f}.png"/></li>' for f, n in PARTNERS)
    offices = ''.join(f'<a class="ab-office" href="{e(maps_link(o))}" rel="noopener" target="_blank"><span class="ab-office-ico">{ico("pin")}</span>'
                      f'<span><small>{"Kantor pusat" if o["hq"] else "Cabang"}</small><b>{e(o["label"])}</b><span>{e(one_line(o))}</span><em>Buka di Google Maps →</em></span></a>' for o in OFFICES)
    msg = 'Halo Altora, saya ingin berdiskusi tentang kebutuhan software atau pengadaan hardware.'
    body = f'''<main class="ct-page ab-page">
<section class="ab-hero"><div class="ct-wrap ab-hero-grid">
<div class="ab-hero-copy"><p class="eyebrow eyebrow-purple">Tentang Altora</p>
<h1>Jasa pembuatan software dan pengadaan hardware untuk bisnis dan instansi.</h1>
<p class="ct-lead">Altora Indonesia berkantor pusat di Samarinda, dengan dua cabang di Balikpapan. Kami membuat aplikasi dan website sesuai kebutuhan Anda, serta mengadakan, memasang, dan merawat perangkat dari principal resmi.</p>
<div class="ab-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Diskusi dengan tim kami</a><a class="pd-link" href="/services">Lihat layanan →</a></div></div>
<div class="ab-mosaic"><img alt="Laptop dan perangkat kerja" class="ab-m1" src="{MOSAIC[0]}"/><img alt="Kamera CCTV VIGI" class="ab-m2" src="{MOSAIC[1]}"/><img alt="Rak server" class="ab-m3" src="{MOSAIC[2]}"/></div>
</div></section>
<section class="ab-sec ab-stats-sec"><div class="ct-wrap"><div class="ts-stats">{stats}</div></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split">
<div><p class="eyebrow eyebrow-purple">Yang kami kerjakan</p><h2>Software dan hardware, satu pintu</h2><p class="ab-p">Banyak kebutuhan melibatkan aplikasi sekaligus perangkat. Dengan satu pintu, tidak ada saling lempar tanggung jawab antarvendor.</p></div>
<div class="ab-divs">{work}</div></div></section>
<section class="ab-sec ab-dark"><div class="ct-wrap ab-vm">
<div class="ab-vision"><p class="eyebrow">Cara kerja</p><ol class="ab-mission">{''.join(f'<li>{e(t)}: {e(d)}</li>' for t, d in STEPS)}</ol></div>
<div><p class="eyebrow">Prinsip kami</p><div class="ab-values">{values}</div></div></div></section>
<section class="ab-sec ab-soft"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Principal</p><h2>Perangkat resmi dengan garansi</h2><p class="ab-p">Kami memilihkan yang paling cocok untuk lokasi Anda, tanpa mengunci Anda pada satu merek.</p></div>
<ul class="ab-partners">{partners}</ul></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split ab-split-even">
<div class="ab-legal"><p class="eyebrow eyebrow-purple">Legalitas</p><h2>Resmi dan siap tender</h2>
<ul><li>Badan usaha resmi berstatus PKP</li><li>Terdaftar sebagai penyedia di Inaproc / LKPP</li><li>Kontrak, faktur pajak, dan berita acara di setiap pekerjaan</li></ul></div>
<div><p class="eyebrow eyebrow-purple">Kantor</p><h2>Datang ke kantor kami</h2><div class="ab-offices">{offices}</div></div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Siap mulai? Ceritakan kebutuhan Anda.</h2><p>Konsultasi gratis, tanpa kewajiban lanjut.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a></div></section>
</main>'''
    ld = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'Tentang Altora Indonesia', 'url': SITE + '/about',
          'mainEntity': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': SITE + '/',
                         'logo': SITE + '/assets/img/altora-logo-600.png'}}
    return shell('Tentang Altora Indonesia | Samarinda & Balikpapan',
                 'Altora Indonesia di Samarinda dan Balikpapan: jasa pembuatan software dan website, serta pengadaan hardware dari principal resmi.',
                 '/about', SITE + MOSAIC[0], ld, body)


if __name__ == '__main__':
    (root / 'about.html').write_text(build(), encoding='utf-8')
    print('about.html dibuat')
