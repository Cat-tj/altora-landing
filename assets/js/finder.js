/* Pencari solusi di /produk: sektor + kebutuhan + kota -> rekomendasi halaman. */
(function () {
  'use strict';
  var box = document.querySelector('.fd-box');
  var raw = document.getElementById('fd-data');
  if (!box || !raw) return;
  var data = JSON.parse(raw.textContent);
  var form = box.querySelector('.fd-form');
  var out = box.querySelector('.fd-result');
  var IND = { pertambangan: 'Tambang & industri berat', pemerintahan: 'Pemerintahan & layanan publik', pendidikan: 'Kampus & sekolah', korporasi: 'Korporasi & dunia usaha' };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    var f = form.elements, city = f.city.value, ind = f.ind.value;
    var recs = (data[f.need.value] || []).map(function (r) {
      return '<a class="fd-card" href="' + esc(r[0].replace('{c}', city)) + '"><b>' + esc(r[1]) + '</b><small>' + esc(r[2]) + '</small><span>Lihat →</span></a>';
    }).join('');
    out.innerHTML = '<div class="fd-cards">' + recs +
      '<a class="fd-card fd-ind" href="/industri/' + esc(ind) + '"><b>Solusi ' + esc(IND[ind]) + '</b><small>Paket solusi untuk sektor Anda</small><span>Lihat →</span></a></div>';
  }
  form.addEventListener('change', render);
  render();
}());
