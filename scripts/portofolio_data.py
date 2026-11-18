"""Data portofolio proyek + komponen kartu (dipakai build_portofolio.py, build_infra.py, build_trust.py).
Sumber: konten lama Altora (4 proyek perangkat) dan halaman /portfolio perusahaan saudara (17 proyek, termasuk ringkasan,
fitur utama, teknologi, klien, dan tahun); teks ditulis ulang ke suara Altora. Tanpa harga dan tanpa testimoni.
Gambar di assets/img/portofolio/: tangkapan layar proyek, ilustrasi ASCII ungu (diwarnai ulang dari aset saudara,
atau dibuat dengan gaya yang sama untuk proyek khusus Altora), dan foto absensi dengan wajah dipikselkan."""
import html

e = lambda t: html.escape(str(t), quote=True)

GROUPS = [
    ('infra', 'Infrastruktur, IoT & hardware', 'Perangkat, jaringan, kamera, dan sensor yang dipasang di lokasi.'),
    ('ai', 'AI & computer vision', 'Analitik kamera, pengenalan wajah, NLP, dan pembacaan data operasional.'),
    ('software', 'Software & data', 'Portal, dashboard, HRIS, antrian, dan sistem informasi untuk instansi dan perusahaan.'),
    ('web', 'Website', 'Website resmi dengan konten yang dikelola lewat CMS.'),
]

ICONS = {
    'check': '<path d="M6 12.5 10 16.5 18 8"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'ext': '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    'doc': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
}
icon = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[n]}</svg>'

IMG = '/assets/img/portofolio/'
ART = IMG + 'art/'
# Layanan Altora terkait (kartu kecil di halaman detail): (url, judul, keterangan, ilustrasi)
SVC = {
    'infra': ('/infrastruktur-hardware-kaltim', 'Infrastruktur & hardware Kaltim', 'Jaringan, CCTV AI, dan perangkat lapangan', 'safety.webp'),
    'tracking': ('/services/tracking', 'Tracking armada & aset', 'GPS, telematik, dan dashboard armada', 'fleet.webp'),
    'iot': ('/services/iot-custom', 'IoT custom', 'Sensor, perangkat, dan notifikasi', 'smartlock.webp'),
    'lock': ('/services/smart-lock', 'Smart lock', 'Kunci pintar dan riwayat akses', 'smartlock.webp'),
    'ai': ('/services/ai-custom', 'AI custom', 'Computer vision dan NLP untuk operasional', 'attendance.webp'),
    'private': ('/services/private-ai', 'AI lokal', 'AI yang berjalan di server Anda', 'attendance.webp'),
    'software': ('/services/software-custom', 'Software custom', 'Aplikasi web dan mobile sesuai alur kerja', 'hris.webp'),
    'web': ('/services/web-custom', 'Web custom', 'Portal, dashboard, dan aplikasi web', 'website.webp'),
    'website': ('/services/website-seo', 'Website & SEO', 'Website resmi yang mudah dikelola', 'website.webp'),
}

