# -*- coding: utf-8 -*-
# Lab 38 อัตราเร็วคลื่นในเส้นเชือก — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ทุกตัวเลข = แบบจำลองของแลปเอง (E1–E4: update/loop/toggleTimer/record) · นาฬิกาเสมือน: ดัก requestAnimationFrame
#   แล้วเดินลูปของแลปทีละ dt ด้วยมือ (__adv / __until) — ภาพ 3D ยังวาดทุกเฟรมแต่เวลาจำลองหยุดนิ่งระหว่างถ่าย
# การทดลองที่ 3–4 สุ่ม f, T, μ ตอนกดส่งคลื่น → ตรึงค่าสุ่มเฉพาะ browser ที่ถ่ายภาพ (ภาพตรงข้อความ) · ข้อความบอกช่วงที่สุ่มจริง
GUIDE = {
  'title': 'หาอัตราเร็วคลื่นในเส้นเชือก จากระยะทาง–เวลา และจาก v = fλ แล้ววัดคาบและความถี่',
  'setup': r"""
    window.__q = id => document.getElementById(id);
    window.__sl = (id, v) => { const s = __q(id), vi = __q(id + 'V'); s.value = v; if (vi) vi.value = v; s.dispatchEvent(new Event('input')); };
    /* นาฬิกาเสมือน: เก็บ callback ของ requestAnimationFrame ไว้เอง · เฟรมจริงส่งเวลาเดิม (ฟิสิกส์ไม่เดิน) */
    (function(){ const M = new Map(); let ID = 1e7; const oRAF = window.requestAnimationFrame, oCAF = window.cancelAnimationFrame;
      window.__vt = performance.now();
      window.requestAnimationFrame = cb => { const id = ++ID; M.set(id, cb); return id; };
      window.cancelAnimationFrame = id => { if (M.has(id)) M.delete(id); else oCAF(id); };
      const isR = cb => /renderer\.render/.test(String(cb));
      window.__run = sim => { [...M].forEach(([id, cb]) => { if (sim && isR(cb)) return; M.delete(id); try { cb(__vt); } catch (e) {} }); };
      (function drv(){ oRAF(() => { __run(false); drv(); }); })();
    })();
    window.__adv = (sec, dt) => { dt = dt || 0.005; const n = Math.round(sec / dt); for (let i = 0; i < n; i++) { __vt += dt * 1000; __run(true); } };
    window.__until = (fn, dt, max) => { dt = dt || 0.005; for (let i = 0; i < (max || 20000) && !fn(); i++) { __vt += dt * 1000; __run(true); } };
    window.__fixR = arr => { const o = Math.random; let k = 0; Math.random = () => k < arr.length ? arr[k++] : o(); };
    window.__exp = n => { showExp(n, document.querySelectorAll('.exp-btn')[n - 1]); };
    /* การทดลองที่ 1: ส่งพัลส์ จับเวลาจากขีด a ถึงขีด b แล้ววัด Δx ระหว่างธง START–STOP ด้วยคาลิปเปอร์ */
    window.__p1 = () => { const s = E1.snap(); return s.v * s.t; };
    window.__e1 = (a, b) => { E1.reset(); E1.togglePlay(); __until(() => __p1() >= a); E1.toggleTimer(); __until(() => __p1() >= b); E1.toggleTimer(); E1.togglePlay();
      const s = E1.snap(), c = Caliper.getState('c1'); if (!c.enabled) E1.toggleCaliper(); c.jawA = s.marker1X; c.jawB = s.marker2X;
      __q('e1DxInput').value = Math.abs(c.jawB - c.jawA).toFixed(2); };
    /* การทดลองที่ 2: ยอดคลื่น (A·sin(kx − ωt) = A) ที่อยู่ติดกัน 2 ยอด */
    window.__crest = m => { const s = E2.snap(), v = Math.sqrt(s.T / +__q('e2Mu').value), k = 2 * Math.PI * s.f / v; return (Math.PI / 2 + 2 * Math.PI * s.f * s.t + 2 * Math.PI * m) / k; };
    window.__e2 = f => { E2.reset(); __sl('e2Freq', f); E2.togglePlay(); __adv(1.0); E2.toggleFreeze();
      const lam = Math.sqrt(20 / 0.01) / f; let m = -60; while (__crest(m) < 4) m++;
      const c = Caliper.getState('c2'); if (!c.enabled) E2.toggleCaliper(); c.jawA = __crest(m); c.jawB = __crest(m + 1);
      __q('e2LambdaInput').value = Math.abs(c.jawB - c.jawA).toFixed(2); };
    window.__pr = () => { const s = E3.snap(); return s.points[s.probeIdx] || 0; };
  """,
  'steps': [
   { 'el': ['.exp-nav', '#exp1 .controls-panel'], 'prep': "__exp(1); E1.setMode('manual', document.querySelector('#exp1 .mode-btn')); __sl('gSpeed', 1); __sl('gRopeLen', 30); __q('e1WaveType').value = 'pulse'; __q('e1End').value = 'none'; __sl('e1Tension', 20); __sl('e1Mu', 0.01); E1.reset(); E1.clearTable(); setView('iso'); scrollTo(0,0)",
     'title': 'การทดลองที่ 1: จัดเส้นเชือก',
     'text': 'เลือก <b>1️⃣ วัด v จากระยะทาง</b> และ <b>📝 วัดเอง</b> · เชือกยาว <b>30 m</b> ปลายหนึ่งต่อเครื่องสั่น ปลายอีกด้านต่อตัวดูดซับคลื่น (<b>ไม่มีการสะท้อน</b>) แล้วพาดรอกแขวนตุ้มน้ำหนักให้แรงดึง <b>T = 20 N</b> · เชือกมีมวลต่อความยาว <b>μ = 0.010 kg/m</b> · ชนิดคลื่น <b>พัลส์</b>',
     'out': 'L = 30 m · <b>T</b> = 20 N · <b>μ</b> = 0.010 kg/m' },
   { 'el': ['#e1PlayBtn', '#view3d'], 'prep': "E1.togglePlay(); __adv(0.05); setView('front')",
     'title': 'ส่งพัลส์',
     'text': 'กด <b>▶ ส่งคลื่น</b> เครื่องสั่นกระตุกปลายเชือก 1 ครั้ง เกิด<b>พัลส์</b>เคลื่อนที่ไปทางขวาด้วยอัตราเร็วคงตัว (จุดสีส้ม = ตำแหน่งยอดพัลส์) · ถ้าพัลส์เร็วเกินจะกดทัน ให้ลดความเร็วแสดงผล (⏩) — นาฬิกาจับเวลาช้าลงตามภาพ ค่าที่วัดได้ไม่เปลี่ยน' },
   { 'el': ['#e1TimerBtn', '#view3d'], 'prep': "__until(() => __p1() >= 4); E1.toggleTimer(); __adv(0.01); setView('front')",
     'title': 'เริ่มจับเวลาเมื่อพัลส์ผ่านขีดแรก',
     'text': 'เมื่อยอดพัลส์ผ่านขีด <b>4 m</b> บนสเกล กด <b>⏱ เริ่มจับเวลา</b> · โปรแกรมปักธง <b>START</b> (เขียว) ที่ตำแหน่งพัลส์ขณะกด',
     'out': 'ธง START ที่ x ≈ 4.0 m' },
   { 'el': ['#e1TimerRow', '#view3d'], 'prep': "__until(() => __p1() >= 24); E1.toggleTimer(); E1.togglePlay(); setView('front')",
     'title': 'หยุดเวลาเมื่อพัลส์ผ่านขีดที่สอง',
     'text': 'เมื่อยอดพัลส์ผ่านขีด <b>24 m</b> กด <b>⏹ หยุดเวลา</b> · โปรแกรมปักธง <b>STOP</b> (แดง) และนาฬิกาค้างเวลา Δt ที่พัลส์ใช้เคลื่อนที่ระหว่างธงทั้งสอง',
     'out': '<b>Δt</b> = 0.450 s (อ่านจากนาฬิกา)' },
   { 'el': ['#view3d', '#e1DxInput'], 'prep': "{ const s = E1.snap(), c = Caliper.getState('c1'); if (!c.enabled) E1.toggleCaliper(); c.jawA = s.marker1X; c.jawB = s.marker2X; __q('e1DxInput').value = Math.abs(c.jawB - c.jawA).toFixed(2); } setView('front')",
     'title': 'วัดระยะทาง Δx ระหว่างธง',
     'text': 'กด <b>📐 คาลิปเปอร์</b> แล้วลากเส้นเขียวไปที่ธง START และเส้นแดงไปที่ธง STOP (กด 🔍 ซูมอ่านสเกล ช่วยเล็ง) · อ่าน Δx แล้วกรอกช่อง <b>ระยะทาง Δx</b>',
     'out': 'ธง START ที่ 4.02 m · STOP ที่ 24.15 m → <b>Δx</b> = 20.12 m' },
   { 'el': ['#e1TimerRow', '#e1Tbody', '#e1Readout'], 'prep': "E1.record()",
     'title': 'กดบันทึก → โปรแกรมคำนวณอัตราเร็ว',
     'text': 'กด <b>📥 บันทึก</b> ตารางลง Δt และ Δx แล้วคำนวณ:<br>① อัตราเร็วคลื่นจากการวัด <b>v = Δx/Δt</b><br>② อัตราเร็วตามทฤษฎี <b>v = √(T/μ)</b> (โปรแกรมเปิดเผยค่าหลังบันทึก)<br>③ <b>%Error</b> เทียบสองค่า',
     'out': '<b>v</b> = 20.12 / 0.450 = <b>44.7 m/s</b> · ทฤษฎี √(20/0.010) = 44.72 m/s' },
   { 'el': '#exp1 .data-section', 'prep': "[45, 80].forEach(T => { __sl('e1Tension', T); __e1(4, 24); E1.record(); }); __sl('e1Tension', 80); setView('iso')",
     'title': 'เพิ่มแรงดึง แล้ววัดซ้ำ',
     'text': 'กด <b>↺ รีเซ็ต</b> เพิ่มแรงดึงเป็น <b>T = 45 N</b> และ <b>80 N</b> (μ เท่าเดิม) ส่งพัลส์ จับเวลาจากขีด 4 m ถึง 24 m วัด Δx แล้วบันทึกทุกครั้ง · แรงดึงมาก พัลส์ใช้เวลาน้อยลง',
     'out': 'T = 20 · 45 · 80 N → <b>Δt</b> = 0.450 · 0.300 · 0.225 s → <b>v</b> = 44.7 · 67.1 · 89.4 m/s' },
   { 'el': '#e1Tbody',
     'title': 'วิเคราะห์: อัตราเร็วกับแรงดึง',
     'text': 'แรงดึงเพิ่ม 4 เท่า (20 → 80 N) อัตราเร็วเพิ่ม 2 เท่า (44.7 → 89.4 m/s) → <b>v ∝ √T</b><br>④ คำนวณ <b>v²/T</b> ทุกแถว ได้ค่าคงที่ = 1/μ → <b>μ = T/v²</b>',
     'out': 'v²/T ≈ 100 m/kg ทุกแถว → <b>μ</b> = 0.010 kg/m · สรุป <b>v = √(T/μ)</b>' },
   { 'el': ['#exp2 .cbar', '#view3d'], 'prep': "__exp(2); E2.setMode('manual', document.querySelector('#exp2 .mode-btn')); __sl('e2Tension', 20); __sl('e2Mu', 0.01); __q('e2End').value = 'none'; E2.clearTable(); E2.reset(); __sl('e2Freq', 4); E2.togglePlay(); __adv(1.0); E2.toggleFreeze(); setView('front')",
     'title': 'การทดลองที่ 2: คลื่นต่อเนื่อง แล้วหยุดภาพ',
     'text': 'เลือก <b>2️⃣ วัด v จาก λ</b> ใช้เชือกเดิม (T = 20 N, μ = 0.010 kg/m) ตั้งความถี่ <b>f = 4.0 Hz</b> กด <b>▶ ส่งคลื่น</b> รอจนคลื่นเต็มเชือก แล้วกด <b>⏸ หยุดภาพ</b> คลื่นค้างนิ่งให้วัด',
     'out': 'f = 4.0 Hz → คาบ <b>T = 1/f</b> = 0.250 s' },
   { 'el': ['#view3d', '#e2ManualRow'], 'prep': "{ let m = -60; while (__crest(m) < 4) m++; const c = Caliper.getState('c2'); if (!c.enabled) E2.toggleCaliper(); c.jawA = __crest(m); c.jawB = __crest(m + 1); __q('e2LambdaInput').value = Math.abs(c.jawB - c.jawA).toFixed(2); } setView('front')",
     'title': 'วัดความยาวคลื่นจากยอดคลื่น 2 ยอดที่อยู่ติดกัน',
     'text': 'กด <b>📐 คาลิปเปอร์</b> ลากเส้นเขียวและแดงไปที่<b>ยอดคลื่น 2 ยอดที่อยู่ติดกัน</b> (ซูมอ่านสเกลช่วยเล็งให้ตรงยอด) · ระยะ Δx = ความยาวคลื่น λ กรอกช่อง <b>λ ที่วัดได้</b>',
     'out': '<b>λ</b> = 11.18 m' },
   { 'el': '#exp2 .data-section', 'prep': "E2.record(); [5, 6, 8].forEach(f => { __e2(f); E2.record(); }); setView('front')",
     'title': 'บันทึก แล้วเปลี่ยนความถี่วัดซ้ำ',
     'text': 'กด <b>📥 บันทึก</b> โปรแกรมคำนวณ <b>v = fλ</b> เทียบกับ √(T/μ) · แล้วเปลี่ยนความถี่เป็น <b>5, 6, 8 Hz</b> วัด λ และบันทึกทุกค่า · ความถี่สูงขึ้น ยอดคลื่นถี่ขึ้น λ สั้นลง',
     'out': 'f = 4 · 5 · 6 · 8 Hz → <b>λ</b> = 11.18 · 8.94 · 7.45 · 5.59 m → <b>v = fλ</b> = 44.7 m/s ทุกแถว<br>→ <b>อัตราเร็วคลื่นไม่ขึ้นกับความถี่</b> ขึ้นกับ T และ μ ของเชือกเท่านั้น' },
   { 'el': ['#exp3 .cbar', '#view3d'], 'prep': "__exp(3); E3.setMode('manual', document.querySelector('#exp3 .mode-btn')); E3.clearTable(); E3.reset(); __fixR([0.5, 0.3, 0.4]); E3.togglePlay(); E3.placeProbe(); __adv(0.8); __until(() => __pr() < 0); __until(() => __pr() >= 0); setView('zoom')",
     'title': 'การทดลองที่ 3: วางจุดวัดคาบ',
     'text': 'เลือก <b>3️⃣ วัดคาบ</b> กด <b>▶ ส่งคลื่น</b> (โปรแกรมสุ่มความถี่ 1–6 Hz และแรงดึง ซ่อนความถี่ไว้) แล้วกด <b>📍 วางจุดวัดคาบ</b> จุดสีบนเชือกที่กึ่งกลาง (15 m) <b>เคลื่อนที่ขึ้นลง</b>แบบฮาร์มอนิกอย่างง่าย ไม่เคลื่อนไปตามคลื่น',
     'out': 'จุดบนเชือกสั่นขึ้นลงรอบตำแหน่งสมดุล' },
   { 'el': ['#e3TimerRow', '#view3d'], 'prep': "E3.toggleTimer(); __until(() => +__q('e3Cycles').textContent >= 10); E3.toggleTimer(); setView('zoom')",
     'title': 'จับเวลา 10 รอบ',
     'text': 'กด <b>⏱ เริ่มจับเวลา</b> ตอนจุดเคลื่อนผ่านแนวสมดุลขึ้นข้างบน · โปรแกรมนับรอบให้ (ช่อง <b>รอบ</b>) เมื่อครบ <b>10 รอบ</b> กด <b>⏹ หยุดเวลา</b><br><small>จับหลายรอบแล้วหาร ความคลาดเคลื่อนจากการกดเวลาจะถูกเฉลี่ยลง</small>',
     'out': '10 รอบ ใช้เวลา <b>2.860 s</b>' },
   { 'el': '#exp3 .data-section', 'prep': "E3.record()",
     'title': 'บันทึก → คาบและความถี่',
     'text': 'กด <b>📥 บันทึก</b> โปรแกรมคำนวณ ⑤ <b>คาบ T = เวลา / จำนวนรอบ</b> แล้วเปิดเผยค่าจริง · ความถี่ <b>f = 1/T</b> · ค่า v ที่แสดง ใช้หาความยาวคลื่นได้ <b>λ = v/f</b>',
     'out': '<b>T</b> = 2.860/10 = 0.286 s → <b>f</b> = 1/0.286 ≈ 3.5 Hz · v = 29.7 m/s → λ = v/f ≈ 8.5 m<br><small>(ภาพตัวอย่าง · ความถี่สุ่มใหม่ทุกครั้งที่ส่งคลื่น 1–6 Hz)</small>' },
   { 'el': ['#exp4 .controls-panel', '#e4TimerRow', '#view3d'], 'prep': "__exp(4); E4.setMode('manual', document.querySelector('#exp4 .mode-btn')); E4.clearTable(); E4.reset(); __sl('e4TimeLim', 10); __fixR([0.26, 0.5, 0.25]); E4.togglePlay(); E4.placeRef(); __adv(1.0, 0.01); E4.toggleTimer(); __until(() => E4.snap().wavesStopped, 0.01); __q('e4CycleInput').value = __q('e4Cycles').textContent; setView('front')",
     'title': 'การทดลองที่ 4: นับรอบในเวลาที่กำหนด',
     'text': 'เลือก <b>4️⃣ วัดความถี่</b> กด <b>▶ ส่งคลื่น</b> และ <b>📍 วางเส้นอ้างอิง</b> · ตั้ง<b>เวลาจับ 10 s</b> แล้วกด <b>⏱ เริ่มจับเวลา</b> · ทุกครั้งที่เฟสเดิมผ่านเส้นอ้างอิง เส้นจะกระพริบสีเหลือง ให้นับ 1 รอบ · หมดเวลาคลื่นหยุด จุดสีเหลืองบอกตำแหน่งเฟสเดียวกับจุด START · กรอกจำนวนรอบที่นับได้',
     'out': 'เวลา 10.0 s นับได้ <b>23 รอบ</b>' },
   { 'el': '#exp4 .data-section', 'prep': "E4.record()",
     'title': 'บันทึก → ความถี่',
     'text': 'กด <b>📥 บันทึก</b> โปรแกรมคำนวณ ⑥ <b>f = จำนวนรอบ / เวลา</b> และ <b>T = 1/f</b> แล้วเปิดเผยความถี่จริง · ยิ่งจับเวลานาน นับรอบได้มาก f ยิ่งแม่น',
     'out': '<b>f</b> = 23/10.0 = <b>2.3 Hz</b> · T = 0.435 s<br><small>(ภาพตัวอย่าง · ความถี่สุ่มใหม่ทุกครั้ง 1–6 Hz)</small> · สรุปทั้งแลป: <b>v = √(T/μ) = fλ</b> ไม่ขึ้นกับความถี่' },
  ],
 }
