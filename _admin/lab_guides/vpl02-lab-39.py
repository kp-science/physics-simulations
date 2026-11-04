# -*- coding: utf-8 -*-
# Lab 39 วงกลมเฟสกับคลื่น — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ทุกตัวเลข = แบบจำลองของแลปเอง (state.t · releasePulse/toggleTimerA/toggleContFreeze/autoPlaceCalipers · kwave()) ·
# หยุดนาฬิกาแลป (__kpSpeed.set(0)) แล้วตั้ง state.t เอง = จังหวะที่นักเรียนกดปุ่ม
GUIDE = {
  'title': 'อัตราเร็วคลื่นดลกับคลื่นต่อเนื่อง · เฟสของจุดบนคลื่น · การรวมคลื่นที่เฟสต่างกัน',
  'setup': r"""
    if (window.__kpSpeed) __kpSpeed.set(0);
    window.__q = s => document.querySelector(s);
    window.__sl = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input')); };
    window.__exp = e => __q('#segExp button[data-exp="' + e + '"]').click();
    window.__T = t => { state.t = t; draw(); updateReadout(); };
    /* คลื่นดล: กดเริ่ม/หยุดจับเวลาเมื่อยอดดลถึงตำแหน่ง xa และ xb */
    window.__pulse = (xa, xb) => { resetExpA(); togglePlay(); releasePulse(); const v = vwave(), t0 = state.pulseT0;
      __T(t0 + xa / v); toggleTimerA(); __T(t0 + xb / v); toggleTimerA(); };
    window.__dRow = () => { const r = state.pulseRows[state.pulseRows.length - 1]; r.d = +Math.abs(state.pulseStopX - state.pulseStartX).toFixed(2); r.v = r.d / r.t; renderTableA(); };
    window.__lRow = () => { const r = state.contRows[state.contRows.length - 1]; r.lam = +Math.abs(state.calX2 - state.calX1).toFixed(2); r.v = r.lam * r.f; renderTableA(); };
    window.__hn = () => { const n = document.getElementById('savedNote'); if (n) { n.style.transition = 'none'; n.style.opacity = '0'; } };
    window.__in = (sel, v) => { const e = __q(sel); e.value = v; };
  """,
  'steps': [
   { 'el': ['.cbar', '#sl-lam', '#sl-f'], 'prep': "__q('#segMode button[data-mode=\"manual\"]').click(); __exp('A'); __sl('sl-lam', 1.2); __sl('sl-f', 1.5); state.pulseRows = []; state.contRows = []; resetExpA(); renderTableA(); scrollTo(0,0)",
     'title': 'ฐาน A: ตั้งค่าคลื่น',
     'text': 'เลือกฐาน <b>A · Pulse vs Continuous</b> และโหมด <b>✍ บันทึกเอง</b> · ตั้งความยาวคลื่น <b>λ = 1.20 m</b> และความถี่ <b>f = 1.5 Hz</b> (ฐาน A ซ่อนค่า v ไว้ให้วัดเอง) · จอบนเป็น<b>คลื่นดล</b> (สะบัดเชือก 1 ครั้ง) จอล่างเป็น<b>คลื่นต่อเนื่อง</b> ในเชือกเส้นเดียวกัน',
     'out': 'λ = 1.20 m · f = 1.5 Hz' },
   { 'el': ['#aReleaseBtn', '#cvWrap'], 'prep': "resetExpA(); togglePlay(); releasePulse(); __T(state.pulseT0 + 0.3 / vwave())",
     'title': 'ปล่อยคลื่นดล',
     'text': 'กด <b>🚀 ปล่อยคลื่น</b> (เริ่มเดินเวลาให้ด้วย) ดลสีแดงออกจาก x = 0 เคลื่อนที่ไปทางขวา และคลื่นต่อเนื่องจอล่างเริ่มแผ่ออกไปพร้อมกัน · ถ้าเร็วเกินไป ลด <b>สปีดอนิเมชัน</b> ได้ (นาฬิกาช้าลงตาม ค่าที่วัดไม่เปลี่ยน)' },
   { 'el': ['#aTimerBtn', '#cvWrap'], 'prep': "__T(state.pulseT0 + 0.52 / vwave()); toggleTimerA(); __T(state.pulseT0 + 1.2 / vwave())",
     'title': 'เริ่มจับเวลาเมื่อดลผ่านตำแหน่งแรก',
     'text': 'เมื่อยอดดลถึงประมาณ <b>0.5 m</b> กด <b>⏱ เริ่มจับเวลา</b> · โปรแกรมปักเส้นสีเหลืองที่ตำแหน่งยอดดลขณะกด',
     'out': 'เส้นเหลือง <b>x₁</b> = 0.52 m' },
   { 'el': ['#aTimerBtn', '#cvWrap'], 'prep': "__T(state.pulseT0 + 3.02 / vwave()); toggleTimerA()",
     'title': 'หยุดเวลาเมื่อดลผ่านตำแหน่งที่สอง',
     'text': 'เมื่อยอดดลถึงประมาณ <b>3.0 m</b> กด <b>⏱ หยุด</b> ได้เส้นสีเขียว · เวลาที่ดลใช้ Δt แสดงที่มุมล่างซ้ายของจอบน',
     'out': 'เส้นเขียว <b>x₂</b> = 3.02 m · <b>Δt</b> = 1.389 s' },
   { 'el': ['[onclick="savePulseRecord()"]', '#tableWrap'], 'prep': "savePulseRecord(); __dRow()",
     'title': 'บันทึกคลื่นดล แล้วกรอกระยะ',
     'text': 'กด <b>💾 บันทึกคลื่นดล</b> โปรแกรมลง Δt ในตารางคลื่นดลให้ · อ่าน x ของเส้นเหลืองและเส้นเขียวจากสเกล แล้วพิมพ์ <b>d = x₂ − x₁</b> ในช่อง d<br>① อัตราเร็วคลื่นดล <b>v = d/Δt</b>',
     'out': 'd = 3.02 − 0.52 = 2.50 m → <b>v<sub>ดล</sub></b> = 2.50 / 1.389 = <b>1.80 m/s</b>' },
   { 'el': ['#aContFreezeBtn', '#cvWrap'], 'prep': "__hn(); toggleContFreeze()",
     'title': 'หยุดคลื่นต่อเนื่อง แล้ววัด λ',
     'text': 'กด <b>⏸ หยุดคลื่น</b> คลื่นจอล่างค้างนิ่ง คาลิปเปอร์ ① ② วางที่สันคลื่น · ลากให้ตรง<b>สันคลื่น 2 สันที่อยู่ติดกัน</b> แล้วอ่าน x ของทั้งสองจากสเกล (ขีดละ 0.05 m)<br><small>ระยะระหว่างสันติดกัน = ความยาวคลื่น λ</small>',
     'out': '① x = 0.32 m · ② x = 1.52 m → <b>λ</b> = 1.52 − 0.32 = 1.20 m' },
   { 'el': ['[onclick="saveContinuousRecord()"]', '#tableWrap'], 'prep': "saveContinuousRecord(); __lRow()",
     'title': 'บันทึกคลื่นต่อเนื่อง → เทียบอัตราเร็ว',
     'text': 'กด <b>💾 บันทึกต่อเนื่อง</b> โปรแกรมลง f ให้ · พิมพ์ λ ที่วัดได้ในช่อง λ<br>② อัตราเร็วคลื่นต่อเนื่อง <b>v = fλ</b><br>③ กรอบ <b>📐 เปรียบเทียบความเร็ว</b> คำนวณ |v<sub>ดล</sub> − v<sub>ต่อเนื่อง</sub>|',
     'out': '<b>v<sub>ต่อเนื่อง</sub></b> = 1.5 × 1.20 = <b>1.80 m/s</b> = v<sub>ดล</sub> (ต่างกัน 0.0%)' },
   { 'el': '#tableWrap', 'prep': "__sl('sl-lam', 0.8); __sl('sl-f', 2.0); __pulse(0.52, 3.02); savePulseRecord(); __dRow(); toggleContFreeze(); saveContinuousRecord(); __lRow()",
     'title': 'เปลี่ยนค่า แล้ววัดซ้ำ',
     'text': 'กด <b>↺ รีเซ็ตฐาน A</b> เปลี่ยนเป็น λ = 0.80 m, f = 2.0 Hz แล้ววัดคลื่นดลและคลื่นต่อเนื่องแบบเดิม',
     'out': 'แถว 2: d = 2.50 m, Δt = 1.563 s → v<sub>ดล</sub> = 1.60 m/s · λ = 0.80 m → v<sub>ต่อเนื่อง</sub> = 2.0 × 0.80 = 1.60 m/s<br>→ <b>คลื่นดลและคลื่นต่อเนื่องในตัวกลางเดียวกันมีอัตราเร็วเท่ากัน</b>' },
   { 'el': ['#cvWrap'], 'prep': "__hn(); resetExpA(); __sl('sl-lam', 1.2); __sl('sl-f', 1.5); __exp('B'); ['q1','q2','q3','q4'].forEach(k => state.selB[k] = true); renderTableB(); if (!state.playing) togglePlay(); __T(1 / 6); scrollTo(0,0)",
     'title': 'ฐาน B: ดูการสั่นของจุดบนเชือก',
     'text': 'เลือกฐาน <b>B · เฟสริบบิ้น</b> ติ๊ก ✓ จุดที่ห่างจากแหล่งกำเนิด (R สีแดง) <b>Δx = λ/4, λ/2, 3λ/4, λ</b> แล้วกด <b>▶ เริ่ม</b> · ลูกบอลบนวงกลมเฟสหมุนรอบละ 1 คาบ ภาพฉายแนวตั้งของลูกบอล = การกระจัด y ของจุดบนเชือก · สังเกตว่าแต่ละจุดสั่น<b>พร้อม</b>หรือ<b>สวน</b>กับ R',
     'out': 'ภาพ y–x ล่าง ขณะ R อยู่ที่ +A: จุด λ/4 (เหลือง) อยู่ที่แนวสมดุล · λ/2 (ฟ้า) อยู่ที่ −A · 3λ/4 (ม่วง) อยู่ที่แนวสมดุล · λ (เขียว) อยู่ที่ +A พร้อม R' },
   { 'el': '#tableWrap', 'prep': "[['q1',90,'ช้า 90°'],['q2',180,'สวนทาง'],['q3',270,'ช้า 270°'],['q4',360,'พร้อมกัน']].forEach(([k,d,r]) => { __in('[data-b-dphi=\"' + k + '\"]', d); __in('[data-b-rel=\"' + k + '\"]', r); })",
     'title': 'บันทึกเฟสที่ต่างกันลงตาราง',
     'text': 'กรอก <b>Δφ</b> และความสัมพันธ์กับ R ของแต่ละจุด · จุดที่อยู่ไกลกว่าได้รับการสั่นช้ากว่า เฟสจึง "ช้ากว่า" R<br>④ <b>Δφ = (Δx/λ) × 360°</b>',
     'out': 'λ/4 → 90° (ช้า 90°) · λ/2 → 180° (<b>เฟสตรงข้าม</b> สวนทาง) · 3λ/4 → 270° · λ → 360° = 0° (<b>เฟสตรงกัน</b> สั่นพร้อมกัน)' },
   { 'el': ['#cvWrap', '#ro-dphi'], 'prep': "__exp('C'); __T(1 / 6); state.cursorX = 0.30; draw(); updateReadout(); scrollTo(0,0)",
     'title': 'ฐาน C: วาง cursor แล้วอ่านเฟส',
     'text': 'เลือกฐาน <b>C · Δφ + ซ้อนคลื่น</b> <b>คลิกบนแถบคลื่น y–x</b> (จอล่าง) เพื่อวาง cursor ห่างจากแหล่งกำเนิด Δx · อ่าน <b>Δφ ที่ cursor</b> ในกรอบค่าที่อ่านได้ (Readout)<br>⑤ <b>Δφ = kΔx = 2π(Δx/λ)</b>',
     'out': 'cursor Δx = 0.30 m = λ/4 → <b>Δφ</b> = 90° (1.57 rad)' },
   { 'el': ['#row-dphi', '#cvWrap'], 'prep': "state.cursorX = null; __sl('sl-dphi', 180); document.getElementById('vi-dphi').value = 180; draw(); updateReadout()",
     'title': 'ซ้อนคลื่น 2 ขบวนที่เฟสต่างกัน 180°',
     'text': 'เลื่อน <b>Δφ เฟสคลื่น 2</b> คลื่น 2 (เส้นประชมพู) เลื่อนไปตามเฟส · คลื่นผลรวม y₁ + y₂ (สีเหลือง) · ตั้ง <b>Δφ = 180°</b> สันของคลื่นหนึ่งตรงกับท้องของอีกคลื่น<br>⑥ แอมพลิจูดผลรวม <b>A<sub>รวม</sub> = 2A|cos(Δφ/2)|</b>',
     'out': 'Δφ = 180° → คลื่นผลรวมเป็นเส้นตรง y = 0 → <b>A<sub>รวม</sub> = 0</b> (หักล้างกัน)' },
   { 'el': ['#tableWrap', '[onclick="exportCSV()"]'], 'prep': "__sl('sl-dphi', 90); document.getElementById('vi-dphi').value = 90; [[90,1.57,1.41],[180,3.14,0],[270,4.71,1.41],[0,0,2]].forEach(([d,r,a], i) => { const tr = __q('#tableWrap tr[data-row=\"' + i + '\"]'); tr.querySelector('[data-col=\"dphi\"]').value = d; tr.querySelector('[data-col=\"dphir\"]').value = r; tr.querySelector('[data-col=\"Atot\"]').value = a; })",
     'title': 'กรอกตาราง แล้วสรุปผล',
     'text': 'วาง cursor ที่ λ/4, λ/2, 3λ/4, λ อ่าน Δφ (องศาและเรเดียน) · ตั้ง Δφ คลื่น 2 เท่าค่านั้น อ่าน A<sub>รวม</sub>/A แล้วกรอก · กด <b>⬇ CSV</b> เก็บตารางแนบใบงาน<br><small>ที่ Δx = λ ให้กรอก 0° เพราะ 360° คือเฟสเดียวกับ 0°</small>',
     'out': 'Δφ = 90° · 180° · 270° · 0° → <b>A<sub>รวม</sub>/A</b> = 1.41 · 0 · 1.41 · 2 → เฟสตรงกันเสริมกันมากที่สุด (2A) · เฟสตรงข้ามหักล้างกัน (0)' },
  ],
 }
