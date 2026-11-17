"""Bangun halaman lokal 'software house <kota>' dari data CITIES.
Jalankan dari root repo:  python3 scripts/build_local.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py
Isi setiap kota harus berbeda dan hanya memakai fakta yang bisa dipertanggungjawabkan."""
import html, json, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import OFFICES, ORG_ID, one_line, maps_link, org, office_node

root = pathlib.Path(__file__).resolve().parent.parent
CSS_VER = '20261016i'
SITE = 'https://altora.id'
WA = 'https://wa.me/6285190911170?text='
e = lambda t: html.escape(t, quote=True)

SERVICES = [
    ('/services/software-custom', 'Aplikasi & software custom', 'Web app, aplikasi HP, approval, dan laporan internal.'),
    ('/services/website-seo', 'Website', 'Company profile, website instansi, dan landing page yang cepat dan mudah diperbarui.'),
    ('/services/seo', 'SEO', 'Audit, perbaikan on-page, dan SEO lokal supaya mudah ditemukan di Google.'),
]
HERO = '/assets/img/apps/office-board.webp'


CITIES = [
    dict(slug='software-house-balikpapan', city='Balikpapan', area='Balikpapan',
         title='Software House Balikpapan | Altora Indonesia',
         desc='Altora Indonesia, software house di Balikpapan: jasa pembuatan aplikasi custom, website, dan SEO untuk perusahaan, instansi, dan UMKM.',
         h1='Software house di Balikpapan',
         lead='Altora Indonesia punya dua kantor cabang di Balikpapan, di Balikpapan Utara dan Pasar Baru. Kami membuat aplikasi custom, website, dan SEO untuk perusahaan, instansi, dan UMKM di Balikpapan.',
         why=[('Dua cabang di Balikpapan', 'Cabang kami di Jl. Soekarno Hatta, Muara Rapak (Balikpapan Utara) dan di Pasar Baru. Diskusi kebutuhan dan pelatihan bisa dilakukan langsung di lokasi Anda.'),
              ('Dibuat mengikuti proses Anda', 'Kami pelajari alur kerja dulu, lalu aplikasi dibuat bertahap dan diuji bersama pengguna, bukan memaksa proses Anda mengikuti software.'),
              ('Dukungan setelah jalan', 'Saat ada kendala, tim teknis menanggapi lewat WhatsApp dan video call, dan bisa datang ke lokasi bila diperlukan.')],
         needs=[('Perusahaan jasa migas, logistik, dan kontraktor', 'Aplikasi pelaporan, approval, dan dashboard yang menggantikan rekap manual di spreadsheet.'),
                ('Kantor dan instansi', 'Aplikasi persuratan, approval, dan website resmi yang mudah diperbarui.'),
                ('Toko, kafe, dan usaha jasa', 'Website yang ditemukan pelanggan di Google, serta aplikasi pencatatan sesuai cara usaha Anda.')],
         faq=[('Di mana kantor Altora di Balikpapan?', 'Ada dua cabang: Jl. Soekarno Hatta, Muara Rapak, Balikpapan Utara, dan Pasar Baru, Balikpapan. Kantor pusat kami di Samarinda. Untuk diskusi, kami juga bisa datang ke kantor Anda.'),
              ('Bisa dibuatkan aplikasi sesuai proses kerja kami?', 'Bisa. Kami pelajari alur kerja Anda dulu, lalu aplikasi dibuat bertahap dan diuji bersama pengguna.'),
              ('Apakah melayani pembuatan website dan SEO di Balikpapan?', 'Ya. Kami membuat website company profile dan website instansi, lalu menyusunnya agar mudah ditemukan di Google, termasuk SEO lokal untuk Balikpapan.')],
         nearby=[('/software-house-samarinda', 'Software house Samarinda'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'), ('/blog/cara-memilih-software-house-samarinda-balikpapan', 'Cara memilih software house')]),
    dict(slug='software-house-samarinda', city='Samarinda', area='Samarinda',
         title='Software House Samarinda | Altora Indonesia',
         desc='Software house di Samarinda: jasa pembuatan aplikasi custom, website, dan SEO untuk instansi, kampus, dan bisnis.',
         h1='Software house di Samarinda',
         lead='Altora Indonesia berkantor pusat di Samarinda. Kami membuat aplikasi custom, website, dan SEO untuk instansi, kampus, dan bisnis di Samarinda.',
         why=[('Kantor pusat di Samarinda', 'Kantor pusat kami di Perum Graha Indah Blok A13, Air Putih, Samarinda Ulu. Tim bisa datang untuk diskusi kebutuhan dan pelatihan di lokasi Anda.'),
              ('Terbiasa dengan administrasi instansi', 'Penawaran, faktur, berita acara serah terima, dan dokumentasi pekerjaan kami siapkan untuk kebutuhan administrasi.'),
              ('Bisa datang ke lokasi', 'Diskusi, demo, dan pelatihan pengguna dapat dilakukan langsung di kantor Anda di Samarinda.')],
         needs=[('Kelurahan, kecamatan, dan dinas', 'Website resmi dan aplikasi pelayanan yang mudah dipakai warga dan mudah dikelola petugas.'),
                ('Kampus dan sekolah', 'Website fakultas, portal informasi, dan aplikasi administrasi.'),
                ('Bisnis dan UMKM', 'Website yang muncul di Google dan aplikasi sesuai proses usaha.')],
         faq=[('Apakah bisa untuk instansi pemerintah?', 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara serah terima.'),
              ('Apakah melayani pembuatan website instansi?', 'Ya. Kami membuat website resmi yang bisa diperbarui sendiri oleh tim Anda.'),
              ('Bisa dibuatkan aplikasi sesuai proses kerja kami?', 'Bisa. Kami pelajari alur kerja Anda dulu, lalu aplikasi dibuat bertahap dan diuji bersama pengguna.'),
              ('Bagaimana memulai?', 'Hubungi kami lewat WhatsApp atau form konsultasi. Diskusi awal gratis.')],
         nearby=[('/software-house-balikpapan', 'Software house Balikpapan'), ('/software-house-kalimantan-timur', 'Software house Kalimantan Timur'), ('/jasa-pembuatan-website-samarinda', 'Jasa pembuatan website Samarinda')]),
    dict(slug='software-house-kalimantan-timur', city='Kalimantan Timur', area='Kalimantan Timur',
         title='Software House Kalimantan Timur | Altora Indonesia',
         desc='Software house di Kalimantan Timur: aplikasi custom, website, dan SEO untuk perusahaan dan instansi di Balikpapan, Samarinda, dan sekitarnya.',
         h1='Software house di Kalimantan Timur',
         lead='Altora Indonesia berkantor pusat di Samarinda, dengan dua cabang di Balikpapan. Kami melayani perusahaan dan instansi di Kalimantan Timur yang butuh aplikasi custom, website, atau SEO.',
         why=[('Paham kebutuhan Kaltim', 'Banyak pekerjaan di Kaltim ada di lapangan: tambang, logistik, perkebunan, dan pelayanan publik. Aplikasi dirancang untuk dipakai di kantor maupun di lokasi.'),
              ('Aplikasi yang tetap jalan di lapangan', 'Aplikasi dapat dirancang agar tetap berfungsi saat sinyal lemah, lalu menyinkronkan data begitu terhubung.'),
              ('Tim lokal', 'Kantor pusat di Samarinda dan dua cabang di Balikpapan. Tim kami bisa datang untuk diskusi kebutuhan dan pelatihan pengguna.')],
         needs=[('Tambang, kontraktor, dan logistik', 'Aplikasi pelaporan, approval, dan dashboard untuk lokasi kerja.'),
                ('Perkebunan dan pertanian', 'Aplikasi pencatatan lapangan yang tetap jalan saat sinyal lemah.'),
                ('Pemerintah daerah dan instansi', 'Website resmi dan aplikasi layanan publik.')],
         faq=[('Kota mana saja yang dilayani?', 'Kantor pusat kami di Samarinda dan cabang di Balikpapan. Kami juga melayani kabupaten dan kota lain di Kaltim, serta seluruh Indonesia secara jarak jauh.'),
              ('Apakah aplikasinya bisa dipakai di lokasi yang sinyalnya lemah?', 'Bisa. Aplikasi dapat dirancang menyimpan data sementara lalu mengirimnya saat sinyal tersedia.'),
              ('Bagaimana memulai?', 'Hubungi kami lewat WhatsApp atau form konsultasi. Diskusi awal gratis.')],
         nearby=[('/software-house-balikpapan', 'Software house Balikpapan'), ('/software-house-samarinda', 'Software house Samarinda'), ('/infrastruktur-hardware-kaltim', 'Infrastruktur & hardware Kaltim'), ('/services', 'Layanan kami')]),
]


def page(c):
    url = '/' + c['slug']
    if len(c['desc']) > 160:
        c['desc'] = c['desc'][:157].rsplit(' ', 1)[0].rstrip(',.:;') + '.'
    why = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in c['why'])
    needs = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in c['needs'])
    svc_list = SERVICES[:2] if c.get('remote') else SERVICES
    svcs = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for u, t, d in svc_list)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c['faq'])
    nearby = ''.join(f'<a href="{u}">{e(t)}</a>' for u, t in c['nearby'])
    offices = ''.join(f'<p><b>{e(o["label"])}</b><br/><a href="{e(maps_link(o))}" rel="noopener" target="_blank">{e(one_line(o))}</a></p>' for o in OFFICES)
    msg = f'Halo Altora, saya dari {c["city"]} dan ingin konsultasi kebutuhan software.'
    # Satu entitas Altora (org) yang menyediakan layanan untuk kota ini; simpul kantor hanya untuk kota yang punya kantor.
    local_offices = [o for o in OFFICES if not c.get('remote') and o['city'] == c['city']]
    ld = {'@context': 'https://schema.org', '@graph': [org()] + [office_node(o) for o in local_offices] + [
        {'@type': 'Service', '@id': SITE + url + '#layanan', 'name': c['h1'], 'serviceType': 'Software house',
         'description': c['desc'], 'url': SITE + url,
         'provider': {'@id': f"{SITE}/#kantor-{local_offices[0]['key']}" if local_offices else ORG_ID},
         'areaServed': {'@type': 'City' if c['area'] != 'Kalimantan Timur' else 'AdministrativeArea', 'name': c['area']},
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Layanan software house',
                             'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': t, 'url': SITE + u}} for u, t, _ in (SERVICES[:2] if c.get('remote') else SERVICES)]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': c['h1'], 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]}]}
    return f'''<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/><title>{e(c["title"])}</title><meta content="{e(c["desc"])}" name="description"/><link href="{SITE}{url}" rel="canonical"/><meta content="index,follow,max-image-preview:large" name="robots"/><meta content="id_ID" property="og:locale"/><meta content="website" property="og:type"/><meta content="{e(c["title"])}" property="og:title"/><meta content="{e(c["desc"])}" property="og:description"/><meta content="{SITE}{url}" property="og:url"/><meta content="{SITE}{HERO}" property="og:image"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/><link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/><link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body class="company-page"><header></header>
<main class="ct-page svd-page lc-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/">Beranda</a><span>/</span><span>{e(c["h1"])}</span></nav>
<p class="eyebrow eyebrow-purple">Altora Indonesia · {e(c["city"])}</p><h1>{e(c["h1"])}</h1><p class="ct-lead">{e(c["lead"])}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Konsultasi gratis</a><a class="svd-link" href="#lihat-juga">Lihat juga</a></div></div>
<figure class="svd-hero-pic"><img alt="{e(c["h1"])}" src="{HERO}" style="object-position:50% 45%"/><span class="svd-chip svd-chip-0">{e(c["city"])}</span><span class="svd-chip svd-chip-1">{"Dikerjakan jarak jauh" if c.get("remote") else "Tim lokal"}</span><span class="svd-chip svd-chip-2">Konsultasi gratis</span></figure>
</div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Kenapa memilih Altora di {e(c["city"])}</h2></div><div class="svd-dos lc-why">{why}</div></div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>{"Kebutuhan yang umum di " if c.get("remote") else "Kebutuhan yang sering kami kerjakan di "}{e(c["city"])}</h2></div><ul class="lc-needs">{needs}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Layanan software house kami</h2></div><div class="lc-svcs">{svcs}</div></div></section>
<section class="svd-sec" id="lihat-juga"><div class="ct-wrap">
<div class="svd-related"><b>Lihat juga</b>{nearby}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>Kantor</h2>{offices}<p><a href="tel:+6285190911170">+62 851-9091-1170</a> · <a href="mailto:hello@altora.id">hello@altora.id</a></p></div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh software house di {e(c["city"])}?</h2><p>Ceritakan kebutuhan Anda. Diskusi awal gratis.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>
<footer></footer>
<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>
'''


