"""Isi bagian edukasi beranda (index.html) di antara penanda <!-- home-*:start/end -->.
Jalankan dari root repo:  python3 scripts/build_home.py
Artikel terbaru diambil dari content/blog/*.md (lewat build_blog.parse)."""
import html, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / 'scripts'))
from build_blog import parse, tanggal  # noqa: E402

e = lambda t: html.escape(t, quote=True)

# Masalah yang sering ditemui: judul (bahasa pemilik usaha), penyebab, arah solusi, link
PROBLEMS = [
    ('Rekap absensi tiap akhir bulan makan waktu berhari-hari.',
     'Data dari mesin absensi, izin lewat chat, dan lembur di kertas harus disatukan manual sebelum payroll.',
     'Absensi lewat HP atau wajah dari CCTV, izin dan lembur diajukan di aplikasi, rekap jadi otomatis.',
     '/produk#teams', 'Altora Teams'),
    ('CCTV ada, tapi rekaman baru dibuka setelah kejadian.',
     'Tidak ada yang sanggup memantau puluhan layar seharian, jadi kamera hanya jadi alat bukti.',
     'AI membaca rekaman dan mengirim notifikasi saat ada pelanggaran APD atau orang masuk area terlarang.',
     '/services/ai-cctv', 'AI CCTV & Safety'),
    ('Posisi truk baru diketahui setelah menelepon sopir.',
     'Tanpa pelacak, dispatcher bergantung pada laporan sopir, dan pemakaian BBM baru ketahuan di akhir bulan.',
     'GPS tracker di tiap kendaraan, posisi dan rute terlihat di peta, alert saat keluar jalur.',
     '/services/fleet-management-service', 'Fleet Management'),
    ('Approval tertahan karena atasan sedang di lapangan.',
     'Pengajuan masih berupa kertas atau pesan chat yang mudah tenggelam.',
     'Pengajuan dan persetujuan lewat aplikasi di HP, lengkap dengan riwayatnya.',
     '/services/software-custom', 'Software Custom'),
    ('Calon klien mencari di Google, yang ketemu justru pesaing.',
     'Website lama sulit diperbarui, lambat di HP, dan tidak disusun untuk pencarian.',
     'Website yang cepat, isinya jelas, dan disusun supaya mudah ditemukan di kota Anda.',
     '/services/website-seo', 'Website & SEO'),
    ('Perangkat sudah dibeli, tapi tidak ada yang memasang dan merawat.',
     'Penjual, teknisi, dan pembuat aplikasi berbeda orang, jadi saat rusak saling lempar tanggung jawab.',
     'Satu tim dari pemilihan perangkat, pemasangan, sampai perawatan berkala.',
     '/services/pengadaan-instalasi-maintenance', 'Pengadaan & Maintenance'),
]

GUIDE = [
    ('Proses Anda umum', 'Absensi, kasir, pelacakan armada, CCTV, akses pintu.',
     'Pakai aplikasi jadi', 'Lebih cepat dipasang dan biayanya lebih ringan, karena fiturnya sudah dipakai klien lain.', '/produk', 'Lihat aplikasi'),
    ('Proses Anda khusus', 'Alur approval berlapis, aturan internal yang unik, atau harus tersambung ke sistem lama.',
     'Buat aplikasi custom', 'Dibuat mengikuti proses Anda. Butuh waktu lebih lama karena dirancang dan diuji bersama tim Anda.', '/services/software-custom', 'Tentang aplikasi custom'),
    ('Sebagian umum, sebagian khusus', 'Misalnya absensi standar, tapi laporan dan approval-nya punya aturan sendiri.',
     'Mulai dari aplikasi jadi, lalu kembangkan', 'Bagian umum langsung jalan, bagian khusus ditambahkan bertahap.', '/contact', 'Konsultasi gratis'),
]

BEFORE_AFTER = [
    ('Kios layanan kelurahan', '/portfolio/custom-kios-k-pengadaan-hardware', '/assets/img/portfolio/hardware-field/kiosk-baqa-service.jpg',
     ['Perangkat layanan warga belum tersedia di kantor kelurahan.', 'Pengadaan, pemasangan, dan serah terima diurus terpisah.'],
     ['Kios, PC, dan tablet dipasang dan diuji di tiap kelurahan.', 'Satu tim menangani dari pengadaan sampai serah terima.']),
    ('Absensi wajah dari CCTV', '/portfolio/smart-attendance', '/assets/img/portfolio/attendance.jpg',
     ['Karyawan antre di mesin absensi saat jam masuk.', 'Data kehadiran direkap manual untuk payroll.'],
     ['Kamera di pintu masuk mengenali wajah dan mencatat jam masuk.', 'Data kehadiran langsung tersedia untuk HR.']),
    ('Pemantauan armada hauling', '/portfolio/fleet-management', '/assets/img/portfolio/fms.jpg',
     ['Posisi kendaraan diketahui lewat telepon atau radio.', 'Data perjalanan dicatat dari laporan sopir.'],
     ['Posisi dan perjalanan kendaraan terlihat di dashboard.', 'Data kendaraan terbaca langsung dari tracker.']),
]


