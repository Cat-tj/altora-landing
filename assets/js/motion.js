/* Posisi kursor untuk hover kartu (motion.css bagian 3). Hanya jalan bila html.m-on dan perangkat pakai mouse. */
(function () {
  if (!document.documentElement.classList.contains('m-on')) return;
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;
  var card = null, ev = null, raf = 0;
  function paint() {
    raf = 0;
    if (!card || !ev) return;
    var r = card.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top;
    card.style.setProperty('--mx', x + 'px');
    card.style.setProperty('--my', y + 'px');
    card.style.setProperty('--px', (x / r.width * 2 - 1).toFixed(3));
    card.style.setProperty('--py', (y / r.height * 2 - 1).toFixed(3));
  }
  document.addEventListener('pointermove', function (e) {
    var c = e.target.closest && e.target.closest('.svc2-card,.ap2-card');
    if (!c) return;
    card = c; ev = e;
    if (!raf) raf = requestAnimationFrame(paint);
  }, { passive: true });
})();
