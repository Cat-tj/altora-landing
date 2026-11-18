"""Halaman /infrastruktur-hardware-kaltim + dua blok beranda (Infrastruktur & Hardware, Contoh pekerjaan).
Penawaran ini untuk proyek infrastruktur perusahaan di Kalimantan Timur (Starlink, CCTV berbasis AI, jaringan & IoT).
Layanan perangkat kecil (CCTV rumahan, smart lock, smart home, IT support bulanan) tetap hanya Samarinda, lihat hw_redirects.py.
Tanpa harga, tanpa nama klien, tanpa angka karangan. Jalankan sebelum apply_shell.py (lihat build_all.sh).
Kartu portofolio dari portofolio_data.py. Blok beranda disisipkan di antara penanda <!-- infra:start --> ... <!-- infra:end -->."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import OFFICES, ORG_ID, org, office_node
from portofolio_data import BY, HOME_SLUGS, INFRA_SLUGS, card as pf_card

root = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://altora.id'
SLUG = 'infrastruktur-hardware-kaltim'
URL = '/' + SLUG
CSS_VER = '20261016i'
WA = 'https://wa.me/6285190911170?text='
MSG = 'Halo Altora, saya ingin konsultasi infrastruktur dan hardware (Starlink, CCTV AI, atau jaringan) di Kalimantan Timur.'
HERO = '/assets/img/services/cctv.webp'
e = lambda t: html.escape(t, quote=True)

TITLE = 'Infrastruktur & Hardware Kaltim | Starlink, CCTV AI | Altora'
DESC = 'Starlink untuk lokasi terpencil, CCTV dengan AI, jaringan dan IoT untuk perusahaan di Kalimantan Timur: Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya.'
H1 = 'Infrastruktur dan hardware untuk lokasi kerja di Kalimantan Timur'
LEAD = ('Internet satelit Starlink untuk lokasi tanpa fiber, CCTV yang bisa mengenali pelanggaran K3 dan penyusup, serta jaringan dan sensor '
        'yang dirapikan dan dirawat. Untuk tambang, perkebunan, kapal, gudang, kantor proyek, dan perusahaan di Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya.')

ICONS = {
    'sat': '<path d="M5 19 19 5"/><path d="M7 13a4 4 0 0 0 4 4M4 13a7 7 0 0 0 7 7"/><rect height="6" rx="1" transform="rotate(45 16 8)" width="8" x="12" y="5"/>',
    'tool': '<path d="M14 7a4 4 0 0 0-5 5l-5 5 3 3 5-5a4 4 0 0 0 5-5l-2.5 2.5-2-2z"/>',
    'plug': '<path d="M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0zM12 16v5"/>',
    'camera': '<path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/>',
    'helmet': '<path d="M4 16a8 8 0 0 1 16 0zM2 16h20v2H2zM12 8V5"/>',
    'zone': '<path d="M4 4h16v16H4z" stroke-dasharray="3 3"/><path d="M9 9h6v6H9z"/>',
    'monitor': '<rect height="12" rx="2" width="18" x="3" y="4"/><path d="M9 20h6M12 16v4"/>',
    'layout': '<rect height="16" rx="2" width="18" x="3" y="4"/><path d="M3 9h18M9 9v11"/>',
    'sensor': '<circle cx="12" cy="12" r="2.2"/><path d="M8.2 8.2a5.4 5.4 0 0 0 0 7.6M15.8 8.2a5.4 5.4 0 0 1 0 7.6M5.4 5.4a9.3 9.3 0 0 0 0 13.2M18.6 5.4a9.3 9.3 0 0 1 0 13.2"/>',
    'bell': '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
}
icon = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICONS[n]}</svg>'

# Tiga bidang (dipakai di beranda dan halaman): (id ikon beranda, judul, ringkasan beranda, chip, ringkasan halaman)
AREAS = [
    ('i-globe', 'Starlink untuk lokasi terpencil',
     'Terminal Starlink untuk tambang, kebun sawit, kapal, dan kantor proyek yang tidak terjangkau fiber.',
     ['Tambang & sawit', 'Kapal & vessel', 'Kantor proyek', 'Failover dual-WAN']),
    ('i-shield', 'CCTV dengan AI',
     'Kamera IP dengan analitik di perangkat tepi: pelanggaran APD/K3, penyusup di perimeter, dan hitung orang.',
     ['Deteksi APD/K3', 'Perimeter', 'Hitung orang', 'Command center']),
    ('i-layers', 'Jaringan, switch & IoT',
     'Kabel terstruktur, rak server, PoE switch, Wi-Fi roaming, dan sensor suhu atau asap, dengan perawatan berkala.',
     ['Kabel Cat6', 'PoE & Mikrotik', 'VLAN', 'Sensor ruang server']),
]



def home_blocks():
    cards = ''.join(
        f'<a class="hs-card reveal" data-d="{i}" href="{URL}"><span class="hs-ic"><svg class="ico"><use href="#{ic}"></use></svg></span><h3>{e(t)}</h3><p>{e(p)}</p>'
        f'<ul>{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul><em>Pelajari <svg class="ico ico-sm"><use href="#i-arrow"></use></svg></em></a>'
        for i, (ic, t, p, chips) in enumerate(AREAS))
    infra = (f'<section class="sec ti-sec" id="infrastruktur"><div class="wrap"><div class="tl-head"><p class="eyebrow eyebrow-purple">Infrastruktur &amp; hardware</p>'
             '<h2>Starlink, CCTV AI, dan jaringan untuk lokasi kerja di Kaltim</h2>'
             '<p>Untuk proyek infrastruktur perusahaan di Kalimantan Timur: Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya. '
             'Pasang CCTV rumahan, smart lock, smart home, dan IT support bulanan tetap di Samarinda.</p></div>'
             f'<div class="lc-svcs">{cards}</div>'
             f'<p style="margin:22px 0 0"><a class="btn btn-white" href="{URL}">Lihat infrastruktur &amp; hardware <svg class="ico ico-sm"><use href="#i-arrow"></use></svg></a></p></div></section>')
    cards6 = ''.join(pf_card(BY[k]) for k in HOME_SLUGS)
    porto = ('<section class="sec ti-sec" id="portofolio"><div class="wrap"><div class="tl-head"><p class="eyebrow eyebrow-purple">Portofolio</p>'
             '<h2>Proyek yang pernah kami kerjakan</h2>'
             '<p>Sebagian proyek perangkat, jaringan, AI, dan software untuk pemerintahan, kampus, industri, dan usaha di Kaltim.</p></div>'
             f'<div class="pf-grid">{cards6}</div>'
             '<p style="margin:22px 0 0"><a class="btn btn-white" href="/portofolio">Lihat semua portofolio <svg class="ico ico-sm"><use href="#i-arrow"></use></svg></a></p></div></section>')
    return f'<!-- infra:start -->{infra}{porto}<!-- infra:end -->'


def inject_home():
    block = home_blocks()
    for name in ('index.html', 'beranda.html'):
        p = root / name
        s = p.read_text(encoding='utf-8')
        if '<!-- infra:start -->' in s:
            s = re.sub(r'<!-- infra:start -->.*?<!-- infra:end -->', lambda _: block, s, flags=re.S)
        else:
            assert '<!-- ══════════ HOW WE WORK ══════════ -->' in s, name
            s = s.replace('<!-- ══════════ HOW WE WORK ══════════ -->', block + '\n<!-- ══════════ HOW WE WORK ══════════ -->', 1)
        if 'portofolio.css' not in s:
            s = s.replace('</head>', '<link rel="stylesheet" href="/assets/css/portofolio.css?v=20261118"/></head>', 1)
        p.write_text(s, encoding='utf-8')
    print('beranda: blok infrastruktur + contoh pekerjaan dipasang')


PAINS = [
    ('Lokasi tanpa fiber atau sinyal yang stabil', 'Tambang, kebun, kapal, dan kantor proyek sering hanya punya sinyal seluler yang putus-putus.'),
    ('CCTV hanya merekam, tidak memberi tahu', 'Pelanggaran APD atau orang masuk area terlarang baru ketahuan saat rekaman diputar ulang.'),
    ('Jaringan tumbuh tanpa rencana', 'Kabel berantakan, tanpa pemisahan jaringan, dan tidak ada yang bertanggung jawab saat putus.'),
]

DOS = [
    ('sat', 'Terminal Starlink', 'Terminal Starlink untuk site tambang, kebun sawit, vessel, dan kantor proyek yang tidak terjangkau kabel fiber optik.'),
    ('tool', 'Tiang dan grounding', 'Pemasangan mounting pole dan grounding anti-petir supaya terminal aman di lokasi terbuka.'),
    ('plug', 'Failover dual-WAN', 'Router Mikrotik dengan dua jalur internet, sehingga koneksi pindah otomatis saat salah satu jalur putus.'),
    ('camera', 'Kamera IP & edge AI', 'Kamera IP Hikvision, HiLook, atau Dahua dengan analitik AI yang berjalan di perangkat, bukan sekadar merekam.'),
    ('helmet', 'Deteksi APD/K3', 'Mengenali pekerja tanpa helm, rompi, atau sepatu safety, lalu mengirim peringatan.'),
    ('zone', 'Perimeter & hitung orang', 'Pengawasan pagar dan area terlarang di gudang, serta penghitungan orang di pintu atau area tertentu.'),
    ('monitor', 'Command center multi-cabang', 'Satu layar pantau untuk kamera dari beberapa cabang atau lokasi.'),
    ('layout', 'Kabel dan rak terstruktur', 'Kabel LAN Cat6, terminasi patch panel, dan server rack yang rapi; PoE switch, Mikrotik, dan Wi-Fi roaming.'),
    ('sensor', 'VLAN, sensor, dan perawatan', 'Pemisahan jaringan (misalnya kasir dan tamu), sensor suhu atau asap untuk ruang server, dan perawatan berkala dengan SLA.'),
]

STEPS = ['Survei lokasi & kebutuhan', 'Rancangan & penawaran', 'Pemasangan & konfigurasi', 'Uji & serah terima', 'Perawatan berkala']

FAQ = [
    ('Kota apa saja yang dilayani untuk infrastruktur dan hardware?', 'Kalimantan Timur: Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya. Kantor pusat kami di Samarinda dan dua cabang di Balikpapan, sehingga tim bisa datang ke lokasi untuk survei dan pemasangan.'),
    ('Apakah pasang CCTV rumahan, smart lock, dan IT support bulanan juga melayani Balikpapan?', 'Belum. Layanan perangkat kecil itu saat ini hanya untuk Samarinda. Halaman ini untuk proyek infrastruktur perusahaan di Kalimantan Timur, seperti site terpencil, CCTV berbasis AI, dan jaringan multi-cabang.'),
    ('Apakah Altora mitra resmi Starlink?', 'Tidak. Altora bukan mitra resmi Starlink. Kami membantu survei lokasi, pemasangan, grounding, dan integrasi ke jaringan Anda. Soal terminal dan langganan, kami bahas saat konsultasi. Starlink adalah merek dagang SpaceX.'),
    ('Apa yang bisa dikenali oleh CCTV AI?', 'Contohnya pelanggaran APD (helm, rompi, sepatu safety), orang yang masuk area perimeter, dan jumlah orang. Jenis deteksi yang cocok kami tentukan saat survei, karena hasilnya dipengaruhi sudut kamera dan pencahayaan.'),
    ('Merek kamera apa yang dipakai?', 'Kami memasang kamera IP seperti Hikvision, HiLook, dan Dahua, dan bisa menyesuaikan dengan perangkat yang sudah Anda punya.'),
    ('Bagaimana perawatannya?', 'Perawatan berkala bisa disepakati dalam kontrak SLA. Isi dan jadwalnya kami bahas bersama setelah survei.'),
]


def page():
    chips = ''.join(f'<span class="svd-chip svd-chip-{i}">{e(c)}</span>' for i, c in enumerate(['Kalimantan Timur', 'Tim lokal', 'Konsultasi gratis']))
    pains = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in PAINS)
    dos = ''.join(f'<article class="svd-do"><span class="svd-ico">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, t, d in DOS)
    steps = ''.join(f'<li><b>{e(s)}</b></li>' for s in STEPS)
    works = ''.join(pf_card(BY[k]) for k in INFRA_SLUGS)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    offices = ''.join(f'<p><b>{e(o["label"])}</b>, {e(o["street"])}, {e(o["city"])}</p>' for o in OFFICES)
    related = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in [
        ('/services/cctv', 'Pasang CCTV (Samarinda)'), ('/services/iot-custom', 'IoT custom'), ('/services/tracking', 'Tracking armada & aset'),
        ('/it-support-samarinda', 'IT support Samarinda'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'), ('/industri/pertambangan', 'Solusi tambang')])
    ld = {'@context': 'https://schema.org', '@graph': [org()] + [office_node(o) for o in OFFICES] + [
        {'@type': 'Service', '@id': SITE + URL + '#layanan', 'name': 'Infrastruktur dan hardware di Kalimantan Timur', 'serviceType': 'Infrastruktur jaringan, Starlink, dan CCTV AI',
         'description': DESC, 'url': SITE + URL, 'provider': {'@id': ORG_ID},
         'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Kalimantan Timur'}, {'@type': 'City', 'name': 'Balikpapan'}, {'@type': 'City', 'name': 'Samarinda'}],
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Infrastruktur dan hardware', 'itemListElement': [
             {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in ('Starlink untuk lokasi terpencil', 'CCTV dengan AI', 'Jaringan, switch, dan IoT')]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Layanan', 'item': SITE + '/services'},
            {'@type': 'ListItem', 'position': 3, 'name': 'Infrastruktur dan hardware Kalimantan Timur', 'item': SITE + URL}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]}
    wa = WA + quote(MSG)
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(TITLE)}</title><meta content="{e(DESC)}" name="description"/><link href="{SITE}{URL}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(TITLE)}" property="og:title"/><meta content="{e(DESC)}" property="og:description"/><meta content="{SITE}{URL}" property="og:url"/><meta content="{SITE}{HERO}" property="og:image"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><link rel="stylesheet" href="/assets/css/portofolio.css?v=20261118"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
<main class="ct-page svd-page lc-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/services">Layanan</a><span>/</span><span>Infrastruktur &amp; hardware</span></nav>
<p class="eyebrow eyebrow-purple">Altora Indonesia · Kalimantan Timur</p><h1>{e(H1)}</h1><p class="ct-lead">{e(LEAD)}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{wa}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#lihat-juga">Lihat juga</a></div></div>
<figure class="svd-hero-pic"><img alt="Infrastruktur dan hardware di Kalimantan Timur" src="{HERO}" style="object-position:50% 45%"/>{chips}</figure>
</div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Masalah yang sering kami temui</h2></div><ul>{pains}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang kami kerjakan</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Alur kerja</h2></div><ol class="svd-steps">{steps}</ol></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Contoh pekerjaan</h2></div><div class="pf-grid">{works}</div><div class="pf-actions"><a class="btn btn-white" href="/portofolio">Lihat semua portofolio →</a></div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Cakupan wilayah</h2><p>Infrastruktur dan hardware untuk perusahaan dan instansi di Kalimantan Timur: Balikpapan, Samarinda, IKN, Kutai, dan sekitarnya.</p><p>Pasang CCTV untuk rumah dan toko, smart lock, smart home, dan IT support bulanan saat ini hanya melayani Samarinda. Lihat <a href="/services/cctv">Pasang CCTV</a> dan <a href="/it-support-samarinda">IT support Samarinda</a>.</p>{offices}</div></div></section>
<section class="svd-sec" id="lihat-juga"><div class="ct-wrap">
<div class="svd-related"><b>Lihat juga</b>{related}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh infrastruktur atau hardware di Kaltim?</h2><p>Ceritakan lokasi dan kebutuhan Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{wa}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


if __name__ == '__main__':
    (root / f'{SLUG}.html').write_text(page(), encoding='utf-8')
    from build_area import update_sitemap
    update_sitemap([URL])
    sm = root / 'sitemap.xml'
    t = sm.read_text(encoding='utf-8')
    t = re.sub(r'(<loc>' + re.escape(SITE + URL) + r'</loc><lastmod>)[^<]*', r'\g<1>2026-11-18', t)
    sm.write_text(t, encoding='utf-8')
    inject_home()
    print('halaman:', URL)
