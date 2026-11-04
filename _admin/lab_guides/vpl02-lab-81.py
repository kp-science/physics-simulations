# -*- coding: utf-8 -*-
# Lab 81 การชนแบบแยกจากกัน (ยืดหยุ่น/ไม่ยืดหยุ่น) — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ข้อมูลทุกแถว = แบบจำลองของแลปเอง (buildRun: รถ 2 คันบนรางลม + collide(e) + โฟโตเกต 2 ตัว · เวลา ±0.2 ms)
# มวลรถ X · e ของกันชนทุกแบบ · ความหน่วงราง สุ่มทุกครั้งที่เปิดหน้า → ตรึงค่าตัวอย่างเฉพาะ browser ที่ถ่ายภาพ
GUIDE = {
  'title': 'ตรวจการอนุรักษ์โมเมนตัมและพลังงานจลน์ในการชน หาค่า e ของยาง Y และมวลรถ X',
  'setup': r"""
    /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองเอง (stepRun) · สุ่มแบบมีเมล็ด */
    setSimSpeed(0); { const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    { let s = 81; Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
    BUMPS[0].e = 0.97; BUMPS[1].e = 0.81; BUMPS[2].e = 0.58;
    window.__MX = 0.380; window.__DEC = 0.0006;
    window.__mb = () => isX() ? __MX : MB_OPT[bI] / 1000;
    const __fx = f => (0, eval)('(' + f.toString().replace(/mBkg\(\)/g, '__mb()').replace(/\bM_X\b/g, '__MX').replace(/\bDECEL\b/g, '__DEC') + ')');
    buildRun = __fx(buildRun); checkM = __fx(checkM); updateHint = __fx(updateHint); renderTable = __fx(renderTable);
    window.__go = t => { if (phase === 'done') rearm(); if (phase === 'armed') fireRun(); let k = 0; while (phase === 'run' && (t == null || runT < t) && k++ < 100000) stepRun(0.002); drawAll(); };
    window.__in = () => { const L = lastRun; $('in-t1').value = fmt(L.t1, 1); $('in-tB').value = fmt(L.tB, 1); $('in-dir').value = L.dir; dirChanged(); $('in-tA').value = L.tA == null ? '' : fmt(L.tA, 1); };
    window.__shot = (a, b, bp, c) => { if (phase === 'done') rearm(); setBump(bp); setA(a); setB(b); setComp(c); __go(); __in(); recordRow(); };
    window.__B = id => setTimeout(() => { const w = $(id); w.scrollTop = 1e4; }, 400);
  """,
  'steps': [
   { 'el': ['#aBtns', '#bBtns', '#bumpBtns'], 'prep': "setMode('manual'); resetLab(); rows = []; renderAll(); scrollTo(0,0)",
     'title': 'เลือกกันชนแม่เหล็ก รถ A และ B 200 g',
     'text': 'ในแผงด้านขวา เลือกรถ A <b>200 g</b> รถ B <b>200 g</b> และกันชน <b>🧲 แม่เหล็ก</b> (ผลักกันก่อนแตะ) · ระยะอัดสปริง <b>2.0 cm</b> · การ์ดบังแสง <b>5.0 cm</b>',
     'out': 'ทราบค่า: <b>m<sub>A</sub></b> = <b>m<sub>B</sub></b> = 0.200 kg · <b>d</b> = 0.050 m' },
   { 'el': '#view3d', 'prep': "setView('front')",
     'title': 'จัดตำแหน่งรถ B และโฟโตเกต',
     'text': '<b>ลากรถ B</b> ไปจอดกลางราง · <b>เกต 1</b> ไว้ระหว่างรถ A กับรถ B · <b>เกต 2</b> ไว้หน้ารถ B ใกล้จุดชน (อ่านตำแหน่งจากสเกลบนราง)<br><small>เกตใกล้จุดชน ความเร็วที่วัดได้ใกล้ความเร็วก่อน–หลังชนจริง</small>',
     'out': 'เกต 1 = 34.0 cm · รถ B = 58.0 cm · เกต 2 = 68.0 cm' },
   { 'el': ['#ab-fire', '#view3d'], 'prep': "__go(0); { let k = 0; while (phase === 'run' && runT < RUN.hit.t + 0.2 && k++ < 1e5) stepRun(0.002); } setView('hit')",
     'title': 'ยิงรถ A แล้วดูรถ A หลังชน',
     'text': 'กด <b>▶ ยิงรถ A</b> · กด 🐢 ให้ช้าลง และ <b>🔍 จุดชน</b> ดูว่าหลังชนรถ A <b>วิ่งต่อ · หยุด · หรือกระดอนกลับ</b><br><small>มวลเท่ากัน + แม่เหล็ก: รถ A เกือบหยุดนิ่ง รถ B วิ่งออกไปแทน</small>',
     'out': 'รถ A หลังชน: <b>หยุด/เกือบหยุด</b>' },
   { 'el': ['#view3d', '#in-t1', '#in-tB', '#in-dir'], 'prep': "__go(); setView('tm'); __in()",
     'title': 'อ่านเวลาบังแสงจากจอ',
     'text': 'รอรถหยุด กด <b>🔍 จอจับเวลา</b><br>② <b>t₁</b> = <b>เกต 1 ครั้งที่ 1</b> (รถ A ก่อนชน)<br>③ <b>t<sub>B</sub></b> = <b>เกต 2 ครั้งที่ 1</b> (รถ B หลังชน)<br>④ เลือก <b>หยุด/เกือบหยุด</b> ⑤ t<sub>A</sub> ไม่ต้องกรอก',
     'out': '<b>t₁</b> = 101.1 ms · <b>t<sub>B</sub></b> = 102.6 ms · รถ A หยุด' },
   { 'el': '#lastRec', 'prep': "recordRow(); renderLast(rows.length - 1)",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> (ทิศขวา = +) โปรแกรมคำนวณ:<br>① <b>v₁ = d/t₁</b> · <b>v<sub>B</sub>′ = d/t<sub>B</sub></b> · <b>v<sub>A</sub>′ = ±d/t<sub>A</sub></b> (หยุด = 0 · กระดอนกลับ = ลบ)<br>② <b>p<sub>ก่อน</sub> = m<sub>A</sub>v₁</b> · <b>p<sub>หลัง</sub> = m<sub>A</sub>v<sub>A</sub>′ + m<sub>B</sub>v<sub>B</sub>′</b><br>③ E<sub>k หลัง</sub>/E<sub>k ก่อน</sub><br>④ สัมประสิทธิ์การกระดอน <b>e = (v<sub>B</sub>′ − v<sub>A</sub>′)/v₁</b>',
     'out': 'v₁ = 0.4946 · v<sub>B</sub>′ = 0.4873 · v<sub>A</sub>′ = 0 m/s → <b>p<sub>ก่อน</sub></b> = 0.0989 · <b>p<sub>หลัง</sub></b> = 0.0975 kg·m/s (98.5 %) · <b>E<sub>k</sub></b> เหลือ 97.1 % · <b>e</b> = 0.985' },
   { 'el': '#lastRec', 'prep': "__shot(2, 0, 0, 2); renderLast(rows.length - 1)",
     'title': 'm_A > m_B: รถ A วิ่งตาม',
     'text': 'กด <b>↩ ตั้งรถใหม่</b> เลือกรถ A <b>400 g</b> รถ B <b>200 g</b> ยิง · หลังชนรถ A <b>วิ่งต่อไปทางขวา</b> ช้ากว่ารถ B · เลือกข้อ ④ <b>วิ่งต่อ</b> แล้วอ่าน <b>t<sub>A</sub> = เกต 2 ครั้งที่ 2</b>',
     'out': 't₁ = 145.8 · t<sub>B</sub> = 110.7 · t<sub>A</sub> = 433.3 ms → v₁ = 0.343 · v<sub>B</sub>′ = 0.452 · v<sub>A</sub>′ = +0.115 m/s → p<sub>หลัง</sub>/p<sub>ก่อน</sub> = 99.5 % · E<sub>k</sub> เหลือ 98.1 % · <b>e</b> = 0.981' },
   { 'el': '#lastRec', 'prep': "__shot(0, 2, 0, 2); renderLast(rows.length - 1)",
     'title': 'm_A < m_B: รถ A กระดอนกลับ',
     'text': 'เลือกรถ A <b>200 g</b> รถ B <b>400 g</b> ยิง · หลังชนรถ A <b>กระดอนกลับ</b>ทางซ้าย · เลือกข้อ ④ <b>กระดอนกลับ</b> แล้วอ่าน <b>t<sub>A</sub> = เกต 1 ครั้งที่ 2</b> · v<sub>A</sub>′ เป็น<b>ลบ</b>',
     'out': 't₁ = 103.2 · t<sub>B</sub> = 156.3 · t<sub>A</sub> = 323.9 ms → v₁ = 0.485 · v<sub>B</sub>′ = 0.320 · v<sub>A</sub>′ = <b>−0.154</b> m/s → p<sub>หลัง</sub>/p<sub>ก่อน</sub> = 100.2 % · E<sub>k</sub> เหลือ 97.3 % · <b>e</b> = 0.979' },
   { 'el': '#tableB', 'prep': "__shot(1, 0, 0, 1); __shot(0, 1, 0, 0); __shot(0, 0, 1, 2); __shot(2, 0, 1, 1); __shot(0, 2, 1, 2); __shot(0, 0, 2, 2); __shot(2, 0, 2, 1); __shot(1, 1, 2, 0); __B('tableB')",
     'title': 'เปลี่ยนกันชน: สปริงแผ่น และยาง Y',
     'text': 'เปลี่ยนกันชนเป็น <b>🌀 สปริงแผ่น</b> และ <b>❓ ยาง Y</b> บันทึกกันชนละอย่างน้อย <b>3 แถว</b> โดยเปลี่ยนมวลและระยะอัดสปริง (v₁ ต่างกัน) · ดูตาราง ② : E<sub>k หลัง</sub>/E<sub>k ก่อน</sub> และ e ของแต่ละกันชน',
     'out': 'p<sub>หลัง</sub>/p<sub>ก่อน</sub> = 97.8 – 100.2 % ทุกแถว · E<sub>k</sub> เหลือ: 🧲 96 – 98 % · 🌀 77 – 88 % · ❓ ยาง Y 66 – 77 % → <b>e</b> ≈ 0.97 – 0.99 · 0.81 – 0.82 · 0.58 – 0.60' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('pp')",
     'title': 'กราฟ p หลัง – p ก่อน',
     'text': 'จุดของ<b>ทุกกันชน</b>อยู่บนเส้นประ p<sub>หลัง</sub> = p<sub>ก่อน</sub> · ความชันใกล้ 1<br>⑤ <b>โมเมนตัมอนุรักษ์ทุกการชน</b> แม้พลังงานจลน์จะหายไปไม่เท่ากัน',
     'out': '<b>ความชัน</b> ≈ 0.994 → p<sub>หลัง</sub> = p<sub>ก่อน</sub> ทุกกันชน' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('e')",
     'title': 'กราฟ v_B′ − v_A′ กับ v₁ → e',
     'text': 'ความเร็วแยกจากกัน (v<sub>B</sub>′ − v<sub>A</sub>′) แปรผันตรงกับความเร็วเข้าหากัน v₁ · จุดของกันชนเดียวกันเรียงเป็นเส้นตรงผ่านจุดกำเนิด<br>⑥ <b>ความชัน = e</b> · e = 1 ยืดหยุ่นสมบูรณ์ · e &lt; 1 ไม่ยืดหยุ่น',
     'out': '<b>e</b> ≈ 0.980 (🧲 แม่เหล็ก · เกือบยืดหยุ่นสมบูรณ์) · 0.816 (🌀 สปริงแผ่น) · 0.583 (❓ ยาง Y)' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('vb')",
     'title': 'กราฟ v_B′/v₁ กับ m_A/(m_A+m_B)',
     'text': 'จากการอนุรักษ์โมเมนตัมและนิยาม e → <b>v<sub>B</sub>′/v₁ = (1 + e)·m<sub>A</sub>/(m<sub>A</sub>+m<sub>B</sub>)</b> · จุดของกันชนเดียวกันเป็นเส้นตรงผ่านจุดกำเนิด<br>⑦ <b>ความชัน = 1 + e</b> ใช้ตรวจค่า e อีกวิธี',
     'out': 'ความชัน = 1.971 · 1.811 · 1.576 → <b>e</b> ≈ 0.971 · 0.811 · 0.576 (สอดคล้องกับกราฟก่อน)' },
   { 'el': ['.ans-row:has(#ans-e)', '#ansEMsg'], 'prep': "{ const Y = goodRows().filter(q => q.bump === 2); $('ans-e').value = (Y.reduce((a, q) => a + q.e, 0) / Y.length).toFixed(2); } checkE()",
     'title': 'ตอบค่า e ของยาง Y',
     'text': '⑧ นำ e ของแถวยาง Y มาเฉลี่ย (หรือใช้ความชันกราฟ v<sub>B</sub>′ − v<sub>A</sub>′ กับ v₁) กรอกช่อง <b>e</b> แล้วกด <b>ตรวจค่า e</b> (ยอมคลาด ±0.04)',
     'out': '<b>e</b><sub>ยาง Y</sub> = (0.581 + 0.581 + 0.597)/3 ≈ 0.59 ในภาพตัวอย่าง (สุ่มทุกครั้งที่เปิดหน้า ในช่วง 0.45 – 0.70)' },
   { 'el': '#tableA', 'prep': "__shot(0, 3, 0, 2); __shot(1, 3, 0, 2); __B('tableA')",
     'title': 'รถปริศนา X',
     'text': 'กลับเป็น <b>🧲 แม่เหล็ก</b> เลือกรถ B เป็น <b>❓ X</b> ยิงและบันทึกอย่างน้อย 2 แถว (รถ A ต่างมวล) · ดูทิศของรถ A หลังชนทุกครั้ง<br>⑨ จากการอนุรักษ์โมเมนตัม m<sub>A</sub>v₁ = m<sub>A</sub>v<sub>A</sub>′ + m<sub>X</sub>v<sub>B</sub>′ → <b>m<sub>X</sub> = m<sub>A</sub>(v₁ − v<sub>A</sub>′)/v<sub>B</sub>′</b> (ไม่ต้องรู้ e)',
     'out': 'รถ A 200 g: กระดอนกลับ v<sub>A</sub>′ = −0.145 m/s → m<sub>X</sub> = 380 g · รถ A 300 g: กระดอนกลับ v<sub>A</sub>′ = −0.038 m/s → m<sub>X</sub> = 378 g' },
   { 'el': ['.ans-row:has(#ans-m)', '#ansMMsg'], 'prep': "{ const X = goodRows().filter(q => q.X); $('ans-m').value = (X.reduce((a, q) => a + q.mEst, 0) / X.length).toFixed(0); } checkM()",
     'title': 'ตอบมวลรถ X แล้วตรวจ',
     'text': '⑩ เฉลี่ย m<sub>X</sub> ของแถวรถ X (ใต้ตาราง ①) กรอกช่อง <b>มวลรถปริศนา X</b> แล้วกด <b>ตรวจมวล X</b> (ยอมคลาด 5%)',
     'out': '<b>m<sub>X</sub></b> ≈ 379 g ในภาพตัวอย่าง (สุ่มทุกครั้งที่เปิดหน้า ในช่วง 250 – 550 g)' },
  ],
 }
