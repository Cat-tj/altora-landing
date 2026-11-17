"""Halaman SEO per aplikasi Altora, satu halaman per kebutuhan bisnis (kata kunci berbahasa Indonesia):
/aplikasi-toko (Store), /aplikasi-pertambangan (FieldOps), /aplikasi-manajemen-proyek (Office), /aplikasi-hris (Teams),
/aplikasi-monitoring-server (Control Center), /aplikasi-perkantoran (Word, Sheets, Slides).
Isi: masalah, alur, fitur, cocok untuk, screenshot (data contoh), FAQ, dan schema SoftwareApplication + FAQPage + Breadcrumb.
Jalankan lewat scripts/build_all.sh (setelah build_aplikasi.py)."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA
from build_aplikasi import APPS, pic, cta_buttons, wa_alt

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(t, quote=True)

PAGES = {
    'store': dict(
        url='/aplikasi-toko', apps=['store'], crumb='Aplikasi toko', sub='Inventory, sales and point of sale',
        title='Aplikasi Toko & Distributor: Stok, PO, Surat Jalan | Altora',
        desc='Aplikasi toko dan distributor: stok FIFO, nomor PO pembeli, penawaran jadi nota, invoice dan surat jalan PDF, piutang, utang, dan laporan laba.',
        eyebrow='Altora Store · aplikasi toko & distributor',
        h1='Aplikasi toko dan distributor untuk stok, PO pembeli, invoice, dan surat jalan.',
        lead='Ganti catatan manual dan Excel dengan satu sistem: stok dengan barcode, penawaran yang jadi nota, nomor PO pembeli di setiap invoice, surat jalan, piutang dan utang dengan jatuh tempo, sampai laporan laba dan pajak. Dibuka dari komputer kasir maupun HP, dan bisa dicoba gratis lewat demo pribadi.',
        pains=[('Stok di Excel tidak cocok dengan gudang', 'Barang tercatat ada padahal sudah habis, atau sebaliknya, karena barang masuk dan keluar tidak dicatat di satu tempat.'),
               ('PO pembeli tercecer', 'Nomor PO dari pembeli proyek atau instansi ada di chat dan kertas, sehingga sulit dicocokkan saat menagih.'),
               ('Nota, surat jalan, dan invoice diketik ulang', 'Data yang sama ditulis berkali-kali di dokumen berbeda, dan salah ketik baru ketahuan saat barang sampai.'),
               ('Piutang dan utang lewat jatuh tempo', 'Tidak ada pengingat tagihan yang mendekati atau lewat jatuh tempo, jadi arus kas sulit ditebak.')],
        flow_title='Alur dari penawaran sampai lunas', flow_sub='Satu data mengalir ke semua dokumen, tanpa ketik ulang.',
        flow=[('Penawaran harga', 'Kirim surat penawaran PDF ke calon pembeli.'), ('PO pembeli', 'Nomor PO pembeli dicatat di penjualan dan tampil di invoice.'),
              ('Nota & surat jalan', 'Penawaran dijadikan penjualan; stok berkurang otomatis dengan FIFO, surat jalan dicetak.'),
              ('Invoice & tagihan', 'Invoice PDF, surat tagihan, dan kwitansi dari penjualan yang belum lunas.'),
              ('Lunas & laporan', 'Pembayaran tercatat; omzet, laba, piutang, dan stok terbaru terlihat di laporan.')],
        fit_sub='Bisnis yang menjual barang dengan kode atau nomor part, tunai maupun tempo.',
        fit=['Distributor dan grosir', 'Toko spare part dan bearing', 'Toko bangunan dan material', 'Toko alat teknik dan kebutuhan industri', 'Toko yang melayani proyek, perusahaan, atau instansi dengan PO'],
        faq=[('Apa itu aplikasi toko Altora Store?', 'Altora Store adalah sistem toko dan distributor berbasis web untuk mencatat stok, pembelian, penjualan, penawaran, nomor PO pembeli, invoice, surat jalan, dan laporan dalam satu aplikasi.'),
             ('Apakah cocok untuk distributor dengan banyak pembeli tempo?', 'Cocok. Piutang dicatat per pembeli dengan jatuh tempo dan nomor PO, lengkap dengan surat tagihan dan kwitansi.')],
        cta='Lihat aplikasi toko ini langsung', link='Untuk toko & distributor'),
    'fieldops': dict(
        url='/aplikasi-pertambangan', apps=['fieldops'], crumb='Aplikasi pertambangan & migas', sub='Field operations, HSE and asset management',
        title='Aplikasi Pertambangan & Migas: HSE, PTW, Aset | Altora',
        desc='Aplikasi lapangan tambang dan migas: Permit to Work, JSA, insiden, CAPA, aset berat, sertifikasi dan MCU kru, legalitas, dan anggaran AFE per site.',
        eyebrow='Altora FieldOps · tambang & migas',
        h1='Aplikasi operasional lapangan untuk pertambangan dan migas.',
        lead='Kelola site dan sumur, izin kerja (Permit to Work), insiden dan CAPA, aset berat, sertifikasi kru, legalitas, dan anggaran dari satu sistem, dengan peringatan otomatis saat izin, sertifikat, atau perawatan jatuh tempo.',
        pains=[('Izin kerja masih di kertas dan grup chat', 'Sulit memastikan setiap pekerjaan berisiko sudah diverifikasi HSE dan disetujui sebelum dimulai.'),
               ('Sertifikat dan MCU kru kedaluwarsa diam-diam', 'Kru ditugaskan ke site padahal sertifikat wajib atau hasil MCU-nya sudah tidak berlaku.'),
               ('Perawatan alat berat terlambat', 'Jadwal perawatan berbasis jam operasi dan masa berlaku sertifikat alat dicatat terpisah dan mudah terlewat.'),
               ('Serapan anggaran baru diketahui akhir bulan', 'Biaya per sumur atau site tidak terlihat sampai rekap akuntansi selesai.')],
        flow_title='Alur izin kerja (Permit to Work)', flow_sub='Setiap tahap tercatat dengan nama dan waktu.',
        flow=[('Diajukan', 'Pemohon mengisi jenis pekerjaan, lokasi, dan masa berlaku.'), ('Diverifikasi HSE', 'HSE Officer memeriksa analisis bahaya dan pengendaliannya.'),
              ('Disetujui Field Manager', 'Pekerjaan hanya bisa dimulai setelah disetujui.'), ('Aktif', 'Izin yang lewat masa berlaku ditandai di overview.'),
              ('Ditutup & serah terima', 'Pekerjaan selesai dan area diserahkan kembali.')],
        fit_sub='Organisasi dengan pekerjaan lapangan berisiko dan banyak aset di beberapa site.',
        fit=['Kontraktor pertambangan', 'Operator dan kontraktor migas', 'Kontraktor pengeboran dan jasa penunjang', 'Perusahaan alat berat dan rental', 'Proyek konstruksi di lokasi terpencil'],
        faq=[('Apakah Altora FieldOps mendukung Permit to Work dan JSA?', 'Ya. Izin kerja mengikuti alur diajukan, diverifikasi HSE, disetujui Field Manager, aktif, ditutup, dan serah terima, lengkap dengan JSA, insiden, CAPA, toolbox meeting, dan limbah B3.'),
             ('Apakah bisa memantau sertifikat dan MCU kru?', 'Bisa. Matriks sertifikasi dan status MCU tiap kru dipantau, dan penugasan ke site diblokir bila sertifikat wajib kedaluwarsa atau kru tidak fit.')],
        cta='Lihat FieldOps langsung', link='Untuk tambang & migas'),
    'office': dict(
        url='/aplikasi-manajemen-proyek', apps=['office'], crumb='Aplikasi manajemen proyek', sub='Project management and office operations',
        title='Aplikasi Manajemen Proyek & Kantor | Altora Office',
        desc='Aplikasi manajemen proyek dan kantor: papan Kanban, tugas, dokumen, permintaan barang, inventaris, pengeluaran, HRIS, hak akses, dan audit log.',
        eyebrow='Altora Office · manajemen proyek & kantor',
        h1='Aplikasi manajemen proyek, tugas, dan operasional kantor.',
        lead='Satukan proyek, tugas, permintaan barang, inventaris, pengeluaran, dan data karyawan dalam satu aplikasi, dengan peran dan hak akses yang jelas serta laporan harian yang bisa dibantu asisten AI.',
        pains=[('Progres proyek tersebar di chat', 'Siapa mengerjakan apa dan sudah sampai mana harus ditanyakan satu per satu.'),
               ('Permintaan barang dan pengeluaran di kertas', 'Persetujuan lambat dan sulit ditelusuri saat diperiksa.'),
               ('Laporan harian ditagih manual', 'Pimpinan menunggu rekap, tim menghabiskan waktu menyusunnya.'),
               ('Data karyawan dan kontrak di file terpisah', 'Informasi penting sulit dicari saat dibutuhkan.')],
        flow_title='Dari proyek sampai laporan', flow_sub='Semua tercatat di satu tempat, sesuai peran masing-masing.',
        flow=[('Proyek dibuat', 'Tim, tenggat, dan dokumen proyek disiapkan.'), ('Tugas di papan Kanban', 'Tugas bergerak dari backlog sampai selesai.'),
              ('Permintaan & pengeluaran', 'Barang dan biaya diajukan dari dalam aplikasi.'), ('Persetujuan', 'Disetujui sesuai peran dan hak akses.'),
              ('Laporan & audit', 'Ringkasan progres dan jejak perubahan siap dibaca pimpinan.')],
        fit_sub='Tim yang menjalankan banyak proyek dan pekerjaan kantor sekaligus.',
        fit=['Software house dan agensi', 'Kontraktor dan konsultan', 'Perusahaan jasa dengan banyak proyek', 'Kantor cabang dan instansi', 'Tim operasional dan administrasi'],
        faq=[('Apakah ada papan Kanban untuk tugas?', 'Ada. Setiap proyek punya papan Kanban, daftar tugas, anggota tim, dokumen, dan ringkasan progres.'),
             ('Apakah hak akses bisa diatur per peran?', 'Bisa. Peran dan hak akses diatur di menu Admin, dan setiap perubahan tercatat di audit log.')],
        cta='Lihat Altora Office langsung', link='Untuk manajemen proyek'),
    'teams': dict(
        url='/aplikasi-hris', apps=['teams'], crumb='Aplikasi HRIS', sub='HRIS, KPI and leave management',
        title='Aplikasi HRIS: KPI Karyawan & Cuti Online | Altora Teams',
        desc='Aplikasi HRIS: KPI karyawan dengan bobot per departemen, persetujuan capaian, cuti online, kalender kerja, analitik, dan ekspor Excel atau PDF.',
        eyebrow='Altora Teams · HRIS & kinerja',
        h1='Aplikasi HRIS untuk KPI karyawan, cuti online, dan kalender kerja.',
        lead='Tetapkan KPI per departemen dengan bobot, terima capaian dari karyawan, tinjau dan setujui, lalu pantau hasilnya di dasbor. Cuti diajukan dan disetujui online, dan jadwal kerja tim terlihat di satu kalender.',
        pains=[('KPI di spreadsheet berbeda versi', 'Setiap departemen punya file sendiri, dan bobotnya tidak pernah pas 100%.'),
               ('Cuti diajukan lewat chat', 'Sisa cuti dihitung manual dan persetujuan sulit ditelusuri.'),
               ('Atasan sulit melihat pekerjaan tim', 'Siapa mengerjakan apa dan kapan tenggatnya tidak terlihat di satu tempat.'),
               ('Laporan kinerja makan waktu', 'Rekap akhir bulan disusun ulang dari banyak sumber.')],
        flow_title='Alur KPI dan penilaian', flow_sub='Dari target sampai laporan, tanpa rekap manual.',
        flow=[('KPI ditetapkan', 'Target, satuan, jadwal, dan bobot per departemen.'), ('Capaian diisi', 'Karyawan mengirim capaian sesuai periode.'),
              ('Ditinjau atasan', 'Disetujui atau dikembalikan dengan catatan.'), ('Dasbor & analitik', 'Pencapaian per KPI, orang, dan departemen.'),
              ('Ekspor laporan', 'Rekap siap diekspor ke Excel atau PDF.')],
        fit_sub='Organisasi yang ingin kinerja tim terukur dan administrasi SDM lebih rapi.',
        fit=['Perusahaan dengan beberapa departemen', 'Instansi dan BUMD', 'Program dan proyek dengan target terukur', 'Tim penjualan dan marketing', 'Perusahaan dengan tim di beberapa kota'],
        faq=[('Apakah karyawan bisa mengajukan cuti dari HP?', 'Bisa. Altora Teams berbasis web, jadi pengajuan cuti, capaian KPI, dan persetujuan bisa dilakukan dari HP.'),
             ('Apakah bobot KPI bisa diatur per departemen?', 'Bisa. Bobot KPI diatur per departemen dan aplikasi menandai departemen yang totalnya belum 100%.')],
        cta='Lihat Altora Teams langsung', link='Untuk HRIS & KPI'),
    'control-center': dict(
        url='/aplikasi-monitoring-server', apps=['control-center'], crumb='Aplikasi monitoring server', sub='Server, website and job monitoring',
        title='Aplikasi Monitoring Server & Website | Altora',
        desc='Pantau server, website, SSL, cron job, dan agen AI dari satu layar, dengan insiden otomatis dan peringatan WhatsApp, plus workspace proyek dan papan Kanban.',
        eyebrow='Altora Control Center · monitoring',
        h1='Monitoring server, website, dan cron job dengan peringatan WhatsApp.',
        lead='Satu layar untuk CPU, RAM, disk, container, status dan kecepatan website, masa berlaku SSL, serta jadwal tugas. Saat masalah menetap, insiden dibuka dan Anda dikabari lewat WhatsApp; saat pulih, insiden ditutup otomatis.',
        pains=[('Website mati, tahu dari pelanggan', 'Gangguan baru diketahui setelah ada yang mengeluh.'),
               ('Sertifikat SSL habis tanpa pemberitahuan', 'Pengunjung melihat peringatan keamanan di browser.'),
               ('Cron backup gagal diam-diam', 'Cadangan ternyata tidak berjalan saat dibutuhkan.'),
               ('Banyak server, banyak panel', 'Memeriksa kondisi semua mesin berarti membuka banyak aplikasi.')],
        flow_title='Dari gejala sampai pulih', flow_sub='Peringatan hanya untuk masalah yang benar-benar menetap.',
        flow=[('Daftarkan', 'Server, website, dan jadwal tugas ditambahkan lewat konfigurasi.'), ('Pantau berkala', 'Status, waktu respons, dan sumber daya dicek terus.'),
              ('Insiden dibuka', 'Saat masalah menetap, bukan sekadar kedip sesaat.'), ('Kabar WhatsApp', 'Satu pesan per putaran, dibatasi agar tidak membanjiri.'),
              ('Pulih & tercatat', 'Insiden ditutup otomatis dan riwayatnya tersimpan.')],
        fit_sub='Siapa pun yang bertanggung jawab atas server dan website yang harus selalu menyala.',
        fit=['Software house dan agensi web', 'Tim IT internal', 'Pemilik website dan toko online', 'Pengelola server kantor atau Raspberry Pi', 'Instansi dengan banyak situs'],
        faq=[('Apakah bisa memantau masa berlaku SSL?', 'Bisa. Setiap website dipantau status HTTP, waktu respons, uptime, dan masa berlaku sertifikat SSL-nya.'),
             ('Apakah peringatan dikirim lewat WhatsApp?', 'Ya. Insiden dibuka saat masalah menetap dan ditutup saat pulih, dengan pesan WhatsApp yang dibatasi jumlahnya per jam.')],
        cta='Lihat Control Center langsung', link='Untuk monitoring server'),
    'suite': dict(
        url='/aplikasi-perkantoran', apps=['word', 'sheets', 'slides'], crumb='Aplikasi perkantoran', sub='Office suite',
        title='Aplikasi Perkantoran: Dokumen, Lembar Kerja, Presentasi | Altora',
        desc='Aplikasi perkantoran berbahasa Indonesia: Altora Word (.docx), Altora Sheets (.xlsx), dan Altora Slides (.pptx), dengan ekspor PDF.',
        eyebrow='Altora Word, Sheets & Slides · perkantoran',
        h1='Aplikasi perkantoran native untuk dokumen, lembar kerja, dan presentasi.',
        lead='Tiga aplikasi dengan alur kerja yang sudah familier: Altora Word untuk dokumen, Altora Sheets untuk lembar kerja, dan Altora Slides untuk presentasi. Membuka dan menyimpan .docx, .xlsx, dan .pptx, dengan antarmuka Bahasa Indonesia.',
        basis='Dikembangkan dari proyek open-source WordCraft, GridCraft, dan DeckCraft (lisensi MIT atau Apache-2.0), disesuaikan oleh Altora. Altora Slides masih dalam pengembangan awal.',
        pains=[('File dari mitra harus tetap terbuka', 'Dokumen, lembar kerja, dan presentasi yang diterima harus bisa dibuka dan disimpan dengan format yang sama.'),
               ('Komputer kantor terasa berat', 'Aplikasi yang lambat membuat pekerjaan sederhana memakan waktu.'),
               ('Antarmuka berbahasa asing', 'Staf lebih cepat bekerja dengan menu berbahasa Indonesia.'),
               ('Templat dokumen tidak seragam', 'Setiap orang memakai format sendiri untuk surat, laporan, dan presentasi.')],
        flow_title='Tiga aplikasi, satu gaya kerja', flow_sub='Pita menu, pintasan, dan format file yang sudah dikenal.',
        flow=[('Altora Word', 'Dokumen .docx, gaya, panel navigasi, ekspor PDF.'), ('Altora Sheets', 'Lembar kerja .xlsx, 500+ fungsi, grafik, PivotTable.'),
              ('Altora Slides', 'Presentasi .pptx, tema, animasi, mode tayang.')],
        fit_sub='Organisasi yang ingin aplikasi perkantoran yang ringan dan bisa disesuaikan.',
        fit=['Kantor dan instansi', 'Sekolah dan kampus', 'Usaha kecil dan menengah', 'Tim yang bertukar file .docx, .xlsx, dan .pptx dengan mitra', 'Organisasi yang butuh templat dokumen seragam'],
        modules=APPS['word']['modules'][:3] + APPS['sheets']['modules'][:3] + APPS['slides']['modules'][:3],
        faq=[('Apakah bisa membuka file Word, Excel, dan PowerPoint?', 'Bisa. Altora Word membuka dan menyimpan .docx, Altora Sheets memakai .xlsx sebagai format asli, dan Altora Slides membuka dan menyimpan .pptx.'),
             ('Apakah antarmukanya berbahasa Indonesia?', 'Altora Word dan Altora Sheets tersedia dengan antarmuka Bahasa Indonesia, dan bahasa bisa diganti di pengaturan.')],
        cta='Lihat aplikasi perkantoran Altora', link='Untuk perkantoran'),
}


def build(key, p):
    apps = [APPS[k] for k in p['apps']]
    mods = p.get('modules') or apps[0]['modules']
    shots = [s for a in apps for s in a['shots']]
    faq = p['faq'] + [qa for a in apps for qa in a['faq']]
    seen = set()
    faq = [qa for qa in faq if not (qa[0] in seen or seen.add(qa[0]))]
    name = ', '.join(a['name'] for a in apps)
    demo = WA + quote(f'Halo Altora, saya ingin minta demo {name}.')
    prim = cta_buttons(apps[0]) if len(apps) == 1 else f'<a class="btn btn-purple" href="{demo}" rel="noopener" target="_blank">Minta demo</a>'
    wa = wa_alt(apps[0]) if len(apps) == 1 else ''
    pains = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in p['pains'])
    flow = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in p['flow'])
    modh = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in mods)
    fit = ''.join(f'<li>{e(x)}</li>' for x in p['fit'])
    gal = ''.join(f'<div class="ap2-feat"><div class="ap2-feat-txt"><h3>{e(t)}</h3></div>{pic(sid, alt)}</div>' for sid, alt, t in shots[1:])
    faqh = ''.join(f'<details><summary>{e(q)}</summary><p>{e(x)}</p></details>' for q, x in faq)
    basis = p.get('basis') or apps[0].get('basis')
    basis = f'<p style="font-size:.875rem;max-width:56ch;color:#5A6785;margin-top:14px">{e(basis)}</p>' if basis else ''
    details = ''.join(f'<a class="svd-link" href="/aplikasi/{k}">Detail {e(APPS[k]["name"])}</a>' for k in p['apps'])
    url = p['url']
    ld = {'@context': 'https://schema.org', '@graph': [
        *[{'@type': 'SoftwareApplication', 'name': a['name'], 'url': SITE + url, 'description': a['short'],
           'applicationCategory': 'BusinessApplication', 'applicationSubCategory': p['sub'], 'operatingSystem': a.get('os') or 'Web',
           'image': SITE + '/assets/img/apps/' + a['shots'][0][0] + '.webp', 'inLanguage': 'id', 'featureList': [t for t, _ in a['modules']],
           'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': SITE + '/'}} for a in apps],
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Aplikasi', 'item': SITE + '/aplikasi'}, {'@type': 'ListItem', 'position': 3, 'name': p['crumb'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in faq]}]}
    body = f'''<main class="ct-page svd-page ap2-page">
<section class="svd-hero"><div class="ct-wrap ap2-hero">
<div class="ap2-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/aplikasi">Aplikasi</a><span>/</span><span>{e(p["crumb"])}</span></nav>
<p class="eyebrow eyebrow-purple">{e(p["eyebrow"])}</p><h1>{e(p["h1"])}</h1><p class="ct-lead">{e(p["lead"])}</p>{basis}
<div class="svd-actions">{prim}{details}</div></div>
{pic(shots[0][0], shots[0][1], True)}
</div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Masalah yang sering kami temui</h2><p>Tanda organisasi Anda butuh sistem yang lebih rapi.</p></div><ul>{pains}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>{e(p["flow_title"])}</h2><p>{e(p["flow_sub"])}</p></div><ol class="svd-steps st-flow">{flow}</ol></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Fitur utama</h2></div><div class="svd-dos">{modh}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Cocok untuk</h2><p>{e(p["fit_sub"])}</p></div><ul class="ap2-fitlist">{fit}</ul></div></section>
{f'<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Tampilan aplikasi</h2><p>Screenshot dari toko demo fiktif (CV Mitra Teknik Mandiri); semua datanya data contoh.</p></div><div class="ap2-feats">{gal}</div></div></section>' if gal else ''}
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faqh}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>{e(p["cta"])}</h2><p>Kami tunjukkan lewat demo singkat dan bahas penyesuaiannya untuk organisasi Anda.</p></div><div class="svd-actions">{prim}{wa}</div></div></section>
</main>'''
    return shell(p['title'], p['desc'], url, SITE + '/assets/img/apps/' + shots[0][0] + '.webp', ld, body)


if __name__ == '__main__':
    for key, p in PAGES.items():
        (root / (p['url'].lstrip('/') + '.html')).write_text(build(key, p), encoding='utf-8')
    update_sitemap([p['url'] for p in PAGES.values()])
    print('halaman SEO aplikasi:', ', '.join(p['url'] for p in PAGES.values()))
