"""Bangun halaman lokal 'software house <kota>' dari data CITIES.
Jalankan dari root repo:  python3 scripts/build_local.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py
Isi setiap kota harus berbeda dan hanya memakai fakta yang bisa dipertanggungjawabkan.

Tiga halaman utama (Samarinda, Balikpapan, Kalimantan Timur) memakai konten lokal lengkap: kantor + peta, proyek nyata dari
portofolio_data, layanan, tim, area kunjungan, FAQ lokal, dan tautan ke halaman layanan per kota (masing-masing punya maksud
pencarian berbeda supaya tidak saling bersaing). Kota di luar Kalimantan: noindex,follow (lihat regions_nasional.is_indexed)."""
import html, json, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import (OFFICES, ORG_ID, FACTS, PHONE_DISPLAY, EMAIL, one_line, with_city, label_lc, maps_link, org, office_node, office_id, map_html)
from portofolio_data import BY as PF, card as pf_card

root = pathlib.Path(__file__).resolve().parent.parent
CSS_VER = '20261016i'
LOCAL_CSS = '/assets/css/local-seo.css?v=20261119a'
PF_CSS = '/assets/css/portofolio.css?v=20261118p'
SITE = 'https://altora.id'
WA = 'https://wa.me/6285190911170?text='
TODAY = '2026-11-18'
e = lambda t: html.escape(t, quote=True)

SERVICES = [
    ('/services/software-custom', 'Aplikasi & software custom', 'Web app, aplikasi HP, approval, dan laporan internal.'),
    ('/services/website-seo', 'Website', 'Company profile, website instansi, dan landing page yang cepat dan mudah diperbarui.'),
    ('/services/seo', 'SEO', 'Audit, perbaikan on-page, dan SEO lokal supaya mudah ditemukan di Google.'),
]
# Daftar layanan lengkap untuk halaman kota utama. 'home' = layanan perangkat rumahan/kantor kecil, khusus Samarinda.
SERVICES_FULL = [
    ('/services/software-custom', 'Software custom', 'Sistem internal, approval, ERP ringan, dan integrasi mengikuti proses Anda.', ''),
    ('/services/web-custom', 'Aplikasi web', 'Portal, dashboard, dan aplikasi berbasis browser yang dibangun dari nol.', ''),
    ('/services/mobile-app-custom', 'Aplikasi mobile', 'Android dan iOS untuk tim lapangan, absensi GPS, dan pelanggan.', ''),
    ('/services/website-seo', 'Pembuatan website', 'Company profile dan website instansi dengan CMS yang bisa diperbarui sendiri.', ''),
    ('/services/seo', 'SEO', 'Audit teknis, on-page, dan SEO lokal supaya mudah ditemukan di Google.', ''),
    ('/services/ai-custom', 'AI custom', 'Analitik CCTV, pengenalan wajah, otomasi dokumen, dan analisis data.', ''),
    ('/services/iot-custom', 'IoT', 'Sensor suhu, asap, cuaca, dan kelembapan yang tersambung ke dashboard.', ''),
    ('/services/tracking', 'Tracking armada', 'GPS tracker, telematik, dan dashboard armada serta aset.', ''),
    ('/pengadaan', 'Pengadaan & pemasangan perangkat', 'CCTV, jaringan, server rack, GPS tracker, videotron, dan komputer untuk perusahaan dan instansi di Kaltim.', ''),
    ('/services/cctv', 'Pasang CCTV', 'Survei, pemasangan, dan perawatan CCTV, termasuk tenaga surya dan 4G.', 'home'),
    ('/services/smart-lock', 'Smart lock & smart home', 'Kunci pintu digital, akses tamu, dan perangkat rumah pintar.', 'home'),
    ('/services/it-support', 'IT support bulanan', 'Komputer, jaringan, server, dan backup untuk kantor.', 'home'),
]
HERO = '/assets/img/apps/office-board.webp'
HERO_ALT = 'Tampilan Altora Office, aplikasi manajemen proyek buatan Altora Indonesia'
STATS = [(FACTS['since'], 'berdiri di Samarinda'), (FACTS['projects'], 'proyek terdeliver'), (FACTS['team'], 'ahli in-house'), ('PKP', 'terdaftar di Inaproc/LKPP')]
OFFICE = {o['key']: o for o in OFFICES}

FREELANCE_QA = ('Apa bedanya software house dengan freelancer?',
                'Freelancer cocok untuk pekerjaan kecil yang lingkupnya sudah jelas. Software house seperti Altora bekerja sebagai tim dan badan usaha: '
                'analisis, desain, pengembangan, pengujian, pelatihan, dan dukungan ditangani tim yang sama, ada kontrak tertulis, faktur pajak (PKP), '
                'dokumentasi, dan penyerahan kode sumber sesuai kontrak, sehingga sistem tetap bisa dirawat walau ada pergantian orang.')
PRICE_QA = lambda city: (f'Berapa biaya pembuatan aplikasi atau website di {city}?',
                         'Biaya bergantung pada lingkup, jumlah modul, dan integrasi yang dibutuhkan, jadi kami tidak memasang daftar harga di situs. '
                         'Ceritakan kebutuhan Anda lewat WhatsApp; setelah lingkupnya jelas, kami kirim penawaran tertulis. Diskusi awal gratis.')
TIME_QA = ('Berapa lama pembuatan aplikasi atau website?',
           'Tergantung lingkup dan kesiapan bahan. Jadwal ditulis di penawaran dan progres ditunjukkan lewat demo berkala. '
           'Untuk sistem yang lebih besar, kami sarankan mulai dari pilot 2–4 minggu dengan indikator yang jelas sebelum diperluas.')
SUPPORT_QA = ('Apakah ada maintenance setelah aplikasi selesai?',
              'Ada. Setelah serah terima, kami melatih pengguna lalu memberi dukungan lewat WhatsApp (dibalas di jam kerja), akses jarak jauh, '
              'dan kunjungan ke lokasi bila perlu. Cakupan pemeliharaan, pembaruan, dan backup ditulis di kontrak.')

