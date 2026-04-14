# คำสั่งประจำโปรเจกต์ — Physics Simulations (KP Science)

## 📌 อ่านก่อนเริ่มงานทุกครั้ง

โปรเจกต์นี้เจ้าของทำงานสลับกันระหว่าง **2 เครื่อง** (Mac ที่บ้าน กับ Mac ที่ทำงาน) โดยโฟลเดอร์นี้ sync ผ่าน cloud ทั้ง 2 เครื่องเห็นไฟล์เดียวกัน

### ⚡ ขั้นตอนบังคับเมื่อเริ่ม session ใหม่

1. **อ่านไฟล์ `SESSION_LOG.md`** ก่อนทำอะไรทั้งสิ้น — เพื่อรู้ว่างานทำถึงไหนแล้ว เครื่องไหนทำอะไรไว้ มีอะไรค้างอยู่
2. **สรุปสถานะล่าสุด** ให้ผู้ใช้ฟังแบบสั้นๆ 2-3 บรรทัด ว่าครั้งก่อนทำอะไรเสร็จ และกำลังจะทำอะไรต่อ
3. รอคำสั่งจากผู้ใช้ว่าจะทำต่อส่วนไหน

### ⚡ ขั้นตอนบังคับเมื่อจบงาน (ก่อนผู้ใช้ปิด session)

เขียน entry ใหม่ต่อท้าย `SESSION_LOG.md` ตามรูปแบบนี้:

```markdown
## [YYYY-MM-DD HH:MM] — [ชื่อเครื่อง: บ้าน / ที่ทำงาน]

### ทำอะไรไปบ้าง
- ...
- ...

### ไฟล์ที่แก้
- `path/to/file.html` — อะไรที่เปลี่ยน
- ...

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ...

### หมายเหตุ
- (ถ้ามี bug, idea, หรือข้อควรระวัง)
```

**สำคัญ:** entry ใหม่ให้ต่อท้ายไฟล์ (append) — ห้ามลบของเก่า เพราะอีกเครื่องต้องอ่านประวัติ

---

## 📂 โครงสร้างโปรเจกต์ (โดยย่อ)

- `index.html` — หน้าแรก มี Featured Demos (canvas animations) + Virtual Physics Lab 01 section + Collections (accordion)
- `virtual-physics-lab-01.html` — หน้ารวม 22 simulations ของ VPL (ใช้ canvas previews)
- `library.html` — หน้ารวมไฟล์ทั้งหมด มี search
- `mechanics.html` — บทเรียนกลศาสตร์ (ปลดล็อก password แล้ว — free preview)
- `Virtual Physics Lab 01/Mechacnics/` — 22 ไฟล์ simulation (มี frame-busting + back button)

## 🎨 Design tokens

- Font: Sarabun (ไทย) + Share Tech Mono (ตัวเลข)
- Dark theme: bg `#06090f`, accent `#38bdf8` (cyan)
- CSS vars: `--accent`, `--accent2` (purple), `--accent3` (green), `--accent4` (orange), `--accent5` (pink)

## 📊 Google Analytics

**Measurement ID:** `G-2YTJBNHP6D`

