#!/bin/sh
# Bangun ulang seluruh halaman yang digenerate, dengan urutan yang benar.
# build_produk menulis ulang produk.html, build_area menulis ulang area-layanan.html;
# build_produk_kota dan build_trust menyisipkan blok ke halaman itu, jadi harus jalan sesudahnya.
set -e
cd "$(dirname "$0")/.."
python3 scripts/build_services.py
python3 scripts/build_careers.py
python3 scripts/build_blog.py
python3 scripts/build_local.py
python3 scripts/build_area.py
python3 scripts/build_produk.py
python3 scripts/build_vigi.py
python3 scripts/build_apps.py
python3 scripts/build_industri.py
python3 scripts/build_produk_kota.py
python3 scripts/build_about.py
python3 scripts/build_trust.py
python3 scripts/apply_shell.py
python3 scripts/apply_seo.py
