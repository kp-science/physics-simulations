# -*- coding: utf-8 -*-
# Lab 17 แรงสู่ศูนย์กลาง (หลอดแก้ว–จุกยาง) — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'แกว่งจุกยางเป็นวงกลม จับเวลา n รอบ หาความสัมพันธ์ F = mv²/r',
  'setup': r"""
    /* ไม่เล่นแอนิเมชัน: ตั้งนาฬิกา/ตัวนับรอบของแลปเอง แล้วเรียก recordTrial() ของแลป (v = 2πrn/t)
       เวลาที่วัด = เวลาของ n รอบตามแบบจำลอง calcV(F, r, m) + ความช้าของมือที่กดหยุด (ตรึงไว้ให้ภาพตรงกับข้อความ) */
    window.__tN = n => 2 * Math.PI * state.r * n / calcV(state.F, state.r, state.m);
    window.__var = v => { const s = document.getElementById('sl-var'); s.value = v; s.dispatchEvent(new Event('input')); };
    window.__run = (n, tt) => { state.angle = 2 * Math.PI * n; state.swRunning = true; state.swRevs = Math.floor(n); state.swElapsed = tt; state.elapsed = tt; updateReadouts();
      const b = document.getElementById('swBtn'); b.textContent = '⏸ หยุดจับเวลา'; b.classList.add('running'); updateSWDisplay(); };
    window.__stop = () => { state.swRunning = false; const b = document.getElementById('swBtn'); b.textContent = '▶ เริ่มจับเวลา'; b.classList.remove('running'); updateSWDisplay(); };
    window.__rec = (v, d) => { __var(v); const n = EXPERIMENTS[state.exp].targetN; state.swRevs = n; state.swElapsed = __tN(n) + d; recordTrial(); };
    window.__exp = k => { selectExp(k); state.data[k] = []; updateTable(); drawGraph(); };
  """,
  'steps': [
   { 'el': ['.exp-selector', '.mode-row'], 'prep': "setMode('manual'); __exp('force'); setView('iso'); scrollTo(0,0)",
     'title': 'เลือกการทดลอง ① และโหมดบันทึกค่าเอง',
     'text': 'กด <b>① แปรผันแรงสู่ศูนย์กลาง</b> (เปลี่ยนมวลแขวน M คงรัศมี r และมวลจุก m) และโหมด <b>✋ บันทึกค่าเอง</b>',
     'out': 'คงที่: <b>r</b> = 0.50 m · <b>m</b> = 0.031 kg · นับ <b>n</b> = 20 รอบ' },
   { 'el': '#view3d', 'prep': "setView('iso')",
     'title': 'ดูชุดอุปกรณ์',
     'text': 'เชือกผูก<b>จุกยาง m</b> ลอดผ่าน<b>หลอดแก้ว</b>ลงไปแขวน<b>ตุ้มถ่วง M</b> · มือจับหลอดแกว่งให้จุกยางหมุนเป็นวงกลมในแนวระดับ · <b>มาร์กเกอร์ (คลิป)</b> บนเชือกใต้ปลายหลอดช่วยคุมรัศมี: ถ้ามาร์กเกอร์อยู่นิ่งที่เดิม รัศมี r คงตัว<br><small>แรงตึงเชือก = น้ำหนักตุ้มถ่วง Mg = แรงสู่ศูนย์กลางที่ดึงจุกยาง</small>',
     'out': '<b>F</b> = Mg (แรงสู่ศูนย์กลาง)' },
   { 'el': ['#fixedBox', '#paramsBox'], 'prep': "__var(0.1)",
     'title': 'ตั้งมวลแขวน M = 0.100 kg',
     'text': 'เลื่อน <b>M มวลแขวน</b> เป็น 0.100 kg โปรแกรมคำนวณแรง <b>F = Mg</b> ให้ (ช่องสีเทา) · ตั้ง <b>N รอบเป้าหมาย = 20</b> ในกรอบนาฬิกา',
     'out': '<b>F</b> = 0.100 × 9.8 = 0.98 N' },
   { 'el': ['#view3d', '#swBox'], 'prep': "resetSW(); __run(12.4, __tN(12.4)); setView('top')",
     'title': 'เริ่มหมุนและจับเวลาพร้อมกัน',
     'text': 'กด <b>▶ เริ่มจับเวลา</b> จุกยางเริ่มหมุน นาฬิกาเดินและ<b>นับรอบ</b>ไปพร้อมกัน · กด <b>⬇ มองจากด้านบน</b> เห็นเวกเตอร์ความเร็ว v ตามแนวสัมผัสวงกลม และแรง F ชี้เข้าหาจุดศูนย์กลาง' },
   { 'el': '#swBox', 'prep': "__run(20, __tN(20) + 0.20); state.swTargetReached = true; document.getElementById('targetReachedMsg').style.display = 'block'",
     'title': 'ครบ 20 รอบ → หยุดจับเวลา',
     'text': 'เมื่อขึ้นข้อความ <b>✅ ครบ 20 รอบแล้ว</b> กด <b>⏸ หยุดจับเวลา</b> ทันที · อ่านเวลา t และจำนวนรอบ n<br><small>นาฬิกาเดินต่อจนกว่าจะกดหยุด ถ้ากดช้า t จะเกินจริงเล็กน้อย</small>',
     'out': '<b>n</b> = 20 รอบ · <b>t</b> = 16.00 s' },
   { 'el': ['[onclick="recordTrial()"]', '#dataTable'], 'prep': "__stop(); recordTrial()",
     'title': 'บันทึกลงตาราง → โปรแกรมคำนวณ v',
     'text': 'กด <b>💾 บันทึกลงตาราง</b> โปรแกรมคำนวณต่อ:<br>① ระยะทางรวม <b>d = 2πrn</b> = 2π × 0.50 × 20 = 62.8 m<br>② อัตราเร็ว <b>v = d/t</b> = 62.8 / 16.00',
     'out': '<b>v</b> = 3.93 m/s (M = 0.100 kg, F = 0.98 N)' },
   { 'el': '#dataTable', 'prep': "__rec(0.2, 0.15); __rec(0.3, 0.22); __rec(0.4, 0.18)",
     'title': 'เปลี่ยน M แล้วทำซ้ำ',
     'text': 'ตั้ง M = 0.200, 0.300, 0.400 kg ทีละค่า แล้วจับเวลา 20 รอบ → บันทึก · แรงมากขึ้น จุกยางหมุนเร็วขึ้น ใช้เวลาน้อยลง',
     'out': 'F = 1.96 · 2.94 · 3.92 N → <b>t</b> = 11.33 · 9.34 · 8.08 s → <b>v</b> = 5.55 · 6.72 · 7.77 m/s' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "drawGraph()",
     'title': 'กราฟ F กับ v',
     'text': 'จุดข้อมูลเรียงเป็น<b>เส้นโค้งพาราโบลา</b> ไม่ใช่เส้นตรง · เส้นประ = ทฤษฎี F = mv²/r (m = 0.031 kg, r = 0.50 m) · จุดอยู่ใกล้เส้นประ',
     'out': 'F ไม่แปรผันตรงกับ v แต่เพิ่มเร็วกว่า → ลองเทียบกับ v²' },
   { 'el': '#dataTable',
     'title': 'วิเคราะห์: F แปรผันตรงกับ v²',
     'text': 'ยกกำลังสอง v ทุกแถว แล้วหาร F ด้วย v² (หรือเขียนกราฟ F กับ v² จะได้เส้นตรงผ่านจุดกำเนิด)<br>v² = 15.4 · 30.8 · 45.2 · 60.4 m²/s² → F/v² เกือบเท่ากันทุกแถว · ตามทฤษฎี F/v² = m/r = 0.031/0.50 = 0.062 kg/m',
     'out': '<b>F/v²</b> ≈ 0.064 kg/m ≈ m/r → <b>F ∝ v²</b> (มากกว่า 0.062 เล็กน้อยเพราะกดหยุดนาฬิกาช้า v จึงต่ำไปนิด)' },
   { 'el': ['#dataTable', '#graphCanvas'], 'prep': "__exp('radius'); __rec(0.6, 0.17); __rec(0.7, 0.21); __rec(0.8, 0.14); __rec(0.9, 0.19); drawGraph()",
     'title': 'การทดลอง ② เปลี่ยนรัศมี r',
     'text': 'กด <b>② แปรผันรัศมี</b> (m = 0.016 kg, F = 0.98 N คงที่ · นับ 10 รอบ) ตั้ง r = 0.60, 0.70, 0.80, 0.90 m (แถบเลื่อน หรือลากจุกยางในภาพ 3D) แล้วจับเวลาแบบเดิม · กราฟ v กับ r โค้ง (v ∝ √r)',
     'out': '<b>v</b> = 5.90 · 6.35 · 6.87 · 7.24 m/s → <b>v²/r</b> ≈ 58 m/s² ทุกแถว (ทฤษฎี F/m = 61) → <b>v² ∝ r</b>' },
   { 'el': ['#dataTable', '#graphCanvas'], 'prep': "__exp('mass'); __rec(0.022, 0.16); __rec(0.028, 0.20); __rec(0.036, 0.18); drawGraph()",
     'title': 'การทดลอง ③ เปลี่ยนมวลจุกยาง m',
     'text': 'กด <b>③ แปรผันมวลจุกยาง</b> (r = 1.00 m, F = 2.0 N คงที่ · นับ 10 รอบ) ตั้ง m = 0.022, 0.028, 0.036 kg แล้วจับเวลาแบบเดิม · จุกหนักขึ้น หมุนช้าลง (v ∝ 1/√m)',
     'out': '<b>v</b> = 9.31 · 8.23 · 7.30 m/s → <b>mv²</b> ≈ 1.91 N·m ทุกแถว (ทฤษฎี Fr = 2.0) → <b>v² ∝ 1/m</b>' },
   { 'el': '#view3d', 'prep': "__exp('force'); __var(0.1); state.angle = 1.2; state.elapsed = 1; setView('top')",
     'title': 'สรุปผล',
     'text': 'รวมผลทั้ง 3 การทดลอง: F ∝ v² (r, m คงที่) · v² ∝ r (F, m คงที่) · v² ∝ 1/m (F, r คงที่)<br>→ <b>F = mv²/r</b> · แรงสู่ศูนย์กลางชี้เข้าหาจุดศูนย์กลางวงกลม ตั้งฉากกับความเร็วเสมอ',
     'out': '<b>F<sub>c</sub> = mv²/r</b> · mv²/r จากค่าที่วัด ≈ 95 – 97% ของ F (ต่ำไปเล็กน้อยเพราะกดหยุดนาฬิกาช้า)' },
  ],
 }
