# -*- coding: utf-8 -*-
# Lab 76 กำลังและประสิทธิภาพของมอเตอร์ — วิธีการทดลองแบบมีภาพ · รูปแบบดู _admin/lab_guides.py · ต้นแบบ vpl02-lab-60.py
GUIDE = {
  'title': 'หากำลังขาออก กำลังขาเข้า และประสิทธิภาพของมอเตอร์ยกของ',
  'setup': r"""
    /* หยุดนาฬิกาของแลป แล้วเดินแบบจำลองเอง (tick) · ค่ามอเตอร์ (I₀, R ขดลวด, รัศมีดรัม) สุ่มเป็น const ทุกครั้งที่เปิดแลป
       → ตรึงค่าตัวอย่างไว้เฉพาะ browser ที่ถ่ายภาพ: มวลออกแบบ 0.300 kg · η ออกแบบ 0.34 · v ยก 0.46 m/s (สูตรเดียวกับแลป) */
    simSpeed = 0;
    (() => { const MD = 0.300, ED = 0.34, VL = 0.46, CE = 1 - Math.sqrt(ED), IS = MD*G*VL/(ED*V_REF);
      window.__I0 = CE*IS; window.__RA = CE*V_REF/IS; window.__AE = KT*(IS - __I0)/(G*MD); })();
    const __sub = f => (0, eval)('(' + f.toString().replace(/\bI0\b/g, '__I0').replace(/\bRA\b/g, '__RA').replace(/\bA_EFF\b/g, '__AE') + ')');
    steady = __sub(steady); checkI0 = __sub(checkI0);
    M_OPT = 0; ETA_OPT = 0; for (let mg = 40; mg <= 640; mg++){ const r = steady(mg/1000, V_REF); if (!r.stall && r.eta > ETA_OPT){ ETA_OPT = r.eta; M_OPT = mg; } }
    /* ความกระเพื่อมของแปรงถ่าน/มิเตอร์/นาฬิกาใน runMotor ใช้ลำดับคงที่ */
    window.__seq = [0.62,0.41,0.73,0.35,0.55,0.28,0.66]; window.__si = 0;
    runMotor = (orig => function(){ const R = Math.random; Math.random = () => __seq[(__si++) % __seq.length];
      try { return orig(); } finally { Math.random = R; } })(runMotor);
    window.__vs = v => { vset = v; vsTarget = v; dragged = true; syncSup3D(); syncSet(); };
    window.__end = () => { let n = 0; while (phase === 'run' && n++ < 20000) tick(0.002); for (let i = 0; i < 120; i++) tick(0.01); };
    window.__fill = () => { $('in-y1').value = (sA*10).toFixed(0); $('in-y2').value = (sB*10).toFixed(0); $('in-t').value = runTmeas.toFixed(2);
      $('in-v').value = runShowV.toFixed(2); $('in-i').value = runShowI.toFixed(2); };
    window.__run = m => { clearRun(); sL = S_REST; setMass(m); clearRun(); runMotor(); __end(); __fill(); recordRow(); };
  """,
  'steps': [
   { 'el': '#massBtns', 'prep': "setMode('manual'); resetLab(); rows = []; renderAll(); scrollTo(0,0)",
     'title': 'เลือกโหลด 100 g',
     'text': 'กด <b>100 g</b> (ตุ้มแผ่นละ 50 g) · มอเตอร์กระแสตรงที่ปลายคานด้านบนม้วนเชือกด้วยดรัม ยกโหลดขึ้นในแนวดิ่งด้วยอัตราเร็วคงตัว<br><small>เริ่มจากโหลดเบา แล้วเพิ่มทีละขั้นภายหลัง</small>',
     'out': 'โหลด <b>m</b> = 100 g = 0.100 kg' },
   { 'el': '#view3d', 'prep': "__vs(6.0); setView('kz')",
     'title': 'ตั้งแรงดันเครื่องจ่ายไฟ 6.0 V',
     'text': 'กด <b>🔍 ซูมปุ่มไฟ</b> แล้ว<b>ลากปุ่มสีส้ม</b>บนเครื่องจ่ายไฟให้จอแสดง <b>6.0 V</b> · ใช้แรงดันนี้เท่ากันทุกโหลด เพื่อเปรียบเทียบประสิทธิภาพ',
     'out': 'แรงดันที่ตั้ง = 6.0 V' },
   { 'el': ['#view3d', '#in-y1'], 'prep': "setView('ha'); $('in-y1').value = (sA*10).toFixed(0)",
     'title': 'อ่านตำแหน่งขีดเริ่ม y₁',
     'text': '<b>ลากขีดชี้เขียว</b> (เริ่มจับเวลา) และ<b>ขีดชี้แดง</b> (หยุดจับเวลา) ให้ห่างกันราว 30–50 cm · กด <b>🔍 ซูม y₁</b> อ่านขีดชี้เขียวบนสเกลเสา (ตัวเลข = cm · ขีดเล็ก = 1 mm) แล้วกรอกช่อง <b>② y₁</b> เป็น mm',
     'out': '<b>y₁</b> = 200 mm' },
   { 'el': ['#view3d', '#in-y2'], 'prep': "setView('hb'); $('in-y2').value = (sB*10).toFixed(0)",
     'title': 'อ่านตำแหน่งขีดหยุด y₂',
     'text': 'กด <b>🔍 ซูม y₂</b> อ่านขีดชี้แดง แล้วกรอกช่อง <b>③ y₂</b> · ระยะยก h = y₂ − y₁',
     'out': '<b>y₂</b> = 600 mm → h = 400 mm' },
   { 'el': ['#view3d', '#ab-run'], 'prep': "setView('iso'); runMotor(); { let n = 0; while (phase === 'run' && sL < 42 && n++ < 20000) tick(0.002); for (let i = 0; i < 30; i++) tick(0); }",
     'title': 'กดเดินมอเตอร์',
     'text': 'กด <b>▶ เดินมอเตอร์</b> โหลดถูกยกขึ้น นาฬิกา<b>เริ่มจับเวลาเมื่อผ่านขีดเขียว</b> และ<b>หยุดเมื่อผ่านขีดแดง</b> · มอเตอร์หยุดเองเหนือขีดแดงเล็กน้อย<br><small>มิเตอร์ค้างค่า (HOLD) ไว้หลังมอเตอร์หยุด จึงอ่านทีหลังได้</small>' },
   { 'el': ['#view3d', '#in-t'], 'prep': "__end(); setView('tz'); $('in-t').value = runTmeas.toFixed(2)",
     'title': 'อ่านเวลายก t',
     'text': 'กด <b>🔍 ซูมนาฬิกา</b> อ่านเวลาที่โหลดใช้เคลื่อนจากขีดเขียวถึงขีดแดง (ละเอียด 0.01 s) แล้วกรอกช่อง <b>④ t</b>',
     'out': '<b>t</b> = 0.70 s' },
   { 'el': ['#view3d', '#in-v', '#in-i'], 'prep': "setView('mz'); $('in-v').value = runShowV.toFixed(2); $('in-i').value = runShowI.toFixed(2)",
     'title': 'อ่านโวลต์มิเตอร์และแอมมิเตอร์',
     'text': 'กด <b>🔍 ซูมมิเตอร์</b> อ่านเข็ม<b>โวลต์มิเตอร์</b> (ต่อคร่อมขั้วมอเตอร์ · ขีดเล็ก 0.1 V) และ<b>แอมมิเตอร์</b> (ต่ออนุกรม · ขีดเล็ก 0.02 A) กรอกช่อง <b>⑤ V</b> และ <b>⑥ I</b><br><small>V ที่ขั้วมอเตอร์ต่ำกว่า 6.0 V เล็กน้อย เพราะความต้านทานภายในของเครื่องจ่ายไฟ</small>',
     'out': '<b>V</b> = 5.85 V · <b>I</b> = 0.41 A' },
   { 'el': '#lastRec', 'prep': "recordRow(); setView('iso')",
     'title': 'กดบันทึก → โปรแกรมคำนวณให้',
     'text': 'กด <b>📝 บันทึก</b> ค่าเข้าตาราง และแสดงใน <b>📊 ผลที่บันทึกล่าสุด</b> โปรแกรมคำนวณต่อ:<br>① ระยะยก <b>h = y₂ − y₁</b> = 0.400 m<br>② งาน <b>W = mgh</b> = 0.100 × 9.80 × 0.400 = 0.392 J<br>③ กำลังขาออก <b>P<sub>out</sub> = W/t</b> = 0.392 / 0.70 = 0.560 W<br>④ กำลังขาเข้า <b>P<sub>in</sub> = VI</b> = 5.85 × 0.41 = 2.40 W<br>⑤ ประสิทธิภาพ <b>η = P<sub>out</sub>/P<sub>in</sub> × 100%</b>',
     'out': '<b>W</b> = 0.392 J · <b>P<sub>out</sub></b> = 0.560 W · <b>P<sub>in</sub></b> = 2.398 W · <b>η</b> = 23.3 %' },
   { 'el': '#tableA', 'prep': "[200, 300, 400, 500].forEach(__run); $('tableA').style.maxHeight = 'none'; setView('iso'); renderAll()",
     'title': 'ลดโหลดลง เปลี่ยนโหลด แล้ววัดซ้ำ',
     'text': 'กด <b>↓ ลดโหลดลง</b> เลือกโหลดถัดไป แล้วทำซ้ำที่ <b>6.0 V</b> และช่วง y₁–y₂ เดิม ให้ครบ <b>อย่างน้อย 5 ค่าโหลด</b> (100 – 500 g) · ทำ 2–3 ครั้งต่อโหลดแล้วเฉลี่ยจะแม่นขึ้น<br><small>โหลดมากขึ้น ยกช้าลง และกระแสเพิ่มขึ้น</small>',
     'out': 'm = 100 · 200 · 300 · 400 · 500 g → <b>t</b> = 0.70 · 0.80 · 0.93 · 1.11 · 1.37 s · <b>I</b> = 0.41 · 0.54 · 0.66 · 0.79 · 0.93 A · <b>η</b> = 23.3 · 31.3 · 33.1 · 31.2 · 27.2 %' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('eta')",
     'title': 'กราฟ η – m หาโหลดที่ประสิทธิภาพสูงสุด',
     'text': 'กด <b>📈 η – m</b> เส้น<b>ขึ้นแล้วลง</b> มีจุดสูงสุด (เส้นประเหลือง) · โหลดเบา: กำลังส่วนใหญ่เสียไปกับแรงเสียดทานภายใน · โหลดหนัก: กระแสมาก เสียเป็นความร้อนในขดลวด (I²R) มาก',
     'out': 'η สูงสุดที่โหลด <b>≈ 300 g</b> (η ≈ 33 %)' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('pout')",
     'title': 'กราฟ P_out – m',
     'text': 'กด <b>📈 P<sub>out</sub> – m</b> กำลังขาออก <b>P<sub>out</sub> = mgh/t = mgv</b> เพิ่มขึ้นตามโหลดในช่วงแรก แล้วเพิ่มช้าลงจนเกือบคงที่ เพราะโหลดหนักทำให้มอเตอร์ยกช้าลงมาก',
     'out': '<b>P<sub>out</sub></b> = 0.560 · 0.980 · 1.265 · 1.413 · 1.431 W' },
   { 'el': ['#graphCanvas', '#graphNote'], 'prep': "setGraph('im')",
     'title': 'กราฟ I – m หากระแสขณะไม่มีโหลด I₀',
     'text': 'กด <b>📈 I – m</b> จุดเรียงเป็น<b>เส้นตรง</b> เพราะแรงบิดของมอเตอร์ τ = kI · ต่อเส้นย้อนไปที่ m = 0 → <b>จุดตัดแกน I = I₀</b> คือกระแสที่ใช้เอาชนะแรงเสียดทานภายในมอเตอร์เท่านั้น',
     'out': 'จุดตัดแกน <b>I₀ ≈ 0.279 A</b> · ความชัน ≈ 1.29 A/kg' },
   { 'el': ['#ans-opt', '#ansOptMsg', '#ans-i0', '#ansI0Msg'], 'prep': "{ const eb = etaByLoad(); let b = eb[0]; eb.forEach(e => { if (e.eta > b.eta) b = e; }); $('ans-opt').value = b.m; $('ans-i0').value = fitIm().a.toFixed(3); } checkOpt(); checkI0()",
     'title': 'ตอบปริศนา: โหลดที่ η สูงสุด และ I₀',
     'text': 'กรอกโหลดที่ η สูงสุด (g) และ I₀ (A) ในกรอบ <b>🎯 ตรวจคำตอบ</b> แล้วกดตรวจ · โหลดถูกเมื่อคลาดไม่เกิน 100 g · I₀ ถูกเมื่อคลาดไม่เกิน 10%',
     'out': 'โหลดที่ η สูงสุด ≈ <b>300 g</b> · <b>I₀ ≈ 0.279 A</b> ในภาพตัวอย่าง (ค่ามอเตอร์สุ่มทุกครั้งที่เปิดแลป · โหลดที่ η สูงสุดอยู่ราว 220 – 360 g)' },
   { 'el': '#view3d', 'prep': "clearRun(); sL = S_REST; setMass(300); __vs(10.0); clearRun(); runMotor(); __end(); __fill(); recordRow(); setView('mz')",
     'title': 'เปลี่ยนแรงดันที่โหลดเดิม',
     'text': 'ตั้งโหลด 300 g แล้วเปลี่ยนแรงดันเป็น <b>10.0 V</b> วัดแบบเดิม · เทียบกับแถว 300 g ที่ 6.0 V<br><small>กระแสขึ้นกับแรงบิดที่ต้องใช้ยกโหลด จึงแทบไม่เปลี่ยน แต่แรงดันสูงขึ้นทำให้มอเตอร์หมุนเร็วขึ้น ยกเร็วขึ้น</small>',
     'out': '300 g ที่ 10.0 V: <b>I</b> = 0.66 A (เท่าเดิม) · <b>t</b> = 0.42 s (เดิม 0.93 s) · V = 9.78 V' },
  ],
 }
