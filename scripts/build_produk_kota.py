"""Bangun halaman lokal produk x kota (mis. /jual-smartlock-samarinda): jual, pengadaan, instalasi, maintenance.
Produk: smart lock, CCTV VIGI, dan CCTV tenaga surya & 4G. Tanpa keranjang; pemesanan lewat WhatsApp.
Schema hanya Service (tanpa Product) supaya tidak memicu laporan cuplikan produk Google.
Jalankan dari root repo:  python3 scripts/build_produk_kota.py && python3 scripts/apply_shell.py && python3 scripts/apply_seo.py
Setiap halaman berisi daftar perangkat nyata (foto VIGI dan smart lock), FAQ khusus produk,
dan bagian kota (kantor, proyek). Jangan menambah kota tanpa kantor/proyek nyata di sana."""
import html, json, pathlib, re, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, CITIES as ALL_CITIES, PF, SITE, WA, office_of, near_of, needs_html
# perangkat dijual & dipasang tim sendiri: hanya kota dengan jangkauan teknisi (Kaltim)
CITIES = {k: v for k, v in ALL_CITIES.items() if v.get('scope') != 'nasional'}
# Kota di luar Kaltim: jual & kirim saja (tanpa janji pemasangan oleh tim sendiri). Videotron tidak, karena butuh perakitan di lokasi.
NAT_CITIES = {k: v for k, v in ALL_CITIES.items() if v.get('scope') == 'nasional'}
NAT_NAME = {'smartlock': 'smart lock', 'cctv': 'CCTV VIGI', 'cctv-surya': 'CCTV tenaga surya & 4G'}
NAT_DOS = [('Bantu pilih tipe', 'Ceritakan lokasi dan kebutuhan Anda, kami rekomendasikan tipe dan jumlah yang pas.'),
           ('Produk resmi & bergaransi', 'Dari distributor dan principal resmi, dengan garansi sesuai ketentuan principal.'),
           ('Dikirim ke {C}', 'Dikemas aman dan dikirim lewat ekspedisi ke alamat Anda. Detail pengiriman kita bahas lewat chat.'),
           ('Disiapkan sebelum dikirim', 'Untuk perangkat yang memungkinkan, akun dan pengaturan dasar kami siapkan lebih dulu.'),
           ('Panduan & bantuan jarak jauh', 'Panduan pemasangan dan bantuan pengaturan lewat WhatsApp atau video call.'),
           ('Pengadaan instansi', 'Penawaran, faktur, dan dokumen pengadaan untuk perusahaan dan instansi.')]
NAT_FAQ = [('Apakah bisa dikirim ke {C}?', 'Bisa. Barang dikirim lewat ekspedisi ke alamat Anda di {C}. Detail pengiriman kita bahas lewat chat.'),
           ('Apakah tim Altora ikut memasang di {C}?', 'Kantor dan teknisi kami ada di Kalimantan Timur. Untuk {C}, kami bantu lewat panduan dan pendampingan jarak jauh. Bila butuh pemasangan di lokasi, kami bahas per proyek.'),
           ('Apakah produknya resmi dan bergaransi?', 'Ya. Produk berasal dari distributor dan principal resmi, dengan garansi sesuai ketentuan masing-masing.'),
           ('Bagaimana cara memesan?', 'Chat kami lewat WhatsApp dengan tipe dan jumlah yang dibutuhkan. Kami balas dengan penawaran tertulis.')]
from site_data import OFFICES, ORG_ID

root = pathlib.Path(__file__).resolve().parent.parent
KATALOG = {'smartlock': '/pengadaan#p-smartlock', 'cctv': '/pengadaan#cctv', 'cctv-surya': '/pengadaan#p-vigi-solar'}   # katalog pengadaan perangkat
e = lambda t: html.escape(str(t), quote=True)


def vigi(model, specs):
    slug = re.sub(r'[^a-z0-9]+', '-', model.lower()).strip('-')
    return (f'vigi-{slug}', f'VIGI {model}', 'VIGI', f'/assets/img/vigi/{slug}.webp', specs)


