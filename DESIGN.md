---
version: 1.0
name: Altora-Indonesia-design-system
description: Design system Altora Indonesia (altora.id). Software house, CCTV, IoT, dan pengadaan untuk instansi dan bisnis di Kalimantan Timur. Tinta biru tua, satu aksen ungu, latar lavender sangat muda, gradien ungu-putih yang bergerak pelan sebagai penanda brand, dan Plus Jakarta Sans tebal dengan tracking rapat. Struktur dokumen ini mengikuti format DESIGN.md (referensi: analisis gaya Stripe dari getdesign.md), tetapi semua token dan aturan adalah milik Altora.

colors:
  primary: "#7C5CE8"          # aksen tunggal: tombol utama, link, titik eyebrow
  primary-hover: "#6A4AD6"
  primary-deep: "#5B3FC4"     # teks aksen, kicker, ikon aktif
  primary-press: "#4A31A8"
  primary-ink: "#3E2A97"      # bingkai tegas, angka di atas gradien
  primary-tint: "#F3F0FD"     # latar ikon, chip lembut
  primary-tint-2: "#F1EDFD"   # penanda menu aktif
  accent-magenta: "#C05BD0"   # HANYA di ujung gradien teks judul
  glow: "#FFE7A3"             # jendela menyala / sorotan ilustrasi, bukan warna UI
  whatsapp: "#16A34A"         # hanya untuk tautan/tombol WhatsApp
  ink: "#10224F"              # semua judul dan teks utama
  ink-secondary: "#2A2F5E"
  ink-mute: "#5A6785"         # paragraf, keterangan
  on-primary: "#FFFFFF"
  canvas: "#FBF9FE"           # latar halaman
  surface: "#FFFFFF"          # kartu
  surface-soft: "#F7F5FD"     # chip, pita lembut
  hairline: "#E9E5F6"         # border 1px kartu & pemisah
  hairline-strong: "#E4DEFA"  # border tombol putih, chip
  gradient-flow: "linear-gradient(115deg,#A98BFF 0%,#D6C8FF 22%,#FFFFFF 45%,#EEE6FF 62%,#BBA2FF 82%,#A98BFF 100%)"
  gradient-title: "linear-gradient(90deg,#7C5CE8,#C05BD0)"

typography:
  font: "'Plus Jakarta Sans', system-ui, sans-serif"   # Google Fonts, bobot 400–800
  mono: "'JetBrains Mono', ui-monospace, monospace"     # hanya label teknis/data kecil
  display-xxl: { size: "clamp(2.3rem, 1.6rem + 2.6vw, 4rem)", weight: 800, lineHeight: 1.02, letterSpacing: "-0.04em" }
  display-xl:  { size: "clamp(1.8rem, 1.3rem + 1.8vw, 3rem)", weight: 800, lineHeight: 1.06, letterSpacing: "-0.03em" }
  display-lg:  { size: "clamp(1.5rem, 1.2rem + 1.1vw, 2.1rem)", weight: 800, lineHeight: 1.15, letterSpacing: "-0.02em" }
  heading-md:  { size: "1.05rem", weight: 800, lineHeight: 1.3, letterSpacing: "-0.01em" }
  body-lg:     { size: "1.05rem", weight: 400, lineHeight: 1.7 }
  body-md:     { size: "0.9rem", weight: 400, lineHeight: 1.6 }
  eyebrow:     { size: "0.8125rem", weight: 700, letterSpacing: "0.01em", transform: none }
  button:      { size: "0.95rem", weight: 800 }
  numeric:     { weight: 800, fontVariantNumeric: tabular-nums }

rounded:
  sm: 8px      # tag kecil
  md: 12px     # input, chip kotak
  lg: 18px     # kartu standar
  xl: 24px     # panel besar, CTA, FAQ
  pill: 999px  # semua tombol, chip, menu

spacing:
  base: 8px
  card-padding: "22px – 36px"
  section: "clamp(56px, 7vw, 96px)"
  container: "min(1200px, 100% - 40px)"
  gutter-mobile: 16px

shadow:
  level-1: "0 14px 34px -24px rgba(43,30,110,.25)"   # kartu
  level-2: "0 18px 40px -24px rgba(43,30,110,.35)"   # hover kartu, mockup
  cta: "0 10px 24px -10px rgba(124,92,232,.8)"       # tombol ungu
  glow: "0 18px 40px rgba(91,63,196,.12)"            # panel gradien

