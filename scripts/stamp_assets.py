"""Cache-busting berbasis isi file untuk dist/ (dipanggil scripts/build_pages.sh setelah rsync).

Setiap rujukan /assets/css/*.css, /assets/js/*.js, dan /assets/vendor/*.js di HTML dist/ diberi ?v=<10 hex sha1 isi file>,
menggantikan ?v= tulisan tangan. Karena URL selalu berubah saat isinya berubah, _headers boleh menyimpan file tersebut
setahun dengan 'immutable'. Import di dalam JS (swell-bg.js -> vendor) ikut distempel lebih dulu, jadi hash JS induknya
ikut berubah bila vendor berubah. Hanya menyentuh dist/, berkas sumber di repo tidak berubah.
Pakai: python3 scripts/stamp_assets.py dist"""
import hashlib, pathlib, re, sys

dist = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'dist').resolve()
REF = re.compile(r'(/assets/(?:css|js|vendor)/[\w./-]+?\.(?:css|js))(?:\?v=[\w.-]*)?(?=["\'\s)>])')
cache = {}


def ver(path):
    if path not in cache:
        f = dist / path.lstrip('/')
        cache[path] = hashlib.sha1(f.read_bytes()).hexdigest()[:10] if f.is_file() else None
    return cache[path]


def stamp(text):
    def rep(m):
        v = ver(m.group(1))
        return f'{m.group(1)}?v={v}' if v else m.group(0)
    return REF.sub(rep, text)


# 1) JS yang meng-import file lokal lain (urutan: vendor dulu, lalu js) supaya hash induk mencerminkan anaknya
for sub in ('vendor', 'js'):
    for f in sorted((dist / 'assets' / sub).glob('*.js')):
        s = f.read_text(encoding='utf-8', errors='surrogateescape')
        t = stamp(s)
        if t != s:
            f.write_text(t, encoding='utf-8', errors='surrogateescape')
            cache.pop('/' + str(f.relative_to(dist)), None)
# 2) semua halaman HTML
n = 0
for f in dist.rglob('*.html'):
    s = f.read_text(encoding='utf-8')
    t = stamp(s)
    if t != s:
        f.write_text(t, encoding='utf-8')
        n += 1
print(f'stamp_assets: {n} halaman, {sum(1 for v in cache.values() if v)} aset distempel hash isi')
