# -*- coding: utf-8 -*-
# Lab 82 การดีดตัวแยกบนรางลม — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# เวลาบังแสง = แบบจำลองของแลปเอง (buildRun: พลังงานสปริง → v_A, v_B · รางหน่วงเล็กน้อย · readMs ±0.2 ms)
# ค่าสุ่มตอนโหลด (พลังงานสปริง ±3% · ความหน่วงราง · มวลรถ X) ตรึงไว้เฉพาะ browser ที่ถ่ายภาพ ให้ภาพตรงกับข้อความ
GUIDE = {
  'title': 'ตรวจกฎอนุรักษ์โมเมนตัมเมื่อรถดีดตัวแยก แล้วหามวลรถปริศนา X',
  'setup': r"""
    simSpeed = 0;   /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองเอง (stepRun) */
    E_LV[0] = 0.020; E_LV[1] = 0.045; E_LV[2] = 0.080;
    window.__MX = 0.360;
    buildRun = (0, eval)('(' + buildRun.toString().replace(/mBkg\(\)/g, '(isX()?__MX:MB_OPT[bI]/1000)').replace(/\bDECEL\b/g, '0.0006') + ')');
    checkM = (0, eval)('(' + checkM.toString().replace(/\bM_X\b/g, '__MX') + ')');
    window.__k = 0;
    window.__seed = n => { let s = n; Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
    window.__fire = () => { __seed(8200 + (++__k) * 31); rearm(); fireRun(); let i = 0; while (phase === 'run' && i++ < 100000) stepRun(0.01); };
    window.__fill = () => { $('in-tA').value = fmt(lastRun.tA, 1); $('in-tB').value = fmt(lastRun.tB, 1); };
    window.__meas = (a, b, c) => { setA(a); setB(b); setComp(c); __fire(); __fill(); recordRow(); };
    window.__B = () => setTimeout(() => { document.querySelectorAll('.tbl-wrap').forEach(w => w.scrollTop = 1e4); }, 400);
  """,
  'steps': [
   { 'el': ['#aBtns', '#bBtns'], 'prep': "setMode('manual'); resetLab(); rows = []; renderAll(); setA(0); setB(0); scrollTo(0,0)",
     'title': 'เลือกมวลรถ A และรถ B',
     'text': 'เริ่มจากรถ <b>A 200 g</b> (สีน้ำเงิน ติดสปริงแผ่นอัดค้างด้วยสลัก) และรถ <b>B 200 g</b> (สีส้ม) · เพิ่มมวลได้ด้วยก้อนเหล็กก้อนละ 100 g<br><small>ก่อนปลดสลัก รถทั้งสองอยู่นิ่ง โมเมนตัมรวมเป็นศูนย์</small>',
     'out': '<b>m<sub>A</sub></b> = 200 g · <b>m<sub>B</sub></b> = 200 g' },
   { 'el': ['#compBtns', '#cardBtns'], 'prep': "setComp(1); setCard(1)",
     'title': 'ตั้งระดับสปริงและการ์ดบังแสง',
     'text': 'เลือกสปริง <b>ระดับ 2</b> และการ์ดบังแสงกว้าง <b>d = 5.0 cm</b> (ติดบนรถทั้งสองคัน)<br><small>สปริงอัดระดับเดียวกันปล่อยพลังงานเท่ากันทุกครั้ง ไม่ขึ้นกับมวลรถ</small>',
     'out': '<b>d</b> = 5.0 cm = 0.050 m · สปริงระดับ 2' },
   { 'el': '#view3d', 'prep': "setView('front')",
     'title': 'วางรถคู่และโฟโตเกต',
     'text': 'ลาก<b>รถคู่</b>ไว้กลางราง แล้วลาก <b>เกต 1</b> ไว้ทางซ้ายของรถ A และ <b>เกต 2</b> ไว้ทางขวาของรถ B ใกล้ ๆ · ตำแหน่งแสดงที่กรอบ <b>เกต 1 · เกต 2</b> ในแผงด้านข้าง<br><small>วางเกตใกล้รถ แรงต้านเล็กน้อยของรางจะไม่ทำให้ความเร็วลดลงก่อนวัด</small>',
     'out': 'รอยต่อรถคู่ 60.0 cm · เกต 1 = 36.0 cm · เกต 2 = 84.0 cm' },
   { 'el': ['#ab-fire', '#view3d'], 'prep': "__seed(8200); rearm(); fireRun(); for (let i = 0; i < 22; i++) stepRun(0.01); setView('iso')",
     'title': 'ปลดสลัก ให้สปริงดันรถแยกกัน',
     'text': 'กด <b>▶ ปลดสลัก</b> สปริงดันรถ A ไปทาง<b>ซ้าย</b> และรถ B ไปทาง<b>ขวา</b> พร้อมกัน · การ์ดบนรถแต่ละคันบังแสงของเกตที่อยู่ข้างหน้า เครื่องจับเวลาจับเวลาที่แสงถูกบัง<br><small>แรงที่สปริงดันรถทั้งสองมีขนาดเท่ากัน ทิศตรงข้าม ในช่วงเวลาเดียวกัน</small>' },
   { 'el': '#view3d', 'prep': "__k = 0; __fire(); setView('tm')",
     'title': 'อ่านเวลาบังแสงที่จอจับเวลา',
     'text': 'รอรถผ่านเกตทั้งสอง แล้วกด <b>🔍 จอจับเวลา</b> · อ่าน <b>t<sub>A</sub></b> = เกต 1 ครั้งที่ 1 (รถ A) และ <b>t<sub>B</sub></b> = เกต 2 ครั้งที่ 1 (รถ B)<br><small>ครั้งที่ 2 ของแต่ละเกตคือรถที่สะท้อนกลับจากปลายราง ไม่ใช้</small>',
     'out': '<b>t<sub>A</sub></b> = 108.1 ms · <b>t<sub>B</sub></b> = 108.1 ms' },
   { 'el': ['#in-tA', '#in-tB'], 'prep': "__fill(); setView('iso')",
     'title': 'กรอกเวลาลงใบบันทึก',
     'text': 'กรอก t<sub>A</sub> ลงช่อง <b>②</b> และ t<sub>B</sub> ลงช่อง <b>③</b> (หน่วย ms) · ช่อง ① แสดงความกว้างการ์ดและมวลรถให้แล้ว',
     'out': '<b>t<sub>A</sub></b> = 108.1 ms · <b>t<sub>B</sub></b> = 108.1 ms' },
   { 'el': '#lastRec', 'prep': "recordRow()",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> ค่าเข้าตาราง และ <b>📊 ผลที่บันทึกล่าสุด</b> คำนวณต่อ (ทิศขวาเป็น +):<br>① <b>v<sub>A</sub> = −d / t<sub>A</sub></b> (รถ A ไปทางซ้าย จึงเป็นลบ) · <b>v<sub>B</sub> = +d / t<sub>B</sub></b><br>② โมเมนตัม <b>p<sub>A</sub> = m<sub>A</sub>v<sub>A</sub></b> · <b>p<sub>B</sub> = m<sub>B</sub>v<sub>B</sub></b><br>③ โมเมนตัมรวม <b>p<sub>A</sub> + p<sub>B</sub></b> เทียบกับ 0<br>④ <b>Ek = ½mv²</b> ของรถแต่ละคันและรวม',
     'out': '<b>v<sub>A</sub></b> = −0.4625 m/s · <b>v<sub>B</sub></b> = +0.4625 m/s · <b>p<sub>A</sub></b> = −0.0925 · <b>p<sub>B</sub></b> = +0.0925 kg·m/s → <b>p<sub>A</sub> + p<sub>B</sub></b> = 0 · Ek รวม = 42.8 mJ (A ได้ 50 %)' },
   { 'el': '#tableA', 'prep': "[[0,1,1],[0,2,1],[1,0,1],[2,0,1],[0,0,0],[2,0,0],[0,0,2],[0,2,2]].forEach(m => __meas(...m)); setA(0); setB(0); setComp(1); renderAll(); __B()",
     'title': 'เปลี่ยนมวลและสปริง แล้ววัดซ้ำ',
     'text': 'กด <b>↩ ตั้งรถใหม่</b> เปลี่ยนมวลรถให้ <b>m<sub>A</sub>/m<sub>B</sub></b> ต่างกันอย่างน้อย 3 ค่า (สปริงระดับ 2) แล้วลองสปริง<b>ระดับ 1</b> และ <b>ระดับ 3</b> · ปลดสลัก อ่านเวลา บันทึกทุกครั้ง · ตาราง ① แสดง v, p และ <b>p<sub>A</sub> + p<sub>B</sub></b> (สีเหลือง) ทุกแถว',
     'out': 'สปริงระดับ 2: m<sub>A</sub>/m<sub>B</sub> = 1 · 0.667 · 0.5 · 1.5 · 2 → t<sub>A</sub> = 108.1 · 97.8 · 92.2 · 147.6 · 185.3 ms · t<sub>B</sub> = 108.1 · 146.8 · 184.8 · 98.4 · 92.4 ms<br><b>(p<sub>A</sub> + p<sub>B</sub>)/|p<sub>A</sub>|</b> ทุกแถวอยู่ในช่วง −0.2 % ถึง +0.3 % (เฉลี่ย 0.0 %) → <b>โมเมนตัมรวมหลังดีดแยกยังเป็นศูนย์</b>' },
   { 'el': '#tableB', 'prep': "__B()",
     'title': 'อ่านตาราง ② อัตราส่วนและพลังงานจลน์',
     'text': 'เทียบคอลัมน์ <b>|v<sub>B</sub>|/|v<sub>A</sub>|</b> กับ <b>m<sub>A</sub>/m<sub>B</sub></b> และ <b>A ได้ (%)</b> กับ <b>m<sub>B</sub>/(m<sub>A</sub>+m<sub>B</sub>)</b> · ดู <b>Ek รวม</b> ของสปริงระดับเดียวกัน<br><small>รถเบาเคลื่อนที่เร็วกว่าและได้พลังงานจลน์มากกว่า เพราะ Ek = p²/2m และ p ของรถทั้งสองเท่ากัน</small>',
     'out': 'แถว 6–9: m<sub>A</sub>/m<sub>B</sub> = 1 · 2 · 1 · 0.5 → |v<sub>B</sub>|/|v<sub>A</sub>| = 1.000 · 2.001 · 0.999 · 0.501 · A ได้ 50.0 · 33.3 · 50.1 · 66.6 % (ทฤษฎี 50.0 · 33.3 · 50.0 · 66.7 %)<br><b>Ek รวมเฉลี่ย</b> = 19.5 mJ (ระดับ 1) · 43.5 mJ (ระดับ 2) · 77.3 mJ (ระดับ 3)' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('pp')",
     'title': 'กราฟ |p_B| กับ |p_A|',
     'text': 'กด <b>|p_B| – |p_A|</b> จุดทุกจุดอยู่บน<b>เส้นตรงความชัน 1 ผ่านจุดกำเนิด</b> แปลว่าโมเมนตัมของรถทั้งสองมีขนาดเท่ากัน ทิศตรงข้าม<br><small>0 = m<sub>A</sub>v<sub>A</sub> + m<sub>B</sub>v<sub>B</sub></small>',
     'out': '<b>ความชัน</b> = 1.000 → |p<sub>A</sub>| = |p<sub>B</sub>| ทุกคู่มวลและทุกระดับสปริง' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('rv')",
     'title': 'กราฟ |v_B|/|v_A| กับ m_A/m_B',
     'text': 'กด <b>|v_B|/|v_A| – m_A/m_B</b> จุดเรียงบนเส้นตรงความชัน 1 ผ่านจุดกำเนิด → <b>|v<sub>B</sub>| / |v<sub>A</sub>| = m<sub>A</sub> / m<sub>B</sub></b> (รถหนักเคลื่อนที่ช้ากว่า)',
     'out': '<b>ความชัน</b> ≈ 1 · ทุกจุดตกบนเส้นประ |v<sub>B</sub>|/|v<sub>A</sub>| = m<sub>A</sub>/m<sub>B</sub>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('ek')",
     'title': 'กราฟ Ek รวม',
     'text': 'กด <b>Ek รวม</b> จุดของสปริงระดับเดียวกัน (สีเดียวกัน) อยู่<b>ระดับเดียวกันทุกอัตราส่วนมวล</b> → พลังงานจลน์รวมไม่ขึ้นกับมวลรถ มาจากพลังงานศักย์ยืดหยุ่นของสปริง (สูญเสียเป็นความร้อน/เสียงเล็กน้อย)',
     'out': '<b>Ek รวม</b> ≈ 19.5 · 43.5 · 77.3 mJ (สปริงระดับ 1 · 2 · 3) ไม่ขึ้นกับคู่มวล' },
   { 'el': ['.ans-row:has(#ans-k)', '#ansKMsg'], 'prep': "$('ans-k').value = (100 * 400 / 600).toFixed(1); checkK()",
     'title': 'ทำนายการแบ่งพลังงานจลน์',
     'text': 'รถ A 200 g กับรถ B 400 g ดีดแยกกัน รถ A ได้พลังงานจลน์กี่ % ของทั้งหมด · ใช้ <b>Ek<sub>A</sub> / Ek<sub>รวม</sub> = m<sub>B</sub> / (m<sub>A</sub> + m<sub>B</sub>)</b> = 400 / 600 · กรอกแล้วกด <b>ตรวจคำทำนาย</b> (เทียบกับแถว 200 g / 400 g ในตาราง ②)',
     'out': '<b>Ek<sub>A</sub></b> = 66.7 % ของพลังงานจลน์รวม' },
   { 'el': '#tableA', 'prep': "__meas(0, 3, 1); __meas(2, 3, 1); renderAll(); __B()",
     'title': 'เปลี่ยนรถ B เป็นรถปริศนา X',
     'text': 'กด <b>❓ X</b> (รถสีม่วง มีฝาปิด ไม่ทราบมวล) ปลดสลัก อ่าน t<sub>A</sub> t<sub>B</sub> แล้วบันทึกแบบเดิม · ทำอย่างน้อย 2 แถว (เช่น m<sub>A</sub> = 200 g และ 400 g) · แถวสีม่วงคำนวณ<br>⑤ <b>m<sub>X</sub> = m<sub>A</sub>|v<sub>A</sub>| / |v<sub>B</sub>| = m<sub>A</sub> · t<sub>B</sub> / t<sub>A</sub></b> (การ์ดกว้างเท่ากันจึงตัดกันไป)',
     'out': 'm<sub>A</sub> = 200 g: t<sub>A</sub> = 94.4 ms · t<sub>B</sub> = 170.3 ms → m<sub>X</sub> = 361 g<br>m<sub>A</sub> = 400 g: t<sub>A</sub> = 157.3 ms · t<sub>B</sub> = 141.2 ms → m<sub>X</sub> = 359 g · <b>เฉลี่ย 360 g</b>' },
   { 'el': ['.ans-row:has(#ans-m)', '#ansMMsg'], 'prep': "{ const X = goodRows().filter(q => q.X); $('ans-m').value = (X.reduce((a, q) => a + q.mEst, 0) / X.length).toFixed(0); } checkM()",
     'title': 'ตอบมวลรถปริศนา X',
     'text': 'นำค่าเฉลี่ย m<sub>X</sub> ใต้ตาราง ① กรอกในกรอบ <b>🎯 ตรวจคำตอบ</b> แล้วกด <b>ตรวจมวล X</b> (ยอมคลาด 5%)',
     'out': '<b>m<sub>X</sub></b> ≈ 360 g ในภาพตัวอย่าง (มวลรถ X สุ่มทุกครั้งที่เปิดแลป ในช่วง 250 – 550 g)' },
  ],
 }
