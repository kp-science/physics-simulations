# -*- coding: utf-8 -*-
# Lab 30 คลื่นบนสปริงขด — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ทุกตัวเลข = แบบจำลองของแลปเอง (updateWave: มวล 200 ก้อน · v = √(T/μ) · ตามยาวเร็วกว่า 1.2 เท่า)
# หยุดนาฬิกาแลป (__kpSpeed.set(0)) แล้วเดินแบบจำลองเอง · ตำแหน่งเส้นเขียว/แดงมาจาก toggleStopwatch() ของแลป
GUIDE = {
  'title': 'วัดอัตราเร็วของพัลส์บนสปริง · การสะท้อน · คลื่นนิ่ง',
  'setup': r"""
    if (window.__kpSpeed) { __kpSpeed.set(0); const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    window.__q = id => document.getElementById(id);
    window.__sl = (id, v) => { const s = __q(id); s.value = v; s.dispatchEvent(new Event('input')); };
    window.__fin = () => { updateStopwatch(); updateReadout(); draw(); };
    window.__adv = s => { const t1 = simTime + s; let k = 0; while (simTime < t1 && k++ < 20000) updateWave(0.002); __fin(); };
    /* เดินจนยอดพัลส์ถึงตำแหน่ง x (m) */
    window.__toPeak = x => { let k = 0; while (findPulsePeakM() < x - 1e-9 && k++ < 4000) updateWave(0.002); __fin(); };
    window.__mode = m => setExpMode(m, [...document.querySelectorAll('#exp-modes button')].find(b => b.getAttribute('onclick').includes("'" + m + "'")));
    window.__type = t => setPulseType(t, [...document.querySelectorAll('#pulse-types button')].find(b => b.getAttribute('onclick').includes("'" + t + "'")));
    window.__end = t => setEndType(t, [...document.querySelectorAll('#end-types button')].find(b => b.getAttribute('onclick').includes("'" + t + "'")));
    /* 1 trial: ส่งพัลส์ · เริ่มจับเวลาที่ 0.50 m · หยุดที่ 1.50 m · อ่าน x₁ x₂ · บันทึก */
    /* ระยะระหว่างบัพ: เดินแบบจำลอง 2 คาบ เก็บแอมพลิจูดสูงสุดของแต่ละขด แล้วหาจุดต่ำสุด (บัพ) ครึ่งซ้ายของสปริง เฉลี่ยระยะห่าง */
    window.__nodeX = () => { const env = new Float64Array(N), t1 = simTime + 2 / drivingFreq; let k = 0;
      while (simTime < t1 && k++ < 20000) { updateWave(0.002); for (let i = 0; i < N; i++) env[i] = Math.max(env[i], Math.abs(disp[i])); }
      const mins = []; for (let i = 3; i < N / 2; i++) if (env[i] <= env[i - 1] && env[i] < env[i + 1] && env[i] <= env[i - 2] && env[i] < env[i + 2]) mins.push(i);
      __fin(); return { X: (mins[mins.length - 1] - mins[0]) / (mins.length - 1) / (N - 1) * springLength, n: mins.length - 1, a: mins[0] / (N - 1) * springLength, b: mins[mins.length - 1] / (N - 1) * springLength }; };
    window.__sw = f => { __sl('sl-freq', f); __q('vi-freq').value = f; resetSim(); togglePlay(); __adv(12); return __nodeX(); };
    window.__trial = () => { resetSim(); sendPulseFromUI(); __toPeak(0.5); toggleStopwatch(); __toPeak(1.5); toggleStopwatch();
      __q('meas-x1').value = markStartM.toFixed(2); __q('meas-x2').value = markEndM.toFixed(2); saveMeasurement(); };
  """,
  'steps': [
   { 'el': ['#canvas-wrap', '#exp-modes'], 'prep': "if (__q('rec-toggle').checked) { __q('rec-toggle').checked = false; toggleRecMode(); } __mode('single'); __type('transverse'); __end('free'); __sl('sl-amp', 40); resetSim(); clearDataChart1(); showRuler = true; __q('ruler-toggle').checked = true; draw(); setView('iso'); scrollTo(0,0)",
     'title': 'เตรียมสปริงบนพื้น',
     'text': 'เลือกโหมด <b>พัลส์เดี่ยว</b> และ <b>📏 วัดค่าเอง</b> · สปริงยาว <b>2.0 m</b> วางบนพื้นเรียบ ปลายซ้ายถือด้วยมือ ปลายขวาผูกด้ายเบา (ปลายอิสระ) · มีเทปวัดวางข้างสปริง และ<b>ริบบิ้น</b>ผูกขดกลางสปริง',
     'out': 'L = 2.0 m · ความตึง T = 5 N' },
   { 'el': ['#pulseBtn', '#canvas-wrap'], 'prep': "sendPulseFromUI(); __toPeak(0.75); setView('pulse')",
     'title': 'ส่งพัลส์ตามขวาง',
     'text': 'เลือกชนิด <b>ตามขวาง</b> แล้วกด <b>➜ ส่งพัลส์</b> (เหมือนสะบัดมือไปด้านข้างแล้วกลับ) · ขดสปริงเคลื่อน<b>ตั้งฉาก</b>กับทิศที่พัลส์เคลื่อนที่ · ริบบิ้นกลางสปริงขยับซ้าย–ขวา แล้วกลับที่เดิม ไม่ได้เคลื่อนไปกับพัลส์',
     'out': 'พัลส์ตามขวาง: อนุภาคสั่นตั้งฉากกับทิศการเคลื่อนที่ของคลื่น' },
   { 'el': ['#sw-btn', '#canvas-wrap'], 'prep': "resetSim(); sendPulseFromUI(); __toPeak(0.5); toggleStopwatch(); __adv(0.35); setView('iso')",
     'title': 'เริ่มจับเวลาเมื่อยอดพัลส์ถึง 0.5 m',
     'text': 'ส่งพัลส์ใหม่ เมื่อ<b>ยอดพัลส์</b>ผ่านขีด <b>0.5 m</b> บนเทปวัด กด <b>▶ เริ่มจับเวลา</b> · ระบบปัก<b>เส้นสีเขียว</b>ที่ยอดพัลส์ตอนกด<br><small>กด 🐢 ให้ภาพช้าลงได้ เวลาที่วัดไม่เปลี่ยน</small>' },
   { 'el': ['#sw-display', '#sw-btn', '#canvas-wrap'], 'prep': "__toPeak(1.5); toggleStopwatch(); __fin()",
     'title': 'หยุดจับเวลาเมื่อยอดพัลส์ถึง 1.5 m',
     'text': 'เมื่อยอดพัลส์ถึงขีด <b>1.5 m</b> กด <b>⏸ หยุดจับเวลา</b> (ก่อนพัลส์ถึงปลายสปริง) · ได้<b>เส้นสีแดง</b> · อ่านเวลาบนนาฬิกา',
     'out': '<b>t</b> = 1.75 s' },
   { 'el': ['#canvas-wrap', '#meas-x1'], 'prep': "setView('x1'); __q('meas-x1').value = markStartM.toFixed(2)",
     'title': 'อ่านตำแหน่ง x₁ (เส้นสีเขียว)',
     'text': 'กด <b>🔍 x₁ เขียว</b> ซูมเทปวัด อ่านตำแหน่งเส้นสีเขียว (ขีดเล็กห่าง 1 cm) แล้วพิมพ์ในช่อง <b>x₁</b> หน่วยเมตร',
     'out': '<b>x₁</b> = 0.50 m' },
   { 'el': ['#canvas-wrap', '#meas-x2'], 'prep': "setView('x2'); __q('meas-x2').value = markEndM.toFixed(2)",
     'title': 'อ่านตำแหน่ง x₂ (เส้นสีแดง)',
     'text': 'กด <b>🔍 x₂ แดง</b> อ่านตำแหน่งเส้นสีแดง แล้วพิมพ์ในช่อง <b>x₂</b>',
     'out': '<b>x₂</b> = 1.51 m' },
   { 'el': '#data-chart1', 'prep': "saveMeasurement(); setView('iso')",
     'title': 'บันทึก → อัตราเร็ว v = d/t',
     'text': 'กด <b>💾 บันทึก</b> ตารางลงค่าในช่อง Trial 1 (Transverse) แล้วคำนวณ<br>① ระยะทาง <b>d = x₂ − x₁</b><br>② อัตราเร็ว <b>v = d / t</b>',
     'out': '<b>d</b> = 1.51 − 0.50 = 1.01 m · <b>t</b> = 1.75 s → <b>v</b> = 1.01/1.75 = 0.58 m/s' },
   { 'el': ['#pulse-types', '#canvas-wrap'], 'prep': "__trial(); __type('longitudinal'); resetSim(); sendPulseFromUI(); __toPeak(0.9); setView('pulse')",
     'title': 'พัลส์ตามยาว (อัด)',
     'text': 'วัดตามขวางซ้ำอีกครั้ง (Trial 2) แล้วเลือก <b>ตามยาว (อัด)</b> กดส่งพัลส์ · เห็น<b>ช่วงที่ขดสปริงอัดแน่น</b>เคลื่อนไปตามสปริง · ริบบิ้นขยับ<b>หน้า–หลังในแนวเดียวกับ</b>ทิศการเคลื่อนที่ของคลื่น<br><small>ตามยาว (ขยาย) = ช่วงที่ขดห่างกันเคลื่อนไป</small>',
     'out': 'พัลส์ตามยาว: อนุภาคสั่นในแนวเดียวกับทิศการเคลื่อนที่ของคลื่น' },
   { 'el': '#data-chart1', 'prep': "__trial(); __trial(); setView('iso')",
     'title': 'วัดอัตราเร็วพัลส์ตามยาว',
     'text': 'จับเวลาพัลส์ตามยาวจาก 0.5 m ถึง 1.5 m แบบเดิม 2 ครั้ง (Trial 3, 4) แล้วเทียบกับตามขวาง',
     'out': 'ตามยาว d = 1.01 m · t = 1.46 s → <b>v ≈ 0.69 m/s</b> · ตามขวาง <b>v ≈ 0.58 m/s</b>' },
   { 'el': 'div:has(> #data-chart1)', 'prep': "__type('transverse'); __sl('sl-amp', 15); __trial(); __trial(); __sl('sl-amp', 70); __trial(); __trial(); __sl('sl-amp', 40); __q('data-chart1').parentElement.scrollLeft = 9999",
     'title': 'เปลี่ยนแอมพลิจูด',
     'text': 'กลับเป็นตามขวาง · ตั้ง <b>แอมพลิจูดเล็ก (15)</b> วัด 2 ครั้ง (Trial 5, 6) แล้ว<b>แอมพลิจูดใหญ่ (70)</b> อีก 2 ครั้ง (Trial 7, 8)',
     'out': 'Small Amp t = 1.75 s → v = 0.58 m/s · Large Amp t = 1.75 s → v = 0.58 m/s → <b>อัตราเร็วไม่ขึ้นกับแอมพลิจูด</b> (ขึ้นกับตัวกลาง)' },
   { 'el': ['#end-types', '#canvas-wrap'], 'prep': "__q('data-chart1').parentElement.scrollLeft = 0; __end('fixed'); resetSim(); sendPulseFromUI(); __adv(5.0); setView('top')",
     'title': 'การสะท้อนที่ปลายตรึง',
     'text': 'เลือกปลายขวา <b>ตรึงแน่น (Fixed)</b> ส่งพัลส์ขึ้นด้านเดียว แล้วดูพัลส์ที่สะท้อนกลับมา',
     'out': 'ปลายตรึง: พัลส์สะท้อน<b>กลับหัว</b> (เฟสเปลี่ยน 180°)' },
   { 'el': ['#end-types', '#canvas-wrap'], 'prep': "__end('free'); resetSim(); sendPulseFromUI(); __adv(5.0); setView('top')",
     'title': 'การสะท้อนที่ปลายอิสระ',
     'text': 'เลือก <b>อิสระ (Free)</b> ส่งพัลส์แบบเดิม แล้วเทียบกับปลายตรึง',
     'out': 'ปลายอิสระ: พัลส์สะท้อน<b>ไม่กลับหัว</b> (ด้านเดียวกับพัลส์ที่ส่งไป)' },
   { 'el': ['#exp-modes', '#canvas-wrap'], 'prep': "__mode('superpos'); __type('transverse'); resetSim(); sendPulseFromUI(); __adv(1.32); setView('pulse')",
     'title': 'การซ้อนทับของพัลส์',
     'text': 'เลือกโหมด <b>ซ้อนทับ</b> กด <b>⇆ ส่งพัลส์ 2 ฝั่ง</b> · ขณะพัลส์ทับกัน การกระจัดรวม = ผลบวกของการกระจัดแต่ละพัลส์ แล้วพัลส์ผ่านกันไปเหมือนเดิม',
     'out': 'ขณะซ้อนกันพอดี แอมพลิจูดรวม ≈ 2 เท่าของพัลส์เดียว' },
   { 'el': ['#sec-density', '#canvas-wrap'], 'prep': "__mode('twospring'); __type('transverse'); __end('absorb'); __sl('sl-dratio', 3); __q('vi-dratio').value = 3; resetSim(); sendPulseFromUI(); __adv(2.0); setView('iso')",
     'title': 'สปริง 2 อันต่อกัน',
     'text': 'เลือกโหมด <b>สปริง 2 อัน</b> ตั้ง <b>μ₂/μ₁ = 3</b> (สปริงขวาหนักกว่า) ส่งพัลส์จากซ้าย · ที่รอยต่อ (เส้นชมพู) พัลส์<b>แยกเป็น 2 ส่วน</b>: ส่วนที่ส่งผ่านไปสปริงหนัก และส่วนที่สะท้อนกลับ<br><small>อัตราเร็วในสปริงหนัก v₂ = v₁√(μ₁/μ₂) วัดได้ด้วยนาฬิกาเส้น 1 / เส้น 2 ใต้ภาพ</small>',
     'out': 'เบา → หนัก: พัลส์สะท้อน<b>กลับหัว</b> · ส่งผ่านช้าลง v₂/v₁ = √(1/3) ≈ 0.58' },
   { 'el': ['#sec-freq', '#canvas-wrap'], 'prep': "__end('free'); __mode('standing'); window.__r1 = __sw(3.2); setView('top')",
     'title': 'คลื่นนิ่ง: สั่นปลายสปริงต่อเนื่อง',
     'text': 'เลือกโหมด <b>คลื่นนิ่ง</b> (ปลายขวาตรึง) ตั้ง <b>f = 3.2 Hz</b> แล้วกด <b>▶ เริ่ม</b> · คลื่นที่ส่งไปซ้อนกับคลื่นสะท้อนเกิดคลื่นนิ่ง มี<b>บัพ</b> (ขดที่แทบไม่สั่น) สลับกับ<b>ปฏิบัพ</b> (ขดที่สั่นมากที่สุด) · กด <b>⬇ มุมบน</b> แล้วอ่านตำแหน่งบัพบนเทปวัด<br>วัดระยะจากบัพแรกถึงบัพที่ 10 แล้วหารด้วย 9 ช่วง ได้ระยะระหว่างบัพที่อยู่ติดกัน X',
     'out': 'บัพที่ 0.10 m → 0.91 m (9 ช่วง) → <b>X</b> = 0.81/9 = 0.090 m' },
   { 'el': '#data-chart2', 'prep': "{ const r2 = __sw(4.0), r3 = __sw(5.0); [[3.2, __r1], [4.0, r2], [5.0, r3]].forEach(([f, r], i) => { __q('f' + (i + 1)).value = f.toFixed(1); __q('x' + (i + 1)).value = r.X.toFixed(3); }); } calcWaveSpeeds(); setView('iso')",
     'title': 'บันทึก F และ X → λ และ v',
     'text': 'กรอก F และ X ในตาราง Speed of Waves · ทำซ้ำที่ <b>4.0 Hz</b> และ <b>5.0 Hz</b> แล้วกด <b>🧮 คำนวณ Speed</b><br>③ ความยาวคลื่น <b>λ = 2X</b><br>④ อัตราเร็ว <b>v = fλ</b>',
     'out': 'X = 0.090 · 0.072 · 0.057 m → λ = 0.18 · 0.14 · 0.11 m → <b>v = fλ ≈ 0.58 m/s</b> ทุกความถี่ เท่ากับอัตราเร็วพัลส์ที่จับเวลาได้' },
  ],
 }
