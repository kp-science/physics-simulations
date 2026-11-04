# -*- coding: utf-8 -*-
# Lab 41 การแทรกสอดของคลื่นน้ำจากแหล่งกำเนิดอาพันธ์ 2 แหล่ง — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
# หยุดนาฬิกาแลป (__kpSpeed.set(0)) · จุด P วางบนแนวบัพ/ปฏิบัพจริงของแลป (|S₁P − S₂P| = (ตัวหารของ getDiv) × λ ที่ระยะ R จาก M)
# แล้วปัดตำแหน่งเป็น 0.1 cm เหมือนนักเรียนแตะบนกระดาษ · ทุกตัวเลขในตาราง = recordExp1/recordExp2 ของแลปเอง
GUIDE = {
  'title': 'หาความยาวคลื่นจากแนวบัพและแนวปฏิบัพ',
  'setup': r"""
    if (window.__kpSpeed) { __kpSpeed.set(0); const b = document.getElementById('spdBtn'); if (b) b.innerHTML = '🐢 ความเร็วปกติ ×1'; }
    window.__q = id => document.getElementById(id);
    window.__sl = (id, v) => { const s = __q(id); s.value = v; s.dispatchEvent(new Event('input')); };
    /* วาง P บนแนวที่ |S₁P − S₂P| = div·λ ห่างจาก M เป็นระยะ R cm · side = +1 ด้านบน (y บวก) / −1 ด้านล่าง */
    window.__on = (div, R, side) => { const { S1, S2, xM } = srcPositions(), D = div * lambdaReal(); let lo = 0, hi = Math.PI / 2, x = 0, y = 0;
      for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; x = xM + R / 100 * Math.cos(m); y = side * R / 100 * Math.sin(m);
        const pd = Math.abs(Math.hypot(x - S1.x, y - S1.y) - Math.hypot(x - S2.x, y - S2.y)); if (pd < D) lo = m; else hi = m; }
      markers = [{ x: Math.round(x * 1000) / 10, y: Math.round((y * 100 + 15) * 10) / 10 }]; updateMeasureDisplay(); draw(); };
    window.__rec1 = (type, n, div, R, side) => { __on(div, R, side); __q('exp1Type').value = type; __q('exp1N').value = n; recordExp1(); };
    window.__rec2 = (type, n, div, R, side) => { __on(div, R, side); __q('exp2Type').value = type; __q('exp2N').value = n;
      __q('exp2Ang').value = (Math.round(Math.abs(parseFloat(__q('thVal').textContent)) * 2) / 2).toFixed(1); recordExp2(); };
  """,
  'steps': [
   { 'el': ['#srcSlitBtn', '#modeManBtn', '#view3d'], 'prep': "setRecMode('manual'); setExpTab(1); setSourceType('slit'); __sl('sl-d', 5); __sl('sl-f', 10); __sl('sl-v', 22); S.records1 = []; S.records2 = []; renderTable1(); renderTable2(); resetSim(); setView('iso'); scrollTo(0,0)",
     'title': 'จัดถาดคลื่นและแผ่นกั้นช่องแคบคู่',
     'text': 'เลือก <b>ช่องแคบคู่</b> · <b>📝 บันทึกเอง</b> · <b>การทดลอง 1 · Path Diff</b> · คลื่นหน้าตรงจากคานจุ่มน้ำเคลื่อนไปผ่านแผ่นกั้นที่มี 2 ช่อง ช่องทั้งสองจึงเป็น<b>แหล่งกำเนิดอาพันธ์</b> S₁ และ S₂ (ความถี่เท่ากัน เฟสตรงกัน) · ภาพคลื่นตกบน<b>กระดาษขาวใต้ถาด</b>ที่มีสเกล cm<br><small>M = จุดกึ่งกลางระหว่าง S₁ กับ S₂</small>' },
   { 'el': ['#sl-d', '#sl-f', '#lamReal'],
     'title': 'ตั้งระยะห่างช่อง d และความถี่ f',
     'text': 'ตั้ง <b>ระยะ d</b> = 5 cm และ <b>ความถี่ f</b> = 10 Hz · อัตราเร็วคลื่นในตัวอย่างนี้ v = 22 cm/s จึงรู้ค่าจริง λ = v/f ไว้เทียบผล<br><small>อยากทดลองแบบไม่รู้คำตอบ กด 🎲 ให้โปรแกรมสุ่ม v (15–35 cm/s) และซ่อนไว้</small>',
     'out': '<b>d</b> = 5.0 cm · <b>f</b> = 10 Hz · λ จริง = 22/10 = <b>2.20 cm</b>' },
   { 'el': ['#playBtn', '#view3d'], 'prep': "if (!S.isPlaying) togglePlay(); setView('top')",
     'title': 'เปิดเครื่องกำเนิดคลื่น ดูรูปแบบการแทรกสอด',
     'text': 'กด <b>▶ เริ่ม</b> แล้วกด <b>🌊 มองผิวน้ำ</b> · หลังช่องแคบ คลื่นวงกลมจาก S₁ และ S₂ ซ้อนทับกัน เห็นเป็น<b>แนวเส้นโค้งแผ่ออก</b>เหมือนรัศมี: แนวที่สันคลื่นกับท้องคลื่นสลับกันแรงที่สุด = <b>แนวปฏิบัพ</b> (เสริมกัน) · แนวที่ผิวน้ำเกือบนิ่ง = <b>แนวบัพ</b> (หักล้างกัน)',
     'out': 'แนวปฏิบัพและแนวบัพเกิดสลับกัน สมมาตรรอบแนวกลาง' },
   { 'el': ['#chkHint', '#view3d'], 'prep': "__q('chkHint').checked = true; toggleHint(); setView('top')",
     'title': 'เรียกชื่อแนวและลำดับ n',
     'text': 'แนวกลาง (ตั้งฉากกับแผ่นกั้นที่ M) เป็นปฏิบัพ <b>A₀</b> · ถัดออกไปทั้งสองข้างเป็นบัพ <b>N₁</b> → ปฏิบัพ <b>A₁</b> → บัพ <b>N₂</b> → ปฏิบัพ <b>A₂</b> … · ติ๊ก <b>แสดง hint แนวบัพ/ปฏิบัพ</b> เพื่อตรวจว่าดูถูก (เส้นทึบเขียว = ปฏิบัพ · เส้นประฟ้า = บัพ)',
     'out': 'ปฏิบัพ: |S₁P − S₂P| = nλ · บัพ: |S₁P − S₂P| = (n − ½)λ' },
   { 'el': ['#view3d', '#probeRead'], 'prep': "setLineType('antinode'); __on(1, 15, -1); setView('read')",
     'title': 'แตะจุด P บนแนวปฏิบัพ A₁',
     'text': 'กด <b>ปฏิบัพ (A)</b> แล้วกด <b>🔍 ซูมอ่านภาพบนกระดาษ</b> · แตะกระดาษตรง<b>แนวปฏิบัพเส้นแรกถัดจากแนวกลาง</b> ได้หมุด P (ลากหมุดปรับละเอียดได้) · โปรแกรมลากเส้น S₁P, S₂P บนกระดาษและอ่านระยะให้',
     'out': '<b>S₁P</b> = 14.04 cm · <b>S₂P</b> = 16.25 cm · <b>|S₁P − S₂P|</b> = 2.21 cm' },
   { 'el': ['#exp1N', '#btnRec1', '#tbl1'], 'prep': "__q('exp1Type').value = 'antinode'; __q('exp1N').value = 1; recordExp1()",
     'title': 'ระบุลำดับ n แล้วบันทึก',
     'text': 'ตั้ง ประเภท = <b>ปฏิบัพ (A)</b> · ลำดับ <b>n = 1</b> แล้วกด <b>➕ บันทึกจุดนี้</b> · ตารางลง S₁P, S₂P, Δr ให้ แล้วคำนวณ<br>① ปฏิบัพ <b>λ = |S₁P − S₂P| / n</b> = 2.21 / 1',
     'out': '<b>λ</b> = 2.211 cm' },
   { 'el': ['#tbl1', '#sum1'], 'prep': "__rec1('antinode', 2, 2, 14, 1); __rec1('node', 1, 0.5, 15, 1); __rec1('node', 2, 1.5, 15, -1); setView('read')",
     'title': 'วัดซ้ำที่แนวอื่น ทั้งปฏิบัพและบัพ',
     'text': 'วางจุด P บนแนวอื่นอีก เช่น <b>A₂</b>, <b>N₁</b>, <b>N₂</b> (คนละข้างของแนวกลางก็ได้) เลือกประเภทและ n ให้ตรงแล้วบันทึกทุกจุด<br>② บัพ <b>λ = |S₁P − S₂P| / (n − ½)</b>',
     'out': 'A₂: Δr = 4.40 → λ = 2.199 · N₁: Δr = 1.09 → λ = 2.176 · N₂: Δr = 3.30 → λ = 2.203 cm' },
   { 'el': '#sum1',
     'title': 'สรุป λ เฉลี่ยของการทดลอง 1',
     'text': 'กล่องสรุปใต้ตารางหา<b>ค่าเฉลี่ย</b>และ SD ของ λ ทุกแถว แล้วเทียบกับ λ จริง = v/f<br>③ <b>%error = |λ<sub>เฉลี่ย</sub> − λ<sub>จริง</sub>| / λ<sub>จริง</sub> × 100</b>',
     'out': '<b>λ<sub>เฉลี่ย</sub></b> ≈ 2.197 cm · λ จริง 2.200 cm · error ≈ 0.1%' },
   { 'el': ['#view3d', '#probeRead2'], 'prep': "setExpTab(2); __q('chkProt').checked = true; toggleProtractor(); __q('exp2Type').value = 'antinode'; __q('exp2N').value = 1; __on(1, 22, 1); setView('read')",
     'title': 'การทดลอง 2: วางไม้โปรแทกเตอร์ แล้ววัดมุม θ',
     'text': 'กด <b>การทดลอง 2 · มุม θ</b> ไม้โปรแทกเตอร์แผ่นใสวางบนกระดาษ จุดศูนย์กลางที่ <b>M</b> แนว 0° = แนวกลาง · แตะ P บนแนว <b>A₁</b> ให้<b>ไกลจาก M</b> (ราว 20 cm ขึ้นไป) อ่านมุมที่เส้น MP ตัดขอบไม้โปรแทกเตอร์',
     'out': '<b>θ</b> ≈ 26.0° (โปรแกรมวัดได้ 26.2°)' },
   { 'el': ['#exp2Ang', '#btnRec2'], 'prep': "__q('exp2Ang').value = '26.0'",
     'title': 'กรอกมุมที่อ่านได้ แล้วบันทึก',
     'text': 'กรอก <b>มุม θ อ่านจากไม้โปรแทกเตอร์</b> = 26.0 · ประเภท ปฏิบัพ (A) · n = 1 แล้วกด <b>➕ บันทึกจุดนี้</b> · โปรแกรมคำนวณจากสูตรเมื่อ P อยู่ไกลมาก (r ≫ d)<br>④ ปฏิบัพ <b>d sin θ = nλ</b> → λ = 5.0 × sin 26.0° / 1',
     'out': 'sin θ = 0.438 → <b>λ</b> = 2.192 cm' },
   { 'el': ['#tbl2', '#sum2'], 'prep': "recordExp2(); __rec2('antinode', 2, 2, 14, 1); __rec2('node', 1, 0.5, 24, 1); __rec2('node', 2, 1.5, 18, 1)",
     'title': 'วัดมุมของแนวอื่น แล้วหาค่าเฉลี่ย',
     'text': 'ทำซ้ำกับแนว A₂, N₁, N₂ · บัพใช้ <b>d sin θ = (n − ½)λ</b> · สังเกตว่ายิ่ง n มาก มุม θ ยิ่งกว้าง',
     'out': 'A₂: θ = 62.0° → λ = 2.207 · N₁: θ = 13.0° → λ = 2.250 · N₂: θ = 41.5° → λ = 2.209 cm · <b>λ<sub>เฉลี่ย</sub></b> = 2.214 cm (error ≈ 0.7%) · มากกว่าวิธีที่ 1 เล็กน้อย เพราะ d sin θ = nλ เป็นสูตรประมาณ' },
   { 'el': ['#sl-f', '#view3d'], 'prep': "__q('chkHint').checked = true; toggleHint(); __sl('sl-f', 15); markers = []; updateMeasureDisplay(); setView('top')",
     'title': 'เพิ่มความถี่ ดูแนวที่เปลี่ยนไป',
     'text': 'เปลี่ยน <b>f</b> จาก 10 เป็น 15 Hz (d เท่าเดิม) · ความยาวคลื่นสั้นลง แนวบัพ/ปฏิบัพจึง<b>ถี่ขึ้น</b> มุมระหว่างแนวแคบลง และมีจำนวนแนวมากขึ้น · ถ้าเพิ่ม d (f เท่าเดิม) ผลก็คล้ายกัน เพราะ sin θ = nλ/d',
     'out': 'λ = 22/15 = <b>1.47 cm</b> · แนว A₁ ทำมุม sin⁻¹(1.47/5.0) ≈ 17° (เดิม 26°)' },
   { 'el': ['#phaseToggle', '#view3d'], 'prep': "__sl('sl-f', 10); setSourceType('point'); setPhase('anti'); setView('top')",
     'title': 'จุดสั่น 2 อัน เฟสตรงข้าม',
     'text': 'เลือก <b>จุดสั่น 2 อัน</b> และ <b>เฟสตรงข้าม</b> (f = 10 Hz) · ตัวจุ่มหนึ่งกดลงขณะอีกตัวยกขึ้น · แนวกลางที่เคยเป็นปฏิบัพกลายเป็น<b>บัพ N₀</b> สูตรสลับกัน: ปฏิบัพ |Δr| = (n − ½)λ · บัพ |Δr| = nλ',
     'out': 'แนวกลาง = <b>บัพ</b> (คลื่นจาก S₁ S₂ มาถึงพร้อมกันแต่เฟสตรงข้าม จึงหักล้างกัน)' },
   { 'el': ['#view3d', '#tbl1'], 'prep': "setSourceType('single'); setExpTab(1); __sl('sl-d', 8); S.records1 = []; renderTable1(); __rec1('node', 1, 0.5, 18, 1); setView('read')",
     'title': 'ช่องแคบเดียว: วัดแถบมืดแรก',
     'text': 'เลือก <b>ช่องแคบเดียว</b> ตั้ง <b>กว้างช่อง a</b> = 8 cm · เกิดการเลี้ยวเบน มีแถบสว่างกลางกว้าง ขนาบด้วยแนวบัพ · แตะ P บน<b>แนวบัพแรก</b> เลือก บัพ (N) n = 1 แล้วบันทึก · S₁ S₂ อยู่กลางครึ่งช่องแต่ละครึ่ง (ห่างกัน a/2)<br>⑤ แถบมืด <b>a sin θ = nλ</b> → <b>λ = |Δr| / (n/2)</b>',
     'out': 'S₁P = 18.66 · S₂P = 17.56 · |Δr| = 1.10 cm → <b>λ</b> = 2.209 cm ≈ ค่าจริง 2.20 cm' },
  ],
 }
