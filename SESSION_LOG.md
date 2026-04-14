# 📋 Session Log — Physics Simulations

> บันทึกงานแต่ละครั้งที่ทำ เพื่อให้ทำงานต่อเนื่องได้ระหว่าง Mac ที่บ้าน ↔ Mac ที่ทำงาน
>
> **กติกา:** เขียน entry ใหม่ต่อท้ายด้านล่าง อย่าลบของเก่า อ่านจากล่างขึ้นบนเพื่อดูสถานะล่าสุด
>
> **Note (2026-04-14):** ประวัติก่อน 4-14 ถูกบีบอัดเป็น timeline เพื่อให้ไฟล์ไม่ใหญ่เกิน — backup เต็มเก็บใน `SESSION_LOG.md.backup` (ไม่ push ขึ้น git)

---

## 📆 Timeline (สรุปย่อ)

### 2026-04-08 (เครื่องที่ทำงาน)
- **Marketing makeover:** `index.html` เป็น Demo Preview Page (8 featured canvas animations + VPL01 section + accordion collections), เปลี่ยน topbar nav, เพิ่ม hero CTAs
- สร้าง `virtual-physics-lab-01.html` (22 VPL labs พร้อม canvas animation + filter chips 6 หมวด)
- สร้าง `library.html` (catalog 38 ไฟล์ + search)
- `mechanics.html` ปลดล็อก password → free preview
- Frame-busting + back button ใน 22 ไฟล์ VPL01/Mechanics
- Fix iOS Safari canvas drift (`2. vector_forces_sim.html`) — debounce resize 150ms
- สร้าง `CLAUDE.md` + `SESSION_LOG.md` (cross-machine sync system)

### 2026-04-09
- เพิ่ม tab "📋 วิธีการทดลอง" ใน 22 ไฟล์ VPL01/Mechanics (child-centered wording, 4 templates: goal → steps → reflection → extension)

### 2026-04-10
- Auth v2.0 Firebase + Firestore (email/password + Google Sign-in)
- Role system: member / premium / admin / blocked
- Download quota (3 ครั้ง/เดือน, admin ตั้ง per-user ได้)

### 2026-04-11
- **Created Lab 30-34, 32B, 32C, 37** (VPL02 Waves & Optics series)
  - Lab 30: Waves on Coiled Spring
  - Lab 31: Waves in Ripple Tank
  - Lab 32: Wave Reflection
  - Lab 32B: Light Reflection
  - Lab 32C: Microwave Reflection
  - Lab 33: Wave Refraction in Ripple Tank
  - Lab 34: Wave Diffraction & Interference
  - Lab 37: Standing Waves
- Auth-aware download buttons (free vs locked)
- Mobile UI fixes (canvas order:-1)
- CTA banner + subtle glass morphism

### 2026-04-12
- Admin panel v1 (`_admin/admin.html`) — member list, topics editor, download log, watermark tier control
- Member CTA banner auto-hide เมื่อ login
- KP Topbar unified across all pages (via `protect_new_file.py`)
- Watermark system (`_shared/watermark.js`) — tier-based unlock via `localStorage.kp_access_tier`

### 2026-04-14 (เครื่องที่บ้าน)

**Session 1: Lab 33B — Light Refraction (air → glass/liquid)**
- File: `Virtual Physics Lab 02/33B. light-refraction-glass.html`
- 3 tabs, 8 materials (Crown/Flint/Diamond/Water/Oil/Glycerol/CS₂), Manual + Auto modes, protractor, Snell's Law graph
- Run protect script ✅

**Session 2: Lab 35 — Converging Lenses**
- File: `Virtual Physics Lab 02/35. images-converging-lenses.html`
- 3 tabs, Part A (focal length) + Part B (image study), Manual + Auto, Thin Lens Equation, ray diagrams, 1/d_o vs 1/d_i graph
- Run protect script ✅

---

## 🎯 2026-04-14 Session 3 — Phase 1 Access Control System (major)

### Summary
Implemented string-based access control system replacing old `topics[]` + `contentTypes[]` + `labs[]` model with unified `access[]` using format `<category>:<source>:<item>` + wildcards.

### Architecture

