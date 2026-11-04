# -*- coding: utf-8 -*-
# Lab 83 การชน 2 มิติ ภาพแฟลชบนโต๊ะลม — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ภาพแฟลช = แบบจำลองของแลปเอง (buildRun) · ค่าที่กรอก = ความยาว/มุมจริงของภาพแฟลช ปัดแบบอ่านไม้บรรทัด (0.1 cm) และโปรแทรกเตอร์ (1°)
# ค่าสุ่มตอนโหลด (มวลลูกยาง X · สัมประสิทธิ์การกระดอน) ตรึงไว้เฉพาะ browser ที่ถ่ายภาพ ให้ภาพตรงกับข้อความ
GUIDE = {
  'title': 'ตรวจกฎอนุรักษ์โมเมนตัมแกน x และแกน y ในการชน 2 มิติ แล้วหามวลลูกยาง X',
  'setup': r"""
    simSpeed = 0;   /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองเอง (stepRun) */
    window.__MX = 220;
    buildRun = (0, eval)('(' + buildRun.toString().replace(/mBg\(\)/g, '(isX()?__MX:MB_OPT[bI])').replace(/\bE_REST\b/g, '0.95') + ')');
    checkM = (0, eval)('(' + checkM.toString().replace(/\bM_XP\b/g, '__MX') + ')');
    window.__k = 0;
    window.__seed = n => { let s = n; Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
    window.__fire = () => { __seed(8300 + (++__k) * 37); rearm(); fireRun(); let i = 0; while (phase === 'run' && i++ < 100000) stepRun(0.01); };
    window.__read = () => { const L = lastRun; $('in-aL').value = L.sA.L.toFixed(1); $('in-a2L').value = L.sA2.L.toFixed(1); $('in-a2T').value = Math.round(L.sA2.T); $('in-b2L').value = L.sB2.L.toFixed(1); $('in-b2T').value = Math.round(L.sB2.T); };
    window.__meas = (b, y) => { setB(b); xB = 38; yB = y; clampB(); __fire(); __read(); recordRow(); };
    /* วางไม้บรรทัด: ขีดศูนย์ที่จุดที่ 1 หมุนให้ขอบผ่านจุดที่ 5 */
    window.__rul = P5 => { rul = { x: P5[0].x, y: P5[0].y, ang: Math.atan2(P5[4].y - P5[0].y, P5[4].x - P5[0].x) }; drawAll(); };
    window.__look = (x, y, w) => { setView('top'); curView = 'free'; orbit.target.set(x, TBL, 25 - y); orbit.dist = fitDist(w, w * 0.62); };
    window.__B = () => setTimeout(() => { document.querySelectorAll('.tbl-wrap').forEach(w => w.scrollTop = 1e4); }, 400);
  """,
  'steps': [
   { 'el': ['#bBtns', '#spdBtns'], 'prep': "setMode('manual'); resetLab(); rows = []; renderAll(); setB(0); setSpd(1); scrollTo(0,0)",
     'title': 'เลือกลูกยาง B 150 g และแรงยิงกลาง',
     'text': 'เลือกลูกยาง <b>B 150 g</b> (มวลเท่ากับลูกยาง A) และแรงยิง <b>กลาง</b> · ลูกยาง A (น้ำเงิน 150 g) ถูกยิงด้วยเครื่องยิงสปริงตามแนว <b>y = 25.0 cm</b> ไปทาง +x',
     'out': '<b>m<sub>A</sub></b> = 150 g · <b>m<sub>B</sub></b> = 150 g' },
   { 'el': ['#view3d', '#roOff'], 'prep': "xB = 38; yB = 27.0; clampB(); syncCtl(); setView('hit')",
     'title': 'ลากลูกยาง B ให้เยื้องแนวยิง',
     'text': 'ลาก<b>ลูกยาง B</b> ในภาพให้อยู่<b>เหนือแนวยิงเล็กน้อย</b> (เยื้อง 1–3 cm) อ่านค่าที่กรอบ <b>ระยะเยื้อง b</b><br><small>ชนไม่ตรงศูนย์กลาง ลูกยางจึงแยกออกเป็นมุม · เยื้องเกิน 5 cm (เส้นผ่านศูนย์กลางลูก) จะไม่ชน</small>',
     'out': 'ลูกยาง B ที่ (38.0, 27.0) cm · <b>b</b> = 2.0 cm' },
   { 'el': ['#ab-fire', '#view3d'], 'prep': "__seed(8300); rearm(); fireRun(); for (let i = 0; i < 70; i++) stepRun(0.01); setView('iso')",
     'title': 'ยิง + ถ่ายภาพแฟลช',
     'text': 'กด <b>▶ ยิง + ถ่ายแฟลช</b> ลูกยาง A พุ่งไปชน B แล้วแยกกันเป็นมุม · ไฟแฟลชทุก <b>Δt = 0.040 s</b> ภาพลูกยางทุกครั้งพิมพ์ลงบนพื้นโต๊ะพร้อมหมายเลขจุด' },
   { 'el': '#view3d', 'prep': "__k = 0; __fire(); setView('top')",
     'title': 'ดูภาพแฟลชจากด้านบน',
     'text': 'รอลูกยางหยุด แล้วกด <b>📸 ดูภาพ</b> · จุด <b>A1, A2 …</b> = ลูกยาง A ก่อนชน · <b>A′1, A′2 …</b> = A หลังชน · <b>B′1, B′2 …</b> = B หลังชน · วัดจาก<b>กากบาทกลางลูก</b><br><small>ใช้จุดที่ห่างกัน 4 ช่วงแฟลชเสมอ (จุดที่ 1 → จุดที่ 5) = เวลา 4Δt = 0.160 s</small>' },
   { 'el': '#view3d', 'prep': "__rul(RUN.A1); setView('tool')",
     'title': 'วัดความยาว A1 → A5 ด้วยไม้บรรทัด',
     'text': 'ลาก<b>ไม้บรรทัด</b>ให้ขีดศูนย์อยู่ที่กากบาทของ <b>A1</b> ลาก<b>จุดแดง</b>ที่ปลายหมุนให้ขอบผ่าน <b>A5</b> แล้วอ่านความยาวที่ A5 (ขีดละ 1 mm) · กรอกช่อง <b>②</b>',
     'out': '<b>|d<sub>A</sub>|</b> = 7.9 cm (ทิศ θ = 0° ตามแนวยิง)' },
   { 'el': '#view3d', 'prep': "__rul(RUN.A2); setView('tool')",
     'title': 'วัดความยาว A′1 → A′5',
     'text': 'ย้ายไม้บรรทัดไปที่ <b>A′1</b> หมุนให้ขอบผ่าน <b>A′5</b> อ่านความยาว · กรอกช่อง <b>③</b>',
     'out': '<b>|d<sub>A′</sub>|</b> = 3.1 cm' },
   { 'el': '#view3d', 'prep': "stowTools(); pro = { x: RUN.A2[0].x, y: RUN.A2[0].y }; drawAll(); __look(pro.x + 3, pro.y, 30)",
     'title': 'วัดมุมของ A หลังชนด้วยโปรแทรกเตอร์',
     'text': 'ลาก<b>โปรแทรกเตอร์</b>ให้จุดกลางอยู่ที่ <b>A′1</b> (เส้นฐาน 0° ขนานทิศยิง) อ่านมุมที่แนว A′1 → A′5 ตัดขอบโปรแทรกเตอร์ · <b>ใต้แนว 0° ใส่ลบ</b> เหนือแนวใส่บวก · กรอกช่อง <b>④</b>',
     'out': '<b>θ<sub>A′</sub></b> = −63° (ใต้แนวยิง)' },
   { 'el': '#view3d', 'prep': "__rul(RUN.B2); pro = { x: RUN.B2[0].x, y: RUN.B2[0].y }; drawAll(); __look(RUN.B2[2].x, RUN.B2[2].y, 34)",
     'title': 'วัดความยาวและมุมของ B หลังชน',
     'text': 'ทำแบบเดียวกันกับลูกยาง B: ไม้บรรทัดจาก <b>B′1 → B′5</b> (ช่อง <b>⑤</b>) และโปรแทรกเตอร์ที่ <b>B′1</b> (ช่อง <b>⑥</b> · เหนือแนวใส่บวก) · วัดเสร็จกด <b>📥 เก็บเครื่องมือ</b>',
     'out': '<b>|d<sub>B′</sub>|</b> = 7.0 cm · <b>θ<sub>B′</sub></b> = +24° (เหนือแนวยิง)' },
   { 'el': '#recForm', 'prep': "stowTools(); __read(); setView('top')",
     'title': 'กรอกค่าลงใบบันทึก',
     'text': 'ตรวจว่ากรอกครบ 5 ช่อง: ความยาว (cm) ของ A ก่อนชน · A หลังชน · B หลังชน และมุม (องศา) ของ A และ B หลังชน · ช่อง ① แสดงมวลและช่วงแฟลชให้แล้ว',
     'out': '② 7.9 cm · ③ 3.1 cm · ④ −63° · ⑤ 7.0 cm · ⑥ +24°' },
   { 'el': '#lastRec', 'prep': "recordRow()",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> โปรแกรมคำนวณต่อเป็นลำดับ:<br>① ความเร็ว <b>|v| = |d| / (4Δt)</b> = |d| / 0.160 s<br>② แตกเวกเตอร์ <b>v<sub>x</sub> = |v| cos θ</b> · <b>v<sub>y</sub> = |v| sin θ</b><br>③ ก่อนชน <b>p<sub>x</sub> = m<sub>A</sub>v<sub>A</sub></b> · p<sub>y</sub> = 0<br>④ หลังชน <b>Σp<sub>x</sub> = m<sub>A</sub>v<sub>A′x</sub> + m<sub>B</sub>v<sub>B′x</sub></b> · <b>Σp<sub>y</sub> = m<sub>A</sub>v<sub>A′y</sub> + m<sub>B</sub>v<sub>B′y</sub></b><br>⑤ มุมระหว่างแนว A′ กับ B′ และ Ek หลัง/ก่อน',
     'out': '<b>v<sub>A</sub></b> = 0.494 m/s · <b>v<sub>A′</sub></b> = (+0.088, −0.173) m/s · <b>v<sub>B′</sub></b> = (+0.400, +0.178) m/s<br><b>p<sub>x</sub> ก่อน</b> = 0.0741 kg·m/s · <b>Σp<sub>x</sub> หลัง</b> = 0.0731 (98.8 %) · <b>Σp<sub>y</sub> หลัง</b> = +0.0008 (1.1 %) ≈ 0 · มุมแยก 87.0° · Ek หลัง/ก่อน 93.9 %' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('vec')",
     'title': 'รวมเวกเตอร์โมเมนตัม',
     'text': 'กราฟ <b>เวกเตอร์ p (แถวล่าสุด)</b> นำ <b>p<sub>A′</sub></b> (ฟ้า) ต่อหัว-ท้ายด้วย <b>p<sub>B′</sub></b> (ส้ม) ผลรวม (เขียว) <b>ทับเวกเตอร์ p<sub>A</sub> ก่อนชน</b> (เทา) → โมเมนตัมอนุรักษ์ทั้งขนาดและทิศ<br><small>p<sub>A′</sub> กับ p<sub>B′</sub> เกือบตั้งฉากกัน เพราะมวลเท่ากัน</small>',
     'out': 'Σp หลัง = 0.0731 kg·m/s เทียบ p ก่อน 0.0741 kg·m/s · มุมแยก 87.0°' },
   { 'el': '#tableB', 'prep': "__meas(0, 26.0); __meas(0, 28.5); __meas(1, 27.0); __meas(1, 28.5); setB(0); renderAll(); __B()",
     'title': 'เปลี่ยนระยะเยื้องและมวล แล้ววัดซ้ำ',
     'text': 'กด <b>↩ วางใหม่</b> ลากลูกยาง B ให้เยื้องต่างจากเดิม ยิงและวัดอีกอย่างน้อย 2 แถว (รวม 3 แถว) · แล้วเปลี่ยนเป็นลูกยาง <b>🟤 300 g</b> วัดอีก 2 แถว · ตาราง ② แสดง <b>Σp<sub>x</sub>/p</b> และ <b>Σp<sub>y</sub>/p</b> (สีเหลือง) และมุมแยก',
     'out': 'B 150 g (b = 2.0 · 1.0 · 3.5 cm): Σp<sub>x</sub>/p = 98.8 · 99.5 · 100.4 % · Σp<sub>y</sub>/p = +1.1 · +0.3 · −0.9 % · มุมแยก 87 · 83 · 88° (เฉลี่ย 86.0°)<br>B 300 g (b = 2.0 · 3.5 cm): Σp<sub>x</sub>/p = 98.5 · 99.6 % · Σp<sub>y</sub>/p = +0.2 · +0.7 % · มุมแยก 125 · 107° (เฉลี่ย 116.0°)' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('pp')",
     'title': 'กราฟ Σp หลังชน กับ p ก่อนชน',
     'text': 'กด <b>Σp หลัง – p ก่อน</b> · ● Σp<sub>x</sub> หลังชน อยู่บน<b>เส้นประทแยง</b> (เท่ากับ p<sub>x</sub> ก่อนชน) · ▲ Σp<sub>y</sub> หลังชน อยู่บน<b>เส้นประศูนย์</b> ทั้งลูกยาง 150 g (ฟ้า) และ 300 g (ส้ม)',
     'out': 'เฉลี่ย <b>Σp<sub>x</sub>/p</b> = 99.3 % · <b>Σp<sub>y</sub>/p</b> = +0.3 % → โมเมนตัมอนุรักษ์ทั้งแกน x และแกน y' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('ang')",
     'title': 'กราฟมุมแยกกับอัตราส่วนมวล',
     'text': 'กด <b>มุมแยก · Ek</b> · มวลเท่ากัน มุมแยกใกล้ <b>90°</b> (น้อยกว่าเล็กน้อย เพราะสูญเสียพลังงานบ้าง) · B หนักกว่า A มุมแยก<b>มากกว่า 90°</b>',
     'out': 'มุมแยกเฉลี่ย <b>86.0°</b> (B 150 g) · <b>116.0°</b> (B 300 g) · Ek หลัง/ก่อน ≈ 95 % (ชนแบบไม่ยืดหยุ่นเล็กน้อย)' },
   { 'el': ['.ans-row:has(#ans-k)', '#ansKMsg'], 'prep': "$('ans-k').value = 90; checkK()",
     'title': 'ทำนายมุมแยกของมวลเท่ากัน',
     'text': 'ชนแบบยืดหยุ่นสมบูรณ์ มวลเท่ากัน: <b>p<sub>A</sub> = p<sub>A′</sub> + p<sub>B′</sub></b> (เวกเตอร์) และ <b>p<sub>A</sub>² = p<sub>A′</sub>² + p<sub>B′</sub>²</b> (จากพลังงานจลน์) → สามเหลี่ยมเวกเตอร์เป็นมุมฉาก (ทฤษฎีบทพีทาโกรัส) · กรอกแล้วกด <b>ตรวจคำทำนาย</b>',
     'out': '<b>มุมแยก</b> = 90°' },
   { 'el': '#tableB', 'prep': "__meas(2, 27.0); __meas(2, 28.5); renderAll(); __B()",
     'title': 'เปลี่ยนเป็นลูกยางปริศนา X',
     'text': 'เลือก <b>❓ X</b> ยิง วัด แล้วบันทึกแบบเดิมอย่างน้อย 2 แถว · แถวสีม่วงคำนวณมวล X จากกฎอนุรักษ์โมเมนตัม<br>⑥ แกน y: <b>m<sub>X</sub> = −m<sub>A</sub>v<sub>A′y</sub> / v<sub>B′y</sub></b><br>⑦ แกน x: <b>m<sub>X</sub> = m<sub>A</sub>(v<sub>A</sub> − v<sub>A′x</sub>) / v<sub>B′x</sub></b> แล้วเฉลี่ยสองแกน',
     'out': 'แถว 6: m<sub>X</sub> = 216 g (แกน y) · 223 g (แกน x) → 219 g · แถว 7: 225 · 222 → 224 g · <b>เฉลี่ย 221 g</b>' },
   { 'el': ['.ans-row:has(#ans-m)', '#ansMMsg'], 'prep': "{ const X = goodRows().filter(q => q.X && q.mEst); $('ans-m').value = (X.reduce((a, q) => a + q.mEst, 0) / X.length).toFixed(0); } checkM()",
     'title': 'ตอบมวลลูกยางปริศนา X',
     'text': 'นำค่าเฉลี่ย m<sub>X</sub> ใต้ตาราง ② กรอกในกรอบ <b>🎯 ตรวจคำตอบ</b> แล้วกด <b>ตรวจมวล X</b> (ยอมคลาด 6%)',
     'out': '<b>m<sub>X</sub></b> ≈ 221 g ในภาพตัวอย่าง (มวลลูกยาง X สุ่มทุกครั้งที่เปิดแลป ในช่วง 100 – 350 g)' },
  ],
 }
