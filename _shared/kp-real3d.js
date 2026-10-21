/* ═══ KP Real3D — ทำภาพ 3D ของแลปให้สมจริงขึ้น (โหลดต่อจาก three.js ทันที) ═══
   ครอบ THREE.WebGLRenderer ไว้ แล้วตอนเรนเดอร์ครั้งแรกของแต่ละฉากจะเติมให้เอง:
   1. แสงสะท้อนรอบตัว (environment map แบบห้อง) → โลหะ/พลาสติกเงาวาว
   2. เงานุ่มจากไฟหลัก ทอดลงพื้นโต๊ะ
   3. ห้อง: โต๊ะลายไม้ + ผนังเทาอ่อน (ปิดได้)
   4. ป้ายชื่อ (Sprite) ได้กรอบทึบสีเข้ม อ่านออกบนพื้นสว่าง
   ไม่แตะฟิสิกส์ กล้อง หรือการวัดของแลป · ภาพคมทุกจุด (ไม่มี depth of field)

   ตั้งค่ารายไฟล์ (ใส่ก่อนโหลดสคริปต์นี้):  window.KP_REAL3D = { room:false, shadows:false, table:false, env:0.8 }
   ปิดทั้งหมดชั่วคราว: เติม ?real3d=0 ท้าย URL */
