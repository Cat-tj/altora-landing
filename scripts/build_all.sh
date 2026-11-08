#!/bin/sh
# Bangun ulang seluruh halaman yang digenerate, dengan urutan yang benar.
# build_area menulis ulang area-layanan.html; build_trust menyisipkan blok ke beranda.
set -e
cd "$(dirname "$0")/.."
python3 scripts/build_services.py
python3 scripts/build_services_hub.py
python3 scripts/build_careers.py
python3 scripts/build_blog.py
python3 scripts/build_local.py
python3 scripts/build_area.py
python3 scripts/build_industri.py
python3 scripts/build_aplikasi.py
python3 scripts/build_app_seo.py
python3 scripts/build_about.py
python3 scripts/build_support.py
python3 scripts/build_trust.py
python3 scripts/build_gedung.py
python3 scripts/purge_removed.py services.html algora.html 404.html jasa-pembuatan-software-samarinda.html
python3 scripts/apply_shell.py
python3 scripts/apply_stage.py
python3 scripts/apply_motion.py
python3 scripts/apply_seo.py
python3 scripts/apply_schema.py
python3 scripts/purge_removed.py --images
python3 scripts/clean_sitemap.py