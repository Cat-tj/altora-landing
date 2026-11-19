#!/bin/sh
# Susun folder dist/ untuk Cloudflare Pages: isi sama dengan yang dikirim deploy.sh ke Pi (file internal tidak ikut),
# ditambah _redirects dan _headers. Rujukan CSS/JS di dist/ diberi ?v=<hash isi> (scripts/stamp_assets.py). functions/ dibaca wrangler dari akar repo, jadi tidak disalin ke dist/.
# Pakai:  sh scripts/build_pages.sh            -> hanya menyusun dist/
#         sh scripts/build_pages.sh --deploy   -> menyusun lalu deploy produksi (npx wrangler pages deploy)
set -e
cd "$(dirname "$0")/.."
rsync -a --delete --delete-excluded \
  --exclude='.git/' --exclude='.claude/' --exclude='.DS_Store' --exclude='dist/' --exclude='functions/' --exclude='node_modules/' \
  --exclude='leads/' --exclude='partials/' --exclude='ops/' --exclude='content/' --exclude='outreach/' --exclude='scripts/' --exclude='design/' \
  --exclude='*.md' --exclude='*.py' --exclude='*.tmp' --exclude='*.sh' --exclude='*.log' \
  ./ dist/
python3 scripts/stamp_assets.py dist
echo "dist/ siap: $(find dist -type f | wc -l | tr -d ' ') file, $(du -sh dist | cut -f1)"
if [ "${1:-}" = "--deploy" ]; then
  npx --yes wrangler pages deploy dist --project-name "${PAGES_PROJECT:-altora-landing}" --branch "${PAGES_BRANCH:-main}" --commit-dirty=true
fi
