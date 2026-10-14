"""Bangun halaman lokal 'software house <kota>' dari data CITIES.
Jalankan dari root repo:  python3 scripts/build_local.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py
Isi setiap kota harus berbeda dan hanya memakai fakta yang bisa dipertanggungjawabkan."""
import html, json, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import OFFICES, postal_address, one_line, maps_link

root = pathlib.Path(__file__).resolve().parent.parent
CSS_VER = '20261014s'
SITE = 'https://altora.id'
WA = 'https://wa.me/6285190911170?text='
e = lambda t: html.escape(t, quote=True)

SERVICES = [
    ('/services/software-custom', 'Aplikasi & software custom', 'Web app, aplikasi HP, HRIS, approval, dan laporan internal.'),
    ('/services/website-seo', 'Website & SEO', 'Company profile, website instansi, dan landing page yang mudah ditemukan.'),
    ('/services/ai-cctv', 'AI CCTV', 'Deteksi APD, absensi wajah, dan alert area terlarang dari CCTV.'),
    ('/services/fleet-management-service', 'Fleet management', 'GPS tracker dan dashboard armada untuk logistik dan tambang.'),
    ('/services/iot-command-center', 'IoT & command center', 'Sensor, smartlock, dan ruang kendali.'),
    ('/services/pengadaan-instalasi-maintenance', 'Pengadaan & maintenance', 'CCTV, jaringan, komputer, dan perawatan berkala.'),
]

PF = {
    'custom-kios-k-pengadaan-hardware': ('Kios layanan kelurahan Samarinda', '/assets/img/portfolio/hardware-field/kiosk-baqa-service.jpg', 'Pengadaan dan pemasangan kios, PC, dan tablet di kantor kelurahan.'),
    'unmul-website-redesign': ('Redesign website Universitas Mulawarman', '/assets/img/portfolio/feb-unmul.jpg', 'Pembaruan website fakultas dan jurusan.'),
    'unmul-infrastruktur-cctv-jaringan': ('CCTV & jaringan Universitas Mulawarman', '/assets/img/portfolio/unmul-infrastructure/cable-cctv-installation.png', 'Penarikan kabel, perangkat jaringan, dan CCTV.'),
    'website-resmi-institusi': ('Website resmi institusi', '/assets/img/portfolio/farmasi.jpg', 'Website publik dengan struktur informasi yang rapi.'),
    'fleet-management': ('Fleet management armada hauling', '/assets/img/portfolio/fms.jpg', 'Pemantauan posisi dan data kendaraan armada.'),
    'smart-attendance': ('Absensi wajah dari CCTV', '/assets/img/portfolio/attendance.jpg', 'Check-in otomatis dari kamera di pintu masuk.'),
    'altora-teams': ('Altora Teams (HRIS)', '/assets/img/portfolio/altora-teams-kpi-analytics.jpg', 'KPI, approval, dan jadwal kerja tim.'),
}

