# -*- coding: utf-8 -*-
# Lab 20 calibrate ยางยืดบนรางอากาศ — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ระยะยืดจริง = stretchForForce(mg) ของแลป (F = 2500·h^1.5) · ค่าที่นักเรียนอ่าน caliper = ค่าจริง ± ≤0.02 mm (ตรึงไว้ ภาพตรงกับข้อความ)
GUIDE = {
  'title': 'calibrate ยางยืด: กราฟแรง F กับระยะยืด h และพลังงานในยาง',
  'setup': r"""
    /* จบการทดลอง 1 แถวทันที (แทนรอภาพเคลื่อนไหว 2.2 s) — ทำแบบเดียวกับตอนจบ animLoop() ของแลป */
    window.__done = i => { cancelAnimationFrame(animId); state.running = false; selectRow(i);
      state.stretchEq = stretchForForce(PRESET_MASSES[i] * G); state.stretchCur = state.stretchEq;
      state.running = false; state.stopped = true; state.t = 3; $('btn-launch').disabled = false;
      setupCaliperForMeasurement(); updateRecordBtn(); updateOutputs(); renderTable(); draw(); };
    /* ค่าที่อ่านจาก caliper (mm) = ระยะยืดจริง + ความคลาดเคลื่อนการเล็งเล็กน้อย */
    window.__NZ = [0.01, -0.02, 0.00, 0.02, -0.01, 0.01, -0.02, 0.01, 0.00, -0.01];
    window.__cal = i => { state.caliper.y1 = 0; state.caliper.y2 = Math.round((state.stretchEq * 1000 + __NZ[i]) * 100) / 100; state.caliper.initialized = true; updateOutputs(); draw(); };
    window.__rec = i => { __done(i); __cal(i); manualRecord(); };
    window.__clr = () => { tableData.forEach(r => { r.stretch = null; r.pe = null; }); renderTable(); drawChart(); };
  """,
  'steps': [
   { 'el': ['#view3d', '#sl-angle', '#mode-manual'], 'prep': "setMode('manual'); __clr(); $('sl-angle').value = 0; $('vi-angle').value = 0; state.angleDeg = 0; resetSim(); selectRow(0); setView('iso'); scrollTo(0,0)",
     'title': 'ตั้งรางแนวระดับ เลือกบันทึกเอง',
     'text': 'ตั้ง <b>มุมเอียงราง = 0°</b> (แนวระดับ) และกด <b>✍️ บันทึกเอง</b> · ยางยืดผูกระหว่างหมุดปลายรางกับ glider ส่วนอีกด้านของ glider ผูกเชือกข้ามรอกไปห้อย<b>ถ้วยทราย</b><br><small>ลมจากรางทำให้ glider ลอย ไม่มีแรงเสียดทาน แรงที่ดึงยางจึงเท่ากับน้ำหนักถ้วยพอดี</small>',
     'out': 'มุมราง = 0° · glider อยู่ที่ตำแหน่งยางยังไม่ยืด' },
   { 'el': '#calTbody', 'prep': "selectRow(0)",
     'title': 'เลือกมวลถ้วยทรายแถวแรก',
     'text': 'แตะ<b>แถวที่ 1</b> ในตาราง (แถวเป็นสีฟ้า) · คอลัมน์ 1 คือมวลถ้วยกับทราย และคอลัมน์ 2 คำนวณน้ำหนักให้<br>① <b>F = mg</b> (g = 9.8 m/s²)',
     'out': '<b>m</b> = 0.010 kg → <b>F</b> = 0.010 × 9.8 = 0.0980 N' },
   { 'el': ['#btn-launch', '#view3d'], 'prep': "__done(0); setView('iso')",
     'title': 'กดทดลอง ถ้วยตกดึงยางจนสมดุล',
     'text': 'กด <b>🧪 ทดลองแถวที่เลือก</b> ถ้วยตกลงดึง glider ผ่านเชือก ยางยืดออกจนแรงดึงกลับของยางเท่ากับน้ำหนักถ้วย แล้วหยุดนิ่ง · รอจนแถบใต้ภาพขึ้น <b>✓ สมดุลแล้ว</b><br><small>เชือกไม่ยืด ระยะที่ถ้วยลดระดับลง = ระยะที่ยางยืด h</small>',
     'out': 'สมดุล: <b>F<sub>ยาง</sub> = mg</b>' },
   { 'el': ['#view3d', '#out-caliper'], 'prep': "setView('read'); __cal(0)",
     'title': 'วัดระยะยืด h ด้วย caliper',
     'text': 'กด <b>🔍 ซูมอ่านสเกล</b> · ปาก <b>A</b> ของ caliper สีเหลืองอยู่ที่<b>เส้นเริ่ม (เขียว)</b> = ขอบถ้วยก่อนตก · ลาก<b>ปุ่ม B</b> ลงให้เส้นเล็งตรง<b>เส้นส้ม</b> = ขอบถ้วยตำแหน่งใหม่ · ระยะห่างของปาก A กับ B คือ h อ่านได้ที่ป้ายในภาพ และช่อง <b>caliper อ่านได้</b>',
     'out': '<b>h</b> = 1.160 mm = 0.001160 m' },
   { 'el': ['#btn-record', '#calTbody tr:first-child'], 'prep': "manualRecord(); setView('iso')",
     'title': 'บันทึกค่า caliper → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึกค่า caliper ลงตาราง</b> ค่า h ลงคอลัมน์ 3 แล้วโปรแกรมคำนวณคอลัมน์ 4<br>② พลังงานศักย์โน้มถ่วงที่ถ้วยเสียไป <b>ΔE<sub>p</sub> = mgh</b> = 0.0980 × 0.001160',
     'out': '<b>h</b> = 1.160 mm · <b>mgh</b> = 0.000114 J' },
   { 'el': '#calTable', 'prep': "for (let i = 1; i < 10; i++) __rec(i); selectRow(9); __done(9); __cal(9); setView('iso')",
     'title': 'ทำซ้ำทุกมวล 0.010 – 0.100 kg',
     'text': 'แตะแถวถัดไป (หรือกด <b>▶ ทดลอง</b> ท้ายแถว) แล้ววัด h และบันทึกแบบเดิมจน<b>ครบ 10 แถว</b> · มวลเพิ่มทีละ 0.010 kg แรง F เพิ่มทีละเท่ากัน แต่ h เพิ่มน้อยลงเรื่อย ๆ<br><small>ปาก A อยู่ที่เส้นเริ่มให้ทุกครั้ง ลากเฉพาะปุ่ม B</small>',
     'out': '<b>h</b> (mm) = 1.160 · 1.810 · 2.400 · 2.930 · 3.360 · 3.820 · 4.200 · 4.630 · 4.990 · 5.350' },
   { 'el': '#chartCanvas', 'prep': "drawChart()",
     'title': 'กราฟ F กับ h → พื้นที่ใต้กราฟ',
     'text': 'จุดสีเขียว = (h, F) ทุกแถว · จุดเรียงเป็น<b>เส้นโค้งขึ้น</b> ไม่เป็นเส้นตรง แสดงว่ายางยืด<b>ไม่เป็นไปตามกฎของฮุก</b> (ยางแข็งขึ้นเมื่อยืดมาก) · เส้นชมพูคือแบบจำลองของยาง F = k h<sup>1.5</sup><br>③ พลังงานศักย์ยืดหยุ่นในยาง <b>E<sub>p</sub> = พื้นที่ใต้กราฟ F–h</b> ≈ Σ ½(F<sub>1</sub>+F<sub>2</sub>)Δh (สี่เหลี่ยมคางหมูทีละช่อง เริ่มจากจุดกำเนิด h = 0, F = 0)',
     'out': '<b>E<sub>p ยาง</sub></b> ≈ 0.00211 J เมื่อยืด 5.35 mm (ที่กราฟบอก "PE สะสม" · แบบจำลอง ∫F dh = 0.00209 J)' },
   { 'el': ['#calTbody tr:last-child', '#chartCanvas'],
     'title': 'สรุป: ใช้กราฟเป็นตาราง calibrate',
     'text': 'กราฟนี้ใช้หาพลังงานในยางที่ระยะยืดใด ๆ ได้ (อ่านพื้นที่ใต้กราฟตั้งแต่ 0 ถึง h นั้น) — ใช้ต่อในการทดลองการเปลี่ยนรูปพลังงาน<br>เทียบกับคอลัมน์ 4: แถวสุดท้าย mgh = 0.98 × 0.00535 = 0.00524 J มากกว่าพื้นที่ใต้กราฟ เพราะถ้วยตกเร่งแล้วแกว่งก่อนหยุด พลังงานส่วนหนึ่งกลายเป็นความร้อน',
     'out': '<b>E<sub>p ยาง</sub></b> ≈ 2.1 × 10⁻³ J (ยืด 5.35 mm ด้วยแรง 0.98 N) · E<sub>p ยาง</sub> ≈ 0.4 mgh · ยางไม่เป็นไปตามกฎของฮุก' },
  ],
 }
