"""Tulis partials/footer.html ke semua halaman publik (ganti <footer> lama).
Jalankan dari root repo:  python3 scripts/apply_footer.py"""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
footer = (root / 'partials/footer.html').read_text(encoding='utf-8').strip()
skip = ('id/', 'leads/', 'outreach/', 'design/', 'partials/')
changed = 0
for f in sorted(root.rglob('*.html')):
    rel = f.relative_to(root).as_posix()
    if rel.startswith(skip) or rel.startswith('google'):
        continue
    s = f.read_text(encoding='utf-8')
    new, n = re.subn(r'<footer\b.*?</footer>', lambda _: footer, s, count=1, flags=re.S)
    if n == 0:
        new = s.replace('</main>', '</main>' + footer, 1)
    if new != s:
        f.write_text(new, encoding='utf-8'); changed += 1
print(f'footer diterapkan ke {changed} halaman')
