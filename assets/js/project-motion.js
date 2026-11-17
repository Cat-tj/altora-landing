/* Altora project motion: story pacing, no scroll listeners. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var page = document.querySelector('.project-page');
  if (!page || reduce) return;

  page.classList.add('motion-ready');
  var targets = document.querySelectorAll('.project-hero > *, .project-section > .project-wrap');
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('in-view'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -7% 0px' });

  targets.forEach(function (el) { observer.observe(el); });

  document.querySelectorAll('.project-photo-story figure, .project-evidence figure').forEach(function (figure) {
    figure.addEventListener('pointerenter', function () { figure.classList.add('is-focused'); });
    figure.addEventListener('pointerleave', function () { figure.classList.remove('is-focused'); });
  });
}());
