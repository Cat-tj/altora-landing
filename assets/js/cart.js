/* Keranjang permintaan penawaran (tanpa harga).
   Tombol: <button class="cart-add" data-cart-id data-cart-name data-cart-meta data-cart-img>.
   Isi keranjang disimpan di localStorage browser pengunjung, lalu dikirim sebagai pesan WhatsApp. */
(function () {
  'use strict';
  var KEY = 'altora-cart-v1';
  var WA = '6285190911170';
  var items = load();

  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return []; }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { /* mode privat: keranjang tetap jalan selama halaman terbuka */ }
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function count() { return items.reduce(function (n, it) { return n + it.qty; }, 0); }
  function find(id) { for (var i = 0; i < items.length; i++) if (items[i].id === id) return items[i]; return null; }

  var hasProducts = !!document.querySelector('.cart-add');

  // ── elemen UI ──
  var fab = document.createElement('button');
  fab.type = 'button';
  fab.className = 'cart-fab';
  fab.setAttribute('aria-label', 'Buka keranjang pesanan');
  fab.innerHTML = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M3 4h2.2l2.2 10.5h10.2L20 7.5H6.4"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/></svg><span>Keranjang</span><b class="cart-count">0</b>';

  var drawer = document.createElement('div');
  drawer.className = 'cart-drawer';
  drawer.hidden = true;
  drawer.innerHTML =
    '<div class="cart-backdrop" data-cart-close></div>' +
    '<aside aria-labelledby="cartTitle" aria-modal="true" class="cart-panel" role="dialog">' +
    '<header class="cart-head"><h2 id="cartTitle">Keranjang pesanan</h2><button aria-label="Tutup" class="cart-x" data-cart-close type="button">×</button></header>' +
    '<div class="cart-body"><ul class="cart-list"></ul>' +
    '<div class="cart-empty"><p>Keranjang masih kosong.</p><a class="btn btn-purple" href="/produk">Lihat produk</a></div>' +
    '<form class="cart-form" novalidate>' +
    '<p class="cart-form-title">Data untuk penawaran <small>(opsional)</small></p>' +
    '<label>Nama<input autocomplete="name" name="nama" type="text"/></label>' +
    '<label>Instansi / perusahaan<input autocomplete="organization" name="instansi" type="text"/></label>' +
    '<label>Lokasi pemasangan<input name="lokasi" placeholder="mis. Samarinda Ulu" type="text"/></label>' +
    '<label class="cart-check"><input checked name="instalasi" type="checkbox"/> Sekalian dengan instalasi</label>' +
    '<label>Catatan<textarea name="catatan" placeholder="Jumlah titik, kebutuhan khusus, target waktu…" rows="2"></textarea></label>' +
    '</form></div>' +
    '<footer class="cart-foot"><p class="cart-note">Detail pesanan kita diskusikan lewat WhatsApp.</p>' +
    '<a class="btn btn-green cart-send" href="#" rel="noopener" target="_blank"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/></svg>Kirim pesanan via WhatsApp</a>' +
    '<button class="cart-clear" type="button">Kosongkan keranjang</button></footer>' +
    '</aside>';

  var toast = document.createElement('div');
  toast.className = 'cart-toast';
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');

  document.body.appendChild(fab);
  document.body.appendChild(drawer);
  document.body.appendChild(toast);

  var list = drawer.querySelector('.cart-list');
  var form = drawer.querySelector('.cart-form');
  var send = drawer.querySelector('.cart-send');

  function message() {
    var f = form.elements;
    var lines = ['Halo Altora, saya ingin minta penawaran untuk pesanan berikut:', ''];
    items.forEach(function (it, i) {
      lines.push((i + 1) + '. ' + it.name + (it.meta ? ' (' + it.meta + ')' : '') + ' — ' + it.qty + ' unit');
    });
    lines.push('', 'Total: ' + count() + ' unit, ' + items.length + ' produk');
    lines.push('Instalasi: ' + (f.instalasi.checked ? 'Ya, sekalian dipasang' : 'Barang saja'));
    if (f.nama.value.trim()) lines.push('Nama: ' + f.nama.value.trim());
    if (f.instansi.value.trim()) lines.push('Instansi: ' + f.instansi.value.trim());
    if (f.lokasi.value.trim()) lines.push('Lokasi: ' + f.lokasi.value.trim());
    if (f.catatan.value.trim()) lines.push('Catatan: ' + f.catatan.value.trim());
    lines.push('', 'Dikirim dari keranjang altora.id');
    return lines.join('\n');
  }

  function render() {
    var n = count();
    fab.querySelector('.cart-count').textContent = n;
    fab.hidden = !hasProducts && n === 0;
    fab.classList.toggle('has-items', n > 0);
    drawer.classList.toggle('is-empty', n === 0);
    list.innerHTML = items.map(function (it) {
      var pic = it.img ? '<img alt="" src="' + esc(it.img) + '"/>' : '';
      return '<li data-id="' + esc(it.id) + '"><span class="cart-pic">' + pic + '</span>' +
        '<span class="cart-info"><b>' + esc(it.name) + '</b><small>' + esc(it.meta || '') + '</small></span>' +
        '<span class="cart-qty"><button aria-label="Kurangi" data-step="-1" type="button">−</button>' +
        '<input aria-label="Jumlah ' + esc(it.name) + '" inputmode="numeric" min="1" type="number" value="' + it.qty + '"/>' +
        '<button aria-label="Tambah" data-step="1" type="button">+</button></span>' +
        '<button aria-label="Hapus ' + esc(it.name) + '" class="cart-del" type="button">×</button></li>';
    }).join('');
    send.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message());
    document.querySelectorAll('.cart-add').forEach(function (b) {
      var it = find(b.getAttribute('data-cart-id'));
      b.classList.toggle('in-cart', !!it);
      b.querySelector('.cart-add-label').textContent = it ? 'Di keranjang (' + it.qty + ')' : 'Tambah ke keranjang';
    });
  }

  var toastTimer;
  function notify(text) {
    toast.textContent = text;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  }

  function open() { drawer.hidden = false; document.documentElement.classList.add('cart-open'); setTimeout(function () { drawer.classList.add('open'); drawer.querySelector('.cart-x').focus(); }, 10); }
  function close() { drawer.classList.remove('open'); document.documentElement.classList.remove('cart-open'); setTimeout(function () { drawer.hidden = true; fab.focus(); }, 220); }

  // tambah dari kartu produk
  document.querySelectorAll('.cart-add').forEach(function (b) {
    if (!b.querySelector('.cart-add-label')) b.innerHTML = '<span aria-hidden="true">+</span><span class="cart-add-label">Tambah ke keranjang</span>';
  });
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('.cart-add');
    if (!b) return;
    var id = b.getAttribute('data-cart-id');
    var it = find(id);
    if (it) it.qty += 1;
    else items.push({ id: id, name: b.getAttribute('data-cart-name'), meta: b.getAttribute('data-cart-meta') || '', img: b.getAttribute('data-cart-img') || '', qty: 1 });
    save(); render();
    fab.classList.remove('bump'); void fab.offsetWidth; fab.classList.add('bump');
    notify(b.getAttribute('data-cart-name') + ' ditambahkan ke keranjang');
  });

  fab.addEventListener('click', open);
  drawer.addEventListener('click', function (ev) {
    if (ev.target.closest('[data-cart-close]')) return close();
    var row = ev.target.closest('li[data-id]');
    if (!row) return;
    var it = find(row.getAttribute('data-id'));
    if (!it) return;
    var step = ev.target.closest('[data-step]');
    if (step) { it.qty = Math.max(1, it.qty + Number(step.getAttribute('data-step'))); save(); render(); }
    else if (ev.target.closest('.cart-del')) { items = items.filter(function (x) { return x !== it; }); save(); render(); }
  });
  list.addEventListener('change', function (ev) {
    var row = ev.target.closest('li[data-id]');
    var it = row && find(row.getAttribute('data-id'));
    if (!it) return;
    it.qty = Math.max(1, Math.min(999, parseInt(ev.target.value, 10) || 1));
    save(); render();
  });
  form.addEventListener('input', function () { send.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message()); });
  form.addEventListener('change', function () { send.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message()); });
  send.addEventListener('click', function (ev) { if (!items.length) { ev.preventDefault(); } });
  drawer.querySelector('.cart-clear').addEventListener('click', function () {
    if (!items.length || window.confirm('Kosongkan semua isi keranjang?')) { items = []; save(); render(); }
  });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && !drawer.hidden) close(); });
  window.addEventListener('storage', function (ev) { if (ev.key === KEY) { items = load(); render(); } });

  render();
}());