# Panduan (artikel informasional) yang ditautkan dari halaman kota utama. Halaman kota = niat komersial,
# artikel = niat informasional; artikelnya menaut balik ke /software-house-samarinda, /software-house-balikpapan, dan /contact.
GUIDES = [('/blog/cara-memilih-software-house-samarinda-balikpapan', 'Cara memilih software house', '8 pertanyaan sebelum tanda tangan kontrak.'),
          ('/blog/software-house-vs-freelancer-kaltim', 'Software house atau freelancer?', 'Kapan freelancer cukup, kapan perlu tim dan badan usaha.'),
          ('/blog/vendor-aplikasi-lokal-atau-luar-kaltim', 'Vendor lokal atau dari luar Kaltim?', 'Bagian proyek yang dipengaruhi jarak, dan yang tidak.'),
          ('/blog/contoh-aplikasi-instansi-perusahaan-kaltim', 'Contoh aplikasi di Kalimantan Timur', 'Kampus, klinik, tambang, logistik, dan perkebunan.')]


def guides_html():
    items = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for u, t, d in GUIDES)
    return ('<section class="svd-sec" id="panduan"><div class="ct-wrap"><div class="pd-block-head"><h2>Panduan sebelum memilih software house</h2>'
            '<p>Bahan pertimbangan yang bisa Anda baca dulu sebelum menghubungi vendor mana pun.</p></div>'
            f'<div class="lc-svcs">{items}</div></div></section>')


