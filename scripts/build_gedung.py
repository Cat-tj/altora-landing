"""Prototipe pembuka beranda 'gedung Altora': /preview-gedung (noindex).
Halaman = beranda asli (index.html) + satu adegan 3D pembuka di depannya:
gedung utuh -> atap terbuka -> kamera masuk ke ruang meeting -> layar proyektor menampilkan hero beranda dan memenuhi
layar pengunjung -> kanvas 3D disembunyikan dan beranda asli berlanjut seperti biasa (tanpa transisi).
Animasi: assets/js/gedung3d.js; gaya adegan: assets/css/gedung-scenes.css.
Jalankan lewat scripts/build_all.sh (setelah build_produk/build_trust yang mengubah index.html)."""
import pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'index.html').read_text(encoding='utf-8')

# head: judul preview, noindex, tanpa canonical/JSON-LD beranda, plus gaya adegan
s = re.sub(r'<title>.*?</title>', '<title>Preview: Gedung Altora</title>', s, count=1, flags=re.S)
s = re.sub(r'<link[^>]*rel="canonical"[^>]*/>', '', s, count=1)
s = re.sub(r'<script type="application/ld\+json">.*?</script>', '', s, flags=re.S)
s = re.sub(r'<meta[^>]*name="robots"[^>]*/>', '', s)
s = s.replace('</head>', '<meta content="noindex,nofollow" name="robots"/><link rel="stylesheet" href="/assets/css/gedung-scenes.css?v=7"/></head>', 1)

# adegan pembuka di awal <main>, hero beranda ditandai sebagai isi layar proyektor
intro = ('<div class="gd-scene" data-to="7"><div class="gd-scene-in"><div class="gd-hero">'
         '<p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>'
         '<p class="gd-title">Kami membangun sistem Anda, <span>lantai demi lantai.</span></p>'
         '<p>Scroll untuk masuk ↓</p></div></div></div>')
assert '<main id="top">' in s and '<section class="hero">' in s
s = s.replace('<main id="top">', '<main class="gd2" id="top">' + intro, 1)
s = s.replace('<section class="hero">', '<section class="hero" data-gd-cover="">', 1)

# skrip 3D
s = s.replace('</body>', '<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",'
              '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>'
              '<script type="module" src="/assets/js/gedung3d.js?v=212"></script></body>', 1)

(root / 'preview-gedung.html').write_text(s, encoding='utf-8')
print('preview-gedung.html dibuat (beranda + pembuka gedung)')