**Format:**
```
demo:mechanics           — Demo วิชากลศาสตร์
demo:*                   — Demo ทุกวิชา (bundle)
vlab:vpl01:lab-16        — specific lab (per-item for paid access)
vlab:vpl01:*             — ทั้ง series (bundle)
manual:vpl01:*           — คู่มือ VPL01
exam:*, examsim:*        — Phase 2 (placeholder)
course:*                 — Phase 3 (placeholder)
*                        — Superuser (admin)
```

**Categories (`ACCESS_SCHEMA`):**
- `demo` × subjects: mechanics, waves, astronomy, optics, magnetism (ตรงกับ `Demo/` folder)
- `vlab` × series: vpl01 (lab-1..21 incl. 6.1/6.2/6.3) + vpl02 (lab-30,31,32,32b,32c,33,33b,34,35,37)
- `manual` × series: vpl01, vpl02
- Phase 2-3 placeholders: exam, examsim, course (`comingSoon: true`)

**Role Presets (`ROLE_ACCESS_PRESETS`):**
```js
blocked:  []
member:   ['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*']            // = anonymous default
pro:      [+ 'manual:vpl01:*']
premium:  [+ 'manual:vpl02:*', 'exam:*']
ultimate: ['*']
admin:    ['*']
```

### Features Delivered

1. **Profile Modal** (คลิก 👤 ใน topbar ของ `index.html`)
   - Avatar (Google photo หรือ initial letter)
   - Role badge: Member / Pro / Premium / Ultimate / Admin / Blocked (สีต่างกัน)
   - Access list แบบ grouped (Demo by subject, VLab/Manual by series) + count unlocked
   - Watermark status, download quota, join date
   - Logout button
   - ✅ ใช้งานได้ใน `index.html` (ไฟล์อื่นยังไม่มี profile button)

2. **Admin Panel UI overhaul** (`_admin/admin.html`)
   - Quick Presets: Free / Pro / Premium / Ultimate / Blocked
   - 3 Phase-1 sections: Demo (subjects) / VLab (series + drill-down per-lab) / Manual (series + drill-down)
   - Phase 2-3 placeholders (Coming Soon)
   - Auto-consolidate: ติ๊ก per-item ครบ series → แปลงเป็น bundle อัตโนมัติ

3. **Anonymous Settings** (`settings/public.anonymous_access`)
   - Card ที่ top ของ Admin > Members tab
   - 4 presets: 🔓 เปิดหมด / 🎬 แค่ Demo / 🎬⚡ Demo+VPL01 / 🚫 ปิด
   - ⚙️ กำหนดเอง → reuse topics-modal in `editMode='anonymous'`
   - Fallback (ถ้าโหลด Firestore ไม่ได้): `['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*']`

4. **2-Layer Page Lock**
   - **Link lock** (UX): `data-locked="true" data-access="..."` บนลิงก์ → `.kp-locked` overlay 🔒
   - **Page guard** (Security): `kpPageAccess(required, listingUrl)` ต้น lab file → redirect ถ้าไม่มีสิทธิ์
   - Covers: 77 VLab links + 79 Demo links + 33 VPL files + ~30 Demo files

5. **Library Reorganization** (`library.html`)
   - Order ใหม่: 🧪 VIRTUAL LABS (VPL01, VPL02) → 🎬 DEMOS (mechanics, waves, optics, magnetism, astronomy)

### Firestore Schema

```js
users/{uid}: {
  email, role, access: [...], access_tier, createdAt,
  downloadsThisMonth, downloadMonth, downloadYear, downloadQuota,
  // legacy back-compat (derived from access):
  topics: [...], labs: [...]
}
settings/public: {
  anonymous_access: [...],
  updated_at: timestamp,
  updated_by: email
}
```

### Firestore Rules ที่ต้องมี

```js
match /users/{userId} {
  allow read, write: if request.auth.token.email == 'komanepapato@gmail.com';
  allow read, write: if request.auth.uid == userId;
}
match /settings/{docId} {
  allow read: if true;
  allow write: if request.auth.token.email == 'komanepapato@gmail.com';
}
```

