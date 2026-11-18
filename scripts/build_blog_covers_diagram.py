"""Sampul artikel (1200x630 webp) dari diagram hero artikel: judul pendek di kiri, diagram di kartu putih di kanan.
Dipakai untuk artikel yang punya diagram di assets/img/blog/<slug>/. Jalankan: python3 scripts/build_blog_covers_diagram.py
Butuh Google Chrome atau Microsoft Edge (headless) dan cwebp. Hasil: assets/img/blog/cover/<slug>.webp"""
import pathlib, subprocess, tempfile, html, shutil
root = pathlib.Path(__file__).resolve().parent.parent
BROWSERS = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
BR = next(b for b in BROWSERS if pathlib.Path(b).exists())
# slug: (kategori, judul pendek, file diagram)
COVERS = {
 'tanda-bisnis-perlu-pos': ('Operasional', 'Tanda bisnis perlu sistem POS, bukan buku kas', 'alur-buku-kas-ke-pos.svg'),
 'fleet-management-logistik-tambang': ('Operasional', 'Fleet management untuk logistik dan tambang di Kaltim', 'fleet-management-alur.svg'),
 'absensi-gps-wajah-fingerprint': ('Operasional', 'Absensi GPS, wajah, atau fingerprint untuk tim lapangan', '01-hero-overview.svg'),
 'deteksi-apd-ai-cctv': ('Keamanan & CCTV', 'Deteksi APD dengan AI CCTV di proyek konstruksi', 'hero.svg'),
 'monitoring-suhu-asap-iot': ('IoT & sensor', 'Monitoring suhu dan asap IoT untuk ruang server dan gudang', 'hero-monitoring-ruang.svg'),
 'smart-farming-sensor-tanah': ('IoT & sensor', 'Sensor kelembapan tanah untuk smart farming Kaltim', 'hero-zona-sensor.svg'),
 'barcode-vs-qr-code-kasir-gudang': ('Operasional', 'Barcode vs QR code di kasir dan gudang UMKM', 'hero-barcode-vs-qrcode.svg'),
 'checklist-keamanan-aplikasi-bisnis': ('Panduan memilih vendor', 'Checklist keamanan aplikasi bisnis sebelum go-live', 'hero-security-layers.svg'),
 'command-center-satu-layar': ('Operasional', 'Command center: satu layar untuk CCTV, armada, dan sensor', 'hero-command-center.svg'),
 'digitalisasi-layanan-kelurahan-kios-mandiri': ('Operasional', 'Digitalisasi layanan kelurahan dengan kios mandiri', 'hero.svg'),
 'smart-iot-industri-kalimantan-timur': ('IoT & sensor', 'Smart IoT industri di Kaltim: monitoring aset lapangan', 'hero-iot-industrial-architecture.svg'),
 'website-company-profile-prospek': ('Website & SEO', 'Website company profile yang menghasilkan prospek', 'hero-alur-prospek.svg'),
}
TPL = '''<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box;margin:0}body{width:1200px;height:630px;font-family:"Plus Jakarta Sans",system-ui,sans-serif;color:#10224F;
background:linear-gradient(115deg,#E9E1FF 0%,#F8F5FF 45%,#E4DAFF 100%);display:flex;align-items:center;gap:44px;padding:0 64px;position:relative;overflow:hidden}
.ring{position:absolute;right:-180px;top:-200px;width:560px;height:560px;border-radius:50%;background:rgba(124,92,232,.12)}
.t{position:relative;flex:none;width:430px}.e{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:24px;color:#5B3FC4;margin-bottom:20px}
.e:before{content:"";width:13px;height:13px;border-radius:50%;background:#7C5CE8}
h1{font-size:46px;line-height:1.12;letter-spacing:-.03em;font-weight:800}.b{margin-top:26px;font-weight:700;font-size:22px;color:#5A6785}
.card{position:relative;flex:1;background:#fff;border-radius:24px;padding:14px;box-shadow:0 30px 60px -34px rgba(43,30,110,.45);border:1px solid #E9E5F6}
.card img{display:block;width:100%;height:auto;max-height:420px;object-fit:contain;border-radius:14px}</style>
<div class="ring"></div><div class="t"><div class="e">%CAT%</div><h1>%TITLE%</h1><div class="b">Altora Indonesia</div></div>
<div class="card"><img src="%IMG%"></div>'''
for slug, (cat, title, svg) in COVERS.items():
    img = (root / 'assets/img/blog' / slug / svg).resolve()
    h = TPL.replace('%CAT%', html.escape(cat)).replace('%TITLE%', html.escape(title)).replace('%IMG%', img.as_uri())
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d, 'c.html'); f.write_text(h, encoding='utf-8'); png = pathlib.Path(d, 'c.png')
        for _ in range(3):  # headless kadang macet; ulangi dengan batas waktu
            try:
                subprocess.run([BR, '--headless=new', '--allow-file-access-from-files', '--hide-scrollbars', '--virtual-time-budget=6000', '--window-size=1200,630', f'--screenshot={png}', f.as_uri()], check=True, capture_output=True, timeout=45)
                break
            except subprocess.TimeoutExpired:
                continue
        subprocess.run(['cwebp', '-quiet', '-q', '82', str(png), '-o', str(root / 'assets/img/blog/cover' / f'{slug}.webp')], check=True)
    print('cover', slug)
