/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.3.2 เนินวงเวียน (วงกลม)
   Stage B "ใช้สูตรไหน" · 80 ข้อ · noReveal pattern
   MCQ + FILL · ดึงตัวแปร + เลือกสูตร + ดูทิศ
   ใช้ g = 10 · π ≈ 3.14 · sin37°=cos53°=0.6 · cos37°=sin53°=0.8

   หมวด:
     B1 ดึงตัวแปร · v=ωR, ω=2π/T=2πf      (R132C081-095 · 15)
     B2 a_c, F_c สูตรเลือก                  (R132C096-107 · 12)
     B3 ผันผัน v, r, m, ω, f, T             (R132C108-117 · 10)
     B4 13 Pattern · เลือกแรง F_c           (R132C118-133 · 16)
     B5 vertical loop (top/bottom)          (R132C134-143 · 10)
     B6 banked + conical pendulum           (R132C144-153 · 10)
     B7 satellite / orbital                 (R132C154-160 · 7)
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  const F_TAG = ['circular-b'];

  function M(id, statement, choices, correct, hints, figure){
    const arr = choices.map((t,i) => ({key:String.fromCharCode(65+i), text:t}));
    const q = {id, group:'B', type:'mcq', statement, choices:arr, correct, hints, formula_tags:F_TAG, noReveal:true};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function F(id, statement, ans, unit, hints, figure){
    const q = {id, group:'B', type:'fill', statement, correct: String(ans), unit:unit||'', hints, formula_tags:F_TAG, noReveal:true};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function CHK(id, statement, options, correctIdx, hints, figure){
    const items = options.map((t,i) => ({key:String(i+1), text:t}));
    const q = {id, group:'B', type:'check', statement, items, correct: correctIdx.map(String), hints, formula_tags:F_TAG, noReveal:true};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }

  // ─── SVG library (compact · cover 13 patterns) ───
  const SVG_VLOOP_FORCES = '<svg viewBox="0 0 220 200" xmlns="http://www.w3.org/2000/svg"><circle cx="110" cy="100" r="70" fill="none" stroke="#34d399" stroke-width="1.2" stroke-dasharray="3,2"/><circle cx="110" cy="100" r="3" fill="#fbbf24"/><circle cx="110" cy="30" r="7" fill="#fbbf24" stroke="#fff" stroke-width="1"/><line x1="110" y1="33" x2="110" y2="65" stroke="#a78bfa" stroke-width="2"/><polygon points="110,68 107,62 113,62" fill="#a78bfa"/><text x="115" y="58" fill="#a78bfa" font-size="10">T↓</text><line x1="110" y1="40" x2="110" y2="58" stroke="#f87171" stroke-width="2"/><text x="80" y="55" fill="#f87171" font-size="10">W↓</text><text x="115" y="22" fill="#fff" font-size="10">บน</text><circle cx="110" cy="170" r="7" fill="#fbbf24" stroke="#fff" stroke-width="1"/><line x1="110" y1="167" x2="110" y2="135" stroke="#a78bfa" stroke-width="2"/><polygon points="110,132 107,138 113,138" fill="#a78bfa"/><text x="115" y="150" fill="#a78bfa" font-size="10">T↑</text><line x1="110" y1="173" x2="110" y2="190" stroke="#f87171" stroke-width="2"/><polygon points="110,193 107,187 113,187" fill="#f87171"/><text x="115" y="195" fill="#f87171" font-size="10">W↓</text><text x="115" y="186" fill="#fff" font-size="10">ล่าง</text></svg>';
  const SVG_BANKED_B = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg"><polygon points="20,120 200,120 200,75" fill="#1f2937" stroke="#fbbf24" stroke-width="1.5"/><line x1="20" y1="120" x2="200" y2="120" stroke="#fff" stroke-width="0.8" stroke-dasharray="3,2"/><rect x="135" y="86" width="40" height="22" fill="#38bdf8" stroke="#fff" stroke-width="1" transform="rotate(-15 155 97)"/><line x1="155" y1="97" x2="125" y2="55" stroke="#34d399" stroke-width="2"/><polygon points="123,52 130,55 127,61" fill="#34d399"/><text x="105" y="50" fill="#34d399" font-size="11" font-weight="700">N</text><line x1="155" y1="97" x2="155" y2="125" stroke="#f87171" stroke-width="2"/><polygon points="155,128 152,122 158,122" fill="#f87171"/><text x="160" y="120" fill="#f87171" font-size="10">W</text><path d="M 195,115 A 18,18 0 0,0 182,100" fill="none" stroke="#a78bfa" stroke-width="1.2"/><text x="180" y="115" fill="#a78bfa" font-size="11">θ</text><text x="50" y="135" fill="#fff" font-size="9">tan θ = v²/(rg)</text></svg>';

  // แกว่งราบ — ด้านบนมอง (top view) · เชือก + วัตถุ + v แนวสัมผัส
  const SVG_HSWING = '<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="80" r="55" fill="none" stroke="#34d399" stroke-width="1.2" stroke-dasharray="3,2"/><circle cx="100" cy="80" r="4" fill="#fbbf24"/><line x1="100" y1="80" x2="155" y2="80" stroke="#a78bfa" stroke-width="2"/><circle cx="155" cy="80" r="7" fill="#fbbf24" stroke="#fff" stroke-width="1"/><text x="120" y="75" fill="#a78bfa" font-size="11" font-weight="700">T</text><line x1="155" y1="74" x2="155" y2="45" stroke="#38bdf8" stroke-width="2"/><polygon points="155,42 152,48 158,48" fill="#38bdf8"/><text x="160" y="50" fill="#38bdf8" font-size="10">v</text><text x="55" y="155" fill="#fff" font-size="10">แกว่งแนวระดับ (top view)</text></svg>';

  // Conical pendulum — แตกแรง T cosα = mg, T sinα = F_c
  const SVG_CONICAL = '<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="15" x2="180" y2="15" stroke="#fff" stroke-width="2"/><line x1="100" y1="15" x2="100" y2="120" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3"/><line x1="100" y1="15" x2="160" y2="120" stroke="#a78bfa" stroke-width="2"/><circle cx="160" cy="120" r="8" fill="#fbbf24" stroke="#fff" stroke-width="1"/><ellipse cx="100" cy="120" rx="60" ry="14" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="2,2"/><text x="115" y="58" fill="#a78bfa" font-size="11" font-weight="700">T</text><text x="120" y="35" fill="#34d399" font-size="11">α</text><text x="125" y="115" fill="#38bdf8" font-size="10">r</text><line x1="160" y1="128" x2="160" y2="155" stroke="#f87171" stroke-width="2"/><polygon points="160,158 157,152 163,152" fill="#f87171"/><text x="165" y="148" fill="#f87171" font-size="10">W</text></svg>';

  // จานหมุน (top view) — วัตถุติดผิวจาน + f_s เข้าศูนย์
  const SVG_DISC = '<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg"><ellipse cx="100" cy="80" rx="75" ry="20" fill="#1f2937" stroke="#fbbf24" stroke-width="1.5"/><circle cx="100" cy="80" r="3" fill="#fbbf24"/><rect x="146" y="72" width="18" height="16" fill="#38bdf8" stroke="#fff" stroke-width="1"/><line x1="146" y1="80" x2="115" y2="80" stroke="#fbbf24" stroke-width="2"/><polygon points="112,80 118,77 118,83" fill="#fbbf24"/><text x="118" y="75" fill="#fbbf24" font-size="10" font-weight="700">f_s</text><path d="M 30 50 A 70 18 0 0 1 170 50" fill="none" stroke="#a78bfa" stroke-width="1.2"/><polygon points="172,52 165,48 167,55" fill="#a78bfa"/><text x="85" y="35" fill="#a78bfa" font-size="10">ω หมุน</text><text x="40" y="140" fill="#fff" font-size="10">จานหมุน (top view)</text></svg>';

  // รถบนยอดเนิน (hill) — W ลง, N ขึ้น, F_c=W−N
  const SVG_HILL_TOP = '<svg viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg"><path d="M 20 110 Q 110 30 200 110" fill="none" stroke="#fbbf24" stroke-width="1.5"/><rect x="92" y="45" width="36" height="16" fill="#38bdf8" stroke="#fff" stroke-width="1"/><line x1="110" y1="50" x2="110" y2="20" stroke="#34d399" stroke-width="2"/><polygon points="110,17 107,23 113,23" fill="#34d399"/><text x="115" y="25" fill="#34d399" font-size="11" font-weight="700">N</text><line x1="110" y1="62" x2="110" y2="95" stroke="#f87171" stroke-width="2.5"/><polygon points="110,98 107,92 113,92" fill="#f87171"/><text x="115" y="92" fill="#f87171" font-size="11" font-weight="700">W</text><line x1="110" y1="135" x2="110" y2="115" stroke="#a78bfa" stroke-width="0.8" stroke-dasharray="2,2"/><circle cx="110" cy="135" r="3" fill="#a78bfa"/><text x="115" y="135" fill="#a78bfa" font-size="9">ศูนย์กลาง</text><text x="70" y="130" fill="#fff" font-size="10">รถบนยอดเนิน · F_c=W−N</text></svg>';

  // รถในร่อง (valley) — N ขึ้น, W ลง, F_c=N−W
  const SVG_VALLEY = '<svg viewBox="0 0 220 150" xmlns="http://www.w3.org/2000/svg"><path d="M 20 30 Q 110 130 200 30" fill="none" stroke="#fbbf24" stroke-width="1.5"/><rect x="92" y="100" width="36" height="16" fill="#38bdf8" stroke="#fff" stroke-width="1"/><line x1="110" y1="100" x2="110" y2="60" stroke="#34d399" stroke-width="2.5"/><polygon points="110,57 107,63 113,63" fill="#34d399"/><text x="115" y="65" fill="#34d399" font-size="11" font-weight="700">N</text><line x1="110" y1="118" x2="110" y2="140" stroke="#f87171" stroke-width="2"/><polygon points="110,143 107,137 113,137" fill="#f87171"/><text x="115" y="138" fill="#f87171" font-size="10">W</text><circle cx="110" cy="15" r="3" fill="#a78bfa"/><text x="115" y="18" fill="#a78bfa" font-size="9">ศูนย์กลาง</text><line x1="110" y1="15" x2="110" y2="95" stroke="#a78bfa" stroke-width="0.8" stroke-dasharray="2,2"/><text x="60" y="135" fill="#fff" font-size="10">รถในร่อง · F_c=N−W</text></svg>';

  // รถเลี้ยวถนนราบ (top view) — f_s เข้าศูนย์
  const SVG_FLATCURVE = '<svg viewBox="0 0 220 150" xmlns="http://www.w3.org/2000/svg"><path d="M 30 130 A 80 80 0 0 1 180 50" fill="none" stroke="#fbbf24" stroke-width="2"/><path d="M 50 130 A 60 60 0 0 1 170 70" fill="none" stroke="#fbbf24" stroke-width="2" stroke-dasharray="3,2"/><rect x="100" y="65" width="30" height="16" fill="#38bdf8" stroke="#fff" stroke-width="1" transform="rotate(-30 115 73)"/><line x1="115" y1="73" x2="180" y2="120" stroke="#34d399" stroke-width="0.8" stroke-dasharray="2,2"/><circle cx="180" cy="120" r="3" fill="#a78bfa"/><text x="183" y="125" fill="#a78bfa" font-size="9">ศูนย์โค้ง</text><line x1="115" y1="73" x2="145" y2="93" stroke="#fbbf24" stroke-width="2"/><polygon points="148,95 141,93 144,99" fill="#fbbf24"/><text x="148" y="90" fill="#fbbf24" font-size="11" font-weight="700">f_s</text><text x="40" y="20" fill="#fff" font-size="10">เลี้ยวถนนราบ · F_c=f_s</text></svg>';

  // Rotor (wall of death) — N เข้าศูนย์ · f_s ขึ้น · W ลง
  const SVG_ROTOR = '<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg"><ellipse cx="100" cy="25" rx="70" ry="12" fill="none" stroke="#fbbf24" stroke-width="1.5"/><ellipse cx="100" cy="155" rx="70" ry="12" fill="none" stroke="#fbbf24" stroke-width="1.5"/><line x1="30" y1="25" x2="30" y2="155" stroke="#fbbf24" stroke-width="1.5"/><line x1="170" y1="25" x2="170" y2="155" stroke="#fbbf24" stroke-width="1.5"/><rect x="155" y="80" width="14" height="22" fill="#38bdf8" stroke="#fff" stroke-width="1"/><line x1="155" y1="91" x2="125" y2="91" stroke="#34d399" stroke-width="2"/><polygon points="122,91 128,88 128,94" fill="#34d399"/><text x="128" y="85" fill="#34d399" font-size="10" font-weight="700">N</text><line x1="162" y1="80" x2="162" y2="55" stroke="#fbbf24" stroke-width="2"/><polygon points="162,52 159,58 165,58" fill="#fbbf24"/><text x="167" y="65" fill="#fbbf24" font-size="10">f_s</text><line x1="162" y1="102" x2="162" y2="125" stroke="#f87171" stroke-width="2"/><polygon points="162,128 159,122 165,122" fill="#f87171"/><text x="167" y="120" fill="#f87171" font-size="10">W</text><text x="60" y="13" fill="#a78bfa" font-size="10">↻ ถังหมุน</text></svg>';

  // ดาวเทียม + โลก + F_grav เข้าศูนย์
  const SVG_ORBIT = '<svg viewBox="0 0 220 180" xmlns="http://www.w3.org/2000/svg"><circle cx="110" cy="90" r="70" fill="none" stroke="#34d399" stroke-width="1.2" stroke-dasharray="3,3"/><circle cx="110" cy="90" r="22" fill="#1d4ed8" stroke="#38bdf8" stroke-width="1.5"/><text x="100" y="95" fill="#fff" font-size="11" font-weight="700">โลก</text><circle cx="180" cy="90" r="6" fill="#fbbf24" stroke="#fff" stroke-width="1"/><line x1="180" y1="85" x2="180" y2="55" stroke="#38bdf8" stroke-width="2"/><polygon points="180,52 177,58 183,58" fill="#38bdf8"/><text x="183" y="50" fill="#38bdf8" font-size="10">v</text><line x1="174" y1="90" x2="140" y2="90" stroke="#f87171" stroke-width="2"/><polygon points="137,90 143,87 143,93" fill="#f87171"/><text x="145" y="85" fill="#f87171" font-size="10" font-weight="700">F_grav</text><text x="125" y="160" fill="#fbbf24" font-size="10">ดาวเทียม</text></svg>';

  // มอเตอร์ไซค์เอียง — มุม θ + N + W + เส้นเอียง
  const SVG_BIKE = '<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="135" x2="180" y2="135" stroke="#fff" stroke-width="1.5"/><line x1="100" y1="135" x2="75" y2="65" stroke="#38bdf8" stroke-width="3"/><circle cx="75" cy="65" r="6" fill="#fbbf24"/><circle cx="100" cy="135" r="8" fill="#1f2937" stroke="#fbbf24" stroke-width="1.5"/><line x1="100" y1="135" x2="100" y2="65" stroke="#fbbf24" stroke-width="0.8" stroke-dasharray="3,2"/><path d="M 100 105 A 30 30 0 0 0 90 95" fill="none" stroke="#a78bfa" stroke-width="1.2"/><text x="85" y="108" fill="#a78bfa" font-size="12" font-weight="700">θ</text><line x1="75" y1="65" x2="75" y2="30" stroke="#34d399" stroke-width="2"/><polygon points="75,27 72,33 78,33" fill="#34d399"/><text x="55" y="32" fill="#34d399" font-size="10">N</text><line x1="75" y1="65" x2="75" y2="100" stroke="#f87171" stroke-width="2"/><text x="80" y="90" fill="#f87171" font-size="10">W</text><text x="30" y="155" fill="#fff" font-size="10">tan θ = v²/(rg)</text></svg>';

  const Q = [
    // ════════ B1 — ดึงตัวแปร · v, ω, T, f relations (R132C081-095 · 15) ════════
    M('R132C081','สูตรของ <strong>ω (อัตราเร็วเชิงมุม)</strong> ในรูปคาบ T?',
      ['ω = T','ω = 2πT','ω = 2π/T','ω = T/(2π)'],'C',
      ['💡 ครบ 1 รอบ θ = 2π · เวลา T','🔍 ω = θ/t = 2π/T','📐 หน่วย rad/s']),

    M('R132C082','สูตรของ <strong>ω</strong> ในรูปความถี่ f?',
      ['ω = f','ω = πf','ω = 2πf','ω = f/(2π)'],'C',
      ['💡 ω = 2π/T และ T = 1/f','🔍 ω = 2πf','📐 1 รอบ = 2π rad → f Hz × 2π = 2πf rad/s']),

    M('R132C083','สูตรเชื่อม <strong>ความเร็วเชิงเส้น v</strong> กับ <strong>เชิงมุม ω</strong>?',
      ['v = ω/R','v = ωR','v = ω + R','v = ω²R'],'B',
      ['💡 v = ωR (จำง่าย "วี-โอเมก้า-อาร์")','🔍 R เพิ่ม → v เพิ่ม (ω เดิม)','📐 หน่วย: rad/s × m = m/s ✓']),

    M('R132C084','ความสัมพันธ์ <strong>คาบ T</strong> กับ <strong>ความถี่ f</strong>?',
      ['T·f = 1','T = f','T = 2πf','T = f²'],'A',
      ['💡 T = 1/f และ f = 1/T','🔍 ดังนั้น T·f = 1','📐 เช่น f=2 Hz → T=0.5 s']),

    F('R132C085','T = 2 s → ω เท่ากับ (rad/s)? (ใช้ π = 3.14)', 3.14, 'rad/s',
      ['💡 ω = 2π/T','🔍 = 2π/2 = π','📐 ≈ 3.14']),

    F('R132C086','T = π s → ω เท่ากับ (rad/s)?', 2, 'rad/s',
      ['💡 ω = 2π/T','🔍 = 2π/π','📐 = 2 rad/s']),

    F('R132C087','f = 2 Hz → ω เท่ากับ (rad/s)? (ใช้ π = 3.14)', 12.56, 'rad/s',
      ['💡 ω = 2πf','🔍 = 2π × 2 = 4π','📐 ≈ 12.56']),

    F('R132C088','ω = 4 rad/s · R = 5 m → v เท่ากับ (m/s)?', 20, 'm/s',
      ['💡 v = ωR','🔍 = 4 × 5','📐 = 20 m/s']),

    F('R132C089','f = 0.5 Hz → T เท่ากับ (s)?', 2, 's',
      ['💡 T = 1/f','🔍 = 1/0.5','📐 = 2 s']),

    F('R132C090','รถถังหมุน 10 รอบใน 5 วินาที → f เท่ากับ (Hz)?', 2, 'Hz',
      ['💡 f = จำนวนรอบ/เวลา','🔍 = 10/5','📐 = 2 Hz']),

    F('R132C091','ω = 5 rad/s · R = 2 m → v เท่ากับ (m/s)?', 10, 'm/s',
      ['💡 v = ωR','🔍 = 5 × 2','📐 = 10 m/s']),

    M('R132C092','หน่วยที่ <strong>ถูกต้อง</strong> ของ ω?',
      ['m/s','m/s²','rad/s','Hz·m'],'C',
      ['💡 ω = θ/t · θ rad · t s','🔍 → rad/s','📐 ω = 2πf (Hz × rad = rad/s)']),

    F('R132C093','5 รอบ เท่ากับกี่เรเดียน? (ใช้ π = 3.14)', 31.4, 'rad',
      ['💡 1 รอบ = 2π rad','🔍 5 × 2π = 10π','📐 ≈ 31.4 rad']),

    M('R132C094','ถ้า <strong>ω เพิ่ม 2 เท่า</strong> (R เดิม) v เป็นเท่าใดของเดิม?',
      ['1/2 เท่า','2 เท่า','4 เท่า','คงเดิม'],'B',
      ['💡 v = ωR (linear)','🔍 ω×2 → v×2','📐 ตรง ๆ ไม่กำลัง']),

    M('R132C095','ถ้า <strong>R เพิ่ม 3 เท่า</strong> · ω เดิม → v เป็นเท่าใด?',
      ['1/3 เท่า','3 เท่า','9 เท่า','คงเดิม'],'B',
      ['💡 v = ωR','🔍 R×3 → v×3','📐 ความเร็วที่ขอบนอกของจานหมุน > ตรงกลาง']),

    // ════════ B2 — a_c, F_c สูตรเลือก (R132C096-107 · 12) ════════
    M('R132C096','สูตรของ <strong>ความเร่งสู่ศูนย์กลาง a_c</strong>?',
      ['a_c = v/r','a_c = v²/r','a_c = vr','a_c = ω/r'],'B',
      ['💡 a_c = v²/r = ω²R','🔍 หน่วย: (m/s)²/m = m/s²','📐 ทิศเข้าศูนย์กลาง']),

    M('R132C097','สูตรของ a_c ในรูปเชิงมุม?',
      ['a_c = ω/R','a_c = ωR','a_c = ω²R','a_c = ω²/R'],'C',
      ['💡 a_c = v²/r และ v = ωR','🔍 (ωR)²/R = ω²R','📐 รูปสองเท่ากัน']),

    M('R132C098','สูตรของ <strong>แรงสู่ศูนย์กลาง F_c</strong>?',
      ['F_c = mv²/r','F_c = mv/r','F_c = mr/v²','F_c = mω/r'],'A',
      ['💡 F = ma → F_c = m·a_c = m(v²/r)','🔍 = mv²/r','📐 หรือ mω²R · m(2π/T)²R · m(2πf)²R']),

    M('R132C099','สูตร F_c ในรูปเชิงมุม?',
      ['F_c = mωR','F_c = mω²R','F_c = mω/R','F_c = mω²/R'],'B',
      ['💡 F_c = m·a_c = mω²R','🔍 ใช้เมื่อโจทย์ให้ ω หรือ T, f','📐 เทียบเท่า mv²/r']),

    F('R132C100','m = 2 kg · v = 10 m/s · r = 5 m → F_c เท่ากับ (N)?', 40, 'N',
      ['💡 F_c = mv²/r','🔍 = 2 × 100/5','📐 = 40 N']),

    F('R132C101','m = 1 kg · v = 4 m/s · r = 2 m → F_c (N)?', 8, 'N',
      ['💡 F_c = mv²/r','🔍 = 1 × 16/2','📐 = 8 N']),

    F('R132C102','m = 0.5 kg · ω = 4 rad/s · R = 2 m → F_c (N)?', 16, 'N',
      ['💡 F_c = mω²R','🔍 = 0.5 × 16 × 2','📐 = 16 N']),

    F('R132C103','v = 10 m/s · r = 5 m → a_c (m/s²)?', 20, 'm/s²',
      ['💡 a_c = v²/r','🔍 = 100/5','📐 = 20 m/s²']),

    M('R132C104','หน่วย SI ของ <strong>F_c</strong>?',
      ['kg','m/s²','N (Newton)','rad'],'C',
      ['💡 F_c เป็น "แรง" → หน่วย N','🔍 N = kg·m/s²','📐 ตรวจ: kg × m²/s² × 1/m = kg·m/s²']),

    M('R132C105','หน่วย SI ของ <strong>a_c</strong>?',
      ['m/s','m/s²','rad/s','N'],'B',
      ['💡 ความเร่ง — หน่วยเหมือน a ทั่วไป','🔍 m/s²','📐 ไม่ขึ้นกับชนิดของการเคลื่อนที่']),

    F('R132C106','m = 1 kg · ω = 2 rad/s · R = 5 m → F_c (N)?', 20, 'N',
      ['💡 F_c = mω²R','🔍 = 1 × 4 × 5','📐 = 20 N']),

    M('R132C107','ทิศของ F_c คือ?',
      ['ทิศ v (แนวสัมผัส)','เข้าหาศูนย์กลาง','ออกจากศูนย์กลาง','ขนานแกนหมุน'],'B',
      ['💡 F_c = m·a_c · ทิศ a_c เข้าศูนย์','🔍 ดังนั้น F_c เข้าศูนย์เสมอ','📐 ตั้งฉากกับ v']),

    // ════════ B3 — ผันผัน v, r, m, ω, f, T (R132C108-117 · 10) ════════
    M('R132C108','ถ้า <strong>v เพิ่ม 2 เท่า</strong> (m, r เดิม) F_c เป็นกี่เท่า?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'B',
      ['💡 F_c = mv²/r → v² → (2v)² = 4v²','🔍 F_c × 4','📐 ความเร็วมีผลแบบกำลัง 2']),

    M('R132C109','ถ้า <strong>r เพิ่ม 2 เท่า</strong> (m, v เดิม) F_c เป็น?',
      ['2 เท่า','4 เท่า','1/2 เท่า','1/4 เท่า'],'C',
      ['💡 r อยู่ตัวหาร → r × 2 → F_c × 1/2','🔍 รัศมีกว้างขึ้น → ต้องการแรงน้อยลง','📐 รถเลี้ยวโค้งกว้างขึ้น = ปลอดภัยกว่า']),

    M('R132C110','ถ้า <strong>m เพิ่ม 2 เท่า</strong> (v, r เดิม) F_c?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'A',
      ['💡 m อยู่ตัวคูณ','🔍 m × 2 → F_c × 2','📐 มวลมาก → ต้องการแรงมาก']),

    M('R132C111','ถ้า <strong>ω เพิ่ม 2 เท่า</strong> (m, R เดิม) F_c?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'B',
      ['💡 F_c = mω²R · ω² → (2ω)² = 4ω²','🔍 F_c × 4','📐 หรือคิดผ่าน v=ωR — v×2 → v²×4']),

    M('R132C112','ถ้า <strong>f เพิ่ม 2 เท่า</strong> (m, R เดิม) F_c?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'B',
      ['💡 ω = 2πf → f×2 → ω×2','🔍 F_c ∝ ω² → × 4','📐 รอบเร็วขึ้น 2 เท่า → F ต้องเพิ่ม 4']),

    M('R132C113','ถ้า <strong>T เพิ่ม 2 เท่า</strong> (m, R เดิม) F_c?',
      ['2 เท่า','4 เท่า','1/4 เท่า','1/2 เท่า'],'C',
      ['💡 ω = 2π/T → T×2 → ω×1/2','🔍 F_c ∝ ω² → × 1/4','📐 หมุนช้าลง → F น้อยลง']),

    M('R132C114','ถ้า <strong>r ลด 1/2</strong> · v เดิม → F_c?',
      ['1/2 เท่า','เท่าเดิม','2 เท่า','4 เท่า'],'C',
      ['💡 r × 1/2 → 1/r × 2 → F_c × 2','🔍 รัศมีน้อยลง → ต้องการ F มากขึ้น','📐 (โจทย์ข้อ 17 ในชีท)']),

    F('R132C115','v × 3, r × 3, m เดิม → F_c เป็นกี่เท่าของเดิม?', 3, 'เท่า',
      ['💡 F_c × (3²/3) = 9/3','🔍 = 3','📐 v² ทำให้กำลัง 2 · r ทำให้หาร']),

    M('R132C116','ถ้าต้องการ F_c × 9 ที่ r, m เดิม → v ต้อง × ?',
      ['3','9','81','√3'],'A',
      ['💡 F_c ∝ v² → ต้องการ × 9 → v² × 9 → v × 3','🔍 v × 3','📐 รากที่สองของอัตราส่วน']),

    F('R132C117','m, r เดิม · v เพิ่ม 3 เท่า → F_c เป็นกี่เท่า?', 9, 'เท่า',
      ['💡 F_c ∝ v²','🔍 v × 3 → v² × 9','📐 F_c × 9']),

    // ════════ B4 — 13 Pattern · เลือกแรง F_c (R132C118-133 · 16) ════════
    M('R132C118','<strong>แกว่งวัตถุในแนวระดับด้วยเชือก</strong> — แรงตึงเชือก T = ?',
      ['T = mg','T = mv²/r','T = mg + mv²/r','T = mg − mv²/r'],'B',
      ['💡 บนแนวระดับ — เชือกขนานพื้น = F_c','🔍 T = F_c = mv²/r','📐 W ลง — ตั้งฉากกับเชือก ไม่เกี่ยว'],
      SVG_HSWING),

    F('R132C119','แกว่งวัตถุ m=1 kg ในแนวระดับ · v=2 m/s · r=1 m → T (N)?', 4, 'N',
      ['💡 T = mv²/r','🔍 = 1 × 4/1','📐 = 4 N'],
      SVG_HSWING),

    M('R132C120','<strong>conical pendulum</strong> (เชือกแกว่งเป็นกรวย) — F_c มาจาก?',
      ['T (เชือกทั้งหมด)','W (น้ำหนักทั้งหมด)','T sinα (component แนวนอน)','T cosα'],'C',
      ['💡 T เอียง · แตกเป็น 2 แกน','🔍 แนวดิ่ง: T cosα = W (สมดุล)','📐 แนวนอน: T sinα = F_c = mv²/r'],
      SVG_CONICAL),

    M('R132C121','<strong>vertical loop</strong> ที่ <strong>จุดสูงสุด</strong> — F_c = ?',
      ['T − W','T + W (ทั้งคู่ลง = เข้าศูนย์)','W − T','T เพียง'],'B',
      ['💡 ที่บน — T ลง · W ลง · ทั้งคู่เข้าศูนย์','🔍 F_c = T + W = mv²/r','📐 (O-NET 52)'],
      SVG_VLOOP_FORCES),

    M('R132C122','<strong>vertical loop</strong> ที่ <strong>จุดต่ำสุด</strong> — F_c = ?',
      ['T + W','T − W','W − T','T เพียง'],'B',
      ['💡 ที่ล่าง — T ขึ้น (เข้าศูนย์) · W ลง (ออก)','🔍 F_c = T − W = mv²/r','📐 → T = mg + mv²/r (สูงสุด)']),

    M('R132C123','<strong>vertical loop</strong> ที่ <strong>ตำแหน่ง 3 หรือ 9 นาฬิกา</strong> — F_c = ?',
      ['T + W','T − W','T เพียง','W เพียง'],'C',
      ['💡 ตำแหน่งนี้ — เชือกแนวระดับ ดึงเข้าศูนย์','🔍 W ลงในแนวดิ่ง — ตั้งฉากกับเชือก ไม่เกี่ยว F_c','📐 T = F_c = mv²/r']),

    M('R132C124','<strong>วัตถุบนจานหมุน</strong> หมุนตามจาน — F_c มาจาก?',
      ['แรงเสียดทานจลน์','แรงเสียดทานสถิต f_s','แรงตั้งฉาก N','แรงโน้มถ่วง'],'B',
      ['💡 จานหมุน → ดันวัตถุออก (inertia)','🔍 f_s ดึงให้วัตถุหมุนตาม → ทิศเข้าศูนย์','📐 ถ้า ω มาก → f_s ไม่พอ → ไถลออก'],
      SVG_DISC),

    M('R132C125','<strong>รถบนยอดเนิน</strong> (top of hill) — F_c = ?',
      ['N − W','W − N (W มากกว่า N)','N + W','W เพียง'],'B',
      ['💡 ที่ยอดเนิน — ศูนย์อยู่ "ล่าง"','🔍 W ลง (เข้าศูนย์) · N ขึ้น (ออก) → F_c = W − N','📐 ดังนั้น N < W → "เบา" กว่าปกติ'],
      SVG_HILL_TOP),

    F('R132C126','รถ m=60 kg ที่ยอดเนินรัศมี 100 m · v=20 m/s · g=10 → F_c (N)?', 240, 'N',
      ['💡 F_c = mv²/r','🔍 = 60 × 400/100','📐 = 240 N'],
      SVG_HILL_TOP),

    M('R132C127','<strong>รถในร่อง (valley)</strong> ที่ก้นโค้ง — F_c = ?',
      ['W − N','N − W (N มากกว่า W)','W + N','N เพียง'],'B',
      ['💡 ที่ก้นร่อง — ศูนย์อยู่ "บน"','🔍 N ขึ้น (เข้าศูนย์) · W ลง (ออก) → F_c = N − W','📐 → N > W → "หนัก" กว่าปกติ'],
      SVG_VALLEY),

    M('R132C128','<strong>รถเลี้ยวบนถนนราบ</strong> (ไม่ยกสูง) — F_c มาจาก?',
      ['น้ำหนัก W','แรงเสียดทานสถิตของยาง f_s','แรงตั้งฉาก N','แรงเครื่องยนต์'],'B',
      ['💡 N, W หักล้างแนวดิ่ง','🔍 f_s ในแนวระดับ ดึงเข้าศูนย์ = F_c','📐 f_s,max = μN = μmg'],
      SVG_FLATCURVE),

    M('R132C129','<strong>รถเลี้ยวบนถนนยกสูง (banked)</strong> · ไม่มีเสียดทาน — F_c มาจาก?',
      ['W เพียง','N เพียง','N sinθ (component แนวระดับของ N)','N + W'],'C',
      ['💡 N ตั้งฉากกับผิวเอียง → เอียงเข้าศูนย์','🔍 แตก N: แนวดิ่ง N cosθ=W · แนวนอน N sinθ=F_c','📐 tanθ = v²/(rg)'],
      SVG_BANKED_B),

    M('R132C130','<strong>มอเตอร์ไซค์เอียงเข้าโค้ง</strong> — มุมเอียง θ?',
      ['tanθ = v/r','tanθ = v²/(rg)','tanθ = mg/v','tanθ = r/v'],'B',
      ['💡 tanθ = F_c/W = (mv²/r)/(mg)','🔍 = v²/(rg)','📐 ไม่ขึ้นกับมวลรถ'],
      SVG_BIKE),

    M('R132C131','<strong>วัตถุติดผนังถังหมุน (rotor)</strong> — F_c มาจาก?',
      ['แรงเสียดทาน f_s','น้ำหนัก W','แรงตั้งฉาก N (จากผนัง)','แรงตึงเชือก'],'C',
      ['💡 ผนังดันวัตถุเข้าศูนย์','🔍 N (จากผนัง) = F_c','📐 f_s ในแนวดิ่ง — ค้านน้ำหนักไม่ให้ตก'],
      SVG_ROTOR),

    M('R132C132','<strong>ดาวเทียมโคจร</strong> — F_c มาจาก?',
      ['แรงตึงเชือก','แรงโน้มถ่วงระหว่างดาวเทียมกับโลก','แรงเสียดทานในอวกาศ','แรงผลักจากเครื่องยนต์'],'B',
      ['💡 ดาวเทียม "ตก" เข้าหาโลกตลอด','🔍 F_grav = F_c = mv²/r','📐 ในอวกาศไม่มีเสียดทาน'],
      SVG_ORBIT),

    CHK('R132C133','จับคู่ <strong>"แรงที่ทำหน้าที่ F_c"</strong> ที่ <strong>ถูก</strong>',
      ['แกว่งราบ → T','ดาวเทียม → F_grav','รถบนยอดเนิน → W − N','vertical loop จุดล่าง → T − W','banked ไร้เสียดทาน → N sinθ','rotor → f_s'],
      [1,2,3,4,5],
      ['💡 6 ผิด — rotor ใช้ N (จากผนัง) ไม่ใช่ f_s','🔍 f_s ใน rotor ค้านน้ำหนักในแนวดิ่ง','📐 รวบยอด 13 pattern']),

    // ════════ B5 — vertical loop (R132C134-143 · 10) ════════
    M('R132C134','<strong>v_min ที่จุดสูงสุด</strong> ของ vertical loop (T = 0) คือ?',
      ['v_min = √(gR)','v_min = √(2gR)','v_min = gR','v_min = 0'],'A',
      ['💡 ที่ v_min · T = 0 · F_c = W = mg','🔍 mg = mv²/R → v² = gR','📐 v_min = √(gR)']),

    F('R132C135','vertical loop รัศมี r = 10 m · g = 10 → v_min ที่จุดสูงสุด (m/s)?', 10, 'm/s',
      ['💡 v_min = √(gR)','🔍 = √(10 × 10)','📐 = 10 m/s']),

    F('R132C136','vertical loop r = 2.5 m · g = 10 → v_min ที่บน (m/s)?', 5, 'm/s',
      ['💡 v_min = √(gR)','🔍 = √(10 × 2.5) = √25','📐 = 5 m/s']),

    M('R132C137','สูตร <strong>แรงตึง T ที่จุดบน</strong> ของ vertical loop?',
      ['T = mv²/r','T = mv²/r − mg','T = mv²/r + mg','T = mg − mv²/r'],'B',
      ['💡 ที่บน F_c = T + W → T = F_c − W','🔍 T = mv²/r − mg','📐 T น้อยที่สุดที่จุดบน']),

    M('R132C138','สูตร <strong>แรงตึง T ที่จุดล่าง</strong> ของ vertical loop?',
      ['T = mv²/r','T = mv²/r − mg','T = mv²/r + mg','T = mg − mv²/r'],'C',
      ['💡 ที่ล่าง F_c = T − W → T = F_c + W','🔍 T = mv²/r + mg','📐 T สูงสุดที่จุดล่าง']),

    F('R132C139','m=2 kg · v=10 m/s · r=5 m · g=10 → T ที่จุดบน (N)?', 20, 'N',
      ['💡 T = mv²/r − mg','🔍 = 2×100/5 − 2×10 = 40 − 20','📐 = 20 N']),

    F('R132C140','m=2 kg · v=10 m/s · r=5 m · g=10 → T ที่จุดล่าง (N)?', 60, 'N',
      ['💡 T = mv²/r + mg','🔍 = 40 + 20','📐 = 60 N']),

    M('R132C141','ที่ <strong>v_min ที่จุดบน</strong> · T มีค่าเท่าใด?',
      ['T = mv²/r','T = mg','T = 0','T = 2mg'],'C',
      ['💡 v_min คือเงื่อนไข T = 0 พอดี','🔍 ลึกกว่า v_min → ตกได้','📐 ที่ v_min: F_c = W (โดย W ทำหน้าที่ F_c คนเดียว)']),

    F('R132C142','m=1 kg · v=5 m/s · r=2.5 m · g=10 → T_bottom − T_top (N)?', 20, 'N',
      ['💡 T_bot − T_top = (mv²/r + mg) − (mv²/r − mg) = 2mg','🔍 = 2 × 1 × 10','📐 = 20 N · เท่ากับ 2W เสมอ']),

    CHK('R132C143','vertical loop · เลือกข้อที่ <strong>ถูก</strong>',
      ['T สูงสุดที่จุดล่าง','T น้อยที่สุดที่จุดบน','v_min ที่บน = √(gR)','ที่บน T = 0 ⟺ v = v_min','T ที่บน = mv²/r + mg','T_bottom − T_top = 2mg เสมอ'],
      [1,2,3,4,6],
      ['💡 5 ผิด — ที่บน T = mv²/r − mg','🔍 ใช้สรุปแก่นของ vertical loop','📐 ความต่าง T_bot − T_top = 2mg ไม่ขึ้นกับ v']),

    // ════════ B6 — banked + conical pendulum (R132C144-153 · 10) ════════
    M('R132C144','สูตรของมุม <strong>banked</strong> ที่ไม่ต้องอาศัยเสียดทาน?',
      ['tanθ = v/(rg)','tanθ = v²/(rg)','tanθ = vrg','tanθ = m·g/v²'],'B',
      ['💡 จาก N sinθ = mv²/r และ N cosθ = mg','🔍 หาร: tanθ = v²/(rg)','📐 ไม่ขึ้นกับมวลรถ']),

    F('R132C145','banked curve · v=10 m/s · r=20 m · g=10 → tanθ?', 0.5, '',
      ['💡 tanθ = v²/(rg)','🔍 = 100/(20×10) = 100/200','📐 = 0.5']),

    F('R132C146','banked · v=20 m/s · r=40 m · g=10 → tanθ?', 1, '',
      ['💡 tanθ = v²/(rg)','🔍 = 400/(40×10) = 400/400','📐 = 1 (มุม 45°)']),

    M('R132C147','มุม banked ที่ออกแบบสำหรับ v_design — <strong>ขึ้นกับมวลรถหรือไม่</strong>?',
      ['ขึ้นกับมวลรถ','ไม่ขึ้นกับมวลรถ (ขึ้นเฉพาะ v, r, g)','ขึ้นกับมวลรถและ v','ขึ้นกับน้ำหนัก'],'B',
      ['💡 tanθ = v²/(rg) — ไม่มี m','🔍 รถทุกขนาดผ่านโค้งได้ที่ v_design','📐 จึงออกแบบมุมเดียวให้ทุกรถ']),

    M('R132C148','<strong>conical pendulum</strong> สมดุลแนวดิ่ง — สมการคือ?',
      ['T cosα = mg','T sinα = mg','T = mg','T sinα = mg cosα'],'A',
      ['💡 แนวดิ่งสมดุล: T cosα = W','🔍 T cosα = mg','📐 องค์ประกอบของ T ในแนวดิ่ง = น้ำหนัก'],
      SVG_CONICAL),

    M('R132C149','conical pendulum · F_c ในแนวระดับ — สมการคือ?',
      ['T cosα = mv²/r','T sinα = mv²/r','T = mv²/r','T sinα = mg'],'B',
      ['💡 แนวระดับ: T sinα = F_c = mv²/r','🔍 ใช้คู่กับ T cosα = mg','📐 หาร: tanα = v²/(rg)'],
      SVG_CONICAL),

    M('R132C150','conical pendulum · ω ในรูป L (ความยาวเชือก) และ α?',
      ['ω = √(g·L)','ω = √(g/(L cosα))','ω = √(L cosα/g)','ω = g/(L sinα)'],'B',
      ['💡 r = L sinα · จาก tanα = ω²r/g','🔍 ω² = g·tanα/r = g·tanα/(L sinα) = g/(L cosα)','📐 ω = √(g/(L cosα))']),

    M('R132C151','conical pendulum · เพิ่มมุม α (เอียงมากขึ้น) → ω?',
      ['ลดลง','คงเดิม','เพิ่มขึ้น','เป็น 0'],'C',
      ['💡 ω = √(g/(L cosα))','🔍 α เพิ่ม → cosα ลด → ตัวหารลด → ω เพิ่ม','📐 หมุนเร็วขึ้น เอียงมากขึ้น']),

    M('R132C152','conical pendulum · ω เพิ่ม → r เป็นอย่างไร?',
      ['คงเดิม','ลดลง','เพิ่มขึ้น','เป็น 0'],'C',
      ['💡 ω เพิ่ม → α เพิ่ม (เอียงมากขึ้น)','🔍 r = L sinα → α เพิ่ม → r เพิ่ม','📐 หมุนเร็ว → กรวยกว้างขึ้น']),

    CHK('R132C153','banked + conical · เลือกข้อที่ <strong>ถูก</strong>',
      ['banked tanθ = v²/(rg) ไม่ขึ้นกับมวล','conical T cosα = mg','conical T sinα = mv²/r','conical ω = √(g/(L cosα))','banked มุมเพิ่ม → v_design เพิ่ม','banked สูตรขึ้นกับ μ ของยาง'],
      [1,2,3,4,5],
      ['💡 6 ผิด — banked แบบ ideal (no friction) ไม่ขึ้นกับ μ','🔍 5 ถูก — มุมชันขึ้น → v_design ที่ปลอดภัยสูงขึ้น','📐 ทั้ง 2 รูปแบบ: F_c มาจากองค์ประกอบของ T หรือ N']),

    // ════════ B7 — satellite / orbital (R132C154-160 · 7) ════════
    M('R132C154','<strong>ดาวเทียมโคจร</strong> · ใช้สมการ F_grav = F_c — สูตรคือ?',
      ['mg_orbit = mv²/r','mg = mv','m·g = m','mg_orbit = mv'],'A',
      ['💡 F_grav = mg_orbit (g_orbit = field strength ที่นั่น)','🔍 F_grav = F_c → mg_orbit = mv²/r','📐 จัดใหม่: v² = g_orbit · r'],
      SVG_ORBIT),

    M('R132C155','สูตร <strong>ความเร็วโคจร v</strong> ของดาวเทียม?',
      ['v = √(g_orbit/r)','v = √(g_orbit · r)','v = g_orbit · r','v = g_orbit/r'],'B',
      ['💡 mg_orbit = mv²/r → v² = g_orbit · r','🔍 v = √(g_orbit · r)','📐 ดาวเทียมต่ำกว่า → v มากกว่า (g มาก, r น้อย)'],
      SVG_ORBIT),

    F('R132C156','ดาวเทียมโคจรรัศมี r = 8×10⁶ m · g_orbit = 8 N/kg → v (m/s)?', 8000, 'm/s',
      ['💡 v = √(g_orbit · r)','🔍 = √(8 × 8×10⁶) = √(64×10⁶)','📐 = 8000 m/s']),

    M('R132C157','สูตร <strong>คาบการโคจร T</strong>?',
      ['T = 2π/v','T = 2πr/v','T = v/(2πr)','T = r/v'],'B',
      ['💡 1 รอบ = ระยะ 2πr · ใช้เวลา T','🔍 T = 2πr/v','📐 ดาวเทียมต่ำ → v มาก → T น้อย']),

    F('R132C158','ดาวเทียม v=7000 m/s · r=7×10⁶ m → T (s) (ใช้ π=3.14)?', 6280, 's',
      ['💡 T = 2πr/v','🔍 = 2π × 7×10⁶/7000 = 2π × 1000','📐 = 2000π ≈ 6280 s']),

    M('R132C159','ถ้า g_orbit ที่ระดับนั้น <strong>เพิ่มขึ้น</strong> (โคจรต่ำลง) → v_orbit?',
      ['ลดลง','คงเดิม','เพิ่มขึ้น','เป็น 0'],'C',
      ['💡 v = √(g_orbit · r)','🔍 g_orbit เพิ่ม → v เพิ่ม','📐 ดาวเทียมโคจรต่ำ = เร็วกว่า']),

    CHK('R132C160','satellite/orbital · เลือกข้อที่ <strong>ถูก</strong>',
      ['F_grav ทำหน้าที่ F_c','v = √(g_orbit · r)','T = 2πr/v','ดาวเทียมต่ำ → T น้อยกว่าดาวเทียมสูง','v ดาวเทียมไม่ขึ้นกับมวลของดาวเทียม','ดาวเทียมต้องใช้เครื่องยนต์ตลอดเพื่อโคจร'],
      [1,2,3,4,5],
      ['💡 6 ผิด — โคจรเป็นการ "ตก" ตามแรงโน้มถ่วง · ไม่ใช้เครื่องยนต์','🔍 5 ถูก — v ขึ้นกับ g_orbit, r เท่านั้น','📐 ดาวเทียมเล็ก/ใหญ่ที่โคจรเดียวกัน v เท่ากัน'])
  ];

  window.QUESTIONS_R132_B = Q;
  if(window.console && console.log) console.log('[Region 1.3.2 Stage B] loaded', Q.length, '/ 80 questions');
})();
