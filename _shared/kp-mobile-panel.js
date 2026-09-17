/* ═══ KP Science — แผงตั้งค่าแบบเลื่อนขึ้นจากขอบล่าง (จอแคบ ≤ 900 px: โทรศัพท์ / ไอแพดจอเล็ก)
   · ย้ายเนื้อหาแผงขวา (.sim-panel) ไปไว้ในแผ่นเลื่อนขึ้น (#kpSheet) — ย้าย element จริง จึงคง id และ event เดิมทุกอย่าง
   · แถบติดขอบล่าง (#kpMBar): บรรทัด 🧭 ขั้นตอนตอนนี้ + ปุ่ม 👉 ทำขั้นนี้ · ⚙️ ตั้งค่า · 📊 ผล/ตาราง
   · 👉 ทำขั้นนี้: หาปุ่มที่ชื่ออยู่ใน <b>…</b> ของคำแนะนำ แล้วเปิดแผง/เลื่อนไปที่ปุ่มนั้นพร้อมกระพริบ
   · จอกว้าง: คืนเนื้อหากลับแผงขวาตามลำดับเดิม
   ใช้: <script src="../_shared/kp-mobile-panel.js"></script> (ต่อท้ายสคริปต์ของแลป)
   แลปที่ไม่ได้ใช้ .sim-panel: ตั้งค่าก่อนโหลดสคริปต์ เช่น
     <script>window.KP_MPANEL={move:['.side-panel','#manualSection'], res:['.data-section'], view:'#simCanvas', hint:'#hintBox', tab:'#tab-sim', bp:900};</script>
     move = element ที่ย้ายทั้งก้อนเข้าแผง (ตามลำดับ) · res = ส่วนที่นับเป็น "ผล/ตาราง" · view = ภาพหลักที่ต้องเห็นครึ่งบน
     hint = กล่องคำแนะนำ (ถ้ามี) · tab = ส่วนหน้า simulation · bp = ความกว้างสูงสุดที่เปิดใช้
   ตัวเลือกเสริม (opt-in): canvasBtn:true = ปุ่ม ⚙️ ตั้งค่า / 📊 ผล ลอยบนมุมขวาบนของภาพหลัก กดได้ทันทีไม่ต้องเลื่อนจอ
     · btnBar:'#viewBar' = ใส่ปุ่มในแถบเครื่องมือเหนือภาพแทนการลอยทับภาพ (ไม่บังอุปกรณ์)
     · ถ้า bp > 900 และจอกว้างกว่า 900 px แผงจะเลื่อนออกมาจากขอบขวา (drawer) แทนแผ่นจากขอบล่าง ภาพการทดลองจึงเต็มความกว้าง ═══ */
