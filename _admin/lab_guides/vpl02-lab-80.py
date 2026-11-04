# -*- coding: utf-8 -*-
# Lab 80 การชนแบบติดกัน (โมเมนตัม) — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ข้อมูลทุกแถว = แบบจำลองของแลปเอง (buildRun: รถ 2 คันบนรางลม + โฟโตเกต 2 ตัว · เวลา ±0.2 ms)
# มวลรถ X · ความหน่วงราง · e ของแม่เหล็ก สุ่มทุกครั้งที่เปิดหน้า → ตรึงค่าตัวอย่างเฉพาะ browser ที่ถ่ายภาพ
GUIDE = {
  'title': 'ตรวจกฎการอนุรักษ์โมเมนตัมในการชนแบบติดกัน แล้วหามวลรถ X',
  'setup': r"""
    /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองเอง (stepRun) · สุ่มแบบมีเมล็ด */
    setSimSpeed(0); { const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    { let s = 80; Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
    BUMPS[1].e = 0.97;
    window.__MX = 0.320; window.__DEC = 0.0006;
    window.__mb = () => isX() ? __MX : MB_OPT[bI] / 1000;
    const __fx = f => (0, eval)('(' + f.toString().replace(/mBkg\(\)/g, '__mb()').replace(/\bM_X\b/g, '__MX').replace(/\bDECEL\b/g, '__DEC') + ')');
    buildRun = __fx(buildRun); checkM = __fx(checkM); updateHint = __fx(updateHint); renderTable = __fx(renderTable);
    window.__go = t => { if (phase === 'done') rearm(); if (phase === 'armed') fireRun(); let k = 0; while (phase === 'run' && (t == null || runT < t) && k++ < 100000) stepRun(0.002); drawAll(); };
    window.__in = () => { const L = lastRun; $('in-t1').value = fmt(L.t1, 1); $('in-t2').value = fmt(L.t2, 1);
      if (L.bump === 1) { $('in-dir').value = L.dir; dirChanged(); $('in-tA').value = L.tA == null ? '' : fmt(L.tA, 1); } };
    window.__shot = (a, b, bp, c) => { if (phase === 'done') rearm(); setBump(bp); setA(a); setB(b); setComp(c); __go(); __in(); recordRow(); };
    window.__B = id => setTimeout(() => { const w = $(id); w.scrollTop = 1e4; }, 400);
  """,
  'steps': [
   { 'el': ['#aBtns', '#bBtns', '#bumpBtns'], 'prep': "setMode('manual'); resetLab(); rows = []; renderAll(); scrollTo(0,0)",
     'title': 'เลือกมวลรถ และกันชนตีนตุ๊กแก',
     'text': 'ในแผงด้านขวา เลือกรถ A <b>200 g</b> รถ B <b>200 g</b> และปลายที่ชน <b>🔗 ตีนตุ๊กแก</b> (ชนแล้วติดกันไป) · ระยะอัดสปริง <b>2.0 cm</b> · การ์ดบังแสง <b>5.0 cm</b><br><small>รถเปล่า 200 g · เพิ่มก้อนเหล็กก้อนละ 100 g</small>',
     'out': 'ทราบค่า: <b>m<sub>A</sub></b> = 0.200 kg · <b>m<sub>B</sub></b> = 0.200 kg · <b>d</b> = 0.050 m' },
   { 'el': '#view3d', 'prep': "setView('front')",
     'title': 'จัดตำแหน่งรถ B และโฟโตเกต',
     'text': '<b>ลากรถ B</b> ไปจอดกลางราง · ลาก <b>เกต 1</b> ไว้ระหว่างรถ A กับรถ B และ <b>เกต 2</b> ไว้หน้ารถ B ใกล้ ๆ อ่านตำแหน่งจากสเกลบนราง<br><small>วางเกตใกล้จุดชน แรงต้านเล็กน้อยของรางจะมีผลน้อย</small>',
     'out': 'เกต 1 = 34.0 cm · รถ B = 58.0 cm · เกต 2 = 72.0 cm' },
   { 'el': ['#ab-fire', '#view3d'], 'prep': "__go(0); { let k = 0; while (phase === 'run' && runT < RUN.hit.t + 0.25 && k++ < 1e5) stepRun(0.002); } setView('hit')",
     'title': 'ยิงรถ A',
     'text': 'กด <b>▶ ยิงรถ A</b> รถ A ผ่านเกต 1 ชนรถ B ที่จอดนิ่ง แผ่นตีนตุ๊กแกยึดให้<b>ติดกัน</b> แล้วรถทั้งสองวิ่งไปด้วยกันผ่านเกต 2<br><small>กด 🐢 ให้ภาพช้าลงได้ เวลาที่วัดไม่เปลี่ยน</small>' },
   { 'el': ['#view3d', '#in-t1', '#in-t2'], 'prep': "__go(); setView('tm'); $('in-t1').value = fmt(lastRun.t1, 1); $('in-t2').value = fmt(lastRun.t2, 1)",
     'title': 'อ่านเวลาบังแสง t₁ และ t₂',
     'text': 'รอรถหยุด กด <b>🔍 จอจับเวลา</b><br>④ <b>t₁</b> = <b>เกต 1 ครั้งที่ 1</b> (การ์ดรถ A ก่อนชน)<br>⑤ <b>t₂</b> = <b>เกต 2 ครั้งที่ 1</b> (การ์ดรถ B ที่ติดกับรถ A แล้ว)<br><small>เกต 2 ครั้งที่ 2 = การ์ดรถ A ที่ติดตามมา ควรได้เวลาใกล้ครั้งที่ 1 (ยืนยันว่าติดกันจริง)</small>',
     'out': '<b>t₁</b> = 101.4 ms · <b>t₂</b> = 202.7 ms (เกต 2 ครั้งที่ 2 = 203.3 ms ใกล้กัน → ติดกันจริง)' },
   { 'el': '#lastRec', 'prep': "recordRow(); renderLast(rows.length - 1)",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> (ทิศขวา = +) โปรแกรมคำนวณ:<br>① <b>v₁ = d/t₁</b> · <b>v₂ = d/t₂</b><br>② <b>p<sub>ก่อน</sub> = m<sub>A</sub>v₁</b> · <b>p<sub>หลัง</sub> = (m<sub>A</sub> + m<sub>B</sub>)v₂</b><br>③ เทียบ p<sub>หลัง</sub>/p<sub>ก่อน</sub><br>④ <b>E<sub>k</sub> = ½mv²</b> ก่อนและหลังชน เทียบกับ m<sub>A</sub>/(m<sub>A</sub>+m<sub>B</sub>)',
     'out': 'v₁ = 0.4931 · v₂ = 0.2467 m/s → <b>p<sub>ก่อน</sub></b> = 0.200 × 0.4931 = 0.0986 · <b>p<sub>หลัง</sub></b> = 0.400 × 0.2467 = 0.0987 kg·m/s (100.0 %)<br>E<sub>k</sub> ก่อน 24.31 mJ → หลัง 12.17 mJ = <b>50.0 %</b> (= 200/400)' },
   { 'el': '#tableA', 'prep': "__shot(0, 1, 0, 2); __shot(0, 2, 0, 2); __shot(1, 0, 0, 2); __shot(2, 1, 0, 1); __B('tableA')",
     'title': 'เปลี่ยนมวล แล้วทำซ้ำ',
     'text': 'กด <b>↩ ตั้งรถใหม่</b> เปลี่ยนมวลรถ B เป็น 300 g, 400 g และเปลี่ยนมวลรถ A (หรือระยะอัดสปริง) ยิงและบันทึกแบบเดิม · ให้ได้อย่างน้อย <b>3 แถว</b> ที่ m<sub>B</sub>/m<sub>A</sub> ต่างกัน',
     'out': 'm<sub>A</sub>/m<sub>B</sub> = 200/300 · 200/400 · 300/200 · 400/300 g → <b>p<sub>หลัง</sub>/p<sub>ก่อน</sub></b> = 99.9 · 99.8 · 99.7 · 99.6 %' },
   { 'el': '#tableB', 'prep': "renderAll()",
     'title': 'ตาราง ② พลังงานจลน์',
     'text': '<b>E<sub>k ก่อน</sub> = ½m<sub>A</sub>v₁²</b> · <b>E<sub>k หลัง</sub> = ½(m<sub>A</sub>+m<sub>B</sub>)v₂²</b> · พลังงานจลน์หลังชน<b>น้อยกว่า</b>ก่อนชนทุกแถว และสัดส่วนที่เหลือใกล้ <b>m<sub>A</sub>/(m<sub>A</sub>+m<sub>B</sub>)</b><br><small>พลังงานที่หายไปกลายเป็นความร้อน เสียง และงานที่ทำให้แผ่นตีนตุ๊กแกเสียรูป</small>',
     'out': '<b>E<sub>k หลัง</sub>/E<sub>k ก่อน</sub></b> = 50.0 · 39.9 · 33.2 · 59.7 · 56.6 % เทียบ m<sub>A</sub>/(m<sub>A</sub>+m<sub>B</sub>) = 50.0 · 40.0 · 33.3 · 60.0 · 57.1 %' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('pp')",
     'title': 'กราฟ p หลัง – p ก่อน',
     'text': 'จุดทุกจุดอยู่บน<b>เส้นประ p<sub>หลัง</sub> = p<sub>ก่อน</sub></b> · ความชันของข้อมูลใกล้ 1<br>⑤ แสดงว่า <b>โมเมนตัมรวมของระบบก่อนชน = หลังชน</b> (อนุรักษ์โมเมนตัม)',
     'out': '<b>ความชัน</b> ≈ 0.998 → <b>p<sub>หลัง</sub> = p<sub>ก่อน</sub></b>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('ek')",
     'title': 'กราฟ E_k หลัง/ก่อน – มวล',
     'text': 'จุดของการชนแบบติดกันอยู่บน<b>เส้นประ E<sub>k หลัง</sub>/E<sub>k ก่อน</sub> = m<sub>A</sub>/(m<sub>A</sub>+m<sub>B</sub>)</b> (ได้จาก m<sub>A</sub>v₁ = (m<sub>A</sub>+m<sub>B</sub>)v₂ แทนในสูตรพลังงานจลน์) · รถ B หนักขึ้น พลังงานจลน์เหลือน้อยลง',
     'out': 'E<sub>k หลัง</sub>/E<sub>k ก่อน</sub> ÷ ทฤษฎี ≈ <b>0.996</b> → ชนแบบติดกัน พลังงานจลน์หายไปตามทฤษฎี' },
   { 'el': ['.ans-row:has(#ans-k)', '#ansKMsg'], 'prep': "$('ans-k').value = '33.3'; checkK()",
     'title': 'ทำนายพลังงานจลน์ที่เหลือ',
     'text': '⑥ รถ A 200 g ชนรถ B 400 g ที่จอดนิ่งแล้วติดกัน: <b>E<sub>k หลัง</sub>/E<sub>k ก่อน</sub> = m<sub>A</sub>/(m<sub>A</sub>+m<sub>B</sub>)</b> = 200/600 กรอกเป็น % แล้วกด <b>ตรวจคำทำนาย</b>',
     'out': '<b>E<sub>k หลัง</sub>/E<sub>k ก่อน</sub></b> = 33.3 % (หายไป 2 ใน 3)' },
   { 'el': ['#lastRec'], 'prep': "__shot(0, 2, 1, 2); __shot(2, 0, 1, 2); renderLast(rows.length - 2)",
     'title': 'เปลี่ยนเป็นกันชนแม่เหล็ก',
     'text': 'เลือก <b>🧲 แม่เหล็ก</b> (ผลักกันก่อนแตะ ชนแล้วแยกกัน) ยิงแล้ว<b>ดูในภาพ 3D</b> ว่ารถ A หลังชนวิ่งต่อ หยุด หรือกระดอนกลับ · เลือกข้อ ⑥ แล้วอ่าน <b>t<sub>A</sub></b> จากช่องที่ตรงกัน (กระดอนกลับ = เกต 1 ครั้งที่ 2 · วิ่งต่อ = เกต 2 ครั้งที่ 2)<br>⑦ <b>p<sub>หลัง</sub> = m<sub>A</sub>v<sub>A</sub>′ + m<sub>B</sub>v₂</b> (v<sub>A</sub>′ เป็นลบเมื่อกระดอนกลับ) · <b>e = (v₂ − v<sub>A</sub>′)/v₁</b>',
     'out': 'A 200 g → B 400 g: รถ A <b>กระดอนกลับ</b> t<sub>A</sub> = 324.5 ms → v<sub>A</sub>′ = −0.154 m/s · v₂ = 0.325 m/s → p<sub>หลัง</sub>/p<sub>ก่อน</sub> = 100.0 % · <b>E<sub>k</sub> เหลือ 95.7 %</b> · <b>e</b> = 0.967<br>A 400 g → B 200 g: รถ A วิ่งต่อ · E<sub>k</sub> เหลือ 97.0 % · e = 0.964 → โมเมนตัมอนุรักษ์ทั้งสองแบบ แต่พลังงานจลน์เกือบไม่หาย' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "__shot(0, 3, 0, 2); __shot(1, 3, 0, 2); setGraph('mx')",
     'title': 'รถปริศนา X: กราฟ v₁/v₂ – m_B/m_A',
     'text': 'กลับเป็น <b>🔗 ตีนตุ๊กแก</b> เลือกรถ B เป็น <b>❓ X</b> ยิงและบันทึกอย่างน้อย 2 แถว · กราฟใช้เฉพาะการชนแบบติดกัน: จาก m<sub>A</sub>v₁ = (m<sub>A</sub>+m<sub>B</sub>)v₂ → <b>v₁/v₂ = 1 + m<sub>B</sub>/m<sub>A</sub></b> (เส้นตรง ความชัน 1 ตัดแกนตั้งที่ 1)<br>⑧ ลากเส้นประม่วงของรถ X ไปตัดเส้นเหลือง อ่าน m<sub>X</sub>/m<sub>A</sub>',
     'out': 'v₁/v₂ = 2.607 (m<sub>A</sub> 200 g) · 2.075 (m<sub>A</sub> 300 g) → m<sub>X</sub>/m<sub>A</sub> = 1.603 · 1.071 → <b>m<sub>X</sub></b> ≈ 321 g · เส้นเหลืองของข้อมูล ความชัน 1.001 ตัดแกนตั้ง 1.003' },
   { 'el': ['.ans-row', '#ansMMsg'], 'prep': "{ const X = goodRows().filter(q => q.X); $('ans-m').value = (X.reduce((a, q) => a + q.mEst, 0) / X.length).toFixed(0); } checkM()",
     'title': 'ตอบมวลรถ X แล้วตรวจ',
     'text': '⑨ <b>m<sub>X</sub> = m<sub>A</sub>(v₁/v₂ − 1)</b> ของแต่ละแถว (ตาราง ① คอลัมน์ m<sub>X</sub>) นำมาเฉลี่ย กรอกช่อง <b>มวลรถปริศนา X</b> แล้วกด <b>ตรวจมวล X</b> (ยอมคลาด 5%)',
     'out': 'm<sub>X</sub> = 321 · 323 g → <b>m<sub>X</sub></b> ≈ 322 g ในภาพตัวอย่าง (สุ่มทุกครั้งที่เปิดหน้า ในช่วง 250 – 550 g)' },
  ],
 }
