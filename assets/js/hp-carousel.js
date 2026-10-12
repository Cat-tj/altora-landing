/* Slideshow produk di beranda: tombol panah menggeser satu "halaman" kartu. Tanpa JS tetap bisa digeser. */
(function () {
  'use strict';
  document.querySelectorAll('.hp-carousel').forEach(function (root) {
    var track = root.querySelector('.hp-track');
    var prev = root.querySelector('.hp-prev');
    var next = root.querySelector('.hp-next');
    if (!track || !prev || !next) return;
    function step() { return Math.max(track.clientWidth * 0.9, 200); }
    function update() {
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowRight') { ev.preventDefault(); next.click(); }
      if (ev.key === 'ArrowLeft') { ev.preventDefault(); prev.click(); }
    });
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });
}());
