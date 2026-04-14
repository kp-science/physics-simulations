# 📋 Session Log — Physics Simulations

> บันทึกงานแต่ละครั้งที่ทำ เพื่อให้ทำงานต่อเนื่องได้ระหว่าง Mac ที่บ้าน ↔ Mac ที่ทำงาน
>
> **กติกา:** เขียน entry ใหม่ต่อท้ายด้านล่าง อย่าลบของเก่า อ่านจากล่างขึ้นบนเพื่อดูสถานะล่าสุด

---

## [2026-04-08] — เครื่องที่ทำงาน (session ที่ทำงานครั้งแรก)

### ทำอะไรไปบ้าง (สะสมจากทั้งวัน)

**1. ปรับหน้าแรก `index.html` เป็น Demo Preview Page**
- แทน emoji icons ในการ์ด Featured Demos ด้วย canvas animation สด (8 ตัว)
- เพิ่ม section "Virtual Physics Lab 01" แบบ featured (6 การ์ดตัวอย่าง ใช้ canvas animation)
- เปลี่ยน topbar จาก `Demo | Collections | Simulations` → `Demo | Collections | Library`
- เปลี่ยน Collections เป็นรูปแบบ **accordion** 2 หมวดใหญ่:
  - **Simulation** (กลศาสตร์, คลื่น, ไฟฟ้า, แสง, ความร้อน, สมัยใหม่ — รวม 6 รายการ)
  - **Virtual Lab** (Virtual Physics Lab 01)
- ลบ section "Simulations/Full Library" เก่าออก (-274 บรรทัด)
- เพิ่มฟังก์ชัน `toggleAcc()` สำหรับ accordion

**2. สร้างหน้าใหม่ `virtual-physics-lab-01.html`**
- แสดง 22 simulations ของ VPL พร้อม filter chips 6 หมวด (การวัด, เวกเตอร์, การเคลื่อนที่, กฎนิวตัน, พลังงาน, วงกลม)
- **ล่าสุด:** เปลี่ยน emoji icon ทั้ง 22 การ์ด → canvas animation สด (มี renderer 22 ตัวแยกตามการทดลอง)
- ใช้ DPR scaling + debounced resize (กัน iOS Safari drift)

**3. สร้างหน้าใหม่ `library.html`**
- Full catalog 38 ไฟล์ จัดหมวดตาม folder
- มี search box กรองด้วย JS
- ใช้ dot markers (ไม่มี emoji/canvas)

**4. แก้ `mechanics.html`**
- ปลดล็อก password overlay → free preview
- auto-unlock ทุก topic เมื่อ DOMContentLoaded
- badge เปลี่ยนเป็น "🎁 Free Preview"

**5. ใส่ frame-busting + back button ใน 22 ไฟล์ VPL**
- `Virtual Physics Lab 01/Mechacnics/*.html` ทั้ง 22 ไฟล์
- CSP meta `frame-ancestors 'self'` + X-Frame-Options SAMEORIGIN
- JS `window.self !== window.top` check
- ปุ่มลอย `.kp-back-btn` ด้านซ้ายบน → `../../index.html`

**6. Fix iOS canvas drift bug** ใน `Virtual Physics Lab 01/Mechacnics/2. vector_forces_sim.html`
- ปัญหา: URL bar ของ Safari บน iPad/iPhone ทำให้ canvas.height เปลี่ยน → เวกเตอร์ไหลลงเรื่อยๆ
- แก้: debounce resize 150ms + threshold 8px + force flag สำหรับ orientationchange

**7. สร้างระบบ sync ข้อมูลระหว่างเครื่อง (งานตอนท้าย session นี้)**
- สร้าง `CLAUDE.md` — คำสั่งประจำโปรเจกต์ (Claude อ่านอัตโนมัติทุกครั้งเปิด session)
- สร้าง `SESSION_LOG.md` (ไฟล์นี้) — บันทึกสถานะงานระหว่างเครื่อง

### ไฟล์ที่แก้/สร้าง

- ✏️ `index.html` — canvas animations, VPL section, accordion Collections, ลบ Full Library เก่า
- 🆕 `virtual-physics-lab-01.html` — หน้ารวม VPL 22 รายการ + canvas animations
- 🆕 `library.html` — full catalog + search
- ✏️ `mechanics.html` — ปลดล็อก password
- ✏️ `Virtual Physics Lab 01/Mechacnics/*.html` (22 ไฟล์) — frame-busting + back button
- ✏️ `Virtual Physics Lab 01/Mechacnics/2. vector_forces_sim.html` — fix iOS drift
- 🆕 `CLAUDE.md` — project instructions
- 🆕 `SESSION_LOG.md` — session tracking (ไฟล์นี้)

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่มีงานค้างที่ต้องทำต่อ (งานที่ขอทั้งหมดในวันนี้เสร็จแล้ว)
- ไอเดียในอนาคต (ถ้าเจ้าของสนใจ):
  - สร้าง Virtual Physics Lab 02, 03 (สำหรับหมวดอื่น เช่น คลื่น ไฟฟ้า)
  - เพิ่ม dark/light mode toggle
  - เพิ่ม analytics tracking
  - ทำ responsive mobile menu สำหรับ topbar

### หมายเหตุ

- **โฟลเดอร์นี้ sync ผ่าน cloud** (ไม่ใช่ git pull/push ตรงๆ) — เครื่องบ้านกับที่ทำงานเห็นไฟล์เดียวกันอัตโนมัติ
- แต่ถ้าแก้ไฟล์เดียวกันพร้อมกัน อาจเกิด conflict ของ cloud — แนะนำทำงานทีละเครื่อง
- `CLAUDE.md` จะถูก Claude อ่านอัตโนมัติทุกครั้งที่เปิด session ในโฟลเดอร์นี้ ไม่ต้องสั่งเอง
- iOS drift fix ใช้เฉพาะใน `vector_forces_sim.html` — ถ้าไฟล์อื่นใน VPL มีปัญหาคล้ายกัน ให้ใช้ pattern เดียวกัน (debounce + threshold)

---

