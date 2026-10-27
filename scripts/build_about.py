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
    ('Software custom', 'Aplikasi web dan HP, sistem internal, dan integrasi, dibuat mengikuti proses kerja Anda.', 'code',
     ['Aplikasi web & mobile', 'Integrasi dengan sistem yang ada', 'Dashboard & laporan']),
    ('Website & SEO', 'Website company profile dan instansi yang cepat, mudah diperbarui, dan mudah ditemukan di Google.', 'brief',
     ['Website & CMS', 'SEO teknis & lokal', 'Konten & artikel']),
]
VALUES = [('Jelas', 'Lingkup, jadwal, dan tanggung jawab ditulis sejak awal.'), ('Terbuka', 'Progres ditunjukkan bertahap, bukan hanya di akhir.'),
          ('Bertanggung jawab', 'Satu penanggung jawab dari survei sampai serah terima.'), ('Berkelanjutan', 'Dukungan tetap ada setelah sistem dipakai.')]
STEPS = [('Konsultasi', 'Memahami kebutuhan dan tujuan Anda. Gratis.'), ('Analisis & rancangan', 'Pelajari alur kerja, lalu susun solusi.'),
         ('Penawaran', 'Proposal dan rencana kerja tertulis.'), ('Pengerjaan', 'Pengembangan bertahap dengan demo berkala.'),
         ('Serah terima & dukungan', 'Pelatihan pengguna dan dukungan setelah dipakai.')]
MOSAIC = ['/assets/img/apps/office-board.webp', '/assets/img/apps/office-project.webp', '/assets/img/apps/raphael-board.webp']
APPS = [('Altora Projek', 'Manajemen proyek dan tugas tim'), ('Altora Office', 'Operasional kantor: proyek, SDM, dan logistik'), ('Raphael Control Center', 'Pusat kendali server, website, dan agen AI')]
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
    apps = ''.join(f'<li><a href="/aplikasi"><b>{e(n)}</b><span>{e(d)}</span></a></li>' for n, d in APPS)
    offices = ''.join(f'<a class="ab-office" href="{e(maps_link(o))}" rel="noopener" target="_blank"><span class="ab-office-ico">{ico("pin")}</span>'
                      f'<span><small>{"Kantor pusat" if o["hq"] else "Cabang"}</small><b>{e(o["label"])}</b><span>{e(one_line(o))}</span><em>Buka di Google Maps →</em></span></a>' for o in OFFICES)
    msg = 'Halo Altora, saya ingin berdiskusi tentang kebutuhan software, website, atau SEO.'
    body = f'''<main class="ct-page ab-page">
<section class="ab-hero"><div class="ct-wrap ab-hero-grid">
<div class="ab-hero-copy"><p class="eyebrow eyebrow-purple">Tentang Altora</p>
<h1>Jasa pembuatan software, website, dan SEO untuk bisnis dan instansi.</h1>
<p class="ct-lead">Altora Indonesia berkantor pusat di Samarinda, dengan dua cabang di Balikpapan. Kami membuat aplikasi custom dan website sesuai kebutuhan Anda, lalu membantu agar mudah ditemukan di Google. Kami juga membangun dan memakai sendiri aplikasi seperti Altora Projek, Altora Office, dan Raphael Control Center.</p>
<div class="ab-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Diskusi dengan tim kami</a><a class="pd-link" href="/aplikasi">Lihat aplikasi kami →</a></div></div>
<div class="ab-mosaic" style="display:block"><img alt="Altora Office: papan proyek Kanban, aplikasi buatan Altora" src="{MOSAIC[0]}" style="object-position:left top"/></div>
</div></section>
<section class="ab-sec ab-stats-sec"><div class="ct-wrap"><div class="ts-stats">{stats}</div></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split">
<div><p class="eyebrow eyebrow-purple">Yang kami kerjakan</p><h2>Software, website, dan SEO, satu tim</h2><p class="ab-p">Dari analisis sampai dukungan, ditangani tim yang sama, jadi tidak ada saling lempar tanggung jawab antarvendor.</p></div>
<div class="ab-divs">{work}</div></div></section>
<section class="ab-sec ab-dark"><div class="ct-wrap ab-vm">
<div class="ab-vision"><p class="eyebrow">Cara kerja</p><ol class="ab-mission">{''.join(f'<li>{e(t)}: {e(d)}</li>' for t, d in STEPS)}</ol></div>
<div><p class="eyebrow">Prinsip kami</p><div class="ab-values">{values}</div></div></div></section>
<section class="ab-sec ab-soft"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Aplikasi buatan sendiri</p><h2>Kami memakai apa yang kami bangun</h2><p class="ab-p">Aplikasi yang kami kembangkan dan pakai sendiri untuk bekerja sehari-hari.</p></div>
<ul class="ab-apps">{apps}</ul></div></section>
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
                 'Altora Indonesia di Samarinda dan Balikpapan: jasa pembuatan software custom, website, dan SEO.',
                 '/about', SITE + MOSAIC[0], ld, body)


if __name__ == '__main__':
    (root / 'about.html').write_text(build(), encoding='utf-8')
    print('about.html dibuat')
