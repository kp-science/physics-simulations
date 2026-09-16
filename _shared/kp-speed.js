/* ═══ KP Speed — ปุ่ม 🐢 ปรับความเร็วการแสดงผลของ simulation ═══
   วิธีทำงาน: ชะลอ "เวลาจำลอง" ที่ simulation ใช้ (timestamp ของ requestAnimationFrame และ performance.now())
   → ภาพช้าลง แต่ฟิสิกส์กับนาฬิกาในแลปใช้เวลาชุดเดียวกัน ค่าที่วัดได้จึงไม่เปลี่ยน
   ไฟล์ที่มีปุ่มความเร็วของตัวเองอยู่แล้ว (Lab 62–78) สคริปต์นี้จะไม่ทำอะไร */
(function(){
  if (window.__kpSpeed) return;
  var STEPS = [1, 0.5, 0.25, 0.1];
  var LABEL = { 1:'ความเร็วปกติ ×1', 0.5:'ช้าลง ×½', 0.25:'ช้าลง ×¼', 0.1:'ช้ามาก ×⅒' };
  var speed = 1;

  /* ── นาฬิกาเสมือน: เดินช้าลงตามอัตราที่เลือก ── */
  var perf = window.performance, rawNow = perf && perf.now ? perf.now.bind(perf) : Date.now;
  var lastReal = rawNow(), virt = lastReal;
  function vnow(){ var r = rawNow(); virt += (r - lastReal) * speed; lastReal = r; return virt; }
  if (perf && perf.now) { try { perf.now = vnow; } catch (e) {} }
  var rawRAF = window.requestAnimationFrame && window.requestAnimationFrame.bind(window);
  if (rawRAF) window.requestAnimationFrame = function(cb){ return rawRAF(function(){ cb(vnow()); }); };

  /* ── ปุ่ม ── */
  function pickHost(){
    var btns = document.querySelectorAll('button'), i, b, oc;
    for (i = 0; i < btns.length; i++) {
      b = btns[i]; oc = b.getAttribute('onclick') || '';
      if (/^\s*setView\(/.test(oc)) return { host: b.parentNode, ref: b };
    }
    var cv = document.querySelector('#view3d, .view3d, #simCanvas, #cv, canvas');
    if (cv) {
      var box = cv.closest('.sim-view, .view3d, .canvas-wrap, .sim-wrap, section, div');
      if (box && box.parentNode) {
        var bar = document.createElement('div');
        bar.className = 'kp-spd-bar';
        bar.style.cssText = 'display:flex;gap:6px;justify-content:flex-end;margin:6px 0 0';
        box.parentNode.insertBefore(bar, box.nextSibling);
        return { host: bar, ref: null };
      }
    }
    return null;
  }
  function style(b){
    if (b.parentNode && b.parentNode.className === 'kp-spd-bar')
      b.style.cssText = 'background:rgba(22,27,39,.92);border:1px solid rgba(255,255,255,.14);color:#e2e8f0;'
        + 'padding:6px 12px;border-radius:8px;font:600 .8rem/1.2 "IBM Plex Sans Thai Looped","IBM Plex Sans Thai",system-ui,sans-serif;cursor:pointer';
  }
  function init(){
    if (typeof window.setSimSpeed === 'function' || document.getElementById('spdBtn')) return true;  /* แลปที่มีปุ่มของตัวเอง */
    var h = pickHost(); if (!h) return false;
    var btn = document.createElement('button');
    btn.id = 'spdBtn'; btn.type = 'button';
    btn.title = 'ปรับความเร็วการแสดงผลให้ช้าลง เพื่อดูการเคลื่อนที่ให้ทัน (ค่าที่เครื่องมือวัดได้ไม่เปลี่ยน)';
    btn.innerHTML = '🐢 ' + LABEL[1];
    btn.addEventListener('click', function(){
      speed = STEPS[(STEPS.indexOf(speed) + 1) % STEPS.length];
      btn.innerHTML = '🐢 ' + LABEL[speed];
      btn.classList.toggle('active', speed !== 1);
    });
    h.host.insertBefore(btn, h.ref); style(btn);
    window.__kpSpeed = { get speed(){ return speed; }, set: function(v){ speed = v; btn.innerHTML = '🐢 ' + (LABEL[v] || ('×' + v)); } };
    return true;
  }
  var tries = 0;
  function boot(){ if (init()) return; if (++tries < 80) setTimeout(boot, 100); }
  if (document.readyState === 'complete') setTimeout(boot, 0);
  else window.addEventListener('load', function(){ setTimeout(boot, 0); });
})();
