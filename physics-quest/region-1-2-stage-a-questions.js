/* ═══════════════════════════════════════════════════════════════
   Physics Quest — Region 1.2 ป่าแห่งแรง · Stage A
   "รู้เขารู้เรา" — concept-only · MCQ + T/F · ไม่คำนวณ
   อ้างอิง: Hewitt Conceptual Physics Ch.2 (Inertia) + Ch.4 (F=ma) + Ch.5 (Action-Reaction)

   หมวด:
     A1 แรงคืออะไร            (push/pull, vector, contact vs at-a-distance)
     A2 ความเฉื่อย Inertia      (Galileo inclined plane, มวลมาก = เฉื่อยมาก)
     A3 มวล vs น้ำหนัก          (kg vs N, มวลคงที่ / น้ำหนักเปลี่ยนตาม g)
     A4 แรงลัพธ์ ΣF             (vector sum จาก diagram)
     A5 สมดุล ΣF=0              (วัตถุนิ่ง / v คงที่)
     A6 แรงปฏิกิริยา (3rd law)  (ระบุคู่ action-reaction)
     A7 แรงเสียดทาน             (ทิศตรงข้าม v · สถิต > จลน์)

   เป้าจำนวน: 70-80 ข้อ (MCQ 50 + T/F 20 + ระบุทิศจาก SVG 10)
   ═══════════════════════════════════════════════════════════════ */
'use strict';
(function(){
  // ─── Hint constants ───
  const H_FORCE  = ["💡 แรง = push หรือ pull · มีทั้งขนาดและทิศ (vector)","🔍 แรงสัมผัส (contact) vs แรงระยะไกล (gravity, magnetic)","📐 หน่วย SI: นิวตัน (N)"];
  const H_INERT  = ["💡 ความเฉื่อย = สมบัติของวัตถุที่ต้านการเปลี่ยนสภาพการเคลื่อนที่","🔍 มวลมาก = ความเฉื่อยมาก (เปลี่ยนสภาพยาก)","📐 ไม่มีแรงสุทธิ → วัตถุรักษาสภาพเดิม (นิ่ง/v คงที่)"];
  const H_MW     = ["💡 มวล (kg) คงที่ทุกที่ · น้ำหนัก (N) เปลี่ยนตาม g","🔍 W = mg · บนโลก g≈10 · ดวงจันทร์ g≈1.6","📐 น้ำหนักคือแรง — มวลไม่ใช่แรง"];
  const H_NETF   = ["💡 ΣF = vector sum · ทิศเดียวกันบวก · ทิศตรงข้ามลบ","🔍 ตั้งแกนบวกก่อน แล้วใส่เครื่องหมายให้ตรง","📐 ขนาด = √(Fx² + Fy²) ถ้าตั้งฉาก"];
  const H_EQ     = ["💡 ΣF=0 → วัตถุนิ่ง หรือเคลื่อนที่ด้วย v คงที่","🔍 ต้องสมดุลทั้งแกน x และ y","📐 น้ำหนัก = แรงตั้งฉาก (N) เมื่อบนพื้นราบ"];
  const H_3RD    = ["💡 ทุกแรงมีคู่ปฏิกิริยา ขนาดเท่ากัน ทิศตรงข้าม","🔍 เกิดบนวัตถุคนละตัว — ห้ามหักล้างกันเอง","📐 รูปแบบ: A กระทำ B → B กระทำ A"];
  const H_FRIC   = ["💡 แรงเสียดทานทิศตรงข้ามการเคลื่อนที่","🔍 สถิต (ก่อนเคลื่อน) > จลน์ (กำลังเคลื่อน)","📐 f = μN · μ ขึ้นกับผิวสัมผัส"];

  // ─── SVG library: free body diagrams + force vectors ───
  // (เติมตามต้องการ เมื่อสร้างโจทย์)
  // ตัวอย่าง: 2 แรงต้านกัน 5N← + 3N→
  const SVG_2F_OPP = '<svg viewBox="0 0 220 90" xmlns="http://www.w3.org/2000/svg"><rect x="90" y="35" width="40" height="30" fill="#1f2937" stroke="#fbbf24" stroke-width="1.5"/><line x1="85" y1="50" x2="35" y2="50" stroke="#f87171" stroke-width="2.5"/><polygon points="30,50 38,46 38,54" fill="#f87171"/><text x="40" y="42" fill="#f87171" font-size="11" font-weight="700">5 N</text><line x1="135" y1="50" x2="170" y2="50" stroke="#34d399" stroke-width="2.5"/><polygon points="175,50 167,46 167,54" fill="#34d399"/><text x="138" y="42" fill="#34d399" font-size="11" font-weight="700">3 N</text><text x="98" y="58" fill="#fbbf24" font-size="9">m</text></svg>';
  // วัตถุบนพื้น: W ลง · N ขึ้น
  const SVG_FBD_REST = '<svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg"><line x1="20" y1="105" x2="180" y2="105" stroke="#fff" stroke-width="2"/><rect x="80" y="65" width="40" height="40" fill="#1f2937" stroke="#fbbf24" stroke-width="1.5"/><line x1="100" y1="65" x2="100" y2="20" stroke="#34d399" stroke-width="2.5"/><polygon points="100,15 96,23 104,23" fill="#34d399"/><text x="106" y="35" fill="#34d399" font-size="11" font-weight="700">N</text><line x1="100" y1="105" x2="100" y2="125" stroke="#f87171" stroke-width="2.5"/><polygon points="100,128 96,120 104,120" fill="#f87171"/><text x="106" y="125" fill="#f87171" font-size="11" font-weight="700">W</text></svg>';

  // ─── Question constructors (matching stage-c/d style) ───
  const F_TAG = ['forces-a'];
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

  const Q = [
    // ════════ A1 — แรงคืออะไร ════════
    // TODO: ครูเติมโจทย์ที่นี่ (ตัวอย่างด้านล่าง)
    // M('R12A001','แรงในข้อใดจัดเป็นแรงสัมผัส',['แรงโน้มถ่วง','แรงเสียดทาน','แรงแม่เหล็ก','แรงไฟฟ้า'],'B',H_FORCE),

    // ════════ A2 — ความเฉื่อย ════════

    // ════════ A3 — มวล vs น้ำหนัก ════════

    // ════════ A4 — แรงลัพธ์ ΣF ════════

    // ════════ A5 — สมดุล ΣF=0 ════════

    // ════════ A6 — แรงปฏิกิริยา (3rd law) ════════

    // ════════ A7 — แรงเสียดทาน ════════
  ];

  window.QUESTIONS_R12_A = Q;
  if(window.console && console.log) console.log('[Region 1.2 Stage A] loaded', Q.length, 'questions (concept)');
})();
