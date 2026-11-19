"""Blok kredibilitas di beranda & /about: logo klien, angka, prestasi, proses kerja, keamanan data, industri.
Jalankan dari root repo:  python3 scripts/build_trust.py && python3 scripts/apply_shell.py
Blok disisipkan di antara penanda <!-- nama:start --> ... <!-- nama:end -->."""
import html, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import FACTS, OFFICE_SAMARINDA_GEO, HOME_FAQ, PHONE_DISPLAY, EMAIL
from portofolio_data import CLIENTS

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)

# Angka dan klien sama dengan situs saudara (dikonfirmasi pemilik kedua perusahaan, 2026-11-18). Ikon: (riwayat, piala, tim).
STATS = [('6+', 'tahun beroperasi', 'clock'), ('50+', 'proyek terdeliver', 'trophy'), ('13', 'ahli in-house', 'team')]
HOME_CSS = '<link href="/assets/css/home-sections.css?v=20261119a" rel="stylesheet"/>'
HOME_JS = '<script defer src="/assets/js/home-sections.js?v=20261118p"></script>'

INDUSTRIES = [
    ('pertambangan', 'Tambang & industri berat', 'Aplikasi pelaporan, approval, dan dashboard'),
    ('pemerintahan', 'Pemerintahan & layanan publik', 'Website resmi dan aplikasi layanan'),
    ('pendidikan', 'Kampus & sekolah', 'Website, portal informasi, dan aplikasi administrasi'),
    ('korporasi', 'Korporasi & dunia usaha', 'Aplikasi custom, website, dan SEO'),
]

ICO = {
    'trophy': '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8.5 20h7M10 17h4"/>',
    'cloud': '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 9.5 4.3 4.3 0 0 0 7 18Z"/>',
    'server': '<rect height="6" rx="1.5" width="16" x="4" y="4"/><rect height="6" rx="1.5" width="16" x="4" y="14"/><path d="M8 7h.01M8 17h.01"/>',
    'gov': '<path d="M3 10 12 4l9 6M5 10v8M19 10v8M9 10v8M15 10v8M3 20h18"/>',
    'role': '<circle cx="9" cy="8" r="3"/><path d="M3 19c.6-3 3-5 6-5s5.4 2 6 5"/><path d="m16 11 2 2 3-4"/>',
    'log': '<path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7M9 15h7M9 7h4"/>',
    'backup': '<path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M4 4v4h4M12 8v4l3 2"/>',
    'lock': '<rect height="10" rx="2" width="14" x="5" y="11"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'code': '<path d="m9 8-4 4 4 4M15 8l4 4-4 4M13 6l-2 12"/>',
    'ai': '<rect height="12" rx="2" width="12" x="6" y="6"/><path d="M9.5 9.5h5v5h-5zM9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'clock': '<path d="M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5"/><path d="M12 7v5l3 2"/>',
    'team': '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.2 3-5 6-5s5.4 1.8 6 5"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 14.2c2.3.2 3.9 1.7 4.5 4.3"/>',
}

def ico(n):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICO[n]}</svg>'


# Logo per sektor untuk halaman /industri/* (build_industri.py): (nama, berkas logo, sektor). Belum diisi.
SECTOR_CLIENTS = []


def logo_tile(name, logo, sector):
    inner = (f'<img alt="{e(name)}" height="56" loading="lazy" src="/assets/img/clients/{logo}"/>' if logo
             else f'<span class="tl-word">{e(name)}</span>')
    return f'<li class="tl-tile" title="{e(name)}">{inner}</li>'


def stats_block():
    """Strip kepercayaan seperti situs saudara: judul kecil, logo klien abu-abu, tiga kartu angka; legalitas di bawahnya."""
    logos = ''.join(f'<img alt="{e(n)}" height="46" loading="lazy" src="/assets/img/clients/{f}" width="80"/>' for n, f in CLIENTS)
    stats = ''.join(f'<div class="hm-stat"><span class="hm-stat-ico">{ico(i)}</span><div><b>{e(v)}</b><span>{e(k)}</span></div></div>' for v, k, i in STATS)
    creds = ['Badan usaha resmi, berstatus PKP', 'Terdaftar sebagai penyedia di Inaproc / LKPP']
    return ('<section aria-label="Klien dan angka" class="hm hm-trust"><div class="hm-wrap">'
            '<h2>Dipercaya pemerintahan, kampus, industri, F&amp;B, dan klien internasional</h2>'
            f'<div class="hm-logos">{logos}</div><div class="hm-stats">{stats}</div>'
            '<ul class="hm-creds">' + ''.join(f'<li>{e(c)}</li>' for c in creds) + '</ul></div></section>')


