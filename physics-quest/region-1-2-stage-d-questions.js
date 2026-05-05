/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.2 ป่าแห่งแรง · Stage D
   "เหตุการณ์วิกฤต" — multi-concept · ผสม 2-3 แนวคิด
   อนุญาตผสมกับ Region 1.1 (จลศาสตร์) ได้

   หมวด:
     D1 F=ma + จลศาสตร์         (รู้ F → หา a → หา v หรือ s ที่ t)
     D2 ลิฟต์เร่ง + น้ำหนักปรากฏ  (กับเครื่องชั่ง)
     D3 ระนาบเอียง + เสียดทาน    (กำลังลื่น / นิ่งอยู่)
     D4 Atwood + a + T          (ระบบ pulley)
     D5 Action-reaction         (จรวด, ปืน recoil, ดันรถ)
     D6 Free body + ΣF=0        (เชือก 2 เส้นทำมุม)
     D7 Free fall vs air resist (เปรียบเทียบ a ที่จุดต่างๆ)

   เป้าจำนวน: 90-100 ข้อ (รวมแนว O-NET / สามัญ)
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  const H_FMA_K   = ["💡 หา a จาก F=ma ก่อน → ใช้ a กับสมการจลศาสตร์","🔍 v=u+at · s=ut+½at² · v²=u²+2as","📐 ดูว่าโจทย์ถามอะไร เลือกสมการที่มีตัวที่หา"];
  const H_LIFT_M  = ["💡 N = m(g±a) — ขึ้น +, ลง −","🔍 น้ำหนักปรากฏ = N (แรงที่เครื่องชั่งอ่าน)","📐 ตกอิสระ a=g → N=0 → ไร้น้ำหนัก"];
  const H_INC_FRIC= ["💡 W∥ = mg sinθ ดึงลง · f = μmg cosθ ต้าน","🔍 a = g(sinθ − μcosθ) เมื่อกำลังลง","📐 ถ้า μ ≥ tanθ → ไม่ลื่น (สมดุลสถิต)"];
  const H_ATWOOD2 = ["💡 a = (m₂−m₁)g/(m₁+m₂)","🔍 T เกิดจากแรงรวมที่ดึงมวลใดมวลหนึ่ง","📐 ตรวจ T < น้ำหนักของมวลที่หนักกว่า"];
  const H_AR      = ["💡 m₁v₁ = m₂v₂ (อนุรักษ์โมเมนตัม) หรือ F·t กระทำเท่ากัน","🔍 มวลน้อย → ความเร็วถอย/พุ่งมาก","📐 แรงคู่กัน — ขนาดเท่ากัน ทิศตรงข้าม"];
  const H_FBD_EQ  = ["💡 แตกแรงเชือกแต่ละเส้นเป็นแกน x, y","🔍 ΣFx=0 และ ΣFy=0","📐 มุมจากแนวดิ่ง vs แนวราบ — ระวังให้ถูก"];
  const H_AIR     = ["💡 เริ่มตก: R=0 → a=g · ขณะตก: R เพิ่ม → a ลด","🔍 Terminal: R=mg → a=0 → v คงที่","📐 หนักกว่าเข้าถึง terminal v สูงกว่า"];

  const F_TAG = ['forces-d'];
  function M(id, statement, choices, correct, hints, figure){
    const arr = choices.map((t,i) => ({key:String.fromCharCode(65+i), text:t}));
    const q = {id, group:'D', noReveal:true, type:'mcq', statement, choices:arr, correct, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }

  const Q = [
    // ════════ D1 — F=ma + จลศาสตร์ ════════

    // ════════ D2 — ลิฟต์เร่ง + น้ำหนักปรากฏ ════════

    // ════════ D3 — ระนาบเอียง + เสียดทาน ════════

    // ════════ D4 — Atwood + a + T ════════

    // ════════ D5 — Action-reaction (จรวด, ปืน) ════════

    // ════════ D6 — Free body + ΣF=0 (เชือก 2 เส้น) ════════

    // ════════ D7 — Free fall vs air resistance ════════
  ];

  window.QUESTIONS_R12_D = Q;
  if(window.console && console.log) console.log('[Region 1.2 Stage D] loaded', Q.length, 'questions (multi-concept)');
})();
