"""Buang entri sitemap.xml yang file halamannya sudah tidak ada. Jalankan terakhir di build_all.sh."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
sm = root / 'sitemap.xml'; s = sm.read_text(encoding='utf-8')
def exists(path):
    p = path.strip('/')
    return path in ('', '/') or (root / (p + '.html')).exists() or (root / p / 'index.html').exists() or (root / p).is_file()
removed = []
def keep(m):
    loc = re.search(r'<loc>https://altora\.id([^<]*)</loc>', m.group(0))
    if loc and not exists(loc.group(1)):
        removed.append(loc.group(1)); return ''
    return m.group(0)
s = re.sub(r'\s*<url>.*?</url>', keep, s, flags=re.S)
sm.write_text(s, encoding='utf-8')
print(f'sitemap: {len(removed)} entri dibuang, {len(re.findall("<loc>", s))} tersisa')
