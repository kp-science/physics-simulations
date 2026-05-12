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

---

## [2026-04-15] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง Lab 36 — Images and Diverging Lenses (ภาพจากเลนส์เว้า)
  - 3 tabs: การทดลอง / วิธีการทดลอง / ทฤษฎี
  - **Part A (หาโฟกัสเลนส์เว้า):** laser + เลนส์เว้า + กระดาษ, วัด D ที่ระยะ X ต่างๆ, plot กราฟ D vs X, linear fit + extrapolate หา x-intercept = −|f|
  - **Part B (กล้องกาลิเลโอ):** เลนส์นูน F₁ + เลนส์เว้า F₂, ระยะ L = F₁+F₂, M = −F₁/F₂ (+, ตั้งตรง), inset "มุมมองผ่านกล้อง" แสดงต้นไม้ขยาย
  - Manual mode (default): สุ่มเลนส์ใหม่, ลากอุปกรณ์, ไม้บรรทัด ↔/↕, กรอก X,D หรือ F₁,F₂ เข้าตาราง
  - Auto mode: sliders (f, D₀, X สำหรับ A; F₁, F₂ สำหรับ B), รัศมีวงแสง/กำลังขยายคำนวณสด
  - 5 theory canvases: รังสี 3 เส้นผ่านเลนส์เว้า, ภาพ 3 กรณี, สมการเลนส์บาง, วิธีวัดด้วยลำแสง (สามเหลี่ยมคล้าย), กล้องกาลิเลโอ
- Run protect script — สคริปต์แก้ MOBILE issue ให้อัตโนมัติ (GA + topbar + watermark อยู่แล้ว)
- Sync lab-36 เข้า `kp-auth.js` (VLAB_SERIES.vpl02) และ `_admin/admin.html` (VLAB_SERIES + LAB_LIST)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/36. images-diverging-lenses.html` — ไฟล์ใหม่ (~1500 บรรทัด)
- `kp-auth.js` — เพิ่ม `'lab-36'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-36'` ใน vpl02.labs + entry `{id:'lab-36',label:'Lab 36 (เลนส์เว้า)'}` ใน LAB_LIST

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม canvas preview ใน `virtual-physics-lab-02.html` สำหรับ Lab 36 (ถ้าหน้านั้นมี grid)
- ยังไม่ได้ push ขึ้น git

### หมายเหตุ
- อ้างอิงข้อมูลจริงจาก reference sheet ในคำสั่ง (X=5,10,20,30,40,50,60 cm → D=1.3,2.3,4.7,8.0,11.0,13.1,16.4 cm)
- Physics: D(X) = D₀·(|f|+X)/|f| → linear, slope=D₀/|f|, x-intercept=−|f|
- Galileo telescope: M=−F₁/F₂ (+, erect), L=F₁+F₂ (shorter than Keplerian)
- ใช้ Lab 35 เป็น template หลัก (colors flipped: accent=purple สำหรับเลนส์เว้า, accent2=cyan สำหรับเลนส์นูน)

---

## [2026-04-16] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง **Lab 38 — Wave Speed on a String (ความเร็วคลื่นในเส้นเชือก)**
  - 3 tabs: การทดลอง / วิธีการทดลอง / ทฤษฎี
  - **4 การทดลองย่อย** (sub-nav ภายใน tab simulation):
    1. **วัด v จากระยะทาง (v = Δx/Δt):** พัลส์/คลื่นต่อเนื่อง, timer + marker บน ruler, กรอก Δx
    2. **วัด v จาก λ (v = fλ):** ปรับ f, freeze คลื่น, วัด λ จาก ruler
    3. **วัดคาบ:** สุ่ม f,v ให้, วางจุดวัดบนเชือก (SHM), จับเวลา + นับรอบ
    4. **วัดความถี่:** เส้นอ้างอิง, ตั้งเวลาจับ, เฟสซ้ำกระพริบ, นับรอบ → f = n/t
  - **Manual mode (default):** ฝึกทักษะการวัด — กรอกค่าเอง
  - **Auto mode:** โปรแกรมบันทึกอัตโนมัติ
  - ตัวแปร: T (แรงดึง), μ (ความหนาแน่นเชิงเส้น), A (แอมพลิจูด), f (ความถี่), damping, ปลายตรึง/อิสระ/ไม่สะท้อน
  - ทุก experiment มี: ตารางบันทึก, %Error เทียบค่าจริง, Export CSV
  - Tab ทฤษฎี: 3 theory canvases (v vs T/μ graph, f-λ comparison, reflection types)
  - Tab วิธีการทดลอง: 4 method cards พร้อม tips + warnings
- Run protect script ✅ (TOPBAR, WATERMARK, FIREBASE_CDN, KP_AUTH, ACCESS_GUARD)
- Sync lab-38 เข้า `kp-auth.js` (VLAB_SERIES.vpl02) และ `_admin/admin.html` (VLAB_SERIES + LAB_LIST)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/38. wave-speed-on-string.html` — ไฟล์ใหม่ (~1400+ บรรทัด)
- `kp-auth.js` — เพิ่ม `'lab-38'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-38'` ใน vpl02.labs + entry `{id:'lab-38',label:'Lab 38 (ความเร็วคลื่นในเชือก)'}` ใน LAB_LIST

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม canvas preview ใน `virtual-physics-lab-02.html` สำหรับ Lab 38
- ยังไม่ได้ push ขึ้น git
- อาจเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ภายหลัง

### หมายเหตุ
- Physics: v = √(T/μ), v = fλ, T_period = 1/f
- อ้างอิง: Halliday, Resnick & Krane Ch.16 + หลักสูตรแกนกลาง 2551
- ใช้ accent=purple (คลื่น) ตาม VPL02 theme

---

## [2026-04-17 — เครื่องที่ทำงาน] Lab 39 · Phase · Circle · y-t · y-x

### ทำอะไรไปบ้าง
- สร้าง Lab 39 คู่กับ POE-03 แผน 3 (คลื่นดล/ต่อเนื่อง/เฟส) ครอบคลุม 3 ฐาน (Slinky / Strobe / Sim)
- 3 tabs: Simulation, วิธีการทดลอง+บันทึกผล, ทฤษฎี
- Canvas แบ่ง 3 โซน: Phasor (ซ้ายบน) · y-t graph (ขวาบน) · y-x wave strip (ล่าง)
- 3 โหมดการทดลอง A/B/C:
  - A: Pulse (gaussian แดง) vs Continuous (น้ำเงิน) — แสดงว่า v เท่ากัน
  - B: ริบบิ้น 4 เส้นที่ Δx = λ/4, λ/2, 3λ/4, λ — Δφ จุดละ
  - C: Cursor คลิก canvas + slider Δφ คลื่น 2 + ผลรวม superposition
- Manual (default) + Auto mode · ตาราง + CSV export + Snap ตรวจคำตอบ ✓/✗
- Theory tab: วิชวลวงกลม→ภาพฉาย, phasor↔ribbon, superposition cycle
- Run `protect_new_file.py` ✅ (GA + topbar + watermark + firebase)
- Sync LAB_LIST + VLAB_SERIES vpl02 ใน `_admin/admin.html` และ `kp-auth.js` (เพิ่ม lab-39)
- Preview verified: Δφ=180° → ผลรวมแบน y=0 ✓, λ→A_total=2.00A ✓

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/39. phase-circle-wave.html` — ไฟล์ใหม่ (สิมฯ หลัก)
- `_admin/admin.html` — เพิ่ม lab-39 ใน VLAB_SERIES.vpl02.labs + LAB_LIST
- `kp-auth.js` — เพิ่ม lab-39 ใน VLAB_SERIES.vpl02.labs

### ค้างไว้ที่ไหน / ต้องทำต่อ
- พิจารณาเพิ่มลิงก์ Lab 39 ใน `index.html` + `virtual-physics-lab-01.html` (ถ้าต้องการ feature)
- ถาม user ว่าต้องการเพิ่ม Part 1 (POE tab) หรือ Part 3 (แบบฝึกหัด tab) ไหม

### หมายเหตุ
- Source file POE-03: `~/Documents/วิจัย/wave-mechanics-research/lessons/physics3/waves/แผน03_.../สื่อ02_POE-03_ใบบันทึกPOE.html`
- Physics formula: Δφ = 2π(Δx/λ) · A_total = 2A|cos(Δφ/2)| · v = fλ = √(T/μ)
- Misconceptions target: M3.1/M3.2/M3.3/M3.4

## [2026-04-17 update] Lab 39 · ปรับฐาน A ให้ใช้ 2 จอ + Timer + Caliper

### ทำอะไรไปบ้าง
- รื้อฐาน A ใหม่ตามคำสั่ง: เอาวงกลม phasor ออก · ใช้ layout 2 จอ (บน=Pulse, ล่าง=Continuous)
- เพิ่ม workflow: 🚀 ปล่อย → ⏱ เริ่ม/หยุด → freeze → ลากคาลิปเปอร์จอล่างวัด λ → 💾 บันทึก
- 2 ตารางแยก (ดล / ต่อเนื่อง) + row เปรียบเทียบ |Δv| และ %
- Manual: โปรแกรมเก็บ Δt, นักเรียนกรอก d, λ เอง | Auto: เติมค่าให้ครบ
- Caliper auto-วางที่สัน 2 ลูกติดกันตอน freeze + drag ได้ (mouse + touch)
- ฐาน B/C ไม่ได้ยุ่ง (ยังใช้ phasor+y-t+y-x เดิม)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/39. phase-circle-wave.html` — เพิ่ม drawExpA, drawPulsePanel, drawContinuousPanel, renderTableA, releasePulse, toggleTimerA, savePulse/ContinuousRecord, caliper drag handlers

### Verification
- Preview test: auto mode · v_pulse = v_cont = 1.000 m/s, diff = 0.0% ✓

## [2026-04-17 — เครื่องที่ทำงาน] Lab 40 · Pulse Superposition

### ทำอะไรไปบ้าง
- สร้าง **Lab 40 — การซ้อนทับของคลื่นดล (Pulse Superposition)**
- 3 tabs: การทดลอง / วิธีการทดลอง / ทฤษฎี
- คลื่นดล 2 ลูกสวนทาง: เลือกรูปร่างได้ 6 แบบ (สามเหลี่ยม / สี่เหลี่ยม / Gaussian / ครึ่งวงกลม / ฟันเลื่อย / S-bipolar) อิสระต่อกัน
- **2 โหมดการเคลื่อนที่:**
  - ▶ ปล่อยอัตโนมัติ: v₁=+2, v₂=−2 m/s
  - ✋ ลากเอง: จับวงกลมส้ม/ฟ้าบน canvas ลากเข้าหากัน → เห็นการซ้อนทับสด ๆ (รองรับ touch)
