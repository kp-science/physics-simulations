/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.3.3 เนินสปริง (SHM)
   Stage B "ใช้สูตรไหน" · 70 ข้อ · noReveal pattern
   MCQ + FILL · ดึงสูตร + ใส่ตัวเลข · ใช้ g = 10 · π ≈ 3.14

   หมวด:
     B1 ω, T, f · v_max, a_max สูตร      (R133S071-080 · 10)
     B2 a = −ω²x · v ที่ตำแหน่ง x          (R133S081-090 · 10)
     B3 ผันผัน m, k, L, A, ω             (R133S091-100 · 10)
     B4 x, v, a, KE, PE ⭐                (R133S101-115 · 15)
     B5 Spring T = 2π√(m/k) calc          (R133S116-130 · 15)
     B6 Pendulum T = 2π√(L/g) calc        (R133S131-140 · 10)
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  const F_TAG = ['shm-b'];

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

  // ─── SVG library (compact · reuse จาก Stage A SHM) ───
  const SVG_SPRING = '<svg viewBox="0 0 280 100" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="80" x2="270" y2="80" stroke="#fff" stroke-width="1.2"/><line x1="10" y1="20" x2="10" y2="90" stroke="#fbbf24" stroke-width="2"/><path d="M 10 50 L 20 45 L 25 55 L 30 45 L 35 55 L 40 45 L 45 55 L 50 50 L 70 50" fill="none" stroke="#34d399" stroke-width="1.5"/><rect x="70" y="40" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1"/><text x="40" y="35" fill="#a78bfa" font-size="9">−A</text><path d="M 10 50 L 30 45 L 40 55 L 50 45 L 60 55 L 70 45 L 80 55 L 90 45 L 100 55 L 110 50 L 130 50" fill="none" stroke="#34d399" stroke-width="1.5" opacity="0.5"/><rect x="130" y="40" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1" opacity="0.5"/><line x1="141" y1="65" x2="141" y2="92" stroke="#fbbf24" stroke-width="1" stroke-dasharray="2,2"/><text x="135" y="98" fill="#fbbf24" font-size="9">x=0</text><path d="M 10 50 L 40 45 L 60 55 L 80 45 L 100 55 L 120 45 L 140 55 L 160 45 L 180 50 L 200 50" fill="none" stroke="#34d399" stroke-width="1.5" opacity="0.3"/><rect x="200" y="40" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1" opacity="0.3"/><text x="207" y="35" fill="#a78bfa" font-size="9">+A</text></svg>';

  const SVG_PEND = '<svg viewBox="0 0 200 180" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="15" x2="180" y2="15" stroke="#fff" stroke-width="2"/><line x1="100" y1="15" x2="100" y2="140" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3"/><line x1="100" y1="15" x2="60" y2="135" stroke="#34d399" stroke-width="2"/><circle cx="60" cy="135" r="10" fill="#fbbf24" stroke="#fff" stroke-width="1"/><path d="M 100 60 A 50 50 0 0 0 75 50" fill="none" stroke="#a78bfa" stroke-width="1.2"/><text x="78" y="55" fill="#a78bfa" font-size="11">θ</text><text x="115" y="80" fill="#34d399" font-size="11" font-weight="700">L</text></svg>';

  const SVG_VAX = '<svg viewBox="0 0 280 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="100" x2="270" y2="100" stroke="#fff" stroke-width="1.2"/><line x1="10" y1="40" x2="10" y2="110" stroke="#fbbf24" stroke-width="2"/><path d="M 10 70 L 20 65 L 25 75 L 30 65 L 35 75 L 40 65 L 45 75 L 50 70 L 70 70" fill="none" stroke="#34d399" stroke-width="1.2"/><rect x="70" y="60" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1"/><text x="60" y="55" fill="#fff" font-size="9">x=+A</text><line x1="81" y1="50" x2="81" y2="35" stroke="#34d399" stroke-width="2"/><polygon points="81,32 78,38 84,38" fill="#34d399"/><text x="60" y="30" fill="#34d399" font-size="9" font-weight="700">a=max</text><text x="100" y="75" fill="#fbbf24" font-size="9">v=0</text><rect x="160" y="60" width="22" height="20" fill="#38bdf8" stroke="#fff" stroke-width="1"/><text x="155" y="55" fill="#fff" font-size="9">x=0</text><line x1="180" y1="68" x2="220" y2="68" stroke="#fbbf24" stroke-width="2.5"/><polygon points="223,68 217,65 217,71" fill="#fbbf24"/><text x="190" y="63" fill="#fbbf24" font-size="9" font-weight="700">v=max</text><text x="190" y="92" fill="#a78bfa" font-size="9">a=0</text></svg>';

  const SVG_XT = '<svg viewBox="0 0 240 130" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="65" x2="225" y2="65" stroke="#fff" stroke-width="1.2"/><line x1="20" y1="15" x2="20" y2="115" stroke="#fff" stroke-width="1.2"/><polygon points="225,65 218,62 218,68" fill="#fff"/><polygon points="20,8 17,18 23,18" fill="#fff"/><text x="6" y="22" fill="#fbbf24" font-size="10">x</text><text x="220" y="80" fill="#fbbf24" font-size="10">t</text><path d="M 20 65 Q 40 20 60 20 Q 80 20 100 65 Q 120 110 140 110 Q 160 110 180 65 Q 200 20 220 20" fill="none" stroke="#34d399" stroke-width="2"/><line x1="20" y1="20" x2="225" y2="20" stroke="#a78bfa" stroke-width="0.8" stroke-dasharray="2,2"/><line x1="20" y1="110" x2="225" y2="110" stroke="#a78bfa" stroke-width="0.8" stroke-dasharray="2,2"/><text x="0" y="24" fill="#a78bfa" font-size="9">+A</text><text x="0" y="114" fill="#a78bfa" font-size="9">−A</text><line x1="120" y1="65" x2="120" y2="115" stroke="#fbbf24" stroke-width="0.8" stroke-dasharray="2,2"/><text x="105" y="125" fill="#fbbf24" font-size="9">T (1 รอบ)</text></svg>';

  const Q = [
    // ════════ B1 — ω, T, f · v_max, a_max สูตร (R133S071-080 · 10) ════════
    M('R133S071','สูตรของ <strong>ω (angular frequency)</strong> ในรูปคาบ T?',
      ['ω = T','ω = 2π/T','ω = 2πT','ω = T/(2π)'],'B',
      ['💡 SHM ใช้สูตรเดียวกับ UCM','🔍 ω = 2π/T','📐 หน่วย rad/s']),

    M('R133S072','สูตรของ ω ในรูป f?',
      ['ω = f','ω = 2πf','ω = πf','ω = f/2π'],'B',
      ['💡 ω = 2πf','🔍 หรือ ω = 2π/T และ T = 1/f','📐 หน่วย rad/s']),

    M('R133S073','สูตร <strong>v_max</strong> ใน SHM?',
      ['v_max = A','v_max = ω','v_max = ωA','v_max = ω²A'],'C',
      ['💡 v_max = ωA','🔍 เกิดที่ตำแหน่งสมดุล (x=0)','📐 จาก projection ของ UCM (v_UCM = ωR)']),

    M('R133S074','สูตร <strong>a_max</strong> ใน SHM?',
      ['a_max = A','a_max = ωA','a_max = ω²A','a_max = ω/A'],'C',
      ['💡 |a| = ω²|x| → max ที่ |x|=A','🔍 a_max = ω²A','📐 เกิดที่ extremes (x=±A)'],
      SVG_VAX),

    M('R133S075','สำหรับ <strong>Spring SHM</strong> ω² = ?',
      ['k/m','m/k','km','k+m'],'A',
      ['💡 ω² = k/m → ω = √(k/m)','🔍 จาก a = −(k/m)x = −ω²x','📐 spring แข็ง (k มาก) → ω มาก']),

    F('R133S076','T = 2 s → ω เท่ากับ (rad/s)? (π = 3.14)', 3.14, 'rad/s',
      ['💡 ω = 2π/T','🔍 = 2π/2 = π','📐 ≈ 3.14']),

    F('R133S077','f = 4 Hz → ω เท่ากับ (rad/s)? (π = 3.14)', 25.12, 'rad/s',
      ['💡 ω = 2πf','🔍 = 2π × 4 = 8π','📐 ≈ 25.12']),

    F('R133S078','ω = 10 rad/s · A = 0.5 m → v_max (m/s)?', 5, 'm/s',
      ['💡 v_max = ωA','🔍 = 10 × 0.5','📐 = 5 m/s']),

    F('R133S079','ω = 10 rad/s · A = 0.5 m → a_max (m/s²)?', 50, 'm/s²',
      ['💡 a_max = ω²A','🔍 = 100 × 0.5','📐 = 50 m/s²']),

    M('R133S080','หน่วยของ <strong>ω</strong> ใน SHM?',
      ['m/s','m/s²','rad/s','Hz·m'],'C',
      ['💡 ω = θ/t · rad/s','🔍 ω = 2πf → Hz × rad = rad/s','📐 v_max=ωA: rad/s × m = m/s ✓']),

    // ════════ B2 — a = −ω²x · v ที่ตำแหน่ง x (R133S081-090 · 10) ════════
    M('R133S081','สูตรของ <strong>ความเร่ง a ที่ตำแหน่ง x</strong>?',
      ['a = ω²x','a = −ω²x','a = ωx','a = −ωx'],'B',
      ['💡 a = −ω²x','🔍 เครื่องหมายลบ = ทิศตรงข้ามกับ x','📐 หัวใจของ SHM']),

    F('R133S082','ω = 2 rad/s · x = 0.5 m → ขนาด a (m/s²)?', 2, 'm/s²',
      ['💡 |a| = ω²|x|','🔍 = 4 × 0.5','📐 = 2 m/s²']),

    M('R133S083','ที่ x = +A → a = ?',
      ['+ω²A','−ω²A','0','+ωA'],'B',
      ['💡 a = −ω²(+A) = −ω²A','🔍 ขนาด ω²A · ทิศซ้าย','📐 a สูงสุดที่ extremes'],
      SVG_VAX),

    F('R133S084','ω = 4 rad/s · A = 0.5 m → a_max (m/s²)?', 8, 'm/s²',
      ['💡 a_max = ω²A','🔍 = 16 × 0.5','📐 = 8 m/s²']),

    M('R133S085','สูตร <strong>v ที่ตำแหน่ง x</strong>?',
      ['v = ωA','v = ω(A−x)','v = ±ω√(A²−x²)','v = ω·x'],'C',
      ['💡 จากอนุรักษ์พลังงาน: ½mv² = ½k(A²−x²)','🔍 v = ±ω√(A²−x²)','📐 ที่ x=0 → v=ωA · ที่ x=A → v=0']),

    M('R133S086','ที่ x = 0 → v = ?',
      ['0','ωA (v_max)','A','ω'],'B',
      ['💡 v = ω√(A² − 0) = ωA','🔍 ที่สมดุล v สูงสุด','📐 เพราะ KE สูงสุด, PE=0']),

    M('R133S087','ที่ x = ±A → v = ?',
      ['v_max','ωA','0','ω/A'],'C',
      ['💡 v = ω√(A² − A²) = 0','🔍 ที่ extremes วัตถุพอดีกลับทิศ','📐 KE = 0 · PE สูงสุด']),

    F('R133S088','A = 2 m · x = 1 m · ω = 2 rad/s → v (m/s)? (√3 ≈ 1.73)', 3.46, 'm/s',
      ['💡 v = ω√(A² − x²)','🔍 = 2√(4 − 1) = 2√3','📐 ≈ 2 × 1.73 = 3.46']),

    M('R133S089','ที่ <strong>x = A/2</strong> → ขนาด v = ?',
      ['ωA','ωA·√3/2','ωA/2','0'],'B',
      ['💡 v = ω√(A² − A²/4) = ω·A√(3/4)','🔍 = ωA√3/2','📐 ≈ 0.866 × v_max']),

    M('R133S090','พลังงานจลน์สูงสุด (KE_max) เกิดที่ตำแหน่งใด?',
      ['x = +A','x = −A','x = 0 (สมดุล)','x = A/2'],'C',
      ['💡 KE = ½mv² → max ที่ v_max','🔍 v_max ที่ x=0','📐 KE_max = ½mω²A²']),

    // ════════ B3 — ผันผัน m, k, L, A, ω (R133S091-100 · 10) ════════
    M('R133S091','Spring SHM · m เพิ่ม 4 เท่า (k เดิม) → T เป็นกี่เท่า?',
      ['2 เท่า','4 เท่า','1/2','คงเดิม'],'A',
      ['💡 T ∝ √m','🔍 m×4 → √4 = 2','📐 T × 2']),

    M('R133S092','Spring SHM · k เพิ่ม 4 เท่า (m เดิม) → T เป็น?',
      ['2 เท่า','4 เท่า','1/2 เท่า','1/4 เท่า'],'C',
      ['💡 T ∝ 1/√k','🔍 k×4 → 1/√4 = 1/2','📐 T × 1/2']),

    M('R133S093','Spring · m×4 + k×4 พร้อมกัน → T เป็น?',
      ['คงเดิม','2 เท่า','4 เท่า','1/2 เท่า'],'A',
      ['💡 T ∝ √(m/k)','🔍 m/k = (4m)/(4k) = m/k → ไม่เปลี่ยน','📐 T เท่าเดิม']),

    M('R133S094','Pendulum · L เพิ่ม 4 เท่า · g เดิม → T เป็น?',
      ['2 เท่า','4 เท่า','1/2 เท่า','คงเดิม'],'A',
      ['💡 T ∝ √L','🔍 L×4 → √4 = 2','📐 T × 2']),

    M('R133S095','Pendulum · L ลด 1/4 เท่า · g เดิม → T เป็น?',
      ['2 เท่า','4 เท่า','1/2 เท่า','1/4 เท่า'],'C',
      ['💡 T ∝ √L','🔍 L×1/4 → √(1/4) = 1/2','📐 T × 1/2'],
      SVG_PEND),

    M('R133S096','Pendulum ไป <strong>ดาวอังคาร (g_Mars ≈ 4 m/s²)</strong> · L เดิม → T?',
      ['คงเดิม','น้อยลง √2.5 เท่า','มากขึ้น √2.5 เท่า','4 เท่า'],'C',
      ['💡 T ∝ 1/√g','🔍 g × 0.4 → T × 1/√0.4 = √2.5','📐 g น้อย → แกว่งช้าลง']),

    M('R133S097','SHM · A เพิ่ม 2 เท่า · ω เดิม → v_max?',
      ['คงเดิม','2 เท่า','4 เท่า','1/2 เท่า'],'B',
      ['💡 v_max = ωA','🔍 A×2 → v_max × 2','📐 linear']),

    M('R133S098','SHM · A เพิ่ม 2 เท่า · ω เดิม → a_max?',
      ['คงเดิม','2 เท่า','4 เท่า','1/2 เท่า'],'B',
      ['💡 a_max = ω²A','🔍 A×2 → a_max × 2','📐 linear (A กำลัง 1)']),

    M('R133S099','SHM · A เพิ่ม 2 เท่า · ω เดิม → T?',
      ['คงเดิม','2 เท่า','4 เท่า','1/2 เท่า'],'A',
      ['💡 T = 2π/ω ไม่มี A','🔍 T ไม่ขึ้นกับ amplitude','📐 ปล่อยจาก A เล็ก/ใหญ่ → T เท่ากัน']),

    M('R133S100','SHM · ω เพิ่ม 2 เท่า → T?',
      ['2 เท่า','4 เท่า','1/2 เท่า','1/4 เท่า'],'C',
      ['💡 T = 2π/ω','🔍 ω×2 → T×1/2','📐 ω เพิ่ม → คาบสั้นลง']),

    // ════════ B4 — x, v, a, KE, PE ⭐ (R133S101-115 · 15) ════════
    M('R133S101','ที่ <strong>ตำแหน่งสมดุล (x = 0)</strong> สถานะของวัตถุ?',
      ['v=0, a=0','v=v_max, a=0','v=0, a=a_max','v=v_max, a=a_max'],'B',
      ['💡 v_max ที่สมดุล · a=0 (เพราะ x=0)','🔍 ทุกพลังงานเป็น KE','📐 หัวใจของ A4 ใน Stage A'],
      SVG_VAX),

    M('R133S102','ที่ <strong>ตำแหน่ง extremes (x = ±A)</strong> สถานะของวัตถุ?',
      ['v=0, a=0','v=v_max, a=0','v=0, a=a_max','v=v_max, a=a_max'],'C',
      ['💡 v=0 (วัตถุกลับทิศ) · a=a_max','🔍 ทุกพลังงานเป็น PE','📐 สลับกับสมดุล'],
      SVG_VAX),

    F('R133S103','SHM · ω = 2 rad/s · A = 0.5 m → v_max (m/s)?', 1, 'm/s',
      ['💡 v_max = ωA','🔍 = 2 × 0.5','📐 = 1 m/s']),

    F('R133S104','SHM · ω = 2 rad/s · A = 0.5 m → a_max (m/s²)?', 2, 'm/s²',
      ['💡 a_max = ω²A','🔍 = 4 × 0.5','📐 = 2 m/s²']),

    M('R133S105','ที่ x = A/2 — ขนาด v?',
      ['ωA','ωA·√3/2','ωA/2','0'],'B',
      ['💡 v = ω√(A² − (A/2)²) = ω√(3A²/4)','🔍 = ωA·√3/2','📐 ≈ 0.866 × v_max']),

    M('R133S106','ที่ x = A/2 — ขนาด a?',
      ['ω²A','ω²A/2','ω²A·√3/2','0'],'B',
      ['💡 a = −ω²x','🔍 |a| = ω²·(A/2) = ω²A/2','📐 = 0.5 × a_max']),

    M('R133S107','KE สูงสุด <strong>ที่ตำแหน่งใด</strong>?',
      ['x = 0','x = ±A','x = A/2','ทุกตำแหน่งเท่ากัน'],'A',
      ['💡 KE = ½mv² · max ที่ v_max','🔍 v_max ที่ x=0','📐 KE_max = ½mω²A²']),

    M('R133S108','PE สูงสุด <strong>ที่ตำแหน่งใด</strong>?',
      ['x = 0','x = ±A','x = A/2','ทุกตำแหน่งเท่ากัน'],'B',
      ['💡 PE = ½kx² · max ที่ |x|_max','🔍 |x|_max = A','📐 PE_max = ½kA²']),

    M('R133S109','สูตร <strong>KE_max</strong> ใน Spring SHM?',
      ['½kA','½mωA','½mω²A²','½kA²'],'C',
      ['💡 KE_max = ½m·v_max² = ½m·(ωA)²','🔍 = ½mω²A²','📐 = ½kA² (เท่ากับ PE_max)']),

    M('R133S110','สูตร <strong>PE_max</strong> ใน Spring SHM?',
      ['kA','½kA','½kA²','½mω²A'],'C',
      ['💡 PE = ½kx² · max ที่ x=A','🔍 PE_max = ½kA²','📐 = KE_max (energy conservation)']),

    TF('R133S111','"ใน SHM พลังงานกล total (KE + PE) คงที่ตลอดเวลา"',true,
      ['💡 ไม่มีเสียดทาน → อนุรักษ์พลังงาน','🔍 KE_max ที่สมดุล · PE_max ที่ extremes','📐 ผลรวมเท่ากันเสมอ = ½kA²']),

    M('R133S112','SHM · พลังงานกล total เท่ากับ?',
      ['½kA','½kA²','½mω²','kA²'],'B',
      ['💡 E = KE + PE = ½kA² (คงที่)','🔍 ที่ extremes: KE=0, PE=½kA² → E=½kA²','📐 ที่สมดุล: KE=½kA², PE=0 → E=½kA²']),

    F('R133S113','m = 1 kg · ω = 2 rad/s · A = 0.5 m → KE_max (J)?', 0.5, 'J',
      ['💡 KE_max = ½mω²A²','🔍 = 0.5 × 1 × 4 × 0.25','📐 = 0.5 J']),

    F('R133S114','m = 1 kg · k = 4 N/m · A = 0.5 m → PE_max (J)?', 0.5, 'J',
      ['💡 PE_max = ½kA²','🔍 = 0.5 × 4 × 0.25','📐 = 0.5 J · เท่ากับ KE_max']),

    M('R133S115','ตำแหน่งที่ <strong>KE = PE</strong> ใน SHM?',
      ['x = 0','x = ±A','x = ±A/2','x = ±A/√2'],'D',
      ['💡 KE = ½k(A²−x²) · PE = ½kx²','🔍 KE = PE → A² − x² = x² → x² = A²/2','📐 x = ±A/√2 ≈ ±0.707A']),

    // ════════ B5 — Spring T calc (R133S116-130 · 15) ════════
    M('R133S116','สูตรคาบ T ของ <strong>Spring SHM</strong>?',
      ['T = 2π√(k/m)','T = 2π√(m/k)','T = 2π·m·k','T = 2π·m/k'],'B',
      ['💡 T = 2π/ω และ ω = √(k/m)','🔍 T = 2π√(m/k)','📐 m หนัก → T มาก · k แข็ง → T น้อย'],
      SVG_SPRING),

    F('R133S117','Spring · m = 1 kg · k = 100 N/m · π=3.14 → T (s)?', 0.628, 's',
      ['💡 T = 2π√(m/k)','🔍 = 2π√(1/100) = 2π/10','📐 ≈ 0.628 s']),

    F('R133S118','Spring · m = 0.5 kg · k = 50 N/m · π=3.14 → T (s)?', 0.628, 's',
      ['💡 T = 2π√(m/k)','🔍 = 2π√(0.5/50) = 2π/10','📐 ≈ 0.628 s · เท่ากับ S117 (m/k เท่ากัน)']),

    F('R133S119','Spring · m = 1 kg · k = 400 N/m · π=3.14 → T (s)?', 0.314, 's',
      ['💡 T = 2π√(m/k)','🔍 = 2π√(1/400) = 2π/20','📐 ≈ 0.314 s']),

    F('R133S120','Spring · m = 4 kg · k = 100 N/m · π=3.14 → T (s)?', 1.256, 's',
      ['💡 T = 2π√(m/k)','🔍 = 2π√(4/100) = 2π × 0.2','📐 ≈ 1.256 s']),

    M('R133S121','สูตร ω ของ Spring SHM?',
      ['ω = √(m/k)','ω = √(k/m)','ω = k/m','ω = m·k'],'B',
      ['💡 a = −(k/m)x = −ω²x → ω² = k/m','🔍 ω = √(k/m)','📐 หน่วย: √(N/m / kg) = √(1/s²) = 1/s = rad/s']),

    F('R133S122','Spring · m = 1 kg · k = 100 N/m → ω (rad/s)?', 10, 'rad/s',
      ['💡 ω = √(k/m)','🔍 = √(100/1)','📐 = 10 rad/s']),

    F('R133S123','Spring · m = 2 kg · k = 200 N/m → ω (rad/s)?', 10, 'rad/s',
      ['💡 ω = √(k/m)','🔍 = √(200/2) = √100','📐 = 10 rad/s']),

    M('R133S124','สูตร <strong>f (frequency)</strong> ของ Spring SHM?',
      ['f = √(k/m)/(2π)','f = √(m/k)/(2π)','f = 2π√(k/m)','f = √(km)'],'A',
      ['💡 ω = 2πf → f = ω/(2π) = √(k/m)/(2π)','🔍 f = (1/2π)√(k/m)','📐 หน่วย Hz']),

    F('R133S125','Spring · m = 1 kg · k = 400 N/m · π=3.14 → f (Hz)?', 3.18, 'Hz',
      ['💡 f = √(k/m)/(2π) = ω/(2π)','🔍 ω = √400 = 20 → f = 20/(2π) = 10/π','📐 ≈ 3.18 Hz']),

    M('R133S126','สปริง 2 ตัว k₁ = k₂ = k ต่อ <strong>ขนาน</strong> · k_eq = ?',
      ['k','2k','k/2','k²'],'B',
      ['💡 ขนาน → k_eq = k₁ + k₂','🔍 = 2k','📐 ผูกคู่ → แข็งกว่า → T สั้นลง']),

    M('R133S127','สปริง 2 ตัว k₁ = k₂ = k ต่อ <strong>อนุกรม</strong> · k_eq = ?',
      ['2k','k','k/2','k²/2'],'C',
      ['💡 อนุกรม → 1/k_eq = 1/k + 1/k = 2/k','🔍 k_eq = k/2','📐 ผูกซ้อน → อ่อนกว่า → T ยาวขึ้น']),

    F('R133S128','สปริง 2 ตัว k=100 ขนาน · m=2 kg · π=3.14 → T (s)?', 0.628, 's',
      ['💡 k_eq = 100+100 = 200','🔍 T = 2π√(2/200) = 2π/10','📐 ≈ 0.628 s']),

    TF('R133S129','"Spring แนวดิ่ง (มี gravity) มีคาบ T เท่ากับแนวระดับ"',true,
      ['💡 gravity แค่เลื่อน "ตำแหน่งสมดุล" ลง mg/k','🔍 SHM รอบสมดุลใหม่ — ω = √(k/m) เดิม','📐 T = 2π√(m/k) ไม่เปลี่ยน']),

    M('R133S130','Spring · m เพิ่มเรื่อยๆ (k เดิม) → T เป็นอย่างไร?',
      ['ลดลง','เพิ่มขึ้น','คงเดิม','เปลี่ยนแบบไม่แน่นอน'],'B',
      ['💡 T = 2π√(m/k) → T ∝ √m','🔍 m เพิ่ม → T เพิ่ม','📐 มวลหนัก → แกว่งช้าลง']),

    // ════════ B6 — Pendulum T calc (R133S131-140 · 10) ════════
    M('R133S131','สูตรคาบ T ของ <strong>simple pendulum (มุมเล็ก)</strong>?',
      ['T = 2π√(g/L)','T = 2π√(L/g)','T = 2π·L·g','T = π·L/g'],'B',
      ['💡 T = 2π/ω และ ω = √(g/L)','🔍 T = 2π√(L/g)','📐 L ยาว → T มาก'],
      SVG_PEND),

    F('R133S132','Pendulum · L = 0.4 m · g = 10 m/s² · π=3.14 → T (s)?', 1.256, 's',
      ['💡 T = 2π√(L/g)','🔍 = 2π√(0.4/10) = 2π × 0.2','📐 ≈ 1.256 s']),

    F('R133S133','Pendulum · L = 2.5 m · g = 10 · π=3.14 → T (s)?', 3.14, 's',
      ['💡 T = 2π√(L/g)','🔍 = 2π√(2.5/10) = 2π × 0.5','📐 = π ≈ 3.14 s']),

    F('R133S134','Pendulum · L = 0.1 m · g = 10 · π=3.14 → T (s)?', 0.628, 's',
      ['💡 T = 2π√(L/g)','🔍 = 2π√(0.1/10) = 2π × 0.1','📐 ≈ 0.628 s']),

    M('R133S135','สูตร ω ของ simple pendulum?',
      ['ω = √(L/g)','ω = √(g/L)','ω = L·g','ω = g/L'],'B',
      ['💡 ω = √(g/L)','🔍 T = 2π/ω = 2π√(L/g)','📐 g มาก → ω มาก → T สั้น']),

    F('R133S136','Pendulum · L = 2.5 m · g = 10 → ω (rad/s)?', 2, 'rad/s',
      ['💡 ω = √(g/L)','🔍 = √(10/2.5) = √4','📐 = 2 rad/s']),

    M('R133S137','สูตร f ของ simple pendulum?',
      ['f = √(L/g)/(2π)','f = √(g/L)/(2π)','f = 2π√(g/L)','f = √(gL)'],'B',
      ['💡 f = ω/(2π) = √(g/L)/(2π)','🔍 = (1/2π)√(g/L)','📐 หน่วย Hz']),

    M('R133S138','Pendulum ไป <strong>ดวงจันทร์ (g_moon = g/6)</strong> · L เดิม → T เป็น?',
      ['ลดลง √6 เท่า','เท่าเดิม','เพิ่มขึ้น √6 เท่า','เพิ่ม 6 เท่า'],'C',
      ['💡 T ∝ 1/√g','🔍 g × 1/6 → T × √6','📐 ≈ 2.45 เท่า'],
      SVG_PEND),

    TF('R133S139','"คาบของ simple pendulum ขึ้นกับมวลของลูกตุ้ม"',false,
      ['💡 T = 2π√(L/g) — ไม่มี m','🔍 ลูกตุ้มหนัก/เบา → คาบเท่ากัน','📐 Galileo สังเกตที่โบสถ์']),

    M('R133S140','การแกว่งลูกตุ้มที่ <strong>มุมใหญ่ (เช่น 60°)</strong> — สูตร T = 2π√(L/g) ใช้ได้ไหม?',
      ['ใช้ได้แม่นยำ','ใช้ได้โดยประมาณเท่านั้น (ไม่ใช่ SHM แท้)','ใช้ไม่ได้เลย — T = 0','ใช้ได้ทุกมุม'],'B',
      ['💡 สูตรนี้ใช้ small angle approximation (sin θ ≈ θ)','🔍 มุมใหญ่ → ไม่เป็น SHM แท้ → T จริง > สูตร','📐 ในชุดนี้ใช้สูตรนี้กับ θ ≤ 15° เท่านั้น'])
  ];

  window.QUESTIONS_R133_B = Q;
  if(window.console && console.log) console.log('[Region 1.3.3 Stage B] loaded', Q.length, '/ 70 questions');

  // Helper for TF that wasn't declared (uses local var)
  function TF(id, statement, correct, hints, figure){
    const q = {id, group:'B', type:'tf', statement, correct: correct ? 'T' : 'F', hints, formula_tags:F_TAG, noReveal:true};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
})();
