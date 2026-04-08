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

