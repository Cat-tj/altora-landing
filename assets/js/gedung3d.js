/* Prototipe "halaman = gedung" (Three.js). Setiap lantai adalah ruangan dengan layar yang menampilkan konten:
   7 ruang meeting (proyektor), 6 ruang direksi (TV), 5 ruang karyawan (monitor), 4 ruang server (layar monitoring),
   3 ruang keamanan (video wall CCTV), 2 HP di tangan seseorang, 1 lobi (tablet di tangan resepsionis).
   Semua digerakkan oleh scroll: gedung utuh -> atap terangkat -> kamera masuk ke layar tiap ruangan; lantai yang sudah
   dibaca terangkat dan kamera turun ke ruangan berikutnya -> di akhir gedung tersusun kembali, lalu footer.
   Konten di layar adalah HTML asli (CSS3DRenderer): tajam, bisa diklik, tetap terbaca mesin pencari. */
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
  const cards = [...root.querySelectorAll('.gc')];                     // urutan 7 -> 1
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
  stage.prepend(gl.domElement);
  const css = new CSS3DRenderer();
  css.domElement.className = 'gd-css3d';
  stage.appendChild(css.domElement);

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

  // ── layar konten: elemen HTML ditempatkan tepat di permukaannya ──
  const screens = {};
  function contentScreen(k, room, { w, h, kind, x = 0, y, z, rx = 0, ry = 0, bezel = 0.12, surface = M.screenOff }) {
    const holder = new THREE.Group();
    holder.position.set(x, y, z); holder.rotation.set(rx, ry, 0, 'YXZ');
    if (bezel) holder.add(at(box(w + bezel, h + bezel, kind === 'phone' || kind === 'tablet' ? 0.012 : 0.06, M.dark), 0, 0, kind === 'phone' || kind === 'tablet' ? -0.008 : -0.035));
    holder.add(at(box(w, h, 0.003, surface, false, false), 0, 0, 0));
    room.add(holder);
    screens[k] = { holder, w, h, kind };
    return holder;
  }

  let beam = null;
  const leds = [];
  const ROOMS = {
    // 7 · ruang meeting: proyektor menyala ke layar
    7(room, k) {
      const sw = 7.6, sh = sw * 9 / 16, sy = 0.9 + sh / 2;
      contentScreen(k, room, { w: sw, h: sh, kind: 'wide', y: sy, z: BACK, bezel: 0, surface: M.white });
      room.add(at(box(sw + 0.6, 0.22, 0.25, M.dark), 0, sy + sh / 2 + 0.2, BACK + 0.05));       // rumah layar gulung
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
      const lens = new THREE.Vector3(0, 0.87, 1.92);
      const corners = [[-sw / 2, sy - sh / 2], [sw / 2, sy - sh / 2], [sw / 2, sy + sh / 2], [-sw / 2, sy + sh / 2]].map(([x, y]) => new THREE.Vector3(x, y, BACK + 0.02));
      const pos = [];
      for (let i = 0; i < 4; i++) { const a = corners[i], b = corners[(i + 1) % 4]; pos.push(lens.x, lens.y, lens.z, a.x, a.y, a.z, b.x, b.y, b.z); }
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      beam = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0xFFF2C8, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
      room.add(beam);
      [[-10.5, -6.5], [10.5, -6.5], [-10.5, 6.5], [10.5, 6.5]].forEach(([x, z]) => room.add(at(plant(1.1), x, 0, z)));
    },
    // 6 · ruang direksi: TV dinding menampilkan dashboard
    6(room, k) {
      const sw = 4.8, sh = sw * 9 / 16;
      contentScreen(k, room, { w: sw, h: sh, kind: 'wide', y: 1.2 + sh / 2, z: BACK });
      room.add(at(box(sw + 2.4, 0.5, 0.45, M.wood), 0, 0.25, BACK + 0.4));                          // kabinet bawah TV
      const carpet = new THREE.Mesh(new THREE.PlaneGeometry(9, 6), M.carpet); carpet.rotation.x = -Math.PI / 2; carpet.position.set(0, 0.012, 1.5); carpet.receiveShadow = true; room.add(carpet);
      room.add(at(desk(3, 1.3, 0.78, M.wood), 0, 0, 2.2));
      room.add(at(monitor(0.55, 0.32), -0.8, 0.8, 1.9));
      const c = chair(0.5, M.purple); room.add(at(c, 0.6, 0, 3.4));
      const dir = person({ seated: true, shirt: 0x2A2F5E }); dir.rotation.y = 0.25; room.add(at(dir, 0.6, 0, 3.2));
      const s1 = sofa(3); s1.rotation.y = Math.PI / 2; room.add(at(s1, -8.5, 0, 1));
      room.add(at(box(1.4, 0.4, 0.9, M.wood), -6.8, 0.2, 1));
      for (let i = 0; i < 3; i++) room.add(at(box(2.2, 0.06, 0.45, M.wood), 8.8, 0.8 + i * 0.9, -4));            // rak buku
      room.add(at(box(2.2, 2.8, 0.06, M.wood), 8.8, 1.4, -4.25));
      [[-10.5, -6.5], [10.5, 6.5], [-10.5, 6.5]].forEach(([x, z]) => room.add(at(plant(1.2), x, 0, z)));
    },
    // 5 · ruang karyawan: deretan meja dan monitor; satu monitor menampilkan konten
    5(room, k) {
      [-7.5, -2.5, 2.5, 7.5].forEach((x, ix) => [-4.2, -0.6].forEach((z, iz) => {
        room.add(at(desk(1.8, 0.8), x, 0, z));
        room.add(at(monitor(), x, 0.775, z - 0.2));
        if ((ix + iz) % 2 === 0) { const p = person({ seated: true, arms: 'desk', shirt: [0xFFFFFF, 0x7C5CE8, 0xC9BCFA, 0x3E2A97][ix] }); room.add(at(p, x, 0, z + 0.85)); }
        else room.add(at(chair(), x, 0, z + 0.85));
      }));
      // meja depan dengan monitor besar (konten)
      room.add(at(desk(2.2, 0.9), 0, 0, 3.2));
      const mw = 1.25, mh = mw * 9 / 16;
      contentScreen(k, room, { w: mw, h: mh, kind: 'wide', y: 0.775 + 0.14 + mh / 2, z: 2.95, bezel: 0.05 });
      room.add(at(box(0.08, 0.14, 0.08, M.dark), 0, 0.84, 2.9));
      const p = person({ seated: true, arms: 'desk', shirt: 0x7C5CE8 }); p.rotation.y = 0.35; room.add(at(p, 1.0, 0, 4.1));
      [[-10.5, 6.5], [10.5, 6.5]].forEach(([x, z]) => room.add(at(plant(), x, 0, z)));
    },
    // 4 · ruang server: rak berlampu dan layar monitoring
    4(room, k) {
      const sw = 4.2, sh = sw * 9 / 16;
      contentScreen(k, room, { w: sw, h: sh, kind: 'wide', y: 1.1 + sh / 2, z: BACK });
      [-1, 1].forEach(side => {
        for (let i = 0; i < 5; i++) {
          const z = -4.5 + i * 2.1, x = side * 6.5;
          room.add(at(box(1.0, 2.4, 1.2, M.dark), x, 1.2, z));
          for (let r = 0; r < 6; r++) {
            const led = at(box(0.04, 0.04, 0.04, (r + i) % 3 ? M.led : M.ledP, false, false), x - side * 0.51, 0.4 + r * 0.32, z - 0.4 + ((r * 7 + i) % 5) * 0.18);
            room.add(led); leds.push(led);
          }
        }
      });
      const eng = person({ shirt: 0xFFFFFF }); eng.rotation.y = Math.PI * 0.8; room.add(at(eng, -3.5, 0, 1.5));
    },
    // 3 · ruang keamanan: video wall CCTV, layar tengah menampilkan konten
    3(room, k) {
      const sw = 3.6, sh = sw * 9 / 16, cy = 1.2 + sh / 2;
      contentScreen(k, room, { w: sw, h: sh, kind: 'wide', y: cy, z: BACK });
      let i = 0;
      [-1, 1].forEach(side => [0.5, -0.5].forEach(r => {
        const m = box(1.7, 0.96, 0.06, camFeed(i++)); room.add(at(m, side * (sw / 2 + 1.05), cy + r * 1.02, BACK));
        room.add(at(box(1.8, 1.06, 0.05, M.dark), side * (sw / 2 + 1.05), cy + r * 1.02, BACK - 0.04));
      }));
      room.add(at(desk(5.5, 1.0, 0.78), 0, 0, 1.6));
      [-1.6, 0, 1.6].forEach(x => room.add(at(monitor(0.5, 0.3), x, 0.805, 1.35)));
      const op = person({ seated: true, arms: 'desk', shirt: 0x2A2F5E }); room.add(at(op, -0.9, 0, 2.5));
      room.add(at(chair(), 1.2, 0, 2.5));
      const cam = new THREE.Group(); cam.add(at(box(0.5, 0.22, 0.22, M.white), 0, 0, 0)); cam.add(at(box(0.08, 0.3, 0.08, M.white), 0, 0.2, 0.1));
      room.add(at(cam, 11, 4.6, -7.5));
    },
    // 2 · HP di tangan seseorang (sudut pandang orang itu)
    2(room, k) {
      const s1 = sofa(3); s1.rotation.y = Math.PI; room.add(at(s1, -5, 0, -4.5));
      const s2 = sofa(3); s2.rotation.y = Math.PI; room.add(at(s2, 5, 0, -4.5));
      room.add(at(box(1.6, 0.4, 0.8, M.wood), -5, 0.2, -2.8));
      [[-10.5, -6.5], [10.5, -6.5], [-10.5, 6.5], [10.5, 6.5], [0, -6.8]].forEach(([x, z]) => room.add(at(plant(1.2), x, 0, z)));
      const p = person({ arms: 'phone', shirt: 0xC9BCFA });
      room.add(at(p, 0, 0, 2.2));
      room.updateMatrixWorld(true);
      const hand = p.userData.hands[1].getWorldPosition(new THREE.Vector3());
      room.worldToLocal(hand);
      const pw = 0.075, ph = pw * 844 / 390;
      contentScreen(k, room, { w: pw, h: ph, kind: 'phone', x: hand.x - 0.03, y: hand.y + ph / 2 - 0.02, z: hand.z - 0.04, rx: -0.12, bezel: 0.008 });
      [-6, 6].forEach(x => { const q = person({ seated: true, shirt: x < 0 ? 0x7C5CE8 : 0xFFFFFF }); q.rotation.y = Math.PI; room.add(at(q, x, 0, -4.7)); });
    },
    // 1 · lobi: tablet di tangan resepsionis
    1(room, k) {
      const logo = canvasTex(1024, 256, (x) => { x.fillStyle = '#5B3FC4'; x.fillRect(0, 0, 1024, 256); x.fillStyle = '#fff'; x.font = '800 140px "Plus Jakarta Sans", system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('A L T O R A', 512, 134); });
      room.add(at(box(8, 2, 0.08, std(0xffffff, { map: logo, emissive: 0xffffff, emissiveMap: logo, emissiveIntensity: 0.25 })), 0, 3.6, BACK));
      room.add(at(box(5.2, 1.1, 1.1, M.white), 0, 0.55, -1.8));
      room.add(at(box(5.2, 0.12, 1.12, M.purple), 0, 0.85, -1.79));
      const rec = person({ arms: 'hold', shirt: 0x7C5CE8 }); rec.rotation.y = Math.PI; room.add(at(rec, 0, 0, -2.85));
      room.updateMatrixWorld(true);
      const a = rec.userData.hands[0].getWorldPosition(new THREE.Vector3()), b = rec.userData.hands[1].getWorldPosition(new THREE.Vector3());
      room.worldToLocal(a); room.worldToLocal(b);
      const tw = Math.max(0.26, a.distanceTo(b) + 0.02), th = tw * 0.75;
      contentScreen(k, room, { w: tw, h: th, kind: 'tablet', x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 + th * 0.32, z: (a.z + b.z) / 2 + 0.02, rx: -0.35, bezel: 0.02 });
      [-1, 1].forEach(s => { const so = sofa(3); so.rotation.y = s * Math.PI / 2; room.add(at(so, s * 8.5, 0, 3)); });
      [[-3.4, -2], [3.4, -2], [-10.5, -6.5], [10.5, -6.5]].forEach(([x, z]) => room.add(at(plant(1.3), x, 0, z)));
      room.add(at(box(5, 6.2, 0.3, M.frame), 0, 3.1, D / 2 - 0.1));                                 // pintu masuk
      room.add(at(box(4.4, 5.8, 0.32, std(0xDCD3FB, { roughness: 0.1, metalness: 0.2, transparent: true, opacity: 0.6 })), 0, 2.9, D / 2 - 0.1));
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
    ROOMS[k](room, k);
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

  // ── konten HTML di layar ──
  const boards = {};
  cards.forEach(c => {
    const k = +c.dataset.k, sc = screens[k];
    c.classList.add('sc-' + sc.kind);
    const obj = new CSS3DObject(c);
    obj.position.z = 0.004;
    sc.holder.add(obj);
    boards[k] = { obj, el: c };
  });
  function layoutBoards() {
    cards.forEach(c => {
      const k = +c.dataset.k, sc = screens[k], b = boards[k];
      const prev = c.style.display; c.style.display = 'block';
      b.w = c.offsetWidth; b.h = c.offsetHeight;
      c.style.display = prev;
      b.obj.scale.setScalar(sc.w / b.w);
    });
  }

  // ── kamera ──
  const clamp = v => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const TAN = Math.tan(THREE.MathUtils.degToRad(16));
  const tq = new THREE.Quaternion();
  function shot(k) {
    const sc = screens[k], g = floors[k].g, saved = g.position.y;
    g.position.y = base(k); g.updateMatrixWorld(true);
    const look = new THREE.Vector3().setFromMatrixPosition(sc.holder.matrixWorld);
    sc.holder.getWorldQuaternion(tq);
    g.position.y = saved; g.updateMatrixWorld(true);
    const normal = new THREE.Vector3(0, 0, 1).applyQuaternion(tq).normalize();
    const aspect = stage.clientWidth / stage.clientHeight;
    const fillW = mobile ? 0.94 : (sc.kind === 'phone' ? 0.3 : sc.kind === 'tablet' ? 0.5 : 0.54), fillH = sc.kind === 'phone' ? 0.8 : 0.72;
    const d = Math.max(sc.w / (2 * TAN * aspect) / fillW, sc.h / (2 * TAN) / fillH);
    const side = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), normal).normalize();
    const pos = look.clone().addScaledVector(normal, d).addScaledVector(side, d * 0.12).add(new THREE.Vector3(0, d * 0.06, 0));
    return { pos, look, d };
  }
  const far = () => {
    const look = new THREE.Vector3(0, mobile ? 30 : 40, 0), az = 0.62, el = 0.1, d = mobile ? 260 : 200;
    return { pos: new THREE.Vector3(Math.sin(az) * Math.cos(el) * d, look.y + Math.sin(el) * d, Math.cos(az) * Math.cos(el) * d), look };
  };
  const above = () => ({ pos: new THREE.Vector3(16, TOTAL + 30, 34), look: new THREE.Vector3(0, base(7) + 2, -1) });
  const vA = new THREE.Vector3(), vB = new THREE.Vector3(), arcV = new THREE.Vector3();
  function blend(a, b, t, arc = 0) {
    vA.lerpVectors(a.pos, b.pos, t);
    if (arc) vA.add(arcV.set(arc * 0.3, arc * 0.55, arc).multiplyScalar(Math.sin(Math.PI * t)));
    vB.lerpVectors(a.look, b.look, t);
    camera.position.copy(vA); camera.lookAt(vB);
  }

  let INTRO, SEG, OUTRO; const shots = {};
  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    gl.setSize(w, h); css.setSize(w, h);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    const V = innerHeight; INTRO = 1.9 * V; SEG = 1.5 * V; OUTRO = 1.8 * V;
    story.style.setProperty('--story-h', (INTRO + cards.length * SEG + OUTRO + V) + 'px');
    layoutBoards();
    for (let k = 1; k <= N; k++) shots[k] = shot(k);
  }
  function setLift(k, lift) {
    const f = floors[k];
    f.g.position.y = base(k) + lift * 42;
    f.g.rotation.z = lift * 0.05;
    f.g.visible = lift < 0.985;
  }
  function setRoof(lift) {
    roof.position.y = TOTAL + lift * 42; roof.rotation.z = -lift * 0.05;
    roofAll.forEach(m => { m.opacity = 1 - clamp(lift * 1.3); }); roof.visible = lift < 0.985;
  }
  function setScreen(k, on, gone) {
    const b = boards[k], el = b.el, op = Math.min(clamp(on), 1 - clamp(gone * 1.6));
    el.style.opacity = op;
    el.classList.toggle('act', op > 0.6);
    b.obj.visible = op > 0.01;
    if (k === 7 && beam) beam.material.opacity = 0.14 * op;
  }

  function frame() {
    const g = -story.getBoundingClientRect().top, n = cards.length;
    const lifts = {}, on = {}, gone = {};
    for (let k = 1; k <= N; k++) lifts[k] = 0;
    let roofLift = 0, hero = 0, outroO = 0;
    if (g < INTRO) {
      const p = clamp(g / INTRO);
      hero = 1 - clamp(p / 0.15);
      roofLift = ease(clamp((p - 0.3) / 0.3));
      if (p < 0.45) blend(far(), above(), ease(clamp(p / 0.45)));
      else blend(above(), shots[7], ease(clamp((p - 0.45) / 0.55)));
      on[7] = clamp((p - 0.82) / 0.18);
    } else if (g < INTRO + n * SEG) {
      const x = (g - INTRO) / SEG, i = Math.min(n - 1, Math.floor(x)), u = x - i, cur = 7 - i;
      roofLift = 1;
      for (let k = cur + 1; k <= N; k++) lifts[k] = 1;
      const move = cur > 1 ? ease(clamp((u - 0.62) / 0.38)) : 0;
      lifts[cur] = cur > 1 ? ease(clamp((u - 0.62) / 0.3)) : 0;
      on[cur] = 1; gone[cur] = move;
      if (cur > 1) on[cur - 1] = clamp((move - 0.7) / 0.3);
      if (move > 0) blend(shots[cur], shots[cur - 1], move, 10);
      else blend(shots[cur], shots[cur], 0);
    } else {
      const q = clamp((g - INTRO - n * SEG) / OUTRO), z = ease(clamp(q / 0.8));
      for (let k = 2; k <= N; k++) lifts[k] = 1 - ease(clamp((q * 1.7 - 0.15 - (k - 2) * 0.1) / 0.45));
      roofLift = 1 - ease(clamp((q * 1.7 - 0.8) / 0.45));
      blend(shots[1], far(), z, 14);
      on[1] = 1; gone[1] = clamp(q / 0.12);
      outroO = clamp((q - 0.7) / 0.22);
    }
    for (let k = 1; k <= N; k++) setLift(k, lifts[k]);
    setRoof(roofLift);
    for (let k = 1; k <= N; k++) setScreen(k, on[k] || 0, gone[k] || 0);
    stage.style.setProperty('--hero', hero);
    stage.style.setProperty('--outro', outroO);
  }

  let visible = true; const t0 = performance.now();
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) loop(); }).observe(story);
  function loop() {
    if (!visible) return;
    const t = (performance.now() - t0) / 1000;
    beacon.material.emissiveIntensity = 1.2 + Math.sin(t * 3.3);
    leds.forEach((l, i) => { l.visible = Math.sin(t * 4 + i * 1.7) > -0.3; });
    frame();
    gl.render(scene, camera);
    css.render(scene, camera);
    requestAnimationFrame(loop);
  }
  addEventListener('resize', resize);
  resize();
  loop();
}
