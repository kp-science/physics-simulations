# -*- coding: utf-8 -*-
# Lab 103 ความตึงผิว: วิธีดึงห่วงลวด — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'หาความตึงผิว γ = ΔF/(4πr) จากแรงสูงสุดก่อนฟิล์มขาด',
  'setup': r"""
    /* หยุดเวลาของแลป (simSpeed = 0) แล้วเดินแบบจำลองของแลปเอง stepPhys() · ค่าบนเซนเซอร์ปัดทศนิยม 1 ตำแหน่งแบบเดียวกับแลป */
    simSpeed = 0;
    /* ตรึงของเหลว X: γ = 48.0 mN/m ให้ภาพตรงกับข้อความ (ของจริงสุ่มใหม่ทุกครั้ง) · ป้าย 3D ยังแสดงเป็นของเหลวปริศนาเหมือนเดิม */
    LIQS[3].g = 48.0;
    const hide = f => function () { const s = LIQS[3].g; LIQS[3].g = null; try { return f.apply(this, arguments); } finally { LIQS[3].g = s; } };
    window.update3D = hide(window.update3D);
    window.checkG = function () { const v = parseFloat($('ans-g').value), ok = Math.abs((v - 48.0) / 48.0) <= 0.05;
      $('ansGMsg').innerHTML = ok ? '<span style="color:#86efac">✓ ถูกต้อง! คลาดไม่เกิน 5%</span>' : '<span style="color:#fca5a5">✗ ยังไม่ถูก</span>'; };
    window.__show = () => { Fshow = Math.round(Ftrue * 10) / 10; if (P.senTex) redrawTex(P.senTex); drawAll(); };
    window.__up = () => { nudgeJ(18 - J); stepPhys(0.05); __show(); };                 /* ยกจาน 6 cm: ห่วงจมใต้ผิว 2 mm */
    window.__pull = () => { toggleSlow(true); let k = 0; while (!broke && k++ < 5000) stepPhys(0.05); stepPhys(0.05); __show(); };
    window.__meas = (r, l) => { if (ringI !== r) setRing(r); if (liqI !== l) setLiq(l); stepPhys(0.05); __show();
      const W = Fshow.toFixed(1); __up(); resetPeak(); __pull(); $('in-w').value = W; $('in-f').value = peak.toFixed(1); recordRow(); };
    window.__R = () => setTimeout(() => { const w = $('tableA'); w.scrollLeft = 1e4; w.scrollTop = 1e4; }, 600);
  """,
  'steps': [
   { 'el': ['#view3d', '#ringBtns', '#liqBtns'], 'prep': "setMode('manual'); rows = []; resetLab(); stepPhys(0.05); __show(); renderAll(); setView('iso'); scrollTo(0,0)",
     'title': 'ดูอุปกรณ์ เลือกห่วง r = 1.50 cm กับน้ำ',
     'text': '<b>ห่วงลวดแพลทินัม</b>แขวนด้วยลวด 3 เส้นกับ<b>เซนเซอร์แรง</b> (ละเอียด 0.1 mN มีค่าสดและค่า PEAK = ค่าสูงสุดที่เคยวัดได้) · ใต้ห่วงเป็น<b>จานของเหลว</b>บนแท่นยกที่ปรับขึ้น-ลงได้<br>เลือกห่วง <b>r = 1.50 cm</b> และ <b>💧 น้ำ</b><br><small>ฟิล์มของเหลวเกาะห่วงทั้งขอบด้านในและด้านนอก ความยาวขอบที่ผิวดึงจึงเป็น 2 × 2πr = 4πr</small>',
     'out': '<b>L = 4πr</b> = 4π × 0.0150 = 0.1885 m' },
   { 'el': ['#view3d', '#in-w'], 'prep': "setView('sen'); $('in-w').value = Fshow.toFixed(1)",
     'title': 'อ่านน้ำหนักห่วง W',
     'text': 'ห่วงยังอยู่<b>ในอากาศ</b> กด <b>📟 เซนเซอร์แรง</b> อ่านค่าสด (ตัวเลขใหญ่ด้านบน) กรอกช่อง <b>② น้ำหนักห่วง W</b><br><small>ค่าสดแกว่ง ±0.1 mN ให้อ่านค่าที่ขึ้นบ่อยที่สุด</small>',
     'out': '<b>W</b> = 2.1 mN' },
   { 'el': ['.panel-section [onclick="nudgeJ(1)"]', '#view3d'], 'prep': "__up(); setView('ring')",
     'title': 'ยกจานจนห่วงจมใต้ผิว',
     'text': 'กด <b>⬆ +1 cm</b> หลายครั้ง (6 ครั้ง) ยกจานของเหลวขึ้นจน<b>ห่วงจมใต้ผิว</b>เล็กน้อย · กด <b>🔍 ห่วงกับผิวของเหลว</b> ดูว่าห่วงอยู่ใต้ผิวทั้งวง (ช่อง <b>ห่วง</b> บอก “จมใต้ผิว”)',
     'out': 'ห่วงจมใต้ผิวน้ำราว 2 mm' },
   { 'el': ['.panel-section [onclick="resetPeak()"]', '#view3d'], 'prep': "resetPeak(); setView('sen')",
     'title': 'ล้างค่า PEAK',
     'text': 'กด <b>↺ ล้าง PEAK</b> ให้เซนเซอร์เริ่มจับค่าสูงสุดใหม่ตั้งแต่ตอนนี้ ค่า PEAK จะกลับมาเท่าค่าสด',
     'out': 'PEAK ≈ W ≈ 2.1 mN' },
   { 'el': ['#slowBtn', '#view3d'], 'prep': "toggleSlow(true); for (let i = 0; i < 120; i++) stepPhys(0.05); __show(); setView('sen')",
     'title': 'ลดจานลงช้า ๆ ฟิล์มยืด',
     'text': 'กด <b>⤵ ลดช้า ๆ อัตโนมัติ (0.5 mm/s)</b> จานลดลง ผิวของเหลวต่ำกว่าห่วง แต่<b>ฟิล์มของเหลว</b>ยังเกาะห่วงไว้และดึงห่วงลง · ค่าสดบนเซนเซอร์<b>เพิ่มขึ้นเรื่อย ๆ</b> (ช่อง <b>ฟิล์ม</b> บอก “กำลังยืด” · ดูฟิล์มได้ที่ 🔍 ห่วงกับผิวของเหลว)',
     'out': 'ฟิล์มยืดสูง 1.0 mm: ค่าสดเพิ่มจาก 2.1 เป็น 12.0 mN (PEAK ตามขึ้นไปด้วย)' },
   { 'el': ['#view3d', '#in-f'], 'prep': "__pull(); setView('sen'); $('in-f').value = peak.toFixed(1)",
     'title': 'ฟิล์มขาด อ่านค่า PEAK',
     'text': 'ลดต่อไปจน<b>ฟิล์มขาด</b> (จานหยุดลดเอง) ค่าสดตกกลับเท่า W · อ่าน<b>ค่า PEAK</b> (ตัวเลขสีเหลือง) = แรงสูงสุดก่อนฟิล์มขาด กรอกช่อง <b>③ F<sub>max</sub></b>',
     'out': '<b>F<sub>max</sub></b> = 15.9 mN · ค่าสดกลับเป็น 2.1 mN' },
   { 'el': ['#lastRec', '#recForm .rf-btn'], 'prep': "recordRow(); setView('iso')",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> แล้วโปรแกรมคำนวณต่อ:<br>① แรงจากความตึงผิว <b>ΔF = F<sub>max</sub> − W</b><br>② ความยาวขอบ <b>L = 4πr</b> (r เป็นเมตร)<br>③ ความตึงผิว <b>γ = ΔF/L</b> (mN/m)',
     'out': '<b>ΔF</b> = 15.9 − 2.1 = 13.8 mN · <b>γ</b> = 13.8/0.1885 ≈ 73.2 mN/m (ค่าอ้างอิงของน้ำ 72.8 mN/m)' },
   { 'el': ['#lastRec', '#ab-ring'], 'prep': "__meas(1, 0); setView('iso')",
     'title': 'เปลี่ยนเป็นห่วง r = 2.50 cm วัดซ้ำ',
     'text': 'กด <b>r = 2.50 cm</b> ในแผงขวา หรือปุ่ม <b>⭕ ห่วง</b> ใต้ภาพ (จานลดลงให้เอง) ทำขั้นที่ 2–7 ซ้ำ: อ่าน W → ยกจาน → ล้าง PEAK → ลดช้า ๆ จนฟิล์มขาด → อ่าน PEAK → บันทึก<br><small>ห่วงใหญ่ขอบยาวกว่า ฟิล์มดึงแรงกว่า แต่ γ ของน้ำเท่าเดิม</small>',
     'out': 'W = 3.5 mN · F<sub>max</sub> = 26.3 mN → ΔF = 22.8 mN · L = 4π × 0.025 = 0.3142 m → <b>γ</b> ≈ 72.6 mN/m' },
   { 'el': '#view3d', 'prep': "setRing(0); stepPhys(0.05); __up(); resetPeak(); { let k = 0; while (!broke && k++ < 2000) { J -= 0.4 * 0.02; stepPhys(0.02); } } stepPhys(0.05); __show(); setView('sen')",
     'title': 'ข้อควรระวัง: ลดจานเร็วเกินไป',
     'text': 'ถ้าลากจานลง<b>เร็ว</b> (ราว 4 mm/s) ฟิล์มขาดก่อนแรงถึงค่าสูงสุดจริง ค่า PEAK จึง<b>ต่ำกว่าจริง</b> · ต้องลดช้า ๆ (ปุ่มอัตโนมัติ 0.5 mm/s หรือ −0.5 mm ทีละครั้ง) · ค่าที่ลดเร็วไม่ต้องบันทึก',
     'out': 'ห่วง 1.50 cm ในน้ำ ลดเร็ว: PEAK ≈ 13.3 mN (ช้า ๆ ได้ 15.9 mN) → γ ≈ 59 mN/m ต่ำกว่าจริง' },
   { 'el': '#tableA', 'prep': "__meas(0, 1); __meas(0, 2); setView('iso'); __R()",
     'title': 'น้ำสบู่และเอทานอล',
     'text': 'ใช้ห่วง r = 1.50 cm วัดกับ <b>🫧 น้ำสบู่</b> และ <b>🍶 เอทานอล</b> อย่างละ 1 ครั้ง · ค่า PEAK น้อยกว่าน้ำมาก แสดงว่าความตึงผิวน้อยกว่า<br><small>สบู่เป็นสารลดแรงตึงผิว น้ำสบู่จึงแทรกเข้าเส้นใยผ้าได้ดี</small>',
     'out': 'น้ำสบู่: F<sub>max</sub> = 7.8 mN → ΔF = 5.7 mN → <b>γ</b> ≈ 30.2 mN/m · เอทานอล: 6.3 mN → ΔF = 4.2 mN → <b>γ</b> ≈ 22.3 mN/m' },
   { 'el': '#tableA', 'prep': "__meas(0, 3); __meas(1, 3); setView('iso'); __R()",
     'title': 'ของเหลวปริศนา X: วัดกับห่วงทั้งสองขนาด',
     'text': 'เลือก <b>❓ X</b> วัดกับห่วง 1.50 cm และ 2.50 cm · ดูคอลัมน์ <b>γ</b> และ<b>ค่าเฉลี่ย</b>ใต้ตาราง',
     'out': 'r 1.50 cm: F<sub>max</sub> = 11.2 mN → ΔF = 9.1 mN → γ ≈ 48.3 · r 2.50 cm: 18.5 mN → ΔF = 15.0 mN → γ ≈ 47.7 · <b>γ<sub>X</sub> เฉลี่ย ≈ 48.0 mN/m</b>' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "renderAll()",
     'title': 'กราฟ ΔF – L: ความชัน = γ',
     'text': 'จุดของของเหลวชนิดเดียวกันอยู่บน<b>เส้นตรงผ่านจุดกำเนิด</b> แสดงว่า <b>ΔF ∝ L</b> (แรงแปรผันตรงกับความยาวขอบ) · <b>ความชัน = ΔF/L = γ</b><br><small>เส้นยิ่งชัน ความตึงผิวยิ่งมาก: น้ำ > X > น้ำสบู่ > เอทานอล</small>',
     'out': 'ความชัน น้ำ ≈ 72.7 mN/m · <b>X ≈ 47.9 mN/m</b> · น้ำสบู่ ≈ 30.2 · เอทานอล ≈ 22.3 mN/m' },
   { 'el': ['#ans-g', '#ansGMsg'], 'prep': "$('ans-g').value = 48.0; checkG()",
     'title': 'กรอกความตึงผิวของ X แล้วตรวจ',
     'text': 'พิมพ์ γ ของ X (mN/m) ในกรอบ <b>🎯 ตรวจคำตอบ</b> แล้วกด <b>ตรวจ</b> · ถือว่าถูกเมื่อคลาดไม่เกิน 5%<br><small>ถ้าคลาดมาก: ตรวจว่าใช้ r เป็นเมตร ใช้ 4πr (ไม่ใช่ 2πr) และลดจานช้า ๆ</small>',
     'out': '<b>γ<sub>X</sub></b> ≈ 48 mN/m (ค่าจริงสุ่มใหม่ทุกครั้งที่เปิดแลป ในช่วง 26–68 mN/m)' },
  ],
 }
