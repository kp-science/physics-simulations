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

<!-- ===== entry ใหม่เขียนต่อด้านล่างนี้ ===== -->

---

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