# Peta jangkauan: koordinat pin dalam persen terhadap peta 1000x620 (sama dengan peta titik situs saudara).
# Proyeksi peta Kalimantan (dicocokkan dari pin Bontang, Samarinda, Balikpapan): x% = 64.93 + 7.57*(lon-116.85),
# y% = 61.31 - 12.12*(lat-0.13). Pin kantor pusat dihitung dari OFFICE_SAMARINDA_GEO (Palaran, tenggara kota Samarinda).
HQ_PIN = (round(64.93 + 7.57 * (OFFICE_SAMARINDA_GEO[1] - 116.85), 2), round(61.31 - 12.12 * (OFFICE_SAMARINDA_GEO[0] - 0.13), 2))
HW_PINS = [('Bontang', 69.85, 61.31, 'r', 1, 'M676.6 433.6Q675.4 397.6 698.5 380.1'),
           ('Balikpapan · 2 cabang', 64.93, 77.92, 'r', 2, 'M676.6 433.6Q648.6 449.6 649.3 483.1'),
           ('Penajam · IKN', 63.97, 74.35, 'l', 0, 'M676.6 433.6Q648.7 436.5 639.7 461.0')]
SW_PINS = [('Kuala Lumpur', 45.11, 53.53, 'l', 0, 'M500.5 343.5Q478.4 326.8 451.1 331.9'), ('Shanghai', 51.43, 39.06, 'l', 1, 'M500.5 343.5Q485.1 289.8 514.3 242.2'),
           ('Seoul', 53.19, 35.79, 't', 2, 'M500.5 343.5Q489.4 275.8 531.9 221.9'), ('Tokyo', 57.25, 36.76, 'r', 3, 'M500.5 343.5Q511.1 269.9 572.5 227.9'),
           ('Sydney', 60.93, 72.60, 'r', 4, 'M500.5 343.5Q578.4 372.9 609.3 450.1'), ('Dubai', 30.28, 42.16, 'l', 5, 'M500.5 343.5Q419.7 259.0 302.8 261.4'),
           ('London', 12.58, 28.61, 'r', 7, 'M500.5 343.5Q349.7 178.0 125.8 177.4'), ('San Francisco', 88.52, 35.69, 'l', 6, 'M500.5 343.5Q666.0 197.8 885.2 221.3')]


def _view(cls, img, label, hq, hq_lbl, pins):
    start = f'M{hq[0] * 10:.1f} {hq[1] * 6.2:.1f}'   # garis selalu berangkat dari pin kantor pusat
    pins = [(n, x, y, side, i, start + d[d.index('Q'):]) for n, x, y, side, i, d in pins]
    arcs = ''.join(f'<path class="arc arc-c" d="{d}" pathLength="1" style="--i:{i}"/><path class="arc" d="{d}" pathLength="1" style="--i:{i}"/>' for _, _, _, _, i, d in pins)
    pp = ''.join(f'<button class="pin" style="--x:{x}%;--y:{y}%;--i:{i}" type="button"><i></i><span class="lbl {side}">{e(n)}</span></button>' for n, x, y, side, i, _ in pins)
    return (f'<figure aria-label="{e(label)}" class="reach-view {cls}" role="img"><img alt="" decoding="async" height="620" loading="lazy" src="/assets/img/reach/{img}" width="1000"/>'
            f'<svg aria-hidden="true" viewBox="0 0 1000 620">{arcs}</svg><span class="pin hq" style="--x:{hq[0]}%;--y:{hq[1]}%"><i></i><span class="lbl {hq_lbl}">Samarinda · Kantor pusat</span></span>{pp}</figure>')


