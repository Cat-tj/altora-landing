/* ============================================================
   ALTORA — modal pemilih modul

   Tombol "Login" tetap sebuah <a href="login.html">, jadi tautannya bisa
   di-bookmark, dibuka di tab baru, dan tetap berfungsi kalau skrip ini gagal
   dimuat. Skrip ini hanya mencegat klik biasa dan menampilkan pilihan yang
   sama tanpa meninggalkan halaman.
   ============================================================ */
(function () {
  'use strict';

  var modules = window.ALTORA_MODULES || [];
  var links = document.querySelectorAll('a[href="login.html"]');
  if (!modules.length || !links.length) return;

  var FOCUSABLE = 'a[href],button:not([disabled]),input,[tabindex]:not([tabindex="-1"])';
  var modal = null;
  var lastFocused = null;

  function icon(id) {
    return '<svg class="ico"><use href="#' + id + '"/></svg>';
  }

  function build() {
    var el = document.createElement('div');
    el.className = 'lm';
    el.hidden = true;
    el.innerHTML =
      '<div class="lm-veil" data-close></div>' +
      '<div class="lm-panel" role="dialog" aria-modal="true" aria-labelledby="lmTitle">' +
        '<button class="lm-x" type="button" data-close aria-label="Tutup">' + icon('i-x') + '</button>' +
        '<p class="eyebrow eyebrow-purple">Masuk ke Altora</p>' +
        '<h2 id="lmTitle">Pilih modul yang ingin Anda akses</h2>' +
        '<p class="lm-lead">Setiap modul punya halaman masuk sendiri. Punya lebih dari satu? Masuk ke masing-masing modul sesuai bisnis yang ingin dikelola.</p>' +
        '<ul class="lm-grid">' +
          modules.map(function (m) {
            return '<li><a href="https://' + m.host + '/login" style="--accent:' + m.hex + '">' +
              '<span class="lm-icon" style="background:' + m.hex + '">' + icon(m.icon) + '</span>' +
              '<span class="lm-body"><b>' + m.name + '</b><code>' + m.host + '</code></span>' +
              icon('i-arrow') +
            '</a></li>';
          }).join('') +
        '</ul>' +
        '<p class="lm-foot">Belum punya akun? <a href="#cta" data-close>Mulai gratis</a>' +
          '<span>·</span><a href="login.html">Buka halaman penuh</a></p>' +
      '</div>';

    el.addEventListener('click', function (e) {
      if (e.target.closest('[data-close]')) close();
    });
    document.body.appendChild(el);
    return el;
  }

  function open(trigger) {
    if (!modal) modal = build();
    lastFocused = trigger || document.activeElement;

    // Kunci scroll tanpa menggeser layout saat scrollbar hilang.
    var gap = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = 'hidden';
    if (gap > 0) document.body.style.paddingRight = gap + 'px';

    modal.hidden = false;
    requestAnimationFrame(function () { modal.classList.add('on'); });

    var first = modal.querySelector('.lm-grid a');
    if (first) first.focus();

    document.addEventListener('keydown', onKey);
  }

  function close() {
    if (!modal || modal.hidden) return;

    modal.classList.remove('on');
    document.removeEventListener('keydown', onKey);
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';

    var done = function () {
      modal.hidden = true;
      modal.removeEventListener('transitionend', done);
    };
    modal.addEventListener('transitionend', done);

    if (lastFocused) lastFocused.focus();
  }

  function onKey(e) {
    if (e.key === 'Escape') return close();
    if (e.key !== 'Tab') return;

    var items = Array.prototype.filter.call(
      modal.querySelectorAll(FOCUSABLE),
      function (n) { return n.offsetParent !== null; }
    );
    if (!items.length) return;

    var first = items[0];
    var last = items[items.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  Array.prototype.forEach.call(links, function (link) {
    link.addEventListener('click', function (e) {
      // Biarkan browser menangani buka-di-tab-baru dan sejenisnya.
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault();
      open(link);
    });
  });
})();
