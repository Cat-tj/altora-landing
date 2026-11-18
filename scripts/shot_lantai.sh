#!/bin/bash
# Tangkapan layar asli 8 halaman lantai (semua kecuali Beranda) untuk layar di gedung 3D: assets/img/lantai/<halaman>-<lebar>.webp
# Lebar 390/820/1440/1920 px CSS; gedung3d.js memilih yang paling dekat dengan lebar layar pengunjung dan memasangnya pas lebar.
# Butuh server lokal di port 4321 dan Google Chrome. Jalankan ulang bila tampilan halaman berubah.
set -e
cd "$(dirname "$0")/.."
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=assets/img/lantai; TMP=$(mktemp -d); mkdir -p "$OUT"; rm -f "$OUT"/*.webp
MOB="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
shot() {  # halaman lebar tinggi skala lebar-keluaran [ua]
  "$CH" --headless=new --user-data-dir="$TMP/u" --hide-scrollbars --virtual-time-budget=6000 --window-size=$2,$3 --force-device-scale-factor=$4 \
    ${6:+--user-agent="$6"} --screenshot="$TMP/s.png" "http://localhost:4321/$1.html" 2>/dev/null
  cwebp -quiet -q 72 -resize $5 0 "$TMP/s.png" -o "$OUT/$1-$2.webp"
}
for p in services pengadaan aplikasi portofolio blog about careers support; do
  shot $p 390 1000 2 585 "$MOB"
  shot $p 820 1300 1 820
  shot $p 1440 1100 1 1280
  shot $p 1920 1300 1 1600
done
rm -rf "$TMP"
du -ch "$OUT"/*.webp | tail -1
