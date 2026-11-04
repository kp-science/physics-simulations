# -*- coding: utf-8 -*-
# Lab 43 SHM04 Phase Explorer — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# หยุดนาฬิกา (__kpSpeed 0) แล้วเดินเวลาของแต่ละแถบเองด้วยสูตรเดียวกับแลป (updateTrailA / y = A e^(−βt) sin ωt)
# คาบที่ซ่อนในแถบ C สุ่มทุกครั้งที่กดสุ่มใหม่ → ตรึงค่าตัวอย่าง T = 1.20 s เฉพาะ browser ที่ถ่ายภาพ
GUIDE = {
  'title': 'เฟสของการกระจัด ความเร็ว ความเร่ง และหาคาบจากกราฟ',
  'setup': r"""
    if (window.__kpSpeed) { __kpSpeed.set(0); const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    const sub = n => document.querySelectorAll('.subnav button')[n];
    window.__sub = k => showSubTab(k, sub({ A: 0, B: 1, C: 2 }[k]));
    window.__sl = (id, v) => { const e = document.getElementById('sl-' + id); e.value = v; document.getElementById('vi-' + id).value = v; e.dispatchEvent(new Event('input')); };
    window.__stop = (st, btn) => { if (st.isPlaying) { cancelAnimationFrame(st.animId); st.isPlaying = false; const b = document.getElementById(btn); b.textContent = '▶ เริ่ม'; b.classList.remove('playing'); } };
    /* แถบ A: เดินเวลาจาก 0 ถึง t (เก็บรอยกราฟทุก 0.02 s ด้วยฟังก์ชันของแลป) */
    window.__A = t => { __stop(A_state, 'playBtnA'); A_state.yTrail = []; A_state.xTrail = []; const p = getA(); for (let s = 0; s < t; s += 0.02) { A_state.t = s; updateTrailA(p); } A_state.t = t; updateTrailA(p); drawA(); };
    /* แถบ B: เดินเวลาถึง t แล้วหยุด */
    window.__B = t => { __stop(B_state, 'playBtnB'); B_state.trail = []; const p = getB(); for (let s = 0; s <= t + 1e-9; s += 1 / 60) B_state.trail.push({ t: s, y: p.A * Math.exp(-(p.beta || 0) * s) * Math.sin(p.w * s) }); B_state.t = t; drawB(); };
    window.__Bpick = t => { const p = getB(); B_state.selT = t; B_state.selY = p.A * Math.exp(-(p.beta || 0) * t) * Math.sin(p.w * t); recordSampleB(); };
    /* แถบ C: ตรึงคาบที่ซ่อน แล้วเดินเวลาถึง t */
    window.__TC = 1.20;
    window.__C = t => { __stop(C_state, 'playBtnC'); C_state.trail = []; const p = getC(), w = 2 * Math.PI / p.T; for (let s = 0; s <= t + 1e-9; s += 1 / 60) C_state.trail.push({ t: s, y: p.A * Math.exp(-(p.beta || 0) * s) * Math.sin(w * s + p.phi) }); C_state.t = t; drawC(); };
    /* คลิกจุดบนกราฟ C: ระยะ y ที่อ่านจากไม้บรรทัด (ปัด 0.001 m) */
    window.__Cpick = t => { const p = getC(), y = Math.round(p.A * Math.sin(2 * Math.PI / p.T * t + p.phi) * 1000) / 1000; C_state.selT = t; C_state.selY = y; document.getElementById('rC-meas').style.display = 'block'; setReadout('cC-t', fmt(t, 3) + ' s'); setReadout('cC-y', fmt(y, 3) + ' m', y < 0); drawC(); return y; };
  """,
  'steps': [
   { 'el': ['.subnav', '#sub-A .side-panel > div:first-child', '#cvA'], 'prep': "__sub('A'); setRecModeA('manual'); setAxisA('y'); __sl('Aamp', 0.5); __sl('AT', 3); __sl('Aphi', 0); __sl('Aspd', 1); __sl('Abeta', 0); resetA(); scrollTo(0,0)",
     'title': 'แถบ A: ตั้งเฟเซอร์ A = 0.5 m, T = 3 s',
     'text': 'เลือกแถบ <b>A · Phasor & Projections</b> · ตั้ง <b>A = 0.50 m</b> · <b>T = 3 s</b> · <b>φ₀ = 0°</b> · <b>β = 0</b> · โหมด <b>บันทึก 1 รอบ</b> · แกน <b>y = A sin(ωt+φ)</b><br><small>จุดสีฟ้าหมุนบนวงกลมรัศมี A ด้วยอัตราเร็วเชิงมุม ω เงาของจุดบนแกนดิ่งคือการกระจัด y ของการเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย</small>',
     'out': '<b>ω</b> = 2π/T = 2π/3 = 2.094 rad/s' },
   { 'el': ['#cvA', '#sub-A .readout'], 'prep': "__A(0.75)",
     'title': 'หยุดที่มุมเฟส 90° (ปลายบนสุด)',
     'text': 'กด <b>▶ เริ่ม</b> แล้วกด <b>⏸ หยุด</b> เมื่อจุดสีฟ้าอยู่บนสุดของวงกลม (หรือหยุดแล้วลากจุดสีฟ้าเอง) · อ่านกล่อง <b>ค่าปัจจุบัน</b><br><small>ที่ปลายสุด วัตถุหยุดชั่วขณะ แต่ความเร่งมีขนาดมากที่สุดและชี้กลับเข้าหาสมดุล</small>',
     'out': 'มุมเฟส 90°: <b>y</b> = +0.500 m · <b>v</b> = 0 · <b>a</b> = −ω²A = −2.193 m/s²' },
   { 'el': ['#cvA', '#sub-A .readout'], 'prep': "__A(1.5)",
     'title': 'หยุดที่มุมเฟส 180° (ผ่านตำแหน่งสมดุล)',
     'text': 'เดินต่อแล้วหยุดเมื่อจุดสีฟ้าอยู่ซ้ายสุดของวงกลม เงาบนแกนดิ่งอยู่ที่ศูนย์ · จดค่า y, v, a เหมือนเดิม · ทำซ้ำที่มุมเฟส 0°, 270° (บันทึก 4–8 จุดต่อรอบ)',
     'out': 'มุมเฟส 180°: <b>y</b> = 0 · <b>v</b> = −ωA = −1.047 m/s (มากที่สุด) · <b>a</b> = 0' },
   { 'el': '#cvAcomp', 'prep': "__A(3)",
     'title': 'เทียบกราฟ: เฟสต่างกัน 90°',
     'text': 'เมื่อครบ 1 รอบ (โหมด 1 รอบหยุดเอง) ดูกราฟด้านล่าง y–t (เขียว) กับ x–t (ชมพู) · ยอดของกราฟหนึ่งตรงกับจุดตัดศูนย์ของอีกกราฟ<br>① <b>y = A sin ωt</b> · <b>v = ωA cos ωt</b> (เฟสนำ y อยู่ 90°) · <b>a = −ω²A sin ωt = −ω²y</b> (เฟสต่างจาก y 180°)',
     'out': '<b>v</b> นำ <b>y</b> อยู่ 90° · <b>a</b> มีเฟสตรงข้ามกับ <b>y</b> (ต่างกัน 180°)' },
   { 'el': ['#cvA', '#sl-Abeta'], 'prep': "__sl('Abeta', 0.3); __A(3)",
     'title': 'เปิดการหน่วง β = 0.3 1/s',
     'text': 'ตั้ง <b>β = 0.30 1/s</b> แล้วเล่นใหม่ · รัศมีของวงกลมหดลง แอมพลิจูดลดลงแบบ <b>A e<sup>−βt</sup></b> แต่คาบยังเท่าเดิม',
     'out': 'หลัง 1 คาบ: <b>A</b> = 0.50 × e<sup>−0.3×3</sup> ≈ 0.20 m' },
   { 'el': ['#sub-B .side-panel > div:first-child', '#cvB'], 'prep': "__sl('Abeta', 0); __sub('B'); __sl('Bm', 1); __sl('Bk', 10); __sl('BA', 0.2); __sl('Bf', 0); __sl('Bbeta', 0); resetB(); __B(6)",
     'title': 'แถบ B: มวลติดสปริง m = 1 kg, k = 10 N/m',
     'text': 'เลือกแถบ <b>B · Spring-Mass Sampler</b> ตั้ง <b>m = 1 kg</b> · <b>k = 10 N/m</b> · <b>A = 0.20 m</b> · f = 0 (ใช้ค่าจาก k, m) · กด <b>▶ เริ่ม</b> ดูมวลสั่น แล้วกด <b>⏸ หยุด</b><br>② <b>ω = √(k/m)</b> · <b>T = 2π/ω</b>',
     'out': '<b>ω</b> = √(10/1) = 3.162 rad/s · <b>T</b> = 1.987 s' },
   { 'el': ['#cvB', '#rB-sample'], 'prep': "document.getElementById('cb-vt').checked = true; document.getElementById('cb-at').checked = true; __Bpick(5.3)",
     'title': 'คลิกจุดบนกราฟ อ่าน y, v, a',
     'text': 'ติ๊ก <b>v-t</b> และ <b>a-t</b> ให้กราฟซ้อนกัน · <b>คลิก</b>บนกราฟ โปรแกรมสแนปจุดลงบนเส้น y–t แล้วแสดงเวกเตอร์ y v a และค่าในกล่อง <b>📌 จุดที่บันทึก</b> · คลิกหลายตำแหน่ง จด 5 จุดเป็นตาราง<br>③ <b>v = ωA cos ωt</b> · <b>a = −ω²y</b>',
     'out': 't = 5.300 s: <b>y</b> = −0.174 m · <b>v</b> = −0.314 m/s · <b>a</b> = +1.737 m/s² (= −ω²y = −10 × (−0.174))' },
   { 'el': ['#sub-B .side-panel > div:nth-child(2)', '#cvB'], 'prep': "__sl('Bk', 40); __B(6); __Bpick(5.3)",
     'title': 'เพิ่ม k เป็น 4 เท่า',
     'text': 'ตั้ง <b>k = 40 N/m</b> (4 เท่า) เล่นใหม่ แล้วอ่าน ω และ T ในกล่อง <b>ค่าจริง ณ เวลา t</b> · ω = √(k/m) จึงเพิ่ม 2 เท่า คาบลดลงครึ่งหนึ่ง และอัตราเร็วสูงสุด ωA เพิ่ม 2 เท่า',
     'out': '<b>ω</b> = 6.325 rad/s (2 เท่า) · <b>T</b> = 0.993 s (ครึ่งหนึ่ง) · <b>v</b><sub>max</sub> = ωA = 1.26 m/s (2 เท่า)' },
   { 'el': '#cvC', 'prep': "__sl('Bk', 10); __sub('C'); document.getElementById('objC').value = 'hspring'; changeObjC(); C_state.hiddenT = __TC; __sl('CA', 0.15); __sl('Cphi', 0); __sl('Cbeta', 0); document.getElementById('cb-ruler').checked = true; document.getElementById('cb-phase').checked = false; C_state.caliperA = 1.0; C_state.caliperB = 2.5; __C(7.0)",
     'title': 'แถบ C: คาบถูกซ่อน เล่นจนเห็นหลายยอด',
     'text': 'เลือกแถบ <b>C · Period Challenge</b> วัตถุ <b>สปริงแนวนอน</b> (A = 0.15 m, φ₀ = 0°, β = 0) กด <b>↺ สุ่มใหม่</b> โปรแกรมสุ่มคาบไว้โดยไม่บอก · กด <b>▶ เริ่ม</b> รอให้กราฟมี<b>ยอดคลื่นอย่างน้อย 2 ยอด</b> แล้วกด <b>⏸ หยุด</b>' },
   { 'el': '#cvC', 'prep': "C_state.caliperA = 2.7 - (C_state.t - 6); C_state.caliperB = 3.9 - (C_state.t - 6); drawC()",
     'title': 'วัดคาบด้วยคาลิปเปอร์',
     'text': 'ลาก<b>ปาก A</b> (สีเหลือง) ไปที่ยอดคลื่นยอดหนึ่ง และ<b>ปาก B</b> ไปที่ยอดถัดไปที่อยู่ติดกัน · อ่าน <b>ΔT</b> ใต้วงเล็บ ระยะเวลาระหว่างยอดติดกัน = คาบ<br><small>วัดหลายคู่ยอดแล้วเฉลี่ย ลดความคลาดเคลื่อนจากการวางปากคาลิปเปอร์</small>',
     'out': '<b>ΔT</b> = <b>T</b> ≈ 1.200 s (ค่าในภาพตัวอย่าง)' },
   { 'el': '#cTinput', 'prep': "document.getElementById('cTinput').value = '1.20'; checkPeriodC(); document.getElementById('cb-phase').checked = true; drawC(); document.getElementById('cTinput').closest('.side-panel > div').scrollIntoView({ block: 'center' })",
     'title': 'กรอกคาบ แล้วกดตรวจคาบ',
     'text': 'กรอก <b>T</b> ในช่อง y = A sin(<b>T?</b> · t + φ) แล้วกด <b>🧮 ตรวจคาบ</b> โปรแกรมบอก %error และเฉลยคาบจริง (ผ่านเมื่อคลาดไม่เกิน 10% แล้วเปิด<b>สเกลเฟส</b>ให้ใช้)<br>④ <b>ω = 2π / T</b>',
     'out': '<b>T</b> = 1.20 s → <b>ω</b> = 5.236 rad/s (คาบสุ่มทุกครั้ง: สปริงแนวนอน 0.6 – 1.8 s)' },
   { 'el': ['#cvC', '#rC-meas'], 'prep': "__Cpick(5.5)",
     'title': 'คลิกจุดบนกราฟ วัดการกระจัด y',
     'text': 'คลิกจุดบนกราฟ (ขณะหยุด) แล้วใช้ไม้บรรทัดวัดระยะจากแนวสมดุลถึงจุดนั้น · จุดใต้แนวสมดุลให้ใส่เครื่องหมาย <b>−</b>',
     'out': 't = 5.500 s · <b>y</b> = −0.075 m' },
   { 'el': '#rC-final', 'prep': "document.getElementById('cYInput').value = '-0.075'; checkDisplacementC(); document.getElementById('rC-final').scrollIntoView({ block: 'center' })",
     'title': 'ตรวจค่า y, v, a',
     'text': 'กรอก <b>y = −0.075</b> แล้วกด <b>🧮 ตรวจค่า y,v,a</b> โปรแกรมคำนวณจาก y ที่กรอกเทียบกับค่าจริง<br>⑤ <b>|v| = ω√(A² − y²)</b><br>⑥ <b>a = −ω²y</b><br><small>ทิศของ v ดูจากแนวโน้มกราฟ: กราฟกำลังขึ้น v เป็นบวก กำลังลง v เป็นลบ</small>',
     'out': '<b>|v|</b> = 5.236 × √(0.15² − 0.075²) ≈ 0.680 m/s · <b>a</b> = −(5.236)² × (−0.075) ≈ +2.06 m/s²' },
   { 'el': '#energy-panel', 'prep': "if (document.getElementById('energy-panel').style.display === 'none') toggleEnergyC(); drawEnergyC()",
     'title': 'กราฟพลังงาน',
     'text': 'กด <b>📊 กราฟพลังงาน</b> ดูพลังงานจลน์ KE และพลังงานศักย์ยืดหยุ่น PE<sub>s</sub> (มวลอ้างอิง 1 kg) · ผลรวมคงตัวเมื่อไม่มีการหน่วง · ถ้าตั้ง β &gt; 0 พลังงานรวมลดลงเรื่อย ๆ<br>⑦ <b>k = mω²</b> · <b>E = ½kA²</b>',
     'out': '<b>k</b> = 1 × 5.236² ≈ 27.4 N/m · <b>E</b> = ½ × 27.4 × 0.15² ≈ 0.31 J (KE + PE<sub>s</sub> คงตัว)' },
  ],
 }