(function(){
  if (typeof THREE === 'undefined' || !THREE.WebGLRenderer || THREE.WebGLRenderer.__kpReal) return;
  if (/[?&]real3d=0\b/.test(location.search)) return;
  /* ค่าเฉพาะแลป (ตามเลขหน้าชื่อไฟล์)
     dark = ห้องมืด (แลปแสงที่ต้องเห็นลำแสง/ภาพบนฉาก) · space = ไม่มีห้อง/โต๊ะ (อวกาศ) */
  var PRESETS = {
    dark:  ['35', '36', '46', '47', '50', '51', '52', '53'],
    /* หรี่ไฟ: แลปลำแสง/รังสีแสงที่ต้องอ่านค่าบนกระดาษหรือสเกล — ลำแสงเด่น แต่ยังอ่านได้ */
    dim:   ['32B', '33B', '49', '116', '87', '88', '94'],
    space: ['69']
  };
  var labNo = (decodeURIComponent(location.pathname).match(/\/(\d+[A-Za-z]?)\.[^\/]*$/) || [])[1];
  var preset = {};
  if (PRESETS.dark.indexOf(labNo) >= 0) preset = { room: 'dark' };
  if (PRESETS.dim.indexOf(labNo) >= 0) preset = { room: 'dim' };
  if (PRESETS.space.indexOf(labNo) >= 0) preset = { room: false, shadows: false };
  var CFG = Object.assign({ exposure: 1.25, env: 0.45, rim: 0.6, keyBoost: 1.5, shadows: true, room: true, table: true, labels: true }, preset, window.KP_REAL3D || {});
  /* เทียบสไตล์ห้องได้ทาง URL: ?room=studio | wood | dark */
  var qRoom = (location.search.match(/[?&]room=(studio|wood|dark|dim)\b/) || [])[1];
  if (qRoom) CFG.room = qRoom === 'wood' ? true : qRoom;
  var STUDIO = CFG.room === 'studio';
  if (STUDIO && !(window.KP_REAL3D && window.KP_REAL3D.exposure)) CFG.exposure = 1.15;
  var Orig = THREE.WebGLRenderer;
  var renderers = [], scenes = [];
  var busy = false;   /* PMREM เรียก render ซ้อน — กันวนซ้ำ */
  var LOW = Math.min(screen.width, screen.height) < 600;

  function Wrapped(params){
    var r = new Orig(params);
    renderers.push(r);
    var rawRender = r.render.bind(r);
    r.shadowMap.enabled = !!CFG.shadows;
    r.shadowMap.type = THREE.PCFSoftShadowMap;
    /* ไล่โทนแบบฟิล์ม: ผิวสว่างไม่ขาวโพลน (เฉพาะวัสดุที่รับแสง — ลำแสง/จอ/ป้าย คงสีเดิม) */
    if (CFG.exposure > 0) { r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = CFG.exposure; }
    r.render = function(scene, camera){
      if (scene && scene.isScene && !busy && !scene.userData.__kpEnvScene) {
        busy = true;
        try { prep(r, scene, camera); } catch (e) { if (!r.__kpErr) { r.__kpErr = 1; console.warn('kp-real3d:', e); } }
        busy = false;
      }
      return rawRender(scene, camera);
    };
    return r;
  }
  Wrapped.prototype = Orig.prototype;
  Wrapped.__kpReal = true;
  THREE.WebGLRenderer = Wrapped;

  /* ── environment map: ห้องจำลองเล็ก ๆ (แบบ RoomEnvironment) ── */
  var envCache = new WeakMap();
  function envFor(r){
    if (envCache.has(r)) return envCache.get(r);
    var s = new THREE.Scene(); s.userData.__kpEnvScene = true; var box = new THREE.BoxGeometry();
    var room = new THREE.Mesh(box, new THREE.MeshBasicMaterial({ color: 0x8a8d92, side: THREE.BackSide }));
    room.scale.set(30, 16, 30); room.position.y = 6; s.add(room);
    function panel(x, y, z, sx, sy, sz, c){ var m = new THREE.Mesh(box, new THREE.MeshBasicMaterial({ color: c })); m.position.set(x, y, z); m.scale.set(sx, sy, sz); s.add(m); }
    panel(0, 13.9, 0, 10, 0.1, 6, 0xffffff);        /* ไฟเพดาน */
    panel(-14.9, 7, 0, 0.1, 6, 12, 0xd8dde6);       /* หน้าต่างซ้าย */
    panel(14.9, 6, -4, 0.1, 4, 6, 0xb8bec8);
    panel(0, 5, -14.9, 12, 5, 0.1, 0xc8ccd2);
    panel(0, -1.9, 0, 30, 0.1, 30, 0x5a4636);       /* พื้นสีไม้ */
    var pm = new THREE.PMREMGenerator(r);
    var tex = pm.fromScene(s, 0.04).texture;
    pm.dispose();
    envCache.set(r, tex);
    return tex;
  }

  /* ── ลายไม้ (วาดด้วยโค้ด ไม่ต้องโหลดรูป) ── */
  var woodTex = null;
  function wood(){
    if (woodTex) return woodTex;
    var c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    var g = c.getContext('2d');
    g.fillStyle = '#7a5640'; g.fillRect(0, 0, 1024, 1024);
    for (var p = 0; p < 8; p++) {                       /* แผ่นไม้ 8 แผ่น */
      var y0 = p * 128, tone = 0.86 + ((p * 37) % 7) / 30;
      g.fillStyle = 'rgba(' + Math.round(132 * tone) + ',' + Math.round(94 * tone) + ',' + Math.round(66 * tone) + ',1)';
      g.fillRect(0, y0, 1024, 128);
      for (var k = 0; k < 46; k++) {                    /* เสี้ยนไม้ */
        var yy = y0 + Math.random() * 128, a = 0.04 + Math.random() * 0.09;
        g.strokeStyle = Math.random() < 0.5 ? 'rgba(60,32,14,' + a + ')' : 'rgba(210,160,110,' + a * 0.8 + ')';
        g.lineWidth = 0.6 + Math.random() * 2.2;
        g.beginPath(); g.moveTo(0, yy);
        var ph = Math.random() * 6, amp = 1 + Math.random() * 3;
        for (var x = 0; x <= 1024; x += 32) g.lineTo(x, yy + Math.sin(x / 140 + ph) * amp);
        g.stroke();
      }
      g.fillStyle = 'rgba(40,20,8,.35)'; g.fillRect(0, y0, 1024, 2); /* ร่องระหว่างแผ่น */
    }
    woodTex = new THREE.CanvasTexture(c);
    woodTex.wrapS = woodTex.wrapT = THREE.RepeatWrapping;
    woodTex.anisotropy = 8;
    return woodTex;
  }

  /* ฉากหลังสตูดิโอ: เทาเข้มไล่เฉด กลางสว่าง ขอบมืด (แบบผ้าฉากถ่ายสินค้า) */
  function studioTex(){
    var c = document.createElement('canvas'); c.width = 512; c.height = 512;
    var g = c.getContext('2d'), v = g.createLinearGradient(0, 0, 0, 512);
    v.addColorStop(0, '#26292c'); v.addColorStop(0.42, '#373a3e'); v.addColorStop(1, '#373a3e');   /* ครึ่งล่าง = สีหมอกพื้น → ไม่เห็นขอบ */
    g.fillStyle = v; g.fillRect(0, 0, 512, 512);
    var r = g.createRadialGradient(256, 230, 30, 256, 256, 380);
    r.addColorStop(0, 'rgba(255,255,255,.07)'); r.addColorStop(0.6, 'rgba(255,255,255,0)'); r.addColorStop(1, 'rgba(0,0,0,.28)');
    g.fillStyle = r; g.fillRect(0, 0, 512, 512);
    return new THREE.CanvasTexture(c);
  }
  function wallTex(dark){
    if (CFG.room === 'dim') {
      var cd = document.createElement('canvas'); cd.width = 4; cd.height = 256;
      var gd = cd.getContext('2d'), gg = gd.createLinearGradient(0, 0, 0, 256);
      gg.addColorStop(0, '#24272c'); gg.addColorStop(0.6, '#363a41'); gg.addColorStop(1, '#2e3238');
      gd.fillStyle = gg; gd.fillRect(0, 0, 4, 256);
      return new THREE.CanvasTexture(cd);
    }
    if (STUDIO) return studioTex();
    var c = document.createElement('canvas'); c.width = 4; c.height = 256;
    var g = c.getContext('2d'), gr = g.createLinearGradient(0, 0, 0, 256);
    if (dark) { gr.addColorStop(0, '#0b0e13'); gr.addColorStop(0.6, '#161a21'); gr.addColorStop(1, '#12151a'); }
    else { gr.addColorStop(0, '#9fa3a9'); gr.addColorStop(0.6, '#bfc2c7'); gr.addColorStop(1, '#b3b6bb'); }
    g.fillStyle = gr; g.fillRect(0, 0, 4, 256);
    return new THREE.CanvasTexture(c);
  }

  /* ── ป้ายชื่อ: เพิ่มกรอบทึบด้านหลัง ── */
  var pillTex = null;
  function pill(){
    if (pillTex) return pillTex;
    var c = document.createElement('canvas'); c.width = 256; c.height = 64;
    var g = c.getContext('2d'), R = 22;
    g.fillStyle = 'rgba(15,23,42,.88)'; g.strokeStyle = 'rgba(255,255,255,.25)'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(R + 2, 2); g.arcTo(254, 2, 254, 62, R); g.arcTo(254, 62, 2, 62, R); g.arcTo(2, 62, 2, 2, R); g.arcTo(2, 2, 254, 2, R); g.closePath();
    g.fill(); g.stroke();
    pillTex = new THREE.CanvasTexture(c);
    return pillTex;
  }
  function inkBox(img){
    /* หาขอบเขตตัวหนังสือในแคนวาสของป้าย (สัดส่วน 0–1) */
    try {
      var w = img.width, h = img.height; if (!w || !h || w * h > 1 << 20) return null;
      var d = img.getContext('2d', { willReadFrequently: true }).getImageData(0, 0, w, h).data, x0 = w, x1 = -1, y0 = h, y1 = -1;
      for (var y = 0; y < h; y += 2) for (var x = 0; x < w; x += 2) if (d[(y * w + x) * 4 + 3] > 40) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (x1 < 0) return null;
      /* ป้ายที่มีพื้นทึบเต็มแคนวาสอยู่แล้ว → ไม่ต้องเพิ่ม */
      if (x0 <= 2 && y0 <= 2 && x1 >= w - 3 && y1 >= h - 3) return null;
      return { cx: (x0 + x1) / 2 / w, cy: (y0 + y1) / 2 / h, w: (x1 - x0) / w, h: (y1 - y0) / h };
    } catch (e) { return null; }
  }
  function addBacking(sp){
    sp.userData.__kpPill = true;
    var m = sp.material, img = m && m.map && m.map.image;
    if (!img || !img.getContext || m.blending === THREE.AdditiveBlending) return;
    var b = inkBox(img); if (!b) return;
    var bk = new THREE.Sprite(new THREE.SpriteMaterial({ map: pill(), transparent: true, depthWrite: false, depthTest: m.depthTest, fog: false }));
    bk.userData.__kpPill = true;
    bk.userData.__kpFor = sp; bk.userData.__kpBox = b;
    bk.renderOrder = (sp.renderOrder || 0) - 0.5;
    m.fog = false;
    sp.parent.add(bk);
    sp.userData.__kpBk = bk;
    syncBacking(bk);
  }
  function syncBacking(bk){
    var sp = bk.userData.__kpFor, b = bk.userData.__kpBox;
    bk.visible = sp.visible && sp.material.opacity > 0.05 && !!sp.parent;
    if (!bk.visible) return;
    if (bk.parent !== sp.parent) { if (!sp.parent) return; sp.parent.add(bk); }
    var sx = sp.scale.x, sy = sp.scale.y, padY = 0.18 * sy;
    var w = b.w * sx + padY * 1.6, h = b.h * sy + padY;
    bk.scale.set(w, h, 1);
    /* ให้กึ่งกลางกรอบตรงกับกึ่งกลางตัวหนังสือ (แคนวาส y ลง · สไปรต์ y ขึ้น) */
    bk.center.set(0.5 - (b.cx - sp.center.x) * sx / w, 0.5 - ((1 - b.cy) - sp.center.y) * sy / h);
    bk.position.copy(sp.position);
    bk.material.opacity = sp.material.opacity;
    bk.material.depthTest = sp.material.depthTest;
  }

  /* ── ขอบเขตของอุปกรณ์ในฉาก (ใช้วางโต๊ะ/ตั้งกล้องเงา) ──
     แยก "พื้น" ของแลปเอง (แผ่นราบใหญ่ที่อยู่ล่างสุด) ออกจากตัวอุปกรณ์ */
  function bounds(scene){
    var all = new THREE.Box3(), list = [];
    scene.updateMatrixWorld(true);
    scene.traverse(function(o){
      if (!o.isMesh || !o.visible || o.userData.__kpRoom || !o.geometry) return;
      if (!o.geometry.boundingBox) o.geometry.computeBoundingBox();
      var bx = o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);
      if (!isFinite(bx.min.x) || bx.getSize(new THREE.Vector3()).length() > 4000) return;
      list.push({ o: o, b: bx }); all.union(bx);
    });
    if (!list.length) return null;
    var asz = all.getSize(new THREE.Vector3()), foot = Math.max(asz.x * asz.z, 1e-6);
    var floors = [], gear = new THREE.Box3();
    list.forEach(function(it){
      var z = it.b.getSize(new THREE.Vector3()), flat = z.y < 0.03 * Math.min(z.x, z.z);   /* แบนทั้ง 2 ด้าน (ไม่ใช่แท่งยาว เช่น รางแสง) */
      var low = it.b.max.y <= all.min.y + Math.max(asz.y * 0.04, 1e-3);
      if (flat && low && z.x * z.z >= 0.35 * foot) floors.push(it.o); else gear.union(it.b);
    });
    if (gear.isEmpty()) gear.copy(all);
    return { all: all, gear: gear, floors: floors };
  }

  function noTone(m){ if (m.toneMapped !== false) { m.toneMapped = false; m.needsUpdate = true; } }
  function litMat(m){ return m && (m.isMeshStandardMaterial || m.isMeshLambertMaterial || m.isMeshPhongMaterial); }

  function fixObjects(scene, st){
    scene.traverse(function(o){
      if ((o.isLine || o.isPoints || o.isSprite) && o.material && !Array.isArray(o.material)) noTone(o.material);
      if (o.isSprite) { if (st.room && CFG.labels && !o.userData.__kpPill) addBacking(o); return; }
      if (!o.isMesh || o.userData.__kpSeen) return;
      o.userData.__kpSeen = true;
      var mats = Array.isArray(o.material) ? o.material : [o.material], lit = false, solid = true;
      mats.forEach(function(m){
        if (!m) return;
        if (!litMat(m)) noTone(m);
        if (litMat(m)) lit = true;
        if (m.transparent && m.opacity < 0.9 || m.blending === THREE.AdditiveBlending || m.wireframe) solid = false;
        if (m.isMeshStandardMaterial && !m.__kpEnv) { m.__kpEnv = true; m.envMapIntensity = st.room === 'dark' ? CFG.env * 0.5 : st.room === 'dim' ? CFG.env * 0.6 : (STUDIO ? CFG.env * 1.25 : CFG.env); }
      });
      if (lit && CFG.shadows) { o.receiveShadow = true; o.castShadow = solid; }
    });
    st.pills.forEach(syncBacking);
  }

  var states = new WeakMap();
  function prep(r, scene, camera){
    var st = states.get(scene);
    if (st) {
      fogFollow(scene, st, camera);
      if (++st.frame % 45 === 0) { fixObjects(scene, st); collectPills(scene, st); }
      else st.pills.forEach(syncBacking);
      return;
    }
    var B = bounds(scene);
    if (!B) return;                                    /* ฉากยังว่าง รอเฟรมถัดไป */
    st = { frame: 0, pills: [], room: CFG.room, bounds: B };
    states.set(scene, st); scenes.push(scene);
    var DARK = CFG.room === 'dark', DIM = CFG.room === 'dim';
    var WOODC = DARK ? 0x6b6b6b : DIM ? 0x8c8c8c : 0xffffff;
    /* หรี่ไฟห้อง: ไฟของแลปเหลือ 60% (ลำแสง/จอ/ป้ายเป็นวัสดุไม่รับแสง จึงสว่างเท่าเดิม) */
    if (DIM) scene.traverse(function(o){ if (o.isLight && !o.userData.__kpRoom && !o.__kpDimRoom) { o.__kpDimRoom = true; o.intensity *= 0.6; } });

    var bb = B.gear, size = bb.getSize(new THREE.Vector3()), ctr = bb.getCenter(new THREE.Vector3());
    var span = Math.max(size.x, size.z, size.y * 0.6, 1);

    /* 1) แสงสะท้อนรอบตัว + ลดไฟแวดล้อมเดิมลงชดเชย */
    if (CFG.env > 0) {
      scene.environment = envFor(r);
      scene.traverse(function(o){
        if ((o.isHemisphereLight || o.isAmbientLight) && !o.__kpDim) { o.__kpDim = true; o.intensity *= 0.38; }
      });
    }

    /* 2) เงา: ใช้ไฟ directional ที่แรงที่สุด (ถ้าไม่มี สร้างใหม่) */
    if (CFG.shadows) {
      var key = null;
      scene.traverse(function(o){ if (o.isDirectionalLight && (!key || o.intensity > key.intensity)) key = o; });
      if (!key) {
        key = new THREE.DirectionalLight(0xffffff, 0.45);
        key.position.set(ctr.x + span * 0.6, ctr.y + span * 1.4, ctr.z + span * 0.8);
        key.target.position.copy(ctr); scene.add(key); scene.add(key.target);
      }
      key.castShadow = true;
      /* ไฟหลักแรงขึ้น → ด้านสว่าง/ด้านเงาต่างกันชัด วัตถุดูมีมิติ */
      if (!key.__kpBoost) { key.__kpBoost = true; key.intensity *= CFG.keyBoost; }
      var ms = LOW ? 1024 : 2048;
      key.shadow.mapSize.set(ms, ms);
      key.shadow.radius = 4;
      /* วางไฟให้มองครอบอุปกรณ์ทั้งหมด (ทิศเดิมของไฟ) */
      var dir = key.position.clone().sub(key.target.position); if (dir.lengthSq() < 1e-6) dir.set(0.5, 1, 0.6);
      if (STUDIO) dir.set(0.25, 1, 0.6);   /* ไฟนุ่มจากหน้าเฉียงบน (ฝั่งกล้อง) */
      dir.normalize();
      if (key.target.parent == null) scene.add(key.target);
      key.target.position.copy(ctr);
      key.position.copy(ctr).addScaledVector(dir, span * 2);
      var R = span * 0.85, sc = key.shadow.camera;
      sc.left = -R; sc.right = R; sc.top = R; sc.bottom = -R; sc.near = span * 0.2; sc.far = span * 4;
      sc.updateProjectionMatrix();
      key.shadow.bias = -0.0004; key.shadow.normalBias = span * 0.0015;
    }

    /* 2b) ไฟขอบจากด้านหลังเฉียงบน → ขอบวัตถุสว่างเป็นเส้น แยกจากฉากหลัง */
    if (CFG.rim > 0 && st.room !== 'dark' && st.room !== 'dim') {
      var rim = new THREE.DirectionalLight(0xe6eeff, CFG.rim);
      rim.position.set(ctr.x - span * 0.6, ctr.y + span * 1.2, ctr.z - span * 2);
      rim.target.position.copy(ctr); rim.userData.__kpRoom = true;
      scene.add(rim); scene.add(rim.target);
    }

    /* 3) ห้อง: ผนัง + โต๊ะไม้ */
    if (st.room) {
      scene.background = wallTex(DARK);
      /* พื้นสีเรียบของแลปเอง → ลายไม้ */
      if (CFG.table && !STUDIO) B.floors.forEach(function(fl){
        var m = fl.material;
        if (Array.isArray(m) || !litMat(m) || m.map || m.transparent) return;
        var w = wood().clone(); w.needsUpdate = true;
        var fz = new THREE.Box3().setFromObject(fl).getSize(new THREE.Vector3());
        w.repeat.set(Math.max(1, fz.x / (span * 1.6)), Math.max(1, fz.z / (span * 1.6)));
        m.map = w; m.color.setHex(WOODC);
        if (m.isMeshStandardMaterial) { m.roughness = 0.55; m.metalness = 0; }
        m.needsUpdate = true;
      });
      if (CFG.table && STUDIO) {
        /* พื้นสตูดิโอเทา กลืนเข้ากับฉากหลังด้วยหมอกสีเดียวกัน (ไม่เห็นขอบพื้น) */
        var sw = span * 8;
        var sf = new THREE.Mesh(new THREE.PlaneGeometry(sw, sw), new THREE.MeshStandardMaterial({ color: 0x3b3f44, roughness: 0.95, metalness: 0, envMapIntensity: 0.35 }));
        sf.rotation.x = -Math.PI / 2;
        sf.position.set(ctr.x, B.all.min.y - span * 0.004, ctr.z);
        sf.receiveShadow = true; sf.userData.__kpRoom = sf.userData.__kpSeen = true;
        scene.add(sf);
        if (!scene.fog) { scene.fog = new THREE.Fog(0x373a3e, span * 2.2, span * 4.5); scene.fog.__kp = true; scene.fog.__studio = true; }
      } else if (CFG.table) {
        var t = wood(), tw = span * 6;
        t.repeat.set(tw / (span * 1.6), tw / (span * 1.6));
        var tm = new THREE.MeshStandardMaterial({ map: t, color: WOODC, roughness: 0.55, metalness: 0, envMapIntensity: 0.5 });
        var table = new THREE.Mesh(new THREE.PlaneGeometry(tw, tw), tm);
        table.rotation.x = -Math.PI / 2;
        table.position.set(ctr.x, B.all.min.y - span * 0.004, ctr.z);
        table.receiveShadow = true; table.userData.__kpRoom = table.userData.__kpSeen = true;
        scene.add(table);
        if (!scene.fog) { scene.fog = new THREE.Fog(DARK ? 0x14171c : DIM ? 0x30343a : 0xb7babf, span * 2.2, span * 4.5); scene.fog.__kp = true; }
      }
    }
    st.ctr = ctr; st.span = span;
    fogFollow(scene, st, camera);
    fixObjects(scene, st);
    collectPills(scene, st);
  }
  /* หมอกเริ่มหลังตัวอุปกรณ์เสมอ (นับจากกล้อง) → อุปกรณ์คมชัด โต๊ะไกล ๆ ค่อย ๆ จางเข้าผนัง */
  function fogFollow(scene, st, camera){
    var f = scene.fog; if (!f || !f.__kp || !camera || !camera.position) return;
    var d = camera.getWorldPosition ? camera.getWorldPosition(new THREE.Vector3()).distanceTo(st.ctr) : camera.position.distanceTo(st.ctr);
    if (f.__studio) { f.near = d + st.span * 0.5; f.far = d + st.span * 2.4; }
    else { f.near = d + st.span * 1.2; f.far = d + st.span * 4.5; }
  }
  function collectPills(scene, st){
    st.pills = [];
    scene.traverse(function(o){ if (o.isSprite && o.userData.__kpBk) st.pills.push(o.userData.__kpBk); });
  }

  /* สีพื้นหลังสำหรับ shader ที่ trace แสงเอง (แลป 48 49 51 52): [มองลง (โต๊ะ), มองขึ้น (ผนัง)] เป็น GLSL vec3
     คืน null ถ้าไม่มีห้อง → แลปใช้สีเดิมของตัวเอง */
  function shaderBg(){
    if (!CFG.room) return null;
    var h = 'smoothstep(-0.06,0.06,d.y)';   /* ขอบฟ้าคม: มองตรง = ผนัง · มองต่ำ = โต๊ะ */
    if (CFG.room === 'dark') return ['vec3(0.04,0.045,0.055)', 'vec3(0.07,0.08,0.10)', h];
    if (CFG.room === 'dim') return ['vec3(0.30,0.25,0.21)', 'vec3(0.20,0.22,0.25)', h];
    if (CFG.room === 'studio') return ['vec3(0.21,0.22,0.24)', 'vec3(0.23,0.24,0.26)', h];
    return ['vec3(0.62,0.53,0.44)', 'vec3(0.78,0.80,0.83)', h];
  }
  window.KPReal3D = { config: CFG, renderers: renderers, scenes: scenes, shaderBg: shaderBg };
})();
