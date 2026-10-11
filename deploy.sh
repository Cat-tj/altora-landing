#!/usr/bin/env bash
# Deploy landing statis ke origin altora.id (Raspberry Pi: /home/pi/altora-landing).
# Pakai:  HOST=pi@<ip-rpi> ./deploy.sh        -> dry-run, hanya menampilkan rencana
#         HOST=pi@<ip-rpi> ./deploy.sh --go   -> benar-benar upload
# File internal (leads, outreach, script, catatan) TIDAK ikut dan dihapus dari server.
set -euo pipefail
HOST="${HOST:?Set HOST, contoh: HOST=pi@HOST_IP ./deploy.sh}"
DEST="${DEST:-/home/pi/altora-landing/}"
DRY="-n"; [[ "${1:-}" == "--go" ]] && DRY=""
rsync -avz $DRY --delete --delete-excluded \
  --exclude='.git/' --exclude='.claude/' --exclude='.DS_Store' \
  --exclude='leads/' --exclude='partials/' --exclude='ops/' --exclude='content/' --exclude='outreach/' --exclude='scripts/' --exclude='design/' \
  --exclude='*.md' --exclude='*.py' --exclude='*.tmp' --exclude='*.sh' --exclude='_redirects' \
  ./ "$HOST:$DEST"
[[ -n "$DRY" ]] && echo ">> Dry-run selesai. Jalankan './deploy.sh --go' untuk upload."
