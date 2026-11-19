"""Satu sumber data perusahaan (NAP, kantor, angka) untuk semua generator.
Ubah di sini lalu jalankan ulang build_*.py + apply_shell.py + apply_seo.py."""

SITE = 'https://altora.id'
PHONE = '+6285190911170'
PHONE_DISPLAY = '+62 851-9091-1170'
EMAIL = 'hello@altora.id'

OFFICES = [
    dict(key='samarinda', label='Kantor pusat Samarinda', city='Samarinda', street='Jl. Dayak ASB, Bukuan',
         district='Kec. Palaran', region='Kalimantan Timur', postal='', hq=True),
    dict(key='balikpapan-utara', label='Cabang Balikpapan Utara', city='Balikpapan', street='Jl. Soekarno Hatta, Muara Rapak',
         district='Balikpapan Utara', region='Kalimantan Timur', postal='76125', hq=False),
    # Cabang Bekasi (dikonfirmasi pemilik 2026-11-20). Atas permintaan pemilik alamat sengaja ditampilkan samar
    # (tingkat kelurahan, tanpa nama jalan, RT/RW, atau titik pin). Layanan: software, website, SEO.
    dict(key='bekasi', label='Cabang Bekasi', city='Bekasi', street='Kaliabang Tengah',
         district='Kec. Bekasi Utara', region='Jawa Barat', postal='17125', hq=False),
]

# Titik kantor pusat Samarinda (Jl. Dayak ASB, Bukuan, Kec. Palaran).
# perkiraan, ganti dengan titik Google Maps dari pemilik (sekarang: titik tengah Kelurahan Bukuan dari OpenStreetMap).
OFFICE_SAMARINDA_GEO = (-0.5810649, 117.2105898)

# Angka perusahaan, sama dengan situs saudara (dikonfirmasi pemilik, 2026-11-18). Dipakai build_trust.py.
FACTS = dict(partners='6', since='2019', years='6+', projects='50+', team='13')

# Profil resmi Altora di luar situs (schema.org sameAs). Ini yang membuat Google & mesin AI yakin "Altora Indonesia"
# di altora.id adalah entitas yang sama dengan profil-profil ini, bukan Altora/Alterra lain (ada "Altora" di Australia).
# SENGAJA MASIH KOSONG: isi HANYA URL milik Altora yang sudah aktif, jangan menebak. Urutan yang disarankan:
#   1. Google Business Profile kantor pusat Samarinda (link "Bagikan" di Google Maps, bentuk https://maps.app.goo.gl/...)
#   2. Google Business Profile cabang Balikpapan (bila sudah diverifikasi)
#   3. LinkedIn Company Page  (https://www.linkedin.com/company/...)
#   4. Instagram resmi        (https://www.instagram.com/...)
#   5. Profil penyedia Inaproc/LKPP, Clutch, atau direktori bisnis lain yang memuat NAP yang sama
# Setelah diisi: sh scripts/build_all.sh (sameAs ikut ke semua simpul Organization + llms.txt).
SAME_AS = []

ORG_ID = SITE + '/#organization'
LOGO = SITE + '/assets/img/altora-logo-600.png'

def hq():
    return next(o for o in OFFICES if o['hq'])


def one_line(o):
    parts = [o['street'], o['district'] if o['district'] != o['city'] else '', o['city'] if o['city'] not in o['district'] else '']
    return ', '.join(p for p in parts if p)


def label_lc(o):
    """Label kantor untuk di tengah kalimat: 'kantor pusat Samarinda', 'cabang Balikpapan Utara' (nama kota tetap kapital)."""
    return o['label'].replace('Kantor pusat', 'kantor pusat').replace('Cabang', 'cabang')


def with_city(o):
    """Alamat satu baris yang pasti memuat nama kota tepat sekali (one_line + kota bila belum ada)."""
    a = one_line(o)
    return a if o['city'] in a else f"{a}, {o['city']}"


def postal_address(o):
    a = {'@type': 'PostalAddress', 'streetAddress': o['street'], 'addressLocality': o['city'],
         'addressRegion': o['region'], 'addressCountry': 'ID'}
    if o['postal']:
        a['postalCode'] = o['postal']
    return a


def maps_link(o):
    from urllib.parse import quote
    if o.get('hq'):
        return 'https://www.google.com/maps?q={},{}'.format(*OFFICE_SAMARINDA_GEO)
    if o.get('geo'):
        return 'https://www.google.com/maps?q={},{}'.format(*o['geo'])
    return 'https://www.google.com/maps/search/?api=1&query=' + quote(f"Altora Indonesia {one_line(o)}, {o['region']}")


def maps_embed():
    """URL iframe Google Maps (tanpa API key) dengan pin kantor pusat Samarinda."""
    return 'https://www.google.com/maps?q={},{}&z=15&output=embed'.format(*OFFICE_SAMARINDA_GEO)


