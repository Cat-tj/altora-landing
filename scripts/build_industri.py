"""Halaman solusi per industri: /industri/<slug> + hub /industri.
Jalankan lewat scripts/build_all.sh."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA
from build_trust import CLIENTS, logo_tile

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
STEPS = [('Konsultasi', 'Petakan kebutuhan dan prioritas Anda. Gratis.'), ('Survei', 'Cek lokasi atau alur kerja, lalu susun solusi.'),
         ('Penawaran', 'Proposal dan rencana kerja tertulis.'), ('Pengerjaan', 'Pengembangan aplikasi atau pemasangan perangkat.'),
         ('Didampingi', 'Pelatihan pengguna dan dukungan setelah dipakai.')]
IMG = '/assets/img/'

INDUSTRIES = {
    'pertambangan': dict(name='Tambang & industri berat', h1='Aplikasi dan website untuk tambang dan industri berat', tone='ti-pertambangan',
        title='Aplikasi untuk Tambang & Industri Berat | Altora',
        desc='Aplikasi pelaporan, approval, dan dashboard untuk tambang, kontraktor, dan industri berat di Kalimantan Timur, dirancang tetap jalan saat sinyal lemah.',
        lead='Laporan lapangan yang masih dikumpulkan manual memperlambat keputusan. Kami membuat aplikasi pelaporan, approval, dan dashboard yang tetap berfungsi di lokasi dengan sinyal lemah.',
        hero=IMG + 'person-problem.webp', sectors={'Industri'},
        pains=['Laporan lapangan dikumpulkan lewat chat dan spreadsheet.', 'Approval tertahan karena orangnya di lokasi lain.', 'Data produksi sulit dirangkum untuk pimpinan.', 'Aplikasi biasa tidak jalan saat sinyal lemah.'],
        stack=[('/services/software-custom', 'Aplikasi pelaporan', 'Dibuat sesuai proses lapangan'), ('/services/software-custom', 'Approval & dokumen', 'Pengajuan dan persetujuan tanpa kertas'),
               ('/services/software-custom', 'Dashboard operasional', 'Ringkasan harian untuk pimpinan'), ('/software-house-kalimantan-timur', 'Software house Kaltim', 'Tim lokal Samarinda & Balikpapan'),
               ('/services/website-seo', 'Website perusahaan', 'Company profile yang jelas dan cepat'), ('/services/seo', 'SEO', 'Mudah ditemukan calon mitra')],
        faq=[('Apakah aplikasinya bisa dipakai di lokasi tanpa sinyal?', 'Bisa. Aplikasi dapat dirancang menyimpan data sementara lalu mengirimnya saat sinyal tersedia.'),
             ('Apakah bisa terhubung dengan sistem yang sudah ada?', 'Umumnya bisa. Kami cek dulu sistem yang Anda pakai, lalu tentukan cara menghubungkannya.')]),
    'pemerintahan': dict(name='Pemerintahan & layanan publik', h1='Website dan aplikasi layanan untuk instansi pemerintah', tone='ti-pemerintahan',
        title='Website & Aplikasi untuk Pemerintahan | Altora',
        desc='Website resmi, portal informasi, dan aplikasi layanan untuk pemerintah daerah. Terdaftar Inaproc/LKPP, siap tender.',
        lead='Website resmi yang mudah diperbarui dan aplikasi layanan yang mudah dipakai warga. Altora terdaftar sebagai penyedia Inaproc/LKPP, dengan dokumen administrasi yang lengkap.',
        hero=IMG + 'person-support.webp', sectors={'Pemerintahan'},
        pains=['Website resmi jarang diperbarui.', 'Layanan masih lewat loket dan formulir kertas.', 'Data antar bagian tidak terhubung.', 'Pengadaan butuh dokumen yang lengkap dan rapi.'],
        stack=[('/services/website-seo', 'Website & portal instansi', 'Dengan CMS yang mudah diisi'), ('/services/software-custom', 'Aplikasi pelayanan', 'Dibuat sesuai alur layanan'),
               ('/services/seo', 'SEO instansi', 'Informasi layanan mudah ditemukan warga'), ('/software-house-samarinda', 'Software house Samarinda', 'Tim lokal di Kaltim'),
               ('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website', 'Untuk dinas dan kelurahan'), ('/contact', 'Konsultasi', 'Diskusi awal gratis')],
        faq=[('Apakah bisa untuk pengadaan instansi?', 'Bisa. Altora berstatus PKP dan terdaftar di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara serah terima.'),
             ('Apakah website bisa diperbarui admin sendiri?', 'Bisa. Website dilengkapi CMS sehingga admin dapat memperbarui berita dan informasi tanpa developer.')]),
    'pendidikan': dict(name='Kampus & sekolah', h1='Website dan aplikasi untuk kampus dan sekolah', tone='ti-pendidikan',
        title='Website & Aplikasi untuk Kampus dan Sekolah | Altora',
        desc='Website kampus dan sekolah, portal informasi, dan aplikasi administrasi akademik untuk lembaga pendidikan di Kalimantan Timur.',
        lead='Website yang mudah dikelola admin dan aplikasi administrasi yang menyederhanakan pekerjaan rutin staf dan guru.',
        hero=IMG + 'person-faq.webp', sectors={'Pendidikan'},
        pains=['Website fakultas atau sekolah jarang diperbarui.', 'Administrasi masih manual di spreadsheet.', 'Informasi sulit ditemukan calon mahasiswa atau orang tua.', 'Data tersebar di banyak file.'],
        stack=[('/services/website-seo', 'Website kampus & sekolah', 'Dengan CMS'), ('/services/software-custom', 'Aplikasi administrasi', 'Sesuai proses akademik'),
               ('/services/seo', 'SEO', 'Informasi penerimaan mudah ditemukan'), ('/software-house-samarinda', 'Software house Samarinda', 'Tim lokal'),
               ('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website', 'Untuk sekolah dan kampus'), ('/contact', 'Konsultasi', 'Diskusi awal gratis')],
        faq=[('Apakah website kampus bisa dikelola admin sendiri?', 'Bisa. Website dilengkapi CMS sehingga admin fakultas bisa memperbarui berita dan informasi.'),
             ('Apakah bisa dibuatkan aplikasi sesuai proses sekolah kami?', 'Bisa. Kami pelajari alur kerja Anda dulu, lalu aplikasi dibuat bertahap dan diuji bersama pengguna.')]),
    'korporasi': dict(name='Korporasi & dunia usaha', h1='Aplikasi, website, dan SEO untuk perusahaan', tone='ti-korporasi',
        title='Aplikasi, Website & SEO untuk Perusahaan | Altora',
        desc='Aplikasi custom, website, dan SEO untuk perusahaan di Samarinda dan Balikpapan. Satu tim dari analisis sampai dukungan.',
        lead='Satu mitra untuk aplikasi internal, website perusahaan, dan SEO. Tidak perlu koordinasi banyak vendor.',
        hero=IMG + 'person-flow.webp', sectors={'Korporasi'},
        pains=['Proses kerja masih lewat chat dan spreadsheet.', 'Data antar bagian tidak terhubung.', 'Website ada tetapi tidak ditemukan di Google.', 'Tidak ada tim IT internal.'],
        stack=[('/services/software-custom', 'Aplikasi custom', 'Approval, laporan, dan sistem internal'), ('/services/website-seo', 'Website perusahaan', 'Company profile dan landing page'),
               ('/services/seo', 'SEO', 'Audit dan perbaikan on-page'), ('/aplikasi', 'Aplikasi buatan Altora', 'Projek, Office, Raphael CC'),
               ('/software-house-balikpapan', 'Software house Balikpapan', 'Tim lokal'), ('/contact', 'Konsultasi', 'Diskusi awal gratis')],
        faq=[('Apakah aplikasi bisa disesuaikan dengan proses kami?', 'Bisa. Kami pelajari alur kerja Anda dulu, lalu aplikasi dibuat khusus mengikuti prosesnya.'),
             ('Apakah bisa terhubung dengan aplikasi yang sudah kami pakai?', 'Umumnya bisa. Kami cek dulu aplikasi yang Anda pakai, lalu tentukan cara menghubungkannya.')]),
}


def page(key, d):
    url = f'/industri/{key}'
    pains = ''.join(f'<li>{e(x)}</li>' for x in d['pains'])
    stack = ''.join(f'<a class="ind-stack-item" href="{u}"><b>{e(t)}</b><small>{e(s)}</small></a>' for u, t, s in d['stack'])
    steps = ''.join(f'<li><span>{i:02d}</span><b>{e(t)}</b><p>{e(x)}</p></li>' for i, (t, x) in enumerate(STEPS, 1))
    logos = ''.join(logo_tile(*c) for c in CLIENTS if c[2] in d['sectors'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(x)}</p></details>' for q, x in d['faq'])
    others = ''.join(f'<a class="ti-card ti-{k}" href="/industri/{k}"><b>{e(o["name"])}</b><small>{e(o["lead"][:80])}…</small></a>' for k, o in INDUSTRIES.items() if k != key)
    msg = f'Halo Altora, saya dari sektor {d["name"].lower()} dan ingin konsultasi.'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', 'name': d['h1'], 'description': d['desc'], 'url': SITE + url},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Industri', 'item': SITE + '/industri'},
            {'@type': 'ListItem', 'position': 3, 'name': d['name'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in d['faq']]}]}
    body = f'''<main class="ct-page ind-page">
<section class="ind-hero {d["tone"]}"><div class="ct-wrap ind-hero-grid"><div>
<nav aria-label="Breadcrumb" class="vg-crumb"><a href="/">Beranda</a> / <a href="/industri">Industri</a> / <span>{e(d["name"])}</span></nav>
<h1>{e(d["h1"])}</h1><p class="ct-lead">{e(d["lead"])}</p>
<div class="ap-actions"><a class="btn btn-white" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="ind-link" href="#solusi">Lihat solusi</a></div></div>
<figure class="ind-hero-pic"><img alt="{e(d["name"])}" src="{d["hero"]}"/></figure></div></section>
<section class="ap-sec"><div class="ct-wrap ap-two"><div><h2>Tantangan yang sering kami temui</h2><ul class="ap-pains">{pains}</ul></div>
<div>{d.get("extra", "")}{f'<h2>Klien di sektor ini</h2><ul class="tl-grid ind-logos">{logos}</ul>' if logos else ''}</div></div></section>
<section class="ap-sec" id="solusi"><div class="ct-wrap"><h2>Solusi yang kami rakit</h2><div class="ind-stack">{stack}</div></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Cara kami bekerja</h2><ol class="tp-steps">{steps}</ol></div></section>
<section class="ap-sec"><div class="ct-wrap svd-faq"><h2>Pertanyaan umum</h2><div>{faq}</div></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Industri lainnya</h2><div class="ti-grid ind-others">{others}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Ceritakan kondisi lapangan Anda</h2><p>Survei dan konsultasi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    return url, shell(d['title'], d['desc'], url, SITE + d['hero'], ld, body)


def hub():
    cards = ''.join(f'<a class="ti-card ti-{k}" href="/industri/{k}"><b>{e(d["name"])}</b><small>{e(d["lead"])}</small></a>' for k, d in INDUSTRIES.items())
    body = ('<main class="ct-page ind-page"><section class="ap-hero"><div class="ct-wrap"><nav aria-label="Breadcrumb" class="vg-crumb"><a href="/">Beranda</a> / <span>Industri</span></nav>'
            '<h1>Solusi per industri</h1><p class="ct-lead">Aplikasi, website, dan SEO, disesuaikan untuk konteks yang berbeda: tambang, pemerintahan, pendidikan, dan korporasi.</p></div></section>'
            f'<section class="ap-sec"><div class="ct-wrap"><div class="ti-grid ind-hub">{cards}</div></div></section></main>')
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Solusi per industri', 'url': SITE + '/industri'}
    return shell('Solusi per Industri | Tambang, Pemerintahan, Kampus | Altora', 'Aplikasi, website, dan pengadaan perangkat Altora per sektor: tambang & industri berat, pemerintahan, kampus & sekolah, serta korporasi di Kalimantan Timur.',
                 '/industri', SITE + '/assets/img/altora-logo-600.png', ld, body)


if __name__ == '__main__':
    (root / 'industri').mkdir(exist_ok=True)
    urls = []
    for k, d in INDUSTRIES.items():
        url, h = page(k, d)
        (root / (url.lstrip('/') + '.html')).write_text(h, encoding='utf-8')
        urls.append(url)
    (root / 'industri.html').write_text(hub(), encoding='utf-8')
    update_sitemap(urls + ['/industri'])
    print('halaman industri:', len(urls), '+ hub')
