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

