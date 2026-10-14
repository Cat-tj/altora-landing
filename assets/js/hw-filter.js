/* Katalog: tab Barang / Jasa / Software + filter kategori barang. Tanpa JS semua bagian tetap tampil.
   Hash: #barang, #jasa, #software, #cat-<kategori>, atau #<id-produk>. */
(function () {
  'use strict';
  var panels = document.querySelectorAll('.kt-panel');
  var tabs = document.querySelectorAll('.kt-tab');
  var bar = document.querySelector('.hwi-filter');
  if (!panels.length) return;
  function showPanel(name) {
    panels.forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== name; });
    tabs.forEach(function (t) { t.setAttribute('aria-current', t.getAttribute('data-tab') === name ? 'true' : 'false'); });
  }
  function filter(f) {
    if (!bar) return;
    bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-filter') === f)); });
    document.querySelectorAll('[data-panel="barang"] .hwi').forEach(function (it) { it.hidden = f !== 'all' && it.getAttribute('data-cat') !== f; });
  }
  tabs.forEach(function (t) {
    t.addEventListener('click', function (ev) {
      ev.preventDefault();
      var name = t.getAttribute('data-tab');
      showPanel(name);
      history.replaceState(null, '', '#' + name);
    });
  });
  if (bar) bar.addEventListener('click', function (ev) {
    var b = ev.target.closest('button[data-filter]');
    if (b) filter(b.getAttribute('data-filter'));
  });
  function fromHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    var el = h && document.getElementById(h);
    if (h.indexOf('cat-') === 0 && bar && bar.querySelector('[data-filter="' + h.slice(4) + '"]')) {
      showPanel('barang'); filter(h.slice(4)); bar.scrollIntoView({ block: 'start' });
    } else if (el && el.classList.contains('kt-panel')) {
      showPanel(h); filter('all');
    } else if (el) {
      var panel = el.closest('.kt-panel');
      showPanel(panel ? panel.getAttribute('data-panel') : 'barang'); filter('all');
      setTimeout(function () { el.scrollIntoView({ block: 'center' }); }, 50);
    } else {
      showPanel('barang'); filter('all');
    }
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
}());
