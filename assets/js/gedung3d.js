/* Pembuka beranda "gedung Altora" (Three.js), dipakai di /preview-gedung.
   Adegan: gedung kaca utuh -> atap terangkat -> kamera masuk ke ruang meeting di lantai teratas -> layar proyektor
   menampilkan salinan hero beranda seukuran layar pengunjung -> saat layar memenuhi layar, kanvas 3D disembunyikan dan
   beranda asli (tepat di posisi yang sama) berlanjut seperti biasa. Lantai lain hanya tampak dari luar. */
import * as THREE from 'three';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { SVGLoader } from 'three/addons/loaders/SVGLoader.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const root = document.querySelector('.gd2');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (root && !reduce && webglOK()) {
  try { init(); } catch (e) { fail(e); }
}
function fail(e) {                                                    // apa pun yang gagal: matikan adegan, beranda biasa tetap tampil
  console.warn('gedung3d dimatikan:', e);
  if (window.__gdStop) window.__gdStop();
  document.documentElement.classList.remove('gd-boot', 'gd-boot-night');
  root.classList.remove('gd-live', 'gd-3d', 'gd-3d-on', 'gd-m', 'gd-night');
  root.querySelectorAll('.gd-canvas,.gd-css3d,.gd-floormenu,.gd-floortip').forEach(el => el.remove());
}

function webglOK() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
}

