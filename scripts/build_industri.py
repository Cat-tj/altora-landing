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
H = '/assets/img/hardware/'

INDUSTRIES = {
    'pertambangan': dict(name='Tambang & industri berat', h1='Perangkat dan aplikasi untuk tambang dan industri berat', tone='ti-pertambangan',
        title='Solusi Tambang & Industri Berat | Starlink, CCTV Surya | Altora',
        desc='Starlink, CCTV tenaga surya, GPS tracker, jaringan, dan aplikasi custom untuk tambang, kontraktor, dan industri berat di Kalimantan Timur.',
        lead='Lokasi kerja yang jauh dari jaringan butuh internet, kamera, dan pencatatan yang tetap jalan. Kami mengadakan perangkatnya dan membuat aplikasi pelaporan sesuai proses Anda.',
        hero=H + 'starlink-enterprise.webp', sectors={'Industri'},
        pains=['Internet tidak stabil di lokasi kerja.', 'Area luas sulit dipantau tanpa kamera.', 'Laporan lapangan masih dikumpulkan manual.', 'Perangkat rusak, sementara teknisi jauh.'],
        stack=[('/services/starlink-internet-satelit', 'Starlink', 'Internet untuk site terpencil'), ('/katalog-cctv-vigi', 'CCTV VIGI', 'Kamera, NVR, dan paket tenaga surya'),
               ('/katalog#cat-gps', 'GPS tracker Teltonika', 'Perangkat telematika kendaraan'), ('/services/software-custom', 'Aplikasi pelaporan', 'Dibuat sesuai proses lapangan'),
               ('/services/instalasi-listrik-jaringan', 'Listrik & jaringan', 'Instalasi rapi dan berlabel'), ('/services/pengadaan-instalasi-maintenance', 'Pengadaan & maintenance', 'Perangkat dan perawatan berkala')],
        faq=[('Apakah bisa untuk lokasi tanpa listrik dan jaringan?', 'Bisa. Kami menyiapkan Starlink dan CCTV tenaga surya, dan menghitung kebutuhan daya saat survei.'),
             ('Apakah perangkat bergaransi resmi?', 'Ya. Perangkat berasal dari principal resmi, dengan garansi sesuai ketentuan principal.')]),
    'pemerintahan': dict(name='Pemerintahan & layanan publik', h1='Website, kios layanan, dan pengadaan perangkat untuk instansi', tone='ti-pemerintahan',
        title='Solusi untuk Pemerintahan | Website, Kios, Pengadaan | Altora',
        desc='Website resmi, kios layanan mandiri, dan pengadaan perangkat untuk pemerintah daerah. Terdaftar Inaproc/LKPP, siap tender.',
        lead='Website resmi yang mudah diperbarui, kios layanan mandiri, dan pengadaan perangkat dengan dokumen administrasi lengkap. Terdaftar sebagai penyedia Inaproc/LKPP.',
        hero=H + 'kios-k.webp', sectors={'Pemerintahan'},
        pains=['Website resmi jarang diperbarui.', 'Antrean layanan panjang di loket.', 'Pengadaan butuh dokumen yang lengkap dan rapi.', 'Perangkat kantor tidak seragam dan sulit dirawat.'],
        stack=[('/services/website-seo', 'Website & portal instansi', 'Dengan CMS yang mudah diisi'), ('/mesin-kiosk-samarinda', 'Kios layanan mandiri', 'Antrean dan cetak dokumen'),
               ('/services/pengadaan-instalasi-maintenance', 'Pengadaan perangkat', 'Penawaran, faktur, berita acara'), ('/services/software-custom', 'Aplikasi pelayanan', 'Dibuat sesuai alur layanan'),
               ('/katalog', 'Katalog perangkat', 'Dari principal resmi'), ('/services/smart-display-kios', 'Signage & kios', 'Layar informasi publik')],
        faq=[('Apakah bisa untuk pengadaan instansi?', 'Bisa. Altora berstatus PKP dan terdaftar di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara serah terima.'),
             ('Apakah tersedia produk ber-TKDN?', 'Tersedia sesuai ketersediaan dari principal. Kami cek saat menyusun penawaran.')]),
    'pendidikan': dict(name='Kampus & sekolah', h1='Website, display, dan perangkat untuk kampus dan sekolah', tone='ti-pendidikan',
        title='Solusi Kampus & Sekolah | Website, Display, Jaringan | Altora',
        desc='Website kampus, interactive flat panel, jaringan, dan perangkat komputer untuk kampus dan sekolah di Kalimantan Timur.',
        lead='Website yang mudah dikelola admin, layar interaktif untuk ruang kelas, jaringan yang stabil, dan perangkat komputer dari principal resmi.',
        hero=H + 'hde-ifp.webp', sectors={'Pendidikan'},
        pains=['Website fakultas jarang diperbarui.', 'Ruang kelas belum punya layar interaktif.', 'WiFi kampus lambat di jam sibuk.', 'Komputer lab sudah ketinggalan.'],
        stack=[('/services/website-seo', 'Website kampus & sekolah', 'Dengan CMS'), ('/interactive-flat-panel-samarinda', 'Interactive flat panel', 'Kelas dan ruang rapat'),
               ('/katalog#cat-laptop', 'Laptop, PC & tablet', 'Lenovo ThinkPad, AIO, tablet'), ('/services/instalasi-listrik-jaringan', 'Jaringan & listrik', 'Instalasi kampus dan gedung'),
               ('/services/software-custom', 'Aplikasi kampus', 'Sesuai proses akademik'), ('/services/pengadaan-instalasi-maintenance', 'Pengadaan & maintenance', 'Perangkat dan perawatan berkala')],
        faq=[('Apakah website kampus bisa dikelola admin sendiri?', 'Bisa. Website dilengkapi CMS sehingga admin fakultas bisa memperbarui berita dan informasi.'),
             ('Apakah bisa pengadaan untuk banyak ruang sekaligus?', 'Bisa. Kami survei dulu, lalu menyusun paket perangkat dan jadwal pemasangan per ruang.')]),
    'korporasi': dict(name='Korporasi & dunia usaha', h1='Aplikasi, website, dan perangkat untuk perusahaan', tone='ti-korporasi',
        title='Solusi Digital Perusahaan | Aplikasi, Website, Perangkat | Altora',
        desc='Aplikasi custom, website, CCTV, jaringan, dan perangkat kantor untuk perusahaan di Samarinda dan Balikpapan. Software dan hardware satu pintu.',
        lead='Satu mitra untuk aplikasi, website, CCTV, jaringan, dan perangkat kantor. Tidak perlu koordinasi banyak vendor.',
        hero=H + 'lenovo-thinkpad-t14.webp', sectors={'Korporasi'},
        pains=['Vendor software dan hardware berbeda-beda.', 'Data antar bagian tidak terhubung.', 'Keamanan kantor dan gudang belum terpantau.', 'Tidak ada tim IT internal.'],
        stack=[('/services/software-custom', 'Aplikasi custom', 'Approval, laporan, dan sistem internal'), ('/services/website-seo', 'Website & SEO', 'Company profile dan landing page'),
               ('/katalog-cctv-vigi', 'CCTV VIGI', 'Kantor, gudang, toko'), ('/it-support-balikpapan', 'IT support', 'Komputer, jaringan, server'),
               ('/katalog#cat-laptop', 'Laptop & PC', 'Perangkat kantor dari Lenovo'), ('/services/pengadaan-instalasi-maintenance', 'Pengadaan & maintenance', 'Perangkat dan perawatan berkala')],
        faq=[('Apakah bisa kontrak IT support bulanan?', 'Bisa. Cakupan dan frekuensi kunjungan disesuaikan jumlah perangkat dan kebutuhan kantor.'),
             ('Apakah aplikasi bisa disesuaikan dengan proses kami?', 'Bisa. Kami pelajari alur kerja Anda dulu, lalu aplikasi dibuat khusus mengikuti prosesnya.')]),
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
            '<h1>Solusi per industri</h1><p class="ct-lead">Aplikasi, website, dan perangkat dari principal resmi, disesuaikan untuk konteks yang berbeda: tambang, pemerintahan, pendidikan, dan korporasi.</p></div></section>'
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
