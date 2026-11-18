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
    dict(key='balikpapan-pasar-baru', label='Cabang Balikpapan Pasar Baru', city='Balikpapan', street='Pasar Baru',
         district='Balikpapan', region='Kalimantan Timur', postal='', hq=False),
]

# Titik kantor pusat Samarinda (Jl. Dayak ASB, Bukuan, Kec. Palaran).
# perkiraan, ganti dengan titik Google Maps dari pemilik (sekarang: titik tengah Kelurahan Bukuan dari OpenStreetMap).
OFFICE_SAMARINDA_GEO = (-0.5810649, 117.2105898)

# Angka perusahaan, sama dengan situs saudara (dikonfirmasi pemilik, 2026-11-18). Dipakai build_trust.py.
FACTS = dict(partners='6', since='2019', years='6+', projects='50+', team='13')

# Profil resmi Altora di luar situs (schema.org sameAs). Ini yang membuat Google & mesin AI yakin "Altora Indonesia"
# di altora.id adalah entitas yang sama dengan profil-profil ini, bukan Altora/Alterra lain. Isi HANYA URL milik Altora
# yang sudah aktif, misalnya Google Business Profile (link "Bagikan" di Maps), LinkedIn Company, Instagram, Clutch, Inaproc.
# Setelah diubah: python3 scripts/apply_schema.py (atau build_all.sh).
SAME_AS = []

ORG_ID = SITE + '/#organization'
LOGO = SITE + '/assets/img/altora-logo-600.png'

def hq():
    return next(o for o in OFFICES if o['hq'])


def one_line(o):
    parts = [o['street'], o['district'] if o['district'] != o['city'] else '', o['city'] if o['city'] not in o['district'] else '']
    return ', '.join(p for p in parts if p)


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
    return 'https://www.google.com/maps/search/?api=1&query=' + quote(f"Altora Indonesia {one_line(o)}, {o['region']}")


def maps_embed():
    """URL iframe Google Maps (tanpa API key) dengan pin kantor pusat Samarinda."""
    return 'https://www.google.com/maps?q={},{}&z=15&output=embed'.format(*OFFICE_SAMARINDA_GEO)


def maps_directions():
    return 'https://www.google.com/maps/dir/?api=1&destination={},{}'.format(*OFFICE_SAMARINDA_GEO)


def org():
    """Simpul Organization yang sama di setiap halaman. @id-nya sama dengan beranda, jadi Google menggabungkannya
    jadi satu entitas, bukan ratusan bisnis 'Altora Indonesia' yang berbeda."""
    n = {'@type': 'Organization', '@id': ORG_ID, 'name': 'Altora Indonesia', 'alternateName': ['Altora', 'Algora Teknologi Indonesia'],
         'url': SITE + '/', 'logo': {'@type': 'ImageObject', 'url': LOGO, 'width': 600, 'height': 600},
         'email': EMAIL, 'telephone': PHONE}
    if SAME_AS:
        n['sameAs'] = list(SAME_AS)
    return n


def office_node(o):
    """Kantor fisik sebagai ProfessionalService (LocalBusiness). Hanya untuk kantor yang benar-benar ada di OFFICES."""
    n = {'@type': 'ProfessionalService', '@id': f"{SITE}/#kantor-{o['key']}", 'name': f"Altora Indonesia – {o['label']}",
         'image': LOGO, 'url': SITE + '/', 'telephone': PHONE, 'email': EMAIL, 'address': postal_address(o),
         'hasMap': maps_link(o), 'parentOrganization': {'@id': ORG_ID}}
    if o.get('hq'):
        n['geo'] = {'@type': 'GeoCoordinates', 'latitude': OFFICE_SAMARINDA_GEO[0], 'longitude': OFFICE_SAMARINDA_GEO[1]}
    return n


def map_html():
    """Peta Google Maps (iframe tanpa API key, dimuat malas) dengan pin kantor pusat Samarinda + tautan petunjuk arah.
    Gaya .ofc-map ada di assets/css/footer.css (dimuat di semua halaman lewat partial footer)."""
    return ('<figure class="ofc-map"><iframe allowfullscreen="" height="260" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="{maps_embed()}" title="Peta lokasi kantor pusat Altora di Jl. Dayak ASB, Bukuan, Palaran, Samarinda" width="600"></iframe>'
            '<figcaption><span><b>Kantor pusat Samarinda</b>Jl. Dayak ASB, Bukuan, Kec. Palaran, Samarinda</span>'
            f'<a href="{maps_directions()}" rel="noopener" target="_blank">Petunjuk arah</a></figcaption></figure>')
