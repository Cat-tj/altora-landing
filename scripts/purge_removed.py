"""Bersihkan halaman tulisan-tangan dari rujukan ke halaman yang sudah dihapus (portofolio, /produk, layanan AI/fleet/IoT/Private AI).
Membuang: seksi yang memuat tautan ke portofolio, kartu/tautan ke halaman terhapus, lalu <li> kosong. Aman dijalankan berulang.
Jalankan: python3 scripts/purge_removed.py halaman1.html halaman2.html ..."""
import re, sys, pathlib
BAD = r'(?:/portfolio(?:/[a-z0-9-]*)?|/produk(?:/[a-z0-9-]*)?(?:#[a-z]*)?|/services/(?:ai-cctv|fleet-management-service|iot-command-center|private-ai-gis)|/absensi-face-recognition-[a-z-]+)'
def purge(h):
    # 1) seksi yang berisi tautan portofolio -> dibuang seluruhnya
    h = re.sub(r'<section\b(?:(?!<section\b).)*?href="/portfolio[^"]*".*?</section>', '', h, flags=re.S)
    # 2) tautan/kartu ke halaman terhapus
    h = re.sub(r'<a\b[^>]*href="' + BAD + r'"[^>]*>.*?</a>', '', h, flags=re.S)
    # 3) pembungkus kosong
    for _ in range(3):
        h = re.sub(r'<li>\s*</li>', '', h)
        h = re.sub(r'<(ul|ol)[^>]*>\s*</\1>', '', h)
    return h
if __name__ == '__main__' and '--images' not in sys.argv:
    for f in sys.argv[1:]:
        p = pathlib.Path(f); s = p.read_text(encoding='utf-8'); n = purge(s)
        if n != s: p.write_text(n, encoding='utf-8'); print('dibersihkan:', f, len(s) - len(n), 'karakter')


# ── Gambar proyek/produk lama -> foto perangkat principal ──
H = '/assets/img/hardware/'
def _swap(m):
    p = m.group(0)
    if 'cctv' in p: return '/assets/img/vigi/c340i.webp'
    if 'network-rack' in p: return H + 'hr-close-glass.webp'
    if 'hardware-logistics' in p: return H + 'hr-wallmount-project.webp'
    if 'kiosk' in p or 'serah-terima' in p: return H + 'kios-k.webp'
    if 'aio' in p: return H + 'lenovo-ideacentre-aio-24.webp'
    if 'smartlock' in p or '/produk/pass' in p: return H + 'smartlock.webp'
    if 'agri' in p: return H + 'starlink-v5.webp'
    if '/produk/vision' in p: return '/assets/img/vigi/c340i.webp'
    if '/produk/fms' in p: return H + 'telt-fmc920.webp'
    return H + 'lenovo-thinkpad-t14.webp'
IMG = re.compile(r'/assets/img/(?:portfolio/[A-Za-z0-9_./-]*[A-Za-z0-9]|produk/[a-z0-9-]+\.webp(?:\?v=[0-9a-f]+)?|services/team-podium-system-demo\.png|extra/products/[a-z0-9-]+\.jpg)')
def swap_images(h):
    return IMG.sub(_swap, h)
if __name__ == '__main__' and '--images' in sys.argv:
    root = pathlib.Path(__file__).resolve().parent.parent; n = 0
    for p in root.rglob('*.html'):
        rel = p.relative_to(root).as_posix()
        if rel.startswith(('design/', 'partials/')): continue
        s0 = p.read_text(encoding='utf-8'); s1 = swap_images(s0)
        if s1 != s0: p.write_text(s1, encoding='utf-8'); n += 1
    print('gambar lama diganti di', n, 'halaman')