**กติกาบังคับ:** ไฟล์ HTML ทุกไฟล์ที่สร้างใหม่หรือแก้ไข ต้องมี GA code นี้อยู่ทันทีหลัง `<head>` เสมอ:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2YTJBNHP6D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-2YTJBNHP6D');
</script>
```

ก่อน commit ไฟล์ใหม่ ให้ verify ว่ามี `G-2YTJBNHP6D` อยู่ในไฟล์ด้วยทุกครั้ง

---

## 🛡️ เมื่อเพิ่มไฟล์ HTML ใหม่

**บังคับ:** ทุกครั้งที่สร้างหรือเพิ่มไฟล์ HTML ใหม่เข้าโปรเจกต์ ต้องรันสคริปต์นี้:

```bash
python3 _admin/protect_new_file.py ชื่อไฟล์.html
```

หรือสแกน + แก้ทั้งโปรเจกต์:

```bash
python3 _admin/protect_new_file.py --scan --fix
```

สคริปต์จะเพิ่มให้อัตโนมัติ:
1. Google Analytics (`G-2YTJBNHP6D`)
2. Frame protection (ป้องกัน iframe)
3. Domain protection (เฉพาะ Demo/)
4. KP Topbar (nav bar + login)
5. Mobile layout fix
6. แก้ escaped comments
7. Watermark overlay (เฉพาะ VPL01 + VPL02)

**ถ้าผู้ใช้สั่ง "protect ไฟล์ใหม่"** → รัน `python3 _admin/protect_new_file.py --scan --fix`

---

## ⚠️ กติกาสำคัญ: ซิงก์ไฟล์ใหม่เข้ากับ Admin Panel

**เมื่อเพิ่ม/แก้ไข/ลบ lab หรือ simulation** ใน VPL01/VPL02 → **ต้องอัปเดต `_admin/admin.html` ด้วยเสมอ**

ใน `_admin/admin.html` มี list ที่ admin ใช้เซ็ตสิทธิ์สมาชิก:
- **`LAB_LIST`** (ประมาณบรรทัด ~618) — รายชื่อ lab ทั้งหมดที่ admin ติ๊กอนุญาต/ปฏิเสธให้สมาชิกแต่ละคนได้
- **`TOPIC_LIST`** — หัวข้อ (mechanics, waves, astronomy, electricity, thermodynamics)
- **`CONTENT_TYPES`** — ประเภทเนื้อหา (simulation, lab_manual, exam)

### ✅ Checklist เมื่อเพิ่ม lab ใหม่

- [ ] สร้างไฟล์ `.html` ใน VPL01/Mechacnics หรือ VPL02
- [ ] รัน `python3 _admin/protect_new_file.py --scan --fix`
- [ ] **เพิ่ม entry ใหม่ใน `LAB_LIST` ของ `_admin/admin.html`** (format: `{id:'lab-XX',label:'Lab XX (ชื่อ)'}`)
  - จัดเรียงตามเลข lab (lab-33 → lab-33b → lab-34 → lab-35 → lab-37 ฯลฯ)
  - `id` ใช้ตัวพิมพ์เล็กเสมอ (เช่น `lab-33b` ไม่ใช่ `lab-33B`)
- [ ] ทดสอบเปิด admin panel → แก้ไขสิทธิ์สมาชิก → ดูว่า checkbox lab ใหม่ขึ้นถูกต้อง
- [ ] บันทึกใน `SESSION_LOG.md` ว่าได้แก้ `_admin/admin.html` ด้วย

### ❌ ถ้าลืม

- Admin จะ**ติ๊กสิทธิ์ lab ใหม่ไม่ได้** → สมาชิกอาจเข้าถึงหรือถูกบล็อกผิด
- สิทธิ์ default `curLabs = m.labs || LAB_LIST.map(l=>l.id)` จะให้ lab ใหม่แก่ทุกคนโดยอัตโนมัติ (อาจไม่ตรงเจตนา)

---

## 🔒 Watermark System

ไฟล์ simulation ทุกไฟล์ใน VPL01 + VPL02 มีลายน้ำ "KP Science" แสดงบน canvas

**โครงสร้าง:**
- `_shared/watermark.js` — โมดูลลายน้ำ (overlay canvas, ไม่แตะ logic ของ simulation)
- `protect_new_file.py` — inject `<script src="...watermark.js">` อัตโนมัติเมื่อรัน `--scan --fix`

**การปลดล็อก (ซ่อนลายน้ำ):**
```js
// ระบบ login/admin เซ็ตค่านี้เมื่อผู้ใช้มีสิทธิ์
localStorage.setItem('kp_access_tier', 'pro');   // tier: pro, premium, admin
KPWatermark.check();  // ตรวจสิทธิ์แล้วซ่อนอัตโนมัติ

// เมื่อ logout
localStorage.removeItem('kp_access_tier');
KPWatermark.show();   // ลายน้ำกลับมา
```

**API:**
- `KPWatermark.remove()` — ซ่อนลายน้ำทันที
- `KPWatermark.show()` — แสดงลายน้ำ
- `KPWatermark.check()` — ตรวจ localStorage แล้วซ่อน/แสดงอัตโนมัติ

**หมายเหตุ:** ลายน้ำ sync ข้ามแท็บผ่าน `storage` event — login แท็บหนึ่ง ลายน้ำหายทุกแท็บ

---

## 🚫 ข้อห้าม

- อย่าลบ `CLAUDE.md` หรือ `SESSION_LOG.md`
- อย่าเพิ่ม login/password ลงในไฟล์ใดๆ (เจ้าของต้องการเปิด free preview)
- อย่าใส่ iframe ของไฟล์ใน project ให้เว็บอื่น (frame-busting ตั้งไว้แล้ว)