CITIES = [
    dict(slug='software-house-samarinda', city='Samarinda', area='Samarinda', rich=True, offices=['samarinda'],
         title='Software House Samarinda – Pembuatan Aplikasi & Website | Altora',
         desc='Software house Samarinda sejak 2019: jasa pembuatan aplikasi, website, SEO, AI, dan IoT. Kantor pusat di Palaran, 50+ proyek, terdaftar Inaproc.',
         h1='Software house Samarinda untuk aplikasi, website, dan sistem bisnis',
         eyebrow='Altora Indonesia · Kantor pusat Samarinda',
         lead='Altora Indonesia adalah software house yang berkantor pusat di Samarinda sejak 2019. Tim in-house kami membuat aplikasi custom, website, SEO, AI, dan IoT, lalu memasang perangkatnya, untuk instansi, kampus, dan perusahaan di Samarinda.',
         about=['Altora Indonesia berkantor pusat di Jl. Dayak ASB, Bukuan, Kecamatan Palaran, Kota Samarinda, Kalimantan Timur, dan beroperasi sejak 2019. '
                'Lebih dari 50 proyek sudah kami selesaikan bersama 13 ahli in-house, mulai dari aplikasi web dan HP, website instansi, sampai CCTV siap AI dan sistem absensi pengenalan wajah.',
                'Di Samarinda, klien kami antara lain Pemerintah Kota Samarinda dan Universitas Mulawarman. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, '
                'sehingga bisa melayani pengadaan instansi dengan penawaran, faktur pajak, dan berita acara serah terima yang lengkap.'],
         why=[('Kantor pusat di Samarinda', 'Kantor pusat kami di Jl. Dayak ASB, Bukuan, Kec. Palaran. Diskusi, demo, dan pelatihan bisa di kantor kami atau di lokasi Anda.'),
              ('Software dan perangkat, satu tim', 'Aplikasi, kamera, sensor, dan jaringan dikerjakan tim in-house yang sama, jadi tidak ada saling lempar tanggung jawab.'),
              ('Terbiasa dengan administrasi instansi', 'PKP dan terdaftar di Inaproc/LKPP. Penawaran, faktur, dan berita acara serah terima kami siapkan.')],
         needs=[('Kelurahan, kecamatan, dan dinas', 'Website resmi, anjungan layanan mandiri, dan aplikasi pelayanan yang mudah dipakai warga dan petugas.'),
                ('Kampus dan sekolah', 'Website fakultas, absensi pengenalan wajah, CCTV, dan aplikasi administrasi.'),
                ('Klinik, perusahaan, dan UMKM', 'Sistem antrian, HRIS, stok, dan website yang muncul di Google.')],
         proof=['cctv-ai-farmasi-unmul', 'smart-attendance-unmul', 'website-feb-unmul', 'smartlock-farmasi-unmul', 'antrian-poliklinik', 'fleet-radio-kapal'],
         proof_head='Proyek nyata di Samarinda',
         proof_note='Klien kami di Samarinda antara lain Pemerintah Kota Samarinda dan Universitas Mulawarman (Fakultas Farmasi, Fakultas Ekonomi dan Bisnis).',
         intents=[('/jasa-pembuatan-aplikasi-samarinda', 'Jasa pembuatan aplikasi Samarinda', 'Butuh aplikasi web atau Android untuk approval, absensi, stok, atau laporan.'),
                  ('/jasa-pembuatan-software-samarinda', 'Jasa pembuatan software Samarinda', 'Sistem internal dan integrasi untuk operasional perusahaan.'),
                  ('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website Samarinda', 'Company profile, website instansi, dan landing page.'),
                  ('/jasa-seo-samarinda', 'Jasa SEO Samarinda', 'Website sudah ada, tapi belum muncul di Google.'),
                  ('/jasa-pasang-cctv-samarinda', 'Jasa pasang CCTV Samarinda', 'CCTV kantor, rumah, dan gudang, termasuk tenaga surya.'),
                  ('/it-support-samarinda', 'IT support Samarinda', 'Perawatan komputer, jaringan, dan server kantor.')],
         visit=('Tim kami datang untuk survei, diskusi kebutuhan, pemasangan, dan pelatihan di seluruh Samarinda: Palaran, Samarinda Ilir, Samarinda Kota, '
                'Samarinda Seberang, Samarinda Ulu, Samarinda Utara, Sambutan, Sungai Kunjang, Sungai Pinang, dan Loa Janan Ilir, '
                'juga ke Kutai Kartanegara dan Bontang sesuai jadwal.'),
         directions=('Kantor pusat berada di Kelurahan Bukuan, Kecamatan Palaran, di sisi selatan Sungai Mahakam. Kabari kami lewat WhatsApp sebelum datang '
                     'supaya tim yang menangani kebutuhan Anda ada di kantor, lalu pakai tombol Petunjuk arah untuk rute dari lokasi Anda.'),
         faq=[('Apa software house di Samarinda yang bisa membuat aplikasi custom?',
               'Altora Indonesia adalah software house yang berkantor pusat di Jl. Dayak ASB, Bukuan, Kec. Palaran, Samarinda, sejak 2019. '
               'Kami membuat aplikasi web dan HP, website, SEO, AI, dan IoT, dengan lebih dari 50 proyek dan 13 ahli in-house.'),
              ('Di mana alamat kantor Altora di Samarinda?',
               'Kantor pusat Altora Indonesia: Jl. Dayak ASB, Bukuan, Kecamatan Palaran, Kota Samarinda, Kalimantan Timur. Telepon/WhatsApp +62 851-9091-1170, email hello@altora.id.'),
              ('Bisakah saya datang ke kantor, atau tim yang datang ke lokasi saya?',
               'Keduanya bisa. Kabari kami lewat WhatsApp untuk mengatur jadwal. Di Samarinda tim kami biasa datang untuk survei, demo, dan pelatihan pengguna di kantor Anda.'),
              PRICE_QA('Samarinda'), TIME_QA,
              ('Apa contoh proyek Altora di Samarinda?',
               'Di Universitas Mulawarman kami memasang lebih dari 50 CCTV siap analitik AI dan smartlock di Fakultas Farmasi, membuat absensi pengenalan wajah dari kamera CCTV, '
               'serta website Fakultas Ekonomi dan Bisnis dan Fakultas Farmasi. Kami juga membuat sistem antrian dan pendaftaran untuk klinik swasta di Samarinda.'),
              SUPPORT_QA, FREELANCE_QA,
              ('Apakah Altora bisa melayani instansi pemerintah di Samarinda?',
               'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP. Pemerintah Kota Samarinda termasuk klien kami.'),
              ('Selain software, apakah Altora juga memasang CCTV dan perangkat?',
               'Ya. Untuk perusahaan dan instansi di Kalimantan Timur kami menyediakan pengadaan dan pemasangan perangkat (CCTV, jaringan, server rack, GPS tracker). '
               'Pasang CCTV rumahan, smart lock, smart home, dan IT support bulanan khusus kami layani di Samarinda.')],
         nearby=[('/software-house-balikpapan', 'Software house Balikpapan'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'),
                 ('/software-house-kutai-kartanegara', 'Software house Kutai Kartanegara'), ('/software-house-bontang', 'Software house Bontang'),
                 ('/blog/cara-memilih-software-house-samarinda-balikpapan', 'Cara memilih software house'), ('/portofolio', 'Semua portofolio')]),
    dict(slug='software-house-balikpapan', city='Balikpapan', area='Balikpapan', rich=True, offices=['balikpapan-utara', 'balikpapan-pasar-baru'],
         title='Software House Balikpapan – Pembuatan Aplikasi & Website | Altora',
         desc='Software house Balikpapan dengan dua cabang (Balikpapan Utara & Pasar Baru): jasa pembuatan aplikasi, website, SEO, dan sistem lapangan.',
         h1='Software house Balikpapan untuk aplikasi, website, dan sistem lapangan',
         eyebrow='Altora Indonesia · 2 cabang di Balikpapan',
         lead='Altora Indonesia punya dua cabang di Balikpapan, di Balikpapan Utara dan Pasar Baru, dengan kantor pusat di Samarinda. Kami membuat aplikasi custom, website, SEO, dan sistem lapangan untuk perusahaan jasa migas, logistik, kontraktor, dan instansi di Balikpapan.',
         about=['Altora Indonesia adalah software house dari Kalimantan Timur yang berdiri di Samarinda pada 2019. Di Balikpapan kami punya dua cabang: '
                'Jl. Soekarno Hatta, Muara Rapak (Balikpapan Utara) dan Pasar Baru. Tim in-house kami terdiri dari 13 ahli dan sudah menyelesaikan lebih dari 50 proyek.',
                'Untuk klien di Balikpapan kami membangun aplikasi pelaporan lapangan, monitoring armada, HRIS, dan website. Institut Teknologi Kalimantan dan STT Migas Balikpapan '
                'termasuk klien kami. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.'],
         why=[('Dua cabang di Balikpapan', 'Balikpapan Utara (Jl. Soekarno Hatta, Muara Rapak) dan Pasar Baru. Diskusi kebutuhan dan pelatihan bisa dilakukan langsung di lokasi Anda.'),
              ('Terbiasa dengan operasi lapangan', 'Aplikasi dapat dirancang tetap berjalan saat sinyal lemah di site, lalu menyinkronkan data begitu terhubung.'),
              ('Dukungan setelah jalan', 'Kendala ditanggapi lewat WhatsApp dan akses jarak jauh, dan tim bisa datang ke lokasi bila diperlukan.')],
         needs=[('Jasa migas, kontraktor, dan logistik', 'Aplikasi pelaporan, approval, monitoring armada, dan dashboard yang menggantikan rekap manual di spreadsheet.'),
                ('Kampus, sekolah, dan instansi', 'Website resmi, aplikasi persuratan, dan aplikasi layanan.'),
                ('Toko, distributor, dan usaha jasa', 'Website yang ditemukan pelanggan di Google, serta aplikasi stok dan penjualan.')],
         proof=['optimasi-rute-armada', 'fleet-management-tambang', 'deteksi-apd-ai', 'hris-mobile-payroll', 'iot-monitoring-lahan-sawit', 'lentera-koperasi'],
         proof_head='Proyek di Balikpapan dan Kalimantan Timur',
         proof_note='Institut Teknologi Kalimantan (ITK) dan STT Migas Balikpapan termasuk klien kami. Proyek di bawah dikerjakan untuk operator dan perusahaan di Balikpapan dan Kalimantan Timur.',
         intents=[('/jasa-pembuatan-aplikasi-balikpapan', 'Jasa pembuatan aplikasi Balikpapan', 'Butuh aplikasi web atau Android untuk pelaporan lapangan, approval, atau stok.'),
                  ('/jasa-pembuatan-website-balikpapan', 'Jasa pembuatan website Balikpapan', 'Company profile, website instansi, dan landing page.'),
                  ('/jasa-seo-balikpapan', 'Jasa SEO Balikpapan', 'Website sudah ada, tapi belum muncul di Google.'),
                  ('/infrastruktur-hardware-kaltim', 'Infrastruktur & hardware Kaltim', 'Jaringan, CCTV AI, dan perangkat untuk site dan kantor.')],
         visit=('Tim kami melayani seluruh Balikpapan (Balikpapan Utara, Balikpapan Tengah, Balikpapan Kota, Balikpapan Selatan, Balikpapan Timur, dan Balikpapan Barat), '
                'termasuk kawasan industri dan pergudangan, serta Penajam Paser Utara dan IKN Nusantara sesuai jadwal.'),
         directions=('Cabang Balikpapan Utara berada di Jl. Soekarno Hatta, Muara Rapak; cabang kedua di Pasar Baru. Kabari kami lewat WhatsApp sebelum datang '
                     'supaya kami pastikan tim ada di cabang yang Anda tuju, atau minta tim kami yang datang ke kantor Anda.'),
         faq=[('Apakah ada software house di Balikpapan yang punya kantor sendiri?',
               'Altora Indonesia punya dua cabang di Balikpapan: Jl. Soekarno Hatta, Muara Rapak, Balikpapan Utara, dan Pasar Baru. Kantor pusat kami di Samarinda, berdiri sejak 2019.'),
              ('Bisakah saya datang ke kantor Altora di Balikpapan?',
               'Bisa. Kabari kami lewat WhatsApp +62 851-9091-1170 untuk mengatur jadwal di cabang Balikpapan Utara atau Pasar Baru. Tim kami juga bisa datang ke kantor Anda.'),
              PRICE_QA('Balikpapan'), TIME_QA,
              ('Apa contoh proyek Altora di Balikpapan dan sekitarnya?',
               'Untuk operator logistik di Balikpapan kami membuat monitoring rute armada distribusi. Di Kalimantan Timur kami juga mengerjakan fleet management armada hauling tambang, '
               'deteksi APD berbasis AI untuk PT Multi Harapan Utama, dan HRIS mobile untuk Bukit Baiduri Energi.'),
              ('Apakah aplikasinya bisa dipakai di site yang sinyalnya lemah?',
               'Bisa. Aplikasi lapangan dapat dirancang menyimpan data di HP saat sinyal lemah, lalu mengirimnya ke server begitu terhubung.'),
              SUPPORT_QA, FREELANCE_QA,
              ('Apakah Altora juga menyediakan perangkat untuk perusahaan di Balikpapan?',
               'Ya. Kami menyediakan pengadaan dan pemasangan perangkat untuk perusahaan dan instansi di Kalimantan Timur, termasuk Balikpapan: CCTV, jaringan, server rack, GPS tracker, dan videotron.')],
         nearby=[('/software-house-samarinda', 'Software house Samarinda'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'),
                 ('/software-house-penajam-paser-utara', 'Software house Penajam Paser Utara'), ('/software-house-ikn', 'Software house IKN Nusantara'),
                 ('/blog/cara-memilih-software-house-samarinda-balikpapan', 'Cara memilih software house'), ('/portofolio', 'Semua portofolio')]),
    dict(slug='software-house-kalimantan-timur', city='Kalimantan Timur', area='Kalimantan Timur', rich=True, regions=True,
         offices=['samarinda', 'balikpapan-utara', 'balikpapan-pasar-baru'],
         title='Software House Kalimantan Timur – Aplikasi & Website | Altora',
         desc='Software house Kalimantan Timur sejak 2019: kantor pusat Samarinda dan 2 cabang Balikpapan. Aplikasi, website, SEO, AI, IoT, dan pengadaan perangkat.',
         h1='Software house Kalimantan Timur: Samarinda, Balikpapan, dan seluruh Kaltim',
         eyebrow='Altora Indonesia · Kalimantan Timur',
         lead='Altora Indonesia adalah software house yang berkantor pusat di Samarinda, dengan dua cabang di Balikpapan. Sejak 2019 kami membuat aplikasi custom, website, SEO, AI, dan IoT, serta memasang perangkatnya, untuk perusahaan dan instansi di Kalimantan Timur.',
         about=['Altora Indonesia berdiri di Samarinda pada 2019. Kantor pusatnya di Jl. Dayak ASB, Bukuan, Kec. Palaran, Samarinda, dan dua cabangnya di Balikpapan Utara '
                '(Jl. Soekarno Hatta, Muara Rapak) dan Pasar Baru, Balikpapan. Dengan 13 ahli in-house, Altora sudah menyelesaikan lebih dari 50 proyek.',
                'Banyak pekerjaan di Kalimantan Timur berlangsung di lapangan: tambang, logistik sungai, perkebunan, dan layanan publik. Karena itu kami mengerjakan software dan perangkatnya '
                'sekaligus, dari aplikasi pelaporan dan dashboard sampai kamera, sensor, dan jaringan. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.'],
         why=[('Paham kebutuhan Kaltim', 'Tambang, logistik, perkebunan, dan pelayanan publik. Aplikasi dirancang untuk dipakai di kantor maupun di lokasi.'),
              ('Aplikasi yang tetap jalan di lapangan', 'Data tersimpan saat sinyal lemah, lalu tersinkron begitu terhubung.'),
              ('Tiga kantor di Kaltim', 'Kantor pusat di Samarinda dan dua cabang di Balikpapan. Tim lapangan memasang dan merawat perangkat di seluruh Kaltim.')],
         needs=[('Tambang, kontraktor, dan logistik', 'Fleet management, deteksi APD, pelaporan, dan approval untuk lokasi kerja.'),
                ('Perkebunan dan pertanian', 'Sensor cuaca dan kelembapan lahan serta pencatatan lapangan yang tetap jalan saat sinyal lemah.'),
                ('Pemerintah daerah, kampus, dan koperasi', 'Website resmi, portal data, aplikasi layanan publik, dan penilaian keuangan.')],
         proof=['fleet-management-tambang', 'deteksi-apd-ai', 'hris-mobile-payroll', 'smart-attendance-unmul', 'iot-monitoring-lahan-sawit', 'fleet-radio-kapal',
                'optimasi-rute-armada', 'lentera-koperasi', 'pompy-batara'],
         proof_head='Proyek nyata di Kalimantan Timur dan sekitarnya',
         proof_note='Klien kami antara lain Pemerintah Kota Samarinda, Universitas Mulawarman, Institut Teknologi Kalimantan, STT Migas Balikpapan, dan Diskominfosandi Kabupaten Barito Utara (Kalimantan Tengah).',
         intents=[('/software-house-samarinda', 'Software house Samarinda', 'Kantor pusat, Jl. Dayak ASB, Bukuan, Palaran.'),
                  ('/software-house-balikpapan', 'Software house Balikpapan', 'Dua cabang: Balikpapan Utara dan Pasar Baru.'),
                  ('/infrastruktur-hardware-kaltim', 'Infrastruktur & hardware Kaltim', 'Jaringan, CCTV AI, dan perangkat lapangan.'),
                  ('/pengadaan', 'Pengadaan perangkat', 'Katalog perangkat beserta pemasangannya.')],
         visit=('Dari Samarinda dan Balikpapan kami melayani Bontang, Kutai Kartanegara, Kutai Timur, Kutai Barat, Mahakam Ulu, Berau, Paser, Penajam Paser Utara, dan IKN Nusantara. '
                'Diskusi dan pelatihan dijadwalkan bersama; pengerjaan software berjalan dengan demo berkala.'),
         directions='Kantor pusat di Samarinda; cabang di Balikpapan Utara dan Pasar Baru. Kabari kami lewat WhatsApp sebelum berkunjung.',
         faq=[('Apa software house di Kalimantan Timur yang punya kantor sendiri?',
               'Altora Indonesia: kantor pusat di Jl. Dayak ASB, Bukuan, Kec. Palaran, Samarinda, dan dua cabang di Balikpapan (Balikpapan Utara dan Pasar Baru). Beroperasi sejak 2019.'),
              ('Kota mana saja yang dilayani?',
               'Samarinda dan Balikpapan dilayani langsung dari kantor kami. Bontang, Kutai Kartanegara, Kutai Timur, Kutai Barat, Mahakam Ulu, Berau, Paser, Penajam Paser Utara, dan IKN '
               'dilayani dari kantor terdekat. Untuk software, kami juga melayani klien di seluruh Indonesia secara jarak jauh.'),
              ('Apa contoh proyek Altora di Kalimantan Timur?',
               'Fleet management armada hauling tambang, deteksi APD berbasis AI untuk PT Multi Harapan Utama, HRIS mobile untuk Bukit Baiduri Energi, absensi pengenalan wajah untuk '
               'Universitas Mulawarman, sensor lahan sawit, serta GPS armada dan radio VHF untuk logistik di Sungai Mahakam.'),
              ('Apakah aplikasinya bisa dipakai di lokasi yang sinyalnya lemah?',
               'Bisa. Aplikasi dapat dirancang menyimpan data sementara di perangkat lalu mengirimnya saat sinyal tersedia.'),
              PRICE_QA('Kalimantan Timur'), SUPPORT_QA,
              ('Apakah Altora bisa untuk instansi pemerintah daerah?',
               'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara serah terima.'),
              ('Apakah Altora juga menyediakan dan memasang perangkat?',
               'Ya. Pengadaan dan pemasangan CCTV, jaringan, server rack, GPS tracker, sensor IoT, dan videotron untuk perusahaan dan instansi di seluruh Kalimantan Timur.')],
         nearby=[('/area-layanan', 'Semua area layanan'), ('/portofolio', 'Semua portofolio'), ('/services', 'Layanan kami'), ('/about', 'Tentang Altora')]),
]


def stats_html():
    return '<div class="lc-facts">' + ''.join(f'<div><b>{e(v)}</b><span>{e(k)}</span></div>' for v, k in STATS) + '</div>'


def proof_html(c):
    cards = ''.join(pf_card(PF[s]) for s in c['proof'] if s in PF)
    return (f'<section class="svd-sec" id="proyek"><div class="ct-wrap"><div class="pd-block-head"><h2>{e(c["proof_head"])}</h2>'
            f'<p>{e(c["proof_note"])}</p></div><div class="pf-grid">{cards}</div>'
            '<p class="lc-more"><a href="/portofolio">Lihat semua portofolio →</a></p></div></section>')


def services_full_html(c):
    items = [x for x in SERVICES_FULL if not x[3] or c['city'] == 'Samarinda']
    svcs = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for u, t, d, _ in items)
    note = ('' if c['city'] == 'Samarinda' else
            '<p class="lc-note">Pasang CCTV rumahan, smart lock, smart home, dan IT support bulanan khusus kami layani di Samarinda.</p>')
    return (f'<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Layanan software house kami di {e(c["city"])}</h2>'
            '<p>Bisa diambil satu per satu atau digabung dalam satu proyek.</p></div>'
            f'<div class="lc-svcs">{svcs}</div>{note}</div></section>')


def intents_html(c):
    head = 'Kantor dan layanan Altora di Kalimantan Timur' if c.get('regions') else f'Cari layanan yang lebih spesifik di {c["city"]}?'
    items = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for u, t, d in c['intents'])
    return f'<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>{e(head)}</h2></div><div class="lc-svcs">{items}</div></div></section>'


