"""Halaman /support. Jalankan lewat scripts/build_all.sh.
Form tiket memakai /api/tickets (ticket-form.js), sama seperti /contact."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, SITE, WA
from site_data import OFFICES, one_line, maps_link, PHONE_DISPLAY, EMAIL

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)

ICO = {
    'chat': '<path d="M4 5h16v11H8l-4 4z"/><path d="M8 9h8M8 12h5"/>',
    'tool': '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.5 2.5-2.3-.7-.7-2.3z"/>',
    'book': '<path d="M5 4h11a2 2 0 0 1 2 2v14H7a2 2 0 0 1-2-2z"/><path d="M5 18a2 2 0 0 1 2-2h11"/>',
    'box': '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'target': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".8"/>',
    'image': '<rect height="14" rx="2" width="18" x="3" y="5"/><circle cx="9" cy="10" r="1.6"/><path d="m21 16-5-5-8 8"/>',
    'send': '<path d="M4 12 20 4l-6 16-3-7z"/><path d="m11 13 9-9"/>',
    'search': '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
    'check': '<path d="M5 12.5 10 17 19 7"/>',
    'wa': '<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/><path d="M8.5 8.8c.3 2.7 2.9 5.4 5.7 5.9l1.3-1.3 2 .9-.4 1.7c-4.6.3-9.4-4.5-9.2-9l1.7-.4.9 2-1.3 1.3"/>',
    'mail': '<rect height="14" rx="2" width="18" x="3" y="5"/><path d="m3 7 9 6 9-6"/>',
    'ticket': '<path d="M4 7a2 2 0 0 0 2-2h12a2 2 0 0 0 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 0-2 2H6a2 2 0 0 0-2-2v-3a2 2 0 0 0 0-4z"/><path d="M10 9h4M10 15h4"/>',
}
ico = lambda n: f'<svg aria-hidden="true" viewBox="0 0 24 24">{ICO[n]}</svg>'
wa = lambda m: WA + quote(m)

PATHS = [
    ('chat', 'Sebelum mulai', 'Sedang mempertimbangkan bekerja sama dengan Altora.', ['Pertanyaan produk & layanan', 'Diskusi kebutuhan', 'Integrasi dengan sistem lama', 'Penawaran & survei'],
     'Mulai konsultasi', wa('Halo Altora, saya ingin konsultasi sebelum mulai.'), 'sp-purple'),
    ('tool', 'Sudah jadi klien', 'Ada kendala teknis atau pertanyaan pemakaian.', ['Aplikasi atau perangkat bermasalah', 'Perlu teknisi ke lokasi', 'Tambah pengguna atau fitur', 'Perawatan berkala'],
     'Laporkan kendala', '#tiket', 'sp-green'),
    ('book', 'Informasi layanan', 'Ingin melihat layanan dan perangkat yang tersedia.', ['Halaman layanan', 'Katalog perangkat', 'Artikel & panduan', 'Katalog barang & jasa'],
     'Lihat layanan', '/services', 'sp-blue'),
]
PREP = [('box', 'Aplikasi atau perangkat', 'Aplikasi, fitur, atau perangkat yang bermasalah.'), ('pin', 'Lokasi', 'Kantor atau cabang tempat masalah terjadi.'),
        ('target', 'Yang diharapkan', 'Apa yang seharusnya terjadi.'), ('image', 'Yang terjadi', 'Ceritakan, sertakan foto atau screenshot bila ada.')]
FLOW = [('send', 'Kirim pesan', 'Lewat WhatsApp, email, atau form tiket.'), ('search', 'Kami pelajari', 'Tim membaca dan mengecek masalahnya, dari jarak jauh dulu.'),
        ('tool', 'Kami tangani', 'Solusi jarak jauh, atau teknisi datang ke lokasi bila perlu.'), ('check', 'Selesai', 'Anda menerima kabar hasil dan catatannya.')]
FAQ = [('Apakah bisa dibantu dari jarak jauh?', 'Bisa. Sebagian besar kendala aplikasi dan pengaturan perangkat kami cek dulu dari jarak jauh. Kalau perlu, teknisi datang ke lokasi.'),
       ('Apakah melayani lokasi di luar Samarinda dan Balikpapan?', 'Bisa, sesuai kesepakatan. Kami melayani area Kalimantan Timur dan sekitarnya.'),
       ('Bagaimana dengan garansi perangkat?', 'Perangkat dari principal resmi memiliki garansi pabrikan. Kami bantu proses klaimnya, dan garansi jasa mengikuti lingkup proyek.'),
       ('Apakah ada kontrak perawatan bulanan?', 'Ada. Frekuensi kunjungan dan cakupan disesuaikan dengan jumlah perangkat dan kebutuhan Anda.')]

FORM = '''<form class="inquiry-form ct-form sp-form" data-ticket-form="" novalidate="">
<input name="notes" type="hidden" value="[SUPPORT] Laporan kendala dari halaman /support"/>
<div class="form-row"><label>Nama *<input autocomplete="name" maxlength="100" minlength="2" name="name" placeholder="Nama Anda" required=""/></label><label>Email *<input autocomplete="email" maxlength="254" name="email" placeholder="nama@email.com" required="" type="email"/></label></div>
<div class="form-row"><label>Nomor WhatsApp *<input autocomplete="tel" inputmode="tel" maxlength="32" minlength="8" name="whatsapp" placeholder="Contoh: 0812…" required=""/></label><label>Lokasi / cabang *<input maxlength="100" minlength="2" name="city" placeholder="Contoh: Balikpapan Utara" required=""/></label></div>
<div class="form-row"><label>Instansi / perusahaan<input autocomplete="organization" maxlength="120" name="organization" placeholder="Opsional"/></label><label>Jenis kendala *<select name="service" required=""><option disabled="" selected="" value="">Pilih jenis</option><option value="software">Aplikasi / sistem</option><option value="website">Website</option><option value="ai-vision">CCTV / AI Vision</option><option value="iot">GPS, sensor & IoT</option><option value="hardware">Perangkat, jaringan & listrik</option><option value="integration">Integrasi data</option><option value="other">Lainnya</option></select></label></div>
<label>Ceritakan kendalanya *<textarea aria-describedby="needs-hint needs-counter" maxlength="1800" minlength="15" name="needs" placeholder="Contoh: kamera CCTV di gudang belakang tidak tampil di aplikasi sejak pagi." required="" rows="4"></textarea><span class="field-hint" id="needs-hint">Minimal 15 karakter. Foto atau screenshot bisa dikirim lewat WhatsApp setelah tiket dibuat.</span><span aria-live="polite" class="field-counter" data-needs-counter="" id="needs-counter"></span></label>
<div class="form-row"><label>Seberapa mendesak?<input maxlength="120" name="timeline" placeholder="Contoh: operasional terganggu / bisa minggu ini"/></label><div></div></div>
<div aria-live="polite" class="form-result" data-ticket-result=""></div>
<div class="ct-submit"><button class="btn btn-purple" type="submit">Kirim tiket</button><p class="inquiry-note">Nomor tiket dikirim ke email Anda. Kami lanjutkan lewat WhatsApp.</p></div>
</form>'''


def build():
    paths = ''.join(f'<article class="sp-path {cls}"><span class="sp-path-ico">{ico(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p>'
                    '<ul class="sp-check">' + ''.join(f'<li>{e(x)}</li>' for x in pts) + '</ul>'
                    f'<a class="btn btn-purple" href="{e(href)}"' + (' rel="noopener" target="_blank"' if href.startswith('http') else '') + f'>{e(cta)} →</a></article>'
                    for i, t, d, pts, cta, href, cls in PATHS)
    prep = ''.join(f'<li><span class="sp-mini-ico">{ico(i)}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for i, t, d in PREP)
    flow = ''.join(f'<li><span class="sp-flow-ico">{ico(i)}</span><b>{e(t)}</b><p>{e(d)}</p></li>' for i, t, d in FLOW)
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    offices = ''.join(f'<a href="{e(maps_link(o))}" rel="noopener" target="_blank"><b>{e(o["label"])}</b><span>{e(one_line(o))}</span></a>' for o in OFFICES)
    body = f'''<main class="ct-page sp-page">
<section class="sp-hero"><div class="ct-wrap sp-hero-grid">
<div><p class="eyebrow eyebrow-purple">Support</p><h1>Butuh bantuan? Kami bantu sampai selesai.</h1>
<p class="ct-lead">Pertanyaan sebelum mulai, kendala saat aplikasi atau perangkat sudah dipakai, sampai perawatan berkala. Dicek jarak jauh dulu, teknisi datang bila perlu.</p>
<div class="sp-channels">
<a class="sp-ch sp-ch-wa" href="{wa("Halo Altora, saya butuh bantuan support.")}" rel="noopener" target="_blank"><span>{ico("wa")}</span><div><b>WhatsApp</b><small>{e(PHONE_DISPLAY)}</small></div></a>
<a class="sp-ch" href="mailto:{EMAIL}"><span>{ico("mail")}</span><div><b>Email</b><small>{e(EMAIL)}</small></div></a>
<a class="sp-ch" href="#tiket"><span>{ico("ticket")}</span><div><b>Kirim tiket</b><small>Dapat nomor tiket</small></div></a></div></div>
<div class="sp-visual" aria-hidden="true">
<div class="sp-phone"><div class="sp-phone-head"><span class="sp-av">A</span><div><b>Altora Support</b><small>online</small></div></div>
<div class="sp-msgs"><p class="sp-in">Halo, kamera CCTV di gudang belakang tidak tampil di aplikasi sejak pagi.</p>
<p class="sp-out">Siap. Tiket <b>ALT-1014</b> sudah dibuat. Kami cek koneksinya dari jarak jauh dulu ya.</p>
<p class="sp-out">Ternyata switch PoE-nya mati. Teknisi kami ke lokasi jam 13.00.</p>
<p class="sp-in">Sudah tampil lagi, terima kasih!</p>
<p class="sp-sys">{ico("check")} Tiket ALT-1014 selesai</p></div></div>
<span class="sp-badge sp-b1">{ico("search")} Cek jarak jauh dulu</span><span class="sp-badge sp-b2">{ico("tool")} Teknisi ke lokasi</span><span class="sp-badge sp-b3">{ico("check")} Tercatat sampai selesai</span>
</div></div></section>
<section class="sp-sec"><div class="ct-wrap"><div class="sp-head"><p class="eyebrow eyebrow-purple">Pilih jalur</p><h2>Supaya pertanyaan Anda sampai ke orang yang tepat</h2></div>
<div class="sp-paths">{paths}</div></div></section>
<section class="sp-sec sp-soft" id="tiket"><div class="ct-wrap sp-ticket">
<div class="sp-ticket-side"><p class="eyebrow eyebrow-purple">Laporkan kendala</p><h2>Kirim tiket support</h2><p class="sp-p">Tidak harus lengkap. Kirim saja yang Anda punya, kami tanyakan sisanya.</p>
<p class="sp-sub">Siapkan bila ada:</p><ul class="sp-prep">{prep}</ul></div>
<div class="sp-form-card">{FORM}</div></div></section>
<section class="sp-sec"><div class="ct-wrap"><div class="sp-head"><p class="eyebrow eyebrow-purple">Alurnya</p><h2>Setelah Anda menghubungi kami</h2></div><ol class="sp-flow">{flow}</ol></div></section>
<section class="sp-sec sp-soft"><div class="ct-wrap sp-split"><div class="svd-faq"><h2>Pertanyaan umum</h2><div>{faq}</div></div>
<div class="sp-offices"><h2>Kantor kami</h2>{offices}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Butuh bantuan sekarang?</h2><p>Chat WhatsApp, kami balas secepatnya.</p></div><a class="btn btn-purple" href="{wa("Halo Altora, saya butuh bantuan support.")}" rel="noopener" target="_blank">Chat WhatsApp</a></div></section>
</main>'''
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'ContactPage', 'name': 'Support Altora Indonesia', 'url': SITE + '/support'},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]}
    page = shell('Support Altora Indonesia | Bantuan Teknis & Tiket', 'Bantuan teknis Altora: laporkan kendala aplikasi, CCTV, GPS, jaringan, atau perangkat lewat WhatsApp, email, atau tiket. Teknisi lokal di Samarinda dan Balikpapan.',
                 '/support', SITE + '/assets/img/altora-logo-600.png', ld, body)
    return page.replace('</body>', '<script defer="" src="/assets/js/ticket-form.js?v=20261010-inline"></script></body>')


if __name__ == '__main__':
    (root / 'support.html').write_text(build(), encoding='utf-8')
    print('support.html dibuat')
