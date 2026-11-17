"""Daerah layanan di luar Samarinda & Balikpapan (satu sumber untuk semua generator halaman lokal).
Isi per daerah harus faktual dan spesifik: kantor terdekat, sektor utama, dan kebutuhan yang umum di sana.
Jangan menulis klaim proyek/klien di daerah ini kecuali benar-benar ada."""

# office = kunci kantor terdekat di site_data.OFFICES; near = daerah tetangga untuk tautan internal
REGIONS = {
    'bontang': dict(name='Bontang', seat='Kota Bontang', office='samarinda', near=['samarinda', 'kutai-timur', 'kutai-kartanegara'],
        sectors='kawasan industri pupuk, petrokimia, dan LNG, pelabuhan, kontraktor, perkantoran, serta sekolah',
        needs=[
               ('Kawasan industri & kontraktor', 'Aplikasi pelaporan pekerjaan, approval, dan dashboard untuk tim lapangan.'),
               ('Vendor & logistik', 'Aplikasi pencatatan pengiriman dan laporan pekerjaan.'),
               ('Instansi & sekolah', 'Website resmi dan aplikasi administrasi.')]),
    'kutai-kartanegara': dict(name='Kutai Kartanegara', seat='Tenggarong', office='samarinda', near=['samarinda', 'bontang', 'kutai-barat'],
        sectors='pemerintahan kabupaten, tambang batu bara, migas, perkebunan sawit, dan UMKM',
        needs=[
               ('Pemerintah kabupaten & desa', 'Website instansi dan aplikasi pelayanan publik yang mudah dipakai warga.'),
               ('Tambang, migas & perkebunan', 'Aplikasi pelaporan lapangan yang tetap jalan saat sinyal lemah.'),
               ('Usaha & sekolah', 'Website yang muncul di Google dan aplikasi pencatatan.')]),
    'kutai-timur': dict(name='Kutai Timur', seat='Sangatta', office='samarinda', near=['bontang', 'berau', 'kutai-kartanegara'],
        sectors='tambang batu bara, perkebunan sawit, pelabuhan, dan pemerintahan kabupaten',
        needs=[
               ('Tambang & hauling', 'Aplikasi laporan produksi dan approval untuk tim lapangan.'),
               ('Perkebunan & site jauh', 'Aplikasi pencatatan kebun yang tetap berfungsi tanpa sinyal.'),
               ('Instansi & kantor', 'Website resmi dan aplikasi administrasi.')]),
    'kutai-barat': dict(name='Kutai Barat', seat='Sendawar', office='samarinda', near=['mahakam-ulu', 'kutai-kartanegara', 'samarinda'],
        sectors='tambang, perkebunan, pemerintahan kabupaten, dan wilayah pedalaman',
        needs=[
               ('Wilayah pedalaman', 'Aplikasi yang tetap jalan saat sinyal lemah dan menyinkronkan data saat terhubung.'),
               ('Tambang & perkebunan', 'Aplikasi pelaporan lapangan dan dashboard untuk kantor pusat.'),
               ('Instansi & sekolah', 'Website resmi dan aplikasi pelayanan.')]),
    'mahakam-ulu': dict(name='Mahakam Ulu', seat='Ujoh Bilang', office='samarinda', near=['kutai-barat', 'samarinda', 'kutai-kartanegara'],
        sectors='pemerintahan kabupaten, sekolah dan puskesmas, serta wilayah perbatasan dan pedalaman',
        needs=[
               ('Layanan publik daerah terpencil', 'Aplikasi layanan yang ringan dan tetap berfungsi dengan sinyal terbatas.'),
               ('Sekolah & puskesmas', 'Aplikasi pencatatan dan pelaporan yang sederhana.'),
               ('Pemerintah kabupaten', 'Website resmi dan portal informasi publik.')]),
    'berau': dict(name='Berau', seat='Tanjung Redeb', office='samarinda', near=['kutai-timur', 'bontang', 'samarinda'],
        sectors='tambang batu bara, perkebunan, pelabuhan, pariwisata, dan perikanan',
        needs=[
               ('Tambang & logistik', 'Aplikasi laporan pekerjaan, approval, dan dashboard.'),
               ('Pariwisata & perikanan', 'Website promosi dan aplikasi pemesanan atau pencatatan.'),
               ('Instansi', 'Website resmi dan aplikasi pelayanan.')]),
    'paser': dict(name='Paser', seat='Tana Paser', office='balikpapan-utara', near=['balikpapan', 'penajam-paser-utara', 'samarinda'],
        sectors='perkebunan sawit, tambang batu bara, dan pemerintahan kabupaten',
        needs=[
               ('Perkebunan & pabrik', 'Aplikasi pencatatan lapangan dan laporan produksi.'),
               ('Tambang & armada', 'Aplikasi laporan pengiriman dan dashboard untuk kantor.'),
               ('Instansi & sekolah', 'Website resmi dan aplikasi administrasi.')]),
    'penajam-paser-utara': dict(name='Penajam Paser Utara', seat='Penajam', office='balikpapan-utara', near=['balikpapan', 'ikn', 'paser'],
        sectors='pembangunan kawasan IKN, kontraktor, logistik, perkebunan, dan pemerintahan kabupaten',
        needs=[
               ('Kontraktor & proyek konstruksi', 'Aplikasi laporan harian proyek, approval, dan dokumen.'),
               ('Logistik & perkebunan', 'Aplikasi pencatatan pengiriman dan laporan lapangan.'),
               ('Instansi & kantor baru', 'Website resmi dan aplikasi pelayanan.')]),
    'ikn': dict(name='IKN Nusantara', seat='Ibu Kota Nusantara', office='balikpapan-utara', near=['penajam-paser-utara', 'balikpapan', 'kutai-kartanegara'],
        sectors='pembangunan Ibu Kota Nusantara: kontraktor, instansi, perkantoran, dan hunian baru',
        needs=[
               ('Kontraktor & proyek', 'Aplikasi laporan proyek, approval, dan dokumen kerja.'),
               ('Gedung & perkantoran baru', 'Website perusahaan dan aplikasi internal untuk kantor baru.'),
               ('Instansi', 'Website resmi dan aplikasi layanan.')]),
}
