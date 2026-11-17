"""Data portofolio proyek + komponen kartu (dipakai build_portofolio.py dan build_infra.py).
Sumber: konten lama Altora (4 proyek perangkat) dan halaman portofolio perusahaan saudara (17 proyek); teks ditulis ulang.
Hanya fakta dari sumber itu: tanpa harga, tanpa angka karangan, tanpa testimoni. Gambar di assets/img/portofolio/."""
import html

e = lambda t: html.escape(str(t), quote=True)

GROUPS = [
    ('infra', 'Infrastruktur, IoT & hardware', 'Perangkat, jaringan, kamera, dan sensor yang dipasang di lokasi.'),
    ('ai', 'AI & computer vision', 'Analitik kamera, pengenalan wajah, NLP, dan pembacaan data operasional.'),
    ('software', 'Software & data', 'Portal, dashboard, HRIS, antrian, dan sistem informasi untuk instansi dan perusahaan.'),
    ('web', 'Website', 'Website resmi dengan konten yang dikelola lewat CMS.'),
]

ICONS = {
    'store': '<path d="M4 9l1.5-5h13L20 9"/><path d="M5 9v11h14V9"/><path d="M9 20v-5h6v5"/>',
    'building': '<path d="M4 21V5l8-2v18"/><path d="M12 8h8v13"/><path d="M7 9h2M7 13h2M7 17h2M15 12h2M15 16h2"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    'truck': '<path d="M2.5 6.5h11v9h-11zM13.5 9.5h4l3 3.2v2.8h-7z"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'lock': '<rect height="10" rx="2" width="14" x="5" y="11"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'camera': '<path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/>',
    'sensor': '<circle cx="12" cy="12" r="2.2"/><path d="M8.2 8.2a5.4 5.4 0 0 0 0 7.6M15.8 8.2a5.4 5.4 0 0 1 0 7.6M5.4 5.4a9.3 9.3 0 0 0 0 13.2M18.6 5.4a9.3 9.3 0 0 1 0 13.2"/>',
    'helmet': '<path d="M4 16a8 8 0 0 1 16 0zM2 16h20v2H2zM12 8V5"/>',
    'face': '<path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><circle cx="12" cy="10.5" r="2.6"/><path d="M8 17c.8-1.9 2.2-2.8 4-2.8s3.2.9 4 2.8"/>',
    'route': '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
    'chart': '<path d="M4 20h16M7 16v-4M12 16V8M17 16v-7"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    'mic': '<rect height="11" rx="3" width="6" x="9" y="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    'map': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.2 3-5 6-5s5.4 1.8 6 5"/><circle cx="17" cy="9" r="2.4"/>',
    'queue': '<path d="M5 6h14M5 12h14M5 18h9"/><path d="M17 16l2 2 3-4"/>',
    'coin': '<circle cx="12" cy="12" r="8"/><path d="M12 8v8M9.5 10h4a1.5 1.5 0 0 1 0 3h-3a1.5 1.5 0 0 0 0 3H15"/>',
    'leaf': '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14z"/><path d="M5 19 13 11"/>',
    'layout': '<rect height="16" rx="2" width="18" x="3" y="4"/><path d="M3 9h18M9 9v11"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
}
icon = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[n]}</svg>'

