"""Halaman detail per aplikasi Altora: /produk/<id>.
Jalankan lewat scripts/build_all.sh (atau: python3 scripts/build_apps.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py)."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
P = '/assets/img/portfolio/'

# status: ready = siap dipakai, custom = implementasi sesuai kebutuhan
APPS = {
    'vision': dict(name='Altora Vision', tag='AI CCTV & Safety Analytics', status='ready', tone='green',
        lead='CCTV yang ikut mengawasi: mendeteksi pekerja tanpa APD, orang masuk zona terlarang, dan menghitung pengunjung, lalu langsung mengirim alert.',
        pains=['Pengawas tidak bisa memantau semua titik sepanjang hari.', 'Pelanggaran APD baru ketahuan setelah ada insiden.', 'Rekaman CCTV hanya dibuka setelah kejadian.'],
        feats=[('Deteksi APD', 'Helm, rompi, sepatu, dan safety belt terdeteksi otomatis per titik kamera.'),
               ('Zona terlarang', 'Alert saat orang atau kendaraan masuk area berbahaya.'),
               ('People & vehicle counting', 'Hitung orang dan kendaraan untuk analitik area.'),
               ('Alert real-time', 'Notifikasi ke dashboard dan HP lengkap dengan foto kejadian.'),
               ('Rekap pelanggaran', 'Laporan harian dan mingguan per area dan per shift.'),
               ('Pakai CCTV lama', 'Kamera yang kompatibel bisa dipakai, tanpa ganti semua perangkat.')],
        steps=['Survei titik kamera dan area rawan', 'Pasang atau sambungkan kamera ke server AI', 'Atur aturan deteksi per area', 'Tim menerima alert dan rekap otomatis'],
        hw=[('/katalog-cctv-vigi', 'Kamera CCTV VIGI'), ('/katalog#vigi-nvr', 'NVR'), ('/jual-cctv-samarinda', 'Jual CCTV Samarinda'), ('/jual-cctv-balikpapan', 'Jual CCTV Balikpapan')],
        shots=[(P + 'safety.jpg', 'Deteksi APD dari CCTV'), ('/assets/img/extra/projects/safety.jpg', 'Dashboard pelanggaran'), (P + 'unmul-infrastructure/vigi-cctv-monitoring.png', 'Monitoring CCTV terpusat')],
        who=['Tambang & konstruksi', 'Pabrik & gudang', 'Area publik & kampus'],
        faq=[('Apakah bisa memakai CCTV yang sudah ada?', 'Sering bisa, tergantung resolusi, sudut, dan pencahayaan kamera. Kami cek saat survei.'),
             ('Deteksi apa saja yang tersedia?', 'APD (helm, rompi, sepatu, safety belt), zona terlarang, penghitungan orang dan kendaraan. Deteksi lain bisa dikembangkan sesuai kebutuhan.'),
             ('Di mana data dan rekaman disimpan?', 'Di server Anda sendiri atau cloud pilihan Anda, sesuai kebijakan perusahaan.')],
        proof=[('/portfolio/ai-safety-vision', 'Deteksi APD dari CCTV'), ('/portfolio/instalasi-cctv-ai-analytics', 'Instalasi CCTV AI Analytics')]),
    'teams': dict(name='Altora Teams', tag='HRIS & People Operations', status='ready', tone='purple',
        lead='Satu aplikasi untuk absensi, shift, cuti, lembur, reimbursement, KPI, dan payroll. Karyawan pakai dari HP, HR memantau dari dashboard.',
        pains=['Rekap absensi dan lembur masih manual di spreadsheet.', 'Pengajuan cuti tercecer di chat.', 'Payroll lama karena data dari banyak sumber.'],
        feats=[('Absensi GPS & selfie', 'Absen dari HP dengan validasi lokasi dan foto.'), ('Shift & jadwal', 'Atur shift dan rotasi otomatis.'),
               ('Cuti, izin, lembur', 'Pengajuan dan persetujuan dari aplikasi.'), ('Reimbursement', 'Pengajuan klaim pengeluaran dengan foto bukti.'),
               ('KPI & kalender kerja', 'Target, penilaian, dan kalender tim.'), ('Payroll & slip gaji', 'Gaji dihitung dari data kehadiran, slip digital.')],
        steps=['Impor data karyawan dan struktur', 'Atur aturan absensi, shift, dan cuti', 'Karyawan mulai absen dari HP', 'HR menarik rekap dan payroll'],
        hw=[('/produk/attendance', 'Absensi wajah dari CCTV'), ('/jual-smartlock-samarinda', 'Smartlock & akses pintu')],
        shots=[(P + 'altora-teams-kpi-analytics.jpg', 'Analitik KPI'), (P + 'altora-teams-work-calendar.jpg', 'Kalender kerja'), (P + 'hris.jpg', 'Aplikasi karyawan')],
        who=['Perusahaan multi-lokasi', 'Instansi & kampus', 'Kontraktor dengan tim lapangan'],
        faq=[('Apakah bisa untuk karyawan lapangan?', 'Bisa. Absensi memakai GPS dan foto dari HP, cocok untuk tim lapangan.'),
             ('Apakah terhubung ke mesin absensi atau CCTV?', 'Bisa, termasuk absensi wajah dari CCTV lewat Altora Smart Attendance.'),
             ('Apakah data bisa diekspor ke payroll lain?', 'Bisa. Laporan bisa diunduh atau disambungkan ke sistem lain.')],
        proof=[('/portfolio/altora-teams', 'Altora Teams'), ('/portfolio/hris-mobile-payroll', 'HRIS mobile & payroll')]),
    'attendance': dict(name='Altora Smart Attendance', tag='Absensi wajah dari CCTV', status='ready', tone='pink',
        lead='Absensi otomatis dengan face recognition dari kamera CCTV. Karyawan cukup lewat di depan kamera, tanpa antre di mesin.',
        pains=['Antre di mesin fingerprint saat jam masuk.', 'Titip absen dan kartu dipinjam.', 'Data absensi harus direkap ulang untuk HR.'],
        feats=[('Face recognition', 'Wajah dikenali dari kamera di pintu masuk.'), ('Check-in otomatis', 'Waktu masuk dan pulang tercatat sendiri.'),
               ('Anti titip absen', 'Hanya wajah terdaftar yang tercatat.'), ('Terhubung HRIS', 'Data langsung masuk ke Altora Teams.'),
               ('Audit log', 'Riwayat kehadiran dengan foto bukti.'), ('Akses gedung', 'Bisa sekaligus membuka pintu lewat smartlock.')],
        steps=['Pasang kamera di titik masuk', 'Daftarkan wajah karyawan', 'Absensi berjalan otomatis', 'Rekap masuk ke HRIS'],
        hw=[('/katalog-cctv-vigi#dome', 'Kamera dome VIGI'), ('/absensi-face-recognition-samarinda', 'Absensi wajah Samarinda'), ('/absensi-face-recognition-balikpapan', 'Absensi wajah Balikpapan')],
        shots=[(P + 'attendance.jpg', 'Absensi wajah'), (P + 'unmul-infrastructure/sosialisasi-absensi-ai-cctv.png', 'Sosialisasi absensi AI di kampus')],
        who=['Kantor & pabrik', 'Kampus & sekolah', 'Instansi'],
        faq=[('Bagaimana kalau pencahayaan kurang?', 'Posisi kamera dan pencahayaan kami atur saat pemasangan supaya wajah terbaca.'),
             ('Apakah bisa untuk ratusan karyawan?', 'Bisa. Kapasitas server disesuaikan dengan jumlah karyawan dan titik kamera.'),
             ('Bagaimana keamanan data wajah?', 'Data disimpan di server yang disepakati dan aksesnya dibatasi per peran.')],
        proof=[('/portfolio/smart-attendance', 'Absensi wajah dari CCTV')]),
    'fms': dict(name='Altora FMS', tag='Fleet Management System', status='ready', tone='orange',
        lead='Pantau armada dari truk logistik sampai alat berat tambang: posisi, ritase, BBM, data mesin, dan perilaku pengemudi dalam satu dashboard.',
        pains=['Tidak tahu posisi dan aktivitas unit secara langsung.', 'Konsumsi BBM sulit dikontrol, rawan pencurian.', 'Laporan ritase dan jam operasi masih manual.'],
        feats=[('Live GPS & geofence', 'Posisi, rute, dan alert saat keluar area.'), ('BBM & fuel sensor', 'Konsumsi per liter dan alert pencurian.'),
               ('Data mesin (CAN-Bus)', 'RPM, hour meter, suhu, dan tekanan oli.'), ('TPMS', 'Tekanan dan suhu ban.'),
               ('Kamera & ADAS', 'Dashcam, deteksi kantuk, dan peringatan tabrakan.'), ('Laporan otomatis', 'Ritase, BBM, dan pelanggaran dikirim ke email.')],
        steps=['Pilih perangkat per tipe kendaraan', 'Pasang tracker dan sensor', 'Atur geofence dan aturan alert', 'Pantau dan terima laporan otomatis'],
        hw=[('/katalog#telt-fmc920', 'GPS tracker Teltonika'), ('/katalog#fms-sensors', 'Sensor CAN, BBM & TPMS'), ('/gps-tracker-kendaraan-balikpapan', 'GPS tracker Balikpapan'), ('/gps-tracker-kendaraan-samarinda', 'GPS tracker Samarinda')],
        shots=[(P + 'fms.jpg', 'Dashboard armada'), (P + 'logistik.jpg', 'Optimasi rute')],
        who=['Tambang & hauling', 'Logistik', 'Kontraktor & rental alat berat'],
        faq=[('Perangkat apa yang dipakai?', 'Teltonika, standar Eropa, tahan getar dan debu, dual-SIM.'),
             ('Bagaimana di area tanpa sinyal?', 'Data disimpan di perangkat dan dikirim saat sinyal kembali.'),
             ('Bisa terhubung ke ERP?', 'Bisa, termasuk data BBM dan jam kerja untuk payroll operator.')],
        proof=[('/portfolio/fleet-management', 'Fleet management armada hauling'), ('/portfolio/optimasi-rute-armada', 'Optimasi rute & armada')]),
    'pass': dict(name='Altora Pass', tag='Smart Access & Gate Control', status='ready', tone='blue',
        lead='Akses pintu digital untuk kantor, kampus, dan gudang: smartlock, kartu, wajah, dan aplikasi, semua pintu dikelola dari satu tempat.',
        pains=['Kunci fisik hilang atau digandakan.', 'Tidak tahu siapa masuk ruangan penting.', 'Akses tamu dan vendor sulit diatur.'],
        feats=[('Smartlock & EM lock', 'Untuk pintu kayu, aluminium, kaca, dan gerbang.'), ('Banyak cara buka', 'Aplikasi, PIN, kartu RFID, sidik jari, wajah 3D.'),
               ('Hak akses bertingkat', 'Atur siapa boleh masuk ke ruangan mana dan kapan.'), ('Akses tamu', 'Akses sementara dengan batas waktu.'),
               ('Riwayat akses', 'Log keluar-masuk lengkap.'), ('Integrasi', 'Terhubung ke absensi dan CCTV.')],
        steps=['Survei pintu dan alur keluar-masuk', 'Pasang kunci dan perangkat akses', 'Atur pengguna dan hak akses', 'Pantau riwayat dari aplikasi'],
        hw=[('/katalog#smartlock', 'Smartlock'), ('/jual-smartlock-samarinda', 'Smartlock Samarinda'), ('/jual-smartlock-balikpapan', 'Smartlock Balikpapan')],
        shots=[(P + 'smartlock.jpg', 'Aplikasi akses pintu'), ('/assets/img/extra/products/smartlock.jpg', 'Smartlock')],
        who=['Kantor', 'Kampus & asrama', 'Gudang & ruang server'],
        faq=[('Bagaimana kalau listrik padam?', 'Tersedia baterai cadangan dan kunci darurat sesuai tipe.'),
             ('Bisa untuk banyak gedung?', 'Bisa. Semua pintu dikelola dari satu aplikasi.'),
             ('Bisa terhubung ke absensi?', 'Bisa, akses pintu bisa sekaligus mencatat kehadiran.')],
        proof=[('/portfolio/smartlock-akses-digital', 'Smartlock & akses digital')]),
    'sense': dict(name='Altora Sense', tag='IoT Monitoring & Safety Sensors', status='ready', tone='cyan',
        lead='Sensor asap, api, suhu, kelembapan, dan kondisi lapangan yang mengirim alert ke tim saat ada yang tidak normal.',
        pains=['Kebakaran atau panas berlebih di ruang server terlambat diketahui.', 'Kondisi gudang dan lapangan tidak terpantau.', 'Alarm lokal tidak terdengar saat tidak ada orang.'],
        feats=[('Asap & api', 'Deteksi dini dan alert ke HP.'), ('Suhu & kelembapan', 'Untuk ruang server, gudang, dan cold storage.'),
               ('Status perangkat', 'Baterai dan koneksi sensor terpantau.'), ('Gateway', 'Sensor terhubung ke internet lewat gateway.'),
               ('Dashboard', 'Semua sensor dalam satu tampilan.'), ('Riwayat data', 'Grafik untuk analisis dan audit.')],
        steps=['Tentukan titik dan jenis sensor', 'Pasang sensor dan gateway', 'Atur ambang batas alert', 'Tim menerima alert otomatis'],
        hw=[('/produk/command', 'Altora Command'), ('/rak-server-samarinda', 'Rak server & ruang server')],
        shots=[(P + 'agri.jpg', 'Sensor lapangan')],
        who=['Ruang server & data center', 'Gudang', 'Pabrik & fasilitas'],
        faq=[('Sensor terhubung lewat apa?', 'Lewat gateway ke jaringan kantor, 4G, atau Starlink untuk lokasi terpencil.'),
             ('Bisa disambung ke sistem lain?', 'Bisa, termasuk ke Altora Command atau dashboard yang sudah ada.')],
        proof=[('/portfolio/iot-monitoring-lahan', 'IoT monitoring lahan')]),
    'farming': dict(name='Altora Smart Farming', tag='IoT Monitoring Lahan Pertanian', status='ready', tone='green',
        lead='Kelembapan tanah, kondisi tanaman, suhu, dan kelembapan udara per petak, langsung di HP petugas lapangan.',
        pains=['Penyiraman dan pemupukan berdasarkan perkiraan.', 'Kondisi lahan baru diketahui saat petugas datang.', 'Catatan lapangan tercecer di kertas.'],
        feats=[('Kelembapan tanah', 'Per petak, real-time.'), ('Suhu & udara', 'Kondisi mikro-iklim lahan.'), ('Status tanaman', 'Catatan kondisi dan foto.'),
               ('Field check', 'Catatan petugas dari HP.'), ('Alert', 'Peringatan saat kondisi di luar batas.'), ('Laporan', 'Riwayat per petak dan musim.')],
        steps=['Bagi lahan per petak', 'Pasang sensor dan gateway', 'Petugas memakai aplikasi', 'Analisis data per musim'],
        hw=[('/cctv-tenaga-surya-samarinda', 'Perangkat tenaga surya'), ('/jual-starlink-samarinda', 'Starlink untuk lahan terpencil')],
        shots=[('/assets/img/portfolio/smart-farming.webp', 'Aplikasi smart farming'), (P + 'agri.jpg', 'Sensor lahan')],
        who=['Perkebunan', 'Pertanian & hortikultura', 'Riset agrikultur'],
        faq=[('Bagaimana kalau lahan tidak ada sinyal?', 'Gateway bisa memakai Starlink atau koneksi jarak jauh lain, dengan tenaga surya.')],
        proof=[('/portfolio/iot-monitoring-lahan', 'IoT monitoring lahan')]),
    'command': dict(name='Altora Command', tag='Command Center & Operations Monitoring', status='ready', tone='purple',
        lead='Satu ruang kendali untuk CCTV AI, armada, sensor, dan status perangkat, dengan video wall dan alur penanganan insiden.',
        pains=['Data operasional tersebar di banyak aplikasi.', 'Insiden terlambat ditangani.', 'Pimpinan tidak punya gambaran situasi saat ini.'],
        feats=[('Tampilan terpadu', 'CCTV, peta armada, dan sensor dalam satu layar.'), ('Video wall', 'Dengan decoder dan layar besar.'),
               ('Manajemen insiden', 'Alert, penugasan, dan status penanganan.'), ('Integrasi', 'Menyambungkan sistem yang sudah ada.'),
               ('Dashboard pimpinan', 'Ringkasan operasional harian.'), ('Akses bertingkat', 'Operator, supervisor, dan pimpinan.')],
        steps=['Petakan sistem dan data yang ada', 'Rancang tampilan ruang kendali', 'Integrasi dan pemasangan video wall', 'Pelatihan operator'],
        hw=[('/katalog-cctv-vigi#nvd', 'Video decoder & video wall'), ('/videotron-samarinda', 'Videotron & LED display'), ('/produk/vision', 'Altora Vision')],
        shots=[(P + 'unmul-infrastructure/vigi-cctv-monitoring.png', 'Monitoring CCTV terpusat'), (P + 'barito-dash.jpg', 'Dashboard wilayah')],
        who=['Tambang & industri', 'Pemerintahan', 'Kampus & kawasan'],
        faq=[('Apakah harus mengganti sistem yang sudah ada?', 'Tidak. Command center dirancang untuk menyambungkan sistem yang sudah berjalan.')],
        proof=[('/portfolio/portal-one-map', 'Portal One Map'), ('/portfolio/instalasi-cctv-ai-analytics', 'Instalasi CCTV AI')]),
    'private-ai': dict(name='Altora Private AI & GIS', tag='AI on-premise & peta data spasial', status='ready', tone='blue',
        lead='Asisten AI yang berjalan di server Anda sendiri, tanpa mengirim data ke cloud publik, dilengkapi GIS untuk memetakan dan menganalisis data wilayah.',
        pains=['Data sensitif tidak boleh dikirim ke layanan AI publik.', 'Data wilayah tersebar di banyak dinas.', 'Analisis dokumen internal memakan waktu.'],
        feats=[('LLM on-premise', 'Model bahasa berjalan di server Anda, termasuk air-gapped.'), ('Multi-agen', 'Beberapa agen AI menyelesaikan tugas kompleks.'),
               ('Baca data internal', 'Dokumen dan database yang sudah ada.'), ('GIS terpusat', 'Peta dan analisis data spasial.'),
               ('Enkripsi & backup', 'Keamanan enterprise dan disaster recovery.'), ('Pelatihan tim', 'Admin dan pengguna dilatih sampai mandiri.')],
        steps=['Petakan data dan kebutuhan', 'Siapkan server dan model', 'Integrasi data internal & GIS', 'Pelatihan dan pendampingan'],
        hw=[('/rak-server-samarinda', 'Rak server & data center'), ('/katalog#hde-aio-il24', 'Komputer kerja')],
        shots=[('/assets/img/produk/private-ai.webp', 'Server on-premise'), (P + 'barito-dash.jpg', 'Dashboard GIS')],
        who=['Pemerintahan daerah', 'Keuangan & kesehatan', 'Tambang & energi'],
        faq=[('Apakah data keluar dari server kami?', 'Tidak. Proses AI berjalan di server Anda, bisa tanpa koneksi internet publik.'),
             ('Apa contoh pemakaian GIS?', 'Pemetaan sarana transportasi dan kebijakan satu peta, seperti yang kami bangun untuk Barito Utara.')],
        proof=[('/portfolio/portal-one-map', 'Portal One Map Policy'), ('/portfolio/dashboard-geospasial-dapodik', 'Dashboard geospasial')]),
    'word': dict(name='Altora Word', tag='Pengolah dokumen privat', status='ready', tone='blue',
        lead='Menulis dan menyunting surat, laporan, dan kontrak di browser, dengan dokumen yang tersimpan di server atau cloud milik organisasi Anda sendiri, bukan di layanan publik.',
        pains=['Dokumen rahasia tersimpan di layanan cloud milik pihak lain.', 'File Word berpindah-pindah lewat email dan chat, versinya membingungkan.', 'Lisensi aplikasi perkantoran per pengguna terus bertambah.'],
        feats=[('Format Word', 'Membuka dan menyimpan dokumen .docx, serta ekspor ke PDF.'), ('Di server Anda', 'Berjalan di server kantor atau cloud pilihan organisasi Anda.'),
               ('Komentar & revisi', 'Rekan kerja memberi catatan langsung di dokumen.'), ('Template', 'Kop surat, nota dinas, dan format laporan yang seragam.'),
               ('Dari browser', 'Tanpa instal aplikasi di setiap komputer.'), ('Terhubung Altora Docs', 'Dokumen tersimpan rapi dengan hak akses per folder.')],
        steps=['Tentukan server atau cloud tempat data disimpan', 'Kami pasang dan konfigurasi', 'Impor dokumen dan template yang ada', 'Pelatihan pengguna'],
        hw=[('/produk/docs', 'Altora Docs'), ('/produk/sheets', 'Altora Sheets'), ('/produk/meet', 'Altora Meet'), ('/rak-server-samarinda', 'Server & rak')],
        shots=[('/assets/img/produk/word.webp', 'Ilustrasi tampilan Altora Word')],
        who=['Instansi pemerintah', 'Perusahaan dengan data sensitif', 'Kampus & sekolah'],
        faq=[('Di mana dokumen disimpan?', 'Di server atau cloud milik organisasi Anda sendiri. Kami bantu memasang dan merawatnya.'),
             ('Apakah bisa membuka file Word yang sudah ada?', 'Bisa. Dokumen .docx dibuka dan disimpan kembali dalam format yang sama.'),
             ('Seperti apa tampilannya?', 'Kami tunjukkan langsung saat demo, termasuk cara kerja bersama dan pengaturan aksesnya.')],
        proof=[]),
    'docs': dict(name='Altora Docs', tag='Penyimpanan & berbagi dokumen privat', status='ready', tone='purple',
        lead='Tempat menyimpan, mencari, dan berbagi dokumen kantor dengan hak akses per orang dan per folder, di server atau cloud milik organisasi Anda sendiri.',
        pains=['Dokumen tersebar di laptop, flashdisk, dan grup chat.', 'Tidak jelas siapa yang boleh membuka dokumen penting.', 'Versi terbaru sulit ditemukan.'],
        feats=[('Folder & pencarian', 'Semua dokumen di satu tempat, mudah dicari.'), ('Hak akses', 'Atur siapa bisa melihat atau mengubah, per orang dan per folder.'),
               ('Riwayat versi', 'Versi lama tersimpan dan bisa dikembalikan.'), ('Berbagi internal', 'Bagikan dokumen ke rekan atau divisi tanpa kirim file.'),
               ('Di server Anda', 'Data tidak berpindah ke layanan cloud publik.'), ('Terhubung Word & Sheets', 'Buka dan sunting dokumen langsung dari Altora Docs.')],
        steps=['Petakan struktur folder dan hak akses', 'Pasang di server atau cloud Anda', 'Pindahkan dokumen yang ada', 'Pelatihan pengguna dan admin'],
        hw=[('/produk/word', 'Altora Word'), ('/produk/sheets', 'Altora Sheets'), ('/produk/private-ai', 'Altora Private AI'), ('/rak-server-samarinda', 'Server & rak')],
        shots=[('/assets/img/produk/docs.webp', 'Ilustrasi tampilan Altora Docs')],
        who=['Instansi & dinas', 'Perusahaan multi-divisi', 'Kampus & yayasan'],
        faq=[('Apa bedanya dengan menyimpan di cloud publik?', 'Dokumen tersimpan di server atau cloud milik organisasi Anda, dan aksesnya diatur oleh admin Anda sendiri.'),
             ('Apakah dokumen lama bisa dipindahkan?', 'Bisa. Kami bantu memindahkan dokumen dan menyusun ulang strukturnya.'),
             ('Bisakah dipakai bersama Altora Private AI?', 'Bisa. Dokumen internal dapat menjadi sumber jawaban asisten AI yang juga berjalan di server Anda.')],
        proof=[]),
    'sheets': dict(name='Altora Sheets', tag='Spreadsheet privat', status='ready', tone='green',
        lead='Spreadsheet untuk rekap, anggaran, dan laporan yang bisa disunting bersama, dengan data yang tetap di server atau cloud milik organisasi Anda sendiri.',
        pains=['File Excel dikirim bolak-balik dan angkanya berbeda-beda.', 'Data keuangan dan SDM tersimpan di layanan pihak lain.', 'Rekap gabungan antar cabang memakan waktu.'],
        feats=[('Format Excel', 'Membuka dan menyimpan file .xlsx.'), ('Rumus & grafik', 'Rumus umum, filter, dan grafik untuk laporan.'),
               ('Edit bersama', 'Beberapa orang mengisi satu file yang sama.'), ('Hak akses', 'Batasi siapa yang bisa melihat atau mengubah.'),
               ('Di server Anda', 'Angka penting tidak keluar dari infrastruktur Anda.'), ('Terhubung Altora Docs', 'File tersimpan rapi dengan riwayat versi.')],
        steps=['Tentukan server atau cloud tempat data disimpan', 'Kami pasang dan konfigurasi', 'Impor file yang ada', 'Pelatihan pengguna'],
        hw=[('/produk/docs', 'Altora Docs'), ('/produk/word', 'Altora Word'), ('/produk/erp', 'Altora ERP')],
        shots=[('/assets/img/produk/sheets.webp', 'Ilustrasi tampilan Altora Sheets')],
        who=['Keuangan & administrasi', 'Instansi', 'Usaha multi-cabang'],
        faq=[('Apakah bisa membuka file Excel?', 'Bisa. File .xlsx dibuka dan disimpan kembali dalam format yang sama.'),
             ('Apakah bisa diisi beberapa orang sekaligus?', 'Bisa, dengan hak akses yang diatur per orang.'),
             ('Di mana data disimpan?', 'Di server atau cloud milik organisasi Anda sendiri.')],
        proof=[]),
    'meet': dict(name='Altora Meet', tag='Rapat video privat', status='ready', tone='pink',
        lead='Rapat video untuk kantor pusat, cabang, dan tim lapangan, berjalan di server atau cloud milik organisasi Anda sendiri, termasuk rekaman rapatnya.',
        pains=['Rapat internal yang sensitif berjalan di platform pihak lain.', 'Rekaman rapat tersimpan di luar organisasi.', 'Akun rapat dibagi-bagi tanpa kontrol.'],
        feats=[('Ruang rapat', 'Buat ruang rapat untuk tim, divisi, atau tamu.'), ('Berbagi layar', 'Presentasi dan dokumen tampil ke semua peserta.'),
               ('Chat rapat', 'Catatan dan tautan selama rapat berlangsung.'), ('Rekaman di server Anda', 'Rekaman rapat tidak tersimpan di layanan publik.'),
               ('Dari browser & HP', 'Peserta bergabung tanpa instal aplikasi khusus.'), ('Kontrol admin', 'Akses dan ruang rapat dikelola admin Anda.')],
        steps=['Tentukan server atau cloud dan kapasitas', 'Kami pasang dan konfigurasi', 'Uji coba rapat antar kantor', 'Pelatihan pengguna dan admin'],
        hw=[('/katalog#hde-mrs', 'Meeting recording system'), ('/interactive-flat-panel-samarinda', 'Interactive flat panel ruang rapat'), ('/produk/docs', 'Altora Docs')],
        shots=[('/assets/img/produk/meet.webp', 'Ilustrasi tampilan Altora Meet')],
        who=['Instansi & pemerintah daerah', 'Perusahaan dengan banyak cabang', 'Kampus'],
        faq=[('Apakah rekaman rapat keluar dari server kami?', 'Tidak. Rekaman tersimpan di server atau cloud milik organisasi Anda.'),
             ('Berapa peserta yang didukung?', 'Tergantung kapasitas server. Kami hitung bersama sesuai kebutuhan rapat Anda.'),
             ('Apakah tamu dari luar bisa ikut?', 'Bisa, lewat tautan rapat yang diatur admin.')],
        proof=[]),
    'pos': dict(name='Altora POS', tag='Point of Sale & Kasir', status='custom', tone='orange',
        lead='Kasir untuk retail dan F&B: pesanan cepat, stok real-time, QRIS, dan laporan penjualan multi-cabang. Diterapkan mengikuti alur toko Anda.',
        pains=['Stok di kasir dan gudang tidak sama.', 'Laporan cabang dikirim manual.', 'Pembayaran QRIS dicatat terpisah.'],
        feats=[('Kasir cepat', 'Untuk retail dan F&B.'), ('Stok & varian', 'Sinkron dengan gudang.'), ('QRIS / EDC', 'Pembayaran tercatat otomatis.'),
               ('Multi-cabang', 'Satu dashboard untuk semua cabang.'), ('Member & promo', 'Program pelanggan.'), ('Laporan', 'Penjualan harian dan per produk.')],
        steps=['Pelajari alur toko', 'Konfigurasi produk dan cabang', 'Uji coba di satu outlet', 'Perluas ke cabang lain'],
        hw=[('/katalog#hde-aio-il24', 'PC all-in-one untuk kasir'), ('/mesin-kiosk-samarinda', 'Kios pesan mandiri')],
        shots=[('/assets/img/produk/pos.webp', 'Kasir')],
        who=['Retail', 'Kafe & restoran', 'Usaha multi-cabang'],
        faq=[('Apakah sudah bisa dipakai?', 'Diterapkan sebagai implementasi custom: modul kasir disesuaikan dengan alur toko Anda, mulai dari satu outlet.')],
        proof=[]),
    'erp': dict(name='Altora ERP', tag='Enterprise Resource Planning', status='custom', tone='blue',
        lead='Stok multi-gudang, purchasing, keuangan, dan dashboard eksekutif dalam satu sistem, disusun mengikuti proses perusahaan Anda.',
        pains=['Angka tiap divisi berbeda-beda.', 'Pembelian dan stok tidak terhubung.', 'Laporan keuangan menunggu rekap manual.'],
        feats=[('Stok multi-gudang', 'Transfer dan stok opname.'), ('Purchasing', 'PR, PO, dan portal supplier.'), ('Keuangan', 'Jurnal, hutang-piutang, laporan.'),
               ('Integrasi FMS & HRIS', 'Data armada dan karyawan tersambung.'), ('Dashboard eksekutif', 'Ringkasan untuk pimpinan.'), ('Hak akses', 'Per divisi dan jabatan.')],
        steps=['Analisis proses bisnis', 'Pilih modul prioritas', 'Implementasi bertahap per modul', 'Pelatihan dan pendampingan'],
        hw=[('/produk/fms', 'Integrasi dengan Altora FMS'), ('/produk/teams', 'Integrasi dengan Altora Teams')],
        shots=[('/assets/img/produk/erp.webp', 'Dashboard ERP')],
        who=['Distributor & logistik', 'Kontraktor & tambang', 'Perusahaan multi-cabang'],
        faq=[('Apakah ERP harus dipasang sekaligus?', 'Tidak. Kami sarankan mulai dari modul yang paling mendesak, lalu bertambah bertahap.')],
        proof=[]),
}


def page(key, a):
    url = f'/produk/{key}'
    title = f'{a["name"]} | {a["tag"]} | Altora Indonesia'
    if len(title) > 65:
        title = f'{a["name"]} | {a["tag"]}'
    desc = a['lead'][:158]
    badge = '<span class="ap-badge">Siap dipakai</span>' if a['status'] == 'ready' else '<span class="ap-badge ap-custom">Implementasi custom</span>'
    msg_demo = f'Halo Altora, saya ingin melihat demo {a["name"]}.'
    pains = ''.join(f'<li>{e(x)}</li>' for x in a['pains'])
    feats = ''.join(f'<article><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in a['feats'])
    steps = ''.join(f'<li><span>{i}</span>{e(s)}</li>' for i, s in enumerate(a['steps'], 1))
    shots = ''.join(f'<figure><img alt="{e(c)}" loading="lazy" src="{s}"/><figcaption>{e(c)}</figcaption></figure>' for s, c in a['shots'])
    hw = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in a['hw'])
    who = ''.join(f'<li>{e(w)}</li>' for w in a['who'])
    proof = ''.join(f'<a href="{u}">{e(t)} →</a>' for u, t in a['proof'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(x)}</p></details>' for q, x in a['faq'])
    others = ''.join(f'<a class="ap-other" href="/produk/{k}"><img alt="" loading="lazy" src="/assets/img/produk/{k}.webp"/><b>{e(o["name"])}</b><small>{e(o["tag"])}</small></a>'
                     for k, o in APPS.items() if k != key)
    cart = (f'<button class="cart-add" data-cart-id="{key}" data-cart-img="/assets/img/produk/{key}.webp" data-cart-meta="Aplikasi Altora" '
            f'data-cart-name="{e(a["name"])}" type="button"><span aria-hidden="true">+</span><span class="cart-add-label">Tambah ke keranjang</span></button>')
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'SoftwareApplication', 'name': a['name'], 'description': a['lead'], 'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Web, Android, iOS',
         'url': SITE + url, 'image': SITE + f'/assets/img/produk/{key}.webp', 'featureList': [t for t, _ in a['feats']],
         'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': SITE + '/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Produk', 'item': SITE + '/produk'},
            {'@type': 'ListItem', 'position': 3, 'name': a['name'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in a['faq']]}]}
    body = f'''<main class="ct-page ap-page ap-{a["tone"]}">
<section class="ap-hero"><div class="ct-wrap ap-hero-grid"><div>
<nav aria-label="Breadcrumb" class="vg-crumb"><a href="/">Beranda</a> / <a href="/produk">Produk</a> / <span>{e(a["name"])}</span></nav>
<p class="ap-tag">{e(a["tag"])} {badge}</p><h1>{e(a["name"])}</h1><p class="ct-lead">{e(a["lead"])}</p>
<div class="ap-actions"><a class="btn btn-purple" href="{WA}{quote(msg_demo)}" rel="noopener" target="_blank">Minta demo</a>{cart}</div></div>
<figure class="ap-hero-pic"><img alt="{e(a["name"])}" src="/assets/img/produk/{key}.webp"/></figure></div></section>
<section class="ap-sec"><div class="ct-wrap ap-two"><div><h2>Masalah yang diselesaikan</h2><ul class="ap-pains">{pains}</ul></div>
<div><h2>Cocok untuk</h2><ul class="ap-who">{who}</ul></div></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Fitur utama</h2><div class="ap-feats">{feats}</div></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Tampilan &amp; implementasi</h2><div class="ap-shots">{shots}</div></div></section>
<section class="ap-sec"><div class="ct-wrap ap-two"><div><h2>Cara mulai</h2><ol class="ap-steps">{steps}</ol></div>
<div><h2>Perangkat &amp; produk terkait</h2><div class="ap-links">{hw}</div>{f'<h2 class="ap-h2-sm">Bukti implementasi</h2><div class="ap-proof">{proof}</div>' if proof else ''}</div></div></section>
<section class="ap-sec"><div class="ct-wrap svd-faq"><h2>Pertanyaan umum</h2><div>{faq}</div></div></section>
<section class="ap-sec"><div class="ct-wrap"><h2>Aplikasi Altora lainnya</h2><div class="ap-others">{others}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Lihat {e(a["name"])} langsung</h2><p>Kami tunjukkan demo dan contoh pemakaiannya, gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg_demo)}" rel="noopener" target="_blank">Minta demo via WhatsApp</a></div></section>
</main>'''
    return url, shell(title, desc, url, SITE + f'/assets/img/produk/{key}.webp', ld, body)


if __name__ == '__main__':
    (root / 'produk').mkdir(exist_ok=True)
    urls = []
    for k, a in APPS.items():
        url, h = page(k, a)
        (root / (url.lstrip('/') + '.html')).write_text(h, encoding='utf-8')
        urls.append(url)
    update_sitemap(urls)
    print('halaman aplikasi:', len(urls))
