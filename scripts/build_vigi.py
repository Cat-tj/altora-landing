"""Bangun katalog-cctv-vigi.html: semua model VIGI (VIGI Product Guide 2024), tanpa harga.
Jalankan dari root repo:  python3 scripts/build_vigi.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py"""
import html, pathlib, re
from urllib.parse import quote
from build_area import shell, update_sitemap, SITE

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda s: html.escape(str(s), quote=True)
WA = 'https://wa.me/6285190911170?text='

# (id kategori, judul, keterangan, gambar di assets/img/hardware)
CATS = [
    ('dome', 'Kamera dome', 'Untuk plafon dan dinding: ruangan, lobi, toko, kantor. Tahan benturan (IK10 pada sebagian besar tipe).', 'vigi-dome'),
    ('bullet', 'Kamera bullet', 'Sorotan jarak jauh untuk pagar, parkiran, dan jalur perimeter.', 'vigi-bullet'),
    ('turret', 'Kamera turret', 'Serbaguna untuk teras, gudang, dan area parkir. Lensa tidak berembun karena IR di luar kubah.', 'vigi-turret-fullcolor'),
    ('pt', 'Pan tilt & PTZ', 'Berputar 360° untuk halaman, lapangan, dan area luas. Ada tipe Wi-Fi, 4G, dan zoom hingga 32×.', 'vigi-ptz'),
    ('fisheye', 'Fisheye', 'Satu kamera untuk seluruh ruangan dengan pandangan 180° atau 360°.', 'vigi-dome-ir'),
    ('nvr', 'NVR (perekam)', 'Menyimpan dan memutar ulang rekaman. Tipe P/MP sekaligus memberi daya PoE ke kamera.', 'vigi-nvr'),
    ('kit', 'Paket NVR + kamera', 'Paket siap pasang: NVR, kamera, dan hard disk dalam satu set.', 'vigi-nvr'),
    ('nvd', 'Video decoder', 'Untuk video wall di ruang kendali.', 'vigi-nvr-rack'),
    ('solar', 'Tenaga surya', 'Panel surya dan baterai untuk kamera di lokasi tanpa listrik.', 'vigi-solar'),
    ('net', 'Jaringan pendukung', 'Switch PoE, access point, dan wireless bridge TP-Link Omada yang direkomendasikan untuk sistem VIGI.', None),
    ('acc', 'Aksesori', 'Junction box untuk pemasangan yang rapi dan tahan air.', None),
]

AUR = 'Aurora · ColorPro'
INF, INI, ECF, ECI = 'Insight · Full-Color', 'Insight · IR & zoom', 'Eco · Full-Color', 'Eco · IR'
AUR_S = ['F1.0, malam berwarna 0,0005 lux', 'WDR 120 dB', 'People & vehicle analytics, face recognition']
INF_S = ['Full-color, IR + white light 30 m', 'WDR 120 dB', 'People & vehicle analytics']
INI_S = ['Optical zoom 5× (2,7–13,5 mm)', 'IR 60 m, WDR 120 dB', 'Face capture, people & vehicle analytics']
ECF_S = ['Full-color, IR + white light 30 m', 'Human & vehicle classification']
ECI_S = ['Inframerah 30 m', 'Human & vehicle classification']

NEW = 'InSight S · 2025'
NEW_FC = ['Full-color 24/7', 'People & vehicle analytics']
NEW_CP = ['ColorPro 2.0, malam berwarna', 'People & vehicle analytics']
NEW_ZI = ['IR, lensa varifocal bermotor', 'People & vehicle analytics']
EASY = 'EasyCam'

