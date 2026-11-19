"""Halaman lokal perangkat untuk Kalimantan Timur yang dulu sudah punya peringkat di Google (Search Console, 2026-11):
- /jual-starlink-<kota>      kit Starlink + pemasangan, KHUSUS Kalimantan Timur (keputusan pemilik 2026-11-18).
                             Altora bukan mitra resmi Starlink; tanpa harga; schema hanya Service (tanpa Product).
- /jasa-pasang-cctv-<kota>   CCTV untuk perusahaan, site proyek, dan instansi (bukan CCTV rumahan: itu khusus Samarinda).
Juga menulis blok alihan bertanda di _redirects: /jual-starlink-<kota lain> -> /pengadaan (pengganti aturan wildcard lama,
karena Cloudflare Pages menjalankan alihan sebelum file statis). Jalankan lewat build_all.sh setelah hw_redirects.py."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, CITIES as AREA, SITE, WA, office_of
from site_data import ORG_ID, org, with_city, label_lc
from pengadaan_data import PRODUCTS as PG
from portofolio_data import BY as PF, card as pf_card

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)
TODAY = '2026-11-20'
TODAY_ID = '20 November 2026'
LOCAL_CSS = '<link rel="stylesheet" href="/assets/css/local-seo.css?v=20261120a"/>'
PF_CSS = '<link rel="stylesheet" href="/assets/css/portofolio.css?v=20261118p"/>'
KIT = {it[0]: it for it in PG['starlink'][0][1]}

# Konteks lokal per daerah: siapa yang butuh internet satelit di sana dan kit yang biasanya cocok.
STARLINK = {
    'samarinda': dict(where='rumah dan ruko di pinggiran kota yang belum terjangkau fiber, kantor yang butuh internet cadangan, serta kapal dan tongkang di Sungai Mahakam',
        kits=['starlink-v4', 'starlink-mini', 'starlink-enterprise'],
        cases=[('Rumah & ruko di pinggiran', 'Kawasan Palaran, Sambutan, dan Samarinda Utara yang belum terjangkau fiber.'),
               ('Internet cadangan kantor', 'Starlink sebagai jalur kedua (dual-WAN) saat fiber putus.'),
               ('Kapal di Sungai Mahakam', 'Kit Mini atau Performance untuk tugboat dan kapal operasional.')],
        q=('Apakah Starlink bisa dipasang di kapal yang beroperasi di Sungai Mahakam?', 'Bisa. Untuk kapal, kami sarankan kit Mini atau Performance dengan dudukan permanen, kabel yang dirapikan, dan daya dari aki kapal. Tipe pastinya kami tentukan setelah melihat kapalnya.')),
    'balikpapan': dict(where='kantor dan gudang yang butuh internet cadangan, kapal pendukung dan tugboat di Teluk Balikpapan, serta kawasan Balikpapan Timur dan Utara yang jauh dari jaringan',
        kits=['starlink-enterprise', 'starlink-performance-2', 'starlink-v4'],
        cases=[('Kantor & gudang', 'Jalur internet kedua dengan failover otomatis bila fiber terganggu.'),
               ('Kapal & tugboat', 'Instalasi permanen dengan wedge mount di kapal pendukung.'),
               ('Lokasi baru & proyek', 'Internet cepat menyala di lokasi yang belum ada jaringan.')],
        q=('Apakah Starlink bisa jadi internet cadangan kantor di Balikpapan?', 'Bisa. Kami pasang Starlink sebagai jalur kedua di router dual-WAN, sehingga koneksi berpindah otomatis saat jalur utama terganggu.')),
    'bontang': dict(where='kantor di kawasan pelabuhan dan industri yang butuh internet cadangan, kampung pesisir, serta kapal',
        kits=['starlink-enterprise', 'starlink-mini', 'starlink-v4'],
        cases=[('Kawasan industri & pelabuhan', 'Starlink sebagai jalur cadangan untuk kantor vendor dan kontraktor.'),
               ('Kampung pesisir', 'Internet untuk rumah dan usaha di pesisir yang sulit dijangkau kabel.'),
               ('Kapal & pos lapangan', 'Kit Mini yang ringkas dan hemat daya.')],
        q=('Apakah tim Altora datang ke Bontang untuk memasang?', 'Ya. Bontang kami layani dari kantor pusat Samarinda. Jadwal survei dan pemasangan kami sepakati lewat WhatsApp.')),
    'kutai-kartanegara': dict(where='desa di pedalaman dan pesisir, site tambang dan perkebunan, serta kantor desa dan sekolah',
        kits=['starlink-v4', 'starlink-performance-3', 'starlink-mini'],
        cases=[('Kantor desa & sekolah', 'Internet untuk pelayanan dan belajar di desa yang belum ada fiber.'),
               ('Tambang & perkebunan', 'Kit Performance untuk site yang panas, berdebu, dan berangin.'),
               ('Pesisir & sungai', 'Kit Mini untuk perahu dan pos di pesisir dan sepanjang sungai.')],
        q=('Apakah bisa dipasang di desa tanpa listrik PLN?', 'Bisa. Kami siapkan panel surya dan baterai yang dihitung dari kebutuhan daya kit Starlink dan perangkat Wi-Fi.')),
    'kutai-timur': dict(where='site tambang di sekitar Sangatta, perkebunan sawit, pelabuhan, dan desa yang jauh dari jaringan',
        kits=['starlink-performance-3', 'starlink-enterprise', 'starlink-v4'],
        cases=[('Site tambang', 'Kit Performance untuk pit office dan workshop di lokasi terbuka.'),
               ('Perkebunan sawit', 'Internet untuk kantor afdeling dan mess karyawan.'),
               ('Mess & camp', 'Wi-Fi mesh supaya sinyal merata di beberapa bangunan.')],
        q=('Apakah Wi-Fi bisa menjangkau beberapa bangunan di camp?', 'Bisa. Kami pasang Wi-Fi mesh atau access point outdoor supaya sinyal merata di mess, kantor, dan workshop.')),
    'kutai-barat': dict(where='kampung di pedalaman, perkebunan dan tambang, serta kantor pemerintahan kampung',
        kits=['starlink-mini', 'starlink-v4', 'starlink-performance-3'],
        cases=[('Kantor kampung', 'Internet untuk pelayanan dan pelaporan dari kampung.'),
               ('Perkebunan & tambang', 'Koneksi untuk kantor lapangan dan pelaporan harian.'),
               ('Lokasi tanpa PLN', 'Panel surya dan baterai untuk menyalakan kit dan Wi-Fi.')],
        q=('Berapa lama survei dan pemasangan di Kutai Barat?', 'Jadwal bergantung pada akses ke lokasi. Kami susun bersama setelah titik pemasangan dan kebutuhan daya jelas.')),
    'mahakam-ulu': dict(where='kampung di hulu Mahakam dan wilayah perbatasan, sekolah dan puskesmas, serta pos yang hanya bisa dicapai lewat sungai',
        kits=['starlink-mini', 'starlink-v4', 'starlink-mini-x'],
        cases=[('Sekolah & puskesmas', 'Internet untuk pelaporan dan layanan di kampung hulu.'),
               ('Kantor kampung', 'Koneksi untuk administrasi dan komunikasi.'),
               ('Pos lapangan', 'Kit Mini yang ringan dibawa lewat jalur sungai.')],
        q=('Apakah kit bisa dikirim dan dipasang di Mahakam Ulu?', 'Bisa, dengan jadwal yang disepakati karena akses ke lokasi lewat sungai. Kami siapkan kit, dudukan, dan daya sebelum berangkat supaya pemasangan selesai dalam satu kunjungan.')),
    'berau': dict(where='pulau dan penginapan wisata seperti Derawan dan Maratua, site tambang, pelabuhan, serta kapal',
        kits=['starlink-performance-3', 'starlink-mini', 'starlink-v4'],
        cases=[('Penginapan & wisata pulau', 'Wi-Fi tamu yang stabil di pulau dan pesisir.'),
               ('Tambang & pelabuhan', 'Kit Performance untuk kantor lapangan dan dermaga.'),
               ('Kapal', 'Kit Mini atau Performance dengan dudukan permanen.')],
        q=('Apakah bisa dipasang di penginapan di pulau?', 'Bisa. Kami survei titik antena yang bebas halangan, pasang grounding, dan sebar Wi-Fi ke kamar dan area tamu.')),
    'paser': dict(where='perkebunan sawit dan pabrik, site tambang, serta desa yang belum terjangkau fiber',
        kits=['starlink-v4', 'starlink-performance-3', 'starlink-enterprise'],
        cases=[('Perkebunan & pabrik', 'Internet untuk kantor kebun, timbangan, dan mess.'),
               ('Site tambang', 'Kit Performance untuk kondisi lapangan yang berat.'),
               ('Desa', 'Internet untuk kantor desa, sekolah, dan usaha.')],
        q=('Dari kantor mana Paser dilayani?', 'Paser kami layani dari cabang Balikpapan Utara. Jadwal survei dan pemasangan kami sepakati lewat WhatsApp.')),
    'penajam-paser-utara': dict(where='site proyek konstruksi, kantor kontraktor, perkebunan, dan permukiman baru',
        kits=['starlink-enterprise', 'starlink-v4', 'starlink-performance-3'],
        cases=[('Kantor proyek', 'Internet cepat menyala di direksi keet dan kantor sementara.'),
               ('Perkebunan', 'Koneksi untuk kantor kebun dan pelaporan.'),
               ('Permukiman baru', 'Internet rumah sebelum jaringan fiber masuk.')],
        q=('Apakah kit bisa dipindah saat proyek pindah lokasi?', 'Bisa. Kit Starlink bisa dibongkar dan dipasang ulang; kami bantu memindahkan dudukan, kabel, dan Wi-Fi ke lokasi baru.')),
    'ikn': dict(where='site konstruksi Ibu Kota Nusantara, kantor proyek sementara, dan mess pekerja',
        kits=['starlink-enterprise', 'starlink-performance-3', 'starlink-v4'],
        cases=[('Site konstruksi', 'Koneksi untuk CCTV proyek, laporan harian, dan rapat online.'),
               ('Kantor proyek sementara', 'Dual-WAN dan Wi-Fi untuk banyak pengguna.'),
               ('Mess pekerja', 'Wi-Fi merata di beberapa bangunan dengan mesh outdoor.')],
        q=('Apakah Starlink bisa dipakai untuk CCTV di site proyek IKN?', 'Bisa. Starlink dan CCTV dapat dipasang sekaligus, termasuk perekaman lokal di NVR supaya rekaman tetap aman saat koneksi terganggu.')),
}
CCTV = {
    'bontang': dict(where='kawasan industri, pelabuhan, gudang vendor, kantor, sekolah, dan perumahan karyawan',
        cases=[('Gudang & yard', 'Kamera bullet dan PTZ untuk area luas, dengan rekaman di NVR.'),
               ('Kantor kontraktor', 'Kamera dome, akses dari HP, dan hak lihat per pengguna.'),
               ('Area tanpa listrik', 'CCTV tenaga surya dan 4G untuk pos dan pagar jauh.')]),
    'kutai-kartanegara': dict(where='site tambang, perkebunan, kantor pemerintahan, pelabuhan sungai, dan gudang',
        cases=[('Site tambang', 'Analitik AI untuk kepatuhan APD dan area terlarang.'),
               ('Perkebunan & gudang', 'Kamera tenaga surya dan 4G untuk lokasi tanpa listrik.'),
               ('Kantor & instansi', 'CCTV kantor dengan NVR dan akses dari HP.')]),
    'ikn': dict(where='site konstruksi Ibu Kota Nusantara, kantor proyek, gudang material, dan mess pekerja',
        cases=[('Site konstruksi', 'Pemantauan progres dan keamanan material, termasuk deteksi APD berbasis AI.'),
               ('Gudang material', 'Kamera dengan deteksi penyusup di perimeter.'),
               ('Lokasi tanpa listrik', 'CCTV tenaga surya dan 4G yang bisa dipindah mengikuti proyek.')]),
}
STARLINK_DOS = [('Survei titik pemasangan', 'Kami cek pandangan langit, halangan pohon dan bangunan, serta jalur kabel sebelum memasang.'),
                ('Mounting yang kokoh', 'Tiang, dudukan atap, atau dudukan kapal yang tahan angin dan getaran.'),
                ('Grounding anti-petir', 'Tiang dan perangkat dibumikan untuk mengurangi risiko sambaran petir.'),
                ('Wi-Fi sampai ke titik kerja', 'Repeater, mesh, atau access point outdoor supaya sinyal merata.'),
                ('Failover dual-WAN', 'Starlink sebagai jalur cadangan yang aktif otomatis saat fiber putus.'),
                ('Daya off-grid', 'Panel surya dan baterai untuk lokasi tanpa listrik PLN.')]
CCTV_DOS = [('Survei titik kamera', 'Kami tentukan posisi kamera agar area penting terlihat jelas tanpa titik buta.'),
            ('Kamera IP & NVR resmi', 'VIGI dan Dahua dari mitra resmi; Hikvision dan HiLook juga tersedia.'),
            ('Analitik AI', 'Deteksi APD/K3, penyusup di perimeter, dan hitung orang dari kamera.'),
            ('Tenaga surya & 4G', 'Untuk pos, pagar, dan site yang jauh dari listrik dan kabel.'),
            ('Jaringan PoE & rak', 'Switch PoE, kabel terstruktur, rak, dan UPS yang rapi.'),
            ('Perawatan berkala', 'Pembersihan kamera, cek rekaman, dan pembaruan firmware sesuai kontrak.')]


def kit_card(kid, city):
    _, brand, name, img, desc, specs = KIT[kid]
    lis = ''.join(f'<li>{e(k)}: {e(v)}</li>' for k, v in specs)
    msg = f'Halo Altora, saya di {city} dan ingin penawaran kit {name} beserta pemasangannya.'
    return (f'<article class="pk-item"><div class="pk-pic"><img alt="Kit {e(name)}" loading="lazy" src="/assets/img/pengadaan/{e(img)}"/></div>'
            f'<small>Kit Starlink</small><h3>{e(name)}</h3><p>{e(desc)}</p><ul>{lis}</ul>'
            f'<div class="vg-act"><a class="vg-ask" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Minta penawaran</a></div></article>')


def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def common(kind, k, url, title, desc, h1, lead, eyebrow, hero, hero_alt, chips, sections, faq, links, msg, facts=''):
    c = AREA[k]
    ld = {'@context': 'https://schema.org', '@graph': [org(),
        {'@type': 'WebPage', '@id': SITE + url + '#halaman', 'url': SITE + url, 'name': title, 'description': desc, 'inLanguage': 'id-ID',
         'isPartOf': {'@id': SITE + '/#website'}, 'publisher': {'@id': ORG_ID}, 'about': {'@id': SITE + url + '#layanan'}, 'dateModified': TODAY},
        {'@type': 'Service', '@id': SITE + url + '#layanan', 'name': h1, 'description': desc, 'url': SITE + url, 'serviceType': kind,
         'areaServed': {'@type': 'City' if k in ('samarinda', 'balikpapan', 'bontang') else 'AdministrativeArea', 'name': c['name']},
         'provider': {'@id': ORG_ID}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Pengadaan', 'item': SITE + '/pengadaan'},
            {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': SITE + url}]},
        faq_ld(faq)]}
    faq_html = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    rel = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in links)
    ch = ''.join(f'<span class="svd-chip svd-chip-{i}">{e(t)}</span>' for i, t in enumerate(chips))
    body = f'''<main class="ct-page svd-page lc-page pk-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/pengadaan">Pengadaan</a><span>/</span><span>{e(c["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">{e(eyebrow)}</p><h1>{e(h1)}</h1><p class="ct-lead">{e(lead)}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Minta penawaran</a><a class="svd-link" href="#layanan">Lihat layanan</a></div></div>
<figure class="svd-hero-pic pk-hero-pic"><img alt="{e(hero_alt)}" src="{hero}"/>{ch}</figure>
</div></section>
{facts}
{sections}
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq_html}</div></div></section>
<section class="svd-sec" id="lihat-juga"><div class="ct-wrap"><div class="svd-related"><b>Lihat juga</b>{rel}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Siap dipasang di {e(c["name"])}?</h2><p>Ceritakan lokasi dan kebutuhan Anda. Penawaran tertulis kami kirim lewat chat.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    if len(desc) > 160:
        desc = desc[:157].rsplit(' ', 1)[0].rstrip(',.:;') + '.'
    return shell(title, desc, url, SITE + hero, ld, body, extra_head=PF_CSS + LOCAL_CSS)


def starlink_page(k):
    c, d = AREA[k], STARLINK[k]
    o = office_of(c)
    url = f'/jual-starlink-{k}'
    name = c['name']
    title = f'Starlink {name}: Jual Kit & Jasa Pasang | Altora'
    if len(title) > 65:
        title = f'Starlink {name}: Kit & Pemasangan | Altora'
    desc = f'Kit Starlink di {name}: pengadaan kit, survei, mounting, grounding, Wi-Fi, dan daya surya oleh tim Altora dari {o["city"]}. Khusus Kalimantan Timur.'
    h1 = f'Jual kit Starlink dan pemasangan di {name}'
    lead = (f'Pengadaan kit Starlink beserta pemasangannya di {name}: untuk {d["where"]}. Tim kami dari {label_lc(o)} '
            'mensurvei titik, memasang dudukan dan grounding, lalu menyebar Wi-Fi sampai ke titik kerja.')
    facts_rows = [('Layanan', 'Pengadaan kit Starlink, survei lokasi, mounting, grounding, Wi-Fi, failover dual-WAN, dan daya surya'),
                  ('Wilayah', f'{name} dan seluruh Kalimantan Timur (khusus Kaltim)'),
                  ('Dilayani dari', f'{o["label"]}, {with_city(o)}'),
                  ('Kontak', 'WhatsApp/telepon +62 851-9091-1170 · hello@altora.id'),
                  ('Status', 'Bukan mitra resmi Starlink; PKP dan terdaftar di Inaproc/LKPP'),
                  ('Harga', 'Penawaran tertulis setelah lokasi dan kebutuhan jelas')]
    dl = ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in facts_rows)
    facts = (f'<section class="svd-sec lc-facts-sec" id="ringkasan"><div class="ct-wrap"><div class="lc-facts"><h2>Ringkasan: Starlink di {e(name)}</h2><dl>{dl}</dl>'
             f'<p class="lc-note">Diperbarui <time datetime="{TODAY}">{TODAY_ID}</time>.</p></div></div></section>')
    steps = [('Chat lokasi & kebutuhan', 'Kirim titik lokasi, jenis bangunan atau kapal, dan jumlah pengguna lewat WhatsApp.'),
             ('Survei & rekomendasi kit', 'Kami cek pandangan langit, jalur kabel, dan sumber daya, lalu menyarankan tipe kit.'),
             ('Penawaran tertulis', 'Rincian kit, dudukan, kabel, Wi-Fi, dan daya dikirim tertulis sebelum pekerjaan dimulai.'),
             ('Pemasangan & uji', 'Kit dipasang, dibumikan, Wi-Fi disebar, lalu koneksi diuji bersama Anda.')]
    steps_html = ''.join(f'<li><b>{e(t)}</b><span>{e(x)}</span></li>' for t, x in steps)
    cases = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(x)}</p></article>' for t, x in d['cases'])
    kits = ''.join(kit_card(x, name) for x in d['kits'])
    dos = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(x)}</p></article>' for t, x in STARLINK_DOS)
    sections = f'''<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Siapa yang memakai Starlink di {e(name)}</h2></div><div class="svd-dos">{cases}</div></div></section>
<section class="svd-sec" id="produk"><div class="ct-wrap"><div class="pd-block-head"><h2>Kit yang biasanya cocok untuk {e(name)}</h2><p>Tipe pastinya kami tentukan setelah survei. Semua kit di <a href="/pengadaan#starlink">katalog pengadaan</a>.</p></div><div class="pk-grid">{kits}</div></div></section>
<section class="svd-sec" id="layanan"><div class="ct-wrap"><div class="pd-block-head"><h2>Pemasangan sampai Wi-Fi menyala</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Cara pesan Starlink di {e(name)}</h2></div><ol class="lc-needs lc-steps">{steps_html}</ol></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Dilayani dari {e(label_lc(o))}</h2><p>{e(c["base"])}</p>
<p>Kantor terdekat: {e(o["label"])}, {e(with_city(o))}. Telepon/WhatsApp +62 851-9091-1170.</p>
<p class="lc-note">Altora bukan mitra resmi Starlink. Kami membantu pengadaan kit Starlink dan pemasangannya, khusus wilayah Kalimantan Timur. Aktivasi dan langganan kami bahas saat konsultasi. Starlink adalah merek dagang SpaceX.</p></div></div></section>'''
    faq = [d['q'],
           ('Apakah Altora mitra resmi Starlink?', 'Tidak. Altora bukan mitra resmi Starlink. Kami membantu pengadaan kit, survei lokasi, pemasangan, grounding, dan integrasi ke jaringan Anda. Starlink adalah merek dagang SpaceX.'),
           ('Wilayah mana yang dilayani untuk kit Starlink?', 'Hanya Kalimantan Timur: Samarinda, Balikpapan, Bontang, Berau, Kutai Kartanegara, Kutai Timur, Kutai Barat, Mahakam Ulu, Paser, Penajam Paser Utara, dan IKN.'),
           (f'Berapa harga kit Starlink dan pemasangan di {name}?', 'Kami tidak memasang daftar harga karena kebutuhan dudukan, kabel, Wi-Fi, dan daya berbeda di tiap lokasi. Kirim lokasi dan kebutuhan Anda lewat WhatsApp; kami balas dengan penawaran tertulis.'),
           ('Apa saja yang termasuk dalam pemasangan Starlink?', 'Survei titik, dudukan (tiang, atap, atau kapal), perapian kabel, grounding anti-petir, dan pengaturan Wi-Fi. Bila perlu: failover dual-WAN, Wi-Fi mesh, serta panel surya dan baterai.'),
           (f'Kit Starlink mana yang cocok di {name}?', 'Standard untuk rumah dan kantor kecil, Mini untuk kapal atau lokasi yang sering berpindah, serta Performance atau Enterprise untuk tambang, proyek, dan banyak pengguna. Tipe pastinya kami tentukan setelah survei.'),
           ('Bagaimana dengan aktivasi dan langganan?', 'Aktivasi dan pilihan langganan kami bahas saat konsultasi, sesuai pemakaian Anda.'),
           ('Apakah bisa untuk pengadaan instansi?', 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.')]
    links = [('/pengadaan#starlink', 'Katalog kit Starlink'), ('/infrastruktur-hardware-kaltim', 'Infrastruktur & hardware Kaltim'),
             (f'/software-house-{k}', f'Software house {name}')] + ([(f'/jasa-pasang-cctv-{k}', f'Jasa pasang CCTV {name}')] if k in CCTV or k == 'samarinda' else []) + \
            [(f'/jual-starlink-{n}', f'Kit Starlink {AREA[n]["name"]}') for n in c.get('near', []) if n in STARLINK][:3]
    msg = f'Halo Altora, saya di {name} dan ingin konsultasi kit Starlink beserta pemasangannya.'
    return url, common('Pengadaan dan pemasangan kit Starlink', k, url, title, desc, h1, lead, f'Kit Starlink · {name} · Kalimantan Timur',
                       '/assets/img/pengadaan/starlink-v5.webp', f'Kit Starlink untuk pemasangan di {name}', [name, 'Survei & pasang', 'Khusus Kaltim'],
                       sections, faq, links, msg, facts)


def cctv_page(k):
    c, d = AREA[k], CCTV[k]
    o = office_of(c)
    url = f'/jasa-pasang-cctv-{k}'
    name = c['name']
    title = f'Jasa Pasang CCTV {name} untuk Perusahaan | Altora'
    desc = f'Jasa pasang CCTV di {name} untuk perusahaan, site proyek, dan instansi: kamera IP & NVR resmi, analitik AI, tenaga surya & 4G, dan perawatan.'
    h1 = f'Jasa pasang CCTV di {name} untuk perusahaan dan instansi'
    lead = (f'CCTV untuk {d["where"]} di {name}. Dari survei titik kamera, pemasangan kamera IP dan NVR, sampai analitik AI '
            f'dan perawatan berkala, dikerjakan tim Altora dari {label_lc(o)}.')
    cases = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(x)}</p></article>' for t, x in d['cases'])
    dos = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(x)}</p></article>' for t, x in CCTV_DOS)
    proof = ''.join(pf_card(PF[s]) for s in ('deteksi-apd-ai', 'cctv-ai-farmasi-unmul', 'iot-monitoring-gudang') if s in PF)
    sections = f'''<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Kebutuhan CCTV di {e(name)}</h2></div><div class="svd-dos">{cases}</div></div></section>
<section class="svd-sec" id="layanan"><div class="ct-wrap"><div class="pd-block-head"><h2>Yang kami kerjakan</h2><p>Perangkat lengkap ada di <a href="/pengadaan#cctv">katalog pengadaan CCTV</a>.</p></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec" id="proyek"><div class="ct-wrap"><div class="pd-block-head"><h2>Contoh proyek CCTV dan pemantauan kami</h2><p>Proyek nyata tim Altora di Kalimantan Timur. Nama klien tertera di setiap kartu.</p></div><div class="pf-grid">{proof}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Dilayani dari {e(label_lc(o))}</h2><p>{e(c["base"])}</p>
<p class="lc-note">Halaman ini untuk CCTV perusahaan, site proyek, dan instansi. Pasang CCTV rumahan saat ini khusus Samarinda.</p></div></div></section>'''
    faq = [('Apakah melayani CCTV untuk rumah di ' + name + '?', 'Untuk saat ini pasang CCTV rumahan khusus Samarinda. Di ' + name + ' kami melayani CCTV untuk perusahaan, site proyek, dan instansi.'),
           ('Merek CCTV apa yang dipasang?', 'VIGI by TP-Link dan Dahua sebagai mitra resmi; Hikvision dan HiLook juga tersedia sesuai kebutuhan proyek.'),
           ('Apakah CCTV bisa mendeteksi pelanggaran APD?', 'Bisa. Analitik AI dapat mengenali helm, rompi, dan sepatu safety, lalu mencatat kejadian beserta fotonya untuk tim K3.'),
           ('Bagaimana untuk lokasi tanpa listrik dan internet?', 'Kami pasang CCTV tenaga surya dengan modem 4G, atau digabung dengan kit Starlink untuk lokasi tanpa sinyal seluler.'),
           ('Berapa biaya pemasangan CCTV?', 'Bergantung jumlah titik, jarak kabel, dan perangkat pendukung. Kami tentukan setelah survei, lalu kirim penawaran tertulis lewat chat.'),
           ('Apakah bisa untuk pengadaan instansi?', 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.')]
    links = [('/pengadaan#cctv', 'Katalog CCTV'), ('/infrastruktur-hardware-kaltim', 'CCTV AI untuk perusahaan (Kaltim)'), (f'/jual-starlink-{k}', f'Kit Starlink {name}'),
             (f'/software-house-{k}', f'Software house {name}'), (f'/jasa-pembuatan-aplikasi-{k}', f'Jasa pembuatan aplikasi {name}')]
    msg = f'Halo Altora, saya di {name} dan butuh pemasangan CCTV untuk perusahaan/proyek.'
    return url, common('Pemasangan CCTV untuk perusahaan dan instansi', k, url, title, desc, h1, lead, f'CCTV perusahaan & proyek · {name}',
                       '/assets/img/services/cctv.webp', f'Kamera CCTV terpasang untuk pemantauan area kerja di {name}', [name, 'Analitik AI', 'Tenaga surya & 4G'],
                       sections, faq, links, msg)


def write_redirects():
    """Ganti aturan wildcard /jual-starlink-* dengan alihan eksplisit untuk kota yang tidak punya halaman (di luar Kaltim)."""
    from regions_nasional import NASIONAL
    lines = [f'/jual-starlink-{k}    /pengadaan    301' for k in NASIONAL if k not in STARLINK]
    p = root / '_redirects'; s = p.read_text(encoding='utf-8')
    s = re.sub(r'# starlink-kota:start.*?# starlink-kota:end\n', '', s, flags=re.S)
    s = s.replace('/jual-starlink-*    /pengadaan    301\n', '')
    block = ('# starlink-kota:start (scripts/build_kaltim_hw.py) kit Starlink khusus Kaltim; kota lain -> /pengadaan\n'
             + '\n'.join(lines) + '\n# starlink-kota:end\n')
    p.write_text(block + s.lstrip('\n'), encoding='utf-8')
    return len(lines)


if __name__ == '__main__':
    from build_area import CCTV_PERUSAHAAN
    assert set(CCTV_PERUSAHAAN) == set(CCTV), 'samakan build_area.CCTV_PERUSAHAAN dengan CCTV'
    assert set(STARLINK) == {k for k, v in AREA.items() if v.get('scope') != 'nasional'}, 'kit Starlink: semua kota Kaltim'
    urls = []
    for k in STARLINK:
        url, page = starlink_page(k); (root / f'{url[1:]}.html').write_text(page, encoding='utf-8'); urls.append(url)
    for k in CCTV:
        url, page = cctv_page(k); (root / f'{url[1:]}.html').write_text(page, encoding='utf-8'); urls.append(url)
    update_sitemap(urls, lastmod=TODAY)
    n = write_redirects()
    print(f'perangkat Kaltim: {len(urls)} halaman, {n} alihan starlink luar Kaltim')
