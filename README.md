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
index.html              # beranda — markup + sprite ikon SVG
login.html              # halaman masuk, pemilih modul
assets/css/styles.css   # design token, layout, dan breakpoint
assets/css/login.css    # layout khusus halaman masuk
assets/js/modules.js    # daftar 8 modul Altora (dipakai dua halaman)
assets/js/main.js       # data section beranda + interaksi
assets/js/login.js      # render pemilih modul + filter
assets/js/login-modal.js # modal pemilih modul di beranda
assets/img/             # logo dan foto mascot (WebP, transparan)
```

## Mengubah konten

Isi section Modul, Industri, Alur Kerja, Paket, dan FAQ didefinisikan sebagai
array di bagian atas [`assets/js/main.js`](assets/js/main.js) dan dirender ke
DOM saat load. Menambah atau mengubah satu entri di situ otomatis mengubah
kartu yang tampil — tidak perlu menyentuh markup.

Section lain (hero, problem, CTA, footer) ditulis langsung di `index.html`.

## Halaman masuk

`login.html` tidak meminta email atau password. Tiap modul Altora berjalan di
subdomainnya sendiri dan punya form masuk masing-masing, jadi halaman ini
berperan sebagai pemilih: pengguna memilih modul, lalu diarahkan ke
`https://<modul>.altora.my.id`.

Daftar modul beserta subdomainnya ada di
[`assets/js/modules.js`](assets/js/modules.js) — file yang sama juga mengisi
kartu industri di beranda, jadi menambah modul baru cukup di satu tempat.
Kalau alamat masuknya bukan root subdomain, sesuaikan `href` di
[`assets/js/login.js`](assets/js/login.js) dan
[`assets/js/login-modal.js`](assets/js/login-modal.js).

Di beranda, tombol Login tetap sebuah `<a href="login.html">`, lalu
`login-modal.js` mencegat klik biasa dan menampilkan pilihan yang sama dalam
modal. Jadi tautannya tetap bisa di-bookmark, bisa dibuka di tab baru, dan
halaman tetap berfungsi kalau skripnya gagal dimuat.

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
