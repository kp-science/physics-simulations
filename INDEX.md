# 🔭 physics-simulations/ — สาย S3 (Sim Platform)

> **HQ**: [~/Documents/KP-HQ/COMPANY.md](../../KP-HQ/COMPANY.md)
> **CLAUDE.md**: [CLAUDE.md](CLAUDE.md) (อ่าน + อ่าน SESSION_LOG.md ก่อนเริ่มเสมอ)
> **คนดูแล**: ซี (sim) + ปั้บ (backend) · เรียก "ซี ..." / "ปั้บ ..."

## คืออะไร
Platform รวม simulation ฟิสิกส์ HTML+Canvas
มี Firebase auth + GA tracking + hosting พร้อมแล้ว
ใช้ได้ทั้งในห้องเรียน สอนพิเศษ หรือเปิดสาธารณะ

## ของหลัก
- `index.html` — หน้าแรก (Featured Demos + VPL section + Collections)
- `library.html` — รวมทุกไฟล์ + search
- `course.html` / `mechanics.html` — บทเรียนกลศาสตร์
- `Virtual Physics Lab 01/Mechanics/` — 22 sim (frame-busted, มี back button)
- `Virtual Physics Lab 02/` — เพิ่มเติม
- demo files: mechanics, waves, optics, magnetism, astronomy
- `physics-quest/` — link เข้า S4
- `_admin/`, `_marketing/`, `_shared/`

## Backend
- Firebase project: `physics-quest-21336` (Bangkok)
- `firestore.rules` + `firestore.indexes.json`
- `kp-auth.js` — auth flow

## เชื่อมกับสายอื่น
- → **S4** — Physics Quest อยู่ภายใต้ platform เดียวกัน
- → **S7** — ติวเตอร์ส่งลิงก์ sim ให้เด็กทำเป็นการบ้าน
- → **S8** — ติ๊กดูด screen record ทำ TikTok
- → **S6** (อนาคต) — เป็นโครง host ของ Student Hub

## งานค้าง
- ดู `SESSION_LOG.md` (sync 2 เครื่อง)

## Convention บังคับ
- ฟอนต์ Sarabun + Share Tech Mono
- Dark theme: `--bg: #06090f`, `--accent: #38bdf8`
- ทุก HTML ใหม่ใส่ GA tag `G-2YTJBNHP6D` ใต้ `<head>`
- iOS = popup auth · Android Chrome = redirect · in-app browser block

## Workflow
1. เริ่ม session → อ่าน `SESSION_LOG.md` (mandatory)
2. จบ session → append entry ใหม่ลง log
