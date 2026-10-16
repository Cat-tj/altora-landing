"""Bangun 5 halaman detail layanan (services/<slug>.html) dari data SERVICES.
Jalankan dari root repo:  python3 scripts/build_services.py && python3 scripts/apply_shell.py"""
import html, json, pathlib
from urllib.parse import quote

root = pathlib.Path(__file__).resolve().parent.parent
CSS_VER = '20261016i'
WA = 'https://wa.me/6285190911170?text='
e = lambda t: html.escape(t, quote=True)

ICONS = {
    'flow': '<path d="M4 6h6v4H4zM14 14h6v4h-6zM7 10v4a2 2 0 0 0 2 2h5"/>',
    'phone': '<rect height="18" rx="2.5" width="11" x="6.5" y="3"/><path d="M11 17.5h2"/>',
    'plug': '<path d="M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0zM12 16v5"/>',
    'chart': '<path d="M4 20h16M7 16v-4M12 16V8M17 16v-7"/>',
    'shield': '<path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.2 3-5 6-5s5.4 1.8 6 5"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14.2c2.3.2 3.9 1.7 4.5 4.3"/>',
    'search': '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
    'layout': '<rect height="16" rx="2" width="18" x="3" y="4"/><path d="M3 9h18M9 9v11"/>',
    'pen': '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13 7 4 4"/>',
    'speed': '<path d="M12 14 16 9"/><path d="M4 18a9 9 0 1 1 16 0"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'camera': '<path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/>',
    'helmet': '<path d="M4 16a8 8 0 0 1 16 0zM2 16h20v2H2zM12 8V5"/>',
    'face': '<path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><circle cx="12" cy="10.5" r="2.6"/><path d="M8 17c.8-1.9 2.2-2.8 4-2.8s3.2.9 4 2.8"/>',
    'zone': '<path d="M4 4h16v16H4z" stroke-dasharray="3 3"/><path d="M9 9h6v6H9z"/>',
    'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    'sensor': '<circle cx="12" cy="12" r="2.2"/><path d="M8.2 8.2a5.4 5.4 0 0 0 0 7.6M15.8 8.2a5.4 5.4 0 0 1 0 7.6M5.4 5.4a9.3 9.3 0 0 0 0 13.2M18.6 5.4a9.3 9.3 0 0 1 0 13.2"/>',
    'monitor': '<rect height="12" rx="2" width="18" x="3" y="4"/><path d="M9 20h6M12 16v4"/>',
    'key': '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2.5 2.5M14.5 8.5 17 11"/>',
    'truck': '<path d="M2.5 6.5h11v9h-11zM13.5 9.5h4l3 3.2v2.8h-7z"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'route': '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
    'sat': '<path d="M5 19 19 5"/><path d="M7 13a4 4 0 0 0 4 4M4 13a7 7 0 0 0 7 7"/><rect height="6" rx="1" transform="rotate(45 16 8)" width="8" x="12" y="5"/>',
    'bolt': '<path d="M13 3 5 14h6l-1 7 8-11h-6z"/>',
    'brain': '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V6a2 2 0 0 0-3-2ZM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
    'map': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    'cart_like': '<path d="M3 4h2.2l2.2 10.5h10.2L20 7.5H6.4"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
    'fuel': '<path d="M5 20V5a1 1 0 0 1 1-1h7a1 1 0 0 1 1 1v15M4 20h11M14 9h2a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V8l-3-3"/>',
    'tool': '<path d="M14 7a4 4 0 0 0-5 5l-5 5 3 3 5-5a4 4 0 0 0 5-5l-2.5 2.5-2-2z"/>',
}


def icon(n):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[n]}</svg>'


