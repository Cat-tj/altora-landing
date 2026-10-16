/* Prototipe "halaman = gedung": zoom in ke puncak, lantai terbuka satu per satu, zoom out di akhir. */
(function () {
  var root = document.querySelector('.gd2');
  if (!root) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var VB_X = -220, VB_W = 800, BODY_W = 360, TOP_Y = 70, LOBBY_Y = 430, BOTTOM_Y = 546;
  var intro = root.querySelector('.gd-intro'), outro = root.querySelector('.gd-outro');
  var bIn = intro.querySelector('.gd-bld'), bOut = outro.querySelector('.gd-bld');
  var sIn = intro.querySelector('.gd-scene'), sOut = outro.querySelector('.gd-scene');
  var floors = [].slice.call(root.querySelectorAll('.gf'));
  var lift = root.querySelector('.gd-lift'), liftNum = lift.querySelector('b');

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function progress(sec) {
    var r = sec.getBoundingClientRect(), span = sec.offsetHeight - window.innerHeight;
    return clamp(-r.top / span);
  }

  var L = {};
  function layout() {
    var vw = window.innerWidth, vh = window.innerHeight;
    var W0 = Math.min(vw < 900 ? vw * 0.96 : 620, vw * 0.9);
    var u = W0 / VB_W;
    var H0 = W0 * (BOTTOM_Y + 10) / VB_W;
    L = { vw: vw, vh: vh, W0: W0, u: u, left0: (vw - W0) / 2, top0: vh - H0 + 8, sEnd: vw / (BODY_W * u) };
    bIn.style.width = bOut.style.width = W0 + 'px';
  }

  function place(el, s, ax, ay, Ax, Ay) {
    el.style.transform = 'translate(' + (Ax - ax * s) + 'px,' + (Ay - ay * s) + 'px) scale(' + s + ')';
  }
  function unit(x, y) { return [(x - VB_X) * L.u, (y + 10) * L.u]; }

  function frame() {
    // ── intro: zoom ke puncak, atap terangkat, kaca lantai 7 memudar
    var t = progress(intro);
    var z = ease(clamp((t - 0.06) / 0.6));
    var s = Math.pow(L.sEnd, z);
    var a = unit(BODY_W / 2, TOP_Y);
    var A0x = L.left0 + a[0], A0y = L.top0 + a[1];
    place(bIn, s, a[0], a[1], lerp(A0x, L.vw / 2, z), lerp(A0y, L.vh * 0.36, z));
    var r = ease(clamp((t - 0.5) / 0.25)), f = clamp((t - 0.7) / 0.18), w = clamp((t - 0.82) / 0.14);
    bIn.style.setProperty('--roof-y', (-r * 160) + 'px');
    bIn.style.setProperty('--roof-o', 1 - r);
    bIn.style.setProperty('--top-facade', 1 - f);
    bIn.style.setProperty('--rest', 1 - w);
    sIn.style.setProperty('--walls', w);
    sIn.style.setProperty('--hero', 1 - clamp(t / 0.22));
    sIn.style.setProperty('--veil', clamp((t - 0.88) / 0.1));

    // ── outro: dari dalam lobi, zoom out sampai gedung utuh dan tanah terlihat
    var o = progress(outro);
    var zo = ease(clamp((o - 0.05) / 0.7));
    var so = Math.pow(L.sEnd, 1 - zo);
    var b = unit(BODY_W / 2, LOBBY_Y);
    var endY = L.top0 + b[1];
    place(bOut, so, b[0], b[1], L.vw / 2, lerp(L.vh * 0.08, endY, zo));
    sOut.style.setProperty('--walls', 1 - clamp(zo / 0.25));
    sOut.style.setProperty('--veil', 1 - clamp((o - 0.0) / 0.12));
    sOut.style.setProperty('--outro', clamp((o - 0.7) / 0.2));

    // ── indikator lift
    var mid = L.vh * 0.5, cur = null;
    floors.forEach(function (fl) {
      var rr = fl.getBoundingClientRect();
      if (rr.top < mid && rr.bottom > mid) cur = fl.dataset.k;
    });
    lift.classList.toggle('on', !!cur);
    if (cur) liftNum.textContent = cur;
  }

  // lantai terbuka saat masuk layar
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) en.target.classList.add('open'); });
    }, { threshold: 0.18 });
    floors.forEach(function (fl) { io.observe(fl); });
  } else {
    floors.forEach(function (fl) { fl.classList.add('open'); });
  }
  if (reduce) return;

  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; frame(); }); } }
  layout(); frame();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { layout(); frame(); });
})();
