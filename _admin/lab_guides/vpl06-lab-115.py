# -*- coding: utf-8 -*-
# Lab 115 สะพานวีตสโตน — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'หาความต้านทานปริศนา X ด้วยสะพานวีตสโตน (วิธีเข็มชี้ศูนย์)',
  'setup': r"""
    /* ต่อชิ้นส่วนลงรูเดียวกับที่ผู้เรียนแตะ (elems ของแลป) · I_G มาจากตัวแก้วงจร solveCircuit() ของแลปเอง */
    window.__h = (r, c) => ({ r, c });
    window.__add = (k, a, b) => elems.push({ id: eid++, kind: k, a, b });
    window.__set = rs => { setRS(rs); stepPhys(5); };
    window.__fill = () => { $('in-i').value = (readI() * 1e6).toFixed(1); };
    /* ระยะห่าง R_S ระหว่างจุดวัด ให้ |I_G| ไม่เกินราว 120 µA (อยู่ในย่าน 200 µA) */
    window.__plan = () => { const b = SOL.br, c = RSbal(b); __set(Math.round(c) + 10); const i1 = readI(); __set(Math.round(c) - 10); const i0 = readI();
      const s = Math.abs(i1 - i0) * 1e6 / 20; window.__st = Math.max(1, Math.min(20, Math.round(50 / s))); window.__base = Math.round(c); };
    window.__scan = offs => offs.forEach(k => { const n = rows.length; __set(__base + k * __st); __fill(); recordRow();
      if (rows.length === n) throw new Error('RS=' + RSv() + ' I=' + $('in-i').value + ' ' + $('recMsg').textContent); });
  """,
  'steps': [
   { 'el': ['#view3d', '#ab-w'], 'prep': "resetLab(); __add('w', {j:'SP'}, __h(0,1)); __add('w', {j:'SN'}, __h(11,1)); onCircuitChange(); setView('iso'); scrollTo(0,0)",
     'title': 'ต่อแหล่งจ่ายเข้ารางไฟ',
     'text': 'กด <b>🔌 สายไฟ</b> แล้วแตะรู 2 รู: <b>ขั้ว + ของแหล่งจ่าย → ราง +</b> และ <b>ขั้ว − → ราง −</b> ของเบรดบอร์ด<br><small>รางไฟแต่ละรางต่อถึงกันตลอดแนว</small>' },
   { 'el': ['#view3d', '#ab-H'], 'prep': "__add('w', __h(0,3), __h(1,3)); __add('H', __h(2,3), __h(2,5)); __add('H', __h(4,5), __h(7,5)); __add('w', __h(10,5), __h(11,5)); onCircuitChange(); setView('bb')",
     'title': 'แขนคู่ที่ 1: P = 100 Ω และ Q = 100 Ω',
     'text': 'กด <b>🟫 100 Ω</b> เสียบ <b>P</b> จากคอลัมน์ที่ต่อราง + ไปยังคอลัมน์ <b>จุดกลาง B</b> แล้วเสียบ <b>Q</b> จากจุด B ไปคอลัมน์ที่ต่อราง − (ใช้สายไฟต่อคอลัมน์กับรางไฟ)<br><small>รู 5 รูในคอลัมน์เดียวกันฝั่งเดียวกันต่อถึงกัน</small>',
     'out': '<b>P</b> = 100 Ω · <b>Q</b> = 100 Ω (อัตราส่วน 1 : 1)' },
   { 'el': ['#view3d', '#ab-X'], 'prep': "__add('w', __h(0,9), __h(1,9)); __add('X', __h(2,9), __h(2,11)); __add('w', {j:'BA'}, __h(3,11)); __add('w', {j:'BB'}, __h(11,14)); onCircuitChange(); setView('iso')",
     'title': 'แขนคู่ที่ 2: ❓X และกล่องความต้านทาน R<sub>S</sub>',
     'text': 'กด <b>🟫 ❓X</b> เสียบจากคอลัมน์ที่ต่อราง + ไปยัง<b>จุดกลาง D</b> · ใช้สายไฟ 2 เส้นต่อ<b>กล่องความต้านทาน</b>: ขั้ว 1 → จุด D และขั้ว 2 → ราง −<br><small>ทดสอบวิธีก่อนได้ โดยใช้ 220 Ω แทน X</small>' },
   { 'el': ['#view3d', '#in-known'], 'prep': "__add('w', {j:'GA'}, __h(3,5)); __add('w', {j:'GC'}, __h(4,11)); onCircuitChange(); setView('iso')",
     'title': 'ต่อแกลแวนอมิเตอร์ระหว่างจุด B กับ D',
     'text': 'ต่อสายจาก<b>รู +</b> ของแกลแวนอมิเตอร์ไปจุด B และ<b>รู COM</b> ไปจุด D · เมื่อต่อถูก ช่อง <b>① สะพานที่ต่ออยู่</b> จะบอกสูตรของสะพานนี้ให้<br><small>ถ้าแขนใดมีอุปกรณ์มากกว่า 1 ชิ้น ช่องนี้จะบอกว่ายังไม่เป็นสะพานวีตสโตน</small>',
     'out': 'สะพานครบ: <b>X = R<sub>S</sub> × P/Q</b>' },
   { 'el': '[onclick="nudgeKnob(1)"]', 'prep': "setKnob(3); setRange(0); stepPhys(5); setView('am')",
     'title': 'ตั้งแหล่งจ่าย 3 V และเริ่มที่ย่าน 20 mA',
     'text': 'กด <b>1 V ▶</b> 3 ครั้ง ให้แหล่งจ่าย 3 V · แกลแวนอมิเตอร์เริ่มที่<b>ย่านใหญ่ 20 mA</b> ก่อนเสมอ เพราะตอนสะพานยังไม่สมดุล กระแสอาจมากจนเกินย่านที่ไวกว่า',
     'out': 'I<sub>G</sub> ยังไม่เป็นศูนย์ (หลาย mA) — สะพานยังไม่สมดุล' },
   { 'el': '.panel-section:has(#decBox)', 'prep': "__plan(); setRS(Math.round(__base / 10) * 10); setRange(1); stepPhys(5)",
     'title': 'ปรับ R<sub>S</sub> หลักใหญ่ก่อน ให้ I<sub>G</sub> เข้าใกล้ 0',
     'text': 'กด <b>▲ / ▼</b> ที่หลัก <b>×100</b> แล้ว <b>×10</b> ของกล่องความต้านทาน ดู<b>เครื่องหมาย</b>ของ I<sub>G</sub>: ถ้าเครื่องหมายกลับ แปลว่าผ่านจุดสมดุลไปแล้ว · เมื่อกระแสเล็กลง เปลี่ยนเป็นย่าน 2 mA',
     'out': 'R<sub>S</sub> ที่ใกล้สมดุล (ละเอียดถึงหลักสิบ)' },
   { 'el': '#rangeBtns', 'prep': "setRange(2); __set(__base - 2 * __st)",
     'title': 'เปลี่ยนเป็นย่าน 200 µA แล้วปรับหลัก ×1',
     'text': 'เมื่อ I<sub>G</sub> เล็กกว่า 0.2 mA ให้กด <b>200 µA</b> เพื่อเห็นการเปลี่ยนแปลงละเอียดขึ้น แล้วปรับหลัก <b>×1</b> ต่อ' },
   { 'el': ['#view3d', '#in-i'], 'prep': "setView('am'); __fill()",
     'title': 'อ่านกระแสแกลแวนอมิเตอร์ I<sub>G</sub>',
     'text': 'กด <b>🔍 แกลแวนอมิเตอร์</b> ซูมอ่านหน้าปัด (ศูนย์อยู่ตรงกลาง) แล้วกรอกช่อง <b>③ I<sub>G</sub> เป็น µA</b> พร้อมเครื่องหมาย + / −<br><small>ถ้าจอแสดงเป็น mA ให้คูณ 1000</small>',
     'out': '<b>I<sub>G</sub></b> (µA) ที่ R<sub>S</sub> ค่านี้' },
   { 'el': '#recForm', 'prep': "recordRow()",
     'title': 'กดบันทึก',
     'text': 'กด <b>📝 บันทึก</b> โปรแกรมเก็บ <b>R<sub>S</sub></b> จากกล่องความต้านทาน (ช่อง ②) คู่กับ <b>I<sub>G</sub></b> ที่กรอก ลงตาราง' },
   { 'el': '#tableA', 'prep': "__scan([-1, 0, 1, 2]); setView('iso')",
     'title': 'วัดซ้ำที่ R<sub>S</sub> หลายค่า ทั้งฝั่งบวกและลบ',
     'text': 'ปรับ R<sub>S</sub> ทีละน้อยรอบจุดสมดุล แล้วบันทึก I<sub>G</sub> อย่างน้อย 4–5 จุด ให้มี<b>ทั้งค่าบวก (เขียว) และค่าลบ (แดง)</b> · ค่า |I<sub>G</sub>| ไม่เกิน 150 µA<br><small>กล่องความต้านทานปรับได้ทีละ 1 Ω จึงหา R<sub>S</sub> ที่ I<sub>G</sub> = 0 พอดีไม่ได้</small>',
     'out': 'ตาราง R<sub>S</sub> – I<sub>G</sub> 5 แถว' },
   { 'el': ['#graphCanvas', '#graphNote'],
     'title': 'กราฟ I<sub>G</sub>–R<sub>S</sub> หาจุดสมดุล',
     'text': 'ใกล้จุดสมดุล I<sub>G</sub> เปลี่ยนกับ R<sub>S</sub> เป็นเส้นตรง · โปรแกรมลากเส้นตรงผ่านจุด แล้วหา<b>จุดที่เส้นตัด I<sub>G</sub> = 0</b> (วงกลมเหลือง) — ละเอียดกว่า 1 Ω<br><small>สมดุลเมื่อศักย์ไฟฟ้าที่ B เท่ากับที่ D → P/Q = X/R<sub>S</sub></small>',
     'out': '<b>R<sub>S</sub></b> ที่สมดุล → <b>X = R<sub>S</sub> × P/Q = R<sub>S</sub></b> (เพราะ P = Q)' },
   { 'el': '#graphNote', 'prep': "{ const q = elems.find(e => e.kind === 'H' && e.a.r === 4); q.kind = 'M'; onCircuitChange(); __plan(); __scan([-2, -1, 0, 1, 2]); }",
     'title': 'เปลี่ยน Q เป็น 1 kΩ (อัตราส่วน 1 : 10) แล้ววัดซ้ำ',
     'text': 'ถอด Q = 100 Ω ออก เสียบ <b>🟫 1 kΩ</b> แทน แล้วหาจุดสมดุลแบบเดิม · ตอนนี้ R<sub>S</sub> ที่สมดุลเป็น <b>10 เท่าของ X</b> การปรับทีละ 1 Ω จึงละเอียดขึ้นอีก 1 หลัก',
     'out': 'เส้นที่ 2: R<sub>S</sub> ที่ I<sub>G</sub> = 0 ≈ 10X → <b>X = R<sub>S</sub> × 100/1000</b>' },
   { 'el': '.panel-section:has(#ans-r)', 'prep': "{ const F = balFit(rows[rows.length - 1].key); $('ans-r').value = (F.R0 / 10).toFixed(1); checkR(); }",
     'title': 'สรุปค่า X แล้วตรวจคำตอบ',
     'text': 'คำนวณ <b>X = R<sub>S</sub> × P/Q</b> จากทั้งสองอัตราส่วน — ควรได้ใกล้กัน · ใช้ค่าจากอัตราส่วน 1 : 10 ซึ่งละเอียดกว่า กรอกในกรอบ 🎯 แล้วกด <b>ตรวจ</b><br><small>ค่า X ไม่ขึ้นกับแรงดันแหล่งจ่าย เพราะเงื่อนไขสมดุลมีแต่ความต้านทาน</small>',
     'out': '<b>X</b> ถูกต้องเมื่อคลาดไม่เกิน 1% (วิธีเข็มชี้ศูนย์แม่นยำมาก)' },
  ],
 }
