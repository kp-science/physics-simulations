# -*- coding: utf-8 -*-
# Lab 13 การตกอิสระ — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'หาความเร่งโน้มถ่วง g จากลูกเหล็กตกอิสระชนไม้เมตรที่แกว่ง',
  'setup': r"""
    /* ไม่ปล่อยให้แลปวิ่งเอง: __mid(t) = สภาพขณะตก · __hit() = สภาพตอนชน (ค่า t, s จาก computeQuarter()/computeS() ของแลป)
       __read(off) = นักเรียนอ่าน s จากภาพขยาย ละเอียด 0.1 cm (off = อ่านคลาด ±0.1 cm) */
    window.__el = id => document.getElementById(id);
    window.__set = (Lm, d) => { __el('sl-len').value = Lm; __el('vi-len').value = Lm; __el('sl-disp').value = d; __el('vi-disp').value = d; __el('sl-len').dispatchEvent(new Event('input')); };
    window.__mid = ts => { resetSim(); animTime = ts; __el('playBtn').textContent = '⏸ หยุด'; __el('playBtn').classList.add('playing'); draw(); };
    window.__hit = () => { resetSim(); animTime = computeQuarter(); collided = true; measuredT = computeQuarter(); measuredS = computeS(); updateMeasurementDisplay(); __el('in-t').value = measuredT.toFixed(3); drawMagnifier(); __el('playBtn').textContent = '▶ ทดลองอีกครั้ง'; draw(); };
    window.__read = off => { __el('in-s').value = (Math.round(computeS() * 1000) / 10 + off).toFixed(1); };
    window.__trial = (Lm, d, off) => { __set(Lm, d); __hit(); __read(off); manualCalcAndSave(); };
  """,
  'steps': [
   { 'el': '#view3d', 'prep': "setMode('manual'); trials.length = 0; renderTrials(); setPlanet(9.80, document.querySelectorAll('.planet-btn')[0]); __set(1.00, 20); setView('iso'); scrollTo(0,0)",
     'title': 'ดูอุปกรณ์',
     'text': '<b>ไม้เมตร</b>แขวนที่ปลายบนด้วยตะปู (จุดหมุน) ดึงปลายล่างออกไปด้านข้างระยะ d · <b>ลูกเหล็ก</b>วางข้างขอบไม้ที่ระดับจุดหมุน (ขีด 0 ของสเกลบนไม้อยู่ที่ระดับนี้) · เมื่อปล่อยพร้อมกัน ลูกเหล็ก<b>ตกอิสระ</b> ส่วนไม้แกว่งกลับมาแนวดิ่ง แล้วไม้ชนลูกเหล็กทิ้ง<b>รอยดำ</b>ไว้บนขอบไม้<br><small>เวลาที่ไม้แกว่งจากจุดปล่อยถึงแนวดิ่ง = ¼ คาบของไม้ = เวลาที่ลูกเหล็กตก</small>' },
   { 'el': ['.planet-btn.active', '#vi-len', '#vi-disp'],
     'title': 'ตั้งค่าการทดลอง',
     'text': 'กด <b>🌍 โลก</b> (g ที่ตั้งไว้ = 9.80 m/s² ใช้เทียบผล) · ตั้ง <b>ความยาวไม้ L = 1.00 m</b> · <b>ระยะดึง d = 20 cm</b><br><small>ลากปลายไม้ในภาพ 3D เพื่อตั้งระยะดึงได้เช่นกัน</small>',
     'out': 'L = 1.00 m · d = 20 cm' },
   { 'el': '#mode-manual-btn',
     'title': 'เลือกโหมดบันทึกเอง',
     'text': 'เลือก <b>📝 บันทึกเอง</b> โปรแกรมให้เวลา t เอง แต่นักเรียนต้อง<b>อ่านระยะตก s</b> จากภาพขยายของไม้เมตรเอง' },
   { 'el': ['#playBtn', '#view3d'], 'prep': "__mid(0.22); setView('front')",
     'title': 'กดปล่อย',
     'text': 'กด <b>▶ ปล่อย</b> ลูกเหล็กเริ่มตก และไม้เริ่มแกว่งกลับพร้อมกัน · นาฬิกาจับเวลาบนโต๊ะเริ่มเดิน<br><small>ลด ⏱ ความเร็ว ใต้ภาพเพื่อดูช้า ๆ (ค่าที่วัดไม่เปลี่ยน)</small>' },
   { 'el': ['#view3d', '#disp-t'], 'prep': "__hit(); setView('rd')",
     'title': 'ไม้ชนลูกเหล็ก → ได้เวลาตก t',
     'text': 'เมื่อไม้ถึงแนวดิ่ง ไม้ชนลูกเหล็กพอดี ภาพหยุดเอง · กด <b>🔍 ซูมอ่านค่า s</b> ดูรอยดำบนขอบไม้ · เวลาตก t ขึ้นในช่อง <b>⏱ เวลาที่ลูกบอลตก</b> และช่อง t ด้านล่างให้เอง<br><small>t = ¼ คาบของไม้ที่แกว่ง = (π/2)√(2L/3g)</small>',
     'out': '<b>t</b> = 0.410 s' },
   { 'el': ['#magCanvas', '#in-t'],
     'title': 'อ่านระยะตก s จากภาพขยาย',
     'text': 'ดู <b>🔍 ภาพขยายตำแหน่งชน</b> อ่านสเกลที่<b>ขอบบนของรอยดำ</b> (ขีดเล็กละ 1 mm) ได้ระยะที่ลูกเหล็กตกจากระดับจุดหมุนถึงจุดชน',
     'out': '<b>s</b> = 82.2 cm' },
   { 'el': ['#in-s', '[onclick="manualCalcAndSave()"]'], 'prep': "__read(0)",
     'title': 'กรอก s แล้วกดคำนวณ',
     'text': 'พิมพ์ s (หน่วย cm) ในช่อง <b>s ระยะตก</b> แล้วกด <b>💾 คำนวณ g และบันทึกลงตาราง</b>' },
   { 'el': ['#calc-result'], 'prep': "manualCalcAndSave()",
     'title': 'โปรแกรมคำนวณ g',
     'text': 'ลูกเหล็กตกจากหยุดนิ่ง s = ½gt² จึงคำนวณ<br>① แปลงหน่วย s = 82.2 cm = 0.822 m<br>② <b>g = 2s / t²</b> = 2(0.822) / (0.410)²<br>③ <b>%error = |g − g<sub>ตั้งไว้</sub>| / g<sub>ตั้งไว้</sub> × 100</b>',
     'out': '<b>g</b> = 9.78 m/s² · %error = 0.2 %' },
   { 'el': '#trial-tbody', 'prep': "__trial(1.00, 20, 0.1); __trial(1.00, 15, -0.1); __trial(1.00, 30, 0)",
     'title': 'ทำซ้ำ และเปลี่ยนระยะดึง d',
     'text': 'กด <b>↺ เริ่มใหม่</b> ก่อนทุกครั้ง · ทำซ้ำที่ d = 20 cm แล้วเปลี่ยน <b>d = 15 cm</b> และ <b>30 cm</b> · แต่ละครั้งอ่าน s ใหม่แล้วบันทึก',
     'out': 'd = 20 · 20 · 15 · 30 cm → t = 0.410 s ทุกครั้ง · s = 82.2 · 82.3 · 82.1 · 82.2 cm → <b>g</b> = 9.78 · 9.79 · 9.77 · 9.78 m/s²' },
   { 'el': ['#trial-tbody', '#trial-tfoot'], 'prep': "__trial(0.80, 20, 0.1); __trial(1.20, 20, -0.1)",
     'title': 'เปลี่ยนความยาวไม้ L',
     'text': 'ตั้ง <b>L = 0.80 m</b> และ <b>1.20 m</b> วัดแบบเดิม · ไม้สั้นแกว่งถึงแนวดิ่งเร็วกว่า ลูกเหล็กจึงตกได้สั้นกว่า แต่ g ที่คำนวณได้ยังเท่าเดิม · แถว <b>ค่าเฉลี่ย</b> ท้ายตารางเฉลี่ย g และ %error ให้',
     'out': 'L = 0.80 m: t = 0.366 s · s = 65.9 cm → g = 9.84 m/s²<br>L = 1.20 m: t = 0.449 s · s = 98.6 cm → g = 9.78 m/s²<br><b>g เฉลี่ย 6 ครั้ง</b> = 9.79 m/s² (%error เฉลี่ย 0.2 %)' },
   { 'el': '#gChart', 'prep': "drawGChart()",
     'title': 'กราฟ g ของแต่ละครั้ง',
     'text': 'จุดแต่ละจุด = g จาก 1 ครั้ง · เส้นแดง = ค่ามาตรฐาน 9.8 m/s² · ทุกจุดอยู่ใกล้เส้นแดง ไม่ว่าจะเปลี่ยน d หรือ L → <b>g ไม่ขึ้นกับระยะดึงและความยาวไม้</b> ค่าที่ต่างกันเล็กน้อยมาจากการอ่าน s และการปัดเวลา t',
     'out': '<b>g ≈ 9.79 m/s²</b> (ค่ามาตรฐาน 9.80 m/s²)' },
   { 'el': ['.planet-btn.active', '#disp-t'], 'prep': "__set(1.00, 20); setPlanet(1.62, document.querySelectorAll('.planet-btn')[1]); __hit(); setView('iso')",
     'title': 'ทดลองเพิ่ม: บนดวงจันทร์',
     'text': 'กด <b>🌙 ดวงจันทร์</b> (L = 1.00 m) แล้วปล่อยใหม่ · ทุกอย่างช้าลง เวลาตกนานขึ้นมาก แต่รอยดำอยู่ที่ระยะเดิม เพราะทั้งไม้และลูกเหล็กช้าลงด้วยอัตราเดียวกัน · คำนวณ g = 2s/t² แบบเดิม<br><small>ถ้าจะบันทึกลงตาราง ให้ 🗑 ล้างทั้งหมดก่อน ค่าเฉลี่ยจะได้ไม่ปนกับของโลก</small>',
     'out': '<b>t</b> = 1.008 s · <b>s</b> = 82.2 cm → <b>g</b> = 2(0.822)/(1.008)² ≈ 1.62 m/s²' },
  ],
}
