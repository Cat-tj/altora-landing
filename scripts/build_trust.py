"""Blok kredibilitas di beranda & /about: logo klien, angka, prestasi, proses kerja, keamanan data, industri.
Jalankan dari root repo:  python3 scripts/build_trust.py && python3 scripts/apply_shell.py
Blok disisipkan di antara penanda <!-- nama:start --> ... <!-- nama:end -->."""
import html, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import FACTS

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)

# klien: dikosongkan (portofolio & logo klien dihapus saat pisah dari Sentra); isi ulang hanya dengan klien Altora yang sudah setuju dicantumkan
CLIENTS = []

STATS = [('3', 'kantor di Kaltim'), ('148+', 'produk resmi di katalog'), (FACTS['partners'], 'principal resmi')]

INDUSTRIES = [
    ('pertambangan', 'Tambang & industri berat', 'Starlink, CCTV tenaga surya, jaringan, dan aplikasi custom'),
    ('pemerintahan', 'Pemerintahan & layanan publik', 'Website resmi, kios layanan, dan pengadaan perangkat'),
    ('pendidikan', 'Kampus & sekolah', 'Website, display interaktif, jaringan, dan perangkat'),
    ('korporasi', 'Korporasi & dunia usaha', 'Aplikasi custom, website, CCTV, dan perangkat kantor'),
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
}

def ico(n):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICO[n]}</svg>'


def logo_tile(name, logo, sector):
    inner = (f'<img alt="{e(name)}" height="56" loading="lazy" src="/assets/img/clients/{logo}"/>' if logo
             else f'<span class="tl-word">{e(name)}</span>')
    return f'<li class="tl-tile" title="{e(name)}">{inner}</li>'


def logos_block(heading='Dipercaya oleh'):
    if not CLIENTS:
        return ''
    tiles = ''.join(logo_tile(*c) for c in CLIENTS)
    return (f'<section aria-label="Klien kami" class="sec tl-sec"><div class="wrap">'
            f'<div class="tl-head"><p class="eyebrow eyebrow-purple">Klien kami</p><h2>{e(heading)}</h2>'
            '<p>Sebagian klien mempercayakan lebih dari satu proyek. Dengan persetujuan klien, kami bisa memfasilitasi kontak referensi atau kunjungan lokasi.</p></div>'
            f'<ul class="tl-grid">{tiles}</ul></div></section>')


def stats_block():
    stats = ''.join(f'<div><b>{e(v)}</b><span>{e(k)}</span></div>' for v, k in STATS)
    creds = ['Badan usaha resmi, berstatus PKP', 'Terdaftar sebagai penyedia di Inaproc / LKPP']
    return ('<section aria-label="Angka dan legalitas" class="sec ts-sec"><div class="wrap">'
            f'<div class="ts-stats">{stats}</div>'
            '<ul class="ts-creds">' + ''.join(f'<li>{e(c)}</li>' for c in creds) + '</ul></div></section>')


def process_block():
    steps = [('Konsultasi', 'Pahami kebutuhan dan tujuan Anda. Gratis.'), ('Survei & desain', 'Cek lokasi dan rancang solusinya.'),
             ('Penawaran', 'Proposal dan rencana kerja tertulis.'), ('Pengerjaan', 'Pengembangan aplikasi atau pemasangan perangkat oleh tim kami.'),
             ('Training & purnajual', 'Pelatihan tim Anda dan dukungan berkelanjutan.')]
    st = ''.join(f'<li><span>{i}</span><b>{e(t)}</b><p>{e(d)}</p></li>' for i, (t, d) in enumerate(steps, 1))
    promises = ['Garansi perangkat & jasa sesuai lingkup proyek',
                'Kode sumber, dokumentasi & SOP diserahkan', 'Mulai dari lingkup kecil, lalu berkembang bertahap', 'Tidak terkunci pada satu merek']
    pr = ''.join(f'<li>{e(p)}</li>' for p in promises)
    return ('<section class="sec how tp-sec" id="alur"><div class="wrap">'
            '<div class="tl-head"><p class="eyebrow eyebrow-purple">Cara kerja</p><h2>Dari survei sampai purnajual, kami kawal</h2>'
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


IND_IMG = {'pertambangan': '/assets/img/hardware/starlink-enterprise.webp', 'pemerintahan': '/assets/img/hardware/kios-k.webp',
           'pendidikan': '/assets/img/hardware/hde-ifp.webp', 'korporasi': '/assets/img/hardware/lenovo-thinkpad-t14.webp'}


def industry_block():
    cards = ''.join(f'<a class="tin-card" href="/industri/{k}"><span class="tin-pic"><img alt="" loading="lazy" src="{IND_IMG[k]}"/></span>'
                    f'<span class="tin-body"><b>{e(t)}</b><small>{e(d)}</small><em>Lihat solusi {ico("arrow")}</em></span></a>' for k, t, d in INDUSTRIES)
    return ('<section class="sec ti-sec" id="industri"><div class="wrap"><div class="tl-head"><p class="eyebrow eyebrow-purple">Solusi per industri</p>'
            '<h2>Paham konteks tiap sektor</h2><p>Kebutuhan tambang berbeda dari kampus, instansi berbeda dari korporasi. Pilih sektor Anda.</p></div>'
            f'<div class="tin-grid">{cards}</div></div></section>')


PICKS = [('cctv', 'CCTV', '/jual-cctv-{c}'), ('software', 'Software house', '/software-house-{c}'), ('pengadaan', 'Pengadaan', '/katalog#v-pengadaan'),
         ('jaringan', 'Jaringan & WiFi', '/jasa-instalasi-jaringan-{c}'), ('website', 'Website', '/jasa-pembuatan-website-{c}'), ('starlink', 'Starlink', '/jual-starlink-{c}'),
         ('gps', 'GPS tracker', '/gps-tracker-kendaraan-{c}'), ('itsupport', 'IT support', '/it-support-{c}')]


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
    s = put(s, 'trust', logos_block())
    s = put(s, 'stats', stats_block(), anchor='<!-- trust:end -->', before=False)
    s = put(s, 'proses', process_block(), replace_re=r'<section class="sec how" id="alur">.*?</section>')
    s = re.sub(r'<!-- keamanan:start -->.*?<!-- keamanan:end -->', '', s, flags=re.S)
    s = put(s, 'industri', industry_block(), anchor='<section class="sec faq-sec" id="faq">')
    p.write_text(s, encoding='utf-8')

    print('blok kredibilitas: beranda diperbarui')
