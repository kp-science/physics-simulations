/* ═══ KP Lab Mode — โหมดสอนทำแลป + ล็อกโหมดอัตโนมัติสำหรับสมาชิก ═══
   โหลดท้ายหน้าแลป (หลัง kp-auth.js)

   1) ล็อกโหมดอัตโนมัติ: ปุ่มที่เรียก setMode('auto') / setRecMode('auto') ฯลฯ
      ผู้ที่ยังไม่ล็อกอิน → ขึ้นหน้าต่างชวนสมัครสมาชิกฟรี · ล็อกอินแล้วเข้าโหมดอัตโนมัติให้ต่อทันที

   2) โหมดสอนทำแลป: แลปที่กำหนด window.KP_TUTOR = { title, steps:[...] } ไว้ก่อนโหลดสคริปต์นี้
      จะมีปุ่ม "🎓 โหมดสอน" ใต้ปุ่มเลือกโหมด → ไฮไลต์ทีละขั้น ผู้เรียนต้องกดตามลำดับ
      step = {
        el:   'css selector' | () => Element   (ไม่ใส่ = กล่องข้อความกลางจอ มีปุ่ม "ถัดไป")
        text: 'ข้อความ (HTML)',
        done: () => boolean      (ไม่ใส่ = ผ่านเมื่อกดเป้าหมาย)
        free: true               (ปล่อยให้คลิกที่อื่นได้ เช่น ขั้นที่ต้องลากแถบเลื่อน/หมุนมุมมอง)
        dim:  false              (ไม่ทำให้ส่วนอื่นมืด — ขั้นที่ต้องดูภาพจำลองไปพร้อมกัน)
        start: () => {}          (เรียกตอนเข้าขั้นนี้)
        finish: () => {}         (เรียกตอนผ่านขั้นนี้ — เช่น กรอกค่าลงใบบันทึกให้)
      KP_TUTOR.onStart: () => {} (เรียกก่อนเริ่ม — เช่น รีเซตแลป)
      } */
