"""Pembuka beranda 'gedung Altora' (Three.js), dipasang di beranda (index.html) dan /preview-gedung (noindex).
Beranda tetap utuh di HTML (SEO); adegan 3D hanya lapisan pembuka di depannya:
gedung -> scroll pertama: menu lantai -> scroll kedua: atap terbuka, kamera masuk ke ruang meeting, layar proyektor
menampilkan hero beranda dan memenuhi layar -> kanvas disembunyikan, beranda asli berlanjut. Klik lantai -> halamannya.
Tanpa WebGL / prefers-reduced-motion: adegan tidak tampil sama sekali, beranda biasa.
Animasi: assets/js/gedung3d.js; gaya adegan: assets/css/gedung-scenes.css.
Idempoten: pembuka lama dilepas dulu sebelum dipasang ulang, jadi aman dijalankan berkali-kali.
Jalankan lewat scripts/build_all.sh (setelah build_produk/build_trust yang mengubah index.html)."""
import pathlib, re

JS_V, CSS_V, BACK_V = 282, 17, 8
root = pathlib.Path(__file__).resolve().parent.parent
idx = root / 'index.html'
s = idx.read_text(encoding='utf-8')

INTRO = ('<div class="gd-scene" data-to="9"><div class="gd-scene-in"><div class="gd-hero">'
         '<p class="eyebrow eyebrow-purple">Altora Indonesia · Samarinda &amp; Balikpapan</p>'
         '<p class="gd-title">Kami membangun sistem Anda, <span>lantai demi lantai.</span></p>'
         '<p>Scroll untuk masuk ↓</p><p class="gd-hint">atau klik salah satu lantai gedung untuk langsung ke halamannya</p></div></div></div>')
CSS = f'<link rel="stylesheet" href="/assets/css/gedung-scenes.css?v={CSS_V}"/>'
# Perangkat ringan langsung dapat beranda biasa (3D tidak diunduh sama sekali): hemat data / jaringan 2G-3G, RAM < 4 GB atau
# CPU < 4 inti, HP dengan RAM < 8 GB atau CPU < 8 inti (atau RAM tak terbaca, misalnya iPhone), GPU lemah. ?3d=1 memaksa 3D,
# ?3d=0 mematikannya. Bila 3D tetap tersendat saat berjalan, gedung3d.js mematikannya dan menyimpan 'gd-lite'.
LITE = ('var q=location.search,n=navigator,c=n.connection||{},m=n.deviceMemory,p=n.hardwareConcurrency||0,f=/[?&]3d=1/.test(q),lite=/[?&]3d=0/.test(q);'
        'try{if(localStorage.getItem("gd-lite")==="1")lite=true}catch(e){}'
        'if(c.saveData||/2g|3g/.test(c.effectiveType||""))lite=true;if((m&&m<4)||(p&&p<4))lite=true;'
        'if(matchMedia("(pointer:coarse)").matches&&Math.min(screen.width,screen.height)<768&&(!m||m<8||p<8))lite=true;')
GPU = ('var di=x.getExtension("WEBGL_debug_renderer_info"),gr=di?String(x.getParameter(di.UNMASKED_RENDERER_WEBGL)):"";'
       r'if(x.getParameter(x.MAX_TEXTURE_SIZE)<4096||/SwiftShader|llvmpipe|Mali-(4|T)|Adreno \(TM\) [345]\d\d|PowerVR/i.test(gr))lite=true;'
       'if(f)lite=false;if(lite){document.documentElement.classList.add("gd-lite");return}')