# Urutan = urutan tampil di halaman /portofolio.
# desc = ringkasan kartu; lead = kalimat pembuka halaman detail; about = paragraf "Tentang proyek ini"; feats = fitur utama.
PROJECTS = [
    # ── Infrastruktur, IoT & hardware ──
    dict(slug='rm-payakumbuah', group='infra', title='Jaringan, CCTV, dan POS rumah makan', client='RM Payakumbuah', year='', img='rm-payakumbuah.webp',
         desc='Kasir POS, CCTV multi-sudut, switch 24-port, Wi-Fi pelanggan, dan walkie talkie dapur untuk operasional rumah makan.',
         lead='Perangkat operasional rumah makan, dari kasir sampai dapur, dipasang dan dirapikan satu tim.',
         about='Kami mengadakan dan memasang perangkat operasional RM Payakumbuah: kasir POS, CCTV multi-sudut untuk area makan dan dapur, switch 24-port sebagai inti jaringan, access point untuk pelanggan, dan walkie talkie untuk koordinasi dapur. Kabel dan perangkat ditata supaya mudah dirawat.',
         feats=[('Kasir POS', 'Perangkat kasir untuk transaksi harian.'), ('CCTV multi-sudut', 'Area makan, kasir, dan dapur terpantau.'),
                ('Jaringan & Wi-Fi', 'Switch 24-port dan access point pelanggan.'), ('Radio dapur', 'Walkie talkie untuk koordinasi tim.')],
         tags=['POS', 'CCTV', 'Jaringan', 'Radio'], svc='infra'),
    dict(slug='fleet-radio-kapal', group='infra', title='GPS armada dan radio marine VHF', client='Logistik & maritim · Mahakam', year='', img='fleet-radio-kapal.webp',
         desc='GPS tracker untuk armada logistik tambang di Kaltim dan radio marine VHF untuk komunikasi transportasi perairan Mahakam.',
         lead='Posisi armada darat dan komunikasi kapal di Sungai Mahakam dalam satu pekerjaan lapangan.',
         about='Pemasangan GPS tracker untuk armada logistik tambang di Kalimantan Timur, serta integrasi radio marine VHF untuk komunikasi transportasi perairan di Sungai Mahakam. Pekerjaan mencakup pemasangan perangkat di unit, pengujian sinyal, dan serah terima ke tim operasional.',
         feats=[('GPS tracker armada', 'Posisi dan riwayat perjalanan unit.'), ('Radio marine VHF', 'Komunikasi kapal di perairan Mahakam.'),
                ('Pemasangan di unit', 'Dikerjakan langsung di armada dan kapal.'), ('Uji & serah terima', 'Sinyal diuji sebelum dipakai tim.')],
         tags=['GPS tracker', 'Radio VHF', 'Maritim'], svc='tracking', link=('/blog/integrasi-erp-logistik-maritim-kaltim', 'ERP untuk logistik maritim')),
    dict(slug='fleet-management-tambang', group='infra', title='Fleet management armada hauling', client='Kontraktor tambang · Kaltim', year='2025', img='fleet-management-tambang.webp',
         desc='Telematik armada hauling: posisi dan riwayat perjalanan, status unit, geofence, dan laporan operasi dalam satu dashboard.',
         lead='Telematik armada untuk visibilitas perjalanan, status kendaraan, dan operasi lapangan.',
         about='Sistem fleet management untuk armada hauling kontraktor tambang di Kalimantan Timur. Perangkat telematik membaca posisi dan data kendaraan (termasuk CAN-Bus), lalu dashboard menampilkan perjalanan, status unit, peringatan geofence, dan laporan operasi untuk pengawas dan manajemen.',
         feats=[('Live fleet monitoring', 'Posisi dan status unit secara langsung.'), ('Riwayat perjalanan', 'Rute dan jam operasi tiap unit.'),
                ('Alert & geofence', 'Peringatan saat unit keluar area atau berhenti lama.'), ('Laporan operasi', 'Rekap harian untuk pengawas dan manajemen.')],
         tags=['Telematika', 'CAN-Bus', 'Geofence'], svc='tracking', pos='center top'),
    dict(slug='kios-mandiri-kelurahan', group='infra', title='Anjungan layanan mandiri kelurahan', client='Pemerintahan & pelayanan', year='', img='kios-mandiri-kelurahan.webp',
         desc='Rancangan hardware Anjungan Layanan Mandiri (Kios-K) layar sentuh supaya pengurusan surat kependudukan berjalan tanpa antre.',
         lead='Kios layar sentuh supaya warga bisa mengurus surat sendiri tanpa menunggu di loket.',
         about='Rancangan perangkat Anjungan Layanan Mandiri (Kios-K) untuk kelurahan: layar sentuh, printer, dan casing yang tahan dipakai publik. Warga memilih layanan dan mencetak berkas sendiri, sehingga petugas bisa fokus pada pengurusan yang perlu verifikasi.',
         feats=[('Layar sentuh', 'Menu layanan yang mudah dipakai warga.'), ('Cetak mandiri', 'Berkas dicetak langsung di kios.'),
                ('Casing publik', 'Dirancang untuk area pelayanan yang ramai.'), ('Antrean berkurang', 'Petugas fokus pada verifikasi.')],
         tags=['Kios-K', 'Layar sentuh', 'Pelayanan publik'], svc='infra'),
    dict(slug='iot-monitoring-gudang', group='infra', title='Pemantau ruang server dan gudang', client='Industri & pergudangan', year='', img='iot-monitoring-gudang.webp',
         desc='Sensor suhu, kelembapan, kebocoran, dan asap yang aktif sepanjang waktu, dengan notifikasi WhatsApp dan dashboard pusat.',
         lead='Ruang server dan gudang dipantau sensor sepanjang waktu, dengan peringatan langsung ke WhatsApp.',
         about='Sensor suhu, kelembapan, kebocoran air, dan asap dipasang di ruang server dan gudang. Data dikirim ke dashboard pusat, dan saat nilai melewati batas, tim penanggung jawab menerima notifikasi WhatsApp sehingga masalah tertangani sebelum merusak perangkat atau barang.',
         feats=[('Suhu & kelembapan', 'Dibaca terus-menerus dari tiap ruang.'), ('Kebocoran & asap', 'Deteksi dini kejadian berbahaya.'),
                ('Notifikasi WhatsApp', 'Peringatan langsung ke penanggung jawab.'), ('Dashboard pusat', 'Semua lokasi dalam satu layar.')],
         tags=['IoT', 'Sensor', 'WhatsApp'], svc='iot'),
    dict(slug='cctv-ai-farmasi-unmul', group='infra', title='Instalasi CCTV siap analitik AI, 50+ unit', client='Fakultas Farmasi Universitas Mulawarman', year='2025', img='cctv-ai-farmasi-unmul.webp',
         desc='Lebih dari 50 kamera VIGI yang disiapkan untuk analitik AI dan pemantauan operasional, dipasang langsung di lokasi.',
         lead='Infrastruktur kamera yang disiapkan untuk analitik vision dan monitoring operasional.',
         about='Pemasangan lebih dari 50 kamera VIGI di lingkungan Fakultas Farmasi Universitas Mulawarman. Titik kamera, jaringan, dan perekam disiapkan supaya analitik AI bisa ditambahkan di atas kamera yang sama, tanpa pemasangan ulang.',
         feats=[('Infrastruktur CCTV', 'Kamera, jaringan, dan perekam terpasang rapi.'), ('Kamera siap AI', 'Siap ditambah analitik vision.'),
                ('Monitoring', 'Pemantauan operasional gedung.'), ('Implementasi di lokasi', 'Dikerjakan langsung oleh tim lapangan.')],
         tags=['CCTV AI', 'VIGI', '50+ unit'], svc='infra'),
    dict(slug='smartlock-farmasi-unmul', group='infra', title='Smartlock akses gedung kampus', client='Fakultas Farmasi Universitas Mulawarman', year='2025', img='smartlock-farmasi-unmul.webp',
         desc='Kontrol akses digital untuk ruang dan gedung kampus, dengan pemantauan perangkat dan riwayat akses.',
         lead='Kontrol akses ruang dan gedung yang terhubung ke alur operasional digital.',
         about='Smartlock untuk ruang dan gedung di Fakultas Farmasi Universitas Mulawarman. Akses diberikan dari aplikasi, status perangkat terpantau, dan setiap pembukaan pintu tercatat sehingga pengelola gedung tahu siapa masuk dan kapan.',
         feats=[('Access control', 'Hak akses per ruang dan per pengguna.'), ('Monitoring perangkat', 'Status kunci dan baterai terpantau.'),
                ('Riwayat akses', 'Setiap pembukaan pintu tercatat.'), ('Integrasi IoT', 'Terhubung ke aplikasi dan sistem lain.')],
         tags=['IoT', 'Kontrol akses'], svc='lock', pos='center 30%'),
    dict(slug='iot-monitoring-lahan-sawit', group='infra', title='Pemantau cuaca dan kelembapan lahan', client='Perkebunan sawit · Kaltim', year='2025', img='iot-monitoring-lahan-sawit.webp',
         desc='Kelembapan tanah, suhu, dan kelembapan udara dibaca dari sensor lewat jaringan LoRa, lalu tampil di HP petugas lapangan.',
         lead='Kelembapan tanah, suhu, dan kelembapan udara dari sensor, langsung di HP petugas.',
         about='Sensor lahan untuk perkebunan sawit di Kalimantan Timur. Kelembapan tanah, suhu, dan kelembapan udara dikirim lewat jaringan LoRa yang menjangkau area kebun luas, lalu tampil di aplikasi HP petugas lengkap dengan catatan lapangan.',
         feats=[('Kelembapan tanah', 'Dibaca dari sensor di beberapa blok.'), ('Suhu & kelembapan udara', 'Kondisi cuaca mikro di lahan.'),
                ('Konektivitas LoRa', 'Jangkauan luas tanpa sinyal seluler.'), ('Catatan lapangan', 'Petugas mencatat temuan dari HP.')],
         tags=['Sensor', 'LoRa', 'Cuaca'], svc='iot'),
    # ── AI & computer vision ──
    dict(slug='deteksi-apd-ai', group='ai', title='Deteksi APD berbasis AI', client='PT Multi Harapan Utama', year='2025', img='deteksi-apd-ai.webp',
         desc='Analitik vision dari kamera untuk memantau kepatuhan APD, dengan pemantauan kejadian dan peringatan operasional.',
         lead='Analitik vision untuk membantu memantau kepatuhan atribut keselamatan kerja dari kamera.',
         about='Analitik kamera untuk PT Multi Harapan Utama yang mengenali atribut keselamatan kerja seperti helm, rompi, dan sepatu safety. Kejadian pelanggaran dicatat dengan foto, lalu tim K3 menerima peringatan untuk ditindaklanjuti.',
         feats=[('Safety detection', 'Mengenali helm, rompi, dan sepatu safety.'), ('CCTV analytics', 'Berjalan di atas kamera yang terpasang.'),
                ('Event monitoring', 'Kejadian tercatat lengkap dengan foto.'), ('Alert operasional', 'Peringatan ke tim K3 untuk ditindak.')],
         tags=['AI', 'Vision', 'K3'], svc='ai', pos='center 20%'),
    dict(slug='smart-attendance-unmul', group='ai', title='Absensi face recognition', client='Universitas Mulawarman', year='2025', img='smart-attendance-unmul.webp',
         desc='Absensi otomatis dengan pengenalan wajah dari aliran kamera CCTV, lengkap dengan event kehadiran dan jejak audit.',
         lead='Absensi otomatis dengan pengenalan wajah dari aliran kamera CCTV.',
         about='Sistem absensi untuk Universitas Mulawarman yang mengenali wajah dari aliran kamera CCTV, lalu mencatat event kehadiran tanpa perlu antre di mesin absen. Setiap event punya jejak audit. Wajah pada gambar disamarkan.',
         feats=[('Face recognition', 'Wajah dikenali dari kamera CCTV.'), ('Event kehadiran', 'Kehadiran tercatat otomatis.'),
                ('Integrasi CCTV', 'Memakai kamera yang sudah terpasang.'), ('Audit trail', 'Setiap event bisa ditelusuri.')],
         tags=['Face recognition', 'CCTV', 'Mobile'], svc='ai'),
    dict(slug='optimasi-rute-armada', group='ai', title='Optimasi rute dan monitoring armada distribusi', client='Operator logistik · Balikpapan', year='2024', img='optimasi-rute-armada.webp',
         desc='Monitoring distribusi dan pembacaan rute armada untuk operasi logistik: GPS, visibilitas armada, dan pemantauan rute.',
         lead='Dukungan monitoring distribusi dan pembacaan rute armada untuk operasi logistik.',
         about='Untuk operator logistik di Balikpapan: data GPS armada distribusi dibaca untuk memantau rute yang dilalui, membandingkannya dengan rencana, dan memberi visibilitas armada kepada tim operasional.',
         feats=[('Route monitoring', 'Rute aktual dibanding rencana.'), ('GPS', 'Posisi armada dari perangkat GPS.'),
                ('Visibilitas armada', 'Status seluruh unit dalam satu layar.'), ('Logistik', 'Disusun untuk operasi distribusi.')],
         tags=['Route AI', 'GPS', 'Armada'], svc='tracking'),
    dict(slug='media-monitoring', group='ai', title='Dashboard media monitoring dan analitik isu', client='Intelligence Media Management', year='2024', img='media-monitoring.webp',
         desc='Dashboard untuk membaca isu dan aktivitas media, dengan pelacakan isu dan analitik sebagai bahan insight operasional.',
         lead='Dashboard untuk membaca isu dan aktivitas media sebagai bahan insight operasional.',
         about='Dashboard untuk Intelligence Media Management yang mengumpulkan pemberitaan, mengelompokkan isu, dan menampilkan perkembangannya. Tim bisa melacak isu tertentu dan membaca analitiknya tanpa merekap manual.',
         feats=[('Media monitoring', 'Pemberitaan terkumpul otomatis.'), ('Pelacakan isu', 'Isu dikelompokkan dan diikuti.'),
                ('Analitik', 'Tren dan sebaran isu.'), ('Dashboard', 'Ringkasan untuk pimpinan.')],
         tags=['NLP', 'Analitik'], svc='ai', pos='left top'),
    dict(slug='sentiment-social-listening', group='ai', title='Analisis sentimen dan social listening', client='Platform analitik media sosial', year='2025', img='sentiment-social-listening.webp',
         desc='Analisis percakapan publik untuk membaca tema, sentimen, dan perkembangan isu, lengkap dengan pelaporan.',
         lead='Analisis percakapan publik untuk membantu tim membaca tema, sentimen, dan perkembangan isu.',
         about='Dashboard social listening untuk platform analitik media sosial. Percakapan publik dikumpulkan, sentimennya dibaca, dan topiknya dipantau dari waktu ke waktu, lalu dirangkum dalam laporan.',
         feats=[('Social listening', 'Percakapan publik terkumpul.'), ('Analisis sentimen', 'Positif, negatif, dan netral.'),
                ('Pemantauan topik', 'Perkembangan isu dari waktu ke waktu.'), ('Pelaporan', 'Ringkasan siap dibagikan.')],
         tags=['NLP', 'Social listening'], svc='ai', pos='left top'),
    dict(slug='transkripsi-rapat', group='ai', title='Transkripsi rapat bahasa Indonesia', client='Korporasi & kampus · Kaltim', year='2025', img='transkripsi-rapat.webp',
         desc='Transkripsi rapat berbahasa Indonesia yang berjalan di server sendiri, untuk catatan rapat dan pencarian informasi kembali.',
         lead='Transkripsi bahasa Indonesia untuk dokumentasi rapat dan pencarian kembali informasi.',
         about='Untuk korporasi dan kampus di Kalimantan Timur: rekaman rapat diubah menjadi teks bahasa Indonesia di server milik organisasi sendiri, lalu dirangkum menjadi catatan rapat yang bisa dicari kembali.',
         feats=[('Speech to text', 'Rekaman rapat menjadi teks.'), ('Catatan rapat', 'Ringkasan dan poin keputusan.'),
                ('Bahasa Indonesia', 'Dilatih untuk percakapan sehari-hari.'), ('Knowledge capture', 'Isi rapat bisa dicari kembali.')],
         tags=['ASR', 'NLP', 'On-prem'], svc='private'),
    # ── Software & data ──
    dict(slug='pompy-batara', group='software', title='POMPy BATARA: portal one map dan dashboard daerah', client='Diskominfosandi Kab. Barito Utara', year='2025', img='pompy-batara.webp',
         desc='Portal peta tematik yang menyatukan data spasial dan tematik dari berbagai perangkat daerah sebagai dasar keputusan berbasis data.',
         lead='Portal peta tematik yang menyatukan data spasial dan tematik sebagai fondasi akses informasi publik dan keputusan berbasis data.',
         about='POMPy BATARA adalah portal peta tematik yang mengintegrasikan data spasial dan tematik dari berbagai perangkat daerah Kabupaten Barito Utara. Portal ini membuka informasi pembangunan dan membantu membaca data lapangan dalam konteks wilayah. Kabupaten Barito Utara meraih Digital Innovation Award 2026 melalui POMPy BATARA.',
         source=('https://kalteng.antaranews.com/berita/827475/barito-utara-raih-digital-innovation-award-2026-melalui-pompy-batara', 'ANTARA: Barito Utara raih Digital Innovation Award 2026 melalui POMPy BATARA'),
         feats=[('Peta tematik', 'Data wilayah dalam lapisan peta.'), ('Data terintegrasi', 'Dari berbagai perangkat daerah.'),
                ('Akses informasi', 'Terbuka untuk publik.'), ('Dasar keputusan', 'Membaca data dalam konteks wilayah.')],
         tags=['Web', 'GIS', 'One Map'], svc='web', link=('https://pompy.baritoutarakab.go.id', 'Buka situs POMPy BATARA'), pos='left top'),
    dict(slug='dashboard-geospasial-dapodik', group='software', title='Dashboard geospasial DAPODIK', client='Diskominfosandi Kab. Barito Utara', year='2024', img='dashboard-geospasial-dapodik.webp',
         desc='Peta sebaran sekolah dari data DAPODIK, dengan dashboard analitik untuk mendukung keputusan di bidang pendidikan.',
         lead='Pemetaan data pendidikan untuk membaca sebaran informasi dan mendukung pengambilan keputusan.',
         about='Dashboard geospasial untuk Diskominfosandi Kabupaten Barito Utara yang memetakan sekolah dari data DAPODIK. Sebaran sekolah, jumlah siswa, dan indikator lain bisa dibaca per wilayah sebagai bahan perencanaan pendidikan.',
         feats=[('Pemetaan sekolah', 'Lokasi sekolah di peta wilayah.'), ('Data spasial', 'Indikator dibaca per kecamatan.'),
                ('Dashboard analitik', 'Ringkasan angka pendidikan.'), ('Akses informasi', 'Mudah dibuka pemangku kepentingan.')],
         tags=['GIS', 'DAPODIK', 'Dashboard'], svc='web', pos='left top'),
    dict(slug='hris-mobile-payroll', group='software', title='HRIS mobile: absensi, payroll, dan slip gaji', client='Bukit Baiduri Energi', year='2024', img='hris-mobile-payroll.webp',
         desc='Kehadiran, payroll, dan informasi karyawan dalam satu alur, dengan akses karyawan dari HP.',
         lead='Kehadiran, payroll, dan informasi karyawan dalam alur kerja yang terhubung.',
         about='HRIS untuk Bukit Baiduri Energi: absensi, cuti, payroll, dan slip gaji dikelola dalam satu alur. Karyawan membuka jadwal, pengumuman, dan slip gaji dari aplikasi HP, sementara tim HR tidak perlu merekap ulang.',
         feats=[('Attendance', 'Absensi karyawan dari aplikasi.'), ('Payroll workflow', 'Gaji dihitung dari data kehadiran.'),
                ('Akses karyawan', 'Slip gaji dan pengumuman di HP.'), ('Pengalaman mobile', 'Dirancang untuk dipakai di lapangan.')],
         tags=['HRIS', 'Mobile', 'Payroll'], svc='software', pos='left top'),
    dict(slug='antrian-poliklinik', group='software', title='Sistem antrian dan pendaftaran poliklinik', client='Klinik & RS swasta · Samarinda', year='2024', img='antrian-poliklinik.webp',
         desc='Alur pendaftaran dan antrian yang membuat layanan klinik lebih tertata, dengan display operasional.',
         lead='Alur pendaftaran dan antrian yang membantu operasional layanan klinik lebih tertata.',
         about='Untuk klinik dan rumah sakit swasta di Samarinda: pasien mendaftar dan mengambil nomor antrean, layar display memanggil sesuai poli, dan petugas melihat alur layanan dari meja masing-masing.',
         feats=[('Manajemen antrian', 'Nomor antrean per poli.'), ('Alur pendaftaran', 'Pendaftaran pasien lebih cepat.'),
                ('Display operasional', 'Layar panggilan di ruang tunggu.'), ('Workflow layanan', 'Status pasien terlihat petugas.')],
         tags=['Web', 'Antrian', 'EMR'], svc='software'),
    dict(slug='lentera-koperasi', group='software', title='Lentera: penilaian kesehatan keuangan koperasi', client='BPR & koperasi · Kaltim', year='2023', img='lentera-koperasi.webp',
         desc='Platform web dan mobile untuk membaca indikator dan kondisi keuangan koperasi secara terstruktur, dengan monitoring dan pelaporan.',
         lead='Platform untuk membaca indikator dan kondisi keuangan koperasi secara terstruktur.',
         about='Lentera membantu BPR dan koperasi di Kalimantan Timur menilai kesehatan keuangan. Indikator dihitung dari data keuangan, kondisinya dipantau berkala, dan hasilnya disusun menjadi laporan, dari web maupun aplikasi mobile.',
         feats=[('Indikator keuangan', 'Rasio dihitung otomatis.'), ('Monitoring', 'Kondisi dipantau berkala.'),
                ('Pelaporan', 'Laporan penilaian siap cetak.'), ('Platform web', 'Juga tersedia di aplikasi mobile.')],
         tags=['Web', 'Keuangan', 'Mobile'], svc='software'),
    # ── Website ──
    dict(slug='website-feb-unmul', group='web', title='Website dan sistem informasi fakultas', client='Fakultas Ekonomi dan Bisnis Universitas Mulawarman', year='2024', img='website-feb-unmul.webp',
         desc='Platform informasi fakultas dengan arsitektur informasi yang jelas, tampilan responsif, dan alur editorial untuk pengelolaan konten.',
         lead='Platform informasi yang disusun agar konten fakultas dapat dikelola secara terstruktur.',
         about='Website dan sistem informasi Fakultas Ekonomi dan Bisnis Universitas Mulawarman. Informasi jurusan, berita, dan layanan disusun dalam arsitektur yang jelas, tampil baik di HP, dan dikelola tim fakultas lewat alur editorial di CMS.',
         feats=[('Content management', 'Konten dikelola tim fakultas.'), ('Arsitektur informasi', 'Jurusan dan layanan mudah ditemukan.'),
                ('Responsive web', 'Nyaman dibuka dari HP.'), ('Alur editorial', 'Tulis, tinjau, lalu terbitkan.')],
         tags=['Web', 'CMS'], svc='website', link=('https://feb.unmul.ac.id', 'Buka situs fakultas'), pos='left top'),
    dict(slug='website-farmasi-unmul', group='web', title='Website resmi fakultas', client='Fakultas Farmasi Universitas Mulawarman', year='2023', img='website-farmasi-unmul.webp',
         desc='Website publik untuk struktur informasi, publikasi, dan pembaruan konten fakultas, dikelola lewat CMS.',
         lead='Website publik untuk struktur informasi, publikasi, dan pembaruan konten fakultas.',
         about='Website resmi Fakultas Farmasi Universitas Mulawarman: profil, publikasi, dan pengumuman disusun dalam struktur yang rapi dan diperbarui sendiri oleh tim fakultas lewat CMS.',
         feats=[('Website publik', 'Profil dan informasi fakultas.'), ('Konten terstruktur', 'Publikasi dan pengumuman tertata.'),
                ('CMS', 'Diperbarui sendiri oleh tim.'), ('Antarmuka responsif', 'Tampil baik di semua layar.')],
         tags=['Web', 'CMS'], svc='website', link=('https://ff.unmul.ac.id', 'Buka situs fakultas'), pos='center top'),
]
BY = {p['slug']: p for p in PROJECTS}