def masalah():
    cards = ''.join(
        f'<article class="hm-card"><h3>{e(t)}</h3><p class="hm-why"><b>Penyebabnya</b>{e(why)}</p>'
        f'<p class="hm-fix"><b>Solusinya</b>{e(fix)}</p><a href="{u}">{e(lbl)}</a></article>'
        for t, why, fix, u, lbl in PROBLEMS)
    return ('<section class="sec hm-sec" id="masalah"><div class="wrap"><div class="hm-head"><p class="eyebrow">Masalah umum</p>'
            '<h2>Masalah yang sering kami temui</h2><p class="lead">Kalau salah satunya terasa familiar, Anda tidak sendirian. Ini penyebab dan cara kami biasanya menyelesaikannya.</p></div>'
            f'<div class="hm-grid">{cards}</div></div></section>')


def panduan():
    rows = ''.join(
        f'<li class="hg-row"><div class="hg-if"><small>Jika</small><b>{e(c)}</b><span>{e(cd)}</span></div>'
        f'<div class="hg-then"><small>Maka</small><b>{e(a)}</b><span>{e(ad)}</span><a href="{u}">{e(lbl)}</a></div></li>'
        for c, cd, a, ad, u, lbl in GUIDE)
    return ('<section class="sec hg-sec" id="pilih"><div class="wrap"><div class="hm-head"><p class="eyebrow">Panduan singkat</p>'
            '<h2>Aplikasi jadi atau dibuat khusus?</h2><p class="lead">Pertanyaan yang paling sering kami terima. Jawabannya tergantung seberapa umum proses kerja Anda.</p></div>'
            f'<ol class="hg-list">{rows}</ol></div></section>')


def sesudah():
    items = ''.join(
        f'<article class="ba-card"><a class="ba-pic" href="{u}"><img alt="" loading="lazy" src="{img}"/></a><div class="ba-body"><h3>{e(t)}</h3>'
        f'<div class="ba-cols"><div class="ba-before"><small>Sebelum</small><ul>{"".join(f"<li>{e(x)}</li>" for x in b)}</ul></div>'
        f'<div class="ba-after"><small>Sesudah</small><ul>{"".join(f"<li>{e(x)}</li>" for x in a)}</ul></div></div>'
        f'<a class="ba-link" href="{u}">Lihat proyeknya</a></div></article>'
        for t, u, img, b, a in BEFORE_AFTER)
    return ('<div class="ba-head"><p class="eyebrow">Sebelum dan sesudah</p><h2>Apa yang berubah setelah sistem dipakai</h2>'
            '<p class="lead">Dari beberapa proyek yang sudah kami kerjakan.</p></div>'
            f'<div class="ba-grid">{items}</div>')


def artikel():
    posts = sorted((parse(p) for p in (root / 'content/blog').glob('*.md') if not p.name.startswith('_')),
                   key=lambda p: p['date'], reverse=True)[:3]
    if not posts:
        return ''
    cards = ''.join(
        f'<a class="ha-card" href="/blog/{p["slug"]}"><small>{e(p["category"])}</small><h3>{e(p["title"])}</h3>'
        f'<p>{e(p["description"])}</p><span>Baca panduan</span></a>' for p in posts)
    return ('<section class="sec ha-sec" id="artikel"><div class="wrap"><div class="ha-head"><div><p class="eyebrow">Panduan</p>'
            '<h2>Baca dulu sebelum memutuskan</h2></div><a class="home-more" href="/blog">Semua artikel</a></div>'
            f'<div class="ha-grid">{cards}</div></div></section>')


def fill(s, name, content):
    return re.sub(rf'<!-- home-{name}:start -->.*?<!-- home-{name}:end -->',
                  lambda _: f'<!-- home-{name}:start -->{content}<!-- home-{name}:end -->', s, count=1, flags=re.S)


if __name__ == '__main__':
    idx = root / 'index.html'
    s = idx.read_text(encoding='utf-8')
    for name, fn in [('masalah', masalah), ('panduan', panduan), ('sesudah', sesudah), ('artikel', artikel)]:
        s = fill(s, name, fn())
    idx.write_text(s, encoding='utf-8')
    print('beranda: bagian edukasi diperbarui')