IMG = '/assets/img/portofolio/'
# Urutan = urutan tampil di halaman /portofolio (per kelompok).
PROJECTS = [
    # ── Infrastruktur, IoT & hardware ──
    dict(slug='rm-payakumbuah', group='infra', icon='store', title='Jaringan, CCTV, dan POS rumah makan', client='RM Payakumbuah', year='',
         desc='Pengadaan dan pemasangan perangkat operasional rumah makan: kasir POS, CCTV multi-sudut, switch 24-port, access point untuk pelanggan, dan walkie talkie untuk dapur.',
         tags=['POS', 'CCTV', 'Jaringan', 'Radio']),
    dict(slug='fleet-radio-kapal', group='infra', icon='truck', title='GPS armada dan radio marine VHF', client='Logistik & maritim · Mahakam', year='',
         desc='Pemasangan GPS tracker untuk armada logistik tambang di Kaltim dan integrasi radio marine VHF untuk komunikasi transportasi perairan Mahakam.',
         tags=['GPS tracker', 'Radio VHF', 'Maritim'], link=('/blog/integrasi-erp-logistik-maritim-kaltim', 'Baca: ERP untuk logistik maritim')),
    dict(slug='fleet-management-tambang', group='infra', icon='truck', title='Fleet management armada hauling', client='Kontraktor tambang · Kaltim', year='2025', img='fleet-management-tambang.webp',
         desc='Telematik untuk armada hauling: posisi dan riwayat perjalanan, status unit, peringatan dan geofence, serta laporan operasi dalam satu dashboard.',
         tags=['Telematika', 'CAN-Bus', 'Geofence']),
    dict(slug='kios-mandiri-kelurahan', group='infra', icon='building', title='Anjungan layanan mandiri kelurahan', client='Pemerintahan & pelayanan', year='',
         desc='Rancangan hardware Anjungan Layanan Mandiri (Kios-K) layar sentuh, supaya pengurusan surat kependudukan berjalan tanpa antre.',
         tags=['Kios-K', 'Layar sentuh']),
    dict(slug='iot-monitoring-gudang', group='infra', icon='bell', title='Pemantau ruang server dan gudang', client='Industri & pergudangan', year='',
         desc='Sensor suhu, kelembapan, kebocoran, dan asap yang aktif sepanjang waktu, dengan notifikasi WhatsApp dan dashboard pusat.',
         tags=['IoT', 'Sensor', 'WhatsApp']),
    dict(slug='cctv-ai-farmasi-unmul', group='infra', icon='camera', title='Instalasi CCTV siap analitik AI, 50+ unit', client='Fakultas Farmasi Universitas Mulawarman', year='2025', img='cctv-ai-farmasi-unmul.webp',
         desc='Pemasangan lebih dari 50 kamera VIGI yang disiapkan untuk analitik AI dan pemantauan operasional, dikerjakan langsung di lokasi.',
         tags=['CCTV AI', 'VIGI', '50+ unit']),
    dict(slug='smartlock-farmasi-unmul', group='infra', icon='lock', title='Smartlock akses gedung kampus', client='Fakultas Farmasi Universitas Mulawarman', year='2025', img='smartlock-farmasi-unmul.webp',
         desc='Akses digital untuk ruang dan gedung kampus: kontrol akses, pemantauan perangkat, dan riwayat akses yang terhubung ke alur operasional.',
         tags=['IoT', 'Kontrol akses']),
    dict(slug='iot-monitoring-lahan-sawit', group='infra', icon='leaf', title='Pemantau cuaca dan kelembapan lahan', client='Perkebunan sawit · Kaltim', year='2025',
         desc='Kelembapan tanah, suhu, dan kelembapan udara dibaca dari sensor lewat jaringan LoRa, lalu tampil langsung di HP petugas lapangan.',
         tags=['Sensor', 'LoRa', 'Cuaca']),
    # ── AI & computer vision ──
    dict(slug='deteksi-apd-ai', group='ai', icon='helmet', title='Deteksi APD berbasis AI', client='PT Multi Harapan Utama', year='2025', img='deteksi-apd-ai.webp',
         desc='Analitik vision dari kamera untuk membantu memantau kepatuhan atribut keselamatan kerja, dengan pemantauan kejadian dan peringatan operasional.',
         tags=['AI', 'Vision', 'K3']),
    dict(slug='smart-attendance-unmul', group='ai', icon='face', title='Absensi face recognition', client='Universitas Mulawarman', year='2025',
         desc='Absensi otomatis dengan pengenalan wajah dari aliran kamera CCTV, lengkap dengan event kehadiran dan jejak audit.',
         tags=['Face recognition', 'CCTV', 'Mobile']),
    dict(slug='optimasi-rute-armada', group='ai', icon='route', title='Optimasi rute dan monitoring armada distribusi', client='Operator logistik · Balikpapan', year='2024',
         desc='Dukungan monitoring distribusi dan pembacaan rute armada untuk operasi logistik: GPS, visibilitas armada, dan pemantauan rute.',
         tags=['Route AI', 'GPS', 'Armada']),
    dict(slug='media-monitoring', group='ai', icon='chart', title='Dashboard media monitoring dan analitik isu', client='Intelligence Media Management', year='2024', img='media-monitoring.webp',
         desc='Dashboard untuk membaca isu dan aktivitas media, dengan pelacakan isu dan analitik sebagai bahan insight operasional.',
         tags=['NLP', 'Analitik']),
    dict(slug='sentiment-social-listening', group='ai', icon='chat', title='Analisis sentimen dan social listening', client='Platform analitik media sosial', year='2025', img='sentiment-social-listening.webp',
         desc='Analisis percakapan publik untuk membaca tema, sentimen, dan perkembangan isu, lengkap dengan pelaporan.',
         tags=['NLP', 'Social listening']),
    dict(slug='transkripsi-rapat', group='ai', icon='mic', title='Transkripsi rapat bahasa Indonesia', client='Korporasi & kampus · Kaltim', year='2025',
         desc='Transkripsi rapat berbahasa Indonesia yang berjalan di server sendiri, untuk catatan rapat dan pencarian informasi kembali.',
         tags=['ASR', 'NLP', 'On-prem']),
    # ── Software & data ──
    dict(slug='pompy-batara', group='software', icon='map', title='POMPy BATARA: portal one map dan dashboard daerah', client='Diskominfosandi Kab. Barito Utara', year='2025', img='pompy-batara.webp',
         desc='Portal peta tematik yang menyatukan data spasial dan tematik dari berbagai perangkat daerah, sebagai dasar akses informasi publik dan keputusan berbasis data. Kabupaten Barito Utara meraih Digital Innovation Award 2026 melalui POMPy BATARA.',
         tags=['Web', 'GIS', 'One Map'], link=('https://pompy.baritoutarakab.go.id', 'Buka situs POMPy BATARA')),
    dict(slug='dashboard-geospasial-dapodik', group='software', icon='map', title='Dashboard geospasial DAPODIK', client='Diskominfosandi Kab. Barito Utara', year='2024', img='dashboard-geospasial-dapodik.webp',
         desc='Peta sebaran sekolah dari data DAPODIK, dengan dashboard analitik untuk mendukung pengambilan keputusan di bidang pendidikan.',
         tags=['GIS', 'DAPODIK', 'Dashboard']),
    dict(slug='hris-mobile-payroll', group='software', icon='users', title='HRIS mobile: absensi, payroll, dan slip gaji', client='Bukit Baiduri Energi', year='2024', img='hris-mobile-payroll.webp',
         desc='Kehadiran, payroll, dan informasi karyawan dalam satu alur, dengan akses karyawan dari HP.',
         tags=['HRIS', 'Mobile', 'Payroll']),
    dict(slug='antrian-poliklinik', group='software', icon='queue', title='Sistem antrian dan pendaftaran poliklinik', client='Klinik & RS swasta · Samarinda', year='2024',
         desc='Alur pendaftaran dan antrian yang membuat operasional layanan klinik lebih tertata, dengan display operasional.',
         tags=['Web', 'Antrian', 'EMR']),
    dict(slug='lentera-koperasi', group='software', icon='coin', title='Lentera: penilaian kesehatan keuangan koperasi', client='BPR & koperasi · Kaltim', year='2023',
         desc='Platform web dan mobile untuk membaca indikator dan kondisi keuangan koperasi secara terstruktur, dengan monitoring dan pelaporan.',
         tags=['Web', 'Keuangan', 'Mobile']),
    # ── Website ──
    dict(slug='website-feb-unmul', group='web', icon='layout', title='Website dan sistem informasi fakultas', client='Fakultas Ekonomi dan Bisnis Universitas Mulawarman', year='2024', img='website-feb-unmul.webp',
         desc='Platform informasi fakultas dengan arsitektur informasi yang jelas, tampilan responsif, dan alur editorial untuk pengelolaan konten.',
         tags=['Web', 'CMS'], link=('https://feb.unmul.ac.id', 'Buka situs fakultas')),
    dict(slug='website-farmasi-unmul', group='web', icon='layout', title='Website resmi fakultas', client='Fakultas Farmasi Universitas Mulawarman', year='2023', img='website-farmasi-unmul.webp',
         desc='Website publik untuk struktur informasi, publikasi, dan pembaruan konten fakultas, dikelola lewat CMS.',
         tags=['Web', 'CMS'], link=('https://ff.unmul.ac.id', 'Buka situs fakultas')),
]
BY = {p['slug']: p for p in PROJECTS}

