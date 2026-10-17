"""Pembuka beranda 'gedung Altora' (Three.js), dipasang di beranda (index.html) dan /preview-gedung (noindex).
Beranda tetap utuh di HTML (SEO); adegan 3D hanya lapisan pembuka di depannya:
gedung -> scroll pertama: menu lantai -> scroll kedua: atap terbuka, kamera masuk ke ruang meeting, layar proyektor
menampilkan hero beranda dan memenuhi layar -> kanvas disembunyikan, beranda asli berlanjut. Klik lantai -> halamannya.
Tanpa WebGL / prefers-reduced-motion: adegan tidak tampil sama sekali, beranda biasa.
Animasi: assets/js/gedung3d.js; gaya adegan: assets/css/gedung-scenes.css.
Idempoten: pembuka lama dilepas dulu sebelum dipasang ulang, jadi aman dijalankan berkali-kali.
Jalankan lewat scripts/build_all.sh (setelah build_produk/build_trust yang mengubah index.html)."""
import pathlib, re

JS_V, CSS_V, BACK_V = 252, 14, 4
root = pathlib.Path(__file__).resolve().parent.parent
idx = root / 'index.html'
s = idx.read_text(encoding='utf-8')

INTRO = ('<div class="gd-scene" data-to="8"><div class="gd-scene-in"><div class="gd-hero">'
         '<p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>'
         '<p class="gd-title">Kami membangun sistem Anda, <span>lantai demi lantai.</span></p>'
         '<p>Scroll untuk masuk ↓</p><p class="gd-hint">atau klik salah satu lantai gedung untuk langsung ke halamannya</p></div></div></div>')
CSS = f'<link rel="stylesheet" href="/assets/css/gedung-scenes.css?v={CSS_V}"/>'
JS = ('<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",'
      '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>'
      f'<script type="module" src="/assets/js/gedung3d.js?v={JS_V}"></script>')


def strip(s):
    s = re.sub(r'<div class="gd-scene"[^>]*><div class="gd-scene-in">.*?</div></div></div>', '', s, count=1, flags=re.S)
    s = s.replace('<main class="gd2" id="top">', '<main id="top">')
    s = s.replace('<section class="hero" data-gd-cover="">', '<section class="hero">')
    s = re.sub(r'<link rel="stylesheet" href="/assets/css/gedung-scenes\.css[^"]*"/>', '', s)
    s = re.sub(r'<script type="importmap">.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<script type="module" src="/assets/js/gedung3d\.js[^"]*"></script>', '', s)
    return s


def inject(s):
    assert '<main id="top">' in s and '<section class="hero">' in s
    s = s.replace('</head>', CSS + '</head>', 1)
    s = s.replace('<main id="top">', '<main class="gd2" id="top">' + INTRO, 1)
    s = s.replace('<section class="hero">', '<section class="hero" data-gd-cover="">', 1)
    return s.replace('</body>', JS + '</body>', 1)


home = inject(strip(s))
idx.write_text(home, encoding='utf-8')

# preview: sama dengan beranda, tapi noindex tanpa canonical/JSON-LD
p = re.sub(r'<title>.*?</title>', '<title>Preview: Gedung Altora</title>', home, count=1, flags=re.S)
p = re.sub(r'<link[^>]*rel="canonical"[^>]*/>', '', p, count=1)
p = re.sub(r'<script type="application/ld\+json">.*?</script>', '', p, flags=re.S)
p = re.sub(r'<meta[^>]*name="robots"[^>]*/>', '', p)
p = p.replace('</head>', '<meta content="noindex,nofollow" name="robots"/></head>', 1)
(root / 'preview-gedung.html').write_text(p, encoding='utf-8')
print('index.html + preview-gedung.html: pembuka gedung terpasang')

# 8 halaman lantai: scroll ke atas di puncak halaman -> kembali ke menu lantai di beranda
BACK = f'<script defer src="/assets/js/gedung-back.js?v={BACK_V}"></script>'
for name in ['careers', 'services', 'produk', 'portfolio', 'blog', 'about', 'katalog', 'support']:
    f = root / f'{name}.html'
    t = re.sub(r'<script defer(?:="")? src="/assets/js/gedung-back\.js[^"]*"></script>', '', f.read_text(encoding='utf-8'))
    f.write_text(t.replace('</body>', BACK + '</body>', 1), encoding='utf-8')
print('8 halaman lantai: gedung-back.js terpasang')