def reach_block():
    """'Berbasis di Samarinda, sejak 2019' + peta titik Kalimantan/dunia dengan tab Hardware/Software (perilaku: home-sections.js)."""
    checks = [('Hardware &amp; software, satu tim', 'Dari kamera dan sensor di lapangan sampai aplikasi dan dashboard, dikerjakan tim in-house yang sama.'),
              ('AI yang berjalan di server Anda', 'CCTV analytics, computer vision, dan AI lokal bisa berjalan on-premise, jadi data tidak keluar dari kantor Anda.'),
              ('Pilot dulu, baru skala', 'Mulai dari pilot 2–4 minggu dengan indikator yang jelas sebelum rollout penuh.')]
    li = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in checks)
    hw = _view('hw', 'borneo.svg', 'Peta Kalimantan: area layanan hardware Altora di Kalimantan Timur', HQ_PIN, 'l', HW_PINS)
    sw = _view('sw', 'world.svg', 'Peta dunia: software dan AI Altora dikerjakan dari Samarinda untuk klien di mana saja', (50.05, 55.40), 'b', SW_PINS)
    return ('<section class="hm hm-reach" id="jangkauan"><div class="hm-wrap hm-reach-grid"><div class="hm-reach-copy">'
            '<h2>Berbasis di Samarinda, <span class="hm-hl">sejak 2019</span></h2>'
            '<p class="hm-lead">Altora Indonesia berdiri di Samarinda pada 2019. Tim lapangan kami memasang dan merawat perangkat di Kalimantan Timur. '
            'Software dan AI kami kerjakan dari Samarinda untuk klien di dalam dan luar negeri.</p>'
            f'<ul class="hm-checks">{li}</ul>{nap_block()}'
            '<div class="hm-nap-act"><a class="hm-btn hm-btn-primary" href="/software-house-samarinda">Software house Samarinda</a>'
            '<a class="hm-btn hm-btn-ghost" href="/software-house-balikpapan">Software house Balikpapan</a></div></div>'
            '<div class="reach" data-mode="hw"><div aria-label="Jangkauan layanan Altora" class="reach-tabs" role="tablist">'
            '<button aria-selected="true" data-mode="hw" role="tab" type="button"><b>Hardware</b><span>Kalimantan Timur</span></button>'
            '<button aria-selected="false" data-mode="sw" role="tab" tabindex="-1" type="button"><b>Software</b><span>Seluruh dunia</span></button></div>'
            f'<div class="reach-map">{hw}{sw}</div>'
            '<p aria-live="polite" class="reach-cap"><span class="hw">Tim lapangan kami survei, memasang, dan merawat perangkat proyek di seluruh Kalimantan Timur. '
            'Pasang CCTV rumahan, smart lock, smart home, dan IT support bulanan khusus Samarinda.</span>'
            '<span class="sw">Software, AI, dan dashboard kami kerjakan dari Samarinda untuk klien di mana pun.</span></p></div></div></section>')


def nap_block():
    """Nama-alamat-telepon yang terlihat di beranda (sama persis dengan schema dan Google Business Profile)."""
    return ('<address class="hm-nap"><b>Altora Indonesia</b>'
            '<span>Kantor pusat: Jl. Dayak ASB, Bukuan, Kec. Palaran, Kota Samarinda, Kalimantan Timur</span>'
            '<span>Cabang: Jl. Soekarno Hatta, Muara Rapak, Balikpapan Utara · Kaliabang Tengah, Bekasi Utara</span>'
            f'<span><a href="tel:+6285190911170">{PHONE_DISPLAY}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="/about">Profil lengkap</a></span></address>')


ICON_FAQ = ['i-layers', 'i-monitor', 'i-puzzle', 'i-trend', 'i-sync', 'i-shield', 'i-clipboard', 'i-headset']
TONE_FAQ = ['purple', 'blue', 'cyan', 'green', 'pink', 'orange', 'navy', 'teal']


def faq_items():
    """FAQ beranda sebagai HTML statis (sebelumnya dibangkitkan main.js, tidak terbaca mesin pencari). Markup sama dengan versi JS."""
    return ''.join(f'<div class="qa reveal" data-d="{i % 4}"><summary aria-controls="fa{i}" aria-expanded="false" role="button" tabindex="0">'
                   f'<span class="mi mi-{TONE_FAQ[i % 8]}"><svg class="ico"><use href="#{ICON_FAQ[i % 8]}"/></svg></span><h3>{e(q)}</h3>'
                   '<svg class="ico caret"><use href="#i-chevron"/></svg></summary>'
                   f'<div class="qa-body" id="fa{i}"><p>{e(a)}</p></div></div>' for i, (q, a) in enumerate(HOME_FAQ))