CITIES = [
    dict(slug='software-house-balikpapan', city='Balikpapan', area='Balikpapan',
         title='Software House Balikpapan | Altora Indonesia',
         desc='Altora Indonesia, software house di Balikpapan: aplikasi custom, website, AI CCTV, fleet management, serta pengadaan dan pemasangan perangkat.',
         h1='Software house di Balikpapan',
         lead='Altora Indonesia punya dua kantor cabang di Balikpapan, di Balikpapan Utara dan Pasar Baru. Kami membuat aplikasi, website, dan sistem CCTV pintar, lalu memasang dan merawat perangkatnya, untuk perusahaan, instansi, dan UMKM di Balikpapan.',
         why=[('Dua cabang di Balikpapan', 'Cabang kami di Jl. Soekarno Hatta, Muara Rapak (Balikpapan Utara) dan di Pasar Baru. Diskusi, survei, dan pelatihan bisa dilakukan langsung di lokasi Anda.'),
              ('Software dan perangkat satu tim', 'Banyak kebutuhan di Balikpapan melibatkan perangkat: CCTV, GPS tracker, sensor, jaringan. Kami mengerjakan aplikasi dan pemasangannya sekaligus.'),
              ('Dukungan setelah jalan', 'Saat ada kendala, tim teknis bisa datang ke lokasi, tidak hanya membalas lewat chat.')],
         needs=[('Perusahaan jasa migas, logistik, dan kontraktor', 'Pemantauan armada, absensi karyawan lapangan, dan pengawasan APD di area kerja.'),
                ('Kantor dan instansi', 'Aplikasi persuratan, approval, dan website resmi yang mudah diperbarui.'),
                ('Toko, kafe, dan usaha jasa', 'Kasir, stok, dan website untuk ditemukan pelanggan di Google.')],
         proof=['fleet-management', 'smart-attendance', 'altora-teams'],
         faq=[('Di mana kantor Altora di Balikpapan?', 'Ada dua cabang: Jl. Soekarno Hatta, Muara Rapak, Balikpapan Utara, dan Pasar Baru, Balikpapan. Kantor pusat kami di Samarinda. Untuk diskusi, kami juga bisa datang ke kantor Anda.'),
              ('Apakah melayani pemasangan CCTV dan GPS tracker di Balikpapan?', 'Ya. Kami mengadakan, memasang, dan merawat CCTV, GPS tracker, jaringan, dan perangkat lain, termasuk menghubungkannya ke aplikasi.'),
              ('Berapa biaya membuat aplikasi di Balikpapan?', 'Tergantung fitur, jumlah pengguna, dan integrasi. Konsultasi awal gratis, lalu kami kirim penawaran tertulis. Faktor biayanya kami jelaskan di artikel biaya membuat aplikasi.'),
              ('Apakah bisa mulai dari aplikasi yang sudah jadi?', 'Bisa. Untuk absensi, CCTV pintar, akses pintu, atau pelacakan armada, Anda bisa memakai aplikasi Altora yang sudah jadi lalu menyesuaikannya.')],
         nearby=[('/software-house-samarinda', 'Software house Samarinda'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'), ('/blog/cara-memilih-software-house-samarinda-balikpapan', 'Cara memilih software house')]),
    dict(slug='software-house-samarinda', city='Samarinda', area='Samarinda',
         title='Software House Samarinda | Altora Indonesia',
         desc='Software house di Samarinda: aplikasi custom, website instansi, CCTV pintar, dan pengadaan perangkat. Proyek kelurahan dan Universitas Mulawarman.',
         h1='Software house di Samarinda',
         lead='Altora Indonesia berdiri sejak 2019 dan berkantor pusat di Samarinda. Kami mengerjakan aplikasi, website, CCTV, dan perangkat untuk instansi pemerintah, kampus, dan bisnis, di antaranya Pemkot Samarinda dan Universitas Mulawarman.',
         why=[('Kantor pusat di Samarinda', 'Kantor pusat kami di Perum Graha Indah Blok A13, Air Putih, Samarinda Ulu. Kami sudah memasang kios layanan di kantor kelurahan Samarinda serta mengerjakan website dan jaringan CCTV di Universitas Mulawarman.'),
              ('Terbiasa dengan pengadaan instansi', 'Penawaran, faktur, berita acara serah terima, dan dokumentasi pekerjaan kami siapkan untuk kebutuhan administrasi.'),
              ('Bisa datang ke lokasi', 'Survei, pemasangan, dan pelatihan dilakukan langsung di kantor Anda di Samarinda.')],
         needs=[('Kelurahan, kecamatan, dan dinas', 'Kios layanan warga, website resmi, dan aplikasi pelayanan.'),
                ('Kampus dan sekolah', 'Website fakultas, jaringan, dan CCTV kampus.'),
                ('Bisnis dan UMKM', 'Aplikasi kasir, absensi, dan website yang muncul di Google.')],
         proof=['custom-kios-k-pengadaan-hardware', 'unmul-website-redesign', 'unmul-infrastruktur-cctv-jaringan'],
         faq=[('Proyek apa saja yang sudah dikerjakan di Samarinda?', 'Di antaranya pengadaan dan pemasangan kios layanan, PC, dan tablet di kantor kelurahan, serta website dan infrastruktur CCTV & jaringan di Universitas Mulawarman. Detailnya ada di halaman portofolio.'),
              ('Apakah bisa untuk pengadaan instansi pemerintah?', 'Bisa. Kami siapkan penawaran, faktur, dan berita acara serah terima. Produk ber-TKDN tersedia sesuai ketersediaan dari principal.'),
              ('Apakah melayani pembuatan website instansi?', 'Ya. Kami membuat website resmi dan website fakultas yang bisa diperbarui sendiri oleh tim Anda.'),
              ('Bagaimana memulai?', 'Hubungi kami lewat WhatsApp atau form konsultasi. Diskusi awal gratis, lalu kami jadwalkan survei bila diperlukan.')],
         nearby=[('/software-house-balikpapan', 'Software house Balikpapan'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'), ('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website Samarinda')]),
    dict(slug='software-house-kalimantan-timur', city='Kalimantan Timur', area='Kalimantan Timur',
         title='Software House Kalimantan Timur | Altora Indonesia',
         desc='Software house di Kalimantan Timur: aplikasi, website, AI CCTV, fleet management, dan perangkat untuk perusahaan dan instansi di Balikpapan, Samarinda, dan sekitarnya.',
         h1='Software house di Kalimantan Timur',
         lead='Altora Indonesia berkantor pusat di Samarinda sejak 2019, dengan dua cabang di Balikpapan. Kami melayani perusahaan dan instansi di Kalimantan Timur yang butuh aplikasi, website, CCTV pintar, pelacakan armada, internet satelit, atau pengadaan perangkat.',
         why=[('Paham kebutuhan Kaltim', 'Banyak pekerjaan di Kaltim ada di lapangan: tambang, logistik, perkebunan, dan pelayanan publik. Aplikasi kami dirancang untuk dipakai di kantor maupun di lokasi.'),
              ('Aplikasi dan perangkat', 'Kami mengerjakan software sekaligus memasang perangkatnya: CCTV, GPS tracker Teltonika, sensor, dan jaringan.'),
              ('Tim lokal', 'Kantor pusat di Samarinda dan dua cabang di Balikpapan. Tim kami bisa datang untuk survei, pemasangan, dan perawatan.')],
         needs=[('Tambang, kontraktor, dan logistik', 'Fleet management, absensi karyawan lapangan, dan deteksi APD dari CCTV.'),
                ('Perkebunan dan pertanian', 'Sensor kelembapan tanah dan pemantauan lahan lewat aplikasi.'),
                ('Pemerintah daerah dan instansi', 'Website resmi, aplikasi pelayanan, kios layanan, dan pengadaan perangkat.')],
         proof=['fleet-management', 'custom-kios-k-pengadaan-hardware', 'unmul-infrastruktur-cctv-jaringan'],
         faq=[('Kota mana saja yang dilayani?', 'Kantor pusat kami di Samarinda dan cabang di Balikpapan. Kami juga mengerjakan proyek di luar dua kota itu, misalnya untuk Pemkab Barito Utara. Untuk lokasi lain, hubungi kami untuk dicek.'),
              ('Apakah bisa untuk lokasi tambang atau perkebunan yang sinyalnya lemah?', 'Bisa. GPS tracker dan sensor dapat menyimpan data sementara lalu mengirimnya saat sinyal tersedia, dan sistem bisa dijalankan di server lokal.'),
              ('Apakah tersedia GPS tracker untuk alat berat?', 'Ya. Kami memakai GPS tracker Teltonika yang dipilih sesuai jenis kendaraan, termasuk truk dan alat berat.'),
              ('Bagaimana memulai?', 'Hubungi kami lewat WhatsApp atau form konsultasi. Diskusi awal gratis.')],
         nearby=[('/software-house-balikpapan', 'Software house Balikpapan'), ('/software-house-samarinda', 'Software house Samarinda'), ('/katalog', 'Katalog perangkat')]),
]


def page(c):
    url = '/' + c['slug']
    why = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in c['why'])
    needs = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in c['needs'])
    svcs = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for u, t, d in SERVICES)
    proof = ''.join(f'<a class="svd-proof" href="/portfolio/{p}"><span class="svd-proof-img"><img alt="" loading="lazy" src="{PF[p][1]}"/></span><b>{e(PF[p][0])}</b><small>{e(PF[p][2])}</small></a>' for p in c['proof'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c['faq'])
    nearby = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in c['nearby'])
    offices = ''.join(f'<p><b>{e(o["label"])}</b><br/><a href="{e(maps_link(o))}" rel="noopener" target="_blank">{e(one_line(o))}</a></p>' for o in OFFICES)
    msg = f'Halo Altora, saya dari {c["city"]} dan ingin konsultasi kebutuhan software.'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'ProfessionalService', '@id': SITE + url + '#bisnis', 'name': 'Altora Indonesia', 'alternateName': ['Altora', 'Algora Teknologi Indonesia'],
         'description': c['desc'], 'url': SITE + url, 'telephone': '+6285190911170', 'email': 'hello@altora.id',
         'image': SITE + '/assets/img/altora-logo-600.png', 'logo': SITE + '/assets/img/altora-logo-600.png',
         'address': postal_address(next(o for o in OFFICES if (o['city'] == c['city']) or (c['city'] == 'Kalimantan Timur' and o['hq']))),
         'areaServed': {'@type': 'City' if c['area'] != 'Kalimantan Timur' else 'AdministrativeArea', 'name': c['area']},
         'parentOrganization': {'@id': SITE + '/#organization'},
         'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': t}} for _, t, _ in SERVICES]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': c['h1'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]}]}
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(c["title"])}</title><meta content="{e(c["desc"])}" name="description"/><link href="{SITE}{url}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(c["title"])}" property="og:title"/><meta content="{e(c["desc"])}" property="og:description"/><meta content="{SITE}{url}" property="og:url"/><meta content="{SITE}{PF[c['proof'][0]][1]}" property="og:image"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
<main class="ct-page svd-page lc-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/">Beranda</a><span>/</span><span>{e(c["h1"])}</span></nav>
<p class="eyebrow eyebrow-purple">Altora Indonesia · {e(c["city"])}</p><h1>{e(c["h1"])}</h1><p class="ct-lead">{e(c["lead"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#proyek">Lihat proyek</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(PF[c['proof'][0]][0])}" src="{PF[c['proof'][0]][1]}" style="object-position:50% 45%"/><span class="svd-chip svd-chip-0">{e(c["city"])}</span><span class="svd-chip svd-chip-1">Tim lokal</span><span class="svd-chip svd-chip-2">Konsultasi gratis</span></figure>
</div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Kenapa memilih Altora di {e(c["city"])}</h2></div><div class="svd-dos lc-why">{why}</div></div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Kebutuhan yang sering kami kerjakan di {e(c["city"])}</h2></div><ul class="lc-needs">{needs}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Layanan software house kami</h2></div><div class="lc-svcs">{svcs}</div></div></section>
<section class="svd-sec" id="proyek"><div class="ct-wrap"><div class="pd-block-head"><h2>Proyek kami</h2></div><div class="svd-proofs">{proof}</div>
<div class="svd-related"><b>Lihat juga</b>{nearby}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Kantor</h2>{offices}<p><a href="tel:+6285190911170">+62 851-9091-1170</a> · <a href="mailto:hello@altora.id">hello@altora.id</a></p></div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh software house di {e(c["city"])}?</h2><p>Ceritakan kebutuhan Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


for c in CITIES:
    (root / f'{c["slug"]}.html').write_text(page(c), encoding='utf-8')
print('halaman lokal:', ', '.join(c['slug'] for c in CITIES))
