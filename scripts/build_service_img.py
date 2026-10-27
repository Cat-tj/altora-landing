"""Ilustrasi tampilan untuk layanan Website dan SEO (1600x1000 webp): assets/img/services/{website,seo}.webp. Butuh Chrome dan cwebp."""
import pathlib, subprocess, tempfile
root = pathlib.Path(__file__).resolve().parent.parent
CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CSS = '''<meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet"><style>
*{box-sizing:border-box;margin:0}body{width:1600px;height:1000px;font-family:"Plus Jakarta Sans",system-ui,sans-serif;color:#10224F;background:linear-gradient(115deg,#E9E1FF,#F8F5FF 50%,#E4DAFF);display:grid;place-items:center;overflow:hidden}
.win{width:1360px;height:820px;background:#fff;border-radius:26px;box-shadow:0 40px 90px -40px rgba(43,30,110,.5);overflow:hidden;border:1px solid #E4DEFA}
.bar{height:56px;background:#F6F3FF;display:flex;align-items:center;gap:10px;padding:0 24px;border-bottom:1px solid #E9E5F6}.bar i{width:14px;height:14px;border-radius:50%;background:#D9D0F5}
.url{margin-left:24px;height:30px;width:420px;border-radius:15px;background:#fff;border:1px solid #E4DEFA;padding:0 16px;font-size:15px;line-height:30px;color:#5A6785;font-weight:600}
.p{padding:0 70px}.nav{display:flex;align-items:center;justify-content:space-between;height:90px}.logo{font-weight:800;font-size:26px;color:#5B3FC4}
.nav span{font-weight:600;color:#5A6785;margin-left:34px;font-size:18px}.btn{display:inline-block;background:#7C5CE8;color:#fff;font-weight:700;border-radius:999px;padding:16px 30px;font-size:19px}
.card{border:1px solid #E9E5F6;border-radius:20px;padding:28px;background:#FBF9FE}.card b{display:block;font-size:22px;margin:16px 0 8px}.card p{color:#5A6785;font-size:16px;line-height:1.5}
.ic{width:52px;height:52px;border-radius:15px;background:#F3F0FD}.mut{color:#5A6785}
</style>'''
WEB = CSS + '''<div class="win"><div class="bar"><i></i><i></i><i></i><div class="url">namaperusahaan.co.id (contoh)</div></div><div class="p">
<div class="nav"><div class="logo">Nama Perusahaan</div><div><span>Layanan</span><span>Tentang</span><span>Artikel</span><span>Kontak</span></div></div>
<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:50px;align-items:center;margin-top:30px"><div>
<div style="font-weight:700;color:#5B3FC4;font-size:20px;margin-bottom:18px">● Solusi untuk bisnis Anda</div>
<div style="font-size:66px;line-height:1.05;font-weight:800;letter-spacing:-.03em">Website yang menjelaskan, ditemukan, dan menghasilkan kontak.</div>
<p class="mut" style="font-size:22px;line-height:1.5;margin:26px 0 34px">Cepat dibuka di HP, rapi dibaca, dan mudah dikelola tim Anda.</p><span class="btn">Hubungi kami</span></div>
<div style="height:380px;border-radius:26px;background:linear-gradient(135deg,#BBA2FF,#7C5CE8);position:relative"><div style="position:absolute;left:30px;bottom:30px;right:30px;background:#fff;border-radius:18px;padding:22px"><div style="height:14px;width:60%;background:#E4DEFA;border-radius:7px"></div><div style="height:14px;width:85%;background:#F0ECFB;border-radius:7px;margin-top:12px"></div><div style="height:14px;width:45%;background:#F0ECFB;border-radius:7px;margin-top:12px"></div></div></div></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:50px"><div class="card"><div class="ic"></div><b>Company profile</b><p>Profil usaha yang jelas.</p></div><div class="card"><div class="ic"></div><b>Landing page</b><p>Halaman untuk satu tujuan.</p></div><div class="card"><div class="ic"></div><b>Mudah dikelola</b><p>Konten bisa diisi sendiri.</p></div></div></div></div>'''
SEO = CSS + '''<div class="win"><div class="bar"><i></i><i></i><i></i><div class="url">Contoh laporan SEO (data ilustrasi)</div></div><div class="p" style="padding-top:44px">
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px"><div class="card"><div class="mut" style="font-weight:700">Kata kunci halaman 1</div><div style="font-size:60px;font-weight:800;margin-top:8px;color:#5B3FC4">24</div></div><div class="card"><div class="mut" style="font-weight:700">Klik dari Google</div><div style="font-size:60px;font-weight:800;margin-top:8px;color:#5B3FC4">+38%</div></div><div class="card"><div class="mut" style="font-weight:700">Skor teknis</div><div style="font-size:60px;font-weight:800;margin-top:8px;color:#5B3FC4">96</div></div></div>
<div style="display:grid;grid-template-columns:1.3fr 1fr;gap:24px;margin-top:24px"><div class="card" style="height:400px"><b style="margin:0 0 10px">Trafik organik</b>
<svg viewBox="0 0 600 300" width="100%" height="320"><g stroke="#E9E5F6" stroke-width="2"><path d="M0 60H600M0 140H600M0 220H600"/></g><path d="M0 250C80 240 120 220 180 200S280 170 340 130 460 90 600 30" fill="none" stroke="#7C5CE8" stroke-width="7" stroke-linecap="round"/><path d="M0 250C80 240 120 220 180 200S280 170 340 130 460 90 600 30V300H0Z" fill="#7C5CE8" opacity=".12"/></svg></div>
<div class="card" style="height:400px"><b style="margin:0 0 14px">Posisi kata kunci</b>
<div style="display:grid;gap:14px;font-size:19px;font-weight:600"><div style="display:flex;justify-content:space-between;border-bottom:1px solid #E9E5F6;padding-bottom:12px"><span>jasa pembuatan website</span><span style="color:#12A374">#3</span></div><div style="display:flex;justify-content:space-between;border-bottom:1px solid #E9E5F6;padding-bottom:12px"><span>software house</span><span style="color:#12A374">#5</span></div><div style="display:flex;justify-content:space-between;border-bottom:1px solid #E9E5F6;padding-bottom:12px"><span>aplikasi custom</span><span style="color:#12A374">#4</span></div><div style="display:flex;justify-content:space-between;border-bottom:1px solid #E9E5F6;padding-bottom:12px"><span>jasa seo lokal</span><span style="color:#12A374">#7</span></div><div style="display:flex;justify-content:space-between"><span>website company profile</span><span style="color:#12A374">#6</span></div></div></div></div></div></div>'''
for name, h in (('website', WEB), ('seo', SEO)):
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d, 'c.html'); f.write_text(h, encoding='utf-8'); png = pathlib.Path(d, 'c.png')
        subprocess.run([CH, '--headless=new', '--hide-scrollbars', '--virtual-time-budget=5000', '--window-size=1600,1000', f'--screenshot={png}', f.as_uri()], check=True, capture_output=True)
        subprocess.run(['cwebp', '-quiet', '-q', '82', str(png), '-o', str(root / 'assets/img/services' / f'{name}.webp')], check=True)
    print('img', name)
