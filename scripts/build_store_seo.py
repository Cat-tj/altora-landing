"""Halaman SEO /aplikasi-toko: aplikasi toko untuk stok, PO pembeli, invoice, dan surat jalan (Altora Store).
Kata kunci: aplikasi toko, aplikasi stok barang, sistem PO toko, aplikasi invoice dan surat jalan, aplikasi toko sparepart/bangunan.
Screenshot dari Altora Store dengan data contoh. Jalankan lewat scripts/build_all.sh (setelah build_aplikasi.py)."""
import html, pathlib, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE, WA
from build_aplikasi import APPS, pic

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(t, quote=True)
URL = '/aplikasi-toko'
A = APPS['store']
DEMO = WA + quote('Halo Altora, saya ingin minta demo aplikasi toko (Altora Store).')
PAINS = [('Stok di Excel tidak cocok dengan rak', 'Barang tercatat ada padahal sudah habis, atau sebaliknya, karena pencatatan masuk dan keluar tidak di satu tempat.'),
         ('PO pembeli tercecer', 'Nomor PO dari pembeli proyek atau instansi ada di chat dan kertas, sehingga sulit dicocokkan saat menagih.'),
         ('Nota, surat jalan, dan invoice diketik ulang', 'Data yang sama ditulis berkali-kali di dokumen berbeda, dan salah ketik baru ketahuan saat barang sampai.'),
         ('Piutang dan utang lewat jatuh tempo', 'Tidak ada pengingat tagihan yang mendekati atau lewat jatuh tempo, jadi arus kas sulit ditebak.')]
FLOW = [('Penawaran harga', 'Kirim surat penawaran PDF ke calon pembeli.'), ('PO pembeli', 'Nomor PO dan lokasi proyek dicatat di nota, bisa diisi belakangan.'),
        ('Nota & surat jalan', 'Penawaran dijadikan penjualan; stok berkurang otomatis dengan FIFO, surat jalan dicetak.'),
        ('Invoice & tagihan', 'Invoice, tanda terima invoice bulanan, dan surat tagihan dari nota yang belum lunas.'),
        ('Lunas & laporan', 'Pembayaran tercatat; laba, piutang, dan stok terbaru langsung terlihat di laporan.')]
FIT = ['Toko spare part dan bearing', 'Toko bangunan dan material', 'Toko alat teknik dan kebutuhan industri', 'Grosir dan distributor',
       'Toko yang melayani proyek, perusahaan, atau instansi dengan PO']
FAQ = [('Apa itu aplikasi toko Altora Store?', 'Altora Store adalah sistem toko berbasis web untuk mencatat stok, pembelian, penjualan, penawaran, nomor PO pembeli, invoice, surat jalan, dan laporan dalam satu aplikasi.'),
       ('Apakah aplikasi ini bisa mencatat PO dari pembeli?', 'Bisa. Nomor PO dan lokasi proyek dicatat di setiap nota dan tampil di invoice, sehingga tagihan mudah dicocokkan dengan dokumen pembeli.')] + A['faq'][1:] + [
       ('Apakah bisa disesuaikan dengan alur toko kami?', 'Bisa. Kami menyesuaikan satuan barang, format dokumen, laporan, dan hak akses dengan cara kerja toko Anda.')]


