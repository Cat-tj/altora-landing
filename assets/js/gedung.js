/* Prototipe "gedung yang dibangun": lantai menyala sesuai section yang sedang dibaca. */
(function () {
  var page = document.querySelector('.gd-page');
  if (!page) return;
  var secs = [].slice.call(document.querySelectorAll('.gd-sec[data-floor]'));
  var floors = [].slice.call(document.querySelectorAll('.fl'));
  var hook = document.querySelector('.crane .hook');
  var box = document.querySelector('.crane .hook-box');
  var prog = document.querySelector('.gd-progress');
  var svg = document.querySelector('.gd-svg');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var max = floors.length - 1;

  function topY(level) {
    // y layar atas lantai 'level' (dibaca dari polygon atap lantai itu)
    var f = floors[Math.max(0, level)];
    if (!f) return 560;
    var t = f.querySelector('.fl-top');
    var ys = t.getAttribute('points').split(' ').map(function (pt) { return +pt.split(',')[1]; });
    return Math.min.apply(null, ys);
  }

  function setLevel(level) {
    if (reduce) level = max;
    page.setAttribute('data-level', level);
    floors.forEach(function (f, i) {
      f.classList.toggle('on', i <= level);
      f.classList.toggle('active', i === level);
    });
    secs.forEach(function (s) { s.classList.toggle('is-on', +s.dataset.floor === level); });
    if (prog) prog.style.setProperty('--prog', Math.round(((level + 1) / (max + 1)) * 100) + '%');
    if (hook && box) {
      var target = level < 0 ? 470 : topY(level) - 50;
      var y2 = Math.max(80, target);
      hook.setAttribute('y2', y2);
      box.setAttribute('y', y2);
    }
  }

  var current = -2;
  function onScroll() {
    var mid = window.innerHeight * (window.innerWidth < 900 ? 0.72 : 0.55), level = -1;
    secs.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top < mid) level = +s.dataset.floor;
    });
    if (level !== current) { current = level; setLevel(level); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();
