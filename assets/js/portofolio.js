/* /portofolio: filter kategori (seperti Sentra) + animasi muncul saat scroll. Konten tetap ada di HTML tanpa JS. */
(function () {
  var root = document.documentElement, reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var filters = [].slice.call(document.querySelectorAll('[data-filter]'));
  var cards = [].slice.call(document.querySelectorAll('.pf-card[data-kind]'));
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var kind = b.getAttribute('data-filter');
      filters.forEach(function (x) { x.classList.toggle('is-active', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      cards.forEach(function (c) { c.hidden = !(kind === 'all' || c.getAttribute('data-kind') === kind); });
    });
  });
  var els = [].slice.call(document.querySelectorAll('.pf-rv'));
  if (!els.length || reduce || !('IntersectionObserver' in window)) return;
  root.classList.add('pf-js');
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (el) { io.observe(el); });
})();
