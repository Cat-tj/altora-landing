/* ============================================================
   ALTORA — landing page behaviour
   ============================================================ */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var icon = function (id, cls) { return '<svg class="ico' + (cls ? ' ' + cls : '') + '"><use href="#' + id + '"/></svg>'; };

  /* ── data ────────────────────────────────────────── */

  var MODULES = window.ALTORA_MODULES || [];

  var STEPS = [
    { n: 1, icon: 'i-clipboard', hex: '#12A374', bg: '#DCF0E7', title: 'Pahami Operasi', text: 'Kami memetakan proses, hambatan, dan konteks kerja sebelum menentukan teknologi.' },
    { n: 2, icon: 'i-layers', hex: '#7C5CE8', bg: '#EAE2FB', title: 'Tentukan Pendekatan', text: 'Kami memilih produk, integrasi, atau sistem custom yang paling relevan.' },
    { n: 3, icon: 'i-spark', hex: '#3B82F6', bg: '#E1EBFD', title: 'Implementasi & Dampingi', text: 'Kami membangun, mengintegrasikan, menguji, lalu membantu tim menjalankannya.' },
    { n: 4, icon: 'i-graph', hex: '#F59E0B', bg: '#FCEBD2', title: 'Optimalkan Bersama', text: 'Kami membaca temuan implementasi untuk menentukan penyempurnaan berikutnya.' }
  ];

  var PLANS = [
    { name: 'Leads ada, tapi tidak jadi percakapan', icon: 'i-monitor', tone: 'green', tick: '#12A374',
      desc: 'Orang sudah melihat bisnis Anda, tetapi pesan dan jalur konversinya belum meyakinkan.',
      feats: ['Positioning yang mudah dipahami', 'Website/landing page yang fokus', 'Alur kontak yang jelas', 'Tracking konversi'] },
    { name: 'Calon pelanggan sulit menemukan Anda', icon: 'i-trend', tone: 'purple', tick: '#7C5CE8', popular: true,
      desc: 'Bisnis yang bagus tetap kehilangan peluang ketika tidak terlihat pada saat orang mencari.',
      feats: ['Audit visibilitas digital', 'SEO teknis dan struktur konten', 'Strategi keyword & konten', 'Local search visibility', 'Growth roadmap'] },
    { name: 'Tim habis waktu untuk pekerjaan berulang', icon: 'i-spark', tone: 'blue', tick: '#3B82F6',
      desc: 'Respons, follow-up, rekap, dan alur kerja manual membuat tim lambat bergerak.',
      feats: ['Pemetaan workflow', 'AI assistant sesuai kebutuhan', 'Automation setup', 'Integrasi tools', 'Knowledge base tim'] },
    { name: 'Teknologi bisnis terasa rapuh', icon: 'i-cloud', tone: 'pink', tick: '#EC5B9E',
      desc: 'Server, jaringan, akses, dan data belum dikelola sebagai fondasi yang aman.',
      feats: ['Cloud & server design', 'Network security review', 'Backup & monitoring', 'Access management', 'Infrastructure roadmap'] }
  ];

  var FAQS = [
    { icon: 'i-layers', tone: 'purple', q: 'Apa saja yang dikerjakan Altora?',
      a: 'Dua hal: jasa pembuatan software (aplikasi web dan HP, sistem internal, website) dan pengadaan hardware dari principal resmi, lengkap dengan pemasangan dan perawatannya.' },
    { icon: 'i-puzzle', tone: 'blue', q: 'Jika kebutuhan kami tidak cocok dengan aplikasi yang ada di pasaran, apakah bisa dibuat khusus?',
      a: 'Bisa. Kami pelajari alur kerja Anda dulu, lalu membuat aplikasi web atau HP, sistem internal, website, dashboard, dan integrasi dengan sistem lain sesuai kebutuhan.' },
    { icon: 'i-monitor', tone: 'cyan', q: 'Apakah Altora hanya membuat software?',
      a: 'Tidak. Kami juga mengadakan dan memasang perangkat: server, komputer, CCTV, jaringan, smartlock, kios, display, dan GPS tracker.' },
    { icon: 'i-shield', tone: 'orange', q: 'Perangkat dari merek apa saja yang tersedia?',
      a: 'Dari principal resmi seperti VIGI, TP-Link, Teltonika, Lenovo, HDe, HaganeRack, dan Fasser, dengan garansi resmi. Kami pilihkan tipe yang paling cocok tanpa mengunci Anda pada satu merek.' },
    { icon: 'i-trend', tone: 'green', q: 'Apakah bisa untuk pengadaan instansi?',
      a: 'Bisa. Altora berstatus PKP dan terdaftar sebagai penyedia di Inaproc/LKPP, dengan penawaran, faktur, dan berita acara serah terima.' },
    { icon: 'i-sync', tone: 'pink', q: 'Bisakah aplikasi yang dibuat terhubung dengan aplikasi atau perangkat yang sudah kami gunakan?',
      a: 'Umumnya bisa. Kami cek dulu aplikasi dan perangkat yang Anda pakai, lalu tentukan cara menghubungkannya.' },
    { icon: 'i-clipboard', tone: 'navy', q: 'Bagaimana proses memulai proyek?',
      a: 'Hubungi kami lewat WhatsApp atau form konsultasi. Setelah memahami kebutuhan Anda, kami sarankan solusi yang sesuai, lalu kirim penawaran.' },
    { icon: 'i-headset', tone: 'teal', q: 'Bagaimana pendampingan setelah selesai?',
      a: 'Kami dampingi dari konsultasi awal, pemasangan atau pengembangan, pelatihan pengguna, sampai dukungan setelah sistem berjalan. Detail kerja sama kita diskusikan lewat chat.' }
  ];


  /* ── render: industries ──────────────────────────── */

  var indGrid = $('#indGrid');
  if (indGrid) {
    indGrid.innerHTML = MODULES.map(function (m, i) {
      return '<article class="ind reveal" data-d="' + (i % 4) + '">' +
        '<span class="mi mi-' + m.tone + '">' + icon(m.icon) + '</span>' +
        '<h3>' + m.name + '</h3>' +
        '<p>' + m.short + '</p>' +
        '<ul>' + m.feats.map(function (f) { return '<li>' + icon('i-check') + f + '</li>'; }).join('') + '</ul>' +
        '<a class="more" href="' + (m.href || '/services') + '" style="color:' + m.hex + '">Pelajari lebih lanjut ' + icon('i-arrow') + '</a>' +
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
        (p.popular ? '<span class="tag">Populer</span>' : '') +
        '<div class="plan-top">' +
          '<span class="mi mi-' + p.tone + '">' + icon(p.icon) + '</span>' +
          '<h3>' + p.name + '</h3>' +
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

  /* Top bar (scroll & burger) diurus site-shell.js agar sama di semua halaman. */

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
