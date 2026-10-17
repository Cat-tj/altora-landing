/* Pembuka beranda "gedung Altora" (Three.js), dipakai di /preview-gedung.
   Adegan: gedung kaca utuh -> atap terangkat -> kamera masuk ke ruang meeting di lantai teratas -> layar proyektor
   menampilkan salinan hero beranda seukuran layar pengunjung -> saat layar memenuhi layar, kanvas 3D disembunyikan dan
   beranda asli (tepat di posisi yang sama) berlanjut seperti biasa. Lantai lain hanya tampak dari luar. */
import * as THREE from 'three';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { SVGLoader } from 'three/addons/loaders/SVGLoader.js';

const root = document.querySelector('.gd2');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (root && !reduce && webglOK()) init();

function webglOK() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
}

function init() {
  root.classList.add('gd-live', 'gd-3d');
  const scenes = [...root.querySelectorAll('.gd-scene')];
  const coverEl = root.querySelector('[data-gd-cover]');              // hero beranda = isi layar proyektor
  const mobile = innerWidth < 900;
  if (mobile) root.classList.add('gd-m');

  // ── ukuran gedung (meter) ──
  const W = 24, D = 17, FH = 6, LOBBY = 7, N = 8, SLAB = 0.5;
  const base = k => (k === 1 ? 0 : LOBBY + (k - 2) * FH);
  const height = k => (k === 1 ? LOBBY : FH);
  const TOTAL = LOBBY + (N - 1) * FH;
  const BACK = -D / 2 + 0.65;                                           // z permukaan dinding belakang (dalam)

  // ── renderer ──
  const BG = 0xFBF9FE;
  const gl = new THREE.WebGLRenderer({ antialias: true });
  gl.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.5 : 1.75));
  gl.setClearColor(BG, 1);
  gl.shadowMap.enabled = true;
  gl.shadowMap.type = THREE.PCFSoftShadowMap;
  gl.toneMapping = THREE.ACESFilmicToneMapping;
  gl.toneMappingExposure = 1.05;
  gl.outputColorSpace = THREE.SRGBColorSpace;
  gl.domElement.className = 'gd-canvas';
  root.appendChild(gl.domElement);
  const css = new CSS3DRenderer();
  css.domElement.className = 'gd-css3d';
  root.appendChild(css.domElement);

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(BG, 420, 900);                              // hanya memudarkan cakrawala, bukan kabut
  const pmrem = new THREE.PMREMGenerator(gl);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(32, 1, 0.3, 2500);

  // ── cahaya ──
  const hemi = new THREE.HemisphereLight(0xF4F0FF, 0xCFC3FA, 1.0); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xFFF4E6, 2.2);
  sun.position.set(45, 90, 55);
  sun.castShadow = true;
  sun.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(sun.shadow.camera, { left: -80, right: 80, top: 90, bottom: -60, near: 10, far: 320 });
  sun.shadow.camera.updateProjectionMatrix();
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0xC9BCFA, 0.6);
  fill.position.set(-50, 30, -20); scene.add(fill);

  // ── helper ──
  const at = (m, x, y, z) => { m.position.set(x, y, z); return m; };
  const std = (color, extra = {}) => new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.7 }, extra));
  const box = (w, h, d, mat, cast = true, recv = true) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.castShadow = cast; m.receiveShadow = recv; return m; };
  const cyl = (r1, r2, h, mat, seg = 16) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, seg), mat); m.castShadow = true; return m; };
  const canvasTex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };

  // ── material ──
  const M = {
    glass: new THREE.MeshPhysicalMaterial({ color: 0x8C76F2, roughness: 0.06, metalness: 0.15, transparent: true, opacity: 0.26, envMapIntensity: 1.2, clearcoat: 1, clearcoatRoughness: 0.08 }),
    frame: std(0x3E2A97, { roughness: 0.45, metalness: 0.35 }),
    slab: std(0xFBFAFF, { roughness: 0.6 }),
    wall: std(0xEDE7FF, { roughness: 0.9 }),
    wood: std(0xE9DCCB, { roughness: 0.55 }),
    white: std(0xFFFFFF, { roughness: 0.5 }),
    dark: std(0x1B1F45, { roughness: 0.35, metalness: 0.3 }),
    screenOff: std(0x0F1230, { roughness: 0.2, metalness: 0.2 }),
    purple: std(0x7C5CE8, { roughness: 0.5 }),
    lilac: std(0xC9BCFA, { roughness: 0.6 }),
    sofa: std(0xD9CFFB, { roughness: 0.9 }),
    plant: std(0x8FCBB0, { roughness: 0.8, flatShading: true }),
    pot: std(0xF3EFFE),
    skin: std(0xD9A685, { roughness: 0.8 }),
    hair: std(0x2B2140, { roughness: 0.8 }),
    pants: std(0x2A2F5E),
    led: new THREE.MeshStandardMaterial({ color: 0x9CF5C8, emissive: 0x5BE7A4, emissiveIntensity: 2 }),
    ledP: new THREE.MeshStandardMaterial({ color: 0xC9BCFA, emissive: 0x9C84F5, emissiveIntensity: 2 }),
    glow: new THREE.MeshStandardMaterial({ color: 0xFFFFFF, emissive: 0xE9E3FF, emissiveIntensity: 0.9 }),
  };
  M.floor = std(0xFFFFFF, { roughness: 0.8, map: canvasTex(128, 128, (x) => { x.fillStyle = '#F6F2FF'; x.fillRect(0, 0, 128, 128); x.strokeStyle = 'rgba(124,92,232,.14)'; x.lineWidth = 2; x.strokeRect(0, 0, 128, 128); }) });
  M.floor.map.wrapS = M.floor.map.wrapT = THREE.RepeatWrapping; M.floor.map.repeat.set(W / 3, D / 3);
  M.carpet = std(0xE4DCFF, { roughness: 1 });
  const camFeed = i => std(0xffffff, { roughness: 0.3, emissive: 0xffffff, emissiveIntensity: 0.55, map: canvasTex(320, 180, (x, w, h) => {
    const gr = x.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#2B3360'); gr.addColorStop(1, '#4A4F8C'); x.fillStyle = gr; x.fillRect(0, 0, w, h);
    x.fillStyle = 'rgba(201,188,250,.35)'; x.fillRect(30 + i * 20, 90, 120, 70); x.fillRect(190, 60 - i * 6, 90, 100);
    x.fillStyle = '#9CF5C8'; x.font = '700 18px monospace'; x.fillText('CAM 0' + (i + 1), 12, 26); x.fillStyle = '#FF6B9A'; x.beginPath(); x.arc(w - 18, 20, 6, 0, 7); x.fill();
  }) });

  // ── orang (stilisasi) ──
  // orang voxel (gaya kotak-kotak): kepala kubus, rambut kotak, badan/lengan/kaki balok
  const SKIN = [0xF2B48C, 0xD9946B, 0xB9784F], HAIR = [0x5A3825, 0x2B2140, 0x8A5A2B];
  function person({ shirt = 0x7C5CE8, pants = 0x3FA7B5, seated = false, arms = 'down', beard = false, v = 0 } = {}) {
    const g = new THREE.Group(), sh = std(shirt, { flatShading: true }), pt = std(pants, { flatShading: true });
    const skin = std(SKIN[v % 3], { flatShading: true }), hair = std(HAIR[v % 3], { flatShading: true }), shoe = std(0x5B5560, { flatShading: true }), eye = std(0x1B1F45);
    const hip = seated ? 0.5 : 0.72;
    if (seated) {
      [-0.12, 0.12].forEach(x => { g.add(at(box(0.2, 0.2, 0.5, pt), x, 0.5, -0.2)); g.add(at(box(0.2, 0.42, 0.2, pt), x, 0.27, -0.44)); g.add(at(box(0.22, 0.12, 0.3, shoe), x, 0.06, -0.48)); });
    } else {
      [-0.12, 0.12].forEach(x => { g.add(at(box(0.21, 0.6, 0.24, pt), x, 0.42, 0)); g.add(at(box(0.23, 0.14, 0.3, shoe), x, 0.07, -0.03)); });
    }
    g.add(at(box(0.56, 0.6, 0.34, sh), 0, hip + 0.3, 0));                                   // badan
    g.add(at(box(0.08, 0.32, 0.02, std(0xffffff)), 0, hip + 0.42, -0.175));                  // kerah/dasi
    const head = new THREE.Group(); head.position.set(0, hip + 0.86, 0); g.add(head);
    head.add(at(box(0.5, 0.48, 0.48, skin), 0, 0, 0));                                       // kepala kubus
    head.add(at(box(0.54, 0.16, 0.52, hair), 0, 0.26, 0.01));                                // rambut atas
    head.add(at(box(0.54, 0.4, 0.14, hair), 0, 0.06, 0.2));                                  // rambut belakang
    [-0.11, 0.11].forEach(x => head.add(at(box(0.07, 0.07, 0.02, eye), x, 0.03, -0.245)));   // mata
    if (beard) head.add(at(box(0.4, 0.16, 0.06, hair), 0, -0.17, -0.23));
    const hands = [];
    [-0.36, 0.36].forEach((x, i) => {
      const a = new THREE.Group(); a.position.set(x, hip + 0.56, 0);
      a.add(at(box(0.17, 0.32, 0.2, sh), 0, -0.14, 0));
      const fore = new THREE.Group(); fore.position.set(0, -0.3, 0); a.add(fore);
      fore.add(at(box(0.15, 0.2, 0.18, sh), 0, -0.08, 0));
      const hand = at(box(0.15, 0.14, 0.16, skin), 0, -0.24, 0); fore.add(hand); hands.push(hand);
      if (arms === 'hold') { a.rotation.x = -0.7; fore.rotation.x = -0.9; }
      else if (arms === 'phone' && i === 1) { a.rotation.x = -0.5; fore.rotation.x = -1.5; }
      else if (arms === 'desk') { a.rotation.x = -1.0; fore.rotation.x = -0.4; }
      g.add(a);
    });
    g.userData.hands = hands;
    return g;
  }
  function chair(seatY = 0.48, mat = M.dark) {
    const g = new THREE.Group();
    g.add(at(box(0.55, 0.08, 0.55, mat), 0, seatY, 0));
    g.add(at(box(0.55, 0.6, 0.07, mat), 0, seatY + 0.33, 0.25));
    g.add(at(cyl(0.04, 0.04, seatY, M.frame), 0, seatY / 2, 0));
    return g;
  }
  function plant(s = 1) {                                                // tanaman voxel
    const g = new THREE.Group();
    g.add(at(box(0.55 * s, 0.5 * s, 0.55 * s, M.pot), 0, 0.25 * s, 0));
    g.add(at(box(0.8 * s, 0.6 * s, 0.8 * s, M.plant), 0, 0.85 * s, 0));
    g.add(at(box(0.5 * s, 0.45 * s, 0.5 * s, M.plant), 0, 1.35 * s, 0));
    return g;
  }
  function desk(w = 1.6, d = 0.8, h = 0.75, mat = M.white) {
    const g = new THREE.Group();
    g.add(at(box(w, 0.05, d, mat), 0, h, 0));
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sz]) => g.add(at(box(0.05, h, 0.05, M.frame), sx * (w / 2 - 0.05), h / 2, sz * (d / 2 - 0.05))));
    return g;
  }
  function monitor(w = 0.62, h = 0.36) {
    const g = new THREE.Group();
    g.add(at(box(w + 0.04, h + 0.04, 0.03, M.dark), 0, h / 2 + 0.12, 0));
    g.add(at(box(w, h, 0.005, M.glow, false, false), 0, h / 2 + 0.12, 0.018));
    g.add(at(box(0.05, 0.12, 0.05, M.dark), 0, 0.06, -0.03));
    return g;
  }
  function sofa(w = 2.4) {
    const g = new THREE.Group();
    g.add(at(box(w, 0.45, 0.9, M.sofa), 0, 0.23, 0));
    g.add(at(box(w, 0.55, 0.22, M.sofa), 0, 0.6, 0.34));
    [-1, 1].forEach(s => g.add(at(box(0.2, 0.35, 0.9, M.sofa), s * (w / 2 - 0.1), 0.6, 0)));
    return g;
  }

  // ── layar konten: ukurannya mengikuti bentuk layar pengunjung (lebar/tinggi), lihat sizeScreens() ──
  const screens = {};
  const unitBox = new THREE.BoxGeometry(1, 1, 1);
  function contentScreen(k, room, opt) {
    const holder = new THREE.Group();
    holder.rotation.set(opt.rx || 0, opt.ry || 0, 0, 'YXZ');
    const hand = opt.kind === 'phone' || opt.kind === 'tablet';
    const bezel = new THREE.Mesh(unitBox, M.dark); bezel.castShadow = true;
    bezel.position.z = hand ? -0.008 : -0.035;
    const surface = new THREE.Mesh(unitBox, opt.surface || M.screenOff);
    holder.add(bezel, surface);
    room.add(holder);
    screens[k] = Object.assign({}, opt, { holder, bezel, surface, hand, w: 1, h: 1 });
    return holder;
  }
  function sizeScreens(aspect) {
    for (const k in screens) {
      const s = screens[k];
      let w, h;
      if (s.hand) { if (aspect >= 1) { w = s.L; h = s.L / aspect; } else { h = s.L; w = s.L * aspect; } }
      else { h = s.hBase; w = h * aspect; if (w > s.maxW) { w = s.maxW; h = w / aspect; } }
      s.w = w; s.h = h;
      const b = s.bezelPad === undefined ? 0.12 : s.bezelPad;
      s.surface.scale.set(w, h, 0.003);
      s.bezel.scale.set(w + b, h + b, s.hand ? 0.012 : 0.06);
      s.bezel.visible = b > 0;
      if (s.hand) s.holder.position.set(s.x, s.y, s.z);
      else s.holder.position.set(s.x || 0, s.bottom + h / 2, s.z);
      if (s.onSize) s.onSize(w, h);
    }
    for (const k in LABELS) LABELS[k].draw(aspect);
  }

  let beam = null;
  const leds = [];
  const ROOMS = {
    // 8 · ruang meeting: proyektor menyala ke layar
    8(room, k) {
      const housing = at(box(1, 0.22, 0.25, M.dark), 0, 0, BACK + 0.05); room.add(housing);
      const lens = new THREE.Vector3(0, 0.87, 1.92);
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(new Array(36).fill(0), 3));
      beam = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0xFFF2C8, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
      room.add(beam);
      contentScreen(k, room, { kind: 'wide', hBase: 4.1, maxW: 9.6, bottom: 0.9, z: BACK, bezelPad: 0, surface: M.white, onSize(sw, sh) {
        const sy = 0.9 + sh / 2;
        housing.scale.x = sw + 0.6; housing.position.y = sy + sh / 2 + 0.2;
        const c = [[-sw / 2, sy - sh / 2], [sw / 2, sy - sh / 2], [sw / 2, sy + sh / 2], [-sw / 2, sy + sh / 2]].map(([x, y]) => new THREE.Vector3(x, y, BACK + 0.02));
        const p = beam.geometry.attributes.position;
        for (let i = 0; i < 4; i++) { const a2 = c[i], b2 = c[(i + 1) % 4]; p.setXYZ(i * 3, lens.x, lens.y, lens.z); p.setXYZ(i * 3 + 1, a2.x, a2.y, a2.z); p.setXYZ(i * 3 + 2, b2.x, b2.y, b2.z); }
        p.needsUpdate = true; beam.geometry.computeBoundingSphere();
      } });
      room.add(at(desk(9.5, 3, 0.75, M.wood), 0, 0, 1.4));
      for (let i = 0; i < 4; i++) {
        const x = -3.3 + i * 2.2;
        [[-1, 3.15], [1, -0.35]].forEach(([side, z]) => {
          const c = chair(); c.rotation.y = side < 0 ? 0 : Math.PI; room.add(at(c, x, 0, z));
        });
        if (i % 2 === 0 || i === 3) { const p = person({ seated: true, shirt: [0x7C5CE8, 0x6B3F3A, 0x3E2A97, 0xF26B3A][i], v: i, beard: i === 1, arms: 'desk' }); p.rotation.y = 0.15 * (i - 1.5); room.add(at(p, x, 0, 3.0)); }
      }
      const proj = new THREE.Group(); proj.add(at(box(0.55, 0.2, 0.5, M.white), 0, 0, 0)); proj.add(at(cyl(0.07, 0.07, 0.06, M.dark), 0, 0, -0.27)); proj.children[1].rotation.x = Math.PI / 2;
      room.add(at(proj, 0, 0.87, 2.2));
      [[-10.5, -6.5], [10.5, -6.5], [-10.5, 6.5], [10.5, 6.5]].forEach(([x, z]) => room.add(at(plant(1.1), x, 0, z)));
    },
  };

  // ── aktivitas lantai lain (ringan: tanpa bayangan, orang 5 balok) ──
  const crowd = [];                                                    // orang yang berjalan bolak-balik
  const lite = (w, h, d, mat) => box(w, h, d, mat, false, false);
  const SHIRTS = [0x7C5CE8, 0xF26B3A, 0x3FA7B5, 0xF5C04A, 0x6B3F3A, 0xFFFFFF, 0x3E2A97];
  const shirtMats = SHIRTS.map(c => std(c, { flatShading: true }));
  const skinMats = [0xF2B48C, 0xD9946B, 0xB9784F].map(c => std(c, { flatShading: true }));
  const hairMat = std(0x3A2A30, { flatShading: true });
  function mini(i, seated) {                                           // orang voxel sederhana
    const g = new THREE.Group(), sh = shirtMats[i % shirtMats.length], sk = skinMats[i % 3];
    g.add(at(lite(0.42, seated ? 0.45 : 0.75, 0.3, M.pants), 0, seated ? 0.45 : 0.38, 0));
    g.add(at(lite(0.56, 0.6, 0.34, sh), 0, seated ? 0.95 : 1.05, 0));
    g.add(at(lite(0.46, 0.44, 0.44, sk), 0, seated ? 1.48 : 1.58, 0));
    g.add(at(lite(0.5, 0.16, 0.48, hairMat), 0, seated ? 1.72 : 1.82, 0.02));
    return g;
  }
  const ceilLight = std(0xFFFFFF, { emissive: 0xFFF4DA, emissiveIntensity: 1.1 });
  const screenGlow = std(0xFFFFFF, { emissive: 0xD9CFFF, emissiveIntensity: 1.2 });
  const deskTop = std(0xFFFFFF, { roughness: 0.6 });
  function busyFloor(room, k, gh) {
    room.add(at(lite(W - 1.2, 0.05, D - 1.2, M.lilac), 0, 0.03, 0));
    for (let x = -8; x <= 8; x += 8) room.add(at(lite(5, 0.08, 0.6, ceilLight), x, gh - 0.1, 0));        // lampu langit-langit
    const kind = k === 1 ? 'lobby' : k === 7 ? 'server' : k === 3 || k === 5 ? 'lounge' : 'office';
    if (kind === 'office') {
      let i = k;
      for (const z of [D / 2 - 2.6, -1.2]) for (let x = -9; x <= 9; x += 3) {
        room.add(at(lite(2.2, 0.08, 1, deskTop), x, 0.78, z));
        room.add(at(lite(0.9, 0.55, 0.05, screenGlow), x, 1.15, z - 0.35));
        if ((x + k) % 2 === 0 || i % 3 === 0) { const p = mini(i, true); p.rotation.y = Math.PI; room.add(at(p, x, 0, z - 1.0)); }
        i++;
      }
      for (let j = 0; j < 2; j++) { const p = mini(k + j * 3, false); room.add(at(p, -6 + j * 9, 0, 2.2)); crowd.push({ p, axis: 'x', min: -10, max: 10, dir: j ? -1 : 1, speed: 1.1 + j * 0.4 }); }
    } else if (kind === 'server') {
      for (let x = -9; x <= 9; x += 2.6) [-3.5, 3.5].forEach(z => {
        room.add(at(lite(1.6, 2.3, 1, M.dark), x, 1.15, z));
        for (let r = 0; r < 4; r++) { const led = at(lite(0.08, 0.08, 0.05, (r + x) % 2 ? M.led : M.ledP), x - 0.5 + r * 0.32, 0.6 + r * 0.4, z + 0.52); room.add(led); leds.push(led); }
      });
      const p = mini(2, false); room.add(at(p, 0, 0, 0)); crowd.push({ p, axis: 'x', min: -9, max: 9, dir: 1, speed: 0.9 });
    } else if (kind === 'lounge') {
      [[-7, 3], [0, 4], [7, 3]].forEach(([x, z], j) => {
        room.add(at(lite(1.2, 0.75, 1.2, deskTop), x, 0.38, z));
        for (let a = 0; a < 3; a++) { const p = mini(j * 3 + a, false); const ang = a * 2.1; p.rotation.y = -ang + Math.PI; room.add(at(p, x + Math.sin(ang) * 1.2, 0, z + Math.cos(ang) * 1.2)); }
      });
      room.add(at(lite(6, 0.9, 1.2, std(0xD9CFFB, { flatShading: true })), -4, 0.45, -5));
      const p = mini(5, false); room.add(at(p, 0, 0, -1)); crowd.push({ p, axis: 'x', min: -10, max: 10, dir: -1, speed: 1.3 });
    } else {                                                                                               // lobi
      room.add(at(lite(6, 1.1, 1.2, deskTop), 0, 0.55, -3));
      room.add(at(lite(6, 0.15, 1.22, M.purple), 0, 0.9, -3));
      const rec = mini(0, false); rec.rotation.y = 0; room.add(at(rec, 0, 0, -4.1));
      for (let j = 0; j < 3; j++) { const p = mini(j + 2, false); room.add(at(p, -5 + j * 5, 0, 3 + j)); crowd.push({ p, axis: 'z', min: -1, max: 7, dir: j % 2 ? 1 : -1, speed: 0.9 + j * 0.3 }); }
      [-10, 10].forEach(x => room.add(at(lite(0.8, 2.2, 0.8, M.plant), x, 1.1, 6)));
    }
  }

  // ── tiap lantai = satu halaman; klik lantai -> lantai terbuka -> kamera masuk ke layarnya -> halaman dibuka ──
  const PAGES = { 8: ['Layanan', '/services'], 7: ['Produk', '/produk'], 6: ['Katalog', '/katalog'], 5: ['Portofolio', '/portfolio'],
    4: ['Artikel', '/blog'], 3: ['Tentang', '/about'], 2: ['Karier', '/careers'], 1: ['Support', '/support'] };
  const LABELS = {};
  function labelMat(k) {                                                // isi layar: judul halaman, digambar ulang mengikuti rasio layar pengunjung
    const c = document.createElement('canvas'), tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    const mat = new THREE.MeshStandardMaterial({ map: tex, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: 0.9, roughness: 0.4 });
    LABELS[k] = { mat, draw(aspect) {
      const w = aspect >= 1 ? 1280 : Math.round(1280 * aspect), h = aspect >= 1 ? Math.round(1280 / aspect) : 1280;
      c.width = w; c.height = h; const x = c.getContext('2d');
      const g = x.createLinearGradient(0, 0, w, h); g.addColorStop(0, '#FFFFFF'); g.addColorStop(0.6, '#F3EEFF'); g.addColorStop(1, '#E4DAFF'); x.fillStyle = g; x.fillRect(0, 0, w, h);
      const r = x.createRadialGradient(w * 0.85, 0, 0, w * 0.85, 0, Math.max(w, h) * 0.7); r.addColorStop(0, 'rgba(124,92,232,.22)'); r.addColorStop(1, 'rgba(124,92,232,0)'); x.fillStyle = r; x.fillRect(0, 0, w, h);
      const fs = Math.min(w * 0.17, h * 0.22);
      x.textAlign = 'center'; x.textBaseline = 'middle';
      x.fillStyle = '#7C5CE8'; x.font = '700 ' + Math.round(fs * 0.3) + 'px "Plus Jakarta Sans", system-ui, sans-serif'; x.fillText('ALTORA', w / 2, h / 2 - fs * 0.85);
      x.fillStyle = '#10224F'; x.font = '800 ' + Math.round(fs) + 'px "Plus Jakarta Sans", system-ui, sans-serif'; x.fillText(PAGES[k][0], w / 2, h / 2);
      x.fillStyle = '#5A6785'; x.font = '600 ' + Math.round(fs * 0.26) + 'px "Plus Jakarta Sans", system-ui, sans-serif'; x.fillText('Membuka halaman…', w / 2, h / 2 + fs * 0.85);
      tex.needsUpdate = true;
    } };
    return mat;
  }
  function floorScreen(k, room) {                                      // proyektor / TV dinding / monitor meja / HP, sesuai ruangan
    const surface = labelMat(k);
    if (k === 2) {                                                       // Karier: HP di meja
      room.add(at(desk(1.4, 0.8, 0.75, deskTop), 0, 0, -5.4));
      room.add(at(lite(0.26, 0.14, 0.18, M.dark), 0, 0.84, -5.5));
      contentScreen(k, room, { kind: 'phone', L: 0.34, x: 0, y: 1.02, z: -5.3, rx: -0.3, bezelPad: 0.03, surface });
      const p = mini(4, true); p.rotation.y = Math.PI; room.add(at(p, 1.3, 0, -4.4));
    } else if (k === 4 || k === 6) {                                     // Artikel, Katalog: monitor besar di meja
      room.add(at(desk(2.2, 0.9, 0.75, deskTop), 0, 0, -5.6));
      room.add(at(lite(0.14, 0.22, 0.1, M.dark), 0, 0.88, -5.98));
      contentScreen(k, room, { kind: 'wide', hBase: 0.62, maxW: 1.15, bottom: 0.98, z: -5.8, bezelPad: 0.05, surface });
      const p = mini(k, true); p.rotation.y = Math.PI; room.add(at(p, 1.5, 0, -4.7));
    } else {                                                             // Produk, Portofolio, Tentang, Support: TV di dinding belakang
      contentScreen(k, room, { kind: 'wide', hBase: 2.3, maxW: 4.4, bottom: k === 1 ? 2.2 : 1.5, z: BACK, bezelPad: 0.14, surface });
    }
  }

  // ── lantai ──
  const floors = {};
  for (let k = 1; k <= N; k++) {
    const h = height(k), g = new THREE.Group(), gh = h - SLAB, gy = SLAB + gh / 2;
    g.add(at(box(W + 1.2, SLAB, D + 1.2, M.slab), 0, SLAB / 2, 0));
    const inner = new THREE.Mesh(new THREE.PlaneGeometry(W - 0.6, D - 0.6), M.floor);
    inner.rotation.x = -Math.PI / 2; inner.position.y = SLAB + 0.01; inner.receiveShadow = true; g.add(inner);
    [[0, D / 2], [0, -D / 2]].forEach(([x, z]) => g.add(at(box(W, gh, 0.12, M.glass, false, false), x, gy, z)));
    [[W / 2, 0], [-W / 2, 0]].forEach(([x, z]) => g.add(at(box(0.12, gh, D, M.glass, false, false), x, gy, z)));
    for (let i = 0; i <= 8; i++) { const x = -W / 2 + (i * W) / 8; g.add(at(box(0.28, gh, 0.28, M.frame), x, gy, D / 2)); g.add(at(box(0.28, gh, 0.28, M.frame), x, gy, -D / 2)); }
    for (let i = 1; i < 6; i++) { const z = -D / 2 + (i * D) / 6; g.add(at(box(0.28, gh, 0.28, M.frame), W / 2, gy, z)); g.add(at(box(0.28, gh, 0.28, M.frame), -W / 2, gy, z)); }
    g.add(at(box(W - 0.6, gh, 0.2, M.wall, false, true), 0, gy, -D / 2 + 0.4));
    const room = new THREE.Group(); room.position.y = SLAB; g.add(room);
    scene.add(g);
    if (k === N) { ROOMS[k](room, k); labelMat(k); }                                  // lantai teratas: ruang meeting yang dikunjungi kamera
    else { busyFloor(room, k, gh); floorScreen(k, room); }             // lantai lain: aktivitas yang terlihat dari luar + layar halamannya
    g.position.y = base(k);
    floors[k] = { g, h };
  }

  // ── atap ──
  const roof = new THREE.Group();
  const roofMats = { roof: std(0x5B3FC4, { roughness: 0.5, metalness: 0.2 }), hvac: std(0xE4DEFA, { roughness: 0.5, metalness: 0.4 }), slab: M.slab.clone(), frame: M.frame.clone() };
  roof.add(at(box(W + 1.2, 0.9, D + 1.2, roofMats.roof), 0, 0.45, 0));
  [[0, D / 2 + 0.4], [0, -D / 2 - 0.4]].forEach(([x, z]) => roof.add(at(box(W + 1.2, 1.2, 0.4, roofMats.slab), x, 1.5, z)));
  [[W / 2 + 0.4, 0], [-W / 2 - 0.4, 0]].forEach(([x, z]) => roof.add(at(box(0.4, 1.2, D + 1.2, roofMats.slab), x, 1.5, z)));
  [[-7, 1.5], [-1.5, 1.5], [6, 2]].forEach(([x, z]) => roof.add(at(box(3.4, 1.8, 2.6, roofMats.hvac), x, 1.8, z)));
  roof.add(at(box(0.25, 7, 0.25, roofMats.frame), 10.6, 4.4, 6.6));               // tiang suar di sudut depan, jauh dari logo
  const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.45, 16, 12), new THREE.MeshStandardMaterial({ color: 0xFF6B9A, emissive: 0xFF3D7F, emissiveIntensity: 2, transparent: true }));
  roof.add(at(beacon, 10.6, 8.1, 6.6));
  // logo Altora 3D besar yang menyala di atap: huruf A navy + pita ungu-pink, diekstrusi dari SVG logo
  const logoNavy = new THREE.MeshStandardMaterial({ color: 0x0B2E66, roughness: 0.3, metalness: 0.45, emissive: 0x1B2F8A, emissiveIntensity: 0.35, transparent: true });
  const signMat = new THREE.MeshStandardMaterial({ color: 0xB14BE6, roughness: 0.25, metalness: 0.1, emissive: 0xC23BEA, emissiveIntensity: 0.6, transparent: true });
  const logoHolder = new THREE.Group();
  const logo3d = new THREE.Group(); logoHolder.add(at(logo3d, 0, 18, 0));
  new SVGLoader().load('/assets/img/altora-logo-icon-v2.svg', data => {
    const all = new THREE.Box3();
    const meshes = data.paths.map(pth => {
      const ribbon = String(pth.userData?.style?.fill || '').includes('ribbon');
      const geo = new THREE.ExtrudeGeometry(SVGLoader.createShapes(pth), { depth: ribbon ? 150 : 110, bevelEnabled: true, bevelThickness: 14, bevelSize: 10, bevelSegments: 2, curveSegments: 6 });
      if (ribbon) geo.translate(0, 0, -20);                                     // pita sedikit lebih tebal di depan & belakang
      geo.computeBoundingBox(); all.union(geo.boundingBox);
      const m = new THREE.Mesh(geo, ribbon ? signMat : logoNavy); m.castShadow = true; return m;
    });
    const c = all.getCenter(new THREE.Vector3()), size = all.getSize(new THREE.Vector3());
    const sc = 30 / Math.max(size.x, size.y);
    meshes.forEach(m => { m.geometry.translate(-c.x, -c.y, -c.z); logo3d.add(m); });
    logo3d.scale.set(sc, -sc, sc);                                             // sumbu y SVG terbalik
  });
  const glowC = canvasTex(256, 256, (x) => { const g = x.createRadialGradient(128, 128, 0, 128, 128, 128); g.addColorStop(0, 'rgba(216,107,255,.9)'); g.addColorStop(0.45, 'rgba(124,92,232,.35)'); g.addColorStop(1, 'rgba(124,92,232,0)'); x.fillStyle = g; x.fillRect(0, 0, 256, 256); });
  const logoHalo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowC, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity: 0.4 }));
  logoHalo.scale.set(60, 60, 1); logoHolder.add(at(logoHalo, 0, 18, -4));
  [-5, 5].forEach(x => logoHolder.add(at(box(0.6, 5, 0.6, roofMats.frame), x, 3.4, 0)));        // tiang penyangga voxel
  logoHolder.add(at(box(12, 0.5, 0.8, roofMats.frame), 0, 1.2, 0));
  logoHolder.rotation.y = 0.35; roof.add(at(logoHolder, -1, 0, -D / 2 + 2.2));
  const logoLight = new THREE.PointLight(0xD86BFF, 0, 60, 1.6); logoHolder.add(at(logoLight, 0, 12, 3));
  let haloBase = 0.4;
  roof.position.y = TOTAL; scene.add(roof);
  const roofAll = [...Object.values(roofMats), signMat, logoNavy, beacon.material];
  roofAll.forEach(m => { m.transparent = true; });

  // ── lingkungan: kota voxel ala Crossy Road (jalur rumput & jalan, mobil lewat, pohon kotak, gedung tetangga) ──
  const V = {
    grass: std(0xA6DE7C, { roughness: 1, flatShading: true }), grass2: std(0x94D16C, { roughness: 1, flatShading: true }),
    road: std(0x4B5068, { roughness: 0.95 }), dash: std(0xF4F4F8), walk: std(0xEDE8FB, { roughness: 0.9 }), curb: std(0xD9D2F2),
    trunk: std(0x8A5A44, { flatShading: true }), leafA: std(0x8CCB4E, { flatShading: true }), leafB: std(0x76B83E, { flatShading: true }),
    wheel: std(0x1E2033), win: std(0x2B2F4A, { roughness: 0.3 }), white: std(0xFFFFFF, { roughness: 0.6 }),
  };
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(1600, 1600), V.grass);
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  // jalur sepanjang sumbu x: [z tengah, lebar, jenis]
  const ROADS = [[D / 2 + 13, 12], [-D / 2 - 15, 12], [D / 2 + 44, 12]];
  ROADS.forEach(([z, w]) => {
    scene.add(at(box(700, 0.12, w, V.road, false, true), 0, 0.06, z));
    for (let x = -340; x < 340; x += 7) scene.add(at(box(3.2, 0.02, 0.35, V.dash, false, true), x, 0.13, z));
    [-1, 1].forEach(sd => scene.add(at(box(700, 0.35, 0.6, V.curb, false, true), 0, 0.17, z + sd * (w / 2 + 0.3))));
  });
  // jalur rumput gelap/terang bergantian (khas Crossy Road)
  for (let z = -120; z < 120; z += 8) if (((z / 8) | 0) % 2 === 0) scene.add(at(box(700, 0.04, 8, V.grass2, false, true), 0, 0.02, z));
  // plaza gedung
  scene.add(at(box(W + 14, 0.4, D + 12, V.walk, false, true), 0, 0.2, 0));

  // pohon voxel: batang + 1-3 tumpukan daun
  function vtree(x, z, h = 2) {
    const t = new THREE.Group();
    t.add(at(box(0.9, 1.6, 0.9, V.trunk), 0, 0.8, 0));
    for (let i = 0; i < h; i++) { const s2 = 2.6 - i * 0.5; t.add(at(box(s2, 1.5, s2, i % 2 ? V.leafB : V.leafA), 0, 2.3 + i * 1.5, 0)); }
    scene.add(at(t, x, 0, z));
  }
  const treeSpots = [];
  for (let x = -110; x <= 110; x += 9) [D / 2 + 26, D / 2 + 31, -D / 2 - 27].forEach((z, i) => { if (Math.abs(x) > 16 || i === 2) treeSpots.push([x + ((x * 7) % 5), z, 1 + ((x + i * 3) & 1) + (i === 1 ? 1 : 0)]); });
  [[-17, -4], [-17, 4], [17, -3], [17, 5]].forEach(([x, z]) => treeSpots.push([x, z, 2]));
  treeSpots.forEach(([x, z, h]) => vtree(x, z, h));

  // pejalan kaki voxel di plaza & trotoar
  const walkers = [];
  [[-9, D / 2 + 3.2, 1, 0x7C5CE8], [6, D / 2 + 4.2, -1, 0xF26B3A], [-4, D / 2 + 5.4, 1, 0x3FA7B5], [12, -D / 2 - 4, -1, 0x6B3F3A], [-14, -D / 2 - 3.5, 1, 0xF5C04A]]
    .forEach(([x, z, dir, col], i) => {
      const p = person({ shirt: col, pants: [0x3FA7B5, 0x2A2F5E, 0x6B4F3F][i % 3], v: i, beard: i % 2 === 0 });
      p.scale.setScalar(1.6); p.rotation.y = dir > 0 ? -Math.PI / 2 : Math.PI / 2;
      scene.add(at(p, x, 0.4, z)); walkers.push({ p, dir, x0: x, speed: 1.2 + (i % 3) * 0.3 });
    });
  // gedung tetangga: digambar bersama kota di bawah (gaya sama)
  const NEAR = [];
  [[-38, -2, 14, 12, 24, '#FFD6A5'], [-56, 6, 10, 10, 14, '#BDE0FE'], [36, -4, 12, 14, 30, '#CDB4DB'], [55, 4, 10, 10, 18, '#FFC8DD'],
   [-36, -46, 16, 12, 34, '#E2ECE9'], [0, -50, 18, 12, 40, '#D0C4FF'], [36, -48, 14, 12, 26, '#FDE2E4'], [70, -40, 12, 12, 22, '#C1F0DC'],
   [-72, -38, 12, 12, 28, '#FFE5B4'], [-30, 62, 12, 10, 16, '#BDE0FE'], [28, 62, 14, 10, 20, '#FFD6A5'], [64, 60, 10, 10, 12, '#CDB4DB']]
    .forEach(([x, z, w, d, h, c]) => NEAR.push([x, z, w, d, h * 0.8, c]));

  // mobil voxel yang lewat terus
  const carColors = [0xF26B3A, 0x7AC74F, 0x5BB5F0, 0xF5C04A, 0x7C5CE8, 0xFF8FB1];
  const cars = [];
  function vcar(color, truck = false) {
    const g = new THREE.Group(), body = std(color, { flatShading: true, roughness: 0.6 });
    const L = truck ? 7 : 4.6;
    g.add(at(box(L, 1.1, 2.3, body), 0, 0.95, 0));
    if (truck) { g.add(at(box(4.6, 2.2, 2.3, V.white), -1.1, 2.6, 0)); g.add(at(box(1.6, 1.2, 2.2, body), 2.4, 2.0, 0)); g.add(at(box(0.06, 0.7, 1.9, V.win), 3.24, 2.1, 0)); }
    else { g.add(at(box(2.6, 1.0, 2.1, V.white), -0.3, 2.0, 0)); [-1, 1].forEach(sd => g.add(at(box(2.0, 0.6, 0.06, V.win), -0.3, 2.05, sd * 1.1))); g.add(at(box(0.06, 0.6, 1.8, V.win), 1.04, 2.05, 0)); g.add(at(box(0.06, 0.55, 1.8, V.win), -1.64, 2.05, 0)); }
    [-1, 1].forEach(sx => [-1, 1].forEach(sz => g.add(at(box(0.9, 0.9, 0.4, V.wheel), sx * (L / 2 - 1.0), 0.45, sz * 1.2))));
    return g;
  }
  ROADS.forEach(([z], ri) => [-1, 1].forEach((dir, li) => {
    const n = 4 + ((ri + li) % 2);
    for (let i = 0; i < n; i++) {
      const c = vcar(carColors[(ri * 3 + li * 2 + i) % carColors.length], (i + ri + li) % 4 === 0);
      c.rotation.y = dir > 0 ? 0 : Math.PI;
      c.position.set(-160 + i * (320 / n) + li * 23, 0.12, z + dir * 3);
      scene.add(c);
      cars.push({ c, dir, speed: 7 + ((i * 5 + ri * 3 + li * 7) % 6) });
    }
  }));
  let lastT = performance.now();
  function moveCars(now) {
    const dt = Math.min(0.1, (now - lastT) / 1000); lastT = now;
    moveWorld(dt, now);
    cars.forEach(k => { k.c.position.x += k.dir * k.speed * dt; if (k.c.position.x > 170) k.c.position.x = -170; if (k.c.position.x < -170) k.c.position.x = 170; });
    crowd.forEach(c => {
      c.p.position[c.axis] += c.dir * c.speed * dt;
      if (c.p.position[c.axis] > c.max || c.p.position[c.axis] < c.min) c.dir *= -1;
      c.p.rotation.y = c.axis === 'x' ? (c.dir > 0 ? -Math.PI / 2 : Math.PI / 2) : (c.dir > 0 ? Math.PI : 0);
    });
    walkers.forEach(w => {
      w.p.position.x += w.dir * w.speed * dt;
      if (Math.abs(w.p.position.x) > 19) { w.dir *= -1; w.p.rotation.y = w.dir > 0 ? -Math.PI / 2 : Math.PI / 2; }
      w.p.position.y = 0.4 + Math.abs(Math.sin(now / 160 + w.x0)) * 0.12;                  // langkah melompat kecil
    });
  }

  // ── kota luas sampai cakrawala: blok gedung (instanced), jalan silang, sungai, rel kereta, gunung, balon udara ──
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const XR = [D / 2 + 13, -D / 2 - 15, D / 2 + 44, -100, 128, 215, -235];          // jalan sepanjang x (z tengah)
  const ZR = [-125, -245, 118, 240];                                               // jalan sepanjang z (x tengah)
  const RAIL = -140, RIVER = -182;
  [-100, 128, 215, -235].forEach(z => {
    scene.add(at(box(900, 0.12, 12, V.road, false, true), 0, 0.06, z));
    [-1, 1].forEach(sd => scene.add(at(box(900, 0.35, 0.6, V.curb, false, false), 0, 0.17, z + sd * 6.3)));
  });
  ZR.forEach(x => {
    scene.add(at(box(12, 0.12, 900, V.road, false, true), x, 0.065, 0));
    [-1, 1].forEach(sd => scene.add(at(box(0.6, 0.35, 900, V.curb, false, false), x + sd * 6.3, 0.17, 0)));
  });
  // garis putus-putus semua jalan baru dalam satu InstancedMesh
  const dashSpots = [];
  [-100, 128, 215, -235].forEach(z => { for (let x = -440; x < 440; x += 7) dashSpots.push([x, z, 0]); });
  ZR.forEach(x => { for (let z = -440; z < 440; z += 7) dashSpots.push([x, z, 1]); });
  const dashes = new THREE.InstancedMesh(new THREE.BoxGeometry(3.2, 0.02, 0.35), V.dash, dashSpots.length);
  const o3 = new THREE.Object3D();
  dashSpots.forEach(([x, z, r], i) => { o3.position.set(x, 0.14, z); o3.rotation.set(0, r ? Math.PI / 2 : 0, 0); o3.scale.set(1, 1, 1); o3.updateMatrix(); dashes.setMatrixAt(i, o3.matrix); });
  scene.add(dashes);
  // sungai + tepian + kayu hanyut
  const water = std(0x5CC6F2, { roughness: 0.25, metalness: 0.1 });
  scene.add(at(box(900, 0.1, 18, water, false, true), 0, 0.03, RIVER));
  [-1, 1].forEach(sd => scene.add(at(box(900, 0.6, 1.4, std(0xD9C7A0, { flatShading: true }), false, false), 0, 0.3, RIVER + sd * 9.5)));
  ZR.forEach(x => { scene.add(at(box(14, 1.2, 22, V.road, false, true), x, 0.6, RIVER)); [-1, 1].forEach(sd => scene.add(at(box(0.6, 1.4, 22, V.curb, false, false), x + sd * 6.6, 1.5, RIVER))); });
  const logMat = std(0x9A6446, { flatShading: true }), logs = [];
  for (let i = 0; i < 16; i++) {
    const L = 6 + (i % 3) * 3, lg = box(L, 0.9, 1.8, logMat, false, false);
    lg.position.set(-440 + i * 56 + (i % 2) * 20, 0.35, RIVER + (i % 2 ? 4 : -4)); scene.add(lg); logs.push({ m: lg, dir: i % 2 ? 1 : -1, speed: 3 + (i % 3) });
  }
  // rel kereta + kereta voxel
  scene.add(at(box(900, 0.3, 7, std(0xA59BB8, { flatShading: true }), false, true), 0, 0.15, RAIL));
  [-1.4, 1.4].forEach(dz => scene.add(at(box(900, 0.25, 0.3, std(0x6B6F86, { metalness: 0.6, roughness: 0.4 }), false, false), 0, 0.45, RAIL + dz)));
  const sleeperSpots = []; for (let x = -440; x < 440; x += 2.2) sleeperSpots.push(x);
  const sleepers = new THREE.InstancedMesh(new THREE.BoxGeometry(0.6, 0.15, 4.4), V.trunk, sleeperSpots.length);
  sleeperSpots.forEach((x, i) => { o3.position.set(x, 0.33, RAIL); o3.rotation.set(0, 0, 0); o3.updateMatrix(); sleepers.setMatrixAt(i, o3.matrix); });
  scene.add(sleepers);
  const train = new THREE.Group();
  const trainCols = [0x7C5CE8, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF];
  trainCols.forEach((col, i) => {
    const car = new THREE.Group(), body = std(col, { flatShading: true, roughness: 0.5 });
    car.add(at(box(11, 3.4, 3.4, body, false, false), 0, 2.4, 0));
    car.add(at(box(11.02, 0.5, 3.42, std(0x7C5CE8, { flatShading: true }), false, false), 0, 1.4, 0));
    car.add(at(box(9, 0.9, 3.46, V.win, false, false), 0, 2.9, 0));
    if (i === 0) car.add(at(box(1.6, 2.4, 3.2, body, false, false), 6, 1.9, 0));
    train.add(at(car, -i * 11.6, 0.3, 0));
  });
  train.position.set(-300, 0, RAIL); scene.add(train);
  // gedung kota: satu InstancedMesh, jendela digambar di shader (malam: sebagian menyala)
  const winU = { uNight: { value: 0 } };
  const bldMat = std(0xffffff, { roughness: 0.85 });
  bldMat.onBeforeCompile = sh => {
    sh.uniforms.uNight = winU.uNight;
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP; varying vec3 vLN;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvWP = (modelMatrix * instanceMatrix * vec4(position, 1.0)).xyz; vLN = normal;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uNight; varying vec3 vWP; varying vec3 vLN; float gWin; float gLit;')
      .replace('#include <color_fragment>', `#include <color_fragment>
        vec2 gq = vec2(abs(vLN.x) > 0.5 ? vWP.z : vWP.x, vWP.y) / vec2(3.0, 3.4);
        vec2 gf = fract(gq);
        gWin = (1.0 - abs(vLN.y)) * step(0.22, gf.x) * step(gf.x, 0.78) * step(0.28, gf.y) * step(gf.y, 0.82) * step(2.5, vWP.y);
        gLit = step(0.5, fract(sin(dot(floor(gq) + vec2(floor(vWP.x * 0.1), floor(vWP.z * 0.1)) * 7.0, vec2(12.9898, 78.233))) * 43758.5453));
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.32, 0.36, 0.52), gWin * (0.55 + uNight * 0.4));`)
      .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\ntotalEmissiveRadiance += gWin * gLit * uNight * vec3(1.0, 0.82, 0.5) * 2.6;');
  };
  const PASTEL = [0xFFD6A5, 0xBDE0FE, 0xCDB4DB, 0xFFC8DD, 0xE2ECE9, 0xD0C4FF, 0xFDE2E4, 0xC1F0DC, 0xFFE5B4, 0xF1E3FF, 0xCFE8FF, 0xFFF1C1];
  const bSpots = [], parkSpots = [];
  const CELL = 26;
  const near = (v, list, r) => list.some(c => Math.abs(v - c) < r);
  for (let gx = -16; gx <= 16; gx++) for (let gz = -16; gz <= 16; gz++) {
    const x = gx * CELL + (rnd() - 0.5) * 4, z = gz * CELL + (rnd() - 0.5) * 4;
    if (Math.hypot(x, z) > 430) continue;
    if (Math.abs(x) < 92 && z > -68 && z < 76) continue;                           // area gedung Altora & tetangga dekat
    if (near(z, XR, 14) || near(x, ZR, 14) || Math.abs(z - RAIL) < 13 || Math.abs(z - RIVER) < 19) continue;
    const t = x * 0.58 + z * 0.81, lat = Math.abs(x * 0.81 - z * 0.58);           // koridor pandang kamera dibiarkan kosong
    if (t > 30 && lat < 90) continue;
    if (rnd() < 0.3) { parkSpots.push([x, z]); continue; }
    const dist = Math.hypot(x, z), far2 = Math.max(0, dist - 200) / 230;            // dekat gedung Altora rendah, makin jauh makin tinggi (siluet kota)
    const w = 10 + rnd() * 9, d = 10 + rnd() * 9, h = 7 + rnd() * 12 + far2 * (10 + rnd() * 30);
    bSpots.push([x, z, w, d, h, PASTEL[(rnd() * PASTEL.length) | 0]]);
  }
  bSpots.push(...NEAR);
  const blds = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), bldMat, bSpots.length);
  const capMat = std(0xffffff, { flatShading: true, roughness: 0.9 });
  const caps = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), capMat, bSpots.length);
  const lots = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), V.walk, bSpots.length);
  const col = new THREE.Color();
  bSpots.forEach(([x, z, w, d, h, c], i) => {
    o3.rotation.set(0, 0, 0);
    o3.position.set(x, h / 2, z); o3.scale.set(w, h, d); o3.updateMatrix(); blds.setMatrixAt(i, o3.matrix); blds.setColorAt(i, col.set(c));
    o3.position.set(x - w * 0.15, h + 0.8, z); o3.scale.set(w * 0.4, 1.6, d * 0.4); o3.updateMatrix(); caps.setMatrixAt(i, o3.matrix); caps.setColorAt(i, col.set(c).lerp(new THREE.Color(0xffffff), 0.5));
    o3.position.set(x, 0.15, z); o3.scale.set(w + 5, 0.3, d + 5); o3.updateMatrix(); lots.setMatrixAt(i, o3.matrix);
  });
  blds.castShadow = blds.receiveShadow = caps.castShadow = true;
  scene.add(blds, caps, lots);
  // taman: pohon voxel instanced (batang + 2 tumpuk daun)
  const treeArr = [];
  parkSpots.forEach(([x, z]) => { for (let k = 0; k < 5; k++) treeArr.push([x + (rnd() - 0.5) * 16, z + (rnd() - 0.5) * 16, 0.8 + rnd() * 0.6]); });
  for (let i = 0; i < 260; i++) {                                                    // pohon di pinggir jalan & sungai
    const onRiver = i % 3 === 0, x = -430 + rnd() * 860;
    const z = onRiver ? RIVER + (rnd() < 0.5 ? -13 : 13) : XR[3 + (i % 4)] + (rnd() < 0.5 ? -9 : 9);
    if (Math.abs(x) < 95 || near(x, ZR, 9)) continue;
    treeArr.push([x, z, 0.8 + rnd() * 0.5]);
  }
  const trunks = new THREE.InstancedMesh(new THREE.BoxGeometry(0.9, 1.6, 0.9), V.trunk, treeArr.length);
  const leaf1 = new THREE.InstancedMesh(new THREE.BoxGeometry(2.6, 1.5, 2.6), V.leafA, treeArr.length);
  const leaf2 = new THREE.InstancedMesh(new THREE.BoxGeometry(2.0, 1.5, 2.0), V.leafB, treeArr.length);
  treeArr.forEach(([x, z, s], i) => {
    o3.rotation.set(0, 0, 0); o3.scale.setScalar(s * 1.3);
    o3.position.set(x, 0.8 * s * 1.3, z); o3.updateMatrix(); trunks.setMatrixAt(i, o3.matrix);
    o3.position.set(x, 2.3 * s * 1.3, z); o3.updateMatrix(); leaf1.setMatrixAt(i, o3.matrix);
    o3.position.set(x, 3.8 * s * 1.3, z); o3.updateMatrix(); leaf2.setMatrixAt(i, o3.matrix);
  });
  scene.add(trunks, leaf1, leaf2);
  // gunung low-poly mengelilingi cakrawala
  const mtnMats = [std(0xA7C9C0, { flatShading: true, roughness: 1, fog: false }), std(0xB5B2E6, { flatShading: true, roughness: 1, fog: false }), std(0x9DBFC9, { flatShading: true, roughness: 1, fog: false })];
  const snow = std(0xFFFFFF, { flatShading: true, roughness: 1, fog: false });
  for (let i = 0; i < 34; i++) {
    const a = (i / 34) * Math.PI * 2 + rnd() * 0.1, r = 620 + rnd() * 140, h = 90 + rnd() * 140, rad = 90 + rnd() * 70;
    const m = new THREE.Mesh(new THREE.ConeGeometry(rad, h, 5 + (i % 3), 1), mtnMats[i % 3]);
    m.rotation.y = rnd() * Math.PI; scene.add(at(m, Math.cos(a) * r, h / 2 - 2, Math.sin(a) * r));
    const s = new THREE.Mesh(new THREE.ConeGeometry(rad * 0.3 + 0.6, h * 0.3 + 0.6, 5 + (i % 3), 1), snow); s.rotation.y = m.rotation.y; scene.add(at(s, Math.cos(a) * r, h - h * 0.15 - 2.2, Math.sin(a) * r));
  }
  // gunung tempat matahari/bulan bersembunyi (posisinya diatur placeOrb mengikuti kamera)
  const moonMtn = new THREE.Mesh(new THREE.ConeGeometry(1, 1, 6, 1), mtnMats[1]);
  const moonSnow = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.3, 6, 1), snow);
  scene.add(moonMtn, moonSnow);
  // mobil di jalan silang & jalan jauh
  const farCars = [];
  ZR.forEach((x, ri) => [-1, 1].forEach((dir, li) => { for (let i = 0; i < 5; i++) {
    const c = vcar(carColors[(ri + li * 3 + i) % carColors.length], (i + ri) % 4 === 1);
    c.rotation.y = dir > 0 ? -Math.PI / 2 : Math.PI / 2; c.position.set(x + dir * 3, 0.12, -420 + i * 168 + li * 60);
    c.traverse(o => { o.castShadow = false; }); scene.add(c); farCars.push({ c, dir, axis: 'z', speed: 8 + ((i + ri) % 5) });
  } }));
  [-100, 128, 215, -235].forEach((z, ri) => [-1, 1].forEach((dir, li) => { for (let i = 0; i < 4; i++) {
    const c = vcar(carColors[(ri * 2 + li + i) % carColors.length], (i + li) % 3 === 0);
    c.rotation.y = dir > 0 ? 0 : Math.PI; c.position.set(-420 + i * 210 + li * 80, 0.12, z + dir * 3);
    c.traverse(o => { o.castShadow = false; }); scene.add(c); farCars.push({ c, dir, axis: 'x', speed: 8 + ((i + ri) % 5) });
  } }));
  // balon udara voxel
  const balloons = [];
  [[0xFF8FB1, 0xFFFFFF, -60, 95, -150], [0xF5C04A, 0x7C5CE8, 140, 80, -60], [0x7AC74F, 0xFFFFFF, -190, 110, 40]].forEach(([a, b, x, y, z], i) => {
    const g = new THREE.Group(), ma = std(a, { flatShading: true }), mb = std(b, { flatShading: true });
    [[5, 0], [7, 2.5], [7.6, 5], [7, 7.5], [5, 10]].forEach(([s, yy], j) => g.add(at(box(s, 2.5, s, j % 2 ? mb : ma, false, false), 0, 8 + yy, 0)));
    g.add(at(box(2.4, 1.6, 2.4, V.trunk, false, false), 0, 0.8, 0));
    [-1, 1].forEach(sx => [-1, 1].forEach(sz => g.add(at(box(0.12, 6.5, 0.12, V.wheel, false, false), sx * 1.1, 4.4, sz * 1.1))));
    g.scale.setScalar(1.4); g.position.set(x, y, z); scene.add(g); balloons.push({ g, x, y, z, ph: i * 2.1 });
  });
  function moveWorld(dt, now) {
    const sec = now / 1000;
    farCars.forEach(k => { const p = k.c.position; p[k.axis] += k.dir * k.speed * dt; if (p[k.axis] > 430) p[k.axis] = -430; if (p[k.axis] < -430) p[k.axis] = 430; });
    logs.forEach(l => { l.m.position.x += l.dir * l.speed * dt; if (l.m.position.x > 450) l.m.position.x = -450; if (l.m.position.x < -450) l.m.position.x = 450; l.m.position.y = 0.35 + Math.sin(sec * 1.5 + l.m.position.x) * 0.08; });
    train.position.x += 26 * dt; if (train.position.x > 520) train.position.x = -520;
    balloons.forEach(b => { b.g.position.set(b.x + Math.sin(sec * 0.05 + b.ph) * 40, b.y + Math.sin(sec * 0.4 + b.ph) * 3, b.z + Math.cos(sec * 0.04 + b.ph) * 25); });
  }

  // ── langit mengikuti jam pengunjung: pagi, siang, senja, malam ──
  const SKY = [            // jam, langit atas, cakrawala, warna & kekuatan matahari, cahaya lingkungan
    [0, 0x0A0F2E, 0x232A5C, 0x9FB4FF, 0.35, 0.32],
    [4.5, 0x0E1438, 0x2B2F66, 0x9FB4FF, 0.35, 0.34],
    [6, 0x6874D6, 0xFFB38A, 0xFFC59A, 1.2, 0.75],
    [8, 0x86C2FF, 0xE6F1FF, 0xFFF4E6, 2.1, 1.0],
    [15.5, 0x86C2FF, 0xE6F1FF, 0xFFF4E6, 2.2, 1.0],
    [17.6, 0x7A6AD8, 0xFF9E7A, 0xFFB07A, 1.4, 0.8],
    [18.7, 0x2E2F72, 0x9A6AB8, 0xC9A0FF, 0.6, 0.5],
    [20, 0x0D1236, 0x262C60, 0x9FB4FF, 0.35, 0.34],
    [24, 0x0A0F2E, 0x232A5C, 0x9FB4FF, 0.35, 0.32],
  ];
  const skyU = { top: { value: new THREE.Color() }, bot: { value: new THREE.Color() } };
  const skyDome = new THREE.Mesh(new THREE.SphereGeometry(950, 32, 16), new THREE.ShaderMaterial({
    uniforms: skyU, side: THREE.BackSide, depthWrite: false, fog: false,
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'uniform vec3 top; uniform vec3 bot; varying vec3 vP; void main(){ float h = clamp(vP.y*1.6+0.05,0.0,1.0); gl_FragColor = vec4(mix(bot, top, pow(h,0.8)),1.0); }',
  }));
  scene.add(skyDome);
  // bintang (hanya terlihat malam)
  const starGeo = new THREE.BufferGeometry(), sp = [];
  for (let i = 0; i < 600; i++) { const u = Math.random() * Math.PI * 2, v = 0.15 + Math.random() * 0.85; sp.push(Math.cos(u) * 900 * Math.sqrt(1 - v * v), v * 900, Math.sin(u) * 900 * Math.sqrt(1 - v * v)); }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(sp, 3));
  const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xFFFFFF, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0, fog: false, depthWrite: false }));
  scene.add(stars);
  const night = { v: 0 };
  let skyHour = null;                                                   // null = jam asli pengunjung
  function applySky() {
    const d = new Date(), h = skyHour !== null ? skyHour : d.getHours() + d.getMinutes() / 60;
    let i = 0; while (i < SKY.length - 2 && SKY[i + 1][0] <= h) i++;
    const a = SKY[i], b = SKY[i + 1], t = (h - a[0]) / (b[0] - a[0]);
    const c = (x, y) => new THREE.Color(x).lerp(new THREE.Color(y), t);
    skyU.top.value.copy(c(a[1], b[1])); skyU.bot.value.copy(c(a[2], b[2]));
    sun.color.copy(c(a[3], b[3])); sun.intensity = a[4] + (b[4] - a[4]) * t;
    hemi.intensity = a[5] + (b[5] - a[5]) * t;
    hemi.color.copy(skyU.top.value).lerp(new THREE.Color(0xffffff), 0.6);
    const ang = ((h - 6) / 12) * Math.PI;                                  // matahari terbit 06:00, terbenam 18:00
    const day = h >= 5.5 && h <= 18.5;
    sun.position.set(Math.cos(ang) * 80 + 20, day ? Math.max(18, Math.sin(ang) * 100) : 90, 55);
    scene.fog.color.copy(skyU.bot.value); gl.setClearColor(skyU.bot.value, 1);
    night.v = Math.max(0, Math.min(1, (0.9 - sun.intensity) / 0.55));
    stars.material.opacity = night.v;
    root.classList.toggle('gd-night', night.v > 0.5);
    // malam: lampu gedung & jendela lebih terang
    [ceilLight, screenGlow].forEach(m => { m.emissiveIntensity = 1.1 + night.v * 1.6; });
    gl.toneMappingExposure = 1.05 + night.v * 0.15;
    winU.uNight.value = night.v;
    [...mtnMats, snow].forEach(m => { m.userData.c0 ??= m.color.clone(); m.color.copy(m.userData.c0).multiplyScalar(1 - night.v * 0.6); });
    signMat.emissiveIntensity = 0.6 + night.v * 1.6; logoNavy.emissiveIntensity = 0.35 + night.v * 0.8; haloBase = 0.4 + night.v * 0.5; logoLight.intensity = night.v * 900;
    scene.traverse(o => { if (!o.material) return; (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => {   // malam: pantulan lingkungan ikut redup
      if (m.envMapIntensity === undefined) return;
      if (m.userData.env0 === undefined) m.userData.env0 = m.envMapIntensity;
      m.envMapIntensity = m.userData.env0 * (1 - night.v * 0.75);
    }); });
    // cakram matahari/bulan
    orbMat.color.set(night.v > 0.5 ? 0xEEF1FF : (h < 7 || h > 17 ? 0xFFB070 : 0xFFE27A));
    halo.material.color.set(night.v > 0.5 ? 0xB9C4FF : 0xFFE9A8);
  }
  // matahari/bulan yang bisa diklik
  const orbMat = new THREE.MeshBasicMaterial({ color: 0xFFE27A, fog: false });
  const orb = new THREE.Mesh(new THREE.CircleGeometry(16, 40), orbMat);
  const halo = new THREE.Mesh(new THREE.CircleGeometry(30, 40), new THREE.MeshBasicMaterial({ color: 0xFFE9A8, transparent: true, opacity: 0.25, fog: false, depthWrite: false }));
  halo.position.z = -0.5; orb.add(halo);
  orb.position.set(5, 150, -250); scene.add(orb);
  const CYCLE = [7, 12, 17.9, 22];
  function nextSky() {
    const d = new Date(), cur = skyHour !== null ? skyHour : d.getHours() + d.getMinutes() / 60;
    if (skyHour !== null && skyHour === CYCLE[CYCLE.length - 1]) skyHour = null;      // setelah malam kembali ke jam asli
    else skyHour = CYCLE.find(x => x > cur + 0.1) ?? CYCLE[0];
    applySky();
  }
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  gl.domElement.addEventListener('click', e => {
    ndc.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    if (ray.intersectObject(orb, true).length) nextSky();
  });
  gl.domElement.addEventListener('mousemove', e => {
    ndc.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    gl.domElement.style.cursor = ray.intersectObject(orb, true).length ? 'pointer' : '';
  });

  // ── awan voxel ──
  const cloudMat = std(0xFFFFFF, { flatShading: true, roughness: 1 });
  const clouds = [];
  for (let i = 0; i < 12; i++) {
    const g = new THREE.Group(), n = 3 + (i % 3);
    for (let j = 0; j < n; j++) g.add(at(box(8 + (j % 2) * 4, 3 + (j % 2) * 1.5, 6 + (j % 3) * 2, cloudMat, false, false), j * 6 - n * 3, (j % 2) * 1.5, (j % 3) * 2 - 2));
    g.position.set(-200 + i * 36, 70 + (i * 13) % 45, -120 + ((i * 47) % 220));
    scene.add(g); clouds.push({ g, speed: 1.5 + (i % 4) * 0.6 });
  }
  // ── burung voxel: kawanan terbang melingkar, sayap mengepak ──
  const birdMat = std(0x3E2A57, { flatShading: true });
  const birds = [];
  for (let i = 0; i < 9; i++) {
    const g = new THREE.Group();
    g.add(at(box(0.5, 0.4, 1.3, birdMat, false, false), 0, 0, 0));
    g.add(at(box(0.32, 0.3, 0.3, std(0xF5C04A), false, false), 0, 0.05, -0.75));
    const wl = new THREE.Group(), wr = new THREE.Group();
    wl.add(at(box(1.4, 0.08, 0.6, birdMat, false, false), -0.7, 0, 0)); wr.add(at(box(1.4, 0.08, 0.6, birdMat, false, false), 0.7, 0, 0));
    wl.position.x = -0.25; wr.position.x = 0.25; g.add(wl, wr);
    g.scale.setScalar(1.6);
    scene.add(g); birds.push({ g, wl, wr, off: i * 0.55, r: 55 + (i % 3) * 6, y: 62 + (i % 4) * 3, ph: i * 1.3 });
  }
  function animateSky(now) {
    const sec = now / 1000;
    orb.lookAt(camera.position);
    logo3d.rotation.y = Math.sin(sec * 0.6) * 0.4;                         // logo berayun pelan supaya bentuk 3D-nya terlihat
    clouds.forEach(c => { c.g.position.x += c.speed * 0.016; if (c.g.position.x > 260) c.g.position.x = -260; });
    cloudMat.color.setRGB(1 - night.v * 0.62, 1 - night.v * 0.6, 1 - night.v * 0.45);
    birds.forEach(b => {
      const a = sec * 0.18 + b.off;
      b.g.position.set(Math.cos(a) * b.r + 10, b.y + Math.sin(sec * 1.3 + b.ph) * 1.5, Math.sin(a) * b.r - 10);
      b.g.rotation.y = -a;                                                  // menghadap arah terbang
      const f = Math.sin(sec * 9 + b.ph) * 0.7;
      b.wl.rotation.z = f; b.wr.rotation.z = -f;
      b.g.visible = night.v < 0.7;                                          // malam: burung pulang
    });
  }

  // ── salinan sampul/penutup di layar ──
  const faces = {};
  for (const k in screens) {
    const el = document.createElement('div');
    el.className = 'gd-face'; el.setAttribute('aria-hidden', 'true');
    const obj = new CSS3DObject(el);
    obj.position.z = 0.004;
    screens[k].holder.add(obj);
    el.style.visibility = 'hidden';                    // kosong = tak terlihat (lapisan HTML selalu di atas WebGL)
    faces[k] = { el, obj, shown: null };
  }
  function showFace(k, which) {                       // which: 'cover' | 'close' | null
    const f = faces[k];
    if (f.shown === which) return;
    f.shown = which;
    if (which && !f.wrap) {
      const wrap = document.createElement('div'); wrap.id = 'top-face';      // aturan 'main#top ...' ikut berlaku
      const c = coverEl.cloneNode(true);
      c.removeAttribute('style'); c.removeAttribute('data-gd-cover'); c.removeAttribute('id');
      c.style.setProperty('margin-top', '0px', 'important'); c.style.setProperty('min-height', (VH / Z) + 'px', 'important');
      c.querySelectorAll('.reveal').forEach(x => x.classList.add('revealed'));
      c.querySelectorAll('[id]').forEach(x => x.removeAttribute('id'));
      wrap.style.width = (VW / Z) + 'px'; wrap.style.height = (VH / Z) + 'px';
      wrap.style.transformOrigin = '0 0'; wrap.style.transform = 'scale(' + Z + ')';   // tata letak selebar halaman (zoom), lalu diperkecil seperti zoom
      wrap.appendChild(c); f.wrap = wrap;
    }
    f.el.replaceChildren(...(which ? [f.wrap] : []));
    f.el.style.visibility = which ? '' : 'hidden';
  }

  // ── kamera ──
  const clamp = v => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const TAN = Math.tan(THREE.MathUtils.degToRad(16));
  const tq = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0);
  let VW = innerWidth, VH = innerHeight, Z = 1;
  function screenFrame(k) {                           // pusat & arah hadap layar k saat lantainya belum terangkat
    const s = screens[k], g = floors[k].g, saved = g.position.y;
    g.position.y = base(k); g.updateMatrixWorld(true);
    const c = new THREE.Vector3().setFromMatrixPosition(s.holder.matrixWorld);
    s.holder.getWorldQuaternion(tq);
    g.position.y = saved; g.updateMatrixWorld(true);
    const n = new THREE.Vector3(0, 0, 1).applyQuaternion(tq).normalize();
    const side = new THREE.Vector3().crossVectors(up, n).normalize();
    const camUp = new THREE.Vector3().crossVectors(n, side).normalize();
    return { c, n, side, camUp, s };
  }
  const poses = {};
  function buildPoses() {
    for (const kk in screens) {
      const k = +kk, f = screenFrame(k), d = (f.s.h / 2) / TAN;
      const fill = { pos: f.c.clone().addScaledVector(f.n, d), look: f.c.clone(), up: f.camUp.clone() };
      const back = Math.max(d * 3.2, f.s.hand ? 1.6 : 7);
      const room = { pos: f.c.clone().addScaledVector(f.n, back).addScaledVector(f.side, back * 0.32).addScaledVector(up, back * 0.28), look: f.c.clone().addScaledVector(up, -0.15 * back * 0.3), up: up.clone() };
      const lim = { x: W / 2 - 1.2, zMax: D / 2 - 1.2, yMax: base(k) + height(k) - 0.4 };   // kamera tetap di dalam ruangan
      room.pos.x = Math.max(-lim.x, Math.min(lim.x, room.pos.x));
      room.pos.z = Math.min(lim.zMax, room.pos.z);
      room.pos.y = Math.min(lim.yMax, room.pos.y);
      poses[k] = { fill, room };
    }
  }
  const far = () => {                                                  // desktop: gedung di kanan (panel teks di kiri); mobile: gedung di atas (panel di bawah)
    const narrow = VW < 900, az = 0.62, el = narrow ? 0.14 : 0.1, d = narrow ? 330 : 230;
    const look = new THREE.Vector3(0, narrow ? 13 : 47, 0);
    if (!narrow) look.add(new THREE.Vector3(-Math.cos(az), 0, Math.sin(az)).multiplyScalar(Math.min(60, 0.26 * TAN * d * (VW / VH) * 2)));
    return { pos: new THREE.Vector3(Math.sin(az) * Math.cos(el) * d, look.y + Math.sin(el) * d, Math.cos(az) * Math.cos(el) * d).add(new THREE.Vector3(look.x, 0, look.z)), look, up };
  };
  const above = (k = N) => ({ pos: new THREE.Vector3(18, base(k) + height(k) + 34, 40), look: new THREE.Vector3(0, base(k) + 2, -1), up });
  const vA = new THREE.Vector3(), vB = new THREE.Vector3(), vU = new THREE.Vector3(), arcV = new THREE.Vector3();
  function blend(a, b, t, arc = 0) {
    vA.lerpVectors(a.pos, b.pos, t);
    if (arc) vA.add(arcV.set(arc * 0.35, arc * 0.5, arc).multiplyScalar(Math.sin(Math.PI * t)));
    vB.lerpVectors(a.look, b.look, t);
    vU.lerpVectors(a.up, b.up, t).normalize();
    camera.position.copy(vA); camera.up.copy(vU); camera.lookAt(vB);
  }
  const seg = (t, a, b) => ease(clamp((t - a) / (b - a)));

  // ── tinggi adegan & ukuran layar ──
  function resize() {
    VW = document.documentElement.clientWidth || innerWidth; VH = innerHeight;
    Z = parseFloat(getComputedStyle(document.body).zoom) || 1;               // situs memakai zoom .9 di desktop
    const cw = VW / Z, ch = VH / Z;                                          // ukuran dalam px CSS halaman
    root.style.setProperty('--vhp', ch + 'px');
    gl.setSize(VW, VH, false);
    css.domElement.style.zoom = String(1 / Z);                               // lapisan 3D bekerja di px layar, tanpa zoom halaman
    css.setSize(VW, VH);
    camera.aspect = VW / VH; camera.updateProjectionMatrix();
    sizeScreens(VW / VH);
    for (const k in faces) {
      const f = faces[k], s = screens[k];
      f.el.style.width = VW + 'px'; f.el.style.height = VH + 'px';         // px layar
      f.obj.scale.setScalar(s.w / VW);
      if (f.wrap) { f.wrap.style.width = cw + 'px'; f.wrap.style.height = ch + 'px'; f.wrap.style.transform = 'scale(' + Z + ')'; }
    }
    scenes.forEach(sc => {
      const to = +sc.dataset.to, from = +(sc.dataset.from || 0);
      const len = 3.2;      // intro, penutup, antar-ruangan (dalam tinggi layar)
      sc.style.setProperty('--scene-h', (len * ch) + 'px');
    });
    if (coverEl) { coverEl.style.setProperty('margin-top', -ch + 'px', 'important'); coverEl.style.setProperty('min-height', ch + 'px', 'important'); faces[N] && (faces[N].wrap = null, faces[N].shown = null); }
    buildPoses();
    placeOrb();
  }
  function placeOrb() {                                                  // matahari/bulan terbit di balik puncak gunung, kanan atas pandangan
    const f = far(), dir = f.look.clone().sub(f.pos).normalize();
    const right = new THREE.Vector3().crossVectors(dir, up).normalize();
    const narrow = VW < 900, ref = 420;
    const vh = 2 * TAN * ref, vw = vh * (VW / VH);
    const aim = f.pos.clone().addScaledVector(dir, ref).addScaledVector(right, vw * (narrow ? 0.3 : 0.37)).sub(f.pos);
    const hd = new THREE.Vector3(aim.x, 0, aim.z).normalize();
    const b = f.pos.x * hd.x + f.pos.z * hd.z, R = 700, cc = f.pos.x * f.pos.x + f.pos.z * f.pos.z - R * R;
    const sd = -b + Math.sqrt(b * b - cc);                               // jarak datar kamera -> lingkar gunung
    const pitch = Math.asin(dir.y), elev = pitch + (narrow ? 0.52 : 0.6) * THREE.MathUtils.degToRad(16);
    const H = f.pos.y + sd * Math.tan(elev), rad = H * 0.7;
    const px = f.pos.x + hd.x * sd, pz = f.pos.z + hd.z * sd;
    moonMtn.scale.set(rad, H, rad); moonMtn.position.set(px, H / 2 - 2, pz);
    moonSnow.scale.set(rad, H, rad); moonSnow.position.set(px, H - H * 0.15 - 2, pz);
    const od = sd + 220, orbR = 0.04 * od;                                 // ukuran tampak tetap seperti sebelumnya
    orb.scale.setScalar(orbR / 16);
    const tip = new THREE.Vector3(px, H - 2, pz).sub(f.pos).normalize();
    orb.position.copy(f.pos).addScaledVector(tip, od).addScaledVector(up, orbR * 0.15);   // separuh bawah tertutup puncak
  }

  function setLift(k, lift, rise = 44) { const f = floors[k]; f.g.position.y = base(k) + lift * rise; f.g.rotation.z = lift * 0.05; f.g.visible = lift < 0.985; }
  function setRoof(lift, rise = 44) { roof.position.y = TOTAL + lift * rise; roof.rotation.z = -lift * 0.05; roofAll.forEach(m => { m.opacity = 1 - clamp(lift * 1.3); }); logoHalo.material.opacity = haloBase * (1 - clamp(lift * 1.3)); roof.visible = lift < 0.985; }

  // ── adegan aktif ──
  function activeScene() {
    for (const sc of scenes) {
      const r = sc.getBoundingClientRect(), span = r.height - VH;
      const intro = !sc.dataset.from;
      if ((r.top <= 0.5 || (intro && r.top < VH)) && -r.top <= span - 0.5) return { sc, t: clamp(-r.top / span) };
    }
    return null;
  }
  let on3d = false;
  let visit = null;                                                    // { k, t0 } saat lantai diklik
  const VISIT_MS = 2600;
  function frame() {
    if (visit) return visitFrame();
    const a = activeScene();
    if (!a || a.t >= 0.999) { if (on3d) { root.classList.remove('gd-3d-on'); on3d = false; } return false; }
    if (!on3d) { root.classList.add('gd-3d-on'); on3d = true; }
    const t = a.t;
    const lifts = {}; for (let k = 1; k <= N; k++) lifts[k] = 0;
    let roofLift = 1, hero = 0, outro = 0;
    const want = {};
    {                                                    // luar gedung -> atap -> ruang meeting -> layar
      hero = 1 - clamp(t / 0.14);
      roofLift = seg(t, 0.24, 0.5);
      if (t < 0.36) blend(far(), above(), seg(t, 0, 0.36));
      else if (t < 0.7) blend(above(), poses[N].room, seg(t, 0.36, 0.7));
      else blend(poses[N].room, poses[N].fill, seg(t, 0.7, 1));
      if (t > 0.42) want[N] = 'cover';                                // isi layar HTML tidak bisa tertutup atap: tampilkan setelah atap terangkat
      beam.material.opacity = 0.15 * clamp((t - 0.55) / 0.2);
    }
    for (const k in faces) showFace(+k, want[k] || null);       // hanya berubah bila isinya berganti
    for (let k = 1; k <= N; k++) setLift(k, lifts[k]);
    setRoof(roofLift);
    root.style.setProperty('--hero', hero);
    root.style.setProperty('--outro', outro);
    return true;
  }
  function visitFrame() {
    const k = visit.k, t = clamp((performance.now() - visit.t0) / VISIT_MS), rise = TOTAL - base(k) + 70;
    const open = seg(t, 0.04, 0.32);                                  // lantai di atasnya & atap terangkat
    for (let j = 1; j <= N; j++) setLift(j, j > k ? open : 0, rise);
    setRoof(k === N ? seg(t, 0.04, 0.32) : open, rise);
    if (t < 0.36) blend(visit.from, above(k), seg(t, 0, 0.36));
    else if (t < 0.7) blend(above(k), poses[k].room, seg(t, 0.36, 0.7));
    else blend(poses[k].room, poses[k].fill, seg(t, 0.7, 1));
    for (const f in faces) showFace(+f, null);
    beam.material.opacity = k === N ? 0.15 * clamp((t - 0.5) / 0.2) : 0;
    root.style.setProperty('--hero', 1 - clamp(t / 0.12));
    hl.visible = false; tip.style.opacity = 0;
    if (t >= 1 && !visit.gone) { visit.gone = true; location.href = PAGES[k][1]; }
    return true;
  }
  function startVisit(k) {
    if (visit || auto) return;
    const ip = introProgress(); if (!ip || ip.t > 0.02) return;           // hanya dari tampilan awal gedung
    if (k === N) screens[N].surface.material = LABELS[N].mat;
    visit = { k, t0: performance.now(), from: far() };
    auto = true;                                                         // input scroll diabaikan selama perjalanan
  }
  addEventListener('pageshow', e => { if (e.persisted && visit) { visit = null; auto = null; screens[N].surface.material = M.white; scrollTo({ top: 0, behavior: 'instant' }); } });

  // sorot lantai saat kursor di atasnya + label halaman
  const hits = [];
  for (let k = 1; k <= N; k++) { const m = new THREE.Mesh(new THREE.BoxGeometry(W + 1.4, height(k), D + 1.4)); m.position.y = base(k) + height(k) / 2; m.visible = false; m.userData.k = k; m.updateMatrixWorld(); hits.push(m); }
  const hl = new THREE.Mesh(new THREE.BoxGeometry(W + 1.6, 1, D + 1.6), new THREE.MeshBasicMaterial({ color: 0x9B6BFF, transparent: true, opacity: 0.45, depthWrite: false, fog: false, toneMapped: false }));
  hl.visible = false; scene.add(hl);
  const tip = document.createElement('div'); tip.className = 'gd-floortip'; tip.setAttribute('aria-hidden', 'true'); root.appendChild(tip);
  function floorAt(e) {
    const ip = introProgress(); if (visit || auto || !ip || ip.t > 0.02) return 0;
    ndc.set((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    if (ray.intersectObject(orb, true).length) return 0;
    const h = ray.intersectObjects(hits, false)[0];
    return h ? h.object.userData.k : 0;
  }
  gl.domElement.addEventListener('mousemove', e => {
    const k = floorAt(e);
    hl.visible = !!k; tip.style.opacity = k ? 1 : 0;
    if (k) {
      hl.scale.y = height(k) + 0.1; hl.position.y = base(k) + height(k) / 2;
      tip.innerHTML = PAGES[k][0] + ' <span aria-hidden="true">→</span>';
      tip.style.transform = 'translate(' + (e.clientX / Z + 16) + 'px,' + (e.clientY / Z - 14) + 'px)';
      gl.domElement.style.cursor = 'pointer';
    }
  });
  gl.domElement.addEventListener('mouseleave', () => { hl.visible = false; tip.style.opacity = 0; });
  gl.domElement.addEventListener('click', e => { const k = floorAt(e); if (k) startVisit(k); });

  const t0 = performance.now();
  let skyTick = 0;
  function loop() {
    const cw = document.documentElement.clientWidth || innerWidth;
    if (cw !== VW || innerHeight !== VH) resize();                        // zoom/resize yang tidak memicu event
    if (frame()) {
      const tt = (performance.now() - t0) / 1000;
      beacon.material.emissiveIntensity = 1.2 + Math.sin(tt * 3.3);
      moveCars(performance.now());
      animateSky(performance.now());
      if (++skyTick % 600 === 1) applySky();                                    // perbarui langit tiap ~10 detik
      leds.forEach((l, i) => { l.visible = Math.sin(tt * 4 + i * 1.7) > -0.3; });
      gl.render(scene, camera);
      css.render(scene, camera);
    }
    requestAnimationFrame(loop);
  }
  // ── sekali scroll ke bawah di pembuka -> animasi berjalan sendiri sampai beranda ──
  let auto = null;
  function introProgress() {
    const sc = scenes[0]; if (!sc) return null;
    const r = sc.getBoundingClientRect(), span = r.height - VH;
    if (-r.top > span - 1) return null;                                    // sudah lewat pembuka
    return { r, span, t: clamp(-r.top / span) };
  }
  function playIntro() {
    const ip = introProgress(); if (!ip || auto) return false;
    const from = scrollY, dist = (ip.r.top + ip.span) / Z + 2;             // px CSS sampai pembuka selesai
    const dur = 3200 * (1 - ip.t) + 400, t0 = performance.now();
    const ez = x => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2);
    auto = true;
    (function step(now) {
      const k = Math.min(1, (now - t0) / dur);
      scrollTo({ top: from + dist * ez(k), behavior: 'instant' });          // situs memakai scroll-behavior:smooth
      if (k < 1) requestAnimationFrame(step); else auto = null;
    })(t0);
    return true;
  }
  const block = e => { if (auto) { e.preventDefault(); return true; } return false; };
  addEventListener('wheel', e => { if (block(e)) return; if (e.deltaY > 4 && introProgress() && playIntro()) e.preventDefault(); }, { passive: false });
  let ty0 = null;
  addEventListener('touchstart', e => { ty0 = e.touches[0].clientY; }, { passive: true });
  addEventListener('touchmove', e => {
    if (block(e)) return;
    if (ty0 !== null && ty0 - e.touches[0].clientY > 8 && introProgress() && playIntro()) e.preventDefault();
  }, { passive: false });
  addEventListener('keydown', e => {
    if (!['ArrowDown', 'PageDown', ' ', 'Spacebar', 'End'].includes(e.key)) return;
    if (block(e)) return;
    if (introProgress() && playIntro()) e.preventDefault();
  });
  addEventListener('resize', resize);
  if (window.visualViewport) visualViewport.addEventListener('resize', resize);
  resize();
  loop();
}