- **2 โหมดบันทึก:**
  - บันทึกเอง (default): นักเรียนกรอก y รวม → ระบบเทียบ %ผิดกับ y₁+y₂ ทาง ทษ.
  - บันทึกอัตโนมัติ: เติมค่าครบ
- Probe (หมุดวัด): คลิกบนเชือกปักจุด แสดง y₁/y₂/y_sum สด
- Timeline scrubber 0–6 s + ปุ่มลัด ก่อนพบ/ขณะพบ/หลังพ้น (คำนวณ meet time จาก x1,x2,v อัตโนมัติ)
- 4 Presets: ยอด+ยอด · ยอด+ท้อง · A ต่าง · รูปต่างกัน · URL `?preset=...` รองรับ
- Toggle "แสดงเฉพาะคลื่นรวม" + Speed slider 0.25–2× + Screenshot (PNG) + Export CSV
- Tab ทฤษฎี: 3 visual canvases (superposition, before/during/after, phase circle ↔ y-t link to Lab 39)
- ชน Misconception M4.1–M4.4 (รูปคืน, หักล้างถาวร, ลูกใหญ่กินลูกเล็ก, รูปต่างบวกไม่ได้)
- Run protect script ✅ (GA + topbar + watermark + firebase + access guard)
- Sync lab-40 ใน `kp-auth.js` (vpl02.labs) + `_admin/admin.html` (VLAB_SERIES + LAB_LIST)

### Verification (preview)
- crest+crest → sum=6.00 cm ✓ ที่ meet time t=3.00s
- crest+trough → sum=0.00 cm ✓
- mixed (triangle 4 + square 3) → drag overlap sum=7.00 cm ✓
- ไม่มี console errors

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/40. pulse-superposition.html` — ไฟล์ใหม่ (~750+ บรรทัด)
- `kp-auth.js` — เพิ่ม `'lab-40'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-40'` ใน vpl02.labs + entry `{id:'lab-40',label:'Lab 40 (การซ้อนทับคลื่นดล)'}` ใน LAB_LIST

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม canvas preview ใน `virtual-physics-lab-02.html` สำหรับ Lab 40
- ยังไม่ได้ push ขึ้น git
- ถาม user ว่าต้องการเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ไหม