def regions_html():
    from regions import REGIONS
    links = ''.join(f'<a href="/software-house-{k}">{e(r["name"])}</a>' for k, r in REGIONS.items())
    return f'<div class="svd-related"><b>Kabupaten &amp; kota lain di Kaltim</b>{links}</div>'


def full_addr(o):
    a = one_line(o)
    if o['city'] not in a:
        a += ', ' + o['city']
    return a + ', ' + o['region'] + (' ' + o['postal'] if o['postal'] else '')


def office_html(c):
    offs = [OFFICE[k] for k in c['offices']]
    cards = ''.join(f'<div class="lc-nap-card"><small>{"Kantor pusat" if o["hq"] else "Cabang"}</small><b>{e(o["label"])}</b>'
                    f'<span>{e(full_addr(o))}</span>'
                    f'<a href="{e(maps_link(o))}" rel="noopener" target="_blank">Buka di Google Maps →</a></div>' for o in offs)
    the_map = map_html() if offs[0]['hq'] else map_html(offs[0])
    where = 'di Kalimantan Timur' if c.get('regions') else 'di ' + e(c['city'])
    return (f'<section class="svd-sec" id="kantor"><div class="ct-wrap lc-nap"><div><div class="pd-block-head"><h2>Kantor Altora {where}</h2></div>'
            f'<div class="lc-nap-cards">{cards}</div>'
            f'<p class="lc-nap-contact"><a href="tel:+6285190911170">{PHONE_DISPLAY}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · WhatsApp dibalas di jam kerja</p>'
            f'<h3>Cara ke kantor</h3><p>{e(c["directions"])}</p><h3>Area kunjungan</h3><p>{e(c["visit"])}</p>'
            f'<h3>Tim</h3><p>{FACTS["team"]} ahli in-house menangani analisis, desain, pengembangan, pelatihan, dan dukungan dalam satu tim. '
            'Tim lapangan kami survei, memasang, dan merawat perangkat di seluruh Kalimantan Timur.</p></div>'
            f'<div class="lc-nap-map">{the_map}</div></div></section>')