def build():
    pains = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in PAINS)
    flow = ''.join(f'<li><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in FLOW)
    mods = ''.join(f'<article class="svd-do"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in A['modules'])
    fit = ''.join(f'<li>{e(x)}</li>' for x in FIT)
    shots = ''.join(f'<div class="ap2-feat"><div class="ap2-feat-txt"><h3>{e(t)}</h3></div>{pic(sid, alt)}</div>' for sid, alt, t in A['shots'][1:])
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(x)}</p></details>' for q, x in FAQ)
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'SoftwareApplication', 'name': 'Altora Store', 'alternateName': 'Aplikasi toko Altora', 'url': SITE + URL,
         'description': 'Aplikasi toko berbasis web untuk stok FIFO, pembelian, penjualan dengan nomor PO, penawaran, invoice, surat jalan, dan laporan.',
         'applicationCategory': 'BusinessApplication', 'applicationSubCategory': 'Inventory and point of sale', 'operatingSystem': 'Web',
         'image': SITE + '/assets/img/apps/store-penjualan.webp', 'inLanguage': 'id',
         'featureList': [t for t, _ in A['modules']],
         'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'url': SITE + '/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Aplikasi', 'item': SITE + '/aplikasi'}, {'@type': 'ListItem', 'position': 3, 'name': 'Aplikasi toko', 'item': SITE + URL}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in FAQ]}]}
    body = f'''<main class="ct-page svd-page ap2-page">
<section class="svd-hero"><div class="ct-wrap ap2-hero">
<div class="ap2-hero-copy"><nav aria-label="Breadcrumb" class="bl-crumb"><a href="/aplikasi">Aplikasi</a><span>/</span><span>Aplikasi toko</span></nav>
<p class="eyebrow eyebrow-purple">Altora Store · aplikasi toko</p><h1>Aplikasi toko untuk stok, PO pembeli, invoice, dan surat jalan.</h1>
<p class="ct-lead">Ganti catatan manual dan Excel dengan satu sistem: stok per batch dengan FIFO, penawaran yang jadi nota, nomor PO pembeli di setiap invoice, surat jalan, piutang dan utang dengan jatuh tempo, sampai laporan laba. Dibuka dari komputer kasir maupun HP.</p>
<div class="svd-actions"><a class="btn btn-purple" href="{DEMO}" rel="noopener" target="_blank">Minta demo</a><a class="svd-link" href="/aplikasi/store">Lihat detail Altora Store</a></div></div>
{pic(A["shots"][0][0], A["shots"][0][1], True)}
</div></section>
<section class="svd-sec svd-pains"><div class="ct-wrap svd-pains-grid"><div class="pd-block-head"><h2>Tanda toko Anda butuh sistem</h2><p>Masalah yang paling sering kami temui di toko yang masih memakai buku dan Excel.</p></div><ul>{pains}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Alur dari penawaran sampai lunas</h2><p>Satu data mengalir ke semua dokumen, tanpa ketik ulang.</p></div><ol class="svd-steps st-flow">{flow}</ol></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Fitur aplikasi toko</h2></div><div class="svd-dos">{mods}</div></div></section>
<section class="svd-sec"><div class="ct-wrap ap2-fit"><div class="pd-block-head"><h2>Cocok untuk</h2><p>Toko yang menjual barang dengan kode atau nomor part, tunai maupun tempo.</p></div><ul class="ap2-fitlist">{fit}</ul></div></section>
<section class="svd-sec"><div class="ct-wrap"><div class="pd-block-head"><h2>Tampilan aplikasi</h2><p>Screenshot dari aplikasi yang berjalan, dengan data contoh.</p></div><div class="ap2-feats">{shots}</div></div></section>
<section class="svd-sec"><div class="ct-wrap svd-faq"><div class="pd-block-head"><h2>Pertanyaan umum</h2></div><div>{faq}</div></div></section>
<section class="pd-cta"><div class="ct-wrap pd-cta-inner"><div><h2>Lihat aplikasi toko ini langsung</h2><p>Kami tunjukkan lewat demo singkat dan bahas penyesuaian untuk toko Anda.</p></div><a class="btn btn-purple" href="{DEMO}" rel="noopener" target="_blank">Minta demo</a></div></section>
</main>'''
    return shell('Aplikasi Toko untuk Stok, PO, Invoice & Surat Jalan | Altora Store',
                 'Aplikasi toko berbasis web: stok FIFO per batch, nomor PO pembeli, penawaran jadi nota, invoice dan surat jalan PDF, piutang, utang, dan laporan. Cocok untuk toko sparepart, bangunan, dan distributor.',
                 URL, SITE + '/assets/img/apps/store-penjualan.webp', ld, body)


if __name__ == '__main__':
    (root / 'aplikasi-toko.html').write_text(build(), encoding='utf-8')
    update_sitemap([URL])
    print('aplikasi-toko.html dibuat')
