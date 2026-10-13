/* Filter kategori di /blog. Tanpa JS semua artikel tetap tampil. */
(function () {
  'use strict';
  var bar = document.querySelector('.bl-filter');
  if (!bar) return;
  var items = document.querySelectorAll('.bl-feature, .bl-card');
  bar.addEventListener('click', function (ev) {
    var btn = ev.target.closest('button[data-cat]');
    if (!btn) return;
    var c = btn.getAttribute('data-cat');
    bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    items.forEach(function (it) { it.hidden = c !== 'all' && it.getAttribute('data-cat') !== c; });
  });
}());