def rich_body(c, msg):
    why = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in c['why'])
    needs = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in c['needs'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c['faq'])
    nearby = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in c['nearby'])
    about = ''.join(f'<p>{e(p)}</p>' for p in c['about'])
    return f'''<main class="ct-page svd-page lc-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/beranda">Beranda</a><span>/</span><a href="/area-layanan">Area layanan</a><span>/</span><span>{e(c["city"])}</span></nav>
<p class="eyebrow eyebrow-purple">{e(c["eyebrow"])}</p><h1>{e(c["h1"])}</h1><p class="ct-lead">{e(c["lead"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#proyek">Lihat proyek</a><a class="svd-link" href="#kantor">Alamat kantor</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(HERO_ALT)}" fetchpriority="high" src="{HERO}" style="object-position:50% 45%"/><span class="svd-chip svd-chip-0">Sejak {FACTS["since"]}</span><span class="svd-chip svd-chip-1">{e(c["city"])}</span><span class="svd-chip svd-chip-2">Konsultasi gratis</span></figure>
</div></section>
<section class="svd-sec lc-about-sec"><div class="ct-wrap lc-about"><div><h2>Tentang Altora di {e(c["city"])}</h2>{about}</div>{stats_html()}</div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Kenapa memilih Altora di {e(c["city"])}</h2></div><div class="svd-dos lc-why">{why}</div></div></section>
{services_full_html(c)}
{proof_html(c)}
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Kebutuhan yang sering kami kerjakan di {e(c["city"])}</h2></div><ul class="lc-needs">{needs}</ul></div></section>
{intents_html(c)}
{office_html(c)}
{guides_html()}
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan seputar software house {e(c["city"])}</h2></div><div>{faq}</div></div></section>
<section class="svd-sec" id="lihat-juga"><div class="ct-wrap">{regions_html() if c.get("regions") else ""}
<div class="svd-related"><b>Lihat juga</b>{nearby}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh software house di {e(c["city"])}?</h2><p>Ceritakan kebutuhan Anda. Diskusi awal gratis, tanpa kewajiban lanjut.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''


def plain_body(c, msg):
    why = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in c['why'])
    needs = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in c['needs'])
    svc_list = SERVICES[:2] if c.get('remote') else SERVICES
    svcs = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for u, t, d in svc_list)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c['faq'])
    nearby = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in c['nearby'])
    offices = ''.join(f'<p><b>{e(o["label"])}</b><br/><a href="{e(maps_link(o))}" rel="noopener" target="_blank">{e(one_line(o))}</a></p>' for o in OFFICES)
    proof = proof_html(c) if c.get('proof') else ''
    return f'''<main class="ct-page svd-page lc-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/beranda">Beranda</a><span>/</span><span>{e(c["h1"])}</span></nav>
