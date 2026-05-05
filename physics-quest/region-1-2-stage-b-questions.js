/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.2 ป่าแห่งแรง · Stage B
   "ใช้สูตรไหน" — เลือกสูตร + ระบุตัวแปร · ไม่คำนวณตัวเลขจริง
   noReveal:true → engine บล็อก See50% + choiceCut + scaffolded hint

   หมวด:
     B1 เลือก F=ma vs W=mg
     B2 ΣF=0 vs ΣF=ma            (โจทย์นิ่ง vs มี a)
     B3 แยกแรงบนวัตถุ              (free-body: N, W, T, f, F_app)
     B4 หา a จากสูตรไหน            (F สุทธิ vs F แรงเดียว)
     B5 แรงเสียดทาน f=μN          (เลือก μs vs μk · หา N ก่อน)
     B6 Free fall vs Non-free fall (terminal v ⟹ ΣF=0)
     B7 อ่าน free-body diagram    (เลือก diagram ที่ถูกต้อง)

   เป้าจำนวน: 140-160 ข้อ (MCQ + SVG free-body)
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  // ─── Hint constants ───
  const H_PICK_FMA   = ["💡 รู้ m + a → F=ma · รู้ m → W=mg","🔍 หา 'แรง' (N) → F=ma หรือ W=mg เท่านั้น","📐 ตรวจหน่วย: F[N]=m[kg]×a[m/s²]"];
  const H_PICK_EQ    = ["💡 ถ้านิ่ง/v คงที่ → ΣF=0 · ถ้ามี a → ΣF=ma","🔍 อ่านโจทย์: 'นิ่ง', 'v คงที่', 'เคลื่อนสม่ำเสมอ' = สมดุล","📐 มี 'เร่ง', 'หน่วง', 'a=...' = ใช้ ΣF=ma"];
  const H_FBD        = ["💡 ระบุแรงทั้งหมด: N (พื้นดัน), W=mg (ลง), T (เชือก), f (เสียดทาน), F_app","🔍 แต่ละแรงมีจุดกระทำ + ทิศ","📐 บนพื้นราบ: N=W · บนระนาบเอียง: N=mg cosθ"];
  const H_PICK_A     = ["💡 a = ΣF/m เสมอ — F ต้องเป็น 'แรงสุทธิ'","🔍 ถ้ามีหลายแรง → รวมเป็น vector ก่อน","📐 ระวัง: F_app ≠ ΣF เมื่อมีเสียดทาน"];
  const H_PICK_FRIC  = ["💡 ก่อนเคลื่อน → μs · กำลังเคลื่อน → μk","🔍 หา N ก่อน (พื้นราบ N=mg)","📐 f = μN — f สูงสุดสถิต = μsN"];
  const H_FALL_PICK  = ["💡 ปล่อยตอนต้น → free fall a=g · มี air resistance R","🔍 ΣF = mg − R · ขณะ R<mg → a<g","📐 Terminal v: R=mg → ΣF=0 → a=0"];
  const H_FBD_PICK   = ["💡 นับจำนวนแรง · ตรวจทิศแต่ละแรง","🔍 วัตถุนิ่ง → vector ปิด · วัตถุเร่ง → vector เปิด","📐 W ลงเสมอ · N ตั้งฉากผิวสัมผัสเสมอ"];

  // ─── SVG library: free-body diagrams ───
  // (เติมตามต้องการ)

  const F_TAG = ['forces-b'];
  function M(id, statement, choices, correct, hints, figure){
    const arr = choices.map((t,i) => ({key:String.fromCharCode(65+i), text:t}));
    const q = {id, group:'B', noReveal:true, type:'mcq', statement, choices:arr, correct, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function F(id, statement, correctList, hints, figure){
    const q = {id, group:'B', noReveal:true, type:'fill', statement, correct: correctList, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }

  const Q = [
    // ════════ B1 — เลือก F=ma vs W=mg ════════

    // ════════ B2 — ΣF=0 vs ΣF=ma ════════

    // ════════ B3 — แยกแรงบนวัตถุ (FBD) ════════

    // ════════ B4 — หา a จากสูตรไหน ════════

    // ════════ B5 — แรงเสียดทาน f=μN ════════

    // ════════ B6 — Free fall vs Non-free fall ════════

    // ════════ B7 — อ่าน free-body diagram ════════
  ];

  window.QUESTIONS_R12_B = Q;
  if(window.console && console.log) console.log('[Region 1.2 Stage B] loaded', Q.length, 'questions (formula picker)');
})();
