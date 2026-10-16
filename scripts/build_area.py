"""Bangun halaman lokal layanan x kota (mis. /jasa-pasang-cctv-balikpapan) + hub /area-layanan.
Jalankan dari root repo:  python3 scripts/build_area.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py
Setiap halaman = penjelasan layanan yang spesifik + bagian khusus kota (kantor, proyek nyata, kebutuhan lokal).
Jangan menambah kota tanpa fakta lokal yang nyata (risiko 'doorway pages')."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import OFFICES, postal_address
from regions import REGIONS
from regions_nasional import NASIONAL

root = pathlib.Path(__file__).resolve().parent.parent
CSS_VER = '20261016f'
SITE = 'https://altora.id'
WA = 'https://wa.me/6285190911170?text='
e = lambda t: html.escape(t, quote=True)

PF = {
    'instalasi-cctv-ai-analytics': ('Instalasi CCTV AI Analytics', '/assets/img/portfolio/cctv-farmasi.jpg'),
    'unmul-infrastruktur-cctv-jaringan': ('CCTV & jaringan Universitas Mulawarman', '/assets/img/portfolio/unmul-infrastructure/cable-cctv-installation.png'),
    'ai-safety-vision': ('Deteksi APD dari CCTV', '/assets/img/portfolio/safety.jpg'),
    'smart-attendance': ('Absensi wajah dari CCTV', '/assets/img/portfolio/attendance.jpg'),
    'custom-kios-k-pengadaan-hardware': ('Kios & perangkat kelurahan Samarinda', '/assets/img/portfolio/hardware-field/kiosk-baqa-service.jpg'),
    'fleet-management': ('Fleet management armada hauling', '/assets/img/portfolio/fms.jpg'),
    'optimasi-rute-armada': ('Optimasi rute & armada', '/assets/img/portfolio/logistik.jpg'),
    'unmul-website-redesign': ('Redesign website Universitas Mulawarman', '/assets/img/portfolio/feb-unmul.jpg'),
    'website-cms-institusi': ('Website & CMS institusi', '/assets/img/portfolio/feb-unmul.jpg'),
    'website-resmi-institusi': ('Website resmi institusi', '/assets/img/portfolio/farmasi.jpg'),
    'altora-teams': ('Altora Teams (HRIS)', '/assets/img/portfolio/altora-teams-kpi-analytics.jpg'),
    'hris-mobile-payroll': ('HRIS mobile & payroll', '/assets/img/portfolio/hris.jpg'),
    'sistem-antrian-poliklinik': ('Sistem antrian poliklinik', '/assets/img/portfolio/clinic.jpg'),
    'pompy-batara': ('POMPY BATARA, portal peta tematik Barito Utara', '/assets/img/portfolio/pompy-batara-platform-cropped.jpg'),
}

CITIES = {
    'balikpapan': dict(name='Balikpapan',
        base='Kami punya dua cabang di Balikpapan: Jl. Soekarno Hatta, Muara Rapak (Balikpapan Utara) dan Pasar Baru. Tim bisa datang untuk survei, pemasangan, dan perbaikan di lokasi Anda di Balikpapan.',
        sectors='perusahaan jasa migas, logistik, kontraktor, perkantoran, sekolah, klinik, dan UMKM',
        local_proof=[], office='balikpapan-utara', near=['samarinda', 'penajam-paser-utara', 'ikn']),
    'samarinda': dict(name='Samarinda',
        base='Kantor pusat kami di Perum Graha Indah Blok A13, Air Putih, Samarinda Ulu. Kami sudah memasang kios di kantor kelurahan serta mengerjakan jaringan, CCTV, dan website di Universitas Mulawarman.',
        sectors='kantor kelurahan dan dinas, kampus, sekolah, klinik, perkantoran, dan UMKM',
        local_proof=['custom-kios-k-pengadaan-hardware', 'unmul-infrastruktur-cctv-jaringan'], office='samarinda', near=['balikpapan', 'kutai-kartanegara', 'bontang']),
}
OFFICE_BY_KEY = {o['key']: o for o in OFFICES}
for _k, _r in REGIONS.items():
    _o = OFFICE_BY_KEY[_r['office']]
    CITIES[_k] = dict(_r, local_proof=[],
                      base=f"{_r['name']} kami layani dari {_o['label'].lower()} ({_o['city']}). Untuk survei, pemasangan, dan perawatan, tim kami datang ke lokasi sesuai jadwal; kendala ringan dibantu jarak jauh lewat WhatsApp.")


# Kota di luar Kaltim: hanya layanan jarak jauh (lihat regions_nasional.py)
REMOTE_SERVICES = ('website', 'aplikasi')
for _k, _r in NASIONAL.items():
    CITIES[_k] = dict(_r, local_proof=_r.get('proof', []), office='samarinda', scope='nasional',
                      base=f"Untuk klien di {_r['name']}, aplikasi dan website kami kerjakan jarak jauh dari kantor pusat di Samarinda: diskusi lewat video call, demo berkala di server uji, lalu serah terima, pelatihan, dan dukungan secara online. Pertemuan langsung bisa dijadwalkan bila diperlukan.")


def is_nasional(ckey):
    return CITIES[ckey].get('scope') == 'nasional'


def services_for(ckey):
    return [k for k in SERVICES if not is_nasional(ckey) or k in REMOTE_SERVICES]


def office_of(c):
    return OFFICE_BY_KEY[c['office']]


def near_of(ckey):
    return [k for k in CITIES[ckey].get('near', []) if k in CITIES][:3]


def needs_html(c):
    if not c.get('needs'):
        return ''
    items = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in c['needs'])
    return (f'<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Kebutuhan yang sering muncul di {e(c["name"])}</h2>'
            f'<p>{e(c["name"])} ({e(c["seat"])}): {e(c["sectors"])}.</p></div><div class="svd-dos">{items}</div></div></section>')

SERVICES = {
    'cctv': dict(slug='jasa-pasang-cctv-{c}', h1='Jasa pasang CCTV di {C}', short='Pasang CCTV',
        title='Jasa Pasang CCTV {C} | Altora Indonesia',
        desc='Jasa pasang CCTV di {C}: survei titik, kamera IP & NVR, pantau dari HP, CCTV pintar dengan AI, dan perawatan berkala oleh tim Altora.',
        lead='Pemasangan CCTV untuk kantor, gudang, toko, sekolah, dan area proyek di {C}. Mulai dari survei titik kamera, pemasangan, sampai bisa dipantau dari HP, lalu dirawat secara berkala.',
        hero='/assets/img/portfolio/unmul-infrastructure/cable-cctv-installation.png',
        dos=[('Survei titik kamera', 'Kami tentukan posisi kamera supaya area penting terlihat jelas dan tidak ada titik buta.'),
             ('Kamera IP & NVR', 'Kamera dan perekam dari principal resmi seperti VIGI, dengan garansi resmi.'),
             ('Pantau dari HP', 'Rekaman langsung dan rekaman lama bisa dibuka dari HP atau komputer.'),
             ('CCTV pintar (AI)', 'Tambahan deteksi APD, absensi wajah, atau alert area terlarang dari kamera yang sama.'),
             ('CCTV tenaga surya', 'Untuk lokasi tanpa listrik atau kabel, seperti proyek, kebun, dan tambak.'),
             ('Perawatan berkala', 'Pembersihan kamera, cek rekaman, dan update firmware.')],
        faq=[('Berapa kamera yang dibutuhkan?', 'Tergantung luas area dan titik yang ingin dipantau. Jumlah pastinya kami tentukan saat survei, supaya tidak berlebihan.'),
             ('Apakah bisa dipantau dari HP?', 'Bisa. Setelah terpasang, kami bantu atur aplikasinya di HP Anda.'),
             ('Rekaman tersimpan berapa lama?', 'Tergantung kapasitas penyimpanan dan jumlah kamera. Kami hitung bersama saat survei sesuai kebutuhan Anda.'),
             ('CCTV lama bisa ditambah fitur AI?', 'Sering kali bisa, tergantung posisi dan kualitas kamera. Kami cek saat survei.')],
        proof=['instalasi-cctv-ai-analytics', 'unmul-infrastruktur-cctv-jaringan', 'ai-safety-vision'],
        main='/services/ai-cctv', main_label='Layanan AI CCTV & Safety'),
    'itsupport': dict(slug='it-support-{c}', h1='IT support di {C}', short='IT support',
        title='IT Support {C} | Komputer, Jaringan & Server | Altora',
        desc='IT support di {C} untuk kantor dan instansi: perawatan komputer, jaringan & WiFi, server, CCTV, dan bantuan teknis lewat WhatsApp maupun datang ke lokasi.',
        lead='Bantuan teknis untuk kantor, instansi, dan usaha di {C}: komputer, jaringan, WiFi, server, printer, dan CCTV. Bisa lewat WhatsApp untuk masalah ringan, atau teknisi datang ke lokasi.',
        hero='/assets/img/portfolio/hardware-field/aio-baqa.jpg',
        dos=[('Komputer & laptop', 'Instalasi, perawatan, perbaikan, dan pengadaan unit baru.'),
             ('Jaringan & WiFi', 'Internet lambat atau sering putus? Kami cek dan rapikan jaringan kantor.'),
             ('Server & backup', 'Pemasangan server, penyimpanan data, dan backup berkala.'),
             ('CCTV & perangkat kantor', 'Printer, CCTV, akses pintu, dan perangkat lain di kantor.'),
             ('Bantuan lewat WhatsApp', 'Masalah ringan dibantu jarak jauh tanpa menunggu teknisi datang.'),
             ('Kunjungan berkala', 'Pengecekan rutin sesuai kesepakatan supaya masalah ketahuan lebih awal.')],
        faq=[('Apakah bisa kontrak bulanan?', 'Bisa. Cakupan dan frekuensi kunjungan disesuaikan dengan jumlah perangkat dan kebutuhan kantor Anda.'),
             ('Apakah melayani panggilan sekali datang?', 'Hubungi kami lewat WhatsApp untuk menjelaskan masalahnya, lalu kami sampaikan cara penanganannya.'),
             ('Apakah bisa sekalian pengadaan perangkat?', 'Bisa. Kami mengadakan komputer, perangkat jaringan, dan CCTV dari principal resmi.'),
             ('Bagaimana dengan keamanan data?', 'Kami bantu mengatur akses, backup, dan pembaruan sistem. Akses ke data Anda hanya dipakai untuk pekerjaan yang disepakati.')],
        proof=['custom-kios-k-pengadaan-hardware', 'unmul-infrastruktur-cctv-jaringan', 'instalasi-cctv-ai-analytics'],
        main='/services/pengadaan-instalasi-maintenance', main_label='Pengadaan, instalasi & maintenance'),
    'jaringan': dict(slug='jasa-instalasi-jaringan-{c}', h1='Jasa instalasi jaringan & WiFi di {C}', short='Instalasi jaringan',
        title='Jasa Instalasi Jaringan & WiFi {C} | Altora Indonesia',
        desc='Instalasi jaringan LAN, WiFi kantor, fiber optik, rak server, dan wireless bridge antar gedung di {C}, lengkap dengan dokumentasi dan perawatan.',
        lead='Instalasi jaringan kabel, WiFi, fiber optik, dan rak server untuk kantor, kampus, gudang, dan instansi di {C}. Dipasang rapi, diuji, dan didokumentasikan.',
        hero='/assets/img/portfolio/unmul-infrastructure/network-rack.png',
        dos=[('Jaringan LAN', 'Penarikan kabel, switch, dan penataan rak yang rapi.'),
             ('WiFi kantor', 'Access point dengan sinyal merata, termasuk untuk ruangan luas.'),
             ('Fiber optik', 'Penyambungan dan pengujian jalur fiber dengan alat ukur yang tepat.'),
             ('Rak server', 'Close rack, wallmount, dan penataan perangkat di ruang server.'),
             ('Antar gedung', 'Wireless bridge untuk menghubungkan gedung yang berjauhan tanpa kabel.'),
             ('Dokumentasi', 'Denah jalur, daftar perangkat, dan akses diserahkan setelah selesai.')],
        faq=[('WiFi kantor sering lemah di beberapa ruangan, bisa diperbaiki?', 'Bisa. Kami cek posisi access point dan sumber gangguan, lalu atur ulang atau tambah titik bila perlu.'),
             ('Apakah bisa menyambung dua gedung tanpa kabel?', 'Bisa, dengan wireless bridge, tergantung jarak dan halangan di antara gedung.'),
             ('Perangkat apa yang dipakai?', 'Perangkat dari principal resmi, misalnya TP-Link untuk jaringan dan HaganeRack untuk rak server.'),
             ('Apakah ada dokumentasi setelah selesai?', 'Ada: denah jalur, daftar perangkat, dan akses diserahkan bersama berita acara.')],
        proof=['unmul-infrastruktur-cctv-jaringan', 'custom-kios-k-pengadaan-hardware', 'instalasi-cctv-ai-analytics'],
        main='/services/pengadaan-instalasi-maintenance', main_label='Pengadaan, instalasi & maintenance'),
    'gps': dict(slug='gps-tracker-kendaraan-{c}', h1='GPS tracker kendaraan di {C}', short='GPS tracker',
        title='GPS Tracker Kendaraan {C} | Pasang & Fleet Management',
        desc='Pemasangan GPS tracker kendaraan di {C} untuk mobil, truk, dan alat berat. Pantau posisi, rute, dan BBM lewat dashboard Altora FMS.',
        lead='Pemasangan GPS tracker Teltonika untuk mobil operasional, truk, dan alat berat di {C}. Posisi, rute, dan data kendaraan bisa dipantau dari dashboard dan HP.',
        hero='/assets/img/produk/fms.webp',
        dos=[('Pilih perangkat yang sesuai', 'Tracker untuk mobil, motor, truk, atau alat berat, dipilih sesuai kebutuhan data.'),
             ('Pemasangan di kendaraan', 'Dipasang rapi oleh teknisi, termasuk untuk armada dalam jumlah banyak.'),
             ('Pantau posisi & rute', 'Posisi live, riwayat perjalanan, dan alert saat keluar area.'),
             ('Data BBM & mesin', 'Level BBM dan odometer pada kendaraan yang mendukung.'),
             ('Kamera kendaraan', 'Dashcam dan deteksi kantuk pengemudi untuk keselamatan.'),
             ('Laporan armada', 'Rekap jarak tempuh, jam operasi, dan perilaku mengemudi.')],
        faq=[('Merek GPS tracker apa yang dipakai?', 'Teltonika, dipilih sesuai jenis kendaraan dan data yang dibutuhkan.'),
             ('Apakah bisa untuk alat berat dan truk tambang?', 'Bisa. Ada perangkat untuk kendaraan berat, termasuk pembacaan data mesin pada kendaraan yang mendukung.'),
             ('Bagaimana kalau di lokasi sinyalnya lemah?', 'Tracker menyimpan data sementara dan mengirimnya saat sinyal kembali.'),
             ('Dipantau lewat apa?', 'Lewat dashboard Altora FMS di komputer dan HP.')],
        proof=['fleet-management', 'optimasi-rute-armada'],
        main='/services/fleet-management-service', main_label='Layanan fleet management'),
    'website': dict(slug='jasa-pembuatan-website-{c}', h1='Jasa pembuatan website di {C}', short='Pembuatan website',
        title='Jasa Pembuatan Website {C} | Altora Indonesia',
        desc='Jasa pembuatan website di {C}: company profile, website instansi, dan landing page yang cepat di HP, mudah diperbarui, dan disusun agar mudah ditemukan di Google.',
        lead='Website company profile, website instansi, dan landing page untuk bisnis dan organisasi di {C}. Cepat dibuka di HP, isinya bisa diperbarui sendiri, dan disusun supaya mudah ditemukan di Google.',
        hero='/assets/img/portfolio/feb-unmul.jpg',
        dos=[('Company profile', 'Menjelaskan layanan, portofolio, dan kontak dengan jelas.'),
             ('Website instansi', 'Berita, layanan publik, dan dokumen yang mudah dicari warga.'),
             ('Landing page', 'Satu halaman fokus untuk promosi atau layanan tertentu.'),
             ('Bisa diperbarui sendiri', 'Dilengkapi CMS supaya tim Anda bisa mengubah isi tanpa developer.'),
             ('SEO lokal', 'Disusun supaya muncul saat orang mencari layanan Anda di {C}.'),
             ('Domain, hosting & keamanan', 'Kami bantu urus domain, SSL, dan perawatan berkala.')],
        faq=[('Berapa lama pembuatan website?', 'Tergantung jumlah halaman dan kesiapan isi seperti foto dan teks. Jadwalnya kami sampaikan di penawaran.'),
             ('Apakah bisa memperbarui isi sendiri?', 'Bisa. Website dapat dilengkapi CMS sehingga tim Anda bisa menambah berita atau mengubah isi.'),
             ('Apakah website lama bisa diperbaiki?', 'Bisa. Kami audit dulu, lalu putuskan apakah cukup diperbaiki atau perlu dibuat ulang.'),
             ('Apakah langsung muncul di Google?', 'Website kami susun dan daftarkan ke Google. Peringkat terbentuk bertahap, tergantung persaingan dan isi.')],
        proof=['unmul-website-redesign', 'website-cms-institusi', 'website-resmi-institusi'],
        main='/services/website-seo', main_label='Layanan website & SEO'),
    'aplikasi': dict(slug='jasa-pembuatan-aplikasi-{c}', h1='Jasa pembuatan aplikasi di {C}', short='Pembuatan aplikasi',
        title='Jasa Pembuatan Aplikasi {C} | Web & Android | Altora',
        desc='Jasa pembuatan aplikasi web dan HP di {C} untuk absensi, HRIS, approval, antrian, dan laporan. Bisa mulai dari aplikasi jadi atau dibuat khusus.',
        lead='Aplikasi web dan HP untuk perusahaan, instansi, dan usaha di {C}: absensi, HRIS, approval, antrian, stok, dan laporan. Bisa memakai aplikasi Altora yang sudah jadi, atau dibuat khusus sesuai proses Anda.',
        hero='/assets/img/produk/teams.webp',
        dos=[('Aplikasi web', 'Dibuka dari browser di komputer maupun HP.'),
             ('Aplikasi HP', 'Untuk absensi GPS, kamera, notifikasi, dan pemakaian di lapangan.'),
             ('HRIS & absensi', 'Absensi, cuti, lembur, KPI, dan payroll.'),
             ('Approval & dokumen', 'Pengajuan dan persetujuan tanpa kertas dan chat yang tercecer.'),
             ('Dashboard & laporan', 'Ringkasan yang siap dibaca pimpinan.'),
             ('Integrasi', 'Tersambung ke aplikasi lama, mesin absensi, CCTV, atau GPS tracker.')],
        faq=[('Lebih baik aplikasi jadi atau dibuat khusus?', 'Kalau prosesnya umum seperti absensi atau kasir, aplikasi jadi biasanya cukup dan lebih cepat. Kalau prosesnya khusus, lebih tepat dibuat khusus.'),
             ('Siapa pemilik source code dan data?', 'Kepemilikan dibahas dan ditulis di kontrak sejak awal.'),
             ('Apakah ada pendampingan setelah aplikasi jadi?', 'Ada pelatihan pengguna dan dukungan setelah aplikasi dipakai, sesuai kesepakatan.')],
        proof=['altora-teams', 'hris-mobile-payroll', 'sistem-antrian-poliklinik'],
        main='/services/software-custom', main_label='Layanan software custom'),
}


def fmt(t, c):
    return t.replace('{C}', c['name']).replace('{c}', c['key'])


def page(skey, ckey):
    s = SERVICES[skey]; c = dict(CITIES[ckey], key=ckey)
    url = '/' + fmt(s['slug'], c)
    h1 = fmt(s['h1'], c); title = fmt(s['title'], c); desc = fmt(s['desc'], c)
    if len(title) > 65:
        title = f'{s["short"]} {c["name"]} | Altora Indonesia'
    if len(desc) > 160:
        desc = desc[:157].rsplit(' ', 1)[0].rstrip(',.:;') + '.'
    dos = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(fmt(d, c))}</p></article>' for t, d in s['dos'])
    nas = c.get('scope') == 'nasional'
    proof_ids = list(dict.fromkeys(c['local_proof'] + s['proof']))[:3] if (nas or skey in ('cctv', 'itsupport', 'jaringan')) else s['proof'][:3]
    proof = ''.join(f'<a class="svd-proof" href="/portfolio/{p}"><span class="svd-proof-img"><img alt="" loading="lazy" src="{PF[p][1]}"/></span><b>{e(PF[p][0])}</b><small>Lihat proyek</small></a>' for p in proof_ids)
    last_q = (f'Apakah bisa dikerjakan dari jauh untuk klien di {c["name"]}?' if nas else f'Apakah tim Altora bisa datang ke lokasi di {c["name"]}?')
    faq_items = [(fmt(q, c), fmt(a, c)) for q, a in s['faq']] + [(last_q, c['base'])]
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq_items)
    near = near_of(ckey)
    same_city = ''.join(f'<a href="/{fmt(SERVICES[k]["slug"], dict(CITIES[ckey], key=ckey))}">{e(SERVICES[k]["short"])} {e(c["name"])}</a>' for k in services_for(ckey) if k != skey)
    links = (''.join(f'<a href="/{fmt(s["slug"], dict(CITIES[k], key=k))}">{e(s["short"])} {e(CITIES[k]["name"])}</a>' for k in near) +
             f'<a href="{s["main"]}">{e(s["main_label"])}</a><a href="/software-house-{ckey}">Software house {e(c["name"])}</a>' + same_city)
    msg = f'Halo Altora, saya di {c["name"]} dan butuh {s["short"].lower()}.'
    clients_p = '' if c.get('needs') else f'<p>Klien kami di {e(c["name"])} antara lain {e(c["sectors"])}.</p>'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': h1, 'description': desc, 'url': SITE + url, 'serviceType': s['short'],
         'areaServed': {'@type': 'City', 'name': c['name']},
         'provider': {'@type': 'ProfessionalService', 'name': 'Altora Indonesia', 'alternateName': ['Altora', 'Algora Teknologi Indonesia'],
                      'url': SITE + '/', 'telephone': '+6285190911170', 'image': SITE + '/assets/img/altora-logo-600.png',
                      'address': postal_address(office_of(c))}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Area layanan', 'item': SITE + '/area-layanan'},
            {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items]}]}
    body = f'''<main class="ct-page svd-page lc-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/area-layanan">Area layanan</a><span>/</span><span>{e(c["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">Altora Indonesia · {e(c["name"])}{", " + e(c["seat"]) if nas else ""}</p><h1>{e(h1)}</h1><p class="ct-lead">{e(fmt(s["lead"], c))}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#proyek">Lihat proyek</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(h1)}" src="{s["hero"]}" style="object-position:50% 45%"/><span class="svd-chip svd-chip-0">{e(c["name"])}</span><span class="svd-chip svd-chip-1">{"Dikerjakan jarak jauh" if nas else "Tim lokal"}</span><span class="svd-chip svd-chip-2">Konsultasi gratis</span></figure>
</div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang kami kerjakan</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>{"Cara kami bekerja untuk klien di " + e(c["name"]) if nas else "Melayani " + e(c["name"])}</h2><p>{e(c["base"])}</p>{clients_p}</div></div></section>
{needs_html(c)}
<section class="svd-sec" id="proyek"><div class="ct-wrap"><div class="pd-block-head"><h2>Proyek terkait</h2></div><div class="svd-proofs">{proof}</div>
<div class="svd-related"><b>Lihat juga</b>{links}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh {e(s["short"].lower())} di {e(c["name"])}?</h2><p>Ceritakan kebutuhan Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    return url, h1, shell(title, desc, url, SITE + s['hero'], ld, body)


def shell(title, desc, url, img, ld, body):
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title><meta content="{e(desc)}" name="description"/><link href="{SITE}{url}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="{SITE}{url}" property="og:url"/><meta content="{img}" property="og:image"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
{body}
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


def hub(built):
    rows = ''
    nat = ''
    for ckey, cdat in CITIES.items():
        if is_nasional(ckey):
            links = ''.join(f'<a href="{u}">{e(h)}</a>' for (ck, u, h) in built if ck == ckey)
            nat += f'<div class="pk-hubcity"><h3>{e(cdat["name"])} <small>{e(cdat["seat"])}</small></h3><div class="svd-related"><a href="/software-house-{ckey}">Software house {e(cdat["name"])}</a>{links}</div></div>'
            continue
        links = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(h)}</b></a>' for (ck, u, h) in built if ck == ckey)
        rows += (f'<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>{e(cdat["name"])}</h2><p>{e(cdat["base"])}</p></div>'
                 f'<div class="lc-svcs"><a class="lc-svc" href="/software-house-{ckey}"><b>Software house {e(cdat["name"])}</b></a>{links}</div></div></section>')
    body = ('<main class="ct-page svd-page lc-page"><section class="svd-hero"><div class="ct-wrap"><p class="eyebrow eyebrow-purple">Area layanan</p>'
            '<h1>Area layanan Altora di Kalimantan Timur</h1><p class="ct-lead">Kantor pusat di Samarinda dan dua cabang di Balikpapan. Dari sana kami melayani seluruh Kalimantan Timur, termasuk Bontang, Kutai Kartanegara, Kutai Timur, Kutai Barat, Mahakam Ulu, Berau, Paser, Penajam Paser Utara, dan IKN Nusantara.</p></div></section>'
            + rows +
            '<section class="svd-sec" id="nasional"><div class="ct-wrap"><div class="pd-block-head"><h2>Di luar Kalimantan Timur</h2>'
            '<p>Untuk kota lain di Indonesia kami mengerjakan aplikasi, website, dan sistem secara jarak jauh dari Samarinda. Pemasangan perangkat di luar Kaltim dibahas per proyek.</p></div>'
            + nat + '</div></section>' +
            '<section class="svd-sec"><div class="ct-wrap"><div class="svd-related"><b>Wilayah lain</b><a href="/software-house-kalimantan-timur">Software house Kalimantan Timur</a><a href="/contact">Lokasi lain? Hubungi kami</a></div></div></section>'
            '</main>')
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Area layanan Altora', 'url': SITE + '/area-layanan'}
    return shell('Area Layanan Altora | Kaltim & Seluruh Indonesia', 'CCTV, IT support, jaringan, GPS, Starlink, dan pengadaan di seluruh Kaltim, plus aplikasi dan website untuk Surabaya, Jakarta, Makassar, dan kota lain.', '/area-layanan', SITE + '/assets/img/altora-logo-600.png', ld, body)


def update_sitemap(urls):
    sm = root / 'sitemap.xml'; s = sm.read_text(encoding='utf-8')
    for u in urls:
        if f'<loc>{SITE}{u}</loc>' not in s:
            s = s.replace('</urlset>', f'  <url><loc>{SITE}{u}</loc><lastmod>2026-10-13</lastmod><priority>0.8</priority></url>\n</urlset>')
    sm.write_text(s, encoding='utf-8')


if __name__ == '__main__':
    built = []
    for ckey in CITIES:
        for skey in services_for(ckey):
            url, h1, htmlp = page(skey, ckey)
            (root / (url.lstrip('/') + '.html')).write_text(htmlp, encoding='utf-8')
            built.append((ckey, url, h1))
    (root / 'area-layanan.html').write_text(hub(built), encoding='utf-8')
    update_sitemap([u for _, u, _ in built] + ['/area-layanan'])
    print('area:', len(built), 'halaman +', '/area-layanan')
