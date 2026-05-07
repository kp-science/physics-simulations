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

  // ── Reusable arrow markers (auto-oriented) ──
  const DEFS = '<defs>'+
    '<marker id="aG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#34d399"/></marker>'+
    '<marker id="aR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#f87171"/></marker>'+
    '<marker id="aP" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#818cf8"/></marker>'+
    '<marker id="aY" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#fbbf24"/></marker>'+
    '<marker id="aK" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#f472b6"/></marker>'+
    '<marker id="aO" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#fb923c"/></marker>'+
    '</defs>';
  // S1: Block on flat ground — FBD with vertical+horizontal reference dashed axes through CoM
  const SVG_BLOCK_GND = '<svg viewBox="0 0 220 180" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ground
    '<line x1="10" y1="135" x2="210" y2="135" stroke="#3d5470" stroke-width="1.5"/>'+
    '<line x1="10" y1="138" x2="210" y2="138" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // reference axes through CoM (110, 110)
    '<line x1="110" y1="20" x2="110" y2="170" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<line x1="20" y1="110" x2="210" y2="110" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="170" y="106" fill="#3d5470" font-size="9">แนวระดับ</text>'+
    '<text x="113" y="28" fill="#3d5470" font-size="9">แนวดิ่ง</text>'+
    // block
    '<rect x="85" y="90" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<circle cx="110" cy="110" r="2.5" fill="#e8f0ff"/>'+
    '<text x="55" y="115" fill="#38bdf8" font-size="12" font-weight="700">m</text>'+
    // N up from CoM
    '<line x1="110" y1="110" x2="110" y2="40" stroke="#34d399" stroke-width="2.6" marker-end="url(#aG)"/>'+
    '<text x="115" y="48" fill="#34d399" font-size="13" font-weight="700">N</text>'+
    // W down from CoM
    '<line x1="110" y1="110" x2="110" y2="168" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="115" y="160" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    '</svg>';
  // S2: Lamp on single rope from ceiling — vertical reference dashed
  const SVG_LAMP_HANG = '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ceiling
    '<line x1="10" y1="20" x2="190" y2="20" stroke="#3d5470" stroke-width="2"/>'+
    '<line x1="10" y1="23" x2="190" y2="23" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // vertical reference dashed through CoM
    '<line x1="100" y1="25" x2="100" y2="190" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="103" y="35" fill="#3d5470" font-size="9">แนวดิ่ง</text>'+
    // rope (faint, behind T vector)
    '<line x1="100" y1="23" x2="100" y2="115" stroke="#818cf8" stroke-width="1.6" stroke-opacity="0.4"/>'+
    // lamp
    '<circle cx="100" cy="135" r="20" fill="rgba(251,191,36,.3)" stroke="#fbbf24" stroke-width="2"/>'+
    '<text x="89" y="142" fill="#fbbf24" font-size="20">💡</text>'+
    '<circle cx="100" cy="115" r="2.5" fill="#fbbf24"/>'+
    // T up from CoM
    '<line x1="100" y1="115" x2="100" y2="50" stroke="#818cf8" stroke-width="2.6" marker-end="url(#aP)"/>'+
    '<text x="106" y="60" fill="#818cf8" font-size="13" font-weight="700">T</text>'+
    // W down from CoM
    '<line x1="100" y1="115" x2="100" y2="186" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="106" y="178" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    '</svg>';
  // S3: Block + downward press
  const SVG_BLOCK_PRESS = '<svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="105" x2="190" y2="105" stroke="#3d5470" stroke-width="1.4"/><line x1="10" y1="108" x2="190" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="2,3"/><rect x="75" y="65" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><text x="92" y="90" fill="#38bdf8" font-size="13" font-weight="700">m</text><line x1="100" y1="20" x2="100" y2="62" stroke="#fbbf24" stroke-width="2.4"/><polygon points="100,65 94,53 106,53" fill="#fbbf24"/><text x="105" y="35" fill="#fbbf24" font-size="11" font-weight="700">F (กด)</text></svg>';
  // S4: Block + upward lift (not airborne)
  const SVG_BLOCK_LIFT = '<svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="105" x2="190" y2="105" stroke="#3d5470" stroke-width="1.4"/><line x1="10" y1="108" x2="190" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="2,3"/><rect x="75" y="65" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><text x="92" y="90" fill="#38bdf8" font-size="13" font-weight="700">m</text><line x1="100" y1="62" x2="100" y2="20" stroke="#fbbf24" stroke-width="2.4"/><polygon points="100,16 94,28 106,28" fill="#fbbf24"/><text x="105" y="40" fill="#fbbf24" font-size="11" font-weight="700">F (ยก)</text></svg>';
  // S5: Bird on V-rope at θ from horizontal — refs through bird (CoM)
  // Bird at (140,108). Rope at θ=30° above horizontal: dx=110, dy=110*tan30°≈63.5 → anchors near (30,44.5) and (250,44.5)
  const SVG_BIRD_V = '<svg viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ceiling/anchors
    '<line x1="10" y1="40" x2="270" y2="40" stroke="#3d5470" stroke-width="2"/>'+
    '<line x1="10" y1="43" x2="270" y2="43" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<circle cx="30" cy="45" r="3" fill="#3d5470"/>'+
    '<circle cx="250" cy="45" r="3" fill="#3d5470"/>'+
    // ropes (faint)
    '<line x1="30" y1="45" x2="140" y2="108" stroke="#818cf8" stroke-width="1.6" stroke-opacity="0.4"/>'+
    '<line x1="250" y1="45" x2="140" y2="108" stroke="#818cf8" stroke-width="1.6" stroke-opacity="0.4"/>'+
    // horizontal reference dashed THROUGH bird
    '<line x1="20" y1="108" x2="260" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="225" y="120" fill="#3d5470" font-size="9">แนวระดับ</text>'+
    // vertical reference dashed
    '<line x1="140" y1="50" x2="140" y2="190" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // bird at vertex
    '<circle cx="140" cy="108" r="3" fill="#fbbf24"/>'+
    '<text x="128" y="138" font-size="22">🦜</text>'+
    // T-left vector — from CoM along rope toward upper-left, length 60 at 30° above horiz
    // end = (140 - 60cos30, 108 - 60sin30) = (140-52, 108-30) = (88, 78)
    '<line x1="140" y1="108" x2="88" y2="78" stroke="#818cf8" stroke-width="2.6" marker-end="url(#aP)"/>'+
    '<text x="72" y="74" fill="#818cf8" font-size="13" font-weight="700">T</text>'+
    // T-right vector — mirror
    '<line x1="140" y1="108" x2="192" y2="78" stroke="#818cf8" stroke-width="2.6" marker-end="url(#aP)"/>'+
    '<text x="198" y="74" fill="#818cf8" font-size="13" font-weight="700">T</text>'+
    // W down
    '<line x1="140" y1="108" x2="140" y2="180" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="146" y="170" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    // angle θ markers — between horizontal dashed and T (each side), arc at radius 28 from bird
    // right: from (168,108) on horizontal-right curving CCW to T-right at 28*cos30,28*sin30 from bird = (164.2, 94)
    '<path d="M 168 108 A 28 28 0 0 0 164.2 94" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="170" y="100" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    // left: from (112,108) on horizontal-left curving CW (sweep=1) to T-left at (115.8, 94)
    '<path d="M 112 108 A 28 28 0 0 1 115.8 94" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="100" y="100" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    '</svg>';
  // S6: Lamp + 2 ropes at θ from vertical — refs through CoM
  // Lamp CoM at (140,108). θ=53° from vertical: each rope direction (±sin53, -cos53) = (±0.8, -0.6)
  // length to ceiling y=23: dy=85, dx=85*(0.8/0.6)=113.3 → anchors at (26.7, 23) and (253.3, 23)
  const SVG_LAMP_2ROPE = '<svg viewBox="0 0 280 210" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ceiling
    '<line x1="10" y1="20" x2="270" y2="20" stroke="#3d5470" stroke-width="2"/>'+
    '<line x1="10" y1="23" x2="270" y2="23" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // ropes (faint)
    '<line x1="27" y1="23" x2="140" y2="108" stroke="#818cf8" stroke-width="1.6" stroke-opacity="0.4"/>'+
    '<line x1="253" y1="23" x2="140" y2="108" stroke="#818cf8" stroke-width="1.6" stroke-opacity="0.4"/>'+
    // vertical reference dashed THROUGH CoM
    '<line x1="140" y1="25" x2="140" y2="200" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="143" y="40" fill="#3d5470" font-size="9">แนวดิ่ง</text>'+
    // horizontal reference dashed
    '<line x1="20" y1="108" x2="260" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // lamp
    '<circle cx="140" cy="130" r="22" fill="rgba(251,191,36,.3)" stroke="#fbbf24" stroke-width="2"/>'+
    '<text x="128" y="138" fill="#fbbf24" font-size="20">💡</text>'+
    '<circle cx="140" cy="108" r="2.5" fill="#fbbf24"/>'+
    // T-left vector — along rope, length 60 at 53° from vertical
    // end = (140 - 60*0.8, 108 - 60*0.6) = (92, 72)
    '<line x1="140" y1="108" x2="92" y2="72" stroke="#818cf8" stroke-width="2.6" marker-end="url(#aP)"/>'+
    '<text x="76" y="68" fill="#818cf8" font-size="13" font-weight="700">T</text>'+
    // T-right
    '<line x1="140" y1="108" x2="188" y2="72" stroke="#818cf8" stroke-width="2.6" marker-end="url(#aP)"/>'+
    '<text x="194" y="68" fill="#818cf8" font-size="13" font-weight="700">T</text>'+
    // W
    '<line x1="140" y1="108" x2="140" y2="195" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="146" y="180" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    // angle θ markers — between vertical-up and T (each side), radius 32
    // vertical-up at distance 32: (140, 76)
    // T-right at distance 32: (140+32*0.8, 108-32*0.6) = (165.6, 88.8)
    // arc M 140 76 A 32 32 0 0 1 165.6 88.8 — sweep=1 (CW in screen, from top toward right) ✓
    '<path d="M 140 76 A 32 32 0 0 1 165.6 88.8" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="150" y="82" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    // T-left at distance 32: (114.4, 88.8). M 140 76 A 32 32 0 0 0 114.4 88.8 — sweep=0 (CCW) toward left
    '<path d="M 140 76 A 32 32 0 0 0 114.4 88.8" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="119" y="82" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    '</svg>';
  // S7: Box on incline at θ=30° + rope parallel to slope
  // Incline base (40,150) to (240,150), top at (240, 35) — height 115, base 200, tan-1(115/200) ≈ 30°
  // Slope direction (up-slope): (cos30°, -sin30°) = (0.866, -0.5)
  // Perpendicular to slope (away from surface, into air): (-sin30°, -cos30°) = (-0.5, -0.866)
  // Block CoM on slope at (140, 92) — midway, slightly above slope line
  const SVG_INC_ROPE = '<svg viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ground (horizontal, faint)
    '<line x1="10" y1="150" x2="270" y2="150" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // incline triangle
    '<polygon points="40,150 240,150 240,35" fill="rgba(61,84,112,.18)" stroke="#3d5470" stroke-width="1.6"/>'+
    // angle θ at base vertex (40,150) — between horizontal and incline edge
    // horizontal-right at radius 32: (72,150). Incline edge at radius 32 from vertex going up-right: (40+32*cos30°, 150-32*sin30°) = (67.7, 134)
    '<path d="M 72 150 A 32 32 0 0 0 67.7 134" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="76" y="143" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    // reference axes through CoM (140, 92): parallel & perpendicular to incline, ±40 each side
    // parallel: from (140-40*0.866, 92+40*0.5)=(105.4,112) to (140+40*0.866, 92-40*0.5)=(174.6,72)
    '<line x1="105.4" y1="112" x2="174.6" y2="72" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="178" y="70" fill="#3d5470" font-size="9">ขนานพื้น</text>'+
    // perpendicular: from (140-40*(-0.5), 92-40*(-0.866))=(160,126.6) to (140+40*(-0.5), 92+40*(-0.866))=(120,57.4)
    '<line x1="160" y1="126.6" x2="120" y2="57.4" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="100" y="56" fill="#3d5470" font-size="9">ตั้งฉากพื้น</text>'+
    // block — rotated -30° around CoM (140,92) to align with incline
    '<rect x="120" y="77" width="40" height="30" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2" transform="rotate(-30 140 92)"/>'+
    '<circle cx="140" cy="92" r="2.5" fill="#e8f0ff"/>'+
    // T vector — parallel to incline, up-slope, length 55
    // end = (140 + 55*0.866, 92 - 55*0.5) = (187.6, 64.5)
    '<line x1="140" y1="92" x2="187.6" y2="64.5" stroke="#818cf8" stroke-width="2.6" marker-end="url(#aP)"/>'+
    '<text x="194" y="60" fill="#818cf8" font-size="13" font-weight="700">T</text>'+
    // W — true vertical, downward, length 55
    '<line x1="140" y1="92" x2="140" y2="147" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="146" y="135" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    '</svg>';
  // S8: Block on flat ground + diagonal push at θ below horizontal — refs through CoM, F applied at top of block
  // Block CoM at (130, 100). F applied AT block (tail at top-left corner), going INTO block from upper-left
  // Use θ=37° below horizontal: F direction (cos37°, sin37°) = (0.8, 0.6) (down-right in screen)
  // Tail far from block (upper-left): tail at (130-70*0.8, 100-70*0.6) = (74, 58)... too far
  // Better: F vector tail at upper-left corner of block, head at center of top edge:
  // Actually for a "push down at angle", visualize: someone pushes the block from upper-left, force on block points DOWN-RIGHT into block
  // Tail outside block (upper-left of block top), head at top edge of block (contact point)
  // Use contact point on top of block at (115, 80) (top-left corner area). F points INTO block from upper-left direction (i.e., F vector arrow ends at contact, tail is upper-left)
  // Direction of F applied: down-right at 37° below horizontal = (0.8, 0.6)
  // Tail = contact - 60*(0.8, 0.6) = (115-48, 80-36) = (67, 44)
  // Head = contact (115, 80)
  const SVG_PUSH_DIAG = '<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ground
    '<line x1="10" y1="135" x2="230" y2="135" stroke="#3d5470" stroke-width="1.5"/>'+
    '<line x1="10" y1="138" x2="230" y2="138" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // reference axes through contact point (115, 80) — horizontal+vertical
    '<line x1="20" y1="80" x2="220" y2="80" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="180" y="76" fill="#3d5470" font-size="9">แนวระดับ</text>'+
    // block
    '<rect x="105" y="80" width="50" height="55" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="62" y="115" fill="#38bdf8" font-size="12" font-weight="700">m</text>'+
    // F vector — tail far upper-left, arrowhead at contact (115,80)
    '<line x1="67" y1="44" x2="115" y2="80" stroke="#fbbf24" stroke-width="2.8" marker-end="url(#aY)"/>'+
    '<text x="50" y="40" fill="#fbbf24" font-size="13" font-weight="700">F</text>'+
    // angle θ between horizontal-left dashed (going from contact leftward) and F vector
    // contact (115,80). Horizontal-left at radius 28: (87, 80). F line at radius 28 from contact going BACKWARD along F = toward tail
    // F direction (tail->head): (0.8, 0.6). Backward (head->tail): (-0.8, -0.6)
    // Point on F at radius 28 from contact going backward: (115 - 28*0.8, 80 - 28*0.6) = (92.6, 63.2)
    // arc M 87 80 (on horizontal-left) A 28 28 0 0 1 92.6 63.2 (on F-extended-back) — sweep=1 (CW = curving up)
    '<path d="M 87 80 A 28 28 0 0 1 92.6 63.2" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="78" y="68" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    '</svg>';
  // S9: Block on flat ground + diagonal pull at θ above horizontal — refs through CoM
  // Block at (110, 105). Rope attached at upper-right of block (135, 90) — F direction (cos53, -sin53) = (0.6, -0.8) (up-right)
  // F tail at attach point, head far up-right
  // length 60: head = (135+60*0.6, 90-60*0.8) = (171, 42)
  const SVG_PULL_DIAG = '<svg viewBox="0 0 240 180" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ground
    '<line x1="10" y1="135" x2="230" y2="135" stroke="#3d5470" stroke-width="1.5"/>'+
    '<line x1="10" y1="138" x2="230" y2="138" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // reference axis (horizontal) through attach point (135, 90)
    '<line x1="20" y1="90" x2="220" y2="90" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="20" y="86" fill="#3d5470" font-size="9">แนวระดับ</text>'+
    // block
    '<rect x="85" y="90" width="50" height="45" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="55" y="120" fill="#38bdf8" font-size="12" font-weight="700">m</text>'+
    // F vector — tail at attach (135,90) on block, head up-right at (171, 42)
    '<line x1="135" y1="90" x2="171" y2="42" stroke="#fbbf24" stroke-width="2.8" marker-end="url(#aY)"/>'+
    '<text x="178" y="44" fill="#fbbf24" font-size="13" font-weight="700">F</text>'+
    // angle θ — between horizontal-right dashed and F (going up-right)
    // horizontal-right at radius 30 from (135,90): (165, 90)
    // F at radius 30 from (135,90): (135+30*0.6, 90-30*0.8) = (153, 66)
    // arc M 165 90 A 30 30 0 0 0 153 66 — sweep=0 (CCW = curving up-left)
    '<path d="M 165 90 A 30 30 0 0 0 153 66" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="155" y="80" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    '</svg>';
  // S10: Kid pushing cart
  const SVG_PUSH_CART = '<svg viewBox="0 0 220 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="105" x2="210" y2="105" stroke="#3d5470" stroke-width="1.4"/><text x="40" y="92" font-size="34">🧒</text><rect x="100" y="60" width="65" height="45" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><circle cx="115" cy="110" r="6" fill="#3d5470"/><circle cx="150" cy="110" r="6" fill="#3d5470"/><text x="120" y="88" fill="#38bdf8" font-size="13" font-weight="700">m</text><line x1="80" y1="75" x2="100" y2="75" stroke="#fbbf24" stroke-width="2.4"/><polygon points="103,75 92,70 92,80" fill="#fbbf24"/><text x="78" y="70" fill="#fbbf24" font-size="11" font-weight="700">F</text></svg>';
  // S11: Block + 2 horizontal opposing forces
  const SVG_BLOCK_2F = '<svg viewBox="0 0 240 110" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="90" x2="230" y2="90" stroke="#3d5470" stroke-width="1.4"/><rect x="95" y="50" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><text x="112" y="75" fill="#38bdf8" font-size="13" font-weight="700">m</text><line x1="145" y1="68" x2="220" y2="68" stroke="#fbbf24" stroke-width="2.6"/><polygon points="223,68 212,63 212,73" fill="#fbbf24"/><text x="170" y="62" fill="#fbbf24" font-size="11" font-weight="700">F₁</text><line x1="95" y1="68" x2="40" y2="68" stroke="#f472b6" stroke-width="2.4"/><polygon points="37,68 48,63 48,73" fill="#f472b6"/><text x="55" y="62" fill="#f472b6" font-size="11" font-weight="700">F₂</text></svg>';
  // S12: Block + 2 forces same direction
  const SVG_BLOCK_2SAME = '<svg viewBox="0 0 240 110" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="90" x2="230" y2="90" stroke="#3d5470" stroke-width="1.4"/><rect x="95" y="50" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><text x="112" y="75" fill="#38bdf8" font-size="13" font-weight="700">m</text><line x1="145" y1="62" x2="215" y2="62" stroke="#fbbf24" stroke-width="2.4"/><polygon points="218,62 207,57 207,67" fill="#fbbf24"/><text x="170" y="58" fill="#fbbf24" font-size="11" font-weight="700">F₁</text><line x1="145" y1="78" x2="190" y2="78" stroke="#fb923c" stroke-width="2.4"/><polygon points="193,78 182,73 182,83" fill="#fb923c"/><text x="160" y="74" fill="#fb923c" font-size="11" font-weight="700">F₂</text></svg>';
  // S13: Toy rocket up
  const SVG_ROCKET = '<svg viewBox="0 0 140 180" xmlns="http://www.w3.org/2000/svg"><polygon points="70,20 55,75 85,75" fill="rgba(248,113,113,.35)" stroke="#f87171" stroke-width="2"/><rect x="55" y="75" width="30" height="50" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><polygon points="55,125 40,150 55,140" fill="#fb923c" stroke="#f87171" stroke-width="1.5"/><polygon points="85,125 100,150 85,140" fill="#fb923c" stroke="#f87171" stroke-width="1.5"/><text x="50" y="170" font-size="20">🔥</text><line x1="115" y1="100" x2="115" y2="60" stroke="#34d399" stroke-width="2.4"/><polygon points="115,55 110,67 120,67" fill="#34d399"/><text x="120" y="80" fill="#34d399" font-size="11" font-weight="700">F</text><line x1="115" y1="120" x2="115" y2="160" stroke="#f87171" stroke-width="2.4"/><polygon points="115,163 110,151 120,151" fill="#f87171"/><text x="120" y="148" fill="#f87171" font-size="11" font-weight="700">W</text></svg>';
  // S14: Brake car (deceleration)
  const SVG_CAR_BRAKE = '<svg viewBox="0 0 220 110" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="90" x2="210" y2="90" stroke="#3d5470" stroke-width="1.4"/><rect x="80" y="50" width="90" height="40" rx="6" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><circle cx="100" cy="93" r="7" fill="#3d5470"/><circle cx="150" cy="93" r="7" fill="#3d5470"/><text x="115" y="76" fill="#38bdf8" font-size="11" font-weight="700">m</text><line x1="170" y1="68" x2="200" y2="68" stroke="#fbbf24" stroke-width="2" stroke-dasharray="3,2"/><polygon points="203,68 192,63 192,73" fill="#fbbf24"/><text x="178" y="62" fill="#fbbf24" font-size="10">v</text><line x1="80" y1="68" x2="40" y2="68" stroke="#f87171" stroke-width="2.4"/><polygon points="37,68 48,63 48,73" fill="#f87171"/><text x="48" y="62" fill="#f87171" font-size="11" font-weight="700">F (เบรก)</text></svg>';
  // S15: Person in elevator (moving up)
  const SVG_ELEVATOR = '<svg viewBox="0 0 160 180" xmlns="http://www.w3.org/2000/svg"><line x1="80" y1="5" x2="80" y2="30" stroke="#818cf8" stroke-width="2"/><rect x="30" y="30" width="100" height="130" fill="rgba(15,26,46,.5)" stroke="#3d5470" stroke-width="2"/><line x1="30" y1="158" x2="130" y2="158" stroke="#3d5470" stroke-width="2"/><text x="65" y="120" font-size="32">🧍</text><line x1="20" y1="65" x2="20" y2="35" stroke="#34d399" stroke-width="2.4"/><polygon points="20,30 15,42 25,42" fill="#34d399"/><text x="3" y="58" fill="#34d399" font-size="10" font-weight="700">a↑</text></svg>';
  // S16: Moon scale (apple on Earth vs Moon)
  const SVG_MOON_SCALE = '<svg viewBox="0 0 240 130" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="80" width="100" height="40" rx="6" fill="rgba(34,211,153,.18)" stroke="#34d399" stroke-width="1.6"/><text x="35" y="55" font-size="22">🍎</text><text x="20" y="105" fill="#34d399" font-size="11" font-weight="700">Earth g=10</text><rect x="130" y="80" width="100" height="40" rx="6" fill="rgba(129,140,248,.18)" stroke="#818cf8" stroke-width="1.6"/><text x="155" y="55" font-size="22">🍎</text><text x="138" y="105" fill="#818cf8" font-size="11" font-weight="700">Moon g≈1.6</text></svg>';
  // S17: Ball in space + force arrow (no surface)
  const SVG_BALL_SPACE = '<svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="1" fill="#fbbf24"/><circle cx="180" cy="40" r="1" fill="#fbbf24"/><circle cx="50" cy="100" r="1" fill="#fbbf24"/><circle cx="160" cy="110" r="1" fill="#fbbf24"/><circle cx="100" cy="65" r="22" fill="rgba(56,189,248,.3)" stroke="#38bdf8" stroke-width="2"/><text x="92" y="70" fill="#38bdf8" font-size="12" font-weight="700">m</text><line x1="122" y1="65" x2="180" y2="65" stroke="#fbbf24" stroke-width="2.4"/><polygon points="183,65 172,60 172,70" fill="#fbbf24"/><text x="145" y="58" fill="#fbbf24" font-size="11" font-weight="700">F</text></svg>';
  // S18: Car accelerating (force arrow on car)
  const SVG_CAR_FWD = '<svg viewBox="0 0 220 110" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="90" x2="210" y2="90" stroke="#3d5470" stroke-width="1.4"/><rect x="60" y="50" width="100" height="40" rx="8" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><rect x="75" y="40" width="50" height="14" fill="rgba(56,189,248,.18)" stroke="#38bdf8" stroke-width="1.5"/><circle cx="80" cy="93" r="7" fill="#3d5470"/><circle cx="140" cy="93" r="7" fill="#3d5470"/><text x="95" y="76" fill="#38bdf8" font-size="11" font-weight="700">m</text><line x1="160" y1="68" x2="200" y2="68" stroke="#fbbf24" stroke-width="2.6"/><polygon points="203,68 192,63 192,73" fill="#fbbf24"/><text x="175" y="62" fill="#fbbf24" font-size="11" font-weight="700">F</text></svg>';
  // S19: Runner starting (sprint pose with ground reaction)
  const SVG_RUNNER = '<svg viewBox="0 0 220 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="105" x2="210" y2="105" stroke="#3d5470" stroke-width="1.4"/><line x1="10" y1="108" x2="210" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="2,3"/><text x="60" y="95" font-size="40">🏃</text><line x1="120" y1="92" x2="170" y2="92" stroke="#fbbf24" stroke-width="2.6"/><polygon points="173,92 162,87 162,97" fill="#fbbf24"/><text x="135" y="86" fill="#fbbf24" font-size="11" font-weight="700">F (พื้นผลัก)</text></svg>';
  // S20: Skater pushing wall (action-reaction)
  const SVG_SKATER_WALL = '<svg viewBox="0 0 220 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="105" x2="210" y2="105" stroke="#3d5470" stroke-width="1.4"/><rect x="170" y="20" width="20" height="85" fill="rgba(61,84,112,.5)" stroke="#3d5470" stroke-width="2"/><text x="172" y="60" fill="#3d5470" font-size="10" transform="rotate(90 178 60)">ผนัง</text><text x="80" y="95" font-size="36">⛸️</text><line x1="155" y1="68" x2="115" y2="68" stroke="#fbbf24" stroke-width="2.6"/><polygon points="112,68 123,63 123,73" fill="#fbbf24"/><text x="118" y="62" fill="#fbbf24" font-size="10" font-weight="700">F (ผนังผลักกลับ)</text></svg>';
  // S21: Generic block + single horizontal force F
  const SVG_BLOCK_F = '<svg viewBox="0 0 200 130" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="105" x2="190" y2="105" stroke="#3d5470" stroke-width="1.4"/><line x1="10" y1="108" x2="190" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="2,3"/><rect x="75" y="65" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/><text x="92" y="90" fill="#38bdf8" font-size="13" font-weight="700">m</text><line x1="125" y1="85" x2="175" y2="85" stroke="#fbbf24" stroke-width="2.6"/><polygon points="178,85 167,80 167,90" fill="#fbbf24"/><text x="140" y="78" fill="#fbbf24" font-size="11" font-weight="700">F</text></svg>';
  // S22: Person standing on ground (W only)
  const SVG_PERSON_GND = '<svg viewBox="0 0 160 150" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="125" x2="150" y2="125" stroke="#3d5470" stroke-width="1.4"/><line x1="10" y1="128" x2="150" y2="128" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="2,3"/><text x="55" y="115" font-size="40">🧍</text><line x1="115" y1="80" x2="115" y2="120" stroke="#f87171" stroke-width="2.4"/><polygon points="115,123 110,111 120,111" fill="#f87171"/><text x="120" y="105" fill="#f87171" font-size="11" font-weight="700">W=mg</text></svg>';
  // S23: Rice bag on weighing scale
  const SVG_BAG_SCALE = '<svg viewBox="0 0 180 150" xmlns="http://www.w3.org/2000/svg"><rect x="50" y="100" width="80" height="20" rx="4" fill="rgba(61,84,112,.5)" stroke="#3d5470" stroke-width="2"/><rect x="60" y="115" width="60" height="15" fill="rgba(61,84,112,.7)" stroke="#3d5470" stroke-width="1.5"/><circle cx="90" cy="108" r="6" fill="#fbbf24"/><text x="86" y="112" fill="#000" font-size="9" font-weight="700">N</text><polygon points="60,90 70,40 110,40 120,90" fill="rgba(251,191,36,.25)" stroke="#fbbf24" stroke-width="2"/><text x="78" y="70" font-size="20">🌾</text><text x="55" y="35" fill="#fbbf24" font-size="11" font-weight="700">m kg</text></svg>';
  // S25: Block on flat ground + F applied right + friction f opposing (left) — refs through CoM
  const SVG_FRIC_FLAT = '<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    '<line x1="10" y1="125" x2="230" y2="125" stroke="#3d5470" stroke-width="1.5"/>'+
    '<line x1="10" y1="128" x2="230" y2="128" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // horizontal reference dashed through CoM
    '<line x1="20" y1="100" x2="225" y2="100" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="180" y="96" fill="#3d5470" font-size="9">แนวระดับ</text>'+
    // block
    '<rect x="95" y="80" width="50" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<circle cx="120" cy="100" r="2.5" fill="#e8f0ff"/>'+
    '<text x="60" y="105" fill="#38bdf8" font-size="12" font-weight="700">m</text>'+
    // F (yellow) — applied to right edge of block, pointing further right
    '<line x1="145" y1="100" x2="210" y2="100" stroke="#fbbf24" stroke-width="2.8" marker-end="url(#aY)"/>'+
    '<text x="170" y="94" fill="#fbbf24" font-size="13" font-weight="700">F</text>'+
    // f (pink) — friction on left side of block opposing motion (= pointing left)
    '<line x1="95" y1="100" x2="40" y2="100" stroke="#f472b6" stroke-width="2.6" marker-end="url(#aK)"/>'+
    '<text x="55" y="94" fill="#f472b6" font-size="13" font-weight="700">f</text>'+
    // direction-of-motion indicator above block
    '<line x1="155" y1="60" x2="195" y2="60" stroke="#3d5470" stroke-width="1" stroke-dasharray="2,3"/>'+
    '<polygon points="200,60 192,57 192,63" fill="#3d5470"/>'+
    '<text x="158" y="56" fill="#3d5470" font-size="9">การเคลื่อนที่</text>'+
    '</svg>';
  // S26: Block on smooth incline at θ=30° — shows W vertical + N perpendicular + reference axes
  const SVG_INC_SMOOTH = '<svg viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    '<line x1="10" y1="150" x2="270" y2="150" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<polygon points="40,150 240,150 240,35" fill="rgba(61,84,112,.18)" stroke="#3d5470" stroke-width="1.6"/>'+
    // angle θ at base
    '<path d="M 72 150 A 32 32 0 0 0 67.7 134" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="76" y="143" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    // reference axes through CoM (140, 92): parallel + perpendicular to incline
    '<line x1="105.4" y1="112" x2="174.6" y2="72" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="178" y="70" fill="#3d5470" font-size="9">ขนานพื้น</text>'+
    '<line x1="160" y1="126.6" x2="120" y2="57.4" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="100" y="56" fill="#3d5470" font-size="9">ตั้งฉากพื้น</text>'+
    // block rotated to align with incline
    '<rect x="120" y="77" width="40" height="30" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2" transform="rotate(-30 140 92)"/>'+
    '<circle cx="140" cy="92" r="2.5" fill="#e8f0ff"/>'+
    // N — perpendicular to incline (away from surface = direction (-sin30, -cos30) = (-0.5, -0.866))
    // length 50: end = (140 + 50*(-0.5), 92 + 50*(-0.866)) = (115, 48.7)
    '<line x1="140" y1="92" x2="115" y2="48.7" stroke="#34d399" stroke-width="2.6" marker-end="url(#aG)"/>'+
    '<text x="98" y="46" fill="#34d399" font-size="13" font-weight="700">N</text>'+
    // W — true vertical down
    '<line x1="140" y1="92" x2="140" y2="148" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="146" y="135" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    '</svg>';
  // S27: Block on incline at θ + friction (block sliding down, so f points up-slope)
  const SVG_INC_FRIC = '<svg viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    '<line x1="10" y1="150" x2="270" y2="150" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<polygon points="40,150 240,150 240,35" fill="rgba(61,84,112,.18)" stroke="#3d5470" stroke-width="1.6"/>'+
    // hatching on slope to indicate friction
    '<line x1="50" y1="148" x2="55" y2="155" stroke="#3d5470" stroke-width="0.6"/>'+
    '<line x1="100" y1="120" x2="105" y2="127" stroke="#3d5470" stroke-width="0.6"/>'+
    '<line x1="150" y1="92" x2="155" y2="99" stroke="#3d5470" stroke-width="0.6"/>'+
    '<line x1="200" y1="64" x2="205" y2="71" stroke="#3d5470" stroke-width="0.6"/>'+
    // angle θ at base
    '<path d="M 72 150 A 32 32 0 0 0 67.7 134" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="76" y="143" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    // reference axes through CoM
    '<line x1="105.4" y1="112" x2="174.6" y2="72" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="178" y="70" fill="#3d5470" font-size="9">ขนานพื้น</text>'+
    '<line x1="160" y1="126.6" x2="120" y2="57.4" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="100" y="56" fill="#3d5470" font-size="9">ตั้งฉากพื้น</text>'+
    // block rotated
    '<rect x="120" y="77" width="40" height="30" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2" transform="rotate(-30 140 92)"/>'+
    '<circle cx="140" cy="92" r="2.5" fill="#e8f0ff"/>'+
    // N perpendicular
    '<line x1="140" y1="92" x2="115" y2="48.7" stroke="#34d399" stroke-width="2.6" marker-end="url(#aG)"/>'+
    '<text x="98" y="46" fill="#34d399" font-size="13" font-weight="700">N</text>'+
    // W vertical
    '<line x1="140" y1="92" x2="140" y2="148" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="146" y="135" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    // f — parallel to slope, pointing UP-slope (opposing the down-slope motion)
    // direction up-slope: (cos30°, -sin30°) = (0.866, -0.5)
    // length 40: end = (140 + 40*0.866, 92 - 40*0.5) = (174.6, 72)
    '<line x1="140" y1="92" x2="174.6" y2="72" stroke="#f472b6" stroke-width="2.6" marker-end="url(#aK)"/>'+
    '<text x="178" y="68" fill="#f472b6" font-size="13" font-weight="700">f</text>'+
    // motion indicator (down-slope, dashed)
    '<line x1="170" y1="115" x2="205" y2="135" stroke="#3d5470" stroke-width="1" stroke-dasharray="2,3"/>'+
    '<polygon points="208,137 197,131 200,141" fill="#3d5470"/>'+
    '<text x="180" y="158" fill="#3d5470" font-size="9">ทิศไถล</text>'+
    '</svg>';
  // S29: Block on incline + W decomposed into mg sinθ (down-slope) + mg cosθ (perpendicular into surface)
  // θ=30°. Block at CoM (140,92). W vertical length 50. mg sinθ = 25 down-slope. mg cosθ = 43 perpendicular into surface.
  const SVG_INC_W_RESOLVE = '<svg viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    '<line x1="10" y1="150" x2="270" y2="150" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<polygon points="40,150 240,150 240,35" fill="rgba(61,84,112,.18)" stroke="#3d5470" stroke-width="1.6"/>'+
    '<path d="M 72 150 A 32 32 0 0 0 67.7 134" fill="none" stroke="#fbbf24" stroke-width="1.6"/>'+
    '<text x="76" y="143" fill="#fbbf24" font-size="11" font-weight="700">θ</text>'+
    // reference axes through CoM
    '<line x1="105.4" y1="112" x2="174.6" y2="72" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="178" y="70" fill="#3d5470" font-size="9">ขนานพื้น</text>'+
    '<line x1="160" y1="126.6" x2="120" y2="57.4" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="100" y="56" fill="#3d5470" font-size="9">ตั้งฉากพื้น</text>'+
    // block rotated
    '<rect x="120" y="77" width="40" height="30" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2" transform="rotate(-30 140 92)"/>'+
    '<circle cx="140" cy="92" r="2.5" fill="#e8f0ff"/>'+
    // W full vertical down
    '<line x1="140" y1="92" x2="140" y2="142" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="146" y="135" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    // mg sinθ component (down-slope direction (-cos30°, sin30°) = (-0.866, 0.5), length 25)
    '<line x1="140" y1="92" x2="118.3" y2="104.5" stroke="#fb923c" stroke-width="2.4" stroke-dasharray="5,2" marker-end="url(#aO)"/>'+
    '<text x="80" y="120" fill="#fb923c" font-size="11" font-weight="700">mg sinθ</text>'+
    // mg cosθ component (into surface, direction (sin30°, cos30°) = (0.5, 0.866), length 43)
    '<line x1="140" y1="92" x2="161.5" y2="129.3" stroke="#fb923c" stroke-width="2.4" stroke-dasharray="5,2" marker-end="url(#aO)"/>'+
    '<text x="166" y="138" fill="#fb923c" font-size="11" font-weight="700">mg cosθ</text>'+
    // parallelogram dashed (showing W = sum)
    '<line x1="118.3" y1="104.5" x2="139.85" y2="141.7" stroke="#fb923c" stroke-width="0.7" stroke-dasharray="2,2" stroke-opacity="0.5"/>'+
    '<line x1="161.5" y1="129.3" x2="139.85" y2="141.7" stroke="#fb923c" stroke-width="0.7" stroke-dasharray="2,2" stroke-opacity="0.5"/>'+
    '</svg>';
  // S30: Atwood machine — pulley on ceiling, m1 (lighter, going up) on left, m2 (heavier, going down) on right
  const SVG_ATWOOD = '<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // ceiling
    '<line x1="20" y1="20" x2="220" y2="20" stroke="#3d5470" stroke-width="2"/>'+
    '<line x1="20" y1="23" x2="220" y2="23" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // pulley support
    '<line x1="120" y1="23" x2="120" y2="40" stroke="#3d5470" stroke-width="2"/>'+
    '<circle cx="120" cy="55" r="14" fill="rgba(61,84,112,.4)" stroke="#3d5470" stroke-width="2"/>'+
    '<circle cx="120" cy="55" r="3" fill="#3d5470"/>'+
    // rope over pulley
    '<path d="M 106 55 A 14 14 0 0 1 134 55" fill="none" stroke="#818cf8" stroke-width="2"/>'+
    '<line x1="106" y1="55" x2="106" y2="145" stroke="#818cf8" stroke-width="2"/>'+
    '<line x1="134" y1="55" x2="134" y2="115" stroke="#818cf8" stroke-width="2"/>'+
    // m1 (left, smaller)
    '<rect x="86" y="145" width="40" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="98" y="170" fill="#38bdf8" font-size="14" font-weight="700">m₁</text>'+
    // m2 (right, larger)
    '<rect x="110" y="115" width="50" height="50" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="125" y="146" fill="#38bdf8" font-size="14" font-weight="700">m₂</text>'+
    // W on m1 (down)
    '<line x1="106" y1="185" x2="106" y2="215" stroke="#f87171" stroke-width="2.4" marker-end="url(#aR)"/>'+
    '<text x="78" y="208" fill="#f87171" font-size="11" font-weight="700">m₁g</text>'+
    // W on m2 (down)
    '<line x1="135" y1="165" x2="135" y2="200" stroke="#f87171" stroke-width="2.4" marker-end="url(#aR)"/>'+
    '<text x="142" y="194" fill="#f87171" font-size="11" font-weight="700">m₂g</text>'+
    // direction arrows: m1 up, m2 down
    '<line x1="50" y1="180" x2="50" y2="150" stroke="#3d5470" stroke-width="1.2" stroke-dasharray="2,2"/>'+
    '<polygon points="50,146 47,156 53,156" fill="#3d5470"/>'+
    '<text x="42" y="195" fill="#3d5470" font-size="10">a</text>'+
    '<line x1="195" y1="125" x2="195" y2="165" stroke="#3d5470" stroke-width="1.2" stroke-dasharray="2,2"/>'+
    '<polygon points="195,169 192,158 198,158" fill="#3d5470"/>'+
    '<text x="200" y="150" fill="#3d5470" font-size="10">a</text>'+
    '</svg>';
  // S31: Block A on smooth table + pulley at edge + block B hanging off edge
  const SVG_PULLEY_TABLE = '<svg viewBox="0 0 290 220" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // table top
    '<line x1="10" y1="90" x2="200" y2="90" stroke="#3d5470" stroke-width="2"/>'+
    '<line x1="10" y1="93" x2="200" y2="93" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // table edge (vertical, supporting hanging mass)
    '<line x1="200" y1="90" x2="200" y2="200" stroke="#3d5470" stroke-width="2"/>'+
    // pulley at corner
    '<circle cx="210" cy="88" r="10" fill="rgba(61,84,112,.4)" stroke="#3d5470" stroke-width="2"/>'+
    '<circle cx="210" cy="88" r="2" fill="#3d5470"/>'+
    // block A on table
    '<rect x="80" y="60" width="42" height="30" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="95" y="80" fill="#38bdf8" font-size="14" font-weight="700">A</text>'+
    // rope from A → pulley → down to B
    '<line x1="122" y1="75" x2="200" y2="75" stroke="#818cf8" stroke-width="2"/>'+
    '<path d="M 200 75 A 13 13 0 0 1 220 88" fill="none" stroke="#818cf8" stroke-width="2"/>'+
    '<line x1="220" y1="88" x2="220" y2="155" stroke="#818cf8" stroke-width="2"/>'+
    // block B hanging
    '<rect x="200" y="155" width="40" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="214" y="180" fill="#38bdf8" font-size="14" font-weight="700">B</text>'+
    // T on A (rightward)
    '<line x1="122" y1="50" x2="170" y2="50" stroke="#818cf8" stroke-width="2.4" marker-end="url(#aP)"/>'+
    '<text x="138" y="44" fill="#818cf8" font-size="12" font-weight="700">T</text>'+
    // T on B (upward)
    '<line x1="255" y1="180" x2="255" y2="150" stroke="#818cf8" stroke-width="2.4" marker-end="url(#aP)"/>'+
    '<text x="262" y="170" fill="#818cf8" font-size="12" font-weight="700">T</text>'+
    // W on B (downward)
    '<line x1="220" y1="195" x2="220" y2="215" stroke="#f87171" stroke-width="2.4" marker-end="url(#aR)"/>'+
    '<text x="160" y="212" fill="#f87171" font-size="11" font-weight="700">W_B = m_B·g</text>'+
    '</svg>';
  // S32: 2 blocks connected by rope on horizontal surface, F applied to right block
  const SVG_2BLOCK_TABLE = '<svg viewBox="0 0 260 140" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    '<line x1="10" y1="105" x2="250" y2="105" stroke="#3d5470" stroke-width="1.5"/>'+
    '<line x1="10" y1="108" x2="250" y2="108" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    // block A (left, smaller)
    '<rect x="55" y="65" width="40" height="40" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="68" y="90" fill="#38bdf8" font-size="14" font-weight="700">A</text>'+
    // rope between
    '<line x1="95" y1="85" x2="125" y2="85" stroke="#818cf8" stroke-width="2"/>'+
    '<text x="100" y="79" fill="#818cf8" font-size="11" font-weight="700">T</text>'+
    // block B (right, larger)
    '<rect x="125" y="60" width="50" height="45" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<text x="143" y="88" fill="#38bdf8" font-size="14" font-weight="700">B</text>'+
    // F applied to B (rightward)
    '<line x1="175" y1="82" x2="240" y2="82" stroke="#fbbf24" stroke-width="2.8" marker-end="url(#aY)"/>'+
    '<text x="200" y="76" fill="#fbbf24" font-size="13" font-weight="700">F</text>'+
    '</svg>';
  // S33: Object falling in fluid — W down + R up (drag depends on v)
  const SVG_FALL_FLUID = '<svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // fluid background (subtle blue tint)
    '<rect x="20" y="20" width="160" height="190" fill="rgba(56,189,248,.06)" stroke="#3d5470" stroke-width="1" stroke-dasharray="2,4"/>'+
    '<text x="135" y="35" fill="#3d5470" font-size="9">ของไหล</text>'+
    // vertical reference dashed through CoM
    '<line x1="100" y1="25" x2="100" y2="205" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="103" y="38" fill="#3d5470" font-size="9">แนวดิ่ง</text>'+
    // ball / object
    '<circle cx="100" cy="115" r="20" fill="rgba(56,189,248,.25)" stroke="#38bdf8" stroke-width="2"/>'+
    '<circle cx="100" cy="115" r="2.5" fill="#e8f0ff"/>'+
    '<text x="60" y="120" fill="#38bdf8" font-size="12" font-weight="700">m</text>'+
    // R (drag, up) — opposes motion (object falling down → R points up)
    '<line x1="100" y1="115" x2="100" y2="55" stroke="#34d399" stroke-width="2.6" marker-end="url(#aG)"/>'+
    '<text x="106" y="65" fill="#34d399" font-size="13" font-weight="700">R</text>'+
    // W (weight, down)
    '<line x1="100" y1="115" x2="100" y2="195" stroke="#f87171" stroke-width="2.6" marker-end="url(#aR)"/>'+
    '<text x="106" y="183" fill="#f87171" font-size="13" font-weight="700">W</text>'+
    // motion indicator (down)
    '<line x1="155" y1="100" x2="155" y2="135" stroke="#3d5470" stroke-width="1" stroke-dasharray="2,3"/>'+
    '<polygon points="155,138 152,127 158,127" fill="#3d5470"/>'+
    '<text x="160" y="125" fill="#3d5470" font-size="9">v</text>'+
    '</svg>';
  // S34: v-t graph for terminal velocity — steep at start, flattens to horizontal at v_t
  const SVG_VT_TERMINAL = '<svg viewBox="0 0 240 160" xmlns="http://www.w3.org/2000/svg">'+DEFS+
    // axes
    '<line x1="30" y1="20" x2="30" y2="135" stroke="#e8f0ff" stroke-width="1.5"/>'+
    '<polygon points="30,15 26,25 34,25" fill="#e8f0ff"/>'+
    '<line x1="30" y1="135" x2="220" y2="135" stroke="#e8f0ff" stroke-width="1.5"/>'+
    '<polygon points="225,135 215,131 215,139" fill="#e8f0ff"/>'+
    '<text x="8" y="25" fill="#fbbf24" font-size="11">v(m/s)</text>'+
    '<text x="200" y="148" fill="#fbbf24" font-size="11">t(s)</text>'+
    // v_t reference dashed line (horizontal)
    '<line x1="30" y1="40" x2="220" y2="40" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="3,3"/>'+
    '<text x="5" y="44" fill="#34d399" font-size="11" font-weight="700">v_t</text>'+
    // curve: v(t) approaches v_t — using path: start (30,135), curve up steep, then asymptote to (220,40)
    '<path d="M 30 135 Q 60 60 130 45 T 220 41" fill="none" stroke="#f87171" stroke-width="2.6"/>'+
    // labels
    '<text x="50" y="100" fill="#f87171" font-size="10">ชันมาก</text>'+
    '<text x="100" y="35" fill="#f87171" font-size="10">ชันลด</text>'+
    '<text x="160" y="58" fill="#f87171" font-size="10">~คงที่</text>'+
    '</svg>';
  // S28: Person jumping up (force arrows)
  const SVG_JUMP = '<svg viewBox="0 0 180 150" xmlns="http://www.w3.org/2000/svg"><line x1="10" y1="125" x2="170" y2="125" stroke="#3d5470" stroke-width="1.4"/><line x1="10" y1="128" x2="170" y2="128" stroke="#3d5470" stroke-width="0.8" stroke-dasharray="2,3"/><text x="55" y="115" font-size="40">🤸</text><line x1="125" y1="115" x2="125" y2="55" stroke="#34d399" stroke-width="2.4"/><polygon points="125,50 120,62 130,62" fill="#34d399"/><text x="130" y="78" fill="#34d399" font-size="10" font-weight="700">F (พื้นผลัก)</text><line x1="100" y1="115" x2="100" y2="140" stroke="#f87171" stroke-width="2.4"/><polygon points="100,143 95,131 105,131" fill="#f87171"/><text x="60" y="138" fill="#f87171" font-size="10" font-weight="700">W</text></svg>';

  const F_TAG = ['forces-c'];
  function M(id, statement, choices, correct, hints, figure){
    const arr = choices.map((t,i) => ({key:String.fromCharCode(65+i), text:t}));
    const q = {id, group:'C', stage:'c', noReveal:true, type:'mcq', statement, choices:arr, correct, hints, formula_tags:F_TAG};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }
  function F(id, statement, correctList, hints, figure){
    const q = {id, group:'C', stage:'c', noReveal:true, type:'fill', statement, correct: correctList, hints, formula_tags:F_TAG, tolerance:0.02};
    if(figure) q.figure = figure;
    q.title = statement.replace(/<[^>]+>/g,'').slice(0,50);
    return q;
  }

  const Q = [
    // ════════ C1 — F = ma แบบตรงๆ (C01-C09) ════════
    M('C01','เด็กผลักรถเข็นมวล 8 kg ด้วยแรง 24 N บนพื้นไร้เสียดทาน · จงหาความเร่งของรถเข็น',
      ['2 m/s²','3 m/s² (a = F/m = 24/8)','4 m/s²','6 m/s²'],'B',H_FMA),
    M('C02','ลูกบอล 2 kg ลอยอิสระในอวกาศ · ถูกแรง 6 N ผลักทางเดียว · ความเร่ง = ?',
      ['1 m/s²','2 m/s²','3 m/s² (a = 6/2)','12 m/s²'],'C',H_FMA),
    M('C03','รถยนต์ 1000 kg เร่งตัวด้วยอัตราเร่ง 2 m/s² · จงหาแรงสุทธิที่กระทำกับรถ',
      ['500 N','1000 N','2000 N (F = ma = 1000×2)','5000 N'],'C',H_FMA),
    M('C04','นักวิ่ง 60 kg ออกตัว · พื้นผลักเขาไปข้างหน้า 120 N (ไม่มีแรงต้าน) · ความเร่งขณะออกตัว = ?',
      ['1 m/s²','2 m/s² (a = 120/60)','3 m/s²','5 m/s²'],'B',H_FMA),
    M('C05','รถ 1500 kg เพิ่มความเร็วจาก 5 m/s ถึง 25 m/s ใน 4 วินาที · จงหาแรงสุทธิ',
      ['3000 N','5000 N','7500 N (a = 20/4 = 5 · F = 1500×5)','30000 N'],'C',H_FMA),
    M('C06','รถบรรทุก 2000 kg เคลื่อนที่ไปข้างหน้า ถูกเบรกด้วยแรง 4000 N ทิศตรงข้ามการเคลื่อนที่ · ความเร่ง = ?',
      ['−1 m/s²','−2 m/s² (a = −F/m = −4000/2000)','−4 m/s²','−10 m/s²'],'B',H_FMA),
    M('C07','นักสเก็ต 60 kg ผลักผนัง · ผนังผลักกลับมา 90 N · ความเร่งของนักสเก็ตขณะออกตัว = ?',
      ['1 m/s²','1.5 m/s² (a = 90/60)','2 m/s²','3 m/s²'],'B',H_FMA),
    F('C08','กล่อง 4 kg ถูกแรงลัพธ์ 12 N · ความเร่ง (m/s²) = ?',[3],H_FMA),
    F('C09','รถ 800 kg ถูกเบรกด้วยแรง 2000 N · ขนาดความเร่ง (m/s²) = ?',[2.5],H_FMA),

    // ════════ C2 — W = mg (C10-C15) ════════
    M('C10','นักเรียนมวล 50 kg ยืนบนพื้น · g = 10 m/s² · น้ำหนักของนักเรียน = ?',
      ['5 N','50 N','500 N (W = mg = 50×10)','5000 N'],'C',H_WMG),
    M('C11','ถุงข้าวสารมวล 25 kg วางบนตาชั่ง · g = 10 · ตาชั่ง (วัดเป็นนิวตัน) อ่านได้',
      ['25 N','100 N','250 N (W = 25×10)','2500 N'],'C',H_WMG),
    M('C12','นักบินอวกาศมวล 60 kg ยืนบนผิวดวงจันทร์ · g_จันทร์ ≈ 1.6 m/s² · น้ำหนักบนดวงจันทร์ = ?',
      ['60 N','96 N (W = 60×1.6)','600 N','960 N'],'B',H_WMG),
    M('C13','วัตถุชนิดเดียวกัน บนโลก W = 200 N · g_โลก = 10 · g_จันทร์ ≈ 1.6 · น้ำหนักบนดวงจันทร์ ≈',
      ['200 N (น้ำหนักไม่เปลี่ยน)','100 N','32 N (m = 200/10 = 20 kg · W_จันทร์ = 20×1.6)','20 N'],'C',H_WMG),
    F('C14','กล่อง 8 kg วางบนโต๊ะ · g = 10 · น้ำหนัก (N) = ?',[80],H_WMG),
    F('C15','น้ำหนักวัตถุ W = 300 N · g = 10 · มวลวัตถุ (kg) = ?',[30],H_WMG),

    // ════════ C3 — ΣF = ma (หลายแรงรวม) (C16-C23) ════════
    M('C16','กล่อง 4 kg บนพื้นเรียบ ถูกแรง 2 แรงในแนวระดับ: ขวา 20 N · ซ้าย 8 N · ความเร่ง = ?',
      ['2 m/s² ขวา','3 m/s² ขวา (ΣF = 12 N · a = 12/4)','7 m/s² ขวา','5 m/s² ขวา'],'B',H_SUMF,SVG_BLOCK_2F),
    M('C17','กล่อง 5 kg บนพื้นเรียบ มี 2 แรงทิศเดียวกัน: 30 N + 10 N · ความเร่ง = ?',
      ['4 m/s²','6 m/s²','8 m/s² (ΣF = 40 N · a = 40/5)','40 m/s²'],'C',H_SUMF,SVG_BLOCK_2SAME),
    M('C18','กล่อง 3 kg บนพื้นเรียบ ถูกแรง: ขวา 9 N · ซ้าย 6 N · ความเร่ง = ?',
      ['1 m/s² ขวา (ΣF = 3 N · a = 3/3)','3 m/s² ขวา','5 m/s² ขวา','15 m/s² ขวา'],'A',H_SUMF,SVG_BLOCK_2F),
    M('C19','กล่อง 2 kg บนพื้นเรียบ ถูกแรงดึงเชือก 10 N เฉียง 37° เหนือแนวระดับ (cos37=0.8) · ความเร่งในแนวระดับ = ?',
      ['2 m/s²','3 m/s²','4 m/s² (a = F·cos37 / m = 8/2)','5 m/s²'],'C',H_SUMF,SVG_PULL_DIAG),
    M('C20','กล่อง 4 kg บนพื้นเรียบ ถูกแรงดึงเฉียง 53° เหนือระดับ ขนาด 20 N (cos53=0.6) · ความเร่งแนวระดับ = ?',
      ['2 m/s²','3 m/s² (a = 20×0.6/4 = 12/4)','4 m/s²','5 m/s²'],'B',H_SUMF,SVG_PULL_DIAG),
    M('C21','จรวดของเล่น 0.5 kg มีแรงขับขึ้น 8 N · g=10 · ความเร่ง (ทิศ + คือขึ้น) = ?',
      ['3 m/s² ลง','6 m/s² ขึ้น (ΣF = 8 − 5 = 3 N · a = 3/0.5)','10 m/s² ขึ้น','16 m/s² ขึ้น'],'B',H_SUMF),
    F('C22','คน 50 kg กระโดด · พื้นผลักเขาขึ้น 800 N · g=10 · ขนาดความเร่งสุทธิทิศขึ้น (m/s²) = ?',[6],H_SUMF),
    F('C23','กล่อง 2 kg บนพื้นเรียบ ถูกแรง 10 N เฉียง 37° เหนือระดับ (cos37=0.8) · ความเร่งแนวระดับ (m/s²) = ?',[4],H_SUMF,SVG_PULL_DIAG),

    // ════════ C4 — Equilibrium (หา T, N, f ที่ขาด) (C24-C37) ════════
    M('C24','กล่องหนังสือมวล 4 kg วางนิ่งบนโต๊ะ · g = 10 · แรงปกติจากโต๊ะ = ?',
      ['20 N','30 N','40 N (= mg เพราะกล่องนิ่ง ΣF=0)','50 N'],'C',H_EQ,SVG_BLOCK_GND),
    M('C25','โคมไฟ 2 kg แขวนกับเพดานด้วยเชือกเส้นเดียว · g=10 · แรงตึงในเชือก = ?',
      ['10 N','15 N','20 N (T = mg)','40 N'],'C',H_EQ,SVG_LAMP_HANG),
    M('C26','กล่องมวล 5 kg วางบนพื้น · มีคนเอามือกดลงด้วยแรง 30 N · g=10 · แรงปกติจากพื้น = ?',
      ['50 N','30 N','20 N','80 N (= mg + แรงกด = 50 + 30)'],'D',H_EQ),
    M('C27','กล่อง 6 kg อยู่บนพื้น · คนพยายามยกขึ้นด้วยแรง 20 N (กล่องยังไม่ลอย) · g=10 · แรงปกติจากพื้น = ?',
      ['60 N','80 N','40 N (= mg − F = 60 − 20)','20 N'],'C',H_EQ),
    M('C28','นกแก้วมวล 0.5 kg เกาะกลางเชือกที่ขึงในแนวระดับ · เชือกหย่อนทำมุม 30° กับแนวระดับทั้ง 2 ฝั่ง · g=10 · แรงตึงในเชือกแต่ละข้าง = ?',
      ['2.5 N','5 N (2T·sin30 = mg → T = 5/(2×0.5))','7.5 N','10 N'],'B',H_EQ,SVG_BIRD_V),
    M('C29','โคมไฟ 3 kg ห้อยจากเพดานด้วย 2 เชือกสมมาตร · เชือกแต่ละเส้นทำมุม 53° กับแนวดิ่ง (cos53=0.6) · g=10 · แรงตึงในเชือกแต่ละเส้น = ?',
      ['15 N','20 N','25 N (2T·cos53 = mg → T = 30/(2×0.6))','30 N'],'C',H_EQ,SVG_LAMP_2ROPE),
    M('C30','กล่อง 2 kg วางนิ่งบนพื้นเอียงเรียบ 30° · มีเชือกขนานพื้นเอียงดึงกล่องไม่ให้ไถล · g=10 · แรงตึงในเชือก = ?',
      ['5 N','10 N (T = mg sin30 = 20×0.5)','15 N','20 N'],'B',H_INCLINE,SVG_INC_ROPE),
    M('C31','กล่อง 4 kg บนพื้นราบ มีแรงกดเฉียง 37° ต่ำกว่าแนวระดับ ขนาด 10 N (sin37=0.6) · g=10 · แรงปกติจากพื้น = ?',
      ['34 N','40 N','46 N (= mg + F·sin37 = 40 + 6)','50 N'],'C',H_EQ,SVG_PUSH_DIAG),
    M('C32','กล่อง 5 kg บนพื้นราบ มีคนดึงเชือกเฉียง 53° เหนือแนวระดับด้วยแรง 20 N (กล่องยังไม่ลอย, sin53=0.8) · g=10 · แรงปกติ = ?',
      ['50 N','34 N (= mg − F·sin53 = 50 − 16)','42 N','58 N'],'B',H_EQ,SVG_PULL_DIAG),
    M('C33','กล่อง 8 kg ในลิฟต์ที่จอดนิ่ง · g=10 · แรงปกติจากพื้นลิฟต์ = ?',
      ['40 N','60 N','80 N (ลิฟต์นิ่ง a=0 → N=mg)','100 N'],'C',H_EQ),
    F('C34','โคม 2.5 kg แขวนเชือกเส้นเดียวจากเพดาน · g=10 · แรงตึง T (N) = ?',[25],H_EQ),
    F('C35','กล่อง 3 kg บนพื้น · มีคนเหยียบลงด้วยแรง 12 N · g=10 · แรงปกติจากพื้น (N) = ?',[42],H_EQ),
    F('C36','โคมไฟ 4 kg ห้อย 2 เชือกสมมาตร · เชือกแต่ละเส้นทำมุม 53° กับแนวดิ่ง (cos53=0.6) · g=10 · แรงตึงเชือกแต่ละเส้น (N) ≈ ?',[33.33],H_EQ,SVG_LAMP_2ROPE),
    F('C37','กล่อง 3 kg บนพื้นเอียงเรียบ 37° · เชือกขนานพื้นดึงนิ่ง (sin37=0.6) · g=10 · แรงตึง T (N) = ?',[18],H_INCLINE,SVG_INC_ROPE),

    // ════════ C5 — แรงเสียดทาน f = μN (C38-C59) ════════
    M('C38','กล่อง 5 kg วางบนพื้นราบ · μ_k = 0.4 · g=10 · ขณะกล่องไถลด้วยความเร็วคงที่ · แรงเสียดทาน f = ?',
      ['10 N','15 N','20 N (f = μN = 0.4 × 50)','25 N'],'C',H_FRIC),
    M('C39','กล่อง 10 kg ถูกลากบนพื้นราบ · μ_k = 0.2 · g=10 · แรงเสียดทานจลน์ = ?',
      ['10 N','20 N (= 0.2 × 100)','40 N','100 N'],'B',H_FRIC),
    M('C40','กล่อง 4 kg บนพื้นราบ · ขณะไถลวัดได้ f = 12 N · g=10 · ค่า μ_k = ?',
      ['0.2','0.3 (μ = f/N = 12/40)','0.4','0.5'],'B',H_FRIC),
    M('C41','ความสัมพันธ์ระหว่าง μ_s (สถิต) กับ μ_k (จลน์) คือ',
      ['μ_s < μ_k','μ_s = μ_k','μ_s > μ_k (สถิตมากกว่า — เริ่มต้นไถลยากกว่ารักษาการไถล)','ขึ้นกับมวล'],'C',H_FRIC),
    M('C42','กล่องกำลังไถลไปทางขวาบนพื้น · ทิศของแรงเสียดทาน f บนกล่อง คือ',
      ['ขวา (ตามการเคลื่อนที่)','ซ้าย (ต้านการเคลื่อนที่)','ขึ้น','ลง'],'B',H_FRIC,SVG_FRIC_FLAT),
    M('C43','กล่องนิ่งบนพื้น · มีคนผลักไปทางขวาแต่กล่องยังไม่เคลื่อน · ทิศของแรงเสียดทานสถิต f_s บนกล่อง คือ',
      ['ขวา','ซ้าย (ต้าน "แนวโน้ม" ที่จะเคลื่อนไปขวา)','ไม่มี','ขึ้น'],'B',H_FRIC,SVG_FRIC_FLAT),
    M('C44','ขีดเริ่มไถล (impending motion) เกิดเมื่อ F ที่ดึงมีขนาดเท่ากับ',
      ['μ_k · N','μ_s · N (เกินค่านี้กล่องเริ่มเคลื่อน)','mg','m·a'],'B',H_FRIC),
    M('C45','กล่อง 4 kg บนพื้น · μ_s = 0.5 · g=10 · แรงดึงน้อยที่สุดที่ทำให้เริ่มไถล = ?',
      ['10 N','15 N','20 N (F = μ_s · mg = 0.5 × 40)','40 N'],'C',H_FRIC),
    M('C46','กล่อง 5 kg ถูกดึงด้วยแรง 40 N ในแนวระดับ · μ_k = 0.4 · g=10 · ความเร่ง = ?',
      ['2 m/s²','3 m/s²','4 m/s² (f = 20 · ΣF = 40−20 = 20 · a = 20/5)','8 m/s²'],'C',H_FRIC,SVG_FRIC_FLAT),
    M('C47','กล่อง 4 kg ถูกดึง 20 N · μ_k = 0.3 · g=10 · ความเร่ง = ?',
      ['1 m/s²','2 m/s² (f = 12 · ΣF = 8 · a = 8/4)','3 m/s²','5 m/s²'],'B',H_FRIC,SVG_FRIC_FLAT),
    M('C48','กล่อง 3 kg ถูกดึง 15 N · μ_k = 0.2 · g=10 · ความเร่ง = ?',
      ['1 m/s²','2 m/s²','3 m/s² (f = 6 · ΣF = 9 · a = 9/3)','4 m/s²'],'C',H_FRIC,SVG_FRIC_FLAT),
    M('C49','กล่อง 10 kg ถูกดึง 30 N · μ_k = 0.1 · g=10 · ความเร่ง = ?',
      ['1 m/s²','2 m/s² (f = 10 · ΣF = 20 · a = 20/10)','3 m/s²','5 m/s²'],'B',H_FRIC,SVG_FRIC_FLAT),
    M('C50','กล่อง 2 kg ถูกดึง 20 N เฉียง 37° เหนือแนวระดับ · μ_k = 0.5 · g=10 (cos37=0.8 sin37=0.6) · ความเร่งแนวระดับ = ?',
      ['4 m/s²','5 m/s²','6 m/s² (Fcos37=16 · N=mg−Fsin37=20−12=8 · f=4 · ΣF=12 · a=12/2)','8 m/s²'],'C',H_FRIC,SVG_PULL_DIAG),
    M('C51','กล่อง 2 kg ถูกดึง 20 N เฉียง 53° เหนือระดับ · μ_k = 0.5 · g=10 (cos53=0.6 sin53=0.8) · ความเร่งแนวระดับ = ?',
      ['3 m/s²','4 m/s²','5 m/s² (Fcos53=12 · N=20−16=4 · f=2 · ΣF=10 · a=5)','6 m/s²'],'C',H_FRIC,SVG_PULL_DIAG),
    M('C52','กล่องไถลลงพื้นเอียงเรียบมุม 37° (sin37=0.6) · g=10 · ความเร่ง = ?',
      ['4 m/s²','6 m/s² (a = g·sin37 = 10×0.6)','8 m/s²','10 m/s²'],'B',H_INCLINE,SVG_INC_SMOOTH),
    M('C53','กล่องไถลลงพื้นเอียงเรียบมุม 30° · g=10 · ความเร่ง = ?',
      ['2.5 m/s²','5 m/s² (a = g·sin30 = 10×0.5)','7.5 m/s²','10 m/s²'],'B',H_INCLINE,SVG_INC_SMOOTH),
    M('C54','กล่อง 2 kg ไถลลงพื้นเอียงมุม 37° · μ_k = 0.25 · g=10 (sin37=0.6 cos37=0.8) · ความเร่ง = ?',
      ['2 m/s²','3 m/s²','4 m/s² (a = g(sin37 − μcos37) = 10(0.6 − 0.2))','6 m/s²'],'C',H_INCLINE,SVG_INC_FRIC),
    M('C55','กล่องไถลลงพื้นเอียงมุม 53° · μ_k = 0.5 · g=10 (sin53=0.8 cos53=0.6) · ความเร่ง = ?',
      ['3 m/s²','4 m/s²','5 m/s² (a = 10(0.8 − 0.5×0.6) = 10×0.5)','6.5 m/s²'],'C',H_INCLINE,SVG_INC_FRIC),
    M('C56','พื้นเอียงเรียบ ค่อยๆ เพิ่มมุม θ จาก 0° → 90° · ความเร่งของกล่องที่ไถลลง',
      ['คงที่','ลดลง','เพิ่มขึ้นตาม sinθ (จาก 0 ที่ θ=0° ถึง g ที่ θ=90°)','เพิ่มแบบ exponential'],'C',H_INCLINE),
    F('C57','กล่อง 4 kg บนพื้นราบ · μ_k = 0.3 · g=10 · ขนาดแรงเสียดทาน (N) = ?',[12],H_FRIC),
    F('C58','กล่อง 8 kg บนพื้น · μ_s = 0.4 · g=10 · แรงน้อยที่สุดที่เริ่มไถล (N) = ?',[32],H_FRIC),
    F('C59','กล่อง 4 kg ถูกดึง 24 N ในแนวระดับ · μ_k = 0.2 · g=10 · ความเร่ง (m/s²) = ?',[4],H_FRIC,SVG_FRIC_FLAT),

    // ════════ C6 — ลิฟต์ (น้ำหนักปรากฏ) (C60-C73) ════════
    M('C60','คน 50 kg ในลิฟต์เร่งขึ้นด้วย 2 m/s² · g=10 · แรงปกติจากพื้นลิฟต์ (น้ำหนักรู้สึก) = ?',
      ['400 N','500 N','600 N (N = m(g+a) = 50×12)','700 N'],'C',H_LIFT),
    M('C61','คน 50 kg ในลิฟต์เร่งลงด้วย 2 m/s² (ไม่ใช่ตกอิสระ) · g=10 · แรงปกติ = ?',
      ['300 N','400 N (N = m(g−a) = 50×8)','500 N','600 N'],'B',H_LIFT),
    M('C62','คน 50 kg ในลิฟต์ที่เคลื่อนที่ขึ้นด้วยความเร็วคงที่ (a = 0) · g=10 · แรงปกติ = ?',
      ['400 N','450 N','500 N (a=0 → N=mg)','550 N'],'C',H_LIFT),
    M('C63','คน 50 kg ในลิฟต์ตกอิสระ (a = g) · g=10 · แรงปกติ = ?',
      ['0 N (ไร้น้ำหนักชั่วคราว — N=m(g−g))','250 N','500 N','1000 N'],'A',H_LIFT),
    M('C64','คน 80 kg ในลิฟต์เร่งขึ้น 5 m/s² · g=10 · แรงปกติ = ?',
      ['400 N','800 N','1200 N (N = 80×15)','1600 N'],'C',H_LIFT),
    M('C65','คน 60 kg ในลิฟต์เร่งลง 4 m/s² · g=10 · แรงปกติ = ?',
      ['240 N','360 N (N = 60×6)','480 N','600 N'],'B',H_LIFT),
    M('C66','คน 60 kg ในลิฟต์เร่งขึ้น 2 m/s² · g=10 · แรงปกติ = ?',
      ['600 N','660 N','720 N (N = 60×12)','780 N'],'C',H_LIFT),
    M('C67','คน 50 kg ยืนบนตาชั่งสปริงในลิฟต์ · ตาชั่งอ่านได้ 600 N · g=10 · ลิฟต์กำลัง',
      ['ตกอิสระ','เคลื่อนที่ความเร็วคงที่','เร่งขึ้นด้วย 2 m/s² (m(g+a)=600 → a=2)','เร่งลงด้วย 2 m/s²'],'C',H_LIFT),
    M('C68','คน 50 kg บนตาชั่งสปริงในลิฟต์ · ตาชั่งอ่านได้ 400 N · g=10 · ลิฟต์กำลัง',
      ['เร่งขึ้น 2 m/s²','เร่งลง 2 m/s² (m(g−a)=400 → a=2 ทิศลง)','ตกอิสระ','นิ่ง'],'B',H_LIFT),
    M('C69','"รู้สึกหนักกว่าปกติ" ในลิฟต์ เกิดเมื่อ',
      ['ลิฟต์เร่งลง','ลิฟต์เคลื่อนที่ความเร็วคงที่','ลิฟต์ตกอิสระ','ลิฟต์เร่งขึ้น (N > mg)'],'D',H_LIFT),
    M('C70','"รู้สึกเบากว่าปกติ" ในลิฟต์ เกิดเมื่อ',
      ['ลิฟต์เร่งขึ้น','ลิฟต์นิ่ง','ลิฟต์เร่งลง (N < mg)','ลิฟต์เคลื่อนที่ขึ้นด้วยความเร็วคงที่'],'C',H_LIFT),
    M('C71','สาเหตุที่นักบินอวกาศใน ISS รู้สึกไร้น้ำหนัก (ทั้งที่อยู่ในวงโคจร) คือ',
      ['ไม่มีแรงโน้มถ่วงในอวกาศ','ISS กำลังตกอิสระรอบโลก (a ≈ g) → N ≈ 0','ไม่มีอากาศ','พวกเขาใส่ชุดพิเศษ'],'B',H_LIFT),
    F('C72','คน 40 kg ในลิฟต์เร่งขึ้น 3 m/s² · g=10 · แรงปกติ (N) = ?',[520],H_LIFT),
    F('C73','คน 50 kg ในลิฟต์เร่งลง 1 m/s² · g=10 · แรงปกติ (N) = ?',[450],H_LIFT),

    // ════════ C7 — ระนาบเอียง resolve (C74-C88) ════════
    M('C74','กล่อง 4 kg วางบนพื้นเอียงมุม 37° (cos37=0.8) · g=10 · แรงปกติจากพื้น = ?',
      ['16 N','24 N','32 N (N = mg cosθ = 4×10×0.8)','40 N'],'C',H_INCLINE,SVG_INC_W_RESOLVE),
    M('C75','กล่อง 2 kg บนพื้นเอียง 53° (sin53=0.8) · g=10 · component ของน้ำหนัก "ตามแนวพื้นเอียง" (ดึงให้ไถล) = ?',
      ['8 N','12 N','16 N (mg sinθ = 2×10×0.8)','20 N'],'C',H_INCLINE,SVG_INC_W_RESOLVE),
    M('C76','กล่อง 5 kg บนพื้นเอียง 53° (cos53=0.6) · g=10 · แรงปกติ = ?',
      ['20 N','30 N (N = 5×10×0.6)','40 N','50 N'],'B',H_INCLINE),
    M('C77','กล่อง 3 kg บนพื้นเอียง 37° (sin37=0.6 cos37=0.8) · g=10 · component "ตั้งฉากพื้น" (mg cosθ) = ?',
      ['18 N','20 N','24 N (3×10×0.8)','30 N'],'C',H_INCLINE,SVG_INC_W_RESOLVE),
    M('C78','พื้นเอียงเรียบ ค่อยๆ เพิ่มมุม θ จาก 0° → 90° · component mg cosθ จะ',
      ['คงเดิม','เพิ่มขึ้น','ลดลง (cosθ → 0 ที่ θ=90°)','เพิ่มแบบ exponential'],'C',H_INCLINE),
    M('C79','ที่มุมเริ่มไถล (วัตถุเริ่มเคลื่อน) บนพื้นเอียงที่มี μ_s · ความสัมพันธ์ระหว่าง θ กับ μ_s คือ',
      ['sinθ = μ_s','cosθ = μ_s','tanθ = μ_s (เพราะ mg sinθ = μ_s · mg cosθ)','θ = μ_s'],'C',H_INCLINE),
    M('C80','พื้นเอียง · μ_s = 0.75 · มุมที่กล่องเริ่มไถล (tan37° = 0.75)',
      ['30°','37° (tanθ = 0.75 = μ_s)','45°','53°'],'B',H_INCLINE),
    M('C81','กล่อง 2 kg นิ่งบนพื้นเอียง 30° (sin30=0.5) ที่มี μ_s = 0.6 · g=10 · ตรวจ tan30°≈0.58 < 0.6 → นิ่งได้ · แรงเสียดทานสถิตที่กระทำ = ?',
      ['5 N','10 N (fs = mg sinθ เพื่อสมดุล = 2×10×0.5)','12 N','20 N'],'B',H_INCLINE),
    M('C82','ดึงกล่อง 3 kg ขึ้นพื้นเอียง 37° (sin37=0.6) เรียบ ด้วยความเร็วคงที่ · g=10 · แรงตึง T = ?',
      ['12 N','15 N','18 N (T = mg sinθ = 3×10×0.6)','30 N'],'C',H_INCLINE,SVG_INC_ROPE),
    M('C83','ดึงกล่อง 2 kg ขึ้นพื้นเอียง 30° เรียบ ด้วย a = 2 m/s² · g=10 · แรงตึง T = ?',
      ['10 N','12 N','14 N (T = mg sinθ + ma = 10 + 4)','20 N'],'C',H_INCLINE,SVG_INC_ROPE),
    M('C84','ดึงกล่อง 2 kg ขึ้นพื้นเอียง 37° ด้วยความเร็วคงที่ · μ_k = 0.25 · g=10 (sin37=0.6 cos37=0.8) · T = ?',
      ['12 N','14 N','16 N (T = mg sinθ + μ_k mg cosθ = 12 + 4)','20 N'],'C',H_INCLINE,SVG_INC_ROPE),
    M('C85','กล่อง 4 kg วางนิ่งบนพื้นเอียง 30° (tan30°≈0.58) · ค่า μ_s ขั้นต่ำที่ทำให้กล่องไม่ไถลคือ',
      ['0.3','0.4','0.6 (μ_s ≥ tan θ → 0.6 > 0.58)','ใช้ค่าใดก็ได้'],'C',H_INCLINE),
    M('C86','บนพื้นเอียง · component mg sinθ คือ',
      ['ตั้งฉากกับพื้น','ดิ่งลง','ขนานกับพื้นเอียง (ดึงให้ไถลลง)','แนวระดับ'],'C',H_INCLINE,SVG_INC_W_RESOLVE),
    F('C87','กล่อง 5 kg บนพื้นเอียง 53° (cos53=0.6) · g=10 · แรงปกติ N (N) = ?',[30],H_INCLINE),
    F('C88','ดึงกล่อง 4 kg ขึ้นพื้นเอียง 37° เรียบ ด้วยความเร็วคงที่ (sin37=0.6) · g=10 · แรงตึง T (N) = ?',[24],H_INCLINE,SVG_INC_ROPE),

    // ════════ C8 — Atwood / 2 มวลผูกเชือก (C89-C101) ════════
    M('C89','Atwood: m₁ = 2 kg, m₂ = 3 kg ห้อยจากรอกลื่นมวล · g=10 · ความเร่งของระบบ',
      ['1 m/s²','2 m/s² (a = (m₂−m₁)g/(m₁+m₂) = 10/5)','3 m/s²','5 m/s²'],'B',H_ATWOOD,SVG_ATWOOD),
    M('C90','Atwood: m₁ = 4, m₂ = 6, g=10 · ความเร่ง = ?',
      ['1 m/s²','2 m/s² (= 2×10/10)','4 m/s²','5 m/s²'],'B',H_ATWOOD,SVG_ATWOOD),
    M('C91','Atwood: m₁ = 2, m₂ = 3, g=10 · แรงตึงเชือก T = ?',
      ['12 N','20 N','24 N (T = 2m₁m₂g/(m₁+m₂) = 120/5)','30 N'],'C',H_ATWOOD,SVG_ATWOOD),
    M('C92','Atwood ที่ m₁ = m₂ = 5 kg · g=10 · ระบบ',
      ['เร่งขึ้น','เร่งลง','สมดุล (a=0) · T = mg = 50 N','ตกอิสระ'],'C',H_ATWOOD),
    M('C93','Atwood: m₁ = 1, m₂ = 4, g=10 · ความเร่ง = ?',
      ['3 m/s²','4 m/s²','6 m/s² (= 3×10/5)','8 m/s²'],'C',H_ATWOOD,SVG_ATWOOD),
    M('C94','บล็อก A 3 kg วางบนโต๊ะเรียบ · บล็อก B 2 kg ห้อยข้างโต๊ะผ่านรอกลื่น · g=10 · ความเร่งของระบบ = ?',
      ['2 m/s²','3 m/s²','4 m/s² (a = m_B·g/(m_A+m_B) = 20/5)','6 m/s²'],'C',H_ATWOOD,SVG_PULLEY_TABLE),
    M('C95','A 4 kg บนโต๊ะเรียบ · B 1 kg ห้อย · g=10 · ความเร่ง = ?',
      ['1 m/s²','2 m/s² (= 10/5)','3 m/s²','5 m/s²'],'B',H_ATWOOD,SVG_PULLEY_TABLE),
    M('C96','A 2 kg บนโต๊ะเรียบ · B 3 kg ห้อย · g=10 · แรงตึงเชือก T = ?',
      ['6 N','10 N','12 N (a = 30/5 = 6 · T = m_A · a = 2×6)','15 N'],'C',H_ATWOOD,SVG_PULLEY_TABLE),
    M('C97','A 2 kg บนโต๊ะ μ_k = 0.5 · B 3 kg ห้อย · g=10 · ความเร่ง = ?',
      ['2 m/s²','3 m/s²','4 m/s² (ΣF = m_B g − μ_k m_A g = 30 − 10 = 20 · a = 20/5)','6 m/s²'],'C',H_ATWOOD,SVG_PULLEY_TABLE),
    M('C98','F = 10 N ดึงระบบ A (2 kg) + B (3 kg) ที่ผูกเชือกกันบนพื้นเรียบ · ความเร่งของระบบ = ?',
      ['1 m/s²','2 m/s² (a = F/(m_A+m_B) = 10/5)','5 m/s²','10 m/s²'],'B',H_FMA,SVG_2BLOCK_TABLE),
    M('C99','F = 10 N ดึง B (3 kg) ที่ลาก A (2 kg) ตามหลังด้วยเชือก · พื้นเรียบ · แรงตึงเชือก T (ดึง A) = ?',
      ['2 N','4 N (a = 10/5 = 2 · T = m_A · a = 2×2)','6 N','10 N'],'B',H_FMA,SVG_2BLOCK_TABLE),
    M('C100','F = 24 N ดึง B (4 kg) ลาก A (2 kg) ตามหลัง · พื้นเรียบ · ความเร่งและ T = ?',
      ['a=2, T=8','a=4, T=8 (a = 24/6 = 4 · T = 2×4)','a=4, T=16','a=6, T=12'],'B',H_FMA,SVG_2BLOCK_TABLE),
    F('C101','Atwood: m₁ = 3, m₂ = 5, g=10 · ความเร่ง (m/s²) = ?',[2.5],H_ATWOOD,SVG_ATWOOD),

    // ════════ C9 — Terminal velocity (C102-C109) ════════
    M('C102','"ความเร็วปลายสุด" (terminal velocity, v_t) ของวัตถุที่ตกในอากาศคือ',
      ['ความเร็วเริ่มต้น','ความเร็วสูงสุดที่เป็นไปได้ในจักรวาล','ความเร็วที่ ΣF = 0 → a = 0 → v ไม่เพิ่มอีก','ความเร็วที่ R = 0'],'C',H_TERM,SVG_FALL_FLUID),
    M('C103','ขณะวัตถุตกถึงความเร็วปลายสุด v_t · ความสัมพันธ์ระหว่าง R (แรงต้านอากาศ) กับ mg คือ',
      ['R = 0','R < mg','R = mg (ΣF = 0)','R > mg'],'C',H_TERM,SVG_FALL_FLUID),
    M('C104','ขณะปล่อยวัตถุครั้งแรก (v = 0) · ค่า R เริ่มต้น = ?',
      ['R = mg','R = 0 (เพราะ R ขึ้นกับ v · เริ่มต้น v=0)','R = mg/2','R = ∞'],'B',H_TERM),
    M('C105','ขณะปล่อยวัตถุ (v = 0) · ความเร่งเริ่มต้น a = ?',
      ['a = 0','a = g/2','a = g (เพราะ R=0 · ΣF = mg)','a = 2g'],'C',H_TERM),
    M('C106','ขณะวัตถุตกลง v เพิ่มขึ้น · R จะ ___ และ a จะ ___',
      ['R ลด · a เพิ่ม','R เพิ่ม · a ลด (จนถึง a=0 ที่ v_t)','R คงที่ · a คงที่','R เพิ่ม · a เพิ่ม'],'B',H_TERM),
    M('C107','ลูกบอล 0.5 kg ตกในอากาศ ถึงความเร็วปลายสุด · g=10 · R = ?',
      ['2.5 N','5 N (R = mg = 0.5×10)','10 N','25 N'],'B',H_TERM),
    M('C108','รูปร่างกราฟ v-t ของวัตถุที่ตกในของไหล (มีแรงต้าน) คือ',
      ['เส้นตรงเอียงตลอด','ชันมากตอนต้น → ชันลดลง → ค่อยๆ ราบเข้าใกล้ v_t','คงที่ตลอด','ชันเพิ่มขึ้นเรื่อยๆ'],'B',H_TERM,SVG_VT_TERMINAL),
    F('C109','นกขนนุ่ม 0.2 kg ตกในอากาศจน v_t · g=10 · R (N) = ?',[2],H_TERM),

    // ════════ C10 — ปัญหา 2-step ผสม (C110-C117) ════════
    M('C110','กล่อง 2 kg ไถลลงพื้นเอียง 37° ที่มี μ_k = 0.5 (sin37=0.6 cos37=0.8) · g=10 · ความเร่ง = ?',
      ['1 m/s²','2 m/s² (a = g(sinθ − μcosθ) = 10(0.6 − 0.4))','3 m/s²','4 m/s²'],'B',H_INCLINE,SVG_INC_FRIC),
    M('C111','ดึงกล่อง 2 kg ขึ้นพื้นเอียง 30° เรียบ ด้วย a = 4 m/s² · g=10 · แรงตึง T = ?',
      ['10 N','14 N','18 N (T = mg sinθ + ma = 10 + 8)','22 N'],'C',H_INCLINE,SVG_INC_ROPE),
    M('C112','ดึงกล่อง 4 kg เฉียง 53° เหนือระดับ ลากบนพื้น μ_k = 0.5 ด้วยความเร็วคงที่ · g=10 · F = ?',
      ['10 N','15 N','20 N (Fcos53 = μ(mg − Fsin53) → 0.6F = 0.5(40−0.8F) → F=20)','30 N'],'C',H_FRIC,SVG_PULL_DIAG),
    M('C113','บล็อก A 4 kg บนโต๊ะ μ_k = 0.2 · บล็อก B 2 kg ห้อยข้างโต๊ะผ่านรอกลื่น · g=10 · ความเร่งของระบบ = ?',
      ['1 m/s²','2 m/s² (ΣF = 20 − 0.2×40 = 12 · a = 12/6)','3 m/s²','4 m/s²'],'B',H_FRIC,SVG_PULLEY_TABLE),
    M('C114','ดึงกล่อง 2 kg เฉียง 37° เหนือแนวระดับ บนพื้นเรียบ ทำให้กล่องเร่ง a = 2 m/s² · g=10 (cos37=0.8) · F = ?',
      ['4 N','5 N (Fcos37 = ma → 0.8F = 4)','8 N','10 N'],'B',H_FMA,SVG_PULL_DIAG),
    M('C115','ลิฟต์เร่งขึ้น 3 m/s² · ภายในมีกล่อง 2 kg แขวนกับเพดานลิฟต์ด้วยเชือก · g=10 · แรงตึง T = ?',
      ['20 N','23 N','26 N (T = m(g+a) = 2×13)','30 N'],'C',H_LIFT),
    M('C116','F = 30 N ดึง A (4 kg) ผูกเชือกพ่วง B (6 kg) ตามหลัง · พื้นเรียบ · g=10 · แรงตึงเชือก T (ที่ดึง B) = ?',
      ['10 N','15 N','18 N (a = 30/10 = 3 · T = m_B·a = 6×3)','24 N'],'C',H_FMA,SVG_2BLOCK_TABLE),
    F('C117','กล่องไถลลงพื้นเอียง 30° เรียบ จากนิ่ง · ระยะ 2.5 m · g=10 · ความเร็วปลาย v (m/s) = ?',[5],H_INCLINE,SVG_INC_SMOOTH)
  ];

  window.QUESTIONS_R12_C = Q;
  if(window.console && console.log) console.log('[Region 1.2 Stage C] loaded', Q.length, 'questions (calculation)');
})();
