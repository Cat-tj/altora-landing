"""Satu sumber data perusahaan (NAP, kantor, angka) untuk semua generator.
Ubah di sini lalu jalankan ulang build_*.py + apply_shell.py + apply_seo.py."""

SITE = 'https://altora.id'
PHONE = '+6285190911170'
PHONE_DISPLAY = '+62 851-9091-1170'
EMAIL = 'hello@altora.id'

OFFICES = [
    dict(key='samarinda', label='Kantor pusat Samarinda', city='Samarinda', street='Perum Graha Indah Blok A13, Air Putih',
         district='Samarinda Ulu', region='Kalimantan Timur', postal='', hq=True),
    dict(key='balikpapan-utara', label='Cabang Balikpapan Utara', city='Balikpapan', street='Jl. Soekarno Hatta, Muara Rapak',
         district='Balikpapan Utara', region='Kalimantan Timur', postal='76125', hq=False),
    dict(key='balikpapan-pasar-baru', label='Cabang Balikpapan Pasar Baru', city='Balikpapan', street='Pasar Baru',
         district='Balikpapan', region='Kalimantan Timur', postal='', hq=False),
]

FACTS = dict(partners='6')   # hanya fakta yang dapat diverifikasi; tahun berdiri/jumlah proyek/tim dihapus (pisah dari Sentra)

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
    return 'https://www.google.com/maps/search/?api=1&query=' + quote(f"Altora Indonesia {one_line(o)}, {o['region']}")


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
    return n
