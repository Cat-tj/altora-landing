/* Filter kategori di /katalog. Tanpa JS semua produk tetap tampil.
   /katalog#cat-gps membuka langsung kategori itu; /katalog#<id-produk> menampilkan semua lalu menggulir ke produk. */
(function () {
  'use strict';
  var bar = document.querySelector('.hwi-filter');
  if (!bar) return;
  var items = document.querySelectorAll('.hwi');
  function apply(f) {
    bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-filter') === f)); });
    items.forEach(function (it) { it.hidden = f !== 'all' && it.getAttribute('data-cat') !== f; });
  }
  bar.addEventListener('click', function (ev) {
    var btn = ev.target.closest('button[data-filter]');
    if (btn) apply(btn.getAttribute('data-filter'));
  });
  function fromHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (h.indexOf('cat-') === 0 && bar.querySelector('[data-filter="' + h.slice(4) + '"]')) {
      apply(h.slice(4));
      bar.scrollIntoView({ block: 'start' });
    } else if (h && document.getElementById(h)) {
      apply('all');
    }
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
}());
