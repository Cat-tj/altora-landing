"""Sampul artikel (1200x630 webp) buatan sendiri: panel ungu brand, kategori, judul pendek, dan ikon sesuai topik.
Jalankan: python3 scripts/build_blog_covers.py (butuh Google Chrome dan cwebp). Hasil: assets/img/blog/cover/<slug>.webp"""
import pathlib, subprocess, tempfile, html
root = pathlib.Path(__file__).resolve().parent.parent
CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
ICON = {
 'fork': '<path d="M60 150V90M60 90C60 60 100 60 100 30M60 90C60 60 20 60 20 30" /><circle cx="100" cy="24" r="10"/><circle cx="20" cy="24" r="10"/><circle cx="60" cy="156" r="10"/>',
 'check': '<rect x="22" y="20" width="96" height="124" rx="14"/><path d="M44 62l12 12 22-24M44 106l12 12 22-24"/><path d="M92 68h14M92 112h14"/>',
 'scope': '<rect x="16" y="96" width="38" height="50" rx="8"/><rect x="62" y="64" width="38" height="82" rx="8"/><rect x="108" y="28" width="38" height="118" rx="8"/>',
 'doc': '<rect x="30" y="14" width="100" height="138" rx="14"/><path d="M52 50h56M52 76h56M52 102h34"/><path d="M98 118l10 10 20-24"/>',
 'find': '<circle cx="68" cy="68" r="40"/><path d="M98 98l36 36"/><path d="M52 68l12 12 22-26"/>',
}
COVERS = {
 'altora-store-aplikasi-toko-suku-cadang': ('Cerita Altora', 'Altora Store: aplikasi toko suku cadang dan industri', 'doc'),
 'sistem-po-toko': ('Perencanaan', 'Sistem PO toko: dari penawaran sampai lunas', 'doc'),
 'kapan-software-custom': ('Panduan memilih vendor', 'Kapan perlu software custom, kapan cukup aplikasi siap pakai', 'fork'),
 'cara-memilih-software-house-samarinda-balikpapan': ('Panduan memilih vendor', '8 pertanyaan sebelum memilih software house', 'check'),
 'merencanakan-pembuatan-aplikasi': ('Perencanaan', '7 hal yang menentukan cakupan proyek aplikasi', 'scope'),
 'membimbing-smpn-5-balikpapan-innovakids-2026': ('Cerita Altora', 'Membimbing SMPN 5 Balikpapan ke Juara 2 Innovakids 2026', 'find'),
}
TPL = '''<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box;margin:0}body{width:1200px;height:630px;font-family:"Plus Jakarta Sans",system-ui,sans-serif;color:#10224F;
background:linear-gradient(115deg,#E9E1FF 0%,#F8F5FF 45%,#E4DAFF 100%);display:flex;align-items:center;gap:56px;padding:0 84px;position:relative;overflow:hidden}
.ring{position:absolute;right:-160px;top:-160px;width:560px;height:560px;border-radius:50%;background:rgba(124,92,232,.12)}
.ring2{position:absolute;left:-120px;bottom:-200px;width:420px;height:420px;border-radius:50%;background:rgba(124,92,232,.08)}
.tile{flex:none;width:260px;height:260px;border-radius:56px;background:#7C5CE8;display:grid;place-items:center;box-shadow:0 30px 60px -30px rgba(91,63,196,.7);position:relative}
svg{width:170px;height:170px;fill:none;stroke:#fff;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.t{position:relative}.e{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:26px;color:#5B3FC4;margin-bottom:22px}
.e:before{content:"";width:14px;height:14px;border-radius:50%;background:#7C5CE8}
h1{font-size:60px;line-height:1.1;letter-spacing:-.03em;font-weight:800}.b{margin-top:30px;font-weight:700;font-size:24px;color:#5A6785}</style>
<div class="ring"></div><div class="ring2"></div><div class="tile"><svg viewBox="0 0 160 170">%ICON%</svg></div>
<div class="t"><div class="e">%CAT%</div><h1>%TITLE%</h1><div class="b">Altora Indonesia</div></div>'''
for slug, (cat, title, ic) in COVERS.items():
    h = TPL.replace('%ICON%', ICON[ic]).replace('%CAT%', html.escape(cat)).replace('%TITLE%', html.escape(title))
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d, 'c.html'); f.write_text(h, encoding='utf-8'); png = pathlib.Path(d, 'c.png')
        subprocess.run([CH, '--headless=new', '--hide-scrollbars', '--virtual-time-budget=5000', '--window-size=1200,630', f'--screenshot={png}', f.as_uri()], check=True, capture_output=True)
        subprocess.run(['cwebp', '-quiet', '-q', '82', str(png), '-o', str(root / 'assets/img/blog/cover' / f'{slug}.webp')], check=True)
    print('cover', slug)