PRODUCTS = {
    'smartlock': dict(slug='jual-smartlock-{c}', short='Smartlock', noun='smart lock', h1='Jual & pasang smartlock di {C}',
        title='Jual & Pasang Smartlock {C} | Kunci Digital | Altora',
        desc='Jual dan pasang smartlock di {C}: kunci pintu digital untuk rumah, kantor, kampus, dan gudang. Buka dengan aplikasi, PIN, kartu, sidik jari, atau wajah.',
        lead='Kunci pintu digital untuk rumah, kantor, ruko, kampus, dan gudang di {C}. Kami bantu pilih tipe yang cocok dengan pintu Anda, pasang, atur aplikasinya, dan rawat setelahnya.',
        hero='/assets/img/hardware/smartlock.webp', main='/services/smart-lock', main_label='Layanan smart lock',
        items=[('smartlock-pintu', 'Smartlock pintu (handle & sliding)', 'Smartlock', '/assets/img/hardware/smartlock.webp',
                ['Buka via aplikasi, PIN, kartu RFID, sidik jari', 'Untuk pintu kayu, aluminium, dan kaca geser', 'Kunci darurat (emergency key)']),
               ('smartlock-doorcam', 'Smartlock + kamera pintu', 'Smartlock', '/assets/img/hardware/smartlock.webp',
                ['Wajah 3D dan kamera pintu', 'Notifikasi video ke HP', 'Riwayat keluar-masuk lengkap']),
               ('smartlock-em', 'Akses kantor (EM lock & solenoid)', 'Smartlock', '',
                ['Dropbolt / EM lock untuk pintu kantor', 'Tombol keluar tanpa sentuh, auto relock', 'Kartu akses per karyawan'])],
        dos=[('Pilih tipe sesuai pintu', 'Kami cek jenis pintu, ketebalan, dan arah bukaan sebelum menentukan tipe kunci.'),
             ('Pemasangan rapi', 'Lubang, kabel, dan tombol keluar dipasang rapi tanpa merusak kusen.'),
             ('Atur aplikasi & pengguna', 'Akun admin, pengguna, kartu, dan akses tamu kami siapkan sampai siap dipakai.'),
             ('Riwayat akses', 'Catatan siapa masuk dan kapan, bisa diekspor untuk keperluan administrasi.'),
             ('Pengadaan jumlah banyak', 'Untuk kantor, kos, hotel, atau kampus dengan banyak pintu.'),
             ('Garansi & perawatan', 'Penggantian baterai, cek mekanik, dan bantuan teknis setelah terpasang.')],
        faq=[('Apakah smartlock bisa dipasang di pintu yang sudah ada?', 'Umumnya bisa. Kami cek ketebalan dan jenis pintu saat survei supaya tipe kuncinya pas.'),
             ('Kalau baterai habis bagaimana?', 'Aplikasi memberi peringatan sebelum baterai habis, dan tersedia kunci darurat atau port daya cadangan sesuai tipe.'),
             ('Bisa memberi akses sementara untuk tamu?', 'Bisa. Akses tamu dapat dibatasi waktu dari aplikasi.'),
             ('Apakah bisa untuk banyak pintu di kantor?', 'Bisa. Semua pintu dikelola dari satu aplikasi dengan hak akses per orang.')]),
    'cctv': dict(slug='jual-cctv-{c}', short='Jual CCTV', noun='CCTV', h1='Jual CCTV VIGI di {C}',
        title='Jual CCTV {C} | Kamera VIGI, NVR & Pasang | Altora',
        desc='Jual CCTV di {C}: kamera VIGI dome, bullet, turret, pan tilt, 4G, NVR, dan paket CCTV. Pengadaan resmi, instalasi, dan garansi oleh tim Altora.',
        lead='Kamera CCTV VIGI by TP-Link, NVR, dan paket CCTV untuk rumah, toko, kantor, gudang, dan proyek di {C}. Beli putus atau sekalian dipasang dan dirawat oleh tim kami.',
        hero='/assets/img/vigi/s385dps.webp', main='/services/cctv', main_label='Layanan pasang CCTV',
        items=[vigi('S245', ['Dome 4 MP full-color', 'People & vehicle analytics', 'Untuk ruangan & lobi']),
               vigi('S345', ['Bullet 4 MP full-color', 'Outdoor, tahan cuaca', 'Untuk pagar & parkiran']),
               vigi('S445', ['Turret 4 MP full-color', 'Audio dua arah', 'Untuk teras & gudang']),
               vigi('C540', ['Pan tilt 4 MP, putar 360°', 'Auto tracking', 'Untuk halaman luas']),
               vigi('C540-4G', ['Pan tilt 4G (SIM)', 'Tanpa kabel internet', 'Untuk proyek & kebun']),
               vigi('S385DPS', ['Panoramic 8 MP dual-lens', 'ColorPro, malam tetap berwarna', 'Untuk area terbuka lebar']),
               vigi('NVR1008H-8MP', ['NVR 8 kanal', '8 port PoE+', 'Rekaman hingga 10 TB']),
               vigi('NVR2016H-16MP', ['NVR 16 kanal', '16 port PoE+', '2 HDD'])],
        dos=[('Pengadaan resmi', 'Kamera dan NVR VIGI resmi dengan garansi, untuk satuan maupun proyek.'),
             ('Hitung kebutuhan', 'Kirim denah atau foto lokasi, kami hitungkan jumlah kamera dan kapasitas rekaman.'),
             ('Paket siap pasang', 'Kamera, NVR, hard disk, kabel, dan instalasi dalam satu penawaran.'),
             ('Instalasi rapi', 'Tiang, bracket, junction box, dan jalur kabel yang rapi.'),
             ('Pantau dari HP', 'Aplikasi VIGI dan VMS kami atur sampai bisa dipantau dari HP.'),
             ('Perawatan berkala', 'Cek kamera, rekaman, dan firmware secara berkala.')],
        faq=[('Apakah bisa beli CCTV saja tanpa pasang?', 'Bisa. Kami juga melayani pembelian putus, termasuk untuk teknisi dan kontraktor.'),
             ('CCTV VIGI itu merek apa?', 'VIGI adalah lini CCTV profesional dari TP-Link, dengan kamera AI, NVR, dan aplikasi pemantauan.'),
             ('Apakah tersedia merek selain VIGI?', 'Dahua (mitra resmi) serta Hikvision dan HiLook juga tersedia sesuai kebutuhan proyek. Tanyakan lewat WhatsApp.'),
             ('Kamera mana yang cocok untuk malam hari?', 'Untuk area gelap, pilih seri ColorPro (kode S) yang tetap berwarna di malam hari, atau seri IR (kode I).'),
             ('Apakah tersedia paket CCTV?', 'Tersedia paket NVR + kamera + hard disk, dan bisa disesuaikan jumlah titiknya.')]),
    'cctv-surya': dict(slug='cctv-tenaga-surya-{c}', short='CCTV tenaga surya', noun='CCTV tenaga surya', h1='CCTV tenaga surya & 4G di {C}',
        title='CCTV Tenaga Surya {C} | Solar Panel & 4G | Altora',
        desc='CCTV tenaga surya dan 4G di {C} untuk proyek, kebun, tambak, tambang, dan area tanpa listrik. Paket panel surya VIGI, kamera 4G, dan instalasi.',
        lead='Untuk lokasi yang tidak ada listrik atau kabel internet di sekitar {C}: area proyek, kebun, tambak, gudang terpencil, dan jalan tambang. Kamera hidup dari panel surya dan terhubung lewat 4G.',
        hero='/assets/img/hardware/vigi-solar.webp', main='/services/cctv', main_label='Layanan pasang CCTV',
        items=[vigi('SP9030', ['Panel surya 90 W', 'Baterai lithium 31,2 Ah', 'IP66, dipantau dari aplikasi']),
               vigi('SP6030', ['Panel surya 60 W', 'Baterai lithium 31,2 Ah', 'IP66']),
               vigi('SP6020', ['Panel surya 60 W', 'Baterai lithium 20,8 Ah', 'IP66']),
               vigi('C540-4G', ['Pan tilt 4G (SIM)', 'Bisa jadi router untuk perangkat lain', 'Full-color']),
               vigi('S345-4G', ['Bullet 4 MP 4G', 'Full-color', 'Outdoor']),
               vigi('PS30', ['Solar controller', 'Untuk sistem solar custom', 'Pantau dari aplikasi'])],
        dos=[('Survei lokasi', 'Cek arah matahari, sinyal 4G, dan titik pandang kamera.'),
             ('Hitung daya', 'Kapasitas panel dan baterai disesuaikan jumlah kamera dan lama cuaca mendung.'),
             ('Tiang & mounting', 'Tiang, bracket, dan grounding yang kuat untuk area terbuka.'),
             ('Koneksi 4G atau Starlink', 'Pakai kamera 4G, atau Starlink untuk lokasi tanpa sinyal seluler.'),
             ('Pantau jarak jauh', 'Rekaman dan status baterai dipantau dari HP.'),
             ('Perawatan', 'Pembersihan panel dan pengecekan baterai berkala.')],
        faq=[('Apakah CCTV tenaga surya tetap menyala di malam hari?', 'Ya. Baterai mengisi di siang hari dan menghidupkan kamera di malam hari. Kapasitasnya kami hitung agar tahan beberapa hari mendung.'),
             ('Bagaimana kalau tidak ada sinyal 4G?', 'Bisa memakai Starlink atau wireless bridge ke titik yang ada internet.'),
             ('Apakah rekaman tersimpan kalau internet putus?', 'Ya. Kamera menyimpan rekaman di microSD, lalu bisa diakses lagi saat koneksi kembali.'),
             ('Cocok untuk area apa?', 'Proyek konstruksi, kebun sawit, tambak, gudang terpencil, jalan hauling, dan pos jaga.')]),
}