# (model, kategori, seri, resolusi/ringkas, [spesifikasi], proteksi/koneksi)
M = [
    # Dome
    ('S285Z', 'dome', NEW, '8 MP (4K)', ['Full-color, varifocal bermotor'] + NEW_FC[1:], 'Seri proyek'),
    ('S285S', 'dome', NEW, '8 MP (4K)', NEW_CP, 'Seri proyek'),
    ('S285', 'dome', NEW, '8 MP (4K)', NEW_FC, 'Seri proyek'),
    ('S245S', 'dome', NEW, '4 MP', NEW_CP, 'Seri proyek'),
    ('S245ZI', 'dome', NEW, '4 MP', NEW_ZI, 'Seri proyek'),
    ('S245I Mini', 'dome', NEW, '4 MP', ['IR, bodi mini', 'Human & vehicle classification'], 'Seri proyek'),
    ('S245', 'dome', NEW, '4 MP', NEW_FC, 'Seri proyek'),
    ('S225', 'dome', NEW, '2 MP', NEW_FC, 'Seri proyek'),
    ('C285S', 'dome', AUR, '8 MP', AUR_S, 'IP67, IK10, metal'),
    ('C245S', 'dome', AUR, '4 MP', AUR_S, 'IP67, IK10, metal'),
    ('C285', 'dome', INF, '8 MP (4K)', INF_S, 'IP67, IK10, metal'),
    ('C255', 'dome', INF, '5 MP', INF_S, 'IP67, IK10, metal'),
    ('C245', 'dome', INF, '4 MP', INF_S + ['Mikrofon & speaker'], 'IP67, IK10, metal'),
    ('C285ZI', 'dome', INI, '8 MP (4K)', INI_S, 'IP67, IK10, metal'),
    ('C245ZI', 'dome', INI, '4 MP', INI_S, 'IP67, IK10, metal'),
    ('C250', 'dome', ECF, '5 MP', ECF_S + ['WDR 120 dB'], 'IP67, IK10'),
    ('C240', 'dome', ECF, '4 MP', ECF_S + ['Mikrofon'], 'IP67, IK10'),
    ('C230', 'dome', ECF, '3 MP', ECF_S, 'IP67, IK10'),
    ('C240I', 'dome', ECI, '4 MP', ECI_S, 'IP67, IK10'),
    ('C230I', 'dome', ECI, '3 MP', ECI_S, 'IP67, IK10'),
    ('C220I', 'dome', ECI, '2 MP', ECI_S, 'IP67, IK10'),
    ('C230I Mini', 'dome', ECI, '3 MP', ECI_S + ['Bodi mini, mikrofon & microSD'], 'IK08, indoor'),
    # Bullet
    ('S385Z', 'bullet', NEW, '8 MP (4K)', ['Full-color, varifocal bermotor'] + NEW_FC[1:], 'Seri proyek'),
    ('S385S', 'bullet', NEW, '8 MP (4K)', NEW_CP, 'Seri proyek'),
    ('S385DPS', 'bullet', NEW, '8 MP dual-lens', ['Panoramic ColorPro'] + NEW_CP[1:], 'Seri proyek'),
    ('S385PI', 'bullet', NEW, '8 MP panoramic', ['Pandangan 180°, IR', 'People & vehicle analytics'], 'Seri proyek'),
    ('S385', 'bullet', NEW, '8 MP (4K)', NEW_FC, 'Seri proyek'),
    ('S355', 'bullet', NEW, '5 MP', NEW_FC, 'Seri proyek'),
    ('LPR345Z', 'bullet', NEW, '4 MP · ANPR', ['Baca plat nomor (ANPR)', 'Full-color, zoom bermotor'], 'Untuk gerbang & parkir'),
    ('S345S', 'bullet', NEW, '4 MP', NEW_CP, 'Seri proyek'),
    ('S345ZI', 'bullet', NEW, '4 MP', NEW_ZI, 'Seri proyek'),
    ('S345-4G', 'bullet', NEW, '4 MP · 4G LTE', ['Koneksi 4G'] + NEW_FC, 'Seri proyek'),
    ('S345', 'bullet', NEW, '4 MP', NEW_FC, 'Seri proyek'),
    ('S325', 'bullet', NEW, '2 MP', NEW_FC, 'Seri proyek'),
    ('C385S', 'bullet', AUR, '8 MP (4K)', AUR_S, 'IP67, metal'),
    ('C385DPS', 'bullet', AUR, '8 MP dual-lens', ['Panoramic 171°'] + AUR_S, 'IP67, metal'),
    ('C345S', 'bullet', AUR, '4 MP', AUR_S, 'IP67, metal'),
    ('C340S', 'bullet', AUR, '4 MP', AUR_S + ['Audio dua arah'], 'IP67'),
    ('C385DP', 'bullet', INF, '8 MP dual-lens', ['Panoramic 32:9 tanpa celah', 'Full-color', 'Human & vehicle classification'], 'IP67'),
    ('C385P', 'bullet', INF, '8 MP panoramic', INF_S, 'IP67, metal'),
    ('C385', 'bullet', INF, '8 MP (4K)', INF_S + ['Active defense'], 'IP67, metal'),
    ('C355', 'bullet', INF, '5 MP', INF_S, 'IP67, metal'),
    ('C345', 'bullet', INF, '4 MP', INF_S + ['Active defense'], 'IP67, metal'),
    ('C345-4G', 'bullet', INF, '4 MP · 4G LTE', ['Koneksi 4G (Nano SIM) / Ethernet'] + INF_S, 'IP67, metal'),
    ('C385ZI', 'bullet', INI, '8 MP (4K)', INI_S, 'IP67, metal'),
    ('C345ZI', 'bullet', INI, '4 MP', INI_S, 'IP67, metal'),
    ('C350', 'bullet', ECF, '5 MP', ECF_S + ['WDR 120 dB'], 'IP67'),
    ('C340', 'bullet', ECF, '4 MP', ECF_S + ['Active defense, audio dua arah'], 'IP67'),
    ('C340-W', 'bullet', ECF, '4 MP · Wi-Fi', ['Koneksi Wi-Fi / Ethernet'] + ECF_S, 'IP67'),
    ('C330', 'bullet', ECF, '3 MP', ECF_S, 'IP67'),
    ('C340I', 'bullet', ECI, '4 MP', ECI_S, 'IP67'),
    ('C330I', 'bullet', ECI, '3 MP', ECI_S, 'IP67'),
    ('C320I', 'bullet', ECI, '2 MP', ECI_S, 'IP67'),
    ('C323I', 'bullet', ECI, '2 MP', ECI_S + ['Mikrofon'], 'IP67'),
    ('C320', 'bullet', EASY, '2 MP', ['Full-color', 'Human & vehicle classification'], 'Paling ekonomis'),
    ('C300HP', 'bullet', EASY, '3 MP', ['Inframerah', 'Deteksi gerak & manusia'], 'Outdoor, paling ekonomis'),
    # Turret
    ('S485Z', 'turret', NEW, '8 MP (4K)', ['Full-color, varifocal bermotor'] + NEW_FC[1:], 'Seri proyek'),
    ('S485S', 'turret', NEW, '8 MP (4K)', NEW_CP, 'Seri proyek'),
    ('S485PI', 'turret', NEW, '8 MP panoramic', ['Pandangan 180°, IR', 'People & vehicle analytics'], 'Seri proyek'),
    ('S485', 'turret', NEW, '8 MP (4K)', NEW_FC, 'Seri proyek'),
    ('S455', 'turret', NEW, '5 MP', NEW_FC, 'Seri proyek'),
    ('S445S', 'turret', NEW, '4 MP', NEW_CP, 'Seri proyek'),
    ('S445ZI', 'turret', NEW, '4 MP', NEW_ZI, 'Seri proyek'),
    ('S445', 'turret', NEW, '4 MP', NEW_FC, 'Seri proyek'),
    ('S425', 'turret', NEW, '2 MP', NEW_FC, 'Seri proyek'),
    ('C485S', 'turret', AUR, '8 MP (4K)', AUR_S, 'IP67, metal'),
    ('C445S', 'turret', AUR, '4 MP', AUR_S, 'IP67, metal'),
    ('C485P', 'turret', INF, '8 MP panoramic', INF_S, 'IP67, metal'),
    ('C485', 'turret', INF, '8 MP (4K)', INF_S + ['Audio dua arah'], 'IP67, metal'),
    ('C455', 'turret', INF, '5 MP', INF_S, 'IP67, metal'),
    ('C445', 'turret', INF, '4 MP', INF_S + ['Audio dua arah'], 'IP67, metal'),
    ('C485ZI', 'turret', INI, '8 MP (4K)', INI_S, 'IP67, metal'),
    ('C445ZI', 'turret', INI, '4 MP', INI_S, 'IP67, metal'),
    ('C450', 'turret', ECF, '5 MP', ECF_S + ['WDR 120 dB, speaker'], 'Indoor / outdoor'),
    ('C440', 'turret', ECF, '4 MP', ECF_S + ['Active defense, audio dua arah'], 'Indoor / outdoor'),
    ('C440-W', 'turret', ECF, '4 MP · Wi-Fi', ['Koneksi Wi-Fi / Ethernet'] + ECF_S, 'Indoor / outdoor'),
    ('C430', 'turret', ECF, '3 MP', ECF_S, 'Indoor / outdoor'),
    ('C440I', 'turret', ECI, '4 MP', ECI_S, 'Indoor'),
    ('C430I', 'turret', ECI, '3 MP', ECI_S, 'Indoor'),
    ('C420I', 'turret', ECI, '2 MP', ECI_S, 'Indoor'),
    ('C420', 'turret', EASY, '2 MP', ['Full-color', 'Human & vehicle classification'], 'Paling ekonomis'),
    ('C400HP', 'turret', EASY, '3 MP', ['Inframerah', 'Deteksi gerak & manusia'], 'Paling ekonomis'),
    # Pan tilt
    ('PTZ7832', 'pt', NEW, '8 MP · zoom 32×', ['Speed dome 7 inci', 'Optical zoom 32×', 'Untuk area sangat luas'], 'Seri proyek'),
    ('PTZ5425', 'pt', NEW, '4 MP · zoom 25×', ['PTZ 5 inci, IR', 'Optical zoom 25×'], 'Seri proyek'),
    ('S545ZR', 'pt', NEW, '4 MP · zoom 5×', ['PTZ 3 inci, IR', 'Optical zoom 5×'], 'Seri proyek'),
    ('S545Z-4G', 'pt', NEW, '4 MP · 4G · zoom 5×', ['Koneksi 4G', 'Full-color PTZ, zoom 5×'], 'Seri proyek'),
    ('S545Z', 'pt', NEW, '4 MP', ['Full-color PTZ', 'People & vehicle analytics'], 'Seri proyek'),
    ('S9165QPS', 'pt', NEW, '4 × 4 MP', ['Panoramic 4 sensor', 'ColorPro 2.0', 'Untuk persimpangan & area terbuka'], 'Seri proyek'),
    ('C540S', 'pt', AUR, '4 MP', ['Pan tilt 360°'] + AUR_S, 'IP66'),
    ('C580', 'pt', 'Pan Tilt', '8 MP (4K)', ['Pan tilt 360°', 'Human & vehicle classification', 'Active defense'], 'Outdoor'),
    ('C540V', 'pt', 'Pan Tilt', '4 MP dual-lens', ['Zoom 3× instan (4–12 mm)', 'Pan tilt 360°', 'Human & vehicle classification'], 'Outdoor'),
    ('C540', 'pt', 'Pan Tilt', '4 MP', ['Pan tilt 360°, auto tracking', 'Full-color', 'Active defense'], 'Outdoor'),
    ('C540-W', 'pt', 'Pan Tilt', '4 MP · Wi-Fi', ['Koneksi Wi-Fi / Ethernet', 'Pan tilt 360°, full-color', 'Active defense'], 'Outdoor'),
    ('C540-4G', 'pt', 'Pan Tilt', '4 MP · 4G LTE', ['Koneksi 4G (Nano SIM), bisa jadi router', 'Pan tilt 360°', 'Cocok dengan VIGI Solar'], 'Outdoor'),
    # Fisheye
    ('S6125I', 'fisheye', NEW, '8 MP', ['Fisheye IR', 'Pandangan 360°'], 'Seri proyek'),
    ('S655I', 'fisheye', NEW, '5 MP', ['Fisheye IR', 'Pandangan 360°'], 'Seri proyek'),
    ('C685I', 'fisheye', INI, '8 MP', ['Lensa 1,4 mm, pandangan 180°', 'IR 10 m, WDR 100 dB', 'Dewarping 180° / quad view'], 'IP67, metal'),
    ('C655I', 'fisheye', INI, '5 MP', ['Pandangan 360° / 180°', 'Smart IR, density heat map', 'Smart detection'], 'IP67, metal'),
    # NVR PoE
    ('NVR2016H-16MP', 'nvr', 'NVR PoE', '16 kanal', ['16 port PoE+, budget 140 W', '2 HDD (maks. 10 TB/HDD)', 'Output 4K, LAN gigabit'], 'Tersedia versi -4TB (HDD terpasang)'),
    ('NVR2016H-16P', 'nvr', 'NVR PoE', '16 kanal', ['16 port PoE, budget 90 W', '2 HDD (maks. 10 TB/HDD)', 'Output 4K'], 'LAN gigabit'),
    ('NVR2008H-8MP-2TB', 'nvr', 'NVR PoE', '8 kanal', ['8 port PoE+, budget 92 W', '2 HDD, 2 TB terpasang', 'Output 4K'], 'HDMI / VGA'),
    ('NVR2008H-8MP', 'nvr', 'NVR PoE', '8 kanal', ['8 port PoE+, budget 92 W', '2 HDD (maks. 10 TB/HDD)', 'Output 4K'], 'HDMI / VGA'),
    ('NVR1008H-8MP', 'nvr', 'NVR PoE', '8 kanal', ['8 port PoE+, budget 113 W', '1 HDD (maks. 10 TB)', 'Output 4K HDMI'], 'HDMI / VGA'),
    ('NVR1008H-8P', 'nvr', 'NVR PoE', '8 kanal', ['8 port PoE, budget 53 W', '1 HDD (maks. 10 TB)', 'Output 4K'], 'HDMI / VGA'),
    ('NVR1004H-4P', 'nvr', 'NVR PoE', '4 kanal', ['4 port PoE, budget 53 W', '1 HDD (maks. 10 TB)', 'Output 4K'], 'Tersedia versi -2TB'),
    ('NVR1104H-4P', 'nvr', 'NVR PoE', '4 kanal', ['4 port PoE, budget 53 W', 'Pasang HDD cepat, speaker bawaan', 'Output 4K'], 'HDMI / VGA'),
    # NVR non-PoE
    ('NVR16128H', 'nvr', 'NVR', '128 kanal', ['16 HDD (SATA)', 'Untuk proyek skala besar', 'Smart search'], 'LAN gigabit'),
    ('NVR4016H', 'nvr', 'NVR', '16 kanal', ['4 HDD (SATA)', 'Rekam hingga 4K'], 'LAN gigabit'),
    ('NVR8096H', 'nvr', 'NVR', '96 kanal', ['8 HDD (maks. 10 TB/HDD)', 'Rekam hingga 8K (32 MP)', 'Face recognition & smart search'], '2× LAN gigabit, RAID'),
    ('NVR8064H', 'nvr', 'NVR', '64 kanal', ['8 HDD (maks. 10 TB/HDD)', 'Rekam hingga 8K (32 MP)', 'Face recognition & smart search'], '2× LAN gigabit, RAID'),
    ('NVR4064H', 'nvr', 'NVR', '64 kanal', ['4 HDD (maks. 10 TB/HDD)', 'Decode 16-ch @2MP', 'Face recognition & smart search'], '2× LAN gigabit, RAID'),
    ('NVR4032H', 'nvr', 'NVR', '32 kanal', ['4 HDD (maks. 10 TB/HDD)', 'Rekam hingga 4K', 'Output HDMI/VGA independen'], '2× LAN gigabit'),
    ('NVR2032H', 'nvr', 'NVR', '32 kanal', ['2 HDD (maks. 10 TB/HDD)', 'Rekam hingga 4K', 'Output HDMI/VGA independen'], '2× LAN gigabit'),
    ('NVR2016H', 'nvr', 'NVR', '16 kanal', ['2 HDD (maks. 10 TB/HDD)', 'Rekam hingga 4K'], 'HDMI / VGA'),
    ('NVR1016H', 'nvr', 'NVR', '16 kanal', ['1 HDD (maks. 10 TB)', 'Rekam hingga 4K'], 'HDMI / VGA'),
    ('NVR1108H-W', 'nvr', 'NVR Wi-Fi', '8 kanal', ['Pairing kamera Wi-Fi', '1 HDD (maks. 10 TB), pasang cepat', 'Rekam hingga 4K'], 'Wi-Fi 300 Mbps'),
    ('NVR1008H', 'nvr', 'NVR', '8 kanal', ['1 HDD (maks. 10 TB)', 'Rekam hingga 4K'], 'HDMI / VGA'),
    ('NVR1004H', 'nvr', 'NVR', '4 kanal', ['1 HDD (maks. 10 TB)', 'Rekam hingga 4K'], 'HDMI / VGA'),
    # Kit
    ('NK16MP-T12425-4T', 'kit', 'NVR Kit', '16 kanal + 12 kamera', ['NVR2016H-16MP', '12× turret C445 (2,8 mm)', 'HDD 4 TB terpasang'], 'Kamera 4 MP full-color, IP67'),
    ('NK8MP-T6425-2T', 'kit', 'NVR Kit', '8 kanal + 6 kamera', ['NVR1008H-8MP', '6× turret C445 (2,8 mm)', 'HDD 2 TB terpasang'], 'Kamera 4 MP full-color, IP67'),
    ('NK4P-T4425-2T', 'kit', 'NVR Kit', '4 kanal + 4 kamera', ['NVR1004H-4P', '4× turret C445 (2,8 mm)', 'HDD 2 TB terpasang'], 'Kamera 4 MP full-color, IP67'),
    ('NK8P-B434I', 'kit', 'NVR Kit', '8 kanal + 4 kamera', ['NVR1008H-8P', '4× bullet C330I (4 mm)', 'Tanpa HDD'], 'Kamera 3 MP IR, IP67'),
    # Decoder
    ('NVD6004', 'nvd', 'Decoder', '4 layar 4K', ['4× HDMI + 4× VGA', 'Decode 64 kamera 1080p bersamaan', 'Hingga 32 split per layar'], 'LAN gigabit, VIGI VMS'),
    ('NVD6012', 'nvd', 'Decoder', '12 layar 4K', ['12× HDMI + 12× VGA', 'Decode 192 kamera 1080p bersamaan', 'Hingga 36 split per layar'], 'LAN gigabit, VIGI VMS'),
    # Solar
    ('SP18090', 'solar', 'Solar', '1–2 panel 60/90 W', ['Baterai 1–3 × 20,8 Ah (custom)', 'Sudut panel 5–55°', 'Pantau daya dari aplikasi VIGI'], 'IP66'),
    ('SP9030', 'solar', 'Solar', 'Panel 90 W', ['Baterai lithium 31,2 Ah', '3 output DC 12 V', 'Pantau daya dari aplikasi VIGI'], 'IP66'),
    ('SP6030', 'solar', 'Solar', 'Panel 60 W', ['Baterai lithium 31,2 Ah', '3 output DC 12 V', 'Pantau daya dari aplikasi VIGI'], 'IP66'),
    ('SP6020', 'solar', 'Solar', 'Panel 60 W', ['Baterai lithium 20,8 Ah', '3 output DC 12 V', 'Pantau daya dari aplikasi VIGI'], 'IP66'),
    ('PS90', 'solar', 'Solar controller', 'Kontroler surya', ['Mengatur panel, baterai & beban', 'Pantau dari aplikasi VIGI'], 'Untuk sistem solar custom'),
    ('PS30', 'solar', 'Solar controller', 'Kontroler surya', ['Mengatur panel, baterai & beban', 'Pantau dari aplikasi VIGI'], 'Untuk sistem solar custom'),
    ('PS20', 'solar', 'Solar controller', 'Kontroler surya', ['Mengatur panel, baterai & beban', 'Pantau dari aplikasi VIGI'], 'Untuk sistem solar custom'),
    # Jaringan
    ('DS1018GMP', 'net', 'Switch PoE', '16 port PoE+', ['Budget PoE 250 W', '2 combo SFP/RJ45', 'Extend mode & PoE auto recovery'], 'Gigabit'),
    ('DS110GMP', 'net', 'Switch PoE', '8 port PoE+', ['Budget PoE 123 W', '1 RJ45 + 2 combo SFP/RJ45', 'PoE auto recovery'], 'Gigabit'),
    ('DS108GP', 'net', 'Switch PoE', '8 port PoE+', ['Budget PoE 65 W', 'Extend mode'], 'Gigabit'),
    ('DS105GP', 'net', 'Switch PoE', '4 port PoE+', ['Budget PoE 65 W', '1 port uplink'], 'Gigabit'),
    ('DS111P', 'net', 'Switch PoE', '8 port PoE+', ['Budget PoE 65 W', '2 GE + 1 SFP uplink', 'Extend mode'], '10/100 Mbps'),
    ('DS106P', 'net', 'Switch PoE', '4 port PoE+', ['Budget PoE 67 W', '2 port uplink', 'Extend mode'], '10/100 Mbps'),
    ('EAP680', 'net', 'Access point', 'Wi-Fi 6', ['Hingga 4804 + 1148 Mbps', '512 klien', 'Port 2,5 GbE PoE+'], 'Omada'),
    ('EAP683 UR', 'net', 'Access point', 'Wi-Fi 6', ['Hingga 4804 + 1148 Mbps', '512 klien', 'Port 2,5 GbE PoE+'], 'Omada'),
    ('EAP613', 'net', 'Access point', 'Wi-Fi 6', ['Hingga 1201 + 574 Mbps', '250+ klien', 'PoE 802.3at'], 'Omada'),
    ('EAP610', 'net', 'Access point', 'Wi-Fi 6', ['Hingga 1201 + 574 Mbps', '256 klien', 'PoE 802.3at'], 'Omada'),
    ('EAP245', 'net', 'Access point', 'Wi-Fi 5', ['Hingga 1300 + 450 Mbps', '220+ klien', '2 port gigabit'], 'Omada'),
    ('EAP215-Bridge KIT', 'net', 'Wireless bridge', '5 GHz, 867 Mbps', ['Jarak 5 km+', '3 port gigabit', 'Passive PoE / DC'], 'IP65'),
    ('EAP211-Bridge KIT', 'net', 'Wireless bridge', '5 GHz, 867 Mbps', ['Jarak 1 km+', '3 port gigabit', 'Passive PoE / DC'], 'IP65'),
    ('EAP115-Bridge KIT', 'net', 'Wireless bridge', '5 GHz, 300 Mbps', ['Jarak 5 km+', '3 port 10/100', 'Passive PoE / DC'], 'IP65'),
    # Aksesori
    ('VJB-300', 'acc', 'Junction box', 'Semua kamera VIGI', ['Tahan air', 'Bodi metal'], 'Aksesori pemasangan'),
    ('VJB-305', 'acc', 'Junction box', 'Kamera VIGI', ['Aluminium, tahan air', 'Kabel tersembunyi rapi'], 'Aksesori pemasangan'),
    ('VJB-240', 'acc', 'Junction box', 'Bullet & turret', ['Tahan air', 'Bodi metal'], 'Aksesori pemasangan'),
]

