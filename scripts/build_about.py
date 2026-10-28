"""Halaman /about. Jalankan lewat scripts/build_all.sh."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, SITE, WA
from build_trust import STATS
from site_data import OFFICES, one_line, maps_link, org, office_node

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
COLLAGE = ['/assets/img/apps/office-board.webp', '/assets/img/apps/teams-overview.webp', '/assets/img/apps/word-main.webp']
MOSAIC = ['/assets/img/apps/office-board.webp', '/assets/img/apps/office-project.webp', '/assets/img/apps/control-center-board.webp']
APPS = [('fieldops', 'Altora FieldOps', 'Operasional lapangan tambang dan migas', 'fieldops-overview'), ('office', 'Altora Office', 'Proyek, tugas, dan operasional kantor', 'office-board'), ('teams', 'Altora Teams', 'KPI, cuti, dan kalender kerja tim', 'teams-overview'),
        ('control-center', 'Altora Control Center', 'Pusat kendali server, website, dan proyek', 'control-center-board'), ('word', 'Altora Word', 'Pengolah kata dengan format .docx', 'word-main'),
        ('sheets', 'Altora Sheets', 'Lembar kerja dengan rumus dan grafik', 'sheets-main')]
SERVICES = [('software-custom', 'Software custom', 'Aplikasi dan sistem internal mengikuti proses Anda.'), ('web-custom', 'Web custom', 'Portal, dashboard, dan aplikasi web dari nol.'),
            ('mobile-app-custom', 'Aplikasi mobile', 'Android dan iOS untuk tim lapangan dan pelanggan.'), ('ai-custom', 'AI custom', 'Asisten, otomasi dokumen, analisis data, visi komputer.'),
            ('private-ai', 'AI lokal', 'Model AI di server Anda, data tidak keluar.'), ('iot-custom', 'IoT custom', 'Sensor dan perangkat terhubung ke aplikasi.'),
            ('tracking', 'Tracking', 'Pelacakan kendaraan, armada, dan aset.'), ('website-seo', 'Website', 'Company profile dan website instansi.'), ('seo', 'SEO', 'Audit, on-page, dan SEO lokal.')]
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
    apps = ''.join(f'<a class="ab-app" href="/aplikasi/{k}"><span class="ab-app-pic"><img alt="{e(n)}" loading="lazy" src="/assets/img/apps/{im}.webp"/></span><b>{e(n)}</b><span>{e(d)}</span></a>' for k, n, d, im in APPS)
    svcs = ''.join(f'<a class="ab-svc" href="/services/{k}"><i>{n:02d}</i><b>{e(t)}</b><span>{e(d)}</span></a>' for n, (k, t, d) in enumerate(SERVICES, 1))
    collage = ''.join(f'<figure class="ap2-shot ab-c{i}"><div class="ap2-bar"><i></i><i></i><i></i></div><img alt="" {"" if i == 1 else "loading=lazy "}src="{u}"/></figure>' for i, u in enumerate(COLLAGE, 1))
    offices = ''.join(f'<a class="ab-office" href="{e(maps_link(o))}" rel="noopener" target="_blank"><span class="ab-office-ico">{ico("pin")}</span>'
                      f'<span><small>{"Kantor pusat" if o["hq"] else "Cabang"}</small><b>{e(o["label"])}</b><span>{e(one_line(o))}</span><em>Buka di Google Maps →</em></span></a>' for o in OFFICES)
    msg = 'Halo Altora, saya ingin berdiskusi tentang kebutuhan software, website, atau SEO.'
    body = f'''<main class="ct-page ab-page">
<section class="ab-hero"><div class="ct-wrap ab-hero-grid">
<div class="ab-hero-copy"><p class="eyebrow eyebrow-purple">Tentang Altora</p>
<h1>Jasa pembuatan software, website, dan SEO untuk bisnis dan instansi.</h1>
<p class="ct-lead">Altora Indonesia berkantor pusat di Samarinda, dengan dua cabang di Balikpapan. Kami membuat aplikasi custom dan website sesuai kebutuhan Anda, lalu membantu agar mudah ditemukan di Google. Kami juga membangun dan memakai sendiri aplikasi seperti Altora Office, Altora Teams, dan Altora Control Center.</p>
<div class="ab-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Diskusi dengan tim kami</a><a class="pd-link" href="/aplikasi">Lihat aplikasi kami →</a></div></div>
<div class="ab-collage">{collage}</div>
</div></section>
<section class="ab-sec ab-stats-sec"><div class="ct-wrap"><div class="ts-stats">{stats}</div></div></section>
<section class="ab-sec"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Yang kami kerjakan</p><h2>Dari ide sampai aplikasi yang dipakai</h2><p class="ab-p">Sembilan layanan software dan digital, bisa diambil satu per satu atau digabung dalam satu proyek.</p></div>
<div class="ab-svcs">{svcs}</div></div></section>
<section class="ab-sec ab-dark"><div class="ct-wrap ab-vm">
<div class="ab-vision"><p class="eyebrow">Cara kerja</p><ol class="ab-mission">{''.join(f'<li>{e(t)}: {e(d)}</li>' for t, d in STEPS)}</ol></div>
<div><p class="eyebrow">Prinsip kami</p><div class="ab-values">{values}</div></div></div></section>
<section class="ab-sec ab-soft"><div class="ct-wrap"><div class="ab-head"><p class="eyebrow eyebrow-purple">Aplikasi buatan sendiri</p><h2>Lebih dari 20 aplikasi, kami pakai sendiri</h2><p class="ab-p">Beberapa yang paling sering kami tunjukkan ke klien. Setiap aplikasi bisa didemokan dan disesuaikan.</p></div>
<div class="ab-appgrid">{apps}</div><p class="ab-more"><a class="pd-link" href="/aplikasi">Lihat semua aplikasi →</a></p></div></section>
<section class="ab-sec"><div class="ct-wrap ab-split ab-split-even">
<div class="ab-legal"><p class="eyebrow eyebrow-purple">Legalitas</p><h2>Resmi dan siap tender</h2>
<ul><li>Badan usaha resmi berstatus PKP</li><li>Terdaftar sebagai penyedia di Inaproc / LKPP</li><li>Kontrak, faktur pajak, dan berita acara di setiap pekerjaan</li></ul></div>
<div><p class="eyebrow eyebrow-purple">Kantor</p><h2>Datang ke kantor kami</h2><div class="ab-offices">{offices}</div></div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Siap mulai? Ceritakan kebutuhan Anda.</h2><p>Konsultasi gratis, tanpa kewajiban lanjut.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a></div></section>
</main>'''
    ld = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'Tentang Altora Indonesia', 'url': SITE + '/about',
          'mainEntity': dict(org(), department=[office_node(o) for o in OFFICES])}
    return shell('Tentang Altora Indonesia | Samarinda & Balikpapan',
                 'Altora Indonesia di Samarinda dan Balikpapan: jasa pembuatan software custom, website, dan SEO.',
                 '/about', SITE + COLLAGE[0], ld, body)


if __name__ == '__main__':
    (root / 'about.html').write_text(build(), encoding='utf-8')
    print('about.html dibuat')
