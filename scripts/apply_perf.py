"""Optimasi muat halaman (Core Web Vitals) yang dipasang ke semua halaman HTML. Dijalankan terakhir oleh build_all.sh.

1. Google Fonts tidak lagi memblokir render: semua varian <link rel="stylesheet" href="https://fonts.googleapis.com/css2?...">
   diganti satu URL yang sama (Plus Jakarta Sans 400-800 + JetBrains Mono 400/500/700, display=swap) yang dimuat dengan
   media="print" lalu dialihkan ke "all" saat selesai, ditambah preload dan <noscript> sebagai cadangan.
   Teks langsung tampil dengan font cadangan sistem lalu bertukar ke Plus Jakarta Sans begitu font siap
   (diukur Lighthouse mobile: CLS tetap 0 di beranda, /software-house-samarinda, /pengadaan, /portofolio).
2. Preconnect ke fonts.googleapis.com dan fonts.gstatic.com dipastikan ada.
Idempoten: tautan yang sudah diubah dikenali dari data-perf="font" dan tidak disentuh lagi.
Cache-busting aset CSS/JS (hash isi file di ?v=) dikerjakan saat menyusun dist/ oleh scripts/stamp_assets.py."""
import pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
FONT = ('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800'
        '&amp;family=JetBrains+Mono:wght@400;500;700&amp;display=swap')
BLOCK = (f'<link as="style" data-perf="font" href="{FONT}" rel="preload"/>'
         f'<link data-perf="font" href="{FONT}" media="print" onload="this.media=\'all\'" rel="stylesheet"/>'
         f'<noscript><link href="{FONT}" rel="stylesheet"/></noscript>')
PRE = '<link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>'
SKIP = {'dist', 'leads', 'outreach', 'ops', 'design', 'partials', 'node_modules', '.claude', '.git', '.wrangler'}
LINK = re.compile(r'<link(?![^>]*data-perf)(?=[^>]*rel="stylesheet")[^>]*href="https://fonts\.googleapis\.com/css2\?[^"]*"[^>]*/?>')


def fix(s):
    if 'data-perf="font"' in s:
        s2 = LINK.sub('', s)
    else:
        n = [0]

        def rep(m):
            n[0] += 1
            return BLOCK if n[0] == 1 else ''
        s2 = LINK.sub(rep, s)
    if 'fonts.googleapis.com/css2' in s2 and 'href="https://fonts.gstatic.com" rel="preconnect"' not in s2:
        s2 = s2.replace('<link as="style" data-perf="font"', PRE + '<link as="style" data-perf="font"', 1)
    return s2


def pages():
    for p in root.rglob('*.html'):
        if not SKIP.intersection(p.relative_to(root).parts):
            yield p


if __name__ == '__main__':
    changed = 0
    for p in pages():
        s = p.read_text(encoding='utf-8')
        t = fix(s)
        if t != s:
            p.write_text(t, encoding='utf-8')
            changed += 1
    print('apply_perf: font non-blocking di', changed, 'halaman')
