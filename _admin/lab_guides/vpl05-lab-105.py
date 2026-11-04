# -*- coding: utf-8 -*-
# Lab 105 สมการความต่อเนื่อง — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'วัดอัตราการไหลและความเร็วในท่อ 3 ช่วง ตรวจ A₁v₁ = A₂v₂ = Q แล้วหาขนาดท่อ X',
  'setup': r"""
    /* หยุดเวลาของแลป (simSpeed = 0) แล้วเดินแบบจำลองของแลปเอง stepPhys() · ปักอัตราการไหลของวาล์ว 4 ระดับ
       ให้ภาพตรงกับข้อความ (แลปจริงสุ่ม ±7%) · เส้นผ่านศูนย์กลางท่อ X ยังสุ่มตามแลป (เป็น const ปักไม่ได้) */
    simSpeed = 0; QL[0] = 8.4; QL[1] = 15.2; QL[2] = 22.6; QL[3] = 31.5;
    window.__col = V => { let k = 0; while (collecting && bV < V - 1e-6 && k++ < 20000) stepPhys(0.01); };
    window.__Q = (l, V) => { setLvl(l); emptyBeaker(); toggleCollect(); __col(V); toggleCollect(); setKind('q'); $('in-1').value = V; $('in-2').value = swT.toFixed(2); recordRow(); };
    window.__dye = () => { injectDye(); let k = 0; while (dye && !dye.done && k++ < 20000) stepPhys(0.02); };
    window.__rd = s => { const F = flashes.filter(x => x > secX0(s) + 1 && x < secX1(s) - 0.5), sp = F[1] - F[0];
      const n = Math.max(1, Math.min(20, Math.floor(22 / sp), F.length - 1)); return { x0: F[0], n, d: +(F[n] - F[0]).toFixed(1) }; };
    window.__put = s => { const m = __rd(s); RX = m.x0; setKind('v'); $('in-sec').value = s; $('in-1').value = m.d.toFixed(1); $('in-2').value = m.n; return m; };
    window.__lvl = (l, V) => { __Q(l, V); __dye(); [0, 1, 2].forEach(s => { __put(s); recordRow(); }); };
    window.__R = id => setTimeout(() => { const w = $(id); w.scrollLeft = 1e4; w.scrollTop = 1e4; }, 500);
  """,
  'steps': [
   { 'el': '#view3d', 'prep': "setMode('manual'); rows = []; resetLab(); renderAll(); setView('iso'); scrollTo(0,0)",
     'title': 'ดูอุปกรณ์',
     'text': 'ถังน้ำระดับคงที่ปล่อยน้ำผ่าน<b>วาล์ว</b>เข้าท่อใสแนวระดับ 3 ช่วง (ยาวช่วงละ 28 cm) ต่อกัน: <b>A</b> กว้าง 2.0 cm · <b>B</b> 1.0 cm · <b>X</b> ไม่ทราบ · น้ำพุ่งออกปลายท่อลงถาด · มี<b>บีกเกอร์</b>กับ<b>นาฬิกา</b>สำหรับวัด Q · <b>หลอดฉีดสี</b> + กล้องแฟลช และ<b>ไม้บรรทัดใส</b>สำหรับวัด v<br>หาพื้นที่หน้าตัดไว้ก่อน <b>A = πD²/4</b>',
     'out': '<b>A<sub>A</sub></b> = π(2.0)²/4 = 3.14 cm² · <b>A<sub>B</sub></b> = π(1.0)²/4 = 0.785 cm²' },
   { 'el': '#lvlBtns', 'prep': "setLvl(0)",
     'title': 'ตั้งวาล์วระดับ 1',
     'text': 'ในแผงขวา กด <b>ระดับ 1</b> (หรือแตะวาล์วในภาพ) · แลปไม่บอกอัตราการไหลของแต่ละระดับ ต้องวัดเอง · <b>ห้ามเปลี่ยนวาล์ว</b>จนกว่าจะวัด Q และ v ทั้ง 3 ช่วงของระดับนี้ครบ',
     'out': 'ช่อง <b>① วาล์ว</b> = วาล์วระดับ 1' },
   { 'el': ['#view3d', '#ab-col'], 'prep': "emptyBeaker(); toggleCollect(); __col(48); setView('iso'); orbit.target.set(46, 7, 0); orbit.dist = fitDist(40, 22)",
     'title': 'เริ่มเก็บน้ำ',
     'text': 'กด <b>🥛 เริ่มเก็บน้ำ</b> บีกเกอร์เลื่อนไปรองสายน้ำที่ปลายท่อ และ<b>นาฬิกาเริ่มเดินเอง</b>เมื่อน้ำเริ่มลงบีกเกอร์ · รอราว 10 วินาที<br><small>เก็บนานขึ้น ปริมาตรมากขึ้น ความคลาดเคลื่อนจากการอ่านขีด 5 mL จึงน้อยลง</small>' },
   { 'el': ['#view3d', '#in-1'], 'prep': "__col(100); toggleCollect(); setKind('q'); setView('bk'); $('in-1').value = 100",
     'title': 'หยุดเก็บน้ำ แล้วอ่านปริมาตร V',
     'text': 'กด <b>⏹ หยุดเก็บน้ำ</b> (นาฬิกาหยุดพร้อมกัน) · กด <b>🥛 บีกเกอร์</b> ซูมอ่านระดับน้ำ (ขีดละ 5 mL) มองให้สายตาระดับเดียวกับผิวน้ำ · กรอกช่อง <b>② ปริมาตรน้ำ V</b>',
     'out': '<b>V</b> = 100 mL = 100 cm³' },
   { 'el': ['#view3d', '#in-2'], 'prep': "setView('sw'); $('in-2').value = swT.toFixed(2)",
     'title': 'อ่านเวลาที่เก็บ t',
     'text': 'กด <b>⏱ นาฬิกา</b> อ่านเวลาที่เก็บน้ำ (ละเอียด 0.01 s) กรอกช่อง <b>③ เวลาที่เก็บ t</b>',
     'out': '<b>t</b> = 11.91 s' },
   { 'el': ['#lastRec', '#recForm .rf-btn'], 'prep': "recordRow(); setView('iso')",
     'title': 'บันทึกแบบ "อัตราการไหล Q"',
     'text': 'ปุ่มแบบบันทึกเลือก <b>อัตราการไหล Q</b> อยู่แล้ว กด <b>📝 บันทึก</b> → โปรแกรมคำนวณ<br><b>Q = V/t</b> (1 mL = 1 cm³)',
     'out': '<b>Q</b> = 100/11.91 = 8.40 mL/s (cm³/s)' },
   { 'el': ['#view3d', '#ab-dye'], 'prep': "injectDye(); { let k = 0; while (dye.x < secX0(1) + 18 && k++ < 9000) stepPhys(0.02); } setView('iso'); orbit.target.set(-14, 15, 0); orbit.dist = fitDist(70, 20)",
     'title': 'ฉีดสี + ถ่ายภาพแฟลช',
     'text': 'กด <b>💉 ฉีดสี + แฟลช</b> สีแดงไหลไปตามท่อพร้อมน้ำ กล้องถ่ายภาพ<b>แฟลชทุก 0.10 s</b> เหลือรอยหน้าสี (วงแดง) บนท่อ · รอจนสีไหลถึงปลายท่อ<br><small>ในช่วง A รอยชิดกัน (ไหลช้า) ในช่วง B รอยห่างกันมาก (ไหลเร็ว)</small>' },
   { 'el': ['#view3d', '#wSec'], 'prep': "{ let k = 0; while (dye && !dye.done && k++ < 20000) stepPhys(0.02); } __put(0); setView('rul'); curView = 'free'; orbit.target.set(RX + 3.3, PY - 0.6, 1.4); orbit.dist = fitDist(9, 4)",
     'title': 'วัดระยะระหว่างรอยในช่วง A',
     'text': 'ปุ่มแบบบันทึกเปลี่ยนเป็น <b>ความเร็วในท่อ v</b> ให้เอง · เลือก <b>ช่วง A</b> · <b>ลากไม้บรรทัด</b> (หรือ ◀ ▶) ให้<b>ขีด 0</b> ตรงรอยหนึ่ง กด <b>📏 ไม้บรรทัด</b> นับไปอีก <b>n ช่วงแฟลช</b> แล้วอ่านระยะ <b>d</b> · กรอก d และ n<br><small>รอยในท่อกว้างชิดกัน ให้นับหลายช่วง (n มาก) ความคลาดเคลื่อนจะน้อยลง</small>',
     'out': '<b>n</b> = 20 ช่วง (เวลา 20 × 0.10 = 2.0 s) · <b>d</b> = 5.4 cm' },
   { 'el': ['#lastRec', '#recForm .rf-btn'], 'prep': "recordRow()",
     'title': 'บันทึก → คำนวณ v และ A v',
     'text': 'กด <b>📝 บันทึก</b> โปรแกรมคำนวณต่อ:<br>① ความเร็วในช่วงนั้น <b>v = d/(n × 0.10 s)</b><br>② <b>A v</b> (พื้นที่หน้าตัด × ความเร็ว) แล้วแสดงคู่กับ Q ที่วัดจากบีกเกอร์',
     'out': '<b>v<sub>A</sub></b> = 5.4/2.0 = 2.70 cm/s · <b>A v</b> = 3.14 × 2.70 = 8.48 mL/s ≈ Q (8.40 mL/s · ต่างกันราว 1%)' },
   { 'el': ['#view3d', '#lastRec'], 'prep': "__put(1); setView('rul'); recordRow()",
     'title': 'ช่วง B: วัดแล้วบันทึก',
     'text': 'เลือก <b>ช่วง B</b> เลื่อนไม้บรรทัดไปช่วง B ทำแบบเดิม · รอยห่างกันมากขึ้นราว 4 เท่า เพราะท่อแคบลงครึ่งหนึ่ง พื้นที่เหลือ 1/4',
     'out': '<b>n</b> = 20 · <b>d</b> = 21.4 cm → <b>v<sub>B</sub></b> = 10.70 cm/s · <b>A v</b> = 0.785 × 10.70 = 8.40 mL/s · v<sub>B</sub>/v<sub>A</sub> ≈ 4 = (D<sub>A</sub>/D<sub>B</sub>)²' },
   { 'el': ['#view3d', '#lastRec'], 'prep': "__put(2); setView('rul'); recordRow()",
     'title': 'ช่วง X: วัด v แล้วหาขนาดท่อ',
     'text': 'เลือก <b>ช่วง X</b> วัดแบบเดิม · ขนาดท่อ X ไม่ทราบ โปรแกรมจึงคำนวณย้อนจากสมการความต่อเนื่อง:<br>① <b>A<sub>X</sub> = Q / v<sub>X</sub></b><br>② <b>D<sub>X</sub> = √(4A<sub>X</sub>/π)</b><br><small>ขนาดท่อ X สุ่มใหม่ทุกครั้งที่เปิดแลป · ตัวเลขในภาพเป็นตัวอย่างหนึ่ง</small>',
     'out': '<b>v<sub>X</sub></b> = d/(n × 0.10) · <b>A<sub>X</sub></b> = 8.40 / v<sub>X</sub> (cm²) · <b>D<sub>X</sub></b> (cm) ดูในผลที่บันทึกล่าสุด' },
   { 'el': '#tableB', 'prep': "__lvl(1, 150); __lvl(2, 225); __lvl(3, 315); __R('tableB')",
     'title': 'ทำซ้ำที่วาล์วระดับ 2 – 4',
     'text': 'เปลี่ยนวาล์วทีละระดับ แล้วทำซ้ำทุกขั้น: เก็บน้ำหา Q → ฉีดสี → วัด v ทั้ง 3 ช่วง · ดูตาราง ② คอลัมน์ <b>A v</b> เทียบกับ <b>Q วัด</b> ในแถวเดียวกัน<br><small>ตาราง ① เก็บ V, t และ Q ของทุกระดับ · แถวช่วง X เป็นสีชมพู (A มีเครื่องหมาย * = คำนวณจาก Q/v)</small>',
     'out': 'Q = 8.40 · 15.2 · 22.6 · 31.5 mL/s · ทุกแถว <b>A v ≈ Q</b> (คลาดไม่เกินราว 2%) → <b>A₁v₁ = A₂v₂ = Q</b>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "drawGraph()",
     'title': 'กราฟ v – Q ของแต่ละช่วง',
     'text': 'จาก v = Q/A จุดของแต่ละช่วงเรียงเป็นเส้นตรงผ่านจุดกำเนิด <b>ความชัน = 1/A</b> · ท่อแคบเส้นชันมาก<br>① A = 1/ความชัน ② D = √(4A/π) · ใต้กราฟคำนวณ D ของทุกช่วงให้ ตรวจว่า A ได้ ≈ 2.0 cm และ B ≈ 1.0 cm',
     'out': 'ช่วง A: ความชัน ≈ 0.319 cm⁻² → D ≈ 2.0 cm · ช่วง B: ≈ 1.27 cm⁻² → D ≈ 1.0 cm · ช่วง X: <b>D<sub>X</sub></b> จากความชันเส้นสีชมพู' },
   { 'el': ['#ans-d', '#ansDMsg'], 'prep': "{ const X = rows.filter(r => r.k === 'v' && r.sec === 2).map(r => Math.sqrt(4 * qMeas(r.lvl) / (r.d / (r.n * FLASH)) / Math.PI)); $('ans-d').value = (X.reduce((a, b) => a + b, 0) / X.length).toFixed(2); } checkD()",
     'title': 'กรอกเส้นผ่านศูนย์กลางท่อ X แล้วตรวจ',
     'text': 'ใช้ <b>D<sub>X</sub> เฉลี่ย</b> ใต้ตาราง ② (หรือค่าจากความชันกราฟ) กรอกในกรอบ <b>🎯 ตรวจคำตอบ</b> กด <b>ตรวจ</b> · ถือว่าถูกเมื่อคลาดไม่เกิน 4%',
     'out': '✓ <b>D<sub>X</sub></b> ของท่อปริศนา (สุ่มในช่วง 0.80 – 1.80 cm)' },
  ],
 }
