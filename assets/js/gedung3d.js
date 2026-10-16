/* Prototipe "halaman = gedung" versi Three.js (WebGL + CSS3D).
   Gedung kaca 7 lantai dengan cahaya, bayangan, dan pantulan; papan konten adalah HTML asli (CSS3DRenderer)
   yang berdiri di dalam lantainya. Semua digerakkan oleh scroll:
   intro (gedung utuh -> kamera mendekat, atap terangkat) -> lantai 7..1 (papan berdiri, lantai dikupas ke atas)
   -> outro (lantai turun kembali, kamera mundur, footer). */
import * as THREE from 'three';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const root = document.querySelector('.gd2');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (root && !reduce && webglOK()) init();

function webglOK() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
}

function init() {
  root.classList.add('gd-live', 'gd-3d');
  const story = root.querySelector('.gd-story'), stage = root.querySelector('.gd-stage');
  const cards = [...root.querySelectorAll('.gc')];                       // urutan 7 -> 1

  // ── ukuran gedung (meter) ──
  const W = 24, D = 17, FH = 4, LOBBY = 5.5, N = 7, SLAB = 0.5;
  const base = k => (k === 1 ? 0 : LOBBY + (k - 2) * FH);
  const height = k => (k === 1 ? LOBBY : FH);
  const TOTAL = LOBBY + (N - 1) * FH;

  // ── renderer ──
  const BG = 0xFBF9FE;
  const gl = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  const mobile = innerWidth < 900;
  gl.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.5 : 1.75));
  gl.setClearColor(BG, 1);
  gl.shadowMap.enabled = true;
  gl.shadowMap.type = THREE.PCFSoftShadowMap;
  gl.toneMapping = THREE.ACESFilmicToneMapping;
  gl.toneMappingExposure = 1.05;
  gl.outputColorSpace = THREE.SRGBColorSpace;
  gl.domElement.className = 'gd-canvas';
  stage.prepend(gl.domElement);
  const css = new CSS3DRenderer();
  css.domElement.className = 'gd-css3d';
  stage.appendChild(css.domElement);

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(BG, 140, 320);
  const pmrem = new THREE.PMREMGenerator(gl);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(32, 1, 0.5, 900);

  // ── cahaya ──
  scene.add(new THREE.HemisphereLight(0xF4F0FF, 0xCFC3FA, 0.9));
  const sun = new THREE.DirectionalLight(0xFFF4E6, 2.2);
  sun.position.set(40, 70, 45);
  sun.castShadow = true;
  sun.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(sun.shadow.camera, { left: -45, right: 45, top: 60, bottom: -20, near: 10, far: 200 });
  sun.shadow.camera.updateProjectionMatrix();
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.03;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0xC9BCFA, 0.6);
  fill.position.set(-50, 30, -20);
  scene.add(fill);

  // ── material dasar ──
  const M = {
    glass: new THREE.MeshPhysicalMaterial({ color: 0x8C76F2, roughness: 0.06, metalness: 0.15, transparent: true, opacity: 0.5, envMapIntensity: 1.4, clearcoat: 1, clearcoatRoughness: 0.08 }),
    frame: new THREE.MeshStandardMaterial({ color: 0x3E2A97, roughness: 0.45, metalness: 0.35 }),
    slab: new THREE.MeshStandardMaterial({ color: 0xFBFAFF, roughness: 0.6 }),
    light: new THREE.MeshStandardMaterial({ color: 0xFFE7A3, emissive: 0xFFD27A, emissiveIntensity: 1.1 }),
    wall: new THREE.MeshStandardMaterial({ color: 0xEDE7FF, roughness: 0.9 }),
    roof: new THREE.MeshStandardMaterial({ color: 0x5B3FC4, roughness: 0.5, metalness: 0.2 }),
    hvac: new THREE.MeshStandardMaterial({ color: 0xE4DEFA, roughness: 0.5, metalness: 0.4 }),
  };
  // lantai bagian dalam: ubin
  const tile = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128;
    const x = c.getContext('2d'); x.fillStyle = '#F6F2FF'; x.fillRect(0, 0, 128, 128);
    x.strokeStyle = 'rgba(124,92,232,.16)'; x.lineWidth = 2; x.strokeRect(0, 0, 128, 128);
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(W / 3, D / 3); t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  M.floor = new THREE.MeshStandardMaterial({ map: tile, roughness: 0.8 });

  const at = (m, x, y, z) => { m.position.set(x, y, z); return m; };
  const box = (w, h, d, mat, cast = true, recv = true) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.castShadow = cast; m.receiveShadow = recv; return m;
  };

  // ── lantai ──
  const floors = {};
  for (let k = 1; k <= N; k++) {
    const h = height(k), g = new THREE.Group(), mats = {};
    for (const key in M) { mats[key] = M[key].clone(); mats[key].transparent = true; }
    // pelat lantai (sedikit menonjol) + permukaan dalam
    g.add(at(box(W + 1.2, SLAB, D + 1.2, mats.slab), 0, SLAB / 2, 0));
    const inner = new THREE.Mesh(new THREE.PlaneGeometry(W - 0.6, D - 0.6), mats.floor);
    inner.rotation.x = -Math.PI / 2; inner.position.y = SLAB + 0.01; inner.receiveShadow = true; g.add(inner);
    // dinding kaca (depan, belakang, kiri, kanan)
    const gh = h - SLAB;
    const glassY = SLAB + gh / 2;
    [[0, D / 2, W, 0.12], [0, -D / 2, W, 0.12]].forEach(([x, z, w, t]) => g.add(at(box(w, gh, t, mats.glass, false, false), x, glassY, z)));
    [[W / 2, 0], [-W / 2, 0]].forEach(([x, z]) => g.add(at(box(0.12, gh, D, mats.glass, false, false), x, glassY, z)));
    // kusen vertikal
    for (let i = 0; i <= 8; i++) {
      const x = -W / 2 + (i * W) / 8;
      g.add(at(box(0.28, gh, 0.28, mats.frame), x, glassY, D / 2));
      g.add(at(box(0.28, gh, 0.28, mats.frame), x, glassY, -D / 2));
    }
    for (let i = 1; i < 6; i++) {
      const z = -D / 2 + (i * D) / 6;
      g.add(at(box(0.28, gh, 0.28, mats.frame), W / 2, glassY, z));
      g.add(at(box(0.28, gh, 0.28, mats.frame), -W / 2, glassY, z));
    }
    // dinding dalam belakang (supaya ruangan terasa) + lampu hangat di beberapa jendela
    g.add(at(box(W - 0.6, gh, 0.2, mats.wall, false, true), 0, glassY, -D / 2 + 0.4));
    if (k > 1) {
      [[-7.5, 0.6], [4.5, 0.9], [9, 0.4]].forEach(([x, on], i) => {
        if ((k + i) % 2 === 0 || on > 0.8) g.add(at(box(2.6, gh - 0.8, 0.1, mats.light, false, false), x, glassY, D / 2 - 0.35));
      });
    } else {
      // lobi: pintu
      g.add(at(box(5, gh - 0.6, 0.3, mats.frame), 0, SLAB + (gh - 0.6) / 2, D / 2 + 0.05));
      g.add(at(box(4.2, gh - 1.1, 0.32, mats.light), 0, SLAB + (gh - 1.1) / 2, D / 2 + 0.06));
    }
    g.position.y = base(k);
    scene.add(g);
    floors[k] = { g, mats, h };
  }

  // ── atap ──
  const roof = new THREE.Group(), roofMats = {};
  for (const key of ['roof', 'hvac', 'frame', 'light', 'slab']) { roofMats[key] = M[key].clone(); roofMats[key].transparent = true; }
  roof.add(at(box(W + 1.2, 0.9, D + 1.2, roofMats.roof), 0, 0.45, 0));
  roof.add(at(box(W + 1.2, 1.2, 0.4, roofMats.slab), 0, 1.5, D / 2 + 0.4));
  roof.add(at(box(W + 1.2, 1.2, 0.4, roofMats.slab), 0, 1.5, -D / 2 - 0.4));
  roof.add(at(box(0.4, 1.2, D + 1.2, roofMats.slab), W / 2 + 0.4, 1.5, 0));
  roof.add(at(box(0.4, 1.2, D + 1.2, roofMats.slab), -W / 2 - 0.4, 1.5, 0));
  [[-6, -3], [-1, -4], [6, 2]].forEach(([x, z]) => roof.add(at(box(3.4, 1.8, 2.6, roofMats.hvac), x, 1.8, z)));
  const mast = at(box(0.25, 7, 0.25, roofMats.frame), 8, 4.4, -4); roof.add(mast);
  const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.45, 16, 12), new THREE.MeshStandardMaterial({ color: 0xFF6B9A, emissive: 0xFF3D7F, emissiveIntensity: 2, transparent: true }));
  beacon.position.set(8, 8.1, -4); roof.add(beacon);
  // papan nama ALTORA
  const signTex = (() => {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 220;
    const x = c.getContext('2d'); x.fillStyle = '#ffffff'; x.fillRect(0, 0, 1024, 220);
    x.fillStyle = '#5B3FC4'; x.font = '800 150px "Plus Jakarta Sans", system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle';
    x.letterSpacing = '30px'; x.fillText('ALTORA', 512, 118);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  })();
  const signMat = new THREE.MeshStandardMaterial({ map: signTex, emissive: 0xffffff, emissiveMap: signTex, emissiveIntensity: 0.35, transparent: true });
  const sign = new THREE.Mesh(new THREE.BoxGeometry(12, 2.6, 0.3), [roofMats.frame, roofMats.frame, roofMats.frame, roofMats.frame, signMat, roofMats.frame]);
  sign.position.set(-1, 3.6, D / 2 - 1.2); sign.castShadow = true; roof.add(sign);
  const signPoles = [-5.5, 3.5].map(x => at(box(0.25, 2.4, 0.25, roofMats.frame), x, 1.6, D / 2 - 1.2));
  signPoles.forEach(p => roof.add(p));
  roof.position.y = TOTAL;
  scene.add(roof);
  const roofAll = [...Object.values(roofMats), signMat, beacon.material];

  // ── lingkungan: tanah, jalan, pohon, gedung latar ──
  const ground = new THREE.Mesh(new THREE.CircleGeometry(260, 64), new THREE.MeshStandardMaterial({ color: 0xF3EFFE, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const plaza = new THREE.Mesh(new THREE.BoxGeometry(W + 16, 0.3, D + 16), new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.9 }));
  plaza.position.y = 0.15; plaza.receiveShadow = true; scene.add(plaza);
  const road = new THREE.Mesh(new THREE.BoxGeometry(260, 0.1, 9), new THREE.MeshStandardMaterial({ color: 0xDCD3FB, roughness: 1 }));
  road.position.set(0, 0.06, D / 2 + 15); road.receiveShadow = true; scene.add(road);
  const treeMat = [new THREE.MeshStandardMaterial({ color: 0xB9A8F7, roughness: 0.8, flatShading: true }), new THREE.MeshStandardMaterial({ color: 0xA7D7C5, roughness: 0.8, flatShading: true })];
  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x9B8BC9 });
  [[-20, 6], [-20, -6], [20, 8], [21, -5], [-12, 14], [13, 14], [-30, 18], [32, 16], [-36, -2], [36, 0]].forEach(([x, z], i) => {
    const t = new THREE.Group();
    t.add(at(box(0.5, 2.6, 0.5, trunkMat), 0, 1.3, 0));
    const crown = new THREE.Mesh(new THREE.IcosahedronGeometry(2 + (i % 3) * 0.4, 0), treeMat[i % 2]);
    crown.position.y = 4; crown.castShadow = true; t.add(crown);
    t.position.set(x, 0, z); scene.add(t);
  });
  const farMat = new THREE.MeshStandardMaterial({ color: 0xE4DCFF, roughness: 0.9 });
  [[-70, -60, 30], [-45, -80, 44], [55, -70, 36], [85, -40, 22], [-95, -30, 18], [25, -95, 52]].forEach(([x, z, h]) => {
    const b = box(16, h, 14, farMat, false, true); b.position.set(x, h / 2, z); scene.add(b);
  });

  // ── papan konten (HTML asli di ruang 3D) ──
  const PX = 0.034;                                   // meter per piksel papan
  const boards = {};
  cards.forEach(c => {
    const k = +c.dataset.k;
    const obj = new CSS3DObject(c);
    obj.scale.setScalar(PX);
    floors[k].g.add(obj);
    boards[k] = { obj, el: c };
  });
  function layoutBoards() {
    const cw = mobile ? Math.min(340, innerWidth - 40) : 560;
    cards.forEach(c => {
      c.style.width = cw + 'px';
      const prev = c.style.display; c.style.display = 'block';            // ukur walau sedang disembunyikan CSS3D
      const b = boards[+c.dataset.k]; b.w = c.offsetWidth; b.h = c.offsetHeight;
      c.style.display = prev;
    });
  }

  // ── kamera mengikuti scroll ──
  const clamp = v => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const lerp = (a, b, t) => a + (b - a) * t;
  let V = innerHeight, INTRO, SEG, OUTRO;
  const target = new THREE.Vector3();
  function rig(az, el, dist, ty) {
    const fit = dist > 80 ? Math.max(1, 1.25 / camera.aspect) : 1;      // layar sempit: mundur saat gedung utuh
    const d = dist * fit;
    target.set(0, ty, 0);
    camera.position.set(Math.sin(az) * Math.cos(el) * d, ty + Math.sin(el) * d, Math.cos(az) * Math.cos(el) * d);
    camera.lookAt(target);
  }
  function resize() {
    V = innerHeight;
    const w = stage.clientWidth, h = stage.clientHeight;
    gl.setSize(w, h); css.setSize(w, h);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    INTRO = 1.6 * V; SEG = 1.3 * V; OUTRO = 1.7 * V;
    story.style.setProperty('--story-h', (INTRO + cards.length * SEG + OUTRO + V) + 'px');
    layoutBoards();
  }

  const FAR = { az: 0.62, el: 0.14, d: 135, ty: 34 };
  // bidikan per lantai: pusat di tengah papan, jarak cukup supaya papan + lantai memenuhi ~65% tinggi layar
  const TAN = Math.tan(THREE.MathUtils.degToRad(16));
  function shot(k) {
    const b = boards[k] || {};
    const bh = (b.h || 360) * PX, bwPx = b.w || 560;
    const vh = stage.clientHeight, vw = stage.clientWidth;
    const wantPx = Math.min(bwPx, vw * (vw < 900 ? 0.92 : 0.62));           // papan tampil ~ukuran aslinya
    const dWidth = (bwPx * PX) * vh / (2 * TAN * wantPx);
    const dHeight = (bh + 5) / 0.82 / (2 * TAN);                              // seluruh papan + lantai masuk layar
    return { ty: base(k) + SLAB + bh * 0.46, d: Math.max(dWidth, dHeight) };
  }
  const NEAR = { az: 0.24, el: 0.42 };

  function setLift(k, lift) {
    const f = floors[k];
    f.g.position.y = base(k) + lift * 34;
    f.g.rotation.z = lift * 0.06;
    const o = 1 - clamp(lift * 1.3);
    for (const key in f.mats) f.mats[key].opacity = key === 'glass' ? 0.5 * o : o;
    f.g.visible = o > 0.01;
  }
  function setRoof(lift) {
    roof.position.y = TOTAL + lift * 36;
    roof.rotation.z = -lift * 0.05;
    const o = 1 - clamp(lift * 1.3);
    roofAll.forEach(m => { m.opacity = o; });
    roof.visible = o > 0.01;
  }
  function setBoard(k, pop, gone) {
    const b = boards[k], el = b.el;
    if (pop <= 0.001 || gone >= 0.999) { el.style.opacity = 0; el.classList.remove('act'); b.obj.visible = false; return; }
    b.obj.visible = true;
    const hPx = b.h || el.offsetHeight, sy = lerp(0.02, 1, pop);
    b.obj.scale.set(PX * lerp(0.7, 1, pop), PX * sy, PX);
    b.obj.rotation.x = -0.22;                              // sedikit condong ke kamera supaya mudah dibaca
    b.obj.position.set(0, SLAB + (hPx * PX * sy) / 2 * Math.cos(0.22), -D / 2 + 2.2);
    const op = Math.min(clamp(pop * 2.2), 1 - clamp(gone * 1.3));
    el.style.opacity = op;
    el.classList.toggle('act', op > 0.6);
  }

  function frame() {
    const g = -story.getBoundingClientRect().top, n = cards.length;
    let hero = 0, outroO = 0;
    const lifts = {}; for (let k = 1; k <= N; k++) lifts[k] = 0;
    let roofLift = 0;
    const state = {};
    if (g < INTRO) {
      const p = clamp(g / INTRO), z = ease(clamp((p - 0.03) / 0.62));
      const s7 = shot(7);
      rig(lerp(FAR.az, NEAR.az, z), lerp(FAR.el, NEAR.el, z), lerp(FAR.d, s7.d, z), lerp(FAR.ty, s7.ty, z));
      roofLift = ease(clamp((p - 0.5) / 0.42));
      hero = 1 - clamp(p / 0.18);
      state[7] = { pop: ease(clamp((p - 0.88) / 0.12)) * 0.25, gone: 0 };
    } else if (g < INTRO + n * SEG) {
      const x = (g - INTRO) / SEG, i = Math.min(n - 1, Math.floor(x)), u = x - i;
      const cur = 7 - i, peel = cur > 1 ? ease(clamp((u - 0.72) / 0.28)) : 0;
      for (let k = cur + 1; k <= N; k++) lifts[k] = 1;
      lifts[cur] = peel; roofLift = 1;
      const a = shot(cur), b = cur > 1 ? shot(cur - 1) : a;
      rig(NEAR.az, NEAR.el, lerp(a.d, b.d, peel), lerp(a.ty, b.ty, peel));
      state[cur] = { pop: lerp(i === 0 ? 0.25 : 0.35, 1, ease(clamp(u / 0.2))), gone: peel };
      if (cur > 1 && peel > 0) state[cur - 1] = { pop: peel * 0.35, gone: 0 };   // papan berikutnya mulai naik saat lantai atas terangkat
    } else {
      const q = clamp((g - INTRO - n * SEG) / OUTRO), z = ease(clamp(q / 0.8));
      for (let k = 2; k <= N; k++) lifts[k] = 1 - ease(clamp((q * 1.7 - (k - 2) * 0.1) / 0.45));
      roofLift = 1 - ease(clamp((q * 1.7 - 0.7) / 0.45));
      const s1 = shot(1);
      rig(lerp(NEAR.az, FAR.az, z), lerp(NEAR.el, FAR.el, z), lerp(s1.d, FAR.d, z), lerp(s1.ty, FAR.ty, z));
      outroO = clamp((q - 0.65) / 0.25);
      state[1] = { pop: 1, gone: clamp(q / 0.15) };
    }
    for (let k = 1; k <= N; k++) setLift(k, lifts[k]);
    setRoof(roofLift);
    for (let k = 1; k <= N; k++) { const s = state[k]; setBoard(k, s ? s.pop : 0, s ? s.gone : 0); }
    stage.style.setProperty('--hero', hero);
    stage.style.setProperty('--outro', outroO);
  }

  // render: setiap frame selama adegan terlihat (lampu sinyal berkedip), berhenti saat di luar layar
  let visible = true, t0 = performance.now();
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) loop(); }).observe(story);
  function loop() {
    if (!visible) return;
    beacon.material.emissiveIntensity = 1.2 + Math.sin((performance.now() - t0) / 300) * 1.0;
    frame();
    gl.render(scene, camera);
    css.render(scene, camera);
    requestAnimationFrame(loop);
  }
  addEventListener('resize', resize);
  resize();
  loop();
}
