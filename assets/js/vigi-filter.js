/* Filter kategori di /katalog-cctv-vigi. Tanpa JS semua model tetap tampil. */
(function () {
  'use strict';
  var bar = document.querySelector('.vg-filter');
  if (!bar) return;
  var groups = document.querySelectorAll('.vg-group');
  bar.addEventListener('click', function (ev) {
    var btn = ev.target.closest('button[data-filter]');
    if (!btn) return;
    var f = btn.getAttribute('data-filter');
    bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    groups.forEach(function (g) { g.hidden = f !== 'all' && g.getAttribute('data-group') !== f; });
  });
}());
