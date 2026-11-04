# -*- coding: utf-8 -*-
# Lab 14 มวลและน้ำหนัก (บาลานซ์ความเฉื่อย) — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# คาบมาจาก REF/interpolateT ของแลป · เวลาที่หยุดนาฬิกา = N·T + ช้าไปเล็กน้อยจากการกดหยุดด้วยมือ (0.04–0.07 s เวลาการทดลอง)
GUIDE = {
  'title': 'หามวลวัตถุด้วยบาลานซ์ความเฉื่อย แล้วหาน้ำหนักบนดาวต่าง ๆ',
  'setup': r"""
    /* ใช้วัตถุ Unknown ค่าอ้างอิง 1.2 C clamp (ค่าตั้งต้นของแลป) · ปุ่ม 🎲 สุ่มจะสุ่ม 0.4–2.8 */
    unknownMass = 1.2;
    window.__sel = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change')); };
    /* จับเวลาตามแบบจำลองของแลป: นาฬิกา = เวลาการทดลอง animTime · โปรแกรมนับรอบจาก ω */
    window.__start = n => { __sel('clampSel', String(n)); startExperiment(); clearInterval(stopwatchInterval); stopwatchInterval = null; };
    window.__mid = (n, k) => { __start(n); animTime = k * getEffectiveT(n); stopwatchTick(); animSpeed = 0; };
    window.__stop = (n, late) => { if (!expRunning) __start(n); animSpeed = 0.5; animTime = targetVibs * getEffectiveT(n) + late; stopwatchTick(); finishExperiment('manual'); };
    window.__meas = (n, late) => { __stop(n, late); recordData(); };
  """,
  'steps': [
   { 'el': ['.canvas-wrap', '.ctrl-bar'], 'prep': "document.getElementById('mManual').click(); __sel('planetSel', 'earth'); __sel('targetSel', '20'); __sel('clampSel', '0'); setView('iso'); scrollTo(0,0)",
     'title': 'ดูอุปกรณ์: บาลานซ์ความเฉื่อย',
     'text': '<b>บาลานซ์ความเฉื่อย</b> = ถาดใส่มวลยึดกับ<b>แผ่นสปริง 2 แผ่น</b> ที่ยึดปลายไว้กับแท่น · ดึงถาดแล้วปล่อย ถาดจะ<b>สั่นในแนวระดับ</b><br>ถาดสั่นในแนวระดับ แรงโน้มถ่วงจึงไม่มีผลต่อการสั่น · <b>คาบ T ขึ้นกับมวลบนถาดเท่านั้น</b> มวลมาก (ความเฉื่อยมาก) สั่นช้า<br><small>มวลมาตรฐาน = <b>C clamp</b> (ตัวหนีบ C) · 1 C clamp มีน้ำหนัก 0.900 N บนโลก</small>',
     'out': 'มวลมาตรฐาน 1 C clamp = 0.900 N ÷ 9.80 m/s² = 0.0918 kg' },
   { 'el': ['.mode-toggle', '#clampSel', '#targetSel', '#planetSel'], 'prep': "__sel('clampSel', '0'); __sel('targetSel', '20')",
     'title': 'เลือกมวล 0 C clamp และจำนวนรอบ 20 รอบ',
     'text': 'เลือกโหมด <b>✏️ บันทึกเอง</b> · มวล <b>0 C clamps</b> (ถาดเปล่า) · จำนวนรอบที่จะจับเวลา <b>20 รอบ</b> · ดาว <b>🌍 โลก</b><br><small>จับเวลาหลายรอบแล้วหาร จะได้คาบแม่นกว่าจับรอบเดียว</small>',
     'out': 'm = 0 C clamp · N = 20 รอบ' },
   { 'el': ['.canvas-wrap', '#btnStart'], 'prep': "__mid(0, 12.4); setView('iso')",
     'title': 'กด ▶ เริ่มจับเวลา แล้วนับรอบ',
     'text': 'กด <b>▶ เริ่มจับเวลา</b> ถาดเริ่มสั่นพร้อมนาฬิกาเดิน · ตัวเลขใหญ่กลางภาพ = <b>จำนวนรอบ</b>ที่ถาดสั่นครบ (ไป–กลับ 1 ครั้ง = 1 รอบ)<br><small>ปุ่ม ⏱ ช้า/เร็ว ชะลอภาพให้นับทัน คาบที่วัดได้ไม่เปลี่ยน</small>',
     'out': 'ระหว่างจับเวลา: นับได้ 12 รอบ' },
   { 'el': ['#btnStart', '.result-sec'], 'prep': "__stop(0, 0.06)",
     'title': 'ครบ 20 รอบ กด ⏹ หยุดจับเวลา',
     'text': 'เมื่อตัวเลขขึ้น <b>20</b> กด <b>⏹ หยุดจับเวลา</b> ทันที · อ่านเวลาในกรอบ <b>🎯 ผลการวัด</b> แล้วคำนวณ<br>① <b>T = เวลา ÷ จำนวนรอบ</b> = 5.72 ÷ 20<br><small>กดหยุดช้าไปเล็กน้อย เวลาจึงเกินไปบ้าง — ฝึกกดให้ตรงจังหวะ</small>',
     'out': 'เวลา 20 รอบ = 5.72 s → <b>T</b> = 0.286 s (0 C clamp)' },
   { 'el': '.data-tbl', 'prep': "recordData()",
     'title': 'กด 💾 บันทึกลงตาราง',
     'text': 'กด <b>💾 บันทึกลงตาราง</b> (ใต้ภาพ) จำนวน C clamp · รอบ · เวลา · T ลงตาราง 1 แถว และจุดสีฟ้าขึ้นบนกราฟ',
     'out': 'แถว 1: 0 C clamp · 20 รอบ · 5.72 s · T = 0.286 s' },
   { 'el': ['.data-tbl', '#chartCanvas'], 'prep': "__meas(1, 0.04); __meas(2, 0.07); __meas(3, 0.05)",
     'title': 'เพิ่มมวลเป็น 1, 2, 3 C clamp แล้ววัดซ้ำ',
     'text': 'เปลี่ยนมวลเป็น <b>1</b>, <b>2</b> และ <b>3 C clamps</b> แล้วจับเวลา 20 รอบ → บันทึก ทีละค่า<br>จุดบนกราฟ <b>T กับจำนวน C clamp</b> สูงขึ้นตามมวล: มวลมาก ความเฉื่อยมาก ถาดเปลี่ยนสภาพการเคลื่อนที่ได้ยาก จึงสั่นช้าลง<br><small>เส้นประบนกราฟ = กราฟมาตรฐานของบาลานซ์ (ใช้อ่านมวลในขั้นต่อไป)</small>',
     'out': 'T = 0.286 · 0.335 · 0.393 · 0.444 s (0 · 1 · 2 · 3 C clamp)' },
   { 'el': ['.result-sec', '#clampSel'], 'prep': "__stop('unknown', 0.05)",
     'title': 'วางวัตถุ Unknown บนถาด แล้วจับเวลา',
     'text': 'เลือก <b>Unknown object</b> (วัตถุที่ไม่ทราบมวล) จับเวลา 20 รอบแบบเดิม<br>① <b>T = 6.94 ÷ 20</b><br><small>ปุ่ม 📌 อ้างอิง = วัตถุตามใบงาน · 🎲 สุ่ม = สุ่มมวลใหม่ (ซ่อนค่า)</small>',
     'out': 'เวลา 20 รอบ = 6.94 s → <b>T</b><sub>Unknown</sub> = 0.347 s' },
   { 'el': ['#chartCanvas', '.data-tbl'], 'prep': "recordData()",
     'title': 'บันทึก แล้วอ่านมวลจากกราฟ',
     'text': 'กด <b>💾 บันทึกลงตาราง</b> · บนกราฟลากเส้นแนวนอนที่ T = 0.347 s ไปตัดกราฟมาตรฐาน แล้วลากลงอ่านค่าบนแกน <b>จำนวน C clamp</b> (เส้นประสีชมพู)<br><small>มวลมีค่าระหว่าง 1 กับ 2 C clamp เพราะ T อยู่ระหว่าง 0.335 กับ 0.393 s · กรอบ 🎯 เฉลยค่าจริงหลังบันทึก</small>',
     'out': '<b>m</b><sub>Unknown</sub> ≈ 1.24 C clamp (ค่าจริง 1.20) = 1.24 × 0.0918 ≈ 0.114 kg' },
   { 'el': '.calc-highlight', 'prep': "",
     'title': 'คำนวณน้ำหนักบนโลก',
     'text': 'แผง <b>🧮 การคำนวณน้ำหนัก Unknown</b> ใช้มวลจากกราฟ:<br>② น้ำหนัก 1 C clamp บนดาวนี้ <b>W₁ = m₁g</b> = 0.0918 × 9.80 = 0.900 N<br>③ <b>W = (จำนวน C clamp) × W₁</b> = 1.24 × 0.900',
     'out': '<b>W</b><sub>โลก</sub> ≈ 1.12 N' },
   { 'el': ['#wmeasInput', '#errDisplay'], 'prep': "document.getElementById('wmeasInput').value = '1.08'; updateError()",
     'title': 'เทียบกับน้ำหนักที่ชั่งได้',
     'text': 'กรอกน้ำหนักที่ชั่งด้วย<b>เครื่องชั่งสปริง</b> ในช่อง <b>W<sub>meas</sub></b> (วัตถุนี้ชั่งได้ 1.20 × 0.900 = 1.08 N) โปรแกรมคำนวณ<br>④ ร้อยละความคลาดเคลื่อน = |W<sub>calc</sub> − W<sub>meas</sub>| ÷ W<sub>meas</sub> × 100',
     'out': 'W<sub>meas</sub> = 1.08 N · ความคลาดเคลื่อน ≈ 3.7 %' },
   { 'el': ['.result-sec', '#planetSel'], 'prep': "__sel('planetSel', 'moon'); __meas('unknown', 0.05); document.getElementById('wmeasInput').value = ''; updateError()",
     'title': 'ย้ายไปดวงจันทร์ แล้ววัดคาบซ้ำ',
     'text': 'เลือกดาว <b>🌙 ดวงจันทร์</b> (g = 1.62 m/s²) แล้วจับเวลาวัตถุ Unknown 20 รอบอีกครั้ง → บันทึก<br>คาบ<b>เท่าเดิม</b> เพราะการสั่นในแนวระดับขึ้นกับมวล (ความเฉื่อย) ไม่ขึ้นกับ g',
     'out': '<b>T</b><sub>ดวงจันทร์</sub> = 0.347 s = T<sub>โลก</sub> → มวลยังเป็น 1.24 C clamp' },
   { 'el': '.calc-highlight', 'prep': "updateCalc()",
     'title': 'สรุป: มวลคงเดิม แต่น้ำหนักเปลี่ยน',
     'text': 'บนดวงจันทร์ <b>W₁ = 0.0918 × 1.62 = 0.149 N</b> → <b>W = 1.24 × 0.149</b><br>ลองเปลี่ยนดาวอื่นในรายการ (คาบไม่ต้องวัดใหม่) แล้วดูน้ำหนักที่เปลี่ยน<br><b>มวล</b> = ปริมาณเนื้อสาร/ความเฉื่อย ไม่ขึ้นกับสถานที่ · <b>น้ำหนัก W = mg</b> เปลี่ยนตาม g ของดาว',
     'out': '<b>W</b><sub>ดวงจันทร์</sub> ≈ 0.185 N (≈ ⅙ ของบนโลก) · ดาวพฤหัส ≈ 2.83 N · มวล ≈ 0.114 kg เท่ากันทุกดาว' },
  ],
 }
