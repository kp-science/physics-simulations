# -*- coding: utf-8 -*-
# Lab 34 การเลี้ยวเบนและแทรกสอด — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# λ ของเลเซอร์สุ่มใหม่ทุกครั้งที่บันทึก (400–700 nm) → ตรึงค่าตัวอย่างเฉพาะ browser ที่ถ่ายภาพ ให้ภาพตรงกับข้อความ
# ตำแหน่งแถบมืด/สว่าง = จุดต่ำสุด/สูงสุดของลวดลายที่แลปคำนวณเอง (cacheB/D/C) ที่หัววัดอ่านได้จริง
GUIDE = {
  'title': 'หาความยาวคลื่นแสงจากช่องเดี่ยว สลิตคู่ และเกรตติง',
  'setup': r"""
    window.__tab = k => document.querySelectorAll('.sub-tab')[k];
    window.__setB = (lam, a, L) => { randomLambdaB = lam; slitWidth = a; screenDistB = L; cacheB = null; buildControls(); buildManualRow(); probeY = 0.5; draw(); };
    window.__setD = (lam, d, a, L) => { randomLambdaD = lam; slitSepD = d; slitWidthD = a; screenDistD = L; cacheD = null; buildControls(); buildManualRow(); probeY = 0.5; draw(); };
    window.__setC = (lam, gr, L) => { randomLambdaC = lam; gratingGrooves = gr; screenDistC = L; cacheC = null; buildControls(); buildManualRow(); probeY = 0.5; draw(); };
    /* เลื่อนหัววัดไปจุดต่ำสุด (k = 1 แถบมืดที่ 1) / สูงสุด (แถบสว่างลำดับ k) ที่ฝั่ง +y ของลวดลายในแลป */
    window.__probe = (k, wantMax, thr = 0) => { const p = ensurePattern(), n = p.length, c = Math.round((n - 1) / 2); let cnt = 0;
      for (let i = c - 1; i > 0; i--) { const a = p[i].I, b = p[i - 1].I, q = p[i + 1].I;
        if (wantMax ? (a >= b && a > q && a > thr) : (a <= b && a < q)) { if (++cnt === k) { probeY = i / (n - 1); break; } } }
      draw(); };
    window.__rec = (inId, extra) => { if (extra) extra(); recordManual(); };
  """,
  'steps': [
   { 'el': ['.sub-tabs', '.mode-toggle', '#ctrlPanel'], 'prep': "setMode('manual'); switchExp('B', __tab(1)); manualB = []; trialCountB = 0; __setB(532, 0.05, 1.0); renderManualTable(); setView('iso'); scrollTo(0,0)",
     'title': 'เลือกการทดลอง B ช่องเดี่ยว',
     'text': 'กดแถบ <b>B — Single Slit (ช่องเดี่ยว)</b> และ <b>📝 บันทึกเอง</b> · เลเซอร์ส่องผ่านช่องแคบเดี่ยวไปตกบนฉากที่มีสเกล · โปรแกรม<b>สุ่มความยาวคลื่น λ</b> ให้ (สีลำแสงเป็นคำใบ้) นักเรียนต้องหา λ จากการวัด',
     'out': 'λ = ??? nm (แถบบอกค่า: ลำแสงสีเขียว)' },
   { 'el': ['#ctrlPanel', '#readoutBar', '#view3d'], 'prep': "__setB(532, 0.05, 1.0); setView('iso')",
     'title': 'ตั้งความกว้างช่อง a และระยะฉาก L',
     'text': 'ตั้ง <b>ความกว้างช่อง a</b> = 0.050 mm (50 μm) และ <b>ระยะจอ L</b> = 1.00 m (พิมพ์ในช่องหรือเลื่อนแถบ) · ค่าทั้งสองแสดงที่แถบบอกค่าด้านล่าง · ป้ายในภาพ 3D บอก a ของสลิตและ L ระหว่างสลิตกับฉาก',
     'out': '<b>a</b> = 0.050 mm = 5.0 × 10⁻⁵ m · <b>L</b> = 1.00 m' },
   { 'el': ['#view3d', '.prof-wrap'], 'prep': "setView('screen')",
     'title': 'สังเกตลวดลายบนฉาก',
     'text': 'กด <b>🎯 มองที่ฉาก</b> เห็น<b>แถบสว่างกลางกว้างที่สุดและสว่างที่สุด</b> ขนาบด้วยแถบมืดและแถบสว่างที่จางลงเรื่อย ๆ · กราฟใต้ภาพคือความเข้มแสงตามตำแหน่ง y บนฉาก<br><small>แถบมืดเกิดที่ a sin θ = nλ (n = 1, 2, 3, …)</small>' },
   { 'el': ['#view3d', '#probeInfo'], 'prep': "__probe(1, false); setView('read')",
     'title': 'ลากหัววัดไปที่แถบมืดลำดับที่ 1',
     'text': 'ลาก<b>หัววัด (เส้นเขียว) บนฉาก</b> ออกจากกลางแถบสว่างกลางไปทางขวา จนถึงจุดแรกที่ความเข้มเกือบเป็นศูนย์ = <b>แถบมืดลำดับที่ 1</b> · กด <b>🔍 ซูมอ่านค่า</b> อ่านสเกลบนฉาก หรืออ่านแถบ 📍 Position<br><small>ระยะ y₁ วัดจากกลางแถบสว่างกลาง</small>',
     'out': '<b>y₁</b> = 1.06 cm (Intensity ≈ 0)' },
   { 'el': '#manualRow', 'prep': "draw()",
     'title': 'บันทึกค่า y₁',
     'text': 'ช่อง <b>y₁ (cm)</b> ขึ้นค่าตามหัววัดให้ (แก้เองได้) · ตรวจว่าตรงกับที่อ่านจากสเกล แล้วกด <b>📝 บันทึก</b>' },
   { 'el': '#manualTable', 'prep': "recordManual(); randomLambdaB = 650; cacheB = null; buildManualRow(); draw()",
     'title': 'โปรแกรมคำนวณ λ',
     'text': 'ตารางเพิ่มแถวใหม่ โปรแกรมคำนวณ:<br>① มุมเล็ก sin θ ≈ y₁/L จาก <b>a sin θ = λ</b> (แถบมืดที่ 1)<br>② <b>λ = y₁ a / L</b> = (1.06 × 10⁻² m)(5.0 × 10⁻⁵ m) / 1.00 m<br>③ เทียบกับ <b>λ จริง</b> ที่โปรแกรมเฉลยหลังบันทึก → %Error<br><small>บันทึกแล้วโปรแกรมสุ่ม λ ใหม่ให้ทันที (สีลำแสงเปลี่ยน)</small>',
     'out': '<b>λ</b> ≈ 530 nm (λ จริง 532 nm · คลาด 0.4%)' },
   { 'el': '#manualData', 'prep': "__setB(650, 0.10, 1.5); __probe(1, false); recordManual(); __setB(589, 0.08, 2.0); __probe(1, false); recordManual(); __setB(450, 0.05, 1.2); __probe(1, false); setView('screen')",
     'title': 'วัดซ้ำ — เปลี่ยน λ, a และ L',
     'text': 'วัดแถบมืดที่ 1 กับ λ ใหม่ที่สุ่มได้ และลองเปลี่ยน a และ L · สังเกต: <b>a แคบลง แถบกว้างขึ้น</b> · <b>L ไกลขึ้น แถบกว้างขึ้น</b> · <b>λ ยาว (แดง) แถบกว้างกว่า λ สั้น (ม่วง)</b>',
     'out': 'a = 0.10 mm, L = 1.5 m: y₁ = 0.97 cm → λ ≈ 647 nm (จริง 650)<br>a = 0.08 mm, L = 2.0 m: y₁ = 1.47 cm → λ ≈ 588 nm (จริง 589) · คลาดไม่เกิน ~1%' },
   { 'el': ['#ctrlPanel', '#view3d'], 'prep': "switchExp('D', __tab(2)); manualD = []; trialCountD = 0; __setD(610, 0.25, 0.05, 1.0); renderManualTable(); setView('screen')",
     'title': 'การทดลอง C สลิตคู่',
     'text': 'กดแถบ <b>C — Double Slit (สลิตคู่)</b> ตั้ง <b>ระยะห่างช่อง d</b> = 0.25 mm · ความกว้างช่อง a = 0.050 mm · <b>L</b> = 1.00 m · บนฉากเห็น<b>แถบสว่าง-มืดถี่ ๆ ห่างเท่ากัน</b> (การแทรกสอด) อยู่ใต้ลวดลายช่องเดี่ยวกว้าง ๆ<br><small>แถบสว่างเกิดที่ d sin θ = nλ (n = 0, 1, 2, …)</small>',
     'out': '<b>d</b> = 0.25 mm = 2.5 × 10⁻⁴ m · L = 1.00 m' },
   { 'el': ['#view3d', '#manualRow'], 'prep': "__probe(3, true); document.getElementById('mi-nD').value = 3; setView('read')",
     'title': 'วัดระยะถึงแถบสว่างลำดับที่ 3',
     'text': 'นับแถบสว่างจากแถบกลาง (n = 0) ไปทางขวา ลากหัววัดไปที่<b>กึ่งกลางแถบสว่างลำดับที่ 3</b> (ความเข้มสูงสุดของแถบนั้น) · ใส่ <b>n = 3</b> ช่อง y (cm) ขึ้นค่าให้<br><small>วัดถึงแถบลำดับสูงแล้วหารด้วย n ลดความคลาดเคลื่อนจากการอ่าน</small>',
     'out': '<b>n</b> = 3 · <b>y</b> = 0.73 cm' },
   { 'el': '#manualTable', 'prep': "recordManual(); __setD(470, 0.25, 0.05, 1.0); __probe(4, true); document.getElementById('mi-nD').value = 4; recordManual(); __setD(470, 0.25, 0.05, 1.0); setView('screen')",
     'title': 'บันทึก → λ จากสลิตคู่',
     'text': 'กด <b>📝 บันทึก</b> โปรแกรมคำนวณ<br>④ <b>λ = y d / (n L)</b> = (0.73 × 10⁻² m)(2.5 × 10⁻⁴ m) / (3 × 1.00 m)<br>ทำซ้ำกับ λ ใหม่ที่สุ่มได้ (แถวที่ 2 วัดแถบสว่างลำดับที่ 4)',
     'out': 'แถว 1: <b>λ</b> ≈ 608 nm (จริง 610 nm) · แถว 2: n = 4, y = 0.74 cm → λ ≈ 463 nm (จริง 470 nm · คลาด 1.6%)' },
   { 'el': ['#ctrlPanel', '#view3d'], 'prep': "switchExp('C', __tab(3)); manualCLaser = []; trialCountC = 0; gratingLightSource = 'laser'; whiteLightC = false; __setC(610, 5276, 1.0); renderManualTable(); setView('screen')",
     'title': 'การทดลอง D เกรตติง',
     'text': 'กดแถบ <b>D — Grating (เกรตติง)</b> เลือกเกรตติง <b>5,276 gr/cm</b> แหล่งกำเนิด <b>🔴 เลเซอร์</b> L = 1.00 m · แถบสว่าง<b>คมชัด</b>ทั้งสองข้าง และ<b>อยู่ห่างแถบกลางมาก</b> เพราะเกรตติงเส้นถี่เลี้ยวเบนแสงเป็นมุมใหญ่<br>⑤ ระยะระหว่างช่อง <b>d = 1 / (จำนวนเส้นต่อ cm)</b> = 1/5276 cm',
     'out': '<b>d</b> = 1.895 × 10⁻⁶ m (1.895 μm)' },
   { 'el': ['#view3d', '#manualRow'], 'prep': "__probe(1, true, 0.5); document.getElementById('mi-nC').value = 1; setView('read')",
     'title': 'วัดระยะถึงแถบสว่างลำดับที่ 1',
     'text': 'ลากหัววัดไปที่<b>แถบสว่างลำดับที่ m = 1</b> (นับจากแถบกลาง m = 0) ใส่ <b>m = 1</b> ช่อง y ขึ้นค่าให้<br><small>มุม θ ราว 19° ไม่ใช่มุมเล็ก → ตำแหน่งบนฉาก y = L tan θ ใช้ y ≈ mλL/d ไม่ได้</small>',
     'out': '<b>m</b> = 1 · <b>y</b> = 33.97 cm' },
   { 'el': '#manualTable', 'prep': "recordManual(); setView('screen')",
     'title': 'บันทึก → λ จากเกรตติง และสรุปผล',
     'text': 'กด <b>📝 บันทึก</b> โปรแกรมคำนวณต่อเป็นลำดับ<br>⑥ <b>sin θ = y / √(y² + L²)</b> = 0.3397 / √(0.3397² + 1.00²) = 0.3216<br>⑦ <b>λ = d sin θ / m</b> = (1.895 × 10⁻⁶ m)(0.3216) / 1<br>เทียบทุกตาราง: λ ที่คำนวณจากการวัดตรงกับ λ จริง แสดงว่าตำแหน่งแถบมืด/สว่างเป็นไปตาม a sin θ = nλ และ d sin θ = nλ<br><small>เกรตติงมีช่องจำนวนมาก แถบสว่างจึงคมชัด วัดตำแหน่งได้แม่นที่สุด · ถ้าใช้สูตรมุมเล็ก λ = yd/(mL) จะได้ราว 644 nm คลาดถึง 6% · ดาวน์โหลดเป็น 📥 Export CSV ได้</small>',
     'out': '<b>λ</b> = 609.6 nm (จริง 610 nm · คลาด 0.06%) · ทุกวิธีได้ λ คลาดจากค่าจริงไม่เกิน ~2%' },
  ],
 }