def maps_directions():
    return 'https://www.google.com/maps/dir/?api=1&destination={},{}'.format(*OFFICE_SAMARINDA_GEO)


NAME = 'Altora Indonesia'
ALT_NAMES = ['Altora', 'Altora Indonesia', 'Algora Teknologi Indonesia']
FOUNDING_DATE = '2019'
EMPLOYEES = 13
DESCRIPTION = ('Altora Indonesia adalah software house yang berkantor pusat di Samarinda, Kalimantan Timur, sejak 2019, '
               'dengan cabang di Balikpapan Utara. Altora membuat software custom, aplikasi web dan mobile, website, SEO, AI, dan IoT, '
               'serta menyediakan pengadaan dan pemasangan perangkat untuk perusahaan dan instansi di Kalimantan Timur. '
               'Cabang Bekasi, Jawa Barat, melayani software, website, dan SEO untuk klien di Bekasi dan Jabodetabek.')
KNOWS_ABOUT = ['Software custom', 'Pembuatan aplikasi web', 'Pembuatan aplikasi mobile', 'Pembuatan website', 'Search engine optimization',
               'Artificial intelligence', 'Computer vision', 'Internet of Things', 'Fleet management', 'HRIS',
               'Pengadaan perangkat IT', 'CCTV', 'Jaringan komputer', 'Sistem informasi pemerintahan']
AREA_SERVED = [{'@type': 'City', 'name': 'Samarinda'}, {'@type': 'City', 'name': 'Balikpapan'},
               {'@type': 'AdministrativeArea', 'name': 'Kalimantan Timur'}, {'@type': 'City', 'name': 'Bekasi'},
               {'@type': 'Country', 'name': 'Indonesia'}]
# halaman kota tiap kantor (dipakai sebagai url simpul kantor)
OFFICE_PAGE = {'samarinda': '/software-house-samarinda', 'balikpapan-utara': '/software-house-balikpapan', 'bekasi': '/software-house-bekasi'}


def office_id(o):
    return f"{SITE}/#kantor-{o['key']}"


def org():
    """Simpul Organization ringkas yang sama di setiap halaman. @id-nya sama dengan beranda, jadi Google menggabungkannya
    jadi satu entitas. Semua nilainya identik dengan org_full() (subset), jadi tidak ada data yang saling bertentangan."""
    n = {'@type': 'Organization', '@id': ORG_ID, 'name': NAME, 'legalName': NAME, 'alternateName': list(ALT_NAMES),
         'url': SITE + '/', 'logo': {'@type': 'ImageObject', 'url': LOGO, 'width': 600, 'height': 600},
         'email': EMAIL, 'telephone': PHONE}
    if SAME_AS:
        n['sameAs'] = list(SAME_AS)
    return n


def org_full():
    """Simpul Organization lengkap (beranda, /about, /contact). Kantor fisik ditautkan lewat subOrganization."""
    n = org()
    n.update({'description': DESCRIPTION, 'image': LOGO, 'foundingDate': FOUNDING_DATE,
              'foundingLocation': {'@type': 'Place', 'name': 'Samarinda, Kalimantan Timur, Indonesia'},
              'numberOfEmployees': {'@type': 'QuantitativeValue', 'value': EMPLOYEES},
              'address': postal_address(hq()), 'areaServed': AREA_SERVED, 'knowsAbout': KNOWS_ABOUT,
              'contactPoint': [{'@type': 'ContactPoint', 'telephone': PHONE, 'email': EMAIL, 'contactType': 'customer service',
                                'areaServed': 'ID', 'availableLanguage': ['id', 'en']}],
              'subOrganization': [{'@id': office_id(o)} for o in OFFICES]})
    return n


def office_node(o):
    """Kantor fisik sebagai ProfessionalService (LocalBusiness) bertipe tambahan 'software company'.
    Hanya untuk kantor yang benar-benar ada di OFFICES. Tanpa jam buka dan priceRange (belum dinyatakan di situs)."""
    n = {'@type': 'ProfessionalService', '@id': office_id(o), 'additionalType': 'https://en.wikipedia.org/wiki/Software_company',
         'name': f"{NAME} – {o['label']}", 'image': LOGO, 'url': SITE + OFFICE_PAGE.get(o['key'], '/'),
         'telephone': PHONE, 'email': EMAIL, 'address': postal_address(o),
         'hasMap': maps_link(o), 'parentOrganization': {'@id': ORG_ID},
         'areaServed': [{'@type': 'City', 'name': o['city']}, {'@type': 'AdministrativeArea', 'name': o['region']}]}
    g = OFFICE_SAMARINDA_GEO if o.get('hq') else o.get('geo')
    if g:
        n['geo'] = {'@type': 'GeoCoordinates', 'latitude': g[0], 'longitude': g[1]}
    return n


