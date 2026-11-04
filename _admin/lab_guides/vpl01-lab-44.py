# -*- coding: utf-8 -*-
# Lab 44 SHM06 Damping & Resonance — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# หยุดนาฬิกา (__kpSpeed 0) แล้วเดินแบบจำลองของแลปเอง: t += 1/60 s · step() 4 ครั้ง · pushTrace() (เหมือน loop() ของแลป)
GUIDE = {
  'title': 'คาบของการสั่นแบบหน่วง และหาความถี่ธรรมชาติจากการสั่นพ้อง',
  'setup': r"""
    if (window.__kpSpeed) { __kpSpeed.set(0); const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    const sub = n => document.querySelectorAll('.subnav button')[n];
    window.__base = k => setBase(k, sub({ A: 0, B: 1, C: 2 }[k]));
    window.__sl = (id, v) => { const e = document.getElementById('sl-' + id); e.value = v; document.getElementById('vi-' + id).value = v; e.dispatchEvent(new Event('input')); };
    window.__run = d => { const T1 = t + d; while (t < T1 - 1e-9) { const dt = 1 / 60; t += dt; for (let i = 0; i < 4; i++) step(dt / 4); pushTrace(); } draw(); drawGraph(); updateReadout(); };
    window.__play = on => { const b = document.getElementById('playBtn'); isPlaying = on; b.textContent = on ? '⏸ หยุด' : '▶ เริ่ม'; b.classList.toggle('playing', on); };
    /* caliper วางบนยอดที่ k และ k+1 (ยอด = จุดสูงสุดเฉพาะที่ของรอยกราฟ แบบเดียวกับ snapToPeak ของแลป) */
    window.__cal = k => { const tS = Math.max(0, t - 8), P = []; for (let i = 1; i < traceA.length - 1; i++) if (traceA[i].x > traceA[i - 1].x && traceA[i].x > traceA[i + 1].x && traceA[i].t >= tS) P.push(traceA[i].t); caliper.x1 = (P[k] - tS) / 8; caliper.x2 = (P[k + 1] - tS) / 8; updateCaliperReadout(); gzFit(); drawGraph(); };
    window.__measA = b => { setB(b); resetCaliper(); __run(4); __cal(2); recordCaliper(); __cal(3); recordCaliper(); };
    /* ฐาน B: เปลี่ยน f แล้วรอ 30 s ให้การสั่นคงตัว · แตะกราฟที่ f เดิมอีกครั้ง (amaxObserved = 0 แบบ handleGraph) รอ 3 s แล้วบันทึกจุด */
    window.__fd = f => { document.getElementById('sl-fd').value = f; document.getElementById('vi-fd').value = f; amaxObserved = 0; updateReadout(); };
    window.__ptB = f => { __fd(f); __run(30); amaxObserved = 0; __run(3); recordPoint(); };
  """,
  'steps': [
   { 'el': ['.subnav', '#sidePanel .base-block[data-base="A"] .readout'], 'prep': "__base('A'); setMode('manual'); damping_log = []; document.querySelector('#tableA tbody').innerHTML = ''; __sl('k', 200); __sl('m', 1); __sl('A0', 0.2); setB(0); setView('iso'); scrollTo(0,0)",
     'title': 'ฐาน A: ตั้ง k = 200 N/m, m = 1 kg, b = 0',
     'text': 'เลือก <b>ฐาน A · Damping Sweep</b> โหมด <b>✍ บันทึกเอง</b> · ตั้ง <b>k = 200 N/m</b> · <b>m = 1 kg</b> · <b>A₀ = 0.20 m</b> · กด <b>b=0</b> (ยกใบพายพ้นน้ำมันหนืด ไม่มีการหน่วง)<br>① <b>ω₀ = √(k/m)</b> · คาบตามทฤษฎี <b>T = 2π/ω</b>',
     'out': '<b>ω₀</b> = 14.14 rad/s · <b>T</b><sub>ทฤษฎี</sub> = 0.444 s' },
   { 'el': '#graphCanvas', 'prep': "if (GZ.on) toggleGraphZoom(); __run(6); __play(false)",
     'title': 'กดเริ่ม แล้วหยุดเมื่อกราฟมีหลายยอด',
     'text': 'กด <b>▶ เริ่ม</b> รถทดลองสั่นบนราง กราฟ A(t) วาดการกระจัดตามเวลา · รอให้มีหลายยอด แล้วกด <b>⏸ หยุด</b> กราฟจะหยุดนิ่ง<br><small>เมื่อ b = 0 ยอดทุกยอดสูงเท่ากัน (แอมพลิจูดคงตัว)</small>',
     'out': 'แอมพลิจูดคงตัว <b>A</b> = 0.20 m' },
   { 'el': ['#graphCanvas', '#cal-dt'], 'prep': "resetSim(); __run(4); __cal(2); if (!GZ.on) toggleGraphZoom()",
     'title': 'วาง caliper บนยอดติดกัน 2 ยอด',
     'text': 'ลาก<b>เส้นประสีส้ม 1 และ 2</b> บนกราฟ ไปที่ยอดคลื่น 2 ยอดที่อยู่ติดกัน เส้นจะดูดเข้ายอดเอง · ยอดอยู่ชิดกันให้กด <b>🔍 ซูมกราฟ</b> · อ่าน <b>ระยะ caliper Δt</b> = คาบ',
     'out': '<b>Δt</b> = 0.433 s (= T₁)' },
   { 'el': ['#caliperPanel', '#tableA'], 'prep': "resetCaliper(); recordCaliper(); __cal(3); recordCaliper()",
     'title': 'บันทึก T₁ แล้ววัดซ้ำได้ T₂',
     'text': 'กด <b>📍 บันทึกคาบนี้</b> ได้ T₁ · เลื่อน caliper ไปยอดคู่ถัดไป กดบันทึกอีกครั้งได้ T₂ · โปรแกรมคำนวณต่อ<br>② <b>T̄ = (T₁ + T₂)/2</b><br>③ คาบตามทฤษฎีของการสั่นแบบหน่วง <b>ω<sub>d</sub> = √(ω₀² − (b/2m)²)</b> · <b>T = 2π/ω<sub>d</sub></b><br>④ %error = |T̄ − T<sub>ทฤษฎี</sub>| / T<sub>ทฤษฎี</sub> × 100 แล้วเพิ่มแถวในตาราง',
     'out': '<b>T₁</b> = 0.433 s · <b>T₂</b> = 0.450 s → <b>T̄</b> = 0.442 s · <b>T</b><sub>ทฤษฎี</sub> = 0.444 s · คลาด 0.6% (T₁ กับ T₂ ต่างกัน 3.8% จากการวางบนยอดของรอยกราฟ)' },
   { 'el': '#tableA', 'prep': "[0.1, 0.5, 1.0].forEach(__measA)",
     'title': 'เปลี่ยน b แล้ววัดคาบซ้ำ',
     'text': 'กด <b>b=0.1</b> · <b>b=0.5</b> · <b>b=1.0</b> (ใบพายจุ่มลึกขึ้นในน้ำมันหนืด) แล้ววัด T₁ T₂ แบบเดิมทุกค่า · เทียบคาบในตาราง<br><small>caliper ดูดเข้ายอดของรอยกราฟที่เก็บทุก 1/60 s คาบที่วัดจึงคลาดได้ราว ±0.02 s</small>',
     'out': 'b = 0 · 0.1 · 0.5 · 1.0: <b>T̄</b> = 0.442 s ทุกค่า · T<sub>ทฤษฎี</sub> 0.444 – 0.445 s → <b>การหน่วงน้อย ๆ แทบไม่เปลี่ยนคาบ</b>' },
   { 'el': ['#graphCanvas', '#view3d'], 'prep': "if (GZ.on) toggleGraphZoom(); setB(1.0); __run(5); setView('paddle')",
     'title': 'สังเกตแอมพลิจูดลดลง',
     'text': 'ที่ b = 1.0 กราฟ A(t) ยอดลดลงเรื่อย ๆ ตาม<b>เส้นประสีส้ม</b> (เส้นห่อหุ้ม) · กด <b>🔍 ใบพาย</b> ดูใบพายในรางน้ำมันหนืดที่ดึงพลังงานออกจากระบบ<br>⑤ <b>A(t) = A₀ e<sup>−bt/2m</sup></b>',
     'out': 'b = 1.0: หลัง 2 s <b>A</b> = 0.20 e<sup>−1</sup> ≈ 0.074 m · <b>สิ่งที่เปลี่ยนคือแอมพลิจูด ไม่ใช่คาบ</b>' },
   { 'el': ['.subnav', '#view3d'], 'prep': "setView('iso'); __base('B'); setMode('manual'); clearPoints(); __sl('F0', 1); __sl('bB', 0.3); __sl('kB', 200); __sl('mB', 1); __fd(1.0); __run(8); setView('drive')",
     'title': 'ฐาน B: ให้มอเตอร์ขับการสั่น',
     'text': 'เลือก <b>ฐาน B · Resonance Sweep</b> โหมด <b>✍ บันทึกเอง</b> (ค่า f_natural ถูกซ่อน ???) · ตั้ง <b>F₀ = 1 N</b> · <b>b = 0.3 N·s/m</b> · <b>k = 200 N/m</b> · <b>m = 1 kg</b> · กด <b>▶ เริ่ม</b> · กด <b>🔍 มอเตอร์</b> ดูจานเหวี่ยงดันปลายสปริงไปมาที่ความถี่ <b>f_drive</b>',
     'out': 'f_drive = 1.00 Hz → รถสั่นด้วยแอมพลิจูดเล็ก (ราว 0.006 m)' },
   { 'el': ['#graphCanvas', '#tableB'], 'prep': "setView('iso'); clearPoints(); [1.0, 1.5, 1.8, 2.0, 2.1, 2.2, 2.25, 2.3, 2.4, 2.6, 3.0].forEach(__ptB); drawGraph()",
     'title': 'กวาดความถี่ บันทึกจุด (f, A)',
     'text': 'เลื่อน <b>f_drive</b> (หรือแตะกราฟล่าง) ทีละค่า · รอให้การสั่นคงตัว (ราว 30 s) แตะกราฟที่ f เดิมอีกครั้งเพื่อเริ่มจับแอมพลิจูดใหม่ รอ 2–3 s แล้วกด <b>+ บันทึกจุด (f, A)</b> · ยิ่งใกล้ยอดให้เลื่อนทีละน้อย (0.05 Hz)<br><small>แอมพลิจูดที่บันทึก = ค่ามากสุดของ |x| ตั้งแต่เริ่มจับ ถ้าไม่รอให้คงตัวจะได้ค่าเกินจริง</small>',
     'out': 'f = 2.00 · 2.20 · <b>2.25</b> · 2.30 · 2.40 Hz → <b>A</b> ≈ 0.024 · 0.101 · <b>0.234</b> · 0.105 · 0.037 m' },
   { 'el': ['[onclick="recordResonancePeak()"]', '#resonanceResult'], 'prep': "__fd(2.25); __run(30); recordResonancePeak()",
     'title': 'ตั้ง f ที่ A สูงสุด แล้วบันทึก peak',
     'text': 'ตั้ง f_drive ที่ให้ <b>A สูงสุด</b> แล้วกด <b>📍 บันทึก peak</b> โปรแกรมเผยค่าจริงของ f_natural และ %error<br>⑥ ความถี่ธรรมชาติ <b>f₀ = (1/2π)√(k/m)</b> · การสั่นพ้องเกิดเมื่อ <b>f_drive = f₀</b>',
     'out': '<b>f</b><sub>วัด</sub> = 2.25 Hz · <b>f₀</b> = (1/2π)√200 = 2.251 Hz · คลาด &lt; 0.1%' },
   { 'el': '#graphCanvas', 'prep': "setMode('auto'); drawGraph()",
     'title': 'เปิดเฉลย: เทียบกราฟการสั่นพ้อง',
     'text': 'กด <b>👁 เผยเฉลย</b> กราฟแสดงเส้น <b>f_n</b> สีเขียวที่ยอดของเส้นโค้ง · จุดที่บันทึกเรียงเป็นยอดแหลมแคบ · ยิ่ง b น้อย ยอดยิ่งสูงและแคบ<br>⑦ <b>Q = √(km)/b</b> · ความกว้างของยอด ≈ f₀/Q',
     'out': '<b>Q</b> = √(200 × 1)/0.3 ≈ 47 · ความกว้าง ≈ 2.251/47 ≈ 0.048 Hz' },
   { 'el': ['#sidePanel .base-block[data-base="B"] .readout', '#view3d'], 'prep': "setMode('manual'); __sl('F0', 5); __fd(0.5); resetSim(); __run(30); setView('iso')",
     'title': 'แรงขับมาก แต่ความถี่ไม่ตรง',
     'text': 'ตั้ง <b>F₀ = 5 N</b> (มากกว่าเดิม 5 เท่า) แต่ <b>f_drive = 0.5 Hz</b> ห่างจาก f₀ · ดู <b>A_steady</b> และ A_current · แอมพลิจูดยังเล็กมาก แสดงว่าการสั่นพ้องต้องการ<b>ความถี่ตรง</b> ไม่ใช่แรงมาก<br>⑧ <b>A = F₀ / √((k − mω²)² + (bω)²)</b>',
     'out': 'F₀ = 5 N, f = 0.5 Hz: <b>A_steady</b> ≈ 0.026 m · เทียบ F₀ = 1 N ที่ f₀: <b>A</b> ≈ 0.236 m' },
   { 'el': ['.preset-grid', '#caseResonanceResult'], 'prep': "__sl('F0', 1); __base('C'); loadCase('swing', document.querySelector('[data-case=\"swing\"]')); document.getElementById('sl-fdC').value = 0.50; syncCfreq(); __run(20); recordCaseResonance()",
     'title': 'ฐาน C: กรณีศึกษา หาความถี่สั่นพ้อง',
     'text': 'เลือก <b>ฐาน C</b> กดกรณี เช่น <b>🎡 ชิงช้า</b> (โปรแกรมตั้ง k, m, b, F₀ ของระบบให้ และตั้ง f_drive ห่างจากยอดไว้) · กด ▶ เริ่ม เลื่อน <b>f_drive</b> จนการแกว่งในภาพมากที่สุด แล้วกด <b>📍 บันทึก resonance</b> · ทำให้ครบ 6 กรณี และเลือกว่าเป็น "ใช้ประโยชน์" หรือ "ต้องป้องกัน"',
     'out': 'ชิงช้า (k = 50 N/m, m = 5 kg): <b>f₀</b> = (1/2π)√(50/5) ≈ 0.503 Hz · ผลักตรงจังหวะ ใช้แรงน้อยแต่แกว่งสูง' },
  ],
 }