<p class="eyebrow eyebrow-purple">Altora Indonesia · {e(c["city"])}</p><h1>{e(c["h1"])}</h1><p class="ct-lead">{e(c["lead"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#lihat-juga">Lihat juga</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(HERO_ALT)}" src="{HERO}" style="object-position:50% 45%"/><span class="svd-chip svd-chip-0">{e(c["city"])}</span><span class="svd-chip svd-chip-1">{"Dikerjakan jarak jauh" if c.get("remote") else "Tim lokal"}</span><span class="svd-chip svd-chip-2">Konsultasi gratis</span></figure>
</div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Kenapa memilih Altora di {e(c["city"])}</h2></div><div class="svd-dos lc-why">{why}</div></div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>{"Kebutuhan yang umum di " if c.get("remote") else "Kebutuhan yang sering kami kerjakan di "}{e(c["city"])}</h2></div><ul class="lc-needs">{needs}</ul></div></section>
{proof}
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Layanan software house kami</h2></div><div class="lc-svcs">{svcs}</div></div></section>
<section class="svd-sec" id="lihat-juga"><div class="ct-wrap">
<div class="svd-related"><b>Lihat juga</b>{nearby}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Kantor</h2>{offices}<p><a href="tel:+6285190911170">+62 851-9091-1170</a> · <a href="mailto:hello@altora.id">hello@altora.id</a></p></div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh software house di {e(c["city"])}?</h2><p>Ceritakan kebutuhan Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''


def page(c):
    url = '/' + c['slug']
    if len(c['desc']) > 160:
        c['desc'] = c['desc'][:157].rsplit(' ', 1)[0].rstrip(',.:;') + '.'
    msg = f'Halo Altora, saya dari {c["city"]} dan ingin konsultasi kebutuhan software.'
    robots = 'index,follow,max-image-preview:large' if c.get('indexed', True) else 'noindex,follow'
    # Satu entitas Altora (org) yang menyediakan layanan untuk kota ini; simpul kantor hanya untuk kota yang punya kantor.
    if c.get('rich'):
        local_offices = [OFFICE[k] for k in c['offices']]
    else:
        local_offices = [o for o in OFFICES if not c.get('remote') and o['city'] == c['city']]
    svc_items = ([(u, t) for u, t, _, h in SERVICES_FULL if not h or c['city'] == 'Samarinda'] if c.get('rich')
                 else [(u, t) for u, t, _ in (SERVICES[:2] if c.get('remote') else SERVICES)])
    crumbs = ([('Beranda', '/'), ('Area layanan', '/area-layanan'), (c['city'], url)] if c.get('rich') else [('Beranda', '/'), (c['h1'], url)])
    ld = {'@context': 'https://schema.org', '@graph': [org()] + [office_node(o) for o in local_offices] + [
        {'@type': 'WebPage', '@id': SITE + url + '#halaman', 'url': SITE + url, 'name': c['title'], 'description': c['desc'], 'inLanguage': 'id-ID',
         'isPartOf': {'@id': SITE + '/#website'}, 'publisher': {'@id': ORG_ID}, 'about': {'@id': SITE + url + '#layanan'},
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': SITE + HERO}},
        {'@type': 'Service', '@id': SITE + url + '#layanan', 'name': c['h1'], 'serviceType': 'Software house',
         'description': c['desc'], 'url': SITE + url,
         'provider': {'@id': office_id(local_offices[0]) if local_offices else ORG_ID},
         'areaServed': {'@type': 'City' if c['area'] != 'Kalimantan Timur' else 'AdministrativeArea', 'name': c['area']},
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Layanan software house',
                             'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': t, 'url': SITE + u}} for u, t in svc_items]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(crumbs)]},
        {'@type': 'FAQPage', '@id': SITE + url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]}]}
    body = rich_body(c, msg) if c.get('rich') else plain_body(c, msg)
    extra_css = (f'<link rel="stylesheet" href="{PF_CSS}"/>' if c.get('proof') else '') + f'<link rel="stylesheet" href="{LOCAL_CSS}"/>'
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(c["title"])}</title><meta content="{e(c["desc"])}" name="description"/><link href="{SITE}{url}" rel="canonical"/><meta content="{robots}" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(c["title"])}" property="og:title"/><meta content="{e(c["desc"])}" property="og:description"/><meta content="{SITE}{url}" property="og:url"/><meta content="{SITE}{HERO}" property="og:image"/><meta content="{e(HERO_ALT)}" property="og:image:alt"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/>{extra_css}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
{body}
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


