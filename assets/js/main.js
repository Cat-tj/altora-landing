/* ============================================================
   ALTORA — landing page behaviour
   ============================================================ */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var icon = function (id, cls) { return '<svg class="ico' + (cls ? ' ' + cls : '') + '"><use href="#' + id + '"/></svg>'; };

  /* ── data ────────────────────────────────────────── */

  var MODULES = [
    { key: 'cafe', name: 'Altora Cafe', icon: 'i-coffee', tone: 'purple', hex: '#7C5CE8',
      short: 'Kelola cafe lebih efisien, dari meja hingga dapur.',
      feats: ['Kasir & meja', 'Resep & bahan baku', 'Pesanan QR meja', 'Laporan penjualan'] },

    { key: 'market', name: 'Altora Market', icon: 'i-cart', tone: 'green', hex: '#12A374',
      short: 'Solusi lengkap untuk minimarket & toko kelontong.',
      feats: ['Kasir POS', 'Stok real-time', 'Promo & diskon', 'Laporan & analitik'] },

    { key: 'supermarket', name: 'Altora Supermarket', icon: 'i-basket', tone: 'blue', hex: '#3B82F6',
      short: 'Kelola stok besar, grosir bertingkat, dan multi-outlet.',
      feats: ['Grosir & retail', 'Multi cabang', 'Purchase order', 'Transfer antar gudang'] },

    { key: 'laundry', name: 'Altora Laundry', icon: 'i-washer', tone: 'cyan', hex: '#22B8CF',
      short: 'Kelola order kiloan, paket, cicilan, dan pengantaran.',
      feats: ['Order kiloan & satuan', 'Paket & harga', 'Pengantaran', 'Laporan keuangan'] },

    { key: 'counter', name: 'Altora Counter', icon: 'i-phone', tone: 'pink', hex: '#EC5B9E',
      short: 'Cocok untuk counter HP, servis, dan aksesoris.',
      feats: ['Servis & perbaikan', 'Aksesoris & stok', 'Stok sparepart', 'Garansi & nota servis'] },

    { key: 'jasa', name: 'Altora Jasa', icon: 'i-scissors', tone: 'orange', hex: '#F59E0B',
      short: 'Untuk barbershop, salon, spa, dan berbagai jasa.',
      feats: ['Booking online', 'Jadwal & terapis', 'Membership', 'Laporan & komisi'] },

    { key: 'pabrik', name: 'Altora Pabrik', icon: 'i-factory', tone: 'navy', hex: '#3E4E7E',
      short: 'Kelola bahan baku, produksi, dan maintenance mesin.',
      feats: ['BOM & produksi', 'Bahan baku', 'QC & maintenance', 'Laporan produksi'] },

    { key: 'company', name: 'Altora Company', icon: 'i-building', tone: 'teal', hex: '#14B8A6',
      short: 'Kelola multi-cabang, dokumen, e-sign, dan audit log.',
      feats: ['Multi cabang', 'E-sign & dokumen', 'Audit log', 'Manajemen user'] }
  ];

  var STEPS = [
    { n: 1, icon: 'i-cart', hex: '#12A374', bg: '#DCF0E7', title: 'Transaksi di Kasir', text: 'Kasir mencatat penjualan dengan cepat dan mudah.' },
    { n: 2, icon: 'i-box', hex: '#7C5CE8', bg: '#EAE2FB', title: 'Stok Otomatis Berkurang', text: 'Stok diupdate otomatis sesuai transaksi yang terjadi.' },
    { n: 3, icon: 'i-file', hex: '#3B82F6', bg: '#E1EBFD', title: 'Data & Laba Terhitung', text: 'Sistem menghitung omzet, laba, dan biaya secara otomatis.' },
    { n: 4, icon: 'i-pie', hex: '#F59E0B', bg: '#FCEBD2', title: 'Laporan Real-time', text: 'Laporan penjualan, stok, dan keuangan selalu up-to-date.' },
    { n: 5, icon: 'i-bell', hex: '#EC5B9E', bg: '#FBE0EC', title: 'Notifikasi & Peringatan', text: 'Dapatkan alert stok menipis, utang jatuh tempo, dan lainnya.' }
  ];

  var PLANS = [
    { name: 'Starter', icon: 'i-leaf', tone: 'green', tick: '#12A374',
      desc: 'Cocok untuk bisnis kecil yang baru memulai.',
      feats: ['Kasir POS', 'Stok & Inventori', 'Laporan Penjualan', 'Multi User'] },
    { name: 'Pro', icon: 'i-crown', tone: 'purple', tick: '#7C5CE8', popular: true,
      desc: 'Untuk bisnis yang sudah berkembang.',
      feats: ['Semua di Starter, plus:', 'Purchase Order', 'Laporan Lanjutan', 'Manajemen Promo', 'Akses Multi Cabang'] },
    { name: 'Business', icon: 'i-brief', tone: 'blue', tick: '#3B82F6',
      desc: 'Untuk bisnis skala besar dan multi-outlet.',
      feats: ['Semua di Pro, plus:', 'Manajemen Gudang', 'Laporan Keuangan', 'Approval & Hak Akses', 'Integrasi API'] },
    { name: 'Enterprise', icon: 'i-building', tone: 'pink', tick: '#EC5B9E',
      desc: 'Solusi khusus untuk kebutuhan enterprise Anda.',
      feats: ['Semua di Business, plus:', 'Kustomisasi Sistem', 'Dedicated Support', 'SLA & Security Tingkat Tinggi', 'On-Premise (Opsional)'] }
  ];

  var FAQS = [
    { icon: 'i-monitor', tone: 'purple', q: 'Apakah Altora bisa digunakan di HP dan tablet?',
      a: 'Ya, Altora bisa diakses dari berbagai perangkat, termasuk HP, tablet, dan komputer.' },
    { icon: 'i-download', tone: 'blue', q: 'Apakah perlu instalasi?',
      a: 'Tidak perlu. Altora berbasis cloud, jadi Anda bisa langsung gunakan tanpa instalasi.' },
    { icon: 'i-cloud', tone: 'cyan', q: 'Apakah data saya aman?',
      a: 'Ya, data Anda dienkripsi dan di-backup setiap hari di server yang aman.' },
    { icon: 'i-headset', tone: 'orange', q: 'Apakah ada bantuan untuk migrasi data?',
      a: 'Ya, tim kami siap membantu migrasi data dari sistem atau pencatatan sebelumnya.' },
    { icon: 'i-store', tone: 'green', q: 'Apakah bisa digunakan untuk banyak cabang?',
      a: 'Bisa. Altora mendukung multi-cabang dengan kontrol terpusat secara real-time.' },
    { icon: 'i-sync', tone: 'pink', q: 'Bisakah saya mencoba Altora terlebih dahulu?',
      a: 'Tentu! Anda bisa mencoba demo gratis dan melihat fitur-fiturnya sebelum berlangganan.' }
  ];

  /* ── render: industries ──────────────────────────── */

  var indGrid = $('#indGrid');
  if (indGrid) {
    indGrid.innerHTML = MODULES.map(function (m, i) {
      return '<article class="ind reveal" data-d="' + (i % 4) + '">' +
        '<span class="mi mi-' + m.tone + '">' + icon(m.icon) + '</span>' +
        '<h3>' + m.name + '</h3>' +
        '<p>' + m.short + '</p>' +
        '<div class="scene" style="background:linear-gradient(140deg,' + m.hex + ',' + shade(m.hex, -22) + ')">' + icon(m.icon) + '</div>' +
        '<ul>' + m.feats.map(function (f) { return '<li>' + icon('i-check') + f + '</li>'; }).join('') + '</ul>' +
        '<a class="more" href="#modul" style="color:' + m.hex + '">Pelajari lebih lanjut ' + icon('i-arrow') + '</a>' +
        '</article>';
    }).join('');
  }

  /* ── render: steps ───────────────────────────────── */

  var stepsEl = $('#steps');
  if (stepsEl) {
    stepsEl.innerHTML = STEPS.map(function (s, i) {
      return '<li class="step reveal" data-d="' + (i % 4) + '">' +
        '<span class="num" style="background:' + s.hex + '">' + s.n + '</span>' +
        '<span class="si" style="background:' + s.bg + ';color:' + s.hex + '">' + icon(s.icon) + '</span>' +
        '<h3>' + s.title + '</h3><p>' + s.text + '</p></li>';
    }).join('');
  }

  /* ── render: plans ───────────────────────────────── */

  var plansEl = $('#plans');
  if (plansEl) {
    plansEl.innerHTML = PLANS.map(function (p, i) {
      return '<article class="plan reveal' + (p.popular ? ' pop' : '') + '" data-d="' + (i % 4) + '">' +
        '<div class="plan-top">' +
          '<span class="mi mi-' + p.tone + '">' + icon(p.icon) + '</span>' +
          '<h3>' + p.name + '</h3>' +
          (p.popular ? '<span class="tag">Populer</span>' : '') +
        '</div>' +
        '<p>' + p.desc + '</p>' +
        '<ul>' + p.feats.map(function (f) {
          return '<li>' + icon('i-check', 'tk') + '<span>' + f + '</span></li>';
        }).join('') + '</ul>' +
        '<div class="plan-foot"><b>Hubungi kami</b><span>untuk informasi lebih lanjut</span></div>' +
        '</article>';
    }).join('');

    $$('.plan').forEach(function (el, i) {
      $$('.tk', el).forEach(function (s) { s.style.color = PLANS[i].tick; });
    });
  }

  /* ── render: faq ─────────────────────────────────── */

  var faqGrid = $('#faqGrid');
  if (faqGrid) {
    faqGrid.innerHTML = FAQS.map(function (f, i) {
      return '<div class="qa reveal" data-d="' + (i % 4) + '">' +
        '<summary role="button" tabindex="0" aria-expanded="false" aria-controls="fa' + i + '">' +
          '<span class="mi mi-' + f.tone + '">' + icon(f.icon) + '</span>' +
          '<h3>' + f.q + '</h3>' +
          icon('i-chevron', 'caret') +
        '</summary>' +
        '<div class="qa-body" id="fa' + i + '"><p>' + f.a + '</p></div>' +
        '</div>';
    }).join('');

    faqGrid.addEventListener('click', function (e) {
      var s = e.target.closest('summary');
      if (s) toggleQa(s.parentElement);
    });
    faqGrid.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var s = e.target.closest('summary');
      if (!s) return;
      e.preventDefault();
      toggleQa(s.parentElement);
    });
  }

  function toggleQa(qa) {
    var body = $('.qa-body', qa);
    var sum = $('summary', qa);
    var open = qa.hasAttribute('data-open');

    if (open) {
      body.style.height = body.scrollHeight + 'px';
      requestAnimationFrame(function () { body.style.height = '0px'; });
      qa.removeAttribute('data-open');
      sum.setAttribute('aria-expanded', 'false');
    } else {
      body.style.height = body.scrollHeight + 'px';
      qa.setAttribute('data-open', '');
      sum.setAttribute('aria-expanded', 'true');
      body.addEventListener('transitionend', function h() {
        if (qa.hasAttribute('data-open')) body.style.height = 'auto';
        body.removeEventListener('transitionend', h);
      });
    }
  }

  /* ── colour helpers ──────────────────────────────── */

  function shade(hex, amt) {
    var n = parseInt(hex.slice(1), 16);
    var r = clamp((n >> 16) + amt), g = clamp((n >> 8 & 255) + amt), b = clamp((n & 255) + amt);
    return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }
  function clamp(v) { return v < 0 ? 0 : v > 255 ? 255 : v; }

  /* ── nav ─────────────────────────────────────────── */

  var navWrap = $('#nav');
  var onScroll = function () { navWrap.classList.toggle('stuck', window.scrollY > 12); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var burger = $('#burger'), mobileMenu = $('#mobileMenu');
  burger.addEventListener('click', function () {
    var open = mobileMenu.classList.toggle('open');
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  });
  $$('#mobileMenu a').forEach(function (a) {
    a.addEventListener('click', function () {
      mobileMenu.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    });
  });

  var hasMenu = $('.has-menu');
  if (hasMenu) {
    var btn = $('.nav-link', hasMenu);
    var setMenu = function (open) {
      hasMenu.toggleAttribute('data-open', open);
      btn.setAttribute('aria-expanded', String(open));
    };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      setMenu(!hasMenu.hasAttribute('data-open'));
    });
    hasMenu.addEventListener('mouseenter', function () { setMenu(true); });
    hasMenu.addEventListener('mouseleave', function () { setMenu(false); });
    document.addEventListener('click', function (e) {
      if (!hasMenu.contains(e.target)) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
  }

  /* ── reveal on scroll ────────────────────────────── */

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduce || !('IntersectionObserver' in window)) {
    $$('.reveal').forEach(function (el) { el.classList.add('revealed'); });
    $$('[data-count]').forEach(function (el) { el.textContent = fmt(+el.dataset.count) + (el.dataset.suffix || ''); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('revealed');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    $$('.reveal').forEach(function (el) { io.observe(el); });
    $('.hero-stage') && $('.hero-stage').classList.add('revealed');

    /* counters */
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        count(en.target);
        cio.unobserve(en.target);
      });
    }, { threshold: 0.4 });
    $$('[data-count]').forEach(function (el) { cio.observe(el); });
  }

  function count(el) {
    var target = +el.dataset.count;
    var suffix = el.dataset.suffix || '';
    var decimals = (String(target).split('.')[1] || '').length;
    var dur = 1500, t0 = performance.now();

    (function tick(now) {
      var p = Math.min((now - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased, decimals) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }

  function fmt(v, decimals) {
    return v.toLocaleString('id-ID', {
      minimumFractionDigits: decimals || 0,
      maximumFractionDigits: decimals || 0
    });
  }

  /* ── footer year ─────────────────────────────────── */
  var yr = $('#yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