### หมายเหตุ
- Reference: `pulse-superposition.html` spec (canvas 0-20m × ±10cm, grid 1m×1cm, baseline dashed)
- Physics: y(x,t) = y₁(x,t) + y₂(x,t) — algebraic, no dispersion
- ใช้ accent=purple (#818cf8) สำหรับธีม + accent2=orange (pulse 1), accent3=cyan (pulse 2), accent4=yellow (sum)
- เชื่อมกับ Lab 39 ในแท็บทฤษฎี: pulse ไม่มีเฟส ↔ continuous wave มีเฟส (วงกลม → y-t projection)

## [2026-04-17 update 2] Lab 40 · เพิ่มลิงก์/การ์ดทุกหน้า

### ทำอะไรไปบ้าง
- เพิ่มการ์ด Lab 40 ใน 3 หน้า + canvas preview animation (`vpl2-superpose`)
  - **virtual-physics-lab-02.html** — เพิ่มการ์ดต่อจาก Lab 39 ในหมวด "คลื่นกล" (count 6→7), inject preview drawer
  - **library.html** — เพิ่ม lib-item ต่อจาก Lab 39 (count 11→12)
  - **index.html** — เพิ่มการ์ดต่อจาก Lab 36 (CTA link 12→13), inject preview drawer
- Preview animation: คลื่นดล Gaussian 2 ลูก (สีส้ม + ฟ้า) วิ่งสวนทางเข้าหากัน · เส้นซ้อนทับสีเหลืองหนาแสดงผลรวม
- Verified ใน preview: card ปรากฏใน parent section "คลื่นกล" ✓ canvas animation render ได้ ✓ ไม่มี console errors

### ไฟล์ที่แก้
- `virtual-physics-lab-02.html` — เพิ่มการ์ด + preview function + count
- `library.html` — เพิ่ม lib-item + count
- `index.html` — เพิ่มการ์ด + preview function + CTA count

---

## [2026-04-17 23:15] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง **Demo: หลักของฮอยเกนส์ (Huygens' Principle)** — `Demo/คลื่น/huygens-principle-demo.html`
- เป็น Demo (ไม่ใช่ Lab) เน้น 2 ประเด็น: (1) ทุกจุดบนหน้าคลื่นเป็นแหล่งกำเนิด wavelet วงกลม (2) คลื่นทุกชนิด (น้ำ/เสียง/แสง) เป็นไปตามหลักเดียวกัน
- 2 tabs: 🎬 Demo + 📐 ทฤษฎี (มี SVG อธิบายภาพ + 4 tile เชื่อมไปสู่ diffraction/refraction/reflection/interference)
- Features: 3 ชนิดหน้าคลื่นเริ่มต้น (ระนาบ/วงกลม/เอียง 30°) · 3 ชนิดคลื่น (เปลี่ยนสี) · slider λ/Δt/N · barrier toggle + d · click-to-add source · auto-place · envelope rendering · animation · 3 preset (กว้าง/แคบ/ไม่มี barrier)
- Verified preview ใช้ได้: plane mode = envelope ขนานเดิม · narrow slit (d=1m, λ=1m) = envelope วงกลม (เลี้ยวเบน)

### ไฟล์ที่แก้
- `Demo/คลื่น/huygens-principle-demo.html` — สร้างใหม่
- `_admin/protect_new_file.py` รัน → inject GA, frame protection, KP topbar, watermark, Firebase, kp-auth, access guard เรียบร้อย

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ลิงก์เข้า `Demo/index.html` หรือ `library.html` หรือหน้า VPL02 (hook section) — ถ้าต้องการให้ขึ้นแคตาล็อกต้องเพิ่ม card
- ไม่ใช่ Lab ที่ต้องเก็บ access string ใน `_admin/admin.html` (อยู่ใน Demo/ → ใช้ access `demo:waves` อัตโนมัติ)

### หมายเหตุ
- v = 2 m/s คงที่เพื่อให้สื่อสาร Δt เป็นวินาที + รัศมีเป็นเมตรอ่านง่าย
- envelope rendering: sample 180 angle/source → keep points ที่ไม่อยู่ใน circle ของ source อื่น → วาดเป็น arc ด้วยการ group contiguous angles
- ผู้ใช้บอกชัดว่า "เป็นเดโม ไม่ต้องวัด" → ตัด tab "วิธีการทดลอง/บันทึกผล" ออก เหลือแค่ 2 tabs

## [2026-04-18] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง **Lab 41 — การแทรกสอดของคลื่นผิวน้ำ (Two-Source Interference)**
- 3 tabs: การทดลอง / วิธีการทดลอง+บันทึกผล / ทฤษฎี
- แหล่งกำเนิด 2 แบบ: (1) ช่องแคบคู่ (in-phase เสมอ) (2) จุดสั่น 2 อัน เลือกเฟสตรงกัน/ตรงข้ามได้
- ปรับได้: d (2-10 cm), f (4-20 Hz), v (10-40 cm/s) + ปุ่ม 🎲 สุ่ม v ซ่อนค่าจริง
- Wave rendering: ImageData 280×168 grid, Σ cos(kr−ωt) กับ causality (คลื่นยังไม่ถึงจุดไม่มี amp)
- **การทดลอง 1 (Path diff):** คลิก P → แสดง S₁P, S₂P, Δr → เลือกชนิด/n → λ = Δr/div
- **การทดลอง 2 (มุม θ):** ไม้โปรแทกเตอร์วงกลม centered ที่ M → นักเรียนอ่านมุมกรอก → λ = d·sinθ/div
- Hint toggle: วาด hyperbola (Δr=mλ) เขียว=ปฏิบัพ, ฟ้าประ=บัพ (สลับเมื่อ anti-phase)
- 2 โหมดบันทึก: บันทึกเอง (default) / อัตโนมัติ (autoFill: A₁,A₂,A₃,N₁,N₂)
- ตาราง + CSV export + summary (mean, SD, %error เทียบ λ จริง)
- Tab ทฤษฎี: canvas 3 รูป (superposition, interference pattern, far-field geometry d·sinθ)

### Verification (preview)
- autoFill1 + autoFill2 ที่ d=5cm, f=10Hz, v=22cm/s → λ_exp = 2.20 cm ทุกจุด = λ_true ✓
- ไม่มี console errors
- Pattern แสดงผลถูกต้อง (ช่องแคบคู่ + barrier) · theory canvases render ครบ

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/41. wave-interference-two-source.html` — ไฟล์ใหม่
- รัน `protect_new_file.py` ✅ (GA + topbar + watermark + firebase + access guard)
- `kp-auth.js` — เพิ่ม `'lab-41'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-41'` ใน VLAB_SERIES + entry `{id:'lab-41',label:'Lab 41 (การแทรกสอดคลื่นผิวน้ำ)'}` ใน LAB_LIST

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม card + canvas preview ใน `virtual-physics-lab-02.html`, `library.html`, `index.html` สำหรับ Lab 41
- ยังไม่ได้ push git
- ถาม user: ต้องการเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ไหม?

### หมายเหตุ
- Physics: in-phase → Δr=nλ (A), (n-½)λ (N) · anti-phase → สลับ
- Far-field: d sinθ = nλ (antinode, in-phase)
- Coord: sources on vertical line x=5cm, y=±d/2 · central axis = +x direction · angle from M relative to +x
- Wave colormap: blue-cyan-white gradient (0-255 mapping from u∈[-2,2])
- Hyperbola hint: y=sign·a·cosh(t), x=xM+b·sinh(t), a=|m|λ/2, b=√(c²-a²)

## [2026-04-18 update 2] Lab 41 · เพิ่มโหมดช่องแคบเดียว

### ทำอะไรไปบ้าง
- เพิ่มโหมดที่ 3: **ช่องแคบเดียว (Single-slit diffraction)** ในปุ่ม source-type toggle
- สูตรการเลี้ยวเบน: minima (บัพ) a sinθ = nλ · secondary maxima (ปฏิบัพ) a sinθ ≈ (n+½)λ
- Rendering: sum ของ Huygens wavelets N=12 ตัวข้าม slit width (ใช้ sR·cos(ωt) + sI·sin(ωt) optimization)
- Barrier เปลี่ยนจาก 2 ช่อง → 1 ช่องกว้าง a · labels เปลี่ยนเป็น "บน/ล่าง" แทน S₁/S₂
- Slider label เปลี่ยน dynamic: d ↔ a · hint hyperbolae ปรับใหม่ (dark=nλ, bright=n+0.5 λ)
- `getDiv()` + `mDiffFor()` helpers จัดการสูตรตาม source type อัตโนมัติ
- Alert n=0 ใน single-slit (central max คำนวณ λ ไม่ได้)
- Theory tab: เพิ่มหัวข้อ 7 "ช่องแคบเดียว — การเลี้ยวเบน" (Huygens wavelet analysis, เปรียบเทียบกับช่องแคบคู่, ความกว้าง central max)
- Procedure tab: เพิ่มการทดลองที่ 3 (single-slit) — 6 ขั้นตอน + hints

### Verification
- autoFill1 + autoFill2 ใน single-slit mode (a=5cm, f=10Hz, v=22cm/s → λ=2.2cm)
- ทุก λ_exp = 2.200 cm = λ_true ✓ (A1, N1, N2 ใน table 1 · A1, N1, N2 ใน table 2)
- Angles ถูกต้อง: N1 sinθ=λ/a=0.44 → 26.1° ✓ · N2 sinθ=0.88 → 61.6° ✓ · A1 sinθ=(1+0.5)·0.44=0.66 → 41.3° ✓
- Pattern render: central max กว้าง + diffraction fringes ข้าง ๆ ดูถูกต้อง
- ไม่มี console errors

## [2026-04-26] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- ย้ายไฟล์ `SHM01_SHM-Identifier_protected.html` จาก `Virtual Physics Lab 02/` → `Demo/`
- รัน `python3 _admin/protect_new_file.py Demo/SHM01_SHM-Identifier_protected.html` → injection: GA, DOMAIN, TOPBAR, MOBILE, WATERMARK, FIREBASE_CDN, KP_AUTH, ACCESS_GUARD ครบ
- Verify: GA `G-2YTJBNHP6D` ✓ · firebase ✓ · kp-topbar ✓ · watermark.js ✓ (ไม่มี duplicate injection)

### ไฟล์ที่แก้
- `Demo/mechanics/SHM/SHM01_SHM-Identifier_protected.html` — ไฟล์ใหม่ (ย้ายจาก VPL02 → Demo/mechanics/SHM/ + protect)
- QA graphic + ปรับ CSS ในไฟล์เดิม:
  - แก้ bug: `#tab-sim` แสดงตลอดเวลา (ID specificity beat `.tab-section{display:none}`) → เปลี่ยนเป็น `#tab-sim.tab-section.active{...}`
  - เพิ่ม height calc ให้รวม KP topbar (110→178px) + `min-height:560px`
  - Cap `.canvas-wrap{max-height:520px}` (เดิมยืดถึง ~819px ทำให้ pendulum/canvas ใหญ่เกิน)
  - เพิ่ม media query 820px (stack canvas + graph-panel แนวตั้ง, slider 50%) + 480px (slider 100%)
- Verified ใน preview: ทั้ง 6 scenario + 3 tab ทำงาน · graphs F-x/x-t/v-t วาดถูก (linear / sin / cos shifted) · ไม่มี console errors
- แก้สูตร scale ใน `drawPendulum` (decode base64 JS → patch → re-encode): เปลี่ยนจาก `min(H-80,W*0.4)/A` (ผกผันกับ A → เชือกยาวเกินกรอบเมื่อ A เล็ก) เป็น `pxPerM = min((H-rootY-40)/Lmax, (W*0.45)/A)` ทำให้ L=2.5m (max) พอดีกรอบ 520px ไม่ล้น
- เขียน `drawConicalPendulum` ใหม่เป็นกรวย 3D: cone outline + orbit ellipse แบ่ง front (solid)/back (dashed) + bob ขนาด/glow ตามความลึก + axis dashed + pivot fixture + centripetal arrow
- แก้ `calcAmplitude case 1` (`A_pct * lk * 0.5` → `lk * sin(A_pct * π/1.5)`) ให้ A_pct=50% ได้ cone half-angle 60° เห็นวงโคจรชัด

### นำเข้าเว็บไซต์
- รัน `protect_new_file.py` ✅ (idempotent — DOMAIN/MOBILE re-injected ไม่มี duplicate)
- เพิ่ม card ใน [demo-mechanics.html](demo-mechanics.html) section "การสั่น · SHM" — accent2 (purple), preview canvas, FREE tag, badges SHM + Identifier · เปลี่ยน count จาก 1 → 2 simulations
- เพิ่ม link ใน [library.html](library.html) section "🌀 การสั่น · SHM" (lib-item #25) · เลื่อน SHM Simulation เดิม → #26
- Verified: คลิก card → เปิดไฟล์ปกติ, title = "SHM01 — SHM Identifier | KP Science Simulation", ไม่มี console errors

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม card ใน `index.html` / `library.html` / `demo-*.html` สำหรับ SHM Identifier
- ยังไม่ได้ push git

---

## [2026-04-26 14:30] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง Lab 42 — SHM03 Spring Builder (อนุกรม/ขนาน + ดิ่ง/ระดับ)
- 3 tabs: Simulation / วิธีการทดลอง / ทฤษฎี (มี SVG visual diagrams)
- 3 ฐาน: A·Builder (single/series/parallel × 1-3 springs), B·F-x Graph (Hooke's slope = -k_eff), C·Dual-view (horizontal vs vertical)
- 2 โหมดบันทึก: Manual (default, มี virtual stopwatch + lap + บันทึก row) / Auto (sample 0.1s + CSV export)
- Misconception traps M3.1-M3.4 (interactive radio + ตรวจ + เฉลย)
- Energy bars (KE/PE_spring/PE_g/E_tot) real-time
- g dropdown (โลก/จันทร์/อังคาร/พฤหัส/อวกาศ)
- Verified ในเบราว์เซอร์: k₁=100,k₂=200 series → k_eff=66.67 ✓, T=0.770s ✓, KE+PE=½kA²=0.75J ✓ (energy conserved), x₀=mg/k=14.7cm ✓

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/42. shm-spring-builder.html` — สร้างใหม่
- `kp-auth.js` — เพิ่ม `'lab-42'` ใน VLAB_SERIES.vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-42'` ใน VLAB_SERIES + LAB_LIST entry
- รัน `protect_new_file.py` ✅ (GA, Topbar, Watermark, Firebase, Access guard)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม card ใน `index.html` / `library.html` / `virtual-physics-lab-02.html` สำหรับ Lab 42
- ยังไม่ได้ push git
- ยังไม่ได้เพิ่ม Part 1 (POE) / Part 3 (แบบฝึกหัด) — รอผู้ใช้ตัดสินใจ

### หมายเหตุ
- Spring Builder ใช้ toggle (series/parallel/single) + dropdown จำนวนสปริง แทน drag-drop UI จริง — เพราะ drag-drop ใน canvas ซับซ้อนเกินสำหรับขนาดหน้านี้ แต่ผลลัพธ์ทาง physics + visual ครบถ้วน
- ฐาน C (Dual-view) เป็นไฮไลต์สำหรับแก้ M3.3/M3.4 ชัดเจนมาก

---

## [2026-04-27] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง Lab 44 — SHM06 Damping & Resonance (`44. shm-damping-resonance.html`)
- 3 Tabs: Simulation / วิธีการทดลอง / ทฤษฎี (พร้อม Misconception Traps M6.1, M6.2, M6.3)
- 3 ฐาน (focus ทีละฐานผ่าน sub-nav):
  - **ฐาน A · Damping Sweep** — slider b/k/m/A₀ + preset b={0,0.1,0.5,1.0} · ปุ่ม "🔖 จับคาบ T (ที่ peak)" ตรวจ peak อัตโนมัติแล้วบันทึกตาราง · readout T, ω₀, ω_d, regime (under/critical/over) · canvas มี dashpot แสดง b
  - **ฐาน B · Resonance Sweep** — slider f_drive/F₀/b/k/m · 2 โหมด: Manual (default, กดปุ่ม "📍 บันทึกจุดนี้") + Auto-Sweep (กวาด 0.1→3 Hz ใน ~30s) · readout f_n, A_steady (ทฤษฎี), Q, FWHM · กราฟแสดง Lorentzian theory + จุดที่บันทึก + marker f_drive (สี pink) + f_natural (สี green)
  - **ฐาน C · Preset Cases** — 6 preset: Tacoma, Wine Glass, ชิงช้า, MRI, LIGO, Taipei 101 · case-info card + วิดีโอ placeholder (มี TODO comment ขอ Gemini prompt) + PBL radio (use/prevent) + textarea reason
- Physics integrator: semi-implicit Euler (4 substeps/frame), peak detection จาก zero-crossing ของ velocity
- Click/drag บนกราฟ A vs f เพื่อตั้ง f_drive ได้
- ปุ่ม Export ดาวน์โหลด JSON ครบ: `b_values_tried`, `damping_log`, `f_drive_sweep_data`, `resonance_peak_identified`, `preset_cases_explored`, `Q_factor`, `f_natural`, `PBL_design_choice`
- Tab 2: วิธีทดลองทีละฐาน + ตารางบันทึกเปล่าให้ปริ้น + checklist ก่อนส่งงาน
- Tab 3: ทฤษฎี damped SHM (พร้อม SVG x(t) + envelope), Lorentzian curve (3 ค่า b ทับกัน), Q-factor, Misconception Traps M6.1-M6.3 พร้อมการทดลองยืนยัน, การประยุกต์ในชีวิตจริง 6 กรณี
- Verified ใน preview:
  - f_natural = √(200/1)/(2π) = 2.25 Hz ✓
  - T_calc = 0.444 s ตรงกับสูตร ✓
  - Peak detection: T_meas = 0.444 s (ตรงทฤษฎี ที่ b=0.2) ✓
  - A_resonance ที่ f_drive=f_n: F₀/(b·ω₀) = 1/(0.3×14.14) = 0.2357 m ตรงกับ readout ✓
  - Regime classification: under-damped ✓
  - ไม่มี console errors

### ไฟล์ที่แก้
- `Virtual Physics Lab 01/Mechacnics/44. shm-damping-resonance.html` — สร้างใหม่
- `kp-auth.js` — เพิ่ม `'lab-44'` ใน VLAB_SERIES.vpl01.labs
- `_admin/admin.html` — เพิ่ม `'lab-44'` ใน VLAB_SERIES + LAB_LIST entry "Lab 44 (SHM06 Damping & Resonance)"
- รัน `python3 _admin/protect_new_file.py` ✅ (FRAME, TOPBAR, MOBILE, WATERMARK, FIREBASE_CDN, KP_AUTH, ACCESS_GUARD ครบ)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่ม card ใน `index.html` / `library.html` / `virtual-physics-lab-01.html` สำหรับ Lab 44
- ยังไม่ได้เจนวิดีโอจริงสำหรับ preset cases (ใช้ placeholder + TODO comment สำหรับ Gemini Video prompt)
- ยังไม่ได้ push git
- ยังไม่ได้เพิ่ม Part 1 (POE) / Part 3 (แบบฝึกหัด) — รอผู้ใช้ตัดสินใจ

### หมายเหตุ
- Auto-sweep ใช้เวลา ~30 วิ เพื่อให้แต่ละความถี่มีเวลา settle ก่อน sample (อาจปรับลด/เพิ่มได้)
- Click-drag บนกราฟทำงานทั้ง mouse + touch — เปลี่ยน f_drive แบบ interactive
- ในการ์ด Preset Cases มี comment `TODO[Gemini-video]` พร้อม prompt template ที่ละเอียด — เมื่อเจนวิดีโอแล้ว replace `<div class="vid-placeholder">` ด้วย iframe/video tag
- Q ที่แสดงใน HUD ใช้สูตร √(km)/b — ถ้า b เล็กมาก (เช่น 0.05) Q จะสูงมาก (~283) ตามจริง wine glass

## [2026-04-27 — รอบ 2] — Redesign Lab 44

### ทำอะไรไปบ้าง
- **ฐาน A** เพิ่มโหมดบันทึกเอง (default) ใช้ caliper:
  - กราฟ A(t) แสดงเส้นต่อเนื่อง 8s window (TRACE_MAX=600, push 1 ครั้ง/frame)
  - ปุ่ม ⏸ หยุด → caliper เปิดใช้ snap-to-peak (เมื่อ paused)
  - ลาก 2 เส้นประส้ม/ชมพูบนกราฟวัด Δt → กดบันทึก T₁ → ลากใหม่กดบันทึก T₂
  - คำนวณ %error ระหว่าง T₁/T₂ + เทียบกับ T_ทฤษฎี
  - ตารางบันทึกเปลี่ยน column: # · b · T วัด · T ทฤษฎี · %error
  - โหมด 👁 เผยเฉลย: ปุ่มจับคาบอัตโนมัติเดิม
- **ฐาน B** เพิ่มโหมดบันทึกเอง (default) แบบ blind:
  - ซ่อนเส้นประ f_natural บนกราฟ + ซ่อนค่า readout (มาส์ก [ซ่อน])
  - นักเรียนลาก slider f_drive หา peak amp เอง
  - ปุ่ม "📍 บันทึก peak (f นี้คือ resonance)" → เผยค่าจริง + %error (สีตามระดับ error)
  - โหมด 👁 เผยเฉลย: เห็น f_n + Auto-Sweep
- **ฐาน C** redesign:
  - เพิ่ม slider f_drive แยก (sl-fdC) sync กับ Base B physics
  - 6 case-specific canvas drawers:
    - 🌉 Tacoma — สะพานแขวน 2 ทาวเวอร์ + cable + deck twist + wind streamlines
    - 🍷 Wine Glass — แก้วคริสตัล + ขอบสั่นเป็น ellipse + speaker + cracks เมื่อ A สูง
    - 🎡 ชิงช้า — frame + เด็ก + chain + pusher arrow + ground
    - 🧲 MRI — magnet bore + 5 proton spins precessing + RF pulse rings
    - 🌌 LIGO — L-shape interferometer + 4-km arms + suspended mirrors + GW wave
    - 🏢 Taipei 101 — building cross-section + windows + tuned mass damper (counter-phase)
  - canvas เปลี่ยนตาม case ที่เลือก (delegate ใน draw())
  - ปุ่ม "📍 บันทึก resonance ของ case นี้" → เผย f_natural จริง + %error
  - loadCase ตั้ง f_drive เริ่มต้นที่ 30% ของ f_n เพื่อให้นักเรียนต้องค้นหา
- **Tab 3** เพิ่มการ์ด "🎬 Gemini Video Prompts" รายละเอียดเต็มทั้ง 6 cases (12-14 sec each, color palette, HUD overlay, style guidelines, สิ่งที่ควรเลี่ยง)
- **Tab 2** อัปเดตวิธีทดลองทั้ง 3 ฐานให้ตรงกับ workflow ใหม่

### ไฟล์ที่แก้
- `Virtual Physics Lab 01/Mechacnics/44. shm-damping-resonance.html` — redesign ครั้งใหญ่ (+~600 บรรทัด)

### Verified ใน preview
- Base A: trace ต่อเนื่อง 18 รอบ/8s ตรงกับ f=2.25 Hz ✓ · envelope ส้มเทียบ A₀·exp(-bt/2m) ✓ · caliper handles + Δt label render ถูก
- Base B: เปลี่ยน mode → mask ตัว f_n ทั้ง readout และเส้นประบนกราฟ ✓
- Base C: tacoma → canvas เป็นสะพานพร้อม wind, twist, towers ✓ · f_drive slider sync ✓ · loadCase set f เริ่มต้น 0.19 Hz (30% ของ 0.64 Hz) ✓
- ไม่มี console errors

### หมายเหตุ
- Snap-to-peak ทำงานเมื่อ paused เท่านั้น — ตอน playing นักเรียนลากได้อิสระ
- TRACE_MAX=600 เก็บ ~10s ที่ 60 fps (เกิน 8s window พอดี)
- Caliper ในกราฟต้องลากครอบ ≥2 peak เพื่อวัดคาบจริง — ระบบเตือนถ้า Δt < 0.05s

---

## [2026-05-01] — เครื่อง: ที่ทำงาน

### ทำอะไรไปบ้าง
- สร้าง **Lab 42 (VPL02) — การวัดด้วยเวอร์เนียร์ &amp; ไมโครมิเตอร์**
- 3 tab: Simulation / วิธีการทดลอง / ทฤษฎี
- 2 เครื่องมือ: Vernier (0.05 mm, 20 ขีด/19 mm) + Micrometer (0.01 mm, pitch 0.5, thimble 50)
- 2 โหมด: Manual (ดีฟอลต์ — ฝึกอ่านสเกลกรอกค่า + ตรวจ + คำใบ้ + เฉลย) / Auto (อ่านอัตโนมัติ + วัด 5 ครั้งทันที)
- วัตถุ Vernier 7 ตัว, Micrometer 6 ตัว (ลูกแก้ว/ลูกเหล็ก/เหรียญ/ลวด/ฟอยล์/กระจก/PVC ฯลฯ)
- Canvas วาดเวอร์เนียร์ (สเกลหลัก + เวอร์เนียร์ 20 ขีด + jaws + วัตถุ) และไมโครมิเตอร์ (frame + anvil + spindle + sleeve + thimble + ratchet)
- Drag เมาส์/touch บน canvas เพื่อเลื่อนตำแหน่ง + Zoom slider 1–4×
- ตารางบันทึก + คำนวณ x̄, σ, รายงาน x̄ ± σ + Export CSV
- Theory tab มี canvas อธิบาย principle ของเวอร์เนียร์และไมโครมิเตอร์ทีละขั้น
- รัน `protect_new_file.py` ✅ (เพิ่ม GA, topbar, mobile, watermark, firebase, kp-auth, access-guard)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/42. measurement-vernier-micrometer.html` — สร้างใหม่
- `_admin/admin.html` — เพิ่ม `lab-42` ใน VLAB_SERIES.vpl02 + LAB_LIST (label "เวอร์เนียร์·ไมโครมิเตอร์")
- `kp-auth.js` — เพิ่ม `lab-42` ใน VLAB_SERIES.vpl02

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 42 ใน `index.html`, `library.html`, `virtual-physics-lab-01.html` (VPL02 catalog page) — ครั้งหน้าควรเพิ่ม
- ทดสอบจริงในเบราว์เซอร์: ลองอ่าน manual mode + ตรวจคำตอบ + Auto fill 5

### หมายเหตุ
- ใน VPL01 มี lab-42 อยู่แล้ว (SHM03 Spring Builder) แต่ access string `vlab:vpl02:lab-42` แยกจาก `vlab:vpl01:lab-42` ตาม schema v4 — ไม่ชนกัน
- Tolerance ตรวจคำตอบ Manual: main exact, sub ±1 ขีด (ตามขีดจำกัดสายตา)
- Random noise ±0.04 mm (Vernier) / ±0.008 mm (Micrometer) จำลองความคลาดเคลื่อนของผู้วัด

---

## [2026-05-02 03:15] — เครื่อง: ที่ทำงาน

### ทำอะไรไปบ้าง
- **สร้างชุด Demo ดาราศาสตร์ใหม่ 13 ไฟล์** — ดึงเนื้อหาจาก research lessons (`วิจัย/wave-mechanics-research/lessons/astronomy/ep01–ep08`) มาแปลงใหม่ให้เข้ากับ template KP Science (orbital_simulation.html)
- ทุกไฟล์: header + scope + tabs (Simulation/Theory) + canvas + side panel + ทฤษฎี + footer
- Pattern เดิม: ตัด narrative/teacher cue/scoring/Book.* ออกหมด · ทำเป็น standalone demo
- รัน `protect_new_file.py --scan --fix` ✅ inject GA + KP Topbar + Watermark + Firebase + Auth + Access Guard ครบทุกไฟล์

### ไฟล์ที่สร้างใหม่ (Demo/ดาราศาสตร์/)
1. `hubble_expansion.html` — ลูกโป่งเอกภพ + กฎฮับเบิล (จาก ep01/p09-balloon)
2. `cosmic_timeline.html` — 6 ยุคของเอกภพ + particle simulation (จาก ep01/p11-timeline + shared/particles.js)
3. `galaxy_rotation.html` — Rotation curve + Dark Matter halo (จาก ep02/p11-rotation)
4. `stellar_parallax.html` — d=1/p + ดาวจริง 10 ดวง (จาก ep03/p05-parallax10)
5. `apparent_magnitude.html` — Pogson scale + เปรียบเทียบ 2 ดาว (จาก ep03/p08-arrive)
6. `absolute_magnitude.html` — Distance modulus + m vs M (จาก ep03/p09-absolute)
7. `sunspot_cycle.html` — Sunspot + Schwabe 11-year cycle + butterfly diagram (จาก ep05/p08b)
8. `solar_corona.html` — โครงสร้างชั้น Sun + Coronal Heating Paradox + T(r) chart (จาก ep05/p10b)
9. `solar_phenomena.html` — 5 ปรากฏการณ์ tabs (sunspot/prominence/flare/CME/wind) (จาก ep05/p14)
10. `cmb_recombination.html` — Recombination + photon decoupling animation (จาก ep08/p03)
11. `cosmic_inflation.html` — Inflation 10²⁶× ใน 10⁻³² s (จาก ep08/p05)
12. `first_stars.html` — Pop III star formation + DM halo (จาก ep08/p08)
13. `galaxy_clustering.html` — Cosmic web · click-to-place DM halos (จาก ep08/p09)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **ยังไม่ได้เพิ่มไฟล์ทั้ง 13 ใน `demo-astronomy.html`** (catalog page) — ครั้งหน้าควรเพิ่มการ์ด preview
- **ยังไม่ได้เพิ่มใน `index.html` Featured Demos** — ครั้งหน้า
- **ยังไม่ได้เพิ่มใน `library.html`** — ครั้งหน้า
- **ยังไม่ได้ทดสอบ rendering ใน browser** ทุกไฟล์ — ทดสอบ live ก่อน publish
- ยังเหลือ ep04, ep06, ep07 ในโฟลเดอร์วิจัย ที่ไม่มี simulation interactive ส่วนใหญ่ (skipped)

### หมายเหตุ
- Pattern ที่ใช้ทุกไฟล์: `<body data-access="demo:astronomy">` เพื่อให้ Access Guard ตรวจสิทธิ์
- mini-bug แก้แล้ว: `cmb_recombination.html` ใช้ `<nav.tabs>` เป็น tag (ผิด) → แก้เป็น `<nav class="tabs">`
- ขนาดไฟล์โดยเฉลี่ย ~600–900 บรรทัด ก่อน protect, ~1100–1500 หลัง protect (จาก injection)
- Theme ใช้สี orange accent (#fb923c) ตรงกับ orbital_simulation.html เดิม — ไม่ใช่ cyan ของ VPL01
- การ์ด simulation ทั้งหมดมี responsive layout (`@media max-width:900px → flex-direction:column`)
- หน้าทฤษฎีใช้ class `.law` block พร้อม fbox สูตรแบบ monospace ให้น่าจดจำ
- ทดสอบ live ใน preview panel ทุกไฟล์ระหว่าง dev — ไม่มี console error สังเกตได้

---

## [2026-05-09] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- สร้าง **Lab 43 (VPL02) — ทฤษฎีบิกแบง (Big Bang Theory)** ตามภาพอ้างอิง 2 หน้า "The Big Bang"
- 3 tabs: Simulation / วิธีการทดลอง+บันทึกผล / ทฤษฎี
- **4 การทดลองย่อย** (sub-nav):
  1. **ไทม์ไลน์เอกภพ (15 ยุค)** — slider log₁₀(t) จาก −43 ถึง +17.6 · แสดง era + T(t) + scale a(t) + อนุภาคเด่น · animation particle ตามยุค · timeline bar 15 segments + marker · ปุ่ม play/pause/reset/snapshot
  2. **กฎฮับเบิล** — 8 กาแล็กซี่กระจายรอบ Earth · คลิก → spectrum Hα 656.28 nm + redshift · plot d-v + linear fit → H₀ → อายุเอกภพ (×0.96 ΛCDM correction)
  3. **BBN** — slider T_freeze (0.5–1.5 MeV) + τ wait (0–500 s) · อนุภาค p/n/He animation 3 phase (freeze→decay→fusion) · Y = 2(n/p)/(1+n/p) · เปรียบเทียบกับ 25%
  4. **CMB Blackbody** — slider T (1–10 K) · เส้น Planck ส้ม + 12 จุดข้อมูล COBE/FIRAS ขาว · SSE + %error vs 2.725 K · Wien ν_peak = 58.79T GHz
- **Manual mode (default)** + Auto mode + Hint toggle (💡)
- ทุกการทดลองมี: ตารางบันทึก + บันทึกแถว + autoFill + clear + Export CSV
- Tab ทฤษฎี: 5 canvas visualization
  - thCv1: log T vs log t (จุดสำคัญ 6 era marker)
  - thCv2: Hubble's Law (8 data points + slope line)
  - thCv3: BBN flow 3 boxes (freeze 1/6 → decay 1/7 → fusion 25%)
  - thCv4: CMB Planck curves 3 ค่า (T=2.5/2.725/3.0 K)
  - thCv5: Pie chart 4.6/23/72.4% + composition breakdown
- Tab วิธีการทดลอง: 4 สเต็ปการ์ด + warning + checklist
- รัน `python3 _admin/protect_new_file.py` ✅ inject GA/TOPBAR/MOBILE/WATERMARK/FIREBASE_CDN/KP_AUTH/ACCESS_GUARD ครบ
- Sync `kp-auth.js` (vpl02.labs += 'lab-43') และ `_admin/admin.html` (VLAB_SERIES + LAB_LIST entry "Lab 43 (ทฤษฎีบิกแบง)")
- Verified ในเบราว์เซอร์: เปิดได้ปกติ · ทั้ง 4 sub-exp render ครบ · slider sync · CSV export ใช้งานได้

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/43. big-bang-theory.html` — สร้างใหม่ (~1500 บรรทัด)
- `kp-auth.js` — เพิ่ม `'lab-43'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-43'` ใน VLAB_SERIES.vpl02 + LAB_LIST entry

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 43 ใน `index.html` / `library.html` / `virtual-physics-lab-02.html` (ต้องสร้าง canvas preview animation ด้วย)
- ยังไม่ได้ push git
- รอ user: ต้องการเพิ่ม Part 1 (POE) หรือ Part 3 (แบบฝึกหัด) ไหม?

### หมายเหตุ
- Physics ที่อ้างอิงตรงจากภาพ: T=2.725 K · Inflation 10²⁷ · 75% H + 25% He · 4.6/23/72.4% · 13.7 Gy · matter-antimatter 1ppb · X-bosons 10⁻¹² s
- T(t) ≈ 1.5×10¹⁰/√t สำหรับ radiation era (0 < log t < 13.08), matter era ใช้ a∝t^(2/3) → T∝t^(-2/3)
- BBN: n/p_freeze = exp(−1.293/T_f) · decay factor exp(−τ/880s) · Y = 2(n/p)/(1+n/p)
- CMB Planck: B(ν,T) = (2hν³/c²)/(exp(hν/kT)−1), ν_peak = 5.879×10¹⁰·T Hz
- VPL01 มี lab-43 (SHM04) อยู่แล้ว — access string `vlab:vpl01:lab-43` กับ `vlab:vpl02:lab-43` แยกกันตาม schema v4 ไม่ชนกัน
- Color theme: orange (#fb923c) astronomy + yellow heat + green matter + purple quantum

---

## [2026-05-10] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- 🚀 **Region 1.3.1 เนินยิงไกล (โพรเจกไตล์) Stage A LIVE** — 80 ข้อ concept-only
- เลือกทาง B (แยก 1.3 เป็น 3 sub-region: 1.3.1 projectile / 1.3.2 วงกลม / 1.3.3 SHM)
- 7 หมวด: A1 นิยาม(10) · A2 แยกแกน x-y ⭐(14) · A3 a_x=0,a_y=g(10) · A4 จุดสูงสุด ⚠(12) · A5 symmetry(10) · A6 มุมยิง complementary(14) · A7 ยิงแนวระดับจากที่สูง(10)
- 5 SVG: PARABOLA, VEL_DECOMP, ANGLE_COMP, HORIZONTAL_LAUNCH, MAX_HEIGHT
- ใช้ g=10 m/s² · ตัด air resistance ตามนโยบายครู
- Wire engine: script tag + REGIONS['1.3'] (rename เนินยิงไกล) + 3 mobs (ลูกปืนใหญ่/ลูกธนู/ลูกบาส) + getQuestionPoolForStage routing R131_A
- Region 1.3 ready:true · Stage A only · B/C/D toast "ยังไม่มีข้อสอบ"
- ครู review pass: แก้ P004 (free fall ≠ projectile · True→False) + P007 (เปลี่ยนจาก meta question เป็นโจทย์ตัวอย่าง projectile ในอุดมคติ)

### ไฟล์ที่แก้
- `physics-quest/region-1-3-1-stage-a-questions.js` — สร้างใหม่ 392 บรรทัด · 80 ข้อ
- `physics-quest/index.html` — script tag + REGIONS['1.3'] stages + 3 mobs + getQuestionPoolForStage
- `Games/engine/region-1-3-1-stage-a-questions.js` — sync source
- `Games/engine/physics-quest.html` — sync engine
- `Games/content/region-1-3-1/region-1-3-1-A-preview.html` — preview ครูใช้ review

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **รอครูตรวจเนื้อหา 80 ข้อ** ในเบราว์เซอร์จริง (เปิด region 1.3 → Stage A)
- Region 1.3.1 Stage B/C/D · Region 1.3.2 วงกลม · Region 1.3.3 SHM
- Mini-boss กาลิเลโอ Throw (1.3.1) — projectile sim arena (Galileo Throw)
- protect_new_file.py: ไฟล์ JS ไม่ต้อง protect · preview HTML ใน Games/ ไม่ขึ้น Pages

### หมายเหตุ
- 1.3 ตอนนี้ scope แค่ projectile (1.3.1) — circular/SHM จะแยกเป็น sub-region ทีหลัง (ตาม decision ทาง B)
- ลูกธนู monkey-and-hunter ใช้เป็นโจทย์ใน P022 (classic Galilean independence)
- misconception killer ใหญ่สุดคือ A4 (จุดสูงสุด) — vᵧ=0 แต่ vₓ≠0, a≠0, KE≠0
- complementary angles (A6) — sin(2θ) = sin(180°−2θ) → 30°↔60° / 20°↔70° R เท่ากัน

---

## [2026-05-10 ต่อ] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- 🚀 **Region 1.3.2 เนินวงเวียน (วงกลม) Stage A LIVE** — 80 ข้อ concept-only
- ครูส่งชีท "การเคลื่อนที่แบบวงกลม" 31 หน้ามาเป็น reference → align โจทย์กับ 13 รูปแบบในชีท
- 7 หมวด: A1 UCM+ทิศ v(10) · A2 ทิศ a/F_c ⭐(12) · A3 สูตร a_c,F_c(10) · A4 ω,T,f,v=ωR(12) · A5 ผันผัน(10) · A6 13 Pattern ⭐(16) · A7 ความเข้าใจลึก(10)
- 7 SVG: UCM_VECTORS, CONICAL, VERTICAL_LOOP, BANKED, ROTOR, ORBIT, HILL_VALLEY
- A6 cover 13 รูปแบบ: แกว่งราบ(T) · กรวย(T sinα) · vertical loop top(T+W)/bottom(T−W) · จานหมุน(f_s) · บนเนิน(W−N) · ในร่อง(N−W) · ถนนราบ(f_s) · banked(N sinθ) · มอเตอร์ไซค์(tanθ=v²/rg) · rotor(N) · ในกรวย(N comp) · ดาวเทียม(F_grav) · แกว่งจุดต่ำสุด(T−W)
- ตัด "centrifugal force" misconception ออกตามนโยบายครู (ครูไม่สอนคำนี้)
- Wire engine: script tag + REGIONS['1.3.2'] (เนินวงเวียน · ready:true) + REGION_ORDER + 3 mobs (ดาวเทียม/จานหมุน/รถบนทางโค้ง) + getQuestionPoolForStage routing R132_A
- คงไว้ pattern "1.3 = parent projectile + 1.3.2 = circular sub-region แยก"

### ไฟล์ที่แก้
- `physics-quest/region-1-3-2-stage-a-questions.js` — สร้างใหม่ 80 ข้อ
- `physics-quest/index.html` — script tag + REGIONS['1.3.2'] + REGION_ORDER + 3 mobs + getQuestionPoolForStage
- `Games/engine/region-1-3-2-stage-a-questions.js` — sync
- `Games/engine/physics-quest.html` — sync
- `Games/content/region-1-3-2/region-1-3-2-A-preview.html` — preview ครูใช้ review
- `KP-HQ/workboard-data.js` — todo + done

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอครูตรวจ 80 ข้อ
- Region 1.3.1 Stage B/C/D · Region 1.3.2 Stage B/C/D · Region 1.3.3 SHM
- Mini-boss กาลิเลโอ Throw (1.3.1) · เคปเลอร์ (1.3.2) · ฮอยเกนส์ (1.3.3)

### หมายเหตุ
- A6 16 ข้อกระจาย: แกว่งราบ(1) · กรวย(1) · vloop top(1) · vloop bottom(1) · จานหมุน(1) · บนเนิน(1) · ในร่อง(1) · ถนนราบ(1) · banked(1) · มอเตอร์ไซค์(1) · rotor(1) · ดาวเทียม(1) · vloop side(1) · แกว่งจุดต่ำสุด(1) · ในกรวย(1) · CHK รวม(1)
- ใน A7 มี v_min ที่จุดบนของ vertical loop = √(gR) (เตรียมพื้นให้ Stage C/D คำนวณ)
- commit cc61df3 · live ที่ kp-science.github.io/physics-simulations/physics-quest/

---

## [2026-05-11] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- 🚀 **Region 1.3.3 เนินสปริง (SHM) Stage A LIVE** — 70 ข้อ concept-only
- ครูเลือก A1-A6 เท่านั้น (ตัด A7 — ดังนั้นรวม 70 ไม่ใช่ 80)
- 6 หมวด: A1 นิยาม SHM(10) · A2 A,T,f,ω,phase(10) · A3 a=−ω²x ⭐(12) · A4 x,v,a cycle ⭐(12) · A5 SHM↔UCM projection(10) · A6 Spring+Pendulum T(16)
- 5 SVG: SHM_SPRING (3 ตำแหน่ง) · SHM_PENDULUM (L+θ) · SHM_PROJECTION (UCM↔SHM) · SHM_XT (sinusoidal graph) · SHM_VAX (extreme vs equilibrium)
- ตัด damped/forced SHM (advanced ม.ปลาย-ป.ตรี)
- Wire engine: script tag + REGIONS['1.3.3'] (เนินสปริง · ready:true) + REGION_ORDER + 3 mobs (มวลผูกสปริง 🪀 / ลูกตุ้มแกว่ง ⏰ / ลูกบอลในชาม 🥣) + getQuestionPoolForStage routing R133_A
- 🏆 **Region 1.3 ครบ 3 sub-region (Plan B):** 1.3.1 (80) + 1.3.2 (80) + 1.3.3 (70) = 230 ข้อ concept

### ไฟล์ที่แก้
- `physics-quest/region-1-3-3-stage-a-questions.js` — สร้างใหม่ 70 ข้อ
- `physics-quest/index.html` — script tag + REGIONS['1.3.3'] + REGION_ORDER + 3 mobs + getQuestionPoolForStage
- `Games/engine/region-1-3-3-stage-a-questions.js` — sync
- `Games/engine/physics-quest.html` — sync
- `Games/content/region-1-3-3/region-1-3-3-A-preview.html` — preview ครูใช้ review
- `KP-HQ/workboard-data.js` — todo + done

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอครูตรวจ 70 ข้อ Stage A SHM
- Stage B/C/D ของ 1.3.1 + 1.3.2 + 1.3.3 (ใส่ตัวเลข + คำนวณ)
- Mini-boss กาลิเลโอ Throw (1.3.1) · เคปเลอร์ (1.3.2) · ฮอยเกนส์ (1.3.3)
- Boss Newton Throne (รอ mini-boss × 6 region · ตอนนี้ 2/6)

### หมายเหตุ
- 1.3.3 ตัด A7 ตามคำสั่งครู — ลด 80→70 ไม่ปรับสัดส่วนกลับ
- หัวใจของ SHM: a=−ω²x · ที่สมดุล v=max,a=0 · ที่ extremes v=0,a=max
- Spring T ไม่ขึ้น g · Pendulum T ไม่ขึ้น m,A (มุมเล็ก)
- commit 407026c · live ที่ kp-science.github.io/physics-simulations/physics-quest/

---

## [2026-05-11 ต่อ] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- 🚀 **Region 1.3.1 Stage B "ใช้สูตรไหน" LIVE** — 80 ข้อ apply
- pattern เดียวกับ 1.2 Stage B (169 ข้อ) — "ดึงตัวแปร + เลือกสูตร + ดูทิศ" ยังไม่คำนวณลึก
- 7 หมวด: B1 ดึงตัวแปร vₓ₀ vᵧ₀(15) + B2 เลือกสูตรเวลา(12) + B3 H(12) + B4 R(12) + B5 ยิงแนวระดับจาก h(15) + B6 จุดสูงสุด(8) + B7 ทิศ + แตกความเร็ว(6)
- MCQ ~50 + FILL ~30 · noReveal:true (บล็อก See50% + choiceCut)
- 3 SVG: LAUNCH (มุม θ + v₀) · PARABOLA_RH (R, H labeled) · HCLIFF (yiing แนวระดับจากหน้าผา)
- ตัวเลขลงตัว: sin37°=0.6, cos37°=0.8 · sin53°=0.8, cos53°=0.6 · sin45°=cos45°=1/√2
- Wire engine: script tag + REGIONS['1.3'] stage B label "apply · vₓ vᵧ t H R" + getQuestionPoolForStage routing

### ไฟล์ที่แก้
- `physics-quest/region-1-3-1-stage-b-questions.js` — สร้างใหม่ 80 ข้อ
- `physics-quest/index.html` — script tag + stage B label + getQuestionPoolForStage
- `Games/engine/region-1-3-1-stage-b-questions.js` — sync
- `Games/engine/physics-quest.html` — sync
- `Games/content/region-1-3-1/region-1-3-1-B-preview.html` — preview
- `KP-HQ/workboard-data.js` — todo + done

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอครูตรวจ 80 ข้อ Stage B 1.3.1
- Stage C (calc) + D (critical events) ของ 1.3.1
- Stage B/C/D ของ 1.3.2 + 1.3.3
- Mini-boss กาลิเลโอ Throw / เคปเลอร์ / ฮอยเกนส์

### หมายเหตุ
- Region 1.3.1 ตอนนี้: A (80 concept) + B (80 apply) = 160 ข้อ
- Stage B mob lv 12 (ตามตาราง STAGES) — เด็กผ่าน Stage A (mob lv 10) มาแล้ว
- เลข ID: A = R131P001-080 · B = R131P081-160 (ต่อเนื่อง)
- commit a3b57ba

---

## [2026-05-11 ปิด Stage B ทั้ง 3 sub] — เครื่องที่บ้าน

### ทำอะไรไปบ้าง
- 🚀 **Region 1.3.3 (SHM) Stage B LIVE** — 70 ข้อ apply
- 6 หมวด: B1 ω,T,f,v_max,a_max(10) · B2 a=−ω²x,v(10) · B3 ผันผัน(10) · B4 x,v,a,KE,PE ⭐(15) · B5 Spring T calc(15) · B6 Pendulum T calc(10)
- 4 SVG ใส่ตั้งแต่แรก: SPRING (3 ตำแหน่ง) · PEND (L+θ) · VAX (extreme vs equilibrium) · XT (sinusoidal)
- รอบเดียวกัน — เพิ่ม SVG ในไฟล์อื่น (รอบ 2: 76 figures total)
  · 1.3.1A: P017, P040, P074 → +3 (รวม 8)
  · 1.3.1B: P083, P096, P102, P109, P120, P121, P123, P132, P133, P135, P138, P139, P140 → +13 (รวม 16)
  · 1.3.2A: C015, C018, C058, C061 → +4 (รวม 11)
  · 1.3.2B: C118, C119, C120, C122, C124, C125, C126, C127, C128, C130, C131, C132, C134, C142, C145, C147, C148, C149, C150, C154, C155, C156 → +22 (รวม 24)
  · 1.3.3A: S009, S025, S028, S033, S034, S036, S057, S058, S061, S062, S063, S064, S065 → +13 (รวม 17)

### ไฟล์ที่แก้
- `physics-quest/region-1-3-3-stage-b-questions.js` — สร้างใหม่ 70 ข้อ
- `physics-quest/region-1-3-{1,2}-stage-{a,b}-questions.js` — เพิ่ม SVG
- `physics-quest/region-1-3-3-stage-a-questions.js` — เพิ่ม SVG
- `physics-quest/index.html` — script tag + stage B label + getQuestionPoolForStage
- Sync ทั้งหมดไป Games/engine/ และ Games/content/region-1-3-3/region-1-3-3-B-preview.html

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอครูตรวจ Stage B SHM 70 ข้อ
- Stage C/D ของทั้ง 3 sub (1.3.1, 1.3.2, 1.3.3)
- Mini-boss กาลิเลโอ Throw / เคปเลอร์ / ฮอยเกนส์
- Boss Newton Throne (รอ mini-boss × 6)

### หมายเหตุ
- 🏆 Region 1.3 (Plan B) ครบ A+B ทั้งสาม sub: 460 ข้อ (160+160+140)
- World 1 progress: 2 full region (1.1, 1.2) + 3 sub-region with A+B (1.3.1-1.3.3)
- รวม SVG ในทั้ง 5 ไฟล์: 76+8 = 84 ข้อมีภาพประกอบ
- ทำงานวันนี้รวม 7 commits: 407026c → a3b57ba → 63911d2 → 4d0b36a → 8828d1a → d666907 → 925ac32

## [2026-05-13] — เครื่องที่ทำงาน

### ทำอะไรไปบ้าง
- สร้าง **Lab 44 (VPL02) — Standing Waves of Sound in an Air Column (คลื่นนิ่งของเสียงในหลอดอากาศ)** ตามภาพอ้างอิงจากใบกิจกรรม "B. Standing Waves of Sound in an Air Column"
- ใช้สกิล `physics-simulation-builder` · 3 tabs: 🎬 Simulation / 🧪 วิธีการทดลอง+บันทึกผล / 📐 ทฤษฎี+อธิบาย
- **Web Audio API จริง** — Oscillator (sine) + bandpass filter + gain envelope; ปุ่ม "🔔 เคาะส้อมเสียง" (decay ~3 sec), ปุ่ม "🎵 ต่อเนื่อง"; gain modulated by `loudnessAtL(L, λ)` = Gaussian peaks ที่ L_n=(2n-1)λ/4 (sigma 2.5 cm)
- เลือกส้อมเสียง 8 ความถี่: 256, 288, 320, 341.3, 384, 426.7, 480, 512 Hz (ค่าเริ่ม 384 Hz)
- Temperature slider 0–40 °C → v = 331.4 + 0.6·T m/s แสดง live; λ ทฤษฎี = v/f
- **Drag interaction บน canvas**: mousedown + drag เปลี่ยน `tubeBottomDepth` (-0.05 ถึง 0.49 m) → L = 0.50 - max(0, depth); รองรับ touch + mouse wheel (shift = fine 1 mm step)
- **Manual mode** (default) — ผู้ใช้ลากหลอด, ฟังเสียงดังสุด, กด "💾 บันทึก L ตอนนี้" บันทึก L₁; ครั้งที่ 2 ระบบคำนวณ λ = 2(L₂−L₁), v = f·λ ใส่ตารางอัตโนมัติ
- **Auto Scan mode** — เลื่อนหลอดอัตโนมัติ 6 cm/s, peak-detection ผ่าน 12-sample sliding window, เก็บ 2 ยอดที่ห่างกัน > λ/4
- **Hint toggle 💡** — แสดงเส้นประสีเหลือง + label `n=1 · L=0.224 m` ฯลฯ ทุกตำแหน่งเรโซแนนซ์บน canvas
- **Loudness bar** — gradient blue→cyan→green→yellow→red แสดง 0–100%, ข้อความ "🔊 ดังที่สุด (resonance!)" เมื่อ > 0.85
- **Canvas visualization** — กระบอกแก้ว + น้ำ (เห็น ripple meniscus) + หลอดพลาสติก + ส้อมเสียง (มี jiggle animation ขณะสั่น) + standing wave envelope (sin(kx) จากผิวน้ำขึ้นไป) + ไม้บรรทัด cm scale
- **ตารางบันทึก** — Trial / f / L₁ / L₂ / λ / v ลบรายตัวได้, partial row โชว์เมื่อรอ L₂; summary v_avg + %error vs v(T) ทฤษฎี; Export CSV
- **Tab วิธีการทดลอง** — 6 step cards ครบครัน: เตรียมอุปกรณ์ · ตั้งค่า · Manual Mode · Auto Mode · ตัวอย่างผล (จากภาพอ้างอิงจริง: 512 Hz/L₁=0.152/L₂=0.481/λ=0.658/v=336.9 และ 384 Hz/L₁=0.210/L₂=0.664/λ=0.908/v=348.7) · วิเคราะห์
- **Tab ทฤษฎี** — 5 sections: closed-end pipe + 4 harmonic mini-canvases (n=1..4, แสดง sin((2n-1)π/2·t) + envelope + node/antinode dots) · v=fλ + thCv1 standing wave full visual · v vs T graph (thCv2) + current temp marker · End correction · Loudness vs L curve (thCv3) + resonance lines
- รัน `python3 _admin/protect_new_file.py "Virtual Physics Lab 02/44. standing-waves-air-column.html"` ✅ inject GA/TOPBAR/MOBILE/WATERMARK/FIREBASE_CDN/KP_AUTH/ACCESS_GUARD ครบ
- Sync admin: เพิ่ม `'lab-44'` ใน `kp-auth.js` VLAB_SERIES.vpl02.labs + `_admin/admin.html` VLAB_SERIES.vpl02.labs + LAB_LIST entry `{id:'lab-44',label:'Lab 44 (คลื่นนิ่งเสียงในหลอด)'}`
- Verified ใน preview: ทั้ง 3 tabs render สมบูรณ์ · canvas ไม่มี artifact · readouts sync ถูกต้อง (f=384, L=0.450, λ=0.897, v=344.6) · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/44. standing-waves-air-column.html` — สร้างใหม่ (~1100 บรรทัดก่อน protect, ~1400 หลัง protect)
- `kp-auth.js` — เพิ่ม `'lab-44'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-44'` ใน VLAB_SERIES.vpl02 + LAB_LIST entry

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 44 ใน `index.html` / `library.html` / `virtual-physics-lab-02.html` (catalog page) — ต้องสร้าง canvas preview animation
- ยังไม่ได้ push git
- ยังเหลือ Demo Astronomy 13 ไฟล์จากครั้งก่อน ที่ยังไม่เพิ่มใน `demo-astronomy.html` catalog / index featured / library

### หมายเหตุ
- Physics ตรงจากภาพ: λ = 2(L₂ − L₁) (ระยะระหว่าง antinode = λ/2) · v(T) = 331.4 + 0.6T · Sample calc 0.658 m จาก 512 Hz/L₁=0.152/L₂=0.481 ✓
- Closed-end pipe modes: L_n = (2n-1)·λ/4, n=1,2,3,... — น้ำเป็น displacement node (ปลายปิด) · ปากหลอดเป็น displacement antinode (ปลายเปิด)
- End correction e ≈ 0.6r — ถูกอธิบายในแท็บทฤษฎีว่าทำไมต้องวัด 2 ตำแหน่ง (เพื่อตัด e ออก)
- Color theme: คลื่น/เสียง — purple #818cf8 (--accent) + cyan #38bdf8 (--accent2) ตามมาตรฐาน physics-simulation-builder
- Loudness sigma 2.5 cm ให้ peak มี FWHM ~6 cm — ค่าจริงในห้องเรียนคาดว่าใกล้เคียงนี้
- Preview server (รัน python3 -m http.server 8765) อยู่ใน worktree `relaxed-lalande-cbb510` — ต้อง cp ไฟล์ไปที่นั่นเพื่อให้ preview เห็น

## [2026-05-13 ต่อ] — เครื่องที่ทำงาน · ปรับ Lab 44 ตาม feedback ครู

### ทำอะไรไปบ้าง (รอบ refinement)
หลังจากสร้าง Lab 44 รอบแรก ครูได้ feedback หลายจุด → iterate 6 รอบ:

**รอบ 1 — Layout fix**
- ป้าย L ตกขอบ canvas เมื่อหลอดอยู่ลึก → wrap เป็น pill + clamp Y position + leader line
- เพิ่ม **คาลิปเปอร์ดิจิทัล** 📐 — 2 ขา (▲ + ▼) draggable วัดระยะ Δ + คำนวณ λ=2Δ realtime
- Auto-snap ตำแหน่งเมื่อเปิด toggle ครั้งแรก ให้เห็นทันทีในขอบเขต canvas

**รอบ 2 — Geometry overhaul**
- ขนาด canvas ผิด (1405×878 จาก stretching) ทำให้ scale ใหญ่เกิน → cap canvas-box height = 620px
- รื้อ worldY model ใหม่: water surface ตรึงใกล้ก้น canvas, air zone ครองพื้นที่บน → เห็น tube + air column ครบ

**รอบ 3 — Real-physics tube + 3 features**
- ขยาย tubeLenM 0.50 → **1.10 m** เพื่อรับประกัน ≥2 เรโซแนนซ์สำหรับทุกความถี่ 256–512 Hz
- เพิ่ม guard ใน randomFreq: filter f ≥ 3v/(4·tubeLenM)
- เพิ่ม toggle 〰️ "แสดงภาพคลื่นในหลอด" (default on)
- **ก้นบีกเกอร์เปิด** — ลบ ellipse base, ผนังลงสุดขอบ canvas, น้ำใช้ linear gradient ลงไปขอบ canvas → ท่อจมหายไปใต้ canvas เป็นธรรมชาติ
- ขยายไม้บรรทัด 0–110 cm ตาม tubeLenM

**รอบ 4 — Challenge Mode**
- ปุ่ม **🎲 สุ่มความถี่ (Challenge Mode)** — สุ่ม f, ซ่อนจาก UI (`???`), disable select
- หลังบันทึก L₁,L₂ → คำนวณ f_วัด = v(T)/λ → เปรียบเทียบกับ f จริง → error %
- การ์ดผลลัพธ์ "🎯 ผลการ Challenge" 3 กล่อง: คุณวัดได้ / ค่าจริง / Error + verdict 4 ระดับ (🏆 <2% / ✅ <5% / 👍 <10% / ⚠️ ≥10%)

**รอบ 5 — แก้เสียงหายตอนกดบันทึก**
- ลบทุก `alert()` / `confirm()` (เพราะบล็อก JS thread → envelope `exp(-t/1.4)` ของส้อมเสียงดีเคย์จนหมด)
- ใช้ `flashHint()` แสดงข้อความ inline ไม่บล็อก audio context
- เพิ่ม **Step Indicator UI**: 2 ขั้นชัด (1/2 → 2/2) + dynamic button label + "↺ ยกเลิก L₁" + คำใบ้ตำแหน่ง λ/2

**รอบ 6 — 3-Step calculate flow + table comparison**
- เปลี่ยนเป็น 3 ขั้น: บันทึก L₁ → บันทึก L₂ → กด **🧮 คำนวณ** (ไม่คำนวณอัตโนมัติแล้ว)
- ปุ่มเปลี่ยน state ตามขั้น (ซ่อน rec, แสดง calc เมื่อพร้อม)
- ตารางบันทึก redesign per-cell 2-line:
  - **f (Hz)**: `มาตรฐาน: 384` (ฟ้า) / `วัด: 383.7` (เขียว) | Challenge mode: `🎲 สุ่ม:` แทน
  - **λ (m)**: `มาตรฐาน: 0.897` / `วัด: 0.898`
  - **error**: `f: 0.07%` / `λ: 0.07%` สีตามระดับ (เขียว/ฟ้า/เหลือง/แดง)
- CSV export 12 คอลัมน์: f_actual, f_measured, error_f, lambda_standard, lambda_measured, error_lambda, L1, L2, T, v_theory, mode

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/44. standing-waves-air-column.html` — refactor หลายรอบตาม feedback
- (kp-auth.js + _admin/admin.html — แก้ครั้งแรกแล้ว ไม่แก้เพิ่ม)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 44 ใน catalog page (`virtual-physics-lab-02.html`) + index Featured + library
- Demo Astronomy 13 ไฟล์จาก session ก่อนหน้า ยังไม่ขึ้น demo-astronomy.html

### หมายเหตุ
- Web Audio: oscillator + bandpass filter + gain envelope; gain modulated by `loudnessAtL(L,λ)` Gaussian (sigma 2.5 cm)
- Calculate flow ใช้ `state.partialL` schema ใหม่: `{f, L1, L2?}` — ถ้า L2 undefined = ขั้น 2 รอ; ถ้ามี = ขั้น 3 รอ calculate
- Challenge mode auto-exit หลัง calculate → fSel re-enable, hide ??? readout
- Verdict colors ใช้เกณฑ์เดียวกันใน Challenge result และ table error column

---

## [2026-05-13] — เครื่อง: ที่ทำงาน

### ทำอะไรไปบ้าง — Lab 43 ทฤษฎีบิกแบง (Big Bang Theory) · VPL02 · ครบจบ

**สร้างใหม่ + 3 รอบ redesign จากฟีดแบ็คผู้ใช้:**

**รอบที่ 1 — โครงสร้างพื้นฐาน (commit f18c4f7 / ab22f4c)**
- ไฟล์: `Virtual Physics Lab 02/43. big-bang-theory.html` (~106 KB)
- 3 Tabs: Simulation / วิธีการทดลอง · บันทึกผล / ทฤษฎี
- 4 sub-experiments:
  1. ไทม์ไลน์เอกภพ (15 era → 6 tier ตามตารางหนังสือ)
  2. กฎฮับเบิล (8 กาแล็กซี · spectrum Hα → z → v → H₀ → อายุ)
  3. BBN (n/p freeze + decay → Y(He))
  4. CMB Blackbody (Wien · Planck spectrum fit)
- รัน `protect_new_file.py` ✅ (GA, topbar, watermark, firebase, KP auth, access guard)
- Sync `kp-auth.js` (vpl02.labs += 'lab-43') และ `_admin/admin.html` (VLAB_SERIES + LAB_LIST)

**รอบที่ 2 — เพิ่ม Build Lab drag-drop (commit ab22f4c)**
- จากเดิมแค่ดูภาพ → ทำเป็นโหมด "ลากควาร์ก/อนุภาคเข้าช่อง" 7 recipes:
  - proton (u+u+d), neutron (u+d+d), pion (qq̄)
  - deuterium (p+n), helium-4 (2p+2n)
  - H atom (p+e⁻), He atom (⁴He+2e⁻)
- ตรวจคำตอบ + feedback อัจฉริยะ (ใส่ udd ตอนถาม proton → "นี่คือนิวตรอน ไม่ใช่โปรตอน")
- Drag/click จาก palette ลง slot · auto-check เมื่อ slot ครบ · reset ปุ่ม

**รอบที่ 3 — Simplify Exp 1 จาก "ดูยาก" (commit 06ee10b)**
- เปลี่ยน log slider (−43 ถึง +17.6) → **6 ปุ่มยุค** (Tier 1-6 ตามตารางหนังสือ)
- เปลี่ยนอนุภาคบินไปมา → **กริดการ์ด 13 อนุภาค** ใหญ่ ✓/×/· status
  - ✓ มี (เขียว) · × หายไป (แดง) · · ยังไม่เกิด (เทา)
  - คลิกการ์ดที่ buildable → เข้า Build Lab โดยตรง
- Banner ตามสี tier + story 1 ประโยค · Stepper 6 ขั้นคลิกได้

**รอบที่ 4 — Redesign tabs 2-4 (commit 30b5769)**
- **Tab 2 Hubble**: spectrum/plot จาก inset เล็กๆ → 2 panel เต็มความกว้าง
  - Top: spectrum (rainbow + λ_rest dashed + λ_obs solid + Δλ arrow + z/v calc box)
  - Mid: d-v plot ใหญ่ + fit line + H₀ + อายุเอกภพ + %error
  - Bottom strip: 8 thumbnail กาแล็กซีคลิกเลือก (✓ badge เมื่อบันทึก)
- **Tab 3 BBN**: random particles → **comic strip 3 ฉาก**
  - Frame 1: ดุลย์เคมี (12p + 12n, n/p=1)
  - Frame 2: Freeze-out (n/p drops to e^(−1.293/T_f))
  - Frame 3: Fusion (He clusters + free p, computed from mass fraction Y)
  - Bottom: H/He bar chart + pie + reference marker 75/25
- **Tab 4 CMB**: graph อย่างเดียว → **Mollweide sky map + Blackbody fit**
  - Top: ellipse projection · จุดน้ำเงิน/เหลือง เปลี่ยนตาม T · readout T ใหญ่กลางวงรี
  - ที่ T≈2.725 K → สี speckle เหมือน Planck satellite จริง
  - Bottom: blackbody curve + COBE/Planck data + success indicator "✅ ฟิตได้!"

**🐛 Bug fix รอบสุดท้าย (commit d21a6b9)**
- ปัญหา: Tab 4 slider ไม่ตอบสนอง — เลื่อนแล้วไม่มีอะไรเกิดขึ้น
- Root cause: ex3.init() throw error ที่ `arc radius -13` เพราะตอน DOMContentLoaded canvas ของแต่ละ tab ที่ซ่อนอยู่มี `clientWidth=0` → ตำแหน่งคำนวณเป็นลบ → exception → init sequence ขาด → ex4 listener ไม่ถูก attach
- แก้:
  - ex3.draw + ex4.draw มี guard `if(w<200||h<200) return;`
  - try/catch รอบ ex*.init() ใน DOMContentLoaded — failure ไม่กระทบลำดับถัดไป
  - Refactor ex4 slider เป็น setT() helper + direct event listener

### นำเข้าเว็บไซต์ (วันนี้ — commit หลัง d21a6b9)
- **virtual-physics-lab-02.html**: เพิ่ม section ใหม่ "🌌 ดาราศาสตร์ · จักรวาลวิทยา" + การ์ด Lab 43 (orange accent #fb923c)
- **library.html**: เพิ่ม lib-item Exp 43 ต่อจาก Exp 41 · เปลี่ยน count VPL02 จาก 13 → 14 files · เพิ่ม "Cosmology" ใน category subtitle
- **index.html**: เพิ่มการ์ด Lab 43 ในส่วน VPL02 ต่อจาก Exp 41 · CTA "ดูทั้ง 15 การทดลอง →"
- **Canvas preview animation** `vpl2-bigbang` (singularity ส้ม + 3 expanding rings + 6 รวมตาวจักรวาลกาแล็กซีถอยห่างพร้อม redshift hue) เพิ่มทั้งใน virtual-physics-lab-02.html และ index.html
- **Admin**: lab-43 อยู่ใน VLAB_SERIES.vpl02 + LAB_LIST `{id:'lab-43',label:'Lab 43 (ทฤษฎีบิกแบง)'}` (จาก commit ก่อนหน้า)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/43. big-bang-theory.html` — สร้างใหม่ + 4 รอบ redesign (~107 KB · ~3200 บรรทัด)
- `kp-auth.js` — เพิ่ม `'lab-43'` ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม `'lab-43'` ใน VLAB_SERIES + LAB_LIST entry
- `virtual-physics-lab-02.html` — section ดาราศาสตร์ใหม่ + preview function `vpl2-bigbang`
- `library.html` — lib-item Exp 43 + count + subtitle
- `index.html` — การ์ด Lab 43 + preview function `vpl2-bigbang`
- `SESSION_LOG.md` — entry นี้

### ค้างไว้ที่ไหน / ต้องทำต่อ
- พิจารณาเพิ่ม Part 1 (POE tab) หรือ Part 3 (แบบฝึกหัด tab) ถ้าผู้ใช้ต้องการ
- Lab 42 (เวอร์เนียร์·ไมโครมิเตอร์ใน VPL02) ยังไม่มีการ์ดในหน้าแคตาล็อก — รอเพิ่มภายหลัง

### หมายเหตุ
- Physics ที่อ้างอิงตรงจากภาพ "The Big Bang" ของผู้ใช้: T=2.725 K · Inflation ×10²⁷ · H 75% / He 25% · 4.6/23/72.4% · 13.7 Gy · matter-antimatter 1ppb · X-bosons 10⁻¹² s
- ตารางอนุภาคต่อยุค (Tier 1-6) ใช้ตามตารางหนังสือเรียนที่ผู้ใช้ส่งมา
- BBN formulas: n/p_freeze = exp(−1.293/T_f) · decay × exp(−τ/880s) · Y = 2(n/p)/(1+n/p)
- CMB: B(ν,T) = (2hν³/c²)/(exp(hν/kT)−1) · ν_peak = 5.879×10¹⁰·T Hz · Wien
- VPL01 มี lab-43 (SHM04) อยู่แล้ว — access string vlab:vpl01:lab-43 vs vlab:vpl02:lab-43 แยกกันตาม schema v4 ไม่ชนกัน
- Workflow แบ่ง main directory ↔ worktree — ทุกครั้งหลัง edit ต้อง cp ไฟล์ไปยัง worktree เพื่อให้ preview server เห็น (server รันจาก worktree)