function init() {
  root.classList.add('gd-live', 'gd-3d'); document.documentElement.classList.remove('gd-boot', 'gd-boot-night');
  const scenes = [...root.querySelectorAll('.gd-scene')];
  const coverEl = root.querySelector('[data-gd-cover]');              // hero beranda = isi layar proyektor
  const mobile = innerWidth < 900;
  if (mobile) root.classList.add('gd-m');

  // ── ukuran gedung (meter) ──
  const W = 24, D = 17, FH = 6, LOBBY = 7, N = 9, SLAB = 0.5;
  const base = k => (k === 1 ? 0 : LOBBY + (k - 2) * FH);
  const height = k => (k === 1 ? LOBBY : FH);
  const TOTAL = LOBBY + (N - 1) * FH;
  const BACK = -D / 2 + 0.65;                                           // z permukaan dinding belakang (dalam)

  // ── renderer ──
  const BG = 0xFBF9FE;
  const gl = new THREE.WebGLRenderer({ antialias: true });
  gl.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.3 : 1.75));
  gl.setClearColor(BG, 1);
  gl.shadowMap.enabled = true;
  gl.shadowMap.type = mobile ? THREE.PCFShadowMap : THREE.PCFSoftShadowMap;
  if (mobile) gl.shadowMap.autoUpdate = false;                       // HP: peta bayangan diperbarui tiap beberapa frame (lihat step)
  gl.toneMapping = THREE.ACESFilmicToneMapping;
  gl.toneMappingExposure = 1.05;
  gl.outputColorSpace = THREE.SRGBColorSpace;
  gl.domElement.className = 'gd-canvas';
  root.appendChild(gl.domElement);
  const css = new CSS3DRenderer();
  css.domElement.className = 'gd-css3d';
  root.appendChild(css.domElement);

  const scene = new THREE.Scene();
  // menu lantai: latar (kota, langit) diburamkan, gedung tetap tajam di depannya
  const rtA = new THREE.WebGLRenderTarget(2, 2, { type: THREE.HalfFloatType }), rtB = rtA.clone();
  const quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1), quadScene = new THREE.Scene();
  const QV = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';
  const blurMat = new THREE.ShaderMaterial({ uniforms: { tex: { value: null }, dir: { value: new THREE.Vector2() } }, vertexShader: QV, depthTest: false, depthWrite: false,
    fragmentShader: 'uniform sampler2D tex; uniform vec2 dir; varying vec2 vUv; void main(){ vec4 c = texture2D(tex, vUv) * 0.227027;'
      + ' c += (texture2D(tex, vUv + dir * 1.3846) + texture2D(tex, vUv - dir * 1.3846)) * 0.316216;'
      + ' c += (texture2D(tex, vUv + dir * 3.2308) + texture2D(tex, vUv - dir * 3.2308)) * 0.070270; gl_FragColor = c; }' });
  const outMat = new THREE.ShaderMaterial({ uniforms: { tex: { value: null }, dim: { value: 0 }, tint: { value: new THREE.Color() } }, vertexShader: QV, depthTest: false, depthWrite: false,
    fragmentShader: 'uniform sampler2D tex; uniform float dim; uniform vec3 tint; varying vec2 vUv; void main(){ vec4 c = texture2D(tex, vUv); c.rgb = mix(c.rgb, tint, dim); gl_FragColor = vec4(c.rgb, 1.0);'
      + '\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}' });
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), blurMat); quad.frustumCulled = false; quadScene.add(quad);
  let blurK = 0;
  function renderScene() {
    if (blurK < 0.02) { gl.render(scene, camera); return; }
    camera.layers.set(0);                                                // 1) latar tanpa gedung -> tekstur setengah resolusi
    gl.setRenderTarget(rtA); gl.render(scene, camera);
    quad.material = blurMat;
    for (let i = 1; i <= 3; i++) {                                       // 2) blur gaussian bolak-balik, makin lebar
      const r = blurK * i;
      blurMat.uniforms.tex.value = rtA.texture; blurMat.uniforms.dir.value.set(r / rtA.width, 0); gl.setRenderTarget(rtB); gl.render(quadScene, quadCam);
      blurMat.uniforms.tex.value = rtB.texture; blurMat.uniforms.dir.value.set(0, r / rtA.height); gl.setRenderTarget(rtA); gl.render(quadScene, quadCam);
    }
    gl.setRenderTarget(null);                                            // 3) latar buram (sedikit diredupkan) ke layar
    quad.material = outMat; outMat.uniforms.tex.value = rtA.texture; outMat.uniforms.dim.value = blurK * 0.3;
    outMat.uniforms.tint.value.set(night.v > 0.5 ? 0x05061A : 0xF1EDFF);
    gl.render(quadScene, quadCam);
    camera.layers.set(1);                                                // 4) gedung tajam di atasnya
    gl.autoClear = false; gl.clearDepth(); gl.render(scene, camera); gl.autoClear = true;
    camera.layers.enable(0);
  }
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
  const camFeed = i => { const m = std(0xffffff, { roughness: 0.3, emissive: 0xffffff, emissiveIntensity: 0.8, map: canvasTex(320, 180, (x, w, h) => {
    const gr = x.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#2B3360'); gr.addColorStop(1, '#4A4F8C'); x.fillStyle = gr; x.fillRect(0, 0, w, h);
    x.fillStyle = 'rgba(201,188,250,.35)'; x.fillRect(30 + i * 20, 90, 120, 70); x.fillRect(190, 60 - i * 6, 90, 100);
    x.fillStyle = '#9CF5C8'; x.font = '700 18px monospace'; x.fillText('CAM 0' + (i + 1), 12, 26); x.fillStyle = '#FF6B9A'; x.beginPath(); x.arc(w - 18, 20, 6, 0, 7); x.fill();
  }) }); m.emissiveMap = m.map; return m; };   // gambar CCTV menyala, bukan tertimpa putih

  // ── orang (stilisasi) ──
  // orang voxel (gaya kotak-kotak): kepala kubus, rambut kotak, badan/lengan/kaki balok
  const SKIN = [0xF2B48C, 0xD9946B, 0xB9784F], HAIR = [0x5A3825, 0x2B2140, 0x8A5A2B];
  const flatCache = new Map();
  function flatMat(c, flat = true) { const key = c + (flat ? 'f' : ''); if (!flatCache.has(key)) flatCache.set(key, std(c, flat ? { flatShading: true } : {})); return flatCache.get(key); }
  function person({ shirt = 0x7C5CE8, pants = 0x3FA7B5, seated = false, arms = 'down', beard = false, v = 0 } = {}) {
    const g = new THREE.Group(), sh = flatMat(shirt), pt = flatMat(pants);   // material dipakai bersama per warna supaya bisa digabung
    const skin = flatMat(SKIN[v % 3]), hair = flatMat(HAIR[v % 3]), shoe = flatMat(0x5B5560), eye = flatMat(0x1B1F45, false);
    const hip = seated ? 0.5 : 0.72;
    if (seated) {
      [-0.12, 0.12].forEach(x => { g.add(at(box(0.2, 0.2, 0.5, pt), x, 0.5, -0.2)); g.add(at(box(0.2, 0.42, 0.2, pt), x, 0.27, -0.44)); g.add(at(box(0.22, 0.12, 0.3, shoe), x, 0.06, -0.48)); });
    } else {
      [-0.12, 0.12].forEach(x => { g.add(at(box(0.21, 0.6, 0.24, pt), x, 0.42, 0)); g.add(at(box(0.23, 0.14, 0.3, shoe), x, 0.07, -0.03)); });
    }
    g.add(at(box(0.56, 0.6, 0.34, sh), 0, hip + 0.3, 0));                                   // badan
    g.add(at(box(0.08, 0.32, 0.02, flatMat(0xffffff, false)), 0, hip + 0.42, -0.175));                  // kerah/dasi
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
      if (arms === 'hold') { a.rotation.x = 0.7; fore.rotation.x = 0.9; }
      else if (arms === 'phone' && i === 1) { a.rotation.x = 0.5; fore.rotation.x = 1.5; }
      else if (arms === 'reach' && i === 1) { a.rotation.x = 1.4; fore.rotation.x = 0.15; }
      else if (arms === 'desk') { a.rotation.x = 1.0; fore.rotation.x = 0.4; }
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
    // 9 · Beranda (lantai teratas): ruang meeting penuh, proyektor menyala ke layar = pintu masuk ke beranda
    9(room, k) {
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
        const p = person({ seated: true, shirt: [0x7C5CE8, 0x6B3F3A, 0x3E2A97, 0xF26B3A][i], v: i, beard: i === 1, arms: 'desk' }); p.rotation.y = 0.15 * (i - 1.5); room.add(at(p, x, 0, 3.0));
        const q = person({ seated: true, shirt: [0x3FA7B5, 0xF5C04A, 0xFF8FB1, 0x7AC74F][i], v: i + 1, beard: i === 2, arms: 'desk' }); q.rotation.y = Math.PI - 0.5; room.add(at(q, x, 0, -0.2));
      }
      const proj = new THREE.Group(); proj.add(at(box(0.55, 0.2, 0.5, M.white), 0, 0, 0)); proj.add(at(cyl(0.07, 0.07, 0.06, M.dark), 0, 0, -0.27)); proj.children[1].rotation.x = Math.PI / 2;
      room.add(at(proj, 0, 0.87, 2.2));
      [[-10.5, -6.5], [10.5, -6.5], [-10.5, 6.5], [10.5, 6.5]].forEach(([x, z]) => room.add(at(plant(1.1), x, 0, z)));
      [-1, 1].forEach(sd => { const c = chair(); c.rotation.y = sd * Math.PI / 2; room.add(at(c, sd * 5.6, 0, 1.4)); const p = person({ seated: true, shirt: sd > 0 ? 0xF26B3A : 0x7C5CE8, v: sd > 0 ? 2 : 0, arms: 'desk' }); p.rotation.y = sd * Math.PI / 2; room.add(at(p, sd * 5.45, 0, 1.4)); });   // yang duduk di ujung meja menghadap meja
      const pres = person({ shirt: 0x3E2A97, v: 1, arms: 'reach' }); pres.rotation.y = Math.PI + 0.9; room.add(at(pres, -5.6, 0, -6.2));   // presenter menunjuk layar
      [[-3, 5.6], [-1.6, 5.9], [2.2, 5.7], [3.6, 5.5]].forEach(([x, z], j) => { const p = person({ shirt: [0xF5C04A, 0x3FA7B5, 0x6B3F3A, 0xFF8FB1][j], v: j, arms: j % 2 ? 'hold' : 'down' }); room.add(at(p, x, 0, z)); });   // peserta berdiri di belakang
      bake(room, new Set([housing, beam, screens[k].holder]));             // perabot & orang digabung; proyektor/sinar/layar tetap terpisah
    },
  };

  // ── isi tiap lantai sesuai halamannya; perabot statis digabung per material agar ringan ──
  const PAGES = {
    9: ['Beranda', '/', 'Kenalan dengan Altora'], 8: ['Karier', '/careers', 'Gabung tim Altora'], 7: ['Layanan', '/services', 'Software, CCTV & IoT'],
    6: ['Produk', '/produk', 'Aplikasi & perangkat'], 5: ['Portofolio', '/portfolio', 'Proyek yang sudah berjalan'],
    4: ['Artikel', '/blog', 'Panduan & wawasan'], 3: ['Tentang', '/about', 'Kenali tim kami'],
    2: ['Katalog', '/katalog', 'Belanja perangkat'], 1: ['Support', '/support', 'Bantuan teknis'],
  };
  const LABELS = {};
  const SHOTS = [390, 820, 1440, 1920];                                  // lebar tangkapan layar yang tersedia; pilih yang paling dekat dengan lebar layar
  const shotW = () => SHOTS.reduce((a, b) => Math.abs(b - VW) < Math.abs(a - VW) ? b : a);
  function labelMat(k, poster = false) {                                // isi layar: judul halaman, digambar ulang mengikuti rasio layar pengunjung
    const c = document.createElement('canvas'), tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    const mat = new THREE.MeshStandardMaterial({ map: tex, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: poster ? 0.55 : 0.9, roughness: poster ? 0.8 : 0.4 });
    const L = LABELS[k] = { mat, img: null, aspect: 1, draw(aspect) {
      L.aspect = aspect;
      const w = aspect >= 1 ? 1280 : Math.round(1280 * aspect), h = aspect >= 1 ? Math.round(1280 / aspect) : 1280;
      c.width = w; c.height = h; const x = c.getContext('2d');
      const vv = shotW(), im = L.img && L.img[vv];
      if (L.img && !im) L.load(vv);                                        // ukuran jendela berubah jauh
      if (im) {                                                          // tangkapan layar asli halamannya, pas lebar & rata atas (seperti halaman dibuka di layar ini)
        const sc = w / im.width;
        x.fillStyle = '#FBF9FE'; x.fillRect(0, 0, w, h);
        x.drawImage(im, 0, 0, w, im.height * sc);
        tex.needsUpdate = true; return;
      }
      const g = x.createLinearGradient(0, 0, w, h); g.addColorStop(0, '#FFFFFF'); g.addColorStop(0.6, '#F3EEFF'); g.addColorStop(1, '#E4DAFF'); x.fillStyle = g; x.fillRect(0, 0, w, h);
      const r = x.createRadialGradient(w * 0.85, 0, 0, w * 0.85, 0, Math.max(w, h) * 0.7); r.addColorStop(0, 'rgba(124,92,232,.22)'); r.addColorStop(1, 'rgba(124,92,232,0)'); x.fillStyle = r; x.fillRect(0, 0, w, h);
      const fs = Math.min(w * 0.17, h * 0.22), F = '"Plus Jakarta Sans", system-ui, sans-serif';
      x.textAlign = 'center'; x.textBaseline = 'middle';
      x.fillStyle = '#7C5CE8'; x.font = '700 ' + Math.round(fs * 0.3) + 'px ' + F; x.fillText('ALTORA', w / 2, h / 2 - fs * 0.85);
      x.fillStyle = '#10224F'; x.font = '800 ' + Math.round(fs) + 'px ' + F; x.fillText(PAGES[k][0], w / 2, h / 2);
      x.fillStyle = '#5A6785'; x.font = '600 ' + Math.round(fs * 0.26) + 'px ' + F; x.fillText(PAGES[k][2], w / 2, h / 2 + fs * 0.85);
      tex.needsUpdate = true;
    }, load(v) {                                                        // v: lebar tangkapan layar (scripts/shot_lantai.sh)
      if ((L.img && L.img[v]) || PAGES[k][1] === '/') return;             // lantai Beranda: isinya beranda asli (lapisan HTML), tanpa tangkapan layar
      const im = new Image(); im.decoding = 'async';
      im.onload = () => { L.img = L.img || {}; L.img[v] = im; L.draw(L.aspect); };
      im.src = '/assets/img/lantai/' + PAGES[k][1].slice(1) + '-' + v + '.webp?v=2';
    } };
    return mat;
  }
  const crowd = [];                                                    // orang yang berjalan bolak-balik
  const lite = (w, h, d, mat) => box(w, h, d, mat, false, false);
  const SHIRTS = [0x7C5CE8, 0xF26B3A, 0x3FA7B5, 0xF5C04A, 0x6B3F3A, 0xFFFFFF, 0x3E2A97, 0x7AC74F, 0xFF8FB1];
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
  const V2 = {
    shelf: std(0xF4EFFF, { flatShading: true }), cab: std(0xDCD3F7, { flatShading: true }), board: std(0xF7F3E8), cork: std(0xC9A27A, { flatShading: true }),
    kiosk: std(0x3E2A97, { roughness: 0.4, metalness: 0.3 }), paper: [0xFFFFFF, 0xFFE7A3, 0xC9F2DC, 0xFFD3E5, 0xD7E6FF].map(c => std(c)),
    prod: [0x7C5CE8, 0xF26B3A, 0x3FA7B5, 0xF5C04A, 0xFF8FB1, 0x7AC74F, 0xFFFFFF, 0x1B1F45].map(c => std(c, { flatShading: true })),
    wood: std(0xC99B6D, { flatShading: true }),
  };
  const portoImgs = ['fms.jpg', 'barito-dash.jpg', 'dapodik.jpg', 'attendance.jpg', 'smart-farming.webp', 'hris.jpg', 'clinic.jpg', 'logistik.jpg']
    .map(f => { const t = new THREE.TextureLoader().load('/assets/img/portfolio/' + f); t.colorSpace = THREE.SRGBColorSpace; return std(0xffffff, { map: t, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: 0.35, roughness: 0.5 }); });
  function bake(group, keep) {                                         // gabungkan mesh statis per material (+ setelan bayangan): ratusan objek -> belasan draw call
    group.updateMatrixWorld(true);                                     // keep: objek (beserta isinya) yang dibiarkan utuh karena dianimasikan/diubah ukurannya
    const inv = group.matrixWorld.clone().invert(), byKey = new Map(), m4 = new THREE.Matrix4(), take = [];
    (function walk(o) {
      if (o !== group && keep && keep.has(o)) return;
      if (o.isMesh && !o.isInstancedMesh && !Array.isArray(o.material) && o.visible && !o.morphTargetInfluences) take.push(o);
      o.children.forEach(walk);
    })(group);
    take.forEach(o => {
      const key = o.material.uuid + (o.castShadow ? 'c' : '') + (o.receiveShadow ? 'r' : '');
      if (!byKey.has(key)) byKey.set(key, { mat: o.material, cast: o.castShadow, recv: o.receiveShadow, list: [] });
      byKey.get(key).list.push(o);
    });
    byKey.forEach(({ mat, cast, recv, list }) => {
      if (list.length < 2) return;
      let gs = list.map(o => o.geometry.clone().applyMatrix4(m4.multiplyMatrices(inv, o.matrixWorld)));
      if (gs.some(g => !g.index) && gs.some(g => g.index)) gs = gs.map(g => g.index ? g.toNonIndexed() : g);
      const merged = mergeGeometries(gs, false); gs.forEach(g => g.dispose());
      if (!merged) return;                                               // atribut tidak cocok: biarkan apa adanya
      list.forEach(o => o.parent.remove(o));
      const m = new THREE.Mesh(merged, mat); m.castShadow = cast; m.receiveShadow = recv; group.add(m);
    });
  }
  const vcMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 0.7 });
  function bakeColor(group) {                                          // objek bergerak berwarna polos -> satu mesh, warna tiap bagian disimpan di vertex (1 draw call)
    group.updateMatrixWorld(true);
    const inv = group.matrixWorld.clone().invert(), m4 = new THREE.Matrix4(), gs = [], take = [];
    let cast = false;
    group.traverse(o => { if (o.isMesh && !Array.isArray(o.material) && o.visible && !o.material.map && !o.material.transparent) take.push(o); });
    if (take.length < 2) return;
    take.forEach(o => {
      let g = o.geometry.clone().applyMatrix4(m4.multiplyMatrices(inv, o.matrixWorld));
      if (g.index) g = g.toNonIndexed();
      const n = g.attributes.position.count, c = o.material.color, a = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) { a[i * 3] = c.r; a[i * 3 + 1] = c.g; a[i * 3 + 2] = c.b; }
      g.setAttribute('color', new THREE.BufferAttribute(a, 3));
      for (const key of Object.keys(g.attributes)) if (!['position', 'normal', 'uv', 'color'].includes(key)) g.deleteAttribute(key);
      if (!g.attributes.uv) g.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(n * 2), 2));
      gs.push(g); cast = cast || o.castShadow;
    });
    const merged = mergeGeometries(gs, false); gs.forEach(g => g.dispose());
    if (!merged) return;
    take.forEach(o => o.parent.remove(o));
    const m = new THREE.Mesh(merged, vcMat); m.castShadow = cast; group.add(m);
  }
  function busyFloor(room, k, gh) {
    const st = new THREE.Group(); room.add(st);
    const S = (m, x, y, z, ry = 0) => { m.rotation.y = ry; st.add(at(m, x, y, z)); return m; };
    const walk = (i, x, z, axis, min, max, speed) => { const p = mini(i, false); room.add(at(p, x, 0, z)); crowd.push({ p, axis, min, max, dir: i % 2 ? 1 : -1, speed }); };
    const seatAt = (i, x, z, ry) => { S(lite(0.55, 0.5, 0.55, M.dark), x, 0.25, z + (ry ? -0.15 : 0.15)); S(mini(i, true), x, 0, z, ry); };
    const station = (x, z, i, sit = true) => {                         // meja kerja: meja, monitor menyala, kursi, orang duduk menghadap -z
      S(lite(2.0, 0.06, 0.9, deskTop), x, 0.76, z); S(lite(1.9, 0.7, 0.05, M.lilac), x, 0.4, z - 0.42);
      S(lite(0.8, 0.5, 0.05, screenGlow), x - 0.3, 1.1, z - 0.25); S(lite(0.4, 0.04, 0.16, M.dark), x - 0.3, 0.8, z);
      if (i % 4 === 1) S(lite(0.18, 0.22, 0.18, V2.prod[i % 8]), x + 0.6, 0.9, z - 0.1);         // gelas/aksesori
      if (sit) seatAt(i, x - 0.3, z + 0.75, 0);
    };
    const plantAt = (x, z, s = 1.2) => S(plant(s), x, 0, z);
    S(lite(W - 1.2, 0.05, D - 1.2, k === 1 ? M.wall : M.lilac), 0, 0.03, 0);
    for (let x = -8; x <= 8; x += 8) for (const z of [-3, 3]) S(lite(4.2, 0.04, 0.35, ceilLight), x, gh - 0.06, z);   // lampu langit-langit
    [[-10.8, -7], [10.8, -7], [-10.8, 7.3], [10.8, 7.3]].forEach(([x, z]) => plantAt(x, z));
    let screen = null;                                                   // layar yang dituju kamera saat lantai ini diklik

    if (k === 3 || k === 4) {                                            // Tentang / Artikel: kantor terbuka yang padat
      let i = k * 5;
      for (const z of [6.2, 3.4, 0.6, -2.4]) for (let x = -9.6; x <= 9.6; x += 2.4) { if (z === -2.4 && Math.abs(x) < 3) continue; station(x, z, i, (i + k) % 5 !== 0); i++; }
      [-10.6, -8.6].forEach(x => S(lite(1.6, 1.9, 0.6, V2.cab), x, 0.95, -7.3));        // lemari arsip
      S(lite(1.0, 1.2, 0.7, M.white), 9.4, 0.6, -7.2); S(lite(0.8, 0.12, 0.5, M.dark), 9.4, 1.25, -7.2);  // printer
      S(lite(0.06, 1.6, 3.2, V2.board), -11.6, 2.2, 0);                                    // papan tulis dinding samping
      walk(2, -6, -4.6, 'x', -10, 10, 1.2); walk(5, 4, -5.2, 'x', -10, 10, 0.9); walk(7, 11, 2, 'z', -5, 7, 1.0);
      if (k === 3) screen = { kind: 'wide', hBase: 2.3, maxW: 4.4, bottom: 1.5, z: BACK, bezelPad: 0.14 };
      else {                                                              // Artikel: poster besar + papan pengumuman berisi kertas
        screen = { kind: 'wide', hBase: 2.8, maxW: 4.2, bottom: 1.3, z: BACK, bezelPad: 0.12, poster: true };
        [-1, 1].forEach(sd => {
          S(lite(3.2, 2.2, 0.06, V2.cork), sd * 5.2, 2.5, BACK + 0.03);
          for (let a = 0; a < 6; a++) S(lite(0.7, 0.85, 0.02, V2.paper[(a + (sd > 0 ? 2 : 0)) % 5]), sd * 5.2 - 1.05 + (a % 3) * 1.05, 2.0 + Math.floor(a / 3) * 1.0, BACK + 0.08);
        });
      }
    } else if (k === 8) {                                                // Karier: ruang wawancara + area onboarding tim baru
      screen = { kind: 'wide', hBase: 2.4, maxW: 4.4, bottom: 1.4, z: BACK, bezelPad: 0.14 };
      S(desk(4.4, 1.4, 0.75, M.wood), 0, 0, -3.0);                                              // meja wawancara
      [-1.4, 0, 1.4].forEach((x, j) => {                                                       // panel pewawancara menghadap kandidat
        const c = chair(); S(c, x, 0, -4.05, Math.PI);
        S(person({ seated: true, shirt: [0x3E2A97, 0x7C5CE8, 0x3FA7B5][j], v: j, arms: 'desk', beard: j === 2 }), x, 0, -3.9, Math.PI);
        S(lite(0.5, 0.32, 0.03, screenGlow), x, 0.95, -3.25);                                  // laptop
      });
      S(chair(), 0, 0, -1.75); S(person({ seated: true, shirt: 0xF5C04A, v: 1, arms: 'desk' }), 0, 0, -1.9);   // kandidat
      S(lite(0.3, 0.02, 0.4, M.white), 0.2, 0.8, -2.5);                                        // berkas CV
      let i = 30;
      for (const z of [2.4, 5.2]) for (let x = 3.6; x <= 10; x += 2.4) { station(x, z, i, i % 3 !== 0); i++; }   // onboarding
      S(lite(0.06, 1.6, 3.2, V2.board), 11.6, 2.2, -3.5);                                     // papan tim baru
      [[-8, 4.6], [-5, 4.6]].forEach(([x, z]) => S(sofa(2.6), x, 0, z, Math.PI));             // lounge
      [[-8.5, 4.4], [-7.4, 4.4], [-5.2, 4.4]].forEach(([x, z], j) => S(mini(j + 3, true), x, 0, z, Math.PI));
      walk(4, -6, 1.5, 'x', -10, 2, 0.9); walk(8, 2, 0.8, 'x', -4, 10, 1.1);
    } else if (k === 7) {                                                // Layanan: ruang monitoring CCTV & sistem
      screen = { kind: 'wide', hBase: 2.0, maxW: 3.6, bottom: 1.7, z: BACK, bezelPad: 0.1 };
      for (let a = 0; a < 8; a++) { const sd = a < 4 ? -1 : 1, j = a % 4; S(lite(2.2, 1.25, 0.08, camFeed(a)), sd * (3.4 + (j % 2) * 2.35), 1.75 + Math.floor(j / 2) * 1.4, BACK + 0.04); }
      for (const z of [-2.2, 0.9]) for (let x = -7.5; x <= 7.5; x += 3) {
        S(lite(2.6, 0.06, 0.9, deskTop), x, 0.76, z);
        [-0.8, 0, 0.8].forEach((dx, j) => S(lite(0.7, 0.45, 0.05, j === 1 ? screenGlow : camFeed((x + z + j) & 7)), x + dx, 1.08, z - 0.3));
        seatAt((x * 3 + z) & 7, x, z + 0.75, 0);
      }
      [-1, 1].forEach(sd => { for (let z = -5; z <= 5; z += 2.2) {
        S(lite(0.9, 2.3, 1.6, M.dark), sd * 10.9, 1.15, z);
        for (let r = 0; r < 4; r++) { const led = at(lite(0.05, 0.08, 0.08, r % 2 ? M.led : M.ledP), sd * 10.43, 0.6 + r * 0.4, z - 0.5 + r * 0.3); room.add(led); leds.push(led); }
      } });
      walk(3, -4, 3.6, 'x', -9, 9, 1.0); walk(6, 5, 5.5, 'x', -9, 9, 1.3);
    } else if (k === 6) {                                                // Produk: showroom perangkat & demo ke klien
      screen = { kind: 'wide', hBase: 1.7, maxW: 3.0, bottom: 1.05, z: -5.6, bezelPad: 0.12 };
      S(lite(3.4, 1.0, 0.6, M.dark), 0, 0.5, -5.75);
      const p0 = mini(6, false); S(p0, 2.3, 0, -5.0, Math.PI * 0.8);                    // presenter di samping TV
      [[-1.4, -3.0], [0.2, -2.6], [1.6, -3.1]].forEach(([x, z], j) => S(mini(j + 1, false), x, 0, z));  // klien menonton TV
      for (const [x, z] of [[-7.5, -3], [-7.5, 1], [-7.5, 5], [7.5, -3], [7.5, 1], [7.5, 5], [-3, 3.5], [3, 3.5]]) {   // meja display
        S(lite(2.6, 0.9, 1.2, V2.shelf), x, 0.45, z);
        S(lite(0.9, 0.04, 0.6, M.dark), x - 0.7, 0.93, z); S(lite(0.9, 0.55, 0.04, screenGlow), x - 0.7, 1.2, z - 0.28);   // laptop
        S(lite(0.35, 0.35, 0.5, M.white), x + 0.5, 1.08, z); S(lite(0.14, 0.14, 0.06, M.dark), x + 0.5, 1.1, z + 0.27);    // kamera CCTV
        S(lite(0.6, 0.12, 0.4, V2.prod[6]), x + 1.0, 0.96, z - 0.3); S(lite(0.03, 0.4, 0.03, M.dark), x + 1.2, 1.2, z - 0.4);   // router
      }
      [-1, 1].forEach(sd => { for (let z = -6; z <= 6; z += 3) { S(lite(0.7, 2.4, 2.6, V2.shelf), sd * 11.1, 1.2, z); for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) S(lite(0.4, 0.4, 0.5, V2.prod[(r + c + z) & 7]), sd * 10.95, 0.55 + r * 0.75, z - 0.8 + c * 0.8); } });
      [[-5, 0, 2], [5, -1, 4], [0, 6, 5], [-9, 6.5, 0], [9, 2.5, 3]].forEach(([x, z, i]) => S(mini(i, false), x, 0, z, i));
      walk(4, -3, 1.0, 'x', -6, 6, 0.9); walk(8, 6, 6.5, 'x', -9, 9, 1.1);
    } else if (k === 5) {                                                // Portofolio: galeri foto proyek
      screen = { kind: 'wide', hBase: 2.5, maxW: 4.2, bottom: 1.4, z: BACK, bezelPad: 0.16, frame: true };
      [-1, 1].forEach(sd => [0, 1].forEach(j => { const x = sd * (5.4 + j * 3.4); S(lite(3.0, 2.0, 0.08, V2.wood), x, 2.55, BACK + 0.02); S(lite(2.8, 1.8, 0.02, portoImgs[(j * 2 + (sd > 0 ? 1 : 0)) % 8]), x, 2.55, BACK + 0.08); }));
      [-1, 1].forEach(sd => [-3.5, 1.5, 5.8].forEach((z, j) => { S(lite(0.08, 2.0, 3.0, V2.wood), sd * 11.55, 2.55, z); S(lite(0.02, 1.8, 2.8, portoImgs[(4 + j + (sd > 0 ? 3 : 0)) % 8]), sd * 11.5, 2.55, z); }));
      [-4, 4].forEach(x => S(lite(3.2, 0.45, 0.9, V2.wood), x, 0.23, 1.8));                 // bangku
      [[-4.4, 1.8], [-3.4, 1.8], [4.0, 1.8]].forEach(([x, z], j) => S(mini(j + 2, true), x, 0, z));
      [[-6.5, -4.6], [-5.2, -4.9], [6.0, -4.8], [9.8, -3.5], [-9.8, 1.5], [9.6, 5.5], [-1.5, 4.5], [2.5, 5.2]].forEach(([x, z], j) => {
        const ry = Math.abs(x) > 9 ? (x > 0 ? -Math.PI / 2 : Math.PI / 2) : 0; S(mini(j + 3, false), x, 0, z, ry);
      });
      walk(1, 0, 3.0, 'x', -8, 8, 0.7);
    } else if (k === 2) {                                                // Katalog: toko, pembeli bertransaksi di kasir
      screen = { kind: 'wide', hBase: 0.46, maxW: 0.8, bottom: 1.2, z: 0.3, x: 0, bezelPad: 0.05, rx: -0.12 };
      S(lite(4.4, 1.05, 0.9, V2.kiosk), 0, 0.53, 0); S(lite(4.5, 0.06, 1.0, deskTop), 0, 1.08, 0);   // meja kasir
      S(lite(0.14, 0.12, 0.1, M.dark), 0, 1.16, 0.3);
      S(lite(0.3, 0.06, 0.22, M.dark), 1.1, 1.14, -0.1); S(lite(0.5, 0.4, 0.4, V2.prod[3]), -1.4, 1.31, -0.2);   // EDC, barang belanja
      S(mini(0, false), -0.9, 0, 1.0, Math.PI);                                                              // kasir
      const buyer = person({ shirt: 0xF26B3A, pants: 0x2A2F5E, arms: 'reach', v: 1 }); buyer.scale.setScalar(1.05); S(buyer, 0.6, 0, -1.0, Math.PI);   // pembeli menyerahkan kartu
      [[1.2, -2.3], [1.6, -3.4], [2.0, -4.5]].forEach(([x, z], j) => S(mini(j + 4, false), x, 0, z, Math.PI));    // antre
      for (const z of [-6.8, -4.6]) for (let x = -10; x <= -3; x += 3.5) { S(lite(3.0, 2.0, 0.8, V2.shelf), x, 1.0, z); for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) S(lite(0.42, 0.42, 0.5, V2.prod[(r * 3 + c + x) & 7]), x - 1.1 + c * 0.55, 0.45 + r * 0.65, z); }
      for (const z of [-6.8, -4.6]) for (let x = 5; x <= 10; x += 3.5) { S(lite(3.0, 2.0, 0.8, V2.shelf), x, 1.0, z); for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) S(lite(0.42, 0.42, 0.5, V2.prod[(r + c * 2 + x) & 7]), x - 1.1 + c * 0.55, 0.45 + r * 0.65, z); }
      for (const z of [3.5, 6.2]) for (const x of [-8, -4, 4, 8]) { S(lite(2.6, 1.0, 1.0, V2.shelf), x, 0.5, z); for (let c = 0; c < 4; c++) S(lite(0.4, 0.35, 0.4, V2.prod[(c + x + z) & 7]), x - 0.9 + c * 0.6, 1.18, z); }
      [[-6, 1.8, 3], [6.5, 1.5, 5], [-2.5, 5, 7], [9.5, -2, 2]].forEach(([x, z, i]) => S(mini(i, false), x, 0, z, i));
      walk(6, -6, -2.6, 'x', -10, -2, 0.8); walk(2, 6, 4.9, 'x', 2, 10, 0.9);
    } else {                                                             // Support: lobi dengan kiosk layanan & resepsionis
      screen = { kind: 'wide', hBase: 0.62, maxW: 0.8, bottom: 1.15, z: -4.3, x: 0, bezelPad: 0.06, rx: -0.28 };
      S(lite(1.0, 0.1, 0.8, V2.kiosk), 0, 0.05, -4.45); S(lite(0.5, 1.05, 0.4, V2.kiosk), 0, 0.6, -4.55); S(lite(1.0, 0.95, 0.25, V2.kiosk), 0, 1.45, -4.5);
      const u = person({ shirt: 0x3FA7B5, pants: 0x2A2F5E, arms: 'reach', v: 2 }); u.scale.setScalar(1.0); S(u, -0.62, 0, -3.35, 0.25);   // menjulurkan tangan ke layar kiosk
      [[-1.4, -2.2], [-1.9, -1.2]].forEach(([x, z], j) => S(mini(j + 5, false), x, 0, z));                   // antre kiosk
      S(lite(5.5, 1.1, 1.2, deskTop), -6.5, 0.55, -3); S(lite(5.5, 0.15, 1.22, M.purple), -6.5, 0.9, -3);     // resepsionis
      S(mini(0, false), -6.5, 0, -4.1); S(mini(3, false), -6.8, 0, -1.8, Math.PI);
      S(lite(0.06, 1.4, 4.2, M.purple), 11.6, 3.2, -2);                                      // papan nama dinding
      [[5.5, 3.5], [8.5, 3.5]].forEach(([x, z]) => S(sofa(2.6), x, 0, z, Math.PI));
      [[5.0, 3.3], [8.9, 3.4], [6.2, 3.4]].forEach(([x, z], j) => S(mini(j + 1, true), x, 0, z, Math.PI));
      for (let j = 0; j < 4; j++) walk(j + 2, -9 + j * 5, 1 + (j % 2) * 3, 'z', -1, 7, 0.8 + j * 0.2);
    }
    bake(st);
    if (screen) contentScreen(k, room, Object.assign({ surface: labelMat(k, !!screen.poster) }, screen));
    if (screen && (screen.poster || screen.frame)) screens[k].bezel.material = V2.wood;
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
    else busyFloor(room, k, gh);             // lantai lain: aktivitas yang terlihat dari luar + layar halamannya
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
    meshes.forEach(m => { m.geometry.translate(-c.x, -c.y, -c.z); m.layers.set(1); logo3d.add(m); });   // layer 1: tetap tajam di menu lantai
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
  const envFrom = scene.children.length;                               // objek kota statis mulai dari sini (digabung setelah gunung)
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
    t.userData.still = true; scene.add(at(t, x, 0, z));
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
  const carMats = new Map(), carMat = c => carMats.get(c) || (carMats.set(c, std(c, { flatShading: true, roughness: 0.6 })), carMats.get(c));
  function vcar(color, truck = false) {
    const g = new THREE.Group(), body = carMat(color);
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
  {                                                                    // jalan, marka, rumput, sungai, rel, jembatan, gunung: ratusan mesh -> beberapa
    const skip = new Set([...logs.map(l => l.m), moonMtn, moonSnow]), envG = new THREE.Group(); scene.add(envG);
    scene.children.slice(envFrom).forEach(o => { if ((o.isMesh && !o.isInstancedMesh && !skip.has(o)) || o.userData.still) envG.attach(o); });   // + pohon
    bake(envG);
  }
  // mobil di jalan silang & jalan jauh
  const farCars = [];
  const nZ = mobile ? 2 : 5, nX = mobile ? 2 : 4;                         // HP: mobil jauh lebih sedikit (terlalu kecil untuk terlihat)
  ZR.forEach((x, ri) => [-1, 1].forEach((dir, li) => { for (let i = 0; i < nZ; i++) {
    const c = vcar(carColors[(ri + li * 3 + i) % carColors.length], (i + ri) % 4 === 1);
    c.rotation.y = dir > 0 ? -Math.PI / 2 : Math.PI / 2; c.position.set(x + dir * 3, 0.12, -420 + i * (840 / nZ) + li * 60);
    c.traverse(o => { o.castShadow = false; }); scene.add(c); farCars.push({ c, dir, axis: 'z', speed: 8 + ((i + ri) % 5) });
  } }));
  [-100, 128, 215, -235].forEach((z, ri) => [-1, 1].forEach((dir, li) => { for (let i = 0; i < nX; i++) {
    const c = vcar(carColors[(ri * 2 + li + i) % carColors.length], (i + li) % 3 === 0);
    c.rotation.y = dir > 0 ? 0 : Math.PI; c.position.set(-420 + i * (840 / nX) + li * 80, 0.12, z + dir * 3);
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
  // pesawat voxel menarik spanduk ALTORA (logo + tulisan), mengitari kota
  const plane = new THREE.Group();
  {
    const body = std(0xFFFFFF, { flatShading: true }), acc = std(0x7C5CE8, { flatShading: true }), glass = std(0x9FC3FF, { roughness: 0.2 });
    plane.add(at(box(9, 1.8, 1.8, body, false, false), 0, 0, 0));
    plane.add(at(box(1.2, 1.4, 1.4, acc, false, false), 5.1, 0, 0));
    plane.add(at(box(1.8, 0.8, 1.6, glass, false, false), 2.4, 1.2, 0));
    plane.add(at(box(2.6, 0.3, 14, body, false, false), 1, 0.2, 0));
    plane.add(at(box(2.6, 0.32, 1.2, acc, false, false), 1, 0.22, 6.4));
    plane.add(at(box(2.6, 0.32, 1.2, acc, false, false), 1, 0.22, -6.4));
    plane.add(at(box(1.6, 0.3, 5, body, false, false), -4, 0.4, 0));
    plane.add(at(box(1.8, 2.6, 0.3, acc, false, false), -4, 1.6, 0));
    const prop = at(box(0.2, 3.6, 0.4, V.wheel, false, false), 5.8, 0, 0); plane.add(prop); plane.userData.prop = prop;
    plane.add(at(box(6, 0.06, 0.06, V.wheel, false, false), -6.5, 0, 0));
    const cv = document.createElement('canvas'); cv.width = 1024; cv.height = 300;
    const g = cv.getContext('2d'), tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const draw = img => {
      g.fillStyle = '#FFFFFF'; g.fillRect(0, 0, 1024, 300);
      g.strokeStyle = '#7C5CE8'; g.lineWidth = 16; g.strokeRect(8, 8, 1008, 284);
      if (img) g.drawImage(img, 60, 50, 200, 200);
      g.fillStyle = '#10224F'; g.font = '800 150px "Plus Jakarta Sans", system-ui, sans-serif'; g.textBaseline = 'middle';
      g.fillText('ALTORA', img ? 290 : 120, 140);
      g.fillStyle = '#7C5CE8'; g.font = '700 40px "Plus Jakarta Sans", system-ui, sans-serif';
      g.fillText('altora.id', img ? 296 : 126, 240);
      tex.needsUpdate = true; if (plane.userData.tb) plane.userData.tb.needsUpdate = true;
    };
    draw(null);
    const img = new Image(); img.onload = () => draw(img); img.src = '/assets/img/altora-logo-icon-v2.svg';
    const bm = new THREE.MeshStandardMaterial({ map: tex, emissive: 0xFFFFFF, emissiveMap: tex, emissiveIntensity: 0.35, roughness: 0.8 });
    const geo = new THREE.PlaneGeometry(9.5, 2.8, 16, 1); geo.translate(-4.75, 0, 0);   // spanduk setinggi pesawat
    const banner = new THREE.Group(); banner.position.x = -9.5;
    const tb = tex.clone(); tb.wrapS = THREE.RepeatWrapping; tb.repeat.x = -1; tb.offset.x = 1;   // sisi belakang: tulisan tetap terbaca
    plane.userData.tb = tb;
    const bb = bm.clone(); bb.map = tb; bb.emissiveMap = tb; bb.side = THREE.BackSide;
    const f = new THREE.Mesh(geo, bm), b = new THREE.Mesh(geo, bb);
    banner.add(f, b); plane.add(banner);
    plane.userData.geo = geo; plane.userData.base = geo.attributes.position.array.slice();
    plane.scale.setScalar(2.4); scene.add(plane);
  }
  function movePlane(sec) {                                               // melintas di langit di belakang gedung, tegak lurus arah pandang
    const az = 0.56, dx = Math.cos(az), dz = -Math.sin(az), u = ((sec * 16) % 600) - 300;
    plane.position.set(dx * u - Math.sin(az) * 70, 90 + Math.sin(sec * 0.5) * 2, dz * u - Math.cos(az) * 70);
    plane.rotation.set(0, Math.atan2(-dz, dx), 0);
    plane.userData.prop.rotation.x = sec * 40;
    const pos = plane.userData.geo.attributes.position, b0 = plane.userData.base;
    for (let i = 0; i < pos.count; i++) { const x = b0[i * 3]; pos.array[i * 3 + 2] = Math.sin(x * 0.9 + sec * 6) * 0.25 * (-x / 9.5); }
    pos.needsUpdate = true;
  }
  function moveWorld(dt, now) {
    const sec = now / 1000;
    farCars.forEach(k => { const p = k.c.position; p[k.axis] += k.dir * k.speed * dt; if (p[k.axis] > 430) p[k.axis] = -430; if (p[k.axis] < -430) p[k.axis] = 430; });
    logs.forEach(l => { l.m.position.x += l.dir * l.speed * dt; if (l.m.position.x > 450) l.m.position.x = -450; if (l.m.position.x < -450) l.m.position.x = 450; l.m.position.y = 0.35 + Math.sin(sec * 1.5 + l.m.position.x) * 0.08; });
    train.position.x += 26 * dt; if (train.position.x > 520) train.position.x = -520;
    movePlane(sec);
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
  const menuPose = () => {                                             // tampilan menu lantai: gedung di tengah, cukup ruang untuk judul di kiri-kanan
    const narrow = VW < 900, az = 0.5, el = 0.12, top = TOTAL + 35;
    let d = (top / 2 + 3) / TAN / 0.82;
    if (narrow) d = Math.max(d, 14.5 / (TAN * (VW / VH) * 0.4));
    const look = new THREE.Vector3(0, top / 2 + (narrow ? 2 : 0), 0);
    return { pos: new THREE.Vector3(Math.sin(az) * Math.cos(el) * d, look.y + Math.sin(el) * d, Math.cos(az) * Math.cos(el) * d), look, up };
  };
  let menu = false, menuP = 0, menuK = 0, lockUntil = 0, lastMenuT = performance.now();
  function startPose() {
    if (menuK <= 0) return far();
    const a = far(), b = menuPose();
    return { pos: a.pos.lerp(b.pos, menuK), look: a.look.lerp(b.look, menuK), up };
  }
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
  let ready = false;
  function resize() {
    VW = document.documentElement.clientWidth || innerWidth; VH = innerHeight;
    if (VW < 2 || VH < 2) return;                                          // tab tersembunyi / belum punya ukuran: tunggu
    Z = parseFloat(getComputedStyle(document.body).zoom) || 1;               // situs memakai zoom .9 di desktop
    const cw = VW / Z, ch = VH / Z;                                          // ukuran dalam px CSS halaman
    root.style.setProperty('--vhp', ch + 'px');
    gl.setSize(VW, VH, false);
    { const ds = gl.getDrawingBufferSize(new THREE.Vector2()); rtA.setSize(Math.ceil(ds.x / 2), Math.ceil(ds.y / 2)); rtB.setSize(Math.ceil(ds.x / 2), Math.ceil(ds.y / 2)); }
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
    ready = true;
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
    if (visit) { if (!on3d) { root.classList.add('gd-3d-on'); on3d = true; } return visitFrame(); }
    const a = activeScene();
    if (!a || a.t >= 0.999) { if (on3d) { root.classList.remove('gd-3d-on'); on3d = false; } return false; }
    if (!on3d) { root.classList.add('gd-3d-on'); on3d = true; }
    const t = a.t;
    const lifts = {}; for (let k = 1; k <= N; k++) lifts[k] = 0;
    let roofLift = 1, hero = 0, outro = 0;
    const want = {};
    {                                                    // luar gedung -> atap -> ruang meeting -> layar
      hero = (1 - clamp(t / 0.14)) * (1 - menuK);
      roofLift = seg(t, 0.24, 0.5);
      if (t < 0.36) blend(startPose(), above(), seg(t, 0, 0.36));
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
    placeMenu(menuK * (1 - clamp(t / 0.04)));
    return true;
  }
  function visitFrame() {
    const now = performance.now(); if (!visit.t0 || (visit.rev && ((visit.f = (visit.f || 0) + 1) < 8 || (!(LABELS[visit.k].img && LABELS[visit.k].img[visit.v]) && now - visit.since < 1500)))) visit.t0 = now;   // rev: tunggu beberapa frame pertama (kompilasi shader) baru mulai
    if (!visit.from) visit.from = startPose();
    const raw = clamp((now - visit.t0) / VISIT_MS), t = visit.rev ? 1 - raw : raw;   // rev: dari layar lantai mundur ke menu lantai
    const k = visit.k, rise = TOTAL - base(k) + 70;
    const open = seg(t, 0.04, 0.32);                                  // lantai di atasnya & atap terangkat
    for (let j = 1; j <= N; j++) setLift(j, j > k ? open : 0, rise);
    setRoof(k === N ? seg(t, 0.04, 0.32) : open, rise);
    if (t < 0.36) blend(visit.from, above(k), seg(t, 0, 0.36));
    else if (t < 0.7) blend(above(k), poses[k].room, seg(t, 0.36, 0.7));
    else blend(poses[k].room, poses[k].fill, seg(t, 0.7, 1));
    for (const f in faces) showFace(+f, null);
    beam.material.opacity = k === N ? 0.15 * clamp((t - 0.5) / 0.2) : 0;
    root.style.setProperty('--hero', (1 - clamp(t / 0.12)) * (1 - menuK));
    hl.visible = false; tip.style.opacity = 0; placeMenu(menuK * (1 - clamp(t / 0.1)));
    if (visit.rev && raw >= 1) { visit = null; auto = null; settle = true; gestUsed = true; lockUntil = now + 900; return true; }
    if (!visit.rev && t >= 1 && !visit.gone) { visit.gone = true; location.href = PAGES[k][1]; }
    return true;
  }
  function startVisit(k) {
    if (visit || auto) return;
    const ip = introProgress(); if (!ip || ip.t > 0.02) return;           // hanya dari tampilan awal gedung
    if (k === N) { menu = true; playIntro(); return; }                   // lantai Beranda: masuk lewat proyektor ruang meeting, sama seperti scroll
    if (k === N) screens[N].surface.material = LABELS[N].mat;
    visit = { k, t0: performance.now(), from: startPose() };
    auto = true;                                                         // input scroll diabaikan selama perjalanan
  }
  function startReturn(k) {                                            // datang dari halaman lantai k: mundur dari layarnya ke menu lantai
    if (k === N) screens[N].surface.material = LABELS[N].mat;
    menu = true; menuP = menuK = 1;
    const v = shotW(); if (LABELS[k]) LABELS[k].load(v);   // layar lantai: tangkapan layar halaman asalnya
    visit = { k, t0: 0, from: null, rev: true, v, since: performance.now() };
    auto = true;
  }
  addEventListener('pageshow', e => { if (e.persisted && visit) { visit = null; auto = null; menu = false; menuP = menuK = 0; screens[N].surface.material = M.white; scrollTo({ top: 0, behavior: 'instant' }); } });

  // menu lantai: garis penunjuk + judul halaman di tiap lantai (muncul setelah scroll pertama)
  const fm = document.createElement('nav'); fm.className = 'gd-floormenu'; fm.setAttribute('aria-label', 'Lantai gedung Altora');
  const fmItems = {};
  for (let k = N; k >= 1; k--) {
    const a = document.createElement('a'); a.href = PAGES[k][1]; a.className = 'gd-fl ' + (k % 2 ? 'gd-fl-r' : 'gd-fl-l');
    a.innerHTML = '<span class="gd-fl-dot"></span><span class="gd-fl-line"></span><span class="gd-fl-txt"><b>' + PAGES[k][0] + '</b><small>' + PAGES[k][2] + '</small></span>';
    a.addEventListener('click', e => { e.preventDefault(); startVisit(k); });
    a.addEventListener('mouseenter', () => { hl.visible = true; hl.scale.y = height(k) + 0.1; hl.position.y = base(k) + height(k) / 2; });
    a.addEventListener('mouseleave', () => { hl.visible = false; });
    fm.appendChild(a); fmItems[k] = a;
  }
  const fmHint = document.createElement('p'); fmHint.className = 'gd-fm-hint';
  fmHint.innerHTML = 'Pilih lantai untuk langsung ke halamannya <span aria-hidden="true">·</span> <b>scroll lagi ke beranda ↓</b>';
  fm.appendChild(fmHint); root.appendChild(fm);
  const pv = new THREE.Vector3();
  const toScreen = (x, y, z) => { pv.set(x, y, z).project(camera); return [(pv.x + 1) / 2 * VW / Z, (1 - pv.y) / 2 * VH / Z]; };
  function placeMenu(o) {
    blurK = o;
    fm.style.opacity = o; fm.classList.toggle('on', o > 0.85);
    if (o <= 0.01) return;
    camera.updateMatrixWorld();
    for (let k = 1; k <= N; k++) {
      const y = base(k) + height(k) / 2, pts = [[-W / 2, D / 2], [W / 2, D / 2], [W / 2, -D / 2], [-W / 2, -D / 2]].map(([x, z]) => toScreen(x, y, z));
      const left = k % 2 === 0, p = pts.reduce((m, q) => (left ? q[0] < m[0] : q[0] > m[0]) ? q : m);
      fmItems[k].style.transform = 'translate(' + p[0].toFixed(1) + 'px,' + p[1].toFixed(1) + 'px) translate(' + (left ? '-100%' : '0') + ',-50%)';
    }
  }
  function tickMenu(now) {
    const dt = Math.min(0.1, (now - lastMenuT) / 1000); lastMenuT = now;
    menuP = clamp(menuP + (menu ? dt : -dt) / 0.9);
    menuK = ease(menuP);
  }

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
    hl.visible = !!k; tip.style.opacity = k && menuK < 0.5 ? 1 : 0;
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
  let stopped = false;
  window.__gdStop = () => { stopped = true; };
  let lastDraw = 0, busyUntil = 0;
  ['scroll', 'wheel', 'touchmove'].forEach(ev => addEventListener(ev, () => { busyUntil = performance.now() + 500; }, { passive: true }));
  function loop(now = performance.now()) {
    if (stopped) return;
    // HP: saat diam cukup 30 fps (mobil/awan tetap mulus, GPU & baterai separuh); saat scroll/animasi tetap penuh
    const idle = mobile && !auto && !visit && now > busyUntil && (menuP === 0 || menuP === 1);
    if (!idle || now - lastDraw > 30) { lastDraw = now; try { step(); } catch (e) { fail(e); return; } }
    requestAnimationFrame(loop);
  }
  function step() {
    const cw = document.documentElement.clientWidth || innerWidth;
    if (cw !== VW || innerHeight !== VH || !ready) resize();               // zoom/resize yang tidak memicu event
    if (!ready) return;
    tickMenu(performance.now());
    if (frame()) {
      const tt = (performance.now() - t0) / 1000;
      beacon.material.emissiveIntensity = 1.2 + Math.sin(tt * 3.3);
      moveCars(performance.now());
      animateSky(performance.now());
      if (++skyTick % 600 === 1) applySky();                                    // perbarui langit tiap ~10 detik
      leds.forEach((l, i) => { l.visible = Math.sin(tt * 4 + i * 1.7) > -0.3; });
      if (mobile && (skyTick % 4 === 1 || visit || auto)) gl.shadowMap.needsUpdate = true;   // HP: bayangan tiap 4 frame, tiap frame saat animasi
      renderScene();
      css.render(scene, camera);
    }
  }
  // ── sekali scroll ke bawah di pembuka -> animasi berjalan sendiri sampai beranda ──
  let auto = null, settle = false;                                       // settle: sisa momentum setelah animasi ditahan sampai ada usapan baru
  function introProgress() {
    const sc = scenes[0]; if (!sc) return null;
    const r = sc.getBoundingClientRect(), span = r.height - VH;
    if (-r.top > span - 1) return null;                                    // sudah lewat pembuka
    return { r, span, t: clamp(-r.top / span) };
  }
  function scrollAnim(to, dur, done) {
    const from = scrollY, t0 = performance.now();
    const ez = x => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2);
    auto = true;
    (function step(now) {
      const k = Math.min(1, (now - t0) / dur);
      scrollTo({ top: from + (to - from) * ez(k), behavior: 'instant' });   // situs memakai scroll-behavior:smooth
      if (k < 1) requestAnimationFrame(step); else { auto = null; settle = true; gestUsed = true; lockUntil = performance.now() + 900; if (done) done(); }
    })(t0);
    return true;
  }
  function playIntro() {                                                  // menu lantai -> beranda
    const ip = introProgress(); if (!ip || auto) return false;
    return scrollAnim(scrollY + (ip.r.top + ip.span) / Z + 2, 3200 * (1 - ip.t) + 400);
  }
  function playBack() {                                                   // beranda -> kembali ke menu lantai
    const sc = scenes[0]; if (!sc || auto) return false;
    const r = sc.getBoundingClientRect(), span = r.height - VH, t = clamp(-r.top / span);
    menu = true; menuP = 1; menuK = 1;
    return scrollAnim(scrollY + r.top / Z, 2400 * t + 400, () => { lockUntil = performance.now() + 900; });
  }
  function nearIntroEnd() {                                               // di puncak konten beranda, tepat di bawah pembuka
    const sc = scenes[0]; if (!sc) return false;
    const r = sc.getBoundingClientRect();
    return (-r.top - (r.height - VH)) / Z < 80;
  }
  const block = e => { if (auto) { e.preventDefault(); return true; } return false; };
  // urutan: 1 pembuka -> (scroll) 2 menu lantai -> (klik) 3 masuk lantai | (scroll) 4 beranda
  // scroll ke atas dari beranda -> 2 menu lantai -> (scroll ke atas lagi) 1 pembuka
  function goDown(gap = 1e9) {                                            // true = ditangani (scroll halaman dicegah); gap = jeda sejak event wheel sebelumnya
    const ip = introProgress(); if (!ip) return false;
    if (ip.t > 0.02) return playIntro();
    if (!menu) { menu = true; lockUntil = performance.now() + 900; return true; }
    if (performance.now() < lockUntil || gap < 280) return true;          // sisa momentum usapan pertama diabaikan
    return playIntro();
  }
  function goUp(gap = 1e9) {
    const ip = introProgress();
    if (!ip) return nearIntroEnd() ? playBack() : false;
    if (ip.t > 0.02) return playBack();
    if (!menu) return false;
    if (performance.now() >= lockUntil && gap >= 280) { menu = false; lockUntil = performance.now() + 900; }
    return true;
  }
  let lastWheel = 0, lastAbs = 0, gestUsed = false;                      // gestUsed: usapan ini sudah memicu perpindahan adegan
  addEventListener('wheel', e => {
    const now = performance.now(), abs = Math.abs(e.deltaY);
    // usapan baru = ada jeda, atau kecepatan melonjak (momentum selalu melambat), atau scroll tetap tidak melambat >1,6 dtk sejak pindah adegan
    const fresh = now - lastWheel >= 250 || abs > lastAbs * 1.5 + 4 || (now > lockUntil + 700 && abs >= 12 && abs >= lastAbs);
    lastWheel = now; lastAbs = abs;
    if (fresh) gestUsed = false;
    if (block(e)) { gestUsed = true; return; }
    if (settle) { if (gestUsed) { e.preventDefault(); return; } settle = false; }   // stopper: sisa usapan tadi tidak keterusan
    const was = menu, gap = gestUsed ? 0 : 1e9;                          // usapan yang belum terpakai tetap berlaku sampai kunci selesai
    const handled = (e.deltaY > 4 && goDown(gap)) || (e.deltaY < -4 && goUp(gap));
    if (menu !== was || auto) gestUsed = true;
    if (handled) e.preventDefault();
  }, { passive: false });
  let ty0 = null;
  addEventListener('touchstart', e => { ty0 = e.touches[0].clientY; }, { passive: true });
  addEventListener('touchmove', e => {
    if (block(e)) return;
    if (ty0 === null) return;
    const dy = ty0 - e.touches[0].clientY;
    if (dy > 8 && goDown()) { e.preventDefault(); ty0 = null; }
    else if (dy < -8 && goUp()) { e.preventDefault(); ty0 = null; }
  }, { passive: false });
  addEventListener('keydown', e => {
    if (auto && ['ArrowDown', 'PageDown', ' ', 'Spacebar', 'End', 'ArrowUp', 'PageUp', 'Home'].includes(e.key)) { e.preventDefault(); return; }
    if (['ArrowDown', 'PageDown', ' ', 'Spacebar', 'End'].includes(e.key) && goDown()) e.preventDefault();
    else if (['ArrowUp', 'PageUp', 'Home'].includes(e.key) && goUp()) e.preventDefault();
  });
  addEventListener('resize', resize);
  if (window.visualViewport) visualViewport.addEventListener('resize', resize);
  // tiap objek bergerak digabung jadi satu mesh per material (bergerak sebagai satu kesatuan), struktur lantai & atap juga
  walkers.forEach(w => bakeColor(w.p)); cars.forEach(k => bakeColor(k.c)); farCars.forEach(k => bakeColor(k.c)); crowd.forEach(c => bakeColor(c.p));
  bakeColor(train); balloons.forEach(b => bakeColor(b.g)); clouds.forEach(c => bake(c.g));
  for (let k = 1; k <= N; k++) bake(floors[k].g, new Set(floors[k].g.children.filter(o => !o.isMesh)));
  bake(roof, new Set([logoHolder]));
  // gedung di layer 1 (dirender tajam terpisah saat menu lantai), sisanya layer 0; cahaya menyinari keduanya
  for (let k = 1; k <= N; k++) floors[k].g.traverse(o => o.layers.set(1));
  roof.traverse(o => o.layers.set(1)); hl.layers.set(1);
  scene.traverse(o => { if (o.isLight) o.layers.enableAll(); });
  camera.layers.enable(1);
  resize();
  setTimeout(() => { const v = shotW(); for (const k in LABELS) LABELS[k].load(v); }, 1200);   // tangkapan layar halaman dimuat setelah gedung tampil
  let back = 0; try { back = +sessionStorage.getItem('gdBack') || 0; sessionStorage.removeItem('gdBack'); } catch (e) {}
  if (back >= 1 && back <= N) { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; scrollTo({ top: 0, behavior: 'instant' }); startReturn(back); }
  loop();
}
