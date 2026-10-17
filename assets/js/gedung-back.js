/* Halaman lantai (Karier, Layanan, ... Support): di puncak halaman, scroll ke atas menampilkan pil
   "scroll lagi untuk kembali ke gedung"; usapan ke atas berikutnya membuka beranda yang mundur
   dari layar lantai ini ke menu lantai (assets/js/gedung3d.js membaca sessionStorage 'gdBack'). */
(function () {
  var MAP = { careers: 8, services: 7, produk: 6, portfolio: 5, blog: 4, about: 3, katalog: 2, support: 1 };
  var k = MAP[location.pathname.replace(/^\/|\.html$|\/$/g, '')];
  if (!k || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var armed = 0, last = 0, hint = null, hideT = 0, ty0 = null;
  function pill() {
    if (hint) return hint;
    hint = document.createElement('div');
    hint.setAttribute('role', 'status');
    hint.style.cssText = 'position:fixed;left:50%;top:96px;z-index:60;transform:translate(-50%,-8px);opacity:0;pointer-events:none;' +
      'background:#fff;border:1px solid #E4DEFA;color:#3E2A97;border-radius:999px;padding:9px 18px;font:600 .875rem/1.2 "Plus Jakarta Sans",system-ui,sans-serif;' +
      'box-shadow:0 14px 34px -24px rgba(43,30,110,.45);transition:opacity .25s,transform .25s;white-space:nowrap';
    hint.textContent = '↑ Scroll lagi untuk kembali ke gedung Altora';
    document.body.appendChild(hint);
    return hint;
  }
  function show(on) {
    var h = pill(); h.style.opacity = on ? 1 : 0; h.style.transform = 'translate(-50%,' + (on ? 0 : -8) + 'px)';
    clearTimeout(hideT); if (on) hideT = setTimeout(function () { armed = 0; show(false); }, 3500);
  }
  function up(gap) {
    if (scrollY > 2) return;
    var now = performance.now();
    if (!armed) { armed = now; show(true); return; }
    if (now - armed < 600 || gap < 280) return;                       // sisa momentum usapan pertama tidak dihitung
    try { sessionStorage.setItem('gdBack', String(k)); } catch (e) {}
    location.href = '/';
  }
  addEventListener('wheel', function (e) {
    var now = performance.now(), gap = now - last; last = now;
    if (e.deltaY < -4) up(gap); else if (e.deltaY > 4 && armed) { armed = 0; show(false); }
  }, { passive: true });
  addEventListener('touchstart', function (e) { ty0 = e.touches[0].clientY; }, { passive: true });
  addEventListener('touchmove', function (e) {
    if (ty0 === null) return;
    var dy = e.touches[0].clientY - ty0;
    if (dy > 40) { ty0 = null; up(1e9); } else if (dy < -40 && armed) { ty0 = null; armed = 0; show(false); }
  }, { passive: true });
})();