components:
  button-primary:   { bg: "{colors.primary}", text: "{colors.on-primary}", rounded: "{rounded.pill}", minHeight: 46px, padding: "0 26px", shadow: "{shadow.cta}", hover: "{colors.primary-hover}" }
  button-white:     { bg: "{colors.surface}", text: "{colors.ink}", border: "1px {colors.hairline-strong}", rounded: "{rounded.pill}" }
  button-whatsapp:  { text: "{colors.whatsapp}", note: "tautan teks/tombol hijau, hanya untuk WhatsApp" }
  nav-floating:     { bg: "rgba(255,255,255,.72)", rounded: "{rounded.pill}", sticky: "top 18px", active: "bg {colors.primary-tint-2}, text {colors.primary-deep}, tanpa border" }
  eyebrow:          { text: "{colors.primary-deep}", dot: "8px {colors.primary}", typography: "{typography.eyebrow}" }
  card:             { bg: "{colors.surface}", border: "1px {colors.hairline}", rounded: "{rounded.lg}", padding: 22px, shadow: "{shadow.level-1}", hover: "border #CFC3F7 + {shadow.level-2} + translateY(-2px)" }
  icon-tile:        { size: 42px, rounded: 12px, bg: "{colors.primary-tint}", icon: "{colors.primary}" }
  chip:             { bg: "{colors.surface-soft}", text: "#41466A", rounded: "{rounded.pill}", size: "0.74rem / 600" }
  stats-card:       { bg: "{colors.surface}", border: "1px {colors.hairline}", dividers: "1px {colors.hairline}", number: "{colors.ink} {typography.numeric}", label: "{colors.ink-mute}" }
  cta-panel:        { bg: "{colors.gradient-flow}", backgroundSize: "300% 300%", animation: "16s ease-in-out infinite", text: "{colors.ink}", rounded: "{rounded.xl}", border: "1px #fff", shadow: "{shadow.glow}" }
  footer:           { bg: "{colors.gradient-flow}", animation: "16s", rounded: "32px 32px 0 0", text: "{colors.ink-secondary}" }
  faq-item:         { bg: "{colors.surface}", border: "1px {colors.hairline}", rounded: "{rounded.lg}", icon: "{components.icon-tile}" }
---

## Overview

Altora terlihat **tenang, terpercaya, dan teknis tanpa dingin**. Halaman berdiri di atas latar lavender sangat muda (`{colors.canvas}`), konten tinggal di kartu putih dengan border tipis, dan semua penekanan memakai **satu warna aksen: ungu** (`{colors.primary}`). Penanda brand yang paling mudah dikenali adalah **gradien ungu–putih yang bergerak pelan** (`{colors.gradient-flow}`) di footer dan panel ajakan (CTA), serta judul besar Plus Jakarta Sans 800 dengan tracking rapat, yang baris terakhirnya sering diberi gradien ungu ke magenta.

Prinsip yang diadaptasi dari referensi Stripe dan disesuaikan untuk Altora:
- **Satu tombol penuh per bagian.** Tombol ungu terisi hanya satu di setiap blok; aksi kedua memakai tombol putih atau tautan.
- **Gradien sebagai kedalaman.** Altora tidak memakai mesh multi-warna, melainkan satu gradien ungu–putih yang bergerak pelan. Bayangan tetap tipis.
- **Angka tabular.** Angka statistik (2019, 50+, 13, 3) memakai `font-variant-numeric: tabular-nums`.
- **Bukti lewat tampilan produk.** Fitur dijelaskan dengan mockup tampilan aplikasi atau foto lapangan asli, bukan ilustrasi abstrak.

**Ciri utama:**
- Tinta `{colors.ink}` biru tua untuk judul dan teks, tidak pernah hitam murni.
- Ungu hanya untuk tombol, tautan, titik eyebrow, ikon, dan penanda aktif. Bukan untuk paragraf.
- Kartu putih, border `{colors.hairline}`, radius 18–24px, bayangan sangat lembut.
- Semua tombol dan chip berbentuk pil (`{rounded.pill}`).
- Maskot Altora (staf berseragam putih dengan tablet) boleh tampil di hero beranda. Tidak memakai foto model stok lain.

