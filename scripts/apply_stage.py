"""Hero bergambar model untuk halaman utama (Layanan, Aplikasi, Tentang, Karier, Support, Konsultasi).
Gaya mengikuti hero beranda: satu jendela aplikasi di belakang, model berdiri di depannya dengan kaki terpotong
tepi bawah hero, dan dua kartu kecil melayang. Tiap halaman memakai foto model yang berbeda (beranda: person-hero).
Artikel dan halaman detail sengaja tanpa model. Idempoten. Jalankan setelah apply_shell.py."""
import pathlib
from bs4 import BeautifulSoup

root = pathlib.Path(__file__).resolve().parent.parent
CSS = '<link href="/assets/css/stage.css?v=4" rel="stylesheet"/>'
ICO = {
    'grid': '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    'chat': '<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    'brief': '<rect height="13" rx="2" width="18" x="3" y="7"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/>',
    'shield': '<path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
}
# berkas: (selektor section, selektor kontainer, selektor visual lama yang diganti, model, tipe foto, screenshot, chip)
PAGES = {
    'services.html': ('section.svh-hero', 'div.svh-wrap', None, 'faq', 'bust', '/assets/img/apps/office-board.webp',
                      [('grid', '14 layanan', 'Software, CCTV, smart home &amp; IT'), ('check', 'Konsultasi gratis', 'Tanpa kewajiban lanjut')]),
    'aplikasi.html': ('section.svd-hero', 'div.ap2-hero-hub', 'div.ab-collage', 'flow', 'full', '/assets/img/apps/fieldops-overview.webp',
                      [('grid', '20+ aplikasi', 'Dikembangkan tim Altora'), ('chat', 'Bisa didemokan', 'Minta demo lewat WhatsApp')]),
    'about.html': ('section.ab-hero', 'div.ab-hero-grid', 'div.ab-collage', 'cta', 'full', '/assets/img/apps/teams-overview.webp',
                   [('pin', '3 kantor', 'Samarinda &amp; Balikpapan'), ('shield', 'Inaproc / LKPP', 'Terdaftar sebagai penyedia')]),
    'careers.html': ('section.ct-hero', 'div.ct-wrap', None, 'stats', 'bust', '/assets/img/apps/control-center-board.webp',
                     [('brief', '3 posisi dibuka', 'Engineering &amp; marketing'), ('pin', 'Balikpapan · Samarinda', 'Kerja bersama tim lokal')]),
    'support.html': ('section.sp-hero', 'div.sp-hero-grid', 'div.sp-hero-grid > div:nth-of-type(2)', 'support', 'bust', '/assets/img/apps/control-center-portfolio.webp',
                     [('check', 'Tiket terselesaikan', 'Dicek jarak jauh dulu'), ('chat', 'WhatsApp', 'Dibalas di jam kerja')]),
    'contact.html': ('section.ct-hero', 'div.ct-wrap', None, 'problem', 'bust', '/assets/img/services/website.webp',
                     [('chat', 'Konsultasi gratis', 'Belum tahu solusinya? Tidak apa-apa'), ('spark', 'Solusi bertahap', 'Mulai dari yang paling penting')]),
}
ALT = {'faq': 'Staf Altora menjelaskan layanan', 'flow': 'Staf Altora memperkenalkan aplikasi', 'cta': 'Staf Altora',
       'stats': 'Calon anggota tim Altora', 'support': 'Tim support Altora', 'problem': 'Klien yang berkonsultasi'}


def stage(model, kind, shot, chips):
    ch = ''.join(f'<div class="pg-chip pg-chip-{i}"><span class="pg-ci pg-ci-{i}"><svg aria-hidden="true" viewBox="0 0 24 24">{ICO[ic]}</svg></span>'
                 f'<span><b>{t}</b><i>{d}</i></span></div>' for i, (ic, t, d) in enumerate(chips, 1))
    win = (f'<figure class="pg-win"><span class="pg-bar"><i></i><i></i><i></i></span><img alt="" loading="eager" src="{shot}"/></figure>' if shot else '')
    return (f'<div class="pg-stage pg-{kind} pg-m-{model}"><span aria-hidden="true" class="pg-blob"></span>{win}{ch}'
            f'<img alt="{ALT[model]}" class="pg-person" src="/assets/img/person-{model}.webp"/></div>')


n = 0
for f, (sec_sel, box_sel, old_sel, model, kind, shot, chips) in PAGES.items():
    p = root / f
    soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    sec = soup.select_one(sec_sel)
    box = sec.select_one(box_sel) if sec else None
    if not box:
        print('lewati', f); continue
    for st in box.select('div.pg-stage'):
        st.decompose()
    for img in soup.select('img.hero-model'):          # sisa pemasangan lama
        img.decompose()
    if old_sel:
        for el in soup.select(old_sel):
            el.decompose()
    copy = box.find('div', class_='pg-copy', recursive=False)
    if copy is None:
        kids = [c for c in box.find_all(recursive=False)]
        if len(kids) == 1 and kids[0].name == 'div':
            copy = kids[0]
            copy['class'] = list(dict.fromkeys((copy.get('class') or []) + ['pg-copy']))
        else:
            copy = soup.new_tag('div', attrs={'class': 'pg-copy'})
            for c in list(box.contents):
                copy.append(c.extract())
            box.append(copy)
    box.append(BeautifulSoup(stage(model, kind, shot, chips), 'html.parser'))
    box['class'] = list(dict.fromkeys((box.get('class') or []) + ['pg-hero']))
    sec['class'] = list(dict.fromkeys((sec.get('class') or []) + ['has-stage']))
    out = str(soup)
    import re as _re; out = _re.sub(r'<link href="/assets/css/models\.css[^"]*" rel="stylesheet"/>', '', out)
    out = _re.sub(r'<link href="/assets/css/stage\.css[^"]*" rel="stylesheet"/>', '', out)
    out = out.replace('</head>', CSS + '</head>', 1)
    p.write_text(out, encoding='utf-8'); n += 1
print('hero model terpasang di', n, 'halaman')
