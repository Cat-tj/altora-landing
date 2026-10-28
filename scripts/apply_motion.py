"""Gerak halus halaman utama: bento aplikasi beranda, judul hero mengecil saat discroll, hover kartu (assets/css/motion.css,
assets/js/motion.js). Skrip gerbang di <head> memasang html.m-on hanya bila perangkat tidak LITE (logika LITE yang sama
dengan beranda 3D, diambil dari build_gedung.py) dan tidak prefers-reduced-motion. Idempoten. Jalankan setelah apply_stage.py."""
import ast
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
V = '1'
# build_gedung.py menulis berkas saat diimpor, jadi LITE dibaca dari sumbernya saja
src = (root / 'scripts' / 'build_gedung.py').read_text(encoding='utf-8')
LITE = next(ast.literal_eval(n.value) for n in ast.parse(src).body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'LITE')
GATE = ('<script id="m-gate">(function(){try{if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;' + LITE +
        'if(f)lite=false;if(!lite)document.documentElement.classList.add("m-on")}catch(e){}})()</script>')
CSS = f'<link href="/assets/css/motion.css?v={V}" rel="stylesheet"/>'
JS = f'<script defer src="/assets/js/motion.js?v={V}"></script>'
PAGES = ['index.html', 'beranda.html', 'services.html', 'aplikasi.html', 'about.html', 'careers.html', 'support.html', 'contact.html']

n = 0
for name in PAGES:
    p = root / name
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<script id="m-gate">.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<link href="/assets/css/motion\.css[^"]*" rel="stylesheet"/>', '', s)
    # skrip lain menulis ulang lewat BeautifulSoup sehingga defer bisa menjadi defer=""
    s = re.sub(r'<script defer(?:="")? src="/assets/js/motion\.js[^"]*"></script>', '', s)
    s = s.replace('</head>', GATE + CSS + '</head>', 1).replace('</body>', JS + '</body>', 1)
    p.write_text(s, encoding='utf-8'); n += 1
print('gerak halus terpasang di', n, 'halaman')
