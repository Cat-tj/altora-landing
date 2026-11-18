/* Beranda: peta jangkauan (tab Hardware/Software, animasi garis saat terlihat, ganti otomatis sampai pengunjung memilih)
   dan carousel proyek (tombol panah; berjalan pelan tanpa ujung, berhenti saat disentuh/hover/fokus/di luar layar).
   Perilaku mengikuti beranda situs saudara. Tanpa JS: peta Kalimantan dan daftar proyek tetap tampil dan bisa digeser. */
(function () {
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var r = document.querySelector('.reach');
  if (r) {
    var tabs = [].slice.call(r.querySelectorAll('[role="tab"]'));
    var auto = 0, chosen = false, inView = false;
    var play = function () { r.classList.remove('play'); void r.offsetWidth; r.classList.add('play'); };
    var set = function (mode) {
      r.setAttribute('data-mode', mode);
      tabs.forEach(function (t) { var on = t.getAttribute('data-mode') === mode; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
      play();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { chosen = true; clearInterval(auto); set(t.getAttribute('data-mode')); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault(); var n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); n.click();
      });
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        inView = e[0].isIntersecting; r.classList.toggle('in-view', inView);
        if (inView && !r.classList.contains('play')) play();
      }, { threshold: 0.35 }).observe(r);
    }
    if (!still) auto = setInterval(function () { if (!chosen && inView && !document.hidden) set(r.getAttribute('data-mode') === 'hw' ? 'sw' : 'hw'); }, 7000);
  }

  [].slice.call(document.querySelectorAll('.hm-carousel')).forEach(function (c) {
    var track = c.querySelector('.hm-track');
    if (!track) return;
    var p = c.querySelector('.hm-prev'), n = c.querySelector('.hm-next');
    var autoRun = c.hasAttribute('data-auto') && !still && track.children.length > 1;
    var pos = 0, half = 0, hold = 0, seen = false, last = 0, resume;
    var pause = function (ms) { hold++; clearTimeout(resume); if (ms) resume = setTimeout(function () { hold = 0; pos = track.scrollLeft; }, ms); };
    var step = function (d) { if (autoRun) pause(1600); track.scrollBy({ left: d * Math.max(260, track.clientWidth * 0.8), behavior: 'smooth' }); };
    if (p) p.addEventListener('click', function () { step(-1); });
    if (n) n.addEventListener('click', function () { step(1); });
    if (!autoRun) return;
    var items = [].slice.call(track.children);
    items.forEach(function (it) { var k = it.cloneNode(true); k.setAttribute('aria-hidden', 'true'); k.tabIndex = -1; track.appendChild(k); });
    track.style.scrollSnapType = 'none';
    var measure = function () { half = track.children[items.length].offsetLeft - items[0].offsetLeft; };
    measure(); addEventListener('resize', measure);
    var release = function () { hold = 0; pos = track.scrollLeft; };
    c.addEventListener('mouseenter', function () { pause(); });
    c.addEventListener('mouseleave', release);
    c.addEventListener('focusin', function () { pause(); });
    c.addEventListener('focusout', release);
    track.addEventListener('touchstart', function () { pause(); }, { passive: true });
    track.addEventListener('touchend', function () { pause(2500); }, { passive: true });
    track.addEventListener('scroll', function () {
      if (!hold) return;
      if (track.scrollLeft >= half) track.scrollLeft -= half; else if (track.scrollLeft <= 0 && half) track.scrollLeft += half;
    }, { passive: true });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { seen = es[0].isIntersecting; }).observe(c); else seen = true;
    var tick = function (t) {
      var dt = Math.min(64, t - (last || t)); last = t;
      if (seen && !hold && !document.hidden && half) { pos += dt * 0.04; if (pos >= half) pos -= half; track.scrollLeft = pos; }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
})();
