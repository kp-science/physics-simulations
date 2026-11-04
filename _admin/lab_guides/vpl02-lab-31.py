# -*- coding: utf-8 -*-
# Lab 31 ถังคลื่น — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ทุกตัวเลข = แบบจำลองของแลปเอง (computeSpeed/computePhysics/labField) · หยุดนาฬิกาแลป (__kpSpeed.set(0)) แล้วตั้งเวลา t เอง
# หมุดวัดปักที่ "แถบสว่าง" = สันคลื่นจริงของสนามคลื่น labField (หาเฟสจากสูตรในแลป) เหมือนนักเรียนแตะกลางแถบสว่าง
GUIDE = {
  'title': 'หาความยาวคลื่นและอัตราเร็วคลื่นน้ำในถังคลื่น',
  'setup': r"""
    if (window.__kpSpeed) { __kpSpeed.set(0); const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    window.__q = id => document.getElementById(id);
    window.__sl = (id, v) => { const s = __q(id); s.value = v; s.dispatchEvent(new Event('input')); const vi = __q(id.replace('sl-', 'vi-')); if (vi) vi.value = v; };
    window.__btn = (sel, k) => [...document.querySelectorAll(sel + ' button')].find(b => b.getAttribute('onclick').includes("'" + k + "'"));
    window.__T = 0.02;   /* เวลาที่ใช้ถ่ายภาพ (s) */
    window.__setT = s => { t = s; strobeDisplayTime = s; lastStrobeFlash = s; draw(); updateReadout(); };
    /* ตำแหน่งสันคลื่น (แถบสว่าง) บนเส้นกลางถาด: เฟสของ labField = π/2 */
    window.__crest = (n, region) => { computePhysics(); const wt = 2 * Math.PI * frequency * t, kd = 2 * Math.PI / wavelengthDeep, ks = 2 * Math.PI / wavelengthShallow;
      const u0 = waveShape === 'plane' ? RT.PLANE_U0 : RT.SRC_U;
      if (region === 's') { const pB = kd * (GLASS_U - u0); const m = Math.ceil((pB - wt - Math.PI / 2) / (2 * Math.PI)); return GLASS_U + (Math.PI / 2 + wt + 2 * Math.PI * (m + n) - pB) / ks; }
      return u0 + (Math.PI / 2 + wt + 2 * Math.PI * n) / kd; };
    window.__pin = (a, b) => { markers = [{ x: +a.toFixed(2), y: RT.SRC_W }, { x: +b.toFixed(2), y: RT.SRC_W }]; updateMeasureDisplay(); draw(); };
  """,
  'steps': [
   { 'el': ['#view3d', '#exp-modes'], 'prep': "if (__q('rec-toggle').checked) { __q('rec-toggle').checked = false; toggleRecMode(); } setExpMode('strobe', __btn('#exp-modes', 'strobe')); setWaveShape('circular', __btn('#wave-shapes', 'circular')); resetSim(); clearTable(); __setT(__T); setView('iso'); scrollTo(0,0)",
     'title': 'จัดถังคลื่น',
     'text': 'เลือกการทดลอง <b>I. Stroboscope</b> และ <b>📏 วัดค่าเอง</b> · ถาดก้นแก้วใส่น้ำลึก <b>10 mm</b> ระดับเรียบ มีหลอดไฟอยู่เหนือถาด แสงผ่านผิวน้ำไปตกบน<b>กระดาษขาวใต้ถาด</b> · ตัวทำคลื่น (ลูกปัดจุ่มน้ำ) ต่อกับแหล่งจ่ายไฟที่ตั้งความถี่ได้',
     'out': 'ความลึกน้ำ h = 10 mm' },
   { 'el': ['#playBtn', '#view3d'], 'prep': "togglePlay(); __setT(__T); setView('top')",
     'title': 'เปิดเครื่องกำเนิดคลื่น',
     'text': 'กด <b>▶ เริ่ม</b> ลูกปัดจุ่มน้ำเป็นจังหวะ เกิด<b>คลื่นวงกลม</b>แผ่ออกจากจุดเดียว · กด <b>🌊 มองผิวน้ำ</b> ดูสันคลื่น (นูน) สลับกับท้องคลื่น (เว้า) · บนกระดาษ สันคลื่นรวมแสงเป็น<b>แถบสว่าง</b> ท้องคลื่นเป็นแถบมืด',
     'out': 'หน้าคลื่นเป็นวงกลม → คลื่นมีอัตราเร็วเท่ากันทุกทิศ' },
   { 'el': ['#sec-strobe', '#view3d'], 'prep': "__q('strobe-toggle').checked = true; toggleStrobe(); __sl('sl-strobe', 8); __setT(__T); setView('iso')",
     'title': 'ใช้สโตรโบสโคปทำให้คลื่นหยุดนิ่ง',
     'text': 'เปิดสวิตช์ <b>เปิดสโตรโบสโคป</b> มองคลื่นผ่านช่องของจานหมุน (6 ช่อง) · เพิ่ม <b>N</b> (ช่องต่อวินาที) ทีละน้อย จนแถบคลื่น<b>หยุดนิ่ง</b> · ค่า N <b>สูงสุด</b>ที่คลื่นนิ่งโดยแถบสว่าง<b>ไม่ถี่ขึ้น</b> = ความถี่ของคลื่น (ที่ N = 4 ก็นิ่ง เพราะเห็นทุก 2 รอบ)<br><small>N = 8 ช่อง/s ↔ จานหมุน 8/6 รอบ/s = 20 รอบ/15 วินาที</small>',
     'out': 'คลื่นนิ่งที่ <b>N = 8 ช่อง/s</b> → <b>f = 8 Hz</b>' },
   { 'el': ['#view3d', '#sec-measure'], 'prep': "__pin(__crest(2), __crest(3)); setView('read')",
     'title': 'ปักหมุดบนแถบสว่าง 2 แถบที่อยู่ติดกัน',
     'text': 'กด <b>🔍 ซูมอ่านภาพบนกระดาษ</b> แล้วแตะ<b>กลางแถบสว่าง</b> 2 แถบที่อยู่ติดกัน ได้หมุด ① และ ② (ลากหมุดปรับให้ตรงกลางแถบ) · ระยะระหว่างหมุดแสดงในแถบวัดใต้ภาพ',
     'out': '<b>λ</b> = ระยะระหว่างแถบสว่างที่อยู่ติดกัน ≈ 3.13 cm' },
   { 'el': '#data-table-container', 'prep': "recordMeasurement(); setView('iso')",
     'title': 'บันทึก แล้วคำนวณอัตราเร็ว',
     'text': 'กด <b>💾 บันทึก</b> ตารางลง N และ λ ให้<br>① ความถี่ <b>f = N</b> (ค่า N สูงสุดที่คลื่นนิ่ง)<br>② อัตราเร็วคลื่น <b>v = fλ</b>',
     'out': 'N = 8 · λ = 3.1 cm → <b>v</b> = 8 × 3.13 ≈ 25 cm/s' },
   { 'el': ['#sec-strobe', '#view3d'], 'prep': "__sl('sl-strobe', 16); __setT(__T); { const h = wavelengthDeep / 2; __pin(__crest(2) - h, __crest(2)); } setView('read')",
     'title': 'หมุนสโตรโบสโคปเร็วขึ้น 2 เท่า',
     'text': 'เพิ่ม <b>N เป็น 16 ช่อง/s</b> (2 เท่าของความถี่) คลื่นหยุดนิ่งอีกครั้ง แต่<b>แถบสว่างถี่ขึ้น 2 เท่า</b> · ช่องเปิดแต่ละครั้ง คลื่นเลื่อนไปเพียง λ/2 ตาเห็นภาพ 2 จังหวะซ้อนกัน · ปักหมุดบนแถบสว่าง 2 แถบที่อยู่ติดกัน',
     'out': '<b>λ ปรากฏ</b> ≈ 1.56 cm = λ/2 (ภาพลวงตา ไม่ใช่ λ จริง)' },
   { 'el': '#data-table-container', 'prep': "recordMeasurement(); __sl('sl-strobe', 24); __setT(__T); { const h = wavelengthDeep / 3; __pin(__crest(2) - h, __crest(2)); } recordMeasurement(); __sl('sl-strobe', 8); setView('iso')",
     'title': 'บันทึก λ ปรากฏ ที่ N = 16 และ 24',
     'text': 'กด <b>💾 บันทึก</b> · ทำซ้ำที่ <b>N = 24 ช่อง/s</b> (3 เท่า) แถบสว่างถี่ขึ้น 3 เท่า · ที่ N ค่าอื่น (เช่น 10, 20) คลื่นดูเคลื่อนช้า ๆ ไม่นิ่ง จึงไม่บันทึก<br><b>λ ปรากฏ = λ × f / N</b> เมื่อ N = 2f, 3f',
     'out': 'N = 16 → λ ปรากฏ ≈ 1.6 cm · N = 24 → ≈ 1.0 cm · จึงต้องใช้ N = f วัด λ จริง' },
   { 'el': ['#sec-freq', '#view3d'], 'prep': "setExpMode('lambda', __btn('#exp-modes', 'lambda')); setWaveShape('plane', __btn('#wave-shapes', 'plane')); __q('strobe-toggle').checked = false; toggleStrobe(); __sl('sl-freq', 8); __setT(__T); __pin(__crest(3), __crest(4)); setView('read')",
     'title': 'II. คลื่นหน้าตรง: วัด λ ที่ความถี่ต่าง ๆ',
     'text': 'เลือก <b>II. λ vs f</b> และหน้าคลื่น <b>☰ หน้าตรง</b> (ใช้คานจุ่มน้ำแทนลูกปัด) · ตั้ง <b>f = 8 Hz</b> ปักหมุดบนแถบสว่าง 2 แถบที่อยู่ติดกัน แล้วกด 💾 บันทึก',
     'out': 'f = 8 Hz → <b>λ</b> = 3.14 cm' },
   { 'el': '#data-table-container', 'prep': "recordMeasurement(); [10, 12, 14, 16, 18].forEach(f => { __sl('sl-freq', f); __setT(__T); __pin(__crest(3), __crest(4)); recordMeasurement(); }); setView('iso')",
     'title': 'เพิ่มความถี่ แล้ววัดซ้ำ',
     'text': 'เปลี่ยนความถี่เป็น <b>10, 12, 14, 16, 18 Hz</b> วัด λ และบันทึกทุกค่า · ตารางคำนวณ <b>v = fλ</b> ให้ในคอลัมน์สุดท้าย',
     'out': '<b>λ</b> = 3.14 · 2.50 · 2.09 · 1.79 · 1.56 · 1.39 cm · <b>v = fλ</b> = 25.0–25.1 cm/s ทุกแถว' },
   { 'el': '#sec-graph', 'prep': "updateGraph()",
     'title': 'กราฟ λ กับ f',
     'text': 'กราฟความยาวคลื่นกับความถี่เป็น<b>เส้นโค้งลดลง</b> · ความถี่เพิ่ม 2 เท่า ความยาวคลื่นลดลงครึ่งหนึ่ง → λ แปรผกผันกับ f<br>③ <b>λ = v / f</b> โดย v คงที่ เพราะความลึกน้ำ (ตัวกลาง) เท่าเดิม',
     'out': 'λ ∝ 1/f · อัตราเร็วคลื่น <b>v ≈ 25 cm/s</b> ไม่ขึ้นกับความถี่' },
   { 'el': ['#sec-depth', '#view3d'], 'prep': "setExpMode('depth', __btn('#exp-modes', 'depth')); setWaveShape('plane', __btn('#wave-shapes', 'plane')); __sl('sl-depth-deep', 10); __sl('sl-depth-shallow', 1); __q('glass-toggle').checked = true; showGlass = true; __setT(__T); setView('top')",
     'title': 'III. วางแผ่นกระจกทำบริเวณน้ำตื้น',
     'text': 'เลือก <b>III. Speed vs Depth</b> · น้ำลึก <b>10 mm</b> วางแผ่นกระจกรองด้วยแหวน ให้น้ำเหนือกระจกลึกเพียง <b>1 mm</b> · เปิดคลื่นหน้าตรง f = 8 Hz · เมื่อคลื่นผ่านเข้าบริเวณน้ำตื้น แถบคลื่น<b>ถี่ขึ้น</b>',
     'out': 'น้ำตื้น: λ สั้นลง (ความถี่เท่าเดิม = 8 Hz)' },
   { 'el': ['#view3d', '#sec-measure'], 'prep': "__pin(__crest(3), __crest(4)); setView('read')",
     'title': 'วัด λ ในน้ำลึก',
     'text': 'ปักหมุดบนแถบสว่าง 2 แถบที่อยู่ติดกัน<b>ก่อนถึงแผ่นกระจก</b> แล้วกด 💾 บันทึก (ลงแถว Deep)',
     'out': '<b>λ<sub>ลึก</sub></b> = 3.14 cm' },
   { 'el': ['#view3d', '#sec-measure'], 'prep': "recordMeasurement(); __pin(__crest(2, 's'), __crest(3, 's')); setView('read')",
     'title': 'วัด λ ในน้ำตื้น',
     'text': 'ปักหมุดใหม่บนแถบสว่าง 2 แถบที่อยู่ติดกัน<b>เหนือแผ่นกระจก</b> แล้วกด 💾 บันทึก (ลงแถว Shallow)',
     'out': '<b>λ<sub>ตื้น</sub></b> = 0.99 cm' },
   { 'el': '#data-table-container', 'prep': "recordMeasurement(); setView('top')",
     'title': 'เทียบอัตราเร็วในน้ำลึกและน้ำตื้น',
     'text': 'ตารางคำนวณ <b>v = fλ</b> ทั้งสองแถว (f = 8 Hz เท่ากัน เพราะคลื่นมาจากแหล่งกำเนิดเดียวกัน)<br>④ v<sub>ลึก</sub> = f λ<sub>ลึก</sub> · v<sub>ตื้น</sub> = f λ<sub>ตื้น</sub>',
     'out': '<b>v<sub>ลึก</sub></b> = 8 × 3.14 ≈ 25.1 cm/s · <b>v<sub>ตื้น</sub></b> = 8 × 0.99 ≈ 7.9 cm/s → คลื่นน้ำเคลื่อนที่<b>ช้าลงในน้ำตื้น</b>' },
  ],
 }
