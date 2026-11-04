# -*- coding: utf-8 -*-
# Lab 6.2 นาฬิกาน้ำ — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ปริมาตร/ระดับน้ำ = แบบจำลองของแลป (computeRate: r = 25 × ช่องเปิด × √(h/10) · กรวย V = (π/12)h³ · เติมน้ำอัตโนมัติ = h คงที่)
#   ก้าวเวลา 1/60 s แบบเดียวกับ loop() ของแลป · เวลาที่กดปิดน้ำ = ค่าคงที่ใกล้ 1, 3, 5, 7 s (มือคนกดไม่ตรงเป๊ะ)
#   ค่าที่ "อ่านจากสเกล" = ปริมาตรจริงปัดเป็น 1 ml (สเกลขีดละ 2 ml อ่านประมาณครึ่งช่อง)
GUIDE = {
  'title': 'นาฬิกาน้ำ: หาอัตราการไหลจากกราฟปริมาตรกับเวลา',
  'setup': r"""
    window.__ui = () => { document.getElementById('r-time').textContent = t.toFixed(2);
      document.getElementById('r-vol').textContent = readMode ? '—' : vol.toFixed(1);
      document.getElementById('r-rate').textContent = currentRate.toFixed(1); draw(); };
    /* เดินแบบจำลองของแลป (สมการเดียวกับ loop) จนเวลาสะสม = T */
    window.__run = T => { while (t < T - 1e-9) { const dt = Math.min(1 / 60, T - t); currentRate = computeRate(currentH); const fl = currentRate * dt; t += dt; vol += fl;
        if (refillMode) { currentH = initialH; funnelVol = FUNNEL_C * Math.pow(currentH, 3); }
        else { funnelVol -= fl; currentH = funnelVol > 0 ? Math.cbrt(funnelVol / FUNNEL_C) : 0; } }
      currentRate = computeRate(currentH); __ui(); };
    /* ปิดน้ำที่เวลา T → กล่องอ่านสเกล → พิมพ์ค่าที่อ่าน (ปัดเป็น 1 ml) → ยืนยัน */
    window.__stop = (T, keep) => { __run(T); openReadingPrompt(); document.getElementById('read-input').value = Math.round(vol); confirmReading(); if (!keep) closeReadingPrompt(); __ui(); };
    window.__chk = (id, on) => { const c = document.getElementById(id); if (c.checked !== on) { c.checked = on; c.dispatchEvent(new Event('change')); } };
    window.__sl = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input')); };
    window.__clear = () => { trials.length = 0; renderTable(); drawGraph(); };
    window.__flowLook = () => { isFlowing = true; const b = document.getElementById('openBtn'); b.textContent = '⏸ ปิดน้ำ'; b.classList.add('flowing'); };
  """,
  'steps': [
   { 'el': ['.sim-panels .panel', '#view3d'], 'prep': "__sl('sl-h', 10); __sl('sl-open', 100); __chk('cb-refill', true); __chk('cb-read', true); resetSim(); __clear(); setView('iso'); scrollTo(0,0)",
     'title': 'ตั้งระดับน้ำ 10 cm ช่องเปิด 100 %',
     'text': 'ตั้ง <b>ระดับน้ำ = 10 cm</b> และ <b>ช่องเปิด = 100 %</b> · ติ๊ก <b>💧 เติมน้ำอัตโนมัติ</b> ให้ระดับน้ำในกรวยคงที่เหมือนในใบงาน · ติ๊ก <b>🔍 โหมดอ่านค่าเอง</b> เพื่ออ่านปริมาตรจากสเกลกระบอกตวงเอง<br><small>ชุดอุปกรณ์: กรวยแก้วใส่น้ำ → สายยางมีตัวหนีบ → กระบอกตวง 200 ml และนาฬิกาจับเวลาบนโต๊ะ</small>',
     'out': '<b>h</b> = 10 cm · ช่องเปิด 100 % → อัตราการไหล (ช่องบนภาพ) = 25.0 ml/s' },
   { 'el': ['#view3d'], 'prep': "setView('funnel')",
     'title': 'ดูระดับน้ำในกรวย',
     'text': 'กด <b>🔍 กรวย</b> น้ำในกรวยสูง 10 cm จากปลายกรวย · ระดับน้ำนี้ทำให้เกิดความดันที่ดันน้ำไหลออกทางสายยาง ถ้าระดับน้ำคงที่ น้ำจะไหลออกด้วย<b>อัตราคงที่</b><br><small>ถ้าระดับน้ำสูงขึ้น น้ำไหลเร็วขึ้น (v = √2gh)</small>',
     'out': 'ระดับน้ำในกรวย <b>h</b> = 10 cm (คงที่ตลอดการทดลอง)' },
   { 'el': ['#openBtn', '#view3d'], 'prep': "__flowLook(); __run(0.55); setView('iso')",
     'title': 'เปิดตัวหนีบ น้ำไหล นาฬิกาเริ่มเดิน',
     'text': 'แตะ<b>ตัวหนีบสายยาง</b> (วงแหวนเขียว) ในภาพ หรือกด <b>▶ เปิดน้ำ</b> · น้ำไหลลงกระบอกตวง และนาฬิกาจับเวลาบนโต๊ะเริ่มเดินพร้อมกัน · ตั้งใจดูนาฬิกา เตรียมปิดน้ำเมื่อเวลาใกล้ <b>1 s</b>' },
   { 'el': '#view3d', 'prep': "stopFlow(); __run(1.04); openReadingPrompt(); document.getElementById('read-input').value = Math.round(vol); __ui()",
     'title': 'ปิดน้ำที่ราว 1 s แล้วอ่านสเกลกระบอกตวง',
     'text': 'แตะตัวหนีบอีกครั้ง (⏸ ปิดน้ำ) น้ำหยุดไหลและนาฬิกาหยุด · ภาพซูมไปที่<b>สเกลกระบอกตวง</b>ให้เอง (ขีดเล็กละ 2 ml) ให้สายตาอยู่ระดับ<b>ส่วนล่างของผิวโค้งน้ำ</b> อ่านปริมาตร แล้วพิมพ์ในช่อง ml',
     'out': '<b>t</b> = 1.04 s · <b>V</b> = 26 ml' },
   { 'el': ['#readOverlay .read-card', '#trialTable'], 'prep': "confirmReading(); __ui()",
     'title': 'กดยืนยัน → ค่าเข้าตาราง',
     'text': 'กด <b>✅ ยืนยัน</b> โปรแกรมบอกว่าอ่านถูกแค่ไหน (เทียบค่าจริง) แล้วบันทึก t และ V ลงตาราง พร้อมคำนวณ<br>① อัตราการไหล <b>r = V / t</b> = 26 / 1.04',
     'out': 'แถว 1: t = 1.04 s · V = 26 ml · <b>r</b> = 25.0 ml/s' },
   { 'el': '#trialTable', 'prep': "closeReadingPrompt(); __stop(3.01); __stop(4.97); __stop(7.03); setView('iso')",
     'title': 'เปิดน้ำต่อ ปิดที่ 3, 5, 7 s',
     'text': 'แตะตัวหนีบเปิดน้ำ<b>ต่อจากเดิม</b> (ไม่รีเซ็ต — นาฬิกาเดินต่อ น้ำสะสมในกระบอกตวง) ปิดเมื่อเวลาราว <b>3 s</b> อ่านสเกล ยืนยัน · ทำซ้ำที่ราว <b>5 s</b> และ <b>7 s</b>',
     'out': '<b>t</b> = 3.01 · 4.97 · 7.03 s → <b>V</b> = 75 · 124 · 176 ml' },
   { 'el': '#trialTable', 'prep': "__ui()",
     'title': 'อ่านตาราง: อัตราการไหลแต่ละช่วง',
     'text': 'คอลัมน์ <b>r = V/t</b> ของทุกแถวเกือบเท่ากัน · แถว <b>μ</b> ล่างสุด = ค่าเฉลี่ยของแต่ละคอลัมน์<br><small>ปุ่ม ✕ ท้ายแถวใช้ลบแถวที่อ่านผิด</small>',
     'out': '<b>r</b> = 25.0 · 24.92 · 24.95 · 25.04 ml/s · เฉลี่ย ≈ <b>24.98 ml/s</b>' },
   { 'el': ['#graphCanvas', '#g-slope'], 'prep': "drawGraph()",
     'title': 'กราฟ V กับ t → ความชัน = อัตราการไหล',
     'text': 'จุดทั้ง 4 เรียงเป็น<b>เส้นตรงผ่านจุดกำเนิด</b> → V ∝ t น้ำไหลออกด้วยอัตราคงที่ · โปรแกรมลากเส้นตรงที่เหมาะสมที่สุดให้ และแสดงความชันใต้กราฟ<br>② <b>V = r t</b> → ความชันของกราฟ = r',
     'out': 'ความชัน = <b>r ≈ 25.0 ml/s</b> (h = 10 cm, ช่องเปิด 100 %)' },
   { 'el': '.predict-box', 'prep': "document.getElementById('pred-t').value = 4; updatePrediction()",
     'title': 'ใช้นาฬิกาน้ำบอกเวลา',
     'text': 'ในกล่อง <b>🎯 โหมดทำนาย</b> พิมพ์เวลา <b>4 s</b> โปรแกรมคำนวณ ③ <b>V = r × t</b> = 25 × 4 · กลับกัน ถ้าน้ำในกระบอกตวงเพิ่มขึ้น 100 ml แปลว่าเวลาผ่านไป <b>t = V / r</b> = 100 / 25 = 4 s — นี่คือหลักของนาฬิกาน้ำ<br><small>ลองเปิดน้ำแล้วปิดเมื่อได้ 100 ml ดูว่านาฬิกาบอกราว 4 s จริงไหม</small>',
     'out': 't = 4 s → <b>V</b> = 100 ml' },
   { 'el': '#hintBox', 'prep': "if (!document.getElementById('hintBox').classList.contains('show')) toggleHint()",
     'title': 'เทียบกับข้อมูลในใบงาน',
     'text': 'กด <b>💡 ดูเฉลย</b> ข้อมูลจากใบงาน (เวลา 1, 3, 5, 7 s) ให้กราฟเป็นเส้นตรงเช่นเดียวกัน · เทียบกับค่า r ที่วัดได้',
     'out': 'ใบงาน: V = 20 · 76 · 126 · 181 ml → <b>r ≈ 25 ml/s</b> ตรงกับที่วัดได้' },
   { 'el': ['#graphCanvas', '#trialTable'], 'prep': "toggleHint(); __chk('cb-refill', false); resetSim(); __clear(); [1.04, 3.01, 4.97, 7.03].forEach(T => __stop(T)); setView('iso')",
     'title': 'ไม่เติมน้ำ: ระดับน้ำในกรวยลดลง',
     'text': 'เอาติ๊ก <b>💧 เติมน้ำอัตโนมัติ</b> ออก กด <b>↺ รีเซ็ต</b> ลบแถวเก่าด้วยปุ่ม ✕ แล้ววัดใหม่ที่ราว 1, 3, 5, 7 s · ตอนนี้น้ำในกรวยลดลงขณะไหล ความดันลดลง น้ำจึงไหล<b>ช้าลงเรื่อย ๆ</b> ค่า r ในตารางลดลงทุกแถว และความชันของกราฟน้อยกว่าเดิม (ถ้าปล่อยนานขึ้น กราฟจะโค้งลงชัดเจน)',
     'out': '<b>V</b> = 26 · 73 · 119 · 164 ml · <b>r</b> = V/t ลดลง 25.0 → 23.3 ml/s · ความชัน ≈ 23.9 ml/s' },
   { 'el': ['.sim-panels .panel', '#trialTable'], 'prep': "__chk('cb-refill', true); __sl('sl-open', 50); resetSim(); __clear(); [2.02, 4.03, 5.98, 7.97].forEach(T => __stop(T)); setView('iso')",
     'title': 'ลดช่องเปิดเหลือ 50 % แล้ววัดซ้ำ',
     'text': 'ติ๊กเติมน้ำอัตโนมัติกลับ ตั้ง <b>ช่องเปิด = 50 %</b> (บีบสายยางให้แคบลง) รีเซ็ต ลบแถวเก่า แล้ววัดที่ราว 2, 4, 6, 8 s',
     'out': '<b>V</b> = 25 · 50 · 75 · 100 ml · <b>r</b> ≈ 12.5 ml/s (ครึ่งหนึ่งของช่องเปิด 100 %)' },
   { 'el': ['#graphCanvas', '#g-slope'], 'prep': "drawGraph()",
     'title': 'สรุปผล',
     'text': 'เมื่อ<b>ระดับน้ำคงที่</b> กราฟ V กับ t เป็นเส้นตรง น้ำไหลด้วยอัตราคงที่ จึงใช้ปริมาตรน้ำวัดเวลาได้: <b>t = V / r</b> · ช่องเปิดเล็กลง ความชันลดลง (นาฬิกาเดินช้า วัดเวลาได้นานขึ้น) · ถ้าไม่รักษาระดับน้ำ อัตราการไหลลดลง นาฬิกาน้ำจะบอกเวลาคลาดเคลื่อน',
     'out': 'ความชัน = <b>r ≈ 12.6 ml/s</b> (ช่องเปิด 50 %) · ≈ <b>25.0 ml/s</b> (ช่องเปิด 100 %)' },
  ],
 }