PF = {  # slug portofolio -> (judul, gambar)
    'portal-one-map': ('Portal One Map Barito Utara', '/assets/img/portfolio/barito-dash.jpg'),
    'media-monitoring-dashboard': ('Media Monitoring Dashboard', '/assets/img/portfolio/imm.jpg'),
    'dashboard-geospasial-dapodik': ('Dashboard Geospasial DAPODIK', '/assets/img/portfolio/dapodik.jpg'),
    'custom-kios-k-pengadaan-hardware': ('Kios-K & Pengadaan Hardware Kelurahan', '/assets/img/portfolio/kiosk-samarinda/kiosk-pampang.jpg'),
    'unmul-infrastruktur-cctv-jaringan': ('Infrastruktur CCTV & Jaringan UNMUL', '/assets/img/portfolio/unmul-infrastructure/cable-cctv-installation.png'),
    'altora-teams': ('Altora Teams', '/assets/img/portfolio/altora-teams-kpi-analytics.jpg'),
    'hris-mobile-payroll': ('HRIS Mobile & Payroll', '/assets/img/portfolio/hris.jpg'),
    'sistem-antrian-poliklinik': ('Sistem Antrian Poliklinik', '/assets/img/portfolio/clinic.jpg'),
    'unmul-website-redesign': ('Redesign Website Universitas Mulawarman', '/assets/img/portfolio/unmul-infrastructure/website-redesign-demonstration.png'),
    'website-cms-institusi': ('Website & CMS Institusi', '/assets/img/portfolio/feb-unmul.jpg'),
    'website-resmi-institusi': ('Website Resmi Institusi', '/assets/img/portfolio/farmasi.jpg'),
    'ai-safety-vision': ('Deteksi Atribut Keselamatan', '/assets/img/portfolio/safety.jpg'),
    'smart-attendance': ('Smart Attendance', '/assets/img/portfolio/attendance.jpg'),
    'instalasi-cctv-ai-analytics': ('Instalasi CCTV AI Analytics', '/assets/img/portfolio/cctv-farmasi.jpg'),
    'iot-monitoring-lahan': ('Altora Smart Farming', '/assets/img/portfolio/smart-farming.webp'),
    'smartlock-akses-digital': ('Smartlock & Akses Digital', '/assets/img/portfolio/smartlock.jpg'),
    'pompy-batara': ('POMPY BATARA', '/assets/img/portfolio/pompy-batara-platform-cropped.jpg'),
    'fleet-management': ('Fleet Management System', '/assets/img/portfolio/fms.jpg'),
    'optimasi-rute-armada': ('Optimasi Rute & Armada', '/assets/img/portfolio/logistik.jpg'),
}