## [2026-04-12 —:—] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**1. สร้าง Simulation ใหม่: การหักเหของคลื่นน้ำในถาดคลื่น (Experiment 33: Refraction)**
- สร้างจากเอกสาร Lab Experiment 33 — ครอบคลุมทั้ง Part A: normal incidence + angled boundary (30°)
- มี 3 tab: 🎬 Simulation, 📋 วิธีการทดลอง, 📐 ทฤษฎี
- 2 โหมดบันทึก: วัดค่าเอง (Manual — คลิกวัดระยะบน canvas) และ อัตโนมัติ (Auto — คำนวณ + บันทึกอัตโนมัติ)
- Sliders: ความถี่ (4-20 Hz), มุมขอบ (0-45°), อัตราส่วนความเร็ว (1.05-2.0), ความเร็ว animation
- Readout แสดง: λ_D, λ_S, v_D, v_S, อัตราส่วน, มุมหักเห (จาก Snell's Law)
- ตารางบันทึกข้อมูล + ส่งออก CSV
- Tab ทฤษฎี: 3 canvas diagrams (normal incidence, Snell's Law, wavefront bending mechanism)
- ค่า physics ตรงกับข้อมูลทดลอง: f=8Hz → λ_D=3.10cm, λ_S=2.58cm, อัตราส่วน≈1.20

**2. รัน protect_new_file.py**
- เพิ่ม Google Analytics (G-2YTJBNHP6D), KP Topbar, mobile layout fix ให้ไฟล์ใหม่
- แก้ CSS selector `nav` → `#simNav` เพื่อไม่ให้ conflict กับ KP topbar nav

**3. แก้ไข Simulation v2 — Physics engine rewrite**
- **แก้บัก:** คลื่นน้ำลึกเอียงตามมุมขอบเขต → แก้ให้วิ่งแนวนอนเสมอ (phase = kD·x − ωt)
- **เพิ่ม depth sliders:** ปรับระดับน้ำลึก (5-15mm) และน้ำตื้น (1-8mm) ได้
- **Dispersion relation จริง:** ω² = (gk + σk³/ρ)·tanh(kd) รวม surface tension ของน้ำ
  - Newton-Raphson solver คำนวณ λ, v จาก depth + frequency
  - ค่าที่ได้: f=8Hz, d=10mm → λ=3.09cm, v=24.7cm/s (ตรงกับข้อมูลทดลอง)
- **Snell's Law ถูกต้อง:** ใช้ vector decomposition ของ k ที่ boundary
  - Tangential k component อนุรักษ์: k_t = k_D·sinα
  - Refracted direction คำนวณจาก k_r = k_t·t̂ + k_n·n̂
  - Phase ต่อเนื่องที่ boundary อัตโนมัติ (ไม่ต้อง offset)
- **Boundary orientation ตาม Figure 2:** ขอบเขตวิ่งจากล่างซ้ายไปบนขวา
  - Normal ชี้ไปทาง shallow (cosα, sinα)
  - แสดง angle arc θi, θr, เส้น normal เมื่อ angle > 0

### ไฟล์ที่แก้/สร้าง
- 🆕 `Virtual Physics Lab 02/33. wave-refraction-ripple-tank.html` — simulation การหักเหคลื่นน้ำ
- ✏️ แก้ไข physics engine + depth sliders (v2)

**4. Rewrite v3 — 4 การทดลอง + Stroboscope + Protractor**
- ปรับ simulation จาก Manual/Auto ธรรมดา → 4 การทดลองแยกกัน:
  - **I. วัด λ** — วัดความยาวคลื่นเอง, เทียบ λ_S/λ_D กับค่า auto, คำนวณ %error
  - **II. Strobe** — Stroboscope 2 ตัว (น้ำลึก/น้ำตื้น), ปรับจนคลื่นหยุดนิ่ง, วัด f → คำนวณ v, %error
  - **III. วัดมุม** — โปรแทรกเตอร์ 360° ลาก+หมุนได้, วัด θi/θr, เทียบ sinθ_r/sinθ_i กับ λ_S/λ_D, %error
  - **IV. เทียบ** — นำเข้าข้อมูลจาก I & III มาเปรียบเทียบ %error ระหว่างกันและกับค่ามาตรฐาน
- Controls เดิมใช้ได้ทุกการทดลอง (f, θ, D, S, speed)
- Readout boxes แสดงเฉพาะโหมดอัตโนมัติ
- ตารางบันทึกผลเปลี่ยนตามการทดลอง พร้อม %error อัตโนมัติ
- Tab วิธีการทดลอง อัปเดตเป็น 4 ส่วน พร้อม Hint

### ไฟล์ที่แก้/สร้าง
- ✏️ `Virtual Physics Lab 02/33. wave-refraction-ripple-tank.html` — rewrite เป็น 4-experiment simulation (923 lines)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ทดสอบผ่านหมด: Exp 1-4, stroboscope freeze, protractor drag/rotate/snap, auto/manual mode
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ในอนาคตได้

### หมายเหตุ
- Stroboscope ใช้ time-quantization: drawWaves quantize เวลาตาม strobe freq แยก deep/shallow
- Protractor: canvas overlay ลาก/หมุนได้ด้วย mousedown/mousemove
- Dispersion relation: ω²=(gk+σk³/ρ)·tanh(kd), g=981, σ=73, ρ=1 (CGS)

## [2026-04-08 ช่วงท้าย session] — เครื่องที่ทำงาน

### ทำอะไรไปบ้าง

- คุยกับเจ้าของเรื่องวิธี sync งานระหว่าง Mac ที่บ้านกับ Mac ที่ทำงาน
- เจ้าของอธิบายว่าโฟลเดอร์ `GitHub/physics-simulations` sync ผ่าน cloud อยู่แล้ว (ทั้ง 2 เครื่องเห็นไฟล์เดียวกันอัตโนมัติ) และเชื่อมกับ GitHub โดยตรง
- ปัญหาของเจ้าของ: ที่ Mac บ้านมี Scheduled task ที่รู้คำสั่งที่สอนไว้แล้ว แต่พอมาเครื่องที่ทำงานต้องเริ่มใหม่ อยากได้ไฟล์กลางที่อ่านแล้วทำงานต่อเนื่องได้
- **แก้ปัญหา:** สร้างไฟล์ 2 ตัวในโฟลเดอร์โปรเจกต์
  1. `CLAUDE.md` — คำสั่งประจำโปรเจกต์ที่ Claude อ่านอัตโนมัติทุกครั้งเปิด session
  2. `SESSION_LOG.md` — บันทึกงานสะสม (ไฟล์นี้)
- อธิบายกติกาให้เจ้าของ: "อัปเดต SESSION_LOG ก่อนเลิก" → อีกเครื่องจะเห็นทันทีผ่าน cloud sync
- ตอบคำถามว่าไฟล์ทั้ง 2 อัปขึ้น GitHub ได้ (และควรอัป) — ถามเจ้าของว่าใช้วิธีไหน push (GitHub Desktop / Terminal / อื่นๆ) ยังรอคำตอบ

### ไฟล์ที่แก้/สร้าง

- 🆕 `CLAUDE.md` — project instructions (Claude อ่านอัตโนมัติ)
- 🆕 `SESSION_LOG.md` — session tracking
- ✏️ `SESSION_LOG.md` — เพิ่ม entry นี้

### ค้างไว้ที่ไหน / ต้องทำต่อ

- รอเจ้าของตอบว่าใช้วิธีไหน push ขึ้น GitHub (GitHub Desktop / Terminal / อื่นๆ) เพื่อแนะนำขั้นตอนให้ตรง
- ยังไม่ได้ commit/push `CLAUDE.md` และ `SESSION_LOG.md` ขึ้น GitHub (จะทำหลังรู้วิธีที่เจ้าของใช้)

### หมายเหตุ

- เจ้าของบอกว่า "ไม่ค่อยรู้เรื่อง git" — ควรอธิบายแบบง่ายที่สุด เลี่ยงศัพท์เทคนิค
- เจ้าของทำงาน 2 เครื่อง (Mac ที่บ้าน = หลัก, Mac ที่ทำงาน = เพิ่งใช้วันนี้ครั้งแรก)
- Mac ที่บ้านเคยตั้ง Scheduled task ไว้แล้ว (รู้คำสั่งที่สอน) — เครื่องที่ทำงานยังไม่ได้ตั้ง ถ้าอยากได้แบบเดียวกันต้อง setup ทีหลัง

---

## [2026-04-08 ท้าย session — Marketing Makeover] — เครื่องที่ทำงาน

### บริบท

เจ้าของปรึกษาเรื่องแผนการตลาด/ขาย — มีไอเดียว่าจะขาย/จัดจำหน่าย/รับจ้างทำในอนาคต ตอนนี้อยากเปิดฟรีก่อน Claude วิเคราะห์ตลาด + เสนอ timeline 6 เดือน + โมเดลธุรกิจ 4 แบบ (Freemium / B2B License / Custom work / Subscription) แล้วเจ้าของขอให้ดู `index.html` และปรับหน้าเพจให้ตรงกับ positioning ใหม่ (soft-launch, ฟรีก่อน)

### สิ่งที่วิเคราะห์เจอใน index.html เดิม

1. ❌ Topbar มีปุ่ม "สั่งซื้อ →" — ขายเร็วเกินไป ครูยังไม่ทัน trust
2. ❌ Pricing section (149/349/549 บาท) เปิดโป๊งบนหน้าแรก — ราคาถูกเกินไปสำหรับ positioning พรีเมียม และทำลายบรรยากาศ free-trial
3. ❌ Section order ผิดหลักการตลาด (How-to มาก่อน About)
4. ❌ Hero copy เป็น feature-focused ไม่ hit pain point
5. ❌ ไม่มี Social Proof / Why-us section
6. ❌ ไม่มี Lead capture / Email gathering
7. ❌ Stats bar จืด (20+ · 5 · 3 · ม.4-6)

### สิ่งที่ปรับให้

**1. Topbar**
- ตัด `สั่งซื้อ →` → เปลี่ยนเป็น `🎬 ทดลองฟรี` (ลิงก์ไป #demos)
- ตัดลิงก์ `ราคา` ออก
- เพิ่ม `ติดต่อ`

**2. Hero copy (benefit-focused)**
- Headline เดิม: "สื่อฟิสิกส์ · เชิงโต้ตอบ · สำหรับห้องเรียน" → ใหม่: **"สอนฟิสิกส์ · ให้เด็กเข้าใจ · ใน 5 นาที"**
- Description: เน้น benefit ครู + "ไม่ต้องสมัคร · ทดลองฟรีทุกตัว"
- Secondary CTA: "👨‍🏫 ทำโดยครูฟิสิกส์จริง" (ชี้ไป #about)

**3. Stats bar**
- เดิม: 20+ / 5 / 3 / ม.4-6
- ใหม่: **30+ Simulation / 100% ภาษาไทย / 5E POE+Inquiry / ม.4-6**

**4. Pricing section — ซ่อนชั่วคราว (comment out ไว้ใน HTML)**
- ไม่ลบทิ้ง เก็บไว้ใน `<!-- -->` comment เพื่อกู้คืนภายหลัง
- แทนด้วย **Early Access section** ใหม่:
  - การ์ดหลัก: "🎁 สิทธิ์พิเศษผู้ลงทะเบียนก่อน" + benefits 4 ข้อ (ฟรีทุกตัว, แจ้งเตือน, ส่วนลด 50% เมื่อเปิด Premium, รับ PDF+ใบงานเดือนละ 1 ชุด)
  - การ์ดข้าง 3 ใบ: สำหรับครู / สำหรับโรงเรียน / รับทำสื่อ Custom
  - CTA ไปที่ #contact

**5. Why KP Science section ใหม่** (แทรกก่อน Collections)
- 6 cards: 🇹🇭 ภาษาไทยตรงหลักสูตร / 👨‍🏫 ครูฟิสิกส์ตัวจริง / 🎯 แก้ Misconception / 📱 เปิดใช้ทันที / 🎨 ดีไซน์มืออาชีพ / 🔄 อัปเดตต่อเนื่อง

**6. Section order** (ลำดับใหม่)
- เดิม: Hero → Demo → VPL → Collections → How-to → Pricing → About → Contact
- ใหม่: **Hero → Demo → VPL → Why → Collections → About → How-to → Early Access → Contact**
- เหตุผล: Trust (Why + About) มาก่อน CTA (Early Access)

**7. How-to section — rewrite**
- เดิม: "วิธีสั่งซื้อ" (01 แจ้งหมวด → 02 ชำระเงิน → 03 รับรหัส → 04 เปิดใช้)
- ใหม่: **"วิธีใช้งาน"** (01 เลือก Sim → 02 คลิกเปิด → 03 สอนในห้อง → 04 ติชม/ขอหัวข้อใหม่)

**8. Contact section**
- Title: "ติดต่อสั่งซื้อ" → **"ติดต่อ / ขอสื่อเพิ่ม / รับทำ Custom"**
- Subtitle: เพิ่ม "ลงชื่อ Early Access ผ่านช่องทางใดก็ได้"

**9. Footer**
- ปรับ copyright 2025 → 2026
- ลบลิงก์ `#pricing` → เพิ่ม `#why` (ทำไมต้อง KP) + `#about`

### ไฟล์ที่แก้/สร้าง

- ✏️ `index.html` — Marketing makeover ทั้งเพจ (topbar, hero, stats, pricing→early-access, why section ใหม่, section reorder, how-to rewrite, contact, footer) + CSS ใหม่ `.ea-*` และ `.why-*`
- ✏️ `SESSION_LOG.md` — entry นี้

### แผนการตลาด 6 เดือน (ที่เสนอไป)

- **เดือน 1-2:** Build audience — ปล่อยฟรี 100% สร้าง Facebook/TikTok/YouTube โพสต์สื่อสั้น 3-4 ครั้ง/สัปดาห์ เก็บ email list
- **เดือน 3:** Validate — ทำโพสต์สอบถาม + Early Bird deal 299 lifetime เช็ค market fit เริ่มรับ custom
- **เดือน 4:** Launch Premium — แยก free/premium tier เปิดระบบล็อกอิน ช่องทางชำระ PromptPay ราคาเปิดตัวลด 50%
- **เดือน 5:** B2B outreach — cold contact โรงเรียน 20-30 แห่ง เสนอ trial 1 เดือน ปิดดีล 5,000 บาท/ปี/โรง
- **เดือน 6:** Scale — ดูช่องทางไหนเวิร์ก ทุ่มไปทางนั้น เริ่ม Virtual Physics Lab 02

### ค้างไว้ที่ไหน / ต้องทำต่อ (สำหรับ session หน้า)

**Quick wins (ทำได้ทันที):**
- สร้าง Facebook Page "KP Science — สื่อฟิสิกส์ Interactive สำหรับครูไทย"
- อัดคลิป screen record 30 วินาที 1 simulation → โพสต์ครั้งแรก
- เพิ่ม Google Form รับ email ในหน้าแรก (ตอนนี้ยังไม่มี — Early Access CTA ชี้ไป contact อย่างเดียว)

**ที่เจ้าของอาจขอทำต่อ:**
- 📝 เขียน copy Facebook Page (bio + first post)
- 📄 Brochure PDF 1 หน้าสำหรับส่งโรงเรียน
- 📋 Pricing table (สำหรับเปิดใช้ภายหลังเมื่อพร้อม)
- 📊 Content calendar 1 เดือนแรก
- 🔧 ระบบ lead capture form จริง (Google Form embed หรือ Typeform)

### หมายเหตุ

- **Pricing section ไม่ได้ลบ** — เก็บไว้ใน HTML comment `<!-- ... -->` ระหว่างบรรทัด ~865-920 กู้คืนได้ง่ายแค่เอา comment ออก
- **ราคาเดิม 149/349/549** เจ้าของอาจอยากปรับใหม่ภายหลัง — ผมเห็นว่าถูกเกินไป แนะนำ 390-990 สำหรับ B2C, 5,000-15,000 สำหรับ B2B School License
- Early Access CTA ตอนนี้ยังชี้ไปที่ `#contact` — ถ้าต้องการระบบเก็บ email จริงต้อง embed Google Form หรือใช้ Mailchimp/ConvertKit
- เจ้าของยังไม่ได้ตอบเรื่องวิธี push ขึ้น GitHub (ยังค้าง) — แต่เจ้าของเคลียร์ว่าโฟลเดอร์ sync ผ่าน cloud อยู่แล้ว อีกเครื่องเห็นอัตโนมัติ

---

## [2026-04-08 ปิด session — บันทึกจุดสุดท้าย] — เครื่องที่ทำงาน

### สถานะ ณ ตอนที่ปิด session นี้

จบงาน Marketing Makeover ของ `index.html` แล้วเจ้าของสั่ง "อัปเดต SESSION_LOG" อีกครั้ง → เป็นสัญญาณว่ากำลังจะปิด session และอยากให้บันทึกสถานะสุดท้ายไว้ให้เครื่องบ้านมาอ่านต่อ

### สรุปงานทั้งหมดที่ทำใน session นี้ (ตั้งแต่เริ่มวันนี้)

1. ✅ เปลี่ยน emoji cards เป็น canvas animation ใน `virtual-physics-lab-01.html` (22 การ์ด + 22 renderers)
2. ✅ สร้างระบบ sync ระหว่างเครื่อง (`CLAUDE.md` + `SESSION_LOG.md`)
3. ✅ วิเคราะห์ตลาด + เสนอแผนธุรกิจ 6 เดือน (Freemium / B2B License / Custom / Subscription)
4. ✅ Marketing Makeover `index.html`:
   - Topbar: ตัด "สั่งซื้อ" → "🎬 ทดลองฟรี"
   - Hero: headline ใหม่ "สอนฟิสิกส์ · ให้เด็กเข้าใจ · ใน 5 นาที"
   - Stats bar ใหม่ (30+ / 100% ไทย / 5E POE / ม.4-6)
   - ซ่อน Pricing (comment ไว้ใน HTML) → แทนด้วย Early Access section
   - เพิ่ม "Why KP Science" section (6 cards)
   - Reorder: About ขึ้นก่อน How-to
   - Rewrite How-to จาก "วิธีสั่งซื้อ" → "วิธีใช้งาน"
   - ปรับ Contact + Footer

### ไฟล์สถานะล่าสุด (ณ ตอนปิด session)

- `index.html` — ผ่าน Marketing Makeover แล้ว (section order: Hero → Demo → VPL → Why → Collections → About → How → Early Access → Contact)
- `virtual-physics-lab-01.html` — มี 22 canvas renderers ทำงานแล้ว
- `library.html` — ยังคงเป็น full catalog (ไม่ได้แก้ใน session นี้)
- `mechanics.html` — ปลดล็อก password แล้ว
- `CLAUDE.md` — project instructions (Claude อ่านอัตโนมัติ)
- `SESSION_LOG.md` — ไฟล์นี้

### สิ่งที่เจ้าของอาจขอทำต่อใน session หน้า (ที่บ้าน)

**ด่วน/Quick wins:**
1. 📘 สร้าง Facebook Page "KP Science" + เขียน bio + first post (Claude ช่วยเขียน copy ได้)
2. 🎬 อัดคลิป screen record 30 วินาที 1 simulation (เจ้าของต้องทำเอง แต่ Claude แนะนำได้ว่าเลือกตัวไหน มุมไหน)
3. 📧 Embed Google Form ในปุ่ม Early Access เพื่อเก็บ email จริง (ตอนนี้ชี้ไป #contact อย่างเดียว)

**กลางๆ:**
4. 📄 Brochure PDF 1 หน้าสำหรับส่งโรงเรียน (ใช้ docx/pdf skill)
5. 📋 Pricing table แยก (เก็บไว้พร้อมใช้เมื่อเปิด Premium เดือน 4)
6. 📊 Content calendar 1 เดือนแรก (โพสต์อะไร วันไหน)
7. ✍️ Copy สำหรับ Facebook Groups ครูฟิสิกส์/วิทย์ไทย (แจกฟรีแบบเนียนๆ)

**ระยะยาว:**
8. 🔧 ระบบ lead capture จริง (Mailchimp/ConvertKit embed)
9. 🎨 Virtual Physics Lab 02 (คลื่น/ไฟฟ้า/แสง)
10. 🏫 Template email สำหรับ B2B outreach หัวหน้ากลุ่มสาระวิทย์

### คำแนะนำสำหรับ Claude ที่จะทำงานต่อ (เครื่องบ้าน)

- เจ้าของเป็นครูฟิสิกส์ที่โรงเรียนสตรีวิทยา ไม่ถนัดเรื่อง tech/git — **อธิบายแบบง่ายที่สุด เลี่ยงศัพท์เทคนิค**
- เจ้าของชอบให้ **ทำให้เลย** มากกว่าอธิบายยาวๆ (เช่น "ทำให้ด้วย" = ลงมือแก้ไฟล์ ไม่ใช่อธิบายวิธี)
- ถ้าจะเสนออะไรใหม่ ให้เสนอพร้อม "ไอเดียเหตุผล + ผลกระทบ" สั้นๆ ไม่ยาว
- เจ้าของมีวิสัยทัศน์เรื่อง **ขาย/จัดจำหน่าย/รับจ้างทำ** ในอนาคต → งานทุกอย่างควรรองรับเป้าหมายนี้
- **ห้ามเปิด Pricing section กลับ** จนกว่าจะมี testimonial + email list 300+ (ตามแผน ~เดือน 4)
- Early Access CTA ตอนนี้ชี้ไป `#contact` — ถ้าเจ้าของพร้อม ให้เสนอ Google Form embed

### หมายเหตุสำคัญ

- วันนี้เป็น session แรกของเจ้าของที่ใช้เครื่องที่ทำงาน (ปกติทำที่บ้าน)
- โฟลเดอร์ sync ผ่าน cloud — แก้ที่ไหนอีกเครื่องเห็นเลย ไม่ต้อง git pull/push
- ยังไม่ได้ commit/push `CLAUDE.md` + `SESSION_LOG.md` + การแก้ `index.html` + `virtual-physics-lab-01.html` ขึ้น GitHub (เจ้าของไม่ได้ตอบวิธี push — ข้ามไปก่อน cloud sync ใช้ได้อยู่)

---

## [2026-04-09] — เพิ่ม tab "📋 วิธีการทดลอง" ครบทุกไฟล์ VPL01/Mechanics

### งานที่ทำ

**สแกนและจัดกลุ่มไฟล์ VPL01/Mechanics ทั้งหมด 22 ไฟล์**
- ✅ มี procedure อยู่แล้ว 8 ไฟล์: 2, 5, 8, 14, 15, 17, 18, 19
- 🟡 มีแค่ callout 1 ไฟล์: 6.3
- 🔴 ยังไม่มี 13 ไฟล์: 1, 3, 4, 6.1, 6.2, 7, 9, 10, 11, 12, 13, 16, 20

**ตัดสินใจ workflow (เจ้าของเลือก option 3)**
- ทำ template 1 ไฟล์ (เลือก `13. free-fall-experiment.html`) ให้ review ก่อน
- เลือกรูปแบบ **เพิ่ม tab ใหม่** (ไม่ใช่เพิ่ม section ใน sim tab) เพื่อไม่ให้หน้ารก

**Template structure (ใช้กับทุกไฟล์)**
1. CSS ใหม่ก่อน `</style>` — classes: `.procedure-box`, `.proc-goal`, `.proc-list`, `.proc-sub`, `.proc-tip` (dark theme ใช้ `--accent` ฟ้า / `--accent2` ม่วง / `--accent3` เขียว)
2. ปุ่มใน `<nav>` ระหว่าง sim ↔ theory: `<button onclick="showTab('procedure',this)">📋 วิธีการทดลอง</button>`
3. `<div id="tab-procedure" class="tab-section">` ก่อน `<div id="tab-theory">` — มี `max-width:900px` จัดกลาง
4. เนื้อหา: กล่อง 🎯 จุดประสงค์ → `<ol>` 6–8 ขั้น → สรุปผล + 2-3 sub-questions → 💡 ทดลองเพิ่มเติม

**ภาษา Child-centered (บังคับทุกไฟล์)**
- ไม่มี "ครูให้นักเรียน...", "ครูแจก..." ใช้ "นักเรียนกดปุ่ม...", "นักเรียนสังเกต..." แทน
- อ้างอิง UI จริง: ปุ่ม/slider/card ของแต่ละ sim เจาะจง (wrap ใน `<strong>` หรือ `<em>`)
- ใช้ `<span class="mono">` สำหรับสูตร/ตัวแปร

**ไฟล์ที่แก้ในรอบนี้ (13 ไฟล์) — ทุกไฟล์ผ่าน verify**

| # | ไฟล์ | หัวข้อ |
|---|---|---|
| 1 | measuring_precision | การวัดด้วยความละเอียด (sig figs, 4 ไม้บรรทัด) |
| 3 | torques_simulation | สมดุลทอร์ก M₁X₁ = M₂X₂ |
| 4 | force_resolution_sim | แตกแรง Fx = F cosθ, Fy = F sinθ |
| 6.1 | pendulum_timer | ลูกตุ้ม T = 2π√(L/g) |
| 6.2 | water-clock-simulation | นาฬิกาน้ำ อัตราไหล |
| 7 | strobe_photography | สโตรบ v = Δx/Δt |
| 9 | galileo-water-clock | Galileo รางเอียง a = g sinθ |
| 10 | spinning_disc_sim | จานหมุนบนรางเอียง |
| 11 | air_track_simulation | รางลมแนวระดับ 1.5m |
| 12 | turntable_gravity | หา g ด้วยจานหมุน 33⅓ rpm |
| **13** | **free-fall-experiment** | **ตกอิสระ (template ต้นฉบับ)** |
| 16 | trajectories_simulation | วิถีโพรเจกไทล์ |
| 20 | tilted_air_track | พลังงานยางยืด / calibration |

**Verify script**
```bash
# ทุกไฟล์ต้องได้ 1|1|2 (1 ปุ่ม / 1 tab div / 2 ครั้งที่เจอ procedure-box = CSS def + HTML)
for f in *.html; do
  btn=$(grep -c "showTab('procedure'" "$f")
  div=$(grep -c 'id="tab-procedure"' "$f")
  css=$(grep -c "procedure-box" "$f")
  echo "$btn|$div|$css  $f"
done
```
ทุกไฟล์ผ่าน ✅

### สถานะตอนนี้

- ✅ VPL01/Mechanics 13 ไฟล์มี tab procedure แล้ว (รวมไฟล์ที่มีอยู่เดิม 8 ไฟล์ + 1 callout ไฟล์ 6.3 → รวมทั้งโฟลเดอร์ 22/22)
- ✅ Layout ทุกไฟล์: 🎬 ทดลอง → 📋 วิธีการทดลอง → 📐 ทฤษฎีและอธิบาย
- ⚠️ ยังไม่ได้ commit/push ขึ้น GitHub (sync ผ่าน cloud ทำงานปกติ)

### งานที่อาจจะทำต่อ

- อัปเกรดไฟล์ 6.3 จาก callout → tab เต็มรูปแบบ (ให้สม่ำเสมอกับที่เหลือ)
- ตรวจรูปแบบ procedure ของไฟล์ที่มีอยู่เดิม 8 ไฟล์ (2, 5, 8, 14, 15, 17, 18, 19) ว่าใช้ `.instr` class แบบเดิมไหม จะแปลงเป็น tab procedure ให้เหมือนกันไหม
- ขยายไป VPL01 โฟลเดอร์อื่น (Waves, Electricity, Optics ฯลฯ) ถ้ามี
- Commit+push งานวันนี้ขึ้น GitHub เมื่อเจ้าของพร้อม

---

## 📋 COMMAND QUEUE — คำสั่งข้ามเครื่อง

> **วิธีใช้:**
> - เขียนคำสั่งใหม่ด้านล่างในรูปแบบ `[ ] ชื่อคำสั่ง — รายละเอียด`
> - Scheduled task "kp-run-command-queue" บนทุกเครื่องจะอ่าน queue นี้และรันคำสั่งที่ยังไม่ได้ทำ (`[ ]`)
> - หลังรันเสร็จจะเปลี่ยนเป็น `[x]` พร้อม timestamp อัตโนมัติ
> - ไฟล์นี้ sync ระหว่างบ้าน ↔ ที่ทำงานผ่าน cloud — เขียนจากเครื่องไหนก็ได้

### คำสั่งที่รองรับ:
| คำสั่ง | ทำอะไร |
|--------|--------|
| `protect-new-files` | สแกนและเพิ่ม GA + frame protection + back button ให้ไฟล์ HTML ที่ขาด |
| `update-session-log` | บันทึกสถานะงานล่าสุดลง SESSION_LOG |
| `check-ga` | ตรวจว่าทุกไฟล์มี GA code `G-2YTJBNHP6D` ครบไหม |

### Queue:
<!-- เขียนคำสั่งใหม่ต่อด้านล่างนี้ -->

---

## [2026-04-10] — เครื่องบ้าน (session วันนี้)

### ทำอะไรไปบ้าง

**1. ตั้งค่า Google Analytics (G-2YTJBNHP6D)**
- สร้าง GA4 Property ชื่อ "KP Science Website"
- ใส่ GA tracking code ให้ทุกไฟล์ HTML ในโปรเจกต์ **54 ไฟล์** ด้วย Python script
- Stream URL ควรแก้เป็น `kp-science.github.io/physics-simulations` (ตอนนี้ตั้งไว้แค่ root)
- GA ทำงานได้แล้ว ยืนยันจาก Active users = 1 ใน Realtime dashboard

**2. Early Access Modal (Google Form)**
- เปลี่ยนปุ่ม "ลงชื่อรับสิทธิ์ Early Access" จากลิงก์ `#contact` → เปิด popup modal
- ฝัง Google Form `1FAIpQLSdzrYmTAB0VYnhkPWa3WeR1qubqtomMGTrJMwEO8mqCnov_OA` ใน modal
- กด ✕ หรือคลิกพื้นหลังเพื่อปิด modal ได้

**3. Facebook Page Copy**
- เขียน bio + first post สำหรับ Page "KP Science — สื่อฟิสิกส์ Interactive สำหรับครูไทย"

**4. สร้างไฟล์ Marketing (ใน `_marketing/`)**
- `brochure.html` — โบรชัวร์ A4 สำหรับส่งโรงเรียน (Cmd+P → Save as PDF)
- `pricing.html` — ตาราง Pricing 3 แผน (ฟรี / Premium 390 บาท / School License 5,000 บาท) + Comparison table
- `content-calendar.html` — แผนโพสต์ 4 สัปดาห์ 16 โพสต์

**5. จัดโครงสร้างโฟลเดอร์**
- สร้าง `_admin/` → ย้าย admin_passwords.html, KP_OrderBot.gs, KP_Orders.xlsx, add_protection.py
- สร้าง `_marketing/` → ย้าย brochure.html, content-calendar.html, pricing.html
- ไฟล์หน้าเว็บ (index, library, mechanics ฯลฯ) คงอยู่ที่ root

**6. Scheduled Tasks**
- สร้าง `kp-protect-new-files` — สแกนและเพิ่ม GA + frame protection + back button ให้ไฟล์ใหม่
- สร้าง `kp-run-command-queue` — อ่าน Command Queue จาก SESSION_LOG.md แล้วรันคำสั่งอัตโนมัติ
- สร้างระบบ Command Queue ใน SESSION_LOG.md นี้ เพื่อสื่อสารคำสั่งข้ามเครื่อง

**7. อัปเดต CLAUDE.md**
- เพิ่มส่วน Google Analytics — Measurement ID + กติกาบังคับใส่ GA ทุกไฟล์ใหม่

### ไฟล์ที่แก้/สร้าง

- ✏️ `index.html` — เพิ่ม Early Access modal + GA code
- ✏️ ทุกไฟล์ HTML (54 ไฟล์) — GA code
- 🆕 `_marketing/brochure.html`
- 🆕 `_marketing/pricing.html`
- 🆕 `_marketing/content-calendar.html`
- 🆕 `_admin/` (ย้ายไฟล์เข้า)
- ✏️ `CLAUDE.md` — เพิ่มกติกา GA
- ✏️ `SESSION_LOG.md` — เพิ่ม Command Queue system

### ค้างไว้ที่ไหน / ต้องทำต่อ

- แก้ Stream URL ใน GA dashboard ให้เป็น `kp-science.github.io/physics-simulations`
- สร้าง Facebook Page "KP Science" + โพสต์แรก (copy พร้อมแล้วในการสนทนา)
- ตั้ง `kp-run-command-queue` ที่เครื่องที่ทำงานด้วย (task นี้มีแค่บ้านตอนนี้)
- อัดคลิป screen record 30 วิ simulation ตัวแรก → โพสต์ Facebook

### หมายเหตุ

- Scheduled tasks ไม่ sync ข้ามเครื่อง — ต้องสร้างใหม่ที่เครื่องที่ทำงานด้วย
- Command Queue: เขียน `[ ] protect-new-files` ในส่วน Queue ด้านบน แล้วรัน task `kp-run-command-queue` บนเครื่องไหนก็ได้
- GA Measurement ID: `G-2YTJBNHP6D` — ใส่ไว้ใน CLAUDE.md แล้ว Claude จะรู้อัตโนมัติ

---

## [2026-04-11] — เครื่องบ้าน

### ทำอะไรไปบ้าง

**1. สร้าง Virtual Physics Lab 02 — Experiment 30: Waves on a Coiled Spring**
- สร้าง simulation ครบถ้วนจาก lab manual Experiment 30 (คลื่นบนสปริงขด)
- **Tab 1: Simulation** — 4 โหมดการทดลอง:
  - พัลส์เดี่ยว (Transverse/Longitudinal/Rarefaction + Fixed/Free end)
  - คลื่นนิ่ง (Standing Waves) ปรับ frequency ได้ แสดง nodes/antinodes
  - สปริง 2 อัน (Two Springs) ต่างความหนาแน่น → reflection/transmission
  - ซ้อนทับ (Superposition) ส่ง 2 พัลส์จาก 2 ฝั่ง
- 2 โหมดบันทึก: **วัดค่าเอง** (Manual — มี stopwatch, ตารางกรอก) + **อัตโนมัติ** (Auto — วัดอัตโนมัติ)
- ตาราง Data Chart I (Speed of Pulses) + Data Chart II (Speed of Waves) ตาม lab manual
- Marker เชือกกลางสปริง แสดงทิศอนุภาคสั่น + ไม้บรรทัดซ้อน
- Wave physics engine ใช้ 1D wave equation (200 nodes, Euler integration, CFL stable)
- Canvas rendering สปริงขดแบบ zigzag/coil ที่เปลี่ยนรูปตามคลื่น
- **Tab 2: วิธีการทดลอง** — 12 ขั้นตอนจาก lab manual เป็นภาษาไทย + ผลที่คาดหวัง
- **Tab 3: ทฤษฎี** — อธิบายด้วย visual: mini-canvas animation 7 ตัว (transverse/longitudinal, fixed/free reflection, standing waves, superposition, two springs) + สูตร v = √(T/μ), v = fλ
- ใช้ physics-simulation-builder skill + design tokens ของโปรเจกต์

**2. รัน protect_new_file.py**
- เพิ่ม KP Topbar + mobile order fix ให้ไฟล์ใหม่
- ยืนยัน GA code G-2YTJBNHP6D ครบ

### ไฟล์ที่แก้/สร้าง

- 🆕 `Virtual Physics Lab 02/waves-on-coiled-spring.html` — simulation คลื่นบนสปริงขด (Experiment 30)

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ทดสอบ simulation บน browser จริง ตรวจ edge cases
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ถ้าต้องการ
- สร้าง simulation เพิ่มสำหรับ Virtual Physics Lab 02

### หมายเหตุ

- Wave engine ใช้ 200 nodes + damping 0.15 → พัลส์สะท้อนไปกลับได้ ~10 ครั้งก่อนหมด
- ค่าอ้างอิงจาก lab: transverse v ≈ 0.57-0.59 m/s, longitudinal v ≈ 0.67-0.70 m/s
- ความเร็วคลื่นปรับได้ผ่าน slider ความตึง (T) ตามสูตร v = √(T/μ)

---

## [2026-04-10 ช่วงบ่าย] — เครื่องบ้าน (session ต่อเนื่อง)

### ทำอะไรไปบ้าง

**8. สร้างคู่มือ Lab 22 ไฟล์ (HTML, พิมพ์ได้ A4)**

สร้างไฟล์คู่มือการทดลองแยกสำหรับนักเรียน 22 ไฟล์ บันทึกที่ `Virtual Physics Lab 01/lab-manuals/`

โครงสร้างทุกไฟล์:
- ปกการทดลอง (หัวข้อ, เลขที่, ลิงก์ไป simulation, badge ชั้น/เวลา/ครู)
- วัตถุประสงค์ (3 ข้อ)
- ทฤษฎีพื้นฐาน (กล่อง theory border ฟ้า)
- การใช้โปรแกรม (ตารางอธิบาย controls/sliders)
- คำถาม Predict ก่อนทดลอง (POE รูปแบบม่วง 2 ข้อ)
- วิธีการทดลอง (ขั้นตอนมีหมายเลข gradient)
- ตารางบันทึกผล
- สรุปผลการทดลอง (กล่องเส้นสำหรับเขียน)
- แบบฝึกหัด (3 ข้อ)
- หมายเหตุสำหรับครู (yellow background)

ทุกไฟล์มี: GA code (G-2YTJBNHP6D), frame-protection meta, Google Fonts Sarabun, @media print A4

### รายชื่อ 22 ไฟล์ที่สร้าง

| ไฟล์ | หัวข้อ |
|------|--------|
| lab-01-measuring.html | การวัดและความละเอียดของการวัด |
| lab-02-vectors.html | การบวกเวกเตอร์แรงและการสลายแรง |
| lab-03-torques.html | สมดุลทอร์กบนคานดีดดุ้น |
| lab-04-force-resolution.html | การสลายแรงและองค์ประกอบของแรง |
| lab-05-incline.html | แรงบนพื้นเอียงและสมดุลสถิต |
| lab-06-1-pendulum-timer.html | การวัดเวลาด้วยลูกตุ้มนาฬิกา |
| lab-06-2-water-clock.html | การวัดเวลาด้วยนาฬิกาน้ำ |
| lab-06-3-tape-timer.html | การวัดเวลาด้วยเครื่องเคาะสัญญาณเวลา |
| lab-07-strobe.html | การถ่ายภาพแบบสโตรบและการวัดความเร็ว |
| lab-08-straight-motion.html | การเคลื่อนที่แนวตรงและกราฟการเคลื่อนที่ |
| lab-09-galileo.html | การทดลองของ Galileo บนรางเอียง |
| lab-10-spinning-disc.html | จานหมุนบนรางเอียงและการหาค่า g |
| lab-11-air-track.html | รางลมและกฎการอนุรักษ์โมเมนตัม |
| lab-12-turntable-gravity.html | การหาค่า g ด้วยจานหมุน |
| lab-13-free-fall.html | การตกอิสระและการหาค่า g |
| lab-14-mass-weight.html | มวล น้ำหนัก และค่า g บนดาวต่างๆ |
| lab-15-newton2.html | กฎข้อที่ 2 ของนิวตัน: F = ma |
| lab-16-projectile.html | การเคลื่อนที่แบบโพรเจกไทล์ |
| lab-17-centripetal.html | แรงสู่ศูนย์กลางและการเคลื่อนที่เป็นวงกลม |
| lab-18-newton3.html | กฎข้อที่ 3 ของนิวตัน |
| lab-19-pendulum-energy.html | พลังงานของลูกตุ้มนาฬิกา |
| lab-20-tilted-track.html | รางลมเอียงและการอนุรักษ์พลังงาน |

### ไฟล์ที่สร้าง

- 🆕 `Virtual Physics Lab 01/lab-manuals/lab-01-measuring.html` ถึง `lab-20-tilted-track.html` (22 ไฟล์)

### ค้างไว้ที่ไหน / ต้องทำต่อ

- Push ไฟล์ lab-manuals ทั้ง 22 ไฟล์ขึ้น GitHub (ยังไม่ได้ commit)
- อาจเพิ่มลิงก์จาก `virtual-physics-lab-01.html` หรือ `index.html` ไปยังหน้า lab manuals
- อาจสร้าง index หน้า `lab-manuals/index.html` รวมลิงก์ทั้ง 22 ไฟล์

### หมายเหตุ

- ไฟล์ทำงานด้วย Python generator script — content ของแต่ละ lab เขียนในรูปแบบ dict
- พิมพ์ได้ผ่าน Cmd+P → A4, Print Background Graphics, No Margins (หรือ Smallest)
- ลิงก์ใน cover page ชี้ไป simulation ใน `../Mechacnics/` (สะกดตรงตามโฟลเดอร์จริง)


---

## [2026-04-11] — Session ต่อเนื่อง (auth-aware downloads + UI updates)

### ทำอะไรไปบ้าง

**1. แปลง DOCX → PDF (17 เล่ม)**
- สร้าง `convert_to_pdf.py` รันบน Mac ด้วย `docx2pdf` + Microsoft Word (รองรับฟอนต์ภาษาไทย TH Sarabun New)
- PDF ทั้ง 17 ไฟล์บันทึกไว้ที่ `Virtual Physics Lab 01/lab-manuals-pdf/`
- รายการ: Lab 1–5, 6.1, 6.2, 6.3, 7–15

**2. เพิ่มปุ่มดาวน์โหลดคู่มือ Lab ใน simulation nav bar (17 ไฟล์)**
- ทุก simulation มีปุ่ม `⬇ ดาวน์โหลดคู่มือ Lab` ใน `<nav>` ถัดจากปุ่มทฤษฎี
- Style: pill shape, border-radius:20px, border:2px solid rgba(52,211,153,0.75), สีเขียว

**3. เพิ่มปุ่มดาวน์โหลดใน `virtual-physics-lab-01.html` (การ์ดทุกใบ)**
- ทุก Lab card มีปุ่ม `⬇ คู่มือ Lab` ที่ footer ของการ์ด

**4. เพิ่มปุ่มดาวน์โหลดใน `library.html` (17 รายการ)**
- ปุ่ม pill style ข้อความ "⬇ คู่มือ Lab" วางใน list view และ card grid

**5. ระบบ Auth-aware Download**
- `dlPdf(path, labNum)` ตรวจสอบ `currentUser` จาก Firebase ก่อนอนุญาตดาวน์โหลด
- Lab 1–5: โหลดได้ฟรีทุกคน
- Lab 6.1–15: ต้องล็อกอิน/สมัครสมาชิกก่อน → ถ้าไม่ได้ล็อกอินจะขึ้น popup
- ใช้งานใน: `virtual-physics-lab-01.html`, `library.html`, และ simulation ทุก 12 ไฟล์ (Lab 6.1–15)
- Firebase CDN + `kp-auth.js` + modal HTML/CSS ถูก inject ในทุกไฟล์ที่ต้องการ

**6. ปรับ Early Access → สมาชิก KP Science (`index.html`)**
- badge: 🔑 สิทธิ์สมาชิก KP Science (ฟรี)
- รายการสิทธิ์ใหม่: เข้าถึงคู่มือ Lab ทุกเล่ม / แจ้งเตือน Lab ใหม่ / ใช้งานออฟไลน์ / เนื้อหาอนาคต
- ปุ่ม CTA: `🔑 สมัครสมาชิกฟรีด้วย Google` → เรียก `showModal('login')` จาก Firebase auth

### ไฟล์ที่เปลี่ยนแปลง

| ไฟล์ | การเปลี่ยนแปลง |
|------|----------------|
| `index.html` | ปรับ Early Access section → Member signup |
| `virtual-physics-lab-01.html` | เพิ่มปุ่มดาวน์โหลดทุก Lab card + auth-aware dlPdf |
| `library.html` | เพิ่มปุ่ม pill style + auth-aware dlPdf ทุก 17 รายการ |
| `Virtual Physics Lab 01/Mechacnics/*.html` (17 ไฟล์) | ปุ่ม pill style ใน nav |
| `Virtual Physics Lab 01/Mechacnics/6.1–15 *.html` (12 ไฟล์) | lock download + Firebase modal |
| `Virtual Physics Lab 01/lab-manuals-pdf/` | PDF คู่มือ Lab 17 เล่ม |

### สถานะ Auth Download

```
Lab 1–5   → ดาวน์โหลดได้ฟรี (ไม่ต้อง login)
Lab 6.1+  → ต้องเป็นสมาชิก (login ด้วย Google หรืออีเมล)
blocked   → admin ปิดได้จาก dashboard
```

### ค้างไว้ / ต้องทำต่อ

- ยังไม่ได้เพิ่มปุ่มดาวน์โหลดใน Lab 16–20 (ยังไม่มีไฟล์คู่มือ)
- HEAD.lock เกิดบ่อยเมื่อ sandbox run git — แก้ด้วย `rm .git/HEAD.lock` ใน Terminal

### หมายเหตุ

- `currentUser` มาจาก `kp-auth.js` — ทุก role (member/premium/admin) โหลดได้, เฉพาะ blocked เท่านั้นที่ถูกบล็อก
- `kp-auth.js` ต้อง path `../../kp-auth.js` จากใน `Mechacnics/` folder
- HEAD.lock: sandbox ลบไม่ได้ เพราะ permission — ต้องลบผ่าน macOS Terminal เสมอ

---

## [2026-04-11 session ยาว] — เครื่องที่ทำงาน

### ทำอะไรไปบ้าง

**1. แก้ Auth Modal + Download Button (Lab 6.1-15 — 12 ไฟล์)**
- ปัญหา: cowork ฝัง modal CSS/HTML/Firebase scripts ไว้ใน frame-busting `<script>` ทำให้ HTML พัง modal ไม่มี styling
- แก้: ลบโค้ดผิดที่ออก → ใส่ frame-busting สะอาด + modal CSS ใน `<style>` หลัก + modal HTML ก่อน `</body>`
- ใช้ CSS variables (var(--muted), var(--accent)) แทน hardcoded hex
- เพิ่ม `.kp-divider::before/::after` pseudo-elements ให้เส้น divider "หรือ" แสดงถูกต้อง

**2. ระบบ Lock/Unlock ดาวน์โหลด (14 ไฟล์)**
- Lab 1-5: ปุ่ม `⬇` สีเขียว ดาวน์โหลดได้เลย
- Lab 6+: ปุ่ม `🔒` สีเทา → กดแล้ว popup login
- Login แล้ว: ปุ่มเปลี่ยนเป็น `⬇` สีเขียวอัตโนมัติ (ผ่าน Firebase onAuthStateChanged)
- ใช้ใน: simulation files, virtual-physics-lab-01.html, library.html

**3. แก้ `<\!--` → `<!--` ทั้งโปรเจกต์ (50+ ไฟล์)**
- escaped comment ทำให้ข้อความ `<!-- Google tag -->` โผล่เป็นตัวอักษรบนหน้าเว็บ

**4. แก้ git issues**
- ลบ `.git/HEAD.lock` + `.git/objects/maintenance.lock`
- ลบ `.git/refs/remotes/origin/HEAD 2` (cloud sync สร้างไฟล์ซ้ำ)

**5. ปรึกษาธุรกิจ + วางแผน**
- วิเคราะห์ material 3 ประเภท: Demo/Simulation, คู่มือ Lab, ข้อสอบ+Simulation
- เสนอ Tier: Free / Premium 390 บาท/ปี / School License 5,000 บาท/ปี
- เสนอฟีเจอร์ admin dashboard ที่ควรเพิ่ม

**6. ปรับ Admin Dashboard (`_admin/admin.html`) — เพิ่ม 4 ฟีเจอร์ใหญ่**
- **Tab Navigation:** ภาพรวม | สมาชิก | ดาวน์โหลด
- **กราฟ 2 ตัว:** สมาชิกใหม่ 30 วัน (ฟ้า) + ดาวน์โหลด 30 วัน (เขียว) — CSS bar chart + hover tooltip
- **ไฟล์ยอดนิยม:** ตารางแสดง Lab ที่ถูกดาวน์โหลดเยอะสุด
- **Download Log:** ตาราง 100 รายการล่าสุด (ใคร โหลดอะไร เมื่อไหร่)
- **สิทธิ์ละเอียด:** modal แก้ไขมี 3 หมวด — Content Types (Sim/คู่มือ/ข้อสอบ) + Topics (5 วิชา) + Labs (Lab 1-20 ทีละตัว)

**7. Download Logging (`kp-auth.js` + simulation files)**
- เพิ่ม `logDownload()` ใน `kp-auth.js` → เขียน Firestore `download_logs` collection
- เรียก `logDownload()` ใน `_doDl()` ทุกไฟล์ (Lab 6.1-20 + VPL + library)

**8. เพิ่ม Lab 16-20 เข้าระบบ (5 ไฟล์ simulation + admin + VPL + library)**
- เพิ่มปุ่มดาวน์โหลด + auth modal + lock system ใน 5 simulation files
- เพิ่ม Lab 16-20 ใน admin LAB_LIST (รวม 22 Labs)
- เพิ่มปุ่ม `⬇ คู่มือ Lab` ใน virtual-physics-lab-01.html (5 การ์ด) + library.html (5 รายการ)

**9. Banner "สมัครสมาชิกฟรี" (index + VPL + library)**
- แถบสีเขียวอ่อน: 🔑 สมัครสมาชิกฟรี — ปลดล็อกคู่มือ Lab ดาวน์โหลดได้ทันที [สมัครเลย →]
- ซ่อนอัตโนมัติเมื่อ login แล้ว

**10. แก้ mobile layout ทั้งโปรเจกต์ (35 ไฟล์)**
- VPL 22 ไฟล์ + Demo 13 ไฟล์: เพิ่ม CSS `order:-1` ให้ canvas ขึ้นก่อน controls บนมือถือ
- แก้ iOS Safari drift bug ใน vector_forces_sim.html (threshold 8px + orientationchange)
- ปรับ canvas height ใน free-fall-experiment.html บนมือถือ (50vw / max 280px)
- ปรับ pendulum_energy_sim.html ให้ canvas ขึ้นก่อน controls บนมือถือ

**11. แก้ hero section เพี้ยน ใน virtual-physics-lab-01.html**
- ลบ CSS ซ้ำจาก index.html ที่ถูกใส่มาผิดไฟล์ (hero เต็มจอ + stats-bar ~30 บรรทัด)

**12. ย้ายตำแหน่ง "ลูกทั้งสองตกพื้นพร้อมกัน" ใน demo02_01_shooter_dropper**
- ย้าย result banner จากกลางล่าง → มุมขวาบน (ไม่บังวัตถุตอนตกถึงพื้น)

**13. KP Topbar ทุกหน้า (50 ไฟล์)**
- เพิ่ม topbar: Logo KP Science + Demo/Collections/Library/เกี่ยวกับ/ติดต่อ + ทดลองฟรี + เข้าสู่ระบบ
- VPL 22 ไฟล์ + Demo 25 ไฟล์ + main pages 3 ไฟล์
- ลบปุ่ม "← กลับหน้าแรก" เก่า (topbar แทน)
- Login แล้ว: แสดงชื่อ user + ปุ่มออก
- บนมือถือ: ซ่อน links + CTA เหลือแค่ logo + login
- **แก้ topbar ถูก inject ผิดที่** ใน frame-busting (VPL 20 ไฟล์) + domain protection (Demo 25 ไฟล์)

**14. แก้ Domain Protection Script (Demo 25 ไฟล์)**
- ปัญหา: `</script>` ใน JS string ทำให้ browser ปิด script ก่อนกำหนด → stray text โผล่
- แก้: เขียน protection script ใหม่ไม่มี `</script>` ใน string + ลบ stray text

**15. ลายน้ำ PDF คู่มือ Lab (22 ไฟล์)**
- ลายน้ำ "KP Science" ทแยงกลางหน้า (สีเทาจาง)
- หัวกระดาษ "KP Science | kp-science.github.io/physics-simulations" มุมบนขวาทุกหน้า

**16. สร้าง `_admin/protect_new_file.py` — สคริปต์ setup ไฟล์ใหม่อัตโนมัติ**
- สแกน + แก้ไขอัตโนมัติ: GA, Frame protection, Domain protection, Topbar, Mobile layout, Comments
- เพิ่มคำสั่งใน CLAUDE.md เพื่อให้ Claude ทุก session รู้จัก

### ไฟล์ที่แก้/สร้าง

| ไฟล์ | การเปลี่ยนแปลง |
|------|----------------|
| `kp-auth.js` | เพิ่ม `logDownload()` |
| `_admin/admin.html` | เขียนใหม่: tab + กราฟ + download log + สิทธิ์ละเอียด |
| `_admin/fix_auth_modal.py` | สคริปต์แก้ auth modal 12 ไฟล์ |
| `_admin/add_lock_system.py` | สคริปต์เพิ่ม lock/unlock ดาวน์โหลด |
| `_admin/add_dl_lab16_20.py` | สคริปต์เพิ่มดาวน์โหลด Lab 16-20 |
| `_admin/fix_mobile_order.py` | สคริปต์แก้ mobile layout |
| `_admin/add_topbar.py` | สคริปต์เพิ่ม topbar |
| `_admin/fix_topbar_v2.py` | สคริปต์แก้ topbar ผิดตำแหน่ง |
| `_admin/fix_demo_mobile.py` | สคริปต์แก้ demo mobile layout |
| `_admin/add_watermark.py` | สคริปต์เพิ่มลายน้ำ PDF |
| `_admin/protect_new_file.py` | สคริปต์ setup ไฟล์ใหม่อัตโนมัติ |
| `Virtual Physics Lab 01/Mechacnics/*.html` (22 ไฟล์) | auth modal + lock + topbar + mobile fix |
| `Demo/mechanics/**/*.html` (25 ไฟล์) | topbar + domain protection fix + mobile fix |
| `index.html` | banner สมัครสมาชิก + แก้ `<!--` |
| `virtual-physics-lab-01.html` | banner + ปุ่ม Lab 16-20 + แก้ hero CSS + lock system |
| `library.html` | banner + ปุ่ม Lab 16-20 + lock system |
| `mechanics.html` | topbar |
| `course.html` | topbar |
| `plane_mirror_reflection.html` | topbar |
| `CLAUDE.md` | เพิ่มคำสั่ง protect ไฟล์ใหม่ |
| `Virtual Physics Lab 01/lab-manuals-pdf/*.pdf` (22 ไฟล์) | ลายน้ำ + หัวกระดาษ |

### ค้างไว้ / ต้องทำต่อ

- `protect_new_file.py --scan` ยังเจอ issues เรื่อง mobile order ในบาง main pages (index, library, course) — ไม่กระทบการใช้งานจริง เพราะหน้าพวกนี้ไม่มี sim canvas
- ข้อสอบ + Simulation (Interactive Exam) ยังไม่ได้สร้าง — รอเจ้าของตัดสินใจ
- Facebook Page "KP Science" ยังไม่ได้สร้าง
- ยังไม่ได้ commit/push ขึ้น GitHub

### หมายเหตุ

- **สั่ง "protect ไฟล์ใหม่"** ใน session ใดก็ได้ → Claude จะรัน `python3 _admin/protect_new_file.py --scan --fix`
- Topbar บน simulation files ใช้ class `.kp-topbar` (ไม่ใช่ `.topbar` ของ index.html) เพื่อไม่ให้ CSS ชนกัน
- Domain protection script ใน Demo ต้องไม่มี `</script>` ใน JS string — ใช้ `document.body.innerHTML` แทน `document.documentElement.innerHTML`
- PDF ลายน้ำ: รัน `python3 _admin/add_watermark.py "Virtual Physics Lab 01/lab-manuals-pdf/" --all`

---

## [2026-04-11 session ต่อ] — สร้าง Experiment 31: Waves in a Ripple Tank

### ทำอะไรไปบ้าง

**1. สร้าง simulation ใหม่: `Virtual Physics Lab 02/31. waves-in-ripple-tank.html`**
- ถังคลื่น (Ripple Tank) — Experiment 31 ครบทั้ง 3 การทดลองย่อย:
  - **I. Stroboscope Calibration** — สโตรโบสโคป 6 ช่อง ปรับ N (slits/s) เพื่อ "หยุดคลื่น" วัด λ จริง
  - **II. λ vs f** — ปรับความถี่ 8-18 Hz สังเกต λ เปลี่ยน (ผกผัน) พร้อมกราฟ mini chart
  - **III. Speed vs Depth** — เปรียบเทียบน้ำลึก (10mm, v≈25 cm/s) กับน้ำตื้น (1mm, v≈21 cm/s) พร้อมแผ่นกระจก visual
- **Canvas animation:** คลื่นวงกลมแผ่ออกจากแหล่งกำเนิดจุด, amplitude decay ∝ 1/√r
- **Stroboscope effect:** sampling wave at discrete intervals — N=f → คลื่นนิ่ง, N=2f → λ ปรากฏ = λ/2
- **Stroboscope disk:** แสดงจานหมุน 6 ช่องที่มุมขวาล่าง canvas
- **Depth mode:** แสดงบริเวณน้ำลึก/ตื้นแยกกัน คลื่นเบียดกันในน้ำตื้น (λ สั้นลง)

**2. โหมดบันทึกค่า 2 โหมด:**
- **📏 วัดค่าเอง (default):** คลิก 2 จุดบน canvas วัดระยะ → บันทึกในตารางเอง
- **🤖 อัตโนมัติ:** ค่า λ, v เติมอัตโนมัติในตารางและ readout

**3. Tab 3 อัน:**
- 🎬 Simulation — canvas + controls + data tables + mini graph
- 📋 วิธีการทดลอง — ขั้นตอน 7 ข้อ + วิธีบันทึกผล
- 📐 ทฤษฎี — visual อธิบาย v=fλ, สโตรโบสโคป, λ vs f, v vs depth พร้อม canvas diagrams

**4. รัน `protect_new_file.py`** — เพิ่ม mobile layout fix อัตโนมัติ

### ไฟล์ที่สร้าง/แก้

| ไฟล์ | การเปลี่ยนแปลง |
|------|----------------|
| 🆕 `Virtual Physics Lab 02/31. waves-in-ripple-tank.html` | simulation ใหม่ครบ 3 การทดลอง |

### ค้างไว้ / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ถ้าต้องการ

### หมายเหตุ

- Physics data ตรงกับ Experiment 31 reference: λ=3.1cm@8Hz, v≈25cm/s deep, v≈21cm/s shallow
- Accent color ใช้ `#818cf8` (purple) สำหรับหมวดคลื่น
- ไฟล์ VPL02 ตอนนี้มี 3 ไฟล์: Lab 21 SHM, Lab 30 Waves on Spring, Lab 31 Ripple Tank

---

## [2026-04-11] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**สร้าง Experiment 32 — Wave Reflection (การสะท้อนของคลื่น)**
- สร้างไฟล์ simulation ใหม่ `Virtual Physics Lab 02/32. wave-reflection.html`
- อ้างอิงจาก Experiment 32 Reflection (ใบงานการทดลอง) + รูปแบบจากไฟล์ 31
- ใช้ physics-simulation-builder skill + protect script

**ฟีเจอร์หลัก:**
- คลื่น 2 ชนิด: หน้าตรง (Plane) / วงกลม (Circular)
- ผิวสะท้อน 3 ชนิด:
  1. หน้าตรง (Flat) — ปรับมุม 0-75°, ตารางบันทึกค่า 7 แถว (α, θi, θr, %ผิดพลาด), กราฟ θi vs θr, export CSV
  2. วงกลม (Circular) — เว้า/นูน, ลากตำแหน่งได้, ปุ่ม Reset Position
  3. พาราโบลา (Parabolic) — เว้า/นูน, ลากตำแหน่งได้, แสดงจุดโฟกัส
- โหมดบันทึก: Manual (default) / Auto
- Wave rendering: arc-based ripple tank style, mirror source (flat), converge-diverge (curved concave/convex)
- Shadow zone ตามรูปทรงผิวสะท้อน (โค้งตามวงกลม/พาราโบลา)
- 3 Tabs: Simulation, วิธีการทดลอง, ทฤษฎี

**ปรับปรุงหลังสร้าง (session เดียวกัน):**
- แก้คำว่า "กระจก" → "ผิวสะท้อน" ทั้งหมด (ถังคลื่นใช้ท่อยาง ไม่ใช่กระจก)
- แก้ทิศคลื่นสะท้อนหน้าตรง (y sign fix) ให้เคลื่อนที่ออกจากผิวสะท้อนถูกต้อง
- เขียน protractor ใหม่ทั้งหมด: θi/θr arcs วัดจาก Normal ถูกต้อง, filled sectors
- แก้คลื่นสะท้อนจากผิวเว้า: converge เข้า F → diverge ออกจาก F (ไม่ใช่แค่กระจายจาก F)
- ขยายขอบผิวสะท้อนวงกลม/พาราโบลาให้ยาวถึงขอบ canvas
- แก้ shadow zone วงกลมนูน (จากรูป X → ตามโค้ง)
- ใช้ drawReflectedConvergeDiverge สำหรับทุกกรณี (ทั้งเว้าและนูน)
- แหล่งกำเนิดวางกลาง canvas สำหรับผิวโค้ง (ไม่ auto วางที่ F)
- **Manual mode:** ไม่แสดง θi/θr arcs + readout, เพิ่มเครื่องวัดมุม 360° ลาก+หมุนได้
- **Auto mode:** แสดง θi/θr arcs + readout ค่ามุม
- เพิ่ม α label (มุมระหว่าง Normal หลังผิวสะท้อนกับทิศคลื่นตกกระทบ)
- เพิ่มเส้นทิศคลื่นตกกระทบ (ลูกศรประสีแดง) วางด้านหลังผิวสะท้อน
- ตาราง: ทุกช่อง (α, θi, θr) กรอกตัวเลขได้ + คอลัมน์ %ผิดพลาด คำนวณอัตโนมัติ
- Theory tab: เปลี่ยนเป็นทฤษฎีคลื่นผิวน้ำในถังคลื่น, ภาพ canvas เป็น ripple tank style ตรงกับ simulation
- Procedure tab: ปรับให้ตรงกับ simulation ปัจจุบัน (11 ขั้นตอน)
- รัน protect script หลายรอบ (MOBILE layout fix)

### ไฟล์ที่แก้/สร้าง

- 🆕 `Virtual Physics Lab 02/32. wave-reflection.html` — simulation การสะท้อนของคลื่น (แก้ไขหลายรอบ)

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ถ้าต้องการ

### หมายเหตุ

- ใช้ accent `#818cf8` (purple) ตามหมวดคลื่น ตรงกับไฟล์ 31
- Physics: v=√(gh)≈25cm/s, λ=v/f, กฎสะท้อน θi=θr, mirror equation 1/v+1/u=1/f สำหรับ curved
- เงามืดตามรูปทรง: flat=เส้นตรงเอียง, circular=โค้งวงกลม, parabolic=โค้งพาราโบลา
- Manual mode: ไม่แสดงคำตอบ (θi, θr) ให้นักเรียนวัดเอง / Auto mode: แสดงทุกอย่าง
- ไฟล์ VPL02 ตอนนี้มี 4 ไฟล์: Lab 21 SHM, Lab 30 Waves on Spring, Lab 31 Ripple Tank, Lab 32 Wave Reflection

---

## [2026-04-11 ต่อ] — เครื่องที่บ้าน (session เดียวกัน)

### ทำอะไรไปบ้าง

**สร้าง Lab 32B — การสะท้อนของแสง (Reflection of Light)**
- สร้างไฟล์ simulation ใหม่ `Virtual Physics Lab 02/32B. light-reflection.html`
- อ้างอิงจาก Experiment 32 Reflection (ใบงานการทดลองเรื่องการสะท้อนของแสงด้วยกระจกเงาราบ + เข็มหมุด)
- ใช้ physics-simulation-builder skill + protect script

**ฟีเจอร์หลัก:**
- การทดลองจำลอง: กระจกเงาราบ (top view), เข็มหมุด P₁-P₄, เส้น Normal, รังสีตกกระทบ/สะท้อน
- **Manual mode (default):** นักเรียนคลิกวางเข็มหมุดสะท้อน P₃ P₄ บน canvas, ลากปรับตำแหน่งได้, โปรแทรกเตอร์ overlay (toggle), ตาราง input กรอก θi θr เอง, %Error คำนวณอัตโนมัติ, Hint system (สี 3 ระดับ: ตรงแนว/ใกล้/ไม่ตรง)
- **Auto mode:** slider ปรับ θi (5-80°), แสดงรังสีสะท้อนพร้อมมุม arc + readout, ปุ่มบันทึกค่า, กราฟ θi vs θr (scatter + reference line y=x), Export CSV
- ภาพเสมือน (virtual image): แสดง P₁' P₂' จางๆ เหนือกระจกใน manual mode
- 3 Tabs: การทดลอง, วิธีการทดลอง, ทฤษฎี
- Theory tab: 2 canvas diagrams (กฎการสะท้อน + การสร้างภาพในกระจกเงาราบ)
- Procedure tab: ขั้นตอน real lab (12 ขั้นตอน) + virtual lab (ทั้ง 2 โหมด) + ตัวอย่างตาราง + สูตร %Error
- รัน protect script → เพิ่ม Topbar + Mobile layout fix

### ไฟล์ที่สร้าง

- 🆕 `Virtual Physics Lab 02/32B. light-reflection.html` — simulation การสะท้อนของแสง

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ถ้าต้องการ

### หมายเหตุ

- ใช้ accent `#fb923c` (orange) สำหรับหมวดแสง ตาม skill mapping
- Physics: กฎการสะท้อน θi = θr, %Error = |θi - θr| / θi × 100
- Manual mode: ไม่แสดงค่ามุมที่ถูกต้อง ให้นักเรียนวัดเองด้วย protractor overlay
- ไฟล์ VPL02 ตอนนี้มี 5 ไฟล์: Lab 21 SHM, Lab 30 Waves on Spring, Lab 31 Ripple Tank, Lab 32 Wave Reflection, Lab 32B Light Reflection

---

## [2026-04-11 ต่อ #2] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**ปรับปรุง Lab 32B — การสะท้อนของแสง (major rework)**
- เขียนใหม่ทั้ง simulation logic ตามคำสั่งผู้ใช้ 6 ข้อ

**การเปลี่ยนแปลงหลัก:**
1. **ย้ายกระจกมาตรงกลาง canvas** (mirrorY = H*0.45) เพื่อให้เงาเสมือนอยู่ภายใน canvas
2. **Step-based workflow 4 ขั้นตอน:**
   - Step 1: นักเรียนวาง P1, P2 เอง → เส้นรังสีตกกระทบปรากฏ + เงา P1', P2' เหนือกระจก
   - Step 2: วาง P3, P4 → เส้นประรังสีสะท้อนปรากฏ
   - Step 3: เส้น Normal ปรากฏ (ลากซ้าย-ขวาได้) + label "เลื่อนเส้นแนวฉากให้ตรงจุด"
   - Step 4: เปิด protractor 360° วัดมุม → กรอกตาราง → บันทึก
3. **เข็มหมุดทั้ง 4 ตัว วางเอง** (ไม่ใช่ slider กำหนดมุม) + ลากปรับตำแหน่งได้
4. **เส้น Normal ลากได้** ตามแนวกระจก — แสดง ✓ ตรงจุด! เมื่อตรง POI
5. **Protractor 360° ชนิด full circle** — ลากเลื่อน (กลาง) + หมุน (ขอบ) ด้วยเมาส์/touch
6. **ตาราง %Error** เทียบกับมุมจริงที่โปรแกรมคำนวณภายใน (ไม่แสดงค่า true angle)
7. **Step indicator dots** + hint box เปลี่ยนตามขั้นตอน
8. Auto mode ปรับให้กระจกอยู่กลางเหมือน manual

### ไฟล์ที่แก้

- `Virtual Physics Lab 02/32B. light-reflection.html` — rewrite ทั้ง JS + ปรับ HTML panel

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub

### หมายเหตุ

- Protractor: outer ring หมุน, center ลาก, เส้นอ้างอิง 0°-180° / 90°-270° สีแดง
- ทุก pin ลากปรับตำแหน่งได้หลังวาง (drag existing pins)
- computeTrueAngles() คำนวณ θi_true, θr_true จาก geometry ภายใน
- ไฟล์ VPL02 ยังมี 5 ไฟล์เท่าเดิม (แก้ไฟล์เดิม ไม่ได้สร้างใหม่)

## [2026-04-11 ต่อ #3] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**สร้าง Lab 32C — การสะท้อนคลื่นไมโครเวฟ (Reflection of Microwaves)**
- สร้างไฟล์ใหม่ `32C. microwave-reflection.html` ตาม reference จากหนังสือทดลอง
- ใช้ accent สีม่วง (#818cf8) สำหรับหมวดคลื่น

**3 Tabs:**
1. **🎬 Simulation** — top-down view มี Transmitter horn, Receiver horn (ลากได้), Reflector, protractor แบบครึ่งวงกลม
   - **โหมดบันทึกเอง (Manual):** ตั้ง θᵢ ด้วย slider → ลาก receiver หามุมที่สัญญาณแรงสุด → กรอก θᵣ → บันทึกลงตาราง + คำนวณ %Error
   - **โหมดอัตโนมัติ (Auto):** ตั้ง θᵢ เริ่ม/สุดท้าย/ช่วงห่าง → สแกนอัตโนมัติ → ตาราง + กราฟ θᵢ vs θᵣ
   - Signal strength: Gaussian falloff (σ=5°), แถบสัญญาณ gradient สี, hint box เปลี่ยนตามความแม่นยำ
   - Wave animation (wavefronts เคลื่อนที่ตลอด)
   - Export CSV ได้ทั้ง 2 โหมด
2. **📋 วิธีการทดลอง** — อุปกรณ์, ขั้นตอน Manual 7 ข้อ, ขั้นตอน Auto 4 ข้อ, ตารางบันทึกผลตัวอย่าง, ข้อควรระวัง (ภาษาไทยทั้งหมด)
3. **📐 ทฤษฎี** — visual canvas 3 ภาพ: กฎการสะท้อน (incident/reflected ray + arcs), การจัดอุปกรณ์ (ตามรูปในหนังสือ), กราฟ θᵢ vs θᵣ (slope=1) + สูตร %Error

**ข้อมูลอ้างอิงจากหนังสือ:**
- ความยาวคลื่น ~3 cm (ความถี่ ~10 GHz)
- แผ่นสะท้อนขนาด 20 cm × 20 cm
- ระยะ ~2 m จากแหล่งกำเนิดถึง reflector
- เกณฑ์ %Error ภายใน 5%

### ไฟล์ที่แก้

- `Virtual Physics Lab 02/32C. microwave-reflection.html` — **สร้างใหม่**
- รัน `protect_new_file.py --scan --fix` → เพิ่ม KP Topbar + Mobile fix

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub
- VPL02 ตอนนี้มี 6 ไฟล์: 21, 30, 31, 32, 32B, 32C

### หมายเหตุ

- Receiver ลากด้วยเมาส์/touch รอบ reflector เพื่อหามุมสะท้อน
- Signal Gaussian: σ = 5° → สัญญาณลด 50% ที่ ±4° จากจุด peak
- คำอธิบายวิธีการทดลองทั้ง tab เป็นภาษาไทยตามที่ผู้ใช้ขอ

## [2026-04-11 ต่อ #4] — เครื่องที่บ้าน (session เดียวกัน)

### ทำอะไรไปบ้าง

**Rewrite Lab 32C — 2-Axis Detection (major redesign)**

ผู้ใช้ขอรีดีไซน์ simulation ใหม่ทั้งหมด:

1. **Canvas แบ่ง 2 มุมมอง:**
   - **Plan View (ด้านบน):** ลากตัวรับซ้าย-ขวา → เปลี่ยนมุมแนวราบ θᵣ
   - **Side View (ด้านข้าง):** ลากตัวรับบน-ล่าง → เปลี่ยนมุมแนวดิ่ง φᵣ (±20°)

2. **สุ่มมุมทุกครั้ง:** กด "🎲 สุ่มมุมใหม่" → θᵢ (15°–75°), φᵢ (±18°) สุ่มใหม่

3. **ไม่แสดงรังสี:** ผู้ทดลองเห็นแค่ตำแหน่ง TX/RX + สัญญาณ (bar + ตัวเลข %)

4. **Workflow:** ลาก RX หา peak → กด "✓ เสร็จสิ้น" (ล็อก) → กด "📝 บันทึก" → เปิดเผยค่าจริง + %Error

5. **Signal:** 2D Gaussian σ=5° จาก (θᵢ, φᵢ)

6. **ตาราง:** แสดง θᵢ, φᵢ, θᵣ, φᵣ, %Error_θ, |Δφ| พร้อม color-code (เขียว=ผ่าน, แดง=ไม่ผ่าน)

7. **Tab ทฤษฎี:** เพิ่ม visual diagram "การสะท้อนเมื่อระนาบเอียง" แสดง φᵣ = φᵢ

### ไฟล์ที่แก้

- `Virtual Physics Lab 02/32C. microwave-reflection.html` — **rewrite ทั้งหมด** (2-axis version)
- รัน `protect_new_file.py` → เพิ่ม KP Topbar + Mobile fix

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push

### หมายเหตุ

- Plan View: ลาก RX บน arc ขวาของ reflector → θᵣ
- Side View: ลาก RX บน-ล่าง → φᵣ (±20°)
- กด "เสร็จสิ้น" ล็อก RX → กด "บันทึก" เปิดเผยค่าจริง
- Auto mode ยังคงมี (สุ่ม+scan อัตโนมัติ + กราฟ)

## [2026-04-12] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**สร้าง Lab 34 — Diffraction & Interference in a Ripple Tank**
- สร้างไฟล์ใหม่ `34. wave-diffraction-interference.html` ตาม Experiment 34 จากหนังสือทดลอง
- ใช้ accent สีม่วง (#818cf8) สำหรับหมวดคลื่น

**3 Tabs:**
1. **🎬 Simulation** — 2 การทดลองย่อย (sub-tab):
   - **A — Single Slit Diffraction:** ปรับความกว้างช่อง (0.5λ–5λ) + ความถี่ (2–10 Hz)
   - **B — Double Slit Interference:** ปรับระยะห่างช่อง (1λ–8λ) + ความถี่ (2–10 Hz)
   - Wave animation ใช้ Huygens' principle: ทุก point source บนช่องเปิดปล่อยคลื่นวงกลม แล้ว superpose
   - **โหมด Manual (default):** โปรแทรกเตอร์บน canvas (คลิกค้าง+ลาก) วัดมุม diffraction → กรอกค่า → บันทึกลงตาราง + คำนวณ %Error
   - **โหมด Auto:** เลือกตัวแปรสแกน (ความกว้างช่อง/ระยะห่างช่อง/ความถี่) → ตั้ง start/end/step → สแกนอัตโนมัติ → ตาราง + กราฟ
   - Export CSV ได้ทั้ง 2 โหมด
2. **📋 วิธีการทดลอง** — อุปกรณ์ 6 รายการ, ขั้นตอน Manual+Auto ทั้ง 2 การทดลอง, ตารางบันทึกผลตัวอย่าง, ข้อควรระวัง (ภาษาไทยทั้งหมด)
3. **📐 ทฤษฎี** — visual canvas 4 ภาพ:
   - Huygens' Principle (secondary sources + envelope)
   - Single Slit Diffraction (barrier, slit, diffracted waves, θ₁, formula a sin θ₁ = λ)
   - Double Slit Interference (S₁/S₂, circular waves, constructive/destructive, d sin θ = nλ)
   - กราฟ λ vs f (hyperbola) + θ₁ vs a/λ (single slit)

**ข้อมูลฟิสิกส์:**
- v = 20 cm/s (น้ำตื้น ~0.7 cm)
- f = 5 Hz → λ = 4.0 cm
- Single slit: a sin θ = mλ (minima), θ₁ = sin⁻¹(λ/a)
- Double slit: d sin θ = nλ (constructive), d sin θ = (n+½)λ (destructive)
- Nodal lines count = 2 × floor(d/λ - 0.5) (ทั้ง 2 ด้าน)

### ไฟล์ที่แก้

- `Virtual Physics Lab 02/34. wave-diffraction-interference.html` — **สร้างใหม่**
- รัน `protect_new_file.py --scan --fix` → เพิ่ม KP Topbar + Mobile fix

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub
- VPL02 ตอนนี้มี 8 ไฟล์: 21, 30, 31, 32, 32B, 32C, 33, 34

### หมายเหตุ

- Wave rendering ใช้ pixel-by-pixel (ImageData) sample ทุก 3px เพื่อประสิทธิภาพ
- Amplitude decay: 1/(r^0.35) ให้ pattern ชัดเจนแม้ไกลจาก slit
- Protractor: คลิกค้าง+ลากบน canvas ด้านขวาของ barrier → วัดมุม θ จากแนวตั้งฉาก → auto-fill ช่อง input
- Auto scan ทำงานสมบูรณ์: เลือก slit width/freq → สแกน → ตาราง + กราฟ θ₁ vs ตัวแปร

## [2026-04-12 ต่อ] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**สร้าง Lab 37 — Standing Waves on a String**
- สร้างไฟล์ใหม่ `37. standing-waves.html` ตาม Experiment 37 จากหนังสือทดลอง
- ใช้ accent สีม่วง (#818cf8) สำหรับหมวดคลื่น

**3 Tabs:**
1. **🎬 Simulation** — คลื่นนิ่งบนเส้นเชือกแนวตั้ง:
   - เชือกแขวนจาก doorbell (สั่น) ด้านบน → น้ำหนักถ่วงด้านล่าง
   - **4 ตัวแปร:** น้ำหนัก W (0.01–3.0 N), ความถี่ f (10–120 Hz), ความยาวเชือก L (0.5–2.5 m), μ (0.5–20 g/m)
   - Animation แสดง standing wave ด้วย sin(nπx/L)·cos(ωt) พร้อม envelope
   - แสดง Nodes (จุดฟ้า) และ Antinodes (จุดม่วง)
   - **Resonance quality:** คำนวณ detuning จาก n_exact → แสดง Q% บน canvas, ถ้า Q<30% แสดงข้อความเตือน
   - Scale bar 10 cm, แสดง L, info box (n, λ, v, Q)
   - **โหมด Manual (default):** คลิก Node 2 จุดบน canvas → วัดระยะ d → กรอกค่า → บันทึก → คำนวณ λ=2d, v=fλ, %Error เทียบกับ v=√(T/μ)
   - **โหมด Auto:** เลือกสแกน W หรือ f → ตั้ง start/end/step → ตาราง (Trial, W, f, L, μ, v, λ, n, d) + กราฟ λ & v vs ตัวแปร
   - Export CSV ได้ทั้ง 2 โหมด
2. **📋 วิธีการทดลอง** — จุดประสงค์, อุปกรณ์ 6 รายการ, ขั้นตอน Manual 7 ขั้น + Auto 5 ขั้น, ตารางบันทึกผลตัวอย่าง, Hint, ข้อควรระวัง (ภาษาไทย)
3. **📐 ทฤษฎี** — visual canvas 4 ภาพ:
   - Superposition diagram (คลื่นขาไป + สะท้อน → คลื่นนิ่ง + N/A labels + λ/2 annotation)
   - v = √(T/μ) diagram (เชือก + tension arrows + สูตร)
   - Harmonic modes (n=1–4 แต่ละ mode สีต่างกัน + envelope + nodes)
   - ผลของ tension (3 เชือกเทียบ: น้ำหนักน้อย/กลาง/มาก → จำนวน loop ต่างกัน)
   - Formula boxes: λ=2d, v=√(T/μ), v=fλ, resonance L=nλ/2
   - ตัวอย่างการคำนวณ 3 trials (W=0.029, 0.44, 1.32 N)

**ข้อมูลฟิสิกส์:**
- Default: f=60Hz (AC 6V), L=1.50m, μ=4.0g/m=0.004kg/m
- v = √(T/μ), λ = v/f, n = 2L/λ, d = λ/2
- ตรวจสอบค่า: W=0.44N → v=10.49 m/s, λ=0.175 m, n≈17 loops ✓
- W=0.1N → v=5.00 m/s ✓, W=1.32N → v=18.17 m/s ✓

**รัน protect_new_file.py**
- เพิ่ม KP Topbar + Mobile fix ให้ไฟล์ใหม่
- GA code (G-2YTJBNHP6D) มีอยู่แล้วตั้งแต่สร้าง

### ไฟล์ที่แก้/สร้าง
- 🆕 `Virtual Physics Lab 02/37. standing-waves.html` — **สร้างใหม่**
- รัน `protect_new_file.py --scan --fix` → เพิ่ม KP Topbar + Mobile fix

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ commit/push ขึ้น GitHub
- VPL02 ตอนนี้มี 9 ไฟล์: 21, 30, 31, 32, 32B, 32C, 33, 34, 37

### หมายเหตุ
- Standing wave ใช้ resonance mode: n_nearest = round(2L/λ), detuning ควบคุม amplitude
- Canvas วาดเชือกแนวตั้ง (doorbell บน, น้ำหนักล่าง) ตามรูปในหนังสือ Lab
- คลิกวัด node: คลิก 2 จุดบน canvas → คำนวณ d จาก pixel distance / string length × L
- Auto scan กราฟ: dual y-axis (λ เส้นทึบ สีเขียว + v เส้นประ สีม่วง)

---

## [2026-04-12 —:—] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง

**1. Rewrite Lab 34 — Diffraction & Interference (He-Ne Laser)**
- เปลี่ยนจาก Ripple Tank simulation → **Laser Diffraction & Interference** ตามเอกสาร Lab Experiment 34
- สร้างใหม่ทั้งหมด 3 การทดลองย่อย:
  - **A — Knife-Edge Diffraction:** เลื่อนใบมีดบังลำแสงเลเซอร์, Fresnel diffraction fringes, Fresnel integral computation
  - **B — Single-Slit Diffraction:** ปรับความกว้างช่องด้วย slider, Fraunhofer diffraction pattern [sin(β)/β]², photometer ลากวัด intensity บน canvas
  - **C — Diffraction Grating:** เลือกเกรตติง (5276/10000/3000/600 gr/cm), ปรับระยะ L, แสดง order maxima ตาม d·sin(θ)=mλ, ruler วัดตำแหน่ง, คำนวณ λ=d·x/L + %Error
- ค่าอ้างอิง: λ(He-Ne) = 632.8 nm
- 2 โหมดบันทึก: Manual (ลาก photometer อ่านค่า → กรอกเอง) และ Auto (สแกน → ตาราง + กราฟ)
- 3 Tab: Simulation, วิธีการทดลอง, ทฤษฎี (4 canvas visuals: Huygens, Fresnel, Fraunhofer, Grating diagram)
- Export CSV, ตารางตัวอย่างตรงกับเอกสาร lab
- รัน protect_new_file.py → เพิ่ม GA, Mobile fix

### ไฟล์ที่แก้/สร้าง
- ✏️ `Virtual Physics Lab 02/34. wave-diffraction-interference.html` — rewrite เป็น Laser Diffraction simulation

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ commit/push ขึ้น GitHub
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ในอนาคตได้

### หมายเหตุ
- Fresnel integral ใช้ trapezoidal numerical integration (25-60 steps ตาม |u|)
- Pattern caching: compute once per parameter change, reuse for animation frames
- Touch support สำหรับ photometer probe บน mobile
- Grating calculation ตรงกับข้อมูลตัวอย่าง: 5276 gr/cm, L≈1.05m → x≈0.35m → λ≈633nm

---

## [2026-04-12 — บ้าน]

### ทำอะไรไปบ้าง
- สร้างระบบ **Watermark Overlay Module** สำหรับ simulation ทุกไฟล์
  - `_shared/watermark.js` — โมดูลลายน้ำ v2 (overlay canvas แยก, ไม่แตะ logic simulation)
  - แสดงลายน้ำ "KP Science / Virtual Physics Lab" จางๆ 12% บน canvas หลัก
  - ปลดล็อกได้ผ่าน `localStorage('kp_access_tier', 'pro')` → ลายน้ำหาย
  - API: `KPWatermark.remove()`, `.show()`, `.check()`
  - Sync ข้ามแท็บผ่าน `storage` event
- **อัปเดต `protect_new_file.py`** — เพิ่ม 3 การตรวจใหม่:
  - `WATERMARK` — inject `<script src="watermark.js">` อัตโนมัติ (VPL01 + VPL02 + Demo)
  - `TOPBAR_CSS` — ตรวจจับกรณี topbar HTML มี แต่ CSS หายไป
  - แก้ label scan output
- **ใส่ watermark ครบ 56 ไฟล์:** VPL01 (22) + VPL02 (9) + Demo (25)
- **แก้บัค watermark v1 → v2:**
  - v1 แปะ overlay บนทุก canvas (graph, theory, hidden) → v2 เฉพาะ canvas แรกที่ ≥400px
  - v1 ใช้ attribute size → canvas HiDPI ล้น/เยื้อง → v2 ใช้ CSS display size (offsetWidth)
  - v1 opacity 7% จางเกินบนพื้นหลังลวดลาย → v2 เพิ่มเป็น 12%
  - v2 ปรับ font size อัตโนมัติตามขนาด canvas (24-48px)
- **แก้บัค topbar CSS หาย** ใน 8 ไฟล์ VPL01 — inject CSS + แก้ `nav { }` selector เป็น `nav:not(.kp-topbar)` เพื่อไม่ override topbar
- ลบ inline watermark เดิมจาก Lab 37 (ใช้ overlay module แทน)
- อัปเดต `CLAUDE.md` เพิ่มเอกสาร Watermark System
- เปลี่ยน dev server ใน `.claude/launch.json` ให้ serve จาก project root (แก้ปัญหา `../_shared/` path 404)

### ไฟล์ที่แก้/สร้าง
- ✨ `_shared/watermark.js` — สร้างใหม่ (watermark overlay module v2)
- ✏️ `_admin/protect_new_file.py` — เพิ่ม WATERMARK + TOPBAR_CSS check/fix
- ✏️ `CLAUDE.md` — เพิ่ม section Watermark System
- ✏️ `.claude/launch.json` — เปลี่ยน server root
- ✏️ `Virtual Physics Lab 02/37. standing-waves.html` — ลบ inline watermark
- ✏️ VPL01 8 ไฟล์ (3,4,5,16,17,18,19,20) — เพิ่ม topbar CSS + แก้ nav selector
- ✏️ VPL01 22 ไฟล์ + VPL02 9 ไฟล์ + Demo 25 ไฟล์ — inject watermark script tag

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ commit/push
- ระบบ login/admin ยังไม่ได้เชื่อมต่อกับ watermark (ต้องเซ็ต `kp_access_tier` ใน localStorage เมื่อ login สำเร็จ)
- VPL02 ตอนนี้มี 9 ไฟล์: 21, 30, 31, 32, 32B, 32C, 33, 34, 37

### หมายเหตุ
- Watermark ใช้ overlay canvas แยก (`pointer-events: none`, `z-index: 999`) → ไม่กระทบ interaction ของ simulation
- ไฟล์ใหม่ในอนาคต → รัน `python3 _admin/protect_new_file.py --scan --fix` จะ inject watermark ให้อัตโนมัติ
- Canvas context ไม่รองรับ CSS `var(--...)` — ระวังเรื่องนี้เสมอเมื่อวาดบน canvas

---

## [2026-04-12 session ยาว] — เครื่องที่บ้าน (Opus)

### ทำอะไรไปบ้าง

**1. อัปเดต index.html — นำเข้าไฟล์ Demo ใหม่ + VPL02 + Lab 21 SHM**

- เพิ่ม section **Virtual Physics Lab 02** (6 การ์ด: Exp 30, 31, 32, 33, 34, 37) พร้อม canvas animation preview 6 ตัว
- เพิ่มการ์ด **Exp 21: SHM รางลม** ใน VPL01 section พร้อม canvas renderer สปริง-มวล
- อัปเดต Stats Bar: 30+ → 40+ Simulation
- Canvas renderers ใหม่ 7 ตัว: `vpl-shm`, `vpl2-spring-wave`, `vpl2-ripple-tank`, `vpl2-wave-reflect`, `vpl2-refraction`, `vpl2-diffraction`, `vpl2-standing`

**2. อัปเดต Collections accordion**

- เปลี่ยนชื่อ "Simulation" → **"Demo"** + หมวดย่อย expand/collapse ได้
- **กลศาสตร์** (12 ลิงก์ตรงไปไฟล์ Demo: บทเรียนรวม, หน่วย SI, Reaction Time, Constant Velocity, Kinematics, Vector, Shooter & Dropper, Monkey Gun, Atwood, Guinea & Feather, Rolling Ball, SHM)
- **คลื่น** (5 ลิงก์: Ripple Tank, Waves, Wave Components, Seismic Wave, คลื่นผิวน้ำ)
- **แสง** (1: Plane Mirror Reflection) — เปลี่ยนจาก SOON เป็น active
- **แม่เหล็กไฟฟ้า** (1: Magnetic Field) — เพิ่มใหม่
- **ดาราศาสตร์** (1: Orbital Simulation) — แก้ลิงก์ตรงไปไฟล์
- ไฟฟ้า / อุณหพลศาสตร์ — ยังเป็น SOON
- เพิ่ม VPL02 ใน Virtual Lab accordion (9 การทดลอง)
- ลบลิงก์ที่เปิดไม่ได้: `waves.html`, `electricity.html`, `thermo.html`
- เพิ่ม CSS `.acc-sub-toggle`, `.acc-sub-list`, `.acc-sub-item` + JS `toggleSubList()`

**3. ออกแบบ Demo cards section ใหม่**

- เปลี่ยนจาก 8 การ์ดกลศาสตร์อย่างเดียว → **9 การ์ดจากทุกหมวด**:
  - กลศาสตร์ 4 ใบ (Guinea & Feather, Monkey Gun, Vector, Atwood)
  - คลื่น 2 ใบ (Ripple Tank, Waves)
  - แสง 1 ใบ (Plane Mirror)
  - แม่เหล็ก 1 ใบ (Magnetic Field)
  - ดาราศาสตร์ 1 ใบ (Orbital)
- ลิงก์ "ดูทั้งหมด" ชี้ไป `#collections` แทน `mechanics.html`

**4. เปลี่ยน "ทดลองฟรี" → "ใช้งานฟรี" (66 ไฟล์)**

- แก้ topbar CTA ทุกไฟล์ HTML + อัปเดต template ใน `protect_new_file.py`

**5. อัปเดต library.html**

- เพิ่ม Lab 21 SHM ใน VPL01
- เพิ่ม section VPL02 (9 ไฟล์)
- เพิ่ม Demo คลื่น (5), แสง (2), แม่เหล็ก (1), ดาราศาสตร์ (1)

**6. Watermark — ระบบปลดล็อกใน Admin**

- เพิ่มส่วน "🎨 ลายน้ำ" ใน admin modal (radio: ไม่ปลดล็อก / Pro / Premium / Admin)
- บันทึก `access_tier` ลง Firestore
- แสดง badge `🎨 tier` ในตารางสมาชิก
- เพิ่ม `syncWatermarkTier()` ใน `kp-auth.js` — login → อ่าน tier จาก Firestore → set localStorage → ลายน้ำหายอัตโนมัติ
- Logout → ลบ tier → ลายน้ำกลับมา

**7. แก้ปุ่มดาวน์โหลดคู่มือ Lab (8 ไฟล์ VPL01)**

- เพิ่ม CSS `.btn-dl-pdf` ที่ขาดใน: 3, 4, 5, 16, 17, 18, 19, 20

**8. Monkey Gun — ปรับมุมยิงอิสระ**

- เพิ่ม slider มุม θ (5°–80°) + checkbox "🎯 เล็งตรงเป้าอัตโนมัติ"
- Auto-aim off: ปรับมุมเอง กระสุนอาจพลาด / Auto-aim on: ล็อกตรง target ชนเสมอ
- แก้ visual angle ของกระบอกปืนให้ขนานกับเส้นไกด์ (แก้ aspect ratio bug)
- เพิ่มเส้นประ "เส้นเล็งตรง" ให้นักเรียนเปรียบเทียบ

**9. แก้ Ripple Tank (Demo/คลื่น/ripple_tank_1.html)**

- แก้บั๊ก clipRect ตัดรังสีสะท้อนออกสำหรับผิวสะท้อนนูน (cx, xp)
- ก่อนแก้: เลือก นูนวงกลม/นูนพาราโบลา → canvas ว่าง
- หลังแก้: คลื่นตกกระทบ + สะท้อนแสดงถูกต้องทุก mirror type

**10. Protect ไฟล์ใหม่**

- รัน `protect_new_file.py --scan --fix` — Demo ใหม่ 8 ไฟล์ได้ GA + Topbar + Watermark

### ไฟล์ที่แก้/สร้าง

| ไฟล์ | การเปลี่ยนแปลง |
|------|----------------|
| `index.html` | VPL02 section, Lab 21 SHM card, 7 canvas renderers, Demo cards ใหม่ 9 ใบ, Collections เป็น Demo accordion + sub-list, stats 40+, ใช้งานฟรี |
| `library.html` | เพิ่ม Lab 21, VPL02 9 ไฟล์, Demo คลื่น/แสง/แม่เหล็ก/ดาราศาสตร์ |
| `kp-auth.js` | เพิ่ม `syncWatermarkTier()` + logout ลบ tier |
| `_admin/admin.html` | เพิ่ม watermark tier control (radio + save + badge) |
| `_admin/protect_new_file.py` | เปลี่ยน "ทดลองฟรี" → "ใช้งานฟรี" ใน topbar template |
| `Demo/คลื่น/ripple_tank_1.html` | แก้ clipRect bug สำหรับ convex mirrors |
| `Demo/mechanics/โปรเจคไทล์/monkey_gun-3.html` | slider มุม + auto-aim + visual angle fix |
| `VPL01 Mechacnics/3,4,5,16,17,18,19,20` (8 ไฟล์) | เพิ่ม CSS `.btn-dl-pdf` |
| ทุกไฟล์ HTML (66 ไฟล์) | "ทดลองฟรี" → "ใช้งานฟรี" |
| Demo ใหม่ 8 ไฟล์ | GA + Topbar + Watermark (ผ่าน protect script) |

### ค้างไว้ที่ไหน / ต้องทำต่อ

- ยังไม่ได้ commit/push ขึ้น GitHub

---

## 📐 SPEC สำหรับ session หน้า — ปรับ Layout index.html

> **คำสั่ง:** เปิด session ใหม่ แล้วสั่ง "ทำตาม Layout Spec ใน SESSION_LOG" — Claude จะอ่านแล้วทำได้เลย

### งาน 1: ลด Hero + เพิ่ม visual ด้านขวา

**ปัจจุบัน:** `.hero { min-height: 100vh }` + เนื้อหาอยู่ซ้ายอย่างเดียว ด้านขวาว่างเปล่า

**เปลี่ยนเป็น:**
- `.hero { min-height: 70vh }` (ลดจาก 100vh)
- เพิ่ม `.hero-visual` ด้านขวา ใช้ CSS grid 2 คอลัมน์
- ด้านขวาแสดง **canvas animation ตัวอย่าง** (เช่น ลูกตุ้มแกว่ง + เส้นกราฟ energy) หรือ iframe เล็กๆ โชว์ simulation จริง
- มือถือ: ซ่อน `.hero-visual` เหลือแค่ text

**CSS แก้:**
```css
.hero { min-height: 70vh; display: grid; grid-template-columns: 1fr 1fr; align-items: center; }
.hero-visual { position: relative; }
@media(max-width: 768px) { .hero { grid-template-columns: 1fr; } .hero-visual { display: none; } }
```

### งาน 2: ย้าย "Why KP Science" ขึ้นมา

**ปัจจุบัน:** ลำดับ = Demo → VPL01 → VPL02 → **Why** → Collections → About
**เปลี่ยนเป็น:** Demo → **Why** → VPL01 → VPL02 → Collections → About

**วิธีทำ:** ย้าย `<section id="why">...</section>` ทั้ง block + `<div class="sdiv">` ที่ตามมา ไปวางหลัง `</section>` ของ Demo cards (ก่อน VPL01)

### งาน 3: Filter chips ใน Demo cards

**ปัจจุบัน:** แสดง 9 การ์ดทั้งหมดเรียงกัน ต้อง scroll ไกล

**เปลี่ยนเป็น:**
- เพิ่ม **filter chips** ก่อน `.demo-grid`:
```html
<div class="demo-filters">
  <button class="demo-chip active" data-cat="all">ทั้งหมด</button>
  <button class="demo-chip" data-cat="mechanics">⚙️ กลศาสตร์</button>
  <button class="demo-chip" data-cat="waves">〰️ คลื่น</button>
  <button class="demo-chip" data-cat="optics">🔦 แสง</button>
  <button class="demo-chip" data-cat="magnetism">🧲 แม่เหล็ก</button>
  <button class="demo-chip" data-cat="astronomy">🪐 ดาราศาสตร์</button>
</div>
```
- แต่ละ `<a class="demo-card">` เพิ่ม `data-cat="mechanics"` ฯลฯ
- JS กรอง: คลิก chip → ซ่อน/แสดง card ตาม data-cat
- CSS: `.demo-chip { padding:6px 14px; border-radius:20px; border:1px solid var(--border); background:transparent; color:var(--muted); cursor:pointer; font-size:.82rem; font-weight:600; } .demo-chip.active { background:var(--accent); color:#06090f; border-color:var(--accent); }`

### งาน 4: รวม VPL01 + VPL02 เป็น compact section

**ปัจจุบัน:** VPL01 = 7 การ์ด section, VPL02 = 6 การ์ด section → ยาวมาก

**เปลี่ยนเป็น:** section เดียว "Virtual Physics Lab" มี 2 tab (หรือ 2 row):

**Option A (tab):**
```html
<section id="vpl">
  <div class="sec-header-row">
    <div>
      <div class="sec-label">Virtual Physics Lab</div>
      <h2 class="sec-title">ห้องปฏิบัติการฟิสิกส์เสมือน</h2>
    </div>
  </div>
  <div class="vpl-tabs">
    <button class="vpl-tab active" onclick="switchVPL('vpl1',this)">VPL 01 · กลศาสตร์ (22)</button>
    <button class="vpl-tab" onclick="switchVPL('vpl2',this)">VPL 02 · คลื่น (9)</button>
  </div>
  <div id="vpl1" class="vpl-panel active">
    <!-- 4 การ์ดเด่น + ปุ่ม "ดูทั้ง 22 การทดลอง →" -->
  </div>
  <div id="vpl2" class="vpl-panel">
    <!-- 4 การ์ดเด่น + ปุ่ม "ดูทั้ง 9 การทดลอง →" -->
  </div>
</section>
```

**Option B (compact 2 rows):**
- VPL01: แสดง 4 การ์ดเด่น (จาก 7) + ลิงก์ "ดูทั้ง 22 →"
- VPL02: แสดง 3 การ์ดเด่น (จาก 6) + ลิงก์ "ดูทั้ง 9 →"
- ทั้งหมดอยู่ใน section เดียว

**เลือก Option A** (tab) — ประหยัดพื้นที่สุด

### ลำดับ section หลังปรับ (ใหม่)

1. Hero (70vh + visual)
2. Stats bar
3. CTA Banner (สมัครสมาชิก)
4. **Demo cards** (9 การ์ด + filter chips)
5. **Why KP Science** (ย้ายขึ้นมา)
6. **Virtual Physics Lab** (tab VPL01/VPL02 — compact)
7. Collections (Demo accordion + Virtual Lab accordion)
8. About
9. How to use
10. Early Access / สมัครสมาชิก
11. Contact
12. Footer

### หมายเหตุสำหรับ Claude ที่ทำงานต่อ

- อ่าน `CLAUDE.md` ก่อนเสมอ — มี GA code, protect script, design tokens
- ไฟล์หลักที่แก้คือ `index.html` (~1900 บรรทัด)
- Canvas renderers อยู่ท้ายไฟล์ใน `<script>` — อย่าลบ!
- test: เปิด preview server ด้วย `.claude/launch.json` (port 8765)
- ทุกครั้งที่แก้ CSS ให้เช็ค mobile responsive ด้วย (`@media max-width: 768px`)


---

## [2026-04-12] — เครื่องที่ทำงาน

### ทำอะไรไปบ้าง

**1. Hero 70vh + 2-column grid + pendulum canvas (งาน 1)**
- `.hero` เปลี่ยนจาก `min-height:100vh; display:flex` → `min-height:70vh; display:grid; grid-template-columns:1fr 1fr; gap:2rem`
- ลบ `max-width:680px` ออกจาก `.hero-inner`
- เพิ่ม `.hero-visual` + `#hero-vis-canvas` — แสดง pendulum animation + กราฟ KE/PE/E_total แบบ real-time
- Mobile (`max-width:768px`): `.hero-visual{display:none}`, hero grid กลับเป็น 1 column

**2. ย้าย Why KP Science ขึ้นก่อน VPL (งาน 2)**
- ลำดับ section ใหม่: Hero → Stats → CTA → Demos → **Why** → VPL → Collections → About → …
- ตัด `sdiv + section#why` ออกจากหลัง VPL02 แล้วแทรกก่อน VPL01

**3. Filter chips ใน Demo section (งาน 3)**
- เพิ่ม `.demo-filters` + 6 chip buttons ก่อน `.demo-grid`: ทั้งหมด / ⚙️ กลศาสตร์ / 〰️ คลื่น / 🔦 แสง / 🧲 แม่เหล็ก / 🪐 ดาราศาสตร์
- เพิ่ม `data-cat` ให้ demo-card ทั้ง 9 ใบ
- เพิ่ม `function filterDemo(chip)` — toggle active chip + show/hide card

**4. รวม VPL01 + VPL02 เป็น tab section เดียว (งาน 4)**
- ลบ `section#vpl01`, `section#vpl02`, sdiv ตรงกลาง
- สร้าง `section#vpl` ใหม่ มี `.vpl-tabs` (2 ปุ่ม) + 2 panel:
  - `#vpl1-panel` — 7 การ์ด VPL01 + ลิงก์ "ดูทั้ง 22 การทดลอง →"
  - `#vpl2-panel` — 6 การ์ด VPL02 + ลิงก์ "ดูทั้ง 9 การทดลอง →" (ชี้ virtual-physics-lab-02.html)
- เพิ่ม CSS `.vpl-tabs`, `.vpl-tab`, `.vpl-tab.active`, `.vpl-panel`, `.vpl-panel.active`
- เพิ่ม `function switchVPL(id, btn)` ใน JS

### ไฟล์ที่แก้
- `index.html` — ทั้ง 4 งานข้างต้น (~1,500+ บรรทัด)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ commit/push ขึ้น GitHub
- `virtual-physics-lab-02.html` ยังไม่มีไฟล์ (ลิงก์ใน VPL02 tab ยังชี้ไปหน้าที่ไม่มี)

### หมายเหตุ
- screenshot preview tool ดำเมื่อ scroll — เกิดจาก canvas rAF หลายตัวพร้อมกัน (dc-preview-canvas แต่ละการ์ด) ไม่ใช่ bug — verify ด้วย `preview_eval` แทน

---

## [2026-04-14 — เครื่องที่บ้าน]

### ทำอะไรไปบ้าง

**1. สร้าง Lab 33B — การหักเหของแสง (อากาศสู่แก้ว/ของเหลว)**
- ไฟล์ใหม่: `Virtual Physics Lab 02/33B. light-refraction-glass.html`
- อ้างอิงจากเอกสารการทดลอง "Refraction of Light Waves Traveling from Air to Glass" (ภาพสแกน)
- ใช้โครงสร้างเดียวกับ `32B. light-reflection.html` (single-file, dark theme, 3 tabs)

**ฟีเจอร์หลัก:**
- 3 Tab: การทดลอง | วิธีการทดลอง | ทฤษฎี
- เปลี่ยนจากวัด d/d' (ตามต้นฉบับ) → วัดมุม θ₁, θ₂ ด้วยโปรแทรกเตอร์ 360° (ลาก+หมุนได้)
- **เลือกวัสดุ 8 ชนิด:**
  - กล่องแก้ว: Crown Glass (n=1.52), Flint Glass (n=1.62), Dense Flint (n=1.76), Diamond (n=2.42)
  - กล่องของเหลว: Water (n=1.33), Oil (n=1.47), Glycerol (n=1.47), CS₂ (n=1.63)
  - สีกล่องเปลี่ยนตามวัสดุ + มีเส้นคลื่นสำหรับของเหลว
- **โหมดบันทึกค่าเอง (Manual):** 4 ขั้นตอน — วาง P₁P₂ เหนือแก้ว → วาง P₃P₄ ใต้แก้ว → ดูรังสีหักเห → วัดมุมด้วยโปรแทรกเตอร์
- **โหมดอัตโนมัติ (Auto):** slider ปรับ θ₁ (5°-85°), แสดง Incident/Refracted/Emerging ray + wavefront AB/CD, readout θ₁, θ₂, n, v
- ตารางบันทึกผล: θ₁, θ₂, sinθ₁, sinθ₂, n = sinθ₁/sinθ₂, %Error + export CSV
- กราฟ sinθ₁ vs sinθ₂ (เส้นตรงผ่าน origin ความชัน = 1/n)
- **ทฤษฎี 3 canvas:** (1) Snell's Law diagram, (2) Wavefront + d/d' explanation, (3) Total Internal Reflection 3 scenarios
- ตารางดัชนีหักเหวัสดุ 9 ชนิด พร้อมความเร็วแสงและมุมวิกฤต

**2. รัน protect_new_file.py --scan --fix**
- ไฟล์ใหม่ผ่าน GA, watermark, topbar ครบ

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/33B. light-refraction-glass.html` — สร้างใหม่ทั้งไฟล์

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ commit/push
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ถ้าต้องการ

### หมายเหตุ
- mobile order fix ยังขาดเหมือนไฟล์ VPL02 อื่นๆ ทั้งหมด (ปัญหาเดิมของ protect script)

---

## [2026-04-14 — เครื่องที่บ้าน (session 2)]

### ทำอะไรไปบ้าง

**1. สร้าง Lab 35 — ภาพจากเลนส์นูน (Images and Converging Lenses)**
- ไฟล์ใหม่: `Virtual Physics Lab 02/35. images-converging-lenses.html`
- อ้างอิงจากเอกสาร Experiment 35 (ภาพสแกนใบงาน)
- ใช้โครงสร้าง single-file dark theme เดียวกับ VPL02 อื่นๆ

**ฟีเจอร์หลัก:**
- 3 Tab: 🎬 การทดลอง | 📋 วิธีการทดลอง | 📐 ทฤษฎี
- **Part A: หาความยาวโฟกัส** — รังสีขนาน 5 เส้นจากวัตถุไกล ผ่านเลนส์นูนรวมที่จุดโฟกัส, ลากจอหาตำแหน่งชัด
- **Part B: ศึกษาภาพ** — วัตถุ (ลูกศร), เลนส์, จอ ลากได้บนม้านั่งเชิงแสง, แสดง 3 principal rays (แดง/เขียว/น้ำเงิน)
- **โหมดวัดค่าเอง (Manual, default):** ลากวัตถุ/เลนส์/จอ บน optical bench, อ่านค่าจากสเกล, พิมพ์ลงตาราง, focus indicator (เขียว/เหลือง/แดง) + hint
- **โหมดอัตโนมัติ (Auto):** slider ปรับ d_o (3-80 cm) และ f (5-25 cm), ray diagram + readout อัตโนมัติ, ตารางบันทึก + กราฟ 1/d_o vs 1/d_i
- **Physics engine:** Thin Lens Equation 1/f = 1/d_o + 1/d_i, Magnification M = -d_i/d_o
  - ภาพจริง (d_o > f): 3 rays converge, inverted image
  - ภาพเสมือน (d_o < f): dashed backward extensions, erect enlarged virtual image
  - d_o = f: no image (parallel rays after lens)
- **ตาราง Part A:** 3 trials, X(L), X(c), f = X(c)-X(L), ค่าเฉลี่ย
- **ตาราง Part B:** บันทึก X(O), X(L), X(S), d_o, d_i, f_calc, ภาพ, ขนาด
- **ตาราง Auto:** d_o, d_i, 1/d_o, 1/d_i, M, ชนิดภาพ + export CSV
- **กราฟ Auto:** 1/d_o vs 1/d_i scatter plot พร้อมเส้นทฤษฎี y = -x + 1/f (dashed)
- **ทฤษฎี 3 canvas:**
  1. Ray diagram 3 เส้นหลัก พร้อม labels สี color-coded
  2. 5 กรณีตำแหน่งวัตถุ (d_o > 2f, =2f, f<d_o<2f, =f, <f) พร้อมคำอธิบาย
  3. Thin Lens Equation derivation (similar triangles, d_o/d_i brackets)
- **ตาราง summary:** 5 กรณี — ชนิด, ทิศทาง, ขนาดภาพ

**2. รัน protect_new_file.py --scan --fix**
- ไฟล์ใหม่ผ่าน GA (G-2YTJBNHP6D), KP Topbar, Watermark ครบ

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/35. images-converging-lenses.html` — สร้างใหม่ทั้งไฟล์

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ commit/push
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ถ้าต้องการ

### หมายเหตุ
- mobile order fix ยังขาดเหมือนไฟล์ VPL02 อื่นๆ ทั้งหมด (ปัญหาเดิมของ protect script)
- f default = 10 cm ตรงกับข้อมูลทดลองจากเอกสาร (ค่าเฉลี่ย ~10.20 cm)

---

## [2026-04-14 — เครื่องที่บ้าน (session 3)]

### ทำอะไรไปบ้าง

**1. สร้างหน้าโปรไฟล์สมาชิก (Profile Modal)**
- เพิ่ม tab "โปรไฟล์" ใน `kp-auth-modal` (เป็น tab ที่ 3, ซ่อนไว้ default — แสดงเฉพาะตอนกด profile icon)
- เพิ่มปุ่มไอคอน 👤 ใน topbar (อยู่ใน `#kp-user-menu` ข้างชื่อ user) — คลิกแล้วเปิด profile modal
- สร้างฟังก์ชัน `showProfile()` + `renderProfile()` ใน `kp-auth.js`

**ข้อมูลที่แสดงในโปรไฟล์ (step ก พื้นฐาน):**
- Avatar (จาก `photoURL` ของ Google, ไม่งั้นใช้อักษรแรก)
- ชื่อ + email
- Role badge: สมาชิก / พรีเมียม / ผู้ดูแล / ถูกระงับ (มีสีและ glow ต่างกัน)
- หัวข้อที่เข้าถึงได้ 5 หมวด (กลศาสตร์, คลื่น, ดาราศาสตร์, ไฟฟ้า, อุณหพลศาสตร์) — ✅ ถ้าเข้าได้ / 🔒 ถ้าล็อก
- สถานะลายน้ำ (ซ่อน/แสดง)
- ดาวน์โหลดเดือนนี้ (X / 3 ครั้ง หรือ ไม่จำกัด)
- วันสมัครสมาชิก (จาก `createdAt` Firestore, fallback `auth.metadata.creationTime`)
- ปุ่มออกจากระบบ

**2. แก้ `showModal()` ให้จัดการ tab visibility**
- เปิด login/register → แสดง 2 tab นี้, ซ่อน profile
- เปิด profile → แสดงเฉพาะ profile tab (ซ่อน login/register)

### ไฟล์ที่แก้
- `index.html` — เพิ่มปุ่ม `#kp-profile-btn` ใน topbar, เพิ่ม CSS profile pane, เพิ่ม `<div id="pane-profile">` + `<button id="tab-profile">` ใน modal
- `kp-auth.js` — เพิ่ม `ROLE_LABELS`, `TOPIC_LABELS`, `showProfile()`, `renderProfile()`, แก้ `showModal()`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **ยังใช้งานได้เฉพาะใน `index.html`** — ไฟล์อื่น (library.html, mechanics.html, VPL01/02 ไฟล์ต่างๆ) ยังไม่มีปุ่ม profile
  - ถ้าอยากให้ใช้ได้ทุกหน้า → แก้ `protect_new_file.py` เพิ่ม profile button + pane อัตโนมัติ
- ยังไม่ได้ commit/push
- ฟีเจอร์เสริมที่ค้างไว้ทำทีหลัง (ตามที่ user เลือกข้อ ก):
  - Stats (เวลาใช้งาน, simulations ที่ดู)
  - Favorites/Bookmarks
  - Admin panel (user list, แก้ tier)
  - ปุ่มอัปเกรดเป็น Premium

### หมายเหตุ
- ตัดสินใจไม่ทำระบบคอมเมนต์ (user ถามถึง Giscus/Disqus/Firebase แต่ตัดสินใจไม่ทำ)
- Firebase + Auth + Firestore มีครบอยู่แล้ว (kp-auth.js) — แค่ต่อยอดแสดงผลเฉยๆ
- Profile icon ใช้ SVG inline (stroke-based) — ไม่พึ่ง emoji, render consistent ทุก OS

**3. อัปเดต `_admin/admin.html` — เพิ่ม Lab 33B + Lab 35 ใน LAB_LIST**
- LAB_LIST เดิมขาด lab ใหม่ที่เพิ่งเพิ่มใน session ก่อน → admin ตั้งสิทธิ์ไม่ได้
- เพิ่ม: `lab-33b` (Lab 33B หักเหแสง) หลัง lab-33, `lab-35` (Lab 35 เลนส์นูน) ก่อน lab-37
- ตอนนี้ admin จัดการสิทธิ์เข้าถึง 2 lab ใหม่ใน checkbox ของ modal "แก้ไขสิทธิ์" ได้แล้ว

### ไฟล์ที่แก้ (เพิ่มเติม)
- `_admin/admin.html` — เพิ่ม lab-33b + lab-35 ใน `LAB_LIST` (บรรทัด ~629-630)

**4. เพิ่มกติกาใน `CLAUDE.md` — ซิงก์ไฟล์ใหม่เข้ากับ Admin Panel**
- เพิ่ม section "⚠️ กติกาสำคัญ: ซิงก์ไฟล์ใหม่เข้ากับ Admin Panel" ระหว่าง section "เมื่อเพิ่มไฟล์ HTML ใหม่" กับ "Watermark System"
- ระบุ checklist เมื่อเพิ่ม lab ใหม่: (1) สร้างไฟล์ (2) รัน protect script (3) เพิ่มใน LAB_LIST ของ admin.html (4) ทดสอบ (5) บันทึก log
- ระบุปัญหาที่จะเกิดถ้าลืม: admin ติ๊กสิทธิ์ไม่ได้ + default behavior ที่อาจไม่ตรงเจตนา

### ไฟล์ที่แก้ (เพิ่มเติม)
- `CLAUDE.md` — เพิ่มกติกา "ซิงก์ admin panel ทุกครั้งที่เพิ่ม lab ใหม่"

**5. ปรับโครงสร้างระบบสิทธิ์ (v3) — แทน topics แบบหัวข้อฟิสิกส์ด้วยระบบ Simulation × Source / เอกสาร × Source**

**เหตุผล:** โครงสร้างเดิม (mechanics/waves/astronomy/electricity/thermodynamics) ไม่สะท้อนว่าเนื้อหามาจาก Demo/VPL01/VPL02 จริงๆ และไม่แยกระหว่าง simulation กับ เอกสาร

**โครงสร้างใหม่:**
```
1. 🎬 Simulation
   ├─ sim_demo  (Demo ทุกหัวข้อ)
   ├─ sim_vpl01 (Virtual Lab 01)
   └─ sim_vpl02 (Virtual Lab 02)
2. 📄 เอกสาร
   ├─ doc_vpl01 (Virtual Lab 01)
   └─ doc_vpl02 (Virtual Lab 02)
```

**ไฟล์ที่แก้:**
- `kp-auth.js`:
  - เพิ่ม `ACCESS_CATEGORIES` (โครงสร้าง grouped)
  - `ALL_TOPICS` คำนวณจาก ACCESS_CATEGORIES
  - `DEFAULT_TOPICS` = `['sim_demo']` (เดิม `['mechanics']`)
  - เพิ่ม `LEGACY_TOPIC_MAP` (mechanics→sim_vpl01, waves/astronomy/electricity/thermodynamics→sim_vpl02) เพื่อให้ `data-topic` เก่ายังทำงาน
  - แก้ `applyTopicAccess()` + `showTopicAlert()` ใช้ mapping ใหม่
  - ลบ `TOPIC_LABELS` เดิม (ใช้ ACCESS_CATEGORIES แทน)
  - `renderProfile()` render แบบ grouped (มี group header)
- `index.html`:
  - เพิ่ม CSS `.kp-topic-group`, `.kp-topic-group-head`, tree line ของ `.kp-topic-row`
- `_admin/admin.html`:
  - เพิ่ม `ACCESS_GROUPS` (โครงสร้างใหม่)
  - `TOPIC_LIST` = flat list จาก ACCESS_GROUPS (backward compat)
  - `openTopics()`: default `curTopics` = `['sim_demo']` (เดิม `['mechanics']`)
  - `topics-checkboxes` render แบบ grouped มี group header + สีตาม accent ของกลุ่ม
- `CLAUDE.md`:
  - อัปเดต section "ซิงก์ admin panel" ให้สะท้อน ACCESS_GROUPS แทน TOPIC_LIST เดิม
  - เน้นว่า IDs ใน `ACCESS_GROUPS` (admin) ต้องตรงกับ `ACCESS_CATEGORIES` (kp-auth.js)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **Migration ข้อมูลสมาชิกเดิมใน Firestore:** user เก่าที่มี topics = ['mechanics'] ฯลฯ จะเข้าไม่ได้ตามระบบใหม่ (นอกจาก admin/premium) → admin ต้องเข้า admin panel แล้ว update สิทธิ์ใหม่ทีละคน
- **Data-topic ในไฟล์เก่า:** ยังใช้ชื่อ mechanics/waves/... อยู่ — ทำงานได้ผ่าน LEGACY_TOPIC_MAP แต่ควร migrate เป็น sim_vpl01/sim_vpl02 โดยตรงทีหลัง
- ยังไม่ได้ commit/push

### หมายเหตุ
- ถ้าต้องการเพิ่มหมวดใหม่ในอนาคต (เช่น `exam_vpl01`, `video_youtube`) เพิ่มใน `ACCESS_GROUPS` ของ admin.html + `ACCESS_CATEGORIES` ของ kp-auth.js พร้อมกันเสมอ (IDs ต้องตรงกัน)

**6. Phase 1 Rollout — Access Schema v4 (`category:source:item`)**

เปลี่ยนระบบสิทธิ์จาก v3 (flat `topics: ['sim_vpl01',...]`) → v4 (access strings `['vlab:vpl01:*',...]`) เพื่อรองรับ:
- ✨ Bundle + Per-item ในระบบเดียว (เช่น `vlab:vpl01:*` หรือ `vlab:vpl01:lab-16`)
- 🔜 Phase 2 (exam, examsim) + Phase 3 (course) — ออกแบบ placeholder ไว้ให้เพิ่มได้โดยไม่กระทบ core
- 💳 Per-item purchase — แค่ append access string ตอนชำระเงินเสร็จ
- ⭐ Wildcard (`*` = superuser, `demo:*` = ทั้ง category)

**Phase 1 Categories (active):**
- `demo` × subjects (mechanics/waves/astronomy/electricity/thermodynamics)
- `vlab` × series (vpl01 = lab-1..21, vpl02 = lab-30..37)
- `manual` × series (vpl01/vpl02)

**Phase 2-3 Placeholders (coming soon):**
- `exam`, `examsim` (Phase 2)
- `course` (Phase 3)

**Role Presets:**
```
blocked: []
member:  ['demo:*']
pro:     ['demo:*', 'vlab:vpl01:*', 'manual:vpl01:*']
premium: ['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*', 'manual:vpl01:*', 'manual:vpl02:*', 'exam:*']
ultimate/admin: ['*']
```

**ไฟล์ที่แก้:**
- `kp-auth.js`:
  - เพิ่ม `ACCESS_SCHEMA`, `ROLE_ACCESS_PRESETS`, `VLAB_SERIES`, `LEGACY_TOPIC_MAP` (v1+v2→v4)
  - เพิ่ม `hasAccess(required)`, `migrateAccess(userData)`, `applyAccessControl()`, `renderProfileCategory()`
  - Auto-migrate user data ตอนโหลดจาก Firestore
  - Register/Google sign-in เซฟ `access: ['demo:*']` (v4 primary field)
  - Back-compat: `data-topic` ยังทำงาน, `getUserTopics()`, `applyTopicAccess()` เป็น alias
- `index.html`:
  - เพิ่ม CSS `.kp-coming-soon`, `.kp-topic-detail`, `.kp-group-coming`, `.kp-coming-hint`
- `_admin/admin.html`:
  - Topics Modal UI ใหม่: Quick Presets (Free/Pro/Premium/Ultimate/Blocked) + 3 sections (Demo/VLab/Manual) + Phase 2-3 placeholders
  - Drill-down per-lab (ปุ่ม "▾ เลือกเฉพาะ lab") สำหรับ VLab + Manual
  - `migrateLegacyAccess(m)` — แปลง user เก่า → access array
  - `accessHas()`, `onAccessChange()`, `applyPreset()`, `renderAccessSections()`
  - `saveTopics()` เขียน `access` array + derive `topics`/`labs` legacy fields ไว้ด้วย (back-compat)
- `CLAUDE.md`:
  - เอกสารโครงสร้าง access v4 ฉบับเต็ม (format, categories, role presets, Firestore schema)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **Auto-migration ทั้ง database:** ตอนนี้ migrate แบบ lazy (เฉพาะ user ที่ login/admin เปิด) — ถ้าอยาก migrate บน batch ทั้งหมด ต้องเขียน admin function เพิ่ม
- **หน้าเว็บเก่า** ยังใช้ `data-topic` อยู่ — ยังทำงานผ่าน LEGACY_TOPIC_MAP แต่ควร migrate เป็น `data-access` ทีหลัง
- **Phase 2 (exam, examsim):** placeholder พร้อม — เมื่อมีเนื้อหาจริง ทำแค่:
  1. เปลี่ยน `comingSoon: true` → `false` ใน ACCESS_SCHEMA
  2. เพิ่ม items array (kind: 'bundles' หรือ 'series')
  3. ใส่ `data-access="exam:bundle-id"` บนหน้า
- **Phase 3 (course):** เหมือน Phase 2 แต่เพิ่ม Firestore collection `courses/` + progress tracking
- ยังไม่ได้ commit/push

### หมายเหตุ
- รูปแบบ `category:source:item` ออกแบบให้อ่านง่าย + extensible
- Wildcard `*` รองรับทุกระดับ — `*`, `demo:*`, `vlab:vpl01:*`
- Admin UI มี drill-down button ("▾ เลือกเฉพาะ lab") ซ่อนไว้ default เพื่อ keep UI สะอาด
- เมื่อติ๊ก bundle (`:*`) per-item ใต้มันจะ disable อัตโนมัติ (ป้องกันข้อมูลซ้ำ)

**7. Option C Complete — Page Access Lock (2-layer: UI + Security)**

เพื่อให้สิทธิ์ที่ admin ตั้งไว้ "มีผลจริง" บนหน้าเว็บ — inject 2 ชั้นล็อก:

**ชั้นที่ 1: Link locks (UX)** ใน listing pages
- เพิ่ม `data-locked="true" data-access="vlab:vpl0X:lab-Y"` บนทุกลิงก์ที่ชี้ไปไฟล์ VPL
- `applyAccessControl()` ใน `kp-auth.js` เติม class `.kp-locked` ให้ลิงก์ที่ไม่มีสิทธิ์ → overlay 🔒
- ครอบคลุม: `virtual-physics-lab-01.html` (22), `virtual-physics-lab-02.html` (11), `library.html` (34), `index.html` (10) → รวม 77 ลิงก์

**ชั้นที่ 2: Page-level guard (Security)** ในไฟล์ lab แต่ละตัว
- เพิ่ม `kpPageAccess(required, redirectTo)` ใน `kp-auth.js` — รอ auth state → ถ้า `!hasAccess(required)` → redirect กลับ listing พร้อม `?locked=<access>`
- `_admin/protect_new_file.py` inject ให้อัตโนมัติ
- ครอบคลุม: VPL01 (23 files) + VPL02 (10 files) = 33 ไฟล์

**อัปเดต `protect_new_file.py`:**
- เพิ่ม `LAB_ID_RE` + `extract_lab_id()` + `get_access_string()` → ดึง `lab-X` จากชื่อไฟล์
- เพิ่ม 3 check: `FIREBASE_CDN`, `KP_AUTH`, `ACCESS_GUARD` (เฉพาะไฟล์ VPL01/VPL02)
- เพิ่ม 3 fix: inject Firebase CDN + kp-auth.js + kpPageAccess() script tag
- รองรับไฟล์ VPL02 ที่เดิมไม่มี firebase เลย (ก่อนหน้านี้ topbar login ใช้ไม่ได้)

**ไฟล์ที่แก้:**
- `kp-auth.js` — เพิ่ม `kpPageAccess()` helper
- `_admin/protect_new_file.py` — เพิ่ม 3 check + 3 fix สำหรับ access guard
- `virtual-physics-lab-01.html` — inject 22 link locks
- `virtual-physics-lab-02.html` — inject 11 link locks + เพิ่ม firebase+kp-auth ตอนท้ายหน้า (เดิมไม่มี)
- `library.html` — inject 34 link locks
- `index.html` — inject 10 link locks
- **VPL01 × 23 files** — inject access guard (บางไฟล์เดิมยังขาด firebase+kp-auth ด้วย)
- **VPL02 × 10 files** — inject firebase CDN + kp-auth.js + access guard (เดิมไม่มีเลย)

**Lab-ID extraction:**
- `16. trajectories_simulation.html` → `lab-16` → `vlab:vpl01:lab-16`
- `6.1 pendulum_timer.html` → `lab-6.1` → `vlab:vpl01:lab-6.1`
- `32B. light-reflection.html` → `lab-32b` → `vlab:vpl02:lab-32b`

### ทดสอบ
1. Logout → ไป listing → ลิงก์ VPL ควรมี overlay 🔒
2. Paste URL ตรงเข้า VPL lab → redirect ออกมาพร้อม `?locked=vlab:vpl01:lab-16`
3. Admin ตั้งสิทธิ์ `vlab:vpl01:*` → login → ทุก lab VPL01 ปลดล็อก, VPL02 ยังล็อก
4. Admin ติ๊ก `vlab:vpl01:*` ออก → login ใหม่ → VPL01 ล็อกทันที

### ค้างไว้ที่ไหน / ต้องทำต่อ
- `Demo/` folder ยังไม่มีระบบล็อก (Phase 1 เลือก Demo = free สำหรับทุกคน — ยังไม่ critical)
- ไฟล์ `.html` ทั่วไปที่เป็นหน้า `demo-mechanics.html`, `demo-waves.html` ฯลฯ ยังไม่มี access control — หน้าพวกนี้ควรเปิดฟรีตาม Phase 1 design
- Mobile order fix pre-existing issue — ยังมีใน 46 ไฟล์ (ไม่เกี่ยวกับงานนี้)
- ยังไม่ได้ commit/push

**8. Fix bugs หลัง Option C deploy**

**Bug #1: Lab-id regex จับผิด**
- เดิม `^(\d+(?:\.\d+)?[A-Za-z]?)` → "6.2water" จับเป็น `lab-6.2w` (ติด w)
- แก้เป็น `^(\d+\.\d+|\d+[A-Za-z]?)` → ลอง decimal ก่อน ถ้าไม่ใช่ค่อยจับ integer+letter
- Fix ใน `_admin/protect_new_file.py` LAB_ID_RE
- Fix data-access ผิดใน 3 ไฟล์: `Virtual Physics Lab 01/Mechacnics/6.2water-clock-simulation.html`, `library.html`, `virtual-physics-lab-01.html`

**Bug #2: CSS `.kp-locked` ขาดใน listing pages**
- `index.html` มี CSS overlay `[data-locked="true"].kp-locked::after` แต่ `virtual-physics-lab-01.html`, `virtual-physics-lab-02.html`, `library.html` ไม่มี → `applyAccessControl()` เติม class ได้แต่ไม่แสดง overlay 🔒
- อาการ: user เห็นการ์ดปกติ + badge "FREE" คลิกเข้าได้ (แม้ redirect ออกภายหลังผ่าน page guard)
- แก้: inject CSS เดียวกับ index.html เข้าไปใน 3 ไฟล์ (ก่อน `</style>` ตัวแรก)

### ไฟล์ที่แก้
- `_admin/protect_new_file.py` — LAB_ID_RE regex
- `Virtual Physics Lab 01/Mechacnics/6.2water-clock-simulation.html` — fix access string
- `virtual-physics-lab-01.html` — fix access string + inject CSS
- `virtual-physics-lab-02.html` — inject CSS
- `library.html` — fix access string + inject CSS

### หมายเหตุ
- ตอนนี้ listing pages ทั้ง 4 (index, library, vpl01, vpl02) มี CSS `.kp-locked` ครบ
- Overlay จะแสดง "🔒 สมาชิกเท่านั้น" บนการ์ด lab ที่ user ไม่มีสิทธิ์
- คลิก overlay → เด้ง `showModal('login')` (ตาม `onLockedClick` ใน kp-auth.js ซึ่งเรียก showModal ถ้ายังไม่ login)

**9. Critical Bug Fix — Firebase + kp-auth.js โหลดซ้ำ 2 ครั้ง**

**อาการ:** ระบบ access control (Phase 1 + Option C) ไม่ทำงานเลย — การ์ดไม่แสดง overlay 🔒, user เข้าถึงได้ทุกอย่างแม้ admin remove access

**ต้นเหตุ:** ใน `virtual-physics-lab-01.html` + `library.html` มี "tail block" ที่อยู่**หลัง `</html>`** ซึ่งโหลด firebase + kp-auth.js อีกครั้ง:
```
</body>
</html>

<!-- Firebase + KP Auth -->
<script src=".../firebase-app-compat.js"></script>  ← โหลดซ้ำ!
<script src=".../firebase-auth-compat.js"></script>
<script src=".../firebase-firestore-compat.js"></script>
<script src="kp-auth.js"></script>
<script>/* KP Download Lock */ ... </script>
</body>
</html>
```

**ผลที่เกิด:**
- `firebase.initializeApp()` ถูกเรียก 2 ครั้ง → throw "Firebase App '[DEFAULT]' already exists"
- `kp-auth.js` รันซ้ำ → `const` declarations 2 ครั้ง → SyntaxError "Identifier already declared"
- `onAuthStateChanged` listener ตัวแรก**ไม่ fire** → `applyAccessControl()` + `lockAll()` ไม่เคยถูกเรียก
- การ์ดที่มี `data-locked="true"` ไม่ได้รับ class `.kp-locked` → overlay ไม่แสดง
- Page-level guard ใน lab file ยังทำงาน (ใช้ kp-auth.js รอบเดียว) แต่ UX หลักพัง

**แก้:**
- ลบ "tail block" หลัง `</html>` แรกทั้งหมด
- เก็บ `KP Download Lock` script ไว้ — move มาแทรกก่อน `</body>` ตัวจริง (หลัง kp-auth.js)
- ตอนนี้ Firebase + kp-auth.js โหลด**ครั้งเดียว** + Download Lock script ใช้ firebase auth จาก rounds แรกได้ปกติ

### ไฟล์ที่แก้
- `virtual-physics-lab-01.html` — ลบ duplicate block, merge Download Lock กลับเข้า body
- `library.html` — เหมือน VPL01

### ไฟล์ที่ไม่ได้รับผลกระทบ
- `virtual-physics-lab-02.html` — มี firebase+kp-auth ครั้งเดียว (ผมเพิ่งเพิ่มเข้าไป ไม่มี tail block เดิม)
- `index.html` — มี firebase+kp-auth ครั้งเดียว (ไม่มี tail block)

### บทเรียน
- Protect script ควรเช็คด้วยว่ามี `</html>` ซ้ำหรือ script หลัง `</html>` ไหม
- legacy "KP Download Lock" tail block อาจยังอยู่ในไฟล์อื่นๆ ที่ยังไม่ได้เปิด → scan หาทีหลัง

**10. UX Bug Fix — Admin "ปลด bundle แล้วได้ per-item ครบ" (ตรงข้ามกับที่ตั้งใจ)**

**อาการ:**
- Admin ติ๊ก bundle `Virtual Lab 01` → per-item 23 ตัวถูก disabled+checked (ดู visual ว่ามีสิทธิ์)
- Admin uncheck bundle
- คาดหวัง: สิทธิ์ VPL01 ถูกปลดทั้งหมด
- ของจริง: Save → Firestore ได้ 23 per-item IDs แทน empty → user ยังมีสิทธิ์ทั้ง VPL01!

**Profile ของ user ยืนยัน:** แสดง "23/23 รายการ ✅" ซึ่งตรงกับข้อมูลใน Firestore — ไม่ใช่บั๊กของ profile UI แต่เป็นข้อมูลที่เขียนผิด

**ต้นเหตุ:**
- ใน `renderSeriesSection()` ผม render per-item ด้วย `${bundleChecked?'checked':''}` + `${bundleChecked?'disabled':''}`
- `onAccessChange()` ใช้ `querySelectorAll('input:checked')` → รวม disabled+checked ด้วย
- เมื่อ uncheck bundle → checkbox ที่เคย disabled ยังคง checked ใน DOM → ถูกนับเป็น per-item ที่เลือก → บันทึก 23 IDs

**แก้ (3 จุด):**

1. **`onAccessChange` ใช้ `:checked:not(:disabled)`** — ไม่นับ disabled checkbox
2. **Auto-consolidate ใน `onAccessChange`** — ถ้าผู้ใช้ติ๊ก per-item ครบทั้ง series → แปลงเป็น bundle อัตโนมัติ (เก็บ data clean)
3. **Auto-consolidate ใน `migrateLegacyAccess` (admin) + `migrateAccess` (kp-auth.js)** — user ที่มีข้อมูลผิดพลาดอยู่แล้ว (23 IDs แทน bundle) จะถูก cleanup อัตโนมัติตอนเปิด modal/login ครั้งต่อไป

### ไฟล์ที่แก้
- `_admin/admin.html` — `onAccessChange()` + `migrateLegacyAccess()`
- `kp-auth.js` — `migrateAccess()`

### ผลหลังแก้
- ติ๊ก bundle ON → all per-item = disabled+checked (visual), data = `['vlab:vpl01:*']`
- Uncheck bundle → all per-item = unchecked, data = `[]` (VPL01 ถูกปลด)
- ติ๊ก per-item ทีละตัวจนครบ → auto-consolidate เป็น bundle อัตโนมัติ (data = `['vlab:vpl01:*']`)

**11. Default สำหรับ Anonymous (ยังไม่ login) — ดู Demo + VLab ได้ฟรี ยกเว้นคู่มือ**

**เปลี่ยน strategy:**
- เดิม: ไม่ login → `lockAll()` → ล็อกทุกอย่าง
- ใหม่: ไม่ login → `currentUserData = {role:'anonymous', access:['demo:*','vlab:vpl01:*','vlab:vpl02:*']}` → เข้าได้ Demo+VLab ฟรี

**ไฟล์ที่แก้:**
- `kp-auth.js`:
  - เพิ่ม `ANONYMOUS_ACCESS = ['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*']`
  - `auth.onAuthStateChanged` branch `user=null` → set `currentUserData` เป็น anonymous object + `applyAccessControl()` แทน `lockAll()`
  - `ROLE_ACCESS_PRESETS.member` อัปเดตเป็น `['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*']` (เท่า anonymous)
  - `kpRegister()` + Google sign-in เซฟ topics legacy = `['sim_demo','sim_vpl01','sim_vpl02']`
- `_admin/admin.html`:
  - `ROLE_ACCESS_PRESETS.member` sync เหมือน kp-auth.js
- `CLAUDE.md`:
  - เอกสาร role presets + anonymous default

**UX หลังเปลี่ยน:**
- ⭐ Visitor (ยังไม่ login) เข้า listing VPL01/VPL02 → ไม่มี 🔒 บน lab cards → คลิกเข้าได้เลย
- ⭐ Page-level guard ก็ปล่อยผ่าน (เพราะ anonymous มี `vlab:vpl01:*`)
- 🔒 คู่มือ Lab (manual:*) ยังล็อก → ต้องสมัคร Pro+ ถึงจะดูได้
- 🔜 Phase 2 (exam) + Phase 3 (course) ยังล็อก (ไม่อยู่ใน anonymous list)

**Marketing rationale:** เปิดเนื้อหา sim ให้ลองฟรีทั้งหมด → ดึงดูด user → upgrade เพื่อเข้าถึงคู่มือ + ข้อสอบ

### ค้างไว้ที่ไหน
- ยังไม่ได้ commit/push
- สมาชิกที่สมัครไว้ก่อนอาจมี `access: ['demo:*']` เก่า → ยังต้อง admin เข้าไปอัพเกรด หรือ auto-upgrade script

**12. Admin UI — ตั้งค่าสิทธิ์ Anonymous ได้ (Firestore `settings/public`)**

**เพิ่มความสามารถ:** Admin เปลี่ยนสิทธิ์ anonymous ได้ผ่าน admin panel — ไม่ต้องแก้โค้ด

**Firestore Schema:**
```
settings/public: {
  anonymous_access: ['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*'],
  updated_at: timestamp,
  updated_by: 'admin@email'
}
```

**ไฟล์ที่แก้:**
- `kp-auth.js`:
  - เปลี่ยน `ANONYMOUS_ACCESS` → `ANONYMOUS_ACCESS_FALLBACK` (ใช้เฉพาะเมื่อโหลด Firestore ไม่ได้)
  - เพิ่ม `publicSettings` state + `loadPublicSettings()` + `getAnonymousAccess()`
  - เรียก `loadPublicSettings()` ทันทีที่ script โหลด (parallel กับ auth) + re-apply access ถ้า user ยัง anonymous
- `_admin/admin.html`:
  - เพิ่มการ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" ที่ด้านบน Members tab
  - 4 preset buttons: 🔓 เปิดหมด / 🎬 แค่ Demo / 🎬⚡ Demo+VPL01 / 🚫 ปิด
  - ปุ่ม "⚙️ กำหนดเอง" → เปิด topics-modal ใน `editMode='anonymous'` (reuse UI เดียวกับ user)
  - เพิ่ม state `editMode` + `anonymousAccessCache`
  - functions: `loadAnonymousSettings()`, `renderAnonymousSummary()`, `saveAnonymousAccess()`, `applyAnonymousPreset()`, `openAnonymousSettings()`
  - `saveTopics()` branch: anonymous → write `settings/public`, user → write `users/{uid}` (เดิม)
  - `closeTopics()` reset `editMode = 'user'`
  - `openTopics()` reset `editMode = 'user'` + แสดง watermark section กลับ
  - เพิ่ม `loadAnonymousSettings()` ใน `Promise.all()` ตอน admin login

**⚠️ Firestore Rules ต้องเพิ่ม:**
```js
match /settings/{docId} {
  allow read: if true;
  allow write: if request.auth != null && request.auth.token.email == 'komanepapato@gmail.com';
}
```
(ไม่เพิ่ม → visitors อ่าน settings/public ไม่ได้ → fallback เป็น default hardcoded — ระบบยังใช้ได้แต่ admin แก้ไม่มีผล)

**UX:**
- Admin Panel → Members tab → เห็นการ์ดข้างบน แสดง current summary (เช่น "✅ Demo · ✅ Virtual Lab · 🔒 คู่มือ Lab")
- กด preset → save + update card ทันที + toast แจ้ง
- กด "⚙️ กำหนดเอง" → เปิด modal แบบเดียวกับแก้ user (ไม่มี watermark section)
- Save ใน modal anonymous mode → write `settings/public` แทน `users/{uid}`

### ค้างไว้ที่ไหน
- ⚠️ User ต้องเพิ่ม Firestore rules สำหรับ `settings/{docId}` ก่อน features นี้จะใช้งานได้จริง
- ยังไม่ได้ commit/push

**13. Phase 1 Complete — Demo access control + schema ปรับให้ตรง folder จริง**

**User feedback:** กด "🚫 ปิด" preset → VPL ถูกล็อก แต่ Demo ยังเปิดอยู่ → Demo ไม่มีระบบล็อกเลย

**1. ปรับ `ACCESS_SCHEMA.demo.items` ให้ตรงกับ Demo/ folder จริง**
- เดิม: `mechanics, waves, astronomy, electricity, thermodynamics` (electricity/thermo ไม่มี content จริง)
- ใหม่: `mechanics, waves, astronomy, optics, magnetism` (ตรงตาม folder `Demo/`)
- `LEGACY_TOPIC_MAP` เพิ่ม `optics`, `magnetism` + map legacy `electricity → demo:magnetism`, `thermodynamics → demo:mechanics` (fallback)

**2. Inject `data-locked` + `data-access` บนลิงก์ Demo ทุกหน้า**
- `index.html` — 13 ลิงก์ (Featured Demos 8 + accordion 5)
- `demo-mechanics.html` — 25 ลิงก์
- `demo-waves.html` — 5 ลิงก์
- `demo-optics.html` — 1 ลิงก์
- `demo-magnetism.html` — 1 ลิงก์
- `demo-astronomy.html` — 1 ลิงก์
- `library.html` — 33 ลิงก์
- **รวม:** 79 ลิงก์ Demo ล็อกเพิ่ม

Pattern ของลิงก์ Demo: `href="Demo/<folder>/...html"` → `data-access="demo:<subject>"`
- Thai folder mapping: `mechanics→mechanics, คลื่น→waves, ดาราศาสตร์→astronomy, แสง→optics, แม่เหล็ก→magnetism`

**3. เพิ่ม Firebase + kp-auth.js + CSS lock overlay ใน 5 demo-*.html**
- เดิม: ไม่มี firebase เลย (modal login ใช้ไม่ได้)
- ใหม่: inject firebase CDN 3 ตัว + kp-auth.js + CSS `.kp-locked::after`

**4. Update `_admin/protect_new_file.py` รองรับ Demo**
- `get_access_string()` — map `/Demo/<thai-folder>/` → `demo:<subject>` อัตโนมัติ
- `check_file()` — ตรวจ ACCESS_GUARD ในไฟล์ `/Demo/` ด้วย (เดิมตรวจแค่ VPL)
- `fix_file()` — redirect path สำหรับ Demo ไปที่ `demo-<subject>.html`

**5. รัน `--scan --fix`**
- Inject Firebase + kp-auth + ACCESS_GUARD ให้ Demo files ทุกไฟล์ใน `Demo/mechanics/`, `Demo/คลื่น/`, `Demo/ดาราศาสตร์/`, `Demo/แสง/`, `Demo/แม่เหล็ก/`
- รวม 30+ ไฟล์

### ไฟล์ที่แก้
- `kp-auth.js` — ACCESS_SCHEMA.demo + LEGACY_TOPIC_MAP
- `_admin/admin.html` — ACCESS_SCHEMA.demo
- `_admin/protect_new_file.py` — get_access_string + check_file + fix_file
- `index.html`, `library.html`, 5× demo-*.html — inject link locks + CSS + firebase
- Demo/**/*.html — inject page guards (30+ ไฟล์ผ่าน protect script)

### ผลหลังแก้ (visitor ไม่ login)
- กด "🚫 ปิด" ใน admin → Demo+VLab+Manual ล็อกทั้งหมด ✅
- กด "🎬 แค่ Demo" → Demo เปิด, VLab+Manual ล็อก
- กด "🔓 เปิดหมด" → Demo+VLab เปิด, Manual ล็อก
- กำหนดเอง → แต่ละวิชา Demo เปิด/ปิดแยกได้

### หมายเหตุ
- Demo folder ภาษาไทยมี space/อักขระพิเศษ → protect script handle ได้ (พบใน `กฎนิวตัน`, `โปรเจคไทล์` ฯลฯ)
- Subjects ใน schema ตอนนี้ตรงกับเนื้อหาจริง 5 วิชา (ถ้าเพิ่ม electricity/thermodynamics ในอนาคต แค่เพิ่ม item ใน ACCESS_SCHEMA.demo.items ทั้ง 2 ไฟล์)
