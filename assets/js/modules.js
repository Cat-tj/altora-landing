/* ============================================================
   ALTORA — daftar modul
   Sumber tunggal untuk section "Wajah Altora" di beranda dan
   pemilih modul di halaman masuk.
   ============================================================ */
window.ALTORA_MODULES = [
  { key: 'resto', name: 'Altora Resto', host: 'resto.altora.my.id',
    icon: 'i-coffee', tone: 'purple', hex: '#7C5CE8',
    short: 'Kelola resto & cafe lebih efisien, dari meja hingga dapur.',
    feats: ['Kasir & meja', 'Resep & bahan baku', 'Pesanan QR meja', 'Laporan penjualan'] },

  { key: 'market', name: 'Altora Market', host: 'market.altora.my.id',
    icon: 'i-cart', tone: 'green', hex: '#12A374',
    short: 'Solusi lengkap untuk minimarket & toko kelontong.',
    feats: ['Kasir POS', 'Stok real-time', 'Promo & diskon', 'Laporan & analitik'] },

  { key: 'supermarket', name: 'Altora Supermarket', host: 'supermarket.altora.my.id',
    icon: 'i-basket', tone: 'blue', hex: '#3B82F6',
    short: 'Kelola stok besar, grosir bertingkat, dan multi-outlet.',
    feats: ['Grosir & retail', 'Multi cabang', 'Purchase order', 'Transfer antar gudang'] },

  { key: 'laundry', name: 'Altora Laundry', host: 'laundry.altora.my.id',
    icon: 'i-washer', tone: 'cyan', hex: '#22B8CF',
    short: 'Kelola order kiloan, paket, cicilan, dan pengantaran.',
    feats: ['Order kiloan & satuan', 'Paket & harga', 'Pengantaran', 'Laporan keuangan'] },

  { key: 'counter', name: 'Altora Counter', host: 'counter.altora.my.id',
    icon: 'i-phone', tone: 'pink', hex: '#EC5B9E',
    short: 'Cocok untuk counter HP, servis, dan aksesoris.',
    feats: ['Servis & perbaikan', 'Aksesoris & stok', 'Stok sparepart', 'Garansi & nota servis'] },

  { key: 'jasa', name: 'Altora Jasa', host: 'jasa.altora.my.id',
    icon: 'i-scissors', tone: 'orange', hex: '#F59E0B',
    short: 'Untuk barbershop, salon, spa, dan berbagai jasa.',
    feats: ['Booking online', 'Jadwal & terapis', 'Membership', 'Laporan & komisi'] },

  { key: 'pabrik', name: 'Altora Pabrik', host: 'pabrik.altora.my.id',
    icon: 'i-factory', tone: 'navy', hex: '#3E4E7E',
    short: 'Kelola bahan baku, produksi, dan maintenance mesin.',
    feats: ['BOM & produksi', 'Bahan baku', 'QC & maintenance', 'Laporan produksi'] },

  { key: 'company', name: 'Altora Company', host: 'company.altora.my.id',
    icon: 'i-building', tone: 'teal', hex: '#14B8A6',
    short: 'Kelola multi-cabang, dokumen, e-sign, dan audit log.',
    feats: ['Multi cabang', 'E-sign & dokumen', 'Audit log', 'Manajemen user'] }
];
