/* Prototipe "halaman = gedung": satu adegan sticky yang sepenuhnya mengikuti scroll (tanpa transisi/auto-scroll).
   Intro: gedung utuh -> kamera mendekat ke puncak, atap terbuka.
   Lantai 7 -> 1: kartu konten keluar dari lantai itu (dari dalam atap untuk lantai teratas), dibaca, lalu naik pergi
   sementara kamera turun ke lantai berikutnya. Outro: kamera mundur ke gedung utuh, lalu footer. */
(function () {
  var root = document.querySelector('.gd2');
  if (!root || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  root.classList.add('gd-live');

  var story = root.querySelector('.gd-story'), stage = root.querySelector('.gd-stage');
  var bld = root.querySelector('.bx3'), world = root.querySelector('.bx3-world'), glow = root.querySelector('.bx3-glow');
  var cards = [].slice.call(root.querySelectorAll('.gc'));            // urutan 7 -> 1
  var floorEl = {};
  [].slice.call(root.querySelectorAll('.bx3-floor')).forEach(function (f) { floorEl[f.dataset.k] = f; });

  var TOTAL = 422, TILT = -22;
  function center(k) { return k === 1 ? 37 : 74 + (k - 2) * 58 + 29; }
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  var V, vw, s0, s1, xDesk, cw, cx, INTRO, SEG, OUTRO, desk;
  function layout() {
    vw = window.innerWidth; V = window.innerHeight; desk = vw >= 900;
    s0 = Math.min(V * 0.5 / 560, vw * 0.78 / 420, 1.15);
    s1 = s0 * (desk ? 1.9 : 1.55);
    cw = desk ? Math.min(560, vw * 0.42) : vw - 32;
    cx = desk ? Math.max(vw * 0.05, (vw - 1200) / 2 + 24) : 16;
    xDesk = desk ? vw * 0.71 : vw / 2;
    INTRO = 1.5 * V; SEG = 1.25 * V; OUTRO = 1.4 * V;
    story.style.setProperty('--story-h', (INTRO + cards.length * SEG + OUTRO + V) + 'px');
    cards.forEach(function (c) {
      c.style.setProperty('--cw', cw + 'px');
      c.style.setProperty('--cx', cx + 'px');
      c.style.setProperty('--ch', c.offsetHeight + 'px');
    });
  }

  function cam(s, focus, ox, oy) {
    world.style.left = ox + 'px';
    world.style.transform = 'translate3d(0,' + oy + 'px,0) scale(' + s + ') rotateX(' + TILT + 'deg) rotateY(' + (desk ? -30 : -32) + 'deg)';
  }

  function frame() {
    var g = -story.getBoundingClientRect().top;          // jarak scroll di dalam cerita
    var s, focus, ox, oy, open = 1, hero = 0, outroO = 0;

    if (g < INTRO) {                                       // intro
      var p = clamp(g / INTRO), z = ease(clamp((p - 0.03) / 0.62));
      s = lerp(s0, s1, z); focus = lerp(TOTAL / 2, TOTAL, z);
      ox = lerp(vw / 2, xDesk, z);
      oy = lerp(V * 0.93, V * 0.5 + s * focus * 0.93, z);
      open = ease(clamp((p - 0.5) / 0.4)); hero = 1 - clamp(p / 0.18);
    } else if (g < INTRO + cards.length * SEG) {           // lantai
      var x = (g - INTRO) / SEG, i = Math.min(cards.length - 1, Math.floor(x)), u = x - i;
      var k = 7 - i, from = i === 0 ? TOTAL : center(k), next = k > 1 ? center(k - 1) : center(1);
      focus = u < 0.7 ? lerp(from, center(k), ease(clamp(u / 0.3))) : lerp(center(k), next, ease((u - 0.7) / 0.3));
      s = s1; ox = xDesk; oy = V * 0.5 + s * focus * 0.93;
    } else {                                               // outro
      var q = clamp((g - INTRO - cards.length * SEG) / OUTRO), z2 = ease(clamp(q / 0.8));
      s = lerp(s1, s0, z2); focus = center(1);
      ox = lerp(xDesk, vw / 2, z2);
      oy = lerp(V * 0.5 + s * focus * 0.93, V * 0.9, z2);
      open = 1 - ease(clamp(q / 0.6)); outroO = clamp((q - 0.6) / 0.3);
    }
    cam(s, focus, ox, oy);
    bld.style.setProperty('--open', (open * 112) + 'deg');
    bld.style.setProperty('--glow', open);
    stage.style.setProperty('--hero', hero);
    stage.style.setProperty('--outro', outroO);

    // kartu: keluar dari lantainya, dibaca, lalu naik pergi
    var any = false;
    cards.forEach(function (c, idx) {
      var k = +c.dataset.k, u = (g - INTRO) / SEG - idx;
      var fl = floorEl[k];
      if (u < -0.05 || u > 1.02) { c.style.opacity = 0; c.classList.remove('act'); fl.classList.remove('lit'); return; }
      var ch = c.offsetHeight, tx0 = cx, ty0 = V / 2 - ch / 2;
      var e = ease(clamp((u + 0.05) / 0.37)), out = ease(clamp((u - 0.72) / 0.28));
      var src = (k === 7 ? glow : fl.querySelector('.fc-front')).getBoundingClientRect();
      var dx = lerp(src.left - tx0, 0, e), dy = lerp(src.top - ty0, 0, e);
      var sx = lerp(Math.max(src.width / cw, .04), 1, e), sy = lerp(Math.max(src.height / ch, .04), 1, e);
      dy -= out * V * 0.55;
      var sc = 1 - out * 0.08;
      c.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(' + (sx * sc) + ',' + (sy * sc) + ')';
      var op = Math.min(clamp(e * 3), 1 - out);
      c.style.opacity = op;
      c.classList.toggle('act', op > 0.6);
      if (op > 0.6) any = true;
      fl.classList.toggle('lit', op > 0.05);
    });
    stage.classList.toggle('has-card', any);
  }

  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; frame(); }); } }
  layout(); frame();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { layout(); frame(); });
})();
