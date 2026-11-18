/* Latar "Swell" (asciify-engine 4.33.0, MIT; lihat /assets/vendor/asciify-engine.LICENSE) untuk band CTA dan footer.
   Modul ESM dimuat malas: hanya diunduh saat salah satu latar mendekati viewport. Tanpa WebGL2 atau tanpa JS,
   elemen tetap tampil sebagai gradient ungu statis (tidak ada canvas). Reduced motion: satu frame diam (ditangani pustaka).
   Footer dibuat lebih samar daripada band CTA supaya tekstur, bukan gambar utama (seperti footer situs saudara). */
const targets = [].slice.call(document.querySelectorAll('[data-swell]'));
const LOOK = {
  cta: { palette: '#B9A6FF', accent: '#FFFFFF', cellSize: 9, speed: 0.7, opacity: 0.75 },
  footer: { palette: '#9A80F5', accent: '#D6C8FF', cellSize: 9, speed: 0.5, opacity: 0.45 },
};
if (targets.length) {
  let kit = null;
  const mount = (el) => {
    const host = el.closest('section,footer') || el;
    const copy = host.querySelector('[data-swell-clear]');
    const look = LOOK[el.getAttribute('data-swell')] || LOOK.cta;
    const bg = kit.background(el, Object.assign({ preset: kit.swell, mark: 'dot', clear: copy || false, cursor: false, lazy: true }, look));
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
