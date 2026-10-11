/* Filter kategori katalog hardware di /produk. Tanpa JS semua produk tetap tampil. */
(function () {
  'use strict';
  var bar = document.querySelector('.hwi-filter');
  if (!bar) return;
  var items = document.querySelectorAll('.hwi');
  bar.addEventListener('click', function (ev) {
    var btn = ev.target.closest('button[data-filter]');
    if (!btn) return;
    var f = btn.getAttribute('data-filter');
    bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    items.forEach(function (it) { it.hidden = f !== 'all' && it.getAttribute('data-cat') !== f; });
  });
}());
