"""Bangun halaman lokal produk x kota (mis. /jual-smartlock-samarinda): jual, pengadaan, instalasi, maintenance.
Jalankan dari root repo:  python3 scripts/build_produk_kota.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py
Setiap halaman berisi daftar perangkat nyata dari katalog (catalog_data.py / foto VIGI), FAQ khusus produk,
dan bagian kota (kantor, proyek). Jangan menambah kota tanpa kantor/proyek nyata di sana."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, CITIES, PF, SITE, WA
from site_data import OFFICES, postal_address
from catalog_data import HW_ITEMS

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
HW = {h['id']: h for h in HW_ITEMS}


def hw(pid, n_specs=3):
    """Kartu dari katalog hardware: (id, nama, merek, gambar, [spesifikasi])."""
    h = HW[pid]
    img = f'/assets/img/hardware/{h["img"]}.webp' if h['img'] else ''
    return (h['id'], h['name'], h['brand'], img, [f'{k}: {v}' for k, v in h['specs'][:n_specs]])


def vigi(model, specs):
    slug = re.sub(r'[^a-z0-9]+', '-', model.lower()).strip('-')
    return (f'vigi-{slug}', f'VIGI {model}', 'VIGI', f'/assets/img/vigi/{slug}.webp', specs)


PRODUCTS = {
    'smartlock': dict(slug='jual-smartlock-{c}', short='Smartlock', h1='Jual & pasang smartlock di {C}',
        title='Jual & Pasang Smartlock {C} | Kunci Digital | Altora',
        desc='Jual dan pasang smartlock di {C}: kunci pintu digital untuk rumah, kantor, kampus, dan gudang. Buka dengan aplikasi, PIN, kartu, sidik jari, atau wajah.',
        lead='Kunci pintu digital untuk rumah, kantor, ruko, kampus, dan gudang di {C}. Kami bantu pilih tipe yang cocok dengan pintu Anda, pasang, atur aplikasinya, dan rawat setelahnya.',
        hero='/assets/img/portfolio/smartlock.jpg', main='/katalog#smartlock', main_label='Smartlock di katalog produk',
        items=[('smartlock-pintu', 'Smartlock pintu (handle & sliding)', 'Altora Pass', '/assets/img/extra/products/smartlock.jpg',
                ['Buka via aplikasi, PIN, kartu RFID, sidik jari', 'Untuk pintu kayu, aluminium, dan kaca geser', 'Kunci darurat (emergency key)']),
               ('smartlock-doorcam', 'Smartlock + kamera pintu', 'Altora Pass', '/assets/img/hardware/smartlock.webp',
                ['Wajah 3D dan kamera pintu', 'Notifikasi video ke HP', 'Riwayat keluar-masuk lengkap']),
               ('smartlock-em', 'Akses kantor (EM lock & solenoid)', 'Altora Pass', '',
                ['Dropbolt / EM lock untuk pintu kantor', 'Tombol keluar tanpa sentuh, auto relock', 'Kartu akses per karyawan'])],
        dos=[('Pilih tipe sesuai pintu', 'Kami cek jenis pintu, ketebalan, dan arah bukaan sebelum menentukan tipe kunci.'),
             ('Pemasangan rapi', 'Lubang, kabel, dan tombol keluar dipasang rapi tanpa merusak kusen.'),
             ('Atur aplikasi & pengguna', 'Akun admin, pengguna, kartu, dan akses tamu kami siapkan sampai siap dipakai.'),
             ('Integrasi absensi', 'Riwayat akses bisa disambungkan ke HRIS atau absensi Altora.'),
             ('Pengadaan jumlah banyak', 'Untuk kantor, kos, hotel, atau kampus dengan banyak pintu.'),
             ('Garansi & perawatan', 'Penggantian baterai, cek mekanik, dan bantuan teknis setelah terpasang.')],
        faq=[('Apakah smartlock bisa dipasang di pintu yang sudah ada?', 'Umumnya bisa. Kami cek ketebalan dan jenis pintu saat survei supaya tipe kuncinya pas.'),
             ('Kalau baterai habis bagaimana?', 'Aplikasi memberi peringatan sebelum baterai habis, dan tersedia kunci darurat atau port daya cadangan sesuai tipe.'),
             ('Bisa memberi akses sementara untuk tamu?', 'Bisa. Akses tamu dapat dibatasi waktu dari aplikasi.'),
             ('Apakah bisa untuk banyak pintu di kantor?', 'Bisa. Semua pintu dikelola dari satu aplikasi dengan hak akses per orang.')],
        proof=['smart-attendance']),
    'starlink': dict(slug='jual-starlink-{c}', short='Starlink', h1='Jual & pasang Starlink di {C}',
        title='Jual & Pasang Starlink {C} | Internet Satelit | Altora',
        desc='Jual dan pasang Starlink di {C}: kit V5, V4, Mini, Enterprise, dan Performance. Instalasi lengkap, Wi-Fi repeater, dan panel surya untuk lokasi tanpa PLN.',
        lead='Internet satelit Starlink untuk rumah, kantor, site proyek, tambang, kebun, dan kapal dari {C}. Kami bantu pilih kit, pasang mounting dan kabel, ratakan Wi-Fi, sampai siap dipakai.',
        hero='/assets/img/hardware/starlink-v5.webp', main='/services/starlink-internet-satelit', main_label='Layanan Starlink & internet satelit',
        items=[hw('starlink-v5'), hw('starlink-v4'), hw('starlink-mini'), hw('starlink-mini-x'), hw('starlink-enterprise'), hw('starlink-performance-3'), hw('starlink-performance-2')],
        dos=[('Pilih kit yang tepat', 'Rumah, kantor, kendaraan, atau site terpencil butuh kit yang berbeda. Kami bantu memilih.'),
             ('Survei titik pasang', 'Mencari posisi antena yang bebas halangan pohon dan bangunan.'),
             ('Mounting & kabel', 'Pipe mount, wall mount, atau tiang, dengan jalur kabel yang rapi.'),
             ('Wi-Fi merata', 'Tambahan router mesh atau repeater supaya sinyal sampai ke seluruh area.'),
             ('Off-grid tenaga surya', 'Panel surya dan baterai untuk lokasi tanpa listrik PLN.'),
             ('Aktivasi & pendampingan', 'Bantuan aktivasi, pengaturan aplikasi, dan dukungan teknis.')],
        faq=[('Kit Starlink mana yang cocok untuk kantor?', 'Untuk kantor biasa, Starlink V4 atau V5 cukup. Untuk lokasi bisnis yang butuh kabel panjang dan router sendiri, pilih Enterprise.'),
             ('Apakah bisa dipasang di lokasi tanpa listrik?', 'Bisa, dengan panel surya dan baterai. Kami hitung kapasitasnya sesuai pemakaian.'),
             ('Bisa dipakai di kendaraan atau kapal?', 'Bisa. Starlink Mini cocok untuk dibawa-bawa, sedangkan Performance untuk instalasi permanen di kendaraan dan kapal.'),
             ('Berapa kecepatannya?', 'Tergantung kit dan paket layanan. Kit Performance Gen 3 mampu download 400+ Mbps.')],
        proof=[]),
    'cctv': dict(slug='jual-cctv-{c}', short='Jual CCTV', h1='Jual CCTV VIGI di {C}',
        title='Jual CCTV {C} | Kamera VIGI, NVR & Pasang | Altora',
        desc='Jual CCTV di {C}: kamera VIGI dome, bullet, turret, pan tilt, 4G, NVR, dan paket CCTV. Pengadaan resmi, instalasi, dan garansi oleh tim Altora.',
        lead='Kamera CCTV VIGI by TP-Link, NVR, dan paket CCTV untuk rumah, toko, kantor, gudang, dan proyek di {C}. Beli putus atau sekalian dipasang dan dirawat oleh tim kami.',
        hero='/assets/img/vigi/s385dps.webp', main='/katalog-cctv-vigi', main_label='Katalog lengkap CCTV VIGI (148 model)',
        items=[vigi('S245', ['Dome 4 MP full-color', 'People & vehicle analytics', 'Untuk ruangan & lobi']),
               vigi('S345', ['Bullet 4 MP full-color', 'Outdoor, tahan cuaca', 'Untuk pagar & parkiran']),
               vigi('S445', ['Turret 4 MP full-color', 'Audio dua arah', 'Untuk teras & gudang']),
               vigi('C540', ['Pan tilt 4 MP, putar 360°', 'Auto tracking', 'Untuk halaman luas']),
               vigi('C540-4G', ['Pan tilt 4G (SIM)', 'Tanpa kabel internet', 'Untuk proyek & kebun']),
               vigi('S385DPS', ['Panoramic 8 MP dual-lens', 'ColorPro, malam tetap berwarna', 'Untuk area terbuka lebar']),
               vigi('NVR1008H-8MP', ['NVR 8 kanal', '8 port PoE+', 'Rekaman hingga 10 TB']),
               vigi('NVR2016H-16MP', ['NVR 16 kanal', '16 port PoE+', '2 HDD'])],
        dos=[('Pengadaan resmi', 'Kamera dan NVR VIGI resmi dengan garansi, untuk satuan maupun proyek.'),
             ('Hitung kebutuhan', 'Kirim denah atau foto lokasi, kami hitungkan jumlah kamera dan kapasitas rekaman.'),
             ('Paket siap pasang', 'Kamera, NVR, hard disk, kabel, dan instalasi dalam satu penawaran.'),
             ('Instalasi rapi', 'Tiang, bracket, junction box, dan jalur kabel yang rapi.'),
             ('Pantau dari HP', 'Aplikasi VIGI dan VMS kami atur sampai bisa dipantau dari HP.'),
             ('Perawatan berkala', 'Cek kamera, rekaman, dan firmware secara berkala.')],
        faq=[('Apakah bisa beli CCTV saja tanpa pasang?', 'Bisa. Kami juga melayani pembelian putus, termasuk untuk teknisi dan kontraktor.'),
             ('CCTV VIGI itu merek apa?', 'VIGI adalah lini CCTV profesional dari TP-Link, dengan kamera AI, NVR, dan aplikasi pemantauan.'),
             ('Kamera mana yang cocok untuk malam hari?', 'Untuk area gelap, pilih seri ColorPro (kode S) yang tetap berwarna di malam hari, atau seri IR (kode I).'),
             ('Apakah tersedia paket CCTV?', 'Tersedia paket NVR + kamera + hard disk, dan bisa disesuaikan jumlah titiknya.')],
        proof=['instalasi-cctv-ai-analytics', 'unmul-infrastruktur-cctv-jaringan']),
    'cctv-surya': dict(slug='cctv-tenaga-surya-{c}', short='CCTV tenaga surya', h1='CCTV tenaga surya & 4G di {C}',
        title='CCTV Tenaga Surya {C} | Solar Panel & 4G | Altora',
        desc='CCTV tenaga surya dan 4G di {C} untuk proyek, kebun, tambak, tambang, dan area tanpa listrik. Paket panel surya VIGI, kamera 4G, dan instalasi.',
        lead='Untuk lokasi yang tidak ada listrik atau kabel internet di sekitar {C}: area proyek, kebun, tambak, gudang terpencil, dan jalan tambang. Kamera hidup dari panel surya dan terhubung lewat 4G.',
        hero='/assets/img/hardware/vigi-solar.webp', main='/katalog-cctv-vigi#solar', main_label='Sistem solar VIGI di katalog',
        items=[vigi('SP9030', ['Panel surya 90 W', 'Baterai lithium 31,2 Ah', 'IP66, dipantau dari aplikasi']),
               vigi('SP6030', ['Panel surya 60 W', 'Baterai lithium 31,2 Ah', 'IP66']),
               vigi('SP6020', ['Panel surya 60 W', 'Baterai lithium 20,8 Ah', 'IP66']),
               vigi('C540-4G', ['Pan tilt 4G (SIM)', 'Bisa jadi router untuk perangkat lain', 'Full-color']),
               vigi('S345-4G', ['Bullet 4 MP 4G', 'Full-color', 'Outdoor']),
               vigi('PS30', ['Solar controller', 'Untuk sistem solar custom', 'Pantau dari aplikasi'])],
        dos=[('Survei lokasi', 'Cek arah matahari, sinyal 4G, dan titik pandang kamera.'),
             ('Hitung daya', 'Kapasitas panel dan baterai disesuaikan jumlah kamera dan lama cuaca mendung.'),
             ('Tiang & mounting', 'Tiang, bracket, dan grounding yang kuat untuk area terbuka.'),
             ('Koneksi 4G atau Starlink', 'Pakai kamera 4G, atau Starlink untuk lokasi tanpa sinyal seluler.'),
             ('Pantau jarak jauh', 'Rekaman dan status baterai dipantau dari HP.'),
             ('Perawatan', 'Pembersihan panel dan pengecekan baterai berkala.')],
        faq=[('Apakah CCTV tenaga surya tetap menyala di malam hari?', 'Ya. Baterai mengisi di siang hari dan menghidupkan kamera di malam hari. Kapasitasnya kami hitung agar tahan beberapa hari mendung.'),
             ('Bagaimana kalau tidak ada sinyal 4G?', 'Bisa memakai Starlink atau wireless bridge ke titik yang ada internet.'),
             ('Apakah rekaman tersimpan kalau internet putus?', 'Ya. Kamera menyimpan rekaman di microSD, lalu bisa diakses lagi saat koneksi kembali.'),
             ('Cocok untuk area apa?', 'Proyek konstruksi, kebun sawit, tambak, gudang terpencil, jalan hauling, dan pos jaga.')],
        proof=['instalasi-cctv-ai-analytics']),
    'videotron': dict(slug='videotron-{c}', short='Videotron', h1='Videotron & LED display di {C}',
        title='Videotron {C} | LED Indoor & Outdoor | Altora',
        desc='Pengadaan dan pemasangan videotron di {C}: LED indoor dan outdoor HDe untuk aula, lobi, ruang kendali, dan papan informasi luar ruangan.',
        lead='Videotron LED indoor dan outdoor untuk aula, lobi, ruang kendali, panggung, dan papan informasi di {C}. Kami bantu hitung ukuran layar, rangka, kelistrikan, hingga pemasangan dan pengaturan konten.',
        hero='/assets/img/hardware/hde-videotron-outdoor.webp', main='/services/smart-display-kios', main_label='Layanan smart display, signage & kios',
        items=[hw('hde-videotron-indoor'), hw('hde-videotron-outdoor'), hw('digital-signage'), hw('hde-ifp')],
        dos=[('Hitung ukuran & jarak pandang', 'Ukuran layar dan pixel pitch disesuaikan jarak penonton.'),
             ('Rangka & struktur', 'Rangka dinding, tiang, atau rigging sesuai lokasi.'),
             ('Kelistrikan', 'Jalur daya dan proteksi yang aman untuk layar besar.'),
             ('Pemasangan & kalibrasi', 'Modul dipasang, disambung, dan dikalibrasi warnanya.'),
             ('Pengaturan konten', 'Konten bisa diganti dari komputer atau jarak jauh.'),
             ('Perawatan', 'Penggantian modul, cek daya, dan pembersihan berkala.')],
        faq=[('Videotron indoor atau outdoor?', 'Outdoor untuk area terkena matahari dan hujan, dengan kecerahan tinggi. Indoor untuk aula, lobi, dan ruang rapat.'),
             ('Ukuran berapa yang cocok?', 'Tergantung lebar dinding dan jarak penonton. Kami bantu hitung saat survei.'),
             ('Apakah bisa untuk instansi pemerintah?', 'Bisa. Kami terdaftar PKP dan dapat melayani pengadaan instansi.'),
             ('Bagaimana mengganti isi tayangan?', 'Lewat software pengelola konten dari komputer, termasuk penjadwalan.')],
        proof=['custom-kios-k-pengadaan-hardware']),
    'ifp': dict(slug='interactive-flat-panel-{c}', short='Interactive flat panel', h1='Interactive flat panel & smartboard di {C}',
        title='Interactive Flat Panel {C} | Smartboard | Altora',
        desc='Jual dan pasang interactive flat panel (smartboard) di {C} untuk ruang kelas, ruang rapat, dan pelatihan, plus sistem rekaman rapat HDe.',
        lead='Layar sentuh besar untuk ruang kelas, ruang rapat, dan ruang pelatihan di {C}. Bisa untuk presentasi, menulis langsung di layar, dan rapat online.',
        hero='/assets/img/hardware/hde-ifp.webp', main='/katalog#hde-ifp', main_label='Interactive flat panel di katalog',
        items=[hw('hde-ifp'), hw('hde-mrs'), hw('hde-aio-il24'), hw('hde-aio-al22')],
        dos=[('Pilih ukuran layar', 'Disesuaikan ukuran ruangan dan jarak duduk peserta.'),
             ('Bracket atau stand', 'Dipasang di dinding atau di stand beroda yang bisa dipindah.'),
             ('Instalasi & koneksi', 'Tersambung ke laptop, HP, dan jaringan kantor atau sekolah.'),
             ('Rapat online', 'Kamera, mikrofon, dan aplikasi rapat siap dipakai.'),
             ('Pelatihan pengguna', 'Guru atau staf kami ajari cara pakai sampai lancar.'),
             ('Pengadaan sekolah & instansi', 'Melayani pengadaan dalam jumlah banyak.')],
        faq=[('Apa bedanya interactive flat panel dengan TV biasa?', 'Layarnya bisa disentuh dan ditulisi, punya sistem sendiri, dan bisa dipakai tanpa laptop.'),
             ('Apakah bisa dipakai untuk rapat online?', 'Bisa, dengan kamera dan mikrofon yang terpasang atau tambahan.'),
             ('Cocok untuk sekolah?', 'Cocok untuk ruang kelas, laboratorium, dan ruang guru.'),
             ('Apakah ada pelatihan?', 'Ada. Kami latih pengguna setelah pemasangan.')],
        proof=[]),
    'kiosk': dict(slug='mesin-kiosk-{c}', short='Mesin kiosk', h1='Mesin kiosk & digital signage di {C}',
        title='Mesin Kiosk & Digital Signage {C} | Altora',
        desc='Pengadaan mesin kiosk layanan mandiri dan digital signage di {C}: antrean, cetak dokumen, informasi publik. Sudah dipakai kelurahan di Samarinda.',
        lead='Kios layanan mandiri untuk antrean, cetak dokumen, dan informasi, serta layar digital signage untuk promosi dan pengumuman di {C}. Kios kami sudah dipakai di kantor-kantor kelurahan Samarinda.',
        hero='/assets/img/portfolio/kiosk-samarinda/kiosk-pampang.jpg', main='/services/smart-display-kios', main_label='Layanan smart display, signage & kios',
        items=[hw('kios-k'), hw('digital-signage'), hw('hde-ifp'), hw('hde-aio-il24')],
        dos=[('Desain sesuai layanan', 'Tampilan dan alur kios disesuaikan layanan Anda.'),
             ('Perangkat lengkap', 'Layar sentuh, scanner barcode, dan printer struk.'),
             ('Aplikasi kios', 'Bisa memakai aplikasi antrean atau sistem layanan yang sudah ada.'),
             ('Pengiriman & instalasi', 'Kios dikirim, dirakit, dan diuji di lokasi.'),
             ('Pelatihan petugas', 'Petugas diajari mengoperasikan dan merawat kios.'),
             ('Perawatan', 'Penggantian kertas printer, update sistem, dan perbaikan.')],
        faq=[('Kios ini sudah dipakai di mana?', 'Di beberapa kantor kelurahan Kota Samarinda untuk layanan mandiri warga.'),
             ('Apakah bisa terhubung ke sistem antrean kami?', 'Bisa. Kami integrasikan dengan sistem yang sudah ada atau buatkan aplikasinya.'),
             ('Digital signage bisa diganti isinya dari jauh?', 'Bisa. Konten dikelola dari cloud dan bisa dijadwalkan.'),
             ('Apakah melayani pengadaan instansi?', 'Ya. Kami PKP dan terdaftar di Inaproc/LKPP.')],
        proof=['custom-kios-k-pengadaan-hardware']),
    'rak': dict(slug='rak-server-{c}', short='Rak server', h1='Rak server & data center di {C}',
        title='Jual Rak Server {C} | Close Rack & Wallmount | Altora',
        desc='Jual dan pasang rak server di {C}: close rack, wallmount, heavy duty, cold/hot aisle containment, dan inrow cooling HaganeRack, plus penataan kabel.',
        lead='Rak server, wallmount, dan solusi data center untuk ruang server kantor, kampus, dan instansi di {C}. Dipasang rapi bersama penataan kabel, PDU, dan jaringan.',
        hero='/assets/img/portfolio/unmul-infrastructure/network-rack.png', main='/katalog#hr-close-perforated', main_label='Rak server di katalog',
        items=[hw('hr-close-perforated'), hw('hr-close-glass'), hw('hr-wallmount-double'), hw('hr-wallmount-single'), hw('hr-heavy-duty'), hw('hr-cold-aisle'), hw('hr-inrow-cooling')],
        dos=[('Pilih ukuran rak', 'Tinggi (U), kedalaman, dan jenis pintu sesuai perangkat.'),
             ('Penataan kabel', 'Kabel diberi label dan ditata supaya mudah dirawat.'),
             ('Daya & pendingin', 'PDU, UPS, dan aliran udara yang tepat untuk ruang server.'),
             ('Data center', 'Cold/hot aisle containment dan inrow cooling untuk skala besar.'),
             ('Dokumentasi', 'Denah rak dan daftar port diserahkan setelah selesai.'),
             ('Pengadaan proyek', 'Melayani satuan maupun proyek instansi.')],
        faq=[('Rak wallmount atau close rack?', 'Wallmount untuk perangkat sedikit di ruangan kecil. Close rack untuk server dan perangkat jaringan yang lebih banyak.'),
             ('Apakah sekalian penataan kabel?', 'Ya. Kabel kami rapikan, beri label, dan dokumentasikan.'),
             ('Bisa untuk data center?', 'Bisa, termasuk containment dan inrow cooling HaganeRack.'),
             ('Merek apa yang dipakai?', 'HaganeRack, partner resmi kami untuk rak dan data center.')],
        proof=['unmul-infrastruktur-cctv-jaringan']),
    'fiber': dict(slug='alat-fiber-optik-{c}', short='Alat fiber optik', h1='Alat fiber optik & jasa splicing di {C}',
        title='Alat Fiber Optik {C} | OTDR & Fusion Splicer | Altora',
        desc='Jual alat fiber optik di {C}: OTDR, fusion splicer, power meter, light source, patch cord Fasser, plus jasa penarikan dan penyambungan fiber.',
        lead='Alat ukur dan sambung fiber optik untuk ISP, kontraktor jaringan, dan tim IT di {C}, plus jasa penarikan, penyambungan, dan pengujian jalur fiber.',
        hero='/assets/img/hardware/fas-fusion-splicer.webp', main='/katalog#fas-otdr', main_label='Alat fiber di katalog',
        items=[hw('fas-otdr'), hw('fas-fusion-splicer'), hw('fas-power-meter'), hw('fas-light-source'), hw('fas-patch-cord')],
        dos=[('Penjualan alat', 'OTDR, fusion splicer, power meter, dan light source resmi Fasser.'),
             ('Penarikan kabel', 'Penarikan fiber dalam gedung dan antar gedung.'),
             ('Splicing', 'Penyambungan fiber dengan fusion splicer.'),
             ('Pengujian OTDR', 'Hasil uji redaman dan jarak diserahkan sebagai laporan.'),
             ('Rak & ODP', 'Penataan terminasi di rak dan ODP.'),
             ('Pelatihan alat', 'Pelatihan pemakaian alat untuk tim Anda.')],
        faq=[('Apakah bisa beli alatnya saja?', 'Bisa. Kami menjual OTDR, splicer, dan alat ukur Fasser.'),
             ('Apakah ada laporan hasil uji?', 'Ada. Hasil OTDR diserahkan setelah penyambungan.'),
             ('Melayani antar gedung?', 'Ya, termasuk area kampus dan kawasan industri.'),
             ('Bisa pelatihan pemakaian alat?', 'Bisa, untuk tim teknis pembeli.')],
        proof=['unmul-infrastruktur-cctv-jaringan']),
    'absensi': dict(slug='absensi-face-recognition-{c}', short='Absensi face recognition', h1='Absensi face recognition di {C}',
        title='Absensi Face Recognition {C} | Altora Indonesia',
        desc='Absensi face recognition di {C}: absen otomatis dari kamera CCTV atau HP dengan GPS, terhubung ke HRIS dan payroll Altora Teams.',
        lead='Absensi wajah untuk kantor, pabrik, sekolah, dan instansi di {C}. Karyawan cukup lewat di depan kamera, atau absen dari HP dengan GPS. Data langsung masuk ke HRIS.',
        hero='/assets/img/portfolio/attendance.jpg', main='/produk/attendance', main_label='Altora Smart Attendance',
        items=[('altora-attendance', 'Altora Smart Attendance', 'Aplikasi Altora', '/assets/img/produk/attendance.webp', ['Absen wajah dari CCTV', 'Tanpa antre di mesin', 'Laporan kehadiran otomatis']),
               ('altora-teams', 'Altora Teams (HRIS)', 'Aplikasi Altora', '/assets/img/produk/teams.webp', ['Absensi GPS & selfie', 'Cuti, lembur, shift', 'Payroll otomatis']),
               vigi('S245', ['Dome 4 MP untuk pintu masuk', 'People analytics', 'Dipakai untuk absen wajah']),
               vigi('S245ZI', ['Dome 4 MP zoom optik', 'Face recognition', 'Untuk lorong & gerbang'])],
        dos=[('Pasang kamera di titik masuk', 'Posisi dan pencahayaan diatur supaya wajah terbaca akurat.'),
             ('Daftar wajah karyawan', 'Kami bantu pendaftaran wajah seluruh karyawan.'),
             ('Absen dari HP', 'Untuk karyawan lapangan, absen GPS dan selfie dari aplikasi.'),
             ('Terhubung ke HRIS', 'Data kehadiran masuk ke Altora Teams untuk cuti, lembur, dan payroll.'),
             ('Pakai CCTV lama', 'Kamera yang sudah ada sering bisa dipakai, kami cek dulu.'),
             ('Sosialisasi', 'Pelatihan HR dan sosialisasi ke karyawan.')],
        faq=[('Apakah bisa memakai CCTV yang sudah ada?', 'Sering bisa, tergantung resolusi dan posisi kamera. Kami cek saat survei.'),
             ('Bagaimana karyawan lapangan absen?', 'Lewat aplikasi HP dengan GPS dan foto wajah.'),
             ('Apakah data kehadiran bisa diekspor?', 'Bisa. Laporan bisa diunduh dan disambungkan ke payroll.'),
             ('Apakah aman untuk data wajah?', 'Data disimpan di server yang disepakati dan aksesnya dibatasi.')],
        proof=['smart-attendance', 'altora-teams', 'hris-mobile-payroll']),
}


def fmt(t, c):
    return t.replace('{C}', c['name']).replace('{c}', c['key'])


def card(it, city):
    pid, name, brand, img, specs = it
    pic = f'<img alt="{e(name)}" loading="lazy" src="{e(img)}"/>' if img else '<span class="pk-noimg" aria-hidden="true"></span>'
    lis = ''.join(f'<li>{e(s)}</li>' for s in specs)
    msg = f'Halo Altora, saya di {city} dan ingin tahu ketersediaan {name}.'
    return (f'<article class="pk-item"><div class="pk-pic">{pic}</div><small>{e(brand)}</small><h3>{e(name)}</h3><ul>{lis}</ul>'
            f'<div class="vg-act"><button class="cart-add cart-add-sm" data-cart-id="{e(pid)}" data-cart-img="{e(img)}" data-cart-meta="{e(brand)}" '
            f'data-cart-name="{e(name)}" type="button"><span aria-hidden="true">+</span><span class="cart-add-label">Tambah ke keranjang</span></button>'
            f'<a class="vg-ask" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Tanya stok</a></div></article>')


def page(pkey, ckey):
    p = PRODUCTS[pkey]; c = dict(CITIES[ckey], key=ckey)
    url = '/' + fmt(p['slug'], c)
    h1, title, desc = fmt(p['h1'], c), fmt(p['title'], c), fmt(p['desc'], c)
    items = ''.join(card(it, c['name']) for it in p['items'])
    dos = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(fmt(d, c))}</p></article>' for t, d in p['dos'])
    proof_ids = [x for x in dict.fromkeys(p['proof'] + (c['local_proof'] if pkey in ('kiosk', 'cctv', 'rak', 'fiber') else [])) if x in PF][:3]
    proof = ''.join(f'<a class="svd-proof" href="/portfolio/{x}"><span class="svd-proof-img"><img alt="" loading="lazy" src="{PF[x][1]}"/></span><b>{e(PF[x][0])}</b><small>Lihat proyek</small></a>' for x in proof_ids)
    proof_sec = (f'<section class="svd-sec" id="proyek"><div class="ct-wrap"><div class="pd-block-head"><h2>Proyek terkait</h2></div><div class="svd-proofs">{proof}</div></div></section>' if proof else '')
    faq_items = [(fmt(q, c), fmt(a, c)) for q, a in p['faq']] + [
        (f'Apakah melayani pengadaan dan pemasangan {p["short"].lower()} di {c["name"]}?', c['base']),
        ('Apakah bisa untuk pengadaan instansi pemerintah?', 'Bisa. Altora berstatus PKP dan terdaftar di Inaproc/LKPP, sehingga dapat melayani pengadaan instansi dan BUMN.')]
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq_items)
    other = [k for k in CITIES if k != ckey][0]
    same_city = ''.join(f'<a href="/{fmt(PRODUCTS[k]["slug"], c)}">{e(PRODUCTS[k]["short"])} {e(c["name"])}</a>' for k in PRODUCTS if k != pkey)
    links = (f'<a href="/{fmt(p["slug"], dict(CITIES[other], key=other))}">{e(p["short"])} {e(CITIES[other]["name"])}</a>'
             f'<a href="{p["main"]}">{e(p["main_label"])}</a><a href="/jasa-pasang-cctv-{ckey}">Jasa pasang CCTV {e(c["name"])}</a>'
             f'<a href="/it-support-{ckey}">IT support {e(c["name"])}</a>' + same_city)
    msg = f'Halo Altora, saya di {c["name"]} dan butuh {p["short"].lower()}.'
    office = next(o for o in OFFICES if o['city'] == c['name'])
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': h1, 'description': desc, 'url': SITE + url, 'serviceType': f'Penjualan, pengadaan & instalasi {p["short"].lower()}',
         'areaServed': {'@type': 'City', 'name': c['name']},
         'provider': {'@type': 'ProfessionalService', 'name': 'Altora Indonesia', 'alternateName': ['Altora', 'Algora Teknologi Indonesia'], 'url': SITE + '/',
                      'telephone': '+6285190911170', 'image': SITE + '/assets/img/altora-logo-600.png', 'address': postal_address(office)},
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': h1, 'itemListElement': [
             {'@type': 'Offer', 'itemOffered': {'@type': 'Product', 'name': it[1], 'brand': {'@type': 'Brand', 'name': it[2]}, 'description': ', '.join(it[4])}} for it in p['items']]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Area layanan', 'item': SITE + '/area-layanan'},
            {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items]}]}
    body = f'''<main class="ct-page svd-page lc-page pk-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/area-layanan">Area layanan</a><span>/</span><span>{e(c["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">Jual · Pengadaan · Instalasi · Maintenance</p><h1>{e(h1)}</h1><p class="ct-lead">{e(fmt(p["lead"], c))}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Minta penawaran</a><a class="svd-link" href="#produk">Lihat produk</a></div></div>
<figure class="svd-hero-pic pk-hero-pic"><img alt="{e(h1)}" src="{p["hero"]}"/><span class="svd-chip svd-chip-0">{e(c["name"])}</span><span class="svd-chip svd-chip-1">Produk resmi</span><span class="svd-chip svd-chip-2">Dipasang tim lokal</span></figure>
</div></section>
<section class="svd-sec" id="produk"><div class="ct-wrap"><div class="pd-block-head"><h2>Produk {e(p["short"].lower())} yang tersedia di {e(c["name"])}</h2><p>Tanpa harga di website. Masukkan ke keranjang, lalu kirim lewat WhatsApp untuk penawaran.</p></div>
<div class="pk-grid">{items}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Pengadaan sampai perawatan</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Melayani {e(c["name"])} dan sekitarnya</h2><p>{e(c["base"])}</p><p>Klien kami di {e(c["name"])} antara lain {e(c["sectors"])}.</p></div></div></section>
{proof_sec}
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div>
<div class="svd-related"><b>Lihat juga</b>{links}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh {e(p["short"].lower())} di {e(c["name"])}?</h2><p>Kirim kebutuhan Anda, kami balas dengan penawaran.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    img = p['hero'] if p['hero'].startswith('http') else SITE + p['hero']
    return url, h1, shell(title, desc, url, img, ld, body)


def hub_section(built):
    rows = ''
    for ckey, cdat in CITIES.items():
        links = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(h)}</b></a>' for (ck, u, h) in built if ck == ckey)
        rows += f'<div class="pk-hubcity"><h3>{e(cdat["name"])}</h3><div class="lc-svcs">{links}</div></div>'
    return ('<!-- produk-kota:start --><section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Jual &amp; pasang produk per kota</h2>'
            '<p>Pengadaan, instalasi, dan perawatan perangkat di Samarinda dan Balikpapan.</p></div>' + rows + '</div></section><!-- produk-kota:end -->')


if __name__ == '__main__':
    built = []
    for ckey in CITIES:
        for pkey in PRODUCTS:
            url, h1, htmlp = page(pkey, ckey)
            (root / (url.lstrip('/') + '.html')).write_text(htmlp, encoding='utf-8')
            built.append((ckey, url, h1))
    # hub /area-layanan & /produk: daftar halaman produk per kota
    sec = hub_section(built)
    for f, anchor in (('area-layanan.html', '</main>'),):
        fp = root / f; s = fp.read_text(encoding='utf-8')
        if '<!-- produk-kota:start -->' in s:
            s = re.sub(r'<!-- produk-kota:start -->.*?<!-- produk-kota:end -->', lambda _: sec, s, count=1, flags=re.S)
        else:
            s = s.replace(anchor, sec + anchor, 1)
        fp.write_text(s, encoding='utf-8')
    update_sitemap([u for _, u, _ in built])
    print('produk x kota:', len(built), 'halaman')