(function(){
  if (window.KPLabMode) return;
  var AUTO_RE = /\b\w*Mode\w*\(\s*['"]auto['"]/;

  /* ── สมาชิก = ล็อกอินแล้ว และไม่ถูกบล็อก ── */
  function user(){ try { return (typeof currentUser !== 'undefined') ? currentUser : null; } catch (e) { return null; } }
  function isMember(){
    var u = user(); if (!u) return false;
    try { if (typeof currentUserData !== 'undefined' && currentUserData && currentUserData.role === 'blocked') return false; } catch (e) {}
    return true;
  }

  var CSS = '' +
    '.kplm-lock{font-size:.7em;margin-left:4px;opacity:.85}' +
    '#kplm-gate{position:fixed;inset:0;z-index:9998;background:rgba(2,6,14,.72);display:none;align-items:center;justify-content:center;padding:16px}' +
    '#kplm-gate.open{display:flex}' +
    '#kplm-gate .box{background:#0d1421;border:1px solid rgba(56,189,248,.35);border-radius:16px;max-width:400px;width:100%;padding:22px 22px 18px;color:#e2e8f0;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.5);font-family:"IBM Plex Sans Thai Looped","IBM Plex Sans Thai",system-ui,sans-serif}' +
    '#kplm-gate h3{margin:4px 0 8px;font-size:1.1rem}' +
    '#kplm-gate p{margin:0 0 16px;font-size:.88rem;line-height:1.6;color:#94a3b8}' +
    '#kplm-gate .row{display:flex;gap:8px;flex-wrap:wrap}' +
    '#kplm-gate button{flex:1;min-width:120px;padding:10px 12px;border-radius:9px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#e2e8f0;font:600 .9rem/1.2 inherit;cursor:pointer}' +
    '#kplm-gate button.pri{background:#38bdf8;border-color:#38bdf8;color:#06090f}' +
    '#kplm-gate .later{margin-top:10px;background:none;border:none;color:#7c8fa6;font-size:.8rem;flex:none;min-width:0}' +
    '.kplm-tbtn{width:100%;margin-top:8px;padding:8px 10px;border-radius:9px;border:1px dashed rgba(250,204,21,.55);background:rgba(250,204,21,.08);color:#fde68a;font:600 .85rem/1.3 "IBM Plex Sans Thai Looped","IBM Plex Sans Thai",system-ui,sans-serif;cursor:pointer}' +
    '.kplm-tbtn:hover{background:rgba(250,204,21,.16)}' +
    '#kplm-spot{position:fixed;z-index:9990;pointer-events:none;border-radius:10px;border:3px solid #facc15;box-shadow:0 0 0 9999px rgba(2,6,14,.6),0 0 18px 4px rgba(250,204,21,.65);transition:all .25s ease;animation:kplmPulse 1.3s ease-in-out infinite}' +
    '#kplm-spot.nodim{box-shadow:0 0 18px 4px rgba(250,204,21,.65);animation:kplmPulse2 1.3s ease-in-out infinite}' +
    '@keyframes kplmPulse2{50%{box-shadow:0 0 28px 9px rgba(250,204,21,.9)}}' +
    '#kplm-spot.none{border:none;animation:none;box-shadow:0 0 0 9999px rgba(2,6,14,.6)}' +
    '@keyframes kplmPulse{50%{box-shadow:0 0 0 9999px rgba(2,6,14,.6),0 0 28px 9px rgba(250,204,21,.9)}}' +
    '#kplm-tip{position:fixed;z-index:9995;max-width:340px;background:#fefce8;color:#1c1917;border-radius:12px;padding:12px 14px 10px;box-shadow:0 12px 34px rgba(0,0,0,.45);font:500 1rem/1.55 "IBM Plex Sans Thai Looped","IBM Plex Sans Thai",system-ui,sans-serif;transition:top .25s,left .25s}' +
    '#kplm-tip small{display:block;margin-top:2px;font-size:.8rem;color:#57534e;line-height:1.45}' +
    '#kplm-tip .hd{display:flex;align-items:center;gap:8px;margin-bottom:4px;font-size:.74rem;font-weight:700;color:#a16207}' +
    '#kplm-tip .hd .x{margin-left:auto;background:none;border:none;color:#78716c;font-size:.78rem;cursor:pointer;font-family:inherit}' +
    '#kplm-tip .bar{height:4px;border-radius:2px;background:#fde68a;margin-bottom:8px;overflow:hidden}' +
    '#kplm-tip .bar i{display:block;height:100%;background:#ca8a04;transition:width .3s}' +
    '#kplm-tip .nx{margin-top:8px;padding:6px 14px;border-radius:8px;border:none;background:#ca8a04;color:#fff;font:700 .85rem/1.2 inherit;cursor:pointer}' +
    '#kplm-tip.shake{animation:kplmShake .35s}' +
    '@keyframes kplmShake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}' +
    '#kplm-tip .warn{display:none;margin-top:6px;font-size:.78rem;color:#b91c1c;font-weight:600}' +
    '#kplm-tip.shake .warn{display:block}' +
    '#kplm-tip .skip{display:none;margin-top:8px;background:none;border:none;padding:0;color:#a16207;font:600 .78rem/1.3 inherit;text-decoration:underline;cursor:pointer}' +
    '#kplm-tip.stuck .skip{display:block}' +
    '@media(max-width:640px){#kplm-tip{left:10px!important;right:10px;bottom:10px;top:auto!important;max-width:none}' +
    '#kplm-tip.attop{top:10px!important;bottom:auto}}';
  function addCSS(){ if (document.getElementById('kplm-css')) return; var s = document.createElement('style'); s.id = 'kplm-css'; s.textContent = CSS; document.head.appendChild(s); }

  /* ═════════ 1) ล็อกโหมดอัตโนมัติ ═════════ */
  var gate = null, pending = null;
  function autoButtons(){
    var out = [];
    document.querySelectorAll('[onclick]').forEach(function(b){ if (AUTO_RE.test(b.getAttribute('onclick') || '')) out.push(b); });
    /* แลปที่ปุ่มอัตโนมัติเขียนแบบอื่น (14 30 31 39 40 42) — ป้าย 🔒 ติดที่ตัวที่ผู้ใช้เห็น */
    document.querySelectorAll(ALT_SEL).forEach(function(b){ out.push(b); });
    ['label[for="mAuto"]', '#rec-label-auto'].forEach(function(q){ var x = document.querySelector(q); if (x) out.push(x); });
    return out;
  }
  /* ปุ่ม/สวิตช์อัตโนมัติแบบอื่น: data-mode="auto" (39 40) · data-rec="auto" (42) · วิทยุ #mAuto (14) · สวิตช์ #rec-toggle (30 31) */
  var ALT_SEL = '[data-mode="auto"],[data-rec="auto"]';
  function autoTarget(t){
    if (!t || !t.closest) return null;
    var b = t.closest('[onclick]');
    if (b && AUTO_RE.test(b.getAttribute('onclick') || '')) return b;
    b = t.closest(ALT_SEL); if (b) return b;
    b = t.closest('#mAuto,label[for="mAuto"]'); if (b) return document.getElementById('mAuto');
    b = t.closest('#rec-toggle,label.switch');
    if (b) { var tg = document.getElementById('rec-toggle');
      /* คลิกที่ช่องติ๊กเอง: สถานะสลับไปก่อน event ถึงเรา → checked = กำลังเปิด · คลิกที่ป้าย: ยังไม่สลับ → !checked = กำลังเปิด */
      if (tg && b === tg && tg.checked) return tg;
      if (tg && b !== tg && b.contains(tg) && !tg.checked) return tg; }
    return null;
  }
  /* กลับเป็นโหมดวัดค่าเอง (ตอนออกจากระบบ) */
  function toManual(){
    try { if (typeof mode !== 'undefined' && mode === 'auto' && typeof setMode === 'function') setMode('manual'); } catch (e) {}
    ['[data-mode="manual"]', '[data-rec="manual"]', '#mManual'].forEach(function(q){
      var x = document.querySelector(q), a = document.querySelector(q.replace('manual', 'auto').replace('#mManual', '#mAuto'));
      if (x && a && (a.classList.contains('active') || a.checked)) x.click();
    });
    var tg = document.getElementById('rec-toggle'); if (tg && tg.checked) tg.click();
  }
  function paintLocks(){
    var m = isMember();
    autoButtons().forEach(function(b){
      var l = b.querySelector('.kplm-lock');
      if (!m && !l) { l = document.createElement('span'); l.className = 'kplm-lock'; l.textContent = '🔒'; b.appendChild(l); b.title = 'โหมดอัตโนมัติสำหรับสมาชิก (สมัครฟรี)'; }
      if (m && l) { l.remove(); b.removeAttribute('title'); }
    });
  }
  function openGate(btn){
    pending = btn;
    if (!gate) {
      gate = document.createElement('div'); gate.id = 'kplm-gate';
      gate.innerHTML = '<div class="box"><div style="font-size:2rem">🔒⚡</div><h3>โหมดอัตโนมัติสำหรับสมาชิก</h3>' +
        '<p>สมัครสมาชิก <b style="color:#e2e8f0">ฟรี</b> เพื่อเปิดโหมดอัตโนมัติ — ดูค่าที่คำนวณได้ทันที ตรวจคำตอบ และสร้างกราฟอัตโนมัติ<br>โหมด <b style="color:#e2e8f0">วัดค่าเอง</b> และ <b style="color:#e2e8f0">🎓 โหมดสอน</b> ใช้ได้เลยไม่ต้องสมัคร</p>' +
        '<div class="row"><button class="pri" data-a="register">สมัครสมาชิกฟรี</button><button data-a="login">เข้าสู่ระบบ</button></div>' +
        '<button class="later" data-a="close">ไว้ก่อน</button></div>';
      gate.addEventListener('click', function(e){
        var a = e.target.getAttribute && e.target.getAttribute('data-a');
        if (e.target === gate || a === 'close') { gate.classList.remove('open'); pending = null; return; }
        if (a === 'register' || a === 'login') {
          gate.classList.remove('open');
          if (typeof showModal === 'function') showModal(a);
          else { var k = document.querySelector('script[src*="kp-auth.js"]'); location.href = (k ? k.getAttribute('src').replace(/kp-auth\.js.*$/, '') : '/') + 'index.html'; }
        }
      });
      document.body.appendChild(gate);
    }
    gate.classList.add('open');
  }
  document.addEventListener('click', function(e){
    var b = autoTarget(e.target);
    if (!b) return;
    if (isMember()) return;
    e.preventDefault(); e.stopImmediatePropagation();
    openGate(b);
  }, true);

  /* เฝ้าสถานะล็อกอิน: เปลี่ยน 🔒 และถ้าเพิ่งล็อกอินหลังกดปุ่มอัตโนมัติ → เข้าโหมดให้เลย */
  var lastM = null;
  setInterval(function(){
    var m = isMember();
    if (m !== lastM) {
      lastM = m; paintLocks();
      /* ออกจากระบบขณะอยู่ในโหมดอัตโนมัติ → กลับเป็นวัดค่าเอง */
      if (!m) toManual();
      if (m && pending) { var b = pending; pending = null; setTimeout(function(){ b.click(); }, 150); }
    }
  }, 600);

  /* ═════════ 2) โหมดสอนทำแลป ═════════ */
  var T = null;   /* สถานะการสอนที่กำลังเล่น */
  function $el(s){ if (!s) return null; try { return typeof s === 'function' ? s() : document.querySelector(s); } catch (e) { return null; } }

  function tutorButton(){
    var cfg = window.KP_TUTOR; if (!cfg || !cfg.steps || !cfg.steps.length) return;
    if (document.querySelector('.kplm-tbtn')) return;
    var anchor = cfg.after ? $el(cfg.after) : null;
    if (!anchor) { var man = document.querySelector('[onclick^="setMode(\'manual\'"]'); anchor = man && man.parentNode; }
    if (!anchor) return;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'kplm-tbtn';
    b.innerHTML = '🎓 โหมดสอนทำแลป — พาทำทีละขั้น';
    b.addEventListener('click', function(){ start(); });
    anchor.parentNode.insertBefore(b, anchor.nextSibling);
  }

  function start(){
    var cfg = window.KP_TUTOR; if (!cfg) return;
    stop();
    try { if (typeof setMode === 'function' && typeof mode !== 'undefined' && mode === 'auto') setMode('manual'); } catch (e) {}
    if (cfg.onStart) try { cfg.onStart(); } catch (e) {}
    T = { cfg: cfg, i: -1, spot: document.createElement('div'), tip: document.createElement('div'), raf: 0, poll: 0 };
    T.spot.id = 'kplm-spot'; T.tip.id = 'kplm-tip';
    document.body.appendChild(T.spot); document.body.appendChild(T.tip);
    T.tip.addEventListener('click', function(e){
      var a = e.target.getAttribute('data-a');
      if (a === 'next') next();
      if (a === 'quit') stop();
      if (a === 'skip') next();
    });
    document.addEventListener('click', guard, true);
    document.addEventListener('pointerdown', guard, true);
    document.addEventListener('keydown', esc, true);
    next();
    T.poll = setInterval(check, 200);
    (function loop(){ if (!T) return; place(); T.raf = requestAnimationFrame(loop); })();
  }
  function stop(){
    if (!T) return;
    clearInterval(T.poll); cancelAnimationFrame(T.raf);
    T.spot.remove(); T.tip.remove();
    document.removeEventListener('click', guard, true);
    document.removeEventListener('pointerdown', guard, true);
    document.removeEventListener('keydown', esc, true);
    T = null;
  }
  function esc(e){ if (e.key === 'Escape') stop(); }
  function step(){ return T && T.cfg.steps[T.i]; }

  function next(){
    if (!T) return;
    var prev = step(); if (prev && prev.finish) try { prev.finish(); } catch (e) {}
    T.i++;
    var s = step();
    if (!s) { stop(); return; }
    if (s.start) try { s.start(); } catch (e) {}
    T.clicked = false;
    var el = $el(s.el);
    if (reveal(el)) {} else if (el && el.scrollIntoView) {
      var r = el.getBoundingClientRect();
      if (r.top < 70 || r.bottom > innerHeight - 20) {
        var tall = r.height > innerHeight * 0.55;
        window.scrollBy({ top: tall ? r.top - 80 : r.top + r.height / 2 - innerHeight / 2, behavior: document.hidden ? 'auto' : 'smooth' });
      }
    }
    var all = T.cfg.steps, n = all.length, last = T.i === n - 1;
    var acts = all.filter(function(x){ return x.el; }).length, k = all.slice(0, T.i + 1).filter(function(x){ return x.el; }).length;
    var lbl = s.el ? 'ขั้น ' + k + '/' + acts : (last ? 'เสร็จแล้ว ✓' : '');
    T.tip.className = '';   /* ล้าง shake / stuck */
    T.tip.innerHTML = '<div class="hd">🎓 ' + (T.cfg.title || 'โหมดสอน') + (lbl ? ' · ' + lbl : '') +
      '<button class="x" data-a="quit">ออกจากโหมดสอน ✕</button></div><div class="bar"><i style="width:' + Math.round((last ? acts : k) / Math.max(1, acts) * 100) + '%"></i></div>' +
      '<div>' + s.text + '</div>' +
      (!s.el ? '<button class="nx" data-a="next">' + (last ? 'จบ ✓' : (T.i === 0 ? 'เริ่มเลย ▶' : 'ถัดไป ▶')) + '</button>' : '') +
      '<div class="warn">👆 กดที่กรอบสีเหลืองก่อนนะ</div>' +
      (s.el && !last ? '<button class="skip" data-a="skip">ติดอยู่? ข้ามขั้นนี้ ▶</button>' : '');
    T.t0 = Date.now();
    place(true);
  }
  /* จอมือถือ: เป้าหมายอยู่ในแผ่น ⚙️ ตั้งค่า ที่เลื่อนขึ้นจากขอบล่าง (kp-mobile-panel.js) → เปิดแผ่นแล้วเลื่อนไปหาเป้าหมาย */
  function reveal(el){
    var sh = document.getElementById('kpSheet');
    if (!el || !sh || !sh.contains(el)) return false;
    if (!sh.classList.contains('open')) {
      var b = document.querySelector('#kpMBar [data-t="set"]');
      if (b) { T.opening = true; b.click(); T.opening = false; }
    }
    setTimeout(function(){ try { el.scrollIntoView({ block: 'center' }); } catch (e) {} }, 320);
    return true;
  }
  function check(){
    var s = step(); if (!s || !s.el || T.adv) return;
    /* ค้างขั้นเดิมนาน → แสดงปุ่มข้าม (กันผู้เรียนติด เช่น อ่านค่าผิดเกินเกณฑ์) */
    if (Date.now() - T.t0 > 25000 && !T.tip.classList.contains('stuck')) { T.tip.classList.add('stuck'); place(); }
    var ok = false;
    if (s.done) { try { ok = !!s.done(); } catch (e) {} }
    else ok = T.clicked;
    if (ok) { T.adv = true; setTimeout(function(){ if (!T) return; T.adv = false; next(); }, 300); }
  }
  /* อนุญาตให้คลิกเฉพาะเป้าหมาย / กล่องข้อความ / แถบบนสุด */
  function guard(e){
    var s = step(); if (!s || T.opening) return;
    if (T.tip.contains(e.target)) return;
    var el = $el(s.el);
    if (el && el.contains(e.target)) { if (e.type === 'click' && T.clicked === false) T.clicked = true; return; }
    if (s.free) return;
    if (e.target.closest && e.target.closest('.kp-topbar,#kp-auth-modal,#kpMBar .tabs,.kp-vbtns')) return;
    /* ภาพ 3D หมุน/ซูม/เลื่อนได้เสมอ แม้อยู่ในโหมดสอน */
    if (window.KPReal3D && KPReal3D.renderers.some(function(r){ return r.domElement === e.target; })) return;
    e.preventDefault(); e.stopImmediatePropagation();
    if (e.type === 'pointerdown') { T.tip.classList.remove('shake'); void T.tip.offsetWidth; T.tip.classList.add('shake'); }
  }
  function place(){
    var s = step(); if (!s) return;
    var el = $el(s.el), sp = T.spot, tp = T.tip, pad = 6;
    if (!el || !el.getClientRects().length) {
      sp.className = 'none'; sp.style.cssText = 'left:50%;top:50%;width:2px;height:2px';
      tp.style.left = Math.max(10, (innerWidth - tp.offsetWidth) / 2) + 'px'; tp.style.top = Math.max(10, (innerHeight - tp.offsetHeight) / 2) + 'px';
      return;
    }
    var r = el.getBoundingClientRect();
    sp.className = s.dim === false ? 'nodim' : '';
    sp.style.left = (r.left - pad) + 'px'; sp.style.top = (r.top - pad) + 'px';
    sp.style.width = (r.width + pad * 2) + 'px'; sp.style.height = (r.height + pad * 2) + 'px';
    /* กล่องข้อความ: ใต้เป้าหมาย ถ้าไม่พอไว้ด้านบน ถ้าเป้าหมายสูงมากไว้ด้านซ้าย/ขวา */
    var w = tp.offsetWidth, h = tp.offsetHeight, x, y;
    if (r.height > innerHeight * 0.45) {
      x = r.left - w - 16 > 10 ? r.left - w - 16 : Math.min(innerWidth - w - 10, r.right + 16);
      y = Math.min(Math.max(10, r.top + 20), innerHeight - h - 10);
    } else {
      x = Math.min(Math.max(10, r.left + r.width / 2 - w / 2), innerWidth - w - 10);
      y = r.bottom + 14 + h < innerHeight ? r.bottom + 14 : Math.max(10, r.top - h - 14);
    }
    tp.style.left = x + 'px'; tp.style.top = y + 'px';
    /* จอมือถือ กล่องข้อความติดล่างจอ → ถ้าเป้าหมายอยู่ช่วงล่าง (เช่นแผงควบคุมล่าง) ย้ายกล่องขึ้นบนจอ */
    tp.classList.toggle('attop', innerWidth <= 640 && r.bottom > innerHeight - h - 24);
  }

  function init(){ addCSS(); paintLocks(); tutorButton(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();

  window.KPLabMode = { start: start, stop: stop, isMember: isMember, refresh: paintLocks };
})();