# Logo klien (sama dengan yang dipakai situs saudara; nama diambil dari atribut alt-nya).
CLIENTS = [('Pemkot Samarinda', 'samarinda.webp'), ('Diskominfosandi Kab. Barito Utara', 'barut.webp'), ('Universitas Mulawarman', 'unmul.webp'),
           ('Institut Teknologi Kalimantan', 'itk.webp'), ('STT Migas Balikpapan', 'sttmigas.webp'), ('PT Adhi Karya', 'adhi.webp'),
           ('PT Astra International Tbk', 'astra.webp'), ('RM Payakumbuah', 'payakumbuah.webp'), ('1Ci Enterprise', '1ci.webp'), ('MBC Entertainment', 'mbc.webp')]
CLIENT_NAMES = [n for n, _ in CLIENTS]

# Carousel beranda: proyek berscreenshot dulu, ilustrasi di akhir (urutan seperti situs saudara).
HOME_SLUGS = ['fleet-management-tambang', 'pompy-batara', 'dashboard-geospasial-dapodik', 'smart-attendance-unmul', 'smartlock-farmasi-unmul',
              'deteksi-apd-ai', 'hris-mobile-payroll', 'rm-payakumbuah', 'website-feb-unmul', 'website-farmasi-unmul', 'media-monitoring',
              'sentiment-social-listening', 'cctv-ai-farmasi-unmul', 'fleet-radio-kapal', 'transkripsi-rapat', 'antrian-poliklinik',
              'lentera-koperasi', 'iot-monitoring-lahan-sawit', 'optimasi-rute-armada', 'kios-mandiri-kelurahan', 'iot-monitoring-gudang']
