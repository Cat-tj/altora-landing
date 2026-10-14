/* Beranda: judul hero mengikuti link kampanye (?layanan=cctv&kota=balikpapan, atau utm_term dari iklan),
   plus pilihan cepat "Saya mencari" yang mengikuti kota pilihan. Tanpa parameter, judul bawaan tidak berubah. */
(function () {
  'use strict';
  var CITY = { balikpapan: 'Balikpapan', samarinda: 'Samarinda', kaltim: 'Kalimantan Timur' };
  var SVC = {
    cctv: { t: 'Pengadaan & pasang CCTV', g: 'di {C}.', l: 'Kamera VIGI, NVR, dan CCTV pintar dengan AI. Kami survei, pasang, dan rawat oleh tim lokal.', h: '/jual-cctv-{c}', b: 'Lihat CCTV di {C}' },
    software: { t: 'Software house', g: 'di {C}.', l: 'Aplikasi web, aplikasi HP, HRIS, ERP, dan sistem internal yang dibuat mengikuti proses Anda.', h: '/software-house-{c}', b: 'Software house {C}' },
    pengadaan: { t: 'Pengadaan perangkat IT', g: 'untuk instansi di {C}.', l: 'Laptop, PC, server, CCTV, dan jaringan resmi bergaransi. PKP dan terdaftar di Inaproc/LKPP.', h: '/katalog#v-pengadaan', b: 'Lihat katalog pengadaan' },
    jaringan: { t: 'Instalasi jaringan & WiFi', g: 'di {C}.', l: 'LAN, WiFi kantor, fiber optik, rak server, dan wireless bridge antar gedung.', h: '/jasa-instalasi-jaringan-{c}', b: 'Jaringan & WiFi {C}' },
    website: { t: 'Jasa pembuatan website', g: 'di {C}.', l: 'Company profile, website instansi, dan landing page yang cepat dan mudah ditemukan di Google.', h: '/jasa-pembuatan-website-{c}', b: 'Website {C}' },
    starlink: { t: 'Jual & pasang Starlink', g: 'di {C}.', l: 'Kit Starlink, instalasi, Wi-Fi merata, dan tenaga surya untuk lokasi tanpa PLN.', h: '/jual-starlink-{c}', b: 'Starlink {C}' },
    gps: { t: 'GPS tracker kendaraan', g: 'di {C}.', l: 'Pantau armada, BBM, dan data mesin dengan perangkat Teltonika dan Altora FMS.', h: '/gps-tracker-kendaraan-{c}', b: 'GPS tracker {C}' },
    itsupport: { t: 'IT support', g: 'di {C}.', l: 'Komputer, jaringan, server, dan CCTV kantor, dibantu lewat WhatsApp atau teknisi datang.', h: '/it-support-{c}', b: 'IT support {C}' },
    smartlock: { t: 'Jual & pasang smartlock', g: 'di {C}.', l: 'Kunci pintu digital untuk rumah, kantor, dan kampus, dikelola dari satu aplikasi.', h: '/jual-smartlock-{c}', b: 'Smartlock {C}' }
  };
  var WORDS = { cctv: 'cctv', kamera: 'cctv', software: 'software', aplikasi: 'software', 'software house': 'software', pengadaan: 'pengadaan', laptop: 'pengadaan', server: 'pengadaan',
    jaringan: 'jaringan', wifi: 'jaringan', fiber: 'jaringan', website: 'website', web: 'website', starlink: 'starlink', gps: 'gps', armada: 'gps', 'it support': 'itsupport', smartlock: 'smartlock' };
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