VIGI_IMG = root / 'assets/img/vigi'
CAT_IMG = {c: img for c, _, _, img in CATS}

def photo(m, cat):
    """Foto resmi model; kalau tidak ada, foto model sekeluarga (mis. S285Z -> S285), lalu foto kategori."""
    slug = re.sub(r'[^a-z0-9]+', '-', m.lower()).strip('-')
    if (VIGI_IMG / f'{slug}.webp').exists():
        return f'/assets/img/vigi/{slug}.webp'
    mm = re.match(r'([a-z]+)(\d+)', slug)
    if mm:
        num = mm.group(2)
        for pre in (mm.group(1), 's', 'c', 'nvr'):
            if (VIGI_IMG / f'{pre}{num}.webp').exists():
                return f'/assets/img/vigi/{pre}{num}.webp'
        sib = sorted(VIGI_IMG.glob(f'*{num}*.webp'))
        if sib and cat != 'net':
            return f'/assets/img/vigi/{sib[0].name}'
    img = CAT_IMG.get(cat)
    return f'/assets/img/hardware/{img}.webp' if img else '/assets/img/partners/tplink-v2.png'

def name(m):
    return m if m.startswith(('DS', 'EAP')) else f'VIGI {m}'

def item(m, cat, series, head, specs, prot):
    pic = f'<div class="vg-pic"><img alt="{e(name(m))}" height="110" loading="lazy" src="{photo(m, cat)}"/></div>'
    msg = f'Halo Altora, saya ingin tahu ketersediaan {name(m)}.'
    lis = ''.join(f'<li>{e(s)}</li>' for s in specs)
    return (f'<article class="vg-item" data-cat="{cat}" id="{e(m.lower().replace(" ", "-"))}">'
            f'{pic}<div class="vg-top"><small>{e(series)}</small><h3>{e(name(m))}</h3><p class="vg-head">{e(head)}</p></div>'
            f'<ul>{lis}</ul><p class="vg-prot">{e(prot)}</p>'
            f'<div class="vg-act"><button class="cart-add cart-add-sm" data-cart-id="vigi-{e(m.lower().replace(" ", "-"))}" data-cart-img="{e(photo(m, cat))}" '
            f'data-cart-meta="{e(series)}" data-cart-name="{e(name(m))}" type="button"><span aria-hidden="true">+</span><span class="cart-add-label">Tambah ke keranjang</span></button>'
            f'<a class="vg-ask" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Tanya stok</a></div></article>')

