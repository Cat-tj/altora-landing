"""Halaman /aplikasi (hub) dan /aplikasi/<id> untuk aplikasi buatan Altora: Altora Office dan Altora Control Center.
Screenshot asli dari aplikasi yang berjalan dengan data contoh (tanpa data klien/server nyata) ada di assets/img/apps/.
Jalankan lewat scripts/build_all.sh."""
import html, json, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA
from site_data import ORG_ID, org

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(t, quote=True)
IMG = '/assets/img/apps/'

APPS = {
    'fieldops': dict(
        name='Altora FieldOps', tag='Operasional lapangan tambang dan migas', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora FieldOps: operasional lapangan tambang dan migas dalam satu sistem.',
        lead='Platform untuk mengelola site dan sumur, keselamatan kerja (HSE), aset berat, kru lapangan, legalitas, dan anggaran, dengan peringatan otomatis saat izin, sertifikat, atau perawatan jatuh tempo.',
        short='Kelola site, HSE dan izin kerja, aset berat, kru, dan anggaran lapangan tambang dan migas.',
        shots=[('fieldops-overview', 'Overview lapangan: hari tanpa LTI, izin kerja aktif, serapan anggaran, HSE, legalitas, kru, dan aset', 'Overview lapangan'),
               ('fieldops-hse', 'HSE dan K3LL: daftar Permit to Work dengan alur persetujuan', 'HSE dan izin kerja'),
               ('fieldops-wells', 'Daftar sumur dan site dengan kesiapan pre-spud', 'Sumur dan site'),
               ('fieldops-assets', 'Registri aset berat dengan sertifikat dan jam operasi', 'Aset berat')],
        modules=[('Sumur & site', 'Daftar sumur, wellpad, site tambang, dan basecamp sebagai pusat biaya, izin kerja, dan penugasan kru.'),
                 ('HSE / K3LL', 'Permit to Work dengan alur persetujuan, JSA, insiden, CAPA, toolbox meeting, dan limbah B3.'),
                 ('Aset berat', 'Registri rig dan alat berat, sertifikat, perawatan berbasis jam operasi, kalibrasi, dan mutasi antar site.'),
                 ('Kru lapangan', 'Matriks sertifikasi, medical check-up, roster, dan penugasan yang otomatis memeriksa kelayakan kru.'),
                 ('Legalitas & pre-spud', 'Pelacakan izin dan checklist kesiapan sebelum pengeboran, dengan peringatan masa berlaku.'),
                 ('AFE, akuntansi & pajak', 'Anggaran per sumur, jurnal, dan dokumen pajak dalam satu tempat.')],
        faq=[('Apakah cocok untuk tambang, bukan hanya migas?', 'Cocok. Modulnya mencakup site tambang dan basecamp, izin kerja, HSE, aset berat, dan kru, yang dipakai di kedua sektor.'),
             ('Apakah bisa mengikuti prosedur perusahaan kami?', 'Bisa. Alur persetujuan, jenis izin kerja, dan checklist disesuaikan dengan prosedur dan standar internal Anda.'),
             ('Apakah bisa dipasang di server kami sendiri?', 'Bisa. Aplikasi berjalan di server atau cloud pilihan Anda, sehingga data tetap di infrastruktur Anda.')]),
    'store': dict(
        name='Altora Store', tag='Sistem toko: stok, PO, nota, dan laporan', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Store: stok, PO, nota, dan surat jalan toko dalam satu sistem.',
        lead='Sistem toko berbasis web untuk menggantikan catatan manual dan Excel: stok dengan barcode atau QR, kasir dengan scan kamera HP, penawaran yang jadi penjualan, piutang pembeli dengan jatuh tempo, invoice dan surat jalan PDF, sampai laporan omzet, laba, dan pajak. Bisa dicoba gratis lewat demo pribadi tanpa daftar.',
        demo_url='https://store.altora.id/coba-demo', site_url='https://store.altora.id',
        short='Stok dengan barcode, kasir scan kamera, penawaran, piutang, invoice, surat jalan, dan laporan pajak toko. Bisa dicoba lewat demo gratis.',
        basis='Dibangun pertama untuk toko spare part bearing, dan bisa disesuaikan untuk toko bangunan, sparepart, alat teknik, grosir, atau distributor.',
        os='Web (komputer, tablet, dan HP)',
        shots=[('store-demo-dashboard', 'Beranda Altora Store: penjualan hari ini dan bulan ini, laba bersih, nilai stok, utang, dan piutang pembeli', 'Beranda dan ringkasan'),
               ('store-demo-piutang', 'Laporan piutang per pembeli dengan keterlambatan, sisa tagihan, dan surat tagihan PDF', 'Piutang per pembeli'),
               ('store-demo-penjualan', 'Daftar penjualan: nota, pembeli, status lunas, dan sisa tagihan', 'Penjualan dan nota'),
               ('store-demo-stok', 'Stok per nomor part dan merek, dengan penanda stok menipis dan habis', 'Stok per barang')],
        modules=[('Stok dan barang dengan barcode/QR', 'Stok per nomor part, merek, dan batch, lengkap dengan barcode atau QR per barang. Stok tidak bisa minus, harga pokok mengikuti batch yang benar-benar terjual (FIFO).'),
                 ('Kasir dan scan kamera', 'Penjualan tunai atau tempo di kasir; barcode di-scan dengan kamera HP Android, tanpa alat scanner tambahan. Info pembayaran QRIS bisa dicantumkan.'),
                 ('Penawaran jadi penjualan', 'Surat penawaran PDF yang bisa langsung dijadikan penjualan tanpa ketik ulang.'),
                 ('Pembelian dan utang pemasok', 'Catat pembelian dari pemasok dan utang yang harus dibayar, lengkap dengan jatuh tempo.'),
                 ('Piutang pembeli', 'Piutang dengan jatuh tempo, nomor PO pembeli, surat tagihan, dan kwitansi, supaya tagihan tidak tercecer.'),
                 ('Retur, biaya, dan stok opname', 'Retur penjualan dan pembelian, pencatatan biaya, dan stok opname untuk mencocokkan stok di sistem dengan barang di rak.'),
                 ('Dokumen PDF', 'Invoice atau nota, surat jalan, penawaran, dan surat dengan kop toko, dicetak dari data yang sama.'),
                 ('Laporan dan pajak', 'Laporan omzet dan laba, PPN 11%, serta PPh final 0,5% untuk UMKM dengan pemantauan batas PKP. Perhitungannya membantu, bukan pengganti konsultan pajak.'),
                 ('Impor Excel dan persetujuan pemilik', 'Stok awal bisa diimpor dari Excel. Diskon di atas batas tertentu butuh persetujuan pemilik; ada peran pemilik dan kasir serta audit log.'),
                 ('Profil perusahaan dan katalog', 'Opsional: halaman profil perusahaan dan katalog produk publik untuk toko Anda.')],
        faq=[('Bisakah saya mencoba dulu sebelum memakai?', 'Bisa. Tombol Coba demo di store.altora.id membuat toko demo pribadi dengan data contoh yang realistis. Tanpa daftar, data hanya untuk Anda, dan dihapus saat keluar atau setelah 30 menit tidak aktif.'),
             ('Apakah Altora Store bisa mencatat nomor PO dari pembeli?', 'Bisa. Nomor PO dicatat di penjualan dan piutang, tampil di invoice, dan membantu mencocokkan tagihan dengan PO pembeli.'),
             ('Apakah cocok untuk toko selain spare part bearing?', 'Cocok untuk toko yang menjual barang dengan nomor part atau kode, seperti toko bangunan, sparepart, alat teknik, grosir, dan distributor. Kami menyesuaikan tampilan dan dokumen dengan toko Anda.'),
             ('Apakah bisa dipakai dari HP?', 'Bisa. Aplikasi berbasis web, jadi bisa dibuka dari komputer kasir, tablet, maupun HP. Di HP Android, kamera bisa dipakai untuk scan barcode di kasir.'),
             ('Bagaimana dengan data stok lama di Excel?', 'Stok awal bisa diimpor dari file Excel.'),
             ('Apakah menghitung pajak?', 'Laporan mencakup PPN 11% dan PPh final 0,5% untuk UMKM, serta pemantauan batas PKP. Ini bantuan perhitungan; keputusan perpajakan tetap bersama konsultan pajak Anda.'),
             ('Di mana data toko disimpan?', 'Setiap bisnis mendapat instance sendiri di subdomain store-namabisnis.altora.id dengan logo dan warna sendiri. Data tersimpan permanen dan terpisah dari bisnis lain, dengan cadangan harian.')]),
    'office': dict(
        name='Altora Office', tag='Platform kerja internal', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Office: proyek, tim, dan operasional kantor di satu tempat.',
        lead='Platform internal untuk mengelola proyek dan tugas, permintaan barang, inventaris, pengeluaran, sampai HRIS. Dibangun dan dipakai sendiri oleh tim Altora; bisa dipasang di server Anda atau dipakai sebagai layanan.',
        short='Kelola proyek, tugas, HRIS, dan operasional kantor dari satu aplikasi.',
        shots=[('office-board', 'Papan Kanban per proyek dengan kolom, penanggung jawab, dan tenggat', 'Papan proyek'),
               ('office-project', 'Ringkasan proyek: progres, tugas yang perlu perhatian, tim, dan tenggat', 'Ringkasan proyek')],
        modules=[('Proyek & tugas (Altora Projek)', 'Papan Kanban, daftar tugas, anggota tim, dokumen, dan ringkasan progres per proyek.'),
                 ('Operasional', 'Permintaan barang, inventaris, pengeluaran, pencatat aktivitas, dan pemantauan domain serta VPS.'),
                 ('HRIS', 'Data karyawan, departemen, reimbursement, langganan, slip gaji, dan kontrak kerja.'),
                 ('Marketing', 'Kampanye, metrik iklan, dan pencatatan leads.'),
                 ('Admin', 'Peran dan hak akses, pengguna, audit log, dan pengaturan.'),
                 ('Asisten Raphael', 'Laporan harian dan pembaruan papan lewat asisten AI, dari dalam proyek.')],
        faq=[('Apakah Altora Office bisa dipasang di server kami sendiri?', 'Bisa. Aplikasi berjalan di server atau cloud pilihan Anda, sehingga data tetap di infrastruktur Anda.'),
             ('Apakah modulnya bisa dipilih?', 'Bisa. Proyek & tugas bisa dipakai sendiri, lalu HRIS atau operasional ditambahkan bertahap.'),
             ('Apakah bisa disesuaikan dengan proses kami?', 'Bisa. Kami menyesuaikan alur, peran, dan laporan sesuai cara kerja organisasi Anda.')]),
    'teams': dict(
        name='Altora Teams', tag='HRIS dan kinerja tim', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Teams: kinerja, cuti, dan jadwal kerja tim di satu tempat.',
        lead='HRIS untuk tim yang bertumbuh: pantau KPI dan hasil kerja tiap orang, kelola cuti dan persetujuan, serta lihat jadwal proyek dan tugas dalam satu kalender. Dibuat dan dipakai sendiri oleh tim Altora.',
        short='Kelola KPI, cuti, kalender kerja, dan persetujuan tim dari satu aplikasi.',
        shots=[('teams-overview', 'Dasbor eksekutif Altora Teams: KPI aktif, staf, departemen, dan pengajuan terbaru', 'Dasbor eksekutif'),
               ('teams-calendar', 'Kalender kerja bulanan dengan jadwal proyek dan tugas serta filter proyek, orang, dan departemen', 'Kalender kerja'),
               ('teams-kpis', 'Daftar KPI per departemen dengan bobot, target, jadwal, dan penanggung jawab', 'KPI dan bobot')],
        modules=[('Dasbor eksekutif', 'Ringkasan KPI aktif, staf, departemen, dan pengajuan yang menunggu tinjauan.'),
                 ('KPI & review', 'KPI per departemen dengan target, bobot, jadwal, dan penanggung jawab, lengkap dengan persetujuan hasil kerja.'),
                 ('Cuti & persetujuan', 'Pengajuan cuti, saldo, dan persetujuan atasan dalam satu alur.'),
                 ('Kalender kerja', 'Jadwal proyek dan tugas bulanan atau mingguan, bisa disaring per proyek, orang, dan departemen.'),
                 ('Tim & departemen', 'Data anggota, peran, dan struktur departemen.'),
                 ('Analitik & laporan', 'Pencapaian KPI dan rekap entri, bisa diekspor ke Excel atau PDF.')],
        faq=[('Apakah Altora Teams bisa dipasang di server kami sendiri?', 'Bisa. Aplikasi berjalan di server atau cloud pilihan Anda, sehingga data tetap di infrastruktur Anda.'),
             ('Apakah KPI dan alur persetujuannya bisa disesuaikan?', 'Bisa. Kami menyesuaikan jenis KPI, bobot, peran, dan alur persetujuan dengan cara kerja organisasi Anda.'),
             ('Apakah bisa dipakai bersama Altora Office?', 'Bisa. Keduanya saling melengkapi: Office untuk proyek dan operasional, Teams untuk kinerja dan cuti tim.')]),
    'word': dict(
        name='Altora Word', tag='Pengolah kata', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Word: menulis dan merancang dokumen dengan antarmuka Bahasa Indonesia.',
        lead='Pengolah kata native yang cepat, dengan pita menu, galeri gaya, dan panel navigasi yang sudah familier. Membuka dan menyimpan .docx, serta .odt, .rtf, .html, .md, dan mengekspor PDF.',
        short='Pengolah kata native dengan format .docx, gaya, panel navigasi, dan ekspor PDF.',
        basis='Dikembangkan dari proyek open-source WordCraft (lisensi MIT atau Apache-2.0), disesuaikan dan diindonesiakan oleh Altora.',
        os='macOS, Windows, Linux',
        shots=[('word-main', 'Altora Word: pita menu, galeri gaya, panel navigasi, dan halaman dokumen', 'Antarmuka Altora Word')],
        modules=[('Pita menu familier', 'Tab, grup, dan pintasan keyboard yang mengikuti alur pengolah kata yang sudah dikenal.'),
                 ('Gaya & panel navigasi', 'Galeri gaya dengan pratinjau langsung dan panel judul untuk berpindah antar bagian.'),
                 ('Format dokumen', 'Membuka dan menyimpan .docx; juga .odt, .rtf, .html, .md, dan .tex.'),
                 ('Ekspor PDF', 'PDF dengan teks yang bisa dipilih, tautan, dan penanda.'),
                 ('Antarmuka Bahasa Indonesia', 'Menu dan dialog tersedia dalam Bahasa Indonesia.'),
                 ('Cepat & ringan', 'Aplikasi native tanpa Electron, tetap lancar pada dokumen panjang.')],
        faq=[('Apakah bisa membuka file Word yang sudah ada?', 'Bisa. Altora Word membuka dan menyimpan format .docx, serta beberapa format lain seperti .odt dan .rtf.'),
             ('Apakah tersedia untuk Windows?', 'Basis kode yang sama dapat dibangun untuk macOS, Windows, dan Linux. Hubungi kami untuk versi yang tersedia.'),
             ('Apakah bisa disesuaikan untuk organisasi kami?', 'Bisa. Kami dapat menyesuaikan templat, bahasa, dan integrasi dengan sistem Anda.')]),
    'sheets': dict(
        name='Altora Sheets', tag='Lembar kerja', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Sheets: lembar kerja dengan rumus, tabel, dan grafik.',
        lead='Aplikasi lembar kerja native dengan mesin hitung yang cepat, ratusan fungsi, tabel, pemformatan bersyarat, dan grafik. Menggunakan format XLSX dan bisa mengimpor CSV.',
        short='Lembar kerja native dengan 500+ fungsi, grafik, tabel, dan format XLSX.',
        basis='Dikembangkan dari proyek open-source GridCraft (lisensi MIT atau Apache-2.0), disesuaikan oleh Altora.',
        os='macOS, Windows, Linux',
        shots=[('sheets-main', 'Altora Sheets: lembar kerja dengan rumus, tabel, dan grafik', 'Antarmuka Altora Sheets')],
        modules=[('Rumus & fungsi', 'Lebih dari 500 fungsi, array dinamis, serta LET dan LAMBDA.'),
                 ('Tabel & pemformatan', 'Tabel terstruktur, pemformatan bersyarat, validasi data, dan format angka lengkap.'),
                 ('Grafik & sparkline', 'Grafik, gambar, dan sparkline langsung di lembar kerja.'),
                 ('Format XLSX', 'XLSX sebagai format asli; CSV dan TSV bisa diimpor dan diekspor.'),
                 ('PivotTable', 'Merangkum data besar dengan tabel pivot.'),
                 ('Cepat', 'Perhitungan inkremental dan tampilan yang hanya menggambar bagian yang terlihat.')],
        faq=[('Apakah bisa membuka file Excel?', 'Bisa. XLSX adalah format asli aplikasi ini, termasuk rumus, tabel, dan grafik.'),
             ('Apakah bisa dipakai untuk data besar?', 'Mesin hitung inkremental dan tampilan virtual dirancang agar tetap lancar pada lembar kerja besar.'),
             ('Apakah bisa disesuaikan untuk organisasi kami?', 'Bisa. Kami dapat menyesuaikan templat dan menghubungkannya dengan sistem Anda.')]),
    'slides': dict(
        name='Altora Slides', tag='Presentasi', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Slides: presentasi dengan tema, animasi, dan mode tayang.',
        lead='Aplikasi presentasi native untuk membuat slide dengan tema, tata letak, bentuk, gambar, tabel, grafik, transisi, dan animasi, lalu menayangkannya layar penuh. Membuka dan menyimpan file PowerPoint (.pptx).',
        short='Presentasi native dengan tema, animasi, mode tayang, dan format .pptx.',
        basis='Dikembangkan dari proyek open-source DeckCraft (lisensi MIT atau Apache-2.0), disesuaikan oleh Altora. Masih dalam pengembangan awal.',
        os='macOS, Windows, Linux',
        shots=[('slides-main', 'Altora Slides: contoh slide presentasi', 'Contoh slide')],
        modules=[('Tema & tata letak', 'Tema, tata letak slide, dan master untuk tampilan yang konsisten.'),
                 ('Bentuk, gambar, tabel, grafik', 'Konten visual lengkap di dalam slide.'),
                 ('Transisi & animasi', 'Perpindahan antar slide dan animasi objek.'),
                 ('Mode tayang', 'Menayangkan presentasi layar penuh.'),
                 ('Format PPTX', 'Membuka dan menyimpan file PowerPoint.'),
                 ('Ekspor', 'Ekspor ke PDF dan gambar.')],
        faq=[('Apakah bisa membuka file PowerPoint?', 'Bisa. Aplikasi ini membuka dan menyimpan format .pptx.'),
             ('Apakah sudah siap dipakai sehari-hari?', 'Aplikasi ini masih dalam pengembangan awal. Hubungi kami untuk melihat demo dan fitur yang sudah tersedia.'),
             ('Apakah bisa disesuaikan untuk organisasi kami?', 'Bisa. Kami dapat menyiapkan templat dan tema sesuai identitas organisasi Anda.')]),
    'control-center': dict(
        name='Altora Control Center', tag='Pusat kendali infrastruktur & proyek', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Altora Control Center: satu layar untuk server, website, dan proyek Anda.',
        lead='Pantau server, website, cron job, dan agen AI dari satu tempat, lengkap dengan papan proyek dan notifikasi lewat WhatsApp. Tersedia sebagai aplikasi menu bar macOS dan sebagai web yang bisa dibuka dari perangkat apa pun.',
        short='Pantau server, website, dan proyek, dengan peringatan lewat WhatsApp.',
        shots=[('control-center-board', 'Papan proyek Kanban di dalam Altora Control Center', 'Papan proyek'),
               ('control-center-portfolio', 'Portofolio proyek dan progresnya', 'Portfolio')],
        modules=[('Monitor server', 'CPU, RAM, disk, dan suhu perangkat dengan riwayat, serta container dan layanan yang berjalan.'),
                 ('Website & SSL', 'Status HTTP, waktu respons, uptime, dan masa berlaku sertifikat SSL.'),
                 ('Cron & job', 'Daftar jadwal tugas dengan waktu jalan terakhir, kegagalan, dan yang terlewat.'),
                 ('Insiden & notifikasi', 'Insiden dibuka saat masalah menetap dan ditutup saat pulih, dengan pesan WhatsApp.'),
                 ('Workspace proyek', 'Portofolio, proyek, papan Kanban, dan detail tugas dalam satu workspace.'),
                 ('Agen AI & token', 'Pemantauan sesi dan pemakaian token agen AI, serta kesehatan penyedia model.')],
        faq=[('Di mana Altora Control Center berjalan?', 'Sebagai aplikasi menu bar macOS dan sebagai server web kecil untuk perangkat yang menyala terus, misalnya Raspberry Pi, yang bisa dibuka dari browser.'),
             ('Apakah data saya dikirim ke pihak lain?', 'Tidak. Aplikasi ini tidak memakai telemetri; koneksi hanya ke perangkat dan layanan yang Anda atur sendiri.'),
             ('Apakah bisa disesuaikan?', 'Bisa. Server, website, dan peringatan yang dipantau diatur lewat konfigurasi, dan kami bisa membantu menyiapkannya.')]),
}

