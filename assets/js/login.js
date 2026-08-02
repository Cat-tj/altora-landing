/* ============================================================
   ALTORA — halaman masuk (pemilih modul)
   ============================================================ */
(function () {
  'use strict';

  var grid = document.getElementById('loginGrid');
  var empty = document.getElementById('loginEmpty');
  var filter = document.getElementById('modFilter');
  var modules = window.ALTORA_MODULES || [];

  if (!grid) return;

  function icon(id) {
    return '<svg class="ico"><use href="#' + id + '"/></svg>';
  }

  grid.innerHTML = modules.map(function (m) {
    // Setiap modul berjalan di subdomainnya sendiri; halaman ini hanya
    // mengarahkan, kredensial diminta di aplikasi masing-masing.
    return '<li class="login-card" data-find="' + (m.name + ' ' + m.short + ' ' + m.feats.join(' ')).toLowerCase() + '">' +
      '<a href="https://' + m.host + '" style="--accent:' + m.hex + '">' +
        '<span class="lc-icon" style="background:' + m.hex + '">' + icon(m.icon) + '</span>' +
        '<span class="lc-body">' +
          '<b>' + m.name + '</b>' +
          '<code>' + m.host + '</code>' +
          '<i>' + m.short + '</i>' +
        '</span>' +
        '<span class="lc-go">Masuk ' + icon('i-arrow') + '</span>' +
      '</a>' +
    '</li>';
  }).join('');

  if (filter) {
    var cards = Array.prototype.slice.call(grid.children);

    filter.addEventListener('input', function () {
      var q = filter.value.trim().toLowerCase();
      var shown = 0;

      cards.forEach(function (card) {
        var hit = !q || card.dataset.find.indexOf(q) !== -1;
        card.hidden = !hit;
        if (hit) shown++;
      });

      empty.hidden = shown > 0;
    });
  }

  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
