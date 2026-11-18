/* /portofolio: filter kategori. Semua konten sudah tampil di HTML; tidak ada animasi muncul yang bisa menyembunyikan konten. */
(function () {
  var filters = [].slice.call(document.querySelectorAll('[data-filter]'));
  var cards = [].slice.call(document.querySelectorAll('.pf-card[data-kind]'));
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var kind = b.getAttribute('data-filter');
      filters.forEach(function (x) { x.classList.toggle('is-active', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      cards.forEach(function (c) { c.hidden = !(kind === 'all' || c.getAttribute('data-kind') === kind); });
    });
  });
})();
