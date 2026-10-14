"""Bangun careers.html dari data di bawah.
Tambah lowongan nyata di OPENINGS, lalu jalankan dari root repo:
    python3 scripts/build_careers.py && python3 scripts/apply_shell.py
Selama OPENINGS kosong, halaman menampilkan talent network (tanpa lowongan palsu).
Lowongan yang diisi otomatis mendapat data terstruktur JobPosting untuk Google Jobs."""
import html, json, pathlib
from urllib.parse import quote

root = pathlib.Path(__file__).resolve().parent.parent
CSS_VER = '20261014a'
EMAIL = 'hello@altora.id'
WA = 'https://wa.me/6285190911170?text='

# Contoh isi:
# dict(id='field-engineer-bpn', title='Field Engineer CCTV & Jaringan', type='Penuh waktu', location='Balikpapan',
#      employment='FULL_TIME', posted='2026-10-12', until='2026-11-30',
#      summary='Memasang dan merawat CCTV, jaringan, dan perangkat di lokasi klien.',
#      duties=['Survei lokasi dan desain titik kamera', 'Pemasangan kabel, fiber, dan rak', 'Konfigurasi NVR, switch, dan access point'],
#      reqs=['Pengalaman instalasi CCTV atau jaringan', 'Bersedia bekerja di lapangan', 'Memiliki SIM C'])
OPENINGS = []

AREAS = [
    ('Software engineer', 'Membangun aplikasi operasional seperti HRIS, POS, dan dashboard, serta menghubungkannya dengan sistem lain.',
     ['TypeScript / Next.js', 'Flutter untuk aplikasi mobile', 'PostgreSQL & integrasi API']),
    ('UI/UX & product designer', 'Merancang tampilan aplikasi yang mudah dipakai pengguna di kantor maupun di lapangan.',
     ['Riset pengguna & wireframe', 'Desain antarmuka web & mobile', 'Design system']),
    ('Field engineer CCTV & jaringan', 'Survei lokasi, memasang kamera, kabel, fiber, dan rak, lalu mengonfigurasi perangkat sampai siap dipakai.',
     ['Instalasi CCTV & NVR', 'Switch, access point, fiber optik', 'Bersedia bekerja di lapangan']),
    ('AI & computer vision', 'Mengembangkan dan menguji model deteksi seperti APD dan pengenalan wajah dengan kamera CCTV sungguhan.',
     ['Python & framework deep learning', 'Dataset & evaluasi model', 'Deployment ke perangkat edge/server']),
    ('IoT & hardware', 'Merakit dan mengintegrasikan sensor, gateway, smartlock, dan kios dengan aplikasi Altora.',
     ['Mikrokontroler & sensor', 'LoRa / 4G gateway', 'Integrasi perangkat ke API']),
    ('Project & implementation', 'Menjembatani klien dan tim: jadwal, koordinasi lapangan, pelatihan pengguna, dan dokumen serah terima.',
     ['Koordinasi proyek', 'Komunikasi dengan klien', 'Dokumentasi & pelatihan']),
]

WORK = [
    ('Proyek sungguhan', 'Aplikasi dan perangkat yang Anda kerjakan langsung dipakai klien. Contohnya ada di portofolio.'),
    ('Software dan perangkat dalam satu tim', 'Developer, field engineer, dan desainer bekerja di proyek yang sama, jadi Anda melihat sistem secara utuh.'),
    ('Dekat dengan pengguna', 'Tim turun ke lokasi untuk memahami cara kerja pengguna sebelum memutuskan solusi.'),
    ('Dokumentasi jadi kebiasaan', 'Setiap implementasi didokumentasikan supaya mudah dirawat dan dipelajari tim berikutnya.'),
]

STEPS = [('Kirim profil', 'Email atau WhatsApp berisi keahlian dan portofolio.'),
         ('Kami tinjau', 'Profil dicocokkan dengan kebutuhan proyek yang sedang berjalan.'),
         ('Ngobrol', 'Diskusi singkat tentang pengalaman dan minat Anda.'),
         ('Diskusi kasus', 'Membahas contoh kasus sesuai bidang Anda.'),
         ('Keputusan', 'Kami kabari hasilnya, termasuk bila profil disimpan untuk proyek berikutnya.')]

e = lambda t: html.escape(t, quote=True)


def mail(subject, body):
    return f'mailto:{EMAIL}?subject={quote(subject)}&amp;body={quote(body)}'


TEMPLATE_BODY = 'Nama:\nBidang keahlian:\nKota domisili:\nLink portofolio / CV:\nNomor WhatsApp:\n\nCeritakan singkat pengalaman Anda:\n'


def opening_card(o):
    duties = ''.join(f'<li>{e(d)}</li>' for d in o['duties'])
    reqs = ''.join(f'<li>{e(r)}</li>' for r in o['reqs'])
    return (f'<article class="cr-job" id="{o["id"]}"><div class="cr-job-head"><h3>{e(o["title"])}</h3>'
            f'<p class="cr-job-meta">{e(o["type"])} · {e(o["location"])}</p></div><p>{e(o["summary"])}</p>'
            f'<div class="cr-job-cols"><div><b>Yang dikerjakan</b><ul>{duties}</ul></div><div><b>Yang kami cari</b><ul>{reqs}</ul></div></div>'
            f'<a class="btn btn-purple" href="{mail("Lamaran: " + o["title"], TEMPLATE_BODY)}">Lamar posisi ini</a></article>')