# Nama klien dan instansi (teks saja, tanpa logo).
CLIENT_NAMES = ['Pemkot Samarinda', 'Diskominfosandi Kab. Barito Utara', 'Universitas Mulawarman', 'ITK', 'STT Migas Balikpapan',
                'PT Adhi Karya', 'PT Astra International Tbk', 'RM Payakumbuah', '1Ci Enterprise', 'MBC Entertainment']

HOME_SLUGS = ['rm-payakumbuah', 'fleet-management-tambang', 'fleet-radio-kapal', 'deteksi-apd-ai', 'pompy-batara', 'hris-mobile-payroll']
INFRA_SLUGS = ['rm-payakumbuah', 'kios-mandiri-kelurahan', 'fleet-radio-kapal', 'iot-monitoring-gudang', 'deteksi-apd-ai', 'cctv-ai-farmasi-unmul',
               'smartlock-farmasi-unmul', 'iot-monitoring-lahan-sawit']


def card(p, mode='link'):
    """Kartu proyek bergaya Sentra: media 16:10, kecil (klien · tahun), judul, ringkasan, tag. Seluruh kartu menaut ke /portofolio/<slug>.
    mode 'full' = dipakai di /portofolio (data-kind untuk filter, id jangkar lama, animasi muncul); lainnya = beranda dan halaman lain."""
    if p.get('img'):
        media = f'<span class="pf-thumb"><img alt="" decoding="async" height="500" loading="lazy" src="{IMG}{e(p["img"])}" width="800"/></span>'
    else:
        media = f'<span class="pf-thumb pf-thumb-ico"><span class="pf-ico">{icon(p["icon"])}</span></span>'
    meta = e(p['client']) + (f' · {e(p["year"])}' if p['year'] else '')
    tags = ''.join(f'<span class="pf-tag">{e(t)}</span>' for t in p['tags'])
    body = f'<span class="pf-body"><small>{meta}</small><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><span class="pf-tags">{tags}</span></span>'
    extra = f' data-kind="{p["group"]}" id="{p["slug"]}"' if mode == 'full' else ''
    cls = 'pf-card pf-rv' if mode == 'full' else 'pf-card'
    return f'<a class="{cls}"{extra} href="/portofolio/{p["slug"]}">{media}{body}</a>'
