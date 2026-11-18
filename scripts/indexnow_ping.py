"""Kirim URL yang berubah ke IndexNow (Bing, Yandex, Seznam, Naver; dipakai juga oleh Copilot dan ChatGPT search).

Cara kerja: baca sitemap.xml (loc + lastmod), bandingkan dengan state terakhir yang berhasil dikirim
(scripts/.indexnow_state.json, tidak di-commit dan tidak ikut dist/), lalu kirim hanya URL yang baru atau lastmod-nya berubah.
State baru disimpan hanya bila API menjawab 200/202, jadi pengiriman yang gagal akan diulang di pemanggilan berikutnya.

Pakai (dari root repo, SETELAH situs ter-deploy, karena mesin pencari langsung mengambil URL dan file kunci):
    python3 scripts/indexnow_ping.py              # kirim URL yang berubah sejak pengiriman terakhir
    python3 scripts/indexnow_ping.py --all        # kirim semua URL di sitemap.xml
    python3 scripts/indexnow_ping.py --dry-run    # tampilkan saja URL yang akan dikirim, tanpa memanggil API
    python3 scripts/indexnow_ping.py --urls /about /blog/xxx   # kirim URL tertentu (path atau URL lengkap)
    python3 scripts/indexnow_ping.py --mark-only  # simpan state dari sitemap sekarang tanpa mengirim apa pun
deploy.sh --go menjalankan skrip ini otomatis setelah deploy produksi berhasil.

Kunci: file <KEY>.txt di root situs (https://altora.id/<KEY>.txt) berisi kunci yang sama. Jangan dihapus;
kalau kunci diganti, ganti KEY di bawah dan nama/isi file kunci bersamaan.
"""
import argparse, json, pathlib, re, sys, urllib.error, urllib.request

KEY = '2ac47fce9c55d6153288346c1b868c41'
SITE = 'https://altora.id'
HOST = 'altora.id'
ENDPOINT = 'https://api.indexnow.org/indexnow'
BATCH = 10000  # batas IndexNow per permintaan

root = pathlib.Path(__file__).resolve().parent.parent
SITEMAP = root / 'sitemap.xml'
STATE = pathlib.Path(__file__).resolve().parent / '.indexnow_state.json'
KEY_FILE = root / f'{KEY}.txt'


def sitemap_entries():
    t = SITEMAP.read_text(encoding='utf-8')
    out = {}
    for block in re.findall(r'<url>(.*?)</url>', t, re.S):
        loc = re.search(r'<loc>([^<]+)</loc>', block)
        if not loc:
            continue
        lm = re.search(r'<lastmod>([^<]+)</lastmod>', block)
        out[loc.group(1).strip()] = lm.group(1).strip() if lm else ''
    return out


def load_state():
    try:
        return json.loads(STATE.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        return None


def save_state(entries):
    STATE.write_text(json.dumps(dict(sorted(entries.items())), indent=1, ensure_ascii=False) + '\n', encoding='utf-8')


def absolute(u):
    if u.startswith('http'):
        return u
    return SITE + ('' if u.startswith('/') else '/') + u


def submit(urls):
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'{SITE}/{KEY}.txt', 'urlList': chunk}).encode()
        req = urllib.request.Request(ENDPOINT, data=body, method='POST',
                                     headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                code = r.status
        except urllib.error.HTTPError as err:
            code = err.code
        except urllib.error.URLError as err:
            print(f'IndexNow: gagal terhubung ({err.reason})', file=sys.stderr)
            return False
        # 200 OK, 202 Accepted (kunci sedang divalidasi). 403 = kunci tidak cocok/belum ter-deploy, 422 = URL bukan milik host.
        print(f'IndexNow: {len(chunk)} URL -> HTTP {code}')
        if code not in (200, 202):
            return False
    return True


def main():
    ap = argparse.ArgumentParser(description='Kirim URL altora.id yang berubah ke IndexNow.')
    ap.add_argument('--all', action='store_true', help='kirim semua URL di sitemap.xml')
    ap.add_argument('--dry-run', action='store_true', help='tampilkan URL tanpa mengirim')
    ap.add_argument('--mark-only', action='store_true', help='simpan state sitemap sekarang tanpa mengirim')
    ap.add_argument('--urls', nargs='+', help='kirim URL tertentu saja (path atau URL lengkap)')
    a = ap.parse_args()

    if not KEY_FILE.exists() or KEY_FILE.read_text(encoding='utf-8').strip() != KEY:
        raise SystemExit(f'File kunci {KEY_FILE.name} tidak ada atau isinya tidak sama dengan KEY.')
    entries = sitemap_entries()
    if a.mark_only:
        save_state(entries)
        print(f'State disimpan ({len(entries)} URL), tidak ada yang dikirim.')
        return
    if a.urls:
        urls = [absolute(u) for u in a.urls]
    elif a.all:
        urls = list(entries)
    else:
        prev = load_state()
        if prev is None:
            print('Belum ada state pengiriman sebelumnya: semua URL di sitemap dianggap berubah.')
            prev = {}
        urls = [u for u, lm in entries.items() if prev.get(u) != lm]
    bad = [u for u in urls if not u.startswith(SITE + '/')]
    if bad:
        raise SystemExit('URL di luar ' + SITE + ': ' + ', '.join(bad))
    if not urls:
        print('IndexNow: tidak ada URL yang berubah sejak pengiriman terakhir.')
        return
    print(f'IndexNow: {len(urls)} URL' + (' (dry-run)' if a.dry_run else ''))
    for u in urls[:50]:
        print('  ' + u)
    if len(urls) > 50:
        print(f'  ... dan {len(urls) - 50} lainnya')
    if a.dry_run:
        return
    if not submit(urls):
        raise SystemExit(1)
    if not a.urls:  # pengiriman sebagian (--urls) tidak menggeser state
        save_state(entries)


if __name__ == '__main__':
    main()