## Colors

### Brand & aksen
- **Primary** `#7C5CE8`: tombol utama, tautan, titik eyebrow, ikon.
- **Primary deep** `#5B3FC4`: teks kicker/eyebrow, ikon aktif, judul kecil berwarna.
- **Primary ink** `#3E2A97`: bingkai tegas dan teks di atas gradien.
- **Primary tint** `#F3F0FD` / `#F1EDFD`: latar ikon dan penanda menu aktif.
- **Magenta** `#C05BD0`: hanya sebagai ujung gradien judul (`{colors.gradient-title}`).
- **Hijau WhatsApp** `#16A34A`: hanya untuk tautan dan tombol WhatsApp.
- **Glow** `#FFE7A3`: hanya untuk ilustrasi (jendela gedung menyala), bukan warna UI.

### Permukaan & teks
- **Canvas** `#FBF9FE`: latar halaman. **Surface** `#FFFFFF`: kartu. **Surface soft** `#F7F5FD`: chip dan pita lembut.
- **Hairline** `#E9E5F6`: border kartu. **Hairline strong** `#E4DEFA`: border tombol putih dan chip.
- **Ink** `#10224F`: judul. **Ink secondary** `#2A2F5E`: teks di footer/gradien. **Ink mute** `#5A6785`: paragraf.

### Larangan warna
Jangan memakai lagi warna aksen lain (hijau, biru, oranye, pink) untuk kartu layanan atau ikon. Dulu beranda memakai lima warna dan terlihat tambal sulam. Jangan memakai pita latar krem atau hijau di antara section.

## Typography

**Plus Jakarta Sans** (Google Fonts, 400–800) untuk semua teks. **JetBrains Mono** hanya untuk label teknis kecil di mockup dashboard.

| Token | Ukuran | Bobot | Line height | Tracking | Pemakaian |
|---|---|---|---|---|---|
| display-xxl | clamp(2.3rem → 4rem) | 800 | 1.02 | -0.04em | Judul hero |
| display-xl | clamp(1.8rem → 3rem) | 800 | 1.06 | -0.03em | Judul section |
| display-lg | clamp(1.5rem → 2.1rem) | 800 | 1.15 | -0.02em | Judul blok |
| heading-md | 1.05rem | 800 | 1.3 | -0.01em | Judul kartu |
| body-lg | 1.05rem | 400 | 1.7 | 0 | Lead paragraf |
| body-md | 0.9rem | 400 | 1.6 | 0 | Isi kartu |
| eyebrow | 0.8125rem | 700 | — | 0.01em | Label di atas judul (dengan titik ungu) |

Prinsip:
- Judul selalu tebal (800) dengan tracking negatif. Ini kebalikan Stripe yang tipis; ketebalan adalah suara Altora.
- Satu baris judul boleh memakai `{colors.gradient-title}` (misalnya "instansi di Kaltim."). Maksimal satu per halaman.
- Eyebrow tidak memakai huruf kapital semua.
- Bahasa Indonesia yang jelas dan langsung. Hindari istilah Inggris kalau ada padanan yang umum ("Integrasi sistem", bukan "System Integration").

## Layout

- Kontainer `min(1200px, 100% - 40px)`, gutter HP 16px, tanpa scroll horizontal.
- Jarak section `clamp(56px, 7vw, 96px)`; padding kartu 22–36px.
- Grid kartu 4 → 2 → 1 kolom pada 1080px dan 560px.
- Latar semua section sama (`{colors.canvas}`). Pemisahan bagian memakai kartu dan jarak, bukan pita warna.
- Hero: latar gradien lembut yang diteruskan sampai ke balik menu sticky (tidak boleh ada pita warna berbeda di atas).

## Elevation & Depth

| Level | Nilai | Pemakaian |
|---|---|---|
| 0 | datar | Latar halaman |
| 1 | `{shadow.level-1}` | Kartu |
| 2 | `{shadow.level-2}` | Kartu saat hover, mockup dashboard |
| Gradien | `{colors.gradient-flow}` bergerak 16s | Footer dan panel CTA. Inilah kedalaman utama brand |

Hormati `prefers-reduced-motion`: semua gradien bergerak dan animasi berhenti.

## Shapes