# tanda boot sejak awal: tampilkan latar langit + logo sampai 3D siap (beranda biasa tidak sempat berkedip); batal sendiri bila 3D tidak jalan
# HP (layar sentuh < 768px) selalu dapat beranda biasa: pembuka 3D (Three.js ±1,3 MB + render WebGL) di HP kelas atas pun
# menahan LCP/TBT berdetik-detik di Lighthouse mobile. ?3d=1 tetap bisa memaksanya untuk demo.
PHONE = 'if(matchMedia("(pointer:coarse)").matches&&Math.min(screen.width,screen.height)<768)lite=true;'
BOOT = ('<script id="gd-boot">(function(){try{if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;' + LITE + PHONE +
        'var g=document.createElement("canvas"),x=g.getContext("webgl2")||g.getContext("webgl");if(!x)return;' + GPU +
        'var l=x.getExtension("WEBGL_lose_context");if(l)l.loseContext();'
        'var d=document.documentElement,h=new Date().getHours();d.classList.add("gd-boot");if(h<5||h>=19)d.classList.add("gd-boot-night");'
        'var b=function(e){if(d.classList.contains("gd-boot"))e.preventDefault()};'  # selama loading scroll ditahan (tidak terlanjur ke konten)
        'addEventListener("wheel",b,{passive:false});addEventListener("touchmove",b,{passive:false});setTimeout(function(){d.classList.remove("gd-boot","gd-boot-night")},8000)}catch(e){}})()</script>')
JS = ('<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",'
      '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>'
      # modul 3D (dan Three.js ±1,3 MB) hanya diunduh bila boot di atas menyalakan gd-boot
      '<script id="gd-load">if(document.documentElement.classList.contains("gd-boot")){var s=document.createElement("script");'
      f's.type="module";s.src="/assets/js/gedung3d.js?v={JS_V}";document.body.appendChild(s)}}</script>')


def strip(s):
    s = re.sub(r'<div class="gd-scene"[^>]*><div class="gd-scene-in">.*?</div></div></div>', '', s, count=1, flags=re.S)
    s = s.replace('<main class="gd2" id="top">', '<main id="top">')
    s = s.replace('<section class="hero" data-gd-cover="">', '<section class="hero">')
    s = re.sub(r'<link rel="stylesheet" href="/assets/css/gedung-scenes\.css[^"]*"/>', '', s)
    s = re.sub(r'<script id="gd-boot">.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<script type="importmap">.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<script type="module" src="/assets/js/gedung3d\.js[^"]*"></script>', '', s)
    s = re.sub(r'<script id="gd-load">.*?</script>', '', s, flags=re.S)
    return s


def inject(s):
    assert '<main id="top">' in s and '<section class="hero">' in s
    s = s.replace('</head>', CSS + BOOT + '</head>', 1)
    s = s.replace('<main id="top">', '<main class="gd2" id="top">' + INTRO, 1)
    s = s.replace('<section class="hero">', '<section class="hero" data-gd-cover="">', 1)
    return s.replace('</body>', JS + '</body>', 1)


plain = strip(s)
home = inject(plain)
# /beranda: isi beranda yang sama tanpa gedung 3D, untuk tautan langsung dan perangkat ringan (canonical tetap ke /)
(root / 'beranda.html').write_text(plain, encoding='utf-8')
idx.write_text(home, encoding='utf-8')

# preview: sama dengan beranda, tapi noindex tanpa canonical/JSON-LD
p = re.sub(r'<title>.*?</title>', '<title>Preview: Gedung Altora</title>', home, count=1, flags=re.S)
p = re.sub(r'<link[^>]*rel="canonical"[^>]*/>', '', p, count=1)
p = re.sub(r'<script type="application/ld\+json">.*?</script>', '', p, flags=re.S)
p = re.sub(r'<meta[^>]*name="robots"[^>]*/>', '', p)
p = p.replace('</head>', '<meta content="noindex,nofollow" name="robots"/></head>', 1)
(root / 'preview-gedung.html').write_text(p, encoding='utf-8')
print('index.html + preview-gedung.html: pembuka gedung terpasang')

# halaman lantai: scroll ke atas di puncak halaman -> kembali ke menu lantai di beranda
BACK = f'<script defer src="/assets/js/gedung-back.js?v={BACK_V}"></script>'
for name in ['services', 'pengadaan', 'aplikasi', 'portofolio', 'blog', 'about', 'careers', 'support']:
    f = root / f'{name}.html'
    t = re.sub(r'<script defer(?:="")? src="/assets/js/gedung-back\.js[^"]*"></script>', '', f.read_text(encoding='utf-8'))
    f.write_text(t.replace('</body>', BACK + '</body>', 1), encoding='utf-8')
print('8 halaman lantai (selain Beranda): gedung-back.js terpasang')
