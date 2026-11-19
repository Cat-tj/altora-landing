#!/usr/bin/env bash
# Deploy altora.id. Sejak 2026-10-28 situs dilayani Cloudflare Pages (proyek altora-landing).
# Pakai:  ./deploy.sh --go                          -> susun dist/, deploy produksi ke Cloudflare Pages, lalu ping IndexNow
#         ./deploy.sh                               -> hanya menyusun dist/ (tanpa upload)
#         TARGET=pi HOST=pi@<ip> ./deploy.sh --go   -> cadangan lama: rsync ke Raspberry Pi (/home/pi/altora-landing)
# File internal (leads, outreach, script, catatan) TIDAK ikut. Untuk rsync ke Pi: semua yang tidak ada di repo
# DIHAPUS dari DEST, jadi simpan backup di luar DEST (mis. /home/pi/altora-landing-backups/).
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${TARGET:-pages}" != "pi" ]]; then
  if [[ "${1:-}" == "--go" ]]; then
    sh scripts/build_pages.sh --deploy
    # Deploy produksi berhasil (set -e): kabari IndexNow soal URL yang berubah. Gagal ping tidak menggagalkan deploy;
    # ulangi manual dengan 'python3 scripts/indexnow_ping.py'. Hanya untuk produksi (PAGES_BRANCH main); lewati dengan INDEXNOW=0
    if [[ "${INDEXNOW:-1}" != "0" && "${PAGES_BRANCH:-main}" == "main" ]]; then python3 scripts/indexnow_ping.py || echo ">> IndexNow gagal; jalankan ulang: python3 scripts/indexnow_ping.py"; fi
  else sh scripts/build_pages.sh; echo ">> dist/ siap. Jalankan './deploy.sh --go' untuk deploy ke Cloudflare Pages."; fi
  exit 0
fi
HOST="${HOST:?Set HOST, contoh: TARGET=pi HOST=pi@HOST_IP ./deploy.sh --go}"
DEST="${DEST:-/home/pi/altora-landing/}"
DRY="-n"; [[ "${1:-}" == "--go" ]] && DRY=""
rsync -avz $DRY --delete --delete-excluded \
  --exclude='.git/' --exclude='.claude/' --exclude='.DS_Store' --exclude='dist/' --exclude='functions/' --exclude='_headers' \
  --exclude='leads/' --exclude='partials/' --exclude='ops/' --exclude='content/' --exclude='outreach/' --exclude='scripts/' --exclude='design/' \
  --exclude='*.md' --exclude='*.py' --exclude='*.tmp' --exclude='*.sh' --exclude='_redirects' \
  ./ "$HOST:$DEST"
[[ -n "$DRY" ]] && echo ">> Dry-run selesai. Jalankan './deploy.sh --go' untuk upload."