counts = {c: sum(1 for x in M if x[1] == c) for c, *_ in CATS}
filters = (f'<button aria-pressed="true" data-filter="all" type="button">Semua <span>{len(M)}</span></button>'
           + ''.join(f'<button aria-pressed="false" data-filter="{c}" type="button">{e(t)} <span>{counts[c]}</span></button>' for c, t, _, _ in CATS))
groups = ''
for c, t, lead, img in CATS:
    pic = f'<img alt="{e(t)} VIGI" loading="lazy" src="/assets/img/hardware/{img}.webp"/>' if img else ''
    groups += (f'<section class="vg-group" data-group="{c}" id="{c}"><div class="vg-ghead">{pic}<div><h2>{e(t)}</h2><p>{e(lead)}</p></div></div>'
               f'<div class="vg-grid">{"".join(item(*x) for x in M if x[1] == c)}</div></section>')

n_cam = sum(counts[c] for c in ('dome', 'bullet', 'turret', 'pt', 'fisheye'))
body = f'''<main class="ct-page svd-page vg-page">
<section class="svd-hero"><div class="ct-wrap">
<nav aria-label="Breadcrumb" class="vg-crumb"><a href="/">Beranda</a> / <a href="/katalog">Katalog</a> / <span>CCTV VIGI</span></nav>
<p class="eyebrow eyebrow-purple">Katalog lengkap · Partner resmi VIGI</p>
<h1>Katalog CCTV VIGI: {n_cam} kamera, NVR, dan perlengkapannya</h1>
<p class="ct-lead">Semua model VIGI by TP-Link yang kami sediakan, pasang, dan rawat di Samarinda, Balikpapan, dan Kalimantan Timur. Tidak yakin tipe mana yang cocok? Kirim denah atau foto lokasi, kami bantu hitung kebutuhannya.</p>
<div class="vg-cta"><a class="btn btn-purple" href="{WA}{quote("Halo Altora, saya ingin konsultasi kebutuhan CCTV VIGI untuk lokasi saya.")}" rel="noopener" target="_blank">Konsultasi CCTV →</a><a class="pd-link" href="/services/pengadaan-instalasi-maintenance">Instalasi &amp; maintenance</a></div>
</div></section>
<section class="svd-sec vg-legend"><div class="ct-wrap"><dl>
<div><dt>Aurora</dt><dd>Paling terang di kondisi gelap, gambar tetap berwarna.</dd></div>
<div><dt>Insight</dt><dd>AI dan kualitas gambar terbaik, bodi metal.</dd></div>
<div><dt>Eco &amp; EasyCam</dt><dd>Hemat dan mudah dipakai untuk rumah, toko, dan kantor kecil.</dd></div>
<div><dt>InSight S (2025)</dt><dd>Generasi proyek terbaru: ColorPro 2.0, zoom bermotor, PTZ, dan ANPR.</dd></div>
<div><dt>Kode</dt><dd>2 = dome, 3 = bullet, 4 = turret, 5 = pan tilt, 6 = fisheye. Angka kedua = megapiksel. I = inframerah, Z = zoom, S = ColorPro, W = Wi-Fi.</dd></div>
</dl></div></section>
<section class="svd-sec"><div class="ct-wrap">
<div aria-label="Filter kategori VIGI" class="hwi-filter vg-filter" role="group">{filters}</div>
{groups}
<p class="vg-note">Daftar model mengikuti situs resmi VIGI Indonesia (2026), VIGI Product Guide 2024, dan roadmap VIGI. Foto produk dari VIGI. Model seri InSight S dirilis bertahap; ketersediaan kami konfirmasi saat Anda bertanya. Spesifikasi dapat berubah sesuai versi produk. Ketersediaan stok: hubungi kami lewat chat.</p>
</div></section>
</main>'''

ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Katalog CCTV VIGI Altora Indonesia', 'url': SITE + '/katalog-cctv-vigi',
      'numberOfItems': len(M),
      'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                           'item': {'@type': 'Product', 'name': name(x[0]), 'brand': {'@type': 'Brand', 'name': 'TP-Link' if x[0].startswith(('DS', 'EAP')) else 'VIGI'},
                                    'category': x[2], 'description': f'{x[3]}. ' + ', '.join(x[4]) + '.'}}
                          for i, x in enumerate(M)]}
title = 'Katalog CCTV VIGI Lengkap | Altora Samarinda & Balikpapan'
desc = f'Semua model CCTV VIGI: {n_cam} kamera dome, bullet, turret, pan tilt, fisheye, plus NVR, kit, decoder, dan solar. Pengadaan & pemasangan di Samarinda dan Balikpapan.'
page = shell(title, desc, '/katalog-cctv-vigi', SITE + '/assets/img/hardware/vigi-dome.webp', ld, body)
page = page.replace('</body>', '<script defer="" src="/assets/js/vigi-filter.js?v=20261014"></script></body>')
(root / 'katalog-cctv-vigi.html').write_text(page, encoding='utf-8')
update_sitemap(['/katalog-cctv-vigi'])
print('katalog-cctv-vigi.html dibuat:', len(M), 'model,', n_cam, 'kamera')
