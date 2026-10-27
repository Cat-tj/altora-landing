"""Halaman /aplikasi (hub) dan /aplikasi/<id> untuk aplikasi buatan Altora: Altora Office dan Raphael Control Center.
Screenshot asli dari aplikasi yang berjalan dengan data contoh (tanpa data klien/server nyata) ada di assets/img/apps/.
Jalankan lewat scripts/build_all.sh."""
import html, json, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(t, quote=True)
IMG = '/assets/img/apps/'

APPS = {
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
    'raphael': dict(
        name='Raphael Control Center', tag='Pusat kendali infrastruktur & proyek', icon='/assets/img/altora-logo-icon-v2.svg',
        h1='Raphael Control Center: satu layar untuk server, website, dan proyek Anda.',
        lead='Pantau server, website, cron job, dan agen AI dari satu tempat, lengkap dengan papan proyek dan notifikasi lewat WhatsApp. Tersedia sebagai aplikasi menu bar macOS dan sebagai web yang bisa dibuka dari perangkat apa pun.',
        short='Pantau server, website, dan proyek, dengan peringatan lewat WhatsApp.',
        shots=[('raphael-board', 'Papan proyek Kanban di dalam Raphael Control Center', 'Papan proyek'),
               ('raphael-portfolio', 'Portofolio proyek dan progresnya', 'Portfolio')],
        modules=[('Monitor server', 'CPU, RAM, disk, dan suhu perangkat dengan riwayat, serta container dan layanan yang berjalan.'),
                 ('Website & SSL', 'Status HTTP, waktu respons, uptime, dan masa berlaku sertifikat SSL.'),
                 ('Cron & job', 'Daftar jadwal tugas dengan waktu jalan terakhir, kegagalan, dan yang terlewat.'),
                 ('Insiden & notifikasi', 'Insiden dibuka saat masalah menetap dan ditutup saat pulih, dengan pesan WhatsApp.'),
                 ('Workspace proyek', 'Portofolio, proyek, papan Kanban, dan detail tugas dalam satu workspace.'),
                 ('Agen AI & token', 'Pemantauan sesi dan pemakaian token agen AI, serta kesehatan penyedia model.')],
        faq=[('Di mana Raphael berjalan?', 'Sebagai aplikasi menu bar macOS dan sebagai server web kecil untuk perangkat yang menyala terus, misalnya Raspberry Pi, yang bisa dibuka dari browser.'),
             ('Apakah data saya dikirim ke pihak lain?', 'Tidak. Raphael tidak memakai telemetri; koneksi hanya ke perangkat dan layanan yang Anda atur sendiri.'),
             ('Apakah bisa disesuaikan?', 'Bisa. Server, website, dan peringatan yang dipantau diatur lewat konfigurasi, dan kami bisa membantu menyiapkannya.')]),
}


def demo_link(name):
    return WA + quote(f'Halo Altora, saya ingin minta demo {name}.')


def pic(sid, alt, big=False):
    return (f'<figure class="ap2-shot{" ap2-shot-big" if big else ""}"><div class="ap2-bar"><i></i><i></i><i></i></div>'
            f'<img alt="{e(alt)}" decoding="async" loading="{"eager" if big else "lazy"}" src="{IMG}{sid}.webp"/></figure>')