def fmt(t, c):
    return t.replace('{C}', c['name']).replace('{c}', c['key'])


def card(it, city):
    pid, name, brand, img, specs = it
    pic = f'<img alt="{e(name)}" loading="lazy" src="{e(img)}"/>' if img else '<span class="pk-noimg" aria-hidden="true"></span>'
    lis = ''.join(f'<li>{e(s)}</li>' for s in specs)
    msg = f'Halo Altora, saya di {city} dan ingin tahu ketersediaan {name}.'
    return (f'<article class="pk-item"><div class="pk-pic">{pic}</div><small>{e(brand)}</small><h3>{e(name)}</h3><ul>{lis}</ul>'
            f'<div class="vg-act">'
            f'<a class="vg-ask" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Tanya stok</a></div></article>')


def page(pkey, ckey):
    p = PRODUCTS[pkey]; c = dict(ALL_CITIES[ckey], key=ckey)
    nas = c.get('scope') == 'nasional'
    url = '/' + fmt(p['slug'], c)
    h1, title, desc = fmt(p['h1'], c), fmt(p['title'], c), fmt(p['desc'], c)
    if nas:
        n = NAT_NAME[pkey]; N = n[0].upper() + n[1:]
        h1 = f'Jual {n} di {c["name"]}'
        title = f'Jual {N} {c["name"]} | Pengadaan Resmi | Altora'
        desc = f'Jual {n} di {c["name"]}: produk resmi bergaransi untuk perusahaan dan instansi, dikirim ke lokasi Anda dengan panduan pengaturan dari tim Altora.'
        p = dict(p, lead=f'{N} untuk perusahaan, instansi, dan usaha di {c["name"]}. Kami bantu pilih tipe, siapkan pengadaan resmi, kirim ke alamat Anda, lalu dampingi pengaturannya dari jarak jauh. Pemasangan di lokasi dibahas per proyek.',
                 dos=NAT_DOS, faq=[f for f in p['faq'] if 'survei' not in f[1] and 'Kami cek' not in f[1]][:2] + NAT_FAQ)
    if len(title) > 65:
        title = f'{p["short"]} {c["name"]} | Altora Indonesia'
    if len(desc) > 160:
        desc = desc[:157].rsplit(' ', 1)[0].rstrip(',.:;') + '.'
    items = ''.join(card(it, c['name']) for it in p['items'])
    dos = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(fmt(d, c))}</p></article>' for t, d in p['dos'])
    proof_sec = ''
    faq_items = [(fmt(q, c), fmt(a, c)) for q, a in p['faq']] + ([] if nas else [
        (f'Apakah melayani pengadaan dan pemasangan {p.get("noun", p["short"].lower())} di {c["name"]}?', c['base'])]) + [
        ('Apakah bisa untuk pengadaan instansi pemerintah?', 'Bisa. Altora berstatus PKP dan terdaftar di Inaproc/LKPP, sehingga dapat melayani pengadaan instansi dan BUMN.')]
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq_items)
    near = near_of(ckey)
    same_city = ''.join(f'<a href="/{fmt(PRODUCTS[k]["slug"], c)}">{e(PRODUCTS[k]["short"])} {e(c["name"])}</a>' for k in products_for(ckey) if k != pkey)
    local_links = (f'<a href="/software-house-{ckey}">Software house {e(c["name"])}</a><a href="/jasa-pembuatan-aplikasi-{ckey}">Jasa pembuatan aplikasi {e(c["name"])}</a>' if nas else
                   f'<a href="/jasa-pasang-cctv-{ckey}">Jasa pasang CCTV {e(c["name"])}</a><a href="/it-support-{ckey}">IT support {e(c["name"])}</a>')
    links = (''.join(f'<a href="/{fmt(p["slug"], dict(ALL_CITIES[k], key=k))}">{e(p["short"])} {e(ALL_CITIES[k]["name"])}</a>' for k in near if pkey in products_for(k)) +
             f'<a href="{p["main"]}">{e(p["main_label"])}</a>' + f'<a href="{KATALOG[pkey]}">Katalog pengadaan perangkat</a>' + local_links + same_city)
    msg = f'Halo Altora, saya di {c["name"]} dan butuh {p.get("noun", p["short"].lower())}.'
    office = office_of(c)
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': h1, 'description': desc, 'url': SITE + url, 'serviceType': f'Penjualan, pengadaan & instalasi {p.get("noun", p["short"].lower())}',
         'areaServed': {'@type': 'City', 'name': c['name']},
         'provider': {'@id': ORG_ID}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Area layanan', 'item': SITE + '/area-layanan'},
            {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': SITE + url}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items]}]}
    body = f'''<main class="ct-page svd-page lc-page pk-page">
<section class="svd-hero"><div class="ct-wrap svd-hero-grid">
<div class="svd-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/area-layanan">Area layanan</a><span>/</span><span>{e(c["name"])}</span></nav>
<p class="eyebrow eyebrow-purple">{"Jual · Pengadaan · Kirim ke " + e(c["name"]) if nas else "Jual · Pengadaan · Instalasi · Maintenance"}</p><h1>{e(h1)}</h1><p class="ct-lead">{e(fmt(p["lead"], c))}</p>
<div class="svd-actions"><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Minta penawaran</a><a class="svd-link" href="#produk">Lihat produk</a></div></div>
<figure class="svd-hero-pic pk-hero-pic"><img alt="{e(h1)}" src="{p["hero"]}"/><span class="svd-chip svd-chip-0">{e(c["name"])}</span><span class="svd-chip svd-chip-1">Produk resmi</span><span class="svd-chip svd-chip-2">{"Dikirim ke lokasi" if nas else "Dipasang tim lokal"}</span></figure>
</div></section>
<section class="svd-sec" id="produk"><div class="ct-wrap"><div class="pd-block-head"><h2>Produk yang tersedia di {e(c["name"])}</h2><p>Tanyakan ketersediaan lewat WhatsApp; detail dan penawaran kami kirim lewat chat.</p></div>
<div class="pk-grid">{items}</div></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>{"Pengadaan sampai pengiriman" if nas else "Pengadaan sampai perawatan"}</h2></div><div class="svd-dos">{dos}</div></div></section>
<section class="svd-sec"><div class="ct-wrap lc-office"><div><h2>{"Pengiriman ke " + e(c["name"]) if nas else "Melayani " + e(c["name"]) + " dan sekitarnya"}</h2><p>{e(NAT_FAQ[1][1].replace("{C}", c["name"]) if nas else c["base"])}</p>{"" if c.get("needs") else f"<p>Klien kami di {e(c['name'])} antara lain {e(c['sectors'])}.</p>"}</div></div></section>
{needs_html(c)}
{proof_sec}
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div>
<div class="svd-related"><b>Lihat juga</b>{links}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh {e(p.get("noun", p["short"].lower()))} di {e(c["name"])}?</h2><p>Kirim kebutuhan Anda, kami balas dengan penawaran.</p></div><a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    img = p['hero'] if p['hero'].startswith('http') else SITE + p['hero']
    return url, h1, shell(title, desc, url, img, ld, body)


def products_for(ckey):
    # perangkat dijual & dipasang hanya di Samarinda
    return list(PRODUCTS) if ckey == 'samarinda' else []


def hub_section(built):
    links = ''.join(f'<a class="lc-svc" href="{u}"><b>{e(h)}</b></a>' for (ck, u, h) in built)
    return ('<!-- produk-kota:start --><section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Perangkat di Samarinda</h2>'
            '<p>Penjualan, pemasangan, dan perawatan CCTV dan smart lock untuk Samarinda dan sekitarnya.</p></div>'
            f'<div class="lc-svcs">{links}</div></div></section><!-- produk-kota:end -->')

if __name__ == '__main__':
    built = []
    for ckey in ALL_CITIES:
        for pkey in products_for(ckey):
            url, h1, htmlp = page(pkey, ckey)
            (root / (url.lstrip('/') + '.html')).write_text(htmlp, encoding='utf-8')
            built.append((ckey, url, h1))
    # hub /area-layanan & /produk: daftar halaman produk per kota
    sec = hub_section(built)
    for f, anchor in (('area-layanan.html', '</main>'),):
        fp = root / f; s = fp.read_text(encoding='utf-8')
        if '<!-- produk-kota:start -->' in s:
            s = re.sub(r'<!-- produk-kota:start -->.*?<!-- produk-kota:end -->', lambda _: sec, s, count=1, flags=re.S)
        else:
            s = s.replace(anchor, sec + anchor, 1)
        fp.write_text(s, encoding='utf-8')
    update_sitemap([u for _, u, _ in built])
    print('produk x kota:', len(built), 'halaman')