### Backward Compatibility
- `LEGACY_TOPIC_MAP` maps v1 topics (mechanics/waves/...) + v2 topics (sim_demo/sim_vpl01/...) → v4 access strings
- `migrateAccess(userData)` runs on every auth load: derives `access[]` from `topics[]` + `labs[]` if missing
- Old `data-topic="mechanics"` attribute still works via mapping

### Critical Bugs Fixed (ในวันนี้)
1. **Firebase + kp-auth.js โหลด 2 รอบ** ใน `virtual-physics-lab-01.html` + `library.html` → SyntaxError → auth ทั้งหมดพัง. แก้: ลบ tail block หลัง `</html>` + merge KP Download Lock กลับเข้าที่
2. **Lab-id regex** `(\d+(?:\.\d+)?[A-Za-z]?)` จับ `6.2w` สำหรับ `6.2water-clock`. แก้: `(\d+\.\d+|\d+[A-Za-z]?)` (decimal ก่อน)
3. **Disabled-checked counted as checked** ใน admin → ปลด bundle แล้วได้ 23 per-item แทน empty. แก้: `:checked:not(:disabled)` + auto-consolidate per-item ครบ series → bundle
4. **Missing `.kp-locked` CSS** ใน listing pages (อยู่แค่ใน `index.html`). แก้: inject CSS ใน `virtual-physics-lab-01/02.html`, `library.html`, 5× `demo-*.html`
5. **Demo ไม่มี access control** — ตอนทำ Option C ผม inject แค่ VPL. แก้: inject `data-access="demo:<subject>"` บนลิงก์ Demo ทุกหน้า + page guard ในไฟล์ `Demo/**/*.html` ผ่าน protect script

### Key Files Modified
- `kp-auth.js` — core access system (ACCESS_SCHEMA, hasAccess, migrateAccess, applyAccessControl, kpPageAccess, showProfile, renderProfile, loadPublicSettings)
- `_admin/admin.html` — Anonymous card + Access modal + ROLE_ACCESS_PRESETS + VLAB_SERIES (sync กับ kp-auth.js) + LAB_LIST เพิ่ม lab-33b, lab-35
- `_admin/protect_new_file.py` — check + fix สำหรับ FIREBASE_CDN, KP_AUTH, ACCESS_GUARD (VPL + Demo), `get_access_string()`, `extract_lab_id()`
- `CLAUDE.md` — docs ทั้งหมดของ v4 system + รูปแบบ access strings + role presets + Firestore schema + rules
- Listing pages: `index.html`, `library.html`, `virtual-physics-lab-01.html`, `virtual-physics-lab-02.html`, 5× `demo-*.html` — ใส่ data-access, CSS lock overlay, firebase CDN (ถ้าขาด)
- VPL01 (23 files) + VPL02 (10 files) + Demo (~30 files) — inject page guards ผ่าน protect script

### ค้าง / ต้องทำต่อ
- 🚨 **Commit + push** — ยังไม่ได้ทำ
- 📝 Profile modal ยังใช้ได้แค่ `index.html` — ถ้าอยากให้ทุกหน้า ต้อง update `protect_new_file.py` inject profile button + pane
- 🔄 Legacy users ใน Firestore ที่มี `topics:['sim_demo']` (v2 preset เก่า) — migrateAccess ทำงานตอน login แต่สิทธิ์จะจำกัดถ้ายังมี topics แบบเก่า ควร run batch upgrade script
- 🎯 Phase 2 (exam, examsim) + Phase 3 (course) — placeholder พร้อม, รอเนื้อหา
- 📱 Mobile order fix ยังขาดใน 46 ไฟล์ (pre-existing issue, protect script ยังไม่มี fix logic)

### Decisions Made (เก็บไว้อ้างอิง)
- ไม่ทำระบบคอมเมนต์ (พิจารณา Giscus/Disqus/Firebase Firestore แล้วตัดสินใจไม่ทำ)
- Anonymous visitors ได้สิทธิ์เท่า member (Demo + VLab, ไม่รวม Manual) — strategy ดึงดูดคนลอง sim ฟรี
- Per-item access เก็บไว้สำหรับ future (บาง lab เก็บเงินแยก) — ใช้ผ่าน `vlab:vpl01:lab-16` format
- Role hierarchy: member → pro → premium → ultimate (เว้นที่ไว้เพิ่ม tier ระหว่างกลางในอนาคต)
