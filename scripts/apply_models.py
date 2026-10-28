"""Pasang foto model (potongan seluruh badan) di hero halaman utama: Layanan, Artikel, Karier, Support, Konsultasi,
detail layanan, dan detail aplikasi. Idempoten: pemasangan lama dilepas dulu. Jalankan paling akhir di build_all.sh."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
IMG = '/assets/img/person-%s.webp'
ALT = {'hero': 'Staf Altora membawa tablet', 'flow': 'Staf Altora memperkenalkan layanan', 'cta': 'Staf Altora', 'support': 'Tim support Altora'}
# (berkas, penanda pembuka kontainer hero, model, kelas tambahan)
RULES = [
    ('services.html', '<div class="company-wrap services-hero-grid">', 'hero', 'hm-services'),
    ('blog.html', '<section class="bl-index-head"><div class="bl-wrap">', 'flow', 'hm-text'),
    ('careers.html', '<section class="ct-hero"><div class="ct-wrap">', 'cta', 'hm-text'),
    ('contact.html', '<section class="ct-hero">\n<div class="ct-wrap">', 'hero', 'hm-contact'),
    ('support.html', '<section class="sp-hero"><div class="ct-wrap sp-hero-grid">', 'support', 'hm-support'),
]
RULES_DIR = [
    ('services/*.html', '<div class="ct-wrap svd-hero-grid">', 'cta', 'hm-detail'),
    ('aplikasi/*.html', '<div class="ct-wrap ap2-hero">', 'flow', 'hm-detail'),
]
TAG = re.compile(r'<img alt="[^"]*" class="hero-model [^"]*" src="/assets/img/person-[a-z]+\.webp"/>')


def put(path, marker, model, cls):
    s = path.read_text(encoding='utf-8')
    s = TAG.sub('', s)
    # penanda dicari longgar terhadap spasi/baris baru
    pat = re.compile(r'\s*'.join(re.escape(p) for p in re.split(r'\s+', marker)))
    m = pat.search(s)
    if not m:
        return False
    img = f'<img alt="{ALT[model]}" class="hero-model {cls}" src="{IMG % model}"/>'
    s = s[:m.end()] + img + s[m.end():]
    if 'models.css' not in s:
        s = s.replace('</head>', '<link href="/assets/css/models.css?v=2" rel="stylesheet"/></head>', 1)
    path.write_text(s, encoding='utf-8')
    return True


n = 0
for f, marker, model, cls in RULES:
    n += put(root / f, marker, model, cls)
for pat, marker, model, cls in RULES_DIR:
    for p in sorted(root.glob(pat)):
        n += put(p, marker, model, cls)
print('foto model terpasang di', n, 'halaman')