def process_block():
    steps = [('Konsultasi', 'Pahami kebutuhan dan tujuan Anda. Gratis.'), ('Analisis & desain', 'Pelajari alur kerja dan rancang solusinya.'),
             ('Penawaran', 'Proposal dan rencana kerja tertulis.'), ('Pengerjaan', 'Pengembangan bertahap, dengan demo berkala untuk Anda.'),
             ('Pelatihan & dukungan', 'Pelatihan tim Anda dan dukungan setelah dipakai.')]
    st = ''.join(f'<li><span>{i}</span><b>{e(t)}</b><p>{e(d)}</p></li>' for i, (t, d) in enumerate(steps, 1))
    promises = ['Lingkup, jadwal, dan tanggung jawab tertulis',
                'Kode sumber, dokumentasi & SOP diserahkan', 'Mulai dari lingkup kecil, lalu berkembang bertahap', 'Teknologi umum, tidak terkunci pada satu vendor']
    pr = ''.join(f'<li>{e(p)}</li>' for p in promises)
    return ('<section class="sec how tp-sec" id="alur"><div class="wrap">'
            '<div class="tl-head"><p class="eyebrow eyebrow-purple">Cara kerja</p><h2>Dari analisis sampai dukungan, kami kawal</h2>'
            '<p>Setiap proyek berjalan lewat alur yang sama dan terdokumentasi, supaya Anda tahu apa yang dikerjakan, kapan, dan siapa penanggung jawabnya.</p></div>'
            f'<ol class="tp-steps">{st}</ol><ul class="tp-promise">{pr}</ul></div></section>')


