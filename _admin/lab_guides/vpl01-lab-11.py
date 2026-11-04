# -*- coding: utf-8 -*-
# Lab 11 รางอากาศ — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'จับเวลา glider บนรางอากาศ หาความเร่งจาก a = 2s/t² และกราฟ s–t²',
  'setup': r"""
    /* ไม่ปล่อยให้แลปวิ่งเอง: __at(t) = ตำแหน่ง glider ตามแบบจำลองของแลป (s = ½at², a = g sin A)
       __click(r, i) = กด 💾 ในรอบที่ r ตอน glider ผ่านขีด DISTANCES[i] ช้า/เร็วกว่าจริง __E วินาที (ปฏิกิริยาคน) → manualClick() ของแลป */
    window.__el = id => document.getElementById(id);
    window.__ang = A => { __el('sl-angle').value = A; __el('sl-angle').dispatchEvent(new Event('input')); };
    window.__at = tt => { const a = getAcc(); t_elapsed = tt; v_current = a * tt; glider_s = 0.5 * a * tt * tt; drawTrack(); updateReadout(); updateStopwatchDisplay(); };
    window.__E = [0.04, -0.03, 0.06, 0.02, -0.05, 0.01, 0.05, -0.02, 0.03, -0.04, 0.00, 0.06, -0.01, 0.04, -0.03, 0.02, 0.05, -0.02, 0.01, 0.03];
    window.__tOf = s => Math.sqrt(2 * s / getAcc());
    window.__click = (r, i) => { __at(__tOf(DISTANCES[i]) + __E[(r * 5 + i) % 20]); manualClick(); };
    window.__run = r => { for (let i = 0; i < 5; i++) __click(r, i); __at(__tOf(155)); };
    window.__clr = () => { tableData.forEach(r => { r.trials = ['', '', '', '']; r._autoRecorded = false; }); resetGlider(); renderTable(); drawGraph(); };
  """,
  'steps': [
   { 'el': '#view3d', 'prep': "setMode('manual'); __clr(); __ang(0.9); setView('iso'); scrollTo(0,0)",
     'title': 'ดูอุปกรณ์รางอากาศ',
     'text': '<b>รางอากาศ</b>ยาว 1.5 m พ่นอากาศออกจากรูเล็ก ๆ ทำให้ <b>glider</b> ลอยเหนือราง แรงเสียดทานน้อยมาก · ยกขาข้างหนึ่งให้รางเอียงมุม A เล็ก ๆ · ข้างรางมีสเกล (cm) และขีดระยะ 30, 60, 90, 120, 150 cm · นาฬิกาจับเวลาอยู่ด้านหลัง<br><small>glider ไถลลงด้วยความเร่ง a = g sin A</small>',
     'out': 'glider เริ่มนิ่งที่ s = 0 cm' },
   { 'el': ['#mode-manual', '#vi-angle', '#vi-speed'],
     'title': 'ตั้งโหมดและมุมเอียง',
     'text': 'เลือก <b>⏱ จับเวลาเอง</b> · ตั้ง <b>มุมเอียง A = 0.9°</b> · <b>ตัวคูณความเร็ว 1×</b> (ลดเป็น 0.5× ถ้ากดไม่ทัน — นาฬิกาใช้เวลาจำลอง ค่าที่วัดไม่เปลี่ยน)',
     'out': '<b>A</b> = 0.9° (sin A = 0.0157)' },
   { 'el': ['#playBtn', '#stopwatchBox'], 'prep': "__at(1.2); __el('playBtn').textContent = '⏸ หยุด (pause)'; __el('playBtn').classList.add('playing'); __el('stopwatchBox').classList.add('running')",
     'title': 'ปล่อย glider พร้อมเริ่มจับเวลา',
     'text': 'กด <b>▶ ปล่อย Glider & เริ่มจับเวลา</b> glider เริ่มไถลจากหยุดนิ่ง นาฬิกาเริ่มเดินพร้อมกัน · มองที่ขีดระยะ 30 cm รอ glider ผ่าน' },
   { 'el': ['#recordBtn', '#view3d'], 'prep': "__click(0, 0); setView('zoom')",
     'title': 'glider ผ่านขีด 30 cm → กดบันทึกเวลา',
     'text': 'กด <b>🔍 ซูมอ่านค่า</b> ภาพตาม glider · เมื่อ<b>ขีดชี้สีส้มที่กึ่งกลาง glider ตรงขีด 30 cm</b> กด <b>💾 บันทึกเวลา</b> ทันที เวลาบนนาฬิกาลงตารางแถวระยะที่ใกล้ glider ที่สุด<br><small>glider ไม่หยุด นาฬิกาเดินต่อ เตรียมกดที่ขีดถัดไป</small>',
     'out': 's = 30 cm → <b>t</b> = 2.01 s (ครั้งที่ 1)' },
   { 'el': '.data-table', 'prep': "for (let i = 1; i < 5; i++) __click(0, i); __at(__tOf(155)); __el('playBtn').textContent = '▶ ปล่อย Glider & เริ่มจับเวลา'; __el('playBtn').classList.remove('playing'); setView('iso')",
     'title': 'กดต่อที่ 60, 90, 120, 150 cm',
     'text': 'ในการปล่อยครั้งเดียว กด 💾 ทุกครั้งที่ glider ผ่านขีด 60, 90, 120 และ 150 cm · ได้เวลาครบ 5 ระยะในคอลัมน์ <b>ครั้งที่ 1</b><br><small>ถ้ากดผิดแถว แก้ตัวเลขในช่องได้โดยตรง</small>',
     'out': 's = 30 · 60 · 90 · 120 · 150 cm → <b>t</b> = 2.01 · 2.76 · 3.48 · 3.97 · 4.36 s' },
   { 'el': '.data-table', 'prep': "for (let r = 1; r < 4; r++) { resetGlider(); __run(r); } resetGlider(); renderTable(); drawGraph()",
     'title': 'Reset แล้ววัดซ้ำให้ครบ 4 ครั้ง',
     'text': 'กด <b>↺ Reset</b> glider กลับจุดเริ่ม นาฬิกาเป็น 0 · ปล่อยและกดบันทึกแบบเดิมอีก 3 รอบ เวลาลงคอลัมน์ครั้งที่ 2–4 · โปรแกรมคำนวณ<br>① <b>t̄</b> = ค่าเฉลี่ยของ 4 ครั้ง',
     'out': '<b>t̄</b> = 1.99 · 2.82 · 3.42 · 3.98 · 4.39 s' },
   { 'el': '.data-table',
     'title': 'โปรแกรมคำนวณ t̄² และ a ทุกแถว',
     'text': 'จาก s = ½at² (ปล่อยจากหยุดนิ่ง u = 0) แต่ละแถวคำนวณต่อ<br>② <b>t̄²</b><br>③ <b>a = 2s / t̄²</b><br>ค่า a ทุกแถวใกล้เคียงกัน แปลว่าความเร่งคงตัวตลอดราง',
     'out': '<b>t̄²</b> = 3.95 · 7.97 · 11.71 · 15.80 · 19.25 s²<br><b>a</b> = 15.19 · 15.06 · 15.37 · 15.19 · 15.58 cm/s² (เฉลี่ย ≈ 15.3 cm/s²)' },
   { 'el': ['#val-ac', '#val-at', '#val-err'],
     'title': 'เทียบกับค่าทฤษฎี',
     'text': 'กรอบสรุปใช้แถว s = 150 cm<br>④ <b>a(c) = 2s/t̄²</b> = 2 × 150 / 4.39²<br>⑤ <b>a(t) = g sin A</b> = 980 × sin 0.9°<br>⑥ <b>ความคลาดเคลื่อน = |a(c) − a(t)| / a(t) × 100%</b> (สีเขียวเมื่อน้อยกว่า 5%)',
     'out': '<b>a(c)</b> = 15.58 cm/s² · <b>a(t)</b> = 15.39 cm/s² · คลาดเคลื่อน <b>1.2 %</b>' },
   { 'el': '#graphCanvas', 'prep': "drawGraph()",
     'title': 'กราฟ s กับ t̄²',
     'text': 'จุดสีเขียว (t̄², s) ทั้ง 5 จุดเรียงเป็น<b>เส้นตรงผ่านจุดกำเนิด</b> และอยู่บนเส้นประทฤษฎี s = ½at² → การเคลื่อนที่มีความเร่งคงตัว<br>⑦ <b>ความชัน = a/2</b> → a = 2 × ความชัน<br><small>เส้นประเป็นค่าทฤษฎีที่โปรแกรมวาดให้ · ความชันของจุดที่วัดได้ ให้ลากเส้นตรงเองแล้วคำนวณ</small>',
     'out': 'ความชัน ≈ 7.69 cm/s² → <b>a</b> ≈ 15.4 cm/s²' },
   { 'el': '.data-table', 'prep': "__clr(); __ang(2.0); for (let r = 0; r < 4; r++) { resetGlider(); __run(r); } __clr(); __ang(3.0); for (let r = 0; r < 4; r++) { resetGlider(); __run(r); } resetGlider(); renderTable(); drawGraph()",
     'title': 'เปลี่ยนมุมเอียง แล้วทำทั้งชุดใหม่',
     'text': 'กด <b>🗑 ลบข้อมูลทั้งหมด</b> ก่อน (ตารางไม่ล้างเองเมื่อเปลี่ยนมุม) · ตั้ง <b>A = 2.0°</b> วัดครบ 5 ระยะ × 4 ครั้ง จดค่า a · แล้วทำซ้ำที่ <b>A = 3.0°</b> (ในภาพ) · มุมมากขึ้น glider ถึงปลายรางเร็วขึ้น',
     'out': 'A = 2.0°: a เฉลี่ยทุกแถว ≈ 33.9 cm/s² (ทฤษฎี 34.20)<br>A = 3.0°: t̄ = 1.10 · 1.56 · 1.87 · 2.19 · 2.40 s → a เฉลี่ย ≈ 50.6 cm/s² (ทฤษฎี 51.29)' },
   { 'el': ['#readout-a', '#readout-ang'],
     'title': 'สรุป: a กับ sin A → หาค่า g',
     'text': 'เขียนกราฟ <b>a กับ sin A</b> (sin 0.9° = 0.0157 · sin 2.0° = 0.0349 · sin 3.0° = 0.0523) ได้เส้นตรงผ่านจุดกำเนิด → <b>a ∝ sin A</b><br>⑧ จาก a = g sin A → <b>ความชัน = g</b>',
     'out': 'a = 15.3 · 33.9 · 50.6 cm/s² → ความชัน ≈ 967 cm/s² → <b>g</b> ≈ 9.7 m/s² (ค่าจริง 9.8 m/s²)' },
  ],
}
