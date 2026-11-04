# -*- coding: utf-8 -*-
# Lab 74 ปืนสปริงยิงโพรเจกไทล์ — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'หาค่านิจสปริง k จากกราฟ v² – x² แล้วทำนายระยะตก',
  'setup': r"""
    /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองการบินเอง (tick) · ค่า k ของสปริงสุ่มทุกครั้งที่เปิดแลป
       → ตรึงค่าตัวอย่างไว้เฉพาะ browser ที่ถ่ายภาพ ให้ภาพตรงกับข้อความ: k_A = 48.0, k_B = 72.5 N/m */
    simSpeed = 0;
    SPRING.A.k = 48.0; SPRING.A.eps = 0.020; SPRING.B.k = 72.5; SPRING.B.eps = 0.015;
    CH.sp = 'B'; CH.bl = 'm20'; CH.H = 92.0; CH.x = 7.5;
    /* noise ±0.6% ของแลป ใช้ลำดับคงที่ (สูตรเดิมของ modelShot ทุกตัว) */
    window.__nz = [0.3,-0.5,0.7,-0.2,0.4,-0.6,0.1,0.5,-0.3,0.2,-0.4,0.6]; window.__ni = 0;
    modelShot = function(sp, bl, Hcm, xcm){ const s = SPRING[sp], b = BALL[bl];
      const noise = 1 + __nz[(__ni++) % __nz.length] * 0.006;
      const v2 = s.k * Math.pow(xcm/100, 2) * (1 - s.eps) / (b.m/1000) * noise * noise;
      const v = Math.sqrt(Math.max(0, v2)), t = Math.sqrt(2*(Hcm/100)/G); return {v, t, R: v*t*100}; };
    window.__land = () => { let n = 0; while (phase === 'fly' && n++ < 5000) tick(0.01); };
    window.__fill = () => { $('in-H').value = Math.round(Hset*10); $('in-x').value = Math.round(xc*10); if (phase === 'done') $('in-R').value = Math.round(shotR*10); };
    window.__shot = x => { if (phase !== 'ready') reloadBall(); xc = x; xTarget = x; xcFly = x; draggedX = true; draggedH = true;
      fireGun(); __land(); __fill(); recordRow(); };
    window.__B = () => setTimeout(() => { const w = $('tableA'); if (w) w.scrollTop = 1e4; }, 400);
  """,
  'steps': [
   { 'el': ['#springBtns', '#ballBtns'], 'prep': "setMode('manual'); resetLab(); rows = []; setSpring('A'); setBall('m40'); renderAll(); scrollTo(0,0)",
     'title': 'เลือกสปริง A และลูก 40.0 g',
     'text': 'กด <b>🅰 สปริง A</b> และ <b>ลูกเหล็ก 40.0 g</b> · ปืนสปริงยึดที่ขอบโต๊ะ ปากกระบอกอยู่ที่ขอบพอดี ยิงลูกออกใน<b>แนวระดับ</b><br><small>ค่านิจสปริง k ยังไม่ทราบ ต้องหาจากการทดลอง</small>',
     'out': 'ช่อง <b>① ชุดที่ใช้</b> ขึ้นให้เอง: สปริง A · m = 40.0 g' },
   { 'el': ['#view3d', '#in-H'], 'prep': "setView('zh'); $('in-H').value = Math.round(Hset*10)",
     'title': 'อ่านความสูงปากกระบอก H',
     'text': 'กด <b>🔍 ซูมอ่าน H</b> อ่านขีดชี้สีแดงบนสเกลแนวดิ่ง (ตัวเลข = cm · ขีดเล็ก = 1 mm) แล้วกรอกช่อง <b>② H</b> เป็น mm<br><small>สเกลตั้งศูนย์ที่ระดับจุดศูนย์กลางลูกเมื่อวางบนพื้น ค่าที่อ่านจึงเป็นระยะที่ลูกตกลงมาโดยตรง</small>',
     'out': '<b>H</b> = 85.0 cm = 850 mm' },
   { 'el': ['#view3d', '#in-x'], 'prep': "xc = 3.0; xTarget = 3.0; xcFly = 3.0; draggedX = true; draggedH = true; setView('zx'); $('in-x').value = 30",
     'title': 'ลากลูกสูบอัดสปริง แล้วอ่านระยะอัด x',
     'text': '<b>ลากลูกสูบ</b> ท้ายกระบอกถอยหลัง เพื่ออัดสปริงเก็บพลังงานศักย์ยืดหยุ่น · กด <b>🔍 ซูมอ่าน x</b> อ่านขีดชี้แดงบนสเกลกระบอก แล้วกรอกช่อง <b>③ x</b> (mm)',
     'out': '<b>x</b> = 30 mm' },
   { 'el': ['#view3d', '#ab-fire'], 'prep': "setView('side'); fireGun(); { let n = 0; while (phase === 'fly' && flyT < 0.09 + shotT*0.55 && n++ < 3000) tick(0.01); }",
     'title': 'กดยิง',
     'text': 'กด <b>🚀 ยิง</b> สปริงดันลูกออกจากปากกระบอกในแนวระดับด้วยความเร็ว v แล้วลูกเคลื่อนที่แบบโพรเจกไทล์ตกลงบนแถบกระดาษคาร์บอน ทิ้งรอยไว้ (เส้นประสีเหลือง = แนวการเคลื่อนที่)<br><small>½kx² กลายเป็น ½mv² (เสียไปเล็กน้อยในกระบอก)</small>' },
   { 'el': ['#view3d', '#in-R'], 'prep': "__land(); setView('zr'); $('in-R').value = Math.round(shotR*10)",
     'title': 'อ่านระยะตก R',
     'text': 'กด <b>🔍 ซูมอ่าน R</b> ภาพเลื่อนไปที่รอยตกล่าสุด · อ่านเส้นดำของรอยบนสเกลพื้น (0 อยู่ใต้ปากกระบอกพอดี) แล้วกรอกช่อง <b>④ R</b> (mm)',
     'out': '<b>R</b> = 429 mm' },
   { 'el': '#lastRec', 'prep': "recordRow(); setView('iso')",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> ค่า H, x, R เข้าตาราง และแสดงใน <b>📊 ผลที่บันทึกล่าสุด</b> โปรแกรมคำนวณต่อ:<br>① เวลาตก <b>t = √(2H/g)</b> = √(2 × 0.850 / 9.80) = 0.4165 s<br>② ความเร็วที่ปากกระบอก <b>v = R/t = R√(g/2H)</b> = 0.429 / 0.4165 = 1.030 m/s<br>③ <b>v²</b> = 1.061 m²/s² · <b>x²</b> = (0.030)² = 9.00 × 10⁻⁴ m²<br>④ พลังงานจลน์ <b>E<sub>k</sub> = ½mv²</b> = ½ × 0.040 × 1.061',
     'out': '<b>v</b> = 1.030 m/s · <b>v²</b> = 1.061 m²/s² · <b>E<sub>k</sub></b> = 21.2 mJ' },
   { 'el': ['#view3d', '#ab-reload'], 'prep': "[2.0, 4.5, 6.0, 7.5].forEach(__shot); setView('iso'); renderAll()",
     'title': 'บรรจุลูกใหม่ เปลี่ยน x แล้วยิงซ้ำ',
     'text': 'กด <b>🔄 บรรจุลูกใหม่</b> ลากลูกสูบให้ได้ระยะอัดใหม่ อ่าน x ยิง อ่าน R แล้วบันทึก · ทำให้ครบ <b>5 ค่าของ x</b> (20 · 30 · 45 · 60 · 75 mm) โดยใช้ H และลูกเดิม · รอยตกบนพื้นเรียงห่างออกไปตาม x<br><small>อัดมากขึ้น ลูกพุ่งเร็วขึ้น ตกไกลขึ้น</small>',
     'out': 'สปริง A: x = 30 · 20 · 45 · 60 · 75 mm → <b>R</b> = 429 · 285 · 645 · 856 · 1074 mm' },
   { 'el': '#tableA', 'prep': "$('tableA').style.maxHeight = 'none'; renderAll()",
     'title': 'อ่านตารางผล',
     'text': 'แต่ละแถว = การยิง 1 ครั้ง · คอลัมน์ <b>v</b>, <b>v²</b>, <b>x²</b> และ <b>E<sub>k</sub></b> คำนวณจาก H, x, R ที่กรอก · เมื่อ x เพิ่มเป็น 2 เท่า R และ v เพิ่มเป็นราว 2 เท่า แต่ E<sub>k</sub> เพิ่มเป็นราว 4 เท่า<br><small>ใต้ตารางมีความชันและ k ของแต่ละชุด · ดาวน์โหลดเป็น 📥 CSV ได้</small>',
     'out': '<b>v²</b> = 1.061 · 0.468 · 2.398 · 4.224 · 6.649 m²/s² · <b>E<sub>k</sub></b> = 21.2 · 9.4 · 48.0 · 84.5 · 133.0 mJ' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('v2x2')",
     'title': 'กราฟ v² – x² หาค่า k ของสปริง A',
     'text': 'กด <b>📈 v² – x²</b> จุดเรียงเป็น<b>เส้นตรงผ่านจุดกำเนิด</b> · จาก ½kx² = ½mv² → <b>v² = (k/m) x²</b><br>ดังนั้น <b>ความชัน = k/m</b> → <b>k = ความชัน × m</b> (m เป็นกิโลกรัม: 40.0 g = 0.040 kg)',
     'out': 'ความชัน ≈ 1180 s⁻² → <b>k<sub>A</sub></b> = 1180 × 0.040 ≈ <b>47.2 N/m</b>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setSpring('B'); [2.0, 3.0, 4.5, 6.0, 7.5].forEach(__shot); setGraph('v2x2'); setView('iso')",
     'title': 'เปลี่ยนเป็นสปริง B แล้ววัดซ้ำ',
     'text': 'กด <b>🅱 สปริง B</b> (แผงเลือกสปริง) ใช้ลูก 40.0 g และ H เดิม ยิงให้ครบ 5 ค่าของ x แบบเดิม · ในกราฟจะมีเส้นสีส้มของสปริง B เพิ่มขึ้น<br><small>เส้นชันกว่า = สปริงแข็งกว่า (k มากกว่า)</small>',
     'out': 'สปริง B: R = 351 · 528 · 794 · 1054 · 1321 mm · ความชัน ≈ 1786 s⁻² → <b>k<sub>B</sub> ≈ 71.5 N/m</b>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('rx')",
     'title': 'กราฟ R – x',
     'text': 'กด <b>📈 R – x</b> แต่ละสปริงได้<b>เส้นตรงผ่านจุดกำเนิด</b> แม้การเคลื่อนที่จะเป็นเส้นโค้ง เพราะ H เท่าเดิม เวลาตก t จึงเท่าเดิม และ v ∝ x → <b>R = vt ∝ x</b>',
     'out': '<b>R/x</b> ≈ 1.43 cm/mm (สปริง A) · ≈ 1.76 cm/mm (สปริง B)' },
   { 'el': ['#ans-kA', '#ansAMsg', '#ans-kB', '#ansBMsg'], 'prep': "$('ans-kA').value = (bestK('A')).toFixed(1); $('ans-kB').value = (bestK('B')).toFixed(1); checkK('A'); checkK('B')",
     'title': 'ตอบค่า k ของสปริง A และ B',
     'text': 'กรอกค่า k ที่ได้จากความชันในกรอบ <b>🎯 ตรวจคำตอบ</b> แล้วกด <b>ตรวจ</b> ทีละสปริง · ถูกเมื่อคลาดไม่เกิน 5%<br><small>k ที่หาได้ต่ำกว่าค่าจริงเล็กน้อย เพราะพลังงานบางส่วนสูญเสียในกระบอก (1–3%)</small>',
     'out': '<b>k<sub>A</sub></b> ≈ 47.2 N/m · <b>k<sub>B</sub></b> ≈ 71.5 N/m ในภาพตัวอย่าง (ค่าจริงสุ่มในช่วง 25 – 90 N/m ทุกครั้งที่เปิดแลป)' },
   { 'el': ['#chalBox', '#ans-R', '#ansRMsg'], 'prep': "setupChallenge(); { const k = bestK(CH.sp), m = BALL[CH.bl].m/1000; $('ans-R').value = (CH.x/100 * Math.sqrt(k/m) * Math.sqrt(2*(CH.H/100)/G) * 100).toFixed(1); } checkPredict()",
     'title': 'โจทย์ทำนาย: คำนวณ R ก่อนยิง',
     'text': 'กด <b>🎯 โจทย์ทำนาย</b> โจทย์กำหนดสปริง ลูก H และ x ให้ · ใช้ k ที่หาได้คำนวณ:<br>① <b>v = x√(k/m)</b> = 0.075 × √(71.5 / 0.020) = 4.48 m/s<br>② <b>t = √(2H/g)</b> = √(2 × 0.920 / 9.80) = 0.433 s<br>③ <b>R = vt</b> = 4.48 × 0.433 m<br>กรอก R (cm) แล้วกด <b>ตรวจคำทำนาย</b>',
     'out': 'โจทย์ตัวอย่าง: สปริง B · ลูก 20.0 g · H = 92.0 cm · x = 75 mm → ทำนาย <b>R ≈ 194.2 cm</b>' },
   { 'el': ['#view3d', '#ab-fire'], 'prep': "fireGun(); __land(); setView('zr')",
     'title': 'ยิงจริง ตรวจคำทำนาย',
     'text': 'กด <b>🚀 ยิง</b> แล้วกด <b>🔍 ซูมอ่าน R</b> อ่านรอยตกบนสเกลพื้น เทียบกับค่าที่ทำนายไว้<br><small>ลูกเบากว่า (20 g) จึงพุ่งเร็วกว่าลูก 40 g ที่อัดเท่ากัน √2 เท่า</small>',
     'out': 'รอยตกจริง <b>R ≈ 193.7 cm</b> ตรงกับคำทำนาย 194 cm (คลาดไม่ถึง 1%) → ½kx² ถ่ายโอนเป็น ½mv² จริง' },
  ],
 }