SERVICES = [
    dict(slug='software-custom', name='Software Custom', kicker='Aplikasi & sistem internal',
         h1='Aplikasi yang mengikuti cara kerja tim Anda.',
         lead='Web app, aplikasi mobile, dan sistem internal untuk proses yang tidak cocok dengan software jadi, seperti approval, absensi, dan laporan yang masih dikumpulkan manual.',
         hero='/assets/img/produk/teams.webp', hero_pos='60% 55%', chips=['Approval berjenjang', 'Laporan otomatis', 'Akses per peran'],
         pains=[('Data tersebar di banyak file', 'Spreadsheet, chat, dan kertas membuat satu angka bisa punya beberapa versi.'),
                ('Approval tertahan', 'Pengajuan menunggu tanda tangan karena orangnya sedang di lapangan atau di kota lain.'),
                ('Laporan makan waktu', 'Tim menghabiskan waktu merekap, bukan menindaklanjuti.')],
        dos=[('flow', 'Workflow & approval', 'Alur pengajuan, persetujuan, dan tindak lanjut dalam satu sistem.'),
              ('phone', 'Aplikasi web & mobile', 'Dipakai dari kantor maupun lapangan, termasuk saat sinyal lemah.'),
              ('users', 'Peran & hak akses', 'Setiap orang hanya melihat dan mengubah yang menjadi tugasnya.'),
              ('chart', 'Dashboard & laporan', 'Ringkasan yang siap dibaca pimpinan tanpa rekap manual.'),
              ('plug', 'Integrasi sistem', 'Terhubung dengan aplikasi akuntansi, perangkat, atau API yang sudah ada.'),
              ('shield', 'Keamanan & log aktivitas', 'Jejak perubahan tercatat dan data tersimpan dengan aman.')],
         steps=['Pemetaan alur kerja', 'Rancangan layar & data', 'Pengembangan bertahap', 'Uji coba bersama pengguna', 'Peluncuran & pendampingan'],
         proof=['altora-teams', 'hris-mobile-payroll', 'sistem-antrian-poliklinik'],
         related=[('/produk/teams', 'Altora Teams (HRIS)'), ('/produk/pos', 'Altora POS'), ('/blog/merencanakan-pembuatan-aplikasi', 'Artikel: merencanakan pembuatan aplikasi')],
         faq=[('Apakah harus dibuat dari nol?', 'Tidak selalu. Bila kebutuhan Anda mirip dengan produk Altora seperti Teams atau POS, produk itu bisa dipakai lalu disesuaikan di bagian yang benar-benar unik.'),
              ('Bisa dipakai di HP?', 'Bisa. Sistem dapat dibuat sebagai aplikasi web yang nyaman di HP, aplikasi mobile, atau keduanya sesuai kebutuhan lapangan.'),
              ('Siapa pemilik data dan aksesnya?', 'Kepemilikan data, akses server, dan source code dibahas dan dicantumkan dengan jelas sejak awal kerja sama.')]),
    dict(slug='website-seo', name='Website & SEO', kicker='Website institusi & bisnis',
         h1='Website yang menjelaskan, ditemukan, dan menghasilkan kontak.',
         lead='Company profile, landing page, dan website institusi dengan struktur konten yang jelas, cepat dibuka di HP, dan disusun agar mudah ditemukan di Google.',
         hero='/assets/img/portfolio/feb-unmul.jpg', hero_pos='50% 30%', chips=['Cepat di HP', 'Struktur SEO', 'CMS mudah diisi'],
         pains=[('Website ada, tapi tidak ditemukan', 'Calon klien mencari layanan Anda di Google, tetapi yang muncul justru pesaing.'),
                ('Isi sulit diperbarui', 'Setiap perubahan kecil harus menunggu developer.'),
                ('Pengunjung datang lalu pergi', 'Informasi penting tersembunyi dan tidak ada ajakan yang jelas untuk menghubungi.')],
         dos=[('layout', 'Struktur & desain halaman', 'Susunan halaman yang menjawab pertanyaan calon klien secara berurutan.'),
              ('search', 'SEO on-page & lokal', 'Judul, deskripsi, data terstruktur, sitemap, dan halaman lokal per kota.'),
              ('pen', 'CMS & konten', 'Tim Anda dapat memperbarui berita, layanan, dan galeri sendiri.'),
              ('speed', 'Performa & mobile', 'Gambar dioptimalkan dan tampilan disesuaikan untuk layar HP.'),
              ('chart', 'Analitik & konversi', 'Mengukur dari mana pengunjung datang dan tombol apa yang mereka klik.'),
              ('shield', 'Domain, SSL & keamanan', 'Website aman diakses dan dirawat secara berkala.')],
         steps=['Audit website & kata kunci', 'Struktur halaman & konten', 'Desain & pengembangan', 'Optimasi SEO & kecepatan', 'Peluncuran & pemantauan'],
         proof=['unmul-website-redesign', 'website-cms-institusi', 'website-resmi-institusi'],
         related=[('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website Samarinda'), ('/jasa-pembuatan-website-indonesia', 'Jasa pembuatan website Indonesia'), ('/blog', 'Artikel & panduan')],
         faq=[('Apakah website lama bisa diperbaiki?', 'Bisa. Kami mulai dari audit website yang ada, lalu memutuskan apakah cukup diperbaiki atau perlu dibangun ulang.'),
              ('Bisakah kami mengisi konten sendiri?', 'Bisa. Website dapat dilengkapi CMS sehingga tim Anda dapat memperbarui berita, layanan, dan galeri.'),
              ('Kapan hasil SEO terlihat?', 'SEO bergantung pada persaingan kata kunci dan konsistensi konten, sehingga hasilnya bertahap. Kami memantau dan melaporkan perkembangannya.')]),
    dict(slug='ai-cctv', name='AI CCTV & Safety', kicker='AI vision dari CCTV',
         h1='CCTV yang tidak hanya merekam, tapi ikut memperhatikan.',
         lead='Analitik AI dari kamera yang sudah ada untuk kepatuhan APD, absensi wajah, pengawasan zona terlarang, dan penghitungan orang atau kendaraan, lengkap dengan notifikasi.',
         hero='/assets/img/produk/vision.webp', hero_pos='60% 60%', chips=['Deteksi APD', 'Absensi wajah', 'Alert zona'],
         pains=[('Rekaman baru dibuka setelah kejadian', 'CCTV hanya berguna untuk investigasi, bukan pencegahan.'),
                ('Pengawasan manual melelahkan', 'Operator tidak mungkin memantau puluhan layar sepanjang hari.'),
                ('Kepatuhan sulit dibuktikan', 'Laporan K3 dan kehadiran masih mengandalkan catatan manual.')],
         dos=[('helmet', 'Deteksi APD', 'Helm, rompi, dan atribut keselamatan lain di area kerja.'),
              ('face', 'Absensi wajah', 'Check-in otomatis dari kamera di pintu masuk, terhubung ke HRIS.'),
              ('zone', 'Zona terlarang', 'Alert saat ada orang atau kendaraan memasuki area berbahaya.'),
              ('users', 'Penghitungan orang & kendaraan', 'Data lalu lintas area untuk keputusan operasional.'),
              ('bell', 'Alert & dashboard', 'Notifikasi real-time dan rekap kejadian per periode.'),
              ('camera', 'Infrastruktur kamera', 'Survei, penambahan kamera, NVR, dan jaringan bila diperlukan.')],
         steps=['Survei kamera & area', 'Uji coba di titik terpilih', 'Kalibrasi aturan & alert', 'Integrasi dashboard', 'Pelatihan & evaluasi'],
         proof=['ai-safety-vision', 'smart-attendance', 'instalasi-cctv-ai-analytics'],
         related=[('/produk/vision', 'Altora Vision'), ('/produk/attendance', 'Altora Smart Attendance'), ('/blog/absensi-face-recognition-cctv', 'Artikel: absensi wajah dari CCTV')],
         faq=[('Apakah CCTV lama bisa dipakai?', 'Sering kali bisa. Kami mengecek posisi, sudut, dan kualitas kamera; bila perlu, cukup menambah kamera di titik tertentu.'),
              ('Bagaimana dengan data wajah karyawan?', 'Data wajah termasuk data pribadi. Kami membantu menyiapkan persetujuan, pembatasan akses, dan kebijakan penyimpanan sesuai UU PDP.'),
              ('Apakah harus selalu online?', 'Pemrosesan bisa di server lokal atau cloud, tergantung kondisi jaringan di lokasi.')]),
    dict(slug='iot-command-center', name='IoT & Command Center', kicker='Sensor, perangkat & pusat kendali',
         h1='Kondisi lapangan terlihat dari satu layar.',
         lead='Sensor, smartlock, kios, dan perangkat lapangan yang terhubung ke dashboard, jadi tim tahu kondisi lokasi tanpa harus datang.',
         hero='/assets/img/produk/command.webp', hero_pos='55% 60%', chips=['Sensor real-time', 'Smart access', 'Alert otomatis'],
         pains=[('Masalah baru diketahui terlambat', 'Suhu, asap, atau gangguan perangkat baru ketahuan setelah kerugian terjadi.'),
                ('Lokasi tersebar & jauh', 'Petugas harus datang hanya untuk mengecek kondisi.'),
                ('Data perangkat tidak menyatu', 'CCTV, sensor, dan akses pintu punya aplikasi masing-masing.')],
         dos=[('sensor', 'Sensor lingkungan & keselamatan', 'Suhu, kelembapan, asap, api, dan kondisi lahan.'),
              ('key', 'Smart access', 'Smartlock, RFID/QR, dan gate dengan log akses.'),
              ('monitor', 'Command center', 'Satu tampilan untuk CCTV, armada, sensor, dan status perangkat.'),
              ('bell', 'Alert & eskalasi', 'Notifikasi ke orang yang tepat saat ambang batas terlewati.'),
              ('plug', 'Gateway & konektivitas', 'LoRa, 4G, atau jaringan lokal sesuai kondisi lokasi.'),
              ('tool', 'Instalasi & perawatan', 'Pemasangan perangkat dan pemeliharaan berkala.')],
         steps=['Survei lokasi & perangkat', 'Desain sensor & jaringan', 'Instalasi & integrasi', 'Kalibrasi ambang alert', 'Monitoring & perawatan'],
         proof=['iot-monitoring-lahan', 'smartlock-akses-digital', 'pompy-batara'],
         related=[('/produk/sense', 'Altora Sense'), ('/produk/command', 'Altora Command'), ('/produk/pass', 'Altora Pass')],
         faq=[('Bagaimana jika lokasi tidak ada internet?', 'Perangkat dapat memakai LoRa, 4G, atau jaringan lokal; data dikirim saat koneksi tersedia sesuai desain sistem.'),
              ('Bisa memakai perangkat yang sudah ada?', 'Bisa, selama perangkat menyediakan akses data. Kami mengecek kompatibilitasnya saat survei.'),
              ('Siapa yang merawat perangkat?', 'Altora dapat menangani pemeliharaan berkala melalui layanan pengadaan, instalasi & maintenance.')]),
    dict(slug='fleet-management-service', name='Fleet Management', kicker='Monitoring armada',
         h1='Tahu posisi, kondisi, dan perilaku armada setiap saat.',
         lead='GPS tracker, kamera kendaraan, dan dashboard armada untuk logistik, tambang, dan konstruksi. Mulai dari pelacakan sampai laporan BBM dan perilaku pengemudi.',
         hero='/assets/img/produk/fms.webp', hero_pos='55% 60%', chips=['Live tracking', 'Geofence', 'Laporan BBM'],
         pains=[('Posisi armada tidak pasti', 'Dispatcher harus menelepon pengemudi satu per satu.'),
                ('BBM & jam kerja sulit dikontrol', 'Penyimpangan rute dan pemakaian BBM baru ketahuan di akhir bulan.'),
                ('Insiden tanpa bukti', 'Saat terjadi kecelakaan atau keluhan, tidak ada data yang bisa diperiksa.')],
         dos=[('pin', 'Live tracking', 'Posisi, kecepatan, dan status kendaraan secara real-time.'),
              ('route', 'Rute & geofence', 'Riwayat perjalanan dan alert saat keluar area atau rute.'),
              ('fuel', 'BBM & data mesin', 'Level BBM, odometer, dan data CAN dari kendaraan yang didukung.'),
              ('camera', 'Kamera & keselamatan', 'Dashcam, DualCam, dan deteksi kantuk pengemudi.'),
              ('chart', 'Laporan armada', 'Rekap jarak, jam operasi, dan perilaku mengemudi.'),
              ('truck', 'Instalasi GPS tracker', 'Pemasangan perangkat Teltonika di kendaraan ringan hingga alat berat.')],
         steps=['Inventaris armada & kebutuhan', 'Pemilihan perangkat', 'Instalasi di kendaraan', 'Konfigurasi dashboard & alert', 'Pelatihan dispatcher'],
         proof=['fleet-management', 'optimasi-rute-armada'],
         related=[('/produk/fms', 'Altora FMS'), ('/katalog#telt-fmc650', 'GPS tracker Teltonika'), ('/services/pengadaan-instalasi-maintenance', 'Pengadaan, instalasi & maintenance')],
         faq=[('Perangkat apa yang dipakai?', 'Kami memakai GPS tracker Teltonika yang dipilih sesuai jenis kendaraan, dari mobil operasional sampai truk dan alat berat.'),
              ('Bisa membaca data BBM?', 'Pada kendaraan yang mendukung, data BBM dan mesin dapat dibaca melalui OBD atau CAN; kami cek saat inventaris armada.'),
              ('Apakah bisa untuk alat berat tambang?', 'Bisa. Ada perangkat untuk kendaraan berat dan alat khusus, termasuk pembacaan data J1939.')]),
    dict(slug='pengadaan-instalasi-maintenance', name='Pengadaan, Instalasi & Maintenance', kicker='Perangkat keras',
         h1='Perangkat dipilihkan, dipasang, dan dirawat oleh satu tim.',
         lead='CCTV, GPS tracker, jaringan, komputer, kios layanan, display, rak server, dan fiber optik. Dari sumber resmi, dipasang tim kami di Balikpapan dan Samarinda, lalu dirawat secara berkala.',
         hero='/assets/img/portfolio/hardware-field/kiosk-pampang-install.jpg', hero_pos='50% 40%', chips=['Garansi resmi', 'Dipasang tim lokal', 'Perawatan berkala'],
         scope=[('/katalog-cctv-vigi', 'CCTV'), ('/katalog#telt-fmc920', 'GPS tracker'), ('/katalog#cat-rack', 'Rak server'), ('/katalog#hde-ifp', 'Display & ruang rapat'), ('/katalog#fas-otdr', 'Fiber optik'), ('/katalog#hde-aio-il24', 'Komputer')],
         pains=[('Beli sendiri, pasang sendiri', 'Perangkat sampai, tapi tidak ada yang memasang dan mengatur sampai siap pakai.'),
                ('Vendor berbeda-beda', 'Penjual, teknisi, dan pembuat aplikasi berbeda orang, jadi saat rusak saling lempar tanggung jawab.'),
                ('Rusak tanpa ketahuan', 'Kamera mati atau rekaman penuh baru ketahuan saat dibutuhkan.')],
         dos=[('cart_like', 'Pemilihan & pengadaan', 'Kami sarankan tipe yang sesuai lokasi dan anggaran, lengkap dengan penawaran dan faktur.'),
              ('pin', 'Survei lokasi', 'Cek titik pasang, jalur kabel, listrik, dan jaringan sebelum pemasangan.'),
              ('tool', 'Instalasi & konfigurasi', 'Tarik kabel, pasang perangkat, atur NVR, jaringan, dan aplikasi.'),
              ('shield', 'Uji & serah terima', 'Setiap perangkat diuji bersama tim Anda, lalu dibuatkan berita acara.'),
              ('users', 'Pelatihan pengguna', 'Tim Anda dilatih sampai bisa memakai sendiri.'),
              ('bell', 'Perawatan berkala', 'Pengecekan rutin, update firmware, dan bantuan klaim garansi.')],
         steps=['Konsultasi', 'Survei lokasi', 'Penawaran', 'Instalasi', 'Serah terima', 'Perawatan'],
         gallery=[('kiosk-air-putih.jpg', 'Persiapan kios layanan', 'Kios dibongkar dan disiapkan di lokasi.', False),
                  ('kiosk-baqa-service.jpg', 'Pengecekan kios', 'Uji layar sentuh, keyboard, dan printer.', False),
                  ('aio-baqa.jpg', 'Komputer kantor', 'Penataan PC dan perangkat pendukung.', False),
                  ('serah-terima-raya-makmur.jpg', 'Serah terima', 'Penyerahan perangkat di Kelurahan Rawa Makmur.', False),
                  ('tablet-sidodamai.jpg', 'Penyerahan tablet', 'Tablet untuk staf Kelurahan Sidodamai.', False)],
         proof=['custom-kios-k-pengadaan-hardware', 'instalasi-cctv-ai-analytics', 'unmul-infrastruktur-cctv-jaringan'],
         related=[('/katalog', 'Katalog perangkat'), ('/services/ai-cctv', 'AI CCTV & Safety'), ('/services/fleet-management-service', 'Fleet Management')],
         faq=[('Apakah garansinya resmi?', 'Ya. Perangkat berasal dari principal partner Altora dan memakai garansi resmi. Kami bantu proses klaimnya.'),
              ('Bisa untuk pengadaan instansi?', 'Bisa. Kami siapkan penawaran, faktur, dan berita acara serah terima. Produk ber-TKDN tersedia sesuai ketersediaan dari principal.'),
              ('Melayani di luar Balikpapan dan Samarinda?', 'Bisa, tergantung lokasi dan cakupan pekerjaan. Hubungi kami untuk dicek.')]),
    dict(slug='starlink-internet-satelit', name='Starlink & Internet Satelit', kicker='Konektivitas',
         h1='Internet cepat untuk lokasi tanpa jaringan kabel.',
         lead='Pemasangan Starlink lengkap dengan instalasi, konfigurasi, repeater WiFi, dan panel surya untuk tambang, perkebunan, proyek, dan kantor di pedalaman Kalimantan. Perangkat kami adakan sendiri, lalu kami pasang dan rawat.',
         hero='/assets/img/portfolio/agri.jpg', hero_pos='50% 50%', chips=['Partner resmi', 'Tenaga surya', 'Remote site'],
         pains=[('Sinyal seluler tidak ada di lokasi', 'Laporan dari site harus menunggu petugas kembali ke kota.'),
                ('Tidak ada listrik PLN', 'Perangkat internet tidak bisa menyala sepanjang hari.'),
                ('Sinyal tidak merata di area luas', 'Hanya satu titik yang dapat internet, area lain tetap putus.')],
         dos=[('sat', 'Pemasangan Starlink', 'Perangkat resmi, mounting, kabel, instalasi, dan konfigurasi di lokasi.'),
              ('bolt', 'Panel surya off-grid', 'Untuk lokasi tanpa PLN supaya internet menyala 24 jam.'),
              ('sensor', 'Repeater WiFi', 'Sinyal diperluas ke seluruh area kantor atau site.'),
              ('camera', 'CCTV & GPS di remote site', 'Internet satelit dipakai untuk CCTV, GPS tracker, dan laporan dari lapangan.'),
              ('tool', 'Perawatan', 'Pengecekan perangkat dan bantuan saat ada gangguan.'),
              ('shield', 'Perangkat asli', 'Kit Starlink asli dengan garansi pabrikan.')],
         steps=['Konsultasi', 'Survei lokasi', 'Penawaran', 'Pemasangan', 'Konfigurasi & uji', 'Perawatan'],
         proof=['fleet-management', 'iot-monitoring-lahan'],
         related=[('/katalog', 'Katalog perangkat'), ('/services/fleet-management-service', 'Fleet management'), ('/services/ai-cctv', 'AI CCTV')],
         faq=[('Starlink cocok untuk lokasi seperti apa?', 'Untuk lokasi tanpa jaringan kabel atau sinyal seluler yang lemah, seperti tambang, perkebunan, proyek konstruksi, dan kantor di pedalaman.'),
              ('Bagaimana kalau tidak ada listrik?', 'Kami pasang paket dengan panel surya dan baterai supaya perangkat tetap menyala tanpa PLN.'),
              ('Apakah bisa untuk CCTV dan GPS tracker?', 'Bisa. Internet dari Starlink dipakai untuk mengirim data CCTV, GPS tracker, dan aplikasi dari lokasi.')]),
    dict(slug='instalasi-listrik-jaringan', name='Instalasi Listrik & Jaringan', kicker='Infrastruktur',
         h1='Instalasi listrik dan jaringan yang aman dan rapi.',
         lead='Pemasangan, penambahan, dan perbaikan instalasi listrik serta jaringan untuk kantor, ruko, sekolah, rumah, dan fasilitas umum. Kabel tembaga sesuai beban, proteksi dan grounding yang benar.',
         hero='/assets/img/portfolio/unmul-infrastructure/network-rack.png', hero_pos='50% 50%', chips=['Standar keamanan', 'Rapi & berlabel', 'Bergaransi'],
         pains=[('Listrik sering turun', 'MCB tidak sesuai beban atau grounding tidak berfungsi.'),
                ('Kabel semrawut', 'Sulit dirawat dan berisiko korsleting.'),
                ('Perangkat baru butuh jalur baru', 'AC, CCTV, atau server ditambah tanpa perencanaan jalur.')],
         dos=[('bolt', 'Instalasi baru', 'Titik lampu, stop kontak, dan jalur baru.'),
              ('shield', 'Panel & proteksi', 'MCB, RCBO, grounding, dan box panel.'),
              ('plug', 'Beban khusus', 'Jalur untuk AC, pemanas air, pompa, dan peralatan berdaya besar.'),
              ('layout', 'Jaringan terstruktur', 'LAN, PoE, switch, dan WiFi dipasang rapi dan berlabel.'),
              ('pen', 'Dokumentasi', 'Denah jalur dan daftar titik diserahkan setelah selesai.'),
              ('tool', 'Garansi kerja', 'Pekerjaan bergaransi sesuai lingkup proyek.')],
         steps=['Konsultasi', 'Survei lokasi', 'Penawaran', 'Pengerjaan', 'Uji fungsi', 'Serah terima'],
         proof=['unmul-infrastruktur-cctv-jaringan', 'custom-kios-k-pengadaan-hardware'],
         related=[('/jasa-instalasi-jaringan-samarinda', 'Instalasi jaringan Samarinda'), ('/jasa-instalasi-jaringan-balikpapan', 'Instalasi jaringan Balikpapan'), ('/services/pengadaan-instalasi-maintenance', 'Pengadaan & maintenance')],
         faq=[('Standar apa yang dipakai?', 'Kabel tembaga sesuai beban, jalur memakai conduit pelindung, sambungan di junction box, dan stop kontak terhubung grounding.'),
              ('Bisa sekalian jaringan internet dan CCTV?', 'Bisa. Listrik, jaringan, dan CCTV bisa dikerjakan bersamaan supaya penarikan kabel cukup sekali.'),
              ('Melayani rumah dan ruko?', 'Ya, selain kantor, sekolah, dan fasilitas umum.')]),
    dict(slug='smart-display-kios', name='Smart Display, Signage & Kios', kicker='Layar & layanan mandiri',
         h1='Layar yang informatif, layanan yang tidak antre.',
         lead='Digital signage, layar interaktif untuk rapat dan kelas, serta kios layanan mandiri yang bisa mencetak dokumen dan struk. Dipasang siap pakai dan dikelola dari satu tempat.',
         hero='/assets/img/portfolio/hardware-field/kiosk-baqa-service.jpg', hero_pos='50% 40%', chips=['Kelola dari cloud', 'Kios mandiri', 'Layar interaktif'],
         pains=[('Antrean panjang di loket', 'Warga atau pelanggan menunggu lama untuk layanan sederhana.'),
                ('Informasi cepat basi', 'Spanduk dan poster harus dicetak ulang setiap ada perubahan.'),
                ('Rapat dan kelas kurang interaktif', 'Presentasi masih bergantung pada proyektor dan papan tulis.')],
         dos=[('monitor', 'Digital signage', 'Gambar, video, dan pengumuman yang dijadwalkan dari jarak jauh.'),
              ('layout', 'Layar interaktif', 'Layar sentuh besar untuk rapat, presentasi, dan kelas.'),
              ('users', 'Kios layanan mandiri', 'Layar sentuh, pemindai barcode, dan printer struk atau dokumen.'),
              ('plug', 'Terhubung ke sistem', 'Kios terhubung ke aplikasi layanan atau antrean yang sudah ada.'),
              ('tool', 'Pemasangan siap pakai', 'Perangkat dipasang, dikonfigurasi, dan diuji di lokasi.'),
              ('bell', 'Perawatan', 'Pengecekan berkala dan bantuan saat ada kendala.')],
         steps=['Konsultasi', 'Survei lokasi', 'Penawaran', 'Pemasangan', 'Konfigurasi konten', 'Perawatan'],
         proof=['custom-kios-k-pengadaan-hardware'],
         related=[('/katalog#hde-ifp', 'Layar interaktif HDe'), ('/katalog#hde-videotron-indoor', 'Videotron'), ('/portfolio/custom-kios-k-pengadaan-hardware', 'Kios kelurahan Samarinda')],
         faq=[('Konten signage diubah dari mana?', 'Dari aplikasi pengelola berbasis cloud, termasuk penjadwalan otomatis per jam atau per hari.'),
              ('Kios bisa untuk layanan apa saja?', 'Antrean, pendaftaran, cetak dokumen, dan layanan mandiri lain yang terhubung ke sistem Anda. Kios kami sudah dipakai di kantor kelurahan Samarinda.'),
              ('Ukuran layar interaktif berapa?', 'Tersedia ukuran besar untuk ruang rapat dan kelas. Kami bantu pilihkan sesuai ruangan.')]),
    dict(slug='private-ai-gis', name='Private AI & GIS', kicker='AI & data spasial',
         h1='AI yang berjalan di server Anda sendiri.',
         lead='Sistem AI untuk menganalisis dokumen dan data internal tanpa mengirim data ke cloud publik, serta GIS untuk memetakan dan menganalisis data wilayah. Cocok untuk instansi dan perusahaan dengan data sensitif.',
         hero='/assets/img/portfolio/barito-dash.jpg', hero_pos='50% 50%', chips=['On-premise', 'Data aman', 'Peta data wilayah'],
         pains=[('Data sensitif tidak boleh keluar', 'AI publik tidak bisa dipakai karena data harus tetap di dalam instansi.'),
                ('Data wilayah tersebar', 'Peta dan data per dinas atau kecamatan sulit dibaca bersama.'),
                ('Laporan disusun manual', 'Dokumen dan data dibaca satu per satu untuk membuat ringkasan.')],
         dos=[('brain', 'AI on-premise', 'Model AI berjalan di server Anda, bisa tanpa akses internet.'),
              ('pen', 'Analisis dokumen', 'Ringkasan, pencarian, dan jawaban dari dokumen internal.'),
              ('map', 'GIS & dashboard peta', 'Data spasial dari banyak perangkat daerah dalam satu peta.'),
              ('chart', 'Dashboard data', 'Visualisasi data untuk perencanaan dan pengambilan keputusan.'),
              ('shield', 'Keamanan data', 'Enkripsi, kontrol akses, dan backup.'),
              ('users', 'Pelatihan tim', 'Tim Anda dilatih memakai dan merawat sistemnya.')],
         steps=['Konsultasi', 'Pemetaan data', 'Desain sistem', 'Pemasangan server', 'Uji coba', 'Pelatihan & dukungan'],
         proof=['pompy-batara', 'portal-one-map', 'media-monitoring-dashboard'],
         related=[('/services/software-custom', 'Software custom'), ('/portfolio/pompy-batara', 'POMPY BATARA'), ('/portfolio/portal-one-map', 'Portal One Map')],
         faq=[('Apa bedanya dengan AI biasa?', 'AI biasa memproses data di server penyedia di luar negeri. Private AI berjalan di server Anda sendiri, sehingga data tidak keluar.'),
              ('Untuk siapa sistem ini?', 'Instansi pemerintah, perusahaan keuangan, kesehatan, dan tambang yang punya data sensitif.'),
              ('Apakah Altora punya pengalaman GIS?', 'Ya, di antaranya portal kebijakan satu peta POMPY BATARA dan dashboard geospasial untuk Pemkab Barito Utara.')]),
]


