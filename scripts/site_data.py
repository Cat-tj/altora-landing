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

FACTS = dict(founded='2019', founded_city='Samarinda', divisions='3', team='13', projects='50+', partners='4')


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
