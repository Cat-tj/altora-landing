"""Ilustrasi produk 800x1000 (assets/img/produk/<id>.webp) dalam gaya yang sama dengan Altora Projek/Office:
logo produk, satu jendela aplikasi berisi contoh tampilan, dan satu catatan singkat. Semua data di dalamnya contoh.
Aturan konten: tanpa harga/nominal uang, tanpa nama klien, tanpa statistik klaim.
Butuh Google Chrome dan cwebp.  Jalankan:  python3 scripts/build_produk_img.py [id ...]"""
import pathlib, subprocess, sys, tempfile

root = pathlib.Path(__file__).resolve().parent.parent
OUT = root / 'assets/img/produk'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
TONE = {'purple': '#7C5CE8', 'blue': '#2F6FED', 'green': '#1F9D6B', 'pink': '#D9468F', 'orange': '#E8812F', 'cyan': '#0EA5B7'}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:800px;height:1000px;overflow:hidden;}
body{display:flex;flex-direction:column;padding:70px 60px 0;font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:#10224F}
body{background:radial-gradient(520px 420px at 78% 12%,#E4DAFF 0,transparent 70%),radial-gradient(520px 420px at 0% 100%,#FBE3F1 0,transparent 70%),linear-gradient(160deg,#F7F3FF,#FBF9FE 60%,#F6F1FE)}
.brand{display:flex;margin:0 20px;align-items:center;gap:12px;font-weight:800;font-size:23px;letter-spacing:-.02em}
.brand i{width:34px;height:34px;border-radius:9px;background:var(--a);color:#fff;font-style:normal;display:grid;place-items:center;font-size:17px}
.stage{flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px;padding-bottom:30px}
.win{border-radius:22px;background:#fff;border:1px solid #E9E5F6;box-shadow:0 34px 70px -34px rgba(43,30,110,.35);overflow:hidden}
.bar{height:62px;display:flex;align-items:center;gap:8px;padding:0 20px;border-bottom:1px solid #EEEAF8;background:#FBFAFE}
.bar>span{width:11px;height:11px;border-radius:50%;background:#F0626E}.bar>span:nth-child(2){background:#F5BE4F}.bar>span:nth-child(3){background:#5CC97B}
.bar b{margin-left:18px;font-size:16px;font-weight:800}
.bar em{margin-left:auto;font-style:normal;font-size:12.5px;font-weight:700;color:#1F7A4D;background:#E7F6EE;padding:7px 12px;border-radius:999px}
.tabs{display:flex;gap:6px;padding:12px 18px;border-bottom:1px solid #F0ECF8;font-size:12.5px;font-weight:600;color:#5A6785}
.tabs span{padding:7px 12px;border-radius:999px}.tabs span.on{background:#F1EDFD;color:#5B3FC4;font-weight:700}
.body{padding:16px 18px 20px}
.note{align-self:flex-start;margin-left:20px;background:#fff;border:1px solid #E9E5F6;border-radius:18px;padding:16px 22px 16px 16px;display:flex;gap:14px;align-items:center;box-shadow:0 14px 34px -24px rgba(43,30,110,.25);max-width:520px}
.note i{width:40px;height:40px;border-radius:11px;background:#F3F0FD;display:grid;place-items:center;font-style:normal;font-size:20px}
.note b{display:block;font-size:15.5px;font-weight:800}.note small{font-size:13px;color:#5A6785}
/* blok umum */
.row{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid #EEEAF8;border-radius:12px;margin-bottom:8px;font-size:13px}
.row b{font-weight:700}.row small{color:#7A8099;font-size:11.5px}.row .r{margin-left:auto}
.av{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:10.5px;font-weight:800;flex:none}
.chip{font-size:11px;font-weight:700;padding:4px 9px;border-radius:999px;white-space:nowrap}
.ok{background:#E7F6EE;color:#1F7A4D}.warn{background:#FFF3D6;color:#8A5A00}.bad{background:#FDE8EA;color:#B4232F}.info{background:#EAF1FE;color:#2452B8}.mut{background:#F1F2F6;color:#5A6785}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.tile{border:1px solid #EEEAF8;border-radius:14px;padding:12px}.tile small{display:block;color:#7A8099;font-size:11.5px;font-weight:600}.tile b{display:block;font-size:22px;font-weight:800;margin-top:4px;font-variant-numeric:tabular-nums}
.cam{position:relative;border-radius:12px;overflow:hidden;background:linear-gradient(160deg,#2B3550,#1A2238);height:150px}
.cam .lbl{position:absolute;left:8px;top:8px;color:#fff;font-size:10.5px;font-weight:700;background:rgba(0,0,0,.35);padding:3px 7px;border-radius:6px}
.box{position:absolute;border:2px solid #5CC97B;border-radius:4px}.box.badb{border-color:#F0626E}
.box span{position:absolute;left:-2px;top:-20px;font-size:10px;font-weight:800;color:#fff;background:#3FAE65;padding:2px 6px;border-radius:4px;white-space:nowrap}.box.badb span{background:#E5484D}
.person{position:absolute;bottom:0;width:38px;height:92px}
.tile .row b{display:inline;font-size:13px;margin:0}
.h{font-size:12px;font-weight:800;color:#5A6785;margin:4px 2px 8px;letter-spacing:.02em}
"""

PERSON = '<svg class="person" style="left:{x}px" viewBox="0 0 38 92"><circle cx="19" cy="14" r="10" fill="#C9D2E6"/><path d="M4 92V44c0-9 6-16 15-16s15 7 15 16v48z" fill="#8E9BBA"/></svg>'


def person(x):
    return PERSON.format(x=x)


APPS = {
    'teams': dict(tone='purple', letter='T', name='Altora Teams', title='Kehadiran hari ini', tabs=['Kehadiran', 'Cuti & izin', 'Lembur', 'Payroll'],
        emoji='👥', n1='Absensi, cuti, dan gaji di satu aplikasi', n2='Rekap otomatis untuk tim HR', body='''
<div class="grid3" style="margin-bottom:12px"><div class="tile"><small>Hadir</small><b>42</b></div><div class="tile"><small>Cuti / izin</small><b>3</b></div><div class="tile"><small>Belum absen</small><b>5</b></div></div>
<div class="row"><span class="av" style="background:#7C5CE8">AR</span><div><b>Andi R.</b><br><small>Kantor pusat · GPS &amp; selfie</small></div><span class="r chip ok">Hadir 07.52</span></div>
<div class="row"><span class="av" style="background:#2F6FED">SL</span><div><b>Sari L.</b><br><small>Site lapangan · GPS</small></div><span class="r chip warn">Terlambat 08.14</span></div>
<div class="row"><span class="av" style="background:#D9468F">DM</span><div><b>Dewi M.</b><br><small>Pengajuan cuti 2 hari</small></div><span class="r chip info">Menunggu persetujuan</span></div>
<div class="row"><span class="av" style="background:#1F9D6B">RS</span><div><b>Rudi S.</b><br><small>Shift malam</small></div><span class="r chip mut">Mulai 20.00</span></div>'''),
    'attendance': dict(tone='pink', letter='A', name='Altora Smart Attendance', title='Pintu masuk · Kamera 01', tabs=['Live', 'Log kehadiran', 'Karyawan', 'Kamera'],
        emoji='🙂', n1='Absen otomatis dari wajah di CCTV', n2='Tanpa antre di mesin absensi', body=f'''
<div class="cam" style="height:230px;margin-bottom:12px"><span class="lbl">● LIVE · Lobi utama</span>{person(120)}{person(300)}
<div class="box" style="left:108px;top:118px;width:62px;height:66px"><span>Andi R. · 98%</span></div><div class="box" style="left:288px;top:118px;width:62px;height:66px"><span>Sari L. · 96%</span></div></div>
<div class="row"><span class="av" style="background:#7C5CE8">AR</span><div><b>Andi R.</b><br><small>Kamera 01 · Lobi utama</small></div><span class="r chip ok">Masuk 07.52</span></div>
<div class="row"><span class="av" style="background:#2F6FED">SL</span><div><b>Sari L.</b><br><small>Kamera 01 · Lobi utama</small></div><span class="r chip ok">Masuk 07.55</span></div>'''),
    'vision': dict(tone='green', letter='V', name='Altora Vision', title='Area produksi · 4 kamera', tabs=['Live', 'Alert', 'Rekap APD', 'Zona'],
        emoji='🦺', n1='Alert APD dan zona terlarang', n2='Langsung ke dashboard dan HP pengawas', body=f'''
<div class="grid2" style="margin-bottom:12px">
<div class="cam"><span class="lbl">CAM 02 · Gudang</span>{person(70)}{person(190)}<div class="box" style="left:62px;top:52px;width:54px;height:98px"><span>Helm ✓ Rompi ✓</span></div><div class="box badb" style="left:182px;top:52px;width:54px;height:98px"><span>Tanpa helm</span></div></div>
<div class="cam"><span class="lbl">CAM 03 · Zona alat berat</span>{person(130)}<div class="box badb" style="left:122px;top:52px;width:54px;height:98px"><span>Masuk zona terlarang</span></div></div></div>
<div class="row"><span class="chip bad">Alert</span><div><b>Pekerja tanpa helm</b><br><small>CAM 02 · Gudang · 09.41</small></div><span class="r chip info">Terkirim ke HP</span></div>
<div class="row"><span class="chip bad">Alert</span><div><b>Orang masuk zona alat berat</b><br><small>CAM 03 · 09.38</small></div><span class="r chip ok">Ditangani</span></div>'''),
    'pass': dict(tone='blue', letter='P', name='Altora Pass', title='Akses pintu & gerbang', tabs=['Pintu', 'Riwayat akses', 'Hak akses', 'Tamu'],
        emoji='🔑', n1='Siapa boleh masuk, ke mana, kapan', n2='Kartu, QR, atau wajah, semua tercatat', body='''
<div class="grid3" style="margin-bottom:12px"><div class="tile"><small>Lobi utama</small><b style="font-size:16px">Terbuka</b><span class="chip ok" style="display:inline-block;margin-top:6px">Jam kerja</span></div>
<div class="tile"><small>Ruang server</small><b style="font-size:16px">Terkunci</b><span class="chip mut" style="display:inline-block;margin-top:6px">Khusus IT</span></div>
<div class="tile"><small>Gerbang parkir</small><b style="font-size:16px">Aktif</b><span class="chip info" style="display:inline-block;margin-top:6px">Barrier gate</span></div></div>
<div class="row"><span class="av" style="background:#2F6FED">AR</span><div><b>Andi R. · Lobi utama</b><br><small>Kartu RFID · 07.51</small></div><span class="r chip ok">Diizinkan</span></div>
<div class="row"><span class="av" style="background:#E8812F">TM</span><div><b>Tamu · Lobi utama</b><br><small>QR undangan · 09.10</small></div><span class="r chip ok">Diizinkan</span></div>
<div class="row"><span class="av" style="background:#8E9BBA">?</span><div><b>Kartu tidak dikenal · Ruang server</b><br><small>09.32</small></div><span class="r chip bad">Ditolak</span></div>'''),
    'fms': dict(tone='orange', letter='F', name='Altora FMS', title='Armada hari ini', tabs=['Peta', 'Kendaraan', 'Perjalanan', 'Geofence'],
        emoji='🚚', n1='Posisi armada dan rute dalam satu peta', n2='Alert saat keluar jalur atau berhenti lama', body='''
<div style="position:relative;height:230px;border-radius:12px;overflow:hidden;background:#EEF2F7;margin-bottom:12px">
<svg width="100%" height="100%" viewBox="0 0 640 230" preserveAspectRatio="none"><g stroke="#DCE3EE" stroke-width="10" fill="none"><path d="M0 60H640M0 170H640M120 0V230M330 0V230M520 0V230"/></g>
<path d="M-10 200 C80 190 120 120 200 110 S320 60 420 90 S560 40 650 30" fill="none" stroke="#E8812F" stroke-width="4" stroke-dasharray="2 0"/>
<rect x="430" y="120" width="150" height="80" rx="10" fill="rgba(124,92,232,.10)" stroke="#7C5CE8" stroke-dasharray="6 5"/><text x="442" y="140" font-size="12" font-weight="700" fill="#5B3FC4">Area tambang</text>
<g><circle cx="200" cy="110" r="11" fill="#E8812F"/><circle cx="420" cy="90" r="11" fill="#2F6FED"/><circle cx="505" cy="168" r="11" fill="#1F9D6B"/></g></svg></div>
<div class="row"><span class="chip warn">DT-07</span><div><b>Dump truck · Bergerak</b><br><small>Menuju area tambang</small></div><span class="r chip info">32 km/j</span></div>
<div class="row"><span class="chip info">LV-03</span><div><b>Light vehicle · Bergerak</b><br><small>Jalan hauling</small></div><span class="r chip info">45 km/j</span></div>
<div class="row"><span class="chip ok">EX-02</span><div><b>Excavator · Di area kerja</b><br><small>Mesin menyala</small></div><span class="r chip ok">Dalam geofence</span></div>'''),
    'sense': dict(tone='cyan', letter='S', name='Altora Sense', title='Sensor gedung & lapangan', tabs=['Ringkasan', 'Sensor', 'Alert', 'Perangkat'],
        emoji='📡', n1='Asap, api, suhu, dan kelembapan terpantau', n2='Tim menerima alert saat ada yang tidak normal', body='''
<div class="grid2" style="margin-bottom:12px">
<div class="tile"><small>Suhu · Ruang server</small><b>24.6°C</b><svg width="100%" height="34" viewBox="0 0 200 34"><path d="M0 22 L25 20 L50 23 L75 18 L100 21 L125 17 L150 19 L175 16 L200 18" fill="none" stroke="#0EA5B7" stroke-width="2.5"/></svg></div>
<div class="tile"><small>Kelembapan · Gudang</small><b>61%</b><svg width="100%" height="34" viewBox="0 0 200 34"><path d="M0 14 L25 16 L50 13 L75 17 L100 15 L125 18 L150 14 L175 16 L200 15" fill="none" stroke="#2F6FED" stroke-width="2.5"/></svg></div>
<div class="tile"><small>Detektor asap · Lantai 2</small><b style="font-size:17px">Normal</b><span class="chip ok" style="display:inline-block;margin-top:6px">Online</span></div>
<div class="tile" style="border-color:#F7C6CB;background:#FFF7F8"><small>Suhu · Panel listrik</small><b style="color:#B4232F">58°C</b><span class="chip bad" style="display:inline-block;margin-top:6px">Di atas batas</span></div></div>
<div class="row"><span class="chip bad">Alert</span><div><b>Suhu panel listrik tinggi</b><br><small>Sensor PL-04 · 10.12</small></div><span class="r chip info">Teknisi diberi tahu</span></div>'''),
    'farming': dict(tone='green', letter='F', name='Altora Smart Farming', title='Kebun blok utara', tabs=['Peta petak', 'Sensor', 'Field check', 'Laporan'],
        emoji='🌱', n1='Kondisi tiap petak terlihat dari HP', n2='Kelembapan tanah, suhu, dan catatan lapangan', body='''
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:10px">
''' + ''.join(f'<div style="height:52px;border-radius:8px;background:{c};display:grid;place-items:center;font-size:11px;font-weight:700;color:#10224F">{n}</div>'
             for n, c in zip([f'P{i}' for i in range(1, 19)], ['#BFE6CF', '#BFE6CF', '#9ED9B6', '#FFE3A3', '#BFE6CF', '#9ED9B6', '#9ED9B6', '#FFE3A3', '#F7C6CB', '#BFE6CF', '#9ED9B6', '#BFE6CF',
                                                              '#BFE6CF', '#9ED9B6', '#BFE6CF', '#FFE3A3', '#9ED9B6', '#BFE6CF'])) + '''</div>
<div style="display:flex;gap:14px;font-size:11.5px;color:#5A6785;margin:0 2px 12px"><span>■ <b style="color:#3FAE65">Cukup air</b></span><span>■ <b style="color:#B98500">Mulai kering</b></span><span>■ <b style="color:#B4232F">Perlu disiram</b></span></div>
<div class="row"><span class="chip bad">P9</span><div><b>Kelembapan tanah rendah</b><br><small>Sensor tanah · 31%</small></div><span class="r chip warn">Jadwalkan penyiraman</span></div>
<div class="row"><span class="chip ok">P3</span><div><b>Field check selesai</b><br><small>Foto &amp; catatan petugas</small></div><span class="r chip ok">Tanaman sehat</span></div>'''),
    'command': dict(tone='purple', letter='C', name='Altora Command', title='Ruang kendali operasional', tabs=['Video wall', 'Peta', 'Insiden', 'Perangkat'],
        emoji='🖥️', n1='CCTV, armada, dan sensor di satu layar', n2='Insiden ditugaskan dan dipantau sampai selesai', body=f'''
<div class="grid3" style="margin-bottom:10px">
<div class="cam" style="height:96px"><span class="lbl">CAM 01</span>{person(60)}</div><div class="cam" style="height:96px"><span class="lbl">CAM 04</span>{person(110)}</div><div class="cam" style="height:96px"><span class="lbl">CAM 07</span></div></div>
<div class="grid2" style="margin-bottom:12px"><div style="height:110px;border-radius:12px;background:#EEF2F7;position:relative;overflow:hidden">
<svg width="100%" height="100%" viewBox="0 0 300 110" preserveAspectRatio="none"><path d="M0 40H300M0 85H300M90 0V110M210 0V110" stroke="#DCE3EE" stroke-width="7"/><circle cx="90" cy="40" r="7" fill="#E8812F"/><circle cx="210" cy="85" r="7" fill="#2F6FED"/><circle cx="150" cy="62" r="7" fill="#E5484D"/></svg></div>
<div class="grid2" style="gap:8px"><div class="tile" style="padding:10px"><small>Kamera online</small><b style="font-size:18px">24</b></div><div class="tile" style="padding:10px"><small>Armada aktif</small><b style="font-size:18px">11</b></div>
<div class="tile" style="padding:10px"><small>Sensor</small><b style="font-size:18px">36</b></div><div class="tile" style="padding:10px;border-color:#F7C6CB"><small>Insiden</small><b style="font-size:18px;color:#B4232F">2</b></div></div></div>
<div class="row"><span class="chip bad">Insiden</span><div><b>Suhu panel listrik tinggi</b><br><small>Ditugaskan ke tim teknisi</small></div><span class="r chip warn">Dalam penanganan</span></div>'''),
    'private-ai': dict(tone='blue', letter='AI', name='Altora Private AI & GIS', title='Asisten AI internal', tabs=['Tanya AI', 'Dokumen', 'Peta GIS', 'Akses'],
        emoji='🔒', n1='AI yang membaca data internal Anda', n2='Berjalan di server sendiri, data tidak keluar', body='''
<div style="display:flex;justify-content:flex-end;margin-bottom:10px"><div style="max-width:78%;background:#7C5CE8;color:#fff;border-radius:16px 16px 4px 16px;padding:11px 14px;font-size:13px;font-weight:600">Ringkas laporan inspeksi jembatan bulan ini dan tandai yang perlu perbaikan.</div></div>
<div style="max-width:88%;background:#F6F4FC;border:1px solid #EEEAF8;border-radius:16px 16px 16px 4px;padding:12px 14px;font-size:13px;line-height:1.55;margin-bottom:12px">
<b style="display:block;margin-bottom:4px">Ringkasan dari 3 laporan</b>• 2 jembatan dalam kondisi baik.<br>• 1 jembatan perlu perbaikan sambungan, terlihat di peta.<br>
<div style="display:flex;gap:6px;margin-top:8px;flex-wrap:wrap"><span class="chip info">Laporan inspeksi.pdf</span><span class="chip info">Data aset.xlsx</span></div></div>
<div style="height:120px;border-radius:12px;background:#EEF2F7;position:relative;overflow:hidden"><svg width="100%" height="100%" viewBox="0 0 640 120" preserveAspectRatio="none">
<path d="M0 70 C120 40 220 100 330 60 S540 30 640 55" stroke="#A9C4F5" stroke-width="16" fill="none"/><path d="M0 30H640M160 0V120M440 0V120" stroke="#DCE3EE" stroke-width="6"/>
<circle cx="160" cy="58" r="8" fill="#1F9D6B"/><circle cx="330" cy="60" r="8" fill="#1F9D6B"/><circle cx="440" cy="44" r="9" fill="#E5484D"/></svg>
<span class="chip mut" style="position:absolute;left:10px;top:10px">Peta GIS · aset jembatan</span></div>'''),
    'pos': dict(tone='orange', letter='P', name='Altora POS', title='Kasir · Outlet utama', tabs=['Kasir', 'Produk', 'Stok', 'Laporan'],
        emoji='🧾', n1='Kasir cepat untuk retail dan F&B', n2='Stok dan laporan cabang terhubung', body='''
<div style="display:grid;grid-template-columns:1.4fr 1fr;gap:12px">
<div class="grid2" style="gap:8px">''' + ''.join(f'<div class="tile" style="padding:10px"><div style="height:44px;border-radius:9px;background:{c};margin-bottom:8px"></div><b style="font-size:13px;margin:0">{n}</b><small>{k}</small></div>'
                                       for n, k, c in [('Kopi susu', 'Minuman', '#F2E3D3'), ('Teh lemon', 'Minuman', '#FBEFC4'), ('Roti bakar', 'Makanan', '#F7DCC7'),
                                                       ('Nasi goreng', 'Makanan', '#F6D7C9'), ('Air mineral', 'Minuman', '#DDEBFA'), ('Donat', 'Snack', '#F9D9E6')]) + '''</div>
<div class="tile" style="display:flex;flex-direction:column;gap:8px"><small>Pesanan #0142 · Meja 4</small>
<div class="row" style="margin:0"><b>Kopi susu</b><span class="r chip mut">× 2</span></div><div class="row" style="margin:0"><b>Roti bakar</b><span class="r chip mut">× 1</span></div><div class="row" style="margin:0"><b>Air mineral</b><span class="r chip mut">× 1</span></div>
<div style="margin-top:auto;display:grid;gap:6px"><div style="background:#7C5CE8;color:#fff;border-radius:10px;padding:10px;text-align:center;font-weight:800;font-size:13px">Bayar QRIS</div><div style="border:1px solid #E4DEFA;border-radius:10px;padding:9px;text-align:center;font-weight:700;font-size:13px">Tunai / EDC</div></div></div></div>'''),
    'erp': dict(tone='blue', letter='E', name='Altora ERP', title='Stok & pembelian', tabs=['Stok', 'Pembelian', 'Keuangan', 'Dashboard'],
        emoji='📦', n1='Stok, pembelian, dan keuangan terhubung', n2='Satu angka yang sama untuk semua divisi', body='''
<div class="h">STOK MULTI-GUDANG</div>
<div style="border:1px solid #EEEAF8;border-radius:12px;overflow:hidden;margin-bottom:12px;font-size:12.5px">
<div style="display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;padding:9px 12px;background:#FBFAFE;color:#7A8099;font-weight:700"><span>Barang</span><span>Gudang A</span><span>Gudang B</span><span>Status</span></div>
''' + ''.join(f'<div style="display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;padding:9px 12px;border-top:1px solid #F0ECF8;align-items:center"><b>{n}</b><span>{a}</span><span>{b}</span><span><span class="chip {c}">{s}</span></span></div>'
             for n, a, b, c, s in [('Oli mesin 20L', '48', '12', 'ok', 'Aman'), ('Filter udara', '9', '3', 'warn', 'Menipis'), ('Ban 11.00-20', '16', '20', 'ok', 'Aman'), ('Baut roda', '0', '35', 'info', 'Transfer')]) + '''</div>
<div class="h">PERMINTAAN PEMBELIAN</div>
<div class="row"><span class="chip info">PR-118</span><div><b>Filter udara · 40 unit</b><br><small>Diajukan bagian workshop</small></div><span class="r chip warn">Menunggu persetujuan</span></div>'''),
}

TEMPLATE = '''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet"><style>{css}</style></head>
<body style="--a:{accent}"><div class="brand"><i>{letter}</i>{name}</div>
<div class="stage"><div class="win"><div class="bar"><span></span><span></span><span></span><b>{title}</b><em>🔒 Server sendiri</em></div>
<div class="tabs">{tabs}</div><div class="body">{body}</div></div>
<div class="note"><i>{emoji}</i><div><b>{n1}</b><small>{n2}</small></div></div></div></body></html>'''


def render(key, a, tmp):
    tabs = ''.join(f'<span{" class=on" if i == 0 else ""}>{t}</span>' for i, t in enumerate(a['tabs']))
    page = TEMPLATE.format(css=CSS, accent=TONE[a['tone']], tabs=tabs, **{k: a[k] for k in ('letter', 'name', 'title', 'body', 'emoji', 'n1', 'n2')})
    src, png = tmp / f'{key}.html', tmp / f'{key}.png'
    src.write_text(page, encoding='utf-8')
    subprocess.run([CHROME, '--headless=new', f'--user-data-dir={tmp}/u', '--hide-scrollbars', '--virtual-time-budget=6000', '--window-size=800,1000',
                    '--force-device-scale-factor=2', f'--screenshot={png}', src.as_uri()], check=True, capture_output=True)
    subprocess.run(['cwebp', '-quiet', '-q', '82', '-resize', '800', '1000', str(png), '-o', str(OUT / f'{key}.webp')], check=True)


if __name__ == '__main__':
    keys = sys.argv[1:] or list(APPS)
    with tempfile.TemporaryDirectory() as d:
        for k in keys:
            render(k, APPS[k], pathlib.Path(d))
            print('ilustrasi:', k)
