"""Halaman solusi per industri: /industri/<slug> + hub /industri.
Jalankan lewat scripts/build_all.sh."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA
from build_trust import CLIENTS, logo_tile

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
P = '/assets/img/portfolio/'
STEPS = [('Survei gratis', 'Petakan kebutuhan dan titik prioritas di lokasi Anda.'), ('Pilot kecil', 'Mulai dari satu modul yang paling mendesak.'),
         ('Integrasi', 'Sambungkan ke sistem yang sudah berjalan.'), ('Bukti & skala', 'Ukur hasil pilot, lalu perluas bertahap.'),
         ('Didampingi', 'Dukungan tim lokal, data tetap milik Anda.')]

INDUSTRIES = {
    'pertambangan': dict(name='Tambang & industri berat', h1='Teknologi untuk tambang dan industri berat', tone='ti-pertambangan',
        title='Solusi Teknologi Tambang & Hauling | FMS, AI Safety | Altora',
        desc='Fleet management, AI safety (deteksi APD), CCTV tenaga surya, dan Starlink untuk tambang, hauling, dan industri berat di Kalimantan Timur.',
        lead='Dari pit sampai port: armada terpantau, keselamatan kerja diawasi AI, dan site terpencil tetap terhubung. Dipasang dan dirawat tim kami di Kaltim.',
        hero=P + 'fms.jpg', sectors={'Tambang', 'Konstruksi', 'Industri'},
        pains=['BBM dan ritase sulit dikontrol di lapangan.', 'Pelanggaran APD baru ketahuan setelah insiden.', 'Site terpencil tanpa listrik dan internet.', 'Downtime unit karena perawatan terlambat.'],
        stack=[('/produk/fms', 'Altora FMS', 'Ritase, BBM, CAN-Bus, TPMS, Cost-per-Ton'), ('/produk/vision', 'Altora Vision', 'Deteksi APD dan zona berbahaya'),
               ('/cctv-tenaga-surya-balikpapan', 'CCTV tenaga surya & 4G', 'Untuk pit, jalan hauling, dan pos jaga'), ('/jual-starlink-balikpapan', 'Starlink Performance', 'Internet untuk site off-grid'),
               ('/produk/command', 'Altora Command', 'Ruang kendali operasi'), ('/produk/teams', 'Altora Teams', 'Absensi dan payroll operator')],
        proof=[('/portfolio/fleet-management', 'Fleet management armada hauling', P + 'fms.jpg'), ('/portfolio/ai-safety-vision', 'Deteksi APD dari CCTV', P + 'safety.jpg'),
               ('/portfolio/optimasi-rute-armada', 'Optimasi rute & armada', P + 'logistik.jpg')],
        faq=[('Apakah perangkat tahan kondisi tambang?', 'Ya. Kami memakai perangkat industrial grade: Teltonika tahan getar dan debu, kamera IP67, Starlink Performance tahan cuaca ekstrem.'),
             ('Bisa mulai dari beberapa unit dulu?', 'Bisa. Kami sarankan pilot di beberapa unit atau satu area, lalu perluas setelah hasilnya terukur.')]),
    'pemerintahan': dict(name='Pemerintahan & layanan publik', h1='Teknologi untuk pemerintahan dan layanan publik', tone='ti-pemerintahan',
        title='Solusi Digital Pemerintah Daerah | GIS, Kios, CCTV Kota | Altora',
        desc='GIS dan kebijakan satu peta, kios layanan mandiri, CCTV kota, dan AI on-premise untuk pemerintah daerah. Terdaftar Inaproc/LKPP, siap tender.',
        lead='Data wilayah dalam satu peta, layanan warga tanpa antre, dan AI yang berjalan di server sendiri. Terdaftar sebagai penyedia Inaproc/LKPP.',
        hero=P + 'kiosk-samarinda/kiosk-pampang.jpg', sectors={'Pemerintahan', 'BUMN'},
        pains=['Data antar-dinas tidak seragam.', 'Warga antre untuk layanan administrasi.', 'Data sensitif tidak boleh ke cloud publik.', 'Pengadaan harus lewat jalur resmi.'],
        stack=[('/produk/private-ai', 'Altora Private AI & GIS', 'Satu peta dan AI on-premise'), ('/mesin-kiosk-samarinda', 'Kios-K layanan mandiri', 'Cetak dokumen tanpa antre'),
               ('/jual-cctv-samarinda', 'CCTV kota & kantor', 'VIGI dengan analitik AI'), ('/videotron-samarinda', 'Videotron & signage', 'Informasi publik'),
               ('/services/website-seo', 'Website & portal instansi', 'Layanan publik satu pintu'), ('/produk/command', 'Command center', 'Pemantauan terpusat')],
        proof=[('/portfolio/portal-one-map', 'Portal One Map Policy, Barito Utara', P + 'barito-dash.jpg'), ('/portfolio/custom-kios-k-pengadaan-hardware', 'Kios-K kelurahan, Kota Samarinda', P + 'hardware-field/kiosk-baqa-service.jpg'),
               ('/portfolio/dashboard-geospasial-dapodik', 'Dashboard geospasial', P + 'dapodik.jpg')],
        faq=[('Apakah Altora bisa mengikuti pengadaan pemerintah?', 'Bisa. Kami berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.'),
             ('Apakah sistem bisa dipasang di pusat data pemerintah?', 'Bisa. Aplikasi dan AI dapat berjalan di server atau pusat data milik instansi.')]),
    'pendidikan': dict(name='Kampus & sekolah', h1='Teknologi untuk kampus dan sekolah', tone='ti-pendidikan',
        title='Smart Campus & Sekolah | Absensi, Website, Display, AI | Altora',
        desc='Absensi wajah, website kampus, interactive flat panel, CCTV, jaringan, dan pembinaan riset AI untuk kampus dan sekolah di Kalimantan Timur.',
        lead='Absensi otomatis, website yang mudah diperbarui, ruang kelas interaktif, dan jaringan kampus yang rapi. Kami juga membimbing siswa membangun inovasi AI.',
        hero=P + 'feb-unmul.jpg', sectors={'Pendidikan', 'Pendidikan & riset'},
        pains=['Rekap kehadiran mahasiswa dan staf masih manual.', 'Website fakultas sulit diperbarui.', 'Jaringan dan CCTV kampus tidak terdokumentasi.', 'Siswa butuh pembimbing untuk proyek teknologi.'],
        stack=[('/produk/attendance', 'Absensi wajah', 'Dari CCTV di pintu masuk'), ('/services/website-seo', 'Website kampus & fakultas', 'Dengan CMS'),
               ('/interactive-flat-panel-balikpapan', 'Interactive flat panel', 'Ruang kelas & rapat'), ('/jasa-instalasi-jaringan-samarinda', 'Jaringan & WiFi kampus', 'LAN, fiber, rak server'),
               ('/jual-smartlock-samarinda', 'Akses lab & asrama', 'Smartlock dan kartu'), ('/produk/teams', 'HRIS dosen & staf', 'Absensi, cuti, payroll')],
        proof=[('/portfolio/unmul-website-redesign', 'Website FEB Universitas Mulawarman', P + 'feb-unmul.jpg'), ('/portfolio/unmul-infrastruktur-cctv-jaringan', 'CCTV & jaringan Unmul', P + 'unmul-infrastructure/cable-cctv-installation.png'),
               ('/portfolio/smart-attendance', 'Absensi wajah dari CCTV', P + 'attendance.jpg')],
        extra='<div class="ts-award ind-award"><span class="ts-award-ico"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8.5 20h7M10 17h4"/></svg></span><div><small>Pembinaan siswa</small><h3>Juara 2 Nasional Innovakids 2026</h3><p>Altora menjadi pembimbing siswa SMP Negeri 5 Balikpapan membangun solusi inovasi berbasis AI hingga meraih Juara 2 tingkat nasional. Kami terbuka untuk pembinaan dan kolaborasi riset dengan sekolah dan kampus.</p></div></div>',
        faq=[('Apakah Altora bisa membimbing proyek AI siswa atau mahasiswa?', 'Bisa. Kami membimbing siswa SMP Negeri 5 Balikpapan hingga Juara 2 Nasional Innovakids 2026 dan berkolaborasi riset dengan ITK.'),
             ('Apakah website kampus bisa dikelola admin sendiri?', 'Bisa. Website dilengkapi CMS sehingga admin fakultas bisa memperbarui berita dan informasi.')]),
    'korporasi': dict(name='Korporasi & dunia usaha', h1='Teknologi untuk korporasi dan dunia usaha', tone='ti-korporasi',
        title='Solusi Digital Perusahaan | HRIS, ERP, CCTV, Smartlock | Altora',
        desc='HRIS, ERP, website, CCTV, smartlock, dan IT support untuk perusahaan di Samarinda dan Balikpapan. Satu tim untuk software dan perangkat.',
        lead='Satu mitra untuk aplikasi, website, CCTV, akses pintu, jaringan, dan IT support. Tidak perlu koordinasi banyak vendor.',
        hero='/assets/img/produk/teams.webp', sectors={'Korporasi', 'Industri'},
        pains=['Vendor software dan hardware berbeda-beda.', 'Data karyawan, stok, dan keuangan tidak terhubung.', 'Keamanan kantor dan gudang belum terpantau.', 'Tidak ada tim IT internal.'],
        stack=[('/produk/teams', 'Altora Teams', 'HRIS, absensi, payroll'), ('/produk/erp', 'Altora ERP', 'Stok, pembelian, keuangan'),
               ('/produk/pass', 'Altora Pass', 'Akses pintu digital'), ('/jual-cctv-balikpapan', 'CCTV VIGI', 'Kantor, gudang, toko'),
               ('/it-support-balikpapan', 'IT support', 'Komputer, jaringan, server'), ('/services/website-seo', 'Website & SEO', 'Company profile dan landing page')],
        proof=[('/portfolio/altora-teams', 'Altora Teams', P + 'altora-teams-kpi-analytics.jpg'), ('/portfolio/hris-mobile-payroll', 'HRIS mobile & payroll', P + 'hris.jpg'),
               ('/portfolio/smartlock-akses-digital', 'Smartlock & akses digital', P + 'smartlock.jpg')],
        faq=[('Apakah bisa kontrak IT support bulanan?', 'Bisa. Cakupan dan frekuensi kunjungan disesuaikan jumlah perangkat dan kebutuhan kantor.'),
             ('Apakah aplikasi bisa disesuaikan dengan proses kami?', 'Bisa. Mulai dari aplikasi jadi, lalu disesuaikan atau dibuat khusus bila prosesnya berbeda.')]),
}


def page(key, d):
    url = f'/industri/{key}'
    pains = ''.join(f'<li>{e(x)}</li>' for x in d['pains'])
    stack = ''.join(f'<a class="ind-stack-item" href="{u}"><b>{e(t)}</b><small>{e(s)}</small></a>' for u, t, s in d['stack'])
    steps = ''.join(f'<li><span>{i:02d}</span><b>{e(t)}</b><p>{e(x)}</p></li>' for i, (t, x) in enumerate(STEPS, 1))
    proof = ''.join(f'<a class="svd-proof" href="{u}"><span class="svd-proof-img"><img alt="" loading="lazy" src="{img}"/></span><b>{e(t)}</b><small>Lihat proyek</small></a>' for u, t, img in d['proof'])
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
<section class="ap-sec"><div class="ct-wrap"><h2>Mulai kecil, tumbuh terukur</h2><ol class="tp-steps">{steps}</ol></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Proyek terkait</h2><div class="svd-proofs">{proof}</div></div></section>
<section class="ap-sec"><div class="ct-wrap svd-faq"><h2>Pertanyaan umum</h2><div>{faq}</div></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Industri lainnya</h2><div class="ti-grid ind-others">{others}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Ceritakan kondisi lapangan Anda</h2><p>Survei dan konsultasi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    return url, shell(d['title'], d['desc'], url, SITE + d['hero'], ld, body)


def hub():
    cards = ''.join(f'<a class="ti-card ti-{k}" href="/industri/{k}"><b>{e(d["name"])}</b><small>{e(d["lead"])}</small></a>' for k, d in INDUSTRIES.items())
    body = ('<main class="ct-page ind-page"><section class="ap-hero"><div class="ct-wrap"><nav aria-label="Breadcrumb" class="vg-crumb"><a href="/">Beranda</a> / <span>Industri</span></nav>'
            '<h1>Solusi per industri</h1><p class="ct-lead">Perangkat, software, dan layanan yang sama, dirakit untuk konteks yang berbeda: tambang, pemerintahan, pendidikan, dan korporasi.</p></div></section>'
            f'<section class="ap-sec"><div class="ct-wrap"><div class="ti-grid ind-hub">{cards}</div></div></section></main>')
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Solusi per industri', 'url': SITE + '/industri'}
    return shell('Solusi per Industri | Tambang, Pemerintahan, Kampus | Altora', 'Solusi teknologi Altora per industri: tambang & industri berat, pemerintahan, kampus & sekolah, serta korporasi di Kalimantan Timur.',
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
