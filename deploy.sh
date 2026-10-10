#!/usr/bin/env bash
# Deploy landing statis ke VPS (Caddy: /srv/altora-landing).
# Pakai:  ./deploy.sh          -> dry-run, hanya menampilkan rencana
#         ./deploy.sh --go     -> benar-benar upload
# File internal (leads, outreach, script, catatan) TIDAK ikut dan dihapus dari server.
set -euo pipefail
HOST="${HOST:-root@103.92.215.166}"
DEST="${DEST:-/srv/altora-landing/}"
DRY="-n"; [[ "${1:-}" == "--go" ]] && DRY=""
rsync -avz $DRY --delete --delete-excluded \
  --exclude='.git/' --exclude='.claude/' --exclude='.DS_Store' \
  --exclude='leads/' --exclude='partials/' --exclude='outreach/' --exclude='scripts/' --exclude='design/' \
  --exclude='*.md' --exclude='*.py' --exclude='*.tmp' --exclude='*.sh' --exclude='_redirects' \
  ./ "$HOST:$DEST"
[[ -n "$DRY" ]] && echo ">> Dry-run selesai. Jalankan './deploy.sh --go' untuk upload."
