/* Katalog: pilih kebutuhan ("Cari apa?") -> tampilkan barang, jasa, dan software yang relevan.
   Hash: #v-<pilihan>, #cat-<kategori barang>, #barang / #jasa / #software, atau #<id-produk>.
   Tanpa JS, bagian hasil tetap disembunyikan oleh atribut hidden; daftar pilihan tetap bisa dipakai lewat link. */
(function () {
  'use strict';
  var res = document.getElementById('hasil');
  var viewsEl = document.getElementById('kc-views');
  if (!res || !viewsEl) return;
  var VIEWS = JSON.parse(viewsEl.textContent);
  var CATS = JSON.parse(document.getElementById('kc-cats').textContent);
  var items = Array.prototype.slice.call(res.querySelectorAll('.hwi'));
  var sub = res.querySelector('.kr-sub');
  var title = res.querySelector('.kr-title');
  var count = res.querySelector('.kr-count');
  var vigi = res.querySelector('.kr-vigi');
  var tiles = document.querySelectorAll('.kc-tile');
  var current = [];

  function matches(it, v) {
    return v.cats.indexOf(it.getAttribute('data-cat')) > -1 || v.ids.indexOf(it.id) > -1;
  }
  function applySub(cat) {
    sub.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-filter') === cat)); });
    var n = 0;
    items.forEach(function (it) {
      var on = current.indexOf(it) > -1 && (cat === 'all' || it.getAttribute('data-cat') === cat);
      it.hidden = !on; if (on) n++;
    });
    count.textContent = n + ' item';
  }
  function show(key, cat, focusId) {
    var v = VIEWS[key];
    if (!v) return;
    current = items.filter(function (it) { return matches(it, v); });
    var cats = [];
    current.forEach(function (it) { var c = it.getAttribute('data-cat'); if (cats.indexOf(c) < 0) cats.push(c); });
    sub.innerHTML = cats.length > 1 ? '<button aria-pressed="true" data-filter="all" type="button">Semua</button>' +
      cats.map(function (c) { return '<button aria-pressed="false" data-filter="' + c + '" type="button">' + (CATS[c] || c) + '</button>'; }).join('') : '';
    sub.hidden = cats.length < 2;
    title.textContent = v.t;
    vigi.hidden = cats.indexOf('cctv') < 0;
    tiles.forEach(function (t) { t.setAttribute('aria-current', t.getAttribute('data-view') === key ? 'true' : 'false'); });
    res.hidden = false;
    applySub(cat && cats.indexOf(cat) > -1 ? cat : 'all');
    var target = focusId && document.getElementById(focusId);
    setTimeout(function () { (target || res).scrollIntoView({ block: target ? 'center' : 'start' }); }, 30);
  }
  function hide() {
    res.hidden = true;
    tiles.forEach(function (t) { t.setAttribute('aria-current', 'false'); });
  }
  sub.addEventListener('click', function (ev) {
    var b = ev.target.closest('button[data-filter]');
    if (b) applySub(b.getAttribute('data-filter'));
  });
  res.querySelector('.kr-back').addEventListener('click', function (ev) {
    ev.preventDefault();
    history.replaceState(null, '', location.pathname);
    hide();
    window.scrollTo({ top: 0 });
  });
  var LEGACY = { barang: 'barang', jasa: 'jasa', software: 'software' };
  function fromHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (!h) return hide();
    if (h.indexOf('v-') === 0 && VIEWS[h.slice(2)]) return show(h.slice(2));
    if (h.indexOf('cat-') === 0) return show('barang', h.slice(4));
    if (LEGACY[h]) return show(LEGACY[h]);
    var el = document.getElementById(h);
    if (el && el.classList.contains('hwi')) {
      var c = el.getAttribute('data-cat');
      return show(c === 'jasa' ? 'jasa' : c === 'app' ? 'software' : 'barang', null, h);
    }
    hide();
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
}());