# Proyek Kaltim yang relevan per sektor daerah (ditampilkan sebagai "proyek kami di Kaltim", bukan klaim proyek di daerah itu).
REGION_PROOF = {
    'bontang': ['deteksi-apd-ai', 'iot-monitoring-gudang', 'fleet-management-tambang'],
    'kutai-kartanegara': ['deteksi-apd-ai', 'hris-mobile-payroll', 'fleet-management-tambang'],
    'kutai-timur': ['fleet-management-tambang', 'deteksi-apd-ai', 'iot-monitoring-lahan-sawit'],
    'kutai-barat': ['iot-monitoring-lahan-sawit', 'fleet-management-tambang', 'kios-mandiri-kelurahan'],
    'mahakam-ulu': ['fleet-radio-kapal', 'kios-mandiri-kelurahan', 'iot-monitoring-lahan-sawit'],
    'berau': ['fleet-management-tambang', 'fleet-radio-kapal', 'deteksi-apd-ai'],
    'paser': ['iot-monitoring-lahan-sawit', 'fleet-management-tambang', 'hris-mobile-payroll'],
    'penajam-paser-utara': ['optimasi-rute-armada', 'deteksi-apd-ai', 'iot-monitoring-gudang'],
    'ikn': ['deteksi-apd-ai', 'kios-mandiri-kelurahan', 'optimasi-rute-armada'],
}