INFRA_SLUGS = ['rm-payakumbuah', 'kios-mandiri-kelurahan', 'fleet-radio-kapal', 'iot-monitoring-gudang', 'deteksi-apd-ai', 'cctv-ai-farmasi-unmul',
               'smartlock-farmasi-unmul', 'iot-monitoring-lahan-sawit', 'fleet-management-tambang']


def short_title(p):
    return p['title'].split(':')[0]


def thumb(p, w=800, h=500, lazy=True, alt=''):
    pos = f' style="object-position:{p["pos"]}"' if p.get('pos') else ''
    ld = ' loading="lazy"' if lazy else ''
    return f'<img alt="{e(alt)}" decoding="async" height="{h}"{ld} src="{IMG}{e(p["img"])}"{pos} width="{w}"/>'


def card(p, mode='link'):
    """Kartu proyek: gambar 16:10, klien · tahun, judul, ringkasan, tag. Seluruh kartu menaut ke /portofolio/<slug>.
    mode 'full' = dipakai di /portofolio (data-kind untuk filter, id jangkar lama)."""
    meta = e(p['client']) + (f' · {e(p["year"])}' if p['year'] else '')
    tags = ''.join(f'<span class="pf-tag">{e(t)}</span>' for t in p['tags'])
    body = f'<span class="pf-body"><small>{meta}</small><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><span class="pf-tags">{tags}</span></span>'
    extra = f' data-kind="{p["group"]}" id="{p["slug"]}"' if mode == 'full' else ''
    return f'<a class="pf-card"{extra} href="/portofolio/{p["slug"]}"><span class="pf-thumb">{thumb(p)}</span>{body}</a>'


def shot(p, cls='pf-shot', lazy=True):
    """Kartu ringkas (gambar + klien + judul): baris unggulan /portofolio dan carousel beranda."""
    return (f'<a class="{cls}" href="/portofolio/{p["slug"]}"><span class="pf-shot-img">{thumb(p, lazy=lazy, alt=short_title(p))}</span>'
            f'<span class="cap"><small>{e(p["client"])}</small><b>{e(short_title(p))}</b></span></a>')
