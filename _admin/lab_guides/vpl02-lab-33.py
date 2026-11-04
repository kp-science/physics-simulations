# -*- coding: utf-8 -*-
# Lab 33 การหักเหของคลื่นน้ำ (ถาดคลื่น 3D) — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# λ, v, θr มาจากแบบจำลองของแลป (solveDispersion + calcPhysics: น้ำลึก 10 mm · น้ำตื้น 2 mm)
# หมุดวัดปักบนยอดคลื่นจริงของภาพ (labField: สันคลื่นที่ kD·u − ωt = π/2 + 2πn) คลาดเล็กน้อยแบบมือคน · มุมอ่านโปรแทรกเตอร์ปัดเป็นองศาเต็ม
GUIDE = {
  'title': 'วัด λ น้ำลึก–น้ำตื้น และมุมหักเห ตรวจกฎของสเนลล์ sin θr / sin θi = λS / λD',
  'setup': r"""
    if (window.__kpSpeed) __kpSpeed.set(0);
    window.__set = (id, v) => { gid('sl-' + id).value = v; gid('vi-' + id).value = v; onSliderChange(); };
    window.__T = 1.3;
    window.__still = () => { if (isPlaying) togglePlay(); t = __T; draw(); };
    /* ยอดคลื่น (สันสว่าง) ใกล้ตำแหน่ง u0 ในฝั่งน้ำลึก / น้ำตื้น (มุมขอบ 0°) */
    window.__crestD = u0 => { const ph = omega * t; const n = Math.round((kD * u0 - ph - Math.PI / 2) / (2 * Math.PI)); return (Math.PI / 2 + 2 * Math.PI * n + ph) / kD; };
    window.__crestS = u0 => { const ph = omega * t, off = kD * BND_U - kS * BND_U; const n = Math.round((kS * u0 + off - ph - Math.PI / 2) / (2 * Math.PI)); return (Math.PI / 2 + 2 * Math.PI * n + ph - off) / kS; };
    window.__mark = (u1, lam, d) => { if (!measuring) toggleMeasure(); markers = [{ x: u1, y: 12 }, { x: u1 + lam + d, y: 12 }]; updateMeasureDisplay(); draw(); };
    window.__dist = () => Math.hypot(markers[1].x - markers[0].x, markers[1].y - markers[0].y).toFixed(2);
    window.__last = n => document.querySelector('#tbody' + n + ' tr:last-child');
    window.__fill = (n, vals, calc) => { const tr = __last(n), ins = tr.querySelectorAll('input'); vals.forEach((v, i) => { if (v !== null) ins[i].value = v; }); calc(tr); };
    /* วัด λ ทั้งสองฝั่งที่ความถี่ f แล้วบันทึก 1 แถว (การทดลอง I) */
    window.__row1 = (f, dD, dS) => { __set('freq', f); __still(); addRow();
      __mark(__crestD(8), lambdaD, dD); const a = __dist(); __mark(__crestS(26), lambdaS, dS); const b = __dist(); __fill(1, [a, b], calcRow1); };
    window.__row3 = (a, r) => { __set('angle', a); __still(); addRow(); __fill(3, [a, r], calcRow3); };
  """,
  'steps': [
   { 'el': ['#expBtn1', '#view3d'], 'prep': "setMode('manual'); setExp(1); resetSim(); clearTbl(); __set('freq', 8); __set('angle', 0); __set('dDeep', 10); __set('dShallow', 2); setView('iso'); scrollTo(0,0)",
     'title': 'ตั้งถาดคลื่น: น้ำลึกกับน้ำตื้น',
     'text': 'วาง<b>แผ่นกระจก</b>ในครึ่งขวาของถาด น้ำบนแผ่นกระจกจึง<b>ตื้น</b>กว่า · เลือก <b>I. วัด λ</b> ตั้งความลึก น้ำลึก <b>10 mm</b> น้ำตื้น <b>2 mm</b> ความถี่ <b>8 Hz</b> และ<b>มุมขอบ 0°</b> (ขอบแผ่นกระจกขนานกับหน้าคลื่น คลื่นไม่เปลี่ยนทิศ)',
     'out': 'f = 8 Hz · มุมขอบ = 0° · ความลึก 10 mm / 2 mm' },
   { 'el': ['#playBtn', '#view3d'], 'prep': "if (!isPlaying) togglePlay(); t = __T; draw(); setView('top')",
     'title': 'เปิดเครื่องทำคลื่น แล้วหยุดภาพ',
     'text': 'กด <b>▶ เริ่ม</b> แล้ว <b>🌊 มองผิวน้ำ</b> · คลื่นหน้าตรงเคลื่อนจากน้ำลึก (ซ้าย) เข้าน้ำตื้น (ขวา) · แถบสว่างบนกระดาษใต้ถาด (ยอดคลื่น) <b>ชิดกันมากขึ้น</b>ในน้ำตื้น · ดูสักครู่แล้วกด <b>⏸ หยุด</b> ภาพจะนิ่ง วัดได้แม่นขึ้น',
     'out': 'สังเกต: λ น้ำตื้น < λ น้ำลึก (ความถี่เท่าเดิม)' },
   { 'el': ['[onclick="addRow()"]', '#tblWrap1'], 'prep': "__still(); addRow()",
     'title': 'เพิ่มแถวในตาราง',
     'text': 'กด <b>+ เพิ่มแถว</b> ตารางขึ้นแถวใหม่ที่ f = 8 Hz พร้อมช่องว่าง <b>λD</b> และ <b>λS</b> · ช่อง <b>มาตรฐาน</b> คือ λS/λD จากแบบจำลอง (ใช้เทียบ)',
     'out': 'λS/λD มาตรฐาน = 0.6903 (f = 8 Hz)' },
   { 'el': ['#measureBtn', '#view3d'], 'prep': "__mark(__crestD(8), lambdaD, -0.01); setView('read')",
     'title': 'วัดความยาวคลื่นในน้ำลึก',
     'text': 'กด <b>📏 วัด</b> แล้วแตะ<b>กลางแถบสว่าง</b> 2 แถบที่อยู่ติดกันบนกระดาษฝั่ง<b>น้ำลึก</b> · หมุด ① ② ปักลงและมีเส้นบอกระยะ · กด <b>🔍 ซูมอ่านภาพ</b> แล้วลากหมุดให้ตรงกลางแถบ<br><small>ระยะระหว่างยอดคลื่นที่อยู่ติดกัน = 1 ความยาวคลื่น · วัดข้ามหลายแถบแล้วหารได้แม่นกว่า</small>',
     'out': '<b>λ<sub>D</sub></b> = 3.08 cm' },
   { 'el': '#tblWrap1', 'prep': "__fill(1, [__dist(), null], calcRow1)",
     'title': 'กรอก λD',
     'text': 'พิมพ์ระยะที่อ่านได้ลงช่อง <b>λD</b> ของแถวที่ 1',
     'out': 'λ<sub>D</sub> = 3.08 cm' },
   { 'el': ['#view3d', '#measureInfo'], 'prep': "__mark(__crestS(26), lambdaS, 0.01); setView('read')",
     'title': 'วัดความยาวคลื่นในน้ำตื้น',
     'text': 'แตะจุดใหม่บนกระดาษฝั่ง<b>น้ำตื้น</b> (เหนือแผ่นกระจก) = เริ่มวัดคู่ใหม่ · แตะกลางแถบสว่าง 2 แถบติดกัน แล้วอ่านระยะที่มุมภาพ',
     'out': '<b>λ<sub>S</sub></b> = 2.14 cm' },
   { 'el': '#tblWrap1', 'prep': "__fill(1, [null, __dist()], calcRow1)",
     'title': 'กรอก λS → โปรแกรมคำนวณ',
     'text': 'พิมพ์ลงช่อง <b>λS</b> โปรแกรมคำนวณ<br>① อัตราส่วน <b>λ<sub>S</sub> / λ<sub>D</sub></b> = 2.14 / 3.08<br>② <b>%err</b> = |วัด − มาตรฐาน| ÷ มาตรฐาน × 100',
     'out': '<b>λ<sub>S</sub>/λ<sub>D</sub></b> = 0.6948 · %err ≈ 0.7%' },
   { 'el': ['#tblWrap1', 'label:has(#sl-freq), #sl-freq'], 'prep': "__row1(10, 0.02, -0.01); __row1(12, -0.02, 0.01); __row1(14, 0.01, 0.02); __row1(16, -0.01, -0.01); setView('top')",
     'title': 'เปลี่ยนความถี่ แล้ววัดซ้ำ',
     'text': 'เลื่อน <b>ความถี่ f</b> เป็น 10, 12, 14, 16 Hz · เพิ่มแถว วัด λ<sub>D</sub> และ λ<sub>S</sub> แบบเดิมทุกความถี่ (ควรได้อย่างน้อย 5 แถว)<br><small>ความถี่สูงขึ้น ความยาวคลื่นสั้นลงทั้งสองฝั่ง</small>',
     'out': 'f = 10 · 12 · 14 · 16 Hz → λ<sub>D</sub> ≈ 2.38 · 1.91 · 1.66 · 1.45 cm · λ<sub>S</sub> ≈ 1.79 · 1.58 · 1.43 · 1.27 cm' },
   { 'el': '#tblWrap1', 'prep': "setView('top')",
     'title': 'อ่านตาราง: λS/λD',
     'text': 'ทุกแถว <b>λ<sub>S</sub> < λ<sub>D</sub></b> และอัตราส่วนที่วัดได้ใกล้ค่ามาตรฐาน · คลื่นผ่านขอบเขตความถี่ไม่เปลี่ยน (ตัวทำคลื่นกำหนด) จาก <b>v = fλ</b> จึงได้ <b>v<sub>S</sub>/v<sub>D</sub> = λ<sub>S</sub>/λ<sub>D</sub></b> → คลื่นในน้ำตื้นช้ากว่า<br><small>อัตราส่วนเพิ่มขึ้นเมื่อ f สูงขึ้น เพราะคลื่นน้ำสั้น ๆ ได้รับผลจากแรงตึงผิว (แบบจำลองของแลปคิดผลนี้ด้วย)</small>',
     'out': 'λ<sub>S</sub>/λ<sub>D</sub> ที่วัดได้ = 0.69 · 0.75 · 0.83 · 0.86 · 0.88 (f = 8 – 16 Hz) · มาตรฐาน 0.69 · 0.76 · 0.81 · 0.85 · 0.88 · %err ไม่เกิน 1.6%' },
   { 'el': ['#strobeSection', '#tblWrap2'], 'prep': "__set('freq', 8); setExp(2); markers = []; updateMeasureDisplay(); clearTbl(); __set('strobeD', 8); __set('strobeS', 8); updateStrobeStatus(); recordStrobe(); __still(); setView('top')",
     'title': 'II. วัดความถี่ด้วยสโตรโบสโคป',
     'text': 'เลือก <b>II. Strobe</b> กด ▶ แล้วเลื่อน<b>ความถี่ Strobe น้ำลึก</b>จนคลื่นฝั่งน้ำลึกดูหยุดนิ่ง (ขึ้น ✅) ทำเช่นเดียวกันกับ<b>น้ำตื้น</b> · กด <b>🔦 บันทึกค่า Strobe</b> โปรแกรมคำนวณ<br>③ <b>v = f<sub>strobe</sub> × λ</b> ของแต่ละฝั่ง และ v<sub>S</sub>/v<sub>D</sub>',
     'out': 'f<sub>D</sub> = f<sub>S</sub> = 8.0 Hz → <b>v<sub>D</sub></b> = 24.7 cm/s · <b>v<sub>S</sub></b> = 17.0 cm/s · v<sub>S</sub>/v<sub>D</sub> = 0.690' },
   { 'el': ['#expBtn3', 'label:has(#sl-angle), #sl-angle', '#view3d'], 'prep': "setExp(3); clearTbl(); __set('angle', 30); __still(); setView('top')",
     'title': 'III. เอียงขอบแผ่นกระจก 30°',
     'text': 'เลือก <b>III. วัดมุม</b> ตั้ง<b>มุมขอบ 30°</b> แล้วกด ▶ · หน้าคลื่นที่เข้าน้ำตื้น<b>เปลี่ยนทิศ</b> (หักเห) เบนเข้าหาเส้นตั้งฉากของขอบ<br><small>มุมขอบ = มุมระหว่างหน้าคลื่นตกกระทบกับขอบ = มุมตกกระทบ θ<sub>i</sub></small>' },
   { 'el': ['#protractorSection', '#view3d'], 'prep': "prot.visible = true; snapProtractor(); __still(); setView('read')",
     'title': 'วางโปรแทรกเตอร์ แล้วอ่านมุม',
     'text': 'กด <b>👁 แสดง/ซ่อน</b> โปรแทรกเตอร์ใส 360° วางบนกระดาษใต้ถาด · ลากจุดกลางสีชมพูไปที่ขอบแผ่นกระจก (หรือ <b>🎯 จับที่ขอบเขต</b>) แล้วหมุนให้<b>เส้น 0° (ส้มประ)</b> ทับเส้นตั้งฉากของขอบ · อ่านมุมที่<b>ทิศคลื่นน้ำลึก</b> (ตั้งฉากกับหน้าคลื่น) ทำกับเส้น 0° = θ<sub>i</sub> และ<b>ทิศคลื่นน้ำตื้น</b> = θ<sub>r</sub>',
     'out': '<b>θ<sub>i</sub></b> = 30° · <b>θ<sub>r</sub></b> = 20°' },
   { 'el': '#tblWrap3', 'prep': "addRow(); __fill(3, [30, 20], calcRow3)",
     'title': 'กรอกมุม → โปรแกรมคำนวณ',
     'text': 'กด <b>+ เพิ่มแถว</b> พิมพ์ θ<sub>i</sub> และ θ<sub>r</sub> โปรแกรมคำนวณ<br>④ <b>sin θ<sub>r</sub> / sin θ<sub>i</sub></b> = sin 20° / sin 30° แล้วเทียบกับ λ<sub>S</sub>/λ<sub>D</sub> มาตรฐาน (กฎของสเนลล์)',
     'out': 'sin θ<sub>r</sub>/sin θ<sub>i</sub> = <b>0.6840</b> · มาตรฐาน 0.6903 · %err ≈ 0.9%' },
   { 'el': ['#tblWrap3', '#view3d'], 'prep': "[[15, 10], [20, 14], [40, 26], [45, 29]].forEach(r => __row3(r[0], r[1])); prot.visible = true; snapProtractor(); __still(); setView('top')",
     'title': 'เปลี่ยนมุมขอบ แล้ววัดซ้ำ',
     'text': 'ตั้งมุมขอบ 15°, 20°, 40°, 45° · กด 🎯 ให้โปรแทรกเตอร์ตามขอบใหม่ อ่าน θ<sub>i</sub> θ<sub>r</sub> แล้วบันทึกทุกมุม · θ<sub>r</sub> < θ<sub>i</sub> ทุกครั้ง',
     'out': 'θ<sub>i</sub> = 15 · 20 · 40 · 45° → <b>θ<sub>r</sub></b> = 10 · 14 · 26 · 29° · sin θ<sub>r</sub>/sin θ<sub>i</sub> ≈ 0.67 · 0.71 · 0.68 · 0.69' },
   { 'el': '#tblWrap4', 'prep': "setExp(4); clearTbl(); __set('angle', 30); __still(); addRow(); __fill(4, [30, 20, '3.08', '2.14'], calcRow4)",
     'title': 'IV. เปรียบเทียบอัตราส่วน → สรุปกฎของสเนลล์',
     'text': 'เลือก <b>IV. เทียบ</b> กรอก θ<sub>i</sub>, θ<sub>r</sub> (จากโปรแทรกเตอร์) และ λ<sub>D</sub>, λ<sub>S</sub> (จาก 📏) ที่ f และมุมขอบเดียวกัน · ตารางใต้ภาพเทียบ sin θ<sub>r</sub>/sin θ<sub>i</sub> กับ λ<sub>S</sub>/λ<sub>D</sub>',
     'out': 'f = 8 Hz · มุมขอบ 30°: sin θ<sub>r</sub>/sin θ<sub>i</sub> = 0.684 ≈ λ<sub>S</sub>/λ<sub>D</sub> = 0.695 (%err ระหว่างกัน 1.5%) → <b>sin θ<sub>r</sub>/sin θ<sub>i</sub> = λ<sub>S</sub>/λ<sub>D</sub> = v<sub>S</sub>/v<sub>D</sub></b>' },
  ],
 }