(function(){
  'use strict';
  var CFG = {}, BP = 900;
  var CSS = ''
  + '#kpMBar{position:fixed;left:0;right:0;bottom:0;z-index:960;display:none;background:rgba(8,13,24,.96);border-top:1px solid #1e3a5f;padding:6px 8px calc(7px + env(safe-area-inset-bottom));font-family:IBM Plex Sans Thai Looped,IBM Plex Sans Thai,sans-serif;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}'
  + '#kpMBar .pk{display:flex;gap:8px;align-items:center;margin-bottom:6px;border:1px solid #38bdf8;border-radius:9px;padding:5px 6px 5px 9px;background:rgba(56,189,248,.07)}'
  + '#kpMBar .pk.warn{border-color:#facc15;background:rgba(250,204,21,.08)}#kpMBar .pk.ok{border-color:#34d399;background:rgba(52,211,153,.08)}'
  + '#kpMBar .pk .t{flex:1;font-size:.78rem;line-height:1.35;color:#dbeafe;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;cursor:pointer}'
  + '#kpMBar .pk.warn .t{color:#fef9c3}#kpMBar .pk.ok .t{color:#d1fae5}#kpMBar .pk .t.full{-webkit-line-clamp:unset;display:block}'
  + '#kpMBar .pk .go{flex-shrink:0;border:none;border-radius:8px;background:#f59e0b;color:#111;font:700 .8rem IBM Plex Sans Thai Looped,IBM Plex Sans Thai,sans-serif;padding:8px 10px}'
  + '#kpMBar .tabs{display:flex;gap:6px}'
  + '#kpMBar .tabs button{flex:1;padding:10px 4px;border-radius:10px;border:1px solid #334155;background:#1a2235;color:#e2e8f0;font:700 .92rem IBM Plex Sans Thai Looped,IBM Plex Sans Thai,sans-serif}'
  + '#kpMBar .tabs button.on{background:#38bdf8;border-color:#38bdf8;color:#06090f}'
  + '#kpSheet{position:fixed;left:0;right:0;bottom:0;z-index:950;height:46vh;display:flex;flex-direction:column;background:#0d1424;border-top:2px solid #38bdf8;border-radius:16px 16px 0 0;box-shadow:0 -12px 32px rgba(0,0,0,.6);transform:translateY(110%);transition:transform .25s ease;visibility:hidden}'
  + '#kpSheet.open{transform:none;visibility:visible}#kpSheet.tall{height:84vh}'
  + '#kpSheet .sh{display:flex;align-items:center;gap:8px;padding:4px 10px 6px;border-bottom:1px solid #1e3a5f;font:700 .9rem IBM Plex Sans Thai Looped,IBM Plex Sans Thai,sans-serif;color:#7dd3fc;touch-action:none}'
  + '#kpSheet .sh .grip{position:absolute;left:50%;top:4px;width:46px;height:5px;margin-left:-23px;border-radius:3px;background:#475569}'
  + '#kpSheet .sh .ttl{flex:1;padding-top:8px}'
  + '#kpSheet .sh button{margin-top:8px;border:1px solid #334155;background:#1a2235;color:#e2e8f0;border-radius:8px;padding:6px 10px;font:700 .8rem IBM Plex Sans Thai Looped,IBM Plex Sans Thai,sans-serif}'
  + '#kpSheet .sb{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;padding:10px;display:flex;flex-direction:column;gap:10px}#kpSheet .sb>*{flex-shrink:0;min-width:0}'
  + '.kp-flash{animation:kpFlash 1.1s ease 2}@keyframes kpFlash{0%,100%{box-shadow:0 0 0 0 rgba(250,204,21,0)}50%{box-shadow:0 0 0 4px rgba(250,204,21,.95)}}'
  + 'body.kp-m-on{padding-bottom:var(--kpMBarH,112px)}body.kp-m-on.kp-m-def .sim-panel{display:none!important}body.kp-m-on.kp-m-def .sim-layout{grid-template-columns:minmax(0,1fr)!important}'
  + '#kpSheet.side{left:auto;right:0;top:56px;width:min(390px,92vw);height:auto!important;max-height:none!important;border-top:none;border-left:2px solid #38bdf8;border-radius:16px 0 0 16px;box-shadow:-12px 0 32px rgba(0,0,0,.6);transform:translateX(110%)}#kpSheet.side.open{transform:none}#kpSheet.side [data-a="tall"]{display:none}#kpSheet.side .grip{display:none}'
  + '.kp-vbtns{position:absolute;right:10px;top:10px;z-index:20;display:none;flex-direction:column;gap:6px}body.kp-m-on .kp-vbtns{display:flex}'
  + '.kp-vbtns button{min-width:92px;padding:9px 12px;border-radius:10px;border:1.5px solid rgba(255,255,255,.35);background:rgba(14,116,144,.92);color:#fff;font:700 .9rem IBM Plex Sans Thai Looped,IBM Plex Sans Thai,sans-serif;box-shadow:0 4px 14px rgba(0,0,0,.45);cursor:pointer;touch-action:manipulation}'
  + '.kp-vbtns button.res{background:rgba(51,65,85,.92)}.kp-vbtns button.on{background:#38bdf8;border-color:#38bdf8;color:#06090f}'
  + 'body.kp-m-on .kp-vbtn-host .viewbtns{max-width:calc(100% - 128px)!important}'
  + '.kp-vbtns.inbar{position:static;flex-direction:row;margin-left:auto;flex-shrink:0}.kp-vbtns.inbar button{min-width:0;padding:7px 12px;font-size:.86rem;box-shadow:none}';

  var panel, tab, sheet, sbody, bar, peekBox, peekTxt, goBtn, tabSet, tabRes, ttl, vbtns=null, active=false, slots=[], lastPeek='';

  function $(sel, root){ return (root||document).querySelector(sel); }
  function isRes(el){ if(!el||!el.querySelector) return false;
    if(CFG.res) return CFG.res.some(function(sel){ return el.matches(sel) || !!el.querySelector(sel) || !!el.closest(sel); });
    return !!el.querySelector('.tbl-wrap, table, canvas[id*="raph"], #lastRec, .readout-grid'); }
  function hintEl(){ if(CFG.hint) return $(CFG.hint); return document.getElementById('hint') || document.getElementById('guideBody') || $('.guide'); }
  function sources(){
    if(!CFG.move) return Array.prototype.slice.call(panel.children);
    var out=[]; CFG.move.forEach(function(sel){ Array.prototype.slice.call(document.querySelectorAll(sel)).forEach(function(el){ if(out.indexOf(el)<0 && !out.some(function(o){ return o.contains(el); })) out.push(el); }); });
    return out; }

  function build(){
    var st=document.createElement('style'); st.textContent=CSS; document.head.appendChild(st);
    sheet=document.createElement('div'); sheet.id='kpSheet';
    sheet.innerHTML='<div class="sh"><div class="grip"></div><div class="ttl">⚙️ ตั้งค่าการทดลอง</div><button type="button" data-a="tall">↕ ขยาย</button><button type="button" data-a="close">✕ ปิด</button></div><div class="sb"></div>';
    sbody=$('.sb', sheet); ttl=$('.ttl', sheet);
    tab.appendChild(sheet);   /* อยู่ใน #tab-sim เพื่อให้แถบปุ่มใต้แผนภาพ (kpCbar) ยังหาปุ่มในแผงเจอ */
    bar=document.createElement('div'); bar.id='kpMBar';
    bar.innerHTML='<div class="pk"><div class="t"></div><button type="button" class="go">👉 ทำขั้นนี้</button></div><div class="tabs"><button type="button" data-t="set">⚙️ ตั้งค่า</button><button type="button" data-t="res">📊 ผล / ตาราง</button></div>';
    document.body.appendChild(bar);
    peekBox=$('.pk', bar); peekTxt=$('.pk .t', bar); goBtn=$('.pk .go', bar); tabSet=$('[data-t="set"]', bar); tabRes=$('[data-t="res"]', bar);
    peekTxt.addEventListener('click', function(){ peekTxt.classList.toggle('full'); fitBody(); });
    goBtn.addEventListener('click', doStep);
    tabSet.addEventListener('click', function(){ toggle('set'); });
    tabRes.addEventListener('click', function(){ toggle('res'); });
    /* ปุ่มลอยบนภาพหลัก (opt-in) */
    var inBar= CFG.canvasBtn && CFG.btnBar ? $(CFG.btnBar) : null, host= inBar || (CFG.canvasBtn ? viewEl() : null);
    if(host){ if(!inBar){ if(getComputedStyle(host).position==='static') host.style.position='relative'; host.classList.add('kp-vbtn-host'); }
      vbtns=document.createElement('div'); vbtns.className='kp-vbtns'+(inBar?' inbar':'');
      vbtns.innerHTML='<button type="button" data-t="set">⚙️ ตั้งค่า</button><button type="button" class="res" data-t="res">📊 ผล</button>';
      host.appendChild(vbtns);
      ['set','res'].forEach(function(k){ var b=$('[data-t="'+k+'"]', vbtns); ['mousedown','touchstart','pointerdown'].forEach(function(ev){ b.addEventListener(ev, function(e){ e.stopPropagation(); }, {passive:true}); }); b.addEventListener('click', function(e){ e.stopPropagation(); toggle(k); }); }); }
    $('[data-a="close"]', sheet).addEventListener('click', close);
    $('[data-a="tall"]', sheet).addEventListener('click', function(){ sheet.classList.toggle('tall'); this.textContent= sheet.classList.contains('tall')?'↕ ย่อ':'↕ ขยาย'; });
    /* ปัดแถบหัวลง = ปิด · ปัดขึ้น = ขยาย */
    var y0=null; var sh=$('.sh', sheet);
    sh.addEventListener('touchstart', function(e){ y0=e.touches[0].clientY; }, {passive:true});
    sh.addEventListener('touchend', function(e){ if(y0===null) return; var dy=e.changedTouches[0].clientY-y0; y0=null; if(dy>40){ if(sheet.classList.contains('tall')){ sheet.classList.remove('tall'); $('[data-a="tall"]', sheet).textContent='↕ ขยาย'; } else close(); } else if(dy<-40){ sheet.classList.add('tall'); $('[data-a="tall"]', sheet).textContent='↕ ย่อ'; } });
  }

  function viewEl(){ return (CFG.view&&$(CFG.view))||document.getElementById('view3d')||$('.diag-wrap')||Array.prototype.slice.call(tab.querySelectorAll('canvas')).filter(function(c){ return c.offsetHeight>120 && (!sheet||!sheet.contains(c)); })[0]; }
  function enter(){
    if(active) return; active=true; slots=[];
    sources().forEach(function(el){ var mark=document.createComment('kp-slot'); el.parentNode.insertBefore(mark, el); slots.push([mark, el]); sbody.appendChild(el); });
    tabRes.style.display= Array.prototype.slice.call(sbody.children).some(isRes) ? '' : 'none'; if(vbtns) $('[data-t="res"]', vbtns).style.display=tabRes.style.display;
    document.body.classList.add('kp-m-on'); if(!CFG.move) document.body.classList.add('kp-m-def'); bar.style.display='block'; fitBody();
  }
  function leave(){
    if(!active) return; active=false; close();
    slots.forEach(function(p){ if(p[0].parentNode) { p[0].parentNode.insertBefore(p[1], p[0]); p[0].parentNode.removeChild(p[0]); } }); slots=[];
    document.body.classList.remove('kp-m-on','kp-m-def'); bar.style.display='none';
  }
  function fitBody(){ var h=bar.offsetHeight||112; sheet.classList.toggle('side', BP>900 && window.innerWidth>900); document.body.style.setProperty('--kpMBarH', (h+8)+'px'); sheet.style.bottom=h+'px'; sheet.style.maxHeight='calc(100vh - '+(h+50)+'px)'; }

  function firstOf(kind){ var kids=Array.prototype.slice.call(sbody.children).filter(function(el){ return !el.classList.contains('hidden') && el.offsetHeight>0; }); for(var i=0;i<kids.length;i++){ if((kind==='res')===isRes(kids[i])) return kids[i]; } return kids[0]; }
  function open(kind, target){
    fitBody(); sheet.classList.add('open'); tabSet.classList.toggle('on', kind==='set'); tabRes.classList.toggle('on', kind==='res');
    if(vbtns){ $('[data-t="set"]', vbtns).classList.toggle('on', kind==='set'); $('[data-t="res"]', vbtns).classList.toggle('on', kind==='res'); }
    ttl.textContent= kind==='res' ? '📊 ผลการวัด · ตาราง · กราฟ' : '⚙️ ตั้งค่าการทดลอง';
    var el= target || firstOf(kind);
    requestAnimationFrame(function(){ if(el){ var top=el.getBoundingClientRect().top - sbody.getBoundingClientRect().top + sbody.scrollTop - (target?60:6); sbody.scrollTo({top:Math.max(0,top), behavior:'smooth'}); } });
    if(kind==='res') setTimeout(function(){ window.dispatchEvent(new Event('resize')); }, 60);
    /* ให้ครึ่งบนของจอเห็นภาพการทดลอง */
    var v=viewEl(); if(v){ var r=v.getBoundingClientRect(); if(r.bottom<60 || r.top>window.innerHeight*0.35) window.scrollTo({top:window.scrollY+r.top-60, behavior:'smooth'}); }
  }
  function close(){ sheet.classList.remove('open'); tabSet.classList.remove('on'); tabRes.classList.remove('on'); if(vbtns) Array.prototype.forEach.call(vbtns.children, function(b){ b.classList.remove('on'); }); }
  function toggle(kind){ var on= sheet.classList.contains('open') && (kind==='set'?tabSet:tabRes).classList.contains('on'); if(on) close(); else open(kind); }

  function topIn(el){ while(el && el.parentElement!==sbody) el=el.parentElement; return el; }
  function flash(el){ el.classList.remove('kp-flash'); void el.offsetWidth; el.classList.add('kp-flash'); setTimeout(function(){ el.classList.remove('kp-flash'); }, 2400); }
  function norm(t){ return (t||'').replace(/\s+/g,' ').trim(); }
  function findTarget(){
    var h=hintEl(); if(!h) return null;
    var names=Array.prototype.slice.call(h.querySelectorAll('b, strong')).map(function(b){ return norm(b.textContent).replace(/^["“”'‘’]+|["“”'‘’]+$/g,''); }).filter(function(t){ return t.length>=2; });
    if(!names.length) return null;
    var cands=Array.prototype.slice.call(tab.querySelectorAll('button, label, .mode-btns button, input[type=checkbox]')).filter(function(b){ return !b.closest('#kpMBar') && b.id!=='kpCbar' && !b.closest('.hidden') && !b.disabled; });
    for(var i=0;i<names.length;i++){ var n=names[i];
      for(var j=0;j<cands.length;j++){ var t=norm(cands[j].textContent); if(t && (t===n || t.indexOf(n)===0 || (n.length>=4 && t.indexOf(n)>=0))) return cands[j]; } }
    return null;
  }
  function doStep(){
    var el=findTarget();
    if(!el){ var he=hintEl(); open('set', he && sheet.contains(he) ? (he.closest('.panel-section')||he) : null); return; }
    if(sheet.contains(el)){ var sec=el.closest('.panel-section')||topIn(el); open(isRes(sec)?'res':'set', sec); setTimeout(function(){ el.scrollIntoView({block:'center', behavior:'smooth'}); flash(el); }, 280); }
    else { close(); el.scrollIntoView({block:'center', behavior:'smooth'}); flash(el); }
  }

  function tickPeek(){
    var h=hintEl(); if(!h) { if(peekBox.style.display!=='none'){ peekBox.style.display='none'; fitBody(); } return; }
    /* แผงปิดอยู่ (visibility:hidden) innerText จะว่าง จึงแปลงจาก innerHTML เอง */
    var tmp=document.createElement('div'); tmp.innerHTML=h.innerHTML.replace(/<br\s*\/?>/gi,' · ').replace(/<\/(div|li|p)>/gi,' </$1>');
    var now=tmp.querySelector('.g-now'); if(now){ var bt=now.querySelector('button'); if(bt) bt.remove(); tmp.innerHTML=now.innerHTML; }   /* Lab 61: แสดงเฉพาะขั้นปัจจุบัน */
    var txt=norm(tmp.textContent), cls=(h.className||'').match(/\b(warn|ok)\b/);
    var want= txt?'':'none'; if(peekBox.style.display!==want){ peekBox.style.display=want; fitBody(); } if(!txt){ lastPeek=''; return; }
    if(txt!==lastPeek){ lastPeek=txt; peekTxt.textContent='🧭 '+txt; }
    peekBox.className='pk'+(cls?' '+cls[1]:''); goBtn.style.display= findTarget()?'':'none';
  }
  function tick(){
    var narrow=window.innerWidth<=BP, onSim= tab.classList.contains('tab-section') ? tab.classList.contains('active') : (tab===document.body || tab.offsetHeight>0);
    if(narrow && !active) enter(); else if(!narrow && active) leave();
    if(active){ bar.style.display= onSim?'block':'none'; if(!onSim) close(); else tickPeek(); }
  }
  function init(){
    CFG=window.KP_MPANEL||{}; if(CFG.bp) BP=CFG.bp;
    panel=$('.sim-panel'); tab= CFG.tab ? $(CFG.tab) : document.getElementById('tab-sim'); if(!tab) tab=document.body;
    if(!CFG.move && !panel) return; if(CFG.move && !sources().length) return;
    build(); tick(); fitBody(); setInterval(tick, 300); window.addEventListener('resize', function(){ tick(); if(active) fitBody(); });
    window.__kpMobile={open:open, close:close, doStep:doStep, findTarget:findTarget};
  }
  if(document.readyState==='complete') setTimeout(init, 0); else window.addEventListener('load', init);
})();
