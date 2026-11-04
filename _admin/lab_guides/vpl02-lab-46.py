# -*- coding: utf-8 -*-
# Lab 46 ภาพจากกระจกเว้า — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py (แบบเดียวกับ vpl02-lab-35.py)
# กระจกปริศนาสุ่ม f 6–22 cm → ตรึงค่าตัวอย่าง (14.5 · 8.0 · 10.0 cm) เฉพาะ browser ที่ถ่ายภาพ
# ตำแหน่งจอที่ภาพชัด = s′ จากแบบจำลองของแลป (calcImage) · y′ อ่านด้วยไม้บรรทัด ↕ บนแผนภาพ (ขนาดภาพที่แลปวาด)
GUIDE = {
  'title': 'หาความยาวโฟกัสของกระจกเว้า แล้วตรวจสมการกระจก',
  'setup': r"""
    window.__pos = (o, s, e, m) => { if (o != null) objCm = o; if (s != null) screenCm = s; if (e != null) eyeCm = e; if (m != null) mirrorCm = m; clampPositions(); syncPosUI(); drawAll(); };
    window.__mys = f => { randomizeF(); fMyst = f; applyMirror(); rebuild3D(); setPart(part); };
    /* Part A: จอที่จุดโฟกัส แล้วกรอก f = กระจก − จอ ในแถว idx */
    window.__fA = idx => { __pos(null, mirrorCm - fTrue); const ins = document.querySelectorAll('#tableWrap input'); ins[idx].value = (mirrorCm - screenCm).toFixed(1); };
    window.__hB = y => { const s = $('sl-hB'); s.value = y; s.dispatchEvent(new Event('input')); $('vi-hB').value = y; };
    /* วางวัตถุที่ระยะ s แล้วเลื่อนจอ (ภาพจริง) หรือตา (ภาพเสมือน) ไปตำแหน่งที่เห็นภาพ */
    window.__s = s => { const r = calcImage(s, fTrue); __pos(mirrorCm - s, r.d_i > 0 ? mirrorCm - r.d_i : null, r.d_i > 0 ? null : mirrorCm - s - 20); return r; };
    /* ไม้บรรทัด ↕ จากแกนถึงหัวลูกศรภาพที่แลปวาด */
    window.__rulV = () => { const r = calcImage(d_o_now(), fTrue), x = r.d_i > 0 ? cm2px(screenCm) - 5 : cm2px(mirrorCm - r.d_i);
      setRulerMode('v'); rulerVX = x; rulerVAy = AY; rulerVBy = AY + (r.d_i > 0 ? 1 : -1) * hpx(Math.abs(r.M) * objHeightCm); drawDiag(); };
    window.__inB = () => { const r = calcImage(d_o_now(), fTrue), yi = Math.abs(rulerVBy - rulerVAy) / (BW / 100 * VSCALE);
      $('inp-do').value = d_o_now().toFixed(1); $('inp-di').value = (r.d_i > 0 ? mirrorCm - screenCm : r.d_i).toFixed(1);
      $('inp-ho').value = objHeightCm.toFixed(1); $('inp-hi').value = ((r.d_i > 0 ? -1 : 1) * yi).toFixed(1); };
    window.__recS = s => { __s(s); __rulV(); __inB(); recordManualB(); };
  """,
  'steps': [
   { 'el': ['#modeBtns', '#partBtns', '#view3d'], 'prep': "setMode('manual'); setMirror('mystery'); fMyst = 14.5; applyMirror(); setPart('A'); clearTable(); __pos(null, 40, null, 70); setView('iso'); scrollTo(0,0)",
     'title': 'โหมดวัดค่าเอง · Part A หาโฟกัส',
     'text': 'กด <b>🖐 วัดค่าเอง</b> และ <b>A: หาโฟกัส</b> · ใช้ <b>❓ กระจกปริศนา</b> (ไม่บอก f) · แสงอาทิตย์เป็น<b>แสงขนาน</b> ส่องจากซ้ายเข้าผิวกระจกเว้า สะท้อนกลับมารวมกันหน้ากระจก · <b>จออยู่ด้านเดียวกับแสงที่มา</b> (หน้ากระจก) · ตำแหน่งกระจกและจออ่านจากสเกลของม้านั่งเชิงแสง (cm)' },
   { 'el': ['#sl-scr', '#view3d'], 'prep': "__pos(null, 40); setView('side')",
     'title': 'เลื่อนจอ ดูวงแสงบนจอ',
     'text': 'เลื่อน<b>จอ</b> (แถบเลื่อน "จอ" หรือลากจอในภาพ/แผนภาพ) ดูกล่อง <b>วงแสงบนจอ</b> มุมขวาบน · จอที่อยู่ไกลหรือใกล้จุดโฟกัสเกินไปเห็นเป็น<b>วงแสงกว้าง</b>',
     'out': 'จอที่ 40.0 cm: วงแสงยังกว้าง' },
   { 'el': ['#view3d', '#posSection'], 'prep': "__pos(null, 55.5); setView('side')",
     'title': 'หาตำแหน่งที่วงแสงเล็กที่สุด',
     'text': 'ขยับจอเข้า-ออกจน<b>วงแสงเล็กที่สุดเป็นจุด</b> (กล่องขึ้น "จุดโฟกัส!") = จออยู่ที่<b>จุดโฟกัส F</b> · อ่านตำแหน่งกระจกและจอจากสเกล (หรือใช้ไม้บรรทัด ↔ บนแผนภาพ)<br>① <b>f = ตำแหน่งกระจก − ตำแหน่งจอ</b>',
     'out': 'กระจก 70.0 cm · จอ 55.5 cm → <b>f</b> = 14.5 cm' },
   { 'el': ['#tableWrap', '#btnRecord'], 'prep': "__fA(0)",
     'title': 'กรอก f แล้วบันทึก',
     'text': 'พิมพ์ f ที่วัดได้ในช่อง <b>f วัด</b> แถวที่ 1 แล้วกด <b>📝 บันทึก</b> · ค่า <b>f จริง</b> และ %error เฉลยหลังบันทึก · ตารางคำนวณรัศมีความโค้งให้<br>② <b>R = 2f</b>',
     'out': '<b>f</b> = 14.5 cm → <b>R</b> = 29.0 cm' },
   { 'el': '#tableWrap', 'prep': "recordData(); __mys(8); __fA(1); recordData(); __mys(10); __fA(2); recordData(); setView('side')",
     'title': 'สุ่มกระจกใหม่ แล้ววัดซ้ำให้ครบ 3 ครั้ง',
     'text': 'กด <b>🎲 สุ่มกระจกปริศนาใหม่</b> หาตำแหน่งจอที่วงแสงเล็กที่สุดใหม่ทุกครั้ง แล้วกรอกแถว 2 และ 3 กดบันทึก<br><small>แถวเดิมยังอยู่ และระบุหมายเลขกระจกของแต่ละแถว</small>',
     'out': 'กระจก 70.0 → จอ 62.0 → f = 8.0 cm (R = 16.0) · จอ 60.0 → f = 10.0 cm (R = 20.0) (ในภาพตัวอย่าง · กระจกสุ่ม f 6–22 cm)' },
   { 'el': '#partBSettings', 'prep': "setPart('B'); clearTable(); __hB(1.5); __s(30); setView('iso')",
     'title': 'Part B: ใช้กระจกบานล่าสุด ตั้งขนาดวัตถุ',
     'text': 'กด <b>B: ศึกษาภาพ</b> ใช้กระจกบานล่าสุด (f = 10.0 cm จาก Part A) ตั้ง<b>ขนาดวัตถุ y</b> = 1.5 cm · วัตถุคือแผ่นลูกศรเรืองแสงหน้ากระจก จอรับภาพอยู่<b>ด้านเดียวกับวัตถุ</b> (วางเยื้องแกนเล็กน้อยไม่ให้บังแสง)<br><small>จุดศูนย์กลางความโค้ง C อยู่ที่ R = 2f = 20 cm หน้ากระจก</small>',
     'out': '<b>f</b> = 10.0 cm · <b>y</b> = 1.5 cm' },
   { 'el': ['#view3d', '#posSection'], 'prep': "__s(30); setView('iso')",
     'title': 'วางวัตถุที่ s = 30 cm แล้วหาภาพบนจอ',
     'text': 'วางวัตถุที่ระยะ <b>s &gt; 2f</b> เช่น ตำแหน่ง 40.0 cm (กระจกที่ 70.0 cm → s = 30.0 cm) · เลื่อนจอจน<b>ภาพบนจอคมชัดที่สุด</b> (กล่อง "ภาพบนจอ") · อ่านตำแหน่งจอ<br>③ <b>s′ = ตำแหน่งกระจก − ตำแหน่งจอ</b>',
     'out': '<b>s</b> = 30.0 cm · จอ 55.0 cm → <b>s′</b> = 15.0 cm · ภาพจริง หัวกลับ เล็กกว่าวัตถุ' },
   { 'el': ['#diagCanvas', '#btnRulerV'], 'prep': "__rulV()",
     'title': 'วัดความสูงภาพ y′ ด้วยไม้บรรทัด ↕',
     'text': 'กด <b>↕ วัดความสูง</b> ลากปลาย A ไว้ที่แกนมุขสำคัญ (เส้นประ) ปลาย B ที่หัวลูกศรภาพบนจอ อ่านตัวเลขข้างไม้บรรทัด<br><small>ภาพหัวกลับ (อยู่ใต้แกน) จึงกรอก y′ เป็น<b>ลบ</b> · สเกลแนวตั้งของแผนภาพขยาย 2.5× แต่ไม้บรรทัดชดเชยให้แล้ว</small>',
     'out': '|y′| = 0.7 cm → <b>y′</b> = −0.7 cm' },
   { 'el': '#manualBInputs', 'prep': "__inB()",
     'title': 'กรอก s, s′, y, y′ แล้วบันทึก',
     'text': 'กรอก 4 ค่าในกรอบบันทึกค่าที่วัดได้ ตามกฎเครื่องหมาย: ภาพจริง (หน้ากระจก) s′ บวก y′ ลบ · แล้วกด <b>📝 บันทึก</b>' },
   { 'el': '#tableWrap', 'prep': "recordManualB(); $('tableWrap').scrollLeft = 1e4",
     'title': 'โปรแกรมคำนวณ f และ M',
     'text': 'ตารางเพิ่มแถว โปรแกรมคำนวณ:<br>④ จากสมการกระจก 1/f = 1/s + 1/s′ → <b>f = s s′ / (s + s′)</b> = 30.0 × 15.0 / 45.0<br>⑤ กำลังขยายจากความสูง <b>M = y′/y</b> = −0.7/1.5 เทียบกับ <b>−s′/s</b> = −15.0/30.0<br><small>M ลบ = ภาพจริงหัวกลับ</small>',
     'out': '<b>f</b> = 10.00 cm (คลาด 0%) · <b>M</b> = −0.47 ≈ −s′/s = −0.50 (ตารางเลื่อนซ้าย-ขวาได้)' },
   { 'el': '#tableWrap', 'prep': "__recS(20); __recS(15); __s(15); setView('iso')",
     'title': 'เปลี่ยนระยะวัตถุ แล้ววัดซ้ำ',
     'text': 'ย้ายวัตถุให้ <b>s = 2f</b> (20 cm) และ <b>f &lt; s &lt; 2f</b> (15 cm) หาภาพบนจอ วัด s′ และ y′ แล้วบันทึกแบบเดิม · สังเกต: วัตถุเข้าใกล้กระจก ภาพอยู่ไกลกระจกขึ้นและใหญ่ขึ้น',
     'out': 's = 20.0 → s′ = 20.0 cm, y′ = −1.5 cm (เท่าวัตถุ ที่ C) · s = 15.0 → s′ = 30.0 cm, y′ = −3.0 cm (ขยาย 2 เท่า) · f คำนวณ = 10.00 cm ทุกแถว' },
   { 'el': ['#sl-eye', '#view3d'], 'prep': "__s(6); setView('eye')",
     'title': 'วัตถุใกล้กว่า f: มองเข้าไปในกระจก',
     'text': 'ย้ายวัตถุให้ <b>s &lt; f</b> (เช่น s = 6.0 cm) จอรับภาพไม่ได้ · เลื่อน<b>ตา 👁</b> ไปอยู่หน้าวัตถุ (ทางซ้าย) กด <b>มุมจากตา</b> มองเข้าไปในกระจก เห็น<b>ภาพหัวตั้ง ขยาย</b> อยู่<b>หลังกระจก</b> (กล่อง <b>มุมมองของตา</b> มุมขวาบน · หลักของกระจกแต่งหน้า) · แผนภาพแสดงภาพเสมือนเป็นลูกศรเส้นประสีม่วง',
     'out': 'ภาพเสมือน · หัวตั้ง · ขยาย' },
   { 'el': ['#diagCanvas', '#tableWrap'], 'prep': "__rulV(); __inB(); recordManualB(); __rulV()",
     'title': 'วัดภาพเสมือน แล้วบันทึก',
     'text': 'อ่านตำแหน่งลูกศรเส้นประสีม่วงบนสเกล → s′ = ตำแหน่งกระจก − ตำแหน่งภาพ (ได้ค่า<b>ลบ</b> เพราะอยู่หลังกระจก) · วัด y′ ด้วยไม้บรรทัด ↕ (หัวตั้ง y′ <b>บวก</b>) แล้วบันทึก',
     'out': 'ภาพที่ 85.0 cm → <b>s′</b> = −15.0 cm · <b>y′</b> = +3.7 cm → f = 6.0 × (−15.0)/(6.0 − 15.0) = 10.00 cm · <b>M</b> = y′/y = +2.47 ≈ −s′/s = +2.50' },
   { 'el': '#graphSection', 'prep': "setMode('auto'); clearTable(); ['sl-f','vi-f'].forEach(i => $(i).value = 10); [15, 20, 25, 30, 40, 50].forEach(s => { ['sl-do','vi-do'].forEach(i => $(i).value = s); recordData(); }); drawAll(); drawGraph()",
     'title': 'กราฟ 1/s′ กับ 1/s หา f',
     'text': 'สรุปผลด้วยกราฟ (ทำเองบนกระดาษกราฟ หรือ <b>⚡ อัตโนมัติ</b> สำหรับสมาชิก ปรับ s แล้วกดบันทึกทีละจุด) · จุดเรียงเป็น<b>เส้นตรงความชัน −1</b> เพราะ 1/s′ = 1/f − 1/s<br>⑥ <b>จุดตัดแกนทั้งสอง = 1/f</b>',
     'out': 'จุดตัดแกน = 0.100 cm⁻¹ → <b>f</b> = 10 cm · R = 2f = 20 cm · ตรงกับ Part A และ f จากสมการกระจกทุกแถว' },
  ],
 }
