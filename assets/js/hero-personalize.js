/* Beranda: judul hero mengikuti link kampanye (?layanan=software&kota=balikpapan, atau utm_term dari iklan),
   plus pilihan cepat "Saya mencari" yang mengikuti kota pilihan. Tanpa parameter, judul bawaan tidak berubah. */
(function () {
  'use strict';
  var CITY = { balikpapan: 'Balikpapan', samarinda: 'Samarinda', kaltim: 'Kalimantan Timur' };
  var SVC = {
    software: { t: 'Software house', g: 'di {C}.', l: 'Aplikasi web, aplikasi HP, HRIS, ERP, dan sistem internal yang dibuat mengikuti proses Anda.', h: '/software-house-{c}', b: 'Software house {C}' },
    website: { t: 'Jasa pembuatan website', g: 'di {C}.', l: 'Company profile, website instansi, dan landing page yang cepat dan mudah ditemukan di Google.', h: '/jasa-pembuatan-website-{c}', b: 'Website {C}' }
  };
  var WORDS = { software: 'software', aplikasi: 'software', 'software house': 'software', website: 'website', web: 'website' };
  var q = new URLSearchParams(location.search);
  function norm(s) { return (s || '').toLowerCase().replace(/\+/g, ' '); }
  function detect(text, dict) { text = norm(text); for (var k in dict) if (text.indexOf(k) > -1) return dict[k]; return null; }
  var term = norm(q.get('utm_term') || q.get('q') || '');
  var svc = (q.get('layanan') || '').toLowerCase(); if (!SVC[svc]) svc = detect(term, WORDS);
  var city = (q.get('kota') || '').toLowerCase(); if (!CITY[city]) city = detect(term, { balikpapan: 'balikpapan', bpp: 'balikpapan', samarinda: 'samarinda', smd: 'samarinda', kaltim: 'kaltim', 'kalimantan timur': 'kaltim' });
  var linkCity = city === 'balikpapan' ? 'balikpapan' : 'samarinda';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  if (svc && SVC[svc]) {
    var d = SVC[svc], C = CITY[city] || 'Kalimantan Timur';
    var fill = function (s) { return s.replace(/\{C\}/g, C).replace(/\{c\}/g, svc === 'software' && city === 'kaltim' ? 'kalimantan-timur' : linkCity); };
    var h1 = document.getElementById('heroTitle'), lead = document.getElementById('heroLead'), cta = document.getElementById('heroCta');
    if (h1) h1.innerHTML = esc(fill(d.t)) + '<br/><span class="grad">' + esc(fill(d.g)) + '</span>';
    if (lead) lead.textContent = fill(d.l);
    if (cta) { cta.setAttribute('href', fill(d.h)); cta.firstChild.nodeValue = fill(d.b) + ' '; }
  }

  // Pilihan cepat "Saya mencari"
  var box = document.querySelector('.hp-picks');
  if (!box) return;
  var saved = null;
  try { saved = localStorage.getItem('altora-city'); } catch (e) { /* abaikan */ }
  var cur = CITY[city] && city !== 'kaltim' ? city : (saved === 'balikpapan' ? 'balikpapan' : 'samarinda');
  function setCity(c) {
    cur = c;
    box.querySelectorAll('[data-city]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-city') === c)); });
    box.querySelectorAll('.hp-pick').forEach(function (a) { a.setAttribute('href', a.getAttribute('data-href').replace('{c}', c)); });
    try { localStorage.setItem('altora-city', c); } catch (e) { /* abaikan */ }
  }
  box.addEventListener('click', function (ev) { var b = ev.target.closest('[data-city]'); if (b) setCity(b.getAttribute('data-city')); });
  setCity(cur);
}());
