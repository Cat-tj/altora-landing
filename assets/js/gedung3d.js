/* Pembuka beranda "gedung Altora" (Three.js), dipakai di /preview-gedung.
   Adegan: gedung kaca utuh -> atap terangkat -> kamera masuk ke ruang meeting di lantai teratas -> layar proyektor
   menampilkan salinan hero beranda seukuran layar pengunjung -> saat layar memenuhi layar, kanvas 3D disembunyikan dan
   beranda asli (tepat di posisi yang sama) berlanjut seperti biasa. Lantai lain hanya tampak dari luar. */
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
  const scenes = [...root.querySelectorAll('.gd-scene')];
  const coverEl = root.querySelector('[data-gd-cover]');              // hero beranda = isi layar proyektor
  const mobile = innerWidth < 900;
  if (mobile) root.classList.add('gd-m');

  // ── ukuran gedung (meter) ──
  const W = 24, D = 17, FH = 6, LOBBY = 7, N = 7, SLAB = 0.5;
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
  scene.fog = new THREE.Fog(BG, 180, 420);
  const pmrem = new THREE.PMREMGenerator(gl);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(32, 1, 0.05, 1000);

  // ── cahaya ──
  scene.add(new THREE.HemisphereLight(0xF4F0FF, 0xCFC3FA, 1.0));
  const sun = new THREE.DirectionalLight(0xFFF4E6, 2.2);
  sun.position.set(45, 90, 55);
  sun.castShadow = true;
  sun.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 70, bottom: -25, near: 10, far: 260 });
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
    glass: new THREE.MeshPhysicalMaterial({ color: 0x8C76F2, roughness: 0.06, metalness: 0.15, transparent: true, opacity: 0.4, envMapIntensity: 1.4, clearcoat: 1, clearcoatRoughness: 0.08 }),
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
  function person({ shirt = 0x7C5CE8, seated = false, arms = 'down' } = {}) {
    const g = new THREE.Group(), shirtM = std(shirt);
    const hip = seated ? 0.5 : 0.95;
    if (seated) {
      [-0.11, 0.11].forEach(x => { g.add(at(box(0.15, 0.14, 0.5, M.pants), x, 0.5, -0.22)); g.add(at(box(0.14, 0.48, 0.14, M.pants), x, 0.24, -0.45)); });
    } else {
      [-0.11, 0.11].forEach(x => g.add(at(box(0.15, 0.92, 0.17, M.pants), x, 0.46, 0)));
    }
    const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.21, 0.42, 6, 12), shirtM); torso.castShadow = true;
    torso.scale.z = 0.72; g.add(at(torso, 0, hip + 0.38, 0));
    g.add(at(cyl(0.07, 0.07, 0.12, M.skin), 0, hip + 0.76, 0));
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.135, 20, 16), M.skin); head.castShadow = true; g.add(at(head, 0, hip + 0.92, 0));
    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.142, 20, 12, 0, Math.PI * 2, 0, Math.PI * 0.55), M.hair); g.add(at(hair, 0, hip + 0.94, 0.01));
    const hands = [];
    [-0.27, 0.27].forEach((x, i) => {
      const a = new THREE.Group(); a.position.set(x, hip + 0.66, 0);
      a.add(at(cyl(0.058, 0.052, 0.34, shirtM), 0, -0.17, 0));
      const fore = new THREE.Group(); fore.position.set(0, -0.34, 0); a.add(fore);
      fore.add(at(cyl(0.05, 0.045, 0.3, M.skin), 0, -0.15, 0));
      const hand = at(new THREE.Mesh(new THREE.SphereGeometry(0.055, 10, 8), M.skin), 0, -0.31, 0); fore.add(hand);
      hands.push(hand);
      if (arms === 'hold') { a.rotation.x = -0.75; a.rotation.z = i ? 0.32 : -0.32; fore.rotation.x = -1.0; fore.rotation.z = i ? -0.55 : 0.55; }
      else if (arms === 'phone' && i === 1) { a.rotation.x = -0.55; a.rotation.z = 0.12; fore.rotation.x = -1.55; }
      else if (arms === 'desk') { a.rotation.x = -0.95; a.rotation.z = i ? 0.12 : -0.12; fore.rotation.x = -0.45; }
      else a.rotation.z = i ? 0.08 : -0.08;
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
  function plant(s = 1) {
    const g = new THREE.Group();
    g.add(at(cyl(0.28 * s, 0.22 * s, 0.5 * s, M.pot), 0, 0.25 * s, 0));
    const leaf = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55 * s, 0), M.plant); leaf.castShadow = true;
    g.add(at(leaf, 0, 0.95 * s, 0)); return g;
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
  }

  let beam = null;
  const leds = [];
  const ROOMS = {
    // 7 · ruang meeting: proyektor menyala ke layar
    7(room, k) {
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
        if (i % 2 === 0 || i === 3) { const p = person({ seated: true, shirt: [0x7C5CE8, 0xFFFFFF, 0x3E2A97, 0xC9BCFA][i] }); p.rotation.y = 0.15 * (i - 1.5); room.add(at(p, x, 0, 3.0)); }
      }
      const proj = new THREE.Group(); proj.add(at(box(0.55, 0.2, 0.5, M.white), 0, 0, 0)); proj.add(at(cyl(0.07, 0.07, 0.06, M.dark), 0, 0, -0.27)); proj.children[1].rotation.x = Math.PI / 2;
      room.add(at(proj, 0, 0.87, 2.2));
      [[-10.5, -6.5], [10.5, -6.5], [-10.5, 6.5], [10.5, 6.5]].forEach(([x, z]) => room.add(at(plant(1.1), x, 0, z)));
    },
  };

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
    if (k === N) ROOMS[k](room, k);                                  // hanya lantai teratas yang dikunjungi kamera
    else room.add(at(box(W - 1.2, 0.05, D - 1.2, M.lilac, false, true), 0, 0.03, 0));
    g.position.y = base(k);
    floors[k] = { g, h };
  }

  // ── atap ──
  const roof = new THREE.Group();
  const roofMats = { roof: std(0x5B3FC4, { roughness: 0.5, metalness: 0.2 }), hvac: std(0xE4DEFA, { roughness: 0.5, metalness: 0.4 }), slab: M.slab.clone(), frame: M.frame.clone() };
  roof.add(at(box(W + 1.2, 0.9, D + 1.2, roofMats.roof), 0, 0.45, 0));
  [[0, D / 2 + 0.4], [0, -D / 2 - 0.4]].forEach(([x, z]) => roof.add(at(box(W + 1.2, 1.2, 0.4, roofMats.slab), x, 1.5, z)));
  [[W / 2 + 0.4, 0], [-W / 2 - 0.4, 0]].forEach(([x, z]) => roof.add(at(box(0.4, 1.2, D + 1.2, roofMats.slab), x, 1.5, z)));
  [[-6, -3], [-1, -4], [6, 2]].forEach(([x, z]) => roof.add(at(box(3.4, 1.8, 2.6, roofMats.hvac), x, 1.8, z)));
  roof.add(at(box(0.25, 7, 0.25, roofMats.frame), 8, 4.4, -4));
  const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.45, 16, 12), new THREE.MeshStandardMaterial({ color: 0xFF6B9A, emissive: 0xFF3D7F, emissiveIntensity: 2, transparent: true }));
  roof.add(at(beacon, 8, 8.1, -4));
  const signTex = canvasTex(1024, 220, (x) => { x.fillStyle = '#fff'; x.fillRect(0, 0, 1024, 220); x.fillStyle = '#5B3FC4'; x.font = '800 150px "Plus Jakarta Sans", system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('A L T O R A', 512, 118); });
  const signMat = new THREE.MeshStandardMaterial({ map: signTex, emissive: 0xffffff, emissiveMap: signTex, emissiveIntensity: 0.35, transparent: true });
  const sign = new THREE.Mesh(new THREE.BoxGeometry(12, 2.6, 0.3), [roofMats.frame, roofMats.frame, roofMats.frame, roofMats.frame, signMat, roofMats.frame]);
  sign.castShadow = true; roof.add(at(sign, -1, 3.6, D / 2 - 1.2));
  [-5.5, 3.5].forEach(x => roof.add(at(box(0.25, 2.4, 0.25, roofMats.frame), x, 1.6, D / 2 - 1.2)));
  roof.position.y = TOTAL; scene.add(roof);
  const roofAll = [...Object.values(roofMats), signMat, beacon.material];
  roofAll.forEach(m => { m.transparent = true; });

  // ── lingkungan ──
  const ground = new THREE.Mesh(new THREE.CircleGeometry(320, 64), std(0xF3EFFE, { roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  scene.add(at(box(W + 18, 0.3, D + 18, std(0xFFFFFF, { roughness: 0.9 }), false, true), 0, 0.15, 0));
  scene.add(at(box(320, 0.1, 9, std(0xDCD3FB, { roughness: 1 }), false, true), 0, 0.06, D / 2 + 16));
  const treeMat = [std(0xB9A8F7, { flatShading: true }), std(0xA7D7C5, { flatShading: true })];
  [[-21, 6], [-21, -6], [21, 8], [22, -5], [-12, 15], [13, 15], [-32, 19], [33, 17], [-38, -2], [38, 0]].forEach(([x, z], i) => {
    const t = new THREE.Group(); t.add(at(box(0.5, 2.8, 0.5, std(0x9B8BC9)), 0, 1.4, 0));
    const crown = new THREE.Mesh(new THREE.IcosahedronGeometry(2.1 + (i % 3) * 0.4, 0), treeMat[i % 2]); crown.castShadow = true; t.add(at(crown, 0, 4.2, 0));
    scene.add(at(t, x, 0, z));
  });
  const farMat = std(0xE4DCFF, { roughness: 0.9 });
  [[-75, -65, 34], [-48, -88, 50], [58, -75, 40], [90, -42, 26], [-100, -32, 22], [26, -100, 58]].forEach(([x, z, hh]) => scene.add(at(box(17, hh, 15, farMat, false, true), x, hh / 2, z)));


  // ── salinan sampul/penutup di layar ──
  const faces = {};
  for (const k in screens) {
    const el = document.createElement('div');
    el.className = 'gd-face'; el.setAttribute('aria-hidden', 'true');
    const obj = new CSS3DObject(el);
    obj.position.z = 0.004;
    screens[k].holder.add(obj);
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
  const far = () => {
    const look = new THREE.Vector3(0, VW < 900 ? 58 : 40, 0), az = 0.62, el = 0.1, d = VW < 900 ? 300 : 200;
    return { pos: new THREE.Vector3(Math.sin(az) * Math.cos(el) * d, look.y + Math.sin(el) * d, Math.cos(az) * Math.cos(el) * d), look, up };
  };
  const above = () => ({ pos: new THREE.Vector3(18, TOTAL + 34, 40), look: new THREE.Vector3(0, base(7) + 2, -1), up });
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
    if (coverEl) { coverEl.style.setProperty('margin-top', -ch + 'px', 'important'); coverEl.style.setProperty('min-height', ch + 'px', 'important'); faces[7] && (faces[7].wrap = null, faces[7].shown = null); }
    buildPoses();
  }

  function setLift(k, lift) { const f = floors[k]; f.g.position.y = base(k) + lift * 44; f.g.rotation.z = lift * 0.05; f.g.visible = lift < 0.985; }
  function setRoof(lift) { roof.position.y = TOTAL + lift * 44; roof.rotation.z = -lift * 0.05; roofAll.forEach(m => { m.opacity = 1 - clamp(lift * 1.3); }); roof.visible = lift < 0.985; }

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
  function frame() {
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
      else if (t < 0.7) blend(above(), poses[7].room, seg(t, 0.36, 0.7));
      else blend(poses[7].room, poses[7].fill, seg(t, 0.7, 1));
      want[7] = 'cover';
      beam.material.opacity = 0.15 * clamp((t - 0.55) / 0.2);
    }
    for (const k in faces) showFace(+k, want[k] || null);       // hanya berubah bila isinya berganti
    for (let k = 1; k <= N; k++) setLift(k, lifts[k]);
    setRoof(roofLift);
    root.style.setProperty('--hero', hero);
    root.style.setProperty('--outro', outro);
    return true;
  }

  const t0 = performance.now();
  function loop() {
    const cw = document.documentElement.clientWidth || innerWidth;
    if (cw !== VW || innerHeight !== VH) resize();                        // zoom/resize yang tidak memicu event
    if (frame()) {
      const tt = (performance.now() - t0) / 1000;
      beacon.material.emissiveIntensity = 1.2 + Math.sin(tt * 3.3);
      leds.forEach((l, i) => { l.visible = Math.sin(tt * 4 + i * 1.7) > -0.3; });
      gl.render(scene, camera);
      css.render(scene, camera);
    }
    requestAnimationFrame(loop);
  }
  addEventListener('resize', resize);
  if (window.visualViewport) visualViewport.addEventListener('resize', resize);
  resize();
  loop();
}
