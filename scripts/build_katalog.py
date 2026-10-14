"""Katalog ringkas yang bisa dicetak / disimpan sebagai PDF: /katalog.
Jalankan lewat scripts/build_all.sh."""
import html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import shell, update_sitemap, SITE
from build_apps import APPS
from catalog_data import HW_CATS, HW_ITEMS
from build_trust import CLIENTS, STATS
from site_data import OFFICES, one_line, PHONE_DISPLAY, EMAIL

root = pathlib.Path(__file__).resolve().parent.parent
e = lambda t: html.escape(str(t), quote=True)

apps = ''.join(f'<article class="kt-app"><img alt="" src="/assets/img/produk/{k}.webp"/><div><small>{e(a["tag"])}</small><h3>{e(a["name"])}</h3>'
               f'<p>{e(a["lead"])}</p><ul>' + ''.join(f'<li>{e(t)}</li>' for t, _ in a['feats'][:4]) + '</ul></div></article>' for k, a in APPS.items())
hw = ''
for c, t in HW_CATS:
    items = [h for h in HW_ITEMS if h['cat'] == c]
    if not items:
        continue
    rows = ''.join(f'<tr><td class="kt-pic">' + (f'<img alt="" src="/assets/img/hardware/{h["img"]}.webp"/>' if h['img'] else '') +
                   f'</td><td><b>{e(h["name"])}</b><br/><small>{e(h["brand"])}</small></td><td>{e(h["desc"])}</td>'
                   f'<td>' + '<br/>'.join(f'{e(k)}: {e(v)}' for k, v in h['specs'][:3]) + '</td></tr>' for h in items)
    hw += f'<h3 class="kt-cat">{e(t)}</h3><table class="kt-table"><tbody>{rows}</tbody></table>'
stats = ''.join(f'<div><b>{e(v)}</b><span>{e(k)}</span></div>' for v, k in STATS)
clients = ' · '.join(e(c[0]) for c in CLIENTS)
offices = ''.join(f'<li><b>{e(o["label"])}</b><br/>{e(one_line(o))}</li>' for o in OFFICES)

body = f'''<main class="ct-page kt-page">
<section class="kt-cover"><div class="ct-wrap">
<div class="kt-bar"><p class="eyebrow eyebrow-purple">Katalog produk & layanan · 2026</p><button class="btn btn-purple kt-print" onclick="window.print()" type="button">Cetak / simpan PDF</button></div>
<h1>Katalog Altora Indonesia</h1>
<p class="ct-lead">Software, AI, CCTV, IoT, perangkat, dan infrastruktur untuk bisnis dan instansi di Kalimantan Timur. Tanpa harga: penawaran disesuaikan kebutuhan dan lokasi.</p>
<div class="ts-stats kt-stats">{stats}</div>
<p class="kt-clients"><b>Klien:</b> {clients}</p>
</div></section>
<section class="kt-sec"><div class="ct-wrap"><h2>Aplikasi Altora</h2><div class="kt-apps">{apps}</div></div></section>
<section class="kt-sec"><div class="ct-wrap"><h2>Perangkat & hardware</h2>{hw}
<p class="kt-note">CCTV VIGI lengkap (148 model kamera, NVR, kit, decoder, solar): altora.id/katalog-cctv-vigi</p></div></section>
<section class="kt-sec"><div class="ct-wrap kt-contact"><h2>Kontak</h2><ul>{offices}</ul><p>WhatsApp {e(PHONE_DISPLAY)} · {e(EMAIL)} · altora.id</p>
<p>Badan usaha resmi berstatus PKP, terdaftar sebagai penyedia Inaproc/LKPP.</p></div></section>
</main>'''

if __name__ == '__main__':
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Katalog Altora Indonesia', 'url': SITE + '/katalog'}
    page = shell('Katalog Produk Altora 2026 | Cetak atau Simpan PDF', 'Katalog lengkap aplikasi, perangkat, dan layanan Altora Indonesia yang bisa dicetak atau disimpan sebagai PDF.',
                 '/katalog', SITE + '/assets/img/produk/vision.webp', ld, body)
    (root / 'katalog.html').write_text(page, encoding='utf-8')
    update_sitemap(['/katalog'])
    print('katalog.html dibuat')
