# -*- coding: utf-8 -*-
# Lab 67 อัตราเร็วเชิงมุมกับเชิงเส้น — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# คาบ = ประตูแสงของแลปเอง (stepPhys ผ่าน tick) · v = เครื่องวัดความเร็วผิวของแลป (คลาด ±1%)
# รัศมีล้อปริศนา (MYST_R) และความคลาดของมอเตอร์ (MOTOR_ERR) สุ่มเป็น const ทุกครั้งที่เปิดหน้า
#   → ตรึงค่าตัวอย่าง r = 7.5 cm และมอเตอร์ +1.0% เฉพาะ browser ที่ถ่ายภาพ (แทนชื่อในสำเนาฟังก์ชัน)
GUIDE = {
  'title': 'ตรวจ v = ωr · แกนร่วม สายพาน เฟือง จักรยาน และหารัศมีล้อปริศนา',
  'setup': r"""
    /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองเอง (tick) · สุ่มแบบมีเมล็ด ให้ภาพตรงกับข้อความ */
    simSpeed = 0;
    /* ความคลาดของเครื่องวัด (noise) ใช้ตัวสุ่มมีเมล็ดของตัวเอง — ภาพ 3D/สคริปต์อื่นเรียก Math.random ระหว่างเฟรม */
    { let s = 67; window.__rnd = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
    window.__nz = s => 1 + (__rnd() - 0.5) * 2 * s;
    window.__MR = 7.5; window.__ME = 1.010;
    window.__rB = () => myst ? __MR : rBsel;
    const fx = f => (0, eval)('(' + f.toString().replace(/\brB\(\)/g, '__rB()').replace(/MOTOR_ERR/g, '__ME').replace(/\bnoise\(/g, '__nz(') + ')');
    wheels = fx(wheels); layout = fx(layout); rebuild3D = fx(rebuild3D); updateHint = fx(updateHint); stepPhys = fx(stepPhys); record = fx(record);
    { const base = fx(_drawDiagBase); drawDiag = function(){ base(); drawCanvasBar(); }; }
    /* หมุนจนรอบมอเตอร์นิ่งและประตูแสงวัดคาบครบทุกล้อ */
    window.__settle = () => { rpm = rpmSet; resetGates(); let k = 0; while (k++ < 300) tick(0.02); drawAll(); };
    window.__rec = (c, rb) => { setCfg(c); setRB(rb); __settle(); record(); };
    window.__B = () => setTimeout(() => { const w = $('tableA'); w.scrollTop = 1e4; }, 400);
  """,
  'steps': [
   { 'el': ['#cfgBtns', '#rowRB'], 'prep': "setMode('manual'); resetLab(); rows = []; recId = 0; drawGraph(); setCfg(0); setRB(4); setRpm(60); __settle(); scrollTo(0,0)",
     'title': 'แกนร่วม: ตั้งรัศมีล้อ B = 4 cm',
     'text': 'กด <b>① แกนร่วม</b> ล้อ A (r<sub>A</sub> = 10 cm) และล้อ B ยึดบนแกนเดียวกัน · เลื่อน <b>รัศมีล้อ B</b> เป็น 4 cm · มอเตอร์ตั้ง 60 rpm<br><small>หน้าปัดมอเตอร์บอกรอบโดยประมาณ (คลาดได้ ±3%) จึงต้องวัดคาบเอง</small>',
     'out': '<b>r<sub>A</sub></b> = 10 cm · <b>r<sub>B</sub></b> = 4.0 cm' },
   { 'el': '#view3d', 'prep': "setView('iso')",
     'title': 'ดูอุปกรณ์: ประตูแสงที่ล้อทุกล้อ',
     'text': 'กด <b>มุมเฉียง</b> ดูล้อ A (สีฟ้า) กับล้อ B (สีส้ม) ซ้อนกันบนแกนเดียว · ล้อแต่ละล้อมี<b>ประตูแสง</b>จับแถบสะท้อนแสงบนล้อ ทุกครั้งที่ล้อหมุนครบรอบ ประตูแสงจับเวลาได้ 1 คาบ<br><small>ต้องให้ล้อหมุนผ่านอย่างน้อย 2 รอบ ประตูแสงจึงแสดงคาบ</small>' },
   { 'el': '#diagCanvas', 'prep': "setView('front'); drawAll()",
     'title': 'อ่านคาบและอัตราเร็วที่ขอบ',
     'text': 'ในแผนภาพ 2 มิติ อ่านกรอบ <b>ประตูแสง: คาบ T</b> ของล้อ A และ B และค่าจาก<b>เครื่องวัดความเร็วผิวที่ขอบ</b> (m/s)<br><small>สังเกต: คาบของ A และ B เท่ากัน แต่อัตราเร็วที่ขอบไม่เท่ากัน</small>',
     'out': '<b>T<sub>A</sub> ≈ T<sub>B</sub></b> ≈ 0.99 s · <b>v<sub>A</sub></b> ≈ 0.635 m/s · <b>v<sub>B</sub></b> ≈ 0.254 m/s' },
   { 'el': ['[onclick="record()"]', '#tableA'], 'prep': "record()",
     'title': 'กดจด → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 จดคาบและอัตราเร็วที่ขอบของทุกล้อ</b> ตารางเพิ่ม 1 แถวต่อล้อ แล้วคำนวณ:<br>① อัตราเร็วเชิงมุม <b>ω = 2π / T</b> = 2π / 0.9912 = 6.34 rad/s<br>② <b>ωr</b> = 6.34 × 0.10 = 0.634 m/s (ล้อ A) · 6.34 × 0.04 = 0.254 m/s (ล้อ B)<br>③ เทียบกับ <b>v วัด</b> จากเครื่องวัดความเร็วผิว',
     'out': '<b>ω<sub>A</sub> = ω<sub>B</sub></b> ≈ 6.34 rad/s · <b>v วัด</b> = 0.636 และ 0.253 m/s ≈ ωr ทั้งสองล้อ' },
   { 'el': ['#tableA', '#summary'], 'prep': "__rec(0, 6); __rec(0, 8); __B()",
     'title': 'เปลี่ยน r_B = 6, 8 cm แล้วจดซ้ำ',
     'text': 'เลื่อนรัศมีล้อ B เป็น 6 และ 8 cm รอประตูแสงวัดคาบใหม่ แล้วจดทุกครั้ง · ใต้ตารางบอกอัตราส่วน <b>ω<sub>B</sub>/ω<sub>A</sub></b> และ <b>v<sub>B</sub>/v<sub>A</sub></b> ของแต่ละครั้ง',
     'out': 'แกนร่วม: <b>ω<sub>B</sub>/ω<sub>A</sub> = 1</b> ทุกครั้ง · <b>v<sub>B</sub>/v<sub>A</sub> ≈ r<sub>B</sub>/r<sub>A</sub></b> = 0.4 · 0.6 · 0.8' },
   { 'el': '#view3d', 'prep': "setCfg(1); setRB(4); __settle(); setView('iso')",
     'title': 'สายพาน: คล้องล้อ A กับล้อ B',
     'text': 'กด <b>② สายพาน</b> ล้อ A และ B อยู่คนละแกน คล้องด้วยสายพานเส้นเดียว (ไม่ลื่น) · ตั้ง r<sub>B</sub> = 4 cm · สังเกตว่า<b>ล้อเล็กหมุนเร็วกว่า</b>ล้อใหญ่<br><small>ทุกจุดบนสายพานเคลื่อนที่ด้วยอัตราเร็วเท่ากัน ขอบล้อทั้งสองจึงมีอัตราเร็วเท่ากัน</small>' },
   { 'el': ['#tableA', '#summary'], 'prep': "record(); __rec(1, 6); __rec(1, 8); __B()",
     'title': 'จดค่าสายพานที่ r_B = 4, 6, 8 cm',
     'text': 'จดที่ r<sub>B</sub> = 4, 6, 8 cm · ในตาราง <b>v วัด</b> ของล้อ A และ B เกือบเท่ากัน แต่ ω ต่างกัน<br>จาก v<sub>A</sub> = v<sub>B</sub> → <b>ω<sub>A</sub>r<sub>A</sub> = ω<sub>B</sub>r<sub>B</sub></b> → ω<sub>B</sub>/ω<sub>A</sub> = r<sub>A</sub>/r<sub>B</sub>',
     'out': 'สายพาน: <b>v<sub>B</sub>/v<sub>A</sub> ≈ 1</b> · <b>ω<sub>B</sub>/ω<sub>A</sub></b> ≈ 2.51 · 1.67 · 1.25 (= 10/4 · 10/6 · 10/8)' },
   { 'el': '#view3d', 'prep': "setCfg(2); setRB(5); __settle(); setView('front')",
     'title': 'เฟืองขบกัน: สังเกตทิศการหมุน',
     'text': 'กด <b>③ เฟืองขบกัน</b> เฟือง A (40 ฟัน) ขบกับเฟือง B (ฟัน = 4 × r) ตั้ง r<sub>B</sub> = 5 cm · ฟันที่ขบกันเคลื่อนที่ไปด้วยกัน ขอบเฟืองจึงมีอัตราเร็วเท่ากันเหมือนสายพาน แต่<b>เฟือง B หมุนทิศตรงข้าม</b>กับเฟือง A' },
   { 'el': ['#tableA', '#summary'], 'prep': "record(); __B()",
     'title': 'จดค่าเฟือง',
     'text': 'กด 📝 จด · คอลัมน์ <b>ทิศ</b> บอกว่าเฟือง A หมุนทวนเข็ม เฟือง B หมุนตามเข็มนาฬิกา · ตรวจ ω<sub>B</sub>/ω<sub>A</sub> = r<sub>A</sub>/r<sub>B</sub> = 10/5',
     'out': 'เฟือง: <b>ω<sub>B</sub>/ω<sub>A</sub> ≈ 2.00</b> · v<sub>B</sub>/v<sub>A</sub> ≈ 1 · หมุน<b>ทิศตรงข้าม</b>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "drawGraph()",
     'title': 'กราฟ v วัด กับ ωr',
     'text': 'ทุกล้อ ทุกรูปแบบการต่อ จุดอยู่บน<b>เส้นตรงผ่านจุดกำเนิด</b> ใกล้เส้นประ v = ωr · ความชันใต้กราฟควรเท่ากับ 1',
     'out': '<b>ความชัน ≈ 1.00</b> → <b>v = ωr</b>' },
   { 'el': ['label:has(#chkMyst)', '#rowRB'], 'prep': "setCfg(1); setMyst(true); __settle(); setView('iso')",
     'title': 'ล้อ B ปริศนา: ไม่ทราบรัศมี',
     'text': 'กลับไปแบบ <b>② สายพาน</b> แล้วติ๊ก <b>ใช้ล้อ B ปริศนา</b> แถบรัศมีถูกล็อก (แสดง ? cm) · รอประตูแสงวัดคาบ แล้วจด<br><small>ใช้แบบเฟืองขบกันก็ได้ หลักเดียวกัน</small>' },
   { 'el': ['#tableA', '#summary'], 'prep': "record(); __B()",
     'title': 'คำนวณรัศมีล้อปริศนา',
     'text': 'ล้อปริศนาในตารางมี r = ? · ใช้ความสัมพันธ์ของสายพาน<br>① <b>r<sub>B</sub> = r<sub>A</sub> ω<sub>A</sub> / ω<sub>B</sub></b><br>② หรือ <b>r<sub>B</sub> = v<sub>B</sub> / ω<sub>B</sub></b> จากเครื่องวัดความเร็วผิว<br>ใต้ตารางคำนวณให้ทั้งสองวิธี (ตัวเลขสีเหลือง)',
     'out': 'r<sub>A</sub>ω<sub>A</sub>/ω<sub>B</sub> ≈ 7.52 cm · v<sub>B</sub>/ω<sub>B</sub> ≈ 7.50 cm → <b>r<sub>B</sub></b> ≈ 7.5 cm ในภาพตัวอย่าง (สุ่มทุกครั้งที่เปิดหน้า ในช่วง 3.5–11.5 cm)' },
   { 'el': ['#view3d'], 'prep': "setMyst(false); setCfg(3); setRB(5); __settle(); setView('front')",
     'title': 'จักรยาน: จานหน้า โซ่ เฟืองหลัง ล้อหลัง',
     'text': 'กด <b>④ จักรยาน</b> จานหน้า A (r 10 cm) ขับโซ่ไปเฟืองหลัง B · <b>ล้อหลัง C</b> (R = 33 cm) อยู่บนแกนเดียวกับ B · มอเตอร์ = รอบการปั่น 60 rpm<br>① โซ่: <b>ω<sub>B</sub> = ω<sub>A</sub> r<sub>A</sub>/r<sub>B</sub></b> ② แกนร่วม: <b>ω<sub>C</sub> = ω<sub>B</sub></b> ③ <b>v<sub>จักรยาน</sub> = ω<sub>C</sub> × 0.33 m</b>' },
   { 'el': ['#tableA', '#summary'], 'prep': "record(); __rec(3, 3); __B()",
     'title': 'เปลี่ยนเฟืองหลัง แล้วเทียบความเร็ว',
     'text': 'จดที่เฟืองหลัง r<sub>B</sub> = 5 cm แล้วเปลี่ยนเป็น 3 cm (ปั่นรอบเท่าเดิม) จดอีกครั้ง · ใต้ตารางบอกความเร็วล้อหลัง เทียบกับมาตรวัดบนแฮนด์ในแถบสถานะใต้ภาพ 3D',
     'out': 'r<sub>B</sub> = 5 cm: v ≈ 4.20 m/s (15.1 km/h) · r<sub>B</sub> = 3 cm: v ≈ 6.96 m/s (25.1 km/h) → <b>เฟืองหลังเล็กลง จักรยานเร็วขึ้น</b>' },
  ],
 }
