# -*- coding: utf-8 -*-
# Lab 7 ภาพถ่ายสโตรโบสโคป — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ภาพแฟลช = แบบจำลองของแลป (currentX: x = v₀t + ½at² · แฟลชทุก 1/f s) เดินด้วยก้าว 1/60 s แบบ loop() ของแลป
# การวัด = handleClick() ของแลปเอง (คลิกบนไม้บรรทัดใต้ภาพ → ดูดเข้าภาพแฟลชที่ใกล้ที่สุด) · t = ลำดับภาพ × 1/f
GUIDE = {
  'title': 'วิเคราะห์การเคลื่อนที่จากภาพถ่ายสโตรบ: ความเร็วและความเร่ง',
  'setup': r"""
    window.__sl = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('input')); };
    window.__motion = m => { const s = document.getElementById('motionType'); s.value = m; s.dispatchEvent(new Event('change')); };
    window.__run = T => { while (S.t < T - 1e-9) { const dt = Math.min(1 / 60, T - S.t); S.t += dt; S.x_real = currentX(S.t); const Tf = 1 / effectiveFlashRate();
        while (S.lastFlashT + Tf <= S.t) { S.lastFlashT += Tf; const xr = currentX(S.lastFlashT); if (xr <= S.trackMeters + 0.001) captureStrobe(S.lastFlashT, xr); } }
      document.getElementById('timeVal').textContent = S.t.toFixed(2); draw(); };
    window.__play = () => { if (!S.isPlaying) togglePlay(); S.speed = 0; };
    window.__stop = () => { stopPlay(); S.speed = 1; };
    window.__meas = n => { for (let i = S.measurements.length; i < Math.min(n, S.strobes.length); i++) handleClick(xToPx(S.strobes[i].x_real), canvas.height * 0.68 + 16); draw(); };
    /* ไม่ใช้ปุ่มขยายภาพถ่าย (+): ในแลปทำให้กล่องภาพขยายตามแคนวาสวนไม่หยุด (บั๊ก รายงานแล้ว) */
    window.__top = () => { document.querySelector('.tbl-wrap').scrollTop = 0; };
  """,
  'steps': [
   { 'el': ['#techGroup', '#row-flash'], 'prep': "setMode('manual'); document.querySelector('input[name=tech][value=xenon]').click(); __sl('sl-flash', 5); resetSim(); setView('iso'); scrollTo(0,0)",
     'title': 'เลือก Xenon Strobe ความถี่แฟลช 5 Hz',
     'text': 'เลือกเทคนิค <b>Xenon Strobe</b> (ไฟแฟลชที่กะพริบสม่ำเสมอ ส่องรถในห้องมืด) แล้วตั้ง <b>Flash rate = 5 Hz</b> · กล้องเปิดชัตเตอร์ค้างไว้ ทุกครั้งที่แฟลชสว่าง ฟิล์มแผ่นเดียวกันจะบันทึกภาพรถ 1 ภาพ',
     'out': 'ช่วงเวลาระหว่างภาพ <b>Δt = 1/f</b> = 1/5 = <b>0.2 s</b>' },
   { 'el': ['.select-row:has(#motionType)', '.sl-row:has(#sl-v0)', '#view3d'], 'prep': "__motion('const'); __sl('sl-v0', 0.30); resetSim(); setView('iso')",
     'title': 'ตั้งรถให้วิ่งด้วยความเร็วคงที่',
     'text': 'ประเภทการเคลื่อนที่ <b>ความเร็วคงที่</b> · ตั้ง <b>v₀ = 0.30 m/s</b> · รถบูลโดเซอร์วิ่งบนโต๊ะหน้าผ้าดำ มี<b>ไม้เมตร</b>วางขนานแนวรถไว้เทียบระยะ',
     'out': 'v₀ = 0.30 m/s · a = 0' },
   { 'el': ['.main-grid > div:first-child > .panel:nth-child(3)', '#view3d'], 'prep': "__sl('sl-dist', 1.4); setView('cam')",
     'title': 'ตั้งกล้องให้ถ่ายภาพได้พอดี',
     'text': 'กด <b>📷 กล้อง · จาน</b> ดูกล้องบนขาตั้ง · ระยะกล้อง–วัตถุ <b>1.4 m</b> (ลากกล้องเข้า-ออกได้) · Xenon ใช้ <b>Film selector 3000</b> · ป้าย Exposure บนภาพถ่ายต้องเป็น <b>Good ✓</b><br><small>ใกล้เกินไปภาพสว่างจ้า ไกลเกินไปภาพมืดและรถเล็ก</small>',
     'out': 'Exposure: Good ✓ (ระยะ 1.4 m · Film 3000)' },
   { 'el': ['#playBtn', '#view3d'], 'prep': "resetSim(); __play(); __run(1.25); setView('front')",
     'title': 'กด ▶ เริ่มทดลอง',
     'text': 'กด <b>▶ เริ่มทดลอง</b> รถออกวิ่งจากขีด 0 cm ของไม้เมตร แฟลชสว่างทุก 0.2 s (ภาพถ่ายด้านล่างมีภาพรถเพิ่มทีละภาพ) · นาฬิกามุมขวาบนแถบควบคุมบอกเวลา' },
   { 'el': '#photoWrap', 'prep': "__run(2.05); __stop()",
     'title': 'หยุดเมื่อได้ภาพราว 10 ภาพ แล้วดูภาพถ่าย',
     'text': 'กด <b>⏸ หยุด</b> เมื่อเวลาเลย 2 s · ภาพถ่ายสโตรบ (ฟิล์มแผ่นเดียว) มีภาพรถหลายภาพเรียงกัน ภาพที่อยู่ติดกันห่างกันในเวลา 0.2 s เท่ากันทุกคู่ · สังเกตว่า<b>ระยะห่างระหว่างภาพเท่ากัน</b>',
     'out': 'ได้ภาพรถ <b>11 ภาพ</b> (t = 0 – 2.0 s)' },
   { 'el': '#photoWrap', 'prep': "__meas(4)",
     'title': 'วัดตำแหน่งภาพรถทีละภาพ',
     'text': '<b>คลิกบนไม้บรรทัดใต้ภาพ</b>ตรงกับภาพรถทีละภาพ จากซ้ายไปขวา โปรแกรมดูดเข้าภาพที่ใกล้ที่สุดและอ่านตำแหน่ง x ให้ · เวลา t ใส่ให้เองตามลำดับภาพ (0, 0.2, 0.4 … s)<br><small>วัดผิดกด ↶ ยกเลิกจุดล่าสุด · ปุ่ม 💡 AI ใบ้ตำแหน่งถัดไป ช่วยได้</small>',
     'out': 'ภาพที่ 1–4: <b>x</b> = 0.00 · 6.00 · 12.00 · 18.00 cm' },
   { 'el': '.data-grid > .panel:first-child', 'prep': "__meas(99); __top()",
     'title': 'วัดครบทุกภาพ → โปรแกรมคำนวณ v และ a',
     'text': 'วัดจนครบ 11 ภาพ ตารางคำนวณต่อเป็นลำดับ<br>① <b>Δx</b> = x ภาพนี้ − x ภาพก่อน<br>② ความเร็วเฉลี่ยในช่วงนั้น <b>v = Δx / Δt</b> = 0.0600 m / 0.2 s<br>③ ความเร่ง <b>a = Δv / Δt</b>',
     'out': '<b>Δx</b> = 6.00 cm ทุกช่วง · <b>v</b> = 0.300 m/s ทุกช่วง · <b>a</b> = 0.000 m/s²' },
   { 'el': ['#chartXT', '#chartVT'], 'prep': "drawCharts()",
     'title': 'กราฟ x–t และ v–t',
     'text': 'กราฟ <b>x–t</b> เป็น<b>เส้นตรง</b> (ความชัน = ความเร็ว) · กราฟ <b>v–t</b> เป็น<b>เส้นระดับ</b> ความเร็วไม่เปลี่ยน → รถเคลื่อนที่ด้วยความเร็วคงตัว<br><small>จุดที่ v = 0 ตอน t = 0 คือแถวแรกซึ่งยังไม่มีค่า v (ต้องใช้ 2 ภาพจึงหา v ได้) ไม่ต้องนำมาพิจารณา</small>',
     'out': 'ความชันของ x–t = 60 cm / 2.0 s = <b>0.30 m/s</b> = v₀' },
   { 'el': ['.select-row:has(#motionType)', '.sl-row:has(#sl-v0)', '.sl-row:has(#sl-a)', '#photoWrap'], 'prep': "__motion('accel'); __sl('sl-v0', 0.10); __sl('sl-a', 0.20); resetSim(); __play(); __run(2.65); __stop(); setView('iso')",
     'title': 'เปลี่ยนเป็นความเร็วเร่ง แล้วถ่ายใหม่',
     'text': 'กด <b>↺ รีเซ็ต</b> เลือก <b>ความเร็วเร่ง (a &gt; 0)</b> ตั้ง <b>v₀ = 0.10 m/s</b> และ <b>a = 0.20 m/s²</b> แล้วเริ่มทดลอง หยุดเมื่อได้ราว 14 ภาพ · ภาพรถ<b>ห่างกันมากขึ้นเรื่อย ๆ</b> เพราะรถเร็วขึ้น ในเวลา 0.2 s เท่ากันจึงไปได้ไกลขึ้น',
     'out': 'ได้ภาพรถ <b>14 ภาพ</b> (t = 0 – 2.6 s) · ระยะระหว่างภาพเพิ่มขึ้น' },
   { 'el': '.data-grid > .panel:first-child', 'prep': "__meas(99); __top()",
     'title': 'วัดตำแหน่งทุกภาพ แล้วอ่านตาราง',
     'text': 'คลิกวัดตำแหน่งครบทุกภาพแบบเดิม · คอลัมน์ <b>Δx</b> เพิ่มขึ้นช่วงละเท่า ๆ กัน (aΔt² = 0.20 × 0.2² m = 0.8 cm) · <b>v</b> เพิ่มขึ้นช่วงละ 0.04 m/s · <b>a</b> คงที่',
     'out': '<b>Δx</b> = 2.40 · 3.20 · 4.00 … 12.00 cm · <b>v</b> = 0.120 → 0.600 m/s · <b>a</b> = 0.200 m/s² ทุกแถว' },
   { 'el': ['#chartXT', '#chartVT'], 'prep': "drawCharts()",
     'title': 'กราฟ x–t โค้ง · v–t เป็นเส้นตรง',
     'text': 'กราฟ <b>x–t</b> เป็น<b>เส้นโค้งพาราโบลา</b> ชันขึ้นเรื่อย ๆ · กราฟ <b>v–t</b> เป็น<b>เส้นตรง</b> ความชัน = ความเร่ง (ไม่นับจุดแรกที่ v = 0 ซึ่งยังไม่มีค่า)<br>④ <b>a = (v<sub>ปลาย</sub> − v<sub>ต้น</sub>) / Δt</b> = (0.600 − 0.120) / (2.6 − 0.2)',
     'out': 'ความชันของ v–t = <b>a ≈ 0.20 m/s²</b> (ตรงกับที่ตั้งไว้)' },
   { 'el': ['#techGroup', '#discCtrls', '#techHint'], 'prep': "document.querySelector('input[name=tech][value=disc]').click(); __sl('sl-slits', 4); __sl('sl-rpm', 150); setView('cam')",
     'title': 'ทางเลือก: จานหมุนมีช่อง (Rotating Disc)',
     'text': 'ถ้าไม่มีไฟแฟลช ใช้<b>จานหมุนมีช่อง</b>หน้ากล้องแทน (ใช้ Film selector 75) · ทุกครั้งที่ช่องหมุนผ่านเลนส์ ฟิล์มรับภาพ 1 ครั้ง<br>⑤ <b>f = จำนวนช่อง × รอบต่อวินาที</b> = 4 × (150/60)',
     'out': '<b>f</b> = 10 Hz → Δt = <b>0.1 s</b>' },
   { 'el': ['.data-grid > .panel:first-child', '#chartVT'], 'prep': "document.querySelector('input[name=tech][value=xenon]').click(); __sl('sl-flash', 5); __motion('accel'); __sl('sl-v0', 0.10); __sl('sl-a', 0.20); resetSim(); __run(2.65); __meas(99); __top(); drawCharts(); setView('iso')",
     'title': 'สรุปผล',
     'text': 'ภาพถ่ายสโตรบบันทึกตำแหน่งของวัตถุทุกช่วงเวลาเท่ากัน Δt = 1/f · <b>ระยะห่างภาพเท่ากัน</b> = ความเร็วคงตัว · <b>ระยะห่างเพิ่มขึ้น</b> = ความเร่ง · <b>ระยะห่างลดลง</b> = ความเร็วลดลง (ลองเลือก หน่วง a &lt; 0) · หา v = Δx/Δt และ a = Δv/Δt ได้จากภาพเดียว',
     'out': 'ความเร็วคงที่: <b>v = 0.30 m/s</b> · ความเร็วเร่ง: <b>a = 0.20 m/s²</b>' },
  ],
 }