def region_entry(k, r):
    """Halaman 'Software house <daerah>' untuk daerah Kaltim yang dilayani dari kantor terdekat."""
    from build_area import CITIES as AREA_CITIES
    o = next(x for x in OFFICES if x['key'] == r['office'])
    near = [n for n in r['near'] if n in AREA_CITIES][:3]
    return dict(slug=f'software-house-{k}', city=r['name'], area=r['name'], office=r['office'],
        title=f'Software House {r["name"]} | Altora Indonesia',
        desc=f'Software house untuk {r["name"]}: aplikasi custom, website, dan SEO. Dilayani tim Altora dari {o["city"]}, Kalimantan Timur, sejak 2019.',
        h1=f'Software house {r["name"]}',
        lead=f'Altora Indonesia melayani {r["name"]} dari {label_lc(o)}. Kami membuat aplikasi custom, website, dan SEO untuk {r["sectors"]}.',
        why=[(f'Dilayani dari {o["city"]}', f'Pengerjaan berjalan lewat video call dan demo berkala; tim kami juga bisa datang dari {label_lc(o)} untuk diskusi dan pelatihan di {r["name"]}.'),
             ('Satu tim dari awal sampai akhir', 'Analisis, desain, pengembangan, pelatihan, dan dukungan ditangani tim yang sama, jadi tidak ada saling lempar tanggung jawab.'),
             ('Bisa untuk lokasi jauh', 'Aplikasi dapat dirancang tetap berjalan saat sinyal lemah, lalu menyinkronkan data begitu terhubung.')],
        needs=r['needs'], proof=REGION_PROOF.get(k, []), proof_head='Proyek kami di Kalimantan Timur',
        proof_note=f'Dikerjakan oleh tim yang sama yang melayani {r["name"]}. Detail lengkap ada di halaman portofolio.',
        faq=[(f'Apakah Altora melayani {r["name"]}?', f'Ya. {r["name"]} kami layani dari {label_lc(o)} ({with_city(o)}). Jadwal diskusi dan pelatihan kami sepakati bersama.'),
             (f'Layanan apa saja yang tersedia di {r["name"]}?', 'Pembuatan aplikasi custom, website, dan SEO, serta pengadaan dan pemasangan perangkat untuk perusahaan dan instansi.'),
             ('Bagaimana dukungan setelah sistem berjalan?', 'Kendala dicek jarak jauh lebih dulu. Bila perlu, teknisi dijadwalkan datang ke lokasi.'),
             ('Apakah bisa untuk instansi?', 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.')],
        nearby=[(f'/software-house-{n}', f'Software house {AREA_CITIES[n]["name"]}') for n in near] + [(f'/jasa-pembuatan-aplikasi-{k}', f'Jasa pembuatan aplikasi {r["name"]}'), (f'/jasa-pembuatan-website-{k}', f'Jasa pembuatan website {r["name"]}'), (f'/jasa-seo-{k}', f'Jasa SEO {r["name"]}'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur')])


def nasional_entry(k, r):
    """'Software house <kota>' di luar Kaltim: hanya layanan jarak jauh, tanpa janji teknisi datang."""
    from build_area import CITIES as AREA_CITIES
    from regions_nasional import is_indexed
    near = [n for n in r['near'] if n in AREA_CITIES][:3]
    return dict(slug=f'software-house-{k}', city=r['name'], area=r['name'], office='samarinda', remote=True, indexed=is_indexed(k),
        proof=r.get('proof', []), proof_head=f'Proyek kami untuk {r["name"]}', proof_note=f'Dikerjakan dari kantor pusat kami di Samarinda untuk klien di {r["name"]}.',
        title=f'Software House {r["name"]} | Aplikasi & Website | Altora',
        desc=f'Software house untuk klien di {r["name"]}: aplikasi web dan HP, website, dan dashboard, dikerjakan jarak jauh oleh tim Altora Indonesia.',
        h1=f'Software house untuk {r["name"]}',
        lead=f'Altora Indonesia adalah software house dari Samarinda, Kalimantan Timur. Untuk perusahaan dan instansi di {r["name"]} ({r["seat"]}), kami membuat aplikasi web dan HP, website, dan dashboard, dikerjakan jarak jauh dengan demo rutin sampai serah terima.',
        why=[('Proses jarak jauh yang jelas', 'Kebutuhan dibahas lewat video call, progres ditunjukkan di server uji setiap tahap, dan semua keputusan tercatat. Anda tidak perlu menunggu kunjungan untuk melihat hasil.'),
             ('Pendampingan sampai dipakai', 'Pelatihan pengguna dan dukungan setelah aplikasi berjalan, dijadwalkan menyesuaikan zona waktu Anda.'),
             ('Bisa untuk instansi', 'Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara yang lengkap.')],
        needs=r['needs'],
        faq=[(f'Apakah Altora punya kantor di {r["name"]}?', f'Tidak. Kantor kami di Samarinda dan Balikpapan, Kalimantan Timur. Proyek aplikasi dan website untuk klien di {r["name"]} kami kerjakan jarak jauh, dan pertemuan langsung bisa dijadwalkan bila diperlukan.'),
             (f'Layanan apa yang tersedia untuk {r["name"]}?', 'Pembuatan aplikasi web dan HP, website, SEO, dashboard, dan integrasi sistem, semuanya dikerjakan jarak jauh.'),
             ('Bagaimana memantau progres kalau tidak bertemu langsung?', 'Ada jadwal demo rutin di server uji, catatan rapat, dan satu kontak yang bertanggung jawab atas proyek Anda.'),
             ('Bagaimana dukungan setelah aplikasi jalan?', 'Pelatihan pengguna dilakukan online, lalu kendala ditangani lewat WhatsApp, tiket support, dan akses jarak jauh sesuai kesepakatan.')],
        nearby=[(f'/software-house-{n}', f'Software house {AREA_CITIES[n]["name"]}') for n in near] + [(f'/jasa-pembuatan-aplikasi-{k}', f'Jasa pembuatan aplikasi {r["name"]}'), (f'/jasa-pembuatan-website-{k}', f'Jasa pembuatan website {r["name"]}'), ('/area-layanan#nasional', 'Kota lain di Indonesia')])


from regions import REGIONS
from regions_nasional import NASIONAL
CITIES += [region_entry(k, r) for k, r in REGIONS.items()]
CITIES += [nasional_entry(k, r) for k, r in NASIONAL.items()]


if __name__ == '__main__':
    for c in CITIES:
        (root / f'{c["slug"]}.html').write_text(page(c), encoding='utf-8')
    from build_area import update_sitemap
    update_sitemap(['/' + c['slug'] for c in CITIES if c.get('indexed', True)],
                   drop=['/' + c['slug'] for c in CITIES if not c.get('indexed', True)], lastmod=TODAY)
    print('halaman lokal:', len(CITIES), '| noindex:', sum(1 for c in CITIES if not c.get('indexed', True)))
