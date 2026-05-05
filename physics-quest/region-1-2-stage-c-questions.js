/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.2 ป่าแห่งแรง · Stage C
   "แก้สถานการณ์" — word problem · คำนวณตัวเลขจริง · g = 10 m/s²

   หมวด:
     C1 F = ma แบบตรงๆ          (รู้ 2 ใน 3)
     C2 W = mg                  (น้ำหนักบนโลก/ดวงจันทร์/g อื่น)
     C3 ΣF = ma                 (หลายแรงรวม → หา a)
     C4 Equilibrium             (วัตถุนิ่ง → หา T, N, f ที่ขาด)
     C5 แรงเสียดทาน             (μ × N · หา f, หา F ที่ต้องดึง)
     C6 ลิฟต์                    (น้ำหนักปรากฏ a ขึ้น/ลง)
     C7 ระนาบเอียง basic        (component ของ W)
     C8 Atwood / 2 มวลผูกเชือก  (a, T)
     C9 Terminal velocity        (R = mg)

   เป้าจำนวน: 160-180 ข้อ
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  // ─── Hint constants ───
  const H_FMA      = ["💡 F = ma","🔍 รู้ 2 ตัว → หาตัวที่ 3","📐 หน่วย: F[N] = m[kg] × a[m/s²]"];
  const H_WMG      = ["💡 W = mg · ใช้ g=10 m/s² (โลก)","🔍 น้ำหนักคือแรง → หน่วย N · มวล → kg","📐 ดวงจันทร์ g≈1.6 · ดาวอังคาร g≈3.7"];
  const H_SUMF     = ["💡 ΣF = ma · ΣF คือผลรวม vector","🔍 ทิศเดียวกัน +, ทิศตรงข้าม −","📐 หา ΣF ก่อน แล้วหารด้วย m"];
  const H_EQ       = ["💡 ΣF=0 → ทุกแรงต้องสมดุล","🔍 แตกเป็นแกน x, y","📐 บนพื้นราบ N = W"];
  const H_FRIC     = ["💡 f = μN · บนพื้นราบ N=mg","🔍 หา N ก่อน แล้วคูณด้วย μ","📐 ก่อนเคลื่อน μs · กำลังเคลื่อน μk"];
  const H_LIFT     = ["💡 ลิฟต์เร่งขึ้น a → N − mg = ma → N = m(g+a)","🔍 ลิฟต์เร่งลง a → mg − N = ma → N = m(g−a)","📐 ลิฟต์ตกอิสระ → N=0 (ภาวะไร้น้ำหนัก)"];
  const H_INCLINE  = ["💡 W แตกเป็น 2 component: ขนาน mg sinθ · ตั้งฉาก mg cosθ","🔍 N = mg cosθ · แรงดึงตามระนาบ = mg sinθ","📐 ลื่น (ไม่มี f): a = g sinθ"];
  const H_ATWOOD   = ["💡 a = (m₂−m₁)g/(m₁+m₂) · T = 2m₁m₂g/(m₁+m₂)","🔍 m₂ > m₁ → m₂ ลง · m₁ ขึ้น","📐 รวมแรงทั้งระบบ ÷ มวลรวม"];
  const H_TERM     = ["💡 Terminal v: R = mg → ΣF=0 → a=0","🔍 ขณะลง R<mg → ยังเร่ง · R=mg → v คงที่","📐 R ขึ้นกับ v และพื้นที่หน้าตัด"];

  // ─── SVG library (เติมตามต้องการ) ───
  // ตัวอย่าง: ระนาบเอียง θ
  const SVG_INCLINE = '<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="120" x2="220" y2="120" stroke="#fff" stroke-width="2"/><polygon points="20,120 220,120 220,40" fill="rgba(56,189,248,.08)" stroke="#38bdf8" stroke-width="1.5"/><rect x="155" y="62" width="28" height="20" fill="#1f2937" stroke="#fbbf24" stroke-width="1.5" transform="rotate(-22, 169, 72)"/><text x="195" y="115" fill="#fbbf24" font-size="11" font-weight="700">θ</text><path d="M 200 120 A 20 20 0 0 0 200 110" fill="none" stroke="#fbbf24" stroke-width="1.5"/></svg>';

  const F_TAG = ['forces-c'];
  function M(id, statement, choices, correct, hints, figure){
    const arr = choices.map((t,i) => ({key:String.fromCharCode(65+i), text:t}));
    const q = {id, group:'C', type:'mcq', statement, choices:arr, correct, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function F(id, statement, correctList, hints, figure){
    const q = {id, group:'C', type:'fill', statement, correct: correctList, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }

  const Q = [
    // ════════ C1 — F = ma แบบตรงๆ ════════

    // ════════ C2 — W = mg ════════

    // ════════ C3 — ΣF = ma (หลายแรง) ════════

    // ════════ C4 — Equilibrium (หา T, N, f ที่ขาด) ════════

    // ════════ C5 — แรงเสียดทาน f = μN ════════

    // ════════ C6 — ลิฟต์ (น้ำหนักปรากฏ) ════════

    // ════════ C7 — ระนาบเอียง basic ════════

    // ════════ C8 — Atwood / 2 มวลผูกเชือก ════════

    // ════════ C9 — Terminal velocity ════════
  ];

  window.QUESTIONS_R12_C = Q;
  if(window.console && console.log) console.log('[Region 1.2 Stage C] loaded', Q.length, 'questions (calculation)');
})();
