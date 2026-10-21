/* Halaman lantai (Karier, Layanan, ... Support): jalan kembali ke gedung di beranda, yang mundur dari layar
   lantai ini ke menu lantai (assets/js/gedung3d.js membaca sessionStorage 'gdBack'):
   - di puncak halaman: scroll ke atas -> pil "scroll lagi", usapan ke atas berikutnya kembali ke gedung
   - di ujung bawah halaman (selesai melihat-lihat): sama, dengan scroll ke bawah
   - tombol "Kembali ke gedung" di kiri bawah setelah halaman di-scroll */
(function () {
  var MAP = { careers: 6, services: 5, blog: 4, about: 3, katalog: 2, support: 1 };
  var k = MAP[location.pathname.replace(/^\/|\.html$|\/$/g, '')];
  if (!k || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var FONT = 'font:600 .875rem/1.2 "Plus Jakarta Sans",system-ui,sans-serif;';
  var armed = 0, dir = 0, last = 0, gest = 0, armGest = 0, hint = null, hideT = 0, ty0 = null;
  function go() {
    try { sessionStorage.setItem('gdBack', String(k)); } catch (e) {}
    location.href = '/';
  }
  function pill() {
    if (hint) return hint;
    hint = document.createElement('div');
    hint.setAttribute('role', 'status');
    hint.style.cssText = 'position:fixed;left:50%;z-index:60;opacity:0;pointer-events:none;background:#fff;border:1px solid #E4DEFA;color:#3E2A97;' +
      'border-radius:999px;padding:9px 18px;' + FONT + 'box-shadow:0 14px 34px -24px rgba(43,30,110,.45);transition:opacity .25s,transform .25s;white-space:nowrap';
    document.body.appendChild(hint);
    return hint;
  }
  function show(on, d) {
    var h = pill();
    if (on) {
      h.textContent = (d < 0 ? '↑' : '↓') + ' Scroll lagi untuk kembali ke gedung Altora';
      h.style.top = d < 0 ? '96px' : 'auto'; h.style.bottom = d < 0 ? 'auto' : '96px';
    }
    h.style.opacity = on ? 1 : 0; h.style.transform = 'translate(-50%,' + (on ? 0 : d < 0 ? -8 : 8) + 'px)';
    clearTimeout(hideT); if (on) hideT = setTimeout(reset, 3500);
  }
  function reset() { if (armed) show(false, dir); armed = 0; dir = 0; }
  var atTop = function () { return scrollY <= 2; };
  var atEnd = function () { return innerHeight + scrollY >= document.documentElement.scrollHeight - 4; };
  function push(d) {                                                   // d: -1 ke atas, 1 ke bawah
    if (!(d < 0 ? atTop() : atEnd())) { if (armed) reset(); return; }
    var now = performance.now();
    if (!armed || dir !== d) { if (armed) reset(); armed = now; dir = d; armGest = gest; show(true, d); return; }
    if (gest === armGest || now - armed < 500) return;                  // harus usapan berikutnya, bukan sisa usapan yang memunculkan pil
    go();
  }
  addEventListener('wheel', function (e) {
    var now = performance.now();
    if (now - last >= 120) gest++;                                      // usapan baru = ada jeda (sisa momentum mengalir tanpa jeda)
    last = now;
    if (e.deltaY < -4) push(-1); else if (e.deltaY > 4) push(1);
  }, { passive: true });
  addEventListener('touchstart', function (e) { ty0 = e.touches[0].clientY; }, { passive: true });
  addEventListener('touchmove', function (e) {
    if (ty0 === null) return;
    var dy = e.touches[0].clientY - ty0;
    if (dy > 40) { ty0 = null; gest++; push(-1); } else if (dy < -40) { ty0 = null; gest++; push(1); }
  }, { passive: true });

  // tombol tetap "Kembali ke gedung"
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Kembali ke gedung Altora di beranda');
  btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M11 21v-3h2v3"/></svg><span>Kembali ke gedung</span>';
  btn.style.cssText = 'position:fixed;left:16px;bottom:24px;z-index:59;display:inline-flex;align-items:center;gap:8px;cursor:pointer;background:#fff;color:#3E2A97;' +
    'border:1px solid #E4DEFA;border-radius:999px;padding:10px 16px;' + FONT + 'box-shadow:0 14px 34px -24px rgba(43,30,110,.45);' +
    'opacity:0;transform:translateY(12px);pointer-events:none;transition:opacity .25s,transform .25s';
  btn.addEventListener('click', go);
  function vis() {
    var on = scrollY > innerHeight * 0.6 && innerHeight + scrollY < document.documentElement.scrollHeight - 140;   // tidak menutupi tautan footer
    btn.style.opacity = on ? 1 : 0; btn.style.transform = on ? 'none' : 'translateY(12px)'; btn.style.pointerEvents = on ? 'auto' : 'none';
  }
  function mount() { document.body.appendChild(btn); vis(); }
  if (document.body) mount(); else addEventListener('DOMContentLoaded', mount);
  addEventListener('scroll', vis, { passive: true });
})();
