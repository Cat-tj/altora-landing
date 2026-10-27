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



SERVICES = [
    dict(slug='software-custom', name='Software Custom', kicker='Aplikasi & sistem internal',
         h1='Aplikasi yang mengikuti cara kerja tim Anda.',
         lead='Web app, aplikasi mobile, dan sistem internal untuk proses yang tidak cocok dengan software jadi, seperti approval, absensi, dan laporan yang masih dikumpulkan manual.',
         hero='/assets/img/apps/office-project.webp', hero_pos='60% 55%', chips=['Approval berjenjang', 'Laporan otomatis', 'Akses per peran'],
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
         related=[('/jasa-pembuatan-aplikasi-samarinda', 'Jasa pembuatan aplikasi Samarinda'), ('/services/website-seo', 'Website & SEO'), ('/blog/merencanakan-pembuatan-aplikasi', 'Artikel: merencanakan pembuatan aplikasi')],
         faq=[('Apakah harus dibuat dari nol?', 'Tidak selalu. Bila ada aplikasi di pasaran yang sudah cocok, kami bantu menilainya dulu; yang dibuat khusus hanya bagian yang benar-benar unik di proses Anda.'),
              ('Bisa dipakai di HP?', 'Bisa. Sistem dapat dibuat sebagai aplikasi web yang nyaman di HP, aplikasi mobile, atau keduanya sesuai kebutuhan lapangan.'),
              ('Siapa pemilik data dan aksesnya?', 'Kepemilikan data, akses server, dan source code dibahas dan dicantumkan dengan jelas sejak awal kerja sama.')]),
    dict(slug='website-seo', name='Website & SEO', kicker='Website institusi & bisnis',
         h1='Website yang menjelaskan, ditemukan, dan menghasilkan kontak.',
         lead='Company profile, landing page, dan website institusi dengan struktur konten yang jelas, cepat dibuka di HP, dan disusun agar mudah ditemukan di Google.',
         hero='/assets/img/apps/raphael-board.webp', hero_pos='50% 30%', chips=['Cepat di HP', 'Struktur SEO', 'CMS mudah diisi'],
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
         related=[('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website Samarinda'), ('/jasa-pembuatan-website-indonesia', 'Jasa pembuatan website Indonesia'), ('/blog', 'Artikel & panduan')],
         faq=[('Apakah website lama bisa diperbaiki?', 'Bisa. Kami mulai dari audit website yang ada, lalu memutuskan apakah cukup diperbaiki atau perlu dibangun ulang.'),
              ('Bisakah kami mengisi konten sendiri?', 'Bisa. Website dapat dilengkapi CMS sehingga tim Anda dapat memperbarui berita, layanan, dan galeri.'),
              ('Kapan hasil SEO terlihat?', 'SEO bergantung pada persaingan kata kunci dan konsistensi konten, sehingga hasilnya bertahap. Kami memantau dan melaporkan perkembangannya.')]),
    dict(slug='seo', name='SEO', kicker='Website yang mudah ditemukan',
         h1='SEO supaya calon pelanggan menemukan Anda di Google.',
         lead='Audit dan perbaikan SEO untuk website bisnis dan organisasi: struktur halaman, kecepatan, konten, dan SEO lokal, dengan laporan yang mudah dipahami.',
         hero='/assets/img/apps/raphael-board.webp', hero_pos='50% 30%', chips=['Audit teknis', 'SEO lokal', 'Laporan berkala'],
         pains=[('Website ada, tapi tidak ditemukan', 'Calon pelanggan mencari layanan Anda di Google, tetapi yang muncul justru pesaing.'),
                ('Tidak tahu harus mulai dari mana', 'Banyak saran SEO beredar, tetapi tidak jelas mana yang paling berdampak untuk website Anda.'),
                ('Perbaikan tidak terukur', 'Sudah ada yang dikerjakan, tetapi tidak ada laporan yang menunjukkan perubahannya.')],
         dos=[('search', 'Audit & riset kata kunci', 'Cek masalah teknis dan tentukan kata yang benar-benar dicari calon pelanggan.'),
              ('layout', 'SEO on-page', 'Judul, deskripsi, heading, tautan internal, dan data terstruktur dirapikan per halaman.'),
              ('pin', 'SEO lokal', 'Profil Google Bisnis, halaman per area, dan konsistensi nama-alamat-telepon.'),
              ('speed', 'Kecepatan & mobile', 'Gambar dan skrip dioptimalkan agar halaman cepat dibuka di HP.'),
              ('pen', 'Konten & artikel', 'Halaman layanan dan panduan yang menjawab pertanyaan calon pelanggan.'),
              ('chart', 'Laporan berkala', 'Pantauan peringkat dan kunjungan, dengan ringkasan tindakan berikutnya.')],
         steps=['Audit website & kata kunci', 'Prioritas perbaikan', 'Eksekusi on-page & teknis', 'Konten & SEO lokal', 'Pantauan & laporan'],
         related=[('/jasa-seo-samarinda', 'Jasa SEO Samarinda'), ('/services/website-seo', 'Website & SEO'), ('/blog', 'Artikel & panduan')],
         faq=[('Berapa lama SEO terlihat hasilnya?', 'SEO bergantung pada persaingan kata kunci dan konsistensi perbaikan, jadi hasilnya bertahap. Kami tidak menjanjikan peringkat tertentu, tetapi melaporkan perkembangannya.'),
              ('Apakah bisa untuk website yang bukan buatan Altora?', 'Bisa. Kami audit dulu website yang ada, lalu menyampaikan perbaikan yang perlu dilakukan.'),
              ('Apa bedanya SEO dengan iklan Google?', 'SEO memperbaiki website agar muncul secara organik, sedangkan iklan berbayar muncul selama dibayar. Keduanya bisa dipakai bersama.')]),
]


def build(sv):
    url = f'/services/{sv["slug"]}'
    chips = ''.join(f'<span class="svd-chip svd-chip-{i}">{e(c)}</span>' for i, c in enumerate(sv['chips']))
    pains = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in sv['pains'])
    dos = ''.join(f'<article class="svd-do"><span class="svd-ico">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, t, d in sv['dos'])
    steps = ''.join(f'<li><b>{e(s)}</b></li>' for s in sv['steps'])
    related = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in sv['related'])
    scope = ''
    if sv.get('scope'):
        scope = '<nav aria-label="Cakupan" class="svd-scope">' + ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in sv['scope']) + '</nav>'
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
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#terkait">Layanan terkait</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(sv["name"])}" src="{sv["hero"]}" style="object-position:{sv["hero_pos"]}"/>{chips}</figure>
</div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Masalah yang sering kami temui</h2></div><ul>{pains}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang kami kerjakan</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Alur kerja</h2></div><ol class="svd-steps">{steps}</ol></div></section>
<section class="svd-sec" id="terkait"><div class="ct-wrap">
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
