#!/bin/bash
# Tangkapan layar asli 8 halaman lantai untuk layar di gedung 3D (assets/img/lantai/<halaman>-d.webp & -m.webp).
# Butuh server lokal di port 4321 (python3 -m http.server 4321) dan Google Chrome. Jalankan ulang bila tampilan halaman berubah.
set -e
cd "$(dirname "$0")/.."
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=assets/img/lantai; TMP=$(mktemp -d); mkdir -p "$OUT"
for p in careers services produk portfolio blog about katalog support; do
  "$CH" --headless=new --user-data-dir="$TMP/u" --hide-scrollbars --virtual-time-budget=6000 --window-size=1440,900 \
    --screenshot="$TMP/$p-d.png" "http://localhost:4321/$p.html" 2>/dev/null
  "$CH" --headless=new --user-data-dir="$TMP/u" --hide-scrollbars --virtual-time-budget=6000 --window-size=390,844 --force-device-scale-factor=2 \
    --user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" \
    --screenshot="$TMP/$p-m.png" "http://localhost:4321/$p.html" 2>/dev/null
  cwebp -quiet -q 72 -resize 1280 0 "$TMP/$p-d.png" -o "$OUT/$p-d.webp"
  cwebp -quiet -q 72 -resize 585 0 "$TMP/$p-m.png" -o "$OUT/$p-m.webp"
done
rm -rf "$TMP"
ls -la "$OUT"
