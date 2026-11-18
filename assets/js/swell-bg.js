/* Latar "Swell" (asciify-engine 4.33.0, MIT; lihat /assets/vendor/asciify-engine.LICENSE) untuk band CTA dan footer.
   Modul ESM dimuat malas: hanya diunduh saat salah satu latar mendekati viewport. Tanpa WebGL2 atau tanpa JS,
   elemen tetap tampil sebagai gradient ungu statis (tidak ada canvas). Reduced motion: satu frame diam (ditangani pustaka). */
const targets = [].slice.call(document.querySelectorAll('[data-swell]'));
if (targets.length) {
  const ink = '#8F72F2', accent = '#FFFFFF';
  let kit = null;
  const mount = (el) => {
    const host = el.closest('section,footer') || el;
    const copy = host.querySelector('[data-swell-clear]');
    const bg = kit.background(el, {
      preset: kit.swell, palette: ink, accent: accent, mark: 'dot', cellSize: 8, speed: 0.8, opacity: 1,
      clear: copy || false, cursor: false, lazy: true,
    });
    el.setAttribute('data-swell-state', 'loading');
    setTimeout(() => el.setAttribute('data-swell-state', bg.supported ? 'on' : 'off'), 2000);
  };
  const load = () => import('/assets/vendor/asciify-swell.min.js?v=20261118a').then((m) => { kit = m; targets.forEach(mount); }).catch(() => {});
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((es) => {
      if (es.some((x) => x.isIntersecting)) { io.disconnect(); load(); }
    }, { rootMargin: '600px 0px' });
    targets.forEach((t) => io.observe(t));
  } else load();
}