- Radius: tag 8px, input/chip kotak 12px, kartu 18px, panel 24px, footer `32px 32px 0 0`, tombol dan chip `999px`.
- Ikon garis (stroke) di dalam ubin 42px berwarna `{colors.primary-tint}`.
- Foto: foto lapangan asli (pemasangan CCTV, kios, jaringan) atau mockup aplikasi. Gambar ilustrasi produk ditandai sebagai ilustrasi.

## Components

- **Tombol utama** (`button-primary`): ungu terisi, teks putih 800, pil, tinggi minimum 46px, bayangan `{shadow.cta}`.
- **Tombol putih** (`button-white`): latar putih, border `{colors.hairline-strong}`, teks ink. Untuk aksi kedua.
- **Menu atas** (`nav-floating`): pil putih transparan, sticky 18px dari atas. Urutan: Layanan, Produk, Katalog, Portofolio, Artikel, Tentang, Karier, Support, lalu tombol "Konsultasi". Penanda aktif: latar `{colors.primary-tint-2}` tanpa border.
- **Kartu layanan** (`card` + `icon-tile` + `chip`): ikon ungu, judul 800, deskripsi, 3–4 chip, tautan "Pelajari →" di bawah.
- **Kotak angka** (`stats-card`): kartu putih dengan pembatas tipis, angka biru tua tabular. Bukan blok ungu pekat.
- **Panel CTA** (`cta-panel`): gradien bergerak, teks gelap, isi di tengah, satu tombol ungu dan satu tombol putih. Tanpa garis putih ganda di dalam panel.
- **FAQ** (`faq-item`): satu kolom, ikon satu warna, akordeon.
- **Footer**: gradien bergerak, empat kolom (Layanan, Produk, Perusahaan, Kontak) plus tiga kantor.
- **Keranjang**: tombol "Tambah ke keranjang", lalu dikirim lewat WhatsApp. Tanpa harga.

## Do's and Don'ts

### Do
- Pakai satu aksen ungu dan satu tombol ungu terisi per section.
- Tulis semua teks di HTML (bukan dibangkitkan JavaScript) supaya terbaca Google.
- Pakai foto proyek asli dan mockup aplikasi sebagai bukti.
- Arahkan semua pembahasan biaya ke chat WhatsApp.
- Uji di 375px dan 1440px. Tidak boleh ada teks terpotong atau scroll horizontal.

### Don't
- **Jangan menampilkan harga, ongkos, tarif, RAB, atau pembahasan biaya** di halaman mana pun.
- **Jangan mengklaim klien, partner, atau proyek yang tidak nyata.** Starlink bukan partner (Altora membeli dan memasangnya sendiri). Hanya cantumkan klien yang sudah dikonfirmasi.
- Jangan membuat statistik, testimoni, atau angka hasil tanpa sumber.
- Jangan memakai foto model stok selain maskot Altora di hero beranda.
- Jangan memakai blok gradien ungu pekat dengan teks putih untuk kartu besar. Hasilnya terlalu "jreng".
- Jangan menambah warna aksen baru atau pita latar berwarna antar-section.
- Jangan menjanjikan teknisi datang ke lokasi di luar Kalimantan Timur.

## Responsive Behavior

| Nama | Lebar | Perubahan |
|---|---|---|
| Desktop | ≥ 1080px | Grid 4 kolom, hero 2 kolom (teks + dashboard/maskot) |
| Tablet | 760–1079px | Grid 2 kolom, menu masih satu baris sampai 1024px |
| HP | < 760px | Grid 1 kolom, menu burger, hero satu kolom tanpa ilustrasi kanan, tombol selebar layar |

- Target sentuh minimal 44px.
- Judul turun bertahap lewat `clamp()`, tidak dengan lompatan breakpoint.

## Agent Prompt Guide

Saat membuat atau mengubah halaman Altora:
1. Mulai dari token di atas. Jangan membuat warna atau radius baru.
2. Struktur halaman: eyebrow → judul 800 → lead → konten kartu → panel CTA gradien.
3. Kartu: putih, border hairline, radius 18px, ikon di ubin ungu muda.
4. Satu tombol ungu terisi per section; tombol kedua putih.
5. Teks bahasa Indonesia, tanpa harga, tanpa klaim palsu.
6. Setelah selesai, cek 375px dan 1440px, lalu pastikan tidak ada tautan rusak.
