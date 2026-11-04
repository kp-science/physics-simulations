# -*- coding: utf-8 -*-
# Lab 35 ภาพจากเลนส์นูน — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# f ของเลนส์สุ่มตอนเปิดหน้า (6–24 cm) → ตรึงค่าตัวอย่าง 10 cm เฉพาะ browser ที่ถ่ายภาพ
# ตำแหน่งจอที่ภาพชัด = s′ จากแบบจำลองของแลป (calcImage) · y′ อ่านด้วยไม้บรรทัด ↕ บนแผนภาพ (ขนาดภาพที่แลปวาด)
GUIDE = {
  'title': 'หาความยาวโฟกัสของเลนส์นูน แล้วตรวจสมการเลนส์บาง',
  'setup': r"""
    window.__pos = (o, l, s, e) => { if (o != null) objCm = o; if (l != null) lensCm = l; if (s != null) screenCm = s; if (e != null) eyeCm = e; clampPositions(); syncPosUI(); drawAll(); };
    window.__fA = (l, idx) => { __pos(null, l, l + fTrue); const ins = document.querySelectorAll('#tableWrap input'); ins[idx].value = (screenCm - lensCm).toFixed(1); };
    window.__setB = (f, y) => { fTrue = f; objHeightCm = y; ['sl-fB', 'vi-fB'].forEach(i => $(i).value = f); ['sl-hB', 'vi-hB'].forEach(i => $(i).value = y); $('rTxt').textContent = fmt(2 * f, 1); rebuild3D(); drawAll(); };
    /* วางวัตถุที่ระยะ s แล้วเลื่อนจอ (ภาพจริง) หรือตา (ภาพเสมือน) ไปตำแหน่งที่เห็นภาพชัด */
    window.__s = s => { const r = calcImage(s, fTrue); __pos(lensCm - s, null, r.d_i > 0 ? lensCm + r.d_i : null, r.d_i > 0 ? null : lensCm + 22); return r; };
    /* ไม้บรรทัด ↕ วัดความสูงภาพบนแผนภาพ (จากแกนถึงหัวลูกศรภาพที่แลปวาด) */
    window.__rulV = () => { const r = calcImage(d_o_now(), fTrue), x = r.d_i > 0 ? cm2px(screenCm) + 5 : cm2px(lensCm + r.d_i);
      setRulerMode('v'); rulerVX = x; rulerVAy = AY; rulerVBy = AY + (r.d_i > 0 ? 1 : -1) * hpx(Math.abs(r.M) * objHeightCm); drawDiag(); };
    window.__inB = () => { const r = calcImage(d_o_now(), fTrue), yi = Math.abs(rulerVBy - rulerVAy) / (BW / 100 * VSCALE);
      $('inp-do').value = (lensCm - objCm).toFixed(1); $('inp-di').value = (r.d_i > 0 ? screenCm - lensCm : r.d_i).toFixed(1);
      $('inp-ho').value = objHeightCm.toFixed(1); $('inp-hi').value = ((r.d_i > 0 ? -1 : 1) * yi).toFixed(1); };
    window.__recS = s => { __s(s); __rulV(); __inB(); recordManualB(); };
  """,
  'steps': [
   { 'el': ['#modeBtns', '#partBtns', '#view3d'], 'prep': "setMode('manual'); fTrue = 10; setPart('A'); clearTable(); __pos(null, 40, 57); setView('iso'); scrollTo(0,0)",
     'title': 'โหมดวัดค่าเอง · Part A หาโฟกัส',
     'text': 'กด <b>🖐 วัดค่าเอง</b> และ <b>A: หาโฟกัส</b> · แสงอาทิตย์เป็น<b>แสงขนาน</b> (ดวงอาทิตย์อยู่ไกลมาก) ส่องจากซ้ายผ่านเลนส์นูนไปตกบนจอทางขวา · ตำแหน่งของเลนส์และจออ่านจากสเกลของม้านั่งเชิงแสง (cm)<br><small>เลนส์ถูกสุ่ม ไม่บอกความยาวโฟกัส f</small>' },
   { 'el': ['#view3d', '#rowScr'], 'prep': "__pos(null, 40, 57); setView('side')",
     'title': 'เลื่อนจอ ดูวงแสงบนจอ',
     'text': 'เลื่อน<b>จอ</b> (แถบเลื่อน "จอ" หรือลากจอในภาพ/แผนภาพ) ดูกล่อง <b>วงแสงบนจอ</b> มุมขวาบน · จอที่อยู่ไกลหรือใกล้จุดโฟกัสเกินไปจะเห็นเป็น<b>วงแสงกว้าง</b>',
     'out': 'จอที่ 57.0 cm: วงแสงยังกว้าง' },
   { 'el': ['#view3d', '#posSection'], 'prep': "__pos(null, 40, 50); setView('side')",
     'title': 'หาตำแหน่งที่วงแสงเล็กที่สุด',
     'text': 'ขยับจอเข้า-ออกจน<b>วงแสงเล็กที่สุดเป็นจุด</b> (กรอบคำแนะนำขึ้น 🎯) = จออยู่ที่<b>จุดโฟกัส F′</b> · อ่านตำแหน่งเลนส์และจอจากสเกล<br>① <b>f = ตำแหน่งจอ − ตำแหน่งเลนส์</b>',
     'out': 'เลนส์ 40.0 cm · จอ 50.0 cm → <b>f</b> = 10.0 cm' },
   { 'el': ['#tableWrap', '#btnRecord'], 'prep': "__fA(40, 0)",
     'title': 'กรอก f แล้วบันทึก',
     'text': 'พิมพ์ f ที่วัดได้ในช่อง <b>f วัด</b> แถวที่ 1 แล้วกด <b>📝 บันทึก</b> · ค่า <b>f จริง</b> และ %error จะเฉลยหลังบันทึก' },
   { 'el': '#tableWrap', 'prep': "recordData(); __fA(30, 1); __fA(55, 2); recordData(); __pos(null, 55, 65); setView('side')",
     'title': 'ย้ายเลนส์ แล้ววัดซ้ำให้ครบ 3 ครั้ง',
     'text': 'เลื่อน<b>เลนส์</b>ไปตำแหน่งใหม่ (เช่น 30 cm และ 55 cm) หาตำแหน่งจอที่วงแสงเล็กที่สุดใหม่ทุกครั้ง แล้วกรอกแถว 2 และ 3 กดบันทึก · หาค่าเฉลี่ย<br><small>ใช้เลนส์เดิมทั้ง 3 ครั้ง — ปุ่ม 🎲 สุ่มเลนส์ใหม่ จะเปลี่ยนเลนส์และล้างตารางนี้</small>',
     'out': 'เลนส์ 30.0 → จอ 40.0 · เลนส์ 55.0 → จอ 65.0 → <b>f<sub>เฉลี่ย</sub></b> = 10.0 cm (ในภาพตัวอย่าง · เลนส์สุ่ม f 6–24 cm)' },
   { 'el': '#partBSettings', 'prep': "setPart('B'); clearTable(); __setB(10, 1.5); lensCm = 40; __s(30); setView('iso')",
     'title': 'Part B: ตั้ง f และขนาดวัตถุ',
     'text': 'กด <b>B: ศึกษาภาพ</b> ตั้ง <b>f</b> = 10 cm (เท่าเลนส์ที่หาได้) และ<b>ขนาดวัตถุ y</b> = 1.5 cm · วัตถุคือแผ่นลูกศรเรืองแสงทางซ้ายเลนส์ จออยู่ทางขวาเลนส์ (คนละด้านกับวัตถุ)<br><small>แผนภาพบอกจุด F, F′ และ 2F, 2F′ (2F = 20 cm จากเลนส์)</small>',
     'out': '<b>f</b> = 10.0 cm · <b>y</b> = 1.5 cm' },
   { 'el': ['#view3d', '#posSection'], 'prep': "__s(30); setView('iso')",
     'title': 'วางวัตถุที่ s = 30 cm แล้วหาภาพบนจอ',
     'text': 'วางวัตถุที่ระยะ <b>s &gt; 2f</b> เช่น ตำแหน่ง 10.0 cm (เลนส์ที่ 40.0 cm → s = 30.0 cm) · เลื่อนจอจน<b>ภาพบนจอคมชัดที่สุด</b> (กล่อง "ภาพบนจอ" และกรอบคำแนะนำ 🎯) · อ่านตำแหน่งจอ<br>② <b>s′ = ตำแหน่งจอ − ตำแหน่งเลนส์</b>',
     'out': '<b>s</b> = 30.0 cm · จอ 55.0 cm → <b>s′</b> = 15.0 cm · ภาพจริง หัวกลับ เล็กกว่าวัตถุ' },
   { 'el': ['#diagCanvas', '#btnRulerV'], 'prep': "__rulV()",
     'title': 'วัดความสูงภาพ y′ ด้วยไม้บรรทัด ↕',
     'text': 'กด <b>↕ วัดความสูง</b> ลากปลาย A ไว้ที่แกนมุขสำคัญ (เส้นประ) ปลาย B ที่หัวลูกศรภาพบนจอ อ่านตัวเลขข้างไม้บรรทัด<br><small>ภาพหัวกลับ (อยู่ใต้แกน) จึงกรอก y′ เป็น<b>ลบ</b> · สเกลแนวตั้งของแผนภาพขยาย 2.5× แต่ไม้บรรทัดชดเชยให้แล้ว</small>',
     'out': '|y′| = 0.7 cm → <b>y′</b> = −0.7 cm' },
   { 'el': '#manualBInputs', 'prep': "__inB()",
     'title': 'กรอก s, s′, y, y′ แล้วบันทึก',
     'text': 'กรอก 4 ค่าในกรอบ <b>📏 บันทึกค่าที่วัดได้</b> ตามกฎเครื่องหมาย: ภาพจริง s′ บวก y′ ลบ · แล้วกด <b>📝 บันทึก</b>' },
   { 'el': '#tableWrap', 'prep': "recordManualB(); $('tableWrap').scrollLeft = 1e4",
     'title': 'โปรแกรมคำนวณ f และ M',
     'text': 'ตารางเพิ่มแถว โปรแกรมคำนวณ:<br>③ จากสมการเลนส์บาง 1/f = 1/s + 1/s′ → <b>f = s s′ / (s + s′)</b> = 30.0 × 15.0 / 45.0<br>④ กำลังขยายจากความสูง <b>M = y′/y</b> = −0.7/1.5 เทียบกับ <b>−s′/s</b> = −15.0/30.0<br><small>M ลบ = ภาพจริงหัวกลับ</small>',
     'out': '<b>f</b> = 10.00 cm (คลาด 0%) · <b>M</b> = −0.47 ≈ −s′/s = −0.50 (ตารางเลื่อนซ้าย-ขวาได้)' },
   { 'el': '#tableWrap', 'prep': "__recS(20); __recS(15); __s(15); setView('iso')",
     'title': 'เปลี่ยนระยะวัตถุ แล้ววัดซ้ำ',
     'text': 'ย้ายวัตถุให้ <b>s = 2f</b> (20 cm) และ <b>f &lt; s &lt; 2f</b> (15 cm) หาภาพบนจอ วัด s′ และ y′ แล้วบันทึกแบบเดิม · สังเกต: วัตถุเข้าใกล้เลนส์ ภาพอยู่ไกลขึ้นและใหญ่ขึ้น',
     'out': 's = 20.0 → s′ = 20.0 cm, y′ = −1.5 cm (ขนาดเท่าวัตถุ) · s = 15.0 → s′ = 30.0 cm, y′ = −3.0 cm (ขยาย 2 เท่า) · f คำนวณ = 10.00 cm ทุกแถว' },
   { 'el': ['#view3d', '#focusHint'], 'prep': "__s(6); setView('eye')",
     'title': 'วัตถุใกล้กว่า f: มองผ่านเลนส์',
     'text': 'ย้ายวัตถุให้ <b>s &lt; f</b> (เช่น s = 6.0 cm) จอรับภาพไม่ได้ · กด <b>มุมจากตา</b> ตาอยู่ทางขวามอง<b>ผ่านเลนส์</b> เห็น<b>ภาพหัวตั้ง ขยาย</b> (หลักของแว่นขยาย) · ภาพเสมือนอยู่<b>ด้านเดียวกับวัตถุ</b> แสดงเป็นลูกศรเส้นประสีม่วงในแผนภาพ',
     'out': 'ภาพเสมือน · หัวตั้ง · ขยาย' },
   { 'el': ['#diagCanvas', '#tableWrap'], 'prep': "__rulV(); __inB(); recordManualB(); __rulV()",
     'title': 'วัดภาพเสมือน แล้วบันทึก',
     'text': 'อ่านตำแหน่งลูกศรเส้นประสีม่วงบนสเกล → s′ = ตำแหน่งภาพ − ตำแหน่งเลนส์ (ได้ค่า<b>ลบ</b> เพราะอยู่ด้านวัตถุ) · วัด y′ ด้วยไม้บรรทัด ↕ (หัวตั้ง y′ <b>บวก</b>) แล้วบันทึก',
     'out': 'ภาพที่ 25.0 cm → <b>s′</b> = −15.0 cm · <b>y′</b> = +3.7 cm → f = 6.0 × (−15.0)/(6.0 − 15.0) = 10.00 cm · <b>M</b> = y′/y = +2.47 ≈ −s′/s = +2.50' },
   { 'el': '#graphSection', 'prep': "setMode('auto'); clearTable(); ['sl-f','vi-f'].forEach(i => $(i).value = 10); [15, 20, 25, 30, 40, 50].forEach(s => { ['sl-do','vi-do'].forEach(i => $(i).value = s); recordData(); }); drawAll(); drawGraph()",
     'title': 'กราฟ 1/s′ กับ 1/s หา f',
     'text': 'สรุปผลด้วยกราฟ (ทำเองบนกระดาษกราฟ หรือ <b>⚡ อัตโนมัติ</b> สำหรับสมาชิก ปรับ s แล้วกดบันทึกทีละจุด) · จุดเรียงเป็น<b>เส้นตรงความชัน −1</b> เพราะ 1/s′ = 1/f − 1/s<br>⑤ <b>จุดตัดแกนทั้งสอง = 1/f</b>',
     'out': 'จุดตัดแกน = 0.100 cm⁻¹ → <b>f</b> = 10 cm · ตรงกับ Part A และ f จากสมการเลนส์ทุกแถว' },
  ],
 }