def build(sv):
    url = f'/services/{sv["slug"]}'
    chips = ''.join(f'<span class="svd-chip svd-chip-{i}">{e(c)}</span>' for i, c in enumerate(sv['chips']))
    pains = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in sv['pains'])
    dos = ''.join(f'<article class="svd-do"><span class="svd-ico">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, t, d in sv['dos'])
    steps = ''.join(f'<li><b>{e(s)}</b></li>' for s in sv['steps'])
    proof = ''.join(f'<a class="svd-proof" href="/portfolio/{p}"><span class="svd-proof-img"><img alt="" loading="lazy" src="{PF[p][1]}"/></span><b>{e(PF[p][0])}</b><small>Lihat dokumentasi</small></a>' for p in sv['proof'])
    related = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in sv['related'])
    scope = ''
    if sv.get('scope'):
        scope = '<nav aria-label="Cakupan" class="svd-scope">' + ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in sv['scope']) + '</nav>'
    gallery = ''
    if sv.get('gallery'):
        figs = ''.join(f'<figure class="svd-photo{" svd-photo-wide" if w else ""}"><img alt="{e(t)}" loading="lazy" src="/assets/img/portfolio/hardware-field/{f}"/><figcaption><b>{e(t)}</b><span>{e(c)}</span></figcaption></figure>' for f, t, c, w in sv['gallery'])
        gallery = f'<section class="svd-sec" id="dokumentasi"><div class="ct-wrap"><div class="pd-block-head"><h2>Dokumentasi pekerjaan</h2><p>Foto dari proyek pengadaan dan pemasangan kami di kantor kelurahan Samarinda.</p></div><div class="svd-gallery">{figs}</div></div></section>'
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in sv['faq'])
    msg = f'Halo Altora, saya ingin konsultasi layanan {sv["name"]}.'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': sv['name'], 'description': sv['lead'], 'url': 'https://altora.id' + url,
         'provider': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': 'https://altora.id/'},
         'areaServed': ['Balikpapan', 'Samarinda', 'Kalimantan Timur', 'Indonesia']},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in sv['faq']]}]}
    title = f'{sv["name"]} | Layanan Altora Indonesia'
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title><meta content="{e(sv["lead"][:158])}" name="description"/><link href="https://altora.id{url}" rel="canonical"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(title)}" property="og:title"/><meta content="{e(sv["lead"])}" property="og:description"/><meta content="https://altora.id{url}" property="og:url"/><meta content="https://altora.id{sv["hero"]}" property="og:image"/><link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
<main class="ct-page svd-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/services">Layanan</a><span>/</span><span>{e(sv["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">{e(sv["kicker"])}</p><h1>{e(sv["h1"])}</h1><p class="ct-lead">{e(sv["lead"])}</p>{scope}
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#bukti">Lihat proyek terkait</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(sv["name"])}" src="{sv["hero"]}" style="object-position:{sv["hero_pos"]}"/>{chips}</figure>
</div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Masalah yang sering kami temui</h2></div><ul>{pains}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang kami kerjakan</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Alur kerja</h2></div><ol class="svd-steps">{steps}</ol></div></section>
{gallery}
<section class="svd-sec" id="bukti"><div class="ct-wrap"><div class="pd-block-head"><h2>Proyek terkait</h2></div><div class="svd-proofs">{proof}</div>
<div class="svd-related"><b>Terkait</b>{related}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Siap mulai? Hubungi kami.</h2><p>Ceritakan kebutuhan {e(sv["name"])} Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat via WhatsApp</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


for sv in SERVICES:
    (root / 'services' / f'{sv["slug"]}.html').write_text(build(sv), encoding='utf-8')
print('layanan dibangun:', ', '.join(sv['slug'] for sv in SERVICES))