def security_block():
    host = [('cloud', 'Cloud pilihan Anda', 'AWS, GCP, atau penyedia lokal.'),
            ('server', 'Server di kantor Anda', 'On-premise, data tidak keluar gedung.'),
            ('gov', 'Pusat data pemerintah', 'Untuk instansi yang wajib di data center sendiri.')]
    ctrl = [('role', 'Hak akses per peran', 'Setiap pengguna hanya melihat menu dan data miliknya.'),
            ('log', 'Audit log', 'Setiap perubahan data tercatat: siapa, kapan, apa.'),
            ('backup', 'Backup otomatis', 'Backup terjadwal dan bisa dipulihkan.'),
            ('lock', 'Enkripsi', 'Koneksi HTTPS, password terenkripsi, akun terkunci setelah salah berulang.'),
            ('code', 'Milik Anda', 'Kode sumber dan dokumentasi diserahkan sesuai kontrak.'),
            ]
    h = ''.join(f'<li><span class="tk-ico">{ico(i)}</span><b>{e(t)}</b><small>{e(d)}</small></li>' for i, t, d in host)
    c = ''.join(f'<li><span class="tk-ico">{ico(i)}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for i, t, d in ctrl)
    return ('<section class="sec tk-sec" id="keamanan"><div class="wrap tk-grid">'
            '<div class="tk-left"><p class="eyebrow eyebrow-purple">Keamanan data</p><h2>Data Anda tetap milik Anda</h2>'
            '<p>Pilih sendiri di mana sistem dan data disimpan. Untuk instansi dan perusahaan dengan data sensitif, semuanya bisa berjalan di server sendiri.</p>'
            f'<ul class="tk-host">{h}</ul></div><ul class="tk-ctrl">{c}</ul></div></section>')


IND_IMG = {'pertambangan': '/assets/img/apps/office-board.webp', 'pemerintahan': '/assets/img/apps/control-center-portfolio.webp',
           'pendidikan': '/assets/img/apps/office-project.webp', 'korporasi': '/assets/img/apps/office-project.webp'}


def industry_block():
    cards = ''.join(f'<a class="tin-card" href="/industri/{k}"><span class="tin-pic"><img alt="" loading="lazy" src="{IND_IMG[k]}"/></span>'
                    f'<span class="tin-body"><b>{e(t)}</b><small>{e(d)}</small><em>Lihat solusi {ico("arrow")}</em></span></a>' for k, t, d in INDUSTRIES)
    return ('<section class="sec ti-sec" id="industri"><div class="wrap"><div class="tl-head"><p class="eyebrow eyebrow-purple">Solusi per industri</p>'
            '<h2>Paham konteks tiap sektor</h2><p>Kebutuhan tambang berbeda dari kampus, instansi berbeda dari korporasi. Pilih sektor Anda.</p></div>'
            f'<div class="tin-grid">{cards}</div></div></section>')


PICKS = [('aplikasi', 'Aplikasi custom', '/jasa-pembuatan-aplikasi-{c}'), ('software', 'Software house', '/software-house-{c}'),
         ('website', 'Website', '/jasa-pembuatan-website-{c}'), ('seo', 'SEO', '/jasa-seo-{c}'), ('cctv', 'CCTV', '/services/cctv'),
         ('itsupport', 'IT support', '/services/it-support'), ('altora', 'Aplikasi Altora', '/aplikasi')]


def picks_block():
    chips = ''.join(f'<a class="hp-pick" data-href="{u}" href="{u.replace("{c}", "samarinda")}">{e(t)}</a>' for _, t, u in PICKS)
    return ('<div class="hp-picks reveal" data-d="3"><div class="hp-picks-top"><b>Saya mencari:</b>'
            '<span class="hp-city" role="group" aria-label="Kota"><button aria-pressed="true" data-city="samarinda" type="button">Samarinda</button>'
            '<button aria-pressed="false" data-city="balikpapan" type="button">Balikpapan</button></span></div>'
            f'<div class="hp-picks-list">{chips}</div></div>')


def put(s, name, block, anchor=None, before=True, replace_re=None):
    wrapped = f'<!-- {name}:start -->{block}<!-- {name}:end -->'
    if f'<!-- {name}:start -->' in s:
        return re.sub(rf'<!-- {name}:start -->.*?<!-- {name}:end -->', lambda _: wrapped, s, count=1, flags=re.S)
    if replace_re:
        new, n = re.subn(replace_re, lambda _: wrapped, s, count=1, flags=re.S)
        if n:
            return new
    assert anchor and anchor in s, (name, anchor)
    return s.replace(anchor, wrapped + anchor if before else anchor + wrapped, 1)


if __name__ == '__main__':
    p = root / 'index.html'; s = p.read_text(encoding='utf-8')
    s = put(s, 'hero-picks', picks_block(), anchor='</div>\n<div class="hero-stage', before=True)
    s = put(s, 'trust', '')
    s = put(s, 'stats', stats_block(), anchor='<!-- trust:end -->', before=False)
    s = put(s, 'reach', reach_block(), anchor='<!-- stats:end -->', before=False)
    if 'home-sections.css' not in s:
        s = s.replace('</head>', HOME_CSS + '</head>', 1)
    if 'home-sections.js' not in s:
        s = s.replace('</body>', HOME_JS + '</body>', 1)
    s = re.sub(r'/assets/(css/home-sections\.css|js/home-sections\.js)\?v=[0-9a-z]+', lambda m: HOME_CSS.split('"')[1] if 'css' in m.group(1) else HOME_JS.split('src="')[1].split('"')[0], s)
    s = put(s, 'proses', process_block(), replace_re=r'<section class="sec how" id="alur">.*?</section>')
    s = re.sub(r'<!-- keamanan:start -->.*?<!-- keamanan:end -->', '', s, flags=re.S)
    s = put(s, 'industri', industry_block(), anchor='<section class="sec faq-sec" id="faq">')
    s = re.sub(r'<div class="faq-grid" id="faqGrid">.*?</div><!-- faqgrid:end -->|<div class="faq-grid" id="faqGrid"></div>',
               lambda _: f'<div class="faq-grid" id="faqGrid">{faq_items()}</div><!-- faqgrid:end -->', s, count=1, flags=re.S)
    p.write_text(s, encoding='utf-8')
    # /beranda (salinan beranda tanpa pembuka 3D, canonical ke /) ikut FAQ statis dan versi CSS yang sama
    b = root / 'beranda.html'; t = b.read_text(encoding='utf-8')
    t = re.sub(r'<div class="faq-grid" id="faqGrid">.*?</div><!-- faqgrid:end -->|<div class="faq-grid" id="faqGrid"></div>',
               lambda _: f'<div class="faq-grid" id="faqGrid">{faq_items()}</div><!-- faqgrid:end -->', t, count=1, flags=re.S)
    t = re.sub(r'/assets/css/home-sections\.css\?v=[0-9a-z]+', HOME_CSS.split('"')[1], t)
    b.write_text(t, encoding='utf-8')

    print('blok kredibilitas: beranda diperbarui')