# halaman SEO per kebutuhan bisnis (scripts/build_app_seo.py)
SEO = {'store': ('/aplikasi-toko', 'Aplikasi toko & distributor'), 'fieldops': ('/aplikasi-pertambangan', 'Aplikasi pertambangan & migas'),
       'office': ('/aplikasi-manajemen-proyek', 'Aplikasi manajemen proyek'), 'teams': ('/aplikasi-hris', 'Aplikasi HRIS & KPI'),
       'control-center': ('/aplikasi-monitoring-server', 'Aplikasi monitoring server'), 'word': ('/aplikasi-perkantoran', 'Aplikasi perkantoran'),
       'sheets': ('/aplikasi-perkantoran', 'Aplikasi perkantoran'), 'slides': ('/aplikasi-perkantoran', 'Aplikasi perkantoran')}


def demo_link(name):
    return WA + quote(f'Halo Altora, saya ingin minta demo {name}.')


def cta_buttons(a):
    """Tombol utama + sekunder. Aplikasi dengan demo_url: Coba demo (ungu) + link ke situs produk; lainnya: Minta demo via WhatsApp."""
    if a.get('demo_url'):
        return (f'<a class="btn btn-purple" href="{a["demo_url"]}" rel="noopener" target="_blank">Coba demo</a>'
                f'<a class="svd-link" href="{a["site_url"]}" rel="noopener" target="_blank">Kunjungi store.altora.id</a>')
    return f'<a class="btn btn-purple" href="{demo_link(a["name"])}" rel="noopener" target="_blank">Minta demo</a>'


