/* Prototipe "halaman = gedung" (3D): zoom ke puncak, atap terbuka, panel terbang keluar lalu auto-scroll ke lantai 7;
   lantai terbuka satu per satu; di akhir zoom out ke gedung utuh dengan footer di bawahnya. */
(function () {
  var root = document.querySelector('.gd2');
  if (!root) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var intro = root.querySelector('.gd-intro'), outro = root.querySelector('.gd-outro');
  var sIn = intro.querySelector('.gd-scene'), sOut = outro.querySelector('.gd-scene');
  var wIn = intro.querySelector('.bx3-world'), wOut = outro.querySelector('.bx3-world');
  var bIn = intro.querySelector('.bx3'), glow = intro.querySelector('.bx3-glow');
  var floorsWrap = root.querySelector('.gd-floors');
  var floors = [].slice.call(root.querySelectorAll('.gf'));
  var fly = root.querySelector('.gd-fly');
  var lift = root.querySelector('.gd-lift'), liftNum = lift.querySelector('b');
  var TOTAL = 422, LOBBY_C = 37, TILT = -22;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function progress(sec) {
    var r = sec.getBoundingClientRect(), span = sec.offsetHeight - window.innerHeight;
    return clamp(-r.top / span);
  }
  var vw, vh, s0;
  function layout() {
    vw = window.innerWidth; vh = window.innerHeight;
    s0 = Math.min(vh * 0.5 / 560, vw * 0.78 / 420, 1.15);
  }
  function cam(world, s, originY, ry) {
    world.style.transform = 'translate3d(0,' + originY + 'px,0) scale(' + s + ') rotateX(' + TILT + 'deg) rotateY(' + ry + 'deg)';
  }

  var flown = false, flying = false, lastY = window.scrollY;
  function frame() {
    // intro
    var p = progress(intro);
    var z = ease(clamp((p - 0.04) / 0.56));
    var s = s0 * (1 + 1.6 * z);
    var y0 = vh * 0.93, y1 = vh * 0.46 + s * TOTAL * 0.93;
    cam(wIn, s, lerp(y0, y1, z), lerp(-34, -24, z));
    var o = ease(clamp((p - 0.5) / 0.28));
    bIn.style.setProperty('--open', (o * 112) + 'deg');
    bIn.style.setProperty('--glow', o);
    sIn.style.setProperty('--hero', 1 - clamp(p / 0.2));
    var down = window.scrollY > lastY; lastY = window.scrollY;
    if (p < 0.45) flown = false;
    if (p >= 0.999) flown = true;           // sudah lewat intro (reload / lompat lewat tautan): jangan terbang
    if (!flown && !flying && down && p >= 0.8) flyIn();

    // outro: dari dekat lobi, mundur sampai gedung utuh
    var q = progress(outro);
    var zo = ease(clamp(q / 0.75));
    var so = lerp(s0 * 2.4, s0, zo);
    var yStart = vh * 0.55 + so * LOBBY_C, yEnd = vh * 0.88;
    cam(wOut, so, lerp(yStart, yEnd, zo), lerp(-20, -34, zo));
    sOut.style.setProperty('--outro', clamp((q - 0.65) / 0.25));

    // lift
    var mid = vh * 0.5, cur = null;
    floors.forEach(function (fl) { var r = fl.getBoundingClientRect(); if (r.top < mid && r.bottom > mid) cur = fl.dataset.k; });
    lift.classList.toggle('on', !!cur);
    if (cur) liftNum.textContent = cur;
  }

  // panel keluar dari lantai teratas -> layar penuh, lalu halaman diletakkan tepat di lantai 7
  function flyIn() {
    flying = true;
    var r = glow.getBoundingClientRect();
    var html = document.documentElement, prevOv = html.style.overflow;
    html.style.overflow = 'hidden';
    fly.classList.add('on');
    var from = 'translate(' + r.left + 'px,' + r.top + 'px) scale(' + Math.max(r.width / vw, .05) + ',' + Math.max(r.height / vh, .05) + ')';
    var anim = fly.animate([
      { transform: from, borderRadius: '18px', opacity: .0 },
      { transform: from, borderRadius: '18px', opacity: 1, offset: .12 },
      { transform: 'translate(0,0) scale(1,1)', borderRadius: '0px', opacity: 1 }
    ], { duration: 950, easing: 'cubic-bezier(.65,0,.25,1)', fill: 'forwards' });
    anim.onfinish = function () {
      var top = floorsWrap.getBoundingClientRect().top + window.scrollY;
      html.style.overflow = prevOv;
      window.scrollTo({ top: top, behavior: 'instant' });
      flown = true;
      var out = fly.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 260, easing: 'ease-out', fill: 'forwards' });
      out.onfinish = function () { fly.classList.remove('on'); anim.cancel(); out.cancel(); flying = false; };
    };
  }

  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) en.target.classList.add('open'); });
    }, { threshold: 0.2 });
    floors.forEach(function (fl) { io.observe(fl); });
  } else {
    floors.forEach(function (fl) { fl.classList.add('open'); });
  }

  layout();
  if (reduce) { cam(wIn, s0, vh * 0.6, -32); cam(wOut, s0, vh * 0.6, -32); return; }
  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; frame(); }); } }
  frame();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { layout(); frame(); });
})();