def map_html(o=None):
    """Peta Google Maps (iframe tanpa API key, dimuat malas) + tautan petunjuk arah. Tanpa argumen: pin kantor pusat Samarinda.
    Untuk cabang (belum punya titik pasti) peta dicari dari alamat, jadi yang tampil adalah area jalannya.
    Gaya .ofc-map ada di assets/css/footer.css (dimuat di semua halaman lewat partial footer)."""
    if o is not None and not o.get('hq'):
        from urllib.parse import quote
        q = '{},{}'.format(*o['geo']) if o.get('geo') else quote(f"{with_city(o)}, {o['region']}")
        return ('<figure class="ofc-map"><iframe allowfullscreen="" height="260" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
                f'src="https://www.google.com/maps?q={q}&amp;z=15&amp;output=embed" title="Peta area {label_lc(o)} Altora: {one_line(o)}" width="600"></iframe>'
                f'<figcaption><span><b>{o["label"]}</b>{with_city(o)}</span></figcaption></figure>')
    return ('<figure class="ofc-map"><iframe allowfullscreen="" height="260" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="{maps_embed()}" title="Peta lokasi kantor pusat Altora di Jl. Dayak ASB, Bukuan, Palaran, Samarinda" width="600"></iframe>'
            '<figcaption><span><b>Kantor pusat Samarinda</b>Jl. Dayak ASB, Bukuan, Kec. Palaran, Samarinda</span></figcaption></figure>')


# FAQ entitas di beranda (HTML statis + FAQPage). Jawaban ditulis sebagai kalimat lengkap yang bisa dikutip mesin AI.
HOME_FAQ = [
    ('Apa itu Altora?',
     'Altora Indonesia (Altora) adalah software house dan penyedia solusi teknologi yang berkantor pusat di Samarinda, Kalimantan Timur, sejak 2019. '
     'Altora membuat software custom, aplikasi web dan mobile, website, SEO, AI, dan IoT, serta menyediakan pengadaan dan pemasangan perangkat. '
     'Lebih dari 50 proyek sudah diselesaikan oleh 13 ahli in-house.'),
    ('Di mana kantor Altora?',
     'Kantor pusat Altora Indonesia di Jl. Dayak ASB, Bukuan, Kecamatan Palaran, Kota Samarinda, Kalimantan Timur. '
     'Cabang di Balikpapan Utara (Jl. Soekarno Hatta, Muara Rapak) dan di Bekasi (Kaliabang Tengah, Bekasi Utara, Jawa Barat). Telepon/WhatsApp +62 851-9091-1170, email hello@altora.id.'),
    ('Apakah Altora software house di Samarinda?',
     'Ya. Altora Indonesia adalah software house yang berkantor pusat di Samarinda, dengan cabang di Balikpapan dan Bekasi. '
     'Klien kami di Samarinda antara lain Pemerintah Kota Samarinda dan Universitas Mulawarman.'),
    ('Apakah Altora juga melayani Balikpapan dan kota lain di Kalimantan Timur?',
     'Ya. Balikpapan dilayani dari cabang Balikpapan Utara, dan kabupaten/kota lain di Kalimantan Timur (Bontang, Kutai Kartanegara, Kutai Timur, Berau, Paser, '
     'Penajam Paser Utara, IKN, dan lainnya) dilayani dari kantor terdekat. Software juga dikerjakan jarak jauh untuk klien di seluruh Indonesia.'),
    ('Layanan apa saja yang dikerjakan Altora?',
     'Software custom, aplikasi web dan mobile, website, SEO, AI (analitik CCTV, pengenalan wajah), IoT, tracking armada, serta pengadaan dan pemasangan perangkat '
     'seperti CCTV, jaringan, server rack, GPS tracker, dan kit Starlink untuk perusahaan dan instansi di Kalimantan Timur. '
     'Pasang CCTV rumahan, smart lock, smart home, dan IT support bulanan khusus Samarinda.'),
    ('Apakah Altora bisa melayani pengadaan instansi pemerintah?',
     'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur pajak, dan berita acara serah terima.'),
    ('Bagaimana cara memulai proyek dengan Altora?',
     'Hubungi kami lewat WhatsApp +62 851-9091-1170 atau form konsultasi. Diskusi awal gratis; setelah kebutuhan jelas, kami kirim penawaran tertulis.'),
    ('Bagaimana pendampingan setelah proyek selesai?',
     'Kami melatih pengguna, lalu memberi dukungan lewat WhatsApp dan akses jarak jauh, serta kunjungan ke lokasi bila perlu, sesuai kontrak.'),
]
