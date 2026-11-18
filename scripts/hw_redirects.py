"""Alihan 301 untuk halaman perangkat per kota di luar Samarinda (CCTV, IT support, smart lock hanya melayani Samarinda).
Menulis blok bertanda di _redirects (Cloudflare Pages) secara eksplisit per URL, karena aturan wildcard akan ikut menangkap
halaman Samarinda. Juga menghapus file HTML kota lain yang tersisa. Aman dijalankan berulang (dipanggil build_all.sh)."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_area import CITIES, is_nasional

root = pathlib.Path(__file__).resolve().parent.parent
FAMILIES = [('jasa-pasang-cctv-', '/services/cctv', False), ('it-support-', '/services/it-support', False),
            ('jual-cctv-', '/pengadaan', True), ('cctv-tenaga-surya-', '/services/cctv', True), ('jual-smartlock-', '/services/smart-lock', True)]
lines, removed = [], 0
for prefix, target, nasional_too in FAMILIES:
    for k in CITIES:
        if k == 'samarinda' or (is_nasional(k) and not nasional_too):
            continue
        lines.append(f'/{prefix}{k}    {target}    301')
        f = root / f'{prefix}{k}.html'
        if f.exists():
            f.unlink(); removed += 1
block = '# perangkat-kota:start (scripts/hw_redirects.py)\n' + '\n'.join(lines) + '\n# perangkat-kota:end\n'
p = root / '_redirects'
s = p.read_text(encoding='utf-8')
s = re.sub(r'# perangkat-kota:start.*?# perangkat-kota:end\n', '', s, flags=re.S)
# ditaruh paling atas: aturan statis sebelum aturan wildcard
p.write_text(block + s.lstrip('\n'), encoding='utf-8')
print(f'alihan perangkat kota: {len(lines)} URL, {removed} file dihapus')