def region_entry(k, r):
    """Halaman 'Software house <daerah>' untuk daerah yang dilayani dari kantor terdekat."""
    from build_area import CITIES as AREA_CITIES
    o = next(x for x in OFFICES if x['key'] == r['office'])
    near = [n for n in r['near'] if n in AREA_CITIES][:3]
    return dict(slug=f'software-house-{k}', city=r['name'], area=r['name'], office=r['office'],
        title=f'Software House {r["name"]} | Altora Indonesia',
        desc=f'Software house untuk {r["name"]}: aplikasi custom, website, dan SEO. Dilayani tim Altora dari {o["city"]}.',
        h1=f'Software house untuk {r["name"]}',
        lead=f'Altora Indonesia melayani {r["name"]} dari {o["label"].lower()}. Kami membuat aplikasi custom, website, dan SEO untuk {r["sectors"]}.',
        why=[(f'Dilayani dari {o["city"]}', f'Pengerjaan berjalan lewat video call dan demo berkala; tim kami juga bisa datang dari {o["label"].lower()} untuk diskusi dan pelatihan di {r["name"]}.'),
             ('Satu tim dari awal sampai akhir', 'Analisis, desain, pengembangan, pelatihan, dan dukungan ditangani tim yang sama, jadi tidak ada saling lempar tanggung jawab.'),
             ('Bisa untuk lokasi jauh', 'Aplikasi dapat dirancang tetap berjalan saat sinyal lemah, lalu menyinkronkan data begitu terhubung.')],
        needs=r['needs'],
        faq=[(f'Apakah Altora melayani {r["name"]}?', f'Ya. {r["name"]} kami layani dari {o["label"].lower()} ({o["city"]}). Jadwal diskusi dan pelatihan kami sepakati bersama.'),
             (f'Layanan apa saja yang tersedia di {r["name"]}?', 'Pembuatan aplikasi custom, website, dan SEO.'),
             ('Bagaimana dukungan setelah sistem berjalan?', 'Kendala dicek jarak jauh lebih dulu. Bila perlu, teknisi dijadwalkan datang ke lokasi.'),
             ('Apakah bisa untuk instansi?', 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP.')],
        nearby=[(f'/software-house-{n}', f'Software house {AREA_CITIES[n]["name"]}') for n in near] + [(f'/jasa-pembuatan-aplikasi-{k}', f'Jasa pembuatan aplikasi {r["name"]}'), (f'/jasa-pembuatan-website-{k}', f'Jasa pembuatan website {r["name"]}'), ('/area-layanan', 'Semua area layanan')])


def nasional_entry(k, r):
    """'Software house <kota>' di luar Kaltim: hanya layanan jarak jauh, tanpa janji teknisi datang."""
    from build_area import CITIES as AREA_CITIES
    near = [n for n in r['near'] if n in AREA_CITIES][:3]
    return dict(slug=f'software-house-{k}', city=r['name'], area=r['name'], office='samarinda', remote=True,
        title=f'Software House {r["name"]} | Aplikasi & Website | Altora',
        desc=f'Software house untuk klien di {r["name"]}: aplikasi web dan HP, website, dan dashboard, dikerjakan jarak jauh oleh tim Altora Indonesia.',
        h1=f'Software house untuk {r["name"]}',
        lead=f'Altora Indonesia adalah software house dari Samarinda, Kalimantan Timur. Untuk perusahaan dan instansi di {r["name"]} ({r["seat"]}), kami membuat aplikasi web dan HP, website, dan dashboard, dikerjakan jarak jauh dengan demo rutin sampai serah terima.',
        why=[('Proses jarak jauh yang jelas', 'Kebutuhan dibahas lewat video call, progres ditunjukkan di server uji setiap tahap, dan semua keputusan tercatat. Anda tidak perlu menunggu kunjungan untuk melihat hasil.'),
             ('Pendampingan sampai dipakai', 'Pelatihan pengguna dan dukungan setelah aplikasi berjalan, dijadwalkan menyesuaikan zona waktu Anda.'),
             ('Bisa untuk instansi', 'Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara yang lengkap.')],
        needs=r['needs'],
        faq=[(f'Apakah Altora punya kantor di {r["name"]}?', f'Tidak. Kantor kami di Samarinda dan Balikpapan, Kalimantan Timur. Proyek aplikasi dan website untuk klien di {r["name"]} kami kerjakan jarak jauh, dan pertemuan langsung bisa dijadwalkan bila diperlukan.'),
             (f'Layanan apa yang tersedia untuk {r["name"]}?', 'Pembuatan aplikasi web dan HP, website, SEO, dashboard, dan integrasi sistem, semuanya dikerjakan jarak jauh.'),
             ('Bagaimana memantau progres kalau tidak bertemu langsung?', 'Ada jadwal demo rutin di server uji, catatan rapat, dan satu kontak yang bertanggung jawab atas proyek Anda.'),
             ('Bagaimana dukungan setelah aplikasi jalan?', 'Pelatihan pengguna dilakukan online, lalu kendala ditangani lewat WhatsApp, tiket support, dan akses jarak jauh sesuai kesepakatan.')],
        nearby=[(f'/software-house-{n}', f'Software house {AREA_CITIES[n]["name"]}') for n in near] + [(f'/jasa-pembuatan-aplikasi-{k}', f'Jasa pembuatan aplikasi {r["name"]}'), (f'/jasa-pembuatan-website-{k}', f'Jasa pembuatan website {r["name"]}'), ('/area-layanan#nasional', 'Kota lain di Indonesia')])


from regions import REGIONS
from regions_nasional import NASIONAL
CITIES += [region_entry(k, r) for k, r in REGIONS.items()]
CITIES += [nasional_entry(k, r) for k, r in NASIONAL.items()]


for c in CITIES:
    (root / f'{c["slug"]}.html').write_text(page(c), encoding='utf-8')
from build_area import update_sitemap
update_sitemap(['/' + c['slug'] for c in CITIES])
print('halaman lokal:', len(CITIES))
