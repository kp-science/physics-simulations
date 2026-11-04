# -*- coding: utf-8 -*-
# Lab 42 SHM03 Spring Builder — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ตัวนับรอบของแลปใช้เวลาจำลอง S.t → หยุดนาฬิกา (__kpSpeed 0) แล้วเลื่อน S.t เอง · นักเรียนกด ⏹ Stop ช้ากว่ารอบที่ 10 ราว 0.05 s
# ค่า k ที่สุ่มในโหมดสุ่ม (50–400 N/m) → ตรึงค่าตัวอย่าง k₁ = 250, k₂ = 150 N/m เฉพาะ browser ที่ถ่ายภาพ
GUIDE = {
  'title': 'หาค่าคงตัวสปริง k จากคาบ และตรวจ k ของสปริงต่ออนุกรม/ขนาน',
  'setup': r"""
    if (window.__kpSpeed) { __kpSpeed.set(0); const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    const q = s => document.querySelector(s);
    window.__clk = s => q(s).click();
    window.__set = (id, v) => { const e = $id('sl-' + id); e.value = v; e.dispatchEvent(new Event('input')); };
    window.__n = v => { const e = $id('nSprings'); e.value = String(v); e.dispatchEvent(new Event('change')); };
    window.__LATE = 0.05;
    /* เลื่อนเวลาจำลองไปจน "รอบที่" ได้ nc รอบ (+ ช้าเล็กน้อย) แล้วให้ตัวนับรอบของแลปอ่านค่าเอง */
    window.__go = (nc, late) => { const T = period(calcKEff(), S.m), d = nc * T + (late || 0); S.t = CYC.simStart + d; CYC.t0 = performance.now() - d * 1000; cycTick(); draw(); };
    window.__meas = () => { cycReset(); resetSim(); cycStart(); __go(10, __LATE); cycStop(); };
    window.__xva = () => { XVA.buf.length = 0; const t0 = S.t; for (let i = 0; i <= 300; i++) { S.t = t0 + i * 0.03; xvaPush(); } xvaDraw(); };
  """,
  'steps': [
   { 'el': ['#recToggle', '#builderSect', '#view3d'], 'prep': "__clk('[data-rec=\"manual\"]'); setManSub('timer'); manualClear(); cycReset(); resetSim(); __clk('[data-base=\"A\"]'); __clk('[data-orient=\"h\"]'); __clk('[data-conn=\"single\"]'); __set('k1', 100); setView('iso'); scrollTo(0,0)",
     'title': 'ตั้งสปริงเดี่ยว k = 100 N/m แนวระดับ',
     'text': 'เลือกโหมดบันทึก <b>✍️ Manual</b> · ฐาน <b>A · Builder</b> แนว <b>↔ ระดับ</b> · ที่แถบประกอบสปริงเลือก <b>เดี่ยว</b> แล้วตั้ง <b>k₁ = 100 N/m</b><br><small>รถทดลองบนรางติดกับสปริงที่ยึดผนัง เมื่อดึงแล้วปล่อย รถจะเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย</small>',
     'out': '<b>k</b> ที่ตั้ง = 100 N/m (ใช้เป็นค่าอ้างอิง)' },
   { 'el': ['div.builder-bar:has(#sl-m)', '#view3d'], 'prep': "__set('m', 1.0); __set('A', 0.15); __set('spd', 1); { const g = $id('gSel'); g.value = '9.8'; g.dispatchEvent(new Event('change')); } setView('iso')",
     'title': 'ตั้งมวล m = 1.0 kg และแอมพลิจูด A = 0.15 m',
     'text': 'ตั้ง <b>มวล m = 1.0 kg</b> · <b>แอม A = 0.15 m</b> (หรือลากรถในภาพขณะหยุด) · ความเร็วเล่น <b>1×</b> เพื่อให้นาฬิกาตรงกับเวลาจริง',
     'out': '<b>m</b> = 1.0 kg · <b>A</b> = 0.15 m' },
   { 'el': ['#cycTarget', '#cycDisplay'], 'prep': "$id('cycTarget').value = 10; cycReset()",
     'title': 'ตั้งเป้าหมาย 10 รอบ',
     'text': 'ในกล่อง <b>📝 บันทึกผล</b> แถบ <b>📌 ใช้ค่าที่กำหนด</b> ตั้ง <b>เป้าหมาย N รอบ = 10</b><br><small>จับเวลาหลายรอบแล้วหารด้วยจำนวนรอบ ลดความคลาดเคลื่อนจากการกดปุ่มช้า/เร็ว</small>' },
   { 'el': ['#cycStartBtn', '#view3d'], 'prep': "cycStart(); __go(4.4, 0); setView('timer'); orbit.el = 0.5",
     'title': 'กด Start ให้รถสั่น แล้วดูตัวนับรอบ',
     'text': 'กด <b>▶ Start</b> รถเริ่มสั่นและนาฬิกาเริ่มเดิน · เกตแสงนับรอบให้ทุกครั้งที่รถสั่นครบ 1 รอบ · กด <b>🔍 ตัวนับรอบ</b> ดูจอ <b>KP TIMER</b> (เวลา · รอบที่)' },
   { 'el': ['#cycDisplay', '#view3d'], 'prep': "__go(10, __LATE); setView('timer'); orbit.el = 0.5",
     'title': 'ครบ 10 รอบ กด Stop',
     'text': 'เมื่อรอบที่ขึ้น <b>10 / 10</b> มีข้อความ <b>✅ ครบ 10 รอบแล้ว</b> ให้กด <b>⏹ Stop</b> ทันที (ถ้าช้าเกินจะเตือน <b>เลยรอบแล้ว</b>) · อ่านเวลารวม',
     'out': '<b>t</b> ≈ 6.33 s สำหรับ <b>n</b> = 10 รอบ' },
   { 'el': ['#cycResult', '#manualTbl'], 'prep': "cycStop(); setView('iso')",
     'title': 'โปรแกรมคำนวณ T และ k',
     'text': 'เมื่อกด ⏹ Stop โปรแกรมคำนวณต่อเป็นลำดับ แล้วเพิ่มแถวในตาราง<br>① คาบ <b>T = t / n</b><br>② จาก <b>T = 2π√(m/k)</b> → <b>k = 4π²m / T²</b><br>③ เทียบกับ k ที่ตั้ง: <b>%error = |k<sub>วัด</sub> − k<sub>ตั้ง</sub>| / k<sub>ตั้ง</sub> × 100</b><br><small>กดหยุดช้าไปเล็กน้อย T จึงยาวขึ้นและ k<sub>วัด</sub> น้อยกว่าค่าที่ตั้งเล็กน้อย</small>',
     'out': '<b>T</b> ≈ 0.633 s · <b>k</b><sub>วัด</sub> ≈ 98.4 N/m · คลาด ≈ 1.6%' },
   { 'el': '#manualTbl', 'prep': "__set('m', 2.0); __meas(); __set('m', 4.0); __meas(); setView('iso')",
     'title': 'เปลี่ยนมวล แล้ววัดซ้ำ',
     'text': 'ตั้ง <b>m = 2.0 kg</b> และ <b>4.0 kg</b> (k เท่าเดิม) จับเวลา 10 รอบแบบเดิม · มวลเพิ่ม 4 เท่า คาบควรเพิ่ม 2 เท่า (T ∝ √m) ส่วน k ที่คำนวณได้ยังเท่าเดิม',
     'out': '<b>T</b> ≈ 0.894 s (2.0 kg) · 1.262 s (4.0 kg) → <b>k</b><sub>วัด</sub> ≈ 99 N/m ทุกมวล' },
   { 'el': ['#builderSect', '#view3d'], 'prep': "__set('m', 1.0); __clk('[data-conn=\"series\"]'); __n(2); __set('k1', 100); __set('k2', 200); resetSim(); setView('iso')",
     'title': 'ต่อสปริง 2 ตัวแบบอนุกรม แล้วทำนาย k',
     'text': 'กลับเป็น m = 1.0 kg · เลือก <b>อนุกรม</b> จำนวน <b>2 ตัว</b> ตั้ง <b>k₁ = 100</b> และ <b>k₂ = 200 N/m</b> · <b>ทำนายก่อน</b>: k ของระบบเป็น 300, 150 หรือ 66.7 N/m<br>④ อนุกรม: <b>1/k = 1/k₁ + 1/k₂</b> = 1/100 + 1/200 = 3/200',
     'out': 'k ตามทฤษฎี (อนุกรม) = <b>66.7 N/m</b>' },
   { 'el': ['#cycResult', '#manualTbody tr:last-child'], 'prep': "__meas()",
     'title': 'วัดคาบของสปริงอนุกรม',
     'text': 'จับเวลา 10 รอบแบบเดิม (▶ Start → ครบ 10 รอบ → ⏹ Stop) · สปริงอนุกรม "อ่อน" กว่าสปริงแต่ละตัว รถจึงสั่นช้าลง',
     'out': '<b>T</b> ≈ 0.775 s · <b>k</b><sub>วัด</sub> ≈ 65.8 N/m (ทฤษฎี 66.7 N/m)' },
   { 'el': ['#manualTbody tr:last-child', '#cycResult'], 'prep': "__clk('[data-conn=\"parallel\"]'); resetSim(); __meas()",
     'title': 'เปลี่ยนเป็นต่อขนาน แล้ววัดซ้ำ',
     'text': 'เลือก <b>ขนาน</b> (k₁ = 100, k₂ = 200 N/m เท่าเดิม) จับเวลา 10 รอบ<br>⑤ ขนาน: <b>k = k₁ + k₂</b> = 300 N/m · สปริงขนาน "แข็ง" กว่า รถสั่นเร็วขึ้น<br><small>คาบสั้น การกดหยุดช้าไปนิดเดียวมีผลมาก ควรนับรอบมากขึ้น (เช่น 20 รอบ)</small>',
     'out': '<b>T</b> ≈ 0.368 s · <b>k</b><sub>วัด</sub> ≈ 292 N/m (ทฤษฎี 300 N/m)' },
   { 'el': '#manualTbl',
     'title': 'อ่านตารางบันทึกผล',
     'text': 'แต่ละแถว = การวัด 1 ครั้ง: การต่อ · n · t · <b>T = t/n</b> · <b>k_meas = 4π²m/T²</b> · <b>k_อ้างอิง</b> (ค่าที่ตั้ง/ตามสูตร) · <b>err%</b> (เขียว &lt; 2% · ส้ม &lt; 5%) · ดาวน์โหลดเป็น <b>⬇ CSV</b> ได้',
     'out': 'สรุป: เดี่ยว ≈ 98 · อนุกรม ≈ 66 · ขนาน ≈ 292 N/m → ตรงกับ <b>1/k = Σ1/kᵢ</b> และ <b>k = Σkᵢ</b>' },
   { 'el': '#simCanvas', 'prep': "__clk('[data-conn=\"single\"]'); __set('k1', 100); __clk('[data-base=\"B\"]'); resetSim(); S.t = 0.3 * period(calcKEff(), S.m); draw(); setView('iso')",
     'title': 'กราฟ F–x: กฎของฮุก',
     'text': 'เลือก <b>ฐาน B · F-x Graph</b> (สปริงเดี่ยว k = 100 N/m) กด ▶ เริ่ม · จุดสีเขียวเลื่อนไปมาบน<b>เส้นตรงผ่านจุดกำเนิด</b>ที่มีความชันเป็นลบ แรงของสปริงมีทิศตรงข้ามกับการกระจัดเสมอ<br>⑥ <b>F = −kx</b> → ความชัน = −k · ลองตั้ง k₁ = 300 N/m กราฟจะชันขึ้น 3 เท่า',
     'out': 'ความชัน = <b>−100 N/m</b> (= −k)' },
   { 'el': ['#baseToggle', '#view3d'], 'prep': "__clk('[data-base=\"C\"]'); resetSim(); setView('iso')",
     'title': 'แนวดิ่งกับแนวระดับ: คาบเท่ากัน',
     'text': 'เลือก <b>ฐาน C · Dual-view</b> เห็นระบบแนวระดับและแนวดิ่งที่ m, k เดียวกัน · <b>ทำนาย</b>ก่อนว่าคาบเท่ากันหรือไม่ แล้วจับเวลา 10 รอบทั้งสองระบบ<br><small>แรงโน้มถ่วงเพียงเลื่อนตำแหน่งสมดุลลงไป x₀ = mg/k ไม่เปลี่ยนคาบ</small>',
     'out': '<b>T</b><sub>ระดับ</sub> = <b>T</b><sub>ดิ่ง</sub> = 2π√(1.0/100) = 0.628 s' },
   { 'el': ['#view3d'], 'prep': "__clk('[data-base=\"A\"]'); __clk('[data-orient=\"v\"]'); resetSim(); setView('read')",
     'title': 'แนวดิ่ง: อ่าน x₀ แล้วหา k = mg/x₀',
     'text': 'เลือก <b>ฐาน A</b> แนว <b>↕ ดิ่ง</b> กด <b>🔍 อ่านสเกล</b> · อ่านไม้เมตรที่<b>ขีดเทา</b> (ปลายสปริงเมื่อยังไม่แขวนมวล) และ<b>ขีดส้ม</b> (ตำแหน่งสมดุลเมื่อแขวนมวล) ระยะห่าง = x₀<br>⑦ ที่สมดุล kx₀ = mg → <b>k = mg / x₀</b>',
     'out': '<b>x₀</b> = 9.8 cm = 0.098 m → <b>k</b> = (1.0 × 9.8) / 0.098 = <b>100 N/m</b>' },
   { 'el': '#rnd1Form', 'prep': "__clk('[data-orient=\"h\"]'); setManSub('random'); rndResetAll(); rndNewK1(); RND.k1True = 250; applyRndK1(); swReset(); { const d = 10 * period(250, S.m) + __LATE; SW.elapsed = d; $id('swDisplay').textContent = d.toFixed(2) + 's'; $id('rnd1t').value = d.toFixed(2); } rndCalc1(); setView('iso')",
     'title': 'โหมดสุ่ม ขั้น 1: หา k₁ ที่ซ่อนไว้',
     'text': 'เลือกแถบ <b>🎲 โหมดสุ่ม</b> กด <b>🎲 สุ่ม k₁ ใหม่</b> (ค่า k₁ แสดงเป็น ???) · กด ▶ เริ่ม แล้วใช้<b>นาฬิกาจับเวลา</b>บนสุดของแถบขวา จับเวลา 10 รอบ · กรอก <b>n</b> และ <b>t</b> แล้วกด <b>🧮 คำนวณ k₁</b> โปรแกรมเฉลยค่าจริงและ %error',
     'out': 't ≈ 4.02 s (10 รอบ) → <b>k₁</b> ≈ 244 N/m (ค่าจริงในภาพ 250 N/m · สุ่ม 50 – 400 N/m)' },
   { 'el': '#rndStage2', 'prep': "rndGotoStage2(); $id('rnd2k1v').value = 100; $id('rnd2k1').value = 100; rndSetConn(document.querySelector('[data-rconn=\"series\"]'), 'series'); rndNewK2(); RND.k2True = 150; applyRndK2(); { const d = 10 * period(calcKEff(), S.m) + __LATE; $id('rnd2t').value = d.toFixed(2); } rndCalc2()",
     'title': 'โหมดสุ่ม ขั้น 2: หา k₂ จากระบบ 2 สปริง',
     'text': 'กด <b>▶ ไปขั้น 2</b> เลือก <b>k₁ ที่รู้ = 100 N/m</b> การต่อ <b>อนุกรม</b> กด <b>🎲 สุ่ม k₂</b> · จับเวลา 10 รอบ กรอก n, t แล้วกด <b>🧮 คำนวณ</b><br>⑧ k = 4π²m/T² · อนุกรม <b>k₂ = 1 / (1/k − 1/k₁)</b> (ขนาน k₂ = k − k₁)',
     'out': '<b>k</b> ≈ 59 N/m → <b>k₂</b> ≈ 145 N/m (ค่าจริงในภาพ 150 N/m · สุ่ม 50 – 400 N/m)' },
  ],
 }