def detail(k, a):
    url = f'/aplikasi/{k}'
    shots = ''.join(f'<div class="ap2-feat"><div class="ap2-feat-txt"><h3>{e(t)}</h3></div>{pic(sid, alt)}</div>' for sid, alt, t in a['shots'][1:])
    mods = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in a['modules'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(x)}</p></details>' for q, x in a['faq'])
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'SoftwareApplication', 'name': a['name'], 'description': a['short'], 'url': SITE + url, 'applicationCategory': 'BusinessApplication',
         'operatingSystem': 'Web' + (', macOS' if k == 'raphael' else ''), 'image': SITE + IMG + a['shots'][0][0] + '.webp',
         'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': SITE + '/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Aplikasi', 'item': SITE + '/aplikasi'}, {'@type': 'ListItem', 'position': 3, 'name': a['name'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in a['faq']]}]}
    body = f'''<main class="ct-page svd-page ap2-page">
<section class="svd-hero"><div class="ct-wrap ap2-hero">
<div class="ap2-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/aplikasi">Aplikasi</a><span>/</span><span>{e(a["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">{e(a["tag"])}</p><h1>{e(a["h1"])}</h1><p class="ct-lead">{e(a["lead"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{demo_link(a["name"])}" rel="noopener" target="_blank">Minta demo</a><a class="svd-link" href="#fitur">Lihat fitur</a></div></div>
{pic(a["shots"][0][0], a["shots"][0][1], True)}
</div></section>
<section class="svd-sec" id="fitur"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang bisa dikerjakan</h2></div><div class="svd-dos">{mods}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Tampilan aplikasi</h2><p>Screenshot dari aplikasi yang berjalan, dengan data contoh.</p></div><div class="ap2-feats">{shots}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Ingin melihat {e(a["name"])} langsung?</h2><p>Kami tunjukkan lewat demo singkat dan bahas penyesuaiannya untuk Anda.</p></div><a class="btn btn-purple" href="{demo_link(a["name"])}" rel="noopener" target="_blank">Minta demo</a></div></section>
</main>'''
    return url, shell(f'{a["name"]} | Aplikasi Buatan Altora', a['short'] + ' Aplikasi buatan Altora Indonesia.', url, SITE + IMG + a['shots'][0][0] + '.webp', ld, body)


def hub():
    cards = ''.join(f'''<article class="ap2-card"><a class="ap2-card-pic" href="/aplikasi/{k}">{pic(a["shots"][0][0], a["shots"][0][1])}</a>
<div class="ap2-card-body"><p class="eyebrow eyebrow-purple">{e(a["tag"])}</p><h2><a href="/aplikasi/{k}">{e(a["name"])}</a></h2><p>{e(a["short"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="/aplikasi/{k}">Lihat detail</a><a class="svd-link" href="{demo_link(a["name"])}" rel="noopener" target="_blank">Minta demo</a></div></div></article>''' for k, a in APPS.items())
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Aplikasi buatan Altora', 'url': SITE + '/aplikasi',
          'hasPart': [{'@type': 'SoftwareApplication', 'name': a['name'], 'url': SITE + f'/aplikasi/{k}'} for k, a in APPS.items()]}
    body = f'''<main class="ct-page svd-page ap2-page">
<section class="svd-hero"><div class="ct-wrap"><p class="eyebrow eyebrow-purple">Aplikasi buatan Altora</p>
<h1>Aplikasi yang kami bangun, dan kami pakai sendiri.</h1>
<p class="ct-lead">Selain mengerjakan aplikasi untuk klien, kami mengembangkan dan memakai aplikasi sendiri setiap hari. Hasilnya bisa dipakai juga oleh organisasi Anda, atau menjadi dasar aplikasi custom yang disesuaikan dengan proses Anda.</p></div></section>
<section class="svd-sec"><div class="ct-wrap ap2-cards">{cards}</div></section>
<section class="svd-sec"><div class="ct-wrap pd-block-head"><h2>Butuh yang berbeda?</h2><p>Kami membuat aplikasi custom yang mengikuti proses kerja Anda, lengkap dengan website dan SEO.</p>
<div class="svd-actions"><a class="btn btn-purple" href="/services/software-custom">Lihat layanan software custom</a><a class="svd-link" href="/contact">Konsultasi gratis</a></div></div></section>
</main>'''
    return shell('Aplikasi Buatan Altora | Altora Office, Teams & Raphael Control Center', 'Aplikasi yang dibangun dan dipakai sendiri oleh Altora: Altora Office untuk proyek dan operasional, Altora Teams untuk KPI dan cuti tim, serta Raphael Control Center untuk server, website, dan proyek.',
                 '/aplikasi', SITE + IMG + 'office-board.webp', ld, body)


if __name__ == '__main__':
    (root / 'aplikasi').mkdir(exist_ok=True)
    urls = ['/aplikasi']
    (root / 'aplikasi.html').write_text(hub(), encoding='utf-8')
    for k, a in APPS.items():
        url, h = detail(k, a)
        (root / (url.lstrip('/') + '.html')).write_text(h, encoding='utf-8'); urls.append(url)
    update_sitemap(urls)
    print('aplikasi:', len(urls), 'halaman')