def job_ld(o):
    return {'@type': 'JobPosting', 'title': o['title'], 'description': o['summary'], 'datePosted': o['posted'],
            'validThrough': o['until'], 'employmentType': o['employment'],
            'hiringOrganization': {'@type': 'Organization', 'name': 'Altora Indonesia', 'sameAs': 'https://altora.id/'},
            'jobLocation': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': o['location'],
                                                          'addressRegion': 'Kalimantan Timur', 'addressCountry': 'ID'}}}


if OPENINGS:
    jobs_html = ''.join(opening_card(o) for o in OPENINGS)
    jobs_head = f'<h2>Lowongan terbuka</h2><p>{len(OPENINGS)} posisi sedang dibuka.</p>'
else:
    jobs_html = ('<div class="cr-empty"><b>Belum ada lowongan yang dibuka saat ini.</b>'
                 '<p>Kami tetap menerima profil untuk talent network. Saat ada proyek yang cocok dengan keahlian Anda, tim Altora akan menghubungi lebih dulu.</p>'
                 f'<a class="btn btn-purple" href="#kirim">Kirim profil</a></div>')
    jobs_head = '<h2>Lowongan terbuka</h2>'

areas_html = ''.join(f'<article class="cr-area"><h3>{e(t)}</h3><p>{e(d)}</p><ul>{"".join(f"<li>{e(s)}</li>" for s in skills)}</ul></article>' for t, d, skills in AREAS)
work_html = ''.join(f'<div class="cr-work-item"><b>{e(t)}</b><p>{e(d)}</p></div>' for t, d in WORK)
steps_html = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in STEPS)

ld = {'@context': 'https://schema.org', '@graph': [job_ld(o) for o in OPENINGS]} if OPENINGS else None
ld_html = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''

title = 'Karier di Altora Indonesia | Balikpapan & Samarinda'
desc = ('Bergabung dengan Altora Indonesia: software engineer, UI/UX designer, field engineer CCTV & jaringan, AI, IoT, '
        'dan project implementation di Balikpapan dan Samarinda.')

page = f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(title)}</title><meta content="{e(desc)}" name="description"/><link href="https://altora.id/careers" rel="canonical"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="Karier di Altora Indonesia" property="og:title"/><meta content="{e(desc)}" property="og:description"/><meta content="https://altora.id/careers" property="og:url"/><meta content="https://altora.id/assets/img/produk/fms.webp" property="og:image"/><link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v=20261014a"/>{ld_html}</head><body class="company-page"><header></header>
<main class="ct-page cr-page">
<section class="ct-hero"><div class="ct-wrap">
<p class="eyebrow eyebrow-purple">Karier di Altora</p>
<h1>Bangun teknologi yang benar-benar dipakai di lapangan.</h1>
<p class="ct-lead">Di Altora, software, perangkat, dan jaringan dikerjakan dalam satu tim, di Balikpapan, Samarinda, dan lokasi klien. Kami mencari orang yang suka memahami masalah sebelum menulis kode atau memasang perangkat.</p>
<nav aria-label="Bagian halaman" class="pd-chips"><a href="#lowongan">Lowongan</a><a href="#bidang">Bidang</a><a href="#proses">Proses</a><a href="#kirim">Kirim profil</a></nav>
</div></section>

<section class="cr-sec" id="lowongan"><div class="ct-wrap"><div class="pd-block-head">{jobs_head}</div>{jobs_html}</div></section>

<section class="cr-sec" id="bidang"><div class="ct-wrap"><div class="pd-block-head"><h2>Bidang yang kami butuhkan</h2><p>Posisi dibuka mengikuti kebutuhan proyek. Kalau keahlian Anda ada di salah satu bidang ini, kirim profil Anda.</p></div>
<div class="cr-areas">{areas_html}</div></div></section>

<section class="cr-sec"><div class="ct-wrap cr-work"><div class="pd-block-head"><h2>Seperti apa bekerja di Altora</h2><p>Lihat juga <a href="/portfolio">portofolio</a> untuk contoh pekerjaan tim.</p></div><div class="cr-work-grid">{work_html}</div></div></section>

<section class="cr-sec" id="proses"><div class="ct-wrap"><div class="pd-block-head"><h2>Proses seleksi</h2></div><ol class="sv-flow cr-flow">{steps_html}</ol></div></section>

<section class="pd-cta" id="kirim"><div class="ct-wrap pd-cta-inner"><div><h2>Kirim profil Anda</h2><p>Sertakan bidang keahlian, kota domisili, dan link portofolio atau CV. Profil disimpan di talent network kami.</p></div>
<div class="cr-cta-actions"><a class="btn btn-purple" href="{mail('Talent Network Altora', TEMPLATE_BODY)}">Kirim lewat email</a><a class="cr-cta-wa" href="{WA}{quote('Halo Altora, saya ingin bergabung dengan talent network. Bidang keahlian saya: ')}" rel="noopener" target="_blank">atau lewat WhatsApp</a></div></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''
(root / 'careers.html').write_text(page, encoding='utf-8')
print(f'careers.html dibuat: {len(OPENINGS)} lowongan, {len(AREAS)} bidang')
