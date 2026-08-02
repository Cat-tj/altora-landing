# Altora — Landing Page

Landing page untuk Altora, sistem manajemen bisnis terintegrasi (kasir, stok,
pembelian, keuangan) untuk berbagai jenis usaha retail dan jasa.

HTML/CSS/JS statis, tanpa build step dan tanpa dependency runtime.

## Menjalankan

```bash
python3 -m http.server 4321
```

Lalu buka <http://localhost:4321>.

## Struktur

```
index.html              # seluruh markup + sprite ikon SVG
assets/css/styles.css   # design token, layout, dan breakpoint
assets/js/main.js       # data section + interaksi
assets/img/             # logo dan foto mascot (WebP, transparan)
```

## Mengubah konten

Isi section Modul, Industri, Alur Kerja, Paket, dan FAQ didefinisikan sebagai
array di bagian atas [`assets/js/main.js`](assets/js/main.js) dan dirender ke
DOM saat load. Menambah atau mengubah satu entri di situ otomatis mengubah
kartu yang tampil — tidak perlu menyentuh markup.

Section lain (hero, problem, CTA, footer) ditulis langsung di `index.html`.

## Catatan aset

Foto mascot dipakai dalam versi yang sudah dipotong latarnya (alpha), lalu
dikonversi ke WebP dan di-crop ke area terlihat. Karena sudah transparan,
gambarnya bisa ditempatkan di atas kartu putih maupun panel berwarna tanpa
trik blend mode.

Dashboard di section hero dan Alur Kerja bukan screenshot — keduanya disusun
dari HTML/CSS supaya tetap tajam di layar retina dan mudah diperbarui.

## Referensi desain

`design/mockups/` berisi mockup tiap section yang jadi patokan implementasi.
`design/source/` berisi foto mascot versi asli (sudah tanpa latar) sebelum
di-crop dan dikonversi ke WebP di `assets/img/`.

Keduanya tidak ikut di-serve — hanya arsip untuk keperluan revisi.
