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
