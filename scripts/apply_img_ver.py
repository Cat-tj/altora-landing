"""Tempelkan ?v=<hash isi> ke setiap URL /assets/img/produk/<id>.webp di semua halaman HTML,
agar browser dan Cloudflare memuat gambar baru setiap kali ilustrasinya diganti (nama file tetap sama).
Dijalankan paling akhir oleh scripts/build_all.sh; aman dijalankan berulang."""
import hashlib, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
IMG = root / 'assets/img/produk'
SKIP = {'.git', '.claude', 'leads', 'partials', 'ops', 'content', 'outreach', 'scripts', 'design', 'node_modules'}
ver = {p.stem: hashlib.md5(p.read_bytes()).hexdigest()[:8] for p in IMG.glob('*.webp')}
pat = re.compile(r'(/assets/img/produk/([a-z0-9-]+)\.webp)(\?v=[0-9a-f]+)?')


def tag(m):
    v = ver.get(m.group(2))
    return f'{m.group(1)}?v={v}' if v else m.group(0)


changed = 0
for page in root.rglob('*.html'):
    if SKIP & set(page.relative_to(root).parts):
        continue
    s = page.read_text(encoding='utf-8')
    t = pat.sub(tag, s)
    if t != s:
        page.write_text(t, encoding='utf-8')
        changed += 1
print('versi gambar produk diperbarui di', changed, 'halaman')
