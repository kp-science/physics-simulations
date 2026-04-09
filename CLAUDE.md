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

## 🚫 ข้อห้าม

- อย่าลบ `CLAUDE.md` หรือ `SESSION_LOG.md`
- อย่าเพิ่ม login/password ลงในไฟล์ใดๆ (เจ้าของต้องการเปิด free preview)
- อย่าใส่ iframe ของไฟล์ใน project ให้เว็บอื่น (frame-busting ตั้งไว้แล้ว)
