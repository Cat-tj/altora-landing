/* Prototipe "halaman = gedung" model rumah boneka. Semua mengikuti scroll (tanpa transisi/auto-scroll):
   intro: gedung utuh -> kamera mendekat dari atas, atap terangkat;
   lantai 7 -> 1: kita melihat ke dalam lantai, kartu konten berdiri dari lantainya; scroll lanjut -> lantai itu
   terangkat bersama isinya dan lantai di bawahnya terlihat;
   outro: semua lantai turun kembali, atap menutup, kamera mundur, lalu footer. */
(function () {
  var root = document.querySelector('.gd2');
  if (!root || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  root.classList.add('gd-live');

  var story = root.querySelector('.gd-story'), stage = root.querySelector('.gd-stage');
  var world = root.querySelector('.bx3-world'), roof = root.querySelector('.bx3-roof');
  var cards = [].slice.call(root.querySelectorAll('.gc'));               // urutan 7 -> 1
  var floors = {}, plate = {};
  [].slice.call(root.querySelectorAll('.bx3-floor')).forEach(function (f) {
    var k = +f.dataset.k;
    floors[k] = { el: f, y: parseFloat(f.style.getPropertyValue('--y')), h: parseFloat(f.style.getPropertyValue('--h')) };
    plate[k] = f.querySelector('.fc-plate');
  });

  var TOTAL = 422, RY = -35, LIFT = 560;
  function base(k) { return floors[k].y; }                                // tinggi pelat lantai k dari tanah
  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  var V, vw, s0, s1, cw, INTRO, SEG, OUTRO, ty;
  function layout() {
    vw = window.innerWidth; V = window.innerHeight;
    var desk = vw >= 900;
    s0 = Math.min(V * 0.5 / 560, vw * 0.78 / 420, 1.15);
    s1 = (desk ? Math.min(vw * 0.6, 720) : vw * 0.84) / 294;
    cw = desk ? Math.min(640, vw * 0.5) : vw - 32;
    ty = desk ? 0.72 : 0.76;
    INTRO = 1.6 * V; SEG = 1.3 * V; OUTRO = 1.7 * V;
    story.style.setProperty('--story-h', (INTRO + cards.length * SEG + OUTRO + V) + 'px');
    cards.forEach(function (c) { c.style.setProperty('--cw', cw + 'px'); });
  }

  function setFloor(k, lift) {
    var f = floors[k];
    f.el.style.transform = 'translateY(' + (-(f.y + f.h / 2) - lift * LIFT) + 'px)';
    f.el.style.setProperty('--fo', 1 - clamp(lift * 1.25));
  }
  function setRoof(lift) {
    roof.style.transform = 'translateY(' + (-TOTAL - lift * LIFT) + 'px)';
    roof.style.setProperty('--fo', 1 - clamp(lift * 1.25));
  }
  function cam(s, rx, Y) {
    var cos = Math.cos(rx * Math.PI / 180);
    var oy = Y === null ? V * 0.9 : V * ty + s * Y * cos;
    world.style.transform = 'translate3d(0,' + oy + 'px,0) scale(' + s + ') rotateX(' + rx + 'deg) rotateY(' + RY + 'deg)';
    return oy;
  }

  function frame() {
    var g = -story.getBoundingClientRect().top;
    var N = cards.length, lifts = {}, roofLift = 0, hero = 0, outroO = 0, cardState = {};
    var k;
    for (k = 1; k <= 7; k++) lifts[k] = 0;

    if (g < INTRO) {
      var p = clamp(g / INTRO), z = ease(clamp((p - 0.03) / 0.6));
      var s = lerp(s0, s1, z), rx = lerp(-22, -38, z);
      var cos = Math.cos(rx * Math.PI / 180);
      var oy = lerp(V * 0.9, V * ty + s * base(7) * cos, z);
      world.style.transform = 'translate3d(0,' + oy + 'px,0) scale(' + s + ') rotateX(' + rx + 'deg) rotateY(' + RY + 'deg)';
      roofLift = ease(clamp((p - 0.5) / 0.42));
      hero = 1 - clamp(p / 0.18);
      cardState[7] = { pop: ease(clamp((p - 0.88) / 0.12)) * 0.25, gone: 0 };
    } else if (g < INTRO + N * SEG) {
      var x = (g - INTRO) / SEG, i = Math.min(N - 1, Math.floor(x)), u = x - i;
      var cur = 7 - i, peel = cur > 1 ? ease(clamp((u - 0.72) / 0.28)) : 0;
      for (k = cur + 1; k <= 7; k++) lifts[k] = 1;
      lifts[cur] = peel;
      roofLift = 1;
      var Y = cur > 1 ? lerp(base(cur), base(cur - 1), peel) : base(1);
      cam(s1, -38, Y);
      cardState[cur] = { pop: i === 0 ? lerp(0.25, 1, ease(clamp(u / 0.18))) : ease(clamp(u / 0.22)), gone: peel };
      if (cur > 1 && peel > 0) cardState[cur - 1] = { pop: 0, gone: 0 };
    } else {
      var q = clamp((g - INTRO - N * SEG) / OUTRO), z2 = ease(clamp(q / 0.8));
      for (k = 2; k <= 7; k++) lifts[k] = 1 - ease(clamp((q * 1.7 - (k - 2) * 0.1) / 0.45));
      roofLift = 1 - ease(clamp((q * 1.7 - 0.7) / 0.45));
      var so = lerp(s1, s0, z2), rxo = lerp(-38, -22, z2);
      var coso = Math.cos(rxo * Math.PI / 180);
      world.style.transform = 'translate3d(0,' + lerp(V * ty, V * 0.9, z2) + 'px,0) scale(' + so + ') rotateX(' + rxo + 'deg) rotateY(' + RY + 'deg)';
      outroO = clamp((q - 0.65) / 0.25);
      cardState[1] = { pop: 1, gone: clamp(q / 0.15) };
    }
    for (k = 1; k <= 7; k++) setFloor(k, lifts[k]);
    setRoof(roofLift);
    stage.style.setProperty('--hero', hero);
    stage.style.setProperty('--outro', outroO);

    // kartu berdiri dari pelat lantainya dan ikut terangkat saat lantainya dikupas
    cards.forEach(function (c) {
      var kk = +c.dataset.k, st = cardState[kk];
      if (!st || st.pop <= 0.001 || st.gone >= 0.999) { c.style.opacity = 0; c.classList.remove('act'); return; }
      var r = plate[kk].getBoundingClientRect();
      var ch = c.offsetHeight, px = r.left + r.width / 2, py = r.top + r.height * 0.62;
      var left = Math.max(16, Math.min(vw - cw - 16, px - cw / 2));
      var top = Math.max(88, py - ch);
      var sy = lerp(0.03, 1, st.pop), sx = lerp(0.6, 1, st.pop);
      c.style.transform = 'translate(' + left + 'px,' + top + 'px) scale(' + sx + ',' + sy + ')';
      var op = Math.min(clamp(st.pop * 2.2), 1 - clamp(st.gone * 1.4));
      c.style.opacity = op;
      c.classList.toggle('act', op > 0.6);
    });
  }

  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; frame(); }); } }
  layout(); frame();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { layout(); frame(); });
})();
