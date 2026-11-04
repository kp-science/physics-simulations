# -*- coding: utf-8 -*-
# Lab 40 การซ้อนทับของคลื่นดล — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# ทุกตัวเลข = แบบจำลองของแลปเอง (y1At/y2At/ySumAt · loadPreset · recordRow) · หยุดนาฬิกาแลป (__kpSpeed.set(0)) แล้วเลื่อนเวลาด้วย seekTime
# ค่า "y รวม (วัด)" = ค่าที่อ่านจากป้ายของหมุดวัดสีเหลือง (ySumAt ที่ตำแหน่งหมุด) เหมือนนักเรียนอ่านจากจอ
GUIDE = {
  'title': 'ตรวจสอบหลักการซ้อนทับของคลื่นดล y = y₁ + y₂',
  'setup': r"""
    if (window.__kpSpeed) __kpSpeed.set(0);
    window.__q = s => document.querySelector(s);
    window.__pause = () => { if (STATE.isPlaying) togglePlay(); };
    window.__pin = x => { STATE.probeX = x; STATE.probeOn = true; __q('#showProbe').checked = true; draw(); };
    window.__rec = () => { recordRow(); const r = records[records.length - 1]; r.measured = ySumAt(STATE.probeX, STATE.t).toFixed(2); renderTable(); };
    window.__low = () => setTimeout(() => { const w = __q('.data-panel'); if (w) w.scrollTop = 1e4; }, 300);
  """,
  'steps': [
   { 'el': ['.preset-row', '.canvas-wrap'], 'prep': "setRecordMode('manual'); records.length = 0; renderTable(); __q('#onlySum').checked = false; loadPreset('crest-crest'); __pin(10); scrollTo(0,0)",
     'title': 'ตั้งคลื่นดล 2 ลูก: ยอด + ยอด',
     'text': 'เลือก <b>บันทึกเอง</b> และ <b>▶ ปล่อยอัตโนมัติ</b> แล้วกด preset <b>🟠 ยอด+ยอด</b> · เชือกยาว 20 m คลื่นดล 1 (ส้ม) เริ่มที่ x = 4 m เคลื่อนที่ไปทางขวา คลื่นดล 2 (ฟ้า) เริ่มที่ x = 16 m เคลื่อนที่ไปทางซ้าย',
     'out': 'A₁ = A₂ = +3 cm · ความกว้าง 2 m · v₁ = +2 m/s · v₂ = −2 m/s' },
   { 'el': ['#playBtn', '.canvas-wrap'], 'prep': "togglePlay(); seekTime(1.5)",
     'title': 'ปล่อยคลื่นดลให้เคลื่อนที่เข้าหากัน',
     'text': 'กด <b>▶ เริ่ม</b> คลื่นดลทั้งสองเคลื่อนที่เข้าหากันด้วยอัตราเร็วเท่ากัน · เส้นสีเหลืองหนา = <b>การกระจัดรวม</b>ของเชือกแต่ละจุด<br><small>ทำนายก่อน: ขณะพบกัน ยอดจะสูงเท่าไร</small>',
     'out': 't = 1.50 s · ดลอยู่ที่ x = 7 m และ 13 m' },
   { 'el': ['.scrubber-row', '.canvas-wrap'], 'prep': "__pause(); seekToMeet(); __pin(10)",
     'title': 'ไปที่ "ขณะพบ" แล้วปักหมุดวัด',
     'text': 'กด <b>⏸ หยุด</b> แล้วกด <b>ขณะพบ</b> ที่แถบเวลา (ยอดทั้งสองซ้อนกันพอดี) · <b>คลิกบนเชือกที่ x = 10 m</b> ปักหมุดวัดสีเหลือง · อ่านค่า y ที่ป้ายของหมุด และ y₁, y₂ ในแถบใต้แถบเวลา',
     'out': 't = 3.00 s · x = 10.0 m · <b>y₁</b> = 3.00 cm · <b>y₂</b> = 3.00 cm · ป้ายหมุด y = 6.00 cm' },
   { 'el': ['[onclick="recordRow()"]', '#dataTable'], 'prep': "__rec()",
     'title': 'บันทึกแถว แล้วกรอก y รวม',
     'text': 'กด <b>💾 บันทึกแถวปัจจุบัน</b> โปรแกรมลง t, x, y₁, y₂ ให้ · อ่าน y ที่หมุดเหลืองแล้วพิมพ์ในช่อง <b>y รวม (วัด)</b><br>① โปรแกรมเทียบกับ <b>y₁ + y₂</b> แสดงใน <b>%ผิด</b>',
     'out': '<b>y รวม</b> = 6.00 cm = 3.00 + 3.00 → %ผิด 0.0% · ยอดสูงเป็น <b>2 เท่า</b> (การแทรกสอดแบบเสริม)' },
   { 'el': ['.canvas-wrap', '#dataTable'], 'prep': "seekTime(2.75); __pin(10); __rec()",
     'title': 'วัดขณะดลซ้อนกันบางส่วน',
     'text': 'เลื่อนแถบเวลาไป <b>t = 2.75 s</b> (ดลเพิ่งเริ่มซ้อนกัน) หมุดที่ x = 10 m · บันทึกแถวและกรอก y รวม · ทุกจุดบนเชือก การกระจัดรวมคือผลบวกของการกระจัดจากแต่ละดลที่จุดนั้น',
     'out': '<b>y₁</b> = 1.10 cm · <b>y₂</b> = 1.10 cm → <b>y รวม</b> = 2.21 cm = y₁ + y₂' },
   { 'el': ['.scrubber-row', '.canvas-wrap'], 'prep': "seekTime(STATE.meetTime + 1)",
     'title': 'หลังพ้นกัน',
     'text': 'กด <b>หลังพ้น</b> คลื่นดลทั้งสองเคลื่อนที่ผ่านกันไป และ<b>มีรูปร่างและแอมพลิจูดเหมือนเดิม</b> — ดลไม่ชนกันเหมือนวัตถุ',
     'out': 't = 4.00 s · ดล 1 ที่ x = 12 m · ดล 2 ที่ x = 8 m · A ยังเป็น 3 cm ทั้งสองลูก' },
   { 'el': ['.preset-row', '.canvas-wrap'], 'prep': "loadPreset('crest-trough'); seekToMeet(); __pin(10); __q('#onlySum').checked = true; draw()",
     'title': 'ยอด + ท้อง: ขณะพบกัน',
     'text': 'กด preset <b>🔴 ยอด+ท้อง</b> (A₂ = −3 cm) ติ๊ก <b>แสดงเฉพาะคลื่นรวม</b> แล้วไปที่ <b>ขณะพบ</b> · ขณะนั้นเชือก<b>แบนราบ</b>ทั้งเส้น',
     'out': 'x = 10 m: y₁ = +3.00 · y₂ = −3.00 → <b>y รวม = 0</b> (การแทรกสอดแบบหักล้าง)' },
   { 'el': ['.canvas-wrap', '#dataTable'], 'prep': "__rec(); __q('#onlySum').checked = false; seekTime(STATE.meetTime + 1)",
     'title': 'บันทึก แล้วดูหลังพ้นกัน',
     'text': 'บันทึกแถวและกรอก y รวม = 0 (ช่อง %ผิด แสดงค่าที่ต่างจาก 0 เป็น cm) · เอาติ๊กออกแล้วกด <b>หลังพ้น</b> ทั้งยอดและท้องกลับมาครบ<br><small>ขณะเชือกแบน คลื่นไม่ได้หายไป พลังงานยังอยู่ในรูปความเร็วของเชือก</small>',
     'out': 'แถว 3: y₁ + y₂ = 3.00 + (−3.00) = <b>0.00 cm</b> · หลังพ้นกัน ดลทั้งสองยังสูง 3 cm' },
   { 'el': ['.canvas-wrap', '#dataTable'], 'prep': "loadPreset('different-A'); seekToMeet(); __pin(10); __rec()",
     'title': 'แอมพลิจูดต่างกัน',
     'text': 'กด preset <b>🟡 A ต่าง</b> (ดลสามเหลี่ยม A₁ = +5 cm, A₂ = +2 cm) ไปที่ <b>ขณะพบ</b> ปักหมุดที่ x = 10 m บันทึกและกรอก y รวม',
     'out': '<b>y รวม</b> = 5.00 + 2.00 = <b>7.00 cm</b> · หลังพ้นกันดลใหญ่ไม่ "กิน" ดลเล็ก' },
   { 'el': ['#motionToggle', '.canvas-wrap'], 'prep': "loadPreset('mixed-shape'); setMotionMode('drag'); STATE.dragX1 = 9.6; STATE.dragX2 = 10.4; __pin(10.0)",
     'title': 'รูปร่างต่างกัน: ลากดลด้วยมือ',
     'text': 'กด preset <b>🟣 รูปต่างกัน</b> (สามเหลี่ยม A₁ = 4 cm + สี่เหลี่ยม A₂ = 3 cm) เลือก <b>✋ ลากเอง</b> แล้วจับวงกลมส้ม/ฟ้าลากเข้าหากันให้ซ้อนกันบางส่วน · เส้นรวมเปลี่ยนทันทีตามผลบวกทีละจุด · ปักหมุดที่ x = 10 m',
     'out': 'ดล 1 ที่ x = 9.6 m · ดล 2 ที่ x = 10.4 m · หมุด x = 10 m: y₁ = 2.72 · y₂ = 3.00 → y = 5.72 cm' },
   { 'el': '#dataTable', 'prep': "__rec()",
     'title': 'สรุปผลจากตาราง',
     'text': 'ทุกแถว ค่า <b>y รวม</b> ที่อ่านได้เท่ากับ <b>y₁ + y₂</b> (%ผิด ≈ 0) ไม่ว่าดลจะมีรูปร่างหรือแอมพลิจูดอย่างไร และไม่ว่าจะซ้อนกันเต็มหรือบางส่วน<br>② <b>หลักการซ้อนทับ: y(x, t) = y₁(x, t) + y₂(x, t)</b> (บวกแบบคิดเครื่องหมาย)',
     'out': 'y รวม = 6.00 · 2.21 · 0.00 · 7.00 · 5.72 cm = y₁ + y₂ ทุกแถว · หลังพ้นกันดลแต่ละลูก<b>คงรูปเดิม</b>' },
  ],
 }