def wa_alt(a):
    return f'<a class="svd-link" href="{demo_link(a["name"])}" rel="noopener" target="_blank">Tanya lewat WhatsApp</a>' if a.get('demo_url') else ''


def pic(sid, alt, big=False):
    return (f'<figure class="ap2-shot{" ap2-shot-big" if big else ""}"><div class="ap2-bar"><i></i><i></i><i></i></div>'
            f'<img alt="{e(alt)}" decoding="async" loading="{"eager" if big else "lazy"}" src="{IMG}{sid}.webp"/></figure>')


def detail(k, a):
    url = f'/aplikasi/{k}'
    basis = f'<p style="font-size:.875rem;max-width:56ch;color:#5A6785;margin-top:14px">{e(a["basis"])}</p>' if a.get('basis') else ''
    shots = ''.join(f'<div class="ap2-feat"><div class="ap2-feat-txt"><h3>{e(t)}</h3></div>{pic(sid, alt)}</div>' for sid, alt, t in a['shots'][1:])
    shots_sec = ('<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Tampilan aplikasi</h2><p>Screenshot dari toko demo fiktif (CV Mitra Teknik Mandiri); semua datanya data contoh.</p></div><div class="ap2-feats">' + shots + '</div></div></section>') if shots else ''
    mods = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in a['modules'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(x)}</p></details>' for q, x in a['faq'])
    ld = {'@context': 'https://schema.org', '@graph': [org(),
        {'@type': 'SoftwareApplication', 'name': a['name'], 'description': a['short'], 'url': SITE + url, 'applicationCategory': 'BusinessApplication',
         'operatingSystem': a.get('os') or ('Web' + (', macOS' if k == 'control-center' else '')), 'image': SITE + IMG + a['shots'][0][0] + '.webp',
         'publisher': {'@id': ORG_ID}},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Aplikasi', 'item': SITE + '/aplikasi'}, {'@type': 'ListItem', 'position': 3, 'name': a['name'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in a['faq']]}]}
    body = f'''<main class="ct-page svd-page ap2-page">
<section class="svd-hero"><div class="ct-wrap ap2-hero">
<div class="ap2-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/aplikasi">Aplikasi</a><span>/</span><span>{e(a["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">{e(a["tag"])}</p><h1>{e(a["h1"])}</h1><p class="ct-lead">{e(a["lead"])}</p>{basis}
<div class="svd-actions">{cta_buttons(a)}<a class="svd-link" href="{SEO[k][0] if k in SEO else "#fitur"}">{SEO[k][1] + " →" if k in SEO else "Lihat fitur"}</a></div></div>
{pic(a["shots"][0][0], a["shots"][0][1], True)}
</div></section>
<section class="svd-sec" id="fitur"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang bisa dikerjakan</h2></div><div class="svd-dos">{mods}</div></div></section>
{shots_sec}
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Ingin melihat {e(a["name"])} langsung?</h2><p>Kami tunjukkan lewat demo singkat dan bahas penyesuaiannya untuk Anda.</p></div><div class="svd-actions">{cta_buttons(a)}{wa_alt(a)}</div></div></section>
</main>'''
    return url, shell(f'{a["name"]} | Aplikasi Buatan Altora', a['short'] + ' Aplikasi buatan Altora Indonesia.', url, SITE + IMG + a['shots'][0][0] + '.webp', ld, body)


def hub():
    cards = ''.join(f'''<article class="ap2-card"><a class="ap2-card-pic" href="/aplikasi/{k}">{pic(a["shots"][0][0], a["shots"][0][1])}</a>
<div class="ap2-card-body"><p class="eyebrow eyebrow-purple">{e(a["tag"])}</p><h2><a href="/aplikasi/{k}">{e(a["name"])}</a></h2><p>{e(a["short"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="/aplikasi/{k}">Lihat detail</a><a class="svd-link" href="{a.get("demo_url") or demo_link(a["name"])}" rel="noopener" target="_blank">{"Coba demo" if a.get("demo_url") else "Minta demo"}</a></div></div></article>''' for k, a in APPS.items())
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Aplikasi buatan Altora', 'url': SITE + '/aplikasi',
          'hasPart': [{'@type': 'SoftwareApplication', 'name': a['name'], 'url': SITE + f'/aplikasi/{k}'} for k, a in APPS.items()]}
    body = f'''<main class="ct-page svd-page ap2-page">
<section class="svd-hero"><div class="ct-wrap ap2-hero ap2-hero-hub"><div class="ap2-hero-copy"><p class="eyebrow eyebrow-purple">Aplikasi buatan Altora</p>
<h1>Aplikasi yang kami kembangkan dan pakai sendiri.</h1>
<p class="ct-lead">Selain mengerjakan aplikasi untuk klien, kami mengembangkan dan memakai aplikasi sendiri setiap hari. Hasilnya bisa dipakai juga oleh organisasi Anda, atau menjadi dasar aplikasi custom yang disesuaikan dengan proses Anda.</p></div>
<div class="ab-collage ab-collage-hub"><figure class="ap2-shot ab-c1"><div class="ap2-bar"><i></i><i></i><i></i></div><img alt="" src="{IMG}fieldops-overview.webp"/></figure><figure class="ap2-shot ab-c2"><div class="ap2-bar"><i></i><i></i><i></i></div><img alt="" src="{IMG}office-board.webp"/></figure><figure class="ap2-shot ab-c3"><div class="ap2-bar"><i></i><i></i><i></i></div><img alt="" src="{IMG}teams-overview.webp"/></figure></div></div></section>
<section class="svd-sec"><div class="ct-wrap ap2-cards">{cards}</div></section>
<section class="svd-sec ap2-more"><div class="ct-wrap"><div class="ap2-more-panel"><div class="ap2-more-copy"><h2>Butuh yang berbeda?</h2><p>Kami membuat aplikasi custom yang mengikuti proses kerja Anda, lengkap dengan website dan SEO.</p>
<div class="svd-actions"><a class="btn btn-purple" href="/services/software-custom">Lihat layanan software custom</a><a class="svd-link" href="/contact">Konsultasi gratis</a></div></div></div></div></section>
</main>'''
    return shell('Aplikasi Buatan Altora | Altora Office, Teams & Altora Control Center', 'Aplikasi yang dibangun dan dipakai sendiri oleh Altora: Altora Office untuk proyek dan operasional, Altora Teams untuk KPI dan cuti tim, serta Altora Control Center untuk server, website, dan proyek.',
                 '/aplikasi', SITE + IMG + 'office-board.webp', ld, body)


def home_cards():
    out = []
    for i, (k, a) in enumerate(APPS.items()):
        sid, alt, _ = a['shots'][0]
        out.append(f'''<article class="ap2-card reveal"{f' data-d="{i % 3}"' if i % 3 else ''}><a class="ap2-card-pic" href="/aplikasi/{k}"><figure class="ap2-shot"><div class="ap2-bar"><i></i><i></i><i></i></div><img alt="{e(alt)}" decoding="async" loading="lazy" src="{IMG}{sid}.webp"/></figure></a><div class="ap2-card-body"><p class="eyebrow eyebrow-purple">{e(a["tag"])}</p><h3><a href="/aplikasi/{k}">{e(a["name"])}</a></h3><p>{e(a["short"])}</p><div class="svd-actions"><a class="btn btn-purple" href="/aplikasi/{k}">Lihat detail</a><a class="svd-link" href="{a.get("demo_url") or demo_link(a["name"])}" rel="noopener" target="_blank">{"Coba demo" if a.get("demo_url") else "Minta demo"}</a></div></div></article>''')
    return '<div class="ap2-cards">\n' + '\n'.join(out) + '\n</div></div></section><!-- apps:end -->'


def update_home():
    import re
    f = root / 'index.html'
    s = f.read_text(encoding='utf-8')
    s2 = re.sub(r'<div class="ap2-cards">.*?</div></div></section><!-- apps:end -->', lambda m: home_cards(), s, count=1, flags=re.S)
    f.write_text(s2, encoding='utf-8')


if __name__ == '__main__':
    (root / 'aplikasi').mkdir(exist_ok=True)
    urls = ['/aplikasi']
    (root / 'aplikasi.html').write_text(hub(), encoding='utf-8')
    for k, a in APPS.items():
        url, h = detail(k, a)
        (root / (url.lstrip('/') + '.html')).write_text(h, encoding='utf-8'); urls.append(url)
    update_sitemap(urls)
    update_home()
    print('aplikasi:', len(urls), 'halaman')
