/* Medan ASCII footer: gumpalan noise simplex 3D yang pelan-pelan berubah bentuk, digambar sebagai grid glyph ".:-=+*#%@".
   Port setia dari footer Sentra (field.js): satu fragment shader WebGL, CPU hanya mengirim waktu per frame (30 fps).
   Ditambah: berhenti saat footer di luar layar (IntersectionObserver) dan saat tab tersembunyi; tanpa WebGL atau saat
   "kurangi gerakan" aktif: satu frame diam. Hanya warna yang diganti ke palet Altora. */
(function () {
  var canvas = document.querySelector('.ft-ocean canvas');
  if (!canvas) return;
  var VERT = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  // Simplex noise 3D: Ian McEwan & Stefan Gustavson (Ashima Arts), MIT License.
  var NOISE = [
    'vec3 m289(vec3 x){return x-floor(x*(1./289.))*289.;}',
    'vec4 m289(vec4 x){return x-floor(x*(1./289.))*289.;}',
    'vec4 perm(vec4 x){return m289(((x*34.)+1.)*x);}',
    'vec4 tis(vec4 r){return 1.79284291400159-.85373472095314*r;}',
    'float snoise(vec3 v){const vec2 C=vec2(1./6.,1./3.);const vec4 D=vec4(0.,.5,1.,2.);',
    'vec3 i=floor(v+dot(v,C.yyy));vec3 x0=v-i+dot(i,C.xxx);vec3 g=step(x0.yzx,x0.xyz);vec3 l=1.-g;',
    'vec3 i1=min(g.xyz,l.zxy);vec3 i2=max(g.xyz,l.zxy);vec3 x1=x0-i1+C.xxx;vec3 x2=x0-i2+C.yyy;vec3 x3=x0-D.yyy;',
    'i=m289(i);vec4 p=perm(perm(perm(i.z+vec4(0.,i1.z,i2.z,1.))+i.y+vec4(0.,i1.y,i2.y,1.))+i.x+vec4(0.,i1.x,i2.x,1.));',
    'float n_=.142857142857;vec3 ns=n_*D.wyz-D.xzx;vec4 j=p-49.*floor(p*ns.z*ns.z);vec4 x_=floor(j*ns.z);vec4 y_=floor(j-7.*x_);',
    'vec4 x=x_*ns.x+ns.yyyy;vec4 y=y_*ns.x+ns.yyyy;vec4 h=1.-abs(x)-abs(y);vec4 b0=vec4(x.xy,y.xy);vec4 b1=vec4(x.zw,y.zw);',
    'vec4 s0=floor(b0)*2.+1.;vec4 s1=floor(b1)*2.+1.;vec4 sh=-step(h,vec4(0.));',
    'vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;',
    'vec3 p0=vec3(a0.xy,h.x);vec3 p1=vec3(a0.zw,h.y);vec3 p2=vec3(a1.xy,h.z);vec3 p3=vec3(a1.zw,h.w);',
    'vec4 norm=tis(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));p0*=norm.x;p1*=norm.y;p2*=norm.z;p3*=norm.w;',
    'vec4 m=max(.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.);m=m*m;',
    'return 42.*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));}'
  ].join('\n');
  var FRAG = [
    'precision mediump float;',
    'uniform vec2 res;uniform float t,cell,scale,thresh;uniform sampler2D atlas;uniform float n;',
    'uniform vec3 bg,bg2,c1,c2;',
    NOISE,
    'float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
    'void main(){',
    '  vec2 px=vec2(gl_FragCoord.x,res.y-gl_FragCoord.y);',
    '  vec2 id=floor(px/cell);vec2 uv=fract(px/cell);',
    '  vec2 q=id*cell/scale;',
    '  float v=snoise(vec3(q*.9,t*.05))*.7+snoise(vec3(q*2.1+7.3,t*.08))*.3;',
    '  v=v*.5+.5;',
    '  float k=clamp((v-thresh)/(1.-thresh),0.,1.);',
    '  vec3 base=mix(bg,bg2,px.y/res.y);vec3 col=base;',
    '  if(k>0.){',
    '    float flick=step(.92,hash(id+floor(t*1.5)));',
    '    float g=floor(min(k*1.6+flick*.35,1.)*(n-1.)+.5);',
    '    float a=texture2D(atlas,vec2((g+uv.x)/n,uv.y)).a;',
    '    col=mix(base,mix(c1,c2,smoothstep(.15,.9,k)),a*smoothstep(0.,.08,k));',
    '  }',
    '  gl_FragColor=vec4(col,1.);',
    '}'
  ].join('\n');
  var GLYPHS = '.:-=+*#%@';
  // Warna palet Altora (Sentra: bg #13306B/#081530, c1 #3E6FCC, c2 #A9C6F5)
  var COLORS = { bg: '#3E2A97', bg2: '#10224F', c1: '#7C5CE8', c2: '#D6C8FF' };
  var small = window.matchMedia('(max-width: 640px)').matches;
  var o = { cell: small ? 10 : 11, scale: small ? 170 : 220, thresh: 0.5, fps: 30 };

  function hex(c) { var n = parseInt(c.slice(1), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; }
  var gl = null;
  try { gl = canvas.getContext('webgl', { antialias: false, alpha: false, powerPreference: 'low-power' }); } catch (err) {}
  if (!gl || !window.ResizeObserver || !window.IntersectionObserver) {
    canvas.style.background = 'linear-gradient(' + COLORS.bg + ',' + COLORS.bg2 + ')';
    return;
  }
  function sh(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  var pr = gl.createProgram();
  try {
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, VERT)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FRAG));
  } catch (err) { canvas.style.background = 'linear-gradient(' + COLORS.bg + ',' + COLORS.bg2 + ')'; return; }
  gl.linkProgram(pr); gl.useProgram(pr);
  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(pr, 'p');
  gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  var u = {};
  ['res', 't', 'cell', 'scale', 'thresh', 'atlas', 'n', 'bg', 'bg2', 'c1', 'c2'].forEach(function (k) { u[k] = gl.getUniformLocation(pr, k); });
  gl.uniform3fv(u.bg, hex(COLORS.bg)); gl.uniform3fv(u.bg2, hex(COLORS.bg2)); gl.uniform3fv(u.c1, hex(COLORS.c1)); gl.uniform3fv(u.c2, hex(COLORS.c2));
  gl.uniform1f(u.thresh, o.thresh); gl.uniform1f(u.n, GLYPHS.length); gl.uniform1i(u.atlas, 0);

  function atlas(cellPx) {
    var c = document.createElement('canvas'), n = GLYPHS.length;
    c.width = cellPx * n; c.height = cellPx;
    var g = c.getContext('2d');
    g.font = '600 ' + Math.round(cellPx * 0.82) + 'px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff';
    for (var i = 0; i < n; i++) g.fillText(GLYPHS[i], i * cellPx + cellPx / 2, cellPx / 2 + 1);
    var tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  }

  var t0 = performance.now(), last = 0, raf = 0, visible = true;
  var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  function reduced() { return mq.matches; }
  function draw(t) { gl.uniform1f(u.t, t); gl.drawArrays(gl.TRIANGLES, 0, 3); }
  function schedule() {
    cancelAnimationFrame(raf);
    if (visible && !reduced() && !document.hidden) raf = requestAnimationFrame(tick);
  }
  function tick(now) {
    raf = requestAnimationFrame(tick);
    if (now - last < 1000 / o.fps - 2) return;   // gerakannya pelan; 30 fps sudah mulus
    last = now;
    draw((now - t0) / 1000);
  }
  function resize() {
    var r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
    if (!r.width || !r.height) return;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
    var cellPx = Math.round(o.cell * dpr);
    atlas(cellPx);
    gl.uniform2f(u.res, canvas.width, canvas.height);
    gl.uniform1f(u.cell, cellPx);
    gl.uniform1f(u.scale, o.scale * dpr);
    draw(reduced() ? 0 : (performance.now() - t0) / 1000);
    schedule();
  }
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(function (e) { visible = e[0].isIntersecting; schedule(); }).observe(canvas);
  document.addEventListener('visibilitychange', schedule);
  if (mq.addEventListener) mq.addEventListener('change', function () { draw(0); schedule(); });
  resize();
})();
