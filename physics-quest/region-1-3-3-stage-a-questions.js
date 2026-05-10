/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.3.3 ที่ราบสูงสองมิติ · เนินสปริง
   Stage A "เนินทำความรู้จัก" · SHM concept · 70 ข้อ
   MCQ + T/F + CHECK · concept-only · ใช้ g = 10 m/s²

   หมวด:
     A1 นิยาม SHM + ตัวอย่าง        (R133S001-010 · 10 ข้อ)
     A2 A · T · f · ω · phase        (R133S011-020 · 10 ข้อ)
     A3 a = −ω²x · restoring ⭐       (R133S021-032 · 12 ข้อ)
     A4 x, v, a ตลอด cycle ⭐         (R133S033-044 · 12 ข้อ)
     A5 SHM ↔ UCM projection         (R133S045-054 · 10 ข้อ)
     A6 Spring + Pendulum T          (R133S055-070 · 16 ข้อ)

   STATUS: COMPLETE — 70/70 ข้อ · 6 หมวด · 5 SVG
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  const F_TAG = ['shm-a'];

  function M(id, statement, choices, correct, hints, figure){
    const arr = choices.map((t,i) => ({key:String.fromCharCode(65+i), text:t}));
    const q = {id, group:'A', type:'mcq', statement, choices:arr, correct, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function TF(id, statement, correct, hints, figure){
    const q = {id, group:'A', type:'tf', statement, correct: correct ? 'T' : 'F', hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function CHK(id, statement, options, correctIdx, hints, figure){
    const items = options.map((t,i) => ({key:String(i+1), text:t}));
    const q = {id, group:'A', type:'check', statement, items, correct: correctIdx.map(String), hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }

  // ─── SVG library ───
  // SHM_SPRING — มวลกับสปริง · 3 ตำแหน่ง (ซ้ายสุด · สมดุล · ขวาสุด)
  const SVG_SPRING = '<svg viewBox="0 0 280 100" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="80" x2="270" y2="80" stroke="#fff" stroke-width="1.2"/><line x1="10" y1="20" x2="10" y2="90" stroke="#fbbf24" stroke-width="2"/><path d="M 10 50 L 20 45 L 25 55 L 30 45 L 35 55 L 40 45 L 45 55 L 50 50 L 70 50" fill="none" stroke="#34d399" stroke-width="1.5"/><rect x="70" y="40" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1"/><text x="40" y="35" fill="#a78bfa" font-size="9">−A</text><line x1="81" y1="65" x2="81" y2="92" stroke="#a78bfa" stroke-width="1" stroke-dasharray="2,2"/><text x="76" y="98" fill="#a78bfa" font-size="9">x=−A</text><path d="M 10 50 L 30 45 L 40 55 L 50 45 L 60 55 L 70 45 L 80 55 L 90 45 L 100 55 L 110 50 L 130 50" fill="none" stroke="#34d399" stroke-width="1.5" opacity="0.5"/><rect x="130" y="40" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1" opacity="0.5"/><line x1="141" y1="65" x2="141" y2="92" stroke="#fbbf24" stroke-width="1" stroke-dasharray="2,2"/><text x="135" y="98" fill="#fbbf24" font-size="9">x=0</text><path d="M 10 50 L 40 45 L 60 55 L 80 45 L 100 55 L 120 45 L 140 55 L 160 45 L 180 50 L 200 50" fill="none" stroke="#34d399" stroke-width="1.5" opacity="0.3"/><rect x="200" y="40" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1" opacity="0.3"/><line x1="211" y1="65" x2="211" y2="92" stroke="#a78bfa" stroke-width="1" stroke-dasharray="2,2"/><text x="207" y="98" fill="#a78bfa" font-size="9">x=+A</text></svg>';

  // SHM_PENDULUM — ลูกตุ้ม + L + θ + arc
  const SVG_PEND = '<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="15" x2="180" y2="15" stroke="#fff" stroke-width="2"/><line x1="100" y1="15" x2="100" y2="140" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3"/><line x1="100" y1="15" x2="60" y2="135" stroke="#34d399" stroke-width="2"/><circle cx="60" cy="135" r="10" fill="#fbbf24" stroke="#fff" stroke-width="1"/><path d="M 100 60 A 50 50 0 0 0 75 50" fill="none" stroke="#a78bfa" stroke-width="1.2"/><text x="78" y="55" fill="#a78bfa" font-size="11">θ</text><text x="115" y="80" fill="#34d399" font-size="11" font-weight="700">L</text><circle cx="100" cy="140" r="3" fill="#fff"/><text x="105" y="155" fill="#fff" font-size="9">สมดุล</text></svg>';

  // SHM_UCM_PROJECTION — วงกลม + จุดบนวง + projection ลงแกน x
  const SVG_PROJ = '<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="90" r="60" fill="none" stroke="#34d399" stroke-width="1.5" stroke-dasharray="3,2"/><circle cx="100" cy="90" r="3" fill="#fbbf24"/><line x1="40" y1="90" x2="160" y2="90" stroke="#fff" stroke-width="1.2"/><text x="165" y="93" fill="#fff" font-size="11">x</text><circle cx="142" cy="60" r="6" fill="#38bdf8" stroke="#fff" stroke-width="1"/><line x1="100" y1="90" x2="142" y2="60" stroke="#a78bfa" stroke-width="1.5"/><line x1="142" y1="60" x2="142" y2="90" stroke="#f87171" stroke-width="1.2" stroke-dasharray="3,2"/><circle cx="142" cy="90" r="6" fill="#fbbf24" stroke="#fff" stroke-width="1"/><text x="148" y="55" fill="#38bdf8" font-size="9">UCM</text><text x="148" y="105" fill="#fbbf24" font-size="9">SHM</text><text x="105" y="85" fill="#a78bfa" font-size="9">A</text><text x="60" y="160" fill="#fff" font-size="9">projection ลงแกน x = SHM</text></svg>';

  // SHM_XT_GRAPH — sinusoidal x vs t
  const SVG_XT = '<svg viewBox="0 0 240 130" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="65" x2="225" y2="65" stroke="#fff" stroke-width="1.2"/><line x1="20" y1="15" x2="20" y2="115" stroke="#fff" stroke-width="1.2"/><polygon points="225,65 218,62 218,68" fill="#fff"/><polygon points="20,8 17,18 23,18" fill="#fff"/><text x="6" y="22" fill="#fbbf24" font-size="10">x</text><text x="220" y="80" fill="#fbbf24" font-size="10">t</text><path d="M 20 65 Q 40 20 60 20 Q 80 20 100 65 Q 120 110 140 110 Q 160 110 180 65 Q 200 20 220 20" fill="none" stroke="#34d399" stroke-width="2"/><line x1="20" y1="20" x2="225" y2="20" stroke="#a78bfa" stroke-width="0.8" stroke-dasharray="2,2"/><line x1="20" y1="110" x2="225" y2="110" stroke="#a78bfa" stroke-width="0.8" stroke-dasharray="2,2"/><text x="0" y="24" fill="#a78bfa" font-size="9">+A</text><text x="0" y="114" fill="#a78bfa" font-size="9">−A</text><line x1="120" y1="65" x2="120" y2="115" stroke="#fbbf24" stroke-width="0.8" stroke-dasharray="2,2"/><text x="105" y="125" fill="#fbbf24" font-size="9">T (1 รอบ)</text></svg>';

  // SHM_VAX — แสดง v, a, F ที่ตำแหน่ง equilibrium vs extreme
  const SVG_VAX = '<svg viewBox="0 0 280 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="100" x2="270" y2="100" stroke="#fff" stroke-width="1.2"/><line x1="10" y1="40" x2="10" y2="110" stroke="#fbbf24" stroke-width="2"/><path d="M 10 70 L 20 65 L 25 75 L 30 65 L 35 75 L 40 65 L 45 75 L 50 70 L 70 70" fill="none" stroke="#34d399" stroke-width="1.2"/><rect x="70" y="60" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1"/><text x="60" y="55" fill="#fff" font-size="9">x=+A</text><line x1="81" y1="50" x2="81" y2="35" stroke="#34d399" stroke-width="2"/><polygon points="81,32 78,38 84,38" fill="#34d399"/><text x="60" y="30" fill="#34d399" font-size="9" font-weight="700">a=max</text><line x1="80" y1="68" x2="60" y2="68" stroke="#a78bfa" stroke-width="2"/><polygon points="57,68 63,65 63,71" fill="#a78bfa"/><text x="40" y="64" fill="#a78bfa" font-size="9">F→</text><text x="100" y="75" fill="#fbbf24" font-size="9">v=0</text><path d="M 10 70 L 25 65 L 35 75 L 45 65 L 55 75 L 65 65 L 75 75 L 85 65 L 95 75 L 105 65 L 115 75 L 130 70 L 160 70" fill="none" stroke="#34d399" stroke-width="1.2" opacity="0.4"/><rect x="160" y="60" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1"/><text x="155" y="55" fill="#fff" font-size="9">x=0</text><line x1="180" y1="68" x2="220" y2="68" stroke="#fbbf24" stroke-width="2.5"/><polygon points="223,68 217,65 217,71" fill="#fbbf24"/><text x="190" y="63" fill="#fbbf24" font-size="9" font-weight="700">v=max</text><text x="190" y="92" fill="#a78bfa" font-size="9">a=0</text></svg>';

  const Q = [
    // ════════ A1 — นิยาม SHM + ตัวอย่าง (R133S001-010) ════════
    M('R133S001','การเคลื่อนที่แบบ <strong>"ฮาร์มอนิกอย่างง่าย" (SHM)</strong> หมายถึงการเคลื่อนที่อย่างไร?',
      ['การเคลื่อนที่เป็นวงกลม','การเคลื่อนที่กลับไปกลับมาผ่านตำแหน่งสมดุล โดยมีแรงคืนตัว ∝ ระยะออก','การเคลื่อนที่เป็นเส้นตรงด้วยอัตราเร็วคงที่','การเคลื่อนที่แบบโพรเจกไตล์'],'B',
      ['💡 SHM = oscillation รอบจุดสมดุล','🔍 แรง F ∝ −x (ตรงข้ามกับระยะ)','📐 เป็น "linear restoring force"']),

    M('R133S002','ข้อใดเป็น <strong>ตัวอย่าง SHM</strong>?',
      ['ลูกบาสกระเด้งบนพื้น','สปริงผูกมวลแกว่งไปมา','รถไฟวิ่งบนทางตรง','ลูกฟุตบอลที่กำลังลอย'],'B',
      ['💡 สปริง F = −kx → SHM แท้','🔍 ลูกบาส — แรงไม่ linear (สัมผัสพื้นเฉพาะตอนหนึ่ง)','📐 ลูกตุ้มมุมเล็ก ≈ SHM']),

    TF('R133S003','"ใน SHM ต้องมีแรงคืนตัวที่มีขนาดเป็นสัดส่วนกับระยะออกจากตำแหน่งสมดุล"',true,
      ['💡 F = −kx (linear restoring)','🔍 ถ้าแรงไม่เป็น linear → ไม่ใช่ SHM แท้','📐 เช่น ลูกตุ้มมุมใหญ่ — ไม่ใช่ SHM แล้ว']),

    M('R133S004','<strong>"ตำแหน่งสมดุล"</strong> ของ SHM คือตำแหน่งใด?',
      ['ตำแหน่งที่ความเร็วเป็น 0','ตำแหน่งที่แรงคืนตัวเป็น 0','ตำแหน่งสุดขอบของการเคลื่อนที่','ตำแหน่งที่ amplitude มากที่สุด'],'B',
      ['💡 จุดที่ F = 0 (no restoring force)','🔍 ที่จุดนี้ a = 0 ด้วย','📐 vัตถุผ่านจุดนี้ตลอด · ไม่หยุด']),

    M('R133S005','<strong>amplitude (A)</strong> ของ SHM คือ?',
      ['ระยะทางที่เคลื่อนที่ใน 1 cycle','ระยะที่ไกลที่สุดจากตำแหน่งสมดุล','คาบการเคลื่อนที่','ความเร็วสูงสุด'],'B',
      ['💡 A = ระยะออกมากที่สุดจากสมดุล','🔍 วัตถุเคลื่อนระหว่าง −A ถึง +A','📐 ระยะใน 1 cycle = 4A']),

    TF('R133S006','"ลูกบอลกระเด้งบนพื้น เป็นตัวอย่างของ SHM"',false,
      ['💡 ลูกบอลกระเด้ง — แรงสัมผัสเป็น impulse ไม่ใช่ linear','🔍 SHM ต้องการ F ∝ −x ตลอด','📐 lukbol แค่ periodic — ไม่ใช่ harmonic']),

    M('R133S007','การเคลื่อนที่แบบ SHM เป็นการเคลื่อนที่แบบ?',
      ['ตามเส้นตรง ไม่ซ้ำเดิม','ซ้ำเดิม (periodic) กลับไปกลับมาผ่านสมดุล','สุ่ม ไม่มีรูปแบบ','เป็นวงกลม'],'B',
      ['💡 periodic = ซ้ำเป็นรอบ','🔍 SHM ⊆ periodic motion (เป็น subset ที่พิเศษ)','📐 ทุก SHM = periodic แต่ ไม่ใช่ทุก periodic = SHM']),

    M('R133S008','ข้อใด <strong>ไม่ใช่</strong> SHM?',
      ['สปริงในแนวระดับ','ลูกตุ้มมุมเล็ก','สปริงในแนวดิ่ง','การเคลื่อนที่แบบวงกลมสม่ำเสมอ'],'D',
      ['💡 UCM ≠ SHM (UCM 2D · SHM 1D)','🔍 แต่ SHM = projection ของ UCM (เรียนใน A5)','📐 1, 2, 3 มี F = −kx ทั้งหมด']),

    M('R133S009','ที่ <strong>ตำแหน่งสุดขอบ (extremes, x = ±A)</strong> ของ SHM ความเร็ว v มีค่าเท่าใด?',
      ['v = ωA (สูงสุด)','v = 0','v = A','ขึ้นกับ k'],'B',
      ['💡 ที่ extremes — วัตถุพอดีจะกลับทิศ','🔍 ก่อนกลับ v ต้องลด → ผ่าน 0','📐 ที่ x=±A → v = 0 เสมอ'],
      SVG_SPRING),

    CHK('R133S010','เลือก <strong>ตัวอย่างของ SHM</strong> ที่ถูกต้อง (ในอุดมคติ)',
      ['สปริงผูกมวลแกว่งไปมาในแนวระดับ','ลูกตุ้มแกว่งมุมเล็ก (small angle)','ลูกตุ้มแกว่งมุมใหญ่ 80°','สปริงในแนวดิ่งกับมวล','ลูกบอลกระเด้งบนพื้น','ดาวเทียมโคจรรอบโลก'],
      [1,2,4],
      ['💡 3 ผิด — มุมใหญ่ไม่ใช่ SHM (sin θ ≠ θ)','🔍 5 ผิด — แรงไม่ linear','📐 6 ผิด — UCM ไม่ใช่ SHM (เป็น 2D)']),

    // ════════ A2 — A · T · f · ω · phase (R133S011-020) ════════
    M('R133S011','<strong>คาบ T</strong> ใน SHM คือ?',
      ['ระยะที่เคลื่อนที่ใน 1 รอบ','เวลาที่ใช้ในการเคลื่อนที่ครบ 1 รอบ','ความเร็วสูงสุด','amplitude'],'B',
      ['💡 T = "เวลา" 1 cycle (s)','🔍 1 cycle = ออกไป +A → กลับ 0 → ลง −A → กลับ 0','📐 T เหมือนของวงกลม 1.3.2']),

    M('R133S012','<strong>ความถี่ f</strong> ใน SHM คือ?',
      ['จำนวน cycle ใน 1 วินาที','เวลาใน 1 cycle','ระยะใน 1 cycle','ความเร็ว ณ จุดสมดุล'],'A',
      ['💡 f = cycle/s · หน่วย Hz','🔍 f = 1/T','📐 ตรงข้ามกับ T']),

    TF('R133S013','"ใน SHM ω = 2πf = 2π/T เหมือนกับใน UCM"',true,
      ['💡 ω = angular frequency · หน่วย rad/s','🔍 ใช้สูตรเดียวกับ UCM','📐 เพราะ SHM = projection ของ UCM']),

    M('R133S014','หน่วยของ <strong>ω (angular frequency)</strong> ใน SHM คือ?',
      ['m/s','m/s²','rad/s','Hz'],'C',
      ['💡 ω = θ/t · θ rad · t s','🔍 → rad/s','📐 ความสัมพันธ์: ω = 2πf (Hz × 2π = rad/s)']),

    M('R133S015','การเคลื่อนที่ <strong>ครบ 1 cycle ของ SHM</strong> หมายถึง?',
      ['เคลื่อนจาก 0 ถึง +A','เคลื่อนจาก +A ถึง −A','เคลื่อนจาก 0 → +A → 0 → −A → 0','เคลื่อนจาก +A ถึง 0 ครั้งเดียว'],'C',
      ['💡 1 cycle = วัตถุกลับมาตำแหน่งและทิศเดิม','🔍 ผ่านสมดุล 2 ครั้ง · ผ่าน extremes 2 ครั้ง','📐 ระยะรวม = 4A · กระจัด = 0']),

    M('R133S016','<strong>เฟส (phase)</strong> ของ SHM หมายถึง?',
      ['ตำแหน่งและทิศการเคลื่อนที่ ณ ขณะหนึ่งของ cycle','ขนาดของ A','ความเร็วสูงสุด','คาบ T'],'A',
      ['💡 phase = "อยู่ที่ใดใน cycle"','🔍 ω·t = phase angle (เรเดียน)','📐 เริ่มจาก 0 → 2π ครบ 1 cycle']),

    M('R133S017','SHM 2 ตัวที่ <strong>"เฟสเดียวกัน" (in phase)</strong> หมายความว่าอย่างไร?',
      ['ขึ้นและลงพร้อมกัน · ผ่านสมดุลพร้อมกัน · ที่ extremes พร้อมกัน','ขึ้นและลงสวนทางกัน','มี A เท่ากัน','มี ω เท่ากัน'],'A',
      ['💡 in phase → กราฟ x-t ทับกันเป็นจังหวะ','🔍 phase difference = 0','📐 มีพฤติกรรมเหมือนกันที่เวลาเดียว']),

    M('R133S018','SHM 2 ตัวที่ <strong>"ตรงข้ามเฟส" (out of phase, π)</strong> หมายความว่าอย่างไร?',
      ['ขึ้น/ลงพร้อมกัน','ขึ้นและลงสวนทางกัน 180°','มี A เท่ากัน','คาบต่างกัน'],'B',
      ['💡 phase diff = π (180°)','🔍 ขณะหนึ่ง: ตัวหนึ่งที่ +A · อีกตัว −A','📐 กราฟ x-t = ภาพสะท้อน']),

    M('R133S019','หน่วยที่ <strong>ถูกต้อง</strong> ของ amplitude (A)?',
      ['s','Hz','m (เมตร)','m/s'],'C',
      ['💡 A = ระยะ → หน่วยความยาว','🔍 m, cm, mm ก็ได้','📐 ไม่ใช่เวลาหรือความเร็ว']),

    CHK('R133S020','เลือก <strong>ปริมาณที่คงที่ใน SHM</strong> (สำหรับการเคลื่อนที่หนึ่งๆ)',
      ['amplitude A','คาบ T','ความถี่ f','ω','x (ตำแหน่ง)','v (ความเร็ว)'],
      [1,2,3,4],
      ['💡 5, 6 ผิด — x และ v เปลี่ยนตามเวลา','🔍 A, T, f, ω = ลักษณะของ "ระบบ" — ไม่เปลี่ยน','📐 ที่เปลี่ยนคือ "สถานะ" ของวัตถุ ณ เวลา']),

    // ════════ A3 — a = −ω²x · restoring force ⭐ (R133S021-032) ════════
    M('R133S021','<strong>"แรงคืนตัว" (restoring force)</strong> ใน SHM คือ?',
      ['แรงที่ดึงวัตถุออกจากสมดุล','แรงที่ดึงวัตถุกลับสู่สมดุลเสมอ','แรงเสียดทาน','แรงโน้มถ่วง'],'B',
      ['💡 restoring = "คืน" ให้กลับมาที่สมดุล','🔍 ทิศตรงข้ามกับ x (ระยะออก)','📐 F = −kx (เครื่องหมายลบ = ตรงข้าม)']),

    M('R133S022','สูตรของแรงในสปริง (Hooke\'s law) คือ?',
      ['F = kx','F = −kx','F = mg','F = mω²x'],'B',
      ['💡 เครื่องหมายลบ = "คืน" ทิศ','🔍 ถ้า x > 0 → F < 0 (ทิศตรงข้าม)','📐 ที่เรียนใน Region 1.2 (ฮุค)']),

    TF('R133S023','"จาก F = −kx และ F = ma → จะได้ a = −(k/m)x = −ω²x"',true,
      ['💡 ω² = k/m → ω = √(k/m)','🔍 a มีทิศตรงข้ามกับ x','📐 หัวใจของ SHM']),

    M('R133S024','เครื่องหมายลบใน <strong>a = −ω²x</strong> หมายถึง?',
      ['a มีค่าน้อยกว่า 0 เสมอ','ทิศของ a ตรงข้ามกับทิศของ x','ω² ติดลบ','x ติดลบเสมอ'],'B',
      ['💡 ทิศ a ⇄ ทิศ x','🔍 ถ้า x > 0 (ขวา) → a < 0 (ซ้าย)','📐 ทำให้วัตถุ "เร่งกลับ" หาสมดุล']),

    M('R133S025','ที่ <strong>x = 0 (สมดุล)</strong> ความเร่ง a มีค่าเท่าใด?',
      ['a_max','0','−ω²A','+ω²A'],'B',
      ['💡 a = −ω²x → x = 0 → a = 0','🔍 ที่สมดุลไม่มีแรงคืนตัว','📐 เป็นตำแหน่งที่ a น้อยที่สุด (ขนาด 0)'],
      SVG_VAX),

    M('R133S026','ที่ <strong>x = +A (ขวาสุด)</strong> ความเร่ง a เท่ากับ?',
      ['+ω²A','−ω²A (ทิศซ้าย ขนาด ω²A)','0','+ωA'],'B',
      ['💡 a = −ω²(+A) = −ω²A','🔍 ทิศซ้าย (ตรงข้ามกับ +A) · ขนาด ω²A','📐 ที่ extremes — a มีขนาดสูงสุด'],
      SVG_VAX),

    M('R133S027','ที่ <strong>x = −A (ซ้ายสุด)</strong> ความเร่ง a เท่ากับ?',
      ['+ω²A (ทิศขวา ขนาด ω²A)','−ω²A','0','−ωA'],'A',
      ['💡 a = −ω²(−A) = +ω²A','🔍 ทิศขวา (ตรงข้ามกับ −A) · ขนาด ω²A','📐 ที่นี่ a เร่งให้กลับไปทาง +A']),

    M('R133S028','ตำแหน่งใดที่ความเร่ง a มี <strong>ขนาดสูงสุด</strong>?',
      ['x = 0 (สมดุล)','x = ±A (extremes)','ขึ้นอยู่กับ T','ทุกตำแหน่งเท่ากัน'],'B',
      ['💡 |a| = ω²|x|','🔍 |x| สูงสุดที่ ±A → |a| สูงสุด','📐 a_max = ω²A'],
      SVG_VAX),

    M('R133S029','ตำแหน่งใดที่ความเร่ง a เท่ากับ <strong>0</strong>?',
      ['x = +A','x = −A','x = 0 (สมดุล)','ทุกตำแหน่ง'],'C',
      ['💡 a ∝ x → x = 0 → a = 0','🔍 ที่สมดุลไม่มีแรงคืนตัว','📐 แต่ v ที่จุดนี้ = max!']),

    TF('R133S030','"ความสัมพันธ์ระหว่าง a กับ x ใน SHM คือ linear · slope = −ω²"',true,
      ['💡 a = −ω²x → กราฟ a-x = เส้นตรง','🔍 ความชัน = −ω² (negative)','📐 พิสูจน์ SHM ได้จากกราฟ a-x']),

    TF('R133S031','"ใน SHM ความเร่ง a มีค่าคงที่ตลอดเวลา"',false,
      ['💡 a ขึ้นกับ x → x เปลี่ยน → a เปลี่ยน','🔍 ขนาด a เปลี่ยนจาก 0 ที่สมดุล → ω²A ที่ extremes','📐 ทิศ a ก็เปลี่ยนตามตำแหน่ง']),

    CHK('R133S032','เลือก <strong>คุณสมบัติของ a ใน SHM</strong> ที่ถูก',
      ['a ∝ −x (ตรงข้าม)','|a| สูงสุดที่ extremes','|a| = 0 ที่สมดุล','a คงที่ทั้งขนาดและทิศ','a และ x ทิศตรงข้ามเสมอ','กราฟ a-x = เส้นตรงผ่านจุดกำเนิด · slope ลบ'],
      [1,2,3,5,6],
      ['💡 4 ผิด — a เปลี่ยนตามตำแหน่ง','🔍 a และ x สลับเครื่องหมายเสมอ','📐 หัวใจของ A3']),

    // ════════ A4 — x, v, a ตลอด cycle ⭐ (R133S033-044) ════════
    M('R133S033','ที่ <strong>ตำแหน่งสมดุล (x = 0)</strong> ความเร็ว v มีค่าเท่าใด?',
      ['0','v_max','ωA','ขึ้นกับ A เท่านั้น'],'B',
      ['💡 ที่ x = 0 — KE สูงสุด · v สูงสุด','🔍 ทุกพลังงานเป็น KE (PE=0)','📐 v_max = ωA'],
      SVG_VAX),

    M('R133S034','ที่ <strong>ตำแหน่งสุดขอบ (x = ±A)</strong> ความเร็ว v มีค่าเท่าใด?',
      ['v_max','ωA','0','−ωA'],'C',
      ['💡 ที่ extremes — วัตถุพอดีจะกลับทิศ → v=0','🔍 ทุกพลังงานเป็น PE (KE=0)','📐 ที่ extremes ทุกครั้ง v = 0'],
      SVG_VAX),

    M('R133S035','ความเร็ว <strong>v_max</strong> ของ SHM เกิดที่ตำแหน่งใด?',
      ['x = +A','x = −A','x = 0 (สมดุล)','ทุกตำแหน่งเท่ากัน'],'C',
      ['💡 ที่ x = 0 → ทุกพลังงานเป็น KE','🔍 KE_max → v_max','📐 v_max = ωA']),

    M('R133S036','สูตร <strong>ความเร็วสูงสุด v_max</strong> ใน SHM คือ?',
      ['v_max = A','v_max = ω','v_max = ωA','v_max = ω²A'],'C',
      ['💡 v_max = ωA','🔍 มาจาก projection ของ UCM (v ของ UCM = ωR)','📐 หรือจากพลังงาน: ½mv²_max = ½kA²'],
      SVG_VAX),

    M('R133S037','สูตร <strong>ความเร่งสูงสุด a_max</strong> ใน SHM คือ?',
      ['a_max = A','a_max = ωA','a_max = ω²A','a_max = ω/A'],'C',
      ['💡 |a| = ω²|x| → x_max = A → a_max = ω²A','🔍 เกิดที่ extremes (x = ±A)','📐 v_max = ωA · a_max = ω²A']),

    M('R133S038','ความเร่ง <strong>a_max</strong> เกิดที่ตำแหน่งใด?',
      ['x = 0 (สมดุล)','x = ±A (extremes)','ระหว่าง 0 ถึง A','ขึ้นกับ ω'],'B',
      ['💡 |a| = ω²|x| → |x| สูงสุดที่ extremes','🔍 ที่นั่น a_max = ω²A','📐 ที่ extremes — v=0 แต่ a สูงสุด']),

    TF('R133S039','"ที่ตำแหน่งสมดุล x=0 ความเร่ง a = 0 และความเร็ว v = สูงสุด"',true,
      ['💡 หัวใจของ A4: ที่สมดุล → a=0, v=v_max','🔍 ที่ extremes → a=a_max, v=0','📐 v และ a "สลับกัน" ตลอด cycle']),

    TF('R133S040','"ที่ตำแหน่ง extremes (x=±A) ความเร่ง a = สูงสุด และความเร็ว v = 0"',true,
      ['💡 ที่ extremes → KE=0, PE สูงสุด','🔍 |a|_max = ω²A · v=0','📐 จุดที่วัตถุกลับทิศ']),

    M('R133S041','ใน SHM ที่ตำแหน่งใดๆ <strong>ทิศของ a เทียบกับ x</strong> เป็นอย่างไร?',
      ['ทิศเดียวกัน','ตรงข้าม','ตั้งฉาก','ขึ้นกับ ω'],'B',
      ['💡 a = −ω²x → ติดลบ → ทิศตรงข้าม','🔍 ถ้า x ขวา → a ซ้าย','📐 misconception killer ของ A3-A4']),

    M('R133S042','ใน SHM ความสัมพันธ์ของ <strong>เฟสระหว่าง v กับ x</strong>?',
      ['ในเฟสเดียวกัน','ต่างกัน 90° (π/2)','ตรงข้าม (180°)','ไม่มีความสัมพันธ์'],'B',
      ['💡 x = A cos(ωt) → v = −Aω sin(ωt)','🔍 cos กับ sin ต่างเฟส 90°','📐 ที่ x_max → v=0 · ที่ x=0 → v_max'],
      SVG_XT),

    M('R133S043','ใน SHM ความสัมพันธ์ของ <strong>เฟสระหว่าง a กับ x</strong>?',
      ['ในเฟสเดียวกัน','ต่างกัน 90°','ตรงข้าม (180°)','ขึ้นกับ A'],'C',
      ['💡 a = −ω²x → ตรงกันข้ามเสมอ','🔍 phase diff = π (180°)','📐 a และ x สลับเครื่องหมายตลอด']),

    CHK('R133S044','จับคู่: <strong>ตำแหน่ง vs สถานะ</strong> ใน SHM (เลือกที่ถูก)',
      ['x = 0 → v = v_max','x = 0 → a = 0','x = +A → v = 0','x = +A → a = a_max (ทิศซ้าย)','x = ±A → KE = max','x = 0 → KE = max'],
      [1,2,3,4,6],
      ['💡 5 ผิด — ที่ extremes KE=0 (PE=max)','🔍 KE สูงสุดที่สมดุล','📐 รวบรวมแก่นของ A4']),

    // ════════ A5 — SHM ↔ UCM projection (R133S045-054) ════════
    M('R133S045','SHM <strong>มีความสัมพันธ์</strong> กับ UCM (uniform circular motion) อย่างไร?',
      ['ไม่เกี่ยวข้องกัน','SHM = projection ของ UCM ลงบนเส้นผ่านศูนย์กลาง','SHM ใช้ในวงกลมเท่านั้น','SHM = UCM แบบ 2D'],'B',
      ['💡 หา shadow ของจุดที่หมุนเป็นวงกลม','🔍 shadow บนแกน x → SHM','📐 ω เดียวกันทั้ง 2 การเคลื่อนที่'],
      SVG_PROJ),

    M('R133S046','ใน SHM ที่เกิดจาก <strong>projection ของ UCM</strong> · ω ของทั้งสองมีค่าอย่างไร?',
      ['ω ของ SHM > UCM','ω ของ SHM < UCM','เท่ากัน','ไม่เกี่ยวข้องกัน'],'C',
      ['💡 ω เดียวกัน → คาบเดียวกัน','🔍 1 cycle ของ SHM = 1 รอบของ UCM','📐 จึงเรียก angular frequency ทั้ง 2 อย่าง']),

    M('R133S047','<strong>amplitude (A)</strong> ของ SHM = อะไรของ UCM?',
      ['อัตราเร็ว v','รัศมีของวงกลม R','คาบ T','ความเร่ง a'],'B',
      ['💡 จุดบนวงกลมระยะ R จากศูนย์ → projection สุดที่ ±R','🔍 A = R','📐 ดังนั้น v_max = ωA = ωR (เหมือน UCM!)']),

    TF('R133S048','"ที่ตำแหน่งสมดุล (x=0) ของ SHM · จุดบน UCM อยู่ที่ตำแหน่งบนสุดหรือล่างสุดของวงกลม"',true,
      ['💡 projection ลงแกน x = 0 → จุด UCM อยู่บนแกน y','🔍 บนแกน y = ตำแหน่ง 12 หรือ 6 นาฬิกาของ UCM','📐 ที่จุดนั้น v ของ UCM ขนานแกน x → v_SHM สูงสุด']),

    TF('R133S049','"ที่ตำแหน่ง extremes (x=±A) ของ SHM · จุดบน UCM อยู่บนแกน x"',true,
      ['💡 projection ลงแกน x = ±R → จุด UCM อยู่ที่ 3 หรือ 9 นาฬิกา','🔍 ที่จุดนั้น v ของ UCM ขนานแกน y → v_SHM = 0','📐 ใช้ visualize หา v, a ของ SHM']),

    M('R133S050','สมการตำแหน่ง <strong>x(t) = A cos(ωt)</strong> หมายความว่าวัตถุเริ่ม (t=0) ที่ใด?',
      ['x = 0 (สมดุล)','x = +A (ขวาสุด)','x = −A (ซ้ายสุด)','ขึ้นกับ ω'],'B',
      ['💡 t=0 → cos(0) = 1 → x = A','🔍 เริ่มจากตำแหน่งสุดขอบ','📐 ใช้เมื่อปล่อยจาก extremes']),

    M('R133S051','สมการตำแหน่ง <strong>x(t) = A sin(ωt)</strong> หมายความว่าวัตถุเริ่ม (t=0) ที่ใด?',
      ['x = 0 (สมดุล)','x = +A','x = −A','ขึ้นกับ A'],'A',
      ['💡 t=0 → sin(0) = 0 → x = 0','🔍 เริ่มจากตำแหน่งสมดุล (กำลังวิ่ง)','📐 ใช้เมื่อเริ่มที่ v_max']),

    TF('R133S052','"ความเร็วของ SHM = projection ของความเร็วของ UCM ลงแกนเดียวกัน"',true,
      ['💡 ทั้ง v และ a ของ SHM = projection จาก UCM','🔍 v ของ UCM = ωR (ขนาดคงที่ · ทิศแนวสัมผัส)','📐 v ของ SHM เปลี่ยนตาม projection']),

    M('R133S053','รัศมีวงกลมที่เกิด UCM ผูกกับ SHM ที่ project ออกมา = ?',
      ['T','f','A (amplitude ของ SHM)','ω'],'C',
      ['💡 R_UCM = A_SHM','🔍 จุดบนวงกลมเดินรอบ R → เงาบนแกนวิ่ง ±R','📐 R = A เสมอ']),

    CHK('R133S054','เลือกข้อ <strong>ที่ถูก</strong> เกี่ยวกับ SHM ↔ UCM',
      ['SHM = projection ของ UCM ลงเส้นผ่านศูนย์กลาง','ω เดียวกันทั้ง 2','A_SHM = R_UCM','SHM = 2D motion','คาบเดียวกัน','v_max ของ SHM = ωR ของ UCM'],
      [1,2,3,5,6],
      ['💡 4 ผิด — SHM เป็น 1D · UCM 2D','🔍 SHM เป็น "เงา" 1 มิติของ UCM','📐 จึงพิสูจน์สูตร v_max = ωA จาก UCM ได้']),

    // ════════ A6 — Spring + Pendulum T (R133S055-070) ════════
    M('R133S055','คาบ T ของ <strong>มวลผูกสปริง</strong> (mass-spring SHM) คือ?',
      ['T = 2π√(m/k)','T = 2π√(k/m)','T = 2π·m·k','T = 2π·m/k'],'A',
      ['💡 T = 2π/ω และ ω = √(k/m)','🔍 T = 2π√(m/k)','📐 m หนัก → T มาก · k แข็ง → T น้อย'],
      SVG_SPRING),

    M('R133S056','คาบ T ของ <strong>spring-mass</strong> ขึ้นกับปริมาณใด?',
      ['m และ k เท่านั้น','A และ k','m และ A','m, k และ A'],'A',
      ['💡 T = 2π√(m/k)','🔍 ไม่ขึ้นกับ amplitude','📐 ปล่อยที่ A ใหญ่/เล็ก → T เท่ากัน']),

    TF('R133S057','"คาบของ spring SHM ไม่ขึ้นกับขนาด amplitude"',true,
      ['💡 T = 2π√(m/k) — ไม่มี A ในสูตร','🔍 ปล่อยจาก A เล็ก v_max เล็ก · A ใหญ่ v_max ใหญ่','📐 แต่ใช้เวลาในแต่ละ cycle เท่ากัน'],
      SVG_SPRING),

    M('R133S058','ถ้า <strong>m เพิ่มเป็น 4 เท่า</strong> (k เดิม) คาบ T ของ spring SHM เป็น?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'A',
      ['💡 T ∝ √m → m × 4 → T × √4 = 2','🔍 m × 9 → T × 3','📐 ใช้กฎ "ราก" ของอัตราส่วน'],
      SVG_SPRING),

    M('R133S059','ถ้า <strong>k เพิ่มเป็น 4 เท่า</strong> (m เดิม) คาบ T เป็น?',
      ['2 เท่า','4 เท่า','1/2 เท่า','1/4 เท่า'],'C',
      ['💡 T ∝ 1/√k → k × 4 → T × 1/2','🔍 สปริงแข็งขึ้น → คาบสั้นลง','📐 ω เพิ่ม → T ลด']),

    M('R133S060','คาบ T ของ <strong>ลูกตุ้มอย่างง่าย (simple pendulum)</strong> มุมเล็ก คือ?',
      ['T = 2π√(L/g)','T = 2π√(g/L)','T = 2π·L·g','T = π·L/g'],'A',
      ['💡 ω = √(g/L) → T = 2π√(L/g)','🔍 ใช้ได้เมื่อมุม θ ≤ ~15° (small angle)','📐 sin θ ≈ θ ในช่วงนี้'],
      SVG_PEND),

    M('R133S061','คาบ T ของ simple pendulum ขึ้นกับปริมาณใด?',
      ['m และ L','L และ g เท่านั้น','m, L และ g','A เท่านั้น'],'B',
      ['💡 T = 2π√(L/g) — ไม่มี m และ A','🔍 ลูกตุ้มหนัก/เบา → คาบเท่ากัน','📐 มุมแกว่งใหญ่/เล็ก (ในช่วง small angle) → คาบเท่ากัน'],
      SVG_PEND),

    TF('R133S062','"คาบของ simple pendulum ไม่ขึ้นกับมวลของลูกตุ้ม"',true,
      ['💡 T = 2π√(L/g) — ไม่มี m','🔍 มาจาก: มวลในแรงคืนตัว = มวลในแรงเฉื่อย → ตัดกัน','📐 Galileo สังเกตเห็นเรื่องนี้ที่โบสถ์'],
      SVG_PEND),

    TF('R133S063','"คาบของ simple pendulum ไม่ขึ้นกับ amplitude ของการแกว่ง (เฉพาะมุมเล็ก)"',true,
      ['💡 small angle approximation: sin θ ≈ θ','🔍 → SHM แท้ → T ไม่ขึ้นกับ A','📐 แกว่งมุมใหญ่ → T ขึ้นกับ A (ไม่ใช่ SHM แล้ว)']),

    M('R133S064','ถ้า <strong>L (ความยาวลูกตุ้ม) เพิ่มเป็น 4 เท่า</strong> · g เดิม → T เป็นเท่าใด?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'A',
      ['💡 T ∝ √L → L × 4 → T × 2','🔍 ลูกตุ้มยาวขึ้น → แกว่งช้าลง','📐 L × 9 → T × 3'],
      SVG_PEND),

    M('R133S065','นำลูกตุ้มไป <strong>ดวงจันทร์ (g_moon ≈ g/6)</strong> · L เดิม → T เป็น?',
      ['เท่าเดิม','น้อยลง (sqrt(6) เท่า)','มากขึ้น (√6 เท่า)','3 เท่า'],'C',
      ['💡 T ∝ 1/√g → g ลด → T เพิ่ม','🔍 g × 1/6 → T × √6 ≈ 2.45','📐 ลูกตุ้มแกว่งช้าลงบนดวงจันทร์'],
      SVG_PEND),

    M('R133S066','การเป็น "simple pendulum SHM" ใช้ <strong>small angle approximation</strong> ที่มุมประมาณ?',
      ['θ ≤ 15° (≈ 0.26 rad)','θ ≤ 90°','θ ≤ 180°','ทุกมุม'],'A',
      ['💡 sin θ ≈ θ ใช้ได้ที่มุมเล็ก','🔍 ที่ θ = 15° error ~1%','📐 มุมใหญ่ → ไม่ใช่ SHM แท้']),

    TF('R133S067','"คาบของ spring-mass ในแนวดิ่ง (มี gravity) เท่ากับในแนวระดับ"',true,
      ['💡 gravity แค่เลื่อนตำแหน่งสมดุล (ลงมา mg/k)','🔍 SHM รอบสมดุลใหม่ — ω เดิม','📐 T = 2π√(m/k) เท่าเดิม']),

    M('R133S068','สปริง 2 ตัว <strong>k₁ และ k₂ ต่อขนานกัน</strong> · ค่า k_eq รวมเท่ากับ?',
      ['k₁ + k₂','k₁·k₂/(k₁+k₂)','√(k₁k₂)','k₁ − k₂'],'A',
      ['💡 ขนาน → แรงรวมที่ระยะเดียว','🔍 F_eq = (k₁+k₂)x → k_eq = k₁+k₂','📐 ขนาน → k_eq มากกว่าทั้งคู่']),

    M('R133S069','สปริง 2 ตัว <strong>k₁ และ k₂ ต่ออนุกรมกัน</strong> · ค่า k_eq รวมเท่ากับ?',
      ['k₁ + k₂','1/(1/k₁ + 1/k₂)','√(k₁k₂)','k₁ × k₂'],'B',
      ['💡 อนุกรม → ระยะรวม = ผลรวมระยะแต่ละตัว','🔍 1/k_eq = 1/k₁ + 1/k₂','📐 อนุกรม → k_eq น้อยกว่าทั้งคู่']),

    CHK('R133S070','เลือก <strong>คุณสมบัติที่ถูก</strong> เปรียบเทียบ Spring SHM vs Pendulum SHM',
      ['ทั้งคู่ T ไม่ขึ้นกับ A (มุมเล็ก)','Spring T ขึ้นกับ m · Pendulum T ไม่ขึ้นกับ m','Spring T = 2π√(m/k)','Pendulum T = 2π√(L/g)','Spring T ขึ้นกับ g','Pendulum T ขึ้นกับ g'],
      [1,2,3,4,6],
      ['💡 5 ผิด — Spring T ไม่ขึ้นกับ g (สมดุลแค่ shift)','🔍 ที่แตกต่างหลัก: m ใน spring vs ไม่ใน pendulum','📐 ทั้งคู่ "ไม่ขึ้นกับ A" ตราบที่อยู่ในช่วง SHM'])
  ];

  window.QUESTIONS_R133_A = Q;
  if(window.console && console.log) console.log('[Region 1.3.3 Stage A] loaded', Q.length, '/ 70 questions');
})();
