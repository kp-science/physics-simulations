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

---

## [2026-05-15] — เครื่อง: ที่ทำงาน · Lab 45 (แบบจำลองการขยายตัวของเอกภพ) NEW

### ทำอะไรไปบ้าง — Lab 45 ใหม่ · VPL02 · กิจกรรม 1.2 (Balloon Universe Model)

สร้าง simulation ตามเอกสารกิจกรรม 1.2 ที่ผู้ใช้แนบมา (ภาพหนังสือเรียน) — ครบทุกขั้นตอนของวิธีทดลอง + 2 modes + ตารางบันทึก + กราฟ Hubble + ทฤษฎี

**ไฟล์:** `Virtual Physics Lab 02/45. expanding-universe-balloon.html` (~38 KB)

### โครงสร้าง 3 Tabs
- **Tab 1 Simulation**: Canvas balloon ขยายตัว (ellipse + grid pattern + tie) + 5 stickers (1 ref สีแดง + 4 กาแล็กซี ก/ข/ค/ง สีฟ้า) — ตำแหน่งตรงตาม textbook (ก r=2.0/35°, ข r=2.7/115°, ค r=4.0/200°, ง r=5.5/295°)
- **Tab 2 วิธีการทดลอง · บันทึกผล**: จุดประสงค์ · 4 ขั้นการทดลอง · ตัวอย่างตารางจากหนังสือ · Q1-Q3 + แนวคำตอบ
- **Tab 3 ทฤษฎี · อธิบาย**: Hubble's Law · ลูกโป่งเป็นแบบจำลอง 2D · สมการ H_balloon = (a-1)/Δt · Redshift visual (animated wave stretching) · ตารางเทียบ balloon↔universe จริง · ข้อจำกัด

### Features
- **2 Modes**: 
  - **Manual (default)**: คลิกอ้างอิง → คลิกกาแล็กซี → ระบบวาดเส้นวัด + แสดง dist บนหน้าจอ → ผู้ใช้กรอกค่าในตารางเอง · 4 step pills (เป่า1 → วัด d₁ → เป่า2 → วัด d₂+คำนวณ)
  - **Auto**: ปุ่ม "⚡ เริ่ม Auto" → ระบบเป่าครั้งที่ 1 → กรอก d₁ → เป่า 5 วินาที → กรอก d₂ → คำนวณ Δd,v + วาดกราฟ
- **ตัวแปรปรับได้**: เวลา Δt (1-10s · default 5) · อัตราขยาย a (1.2-3.0 · default 2.0) · จำนวนกาแล็กซี (3-6 · default 4)
- **Click-to-measure tool**: คลิก ref → คลิกกาแล็กซี → เส้นประเหลือง + กล่องระยะ
- **Animated balloon inflation**: easing smooth · scale linear ตาม dt
- **Hint อัตโนมัติ**: flash message guide ตาม stage (Reset/เป่า1เสร็จ/เป่า2เสร็จ/คำนวณเสร็จ + เทียบทฤษฎี)
- **CSV export** 12-column (d1, d2, Δd, v, Δt, a, mode, H_theory)
- **Graph v vs d₁**: linear best fit ผ่านจุด origin + R² + slope = H_balloon

### Verification (preview_eval)
ทดสอบ workflow เต็ม → ค่าตรงทฤษฎี:
- d₁ (autoFill): ก=2.0, ข=2.7, ค=4.0, ง=5.5 ✓ (ตรง textbook 100%)
- ที่ a=2.0 → d₂: ก=4.0, ข=5.4, ค=8.0, ง=11.0 (ideal scaling — textbook มี noise)
- ความชัน = 0.2000 /s ตรงทฤษฎี (a-1)/Δt = 1/5 = 0.2 ✓
- R² = 1.0000 (เส้นตรงสมบูรณ์) ✓

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/45. expanding-universe-balloon.html` — สร้างใหม่ + protect ✅
- `kp-auth.js` — เพิ่ม 'lab-45' ใน vpl02.labs
- `_admin/admin.html` — เพิ่ม 'lab-45' ใน VLAB_SERIES.vpl02 + LAB_LIST entry `{id:'lab-45',label:'Lab 45 (แบบจำลองการขยายตัวของเอกภพ)'}`
- `SESSION_LOG.md` — entry นี้

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 45 ใน `virtual-physics-lab-02.html` (catalog) + `index.html` Featured + `library.html`
- ยังไม่ได้สร้าง canvas preview animation สำหรับ Lab 45 (suggest: balloon expanding with galaxy dots receding)
- Lab 42 (เวอร์เนียร์·ไมโครมิเตอร์) จาก session ก่อนยังไม่มีการ์ดเช่นกัน
- Demo Astronomy 13 ไฟล์ค้างจาก session เก่า ยังไม่ขึ้น catalog
- ยังไม่ได้ push git

### หมายเหตุ
- Physics ตรง textbook 100%: v = H₀·d (Hubble's Law) · d₂ = a·d₁ → Δd = (a-1)·d₁ → v = (a-1)/Δt × d₁ → H_balloon = (a-1)/Δt
- Galaxy positions in polar coords, ref at (0,0) origin · physical position = a × (x,y) → distances scale linearly with a → perfect Hubble's Law
- Idealized scaling (no noise) ทำให้นักเรียนเข้าใจหลักการก่อน แล้วค่อยเปรียบเทียบกับ textbook ที่มี measurement noise
- Color theme: orange #fb923c (astronomy/cosmology) — เดียวกับ Lab 43 (Big Bang) เพื่อสร้าง cluster cosmology
- ลูกโป่งวาดเป็น ellipse + radial gradient + grid lines (latitude/longitude) + tie ที่ก้น
- Sticker = 1×1 cm square (ตามขนาดในเอกสาร) แสดง label ก/ข/ค/ง/อ้าง
- Stars background (60 pseudo-random points) + ruler ที่มุมล่างซ้าย (0-5 cm)
- Watermark "KP Science" บัง canvas เล็กน้อยตาม default ของระบบ — ปลดล็อกด้วย kp_access_tier
- Verification: Hubble fit ผ่าน origin force-through (เพราะ v=0 ที่ d=0)

### [2026-05-15 ต่อ] — เพิ่มการ์ด Lab 45 เข้า catalog ทั้ง 3 หน้า + preview animation

**ไฟล์ที่แก้:**
- `virtual-physics-lab-02.html` — เพิ่มการ์ด Lab 45 ในส่วน "ดาราศาสตร์ · จักรวาลวิทยา" (ต่อจาก Lab 43) · เปลี่ยน topic count `1 simulations → 2 simulations` · เพิ่ม renderer `'vpl2-expand'`
- `index.html` — เพิ่มการ์ด Lab 45 ใน VPL02 Featured (ต่อจาก Lab 43) · CTA `"ดูทั้ง 15 → 16 การทดลอง →"` · เพิ่ม renderer `'vpl2-expand'`
- `library.html` — เพิ่ม `lib-item` Exp 45 (ต่อจาก Exp 43) · `lib-cat-count` `14 → 15 files`

**Preview renderer `vpl2-expand`** (เหมือนกันใน 2 ไฟล์):
- พื้น space + starfield 40 ดวง (twinkle)
- ลูกโป่ง ellipse pulsing scale a = 0.55–1.0 (period 5s) · radial gradient ส้ม→ชมพู→ม่วง · grid lines latitude (5 เส้น) · tie ที่ก้น
- กาแล็กซีอ้างอิง (จุดสีแดง) ตรงกลางบนของลูกโป่ง
- 4 กาแล็กซีรอบๆ (sticker สีฟ้า) ระยะถอยห่างตาม a × dist
- ลูกศรความเร็ว Hubble flow (hue ต่างกันตาม direction — redshift effect 0–200°)
- ลูกศร length ∝ ระยะ × (0.3+a) — กาแล็กซีไกล/ลูกโป่งโต → ลูกศรยาว

**Verification (preview_eval):**
- VPL02 catalog: Card render ครบ · pixel center (179,157,155) = สีลูกโป่ง · pixel mid (68,40,43) = ลูกโป่งโทนเข้ม ✓
- index.html: หลังกด tab VPL02 → Canvas 641×280 · center pixel (220,38,38) = สีกาแล็กซีอ้างอิง (red) ✓
- library.html: Lab 45 entry + count 15 files ✓
- CTA text "ดูทั้ง 16 การทดลอง →" ตรงตามที่แก้ ✓

### สรุปงาน Lab 45 ที่ทำเสร็จในวันนี้ (2026-05-15)

| Component | Status |
|---|---|
| ไฟล์ Lab 45 หลัก + 3 tabs + 2 modes | ✅ |
| Protect (GA, watermark, auth, access guard) | ✅ |
| kp-auth.js + admin LAB_LIST sync | ✅ |
| VPL02 catalog การ์ด + count | ✅ |
| index.html Featured การ์ด + CTA | ✅ |
| library.html entry + count | ✅ |
| Preview animation `vpl2-expand` × 2 ไฟล์ | ✅ |
| Verification ด้วย preview_eval (pixel sampling) | ✅ |

### ค้างไว้ / ต้องทำต่อ
- Lab 42 (vernier-micrometer) ใน VPL02 ยังไม่มีการ์ดในแคตาล็อก (ค้างจาก session ก่อน)
- Lab 44 (standing-waves-air-column) ค้างจาก session ก่อน — ยังไม่มีการ์ดในแคตาล็อก (เคยใส่แล้วหรือยัง? ต้องเช็คอีกครั้ง)
- Demo Astronomy 13 ไฟล์เก่า ยังไม่ขึ้น demo-astronomy.html
- ยังไม่ได้ push git

### หมายเหตุ
- Bug ที่ค้นพบในระหว่างทาง: ใน `library.html` มี VPL01 entries (Exp 21, 42, 43, 44) ถูกใส่ผิดในส่วน VPL02 — ค้างจาก session ก่อน ไม่ใช่ของวันนี้ ยังไม่แก้
- Index.html ใช้ tab system แบ่ง VPL01/VPL02 panels — `vpl2-panel` อยู่ใน `display:none` จนกว่าจะคลิก tab → canvas จะ init ก็ต่อเมื่อ panel visible
- Preview screenshot tool มีปัญหา viewport position แต่ pixel sampling ผ่าน preview_eval ยืนยันว่า renderer ทำงานทุก canvas
- `vpl2-expand` ใช้ pure 2D canvas (~85 lines) ไม่มี dependency · period 5s pulse แบบ smooth cosine

## [2026-09-05 01:30] — เครื่อง: (ไม่ระบุ) · NEW series VPL03 + Lab 1 การวัดอย่างละเอียด 3D

### ทำอะไรไปบ้าง
- อ่าน PDF `514108-514113-lab1.pdf` (คู่มือปฏิบัติการฟิสิกส์ เล่ม 1 ม.ศิลปากร หน้า 21–27: การทดลอง 1 การวัดอย่างละเอียด) แล้วออกแบบ simulation 3D ตามคู่มือครบทุกตอน
- **สร้าง series ใหม่ `Virtual Physics Lab 03/`** (ปฏิบัติการฟิสิกส์ระดับมหาวิทยาลัย) เพราะเนื้อหาเป็นคนละระดับกับ VPL01/02 — ไฟล์แรก `1. precision-measurement-3d.html` (≈117 KB, access `vlab:vpl03:lab-1`)
- Simulation: three.js r128 (cdnjs) วาดเวอร์เนียร์คาลิปเปอร์ (สเกลหลัก 0–150 mm, เวอร์เนียร์ 20 ช่อง/39 mm → 0.05 mm) + ไมโครมิเตอร์ (pitch 0.5 mm, thimble 50 ช่อง → 0.01 mm, กรอบสีฟ้าตามรูปที่ 7) + วงแหวนโลหะ (washer) ที่ไม่กลมสมบูรณ์ (ปรับ "ความไม่กลม" ได้ 0–0.10 mm) · orbit/zoom เอง (ไม่ใช้ OrbitControls) · ปุ่มมุมหน้า/เฉียง/ซูมสเกล
- **แว่นขยายสเกล 2D** (canvas) = ภาพขยายสเกลจริงที่ตำแหน่งปัจจุบัน ใช้อ่านค่า — โหมด Manual (ดีฟอลต์) ซ่อนลูกศร ให้หาขีดที่ตรงเอง → กรอกสเกลหลัก+ขีด → ✅ ตรวจ (±1 ขีด) → 💡 คำใบ้ 2 ระดับ / 👁 เฉลย → ➕ บันทึก (บันทึกได้เฉพาะเมื่อ "แตะพอดี") · โหมด Auto อ่านให้ + วัดครบชุดอัตโนมัติ
- การทดลองตามคู่มือ: ตอนที่ 1 เวอร์เนียร์วัด D (เขี้ยวนอก) และ d (เขี้ยวใน) อย่างละ 3 ครั้ง (หมุนวงแหวนทุกครั้ง) · ตอนที่ 2 ไมโครมิเตอร์ ตรวจขีดศูนย์ d (สุ่ม −0.03…+0.04 / กำหนดเอง / 0; ขีด 0 เหนือเส้น = ลบ, ใต้เส้น = บวก ตามรูป 9–10) แล้ววัดความหนา t 3 ครั้ง → t = t̄ − d · เสียง "กริ๊ก" ratchet (WebAudio)
- Output: ตารางแยกตอน (θ, สเกลหลัก, ขีด, ค่า, สถานะ ✅/👁/⚡) · x̄, Δx̄ = Σ|xᵢ−x̄|/N (ถ้า 0 ใช้ least count), σ · กล่องรายงาน · dot-plot การกระจาย · CSV / คัดลอกรายงาน · เปรียบเทียบกับขนาดจริง (% error) · progress + streak (motivation layer)
- Tab วิธีการทดลอง: วัตถุประสงค์/อุปกรณ์/วิธีใช้ sim/ขั้นตอนตอนที่ 1–2/รูปแบบตารางบันทึกผล+ตัวอย่างคำนวณ/คำถามท้ายการทดลอง
- Tab ทฤษฎี (วิชวล): canvas โต้ตอบหลักเวอร์เนียร์ 10 ช่อง (รูป 1–3, slider), สมการ (1)–(4) + ตัวอย่าง 20V=39S, รูปที่ 5 (9.15 mm), แผนภาพส่วนประกอบคาลิปเปอร์ (รูป 6) และไมโครมิเตอร์ A B C F H L R S T (รูป 7), canvas ไมโครมิเตอร์โต้ตอบ (6.480 mm), รูป 9–10 ความคลาดเคลื่อนขีดศูนย์, การรายงาน x̄ ± Δx̄, precision vs accuracy
- ตรวจตัวเลขทั้งหมดเทียบ PDF แล้ว: S/n = 1/20 = 0.05 mm · 9.0 + 3×0.05 = 9.15 · 0.5/50 = 0.01 · 6.0 + 48×0.01 = 6.480 · d เหนือเส้น = ลบ
- Verify ใน browser (python http.server 8765): 3D render, snap/rotate tween, manual check/record/hint, zero-check flow (d=+0.01 → t = 3.130 ± 0.010), autoSeries, stats, revealTruth, theory canvases ✓ · ไม่มี console error หลังแก้

### ไฟล์ที่แก้
- `Virtual Physics Lab 03/1. precision-measurement-3d.html` — NEW (GA + frame protection + topbar + watermark + firebase/kp-auth + guard → redirect `../index.html`)
- `kp-auth.js` — เพิ่ม `VLAB_SERIES.vpl03` (labs: lab-1) · `vlab:vpl03:*` ใน presets member/pro/premium + `ANONYMOUS_ACCESS_FALLBACK` · legacy labs mapping รองรับ vpl03
- `_admin/admin.html` — เพิ่ม vpl03 ใน VLAB_SERIES / presets / anonymous fallback ทุกจุด / legacy mapping / legacyLabs loop (`['vpl01','vpl02','vpl03']`) — **ไม่ได้เพิ่มใน `LAB_LIST`** เพราะ id `lab-1` ซ้ำกับ VPL01 (LAB_LIST เป็น legacy flat list); UI v4 ใช้ VLAB_SERIES อยู่แล้ว
- `_admin/protect_new_file.py` — รองรับโฟลเดอร์ `Virtual Physics Lab 03/` (access string, watermark, auth guard; redirect ไป index.html จนกว่าจะมี catalog)
- `CLAUDE.md` — เพิ่มบรรทัดโครงสร้าง VPL02/VPL03

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ⚠️ **สำคัญ:** Firestore `settings/public.anonymous_access` บนเว็บจริงยังมีแค่ vpl01/vpl02 → ผู้เข้าชมทั่วไปจะถูก guard redirect (`index.html?locked=vlab:vpl03:lab-1`) — ต้องเข้า admin panel → การ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" → กด preset/กำหนดเอง ให้มี `vlab:vpl03:*` แล้วบันทึก (ทดสอบในเครื่องเจอ redirect จริง)
- ยังไม่มีหน้า catalog `virtual-physics-lab-03.html` และยังไม่ได้ใส่การ์ดใน index.html / library.html (เมื่อสร้างแล้วให้แก้ redirect ใน protect_new_file.py + guard ในไฟล์ Lab 1)
- ยังไม่ commit/push git (ดู `git status` — มี VPL03 folder ใหม่ + 4 ไฟล์แก้)
- ค้างจาก session ก่อน: การ์ด Lab 42/44 ใน catalog VPL02, Demo Astronomy 13 ไฟล์, library.html VPL01 entries ผิดหมวด

### หมายเหตุ
- Lab 42 ใน VPL02 เป็นหัวข้อเดียวกันแต่เป็น 2D ระดับ ม.ปลาย — Lab 1 VPL03 อิงคู่มือมหาวิทยาลัย (วงแหวนโลหะ D/d/t, ตรวจขีดศูนย์, Δx̄ แบบ mean absolute deviation)
- โมเดล 3D ทำจาก primitives + CanvasTexture (สเกลบนคาน/สไลเดอร์/sleeve/thimble) — ตัวเลขบน thimble ใน 3D อ่านยากตามธรรมชาติ ให้ใช้แว่นขยายเป็นหลัก (เหมือนรูปที่ 7 ที่มีแว่นขยายตรง C)
- tween ใช้ setInterval (ไม่ใช่ rAF) + `cancelTweens()` เมื่อเปลี่ยนเครื่องมือ — แก้บั๊ก tween ค้างข้ามเครื่องมือที่เจอตอนทดสอบ
- ขากรรไกรเลื่อนทะลุวัตถุไม่ได้ (opening ≥ dim) · ค่าที่อ่านถูก quantize เป็น 0.05 / 0.01 · ค่าจริงในตอนเฉลย = ค่าเฉลี่ยรอบวง (D₀, d₀, t₀)
- Preview screenshot tool: ต้อง `tabs_select` ก่อน screenshot และใช้ `resize_window` 1280×2300 แทนการ scroll (scroll แล้วภาพดำ)

### [2026-09-05 ต่อ] — ปรับ Lab 1 VPL03 ตาม feedback: ลากในภาพ 3D ได้ + วงแหวนชิดปากวัด
- **ลากในภาพ 3D โดยตรง** (raycast + ระนาบ z): ลากสไลเดอร์คาลิปเปอร์ / กระบอกหมุนหรือแกนไมโครมิเตอร์ = เลื่อนปากวัด (Shift = ละเอียด ×0.1) · ลากวงแหวน = หมุน θ · ลากที่ว่าง = หมุนมุมมอง · cursor เปลี่ยนตามชิ้นที่ชี้ · รองรับ touch
- เลื่อนเข้าหาวัตถุแล้ว "หยุด" ที่ระยะสัมผัสพอดี (clamp opening ≥ dim) → แตะพอดี + feedback
- **วงแหวนวางชิดปากวัดฝั่งคงที่ (x = 0) เสมอ** ปากเลื่อนมาชน (เดิมวงแหวนลอยกลางระหว่างปาก) · เขี้ยวในสูงขึ้น (y 8–38) และเยื้อง z ±0.2–2.7 ให้วงแหวนสวมรอบเขี้ยวจริง · กล้อง front/iso เล็งต่ำลงให้เห็นวงแหวนครบ
- ไฟล์ที่แก้: `Virtual Physics Lab 03/1. precision-measurement-3d.html` เท่านั้น · verify: drag slider 44.24→38.24 (หยุดที่สัมผัส), drag thimble หยุดที่ t, drag ring θ=41° แล้ว contact หลุดตามจริง
- commit + push แล้ว

### [2026-09-05 ต่อ 2] — Lab 1 VPL03: แก้ไมโครมิเตอร์วัดความหนาจริง · โมเดลคาลิปเปอร์ใหม่ · เพิ่มก้านวัดความลึก
- **บั๊กไมโครมิเตอร์:** วงแหวนถูกหมุน Y 90° ซ้ำ 2 ครั้ง (geometry + mesh) → หน้าวงแหวนหันเข้ากล้อง ดูเหมือนวัดตามรัศมี → แก้ให้หมุนที่ geometry ครั้งเดียว วงแหวนตั้งแกนตาม x หน้าแบนชิดแป้น A แกน B ชนอีกหน้า = วัดความหนา t
- **คาลิปเปอร์ใหม่ตามรูปที่ 6:** หัวคงที่ + เขี้ยวนอกเรียวปลายเหลี่ยม (ExtrudeGeometry จาก polygon) · เขี้ยวในปลายแหลมคม โค้งด้านนอก คมวัดที่ x=0 / x=opening เยื้อง z กัน · สไลเดอร์มีแผ่นเวอร์เนียร์หน้า แผ่นหลัง สะพานคร่อมคาน ฝาปิดปลาย เกลียวยึด + หัวสกรู ปุ่ม S (roller) · ก้านวัดความลึกโผล่ปลายคาน
- **เพิ่มการวัดที่ 3 ของเวอร์เนียร์: ความลึกร่อง h (depth bar)** — บล็อกทองเหลืองมีร่อง (ผิวบนที่ x=175 ปลายคานวางบน ร่องลึก h ตาม +x) · preset A/B/C มี h, สุ่ม, กำหนดเอง (ch) · records.depth, ตาราง/สถิติ/กราฟ/CSV/เฉลย/progress (5 การ์ด) รองรับ · ปุ่ม 🔄 เปลี่ยนเป็น "เปลี่ยนจุดวัด" · ลากบล็อก = เปลี่ยนจุด · เป็นส่วน "เสริม" นอกคู่มือ (คู่มือมีเฉพาะ D, d)
- กล้องมุมหน้า/เฉียงของ outer เล็งต่ำลง (−26, dist 265/270) ให้เห็นวงแหวนครบ
- verify: 4 มุมมอง (outer/inner/depth/micro-thick) render ถูกต้อง ไม่มี console error ใหม่ · commit + push

### [2026-09-05 ต่อ 3] — Lab 1 VPL03: เลือกความละเอียดเวอร์เนียร์ได้ (0.05 / 0.02 / 0.1 mm)
- เพิ่ม `VTYPES` + dropdown "ความละเอียด" (แสดงเฉพาะโหมดเวอร์เนียร์): 0.05 mm (20 ช่อง/39 mm ตามคู่มือ · ดีฟอลต์), **0.02 mm (50 ช่อง/49 mm ที่โรงเรียนใช้)**, 0.1 mm (10 ช่อง/9 mm)
- ทุกจุดที่เคย hard-code 0.05 เปลี่ยนเป็น `lcV()` / `vt().n` / `vDiv()`: trueReading, decompose, ตรวจคำตอบ (tolerance ±1 ขีด), คำใบ้, label ช่องกรอก, รายงาน, สถิติ fallback, กราฟ, แว่นขยาย (n, V, window, labels) และ texture สเกลบนสไลเดอร์ 3D (regenerate เมื่อเปลี่ยนชนิด) · สไลเดอร์กว้างขึ้นเป็น 58 mm รองรับเวอร์เนียร์ 49 mm
- verify: 0.02 mm → อ่าน 38 + 12×0.02 = 38.24 (ค่าจริง 38.237) ✓ · เพิ่มข้อความใน tab วิธีการทดลอง/ทฤษฎีเรื่อง 1/50 = 0.02 mm
- commit + push

### [2026-09-05 ต่อ 4] — Lab 1 VPL03: โมเดลของแข็ง "วัตถุอยู่นิ่ง ผู้วัดขยับเครื่องมือ" (ตาม feedback ครู)
- เครื่องมือ**เริ่มที่ 0** (ปากปิดสนิท) และมีตำแหน่ง `state.pos` ลากตัวเครื่องมือ (คาน/หัว/กรอบ) เพื่อย้ายได้ทั้ง x,y · ลากสไลเดอร์/กระบอกหมุน = เปิด-ปิดปากวัด · วัตถุ (วงแหวน/บล็อก) อยู่นิ่งใน world
- **ระบบชน 2D** (`objSolid`, `toolParts`, `validCfg`, `moveParam`): ทุกชิ้นส่วนเป็นกล่อง/วงกลม ห้ามทับซ้อน · `moveParam` กวาดทีละ ≤ 0.4 mm แล้ว binary-search หาผิวสัมผัส (ไม่กระโดดข้ามวัตถุ) · `ensureValid` ถอยออกเมื่อหมุนวงแหวนแล้วขนาดโตขึ้น
- **ลำดับการวัดจริง:** D = กางปาก → ครอบคาลิปเปอร์ลงจากด้านบน → ดันเขี้ยวคงที่ชน → ปิดสไลเดอร์จนชน · d = วงแหวน**วางนอนตั้งฉาก**เหนือคาลิปเปอร์ (geometry rotateX −90°) → เลื่อนเขี้ยวในไปใต้รู → ยกสอดเข้ารู → เปิดเล็กน้อย → ดันซ้ายชนผนัง → เปิดจนชนอีกด้าน · h = เริ่ม 0 ปลายคานบนบล็อก → ดึงก้านออกจนชนก้นร่อง · t = เปิดแกน B → ยกไมโครมิเตอร์รับขอบวงแหวน → ดันขวาจนแป้น A ชน → ปิดจนชน (กริ๊ก)
- "แตะพอดี" = ผิววัดทั้งสองด้านสัมผัสวัตถุ (ตำแหน่ง + ระยะเปิดตรง `contactCfg` ±0.006 mm) · ปุ่ม 🎯 = `runSeq(contactSeq())` ทำลำดับข้างต้นอัตโนมัติผ่านระบบชน · Auto = `applyCfg(contactCfg())`
- เขี้ยวในสูงขึ้น (y 8–40) · บล็อกร่องย้ายไปอยู่ใน scene (ไม่ติดคาลิปเปอร์) · HUD แสดงขั้นตอนต่อการวัด · tab วิธีการทดลองปรับตาม
- verify (moveParam ตรง ๆ): D หยุดที่ 25.882/38.237 ✓ contact · d 32.295/25.411 ✓ · h 12.330 ✓ · t 10.000/3.131 ✓ · ปิดสนิทลากเข้าวงแหวน → ถูกบล็อก ✓ · ยกเขี้ยวเข้าเนื้อวงแหวน → ถูกบล็อก ✓
- ⚠️ tween ใช้ setInterval → ในแท็บที่ถูกซ่อน Chrome throttle เหลือ 1 ครั้ง/วินาที (ลำดับ 🎯 ช้าลง) — ใช้งานจริงในแท็บที่เปิดอยู่ไม่กระทบ
- commit + push

## [2026-09-05 12:30] — เครื่อง: (ไม่ระบุ) · VPL03 Lab 1 v1.6 — ตรวจปัญหา "ลากไม่ได้" + ปรับ UX การจับชิ้นส่วน

### ทำอะไรไปบ้าง
- ผู้ใช้แจ้ง "มันเลื่อนไม่ได้" → ตรวจแล้ว: ไฟล์บนเว็บ = ในเครื่อง (diff SAME), ลากด้วยเมาส์จริงในเบราว์เซอร์ทดสอบได้ปกติ (คานเลื่อน / สไลเดอร์เปิด / ชนวงแหวนแล้วหยุด) — สาเหตุที่น่าจะเป็น: มุมมองเริ่มต้นเป็นมุมเฉียง ชิ้นส่วนบาง ลากพลาดไปโดนที่ว่าง → กลายเป็นหมุนกล้อง หรือ cache เก่า
- v1.6: มุมมองเริ่มต้น = มุมหน้า (และรีเซ็ตเป็นมุมหน้าทุกครั้งที่เปลี่ยนสิ่งที่วัด) · จับชิ้นส่วนแบบ "อ้วน" (สุ่ม ray รอบเมาส์รัศมี ≤ 28 px) · เมื่อลากโดนที่ว่างจะมีป้าย "🔄 กำลังหมุนมุมมอง — ให้จับที่ตัวเครื่องมือ" · เมื่อการลากถูกบล็อกเพราะชน ป้ายมุมขวาบนขึ้น "⛔ ชนวัตถุ" 1.6 วิ · เพิ่ม meta no-cache + badge เวอร์ชัน (v1.6 · 2569-09-05) + console.log build
- (ก่อนหน้าใน session เดียวกัน) v1.5 rigid-body: วัตถุอยู่นิ่ง เครื่องมือเริ่ม 0 ลากตัวเครื่องมือ (x,y) ได้ ทุกชิ้นชนกันไม่ทะลุ (moveParam sweep 0.4 mm + binary search) · outer: ครอบจากด้านบน · inner: วงแหวนวางนอน สอดเขี้ยวขึ้นเข้ารู เปิดเล็กน้อยก่อนดันชนผนัง · depth: เริ่ม 0 ลากก้านออกชนก้นร่อง · micro: ยกไมโครมิเตอร์รับขอบวงแหวน ดันขวาให้ A ชน ปิด B · ปุ่ม 🎯 = ลำดับอัตโนมัติผ่านการชน · เลือกความละเอียดเวอร์เนียร์ 0.05/0.02/0.1

### ไฟล์ที่แก้
- `Virtual Physics Lab 03/1. precision-measurement-3d.html` — v1.6 (ดูด้านบน)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอผู้ใช้ยืนยันว่าลากได้แล้วบนเครื่อง/อุปกรณ์จริง (ถาม: เบราว์เซอร์อะไร, iPad หรือ Mac, badge บนหน้าแสดง v1.6 หรือไม่)
- ยังไม่ได้ทำ catalog VPL03 / การ์ด index-library / anonymous_access ใน Firestore (ดู entry ก่อนหน้า)

### หมายเหตุ
- ทดสอบด้วย computer left_click_drag ต้องคำนวณพิกัดจาก state ปัจจุบัน (หลัง orbit ตำแหน่งบนจอเปลี่ยน) — ครั้งแรกที่คิดว่า pick พลาดคือพิกัดผิดเอง ไม่ใช่บั๊ก

## [2026-09-13 10:30] — เครื่อง: (ไม่ระบุ) · เมนูทางลัดหน้าแรก + VPL03 เข้าถึงได้จากเว็บ

### ทำอะไรไปบ้าง
- **index.html**: เพิ่ม "🚀 ไปที่ต้องการทันที" (quick menu) ไว้บนสุดใต้ topbar ก่อน hero — 5 ปุ่ม: Demo / VPL01 / VPL02 / VPL03 (NEW) / Library → เห็นทันทีไม่ต้องเลื่อน (ผู้ใช้บอกว่าใช้งานจริงต้องเลื่อนหา lab ยุ่งยาก) · responsive 2 คอลัมน์บนมือถือ
- index.html: เพิ่ม tab "📐 VPL 03 · ปฏิบัติการ ม. (3D)" ใน section Virtual Lab + การ์ด Lab 1 (preview canvas `vpl3-caliper` วาดคาลิปเปอร์เลื่อนปาก) + รายการใน Collections accordion · `openVPL3()` สลับ tab + scroll · รองรับ `#vpl3-panel` ใน URL
- **library.html**: เพิ่มหมวด Virtual Physics Lab 03 (`data-cat="vlab3"`) + รายการ Lab 1
- แก้บั๊กเก่า library.html: `\!==` (escaped) ใน script ดาวน์โหลด → SyntaxError ทั้ง script (มีมาก่อน session นี้) แก้เป็น `!==` แล้ว node --check ผ่านทุก script
- Lab 1 VPL03 ก่อนหน้านี้ (2026-09-05): v1.2–v1.6 — ลากในภาพ 3D, โมเดลคาลิปเปอร์ใหม่ + วัดความลึก, ไมโครฯ วัดความหนา, เลือกความละเอียด 0.05/0.02/0.1, โมเดลของแข็ง (วัตถุนิ่ง ลากเครื่องมือ ชนไม่ทะลุ), front view + จับง่าย + ป้ายเวอร์ชัน (บันทึกใน commit log)

### ไฟล์ที่แก้
- `index.html` — quick menu CSS/HTML, VPL03 tab+panel+card, accordion item, `openVPL3()`, preview sim `vpl3-caliper`
- `library.html` — หมวด VPL03 + แก้ `\!==`
- `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ⚠️ การ์ด VPL03 ยังแสดง "สมาชิกเท่านั้น" สำหรับผู้ไม่ login ถ้า Firestore `settings/public.anonymous_access` ยังไม่มี `vlab:vpl03:*` → admin ต้องเพิ่มใน admin panel
- ยังไม่มีหน้า catalog `virtual-physics-lab-03.html` (ตอนนี้ปุ่ม VPL03 ในเมนูพาไป tab ในหน้าแรก)

### หมายเหตุ
- quick menu ใช้ `color-mix()` — Safari ≥16.2 / Chrome ≥111 รองรับ

## [2026-09-13 12:30] — เครื่อง: (ไม่ระบุ) · Virtual Lab จัดตามบทเรียน สสวท. (ระดับหน้าเว็บ)

### ทำอะไรไปบ้าง
- ผู้ใช้ต้องการเลิกใช้ชื่อ "Lab 01/02/03" ในการจัดกลุ่ม → ตัดสินใจ **ปรับเฉพาะหน้าเว็บ (ระดับ 1)** เฉพาะส่วน Virtual Lab (ไม่แตะ Demo) ยึดบทเรียนตามหลักสูตร สสวท. · ไฟล์/โฟลเดอร์/access string `vlab:vplXX:*` คงเดิมทั้งหมด (ไม่กระทบ URL ที่แชร์และสิทธิ์ใน Firestore)
- **`_admin/labs_data.py`** (ใหม่) — ข้อมูลกลาง 46 labs: access, href, เลข, ชื่อไทย, คำอธิบาย, บทเรียน (11 หัวข้อ), ระดับ (ม.4/5/6/ป.ตรี), ชุด, tags · 3 กลุ่มใหญ่ (กลศาสตร์ 28 · คลื่น-เสียง-แสง 16 · ดาราศาสตร์ 2)
- **`_admin/build_virtual_lab.py`** (ใหม่) — generate `virtual-lab.html` + เขียนหมวด Virtual Lab ใน `library.html` ใหม่ + รัน protect_new_file อัตโนมัติ
- **`virtual-lab.html`** (ใหม่) — catalog รวมทุกชุด: กลุ่ม → บทเรียน → การ์ด (เลข Exp/Lab, ระดับ, ป้ายชุด VPL) · filter bar sticky (กลุ่ม/บทเรียน/ระดับ/ค้นหา) · deep link `?level=uni` `?topic=` `?group=` `?q=` `#g-mech` · ลิงก์ "ดูแบบชุดเดิม" ไป VPL01/02 · kp-auth lock ทำงาน
- **index.html** — quick menu เปลี่ยนเป็น 6 ปุ่ม: Demo · Lab กลศาสตร์ · Lab คลื่น-เสียง-แสง · Lab ดาราศาสตร์ · ปฏิบัติการ ม.(3D) · Library (ลิงก์ไป virtual-lab.html#g-… / ?level=uni) · section Virtual Lab: ยุบ 3 tab ชุด → grid เดียว 19 การ์ด + chips กรองตามบทเรียน (`filterVLab`) + ปุ่ม "ดูทั้ง 46 การทดลอง" + ปุ่มรอง "ชุด VPL 01/02" · Collections accordion เพิ่ม "Virtual Lab ทุกชุด — จัดตามบทเรียน" · `openVPL3()`/`#vpl3-panel` ยังใช้ได้ (map → กรอง "การวัด")
- **library.html** — หมวด Virtual Lab 01/02/03 (3 หมวด, มีรายการซ้ำ SHM และขาด Exp 42/44) → หมวดเดียว "Virtual Physics Lab" 46 รายการ แบ่ง lib-sub ตาม 11 บทเรียน (generated)
- ตรวจ: node --check ทุก inline script ผ่าน · headless Chrome: virtual-lab.html 46 การ์ด/11 บทเรียน/3 กลุ่ม, filter ?level=uni → 1/46, group=wave + ค้น "เลนส์" → 2/46 · หน้าแรก quick menu 6 ปุ่ม, chips 9 อัน

### ไฟล์ที่แก้
- `virtual-lab.html` (ใหม่, generated) · `_admin/labs_data.py` (ใหม่) · `_admin/build_virtual_lab.py` (ใหม่)
- `index.html` — quick menu, VPL section, accordion, JS `filterVLab`
- `library.html` — หมวด Virtual Lab (generated block)
- `CLAUDE.md` — โครงสร้าง + กติกา "เพิ่ม lab ใหม่ = แก้ labs_data.py แล้ว build"

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ⚠️ ทดสอบ in-app browser ไม่ได้ในรอบนี้ (มี popup Google sign-in ค้างอยู่ใน Browser pane ที่ agent ปิดไม่ได้) → ใช้ headless Chrome แทน · ควรเปิดดูจริงอีกครั้งบนมือถือ
- หน้า `virtual-physics-lab-01.html` / `-02.html` (catalog แบบชุด) ยังคงอยู่และยังไม่มี Lab 42/44 ของ VPL02 ในหน้า index cards (มีใน virtual-lab.html แล้ว)
- ยังไม่ได้เพิ่ม `vlab:vpl03:*` ใน Firestore anonymous_access (งานของ admin)

### หมายเหตุ
- ถ้าจะทำ "ระดับ 2" (สิทธิ์แบบ topic:*) หรือ "ระดับ 3" (ย้ายไฟล์ตามหัวข้อ) ในอนาคต — labs_data.py คือจุดเริ่มต้น (มี topic ของทุก lab แล้ว)

## [2026-09-13 13:10] — เครื่อง: (ไม่ระบุ) · admin panel แสดง lab ตามบทเรียน (แสดงผลเท่านั้น)

### ทำอะไรไปบ้าง
- `_admin/admin.html`: modal แก้สิทธิ์ (vlab + manual) ส่วน "▾ เลือกเฉพาะ lab" เดิมเป็น checkbox `L1 L2 …` → ใหม่ `renderLabsByTopic()` จัดกลุ่มตามบทเรียน สสวท. แสดง เลข + ชื่อไทย + ระดับ (tooltip = access string) · ค่า `data-access` ยังเป็น `vlab:vplXX:lab-N` เดิม → สิทธิ์สมาชิกเก่าไม่กระทบ, `onAccessChange()`/bundle logic ไม่แตะ
- `_admin/build_virtual_lab.py`: เพิ่ม `build_admin_meta()` ฝัง `LAB_META` (46) + `TOPIC_META` (11) ระหว่าง marker `/* ── LAB_META … ── */` ใน admin.html (regenerate ได้ซ้ำ)
- ตรวจ: node --check ทุก script ใน admin.html ผ่าน · ทุก lab ใน VLAB_SERIES (vpl01/02/03) มี meta ครบ · จำลอง render vpl01 → 7 กลุ่ม / 26 checkbox / ชื่อไทยขึ้นถูก
- **ยังไม่ได้ทดสอบเปิด admin panel จริง** (ต้อง login admin) → ผู้ใช้ควรเปิดดู modal สิทธิ์ 1 ครั้ง

### ไฟล์ที่แก้
- `_admin/admin.html` — LAB_META/TOPIC_META (generated) + `renderLabsByTopic()`
- `_admin/build_virtual_lab.py`, `CLAUDE.md`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- เพิ่ม `vlab:vpl03:*` ใน anonymous_access (admin panel) — ยังค้าง
- (ทางเลือกอนาคต) ระดับ 2: สิทธิ์แบบ `topic:*` ถ้าจะขายแพ็กเกจตามบทเรียน

## [2026-09-13 13:40] — ระดับ Lab การวัด 3D = ม.4
- ผู้ใช้แจ้งว่าเวอร์เนียร์/ไมโครมิเตอร์ (VPL03 Lab 1) สอนที่ ม.4 → `labs_data.py` level 'ปริญญาตรี' → 'ม.4' (tags: 3D, วงแหวนโลหะ) · rebuild ทั้ง virtual-lab.html / library / admin LAB_META
- virtual-lab.html: chip ระดับ generate เฉพาะระดับที่มี lab จริง (ตอนนี้ ม.4/ม.5/ม.6 — "ปริญญาตรี" หายไปอัตโนมัติ ถ้ามี lab ระดับนั้นในอนาคตจะกลับมาเอง)
- index.html: ปุ่ม quick menu "ปฏิบัติการ ม. (3D)" → "📐 Lab การวัด 3D" (→ `virtual-lab.html?topic=measure`, 3 การทดลอง) · accordion VPL03 → ?topic=measure · การ์ดหน้าแรก dc-topic "การวัด · ม.4 · 3D"
- หมายเหตุ: ชุด VPL03 ยังชื่อ "ปฏิบัติการฟิสิกส์ ม." ในไฟล์ lab (อ้างอิงที่มาคู่มือ) — ไม่ได้แก้

## [2026-09-13 14:10] — Lab 35 bugfix: ภาพจริงต้องกลับหัว
- ผู้ใช้พบว่า Lab 35 (เลนส์นูน) วาดภาพจริงเป็นหัวตั้ง → สาเหตุ: ไฟล์ใช้ convention ไทย M = d_i/d_o (M > 0 = ภาพจริง) แต่โค้ดวาดใช้ `inverted = M < 0` (convention สากล) ทั้ง 2 จุด: กล่อง "ภาพบนจอ" (`drawScreenInset`, บรรทัด ~1162) และลูกศรภาพบนม้านั่งโหมด Auto (`drawAutoMode`, ~1489) → แก้เป็น `M > 0`
- ตรวจด้วย headless Chrome (test copy บังคับ Part B d_o=20,f=10 และ Auto d_o=25): ภาพจริงกลับหัวทั้ง 2 ที่ · ตารางทฤษฎี/ข้อความในไฟล์ถูกอยู่แล้ว ("จริง = กลับหัว")
- Lab 36 (เลนส์เว้า) ตรวจแล้ววาดภาพเสมือนหัวตั้งถูกต้อง (`imgTipY = ay - imgH`) ไม่ต้องแก้
- ไฟล์ที่แก้: `Virtual Physics Lab 02/35. images-converging-lenses.html`

## [2026-09-13 14:40] — Lab 35: ขนาด/ตำแหน่งภาพสัมพันธ์จริง
- ผู้ใช้ขอให้ขนาดภาพสัมพันธ์กับระยะจริง (วัตถุที่ 2F → ภาพที่ 2F ขนาดเท่าวัตถุ)
- Part B (วัดเอง): เพิ่ม `drawImageOnScreen()` วาดภาพจริง **บนผิวจอที่ตำแหน่งจอจริง** สูง |M|·h (สเกลเดียวกับวัตถุบนม้านั่ง) กลับหัว ห้อยจากแกน · เบลอ/จางเมื่อจอไม่อยู่ที่ dᵢ · ชัดแล้วขึ้นป้าย "ภาพจริง h' = x.xx cm"
- กล่อง "ภาพบนจอ" และ "มุมมองของตา": เพิ่มลูกศรวัตถุอ้างอิง (สีส้มจาง) ข้างภาพ สเกลเดียวกัน (วัตถุ = refH, ภาพ = |M|·refH) + เส้นแกน + ป้าย M = x.xx× (เดิม refH คงที่ 45 px ไม่สัมพันธ์กับวัตถุ)
- ตรวจ headless 4 กรณี: d_o=2f (M=1 เท่าวัตถุ ที่ 2F') · d_o=1.5f (M=2 ใหญ่ 2 เท่า ที่ 3f) · จอเลย dᵢ 6 cm (เบลอ) · d_o<f (ภาพเสมือนหัวตั้ง 3.33× ในกล่องตา) ✓
- โหมด Auto ใช้ |M|·OBJ_H อยู่แล้ว (ถูกต้องเดิม)

## [2026-09-13 15:10] — Lab 35: ลดพื้นที่แคนวาส + ขยายสเกลแนวตั้ง
- ผู้ใช้เห็นด้วยว่าแคนวาสใหญ่และว่างเกิน (แต่ **ห้ามย้ายกล่อง "ภาพบนจอ/มุมมองของตา" ออกจากแคนวาส** เพราะบน iPad จะตกไปนอกเฟรม)
- แคนวาส: `.sim-layout` เลิกยืด 100vh, `.canvas-wrap` สูงคงที่ 450 px (≤900 px: 400 px) · แกนแสง AY = 50% · ม้านั่ง BY = สูง−36
- สเกลแนวตั้ง `VSCALE = 2.5` (`OBJ_H_PX_F` และไม้บรรทัดแนวตั้ง `drawRulerV`) — ทุกความสูงคูณเท่ากัน M จึงถูกต้อง: วัตถุ 3 cm ≈ 62 px (เดิม 25) · ภาพ auto cap 240 px
- breakpoint แผงควบคุม 800 → 900 px เพื่อให้ iPad แนวตั้ง (820 px) วางแผงใต้แคนวาส แคนวาสกว้างเต็ม กล่อง inset ไม่บังเลนส์
- ตรวจ headless: Part A, 2f, 1.5f (+ไม้บรรทัดแนวตั้งอ่าน 3.0 cm ถูก), ภาพเสมือน, Auto, iPad 820×1180 ✓ · ทั้งหน้าพอดี 900 px ไม่ต้องเลื่อนหาตาราง
- Lab 36 ยังไม่ปรับ (รอผู้ใช้พอใจ Lab 35 ก่อน)

## [2026-09-13 17:30] — NEW Lab 46 (VPL02) ภาพจากกระจกเว้า 3D
### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/46. images-concave-mirror.html` (≈100 KB) โครงเดียวกับ Lab 35: Part A หาโฟกัสด้วยแสงขนาน (สุ่ม f 6–22) · Part B ศึกษาภาพ (จริง→จอ / เสมือน→ตา) · โหมดวัดเอง (ดีฟอลต์, ไม่โชว์รังสี/ภาพ) / อัตโนมัติ (รังสีหลัก 3 เส้น + ภาพ + กราฟ 1/d_o–1/d_i) · ตาราง A/B/Auto + CSV · ไม้บรรทัด ↔/↕ · ทฤษฎี 4 canvas (f=R/2, รังสี 3 เส้นแบบโต้ตอบ, 5 กรณี, กราฟ)
- **3D (three.js r128):** ม้านั่ง 100 cm มีสเกล · กระจกเว้าเป็น spherical cap R=2f (ผิวสะท้อน metalness 1) · วัตถุลูกศรเรืองแสง · จอ (CanvasTexture: วงแสง Part A / ภาพจริงกลับหัวสเกลจริง |M|·h เบลอเมื่อไม่โฟกัส) · ตา · ดวงอาทิตย์+รังสีขนาน · รังสี 3 เส้นเป็น THREE.Line · ลากอุปกรณ์ในภาพ (raycast) · ปุ่มมุมข้าง/เฉียง/จากตา (มองเข้ากระจกเห็นภาพเสมือน)
- **แผนภาพรังสี 2D ตามสเกล** ใต้ภาพ 3D (VSCALE 2.5) ลากอุปกรณ์/ไม้บรรทัดได้ · กล่อง inset (วงแสง/ภาพบนจอ/มุมมองตา + วัตถุอ้างอิง) **อยู่ในเฟรม 3D** ตามที่ผู้ใช้ต้องการสำหรับ iPad
- convention ไทย: d_i>0 จริง (หน้ากระจก) M=d_i/d_o>0 กลับหัว · ตรวจ 5 กรณี (2f→M=1 ที่ 2f, 1.5f→M=2, d_o<f→เสมือน 2.5×, Part A, Auto) ด้วย headless Chrome + swiftshader ไม่มี runtime error
- `_shared/three.min.js` (603 KB) = fallback offline; Lab 46 + VPL03 Lab 1 ใช้ cdnjs ก่อน ถ้าไม่มี THREE → document.write ไฟล์นี้ · แยกข้อความ "ไม่มี WebGL" ออกจาก "โหลดไลบรารีไม่ได้"
- ลงทะเบียน lab-46: `labs_data.py` (light · ม.5) → build virtual-lab.html/library/admin LAB_META · `VLAB_SERIES` vpl02 ใน kp-auth.js + admin.html · admin LAB_LIST
### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/46. images-concave-mirror.html`, `_shared/three.min.js`
- `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `_admin/admin.html`, `kp-auth.js`, `Virtual Physics Lab 03/1. precision-measurement-3d.html` (fallback), `CLAUDE.md`
### ค้างไว้ / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 46 ใน `virtual-physics-lab-02.html` (catalog ชุดเดิม) และ index cards — มีใน virtual-lab.html/library แล้ว
- ทดสอบใน in-app browser/iPad จริงยังไม่ได้ (popup Google sign-in ค้างใน Browser pane) — ทดสอบด้วย headless เท่านั้น
- Lab 36 ยังไม่ปรับแคนวาสกะทัดรัดแบบ Lab 35

## [2026-09-13 18:30] — Lab 46 ปรับตาม feedback (แผนภาพ 2D)
- ① เอาฐาน/ขาตั้งของวัตถุ จอ ตา ออกจากแผนภาพ 2D (เหลือม้านั่ง+สเกล) · จอ/ลูกศรถูก clamp ไม่ทะลุขอบแคนวาส (สูง 260 px)
- ② โหมดวัดเอง Part A: ไม่วาดรังสีและไม่แสดง F/C (เพราะเฉลยตำแหน่งโฟกัส) ทั้ง 2D และ 3D — เหลือดวงอาทิตย์ + แสงสว่างจาง + วงแสงบนจอ · โหมด Auto ยังแสดงรังสี 3 เส้น
- ③ กระจกใน 2D วาดเป็นส่วนโค้งเว้ารูป ")" (จุดยอดที่ตำแหน่งกระจก ขอบเบนไปทางวัตถุ) sagitta ขยายให้เห็นชัด + hatch ด้านหลัง
- ④ ภาพเสมือน: โหมดวัดเอง เมื่อตาอยู่หน้าวัตถุ วาดภาพเสมือนหัวตั้ง (เส้นประม่วง) **หลังกระจก** ที่ mirrorCm+|d_i| พร้อมตำแหน่ง cm ให้วัดได้ (ทั้ง 2D และ 3D จาง ๆ) · โหมด Auto มีอยู่แล้ว (ตรวจ d_o=6,f=10 → d_i=−15, M=−2.5 หัวตั้งหลังกระจก ✓)
- แก้บั๊ก: comment `//` กลืนโค้ดใน drawArrow2D (ทั้งหน้าไม่ทำงาน) → ใช้ /* */ · ตรวจ headless ผ่าน 3 สถานะ ไม่มี error
- Lab 46: เพิ่ม KP Topbar (protect script ตรวจว่ามีเพราะเจอ CSS แต่ไม่มี HTML — insert เอง) + scope CSS แท็บเป็น nav.tabs ไม่ให้ทับ topbar
- Lab 46 3D: เอาสเกลไม้เมตรออกจากม้านั่ง (เรียบ มีร่อง) ตามที่ผู้ใช้ขอ · กระจกมองเห็นทั้งสองด้าน (หน้าเงิน metalness .55 / หลังเทาทึบ)
- Lab 46 3D: เอาม้านั่งออกทั้งชิ้นตามที่ผู้ใช้ย้ำ — อุปกรณ์ตั้งบนพื้นเรียบ + grid จาง (ตำแหน่งอ่านจากแผนภาพ 2D)
- Lab 46 3D: เอาพื้นและ grid ออกด้วย — อุปกรณ์ลอยบนพื้นหลังเปล่า
- Lab 46 3D: เอาฐานกลม/เสาออกทุกชิ้น · จอสูง 20×12 cm กึ่งกลางที่แกนแสง (ภาพจริงกลับหัวไม่ตกขอบล่าง) · texture แกนที่ H/2

## [2026-09-13 19:40] — Lab 35 (VPL02) ภาพจากเลนส์นูน → 3D
### ทำอะไรไปบ้าง
- เขียน `Virtual Physics Lab 02/35. images-converging-lenses.html` ใหม่ทั้งไฟล์ (2561 → ~960 บรรทัด) โดยใช้โครง 3D ของ Lab 46 (three.js r128 + fallback `_shared/three.min.js` + แผนภาพรังสี 2D ตามสเกล + กล่อง inset ในเฟรม 3D) แต่ฟิสิกส์เป็นเลนส์นูน: แสงเดิน +x · วัตถุซ้ายเลนส์ · จอ/ตาขวาเลนส์ · ตำแหน่งภาพ = lensCm + d_i (จริง → ขวา, เสมือน → ซ้าย ด้านวัตถุ) · convention ไทย M = d_i/d_o เดิม
- 3D: เลนส์นูนสองหน้า (LatheGeometry, Rc ≈ f → f สั้นเลนส์หนา) + วงแหวนยึด · วัตถุลูกศรเรืองแสง · จอขุ่น texture ทั้งสองหน้า (วงแสง Part A / ภาพจริงกลับหัวสเกลจริง เบลอเมื่อไม่โฟกัส) · ตาหันหน้าไปทาง −x · ดวงอาทิตย์ + ลำแสงขนานจาง (Part A) · รังสี 3 เส้น (ขนาน→F′, ผ่านกลาง, ผ่าน F→ขนาน) + ภาพในโหมด Auto · ภาพเสมือนม่วงโปร่ง (manual) · ลากอุปกรณ์ในภาพ · ปุ่มมุมข้าง/เฉียง/จากตา (มุมจากตา = มองผ่านเลนส์จากขวาเห็นภาพเสมือนขยาย) · ไม่มีม้านั่ง/พื้น/ฐาน ตามที่ผู้ใช้ตัดสินใจไว้กับ Lab 46
- 2D: เลนส์รูปนูนสองหน้า · F/F′/2F/2F′ (ซ่อนใน manual Part A) · โหมด manual Part B วาดภาพเสมือนเส้นประ + ตำแหน่ง cm ให้วัดได้ · ไม้บรรทัด ↔/↕ เดิม
- **แก้ฟิสิกส์ผิดของเวอร์ชันเก่า:** เดิมวางตาไว้ด้านซ้าย (ด้านเดียวกับวัตถุ) ตอนดูภาพเสมือน → ใหม่ตาอยู่ด้านขวามองผ่านเลนส์ (แบบแว่นขยาย) · Part A เดิมสุ่ม f 5–90 → 6–24 cm ให้อยู่ในสเกล 100 cm
- เนื้อหาแท็บวิธีทดลอง/ทฤษฎี/กฎเครื่องหมายของ Lab 35 เดิมคงไว้ + เพิ่มส่วน "การใช้งาน Simulation" (3D) + canvas ทฤษฎี 0 (แสงขนาน→F′) · เปลี่ยนสีธีมเป็นชุดเดิมของ Lab 35 (accent ส้ม)
- ตรวจ: node --check inline script 6 ตัวผ่าน · protect script ผ่าน (เตือน MOBILE เท่านั้น — สคริปต์ไม่มีโค้ด fix จริง เหมือน Lab 46) · **ทดสอบใน Browser pane (localhost:8765) ได้แล้วรอบนี้**: Part A ที่โฟกัส, Part B d_o=2f (M=1 บนจอ), d_o<f (เสมือน 2.5× ตาขวา), มุมจากตา, Auto d_o=15/30 + ตาราง + กราฟ, แท็บทฤษฎี 4 canvas, iPad 820×1180 (แผงลงใต้แคนวาส inset อยู่ในเฟรม), ไม้บรรทัด ↔ — ไม่มี console error
- อัปเดต metadata: `labs_data.py` lab-35 ชื่อ "(3D)" + tag 3D → build virtual-lab.html / library.html / admin LAB_META · การ์ดใน index.html + virtual-physics-lab-02.html เปลี่ยน topic/title/desc เป็น 3D · `.gitignore` เพิ่ม `__pycache__/`
### ไฟล์ที่แก้
- `Virtual Physics Lab 02/35. images-converging-lenses.html` (เขียนใหม่) · `_admin/labs_data.py` · `virtual-lab.html`, `library.html`, `_admin/admin.html` (generated) · `index.html`, `virtual-physics-lab-02.html` (การ์ด Lab 35) · `.gitignore` · `SESSION_LOG.md`
### ค้างไว้ที่ไหน / ต้องทำต่อ
- commit + push แล้ว (4613028) — ไฟล์เดิม 2D อยู่ที่ commit 67067a6 ถ้าต้องการย้อน
- canvas preview `vpl2-lens` บนการ์ดหน้าแรกยังเป็นภาพวาด 2D เดิม (ไม่กระทบการใช้งาน)
- Lab 36 (เลนส์เว้า) ยังเป็น 2D — ถ้าพอใจ Lab 35 อาจแปลงด้วยโครงเดียวกัน (เปลี่ยน f เป็นลบ, ภาพเสมือนเสมอ)
### หมายเหตุ
- โหมด Auto: เลนส์จะขยับขวาเองถ้า d_o > lensCm−2 (`curLensCm()`) เพื่อไม่ให้วัตถุหลุดสเกล 0
- Browser pane รอบนี้ใช้ได้แล้ว (ไม่มี popup ค้าง) — server python http.server 8765 ที่ผู้ใช้เปิดไว้อยู่แล้ว

## [2026-09-13 21:00] — Lab 36 (VPL02) เลนส์เว้า & กล้องกาลิเลโอ → 3D
### ทำอะไรไปบ้าง
- เขียน `Virtual Physics Lab 02/36. images-diverging-lenses.html` ใหม่ทั้งไฟล์ (3089 → ~590 บรรทัด, 113 KB) ด้วยโครง 3D เดียวกับ Lab 35/46 (three.js + fallback + แผนภาพ 2D ตามสเกล + inset ในเฟรม 3D)
- **Part A (หา f ด้วยลำแสงเลเซอร์):** 3D = เลเซอร์ทรงกระบอก + ลำแสงแดง + เลนส์เว้าสองหน้า (LatheGeometry ขอบหนากลางบาง) + กรวยแสงบาน + กระดาษมี texture วงแสง D จริง · inset "วงแสงบนกระดาษ" 236×206 มีสเกลไม้บรรทัด + คาลิปเปอร์ A/B ลากวัด D ได้ + ซูม 1–10× (แสดงค่า A–B) · โหมด auto แสดง F เสมือน + เส้นต่อรังสี + วงเล็บ |f|, X · ตาราง X/D แก้ไขได้ + fit เส้นตรง + กราฟ D vs X extrapolate → f = จุดตัดแกน X (แก้เครื่องหมายให้ f = −b/a ติดลบถูกต้อง)
- **Part B (กล้องกาลิเลโอ):** 3D = ต้นไม้ไกล (x = −70) + เลนส์นูน F₁ + เลนส์เว้า F₂ + ตา · รังสีคำนวณจริงด้วยสูตรเลนส์บาง s' = s − y/f (`traceRay`) ทั้ง 2D/3D: ลำขนาน 3 เส้น (ฟ้า) + ลำเฉียง 2 เส้น (ส้ม) → เมื่อ L = F₁+F₂ รังสีออกขนานและมุมขยาย M เท่า (เดิม Lab 36 2D ใช้รังสีประมาณเอา) · รังสีแสดงหลังบันทึก F₂ หรือในโหมด auto · inset "มุมมองผ่านกล้อง" ต้นไม้ขยาย M เบลอเมื่อยังไม่จูน
- เนื้อหาแท็บวิธีทดลอง/ทฤษฎีเดิมคงไว้ + เพิ่มส่วน "การใช้งาน Simulation" · canvas ทฤษฎี 5 รูปเขียนใหม่ (รังสี 3 เส้นเลนส์เว้า, 3 กรณี, กราฟ 1/dᵢ–1/dₒ f<0, สามเหลี่ยมคล้าย D/X, กล้องกาลิเลโอ)
- ตรวจ: node --check 7 script ผ่าน · Browser pane: Part A manual/auto, Part B จูนแล้วบันทึก F₂ (err 5% แสดงการ์ดผล + รังสี), มุมจากตา, auto B (M=5), ทฤษฎี, iPad 820 — ไม่มี console error
- metadata: labs_data.py lab-36 "(3D)" + tags Telescope/3D → build · การ์ด index.html + virtual-physics-lab-02.html เป็น 3D
### ไฟล์ที่แก้
- `Virtual Physics Lab 02/36. images-diverging-lenses.html` (เขียนใหม่) · `_admin/labs_data.py` · `virtual-lab.html`, `library.html`, `_admin/admin.html` (generated) · `index.html`, `virtual-physics-lab-02.html` · `SESSION_LOG.md`
### ค้างไว้ที่ไหน / ต้องทำต่อ
- ไฟล์ 2D เดิมของ Lab 36 อยู่ที่ commit 77a8c72 ถ้าต้องการย้อน
- canvas preview การ์ดหน้าแรก (`data-sim`) ของ Lab 35/36 ยังเป็นภาพวาด 2D เดิม
- Lab อื่นใน VPL02 ที่อาจแปลง 3D ต่อ: 32B แสงสะท้อน, 33B หักเหแก้ว (ถ้าผู้ใช้ต้องการ)
### หมายเหตุ
- ระวังตอนคัดลอก head จาก Lab 35: ห้ามตัดที่ `<body ` เพราะสคริปต์ frame-protection มีสตริง `<body style=` อยู่ก่อน — ให้ตัดที่ `</head>`

## [2026-09-13 21:40] — Lab 36 ปรับตาม feedback
- ① กรวยแสง 3D บานเข้า (ผิด) → สาเหตุ CylinderGeometry หลัง rotateZ(π/2) ด้าน top ชี้ไป −x จึงต้องใส่ radiusTop = D₀/2 (ฝั่งเลนส์), radiusBottom = D/2 (ฝั่งกระดาษ) — ตอนนี้บานออกตรงกับ 2D
- ② เอากล่อง inset "วงแสงบนกระดาษ" (คาลิปเปอร์+ซูม) ออกจาก Part A → ย้ายการวัดไปแผนภาพ 2D: กระดาษมี**สเกล cm** (0 ที่แกนแสง ขีดทุก 0.5/1 cm เลขทุก 2 cm สเกลเดียวกับวงแสง 2.5×) + วงแสงสีแดงสูง D บนกระดาษ + เส้นประขอบบน/ล่าง · เพิ่มไม้บรรทัด **↕ วัด D** (ลากปลาย A/B อ่านค่า cm ชดเชย VSCALE แล้ว) · ลบโค้ด zoom/caliper ทั้งหมด · Part B ยังมี inset "มุมมองผ่านกล้อง" (ผู้ใช้ไม่ได้สั่งเอาออก)
- ③ กล้องกาลิเลโอ: ต้นไม้ 3D ย้ายจาก x=−70 → −260 และสูง 70 cm · 2D วาดต้นไม้เล็กนอกม้านั่ง + เครื่องหมาย "ไกลมาก" (∥) รังสีขนานเข้ามาจากขอบซ้าย
- ตรวจ Browser pane: Part A (D=3.0 ที่ X=40, ไม้บรรทัด ↕ อ่าน 2.31 cm ตามตำแหน่งปลาย), Part B จูนแล้วรังสีผ่าน — ไม่มี error
- ไฟล์: `Virtual Physics Lab 02/36. images-diverging-lenses.html`
- [21:55] Lab 36: ย้ายกล่อง "มุมมองผ่านกล้อง" (Part B) ออกจากเฟรม 3D (บังภาพ) → เป็นแถวของตัวเองระหว่างภาพ 3D กับแผนภาพ 2D (`.inset-row` = กล่อง 150×170 + คำอธิบาย) · ซ่อนใน Part A เหมือนเดิม · ตรวจแล้ว display flex/none ถูกต้อง ไม่มี error

## [2026-09-13 23:00] — Lab 33B (VPL02) การหักเหผ่านแท่งแก้ว → 3D "มองผ่านผลึกได้"
### ทำอะไรไปบ้าง
- เขียน `Virtual Physics Lab 02/33B. light-refraction-glass.html` ใหม่ทั้งไฟล์ (1210 → ~560 บรรทัด, 83 KB) โครง 3D เดียวกับ Lab 35/36/46
- **แนวคิด:** canvas 2D = "กระดาษบนโต๊ะ" มุมบน หน่วย cm (30×21, แท่งแก้ว 12×6 กลางกระดาษ) — ปักหมุด/ลากหมุด/ลากตา/โปรแทรกเตอร์เหมือนเดิม · ภาพกระดาษเดียวกันถูกวาดลง CanvasTexture (1200×840, ธีมกระดาษขาว) ปูบนโต๊ะใน 3D · หมุด 4 ตัวเป็นเข็ม 3D (สูง 3.2 cm) · ตา 3D
- **แท่งแก้วหักเหจริง:** ShaderMaterial แบบ screen-space refraction — render ฉากโดยไม่มีแท่งแก้วลง WebGLRenderTarget (สี + DepthTexture) แล้ววาดแท่งแก้วด้วย shader: refract(v, n, 1/n) ตามกฎสเนลล์ → เดินในแก้วตามความหนาด้านนั้น (dot(|normal|, ขนาดกล่อง)) → รังสีออกขนานรังสีเข้า → หาจุดชนฉากหลังด้วย depth (วนซ้ำ 4 รอบ parallax) → sample สี + tint ตามวัสดุ + fresnel · ผลลัพธ์: **มุมจากตา** เห็นก้านหมุดหลังแก้วเลื่อนด้านข้างและ "หัก" ตรงขอบบนแท่งแก้ว ส่วนหัวหมุดที่พ้นแก้วอยู่ที่เดิม — ตรวจโดยเทียบ n=1.0 กับ 1.52 แล้ว · เปลี่ยนวัสดุ (8 ชนิด) เปลี่ยน n และสี tint ทันที
- ปุ่มมุมมอง: มุมเฉียง / มุมบน / 👁 มุมจากตา (กล้องอยู่ที่ตาสูง 1.6 cm FOV 24° เล็งกึ่งกลาง P₁P₂) · ในมุมจากตาลากได้เล็กน้อยเพื่อกวาดสายตา · ตา 3D ซ่อนตอนอยู่ในมุมจากตา
- เอากล่อง inset "มุมมองของตา" แบบ 2D เดิมออก (แทนด้วยมุมจากตาใน 3D ตามที่ผู้ใช้ขอ) · ปุ่ม ✓ เสร็จสิ้น ย้ายไปใต้คำแนะนำในแผงขวา (เดิมทับ canvas)
- โหมด Auto: รังสี/มุม/normal วาดบนกระดาษ (เห็นผ่านแก้วใน 3D ด้วย) · ตาราง/กราฟ sinθ₁–sinθ₂ (เพิ่มป้าย slope = 1/n) · CSV เพิ่มคอลัมน์วัสดุ/n จริง · ตารางโหมด Auto ไม่โชว์แถวว่างของโหมดวัดเอง
- ทฤษฎี 3 canvas ใช้โค้ดเดิม (verbatim) · หน้าวิธีทดลองเพิ่มส่วน "วิธีใช้ Simulation (3D)"
- ตรวจ Browser pane: ปักหมุด → มุมจากตา (หักเหจริง) → วาง P₃P₄ → ยืนยัน → รังสี+โปรแทรกเตอร์ → Auto θ₁=45° (n=1.52) → ทฤษฎี → iPad 820 · ไม่มี console error
- metadata: labs_data.py lab-33b "(3D)" + tags → build · การ์ด index.html + virtual-physics-lab-02.html
### ไฟล์ที่แก้
- `Virtual Physics Lab 02/33B. light-refraction-glass.html` (เขียนใหม่) · `_admin/labs_data.py` · `virtual-lab.html`, `library.html`, `_admin/admin.html` (generated) · `index.html`, `virtual-physics-lab-02.html` · `SESSION_LOG.md`
### ค้างไว้ที่ไหน / ต้องทำต่อ
- ไฟล์ 2D เดิมอยู่ที่ commit 36df2b9 ถ้าต้องการย้อน
- shader หักเหใช้ DepthTexture — ต้อง WebGL2 หรือ extension WEBGL_depth_texture (iPad Safari ≥ 15 รองรับ) ถ้าอุปกรณ์เก่าไม่รองรับ แท่งแก้วอาจแสดงผิด → ยังไม่ได้ทำ fallback
- 3D lab ใน VPL02 ตอนนี้: 33B, 35, 36, 46 · ตัวถัดไปที่เหมาะ: 32B แสงสะท้อน (กระจกเงาราบ 3D)
### หมายเหตุ
- เทคนิค screen-space refraction นี้ใช้ซ้ำได้กับปริซึม/เลนส์หนา (เปลี่ยนการคำนวณจุดออก) — ฟังก์ชันอยู่ใน GLASS_FRAG

## [2026-09-13 23:40] — Lab 33B ปรับตาม feedback
- ① เอา "ตา" ออกทั้ง 2D และ 3D — ตำแหน่งตาสำหรับปุ่ม "มุมจากตา" คำนวณอัตโนมัติ (`sightLine()`): อยู่บนแนวรังสีออกจริงของ P₁→P₂ (หักเหตามสเนลล์) ที่เลยขอบกระดาษ 4 cm → ในมุมจากตา P₁ กับ P₂ **ซ้อนกันพอดี** (ตรวจแล้ว: เห็นหัวหมุดเดียว = ยืนยันว่า shader หักเหถูกต้องเชิงปริมาณ) แล้วนักเรียนวาง P₃P₄ ให้อยู่ในแนวสายตานั้น
- ② เงาหมุด P₃P₄ โผล่ในแท่งแก้ว = artifact ของ screen-space refraction (sample ไปโดนวัตถุที่อยู่หน้าผิวแก้ว) → shader เพิ่ม `uInvView` คำนวณจุดที่รังสีออกชนระนาบกระดาษเป็นค่าเริ่ม/สำรอง และปฏิเสธตัวอย่างที่ depth อยู่หน้าผิวแก้ว (ใช้สีกระดาษแทน) — ไม่มีเงาแล้ว
- ③ ปุ่ม ✓ เสร็จสิ้น กลับมาอยู่บน canvas กระดาษ 2D (มุมล่างซ้าย เขียวกะพริบ) เอาออกจากแผงขวา
- ไฟล์: `Virtual Physics Lab 02/33B. light-refraction-glass.html` · console มีเฉพาะ Firestore offline (เครือข่าย ไม่เกี่ยวกับโค้ด)
- [23:55] Lab 33B: ภาพหมุด P₁P₂ ผ่านแก้วเอียง/เพี้ยนหลังแก้ ② → เปลี่ยนวิธี sample ใน shader: ใช้จุดชนระนาบกระดาษ (คำนวณตรง ๆ) เป็นฉากหลัง + เดินตามรังสีออก 48 ขั้นเทียบ depth buffer เพื่อหาวัตถุบาง (หมุด) ที่อยู่หลังแก้ว (แทนการวนหา fixed-point เดิมที่ลู่ผิดเมื่อจุดเริ่มไกล) · ยังปฏิเสธวัตถุหน้าแก้ว → ก้านหมุดตรงไม่เอียง ไม่มีเงา P₃P₄
- [00:10] Lab 33B: ภาพหมุดในแก้วซ้อน 2 เส้นต่อหมุด → ภาพที่สองมาจากพิกเซลที่รังสีไม่ชนหมุดแต่ไปสุ่มสี "จุดบนกระดาษ" ซึ่งใน buffer ถูกหมุดบัง → shader ตรวจว่าจุดบนกระดาษถูกบัง (depth อยู่หน้าจุดนั้น > 0.4 cm) แล้วใช้สีกระดาษแทน → เหลือหมุดละ 1 เส้น ตรวจแล้วในมุมจากตา/มุมเฉียง
- [00:25] Lab 33B: "เงา" P₃P₄ ในแก้ว (รอยสีอ่อนรูปหมุดเลื่อน) = บริเวณที่ใช้สีกระดาษคงที่แทนจุดที่ถูกหมุดหน้าแก้วบัง → shader หา sample กระดาษจริงจากพิกเซลข้างเคียงที่ไม่ถูกบัง (±3 px ×8 ขั้น, uniform uRes) → กลมกลืน ไม่มีรอยแล้ว
- [00:40] Lab 33B: เส้นขาวในแก้ว (ภาพก้าน P₁P₂ ลากต่อเป็นแนวนอนที่ฐาน) = false hit ของการเดินรังสีเมื่อรังสีผ่าน "ข้างหลัง" หมุด (เผื่อความหนา 1.5 cm) → refine จุดตัดด้วย bisection 5 รอบ แล้วรับเฉพาะเมื่อระยะรังสี–ผิว < 0.3 cm · ตรวจ 3 มุม (ต่ำ/เอียงซ้าย-ขวา/ตรง) ไม่มีรอยแล้ว

## [2026-09-14 01:20] — Lab 32B (VPL02) การสะท้อนของแสง → 3D (กระจกสะท้อนจริง)
### ทำอะไรไปบ้าง
- เขียน `Virtual Physics Lab 02/32B. light-reflection.html` ใหม่ทั้งไฟล์ (1252 → ~560 บรรทัด, 77 KB) โครงเดียวกับ 33B: canvas 2D = กระดาษ 30×21 cm (ปักหมุด / ลากหมุด / เส้น Normal / โปรแทรกเตอร์ / ปุ่ม ✓ เสร็จสิ้น บนกระดาษ) → texture บนโต๊ะใน 3D · หมุด 3D 4 ตัว · ไม่มี "ตา" (ตามที่ผู้ใช้ให้เอาออกใน 33B)
- **กระจกเงาราบ 3D สะท้อนภาพจริง:** planar reflection แบบ Reflector — ทุกเฟรม render ฉากด้วยกล้องเสมือนที่สะท้อนผ่านระนาบกระจก (z = −3, หันหน้า +z) ลง WebGLRenderTarget แล้ว project ลงระนาบกระจกด้วย texture matrix (texture2DProj) · ใช้ `renderer.clippingPlanes` ตัดวัตถุหลังกระจกออกตอน render ภาพสะท้อน (แทน oblique near-plane) · กระจก 22×8 cm ตั้งฉากบนเส้น y=7.5 มีแท่งไม้ค้ำ + แผ่นหลัง + ขอบ
- **มุมจากตา** อัตโนมัติ (`sightLine()`): ตาอยู่บนรังสีสะท้อนของแนว P₁P₂ เลยขอบกระดาษ 4 cm → ภาพ P₁′ P₂′ ในกระจกซ้อนกันพอดี (ตรวจด้วย camera.project: x เท่ากัน 457 px) · ลากใน 3D กวาดสายตาได้เล็กน้อย = สาธิตพารัลแลกซ์ · โหมด Auto ก็มีมุมจากตา (บนรังสีสะท้อนของ θi)
- ขั้นตอน/ตาราง/%Error/กราฟ θi–θr/ทฤษฎี 2 canvas คงตามเดิม (ปรับเป็นหน่วย cm) · หน้าวิธีทดลองเขียนส่วน Simulation (3D) ใหม่
- ตรวจ Browser pane: ปักหมุด → มุมเฉียง (เห็นภาพหมุดในกระจก) → มุมจากตา → วาง P₃P₄ → ยืนยัน → Normal → โปรแทรกเตอร์ (θ จริง 36.87°) → Auto 50° + ตาราง + กราฟ → ทฤษฎี → iPad 820 · console มีแค่ Firestore offline/400 จากเครือข่าย
- metadata: labs_data.py lab-32b "(3D)" + tags → build · การ์ด index.html + virtual-physics-lab-02.html
### ไฟล์ที่แก้
- `Virtual Physics Lab 02/32B. light-reflection.html` (เขียนใหม่) · `_admin/labs_data.py` · `virtual-lab.html`, `library.html`, `_admin/admin.html` (generated) · `index.html`, `virtual-physics-lab-02.html` · `SESSION_LOG.md`
### ค้างไว้ที่ไหน / ต้องทำต่อ
- ไฟล์ 2D เดิมอยู่ที่ commit f2c8c63 ถ้าต้องการย้อน
- 3D lab ใน VPL02 ตอนนี้: 32B, 33B, 35, 36, 46 · ที่เหลือในบทแสง: 34 (เลี้ยวเบน/แทรกสอด ripple tank) ยังเป็น 2D

## [2026-09-14 02:40] — NEW Lab 47 (VPL02) หาตำแหน่งภาพด้วยวิธีพาราแลกซ์ — กระจกราบ/เว้า/นูน (3D) · Opus 5
### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/47. image-location-parallax-mirrors.html` (≈75 KB) โครงเดียวกับ Lab 46: ภาพ 3D ด้านบน · แผนภาพม้านั่ง 2D (มองด้านข้าง ตามสเกลจริง) ด้านล่าง · แผงขวา · ไม่มีกล่องทับภาพ 3D
- **กระจก 3 แบบสะท้อนด้วย ray tracing ใน fragment shader:** แต่ละพิกเซลของผิวกระจก (ทรงกลมจริง R = 2|f| หรือระนาบ) คำนวณ normal ที่แม่นยำจากจุดศูนย์กลางความโค้ง → reflect() → หาจุดชนกับฉากแบบ analytic (ก้านเข็ม = ทรงกระบอก, หัว = ทรงกลม, ฐานไม้ก๊อก/ม้านั่ง = กล่อง, ผิวม้านั่งใช้ texture สเกลเดียวกับของจริง) → ภาพเสมือน/ภาพจริงกลับหัวเกิดขึ้นเองตามฟิสิกส์ พาราแลกซ์ถูกต้องเมื่อกล้อง (ตา) ขยับ
- วิธีทดลอง: เข็ม O ปลายอยู่ระดับแกน · S หลังกระจก = เข็มยาวโผล่เหนือขอบ (ภาพเสมือน) · S หน้ากระจก = ปลายระดับแกน วิธีปลายชนปลาย (ภาพจริงกระจกเว้า) · 👁 มุมจากตา (ค่าเริ่มต้น) ลากซ้าย-ขวา = ขยับศีรษะ · ปุ่ม ↔ ส่ายสายตา · ระยะตาอัตโนมัติ (ไกลกว่าเข็ม/ภาพจริง) · มุมเฉียง/มุมข้าง ลากเข็มในภาพได้
- **ตรวจความถูกต้องเชิงตัวเลข** (อ่านพิกเซลจาก WebGL, เปลี่ยนสีภาพ O เป็นม่วงแดงชั่วคราว): ตำแหน่งไม่มีพาราแลกซ์ตรงสมการกระจก — ราบ u=20 → 0.0 cm · นูน f=−12 u=20 → 0 · เว้าภาพจริง u=30 (v=20) → 0 · เว้าภาพเสมือน u=8 (v=−24) → ≈0.5 cm · f=15 u=10 (v=−30) → ≈0.4 cm · ถ้า S ผิด 5–6 cm เห็นพาราแลกซ์ชัด (~10 px)
- ปัญหาที่เจอและแก้: (1) ยกตาสูงเพื่อมองข้ามหัว O → เกิด astigmatism ของผิวทรงกลม (Coddington, sagittal) ภาพเสมือนกระจกเว้าคลาด 2–3.5 cm → ลดความสูงตาเหลือ 0.6·AP และใช้การเยื้องตาด้านข้าง (2 cm) แยกหัว O ออกจากภาพแทน (2) ภาพจริง: หัวเข็ม O/S/ภาพซ้อนกลางกระจก → เยื้องตาเพิ่มอัตโนมัติ 1.5 cm เมื่อ S อยู่หน้ากระจก + หัวเข็มเล็กลง (r 0.24) (3) FOV มุมจากตา 14° ให้กระจกใหญ่พอดูรายละเอียด
- โหมดวัดเอง: สุ่ม f (เว้า 9–16, นูน −9…−16) · บันทึกตำแหน่ง → u = 55 − O, v = 55 − S · กระจกราบคิด %err ของ |v| กับ u · กระจกโค้งคิด f = uv/(u+v) เทียบ f จริง · กราฟ 1/u–1/v · CSV
- โหมดอัตโนมัติ: ปรับ |f|, u → วาง S ที่ภาพ (มี checkbox เลื่อน S ออก 4 cm ดูพาราแลกซ์) · แผนภาพแสดงรังสี 2 เส้นจากฐานเข็ม + F/C + ภาพ
- แท็บวิธีทดลอง (วัตถุประสงค์ อุปกรณ์ วิธีใช้ ขั้นตอนภาพเสมือน/ภาพจริง การบันทึก คำถาม) · แท็บทฤษฎี (พาราแลกซ์ · กระจกราบ · กระจกเว้า/นูน 3 กรณี ตาราง กฎเครื่องหมาย หมายเหตุความคลาดทรงกลม)
- ลงทะเบียน: `VLAB_SERIES` vpl02 ใน kp-auth.js + admin.html (+ LAB_LIST) · labs_data.py (light · ม.5) → build virtual-lab.html (48) / library / admin LAB_META · protect script
- ตรวจ Browser pane: ทั้ง 3 กระจก มุมจากตา/เฉียง, auto + ตาราง + กราฟ, ทฤษฎี, iPad 820 · ไม่มี console error
### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/47. image-location-parallax-mirrors.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `SESSION_LOG.md`
### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้เพิ่มการ์ด Lab 46/47 ใน `virtual-physics-lab-02.html` และหน้าแรก (มีใน virtual-lab.html / library แล้ว)
- ถ้า Firestore `settings/public.anonymous_access` ใช้ `vlab:vpl02:*` อยู่แล้ว Lab 47 เปิดฟรีอัตโนมัติ
### หมายเหตุ
- เทคนิค analytic ray tracing ใน shader ใช้ซ้ำได้กับ lab กระจก/เลนส์อื่นที่ต้องการภาพถูกต้องตามฟิสิกส์ (ฉากต้องเป็น primitive ง่าย ๆ)
- [03:30] Lab 47 ปรับตาม feedback: ① กระจกราบ: เข็ม O สูงเกินขอบบนกระจก (HC+AP+1.5) → ภาพในกระจกสูงถึงขอบบน ต่อกับ S เหนือขอบพอดี ② กระจกเว้า: S **แขวนคว่ำ** จากแขนจับด้านบน (เสา+แขน+ฐานด้านข้าง z=−3) ปลาย S สูงกว่าแกน 0.45 cm · ปลาย O ต่ำกว่าแกน 0.45 cm → วาง u = v = R หัวเข็มไม่ชนกัน (เว้นช่อง ~0.4 cm) · shader ray tracing เพิ่ม primitive ของเข็มแขวน · แผนภาพ 2D วาดเข็มแขวน · ตัดการเยื้องตาเพิ่มในกรณีนี้ (หัว O/S แยกแนวดิ่งแล้ว ภาพจริงยังอยู่ในกรอบกระจก) ③ S หลังกระจก (วิธีภาพเสมือน): กระจกโปร่งแสง 30% เฉพาะส่วนที่มองทะลุไปเจอ S/ม้านั่งด้านหลัง (trace ตรงผ่านผิวกระจก ไม่รวมเข็ม O) → เห็น S จาง ๆ ต่อจากส่วนที่โผล่เหนือขอบ · ตรวจตัวเลขซ้ำ: ราบ/นูน/เว้าภาพจริง ไม่มีพาราแลกซ์ที่ตำแหน่งตามสมการ · เว้าภาพเสมือน u=8 คลาด ~0.7 cm · ข้อความในแผง/วิธีทดลอง/คำแนะนำอัปเดตแล้ว
- [03:50] Lab 47: เอาขาตั้ง (เสา/แขน/ฐาน) ของเข็ม S แบบคว่ำออกทั้ง 2D, 3D และใน shader — S ลอยอยู่ด้านบน · แผนภาพ 2D จับหมุดที่ตัวหมุด (ระยะจากจุดคลิกถึงก้านในช่วงความสูงของก้าน) แทนการเทียบแค่ตำแหน่ง x → O (ล่าง) กับ S (บน) ซ้อนตำแหน่งเดียวกันก็เลือกจับได้ · ตรวจด้วย mouse event จำลอง: ลาก S ที่ตำแหน่ง 26.8 ไป 36.7 โดย O อยู่ที่เดิม และลาก O ได้แยกกัน
- [04:10] Lab 47: เพิ่มปุ่ม **↺ รีเซตค่า** (แผงโหมด) → `resetAll()` คืนตำแหน่งเข็ม (ราบ/นูน O 35 S 80 · เว้า O 25 S 30) · สายตาเยื้อง 2 cm · ระยะตาอัตโนมัติ · หยุดส่ายสายตา · มุมจากตา · โหมดอัตโนมัติคืน u 20 f 12 และปิด "เลื่อน S ออก" · **ไม่ลบตาราง ไม่เปลี่ยน f ของกระจก** · แก้บั๊กเฉลย: สลับจากโหมดอัตโนมัติกลับโหมดวัดเอง S เคยค้างที่ตำแหน่งภาพ → ตอนนี้รีเซตตำแหน่งเข็มทุกครั้งที่เข้าโหมดวัดเอง
- [04:30] ปุ่ม **↺ รีเซตค่า** (ใต้ปุ่มเลือกโหมด) เพิ่มใน lab 3D ที่เหลือ → ฟังก์ชัน `resetLab()` ในแต่ละไฟล์ · ไม่ลบตาราง ไม่เปลี่ยน f/ตัวกลางที่สุ่มไว้:
  - 32B: ล้างหมุด/เส้น Normal/โปรแทรกเตอร์ (ใช้ resetAll เดิม) + มุมอัตโนมัติ 35° + มุมเฉียง
  - 33B: ล้างหมุด/โปรแทรกเตอร์ + มุมอัตโนมัติ 30° + มุมเฉียง (ไม่เปลี่ยนตัวกลาง)
  - 35: เลนส์ 40 วัตถุ 20 จอ 55 ตา 70 แล้ว setPart เดิมจัดตาม Part · ปิดไม้บรรทัด · ล้างช่องกรอก · auto f 10 d_o 25 · มุมเฉียง
  - 46: กระจก 70 วัตถุ 45 จอ 50 ตา 20 แล้ว setPart · ปิดไม้บรรทัด · ล้างช่องกรอก · auto f 10 d_o 25 · มุมเฉียง
  - 36: Part A เลนส์ 10 กระดาษ 30 · Part B เลนส์นูน 10 เลนส์เว้าวางคลาดจากระยะที่ถูก 3–8 cm (สุ่ม) + ซ่อนรังสีอีกครั้ง · ปิดไม้บรรทัด · ล้างช่องกรอก · auto ค่าเริ่มต้น · มุมเฉียง
  - ตรวจใน Browser pane ทุกไฟล์: ค่าคืนถูกต้อง ตารางยังอยู่ ไม่มี console error
- [04:45] ย้าย Lab 34 (การเลี้ยวเบนและแทรกสอด) จากบทเรียน "คลื่นกล" ไป "แสงและทัศนศาสตร์" ตามที่ผู้ใช้ขอ — `labs_data.py` topic waves → light และย้ายบรรทัดไปต่อหลัง 33B ให้เรียง 32B · 33B · 34 · 35 · 36 · 46 · 47 → build virtual-lab.html / library.html / admin LAB_META (สิทธิ์ `vlab:vpl02:lab-34` ไม่เปลี่ยน · ไฟล์ lab ไม่ได้แตะ · หน้าแรกไม่มีการ์ด 34)

## [2026-09-14 05:00] — สรุปทั้ง session (Lab แสง 3D ครบชุด) · ปิดแชทนี้ ไปต่อแชทใหม่

### ทำอะไรไปบ้าง
- แปลงเป็น 3D: Lab 35 เลนส์นูน · Lab 36 เลนส์เว้า+กล้องกาลิเลโอ · Lab 33B หักเหผ่านแท่งแก้ว (shader หักเหจริง) · Lab 32B สะท้อนกระจกเงาราบ (planar reflection)
- สร้างใหม่: **Lab 47 หาตำแหน่งภาพด้วยวิธีพาราแลกซ์** กระจกราบ/เว้า/นูน (ray tracing ใน shader) ลงทะเบียนสิทธิ์ `vlab:vpl02:lab-47` แล้ว
- ปุ่ม ↺ รีเซตค่า ใน lab 3D ทุกตัว (32B, 33B, 35, 36, 46, 47) — ไม่ลบตาราง ไม่เปลี่ยน f ที่สุ่ม
- ย้าย Lab 34 (เลี้ยวเบน/แทรกสอด) ไปหมวดแสงใน catalog
- รายละเอียดแต่ละเรื่องอยู่ใน entry ย่อยด้านบน (2026-09-13 19:40 → 2026-09-14 04:45)

### ไฟล์ที่แก้ (หลัก)
- `Virtual Physics Lab 02/32B, 33B, 35, 36, 46, 47 (ใหม่)` · `_admin/labs_data.py` · `virtual-lab.html` · `library.html` · `_admin/admin.html` · `kp-auth.js` · `index.html` · `virtual-physics-lab-02.html` · `.gitignore`
- ทุกอย่าง commit + push แล้ว (ล่าสุด 15b6724)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- Lab 34 ยังเป็น 2D (ผู้ใช้อาจให้ทำ 3D ต่อ)
- lab แสงที่ยังไม่มี: สลิตคู่/เกรตติง (Young), สลิตเดี่ยว, มุมวิกฤต/สะท้อนกลับหมด, ปริซึมกระจายแสง, ความลึกปรากฏ (ต่อยอดจาก 47+33B ได้), โพลาไรเซชัน
- ยังไม่มีการ์ด Lab 46/47 ใน `virtual-physics-lab-02.html` และหน้าแรก (มีใน virtual-lab.html/library แล้ว)
- ถ้าจะเปิด Lab 47 ให้ผู้ไม่ login: ตรวจ Firestore `settings/public.anonymous_access` ว่ามี `vlab:vpl02:*`

### หมายเหตุ (ความชอบของผู้ใช้สำหรับ lab 3D — ใช้กับ lab ใหม่)
- ห้ามมีกล่อง/inset ทับภาพ 3D → วางนอกกรอบ 3D
- ไม่ต้องมีม้านั่ง/พื้น/ฐาน/ขาตั้งเกินจำเป็นในบาง lab (46, 35) · ไม่ใช้รูปตาในแคนวาส (33B, 32B) · ปุ่ม ✓ เสร็จสิ้น อยู่บนแคนวาส 2D
- ภาพสะท้อน/หักเหต้องถูกต้องเชิงฟิสิกส์ — ผู้ใช้ตรวจละเอียด (เงาซ้อน, เส้นเกิน, ทิศลำแสง) → ตรวจเชิงตัวเลขก่อนส่ง
- ข้อมูลเฉลย (รังสี/ตำแหน่งภาพ/f) ต้องไม่หลุดในโหมดวัดเอง

## [2026-09-14 06:00] — NEW Lab 48 (VPL02) ความลึกจริงและความลึกปรากฏ (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/48. real-apparent-depth.html` (~75 KB) โครงเดียวกับ Lab 47: ภาพ 3D ด้านบน · แผนภาพภาคตัดขวาง 2D ตามสเกลด้านล่าง · แผงขวา · ไม่มีกล่องทับภาพ 3D · ไม่มีตาในแคนวาส sim · มีปุ่ม ↺ รีเซตค่า
- **การทดลอง (วิธีไม่มีพาราแลกซ์):** ถังแก้วสี่เหลี่ยม 10×10×28 cm · เข็ม O นอนที่ก้นถัง (สเกล 0) ปลายชี้ไปผนัง · เข็ม S นอนนอกถังชิดผนังเดียวกัน ลอย (ไม่มีขาตั้ง) เลื่อนขึ้น-ลง · 👁 มุมจากตา = มองลงจากเหนือปากถัง (จอด้านบน = S, ด้านล่าง = ภาพของ O ผ่านผิวของเหลว) · ลากซ้าย-ขวา/↔ ส่ายสายตา · สเกลแนวดิ่งติดข้างถัง
- **ของเหลวหักเหแสงด้วย ray tracing ใน fragment shader:** กล่องของเหลว (ผิวบน + ผนัง) → refract เข้า → trace เข็ม O (ทรงกระบอกนอน + หัวทรงกลม), ก้นถัง, ผิว/ผนังจากด้านใน → refract ออก (หรือสะท้อนกลับหมด) → trace เข็ม S + แผ่นรองในอากาศ · Fresnel สะท้อนผิวเล็กน้อย · มุมเฉียง/มุมข้างเห็นการหักเหผ่านผนังถังด้วย
- ของเหลว: น้ำ 1.33 · เอทานอล 1.36 · กลีเซอรีน 1.47 · ปริศนา (สุ่ม 1.30–1.58, 🎲) · โหมดวัดเองไม่แสดง n (เฉลยในตารางหลังบันทึก) · สลับจากอัตโนมัติกลับวัดเอง S ถูกย้ายไปที่ 0.8h (ไม่ค้างที่ภาพ)
- ตาราง: ลึกจริง h | ระดับ S | ลึกปรากฏ = h − S | n คำนวณ | n จริง | %err · กราฟลึกจริง–ลึกปรากฏ + ความชันผ่านจุดกำเนิด = n · CSV
- โหมดอัตโนมัติ: วาง S ที่ h − h/n (checkbox เลื่อนขึ้น 3 cm) · แผนภาพวาดรังสีหักเหจริง 2 เส้นจากปลาย O + แนวต่อ + ภาพ I + ค่าลึกจริง/ลึกปรากฏ
- แท็บวิธีทดลอง + ทฤษฎี (ที่มา d′ = d/n · กราฟ d′/d กับมุมมองเฉียง น้ำ/กลีเซอรีน · แผนภาพวิธีพาราแลกซ์ · ตาราง n)
- **ตรวจเชิงตัวเลข** (อ่านพิกเซล WebGL, ระบายสี O ม่วงแดง/S เขียวชั่วคราว, ตาเยื้อง ±2.5 cm): พาราแลกซ์เป็นศูนย์ที่ S = h − h/n — น้ำ h 20 → −0.5 px (buffer 1316 px), น้ำ h 10 → 0 px, กลีเซอรีน h 20 → 0.03 px · S คลาด 1 cm → เลื่อนสัมพัทธ์ ~10 px (เห็นชัด)
- ลงทะเบียน: `VLAB_SERIES` vpl02 lab-48 ใน kp-auth.js + admin.html (+ LAB_LIST) · labs_data.py (light · ม.5) → build virtual-lab.html (49) / library / admin LAB_META · protect script
- ตรวจ Browser pane: มุมจากตา/เฉียง/ข้าง, อัตโนมัติ + ตาราง, ของเหลวปริศนา, แท็บทฤษฎี, iPad 820 · ไม่มี console error

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/48. real-apparent-depth.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (รอผู้ใช้สั่ง)
- ยังไม่มีการ์ด Lab 46/47/48 ใน `virtual-physics-lab-02.html` และหน้าแรก
- lab แสงที่ยังไม่มี: มุมวิกฤต/สะท้อนกลับหมด (ต่อยอด shader ของ 48 ได้ง่าย), ปริซึม, สลิตคู่/เกรตติง, โพลาไรเซชัน

### หมายเหตุ
- protect script รายงาน "MOBILE" ทุกครั้งทั้ง 47 และ 48 (false positive เดิม ไม่มีผล)
- สูตร d′ = d/n ถูกต้องเมื่อมองเกือบตั้งฉาก — ตาอยู่เหนือแนวปลายเข็ม (x = 5.15) ถ้าเยื้องมากภาพจะยกสูงขึ้นตามฟิสิกส์จริง

## [2026-09-14 07:30] — NEW Lab 49 (VPL02) มุมวิกฤตและการสะท้อนกลับหมด (3D) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ย้ำ "อย่าลืมปุ่มรีเซต" → ยืนยันว่า Lab 48 มีปุ่ม ↺ รีเซตค่า และทดสอบแล้ว (h 20, S 16, สายตา 0/10, ปิดส่ายสายตา, มุมจากตา · ตาราง + n ปริศนาคงอยู่) · Lab 49 มีปุ่มรีเซตตั้งแต่แรก
- สร้าง `Virtual Physics Lab 02/49. critical-angle-total-internal-reflection.html` (~80 KB): แท่งครึ่งวงกลม R 6 cm หนา 2 cm บนกระดาษองศา (สเกล 1° รัศมี 12 cm วัดจากเส้นแนวฉาก 0–90 ทั้ง 4 ส่วน) · กล่องแสงหมุนรอบจุดศูนย์กลาง แสงเข้าผิวโค้งตามรัศมี
- **รังสีบนกระดาษ** คำนวณด้วยสเนลล์ + สมการเฟรเนล (แสงไม่โพลาไรซ์): รังสีตกกระทบ · หักเหออก (ความสว่าง T) · สะท้อน (R) ออกทางผิวโค้ง · วาดเป็นแถบแสงบนกระดาษใน shader ของกระดาษ (uniform segment arrays) → **มองผ่านแท่งแก้วเห็นแถบแสง/สเกลหักเหถูกต้อง** เพราะ shader ของแท่งแก้ว trace ไปที่ฟังก์ชันกระดาษเดียวกัน (ไม่มี mesh ลำแสงลอยที่จะไม่สอดคล้องกับการหักเห)
- แท่งแก้ว: ray tracing ใน fragment shader (ทรงกระบอก ∩ z ≥ 0 ∩ แผ่นหนา) refract เข้า → หาผิวออก → refract ออก/สะท้อนกลับหมด (วนได้ 8 ครั้ง) + Fresnel · depthWrite ปิด
- มุมมอง: ⬇ มุมบน (ค่าเริ่มต้น, ทิศเดียวกับแผนภาพ 2D) · มุมเฉียง · มุมต่ำ · ลากกล่องแสงในภาพ 3D/2D · สไลเดอร์ + ปุ่ม ±1°/±0.1°
- แผนภาพ 2D: กระดาษองศาตามสเกล + **แว่นขยายสเกล** (ขีด 0.5°) ที่จุดรังสีหักเหตัดขอบสเกล ใช้อ่าน θ₂ · บอก "ไม่มีรังสีหักเหออก" เมื่อสะท้อนกลับหมด
- โหมดวัดเอง (ไม่แสดง θ₂/n/θc): ตาราง A กรอก θ₂ ที่อ่านได้ → n = sin θ₂/sin θ₁ + n เฉลี่ย + กราฟ sin θ₂–sin θ₁ (ความชัน) · ตาราง B บันทึก θ₁ เป็นมุมวิกฤต → n = 1/sin θc, n จริง, %err · วัสดุ: อะคริลิก 1.49 · แก้วคราวน์ 1.52 · แก้วฟลินต์ 1.62 · ปริศนา (สุ่ม 1.40–1.75)
- โหมดอัตโนมัติ: แสดง θ₁ θ₂ n θc R% T% สถานะ + ปุ่มกวาดมุม 0→89° + กราฟ R/T กับ θ₁ + เส้น θc
- ↺ รีเซตค่า: θ₁ = 20°, มุมบน, หยุดกวาดมุม, ล้างช่องกรอก θ₂ · ไม่ลบตาราง ไม่เปลี่ยน n ปริศนา
- แท็บวิธีทดลอง (ตอน A สเนลล์ / ตอน B มุมวิกฤต / คำถาม) + ทฤษฎี (3 กรณี θ₁ เทียบ θc · กราฟเฟรเนล · ตารางมุมวิกฤต · เส้นใยนำแสง)
- ลงทะเบียน: `VLAB_SERIES` lab-49 ใน kp-auth.js + admin.html (+ LAB_LIST) · labs_data.py (light · ม.5) → build virtual-lab.html (50) / library / admin · protect
- ตรวจ Browser pane: มุมบน/เฉียง/ต่ำ, ใกล้ θc (41.5° อะคริลิก รังสีหักเหเกือบเลียดผิว), > θc สะท้อนกลับหมด, อัตโนมัติ (ฟลินต์ 30° → θ₂ 54.1°, R 8.5%), ตาราง A/B, รีเซต, ทฤษฎี, iPad 820 · ไม่มี console error

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/49. critical-angle-total-internal-reflection.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- Lab 48 + 49 ยังไม่ commit (รอผู้ใช้สั่ง)
- ยังไม่มีการ์ด Lab 46–49 ใน `virtual-physics-lab-02.html` และหน้าแรก
- lab แสงที่แนะนำต่อ: สลิตคู่/เกรตติง (บทแสงเชิงคลื่นยังไม่มี), สลิตเดี่ยว, ปริซึม, กระจกเงาราบ 2 บาน, โพลาไรเซชัน

### หมายเหตุ
- กล่องแสงไม่อยู่ในฉากที่ shader แท่งแก้ว trace — มองผ่านแท่งแก้วจากบางมุมจะไม่เห็นกล่องแสงด้านหลัง (ผลเล็กน้อย)
- [07:50] Lab 49 แก้ตาม feedback: กล่องแสงในแผนภาพ 2D หมุนผิดทิศ (rotate(−θ₁) → rotate(θ₁)) ตอนนี้แกนยาวของกล่องขนานลำแสง ช่องแสงหันเข้าจุดศูนย์กลาง · ป้าย "กล่องแสง" สีเข้มอ่านได้บนกระดาษ · ตรวจ 40° และ 70° ทั้ง 2D/3D
- [07:50] บั๊กลากค้าง (Lab 49 + Lab 48): ถ้าปล่อยเมาส์นอกหน้าต่าง drag ไม่ถูกยกเลิก → เลื่อนเมาส์ผ่านแคนวาสแล้วมุม/ตำแหน่งเปลี่ยนเอง · แก้: ตรวจ `e.buttons===0` ใน mousemove และยกเลิกเมื่อ window blur/touchcancel (Lab 47 ใช้โค้ดแบบเดิม ยังไม่ได้แก้)
- [08:05] Lab 49 แก้ตาม feedback: ตัวเลขบนกระดาษองศาไม่ตรงกับแว่นขยายสเกล — `labelProtractor()` เดิมวัดระยะถึงพหุคูณของ 90° (ทำให้ใกล้ผิวราบเป็น 0) → แก้เป็นมุมจากเส้นแนวฉาก min(m, |180−m|, 360−m): 0 ที่แนวฉาก 90 ที่ผิวราบ · ใช้ร่วมกันทั้งแผนภาพ 2D และ texture กระดาษ 3D · ตรวจ θ₁ 40° (อะคริลิก θ₂ 73.3°): รังสีตัดสเกลหลักระหว่าง 70–80 ตรงกับแว่นขยาย
- [08:30] Lab 49 ปรับตาม feedback: ① **เลเซอร์อยู่นอกวงสเกล** — กระดาษ 30 → 36 cm · เลเซอร์ที่รัศมี 15.2 (ช่องแสง 13.7) รังสีตกกระทบตัดวงสเกลรัศมี 12 ให้อ่าน θ₁ ได้ · แผนภาพ 2D วาดกระดาษสี่เหลี่ยมรอบวงสเกล (สูง 400 px) · กล้องมุมบนสูง 62 · เปลี่ยนคำ "กล่องแสง" → "เลเซอร์" ทั้งไฟล์ ② **แว่นขยาย 2 ช่อง**: รังสีตกกระทบ (ด้านแท่งแก้ว → θ₁) และรังสีหักเห (ด้านอากาศ → θ₂) · ③ โหมดวัดเองซ่อนตัวเลขมุม (สไลเดอร์ "หมุนเลเซอร์" ไม่มีค่า) — นักเรียนกรอก θ₁ และ θ₂ ที่อ่านได้เอง · ตาราง A ใช้ค่าที่กรอกทั้งคู่ · ตาราง B บันทึก θ₁ ที่กรอกเป็น θc · โหมดอัตโนมัติแสดงค่ามุมเหมือนเดิม · รีเซตล้างช่องกรอกทั้งสอง · ข้อความวิธีทดลองอัปเดต · ตรวจ θ₁ 20° (θ₂ 30.6°) และ 40° (θ₂ 73.3°) ตรงกับแว่นขยายทั้งสองช่อง
- [08:50] แก้บั๊กลากค้างใน Lab 47 (แบบเดียวกับ 48/49): แผนภาพ 2D ตรวจ `e.buttons===0` แล้วเลิกลาก + ยกเลิกเมื่อ window blur/touchcancel · ภาพ 3D ยกเลิกการลาก (เข็ม/สายตา/หมุนมุมมอง) เมื่อไม่ได้กดปุ่มเมาส์ · ทดสอบ: ปล่อยนอกหน้าต่างแล้วเลื่อนเมาส์ผ่าน S ไม่ขยับ (80 cm คงเดิม) และลากปกติยังใช้ได้ (80 → 69.9) · Lab 48 เพิ่ม touchcancel/blur ให้ครบ · ยังไม่ commit
- [09:15] เพิ่มการ์ด Lab 46, 47, 48, 49 ใน `virtual-physics-lab-02.html` (หมวดแสง 5 → 9 simulations · hero stat 11 → 23 ตามจำนวนการ์ดจริง) และ `index.html` (section Virtual Lab, data-topic="light" · chip แสง 3 → 7 · ทั้งหมด 19 → 23 · ข้อความ "46 การทดลอง" → 50) · preview canvas ใหม่ 4 ตัวในทั้งสองไฟล์: `vpl2-concave` (กระจกเว้า ภาพจริงกลับหัว วัตถุขยับ), `vpl2-parallax` (ตาส่าย เข็ม O/ภาพ/S), `vpl2-depth` (ถังน้ำ รังสีหักเห ภาพลอยขึ้น S เลื่อนหาภาพ), `vpl2-critical` (เลเซอร์กวาดมุม รังสีหักเหจางตามเฟรเนล → สะท้อนกลับหมด) · ตรวจทั้งสองหน้าใน Browser pane ไม่มี console error · ยังไม่ commit

## [2026-09-14 10:00] — NEW Lab 50 (VPL02) โพลาไรเซชันของแสง · กฎของมาลุส (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/50. polarization-malus-law.html` (three.js ปกติ ไม่ใช้ shader): หลอดไฟไม่โพลาไรซ์ 800 W/m² → P₁ → (P₃ แผ่นกลาง ใส่/ถอดได้) → P₂ → หัววัด · ลอยตามแนวลำแสง ไม่มีราง/ขาตั้ง
- **เวกเตอร์สนามไฟฟ้า E ในภาพ 3D** (LineSegments อัปเดตทุกเฟรม): ก่อน P₁ ทิศสุ่มต่อความยาวคลื่น (ไม่โพลาไรซ์) · หลังแต่ละแผ่นสั่นตามแกน u(φ) = (0, cos φ, sin φ) แอมพลิจูด ∝ √I · เส้นเชื่อมปลายเวกเตอร์ · ลำแสงโปร่งแสงความสว่าง ∝ √I · หัววัดเรืองตาม I
- ฟิสิกส์: I หลัง P₁ = I_src/2 · I ← I cos²(Δφ) ทุกแผ่น · E = √(2I/(cε₀)) → E₀ = 549.0 V/m, I₀ = 400 W/m² · มิเตอร์ E (V/m) และ I (W/m²) บนแผง + จอบนหัววัด 3D · โหมดวัดเองแกว่ง ±0.3%
- มุมวัดจากแนวดิ่ง ทวนเข็มนาฬิกาเมื่อมองสวนลำแสง — ตรงกันทั้ง 3D (วงแหวนสเกลคงที่ + แผ่นหมุนมีลูกศรแกน) และหน้าปัด 2D · มุมมอง: มุมเฉียง · มุมข้าง · 👁 มองสวนลำแสง (ซ่อนหัววัด)
- 2D: หน้าปัด P₁/(P₃)/P₂ ลากหมุนได้ + แว่นขยายสเกลใต้หน้าปัด (ขีด 0.5°) · แผนภาพเวกเตอร์ E₀ → องค์ประกอบ E₀ cos θ บนแกน P₂ + แท่ง E/E₀ กับ I/I₀
- โหมดวัดเอง: ซ่อนตัวเลขมุม · กรอกมุม P₁ P₂ (P₃) ที่อ่านได้ → บันทึกพร้อม E, I จากมิเตอร์ · ตาราง A (θ, cos θ, cos²θ, E, I, E/E₀, I/I₀ — E₀ I₀ จากแถว θ = 0) · ตาราง B 3 แผ่น (α, β, I, I/I₀, cos²α·cos²β) · กราฟ E–cos θ, I–cos²θ (ความชัน = E₀, I₀) และ E/E₀, I/I₀–θ · CSV
- โหมดอัตโนมัติ: แสดงมุม θ cos θ cos²θ E₀ I₀ อัตราส่วน สถานะ + ปุ่มหมุน P₂ อัตโนมัติ
- ↺ รีเซตค่า: P₁ 0°, P₂ 30°, P₃ 45°, มุมเฉียง, หยุดหมุน, ล้างช่องกรอก · ไม่ลบตาราง · มีแก้ลากค้าง (e.buttons/blur/touchcancel) ตั้งแต่แรก
- แท็บวิธีทดลอง (ตอน A 2 แผ่น / ตอน B 3 แผ่น / คำถาม) + ทฤษฎี (ไม่โพลาไรซ์→โพลาไรซ์ · องค์ประกอบ E₀ cos θ · กราฟ · 3 แผ่น (I₀/4) sin²2α · ตาราง · การนำไปใช้)
- ตรวจ: θ 0/30/60/90° → E 549.0/475.4/274.5/0 V/m, I 400/300/100/0 W/m² · 3 แผ่น (0,45,90) → I 100, E 274.5 · มองสวนลำแสง: แกน P₂ 30° อยู่บนซ้ายตรงกับหน้าปัด 2D · รีเซต · ไม่มี console error
- ลงทะเบียน: VLAB_SERIES lab-50 (kp-auth.js + admin.html + LAB_LIST) · labs_data.py → build (51) · protect · การ์ด + preview `vpl2-polar` ใน virtual-physics-lab-02.html (แสง 10, hero 24) และ index.html (แสง 8, ทั้งหมด 24, "51 การทดลอง")

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/50. polarization-malus-law.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit: การ์ด 46–49 (entry 09:15) + Lab 50 ทั้งหมด
- lab แสงที่ยังไม่มี: สลิตคู่/เกรตติง, สลิตเดี่ยว, ปริซึม, กระจกเงาราบ 2 บาน
- [10:20] Lab 50 เพิ่มการแสดง**ความสว่าง**ตามที่ผู้ใช้ขอ: ① 3D — จอรับแสงหน้าหัววัด (พื้นจอสว่างขึ้น + จุดแสงวงกลม + แสงฟุ้ง sprite) ความสว่าง = (I/I₀)^(1/2.2) (แก้แกมมาให้ตามองเห็นใกล้เคียงจริง) แทนเซนเซอร์ emissive เดิม ② 2D — ช่อง "ความสว่างบนจอ" (gradient ขาวอุ่นตาม I) ข้างแท่ง E/E₀ และ I/I₀ · ตรวจ θ = 0° สว่างเต็ม, θ = 70° สลัว (I 46.7) · ไม่มี console error · ยังไม่ commit
- [10:40] Lab 50 แก้ตาม feedback "ใส่แผ่นที่สามแล้วเปลี่ยนมุมมอง 3D ไม่ได้": สาเหตุ — การลากในภาพ 3D ตรวจการชนกับทั้งกลุ่มแผ่นโพลารอยด์ รวมป้ายชื่อ (sprite กว้าง 12 cm) · พอมี 3 แผ่นเกือบทุกจุดกลางภาพโดนแผ่น/ป้าย → กลายเป็นหมุนแผ่นแทนหมุนมุมมอง · แก้: ① จับได้เฉพาะตัวแผ่นและวงแหวนสเกล (ไม่รวมป้าย) ② กดบนแผ่นแล้วตัดสินจากทิศที่ลากก่อน: ขึ้น-ลง = หมุนแผ่น · ซ้าย-ขวา = หมุนมุมมอง · ข้อความ HUD อัปเดต · ทดสอบด้วย mouse event จำลองบนแผ่น P₃: ลากแนวนอน → มุมมองหมุน (Δaz −0.48) แผ่นไม่ขยับ · ลากแนวตั้ง → P₃ หมุน 20° มุมมองคงที่ · ปุ่มมุมข้าง/เฉียงใช้ได้ · ยังไม่ commit

## [2026-09-14 11:40] — NEW Lab 51 (VPL02) ปริซึม: มุมเบี่ยงเบนน้อยที่สุดและการกระจายแสง (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/51. prism-minimum-deviation-dispersion.html` โครงเดียวกับ Lab 49 (กระดาษ shader + เส้นแสงบนกระดาษ + วัตถุแก้ว ray tracing)
- ปริซึมสามเหลี่ยมด้านเท่า A = 60° ด้าน 6 cm สูง 2.5 cm (ExtrudeGeometry) บน**แท่นหมุนรอบจุดกึ่งกลางผิวรับแสง** (จุดตกกระทบอยู่ที่เดิม) · i = 30° + ρ · เข็มชี้บนแท่น + สเกล i 0–90° บนกระดาษ · แหล่งกำเนิดแสงคงที่ยิงตาม +x
- **ติดตามรังสี 2D ใน JS** (`trace(λ)`): สเนลล์แบบเวกเตอร์ทุกผิว + เฟรเนล (แสงสะท้อนจางที่ผิวรับแสง) + สะท้อนกลับหมดเมื่อ i น้อย · n(λ) สูตรโคชี: คราวน์ 1.5046+4200/λ² · ฟลินต์ 1.5854+12000/λ² · อะคริลิก 1.4828+3100/λ² · ปริศนาสุ่ม A,B
- แสง: เลเซอร์แดง 650 / เขียว 532 / ม่วง 405 / แสงขาว (7 ความยาวคลื่น สีรวมเป็นขาว) · เส้นแสงสีต่อส่วนใน shader (uniform สี vec3 32 ส่วน) → 3D เห็นสเปกตรัมกระจายบนกระดาษ · shader ปริซึมใช้ระนาบข้าง 3 ระนาบจาก JS (uPN/uPD) หักเหจริงเมื่อมองผ่าน
- วัด δ: ✏️ ต่อแนวรังสีด้วยดินสอ (เส้นประบนกระดาษทั้ง 2D/3D) + 📐 โปรแทรกเตอร์วางที่จุดตัดแนวรังสีตกกระทบกับแนวต่อรังสีออก (2D) · แว่นขยาย 2 ช่อง: เข็มชี้แท่นหมุน (i) · โปรแทรกเตอร์ (δ, แสงขาวแสดงทุกสี)
- โหมดวัดเอง: ซ่อนตัวเลขมุม · กรอก i, δ ที่อ่านได้ · ตาราง A (i, δ) + กราฟ δ–i บอกจุดต่ำสุดในข้อมูล · ตาราง B บันทึก δmin → n = sin((60+δmin)/2)/sin30 + n จริงที่ λ นั้น + %err · โหมดอัตโนมัติ: i r₁ r₂ e δ δmin(ทฤษฎี) + กราฟ δ(i) ทฤษฎี + ปุ่มหมุนอัตโนมัติ
- ↺ รีเซตค่า: i = 40°, มุมบน, หยุดหมุน, ล้างช่องกรอก, เปิดดินสอ · ไม่ลบตาราง ไม่เปลี่ยนวัสดุปริศนา · มีแก้ลากค้าง
- แท็บวิธีทดลอง (ตอน A หา δmin / ตอน B การกระจายแสง / คำถาม) + ทฤษฎี (แผนภาพ i r₁ r₂ e δ คำนวณจริง · กราฟ δ–i คราวน์/ฟลินต์ · สเปกตรัม · ตาราง n 3 ความยาวคลื่นสร้างจากสูตรเดียวกับ sim)
- ตรวจ: คราวน์ แดง i 40° → r₁+r₂ = 60.00°, δ = i+e−A ตรงกับ tracer · i 49.2° → δ 38.450° vs δmin ทฤษฎี 38.448° → n จาก δmin 1.5146 vs 1.5145 · แสงขาวฟลินต์เห็นสเปกตรัม 3D · ตาราง/รีเซต · แก้แผนภาพทฤษฎีรูปที่ 1 ที่วาดรังสีผิดให้ใช้ refr() จริง · ไม่มี console error
- ลงทะเบียน lab-51 (kp-auth.js + admin.html + LAB_LIST) · labs_data.py → build (52) · protect · การ์ด + preview `vpl2-prism` ใน virtual-physics-lab-02.html (แสง 11, hero 25) และ index.html (แสง 9, ทั้งหมด 25, "52 การทดลอง")

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/51. prism-minimum-deviation-dispersion.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit
- lab แสงที่ยังไม่มี: สลิตคู่/เกรตติง, สลิตเดี่ยว, กระจกเงาราบ 2 บาน

## [2026-09-14 13:30] — NEW Lab 52 (VPL02) รุ้งปฐมภูมิและทุติยภูมิในห้องทดลอง (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/52. rainbow-primary-secondary.html` — การทดลองที่ทำได้จริง: ทรงกระบอกใสบรรจุน้ำ (R = 1.5 cm สูง 8 cm) บนกระดาษขาว 64 × 64 cm · n น้ำแบบโคชี 1.3242 + 3000/λ²
- **ตอน A เลเซอร์** (แดง 650 / ม่วง 405): เลื่อนเลเซอร์ระยะ b (ไม้บรรทัด mm บนกระดาษ) · ติดตามรังสีแบบเวกเตอร์: สะท้อนผิวนอก · ทะลุ · สะท้อนภายใน 1 ครั้ง (ปฐมภูมิ) · 2 ครั้ง (ทุติยภูมิ) พร้อมเฟรเนลทุกผิว → เส้นแสงบนกระดาษ (shader) · เลือกวัดรังสีปฐมภูมิ/ทุติยภูมิ · ✏️ ต่อแนวรังสี + 📐 โปรแทรกเตอร์ที่จุดตัดกับแนวลำแสง · แว่นขยาย b (ไม้บรรทัด) และ θ (โปรแทรกเตอร์) · กรอบขยายทรงกระบอก + โปรแทรกเตอร์ปรับขนาดอัตโนมัติ · ตาราง A + กราฟ θ–b (โหมดอัตโนมัติมีเส้นทฤษฎี θ₁ = 4r−2i, θ₂ = 180°+2i−6r)
- **ตอน B แสงขาวลำกว้าง** (ห้องมืด): ติดตามรังสี 7 สี × 2,600 เส้น (สุ่มตำแหน่งในช่อง) สะสมแสงลงกริด 1280² Float32 (DDA) → tone map แล้วซ้อนบนกระดาษมืด เป็น texture ของกระดาษ 3D + แผนภาพ 2D (~0.5 s) · เห็นแถบรุ้งจริงด้านไฟฉาย แดงอยู่นอก ม่วงใน · แว่นขยายวงสเกลรัศมี 28 cm ช่วง 35°–60° (สุ่มสีจากกริด ความสว่าง ×6) · ตาราง B เลือกขอบสีของแถบ บันทึก θ แล้วเฉลย θ ทฤษฎีของขอบสี (680/410 nm)
- 3D: ทรงกระบอกน้ำ ray tracing (หักเห/สะท้อนกลับหมด) มองผ่านเห็นกระดาษ/เส้นแสงหักเหจริง · มุมมอง 🔍 มุมใกล้ / ⬇ ทั้งแผ่น / มุมเฉียง · ลากเลเซอร์ใน 3D/2D
- โหมดวัดเองซ่อนตัวเลข b และ θ · ↺ รีเซตค่า: b 10 mm, วัดปฐมภูมิ, เปิดดินสอ, มุมมองเริ่มต้นตามตอน, ล้างช่องกรอก (ไม่ลบตาราง) · แก้ลากค้างตั้งแต่แรก
- แท็บวิธีทดลอง (อุปกรณ์หาได้จริง · ตอน A/B · คำถาม) + ทฤษฎี (ทางเดินแสงในหยดน้ำจาก tracer จริง · กราฟ θ–b แดง/ม่วง + แถบมืดอเล็กซานเดอร์ · รุ้งบนท้องฟ้า)
- **ตรวจเชิงตัวเลข**: ค่าสุดขีดจาก tracer (สแกน b ละเอียด 0.005 mm) ตรงกับสูตรเดส์การ์ต — แดง θ₁max 42.326° / θ₂min 50.444° · ม่วง 40.718° / 53.347° ที่ b/R 0.86 และ 0.95 · ภาพ 3D ตอน B แถบรุ้งอยู่ที่ ~42° บนวงสเกล สีแดงด้านนอก
- แก้ระหว่างตรวจ: กระดาษสว่างกลบแถบรุ้ง → ทำห้องมืด · ลายเส้นซ้ำ → สุ่มตำแหน่งรังสี · แผนภาพทฤษฎีรุ้งบนฟ้าสีทุติยภูมิสลับผิด → แดงใน 50.4° ม่วงนอก 53.3° · clip กราฟ/รูปทฤษฎี · preview การ์ดเขียนใหม่ด้วยเวกเตอร์
- ลงทะเบียน lab-52 (kp-auth.js + admin.html + LAB_LIST) · labs_data.py → build (53) · protect · การ์ด + preview `vpl2-rainbow` ใน virtual-physics-lab-02.html (แสง 12, hero 26) และ index.html (แสง 10, ทั้งหมด 26, "53 การทดลอง")

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/52. rainbow-primary-secondary.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit
- ตอน B: การอ่านบนวงสเกลคลาดจากทฤษฎี ~1–2° (รังสีออกจากขอบทรงกระบอก ไม่ใช่จุดศูนย์กลาง) — อธิบายไว้ในทฤษฎีและคำถาม
- lab แสงที่ยังไม่มี: สลิตคู่/เกรตติง, สลิตเดี่ยว, กระจกเงาราบ 2 บาน
- [14:10] Lab 52 ตอน B แก้ตาม feedback "โหมดแสงขาววัดแปลก ๆ": **สาเหตุ** — แถบรุ้งเป็นแถบตรงของรังสีขนาน ออกห่างแกนทรงกระบอก ~0.86R (ปฐมภูมิ) / 0.95R (ทุติยภูมิ) ไม่ได้พุ่งจากจุดศูนย์กลาง · วงสเกลรัศมี 28 cm รอบทรงกระบอกจึงอ่านได้ ปฐมภูมิแดง 44.8° (ทฤษฎี 42.4°) ทุติยภูมิแดง 48.0° (ทฤษฎี 50.3°) คลาด ±2.4° และขึ้นกับระยะ · **แก้**: เอาวงสเกลออก → เพิ่ม "📐 ไม้วัดมุม" (ไม้บรรทัดใส + โปรแทรกเตอร์) วัดทิศของแถบเทียบแนวลำแสง: จุดหมุน (คลิก/ลากในภาพรวม 2D) · หมุนไม้ (สไลเดอร์ ±1/±0.1° หรือลากในกรอบขยาย) · เลือกซีกบน/ล่าง · กรอบขยาย ±3.5 cm รอบจุดหมุนแสดงแสงจากกริด (×3) + ไม้วัด + เส้นขนานแนวลำแสง + โปรแทรกเตอร์ · แว่นขยายอ่านมุมไม้วัด · 3D วาดไม้วัดเรืองแสงจางบนกระดาษมืด · ห้องมืดสว่างขึ้นเล็กน้อย (0.74 → 0.66) · โหมดวัดเองซ่อนตัวเลข · รีเซตคืนไม้วัด · ข้อความวิธีทดลอง/คำถาม/ทฤษฎีอัปเดต · **ตรวจ**: ทิศแถบจากจุดยอดความสว่างที่รัศมี 16 และ 29 cm — ปฐมภูมิแดง 42.14° (ทฤษฎี 42.42°) ม่วง 40.56° (40.78°) · ทุติยภูมิม่วง 53.09° (53.23°) · ไม้วัดที่ 42.4° ขนานแถบในภาพ 3D และกรอบขยาย · ไม่มี console error · ยังไม่ commit
- [14:35] Lab 52 ตอน B ตาม feedback "ที่วัดมุมน่าจะเลื่อนขยับได้": ที่วัดมุมเป็น**อุปกรณ์ 3D จริงบนกระดาษ** — โปรแทรกเตอร์ครึ่งวงกลมใส (ฐานขนานแนวลำแสง · texture แยกซีกบน/ล่าง ตัวเลขไม่กลับด้าน) + ไม้บรรทัดใสมีเส้นกลางสีฟ้าหมุนรอบจุดกลาง (แทนเส้นเรืองแสงใน shader) · **เลื่อน/หมุนได้ทุกที่**: 3D ลากจุดกลางโปรแทรกเตอร์ = เลื่อน · ลากที่ไม้บรรทัด = หมุน (มุมมองไม่หมุนตาม) · กรอบขยาย 2D ลากใกล้จุดกลาง = เลื่อน · ลากที่อื่น = หมุน · ภาพรวม 2D คลิก/ลาก = ย้าย · ปุ่ม ◀▲▼▶ ทีละ 2 mm · ข้ามแนวลำแสงแล้วสลับซีกอัตโนมัติ · ตรวจด้วย mouse event จำลองใน 3D: เลื่อน (−19,−10) → (−16.83,−11.08) · หมุนเป็น 45.1° · orbit ไม่เปลี่ยน · ทิศไม้บรรทัด 3D ตรงกับ armDir() ทั้งซีกบน (42.4°) และล่าง (50.3°) · ไม่มี console error · ยังไม่ commit
- [15:10] Lab 52 ตอน B เพิ่ม **📄 ฉากเล็กรับแสง** ตามที่ผู้ใช้ขอ (ให้เห็นว่ารุ้งสองแถบหันสีคนละด้าน): การ์ดขาว 9 × 4 cm ตั้งบนกระดาษ หน้าหันเข้าทรงกระบอก ตามแนว 46° ซีกเดียวกับที่วัดมุม · ติ๊กเปิด/ปิด + สไลเดอร์ระยะ 12–28 cm (เริ่ม 24) · สีบนการ์ดสุ่มจากกริดแสงตามแนวการ์ด ใช้การย่อช่วงความสว่างแบบคงสี L/(L+k) + แกมมา 1.8 ให้เห็นแถบทุติยภูมิที่จางโดยสีแถบปฐมภูมิไม่กลายเป็นขาว · 3D มีเงาหลังการ์ดบนกระดาษ (shader ตรวจลิ่มหลังการ์ด) · แผนภาพ 2D: เส้นการ์ดในภาพรวม + ช่อง "ฉากเล็ก (มองจากทรงกระบอก)" พร้อมป้าย ใกล้/ไกลแนวลำแสง · วิธีทดลองเพิ่มข้อสังเกตลำดับสี
- [15:10] **ปรับทรงกระบอกเล็กลง R 1.5 → 0.75 cm** (หลอดทดลอง Ø 1.5 cm): ตรวจโปรไฟล์บนการ์ดพบว่า R 1.5 cm ที่ระยะ 20 cm แถบปฐมภูมิกับทุติยภูมิชิดกันจนแถบมืดหาย (ออฟเซ็ต 0.86R/0.95R ทำให้ตำแหน่งแถบเลื่อนเข้าหากัน) · หลังปรับ ที่ระยะ 22 cm: แดงปฐมภูมิ 43.7° · แดงทุติยภูมิ 49.1° · ม่วงทุติยภูมิ 51.5° · แถบมืดสว่างเพียงครึ่งหนึ่งของแถบทุติยภูมิ → เห็นลำดับสีกลับกันชัด · ลำแสงกว้าง 44 → 28 mm · ตอน A: b สูงสุด 7.5 mm (สไลเดอร์/กราฟ/กรอก/กวาดอัตโนมัติ) · มุมรุ้งจาก tracer ยังตรงทฤษฎี (แดง 42.326° ที่ b 6.46 mm) · ข้อความวิธีทดลอง/ทฤษฎีอัปเดต · ไม่มี console error · ยังไม่ commit

## [2026-09-14 16:30] — NEW Lab 53 (VPL02) การแทรกสอดของแสง: สลิตคู่และเกรตติง (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/53. double-slit-diffraction-grating.html`: เลเซอร์ → แผ่นสลิต (x = 0) → ฉากขาวกว้าง 120 cm มีสเกล mm (x = L 50–200 cm) · ตลับเมตรบนโต๊ะ (0 ที่แผ่นสลิต)
- **ลวดลายบนฉากคำนวณใน fragment shader ทุกพิกเซล**: สลิตเดี่ยว (sinβ/β)² · สลิตคู่ (sinβ/β)² cos²α (เฉลี่ย cos² ภายในความกว้างพิกเซลแบบวิเคราะห์ ไม่เกิดลายมัวเร) · เกรตติง = จุดขนาดลำแสง (σ 0.12 cm) ที่ d sin θ = nλ คูณ envelope · ใช้ sin θ = z/√(z²+L²) (ไม่ประมาณมุมเล็ก) · ความสว่างที่แสดงปรับได้
- แผ่นสลิต: เดี่ยว a 0.08/0.12/0.16 mm · คู่ d 0.25/0.50 mm (a 0.08) · เกรตติง 100/300/600 เส้น/mm · เลเซอร์ 650/532/405 nm + ปริศนา (สุ่ม 420–680 nm)
- 3D: มุมมอง 🎯 มองที่ฉาก (กล้องตามแว่นขยาย ลากเลื่อนได้) · มุมเฉียง · มุมข้าง · ลำแสงไปยังจุดสว่างของเกรตติง · ป้ายชื่อแผ่นสลิต
- แผนภาพ 2D: การจัดอุปกรณ์มองบน · กราฟความเข้มทั้งฉาก (คลิกเลือกตำแหน่ง) · **แว่นขยายสเกลบนฉาก** (ความกว้างปรับตามระยะแถบ ลากเลื่อน ขีด mm)
- โหมดวัดเอง: ซ่อนตำแหน่งแว่นขยายและ λ ปริศนา · กรอก n และ x ที่อ่านได้ → λ = d x/(nL) (คู่), a x/(nL) (เดี่ยว วัดแถบมืด), d sin(tan⁻¹(x/L))/n (เกรตติง) · ตาราง + λ จริงเฉลยหลังบันทึก + %err · กราฟ x–n (ความชัน = Δx) · โหมดอัตโนมัติ: λ, d, Δx, θ₁, x₁ และตำแหน่งแถบ
- ↺ รีเซตค่า: L 120 cm, แว่นขยาย 0, ความสว่าง ×4, มองที่ฉาก, ล้างช่องกรอก (ไม่ลบตาราง ไม่เปลี่ยน λ ปริศนา) · มีแก้ลากค้าง
- แท็บวิธีทดลอง (ตอน A สลิตคู่ / B เกรตติง / C สลิตเดี่ยว / คำถาม) + ทฤษฎี (ความต่างทางเดิน d sin θ · ลวดลายเดี่ยว/คู่/เกรตติง 6 ช่องพร้อม envelope · มุมลำดับของเกรตติง 3 สี)
- **ตรวจ**: สลิตคู่ แดง d 0.25 L 120 → Δx 0.312 cm = x₁ · ความเข้มกึ่งกลางระหว่างแถบ ~0 · สลิตเดี่ยว แถบมืดแรก 0.975 cm ความเข้ม ~0 · ยอดที่สอง 4.7% (ทฤษฎี 4.7%) · เกรตติง 300 เส้น/mm เขียว → x₁ 19.40 cm บนสเกลฉากตรงแว่นขยาย คำนวณกลับ λ = 532.00 nm · บันทึก/รีเซต · ไม่มี console error
- ลงทะเบียน lab-53 (kp-auth.js + admin.html + LAB_LIST) · labs_data.py → build (54) · protect · การ์ด + preview `vpl2-slit` ใน virtual-physics-lab-02.html (แสง 13, hero 27) และ index.html (แสง 11, ทั้งหมด 27, "54 การทดลอง")

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/53. double-slit-diffraction-grating.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit
- lab แสงที่ยังไม่มี: กระจกเงาราบ 2 บาน · Lab 34 ยังเป็น 2D · 33B fallback เครื่องเก่า · VPL03 catalog
- [17:00] Lab 53 เพิ่ม **⚪ แสงขาว** (หลอดไฟ + ช่องแคบ 400–700 nm) ตามที่ผู้ใช้ขอ: **เกรตติง** — สเปกตรัมต่อเนื่องแบบวิเคราะห์ใน shader: แต่ละลำดับ m ที่ตำแหน่ง z รับ λ = d sin θ/m ความเข้มต่อความยาว ∝ dλ/dz × envelope ของช่อง (ขอบ 400/700 นุ่ม) · แถบกลางสีขาว · ม่วงใกล้กลาง แดงไกล · ลำดับ 2–3 ซ้อนกัน (ตรวจ: 300 เส้น/mm L 120 → ลำดับ 1 ม่วง 14.50 cm แดง 25.77 cm ตรงกับภาพบนสเกลฉาก) · สลิตคู่/เดี่ยว — รวม 12 ความยาวคลื่นถ่วงสีให้รวมเป็นขาว (แถบกลางขาว แถบข้างมีสี) · JS `intensityRGB()` ใช้สูตรเดียวกันสำหรับกราฟความเข้มและแว่นขยาย (สี RGB) · แผนภาพบนวาดลำแสงม่วง/แดงแต่ละลำดับ · 3D ลำแสงไปขอบม่วง/แดง · บันทึกแสงขาว: คำนวณ λ ของสีที่วัด (λ จริง/%err แสดง "—") ตรวจ x 20.2 cm → 553.3 nm · โหมดอัตโนมัติแสดงช่วงตำแหน่งม่วง–แดงแต่ละลำดับ · เกรตติงเปลี่ยนความกว้างช่อง a = 0.45d → 0.25d ให้เห็นลำดับที่ 2–3 (เดิม envelope ดับลำดับที่ 2) · วิธีทดลองเพิ่มขั้นแสงขาว · ไม่มี console error · ยังไม่ commit
- [17:15] Lab 53 แก้ตาม feedback "แสงขาวผ่านสลิตคู่/เดี่ยวปกติไม่เห็นการแทรกสอด": จำกัด **แสงขาวใช้กับเกรตติงเท่านั้น** — ปุ่มแสงขาวปิดใช้งาน (จางลง + tooltip) เมื่อเลือกสลิตคู่/เดี่ยว · ถ้ากำลังใช้แสงขาวแล้วเปลี่ยนเป็นสลิตคู่/เดี่ยว เปลี่ยนกลับเป็นเลเซอร์แดงอัตโนมัติ · ถ้าพยายามเลือกจะขึ้นคำอธิบาย (แหล่งกำเนิดกว้าง ไม่อาพันธ์ ลวดลายแต่ละจุดเลื่อนซ้อนจนกลืน + แต่ละสีระยะแถบต่างกัน) · เพิ่ม note ในแท็บทฤษฎี (ทำไมเกรตติงใช้แสงขาวได้ · ยังใช้รูเล็กจึงเห็นแถบสีจาง ๆ) และข้อความในวิธีทดลอง · ตรวจการสลับทุกกรณีแล้ว · ไม่มี console error · ยังไม่ commit
- [17:40] Lab 53 เพิ่มการเปลี่ยนระยะฉาก L นอกจากสไลเดอร์: ① ปุ่ม −10 / −1 / +1 / +10 cm ② **ลากฉากในภาพ 3D** (มุมเฉียง/มุมข้าง) — จับที่ฉากแล้วเลื่อนตามตลับเมตร ใช้ระนาบที่มีแกน x และหันเข้ากล้องมากที่สุดผ่านจุดที่จับ ฉากจึงเลื่อนตามเคอร์เซอร์พอดี · ตรึงกรอบกล้องระหว่างลาก (มุมข้างตั้งกรอบคงที่ 0–200 cm) ③ **ลากฉากในแผนภาพการจัดอุปกรณ์ 2D** — ตำแหน่งฉากในแผนภาพเป็นสัดส่วนกับ L แล้ว · ตรวจด้วย mouse event จำลอง: มุมข้าง 120 → 170 cm ได้ 170 · มุมเฉียง → 90 ได้ 90, → 185 ได้ 185 · แผนภาพ 2D → 150 ได้ 150 · ไม่มี console error · ยังไม่ commit
- [17:55] Lab 53 ตาม feedback "เลื่อนฉากแล้วอยากให้สเกลเท่าเดิม แต่ลายแทรกสอดเปลี่ยน": ① แว่นขยาย 2D ความกว้างขึ้นกับแผ่นสลิตเท่านั้น (สลิตคู่ d 0.25 → ±1.5 cm · d 0.50 → ±0.8 · เดี่ยว a 0.08/0.12/0.16 → ±4/3/2 · เกรตติง ±2) ไม่ขึ้นกับ L และ λ อีกต่อไป ② กล้องมุมเฉียง/มุมข้างใช้กรอบคงที่ (ไม่ตาม L) · มุม "มองที่ฉาก" อยู่ห่างฉากคงที่ 18 cm อยู่แล้ว → เลื่อนฉากหรือเปลี่ยนสี สเกลบนฉาก/แว่นขยายขนาดคงเดิม เห็นแถบขยาย-หดตามจริง · ตรวจ: สลิตคู่ d 0.25 แดง L 60 → Δx 0.156 cm, L 180 → 0.468 cm ในแว่นขยายกว้างเท่ากัน (±1.5 cm) · ไม่มี console error · ยังไม่ commit
- [18:15] Lab 53 เพิ่ม **🔍 ความละเอียดสเกล**: ปุ่มเลือกความกว้างแว่นขยาย อัตโนมัติ (ตามแผ่นสลิต) / 1 / 3 / 6 / 15 / 40 cm · ขีดสเกลปรับตามความละเอียด (ขีดเล็ก 0.1 mm / 1 mm / 5 mm / 1 cm ให้ห่างกันอย่างน้อย 7 px · ขีดกลางทุก 5 · ขีดใหญ่ทุก 10) ตัวเลขเว้นระยะไม่ทับกันและทศนิยมตามขนาดขีด · มุม "มองที่ฉาก" ถอยกล้องตามความกว้างที่เลือก (ขั้นต่ำ 14 cm ให้เห็นทั้งลายและสเกล) · เลื่อนฉากสเกลยังคงที่ · รีเซตกลับเป็นอัตโนมัติ · ตรวจ: 1 cm → ขีด 0.1 mm ตัวเลข −0.1…0.8 cm แถบสว่างที่ 0.31 cm ตรงกลาง · 40 cm (เกรตติง 300 เส้น/mm แดง) → ขีด 5 mm ตัวเลขทุก 5 cm จุดสว่างที่ 0 และ 24.0 cm · ไม่มี console error · ยังไม่ commit

## [2026-09-14 20:25] — NEW หมวดไฟฟ้าสถิต · Lab 54 (VPL02) อิเล็กโทรสโคปและการทำให้วัตถุมีประจุ (3D) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ขอชุดแลปไฟฟ้าสถิตตามหลักสูตร สสวท. + สากล ให้ทำ "เรียงลำดับเลย" — แผน: 54 อิเล็กโทรสโคป · 55 กฎของคูลอมบ์ · 56 สนามไฟฟ้า/เส้นสนาม · 57 เส้นศักย์เท่ากัน · 58 ตัวเก็บประจุแผ่นขนาน · 59 อัด-คายประจุ RC · 60 หยดน้ำมันมิลลิแกน
- สร้าง `Virtual Physics Lab 02/54. electroscope-charging-induction.html` (3D): อิเล็กโทรสโคปแผ่นโลหะบางในกล่องโลหะมีกระจก + การ์ดสเกลมุม 0–60° ด้านหลัง · แท่ง PVC/ผ้าขนสัตว์ (−) · แท่งแก้ว/ผ้าไหม (+) · แท่งปริศนา X (สุ่มชนิดประจุ ซ่อนจนกว่าจะบันทึกตาราง B) · ถู 1/5 ครั้ง (ผ้าเลื่อนบนแท่ง) · ลากแท่งใน 3D/2D ตามไม้บรรทัด (0 ที่ขอบจาน) · แตะจาน = วาง/ยกนิ้ว (ต่อลงดิน)
- **แบบจำลอง**: ตัวนำชิ้นเดียว ศักย์ V เท่ากันทั้งชิ้น · แผ่นโลหะถูกกล่องกำบัง → Q_จาน = C_จาน(V−φ), Q_แผ่น = C_แผ่น V (6 pF/4 pF) · φ = kq(1/r − 1/0.45 m) (ผลกำบังสิ่งแวดล้อม เดิม 1/r ทำให้แท่งที่ 40 cm ยังกาง 4.8°) · ต่อดิน V = 0 · สัมผัส: ประจุบนแท่ง (ฉนวน) ย้ายเข้าจาน 55% ต่อการแตะ · มุมกาง tanθ sin²θ = (V/3000)² (แรงผลักกับน้ำหนัก)
- โหมดวัดเอง: ไม่แสดงประจุ/ตัวเลข อ่าน d จากแว่นขยายไม้บรรทัด, θ จากแว่นขยายสเกลมุม · โหมดอัตโนมัติ: เครื่องหมาย +/− บนจาน แผ่นโลหะ แท่ง + อนุภาค e⁻ ไหลผ่านนิ้ว/จุดสัมผัส · ค่า q, Q, Q_จาน/Q_แผ่น, V · คำอธิบายสถานะ
- ตาราง A (d, θ) + กราฟ θ–d (โหมดอัตโนมัติมีเส้นแบบจำลอง) · ตาราง B ทดสอบชนิดประจุ (เลือกประจุอิเล็กโทรสโคป/ผล/สรุป → เฉลย ✓✗) · CSV · ↺ รีเซต (คายประจุทั้งหมด ยกนิ้ว แท่ง 30 cm ไม่ลบตาราง ไม่เปลี่ยนแท่งปริศนา)
- แท็บวิธีทดลอง: ตอน A ขัดสี+เหนี่ยวนำ θ–d · B สัมผัส · C เหนี่ยวนำ+ต่อดิน (และลำดับผิด) · D แท่งปริศนา · คำถาม 5 ข้อ · แท็บทฤษฎี: triboelectric series · ตัวนำ/ฉนวน · ภาพ 4 ขั้นการเหนี่ยวนำ · 3 ขั้นการสัมผัส · ตารางทดสอบชนิดประจุ · แบบจำลองที่ใช้
- **ตรวจ**: ถู 5 ครั้ง q = −5.85 nC · เหนี่ยวนำ (ใกล้→ดิน→ยกนิ้ว→ถอย) Q = +5.48 nC θ 16.8° (ตรงข้ามแท่ง) · สัมผัส Q = −3.21 nC (ชนิดเดียวกับแท่ง) · อิเล็กโทรสโคป − + แท่งแก้วเข้าใกล้: θ ลด 11.5° → 3.4° แล้วกลับกางที่ d ≤ 3 cm (ประจุกลับชนิด) · แท่ง PVC เข้าใกล้: กางเพิ่ม · θ–d (q −5.85, ไม่มีประจุ): 40:0.7° 30:2.4° 20:4.6° 10:8.7° 5:13.3° 1:23.1° · มุมมองมองตรง: มุมแผ่นโลหะบนจอ = มุมขีดสเกลบนการ์ด = θ (23.72°) · ลากแท่ง 3D (30 → 10 cm) มุมมองไม่หมุนตาม · แตะจานสลับนิ้ว · แท่งปริศนาซ่อน q/Q/V/เครื่องหมายในโหมดอัตโนมัติจนบันทึกตาราง B · ไม่มี console error
- ลงทะเบียน: lab-54 ใน `VLAB_SERIES` (kp-auth.js + admin.html) + `LAB_LIST` · labs_data.py เพิ่มบทเรียน `electro` (🎈 ไฟฟ้าสถิต) + กลุ่ม `elec` (🔌 ไฟฟ้าและแม่เหล็ก) + entry → build (55) · protect · การ์ด + preview `vpl2-electroscope`: virtual-physics-lab-02.html (หมวดใหม่ "ไฟฟ้าสถิต" ก่อนไมโครเวฟ, hero 28) · index.html (chip 🎈 ไฟฟ้าสถิต 1, ทั้งหมด 28, "จากทั้งหมด 55", "ดูทั้งหมด 55")

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/54. electroscope-charging-induction.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit
- ถัดไป Lab 55 กฎของคูลอมบ์ → 56 → … → 60 ตามแผน
- หมายเหตุ: hero ของ virtual-physics-lab-02.html ยังชื่อ "คลื่น แสง และเสียง" ทั้งที่มีหมวดไฟฟ้าแล้ว

## [2026-09-14 20:40] — NEW Lab 55 (VPL02) กฎของคูลอมบ์ด้วยเครื่องชั่ง (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/55. coulombs-law-balance.html` (3D): ทรงกลมโลหะ A (a = 2 cm) บนแท่งอะคริลิกบนเครื่องชั่งดิจิทัล 0.0001 g (มี TARE · ค่าอ่านแกว่ง ±0.0002 g ในโหมดวัดเอง · ยังไม่ TARE อ่านรวมมวล 18.7426 g) · ทรงกลม B ยึดแขนเลื่อนบนเสาตั้ง สเกลอ่าน r (ศูนย์กลาง–ศูนย์กลาง) ที่ขีดชี้ 4.5–35 cm · แหล่งจ่ายไฟแรงสูง 1–10 kV ขั้ว ± · หัวแตะ (q = 4πε₀aV) · ทรงกลมเปล่าขนาดเท่ากัน (แบ่งครึ่ง) · สายดิน — เครื่องมือเคลื่อนไปแตะทรงกลมจริงใน 3D พร้อมสาย
- **แรง**: ประมาณประจุภาพลำดับแรกของทรงกลมตัวนำ F = kq_Aq_B/r² − k(q_A²+q_B²)a³(2r²−a²)/[r³(r²−a²)²] → ระยะใกล้แรงผลักน้อยกว่ากฎคูลอมบ์ (r 10 cm −3.4%, 5 cm −33%) · ประจุลูกเดียวมีแรงดูดเหนี่ยวนำเล็กน้อย · ผลักกดเครื่องชั่ง (ค่าบวก) ดูดยกขึ้น (ค่าติดลบ)
- ลากทรงกลม B/แขนใน 3D และ 2D · มุมมอง มุมเฉียง / ทรงกลม (ตาม r) / สเกลระยะ (ตามแขน) / จอเครื่องชั่ง · แตะปุ่ม TARE บนเครื่องชั่ง 3D ได้
- แผนภาพ 2D: อุปกรณ์ (ลาก B) · แว่นขยายสเกล ±2 cm ขีด mm · จอเครื่องชั่ง · จอแหล่งจ่าย · สถานะประจุตามขั้นตอน (q(V)/2ⁿ) · โหมดอัตโนมัติ: เครื่องหมายประจุ ลูกศรแรง r
- ตาราง A (เปลี่ยน r) / B (เปลี่ยน q) : r, ค่าอ่าน, F = Δm g, q_A·q_B (ตามขั้นตอน), Fr²/q_Aq_B → k เฉลี่ย (r ≥ 10 cm) · กราฟ F–1/r² (เส้นตรงผ่านจุดกำเนิดจากจุด r ≥ 10 cm, จุด r < 10 สีส้ม), F–r, F–q_Aq_B (ความชัน → k) · โหมดอัตโนมัติวาดเส้นจุดประจุ (ประ) และทรงกลมตัวนำ
- แท็บวิธีทดลอง (ตอน A/B, สูตร, คำถาม 5 ข้อ) + ทฤษฎี (กฎคูลอมบ์ · วัดแรงด้วยเครื่องชั่ง · แบ่งประจุ · ทำไมระยะใกล้คลาด พร้อมกราฟ F/F_คูลอมบ์–r/a และตาราง)
- **ตรวจ**: 6 kV → q = 13.35 nC · r 15 cm ค่าอ่าน 0.0072 g (kq²/r² = 7.1×10⁻⁵ N ✓) · k จากตาราง A: r 30→8.977, 20→8.952, 10→(3.4% ต่ำ), 6→7.40, 5→5.99 × 10⁹ · ความชัน F–1/r² (r ≥ 10) 1.572×10⁻⁶ N·m² (kq² = 1.602×10⁻⁶) · ขีดชี้ 3D ตรง 12.3 cm กับแว่นขยาย 2D · ไม่มี console error
- ลงทะเบียน lab-55 (kp-auth.js, admin.html VLAB_SERIES + LAB_LIST) · labs_data.py → build (56) · protect · การ์ด + preview `vpl2-coulomb` ใน virtual-physics-lab-02.html (ไฟฟ้าสถิต 2, hero 29) และ index.html (ไฟฟ้าสถิต 2, ทั้งหมด 29, 56)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/55. coulombs-law-balance.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–55)
- ถัดไป Lab 56 สนามไฟฟ้าและเส้นสนาม

## [2026-09-14 20:55] — NEW Lab 56 (VPL02) สนามไฟฟ้า: เส้นสนามในน้ำมัน และแผ่นขนาน (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/56. electric-field-lines-plates.html` (3D) มี 2 ตอน (สลับฉาก 3D/แผงควบคุม/แผนภาพ)
- **ตอน A เส้นสนามในน้ำมัน**: จานแก้วน้ำมัน + ผงเซโมลินา 3,000 เม็ด (InstancedMesh) · ขั้วไฟฟ้า 6 แบบ: จุด+วงแหวนรอบนอก · จุดคู่ต่างชนิด · จุดคู่ชนิดเดียวกัน (+วงแหวน) · แถบขนาน · แถบขนาน+วงแหวนลอยตัว · จุด+แถบ · **สนามคำนวณจากตัวนำจริง (2 มิติ)**: แทนผิวขั้วด้วยประจุเส้น แก้ระบบเชิงเส้นให้ขั้วมีศักย์ ±V/2 และวงแหวนลอยตัวมีประจุสุทธิ 0 · ผงหมุนเข้าหาทิศสนามด้วยอัตรา ∝ E² (สนามอ่อนผงยังกระจัดกระจาย) · ปุ่มคนผงใหม่
- ทำนาย→สังเกต: แผนภาพ 2D ด้านขวามีภาพลวดลายเส้นสนาม 6 ภาพ (ไม่แสดงขั้ว สุ่มลำดับ) ให้เลือก → ตาราง A เฉลย ✓✗ หลังบันทึก · โหมดอัตโนมัติ: เส้นสนาม + ลูกศร + หัววัด |E| (แตะ/ลากในจาน)
- **ตอน B แผ่นขนาน**: แผ่นซ้าย +V แผ่นขวาต่อดิน (ลาก/สไลเดอร์ d 6–16 cm) · ลูกบอลโฟมเคลือบโลหะ m 0.100 g a 0.75 cm แขวน L 25 cm · ให้ประจุ ±2 kV (q = 4πε₀aV = 1.67 nC ต้องปิดไฟก่อน) · ลูกตุ้มจำลองพลวัต (หน่วง) + แรงประจุภาพจากทั้งสองแผ่น · แตะแผ่นแล้วได้ประจุ (2π³/3)ε₀a²E ชนิดเดียวกับแผ่น · แหล่งจ่ายค่อย ๆ เพิ่มแรงดัน (τ 0.4 s) · ไม้บรรทัดใสหลังลูกบอล + สเกลบนฐาน (แว่นขยาย 2 ช่อง) · ตาราง B (V, d, x → V/d, tan θ) + กราฟ tan θ–V/d → ความชัน = q/mg → q
- แท็บวิธีทดลอง + ทฤษฎี (ภาพเส้นสนาม 6 แบบจากตัวแก้เดียวกัน · โพลาไรเซชันของผง · กรงฟาราเดย์ · แผนภาพแรงบนลูกบอล)
- **ตรวจ**: วงแหวนลอยตัว E ภายใน ≤ 4.3 V/cm เทียบภายนอก 480 V/cm (4 kV) · ผงนอกวงแหวนเรียงตัว |cos 2Δ| = 1.00 ภายใน 0.62 (สุ่ม) · ตอน B: 2 kV/10 cm x = 0.899 cm tan θ 0.0360 (qE/mg 0.0340 ต่างเพราะแรงประจุภาพ +5.8%) · 4/14 tan 0.0496 (0.0486) · 6 kV/8 cm สมดุล tan 0.128 ใกล้แผ่น → ลูกบอลแตะแผ่น ประจุกลายเป็น −0.65 nC (สมจริง) · แก้บั๊ก Texture.userData ไม่มีใน r128 (loop 3D หยุด) · ไม่มี console error
- ลงทะเบียน lab-56 · build (57) · protect · การ์ด + preview `vpl2-efield` (ไฟฟ้าสถิต 3, hero 30, index ทั้งหมด 30 / 57)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/56. electric-field-lines-plates.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–56)
- ถัดไป Lab 57 เส้นศักย์เท่ากันบนกระดาษนำไฟฟ้า

## [2026-09-14 21:05] — NEW Lab 57 (VPL02) เส้นศักย์เท่ากันบนกระดาษนำไฟฟ้า (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/57. equipotential-mapping.html` (3D): แผ่นไม้ก๊อก + กระดาษคาร์บอน 30 × 20 cm มีตาราง 1 cm/0.5 cm และตัวเลขพิกัด · ขั้วเงิน 6 แบบ: จุดสองจุด · แท่งขนาน · จุดกับวงแหวน · แท่งกับจุด · แท่งขนาน + วงแหวนลอยตัว · แท่งขนาน + รอยตัด (ฉนวน) · แหล่งจ่ายไฟตรง 2–12 V · โวลต์มิเตอร์ (COM ที่ขั้วลบ) + ปากกาหัววัดลากบนกระดาษ (3D/2D) ลูกศร/แป้นลูกศรทีละ 1 mm/1 cm
- **ศักย์**: แก้สมการลาปลาซบนกริด 0.25 cm (121 × 81) ด้วย SOR (~40 ms) · ขอบกระดาษและรอยตัดเป็นฉนวน (Neumann) · วงแหวนลอยตัว = ค่าเฉลี่ยเพื่อนบ้าน (กระแสสุทธิ 0) · อ่านค่าแบบ bilinear
- ทำเครื่องหมาย 📍 (ปุ่ม/แป้น M) ตามศักย์ที่เลือก (สีต่างกัน) · เชื่อมจุดสีเดียวกัน (เรียงตามมุมถ้าเป็นวงปิด ไม่งั้นเรียงจุดใกล้สุด) · ↶ ลบจุดล่าสุด · ✔ ตรวจความแม่น (ความคลาดเฉลี่ย ไม่แสดงเส้นจริง) · โหมดอัตโนมัติวาดเส้นศักย์ทุก 1 V (marching squares) + เส้นสนาม (ประ) บนกระดาษ + ลูกศร E ที่หัววัด
- แผนภาพ 2D: กระดาษ (texture เดียวกับ 3D) + มิเตอร์ + คำแนะนำ "ศักย์สูงไป/ต่ำไป" + แว่นขยายตารางรอบหัววัด ±1.5 cm (โหมดวัดเองไม่แสดงพิกัด)
- ตาราง V ตามแนว y = 0 + กราฟ V–x (เส้นตรงช่วง |x| ≤ 5 cm → E = −ΔV/Δx) · แท็บวิธีทดลอง + ทฤษฎี (ภาพเส้นศักย์/เส้นสนาม 6 แบบจากตัวแก้เดียวกัน · กราฟ V–x แท่งขนานเทียบจุดสองจุด)
- **ตรวจ**: แท่งขนาน 10 V: V(−5, 0, 5) = 9.34/5.00/0.66 · ความชัน −0.867 V/cm → E = 87 V/m (10 V / 11.4 cm ระหว่างขอบใน = 87.7) · วงแหวนลอยตัวภายใน 5.001 V ทุกจุด · จุดกับวงแหวน สมมาตรตาม ln r · จุดที่หาได้จริงบนเส้น 4 V ตรวจได้คลาด 0.000 V และจุดที่ 5 V ตรวจเป็นคลาด 1.001 V · เส้นศักย์ตั้งฉากขอบกระดาษ · ไม่มี console error
- ลงทะเบียน lab-57 · build (58) · protect · การ์ด + preview `vpl2-equipot` (ไฟฟ้าสถิต 4, hero 31, index 31/58)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/57. equipotential-mapping.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–57)
- ถัดไป Lab 58 ตัวเก็บประจุแผ่นขนาน

## [2026-09-14 21:15] — NEW Lab 58 (VPL02) ตัวเก็บประจุแผ่นขนาน (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/58. parallel-plate-capacitor.html` (3D): แผ่นอะลูมิเนียมวงกลม (R 8.0 / 12.5 cm) บนขาฉนวน แผ่นขวาเลื่อนบนรางมีสเกล mm (ลากใน 3D, d 1–20 mm) · แหล่งจ่าย 0–100 V · สวิตช์ 3 ตำแหน่ง ① อัดประจุ ② แยกวงจร ③ คายประจุผ่านคูลอมบ์มิเตอร์ (นับประจุสะสม มีปุ่มตั้งศูนย์) · อิเล็กโทรมิเตอร์ต่อ/ไม่ต่อ (15 pF) · แผ่นฉนวนหนา 3.0 mm: อะคริลิก κ 2.8 · แก้ว κ 6.2 · ปริศนา (สุ่ม κ 2–8 ซ่อนจนบันทึกผลที่ใช้แผ่นนี้) — แผ่นเลื่อนลงมาระหว่างแผ่น
- **แบบจำลอง**: C_แผ่น = ε₀πR²/d_eff + ε₀R[ln(16πR/d) − 1] (เคิร์ชฮอฟฟ์ รวมผลขอบ) · d_eff = d − t + t/κ · ความจุแฝงสาย 12 pF · Q ของโหนดคงที่เมื่อแยกวงจร → V = Q/C_รวม
- แผนภาพวงจร 2D (แตะขั้วสวิตช์ได้ · โหมดอัตโนมัติแสดงประจุ ± และเส้นสนามระหว่างแผ่น) + แว่นขยายสเกลราง 0.5 mm
- ตาราง A (R, ฉนวน, d, V, Q → C = Q/V) + กราฟ C–1/d แยกตาม R (เส้นตรง → ความชัน/A = ε₀ + จุดตัด = ความจุแฝง) · ตาราง B (Q คงที่: d, V) + กราฟ V–d · โหมดอัตโนมัติ: C, C_รวม, Q, V, E, U, κ + เส้นประแบบจำลอง
- แท็บวิธีทดลอง (ตอน A หา ε₀ · ตอน B ประจุคงที่ + ฉนวน · สูตร · คำถาม) + ทฤษฎี (ภาพสนาม/ประจุ/สนามล้นขอบ · ฉนวน + ตาราง κ · กราฟ Q, V, U เมื่อ Q คงที่ vs V คงที่ · แบบจำลอง)
- **ตรวจ**: 50 V, R 12.5 cm, d = 2…20 mm → กราฟ C–1/d ความชัน 0.440 pF·m → ε₀ = 8.96 pF/m (จริง 8.854 · ต่างเพราะผลขอบ) จุดตัด 32.4 pF (สาย 12 + มิเตอร์ 15 + ขอบ) · C_แผ่น 2 mm = 225 pF (ε₀A/d = 217) · แยกวงจรที่ 3 mm 50 V → d 4/6/10/15 mm: 62.8/84.5/117.2/145.6 V · สอดอะคริลิก V ลดเป็น 20.4 V (อัตราส่วน 2.45 < κ เพราะความจุแฝง — เขียนในวิธีทดลองให้หักความจุแฝง) · แก้ว 9.6 V · จัดวงจร 2D ใหม่ไม่ให้ทับแว่นขยาย · ไม่มี console error
- ลงทะเบียน lab-58 · build (59) · protect · การ์ด + preview `vpl2-capacitor` (ไฟฟ้าสถิต 5, hero 32, index 32/59)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/58. parallel-plate-capacitor.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–58)
- ถัดไป Lab 59 การอัด-คายประจุ RC · Lab 60 หยดน้ำมันมิลลิแกน

## [2026-09-14 21:25] — NEW Lab 59 (VPL02) การอัดและคายประจุตัวเก็บประจุ RC (3D) · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/59. rc-charge-discharge.html` (3D): แผ่นไม้ต่อวงจร · แบตเตอรี่ AA 4 ก้อน 6.0 V · สวิตช์ 2 ทาง (A อัด / กลาง / B คาย — คลิกคันโยกใน 3D หรือขั้วในแผนภาพ) · ไมโครแอมมิเตอร์อนุกรม · ตัวต้านทาน 10k/22k/47k/100k (แถบสีถูกต้อง ค่าจริงสุ่ม ±5%) · ตัวเก็บประจุอิเล็กโทรไลต์ 470/1000/2200 μF (ฉลากบนตัว ค่าจริง ±20%) + ตัวปริศนา X (300–3000 μF) · โวลต์มิเตอร์ 10 MΩ คร่อม C · นาฬิกาจับเวลา (เริ่มอัตโนมัติเมื่อสับสวิตช์) · เปลี่ยนอุปกรณ์ได้เมื่อคายประจุหมด
- **แบบจำลอง**: เอกซ์โพเนนเชียลแม่นตรงทุกขั้นเวลา · อัด V∞ = 6·R_V/(R+R_V), τ = C(R∥R_V) · คาย τ = C(R∥R_V) · สวิตช์กลางคายผ่านมิเตอร์ τ = R_V C · ความเร็วเวลา ×1/×2/×5
- 📝 จดค่า (ปุ่ม/Space) หรือบันทึกอัตโนมัติทุก 5/10 s · แยกชุดข้อมูล (อัด/คาย/อุปกรณ์) เลื่อนดูชุดก่อน-ถัดไป · ตาราง t, V, I, ln V หรือ ln(V₀−V) · กราฟ V–t, ln–t (ความชัน → τ → C = τ/R ระบุ), I–t · 🎯 ส่งคำตอบ C → เฉลยค่าจริง + %คลาด + ค่าจริงของ R
- แผนภาพวงจร 2D + จอเครื่องวัด + (อัตโนมัติ) สโคป V_C และลูกศรกระแส/ประจุ · แท็บวิธีทดลอง (ตอน A คาย · B อัด · C ตัวปริศนา · คำถาม) + ทฤษฎี (สมการ · กราฟ τ · ตาราง e^(−n) · พลังงาน)
- **ตรวจ**: R 47k (จริง 48.24 k) C 1000 μF (จริง 922) → τ จริง 44.28 s · คายประจุจดทุก 10 s ความชัน ln V–t → τ 44.3 s → C = 943 μF (ใช้ R ระบุ) · อัดประจุ ln(V₀−V) → τ 44.2 s · แรงดันเต็ม 5.964 V (ผลโหลดของมิเตอร์) · ไม่มี console error
- ลงทะเบียน lab-59 · build (60) · protect · การ์ด + preview `vpl2-rc` (ไฟฟ้าสถิต 6, hero 33, index 33/60)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/59. rc-charge-discharge.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–59)
- ถัดไป Lab 60 หยดน้ำมันมิลลิแกน (ชุดสุดท้ายของแผน)

## [2026-09-14 21:35] — NEW Lab 60 (VPL02) การทดลองหยดน้ำมันของมิลลิแกน (3D) · สรุปชุดไฟฟ้าสถิต · Opus 5

### ทำอะไรไปบ้าง
- สร้าง `Virtual Physics Lab 02/60. millikan-oil-drop.html` (3D): ฐาน + แผ่นทองเหลืองขนาน d = 6.00 mm (ผนังอะคริลิกใส รูบนแผ่นบน) · ที่พ่นละออง (ลูกยางบีบ + ละออง) · หลอดไฟส่องข้าง + ลำแสง · กล้องจุลทรรศน์ · แหล่งจ่าย 0–600 V (สลับขั้ว + สวิตช์ลัดวงจรแผ่น) · แหล่งรังสีไอออไนซ์ · จุดแสงของหยดในช่องว่าง (ขยาย)
- **ภาพกล้องจุลทรรศน์ (2D)**: สเกลในเลนส์ตาขีด 0.05/0.25 mm · หยดเป็นจุดแสงกระเจิง · แตะเลือกหยด (วงแหวนเหลือง) หยดอื่นค่อย ๆ หลุดโฟกัส · ภาพข้างแผ่นขนาน + ช่องมอง + ทิศสนาม · จอแรงดันและนาฬิกา
- **ฟิสิกส์**: ความเร็ว = (qE − mΔρg)/(6πη_eff r) · η_eff = η/(1 + b/pr) (คันนิงแฮม) · การเคลื่อนที่แบบบราวน์ D = kT/(6πη_eff r) · หยดสุ่ม r 0.38–0.88 μm ประจุส่วนใหญ่ลบ 1–6 e · ฉายรังสีเปลี่ยนประจุ ±1–2 e · หยดชนแผ่นหายไป · ความเร็วเวลา ×1/×2/×4 · Space = เริ่ม/หยุดนาฬิกา · R = ศูนย์
- ตารางคำนวณ r (แก้คันนิงแฮมแบบวนซ้ำ), m, q = mgd/V จาก s, t, V ที่นักเรียนกรอก (ปุ่มดึงเวลา/แรงดันปัจจุบัน) · กราฟ strip plot ของ q + ตัวเลื่อน "ลองค่า e" เส้นประจำนวนเต็มเท่า · RMS ความห่างจากจำนวนเต็ม · e = Σq/Σn · โหมดอัตโนมัติแสดง r, q = ne, ความเร็วปลาย, แรงดันลอยนิ่ง และเลข n บนหยด
- แท็บวิธีทดลอง + ทฤษฎี (แผนภาพแรง ตก/ลอยนิ่ง · สโตกส์ · ตารางผลคันนิงแฮม · การควอนไทซ์ของประจุ)
- **ตรวจ**: หยด n = −4, r = 0.721 μm → t ตก 0.50 mm = 8.22 s, V ลอยนิ่ง 125.9 V → ตารางคำนวณกลับได้ q = 4.0000 e, r = 0.721 μm · จับเวลาจำลองพร้อมบราวน์ 5 ครั้ง 8.00–8.54 s (±3%) · ตั้ง 126 V หยดเลื่อน −0.003 mm ใน 10 s · ไม่มี console error
- ลงทะเบียน lab-60 (level ม.6) · build (61) · protect · การ์ด + preview `vpl2-millikan` (ไฟฟ้าสถิต 7, hero 34, index 34/61)
- ตรวจหน้า virtual-physics-lab-02.html ผ่าน http://localhost:8765: หมวด "ไฟฟ้าสถิต" 7 การ์ด preview ทำงานครบ · ย้ายจอโวลต์ใน preview RC ไม่ให้ทับป้าย FREE · สคริปต์ใน index.html และ virtual-physics-lab-02.html parse ผ่านทั้งหมด
- แก้เวลาในหัวข้อ log ของ Lab 54–59 ให้ตรงเวลาจริงของไฟล์

### สรุปชุดไฟฟ้าสถิต (Lab 54–60) ตามแผนที่ผู้ใช้สั่ง "เรียงลำดับเลย"
- 54 อิเล็กโทรสโคป/การเหนี่ยวนำ · 55 กฎของคูลอมบ์ (เครื่องชั่ง) · 56 เส้นสนามในน้ำมัน + แผ่นขนาน · 57 เส้นศักย์เท่ากัน · 58 ตัวเก็บประจุแผ่นขนาน (ε₀, κ) · 59 อัด-คายประจุ RC · 60 หยดน้ำมันมิลลิแกน
- บทเรียนใหม่ `electro` (🎈 ไฟฟ้าสถิต) + กลุ่ม `elec` (🔌 ไฟฟ้าและแม่เหล็ก) ใน labs_data.py · สคริปต์ลงทะเบียนชั่วคราวอยู่ใน scratchpad (ไม่ได้เก็บในโปรเจกต์)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/60. millikan-oil-drop.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **ยังไม่ commit** Lab 54–60 ทั้งหมด (รอผู้ใช้ตรวจ/อนุมัติ)
- ผู้ใช้ยังไม่ได้ลองใช้จริงบน iPad — อาจมี feedback ด้าน UI/ความถูกต้องตามเคย
- hero ของ virtual-physics-lab-02.html ยังชื่อ "คลื่น แสง และเสียง" ทั้งที่มีหมวดไฟฟ้าสถิตแล้ว (ควรถามผู้ใช้ว่าจะเปลี่ยนชื่อหรือแยกเป็น VPL ใหม่)
- ต่อยอดได้: การต่อตัวเก็บประจุอนุกรม/ขนาน · แวนเดอกราฟ/ถังน้ำแข็งฟาราเดย์ · เครื่องชั่งแบบบิดของคูลอมบ์

## [2026-09-14 21:41] — ปุ่มรีเซตสีเขียวบนภาพ 3D (Lab 54–60) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้หาปุ่มรีเซตไม่เจอ (บน iPad แนวตั้ง แผงควบคุมอยู่ใต้ภาพ 3D + แผนภาพ ต้องเลื่อนลง ~1150 px) → ขอ "ปุ่มสีเขียวให้เห็นชัดเจนอยู่ที่ canvas"
- เพิ่มปุ่ม **↺ รีเซตค่า** สีเขียว (class `reset3d`) ท้ายแถวปุ่มมุมมองมุมล่างซ้ายของภาพ 3D ทั้ง 7 แลป · เรียก `resetLab()` เดิม · ปุ่มเดิมในแผงควบคุมยังอยู่ · Lab 56 ใส่ในแถวปุ่มที่สร้างใหม่ตามตอน A/B
- **ตรวจ**: คลิกปุ่มเขียวแล้วค่ากลับค่าเริ่มต้นทุกแลป (54 d 30 cm ประจุ 0 · 55 r 15 · 56 ตอน B d 10 q 0 · 57 หัววัด (−3, 4) · 58 d 4 mm · 59 V_C 0 สวิตช์กลาง · 60 0 V ละอองหมด) · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/54–60 *.html` — CSS + ปุ่ม reset3d

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–60 + ปุ่มนี้)
- แลปเก่า (46–53 และอื่น ๆ) ยังไม่มีปุ่มเขียวบน canvas — ถามผู้ใช้ว่าจะใส่ด้วยไหม

## [2026-09-14 21:57] — NEW Lab 61 (VPL02) การต่อตัวเก็บประจุแบบอนุกรม ขนาน และผสม (3D) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ขอ "แลปการต่อตัวเก็บประจุแบบต่าง ๆ" → สร้าง `Virtual Physics Lab 02/61. capacitor-combinations.html` (3D, ใช้ head/CSS/auth จาก Lab 59)
- แผ่นต่อวงจร 3D: แหล่งจ่าย 1–12 V · สวิตช์ ① อัดประจุ ② แยกวงจร ③ คายประจุ (ลัด A–B) · ขั้ว A/B · ตัวเก็บประจุฟิล์มสีน้ำเงินมีฉลากค่า (1.0/2.2/3.3/4.7/10 μF ค่าจริงสุ่ม ±5% ต่อช่อง) · โวลต์มิเตอร์ (สายวัดแดง/ดำย้ายไปคร่อมตัวที่แตะใน 3D/2D) · มิเตอร์วัดความจุ
- **8 รูปแบบ**: 1 ตัว · อนุกรม 2 · ขนาน 2 · อนุกรม 3 · ขนาน 3 · C₁ อนุกรม (C₂∥C₃) · (C₁ อนุกรม C₂) ∥ C₃ · แบ่งประจุ (สวิตช์ S₂ แตะได้)
- **ตัวแก้วงจร**: ศักย์โหนด · โหนดที่ต่อแหล่งจ่าย/ลัดวงจรมีศักย์คงที่ · โหนดโดดเดี่ยวรักษาประจุสุทธิ (อนุรักษ์ประจุ) · C_AB = ประจุที่ A เมื่อ 1 V · วัดความจุต้องแยกวงจรและไม่มีประจุ (ไม่งั้น Err) · "ถอดวัด" ทีละตัว · เปลี่ยนรูปแบบ/ค่า → คายประจุอัตโนมัติ
- แผนภาพวงจร 2D (ป้ายชื่อมีพื้นหลัง ไม่ทับกัน) + จอเครื่องวัด · อัตโนมัติ: V, Q บนแต่ละตัว + ตาราง C/V/Q/U + ข้อสรุป
- ตาราง A (C ที่วัดทีละตัว, C_AB วัด vs สูตร, %ต่าง) · ตาราง B (V_AB, V₁–V₃ → Q = CV, U รวม) · CSV · ปุ่มเขียว ↺ รีเซตค่าบนภาพ 3D
- แท็บวิธีทดลอง (ตอน A ความจุสมมูล · B แรงดัน/ประจุ · C แบ่งประจุ · คำถาม) + ทฤษฎี (ภาพอนุกรม/ขนาน · ผสม · พลังงานที่หายไป)
- **ตรวจ** (9.0 V): อนุกรม 2 (2.2, 4.7) C_AB = สูตร 1.4953 μF · V 6.018/2.982 · Q เท่ากัน 13.46 μC · ขนาน 3 C = 8.1374 · อนุกรม 3 Q เท่ากันทุกตัว 5.57 μC · ผสม 1: Q₁ 15.81 = Q₂ 6.35 + Q₃ 9.46 · ผสม 2 ตรงสูตร · แบ่งประจุ (4.7→2.2): V 6.170 = C₁V₀/(C₁+C₂) · U หลัง/ก่อน 0.6856 = C₁/(C₁+C₂) · ลัดวงจรแล้วไม่มีประจุค้าง · ไม่มี console error
- ลงทะเบียน lab-61 · build (62) · protect · การ์ด + preview `vpl2-capcombo` (ไฟฟ้าสถิต 8, hero 35, index 35/62)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/61. capacitor-combinations.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–61 + ปุ่มรีเซตเขียว)

## [2026-09-14 22:13] — Lab 61 ปรับให้ใช้ง่าย: ขั้นตอนนำทาง + ปุ่มจดค่า · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "แลป 61 ไม่เข้าใจว่าต้องทำอะไร ดูยากจัง" → เพิ่มกรอบสีเขียว **🧭 ทำตามขั้นตอนนี้** บนสุดของคอลัมน์การทดลอง (เหนือภาพ 3D ไม่ทับภาพ): แท็บ A หาความจุรวม / B แรงดันและประจุ / C แบ่งประจุ · แสดงขั้นปัจจุบันตัวใหญ่ + ปุ่ม 👉 ทำขั้นนั้นให้ + แถบขั้นทั้งหมด (✓ อัตโนมัติจากสถานะจริง) · ปุ่ม/ส่วนที่ต้องใช้กระพริบขอบเหลือง · ข้อความยืนยันหลังจดค่า
- เอาฟอร์มกรอกตัวเลข 10 ช่องและปุ่มบันทึกตาราง A/B ออก → ใช้ **📝 จดค่าแรงดัน / 📝 จดค่าความจุ** ใต้เครื่องวัด เขียนค่าบนจอลงช่องที่ตรงกันเอง (ตรวจเงื่อนไข เช่น ตาราง B ต้องอัดประจุก่อน)
- ตาราง A/B/C สร้างจากค่าที่จด แยกแถวตามรูปแบบ (แถวรูปแบบปัจจุบันไฮไลต์) · A: C ที่วัด, C_AB วัด vs สูตร, %ต่าง · B: V_AB, V₁–V₃, Q = CV, ΣV · C: C₁, C₂, V₀, V หลัง, ทำนาย C₁V₀/(C₁+C₂), U หลัง/ก่อน · ล้างรูปแบบนี้/ล้างทั้งหมด · CSV · เปลี่ยนค่าตัวเก็บประจุแล้วล้างค่าที่จดของรูปแบบนั้น
- เลือกแบ่งประจุ ↔ แท็บ C สลับกันอัตโนมัติ · แก้ข้อความแท็บวิธีทดลองให้ตรงกับการจดค่า
- **ตรวจ**: เดินขั้นตอนด้วยปุ่ม 👉 + จดค่า ครบทั้ง 3 ตอน: อนุกรม 2 C 2.09/4.58 → C_AB 1.44 (สูตร 1.44, 0.3%) · ขนาน 2 → 6.67 (0.0%) · ตอน B V 6.18 + 2.82 = 9.00, Q 12.9 = 12.9 μC · ตอน C V₀ 9.00 → 2.82 (ทำนาย 2.82), U หลัง/ก่อน 0.313 · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/61. capacitor-combinations.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–61)
- ถ้าผู้ใช้ชอบกรอบขั้นตอนนำทาง อาจเพิ่มให้ Lab 54–60 ด้วย

## [2026-09-14 22:16] — Lab 61 อธิบายการหาประจุ (Q = C × V) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "ตรงวัดประจุไม่แน่ใจว่าวัดยังไง" → แลปนี้ไม่มีเครื่องวัดประจุโดยตรง ประจุคำนวณจาก Q = C × V แต่เดิมไม่ได้บอกชัด
- ตาราง B: หัวคอลัมน์ "Q = C × V (μC)" + กล่อง **🧮 วิธีหาประจุ** ใต้ตาราง แสดงการคูณทีละตัวของรูปแบบปัจจุบัน เช่น Q₁ = 2.16 μF × 6.10 V = 13.2 μC · ถ้ายังไม่มี C หรือ V บอกว่าต้องวัดอะไรก่อน
- ขั้นตอนนำทางตอน B: เพิ่มขั้นอธิบาย "ประจุวัดตรง ๆ ไม่ได้ ต้องคำนวณจาก Q = C × V" → สวิตช์ ② → วัด C ทีละตัว (ข้ามได้ถ้าทำตอน A แล้ว) → ① อัดประจุ → จด V_AB, V₁, V₂ → ดูตาราง B + กล่องวิธีหาประจุ
- ตาราง/กล่องอัปเดตเมื่อเปลี่ยนรูปแบบหรือค่าตัวเก็บประจุ
- **ตรวจ**: เดินตอน B ด้วยปุ่ม 👉 ครบ 9 ขั้น: อนุกรม 2 C 2.16/4.54 μF · V 6.10 + 2.90 = 9.00 V · Q₁ = Q₂ = 13.2 μC · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/61. capacitor-combinations.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–61)
- ถ้าผู้ใช้อยากวัดประจุโดยตรง: เพิ่มคูลอมบ์มิเตอร์ (ถอดตัวเก็บประจุออกมาคายผ่านมิเตอร์) แบบ Lab 58

## [2026-09-14 22:20] — Lab 61 เครื่องวัดใน 3D ต่อสายวัดให้เห็นจริง · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "มิเตอร์ใน canvas ไม่เห็นมีการวัดเลย" (เดิมจอนอนราบอ่านยาก สายวัดเป็นเส้นบาง มิเตอร์วัดความจุไม่มีสาย)
- เครื่องวัดใหม่: ตัวเครื่องมีหน้าจอเอียงหันเข้าหาผู้ใช้ + ขั้วเสียบแดง/ดำ · ป้ายชื่อเหนือเครื่อง
- โวลต์มิเตอร์: สายวัดเป็นท่อหนาแดง/ดำจากขั้วเครื่องไปหัววัด (ด้ามจับ + ปลายโลหะ) แตะขาทั้งสองของตัวเก็บประจุที่เลือก หรือขั้ว A/B · ตัวที่วัดมีกรอบเขียวกระพริบ
- มิเตอร์วัดความจุ: วัด C_AB → สายพร้อมคลิปเหลืองหนีบขั้ว A และ B · ถอดวัด C₁/C₂/C₃ → ตัวในวงจรจางลง (กรอบฟ้า) และมีตัวเก็บประจุวางบน "ช่องเสียบวัด C" ข้างมิเตอร์พร้อมสาย · เปลี่ยนสวิตช์แล้วการวัดความจุหายไป (ตามจริง)
- สร้างสายวัดใหม่เฉพาะเมื่อเปลี่ยนจุดวัด (ไม่สร้างทุกเฟรม) · ขยายบอร์ด · มุมเฉียงเห็นทั้งวงจรและเครื่องวัด · มุม 📟 เครื่องวัดเห็นจอเอียง
- **ตรวจ**: ถอดวัด C₁ → จอ 2.26 μF + ตัวเก็บประจุบนช่องเสียบ · C_AB → คลิปที่ A/B จอ 1.48 μF · ① อัดประจุ + คร่อม C₂ → หัววัดแตะขา C₂ จอ 2.85 V · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/61. capacitor-combinations.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–61)

## [2026-09-14 22:25] — เมนูทางลัดหน้าแรก "🚀 ไปที่ต้องการทันที" ให้ครบและอัปเดตอัตโนมัติ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ส่งภาพเมนูทางลัด ถามว่าจะทำให้ "มีเนื้อหาครบ" อย่างไร · ปัญหาเดิม: ไม่มีกลุ่มไฟฟ้า · ตัวเลขค้าง (คลื่น·เสียง·แสง 16 จริง 24) · การ์ด 6 ใบเรียงแถวเดียว ข้อความตกหลายบรรทัด ป้าย FREE/ตัวเลขถูกตัด
- `_admin/build_virtual_lab.py`: เพิ่ม `build_quickmenu()`/`write_quickmenu()` สร้างการ์ดระหว่าง `<!-- QM:START -->`…`<!-- QM:END -->` ใน index.html ทุกครั้งที่ build · นับจำนวนจาก GROUPS/LABS · ตั้งค่าไอคอน สี คำอธิบายที่ `QM_STYLE` และป้าย NEW ที่ `QM_NEW`
- การ์ดตอนนี้ (8 ใบ): Demo ช่วยสอน FREE · Lab กลศาสตร์ 28 · Lab คลื่น·เสียง·แสง 24 · **Lab ไฟฟ้าและแม่เหล็ก 8 (NEW)** · Lab ดาราศาสตร์ 2 · Lab การวัด 3D 3 · **Lab ทั้งหมด 62** (ใหม่ → virtual-lab.html) · Library ALL
- CSS: การ์ดกว้างขั้นต่ำ 240px (จอกว้างได้ 4 ใบ/แถว 2 แถว) · ข้อความยืดเต็มพื้นที่ คำอธิบายบรรทัดเดียวตัด … · ป้าย NEW ไม่ทับตัวเลข
- CLAUDE.md: เพิ่มหมายเหตุว่าเมนูทางลัดสร้างอัตโนมัติจาก build
- **ตรวจ**: http://localhost:8765/index.html แสดง 8 การ์ด ตัวเลขตรง labs_data.py · ลิงก์ #g-elec มีใน virtual-lab.html

### ไฟล์ที่แก้
- `_admin/build_virtual_lab.py`, `index.html`, `CLAUDE.md`, `virtual-lab.html`, `library.html`, `_admin/admin.html` (rebuild), `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–61 + เมนูทางลัด)
- ข้อความ "ตัวอย่างเด่น … จากทั้งหมด …" ในหมวด Virtual Lab ของหน้าแรกยังนับด้วยสคริปต์ register ไม่ใช่ build (ถ้าจะให้ครบควรย้ายไป build ด้วย)

## [2026-09-14 22:55] — Lab 62 แรงสู่ศูนย์กลาง: แกว่งจุกยางผ่านหลอดแก้ว (3D) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ถามว่ามีแลปการเคลื่อนที่แบบวงกลมไหม → มีแค่ VPL01 Lab 10/12/17 (2D) · เสนอรายการ 10 แลปใหม่ · ผู้ใช้: "ไล่ตามหัวข้อเลย" → เริ่มข้อ 1
- **Lab 62**: หลอดแก้ว + เชือก + จุกยาง (A 10 / B 15 / C 20 g / ปริศนา สุ่ม 8–22 g ต่อการโหลดหน้า) + ตุ้มถ่วง 50–400 g + คลิปหนีบกระดาษ + ธงนับรอบ · ปรับ L 20–100 cm
- ฟิสิกส์: แรงดึงที่ต้องใช้ mω²L (L จริง = L − ช่องว่างคลิป) เทียบ Mg → ตุ้มถ่วงเลื่อนขึ้น/ลง (คลิปชนหลอดถ้าเร็วเกิน ตุ้มตกถ้าช้าไป) · มือสั่นสุ่ม ~±0.9% · มุมเชือก sinθ = g/(ω²L) · F = mω²L ไม่ขึ้นกับมุม
- โหมดวัดเอง: แถบความเร็ว "ช้า–เร็ว" ไม่มีตัวเลข ไม่บอกมวลจุกปริศนา · ปุ่มช้าลง/เร็วขึ้น/นิดหน่อย + แป้น ← → · นาฬิกา Space/R + ตัวนับรอบนับจากจุดเริ่มจับเวลา · โหมดอัตโนมัติ: แสดง f, T, แรงดึง, มุม, คาบที่สมดุล, มวลจุกปริศนา · ประคองความเร็วให้ · จับเวลา N รอบอัตโนมัติ (เริ่มที่ธง)
- 2D: มองจากด้านบน (ธงกระพริบเมื่อครบรอบ) · ภาพขยายปลายหลอดมีไม้บรรทัด cm + แถบเขียว 0.2–1.5 cm · นาฬิกา/จำนวนรอบ/อุปกรณ์ · กรอบ "🧭 ตอนนี้ต้องทำอะไร" บอกให้เร่ง/ลดตามตำแหน่งคลิป
- ตาราง (T, F, 4π²L/T², m คำนวณ, %ต่าง, ⚠ ถ้าคลิปชนหลอด/ตุ้มตกระหว่างจับเวลา) · กราฟ F กับ 4π²L/T² แยกสีตามจุกยาง เส้นผ่านจุดกำเนิด ความชัน = m · CSV · ↺ รีเซตค่า (ไม่ลบตาราง/ไม่สุ่มจุกปริศนาใหม่)
- แท็บวิธีทดลอง (ตอน A เปลี่ยน L · B เปลี่ยน M · C จุกปริศนา · คำถาม 5 ข้อ) · ทฤษฎี (แผนภาพแรง F cosθ = mω²L cosθ · กราฟความชัน = m · แหล่งความคลาดเคลื่อน)
- **ตรวจ** (จำลองนักเรียนปรับความเร็วเองด้วยปุ่ม +/−0.5% และจับเวลา 20 รอบ): คุมคลิปอยู่ในแถบได้ · m คำนวณ B 14.0–15.6 g (จริง 15.0) · A 9.3 (10.0) · C 20.3 (20.0) · กราฟจุก B ความชัน 15.1 g (1.0%) · ภาพ 3D มุมเฉียง/บน/ข้าง/ปลายหลอด · แท็บทฤษฎี · ไม่มี console error
- ลงทะเบียน lab-62 (kp-auth.js + admin.html VLAB_SERIES + LAB_LIST) · labs_data.py topic `projectile` (ม.4) → build (63) · protect · การ์ด + preview `vpl2-whirl`: virtual-physics-lab-02.html หมวดใหม่ "🎯 การเคลื่อนที่แบบวงกลม" (บนสุด, hero 36) · index.html chip ใหม่ 🎯 การเคลื่อนที่แบบวงกลม (1) ทั้งหมด 36 / 63
- สคริปต์ลงทะเบียนชุดนี้: scratchpad `register_circ.py` (สร้างหมวด/chip ครั้งแรก ครั้งถัดไป bump ตัวเลข)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/62. centripetal-force-whirling-stopper.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–62)
- ต่อไป: Lab 63 ลูกตุ้มกรวย · 64 รถเข้าโค้งถนนเอียง · 65 วงกลมแนวดิ่ง/ลูป · 66 เหรียญบนแผ่นหมุน μs · 67 เฟือง/สายพาน ω–v · 68 เวกเตอร์ v, a ในวงกลม · 69 วงโคจรดาวเทียม · (VPL03) โมเมนต์ความเฉื่อย · โมเมนตัมเชิงมุม

## [2026-09-14 23:20] — Lab 63 ลูกตุ้มกรวย (Conical Pendulum) (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 2 ของรายการวงกลม: จุดแขวน + เชือก L 30–150 cm + ลูกตุ้ม 50/100/200 g + แผ่นใสวงกลมอ้างอิงรัศมี r (≤ 0.6L) + ธงนับรอบ · สถานที่ 🌏 โลก (9.81) / 🪐 ดาวปริศนา (สุ่ม g 3–25 m/s² ต่อการเปิดหน้า)
- ฟิสิกส์: ลูกตุ้มทรงกลม 3 มิติเต็มรูปแบบ RK4 + ฉายกลับให้เชือกยาวคงที่ + แรงต้านอากาศเล็กน้อย (วงหดช้า ๆ) · ผลักเบาไป → วิ่งเข้าใน (วงรี) · แรงไป → ออกนอกวง · พอดี v = r√(g/h) → วงกลม
- โหมดวัดเอง: แถบแรงผลัก "เบา–แรง" ไม่มีตัวเลข · ไม่บอก g ดาวปริศนา · h ในภาพข้างไม่มีตัวเลข · กรอบ 🧭 บอกว่ารอยทางเข้าใน/ออกนอกวง ให้ผลักใหม่ · โหมดอัตโนมัติ: g, h, ความเร็วที่พอดี, คาบทฤษฎี, รัศมีต่ำสุด–สูงสุด, มุม + แรงดึง · ผลักพอดีให้ · จับเวลา N รอบเริ่มที่ธง
- 2D: มองจากด้านบน (วงอ้างอิงเขียว + รอยทาง 3 s) · ภาพข้าง (h, L) · นาฬิกา/จำนวนรอบ · ตาราง (h = √(L²−r²), T, T², g, ⚠ ไม่เป็นวงกลม) · กราฟ T² กับ h แยกโลก/ดาวปริศนา ความชัน → g · CSV · ↺ รีเซตค่า
- แท็บวิธีทดลอง (ตอน A คาบกับ h · B มวล · C ดาวปริศนา · คำถาม 5 ข้อ) · ทฤษฎี (แผนภาพแรง tanθ = v²/rg = r/h · ภาพผลักเบา/พอดี/แรง)
- **ตรวจ**: ผลักพอดี รัศมี 0.965–0.977 r ใน 3 รอบ · ×0.8 เข้าใน 0.78 r · ×1.2 ออก 1.16 r · จำลองกดนาฬิกาเอง 10 รอบ (หน่วงสุ่ม ≤ 0.25 s): โลก g = 9.39–9.73 → กราฟ 9.65 (−1.6%) · ดาวปริศนา 21.05–21.61 → กราฟ 21.44 (จริง 21.8) · แก้บั๊กจับเวลาอัตโนมัติไม่เริ่ม · แก้แผ่นใสกลายเป็นเส้น (scale ผิดแกน) · ปรับกล้องให้เห็นทั้งเชือกและวง · ไม่มี console error
- ลงทะเบียน lab-63 · build (64) · protect · การ์ด + preview `vpl2-conical` (หมวดวงกลม 2, hero 37, index chip 2 · 37/64)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/63. conical-pendulum.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–63)
- ต่อไป: Lab 64 รถเข้าโค้งถนนเอียง
- หมายเหตุ: protect_new_file.py รายงาน "MOBILE" ทุกครั้งกับไฟล์ 3D (ตรวจหา order:-1) แต่ไม่ได้แก้อะไร — Lab 54–61 ก็เป็นแบบเดียวกัน

## [2026-09-14 23:50] — Lab 64 รถเข้าโค้งบนถนนเอียง (Banked Curve) (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 3 ของรายการวงกลม: สนามทดสอบวงกลม 3D (พื้นผิวสร้างจาก mesh เอียงจริง กว้าง 10 m · เส้นขอบ · เส้นกลางประ · เสาแดง-ขาว) ปรับ θ 0–40° · R 20–80 m · ผิว ☀️ แห้ง μ 0.80 · 🌧️ เปียก 0.45 · 🧊 น้ำแข็ง 0.10 · ❓ ปริศนา (สุ่ม 0.15–0.70)
- รถ 1,000 kg ระบบรักษาความเร็ว (แถบ 0–180 km/h, ±1/±5, แป้น ← →, เร่ง 1 m/s²) · มุมกล้อง ตามหลังรถ / ด้านหลัง (เห็นมุมเอียง) / ภาพรวมสนาม (ลากหมุนได้)
- ฟิสิกส์: F = m(v²/r cosθ − g sinθ) · N = m(g cosθ + v²/r sinθ) · ยึดเกาะถ้า |F| ≤ μₛN · ไถลใช้ μₖ = 0.9μₛ (คนขับหักพวงมาลัยช่วยให้ไถลช้า) · รถเลื่อนขึ้น/ลงตามพื้นเอียง ทิ้งรอยล้อ · หลุดขอบ → หยุดแล้วกลับกลางช่องทาง · วิ่งตามเข็มนาฬิกา ศูนย์กลางโค้งอยู่ซ้าย (ตรงกับภาพตัดขวาง)
- 2D: ภาพตัดขวางมองจากหลังรถ + เวกเตอร์ mg, N, f (+ แรงลัพธ์ mv²/R ในโหมดอัตโนมัติ) · มาตรความเร็วแบบเข็ม · เครื่องวัดแรงที่ยาง f (+ ดันลงเนิน), N, สถานะยาง, |f|/N
- กรอบ 🧭 แยกตอน A (หา f ≈ 0 บอกให้เร่ง/ลดตามเครื่องหมาย f) · ตอน B (เพิ่มทีละ +1 จนยางไถลออก) · ปุ่ม 📝 จดค่าจากมาตรวัด (ตอน B รับเฉพาะตอนไถล แล้วลดความเร็วให้ 15 km/h)
- ตาราง A: v, R tanθ, v², v²/Rg เทียบ tanθ · ตาราง B: v, μ จากความเร็ว, f/N ที่วัด + ค่าเฉลี่ยต่อผิว · กราฟ v² กับ R tanθ ความชัน = g · CSV · ↺ รีเซตค่า
- โหมดอัตโนมัติ: μₛ/μₖ, ความเร็วออกแบบ, v_max, v_min, mv²/R, เวกเตอร์แรงบนรถ 3D · โหมดวัดเอง: ไม่บอกค่าเหล่านี้
- **ตรวจ**: ตอน A 4 ค่า %ต่าง −2.8…+0.5 → กราฟความชัน 9.79 (−0.2%) · ตอน B เพิ่มทีละ 1 km/h: แห้ง 20°/50 m v 103 (ทฤษฎี 102.2) μ 0.812 · เปียก μ 0.455 · ถนนราบเปียก 0.453 · ผิวปริศนา 0.496/0.507 (จริง 0.49) · น้ำแข็ง 35° ขับช้า → ไถลลง · ตรวจทิศรถ/กล้องด้วยการฉายพิกัด · แก้ทิศแรงเสียดทาน (สัญลักษณ์กลับ) · ไม่มี console error
- ลงทะเบียน lab-64 · build (65) · protect · การ์ด + preview `vpl2-banked` (หมวดวงกลม 3, hero 38, index 38/65)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/64. banked-curve.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–64)
- ต่อไป: Lab 65 วงกลมแนวดิ่ง (ลูปรถไฟเหาะ + ถังน้ำแกว่ง)
- หมายเหตุ: บนน้ำแข็งที่มุมเอียงมาก รถจอดแล้วไถลลงหลุดขอบในซ้ำ ๆ (ถูกตามฟิสิกส์ แต่ผู้ใช้อาจสับสน)

## [2026-09-15 00:20] — Lab 65 วงกลมแนวดิ่ง: รางวงรอบ Loop-the-Loop (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 4 ของรายการวงกลม: รางลาดโค้ง (พาราโบลา สูง 130 cm) → ทางราบ → วงรอบแนวดิ่งรัศมี R 10–30 cm (เยื้อง z 6 cm ให้วิ่งออกได้) → ทางราบออก · ราง 2 เส้น (Tube) + หมอนรอง + เสาค้ำ + ไม้บรรทัดวัดความสูง · เซนเซอร์แรงจุดบน/ล่าง + ประตูแสงจุดบน · กรวยเหลืองชี้จุดปล่อย
- วัตถุ 50 g: 🛒 รถเข็นล้อเบา (k = 0) · ⚪ ลูกเหล็กกลิ้ง (k = 0.4) · ❓ วัตถุปริศนา (k สุ่ม 0.15–1.0) · h 5–125 cm (±0.5/±5) · ความเร็วภาพ ×0.2/×0.5/×1 · Space = ปล่อย
- ฟิสิกส์: อนุรักษ์พลังงาน ½mv²(1+k) บนราง · ในวง N = m(v²/R + g cos φ) · N < 0 → หลุดจากราง เคลื่อนที่แบบโพรเจกไทล์ · กระทบรางเก็บเฉพาะความเร็วตามแนวราง แล้วค่อย ๆ หยุดที่ก้นวง · h ≤ R ไถลกลับ
- บันทึกผลการปล่อย: ผล (ผ่าน/หลุดที่ φ/ไถลกลับ), v_บน, N_บน, N_ล่าง · สรุปต่อวัตถุ-R: h ต่ำสุดที่ผ่าน / สูงสุดที่ไม่ผ่าน → h_min/R และ k · กราฟ N_บน กับ h (× แดง = ไม่ผ่าน) เส้นตรงตัดแกน h = h_min · CSV
- โหมดอัตโนมัติ: k, h_min ทฤษฎี (เส้นเขียวในภาพข้าง), v และ N ที่จุดบนตามทฤษฎี, แรงปฏิกิริยาตลอดเวลา · โหมดวัดเอง: ไม่บอกค่าเหล่านี้
- แท็บวิธีทดลอง (ตอน A h_min · B แรงจุดบน · C ลูกเหล็ก/ปริศนา · คำถาม 5 ข้อรวมถังน้ำแกว่ง) · ทฤษฎี (แรงที่ล่าง/ข้าง/บน · 3 กรณี ผ่าน/หลุด/ไถลกลับ)
- **ตรวจ** (จำลองละเอียด 0.5 ms): รถเข็น R 20: h 50.5 ผ่าน N_บน 0.0245 N (ทฤษฎี 0.0245) · 49.5 หลุดที่ 170° · 45 หลุดที่ 147° · 18 ไถลกลับ · 80 ผ่าน N_บน 1.4715 = ทฤษฎี, v_บน 2.801 m/s · ลูกเหล็ก 54.5 ผ่าน / 53.5 หลุด → 2.700R, k 0.40 · R 15: 37.5 ผ่าน / 37 หลุด · ภาพ 3D มุมเฉียง/วงรอบขณะหลุดราง · ไม่มี console error
- ลงทะเบียน lab-65 · build (66) · protect · การ์ด + preview `vpl2-loop` (หมวดวงกลม 4, hero 39, index 39/66)
- ถังน้ำแกว่งไม่ได้ทำเป็นฉากแยก (ใส่เป็นคำถามท้ายการทดลอง)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/65. vertical-loop.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–65)
- ต่อไป: Lab 66 เหรียญบนแผ่นหมุน หา μs

## [2026-09-15 00:45] — Lab 66 วัตถุบนแผ่นหมุน: แรงเสียดทานเป็นแรงสู่ศูนย์กลาง (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 5 ของรายการวงกลม: แผ่นหมุนรัศมี 15 cm ปูผ้าสักหลาดพร้อมไม้บรรทัดตามแนวรัศมี (texture) · ฐาน + มาตรวัดรอบบนฐาน · โต๊ะรองรับวัตถุที่ตก
- วัตถุ 🪙 เหรียญ (μ≈0.32) · 🧽 ยางลบ (0.78) · 🪵 ก้อนไม้ (0.50) · ❓ ปริศนา (สุ่ม 0.20–0.90) · แต่ละตำแหน่งที่วางสุ่ม μ ±4% · วางที่ r 2–14 cm ได้สูงสุด 4 ชิ้น หรือ "วาง 3 ชิ้น (4, 8, 12 cm)"
- มอเตอร์: ตั้งรอบ 0–200 rpm (±1/±5) · ⤴ เร่งขึ้นช้า ๆ +2 rpm/s · เปลี่ยนรอบได้ไม่เกิน 30 rpm/s · ⏹ หยุด
- ฟิสิกส์ 2 มิติในกรอบเฉื่อย: ยึดเกาะเมื่อ |−ω²r + αr| ≤ μₛg (หมุนตำแหน่งตามแผ่นแบบแม่นยำ) · ไถลใช้ μₖ = 0.8μₛ ต้านความเร็วสัมพัทธ์กับผิวแผ่น → วิ่งเป็นเส้นโค้งออกนอกแผ่นแล้วตกลงโต๊ะ
- 📝 จดความเร็วรอบตอนวัตถุเริ่มไถล (Space) → ตาราง rpm, ω, ω², 1/r, μₛ = ω²r/g · กราฟ ω² กับ 1/r แยกวัตถุ ความชัน = μₛg · CSV · ↺ รีเซตค่า
- โหมดอัตโนมัติ: μₛ, รอบวิกฤต, % แรงเสียดทานที่ใช้ของทุกชิ้น · โหมดวัดเอง: ไม่บอก
- แท็บวิธีทดลอง/ทฤษฎี (แรงเสียดทานสถิตเป็นแรงสู่ศูนย์กลาง · ทางไถลจริงเทียบแนวสัมผัส)
- **ตรวจ**: แก้บั๊กรัศมีค่อย ๆ เพิ่มจากการอินทิเกรต (เดิมไถลที่ 90% ของรอบวิกฤต μ ต่ำไป 20%) → หลังแก้ ไถลตรงรอบวิกฤต · เร่ง +2 rpm/s แล้วจดช้า 0.3 s: เหรียญ μ 0.326/0.321/0.339 (จริง 0.322/0.314/0.331) กราฟ 0.326 · ยางลบ 0.791 · ปริศนา 0.649 (จริง 0.63–0.67) · วาง 3 ชิ้น ไถลตามลำดับ 12 → 8 → 4 cm · ไม้บรรทัด 3D/2D ตรงกับตำแหน่งวัตถุ · ไม่มี console error
- ลงทะเบียน lab-66 · build (67) · protect · การ์ด + preview `vpl2-turntable` (หมวดวงกลม 5, hero 40, index 40/67)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/66. turntable-friction.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–66)
- ต่อไป: Lab 67 เฟือง/สายพาน ω กับ v

## [2026-09-15 01:10] — Lab 67 อัตราเร็วเชิงมุมกับเชิงเส้น: แกนร่วม สายพาน เฟือง จักรยาน (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 6 ของรายการวงกลม: 4 รูปแบบ ① แกนร่วม ② สายพาน (Tube ตามเส้นสัมผัสจริง) ③ เฟืองขบกัน (ExtrudeGeometry ฟัน 4 ซี่/cm หมุนทิศตรงข้าม) ④ จักรยาน (จานหน้า A r 10 + ขาจาน → โซ่ → เฟืองหลัง B → ล้อหลัง C R 33 cm มีซี่ลวด)
- ล้อ A r 10 cm ขับด้วยมอเตอร์ 0–120 rpm (หน้าปัดคลาด ±3% ต้องวัดเอง) · ล้อ B ปรับ r 3–12 cm หรือ ❓ ล้อปริศนา (สุ่ม 3.5–11.5 cm) · เทปขาวบนทุกล้อ + ประตูแสงวัดคาบ (±0.3%) · เครื่องวัดความเร็วผิวที่ขอบ (±1%)
- 📝 จด (Space) บันทึกทุกล้อพร้อมกัน: r, T, ω = 2π/T, v วัด, ωr, ทิศการหมุน · สรุปต่อครั้ง ω_B/ω_A, v_B/v_A → รัศมีล้อปริศนา · ความเร็วจักรยาน km/h · กราฟ v วัด กับ ωr (เส้น v = ωr) · CSV
- โหมดอัตโนมัติ: ω, v ของทุกล้อ + ลูกศรความเร็วที่ขอบในแผนภาพ 2D · โหมดวัดเอง: ไม่บอกรัศมีล้อปริศนา
- แท็บวิธีทดลอง (5 ขั้น + คำถาม 4 ข้อ) · ทฤษฎี (ω เท่ากันทั้งล้อ v ∝ r · สายพานกับเฟือง)
- **ตรวจ**: แกนร่วม r_B 4 · สายพาน r_B 4 → ω_B/ω_A 2.500, v_B/v_A 0.998 · เฟือง r_B 6 → 1.666, 1.004 · ล้อปริศนา (10 cm) → 9.99 cm · จักรยานเฟืองหลัง 4 cm ที่ 60 rpm → 19.2 km/h · กราฟความชัน 1.000 (10 จุด) · ภาพ 3D/2D ทั้ง 4 แบบ · ไม่มี console error
- ลงทะเบียน lab-67 · build (68) · protect · การ์ด + preview `vpl2-gears` (หมวดวงกลม 6, hero 41, index 41/68)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/67. angular-linear-speed-gears.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–67)
- ต่อไป: Lab 68 เวกเตอร์ความเร็ว/ความเร่งในวงกลม · Lab 69 วงโคจรดาวเทียม

## [2026-09-15 01:35] — Lab 68 เวกเตอร์ความเร็วและความเร่งในวงกลม: ภาพแฟลชบนโต๊ะลม (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 7 ของรายการวงกลม (ทำเป็น 3D + วิเคราะห์ภาพ แทน 2D ล้วน): โต๊ะลม 120×120 cm ตาราง 5 cm + ขอบกั้น · แขนหมุนมีเซนเซอร์แรงดึงที่แกน · ลูกยาง 100/200/400 g · กล้องแฟลชเหนือโต๊ะ (ภาพเงาลูกยางสีเหลืองใน 3D)
- ตั้ง r 10–45 cm · รอบเริ่มต้น 10–90 rpm · แบบอัตราเร็วคงที่ / เร่งรอบ α 5–60 rpm/s (เลือกแล้วตั้งรอบ 15 rpm ให้) · 🔓 ปลดลูกยางจากแขน → วิ่งเป็นเส้นตรงตามแนวสัมผัส ชนขอบแล้วหยุด
- 📸 ถ่ายภาพแฟลช 12 ครั้ง Δt 0.04–0.20 s → ภาพค้างใน 2D · แตะจุดหรือ ◀ ▶ เลือกจุดวิเคราะห์ → วาด v₁, v₂ (คอร์ด/Δt) และ a (×3) บนภาพ · ด้านขวาสร้าง Δv แบบหางชนกัน + ค่าที่วัด |v₁| |v₂| |Δv| a = |Δv|/Δt, v²/r, มุมเบี่ยงจากทิศเข้าศูนย์กลาง, F/m จากเซนเซอร์
- ตาราง (แบบ คงที่/เร่ง/หลุด, r, Δt, v, a ภาพ, มุม, v²/r, F/m) · กราฟ a กับ v²/r (ฟ้า = คงที่ · ส้ม = เร่ง · แดง = หลุด) · CSV
- แท็บวิธีทดลอง (6 ขั้น + คำถาม 4 ข้อ) · ทฤษฎี (สามเหลี่ยม v₁ v₂ Δv คล้ายสามเหลี่ยม r r Δs · a_c กับ a_t)
- **ตรวจ**: อัตราเร็วคงที่ r 30/40 rpm Δt 0.1 → a 5.1873 = v²/r 5.1873, มุม 0.00° · r 20/60 rpm Δt 0.05 · r 45/30 rpm Δt 0.2 → ตรงกันทุกค่า (สูตรคอร์ดให้ค่าตรงพอดี) · F/m ต่างเล็กน้อยตามทฤษฎีคอร์ด · กราฟความชัน 1.000 · เร่งรอบจาก 15 rpm (α 40) → มุมเบี่ยง 14.2° ไปข้างหน้า · ปลดลูกยาง → a = 0 และคำใบ้อธิบาย · ไม่มี console error
- ลงทะเบียน lab-68 · build (69) · protect · การ์ด + preview `vpl2-strobe` (หมวดวงกลม 7, hero 42, index 42/69)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/68. circular-motion-vectors-strobe.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–68)
- ต่อไป: Lab 69 วงโคจรดาวเทียม

## [2026-09-15 02:00] — Lab 69 ดาวเทียมโคจร: ความเร็ววงโคจรและกฎของเคปเลอร์ (3D) · Opus 5

### ทำอะไรไปบ้าง
- ข้อ 8 ของรายการวงกลม: ดาวเคราะห์ 3D (texture สร้างเอง + ชั้นบรรยากาศ + ดาวพื้นหลัง) · ดาวเทียม + รอยทาง · กรวยแดงจุดปล่อย · เส้นเมริเดียนจุดปล่อย · มุมกล้อง เฉียง/ขั้วเหนือ/ใกล้ดาวเทียม (ระยะกล้องปรับตามขนาดวงโคจร)
- 🌏 โลก (R 6,371 km, GM 398,600) / 🪐 ดาวเคราะห์ปริศนา (รู้ R สุ่ม 3,000–9,000 km · ไม่รู้มวล · g ผิวสุ่ม 3–25) · ความสูง h 100–60,000 km (แถบลอการิทึม ±100/±1000) · ความเร็วแนวระดับละเอียด ±0.001–±1 km/s · เร่งเวลา ×100–×50,000
- ฟิสิกส์สองวัตถุ RK4 ขั้นเวลาปรับตามระยะ · ตกชนพื้นผิว / วงรี / วงกลม / หลุดพ้น (พลังงาน ≥ 0 และไกล 25R)
- เรดาร์ภาคพื้น: ความสูง อัตราเร็ว ความสูงต่ำสุด–สูงสุด (รอบล่าสุด) · นาฬิกาภารกิจจับคาบเมื่อผ่านเมริเดียนจุดปล่อย (เติมเศษเวลา) · กรอบ 🧭 บอกช้าไป/เร็วไปจากความสูงต่ำสุด/สูงสุด
- 📝 บันทึก: h ปล่อย, v, h ต่ำ–สูง, r เฉลี่ย, T, GM = v²r, GM = 4π²r³/T² · กราฟ T² กับ r³ (เฉพาะวงกลม < 1%) แยกดาว → GM, มวล, g ผิว · CSV
- โหมดอัตโนมัติ: GM, v วงกลม, คาบทฤษฎี, v หลุดพ้น, ความสูงค้างฟ้า + ปุ่มตั้งความเร็ววงกลมพอดี · โหมดวัดเอง: ไม่บอกมวลดาวปริศนา
- แท็บวิธีทดลอง (ตอน A/B/C + คำถาม 4 ข้อ) · ทฤษฎี (แรงโน้มถ่วงเป็นแรงสู่ศูนย์กลาง · ปืนใหญ่ของนิวตัน 0.8/1/1.2/√2 v_c)
- **ตรวจ**: h 400 km v 7.0 → ตก · v 8.5 → วงรีสูงสุด 4,384 km · v 12 → หลุดพ้น · วงกลมโลก h 400/5,000/20,000/35,786 km: T 5,545.7/12,069/42,625/86,173 s (ทฤษฎี 5,544.9/12,067/42,619/86,154) ความสูงแกว่ง ≤ 0.03% · กราฟ → GM 398,600 → M 5.972 × 10²⁴ kg · ดาวปริศนา 3 ความสูง → GM 369,820 = ค่าจริง, g ผิว 22.00 · ไม่มี console error
- ลงทะเบียน lab-69 · build (70) · protect · การ์ด + preview `vpl2-orbit` (หมวดวงกลม 8, hero 43, index 43/70)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/69. satellite-orbits-kepler.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py`, `virtual-lab.html`, `library.html`, `index.html`, `virtual-physics-lab-02.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit (Lab 54–69)
- ข้อ 9–10 (โมเมนต์ความเฉื่อย · อนุรักษ์โมเมนตัมเชิงมุม) เสนอไว้เป็น VPL03 ระดับมหาวิทยาลัย — ยังไม่ได้ทำ รอผู้ใช้ยืนยันว่าจะให้อยู่ VPL03 หรือ VPL02

## [2026-09-15 02:15] — Commit + push ขึ้นเว็บ (Lab 54–69) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "อัพขึ้นเว็บเลย" → ตรวจ GA ครบทุกไฟล์ใหม่ → commit 2 ชุด แล้ว push main
  - `6738608` Add 3D Labs 54-61 (ไฟฟ้าสถิต)
  - `ed7a674` Add 3D Labs 62-69 (การเคลื่อนที่แบบวงกลม) + ลงทะเบียน Lab 54–69 + เมนูทางลัดสร้างอัตโนมัติ
- ตรวจเว็บจริง https://kp-science.github.io/physics-simulations/ : virtual-physics-lab-02.html มีการ์ดใหม่แล้ว · Lab 54 และ Lab 69 ตอบ 200

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ข้อ 9–10 (โมเมนต์ความเฉื่อย · อนุรักษ์โมเมนตัมเชิงมุม) รอผู้ใช้เลือกว่าอยู่ VPL02 หรือ VPL03

### หมายเหตุ
- ⚠️ git remote origin มี GitHub token ฝังอยู่ใน URL แบบข้อความธรรมดา (เก็บใน .git/config) ควรเปลี่ยน token และตั้ง remote ใหม่แบบไม่มี token

## [2026-09-15 02:30] — Lab 65 ย้ายปุ่มปล่อยเข้าไปในแคนวาส · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ส่งภาพแผงควบคุม Lab 65: "ปรับปุ่มปล่อยไว้ในแคนวาส"
- ปุ่มสีเขียวใหญ่ในภาพด้านข้าง (2D) ใต้กล่องผลลัพธ์ · ข้อความเปลี่ยนตามสถานะ: ▶ ปล่อยวัตถุ / ⟲ หยุด · วางกลับที่จุดปล่อย (ระหว่างวิ่ง) / ▶ ปล่อยอีกครั้ง · ถ้าจอแคบ ปุ่มอยู่มุมขวาบนของแคนวาส · รองรับเมาส์และแตะ (iPad) · เคอร์เซอร์เป็นรูปมือเมื่อชี้ปุ่ม
- เอาปุ่มปล่อย/วางกลับออกจากแผงขวา เหลือคำอธิบาย + ความเร็วภาพ · แคนวาสสูง 340 px
- แก้บั๊กในภาพที่ส่งมา: เปลี่ยน R/h/วัตถุแล้วเซนเซอร์ยังโชว์ค่าของการปล่อยครั้งก่อน → วางกลับที่จุดปล่อยจะล้างค่าเซนเซอร์
- **ตรวจ**: ส่ง mousedown ที่ตำแหน่งปุ่ม → ปล่อยวัตถุ · วิ่งจนจบ ผ่านวงรอบ N_บน 0.491 N · เปลี่ยน R เป็น 23 → เซนเซอร์ล้างเป็น —

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/65. vertical-loop.html`, `SESSION_LOG.md`

## [2026-09-15 03:10] — Lab 62–69: ปุ่มควบคุมในแคนวาส 2D + นิ้วซูม/เลื่อนภาพ 3D บนมือถือ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: (1) "ขอให้ปรับทุกแลปที่ทำมา" (ปุ่มในแคนวาสแบบ Lab 65) (2) "เปิดในโทรศัพท์ … อยากให้ย่อขยายหรือเลื่อนโดยใช้นิ้ว"
- **แถบปุ่มล่างแคนวาส 2D** (สูง 52 px กดด้วยนิ้ว/เมาส์ ข้อความย่ออัตโนมัติให้พอดีปุ่ม ปุ่มที่ใช้ไม่ได้เป็นสีเทา):
  - 62 ▶ เริ่ม/⏹ หยุดแกว่ง · − ช้าลงนิด · + เร็วขึ้นนิด · ⏱ นาฬิกา
  - 63 ▶ ผลักลูกตุ้ม/↻ ผลักใหม่ · ✋ จับหยุด · ⏱ นาฬิกา
  - 64 −5 −1 +1 +5 · ⏹ จอด · 📝 จด (ตามตอน A/B)
  - 65 คงปุ่มใต้กล่องผลลัพธ์แบบเดิม
  - 66 ➕ วางวัตถุ · ⤴ เร่งช้า ๆ/⏸ หยุดเร่ง · ⏹ หยุดมอเตอร์ · 📝 จดตอนไถล
  - 67 −10 rpm · +10 rpm · 📝 จดคาบและความเร็ว
  - 68 ▶ หมุน/⏹ หยุดแขน · 📸 ถ่ายภาพ · 🔓 ปลด · 📝 บันทึก
  - 69 −0.1 −0.01 +0.01 +0.1 · 🚀 ปล่อย · 📝 บันทึก
- **ท่าทางบนภาพ 3D** (ทุกแลป 62–69): 1 นิ้วลาก = หมุน · 2 นิ้วถ่าง/หนีบ = ซูม · 2 นิ้วลาก = เลื่อนภาพ · เมาส์: คลิกขวาหรือ Shift+ลาก = เลื่อน · ล้อ = ซูม · กดปุ่มมุมมองเพื่อกลับตำแหน่งเดิม
  - 64 มุมตามรถ/ด้านหลัง: สองนิ้วซูมระยะกล้อง (ไม่สลับมุม) · มุมภาพรวม: เลื่อนได้ · รีเซตค่าคืนระยะ/การเลื่อน
  - 69 ซูมผ่าน orbit.zoom · กดปุ่มมุมมองคืนจุดศูนย์กลาง
- Lab 68 จอแคบ (< 560 px): ภาพแฟลชเต็มความกว้างด้านบน การสร้าง Δv และค่าที่วัดอยู่ด้านล่าง (เดิมบนมือถือตัวเลขวิเคราะห์ถูกซ่อน) · แก้แสดง −0.0°
- **ตรวจ** (จำลอง 375×812 ส่ง TouchEvent จริง): ทุกแลปลาก 1 นิ้วหมุน · ถ่ายสองนิ้วซูม ×2 · สองนิ้วลากเลื่อนจุดมอง · แตะปุ่มในแถบทำงาน (62 เริ่มแกว่ง · 63 ผลัก · 64 +1 km/h · 66 เร่งช้า ๆ · 67 +10 rpm · 68 หมุน/ถ่าย/บันทึก · 69 +0.1/ปล่อย) · ไม่มี console error · เดสก์ท็อปแสดงแถบปุ่มปกติ

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/62.–69.*.html`, `SESSION_LOG.md`

### หมายเหตุ
- สคริปต์ patch: scratchpad `patch_touch.py` (setupPointer ใหม่ + camRotate/camZoom/camPan + drawCanvasBar) — Lab 46–61 ยังเป็นแบบลากหมุนนิ้วเดียว ถ้าจะใช้ท่าทางเดียวกันต้องปรับเพิ่ม

## [2026-09-15 03:40] — Lab 46–61: นิ้วซูม/เลื่อนภาพ 3D บนมือถือ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "ปรับแลป 46-61 ด้วย" (ท่าทางนิ้วแบบเดียวกับ 62–69)
- แลปเก่าหลายแลปใช้นิ้วเดียวลากวัตถุ (หมุด เข็ม ฉาก เครื่องวัด) จึงไม่แก้ setupPointer เดิม → เพิ่มสคริปต์เสริมก่อน `<!-- KP Watermark -->` ในทุกไฟล์:
  - ดักที่กรอบ `#view3d` แบบ capture: 2 นิ้วถ่าง/หนีบ = ซูม (ใช้ขอบเขตระยะเดียวกับล้อเมาส์ของแต่ละแลป) · 2 นิ้วลาก = เลื่อนจุดมอง · นิ้วเดียวยังทำงานแบบเดิมทุกอย่าง
  - พอนิ้วที่สองแตะ ส่ง touchend ให้ตัวจัดการเดิมเพื่อจบการลากวัตถุที่ค้างอยู่
  - เมาส์: คลิกขวาหรือ Shift+ลาก = เลื่อน · ปิดเมนูคลิกขวาบนภาพ 3D
  - 46 ใช้ตัวแปรกล้อง `cam` · 53 ตั้งจุดมองใหม่ทุกเฟรม จึงเพิ่ม `PAN_OFF` (รีเซตเมื่อกดปุ่มมุมมอง)
  - มุมมองแบบกล้องตายตัว (เช่น มุมตา มุมจอ) และมุมที่ตามวัตถุ การเลื่อนอาจไม่มีผล กดปุ่มมุมมองแบบหมุนได้ก่อน
- **ตรวจ** (375×812 ส่ง TouchEvent จริง ทั้ง 16 แลป): ถ่างสองนิ้ว → ระยะกล้องลดครึ่ง · ลากสองนิ้ว → จุดมองเลื่อน · นิ้วเดียวยังหมุนได้ในแลปที่เริ่มด้วยมุมหมุน (50, 54–56, 58–61) · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/46.–61.*.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ปุ่มควบคุมในแคนวาส 2D ยังมีเฉพาะ Lab 62–69 (Lab 46–61 ยังไม่มี)

## [2026-09-15 04:10] — Lab 46–61: แถบปุ่มควบคุมใต้ภาพ 2D · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "ใส่ปุ่มในแคนวาส 46-61 ด้วย"
- เพิ่มสคริปต์เสริมในทุกไฟล์ (ก่อน `<!-- KP Watermark -->`): สร้างแคนวาสแถบปุ่ม `#kpCbar` ต่อท้าย `#diagCanvas` ในกรอบภาพ 2D เดียวกัน · กดด้วยนิ้ว/เมาส์
  - ปุ่มในแถบ "กดปุ่มเดียวกันในแผงขวา" (button.click()) → พฤติกรรมเหมือนเดิมทุกอย่าง ไม่แตะโค้ดแลปเดิม
  - แสดงเฉพาะปุ่มที่มองเห็น/ใช้ได้ในขณะนั้น (ตามตอน A/B/C) · ปุ่มที่เลือกอยู่ (active) ขอบเหลือง · มือถือแถวละ 4 ปุ่ม เดสก์ท็อปแถวละ 8 · ตัวอักษรย่อให้พอดี · อัปเดตทุก 150 ms
  - สีเขียว = บันทึก/จด · ส้ม = ปุ่มสำคัญ/สวิตช์ · เทา = ปรับค่า
- ปุ่มต่อแลป: 46 ↔/↕ ไม้บรรทัด · 📝 บันทึก | 47–48 ↔ ส่ายสายตา · 📝 บันทึก | 49 ±1°/±0.1° · 📝 θ₁θ₂ · 📍 มุมวิกฤต | 50 ±10°/±1° · 📝 | 51 ±1°/±0.1° · 📝 i,δ | 52 ±1/±0.1 mm (ตอน A) · ±1°/±0.1° + 📝 (ตอน B) | 53 ±5 cm/±1 mm (แว่นขยาย) · 📝 | 54 🧣 ถู · 👉 แตะจาน · ↩ ถอย · 👆 ต่อดิน · 📝 A/B | 55 ⚡A ⚡B · r ±1 · TARE · 📝 A/B | 56 ⏻ ไฟ · 🥄 คนผง · 📝 (A) / ⚡±2 kV · ⏚ · 📝 (B) | 57 ◀▲▼▶ · 📍 ทำจุด · 📝 x,V | 58 d ±1/±0.1 · 0 ศูนย์ Q · 📝 A/B | 59 สวิตช์ A/กลาง/B · ▶ นาฬิกา · 📝 จดค่า | 60 💨 พ่น · ⏻ สวิตช์ · ±1 V · ▶ นาฬิกา · 📝 | 61 ①②③ สวิตช์ · 📝 จด V · 📝 จด C · 👉 ขั้นตอนนำทาง
- **ตรวจ** (375×812 ส่ง TouchEvent ที่ปุ่มแรกของแถบทุกแลป): ปุ่มในแผงถูกกดจริงทั้ง 16 แลป · จำนวนปุ่ม/ความสูงแถบถูกต้อง · ภาพ Lab 61 สวิตช์ที่เลือกมีขอบเหลือง · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/46.–61.*.html`, `SESSION_LOG.md`

## [2026-09-15 10:30] — ตรวจรายการแลปที่ควรปรับ + ข้อ 1: ลากด้วยนิ้วบน Lab 33 · 38 · VPL01-43 · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ถาม "มีแลปไหนที่ควรปรับบ้าง" → สแกนทั้ง 70 ไฟล์ สรุป 4 กลุ่ม: (1) ลากด้วยนิ้วไม่ได้ Lab 33, 38, VPL01-43 (2) VPL01 + VPL02 30–45 ยังไม่มีค่าปริศนา/🧭/แถบปุ่มในแคนวาส/CSV (VPL01) · Lab 5 ไม่มีปุ่มรีเซต (3) 3D ที่ขาด 🧭: 46–49, 51–53, 60 · ขาดค่าปริศนา: 46, 47, 52, 55, 57, 60, 61 · VPL03 Lab 1 ไม่มีท่านิ้ว/แถบปุ่ม (4) เลข 42–44 ซ้ำระหว่าง VPL01 กับ VPL02
- ผู้ใช้: "รันตามลำดับได้เลย"
- ข้อ 1: เพิ่มสคริปต์ `KP Touch Bridge` ก่อน `</body>` แปลง touchstart/move/end บนแคนวาสเป็น mousedown/move/up (กันเลื่อนหน้าเฉพาะตอนจับวัตถุได้ นอกนั้นเลื่อนหน้าได้ตามปกติ) + ขยายระยะจับสำหรับนิ้ว
  - Lab 33: ลาก/หมุนไม้โปรแทรกเตอร์ (ตอน III/IV)
  - Lab 38: ลากขาคาลิปเปอร์ (c1, c2)
  - VPL01 Lab 43: ลากจุดบนวงกลมเฟส (A) · ลากขาไม้วัดเวลา (C)
- **ตรวจ** (375×812 ส่ง TouchEvent จริง): 38 ขา A เลื่อน 9.9 → 13.4 · 33 ลากศูนย์กลาง +30,+20 และหมุน 0 → 90° · 43 วงกลมเฟสและขาไม้วัดขยับ · แตะที่ว่างไม่กันการเลื่อนหน้า · ไม่มี JS error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/33. wave-refraction-ripple-tank.html`, `Virtual Physics Lab 02/38. wave-speed-on-string.html`, `Virtual Physics Lab 01/Mechacnics/43. shm-phase-explorer.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ต่อข้อ 3: 🧭 + ค่าปริศนาให้ Lab 46–61 · ยังไม่ commit

## [2026-09-15 11:00] — VPL03 Lab 1 ท่านิ้ว + แถบปุ่ม · แก้ path สคริปต์ผิดใน VPL01 · Opus 5

### ทำอะไรไปบ้าง
- VPL03 Lab 1: ใส่สคริปต์เสริมแบบเดียวกับ Lab 46–61 ก่อน `<!-- KP Watermark -->` — 2 นิ้วถ่าง/หนีบซูม (ระยะ 25–600) · 2 นิ้วลากเลื่อนภาพ · คลิกขวา/Shift+ลากเลื่อน · แถบปุ่ม `#kpCbar` ใต้ **แว่นขยายสเกล** (`#magCanvas`): 🎯 แตะวัตถุ · 🔄 หมุนวงแหวน · ↔ เปิดออก · ✅ ตรวจค่าที่อ่าน · ➕ บันทึก (แสดงเฉพาะปุ่มที่กดได้)
  - **ตรวจ** 375×812: ถ่างสองนิ้ว ระยะกล้อง 300 → 150 · ลากสองนิ้วจุดมองเลื่อน · แตะ 🎯 ในแถบ → ปากวัดแตะวัตถุ ปุ่มบันทึกเปิดใช้
- **บั๊กที่เจอระหว่างทดสอบ**: VPL01 Lab 21, 42, 43 โหลด `../_shared/watermark.js` / `../kp-auth.js` (ผิดชั้น → 404) ทำให้ไม่มีลายน้ำ และ Lab 42–43 ไม่มี kp-auth (topbar login/สิทธิ์ไม่ทำงาน) → แก้เป็น `../../` · ตรวจแล้วโหลดครบ (kpLogout, KPWatermark มี) · สแกนไฟล์แลปทั้งหมดไม่มี .js path เสียอีก

### ไฟล์ที่แก้
- `Virtual Physics Lab 03/1. precision-measurement-3d.html`
- `Virtual Physics Lab 01/Mechacnics/21. SHM_Linear_Air_Track.html`, `42. shm-spring-builder.html`, `43. shm-phase-explorer.html`
- `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ข้อ 3 ส่วน Lab 46–61 (🧭 + ค่าปริศนา) กำลังทำ · ยังไม่ commit

## [2026-09-15 12:30] — ข้อ 3: 🧭 ตอนนี้ต้องทำอะไร ใน Lab 46–60 + ค่าปริศนาใหม่ 8 แลป · Opus 5

### ทำอะไรไปบ้าง
- พบว่า 🧭 ใน Lab 50–59 เป็นแค่ไอคอนหัวแผนภาพ → ทำกรอบ "🧭 ตอนนี้ต้องทำอะไร" แบบเปลี่ยนตามสถานะ (`#hint` + `hintState()`) ให้ Lab 46–60 ทุกแลป วางต่อจากส่วนโหมด/รีเซต · ลบกล่องคำแนะนำคงที่เดิม (`manualHint`, `focusHint`, `hintA/B`, `hintT`) แล้วรวมเข้ากรอบใหม่ · โหมดวัดเองไม่บอกคำตอบ
- **ค่าปริศนาใหม่**:
  - 46 กระจกเว้าปริศนา f 6–22 cm (ค่าเริ่มต้น) · แก้คำตอบรั่วเดิม: ตำแหน่งจอ/วัตถุเริ่มต้นอิง f, ข้อความ "จออยู่ที่จุดโฟกัส", สไลเดอร์ f ตั้งเป็นค่าซ่อน, 🎲 ลบตาราง A, บันทึกแล้วเขียนทับ f จริงของแถวเก่า
  - 47 กระจกโค้งปริศนา (ไม่บอกว่าเว้า/นูน) |f| 9–16 cm · กราฟลากเส้นความชัน −1 หา 1/f
  - 50 แผ่นโพลารอยด์ปริศนา แกนซ่อนเยื้องจากขีดชี้ φ 10–170° · ตาราง C + ปุ่ม 📍 ตรวจคำตอบ
  - 52 ของเหลวปริศนา n(650) 1.340–1.385 · มุมรุ้งคำนวณจาก n (ตรวจกับสูตรตรง: n 1.376 → 36.21°/61.56° ตรงกัน)
  - 55 ทรงกลม B ประจุปริศนา ±5–18 nC · ตอน C
  - 56 ลูกบอลประจุปริศนา 0.8–1.8 nC (tanθ = qV/(mgd))
  - 57 แหล่งจ่ายปริศนา 6–11.5 V จอปิด ขั้วพันเทปฉนวน → หาจาก E = −ΔV/Δx
  - 60 น้ำมันปริศนา ρ 750–1250 kg/m³ → ปรับสไลเดอร์ ρ ให้ q เป็นจำนวนเท่าของ e
  - 61 ตัวเก็บประจุ Cx 60–120 μF (เครื่องวัดสเกล 50 μF ขึ้น OL ต้องคำนวณจากวงจร) + ตอน D ในคู่มือขั้นตอน
- แก้ขั้นตอน Lab 56: เดิม "4 kV, d = 8 cm" ลูกบอลเบนไปแตะแผ่น (ตรวจแล้ว) → เปลี่ยนเป็น d = 10, 11, 12, 14, 16 cm (ประจุปริศนาสูงสุด 1.8 nC ที่ d 10 ไม่แตะ)
- **ตรวจในเบราว์เซอร์ทั้ง 16 แลป**: โหลดไม่มี JS error · กรอบ 🧭 ขึ้นและเปลี่ยนตามสถานะ (เช่น 55 ใส่ประจุปริศนาก่อน TARE → เตือนต่อดิน) · แถบปุ่ม kpCbar และท่านิ้ว 2 นิ้วยังทำงาน · ค้นข้อความหน้าเว็บไม่พบค่าปริศนา (50, 52, 55, 57, 60, 61) · 50 แกนจริงตรงกับตำแหน่งแสงมากสุด
- หมายเหตุการทดสอบ: แท็บเบราว์เซอร์ที่อยู่เบื้องหลัง requestAnimationFrame หยุด กรอบ 🧭 จึงไม่อัปเดตจนกว่าจะเปิดแท็บ (ไม่ใช่บั๊ก)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/46.–61.*.html` (16 ไฟล์), `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit / ยังไม่ขึ้นเว็บ (รวมข้อ 1 + VPL03 Lab 1 + path fix)
- ข้อ 2 (ยกระดับ VPL01 + VPL02 30–45) ยังไม่เริ่ม — งานใหญ่ รอผู้ใช้เลือกแลปนำร่อง · Lab 5 ไม่มีปุ่มรีเซต
- ข้อ 4 เลข 42–44 ซ้ำ VPL01/VPL02 — ยังไม่แตะ (กระทบ URL/สิทธิ์)

## [2026-09-15 13:30] — Lab 55: ทรงกลมแตะกันได้จริง + กรอบกรอกข้อมูลใต้แผนภาพ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "สเกลเวลาชนกันต้องอ่านได้ 0 มั้ย · แต่ชนกันมันอ่านได้ 4.5" → ตรวจแล้ว r ต่ำสุดเดิม 4.5 cm (ผิวห่าง 5 mm) แต่ภาพ 2D/3D ดูเหมือนชน (ช่องว่าง ≈ 1–2 px) · อธิบายว่าสเกลอ่าน r ศูนย์กลาง–ศูนย์กลาง แตะกันควรอ่าน 2a = 4.0 cm · ผู้ใช้เลือกแบบ 1
- **แตะกันได้จริง**: `R_MIN = R_TOUCH = 4.0` (สไลเดอร์ min 4) · `shareTouch()` เมื่อผิวแตะกัน ประจุไหลจนเท่ากัน q = (q_A+q_B)/2 (เก็บใน `S[k].qx`, ป้าย "q แตะกัน#n", ถ้ามีประจุปริศนาปน `hid` → ป้าย ❓ และไม่คำนวณ k) · ⚡/❓/⏚ ล้าง qx · แผนภาพขึ้น "แตะกัน!" · 🧭 เตือน · บันทึกขณะแตะกันถูกปฏิเสธ · คู่มือเพิ่มข้อเรื่องแตะกัน
- **ผู้ใช้งงปุ่มบันทึกสีเขียว 2 ปุ่ม** → ย้ายการกรอกข้อมูลมาไว้ใต้แผนภาพ 2D (`#recForm`): เลือก ชุด A (เปลี่ยน r) / ชุด B (เปลี่ยนประจุ) · ช่อง ① ระยะ r (อ่านที่ขีดชี้) ② ค่าอ่านเครื่องชั่ง (อ่านค่ากลาง) · ปุ่ม 📝 บันทึกปุ่มเดียว · ข้อความเตือนในกรอบแทน alert · Enter ข้ามช่อง/บันทึก · โหมดอัตโนมัติกรอกค่าให้ (readonly)
  - ลบแผง "🖐 บันทึกผล" และปุ่มบันทึกในแผงอัตโนมัติ · แถบ kpCbar เอาปุ่ม 📝 A/B ออก
  - แผงขวาใหม่ "📊 ผลที่บันทึกล่าสุด": ชุด/แถว · r (cm, m) · 1/r² · Δm · F = Δm·g · ผลัก/ดูด · ประจุ · k ≈ Fr²/(q_Aq_B) หรือ q_X · คำแนะนำขั้นต่อไป
- **ตรวจ**: TARE → ⚡A ⚡B → r 15 บันทึก → k 8.92 × 10⁹ แสดงในแผงขวา · แบ่ง A ครึ่ง แล้วเลื่อนลงแตะ → q ทั้งสอง 1.0014e-8 = (6.68e-9+1.335e-8)/2 · สเกลอ่าน 4.0 · บันทึกขณะแตะถูกปฏิเสธ · ขยับขึ้นประจุยังเท่ากัน · ประจุปริศนาแตะ A → ป้าย ❓ · โหมดอัตโนมัติกรอกค่าให้ · มือถือ 375 px ไม่ล้นจอ · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/55. coulombs-law-balance.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit · ถ้าผู้ใช้ชอบรูปแบบกรอกข้อมูลใต้แผนภาพ อาจทำแบบเดียวกันกับแลปอื่นที่มีปุ่มบันทึกหลายปุ่ม

## [2026-09-15 14:10] — แผงตั้งค่าเลื่อนขึ้นจากขอบล่างบนจอแคบ (ต้นแบบ Lab 55) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: บนโทรศัพท์/ไอแพดจอเล็ก แผงตั้งค่าไปอยู่ล่างสุด คนไม่รู้จะหาไม่เจอ · เสนอ 3 แบบ ผู้ใช้เลือกแบบที่แนะนำ (แผงเลื่อนขึ้นจากขอบล่าง)
- สคริปต์กลางใหม่ `_shared/kp-mobile-panel.js` (ใช้ได้ทุกแลปที่มี `.sim-panel` + `#tab-sim`):
  - จอ ≤ 900 px: ย้ายเนื้อหาแผงขวา (element จริง คง id/event) ไปไว้ในแผ่น `#kpSheet` (สูง 46% จอ · ↕ ขยาย 84% · ✕ ปิด · ปัดหัวแผงลง = ปิด/ย่อ ปัดขึ้น = ขยาย) · แผ่นอยู่ใน #tab-sim เพื่อให้ kpCbar ยังหาปุ่มเจอ
  - แถบติดขอบล่าง `#kpMBar`: บรรทัด 🧭 ขั้นตอนตอนนี้ (สีตาม info/warn/ok แตะเพื่อดูเต็ม) + ปุ่ม **👉 ทำขั้นนี้** + แท็บ **⚙️ ตั้งค่า** / **📊 ผล / ตาราง**
  - 👉 ทำขั้นนี้: หาปุ่มที่ชื่ออยู่ใน `<b>` ของคำแนะนำ → ถ้าอยู่ในแผง เปิดแผงเลื่อนไปที่ปุ่มแล้วกระพริบขอบเหลือง · ถ้าอยู่บนหน้า (เช่น 📝 บันทึก ใต้แผนภาพ) ปิดแผงแล้วเลื่อนหน้าไปที่ปุ่ม
  - เปิดแผงแล้วเลื่อนหน้าให้ภาพ 3D อยู่ครึ่งบน · ไปแท็บอื่น (วิธีทดลอง/ทฤษฎี) แถบซ่อน · ขยายจอเกิน 900 px คืนเนื้อหากลับแผงขวาตามลำดับเดิม
- Lab 55 ใส่ `<script src="../_shared/kp-mobile-panel.js">` ก่อน `<!-- KP Watermark -->`
- **ตรวจ** 375×812: แถบล่างขึ้น บรรทัด 🧭 ตรงกับคำแนะนำ · แตะ ⚙️ ตั้งค่า แผงเลื่อนขึ้น ภาพ 3D ยังเห็นด้านบน · 👉 ทำขั้นนี้ → TARE กระพริบในแผง · กด TARE → เป้าหมายเปลี่ยนเป็น ⚡ แตะทรงกลม A · หลังมีประจุ → เป้าหมาย 📝 บันทึก (ปิดแผง เลื่อนไปกรอบบันทึก) · 📊 ผล/ตาราง เห็นตาราง กราฟกว้าง 331 px · kpCbar ยังมี 5 ปุ่ม · กลับจอกว้าง แผงขวาครบ 9 ส่วน · ไม่มี console error

### ไฟล์ที่แก้
- ใหม่: `_shared/kp-mobile-panel.js`
- `Virtual Physics Lab 02/55. coulombs-law-balance.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอผู้ใช้ลองบนโทรศัพท์/ไอแพด ถ้าโอเค → ใส่สคริปต์ให้ Lab 46–69 (+ VPL03 Lab 1 ถ้าโครงสร้างตรง) · ยังไม่ commit

## [2026-09-15 14:50] — แผงตั้งค่าเลื่อนขึ้นจากขอบล่าง: ขยายไปทุกแลป (ระหว่างทำ) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "ทำแบบนี้กับทุกแลปไหวมั้ย"
- ใส่ `kp-mobile-panel.js` (โหมดปกติ `.sim-panel`) ให้ VPL02 Lab 30, 31, 32, 32B, 32C, 33B, 35, 36, 46–54, 56–69 (31 ไฟล์ + 55 เดิม = 32) · **ตรวจ** 375×812 ทุกไฟล์: แถบล่างขึ้น แผงมีเนื้อหาครบ ไม่มี console error ไม่ล้นจอ · 🧭 ตรงกับคำแนะนำ (61 แสดงเฉพาะขั้นปัจจุบัน) · kpCbar ยังหาปุ่มเจอ
- ปรับสคริปต์: แปลงข้อความ 🧭 เว้นวรรคระหว่างบล็อก · แลปไม่มี #view3d เลื่อนหน้าให้ canvas หลักอยู่ครึ่งบน · เพิ่มการตั้งค่ารายแลป `window.KP_MPANEL={move,res,view,hint,tab,bp}` สำหรับแลปที่ไม่ใช้ `.sim-panel` (ย้าย element ทั้งก้อน · ซ่อนแท็บ 📊 ถ้าไม่มีส่วนผล · หา "หน้า simulation" จากการมองเห็น)
- วัดเค้าโครง 38 แลปที่เหลือด้วย puppeteer ที่ 375 px: บางแลปตัวควบคุมอยู่ใต้ภาพ (VPL01 1–4, 13, 16; VPL02 33, 44, 45) บางแลปกองอยู่เหนือภาพจนภาพลึก > 1000 px (VPL01 7, 8, 14, 17, 18, 21; VPL02 40, 43)
- แบ่งผู้ช่วย 4 ชุดทำ config รายแลป: VPL01 (1–8), (9–17), (18–21, 42–44 + VPL03 Lab 1), VPL02 (33, 34, 37–45) — กำลังทำ

### ไฟล์ที่แก้
- `_shared/kp-mobile-panel.js`, `Virtual Physics Lab 02/30.–36., 46.–69.*.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอผลผู้ช่วย 4 ชุด แล้วตรวจในเบราว์เซอร์ · ยังไม่ commit

## [2026-09-15 15:40] — แก้ JS พังที่เจอระหว่างทำแผงมือถือ (topbar แทรกผิดที่ · \!== · Demo ขาด })();) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ช่วยชุด A รายงานว่า VPL01 Lab 1, 2 มี "Invalid or unexpected token" ตั้งแต่เวอร์ชันใน git → สแกนสคริปต์ inline ทุกไฟล์ HTML ด้วย `node --check`
- **topbar ถูกแทรกกลางข้อความ `'<body style=…>'` ในสคริปต์กันโดเมน** (อยู่ใน `<head>`): สคริปต์กันโดเมนพัง + topbar ไม่แสดง → ย้าย `<!-- KP Topbar -->…</nav>` ไปหลัง `<body>` จริง: `mechanics.html`, `course.html`, `plane_mirror_reflection.html`, VPL01 Lab 1, Lab 2 · `plane_mirror_reflection.html` มีปุ่ม `KP-BACK-BUTTON` ถูกแทรกผิดที่แบบเดียวกัน → ย้ายไปหลัง `<body>`
- **`virtual-physics-lab-01.html`**: `typeof currentUser \!== 'undefined'` → สคริปต์ทั้งก้อนพัง `dlPdf` ไม่มี **ปุ่ม ⬇ คู่มือ Lab ทั้ง 23 ปุ่มกดไม่ได้** → แก้เป็น `!==` · ตรวจแล้ว `dlPdf` เป็น function
- **Demo 22 ไฟล์** (`Demo/mechanics/…`): บล็อก KP-DOMAIN-PROTECTION ขาด `})();` (template รุ่นเก่า) → เติมให้
- `_admin/protect_new_file.py`: ตรวจ TOPBAR_POS เพิ่มกรณี `<!-- KP Topbar -->` อยู่ก่อน `</head>` · ตอนย้ายลบช่องว่าง/ขึ้นบรรทัดก่อนหน้าด้วย (ไม่ให้เหลือบรรทัดใหม่ในข้อความ JS)
- สแกนซ้ำทั้งโปรเจกต์: สคริปต์ inline ที่ syntax ผิด = 0 · เปิดในเบราว์เซอร์ Lab 1 มี topbar + kpLogout · mechanics.html มี topbar · ไม่มี console error

### ไฟล์ที่แก้
- `mechanics.html`, `course.html`, `plane_mirror_reflection.html`, `virtual-physics-lab-01.html`, VPL01 `1.`, `2.`, `Demo/mechanics/**` 22 ไฟล์, `_admin/protect_new_file.py`, `SESSION_LOG.md`

## [2026-09-15 16:30] — แผงตั้งค่าเลื่อนขึ้นจากขอบล่าง: ครบทุกแลป (70) + แก้หน้าแรกบนมือถือ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ช่วย 4 ชุดใส่ config `window.KP_MPANEL` + `kp-mobile-panel.js` ให้ 38 แลปที่โครงสร้างต่างกัน (VPL01 ทั้งหมด, VPL02 33, 34, 37–45, VPL03 Lab 1) · ตรวจ headless ทุกไฟล์: ไม่มี page error · ปุ่ม/ช่องกรอกครบเท่าเดิม · กดตัวควบคุมในแผงแล้วแลปตอบสนอง · จอ 1400 px ตำแหน่งเท่า HEAD (0–3 px) · ย่อ-ขยายจอแล้วคืนที่เดิม
  - ภาพหลักขึ้นมาบนสุดชัดเจน: VPL01 7 (1067→453), 9 (682→271), 11 (665→348), 14 (canvas เคยถูกบีบเหลือ 21 px → 260), 17 (923→383), 18 (1073→370), 21, 42; VPL02 34, 37, 38 (696→445), 40 (1143→460), 43 (1022→433)
  - แลปที่มีหลายตอน (VPL01 43, VPL02 38, 43) เพิ่ม CSS/shim ซ่อนแผงของตอนที่ไม่ได้เลือกในแผ่นเลื่อน
  - `hint:'#kpNoHint'` ปิดบรรทัด 🧭 ในแลปที่กล่อง hint มีเฉลย (VPL01 18, 19, 21) · VPL01 6.2 ไม่ผูก hintBox (เป็นกล่องเฉลย)
- สคริปต์กลาง: บรรทัด 🧭 ว่างให้ซ่อน · 👉 ทำขั้นนี้ อ่าน `<strong>` และตัดเครื่องหมายคำพูด · `#kpSheet .sb>*{flex-shrink:0}` (กล่องที่มี overflow เคยถูกบีบเตี้ย)
- VPL01 Lab 17: หน้ากว้าง 434 px บนมือถือ (grid 1fr ขยายตามเนื้อหา + แถบแท็บไม่ตัดบรรทัด) → `minmax(0,1fr)`, `.sl-range{min-width:0}`, `nav{flex-wrap:wrap}` → 375 px
- **index.html**: จอ 375 px ปุ่มเมนู ☰ อยู่ที่ x = 466 (นอกจอ กดไม่ได้) เพราะปุ่ม "🎬 ใช้งานฟรี" · ซ่อนปุ่มนั้นที่ ≤ 480 px (ลิงก์ Demo มีในเมนูแล้ว) → ☰ อยู่ที่ 353
- ตรวจในเบราว์เซอร์ (375×812): VPL01 1, 2, 7, 9, 12, 14, 17, 18, 43 · VPL02 38, 43 — แถบล่างขึ้น แผงมีเนื้อหา ไม่ล้นจอ ไม่มี console error · VPL03 Lab 1 เปิดแบบไม่ login ถูก guard ส่งกลับหน้าแรก (ตามระบบสิทธิ์) จึงตรวจได้แค่ headless

### ไฟล์ที่แก้
- `_shared/kp-mobile-panel.js`, VPL01 ทุกไฟล์ (26), VPL02 33, 34, 37–45, VPL03 `1.`, `index.html`, `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit / ยังไม่ขึ้นเว็บ (งานทั้งวันนี้: ข้อ 1, 3, Lab 55, แผงมือถือ, แก้ JS พัง)
- ข้อ 2 (ยกระดับแลปรุ่นเก่า) และข้อ 4 (เลข 42–44 ซ้ำ) ยังไม่ทำ

## [2026-09-15 16:50] — Commit + push ขึ้นเว็บ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้: "อัพขึ้นเว็บ" → fetch (ไม่มี commit ใหม่จากอีกเครื่อง) → commit 2 ชุด แล้ว push main
  - `fd8bdae` แก้สคริปต์ inline พังทั้งเว็บ (ปุ่มดาวน์โหลดคู่มือ VPL01 · topbar แทรกผิดที่ · Demo 22 ไฟล์ · protect script) + ปุ่ม ☰ หน้าแรกบนมือถือ
  - `70c8ce4` แผงตั้งค่าเลื่อนขึ้นจากขอบล่าง 70 แลป · 🧭 + ค่าปริศนา Lab 46–61 · Lab 55 · แก้ลากด้วยนิ้ว · VPL03 Lab 1
- ตรวจเว็บจริง: `_shared/kp-mobile-panel.js` ตอบ 200 · Lab 55 มี recForm + สคริปต์แผง · virtual-physics-lab-01.html เป็น `!==` แล้ว · index.html มีกฎซ่อนปุ่มที่ ≤ 480 px

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอผู้ใช้ลองบนโทรศัพท์/ไอแพดจริง
- ข้อ 2 (ยกระดับแลปรุ่นเก่า) · ข้อ 4 (เลข 42–44 ซ้ำ) · ข้อ 9–10 ชุดวงกลม (VPL02/VPL03) ยังไม่ทำ

## [2026-09-15 18:00] — ออกแบบหน้าแรกใหม่ (ต้นแบบใน _preview/) · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ไม่ชอบ index.html (ยาว ≈ 12,000 px · canvas 53 ตัว · เมนูซ้ำ 3 ชุด · ตัวเลข "40+" เก่า)
- ต้นแบบ v1/v2 (`_preview/index-redesign-v1.html`, `index-redesign.html`): แนวคู่มือแล็บ + motion infographic (treemap, กายวิภาคแลป, กราฟลูกตุ้ม g, วงจร POE) + โซนสี → ผู้ใช้: "เหมือนนำเสนอน้ำ ๆ เกินไป"
- v3 (`_preview/index-content.html`): รายการแลป 70 + Demo 48 แบ่งโซนสีตามบท มีค้นหา → ผู้ใช้ให้ดู PhET เป็นตัวอย่าง
- ดู PhET + Brilliant → **v4 (`_preview/index-v4.html`)**: หัวหน้าสั้น (ปุ่ม นักเรียน/ครู + ภาพหน้าจอจริง 3 แลป) · ตัวเลข · การ์ดวิชาพาสเทล 5 ใบ · การ์ดระดับชั้น ม.4/ม.5/ม.6/มหาวิทยาลัย (ลิงก์ virtual-lab.html?level=) · แลปแนะนำ 8 + Demo 6 พร้อมภาพหน้าจอจริง · ส่วนครู + สมัครสมาชิก
  - ภาพหน้าจอ: `assets/thumbs/` 14 ไฟล์ (puppeteer จาก localhost) — Demo ที่ถ่ายแล้วว่าง/ติดหน้าคำถามเปลี่ยนเป็นสนามแม่เหล็ก คลื่นกล กาแล็กซี วงโคจร
  - พบว่า Demo/index.html ลิงก์ Demo แค่ 27 จาก 48 ไฟล์จริง (ดาราศาสตร์ 14 เรื่องไม่อยู่ในหน้ารวม)
- ผู้ใช้ถามฟอนต์ที่ดีกว่า → ทำแถบเลือก 6 ชุดบนหน้า v4 → **ผู้ใช้เลือก B: IBM Plex Sans Thai (หัว) + IBM Plex Sans Thai Looped (เนื้อหา)** · ใส่เป็นค่าเริ่มต้นแล้ว เอาแถบเลือกออก

### ไฟล์ที่แก้
- ใหม่ (ยังไม่ commit): `_preview/index-redesign-v1.html`, `_preview/index-redesign.html`, `_preview/index-content.html`, `_preview/index-v4.html`, `assets/thumbs/*.jpg`
- `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ย้าย v4 ไปเป็น index.html จริง: ต่อ kp-auth/modal ล็อกอิน สมัครสมาชิก GA · ปรับ build_virtual_lab.py (เดิมเขียน QM:START/END ใน index.html) ให้สร้างตัวเลข/การ์ดจาก labs_data.py
- ถามผู้ใช้ว่าจะเปลี่ยนฟอนต์ในแลปทั้งหมดเป็นชุด B ด้วยหรือไม่
- ตัวสร้างหน้า v3/v4 อยู่ใน scratchpad ของ session นี้ (build_home_v4.py + home_v4_template.html)

## [2026-09-15 19:10] — หน้าแรกใหม่ขึ้นจริง (build อัตโนมัติ) · Demo/index ครบ 48 · ฟอนต์ IBM Plex ทั้งเว็บ · Opus 5

### ทำอะไรไปบ้าง
- ผู้ใช้ตอบ "โอเคครับ" ต่อข้อเสนอ 3 ข้อ (ย้าย v4 เป็นหน้าแรก · เปลี่ยนฟอนต์ทั้งเว็บ · แก้ Demo/index)
- **Demo/index.html**: เดิมลิงก์ 27 เรื่อง (ลิงก์ SHM เสีย 1) → ครบ 48 เรื่อง: เพิ่มคลื่น 5 (แยกคลื่นผิวน้ำ), แสง 1, แม่เหล็ก 1, ดาราศาสตร์ 14 (ดวงอาทิตย์/ดาวฤกษ์/เอกภพ) · แก้ SHM → SHM01 · ตัวเลขหัวหน้า 48 · เมนู Collections → Virtual Lab
- **index.html ใหม่** = v4 แบบ PhET: สร้างด้วย `_admin/build_home.py` จาก `_admin/home_template.html` (build_virtual_lab.py เรียกแทน write_quickmenu เดิม)
  - ย้ายจากหน้าเดิม: ปุ่ม `#kp-login-btn` + `#kp-user-menu` (โปรไฟล์/ออก) · CSS โปรไฟล์/โมดัล (ตรึงสีมืดในโมดัล) · `#kp-auth-modal` + Firebase + kp-auth.js · KP-DOMAIN-PROTECTION · GA
  - ปุ่มสมัครสมาชิกเรียก `showModal('register')` · header ใช้ class `topbar` (protect ไม่ใส่ KP topbar ซ้ำ)
  - ใส่จุดปลายทาง `#collections #vpl #about #why #early-access #contact` ให้ลิงก์ในเมนูแลปเดิม (index.html#about ฯลฯ ~480 ลิงก์) ยังใช้ได้
  - ตัดออก: Early Access (Google Form), pricing, canvas 53 ตัว · ขนาด 251 KB → ~50 KB
  - **ตรวจ**: showModal/kpLogout/showProfile มี · โมดัลเปิดได้ ตัวหนังสืออ่านได้ · ลิงก์ในหน้าไม่เสีย ภาพครบ · มือถือ 375 px ไม่ล้น ปุ่มเข้าสู่ระบบอยู่ในจอ · ไม่มี console error
- **ฟอนต์ชุด B ทั้งเว็บ** (`_admin/switch_font_plex.py`): วัดความกว้างก่อน — Plex Sans Thai กว้างกว่า Sarabun ~1–2% · Looped ~8.5% → CSS ใช้ `IBM Plex Sans Thai Looped,IBM Plex Sans Thai` · ข้อความใน canvas/SVG ใช้ `IBM Plex Sans Thai` (ไม่ให้ป้ายในแคนวาสล้น) · ลิงก์ Google Fonts เปลี่ยนเป็น Plex 300–700
  - 149 ไฟล์ (VPL01/02/03, Demo, หน้ารวม, `_shared/kp-mobile-panel.js`, `_shared/watermark.js`, `protect_new_file.py` TOPBAR_CSS, `build_virtual_lab.py`) · rebuild virtual-lab.html + library.html · ลบชื่อเพี้ยน "TH … New" จาก fallback `TH Sarabun New` (112 จุด)
  - **ตรวจ**: เหลือคำว่า Sarabun 0 ไฟล์ (ไม่นับ _preview/_marketing) · node --check สคริปต์ inline 656 ชุด ผ่านทั้งหมด · Lab 55/62 และ virtual-lab.html โหลด Plex แสดงผลปกติ ป้ายในแคนวาสไม่ล้น
- CLAUDE.md: อัปเดตคำอธิบาย index.html (generate), เลิก QM, ฟอนต์ใหม่

### ไฟล์ที่แก้
- ใหม่: `_admin/home_template.html`, `_admin/build_home.py`, `_admin/switch_font_plex.py`, `assets/thumbs/*.jpg` (14)
- `index.html` (สร้างใหม่ทั้งหน้า), `Demo/index.html`, `_admin/build_virtual_lab.py`, `CLAUDE.md`, ~149 ไฟล์ HTML/JS (ฟอนต์), `SESSION_LOG.md`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ commit / ยังไม่ขึ้นเว็บ · `_preview/` เป็นต้นแบบ ไม่ต้อง commit
- หน้ารวมอื่น (virtual-lab.html, library.html, Demo/index.html) ยังเป็นธีมมืดแบบเดิม — ถ้าผู้ใช้อยากให้เข้ากับหน้าแรกใหม่ ต้องปรับต่อ

## [2026-09-15 19:40] — deploy หน้าแรกใหม่ + ฟอนต์ IBM Plex + Demo/index ครบ 48

### ทำอะไรไปบ้าง
- ภาพ hero บนหน้าแรกเพิ่ม onerror (ถ้าโหลดภาพไม่ได้จะไม่โชว์ alt text ทับกรอบ)
- commit + push main (ไม่รวม `_preview/`)

### ไฟล์ที่แก้
- `_admin/build_home.py` — hero img alt="" + onerror · `index.html` build ใหม่

### ค้างไว้ที่ไหน / ต้องทำต่อ
- virtual-lab.html / library.html / Demo/index.html ยังธีมมืดเดิม (เสนอปรับให้เข้ากับหน้าแรก)

## [2026-09-15 20:05] — แถบตัวกรอง virtual-lab.html พับเก็บได้บนมือถือ/ไอแพด

### ทำอะไรไปบ้าง
- จอ ≤1024px: แถบตัวกรองเหลือแถวเดียว (ช่องค้นหา + ปุ่ม "⚙️ ตัวกรอง · สรุปตัวกรองที่เลือก ▼") กดเพื่อกางกลุ่ม/บทเรียน/ระดับ (ชิปเลื่อนแนวนอน) · เลือกกลุ่ม/บทเรียนแล้วพับเอง · กางอยู่แล้วเลื่อนหน้า >220px พับเอง · แถบ nav "KPScience ← กลับหน้าหลัก" ไม่ sticky บนจอเล็ก
- จอคอมใหญ่: หน้าตาเดิม (ช่องค้นหา + ตัวนับย้ายขึ้นแถวบนสุด)
- เดิมบนมือถือแถบสูง ~600px ติดค้างบังจอ → ตอนพับสูง 56px

### ไฟล์ที่แก้
- `_admin/build_virtual_lab.py` — CSS/HTML/JS แถบตัวกรอง · build ใหม่ `virtual-lab.html`, `library.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy (รอ "อัพขึ้นเว็บ")

## [2026-09-15 20:25] — แถบตัวกรอง virtual-lab.html เลื่อนเก็บได้

### ทำอะไรไปบ้าง
- เลื่อนหน้าลง (พ้น hero) → แถบตัวกรองเลื่อนเก็บขึ้นไปพ้นจอ · เลื่อนขึ้น → กลับมา · ปัดแถบขึ้น (touch) ก็เก็บได้
- ตอนเก็บ มีปุ่มลอยเล็ก "🔍 ค้นหา · ตัวกรอง ▾" มุมขวาบน กดเรียกแถบกลับ · ขณะพิมพ์ในช่องค้นหาแถบไม่หนี
- ใช้ทุกขนาดจอ (คอมก็เก็บได้)

### ไฟล์ที่แก้
- `_admin/build_virtual_lab.py` — CSS .fhide/.fpeek + JS showFbar/scroll/swipe · build `virtual-lab.html`, `library.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy (รอ "อัพขึ้นเว็บ")

## [2026-09-15 20:40] — virtual-lab.html: กดตัวกรองแล้วเลื่อนไปที่ผลลัพธ์ทุกครั้ง

### ทำอะไรไปบ้าง
- bug: กดชิประดับชั้น (ม.4/ม.5/ม.6/ทั้งหมด) และลิงก์ `?level=m6` จากการ์ดระดับชั้นบนหน้าแรก → หน้าไม่เลื่อน ผลลัพธ์อยู่ใต้ hero นอกจอ
- แก้: เลือกตัวกรองอะไรก็ตาม แถบพับ + เลื่อนลงไปที่หัวกลุ่มแรกที่เหลือ (กลุ่ม/บทเรียนยังเลื่อนไปหัวข้อนั้นเหมือนเดิม)
- มือถือ: หัวกลุ่มเว้นระยะจากบน 104px ไม่ให้ปุ่มลอยบัง

### ไฟล์ที่แก้
- `_admin/build_virtual_lab.py` — setFilter() · build `virtual-lab.html`, `library.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy (รอ "อัพขึ้นเว็บ")

## [2026-09-15 21:30] — ชุดแลปงานและพลังงาน: Lab 70–71 (3D)

### ทำอะไรไปบ้าง
- เจ้าของอนุมัติรายการแลปงานและพลังงาน 70–78 (ต้องเป็นแลปวัดค่าจริง ไม่ใช่ชุดสาธิต) · ให้ทำ 70–71 ก่อนแล้วส่งดู
- **Lab 70 งานกับแรงและระยะทาง** — ส่วน A ชั่ง/ยกกล่องช้า ๆ (W = F·h) · ส่วน B ลากกล่องด้วยความเร็วคงตัวที่ θ = 0–60° อ่านตาชั่งสปริง (0–30 N ช่องละ 0.2 N เข็มสั่น) + ไม้เมตร · ตาราง/กราฟ W–s, F cosθ–θ, W–h จากค่าที่นักเรียนกรอก · ปริศนา μk ของโต๊ะ (M, μk สุ่ม)
- **Lab 71 ค่าคงตัวสปริงและงานยืดสปริง** — สปริง A/B (k ซ่อน) แขวนมวลทีละ 50 g อ่านขีดชี้ในแว่นขยาย · กราฟ F–x ผ่านจุดกำเนิด (k) · พื้นที่ใต้กราฟ = ½kx² · กราฟ W–x² · ขีดจำกัดสภาพยืดหยุ่น (ยืดค้าง) · ปริศนา: มวลก้อนปริศนา + ตรวจค่า k · ปรับมุมกล้องเริ่มต้นให้เห็นสปริงชัด
- ทั้งสองแลป: 🧭 ขั้นตอน, ฟอร์มบันทึกใต้ภาพ + ปุ่มเดียว, ปุ่มแตะใน canvas, ท่าทางนิ้ว 3D, kp-mobile-panel, ↺ รีเซตค่า, โหมดวัดเองไม่เฉลย · ตรวจด้วย puppeteer: fitted k/μk ตรงค่าซ่อนภายในความคลาดเคลื่อนการอ่าน

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/70. work-force-distance.html` (ใหม่) · `Virtual Physics Lab 02/71. spring-constant-work.html` (ใหม่)
- `_admin/labs_data.py` (topic energy) · `kp-auth.js` + `_admin/admin.html` (VLAB_SERIES, LAB_LIST) · `virtual-physics-lab-02.html` (หมวด ⚡ งานและพลังงาน + preview vpl2-workdrag / vpl2-spring, hero 45)
- build: `virtual-lab.html`, `library.html`, `index.html` (72 แลป), admin LAB_META

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอเจ้าของลอง 70–71 · ถัดไป 72 งาน–พลังงานจลน์ (รางลม+ประตูแสง) … 78
- ยังไม่ deploy (รอ "อัพขึ้นเว็บ")

## [2026-09-16 09:10] — deploy: Lab 70–71 + แถบตัวกรองพับ/เลื่อนเก็บ

### ทำอะไรไปบ้าง
- commit + push main (ไม่รวม `_preview/`) · ตรวจเว็บจริง: virtual-lab.html มี fpeek/fhide แล้ว · Lab 70, 71 โหลด 200
- ตรวจจอ 375px บนเว็บจริง: แถบตัวกรองสูง 56px · เลื่อนลงแล้วเก็บขึ้น (fbar fhide) และปุ่มลอยขึ้นแทน

### ไฟล์ที่แก้
- commit ed23925 — 11 ไฟล์ (Lab 70, 71 ใหม่ + labs_data/kp-auth/admin/virtual-physics-lab-02 + หน้ารวมที่ build)

## [2026-09-16 12:10] — Lab 70 ลากด้วยนิ้ว/เมาส์ + สเกล 3D · Lab 71 เหลือแค่ 3D

### ทำอะไรไปบ้าง
- **Lab 70**: ลากกล่องเองได้ด้วยเมาส์/นิ้ว ทั้งในภาพ 3D (raycast โดนกล่อง/เชือกจึงลาก ไม่โดน = หมุนกล้องเหมือนเดิม) และภาพ 2 มิติ · ค่าตาชั่งคิดจาก F = M(a + μk g)/(cosθ + μk sinθ) จากความเร็ว/ความเร่งของนิ้วจริง (กรองสัญญาณ τ=0.12 s, |a| ≤ 6) + เข็มสั่น ±0.1 N + พีคแรงเสียดทานสถิตตอนเริ่มเคลื่อน · ลากถอยหลังไม่ได้ (เชือกดึงทางเดียว) · เพิ่มแถบบอกความเร็ว "✓ สม่ำเสมอ / ⚠️ ไม่สม่ำเสมอ" ใต้แว่นขยายตาชั่ง · ปุ่ม ▶ ลาก เดิมยังใช้ได้
- **Lab 70 สเกล 3D**: ไม้เมตร (ขีด 1 mm/5 mm/1 cm/5 cm/10 cm + เลข), ไม้บรรทัดตั้งส่วน A, หน้าปัดตาชั่งสปริง (ช่องละ 0.2 N) ทำด้วย CanvasTexture ความละเอียดสูง · แก้บั๊กเดิม: สเกลตาชั่งอยู่คนละด้านกับเข็มและเลขถูกตัด · ขีดชี้แดงที่ขอบหน้ากล่อง/ใต้กล่องตรงตำแหน่งจริง (คลาด 0.00 cm)
- **Lab 71**: ตัดภาพ 2 มิติทั้งหมด (side view + แว่นขยาย + แถบปุ่มใน canvas) · ไม้เมตรใน 3D เป็น CanvasTexture 512×8192 อ่าน mm ได้ · เพิ่มมุมมอง 🔍 ซูมอ่านค่า (ตามขีดชี้) · ย้ายปุ่ม ＋50 g/－50 g/✋/❓/📝 มาเป็นแถบ HTML ใต้ภาพ 3D · อุดช่องค่าเฉลย k ที่ค้างใน DOM หลังสลับกลับโหมดวัดเอง (ล้าง #autoGrid)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/70. work-force-distance.html` · `Virtual Physics Lab 02/71. spring-constant-work.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy (รอ "อัพขึ้นเว็บ") · ถัดไป Lab 72 งาน–พลังงานจลน์
- Lab 70 มี window.KP70() (คืนเฉพาะค่าที่เห็นบนจอ ไม่มี M/μk) ไว้ให้สคริปต์ทดสอบ

## [2026-09-16 12:40] — Lab 70: ลากกล่องได้ทันทีโดยไม่ต้องเลือกส่วน B ก่อน

### ทำอะไรไปบ้าง
- เจ้าของลากแล้วไม่ขยับ เพราะ hdStart/hitBox3D/hitBox2D บังคับ part==='B' แต่ตอนเปิดหน้า part = null
- แก้: ถ้ายังไม่ได้เลือกส่วน แล้วลากที่กล่อง → setPart('B') ให้อัตโนมัติแล้วลากต่อ · ข้อความ "🖐 ลากกล่องด้วยนิ้ว/เมาส์ได้ที่นี่" แสดงตั้งแต่ยังไม่เลือกส่วน
- ทดสอบจาก file:// ทั้งเมาส์ (เลื่อน 38 cm) และนิ้วบนจอ 375px (เลื่อน 45 cm) จากหน้าที่เพิ่งเปิด ไม่มี error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/70. work-force-distance.html`

## [2026-09-16 13:05] — Lab 70: โหมด "🖐 ลากกล่อง" ลากที่ไหนก็ได้ในภาพ

### ทำอะไรไปบ้าง
- เจ้าของยังลากไม่ได้ (เดิมต้องกดโดนตัวกล่องพอดี ซึ่งเล็กมากบนมือถือ)
- เพิ่ม `handMode` (ค่าเริ่มต้น = เปิด) + ปุ่มสลับ `#handBtn` "🖐 ลากกล่อง / 🔄 หมุนภาพ" ในแถวปุ่มมุมมอง
  - โหมดลากกล่อง: ลากที่ใดก็ได้ในภาพ 3D และภาพด้านข้าง 2 มิติ = เลื่อนกล่อง (ไม่กระโดด เพราะจับ offset ไว้) · 2 นิ้ว/ล้อเมาส์ยังซูม-เลื่อนภาพได้
  - โหมดหมุนภาพ: กลับไปหมุนกล้องเหมือนเดิม · ส่วน A (ยกกล่อง) หมุนได้เสมอ
- ทดสอบ file:// จากหน้าที่เพิ่งเปิด: เมาส์ลากจากจุดว่าง 26 cm · นิ้วบนจอ 375px 34 cm · สลับเป็นหมุนภาพแล้วกล้องหมุน กล่องนิ่ง · ส่วน A หมุนได้ · ไม่มี error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/70. work-force-distance.html`

## [2026-09-16 13:30] — Lab 70: ลากกล่องเมื่อกดใกล้กล่อง · ที่ว่าง = หมุนภาพ

### ทำอะไรไปบ้าง
- โหมดลากทั้งภาพ (ค่าเริ่มต้นก่อนหน้า) ทำให้หมุนภาพ 3D ไม่ได้เลย — เจ้าของแจ้งว่ากดตรงไหนก็กลายเป็นดึงกล่อง/ตาชั่ง
- เปลี่ยนค่าเริ่มต้นเป็น `handMode=false`: `hitBox3D()` เพิ่มการเผื่อระยะบนจอ (รัศมี ≥46px หรือ 12% ของด้านสั้น รอบกล่อง/ตะขอ/ตาชั่ง และ ≤28px รอบเส้นเชือก) → กดใกล้กล่องก็ลากได้ ไม่ต้องโดนเป๊ะ · กดที่ว่าง = หมุนภาพเหมือนเดิม
- ภาพ 2 มิติ: เผื่อขอบกล่อง 26px
- ปุ่ม `#handBtn` เหลือเป็นตัวเลือก "🖐 ลากกล่องทั้งภาพ" สำหรับคนที่ยังลากยาก
- ทดสอบ: desktop/mobile — กดบนกล่อง/ใกล้กล่อง = hit true ลากได้ 0.32/0.38 m · กดมุมบนขวาไกล ๆ = hit false กล้องหมุน az 0.42 → −0.16 กล่องนิ่ง

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/70. work-force-distance.html`

### [เพิ่ม 13:50] Lab 70 — ความหนืดตอนลาก
- เดิมกล่องกระโดดตามนิ้วทันที รู้สึกเร็วเกินจริง
- เพิ่ม `HD_LAG=0.30 s` (กล่องตามนิ้วแบบหน่วง) และ `HD_VMAX=0.20 m/s` (เพดานความเร็ว)
- ผล: ลากช้า ๆ ได้ ~8 cm/s (คุมความเร็วได้ตามจริง) · ลากเร็วหรือปัดแรงถูกจำกัดที่ 20 cm/s ไม่เหวี่ยงกล่อง

## [2026-09-16 15:20] — Lab 72–73 (งานและพลังงาน) + กติกาใหม่ "3D ล้วน"

### ทำอะไรไปบ้าง
- **Lab 72 งาน–พลังงานจลน์ (รางลม 3D)** — ลากโฟโตเกต 2 ตัวด้วยนิ้ว/เมาส์ อ่านตำแหน่งจากสเกลบนราง · เครื่องจับเวลา 2 ช่องในฉาก (ms) · v = การ์ด/เวลา · ตาราง ΔEk เทียบ W = Mg·s · กราฟ ΔEk–W, Δ(v²)–s, (Mg−Ma)–a หา m (ความชัน) และ f (จุดตัด) · ปริศนา: มวลรถ ±5%, แรงเสียดทาน ±35% · ตุ้มแขวน 10–60 g การ์ด 2.5/5/10 cm
- **Lab 73 อนุรักษ์พลังงานกล (รางโค้ง 3D)** — ลากลูกขึ้นราง อ่าน h จากสเกล mm · โฟโตเกต+เครื่องจับเวลา · กราฟ v²–h · ลูกตัน/กลวง/แผ่นเลื่อน (β = 2/5, 2/3, 0) · ปริศนา: g ของดาวปริศนา และทายว่าลูก X หรือ Y กลวง
- ทั้งคู่ **3D ล้วน** (ไม่มีภาพ 2 มิติ) ตามที่เจ้าของสั่ง · สเกลเป็น CanvasTexture ความละเอียดสูง · ลากมีความหนืด (lag 0.3 s + เพดานความเร็ว) · จับวัตถุได้ในรัศมี ≥46px · ปุ่มใต้ภาพ · โหมดวัดเองไม่เฉลย (ล้างออกจาก DOM ด้วย)
- ผลตรวจ: Lab 72 หามวลรถคลาด −1.1% ทั้ง 2 รอบ, ΔEk ตรงกับ W−f·s ภายใน 0.8% · Lab 73 ความชัน v²–h ตรงทฤษฎีภายใน 3.5%, g ดาวปริศนาคลาด 0.5–1%
- ลงทะเบียน: labs_data (74 แลป), kp-auth, admin LAB_LIST, หน้า VPL02 (หมวดงานและพลังงาน 4 การ์ด, hero 47) + preview renderer vpl2-airtrack / vpl2-ramp · build หน้ารวมใหม่

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/72. work-kinetic-energy.html`, `73. energy-conservation-ramp.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html`, build: `virtual-lab.html`, `library.html`, `index.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy (Lab 70–73 + แก้ต่าง ๆ รอ "อัพขึ้นเว็บ")
- รอเจ้าของตอบ: Lab 70 จะตัดแว่นขยาย 2 มิติอย่างเดียว หรือย้ายลูกศรแรงเข้า 3D แล้วตัดทั้งแผง
- ถัดไป Lab 74 ปืนสปริงยิงออกจากขอบโต๊ะ (½kx² = ½mv²)

## [2026-09-16 15:45] — deploy: Lab 70–73 ชุดงานและพลังงาน

### ทำอะไรไปบ้าง
- commit ddca168 (12 ไฟล์) + push main · ตรวจเว็บจริง: Lab 70/71/72/73 โหลด 200 · หน้า VPL02 มี lab-73
- ลากกล่องบนเว็บจริง (Lab 70): x 0.110 → 0.237 m, part เปลี่ยนเป็น B อัตโนมัติ, ไม่มี console error

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ถัดไป Lab 74 ปืนสปริงยิงจากขอบโต๊ะ (½kx² = ½mv²) แล้วไล่ถึง 78

## [2026-09-16 16:20] — ปุ่ม ✋ เลื่อนภาพ ในแลป 3D (70–73)

### ทำอะไรไปบ้าง
- เจ้าของแจ้งว่าเมาส์ลากได้แค่หมุนรอบจุดกลาง เลื่อนภาพขึ้น-ลง ซ้าย-ขวาไม่ได้ (เดิมต้อง Shift+ลาก หรือคลิกขวาลาก ซึ่งไม่มีใครรู้)
- เพิ่ม `panMode` + ปุ่ม `#panBtn` "✋ เลื่อนภาพ" ในแถวปุ่มมุมมองของ Lab 70–73: เปิดแล้วลาก (เมาส์/นิ้วเดียว) = เลื่อนภาพ · ปิดแล้วกลับไปหมุน/ลากวัตถุ · เพิ่มปุ่มกลางเมาส์ = เลื่อนภาพ · Shift/คลิกขวา/สองนิ้วยังใช้ได้
- ทดสอบ 4 แลป × (เมาส์/นิ้ว): เปิดโหมดแล้วลาก จุดมองเลื่อน 9.9–32.9 cm · ปิดโหมดแล้วลากกลับไปหมุน (az เปลี่ยน) · ไม่มี error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/70–73` (4 ไฟล์)

## [2026-09-16 17:10] — ปุ่ม ✋ เลื่อนภาพ ครบทุกแลป 3D (33 แลป)

### ทำอะไรไปบ้าง
- ขยายปุ่มเลื่อนภาพจาก 70–73 ไปยังแลป 3D ทั้งหมด
  - **62–69 + 70–73** (มี setupPointer/camPan): เพิ่ม `panMode` + ปุ่มในแถวปุ่มมุมมอง ลากด้วยเมาส์/นิ้วเดียว = เลื่อนภาพ, ปุ่มกลางเมาส์ = เลื่อนภาพ
  - **32B, 33B, 35, 36, 46–61, VPL03 Lab 1** (21 ไฟล์): แนบบล็อก "KP Pan Mode" ท้ายไฟล์ — สร้างปุ่มเองแล้วแทรกหน้าปุ่มมุมมองแรก · pan คำนวณจาก `orbit`/`cam` เอง (ไม่พึ่ง add-on ท่าทาง) · ดัก pointer/touch แบบ capture เฉพาะตอนเปิดโหมด · boot วนรอจนฉาก 3D พร้อม
- ตรวจ: 33 ไฟล์มีปุ่ม, inline script ผ่าน node --check ทั้งหมด, ทดสอบ pan ด้วยเมาส์และนิ้วในแลปตัวอย่าง (32B, 35, 46, 52, 55, 58, 60, 61, 66, VPL03 L1) จุดมองเลื่อน 4.6–18 cm และปิดโหมดแล้วกลับไปหมุนได้
- แก้ระหว่างทาง: บล็อกแรกไปตั้ง `curView='free'` ทำให้ Lab 55 error (`VIEWS[curView].follow`) → เอาออก

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/` 32B, 33B, 35, 36, 46–69 · `Virtual Physics Lab 03/1.` (รวม 70–73 ที่ทำก่อนหน้า)

## [2026-09-16 19:30] — Lab 74–75 (งานและพลังงาน) + แก้การ์ดซ้ำในหน้า VPL02

### ทำอะไรไปบ้าง
- **Lab 74 ปืนสปริงบนขอบโต๊ะ** — ลากลูกสูบอัดสปริง x (สเกลกระบอก mm) · ปรับความสูงโต๊ะ H ด้วยปลอกที่ขาโต๊ะ · ยิงแล้วอ่านระยะตก R จากสเกลบนพื้น (รอยกระแทกค้างไว้ ลบได้) · กราฟ v²–x², R–x, ½mv²–½kx² · ปริศนา: หา k ของสปริง A/B + โจทย์ทำนายระยะตกก่อนยิง · ตรวจ: k จากกราฟคลาด 1.3–2.9% (อคติ = ε ที่ซ่อนไว้), รอยตกตรงกับค่าคำนวณ 0.00 mm
- **Lab 75 งานของแรงเสียดทาน** — ตัวผลักความเร็วคงที่ (ปรับระดับ) · โฟโตเกต+เครื่องจับเวลาในฉาก หา v · อ่านตำแหน่งหยุดบนสเกล 0–150 cm (ขีด 1 mm) · เลือกผิว 4 แบบ + ผิวปริศนา · กราฟ v²–s ความชัน 2μkg · คำถามมวลไม่มีผลต่อระยะไถล (ทดสอบได้ 0.16% ต่างกัน) · ตรวจ: μk คลาดสูงสุด 2.5%
- ทั้งคู่ 3D ล้วน · ปุ่ม ✋ เลื่อนภาพ · ลากแบบมีความหนืด · ปุ่มใต้ภาพ · ไม่มี error
- **แก้บั๊กการลงทะเบียน**: สคริปต์ register รอบนี้เติม lab-72/73 ซ้ำเข้า labs_data และหน้า VPL02 → ลบรายการซ้ำ 2 รายการ, ลบการ์ดซ้ำ 2 ใบ, ลบ preview renderer ซ้ำ, นับ topic-count/hero ใหม่จากจำนวนการ์ดจริง (48 การ์ด) · รวมแลปทั้งเว็บ 76

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/74. spring-launcher-projectile.html`, `75. friction-work-stopping-distance.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

## [2026-09-17 09:30] — Lab 76–78 · ชุดงานและพลังงานครบ 70–78

### ทำอะไรไปบ้าง
- **Lab 76 กำลังและประสิทธิภาพของมอเตอร์** — มอเตอร์ม้วนเชือกยกตุ้ม 100–500 g · ลากขีดเริ่ม/ขีดหยุดกำหนดช่วงยก · นาฬิกาจับเวลา + โวลต์มิเตอร์/แอมมิเตอร์เข็มในฉาก (มี HOLD) · ปรับแรงดัน 3–12 V ด้วยการลากปุ่ม · P_out = mgh/t เทียบ P_in = VI · กราฟ η–m, P_out–m, I–m · ปริศนา: โหลดที่ η สูงสุด + กระแสไม่มีโหลด I₀ · ตรวจ: η พีคกลางช่วงจริง, I₀ คลาด 0.3–2.0%
- **Lab 77 เครื่องกลอย่างง่าย** — พื้นเอียง (ลากแม่แรงปรับมุม 10–42°) + รอกตรึง/รอกเคลื่อนที่/รอกพวง 4 เส้น · ลากตาชั่งสปริง 0–20 N (เข็มค้างค่าเฉลี่ยช่วงความเร็วคงตัว) · อ่านระยะบนสเกลราง + ความสูงจากเสาเลเซอร์ · MA · VR · η · กราฟ η–θ, F–sinθ, F/cosθ–tanθ · ปริศนา: μk (คลาด 0.2–1.1%) · มวลก้อนปริศนา (คลาด 0.01%) · η < 1 ทุกกรณี
- **Lab 78 ตุ้มตกตอกหมุด** — ลากตุ้ม 0.5/1.0/1.5 kg ขึ้นราง อ่าน h · ปล่อยตกตอกหมุดในดินน้ำมัน/ทราย/โฟม/ถาดปริศนา · อ่านความลึกบนสเกลข้างหมุด (0.5 mm) · mgh = F·d · กราฟ d–h หา F₀ (คลาด 0.3–2.0%) · โจทย์ทำนายก่อนตอก · ตอกซ้ำหมุดเดิมจมน้อยลงตามความลึก
- ลงทะเบียน 76–78: labs_data (79 แลป), kp-auth, admin LAB_LIST, หน้า VPL02 (หมวดงานและพลังงาน 9 การ์ด, hero 51) + preview renderer vpl2-motor/pulley/hammer · build หน้ารวมใหม่ · ตรวจไม่มีการ์ดซ้ำ preview วาดครบทุกตัว

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/76. motor-power-efficiency.html`, `77. simple-machines-incline-pulley.html`, `78. drop-hammer-pile-driver.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ชุดงานและพลังงาน 70–78 ครบตามรายการที่เจ้าของอนุมัติแล้ว
- ที่ยังค้างจาก audit เดิม: อัปเกรดแลปเก่า VPL01/VPL02 30–45 · เลขแลปซ้ำ 42–44 · แลปวงกลมข้อ 9–10 (VPL02 หรือ VPL03)

## [2026-09-17 10:40] — ปุ่ม 🐢 ปรับความเร็วการแสดงผล (17 แลป 3D)

### ทำอะไรไปบ้าง
- เจ้าของแจ้งว่าการเคลื่อนที่เร็วเกินจะดูทัน → เพิ่มปุ่มวนค่า `#spdBtn` ×1 → ×½ → ×¼ → ×⅒ ในแถวปุ่มมุมมอง (ข้าง ✋ เลื่อนภาพ) ของ Lab 62–78
- กลไก: loop คำนวณ dt จริงแล้วส่ง `simDt(dt)` เข้า tick — คูณ simSpeed · เวลาที่เครื่องมือวัดได้ไม่เปลี่ยน เพราะทั้งฟิสิกส์และนาฬิกาใช้ dt เดียวกัน · ขณะลากด้วยมือ (HD.on) ใช้เวลาจริงเพื่อให้วัตถุตามนิ้วทัน · แก้ loop สำรอง (กรณีไม่มี WebGL) ด้วย
- ทดสอบ Lab 73: ×1 ปล่อยลูกถึงโฟโตเกตใน 0.72 s เครื่องจับเวลาอ่าน 10.64 ms · ×¼ ใช้เวลาจริง 2.34 s (ช้าลง ~3.3 เท่า) เครื่องจับเวลาอ่าน 10.69 ms (เท่าเดิมในขอบเขต noise)
- inline script ทั้ง 17 ไฟล์ผ่าน node --check

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/62–78` (17 ไฟล์)

## [2026-09-17 11:20] — ปุ่ม 🐢 ความเร็ว ครบทุกแลป (79 แลป)

### ทำอะไรไปบ้าง
- สร้าง `_shared/kp-speed.js` — ชะลอ timestamp ของ requestAnimationFrame + performance.now() (นาฬิกาเสมือน) แล้วแทรกปุ่มเองข้างปุ่มมุมมอง หรือสร้างแถบใต้ canvas ถ้าไม่มีปุ่มมุมมอง · ข้ามไฟล์ที่มี setSimSpeed ของตัวเอง
- แทรก `<script src=".../_shared/kp-speed.js">` ให้แลป 62 ไฟล์ (VPL01 ทั้งหมด · VPL02 30–61 · VPL03) — Lab 62–78 ใช้ปุ่มในตัวเหมือนเดิม
- `_admin/protect_new_file.py` เพิ่มเช็ก SPEED → ไฟล์แลปใหม่จะได้สคริปต์นี้อัตโนมัติ · CLAUDE.md เพิ่มหัวข้ออธิบาย
- ทดสอบ: VPL01 Lab 11 รางลม, VPL02 Lab 31 ถังคลื่น, Lab 55, VPL03 Lab 1 → ปุ่มขึ้นและกดวนค่าได้ · นาฬิกาจำลองเดิน 250 ms ต่อ 1 วินาทีจริงเมื่อตั้ง ×¼ และกลับมา 1001 ms เมื่อตั้ง ×1 · ไม่มี error

### ไฟล์ที่แก้
- ใหม่ `_shared/kp-speed.js` · แลป 62 ไฟล์ใน VPL01/02/03 · `_admin/protect_new_file.py` · `CLAUDE.md`

## [2026-09-17 12:00] — โลโก้หน้าแรกให้ตรงกับโลโก้บนแถบเมนู

### ทำอะไรไปบ้าง
- `_admin/home_template.html`: `.brand-mark` เปลี่ยนเป็นไล่สี 135° #38bdf8 → #818cf8 ตัวอักษร KP หนา 900 สีเข้ม · ข้อความเป็น "KPScience" ติดกัน โดย KP สี accent และ Science สี --text (สลับตามธีมสว่าง/มืดเอง) เหมือน `.tb-logo` ในสคริปต์ protect
- build index.html ใหม่

### ไฟล์ที่แก้
- `_admin/home_template.html` · `index.html` (generate)

## [2026-09-17 22:06] — Lab 80–81 เริ่มชุดโมเมนตัมและการชน (3D ล้วน)

### ทำอะไรไปบ้าง
- เจ้าของอนุมัติชุดแลปโมเมนตัม 79–86 (79 การดล/แรงดล · 80 ชนติดกัน · 81 ชนยืดหยุ่น · 82 ดีดตัวแยก · 83 ชน 2 มิติโต๊ะลม · 84 ลูกตุ้มขีปนะ · 85 ลูกบอลกระดอน · 86 เปลนิวตัน) ให้เริ่ม 80–81 ก่อน · แลปที่เป็น 3D ให้ทำ 3D อย่างเดียว ไม่มี 2D
- **Lab 80 การชนแบบติดกัน** — รางลม 3D · เครื่องยิงสปริง (อัด 1.0/1.5/2.0 cm) ยิงรถ A ชนรถ B ที่จอดนิ่ง ติดกันด้วยตีนตุ๊กแก · ลากรถ B และโฟโตเกต 2 ตัวได้ · จอจับเวลา 4 ช่อง (เกตละ 2 ครั้ง) · รถ A 200/300/400 g · รถ B 200/300/400 g หรือรถปริศนา X (250–550 g) · ตาราง p ก่อน/หลัง, Ek หลัง/ก่อน เทียบ m_A/(m_A+m_B) · กราฟ p–p, Ek ratio, v₁/v₂ – m_B/m_A อ่านมวล X · โจทย์ทำนาย Ek เหลือ 33.3%
- **Lab 81 การชนแบบยืดหยุ่น** — เครื่องมือชุดเดียวกัน + กันชน 3 แบบ (แม่เหล็ก e 0.95–0.99 · สปริงแผ่น 0.76–0.86 · ยางปริศนา Y 0.45–0.70) · กรอกทิศรถ A หลังชน (วิ่งต่อ = เกต 2 ครั้งที่ 2 / กระดอน = เกต 1 ครั้งที่ 2 / หยุด) · ตาราง v มีเครื่องหมาย, p, Ek, e · กราฟ p–p, (v_B′−v_A′)–v₁ ความชัน = e, v_B′/v₁ – m_A/(m_A+m_B) ความชัน 1+e · ตรวจ e ของยาง Y (±0.04) และมวล X (±5%)
- ฟิสิกส์: จำลองทั้งการยิงล่วงหน้าทีละ 0.5 ms (ความหน่วงราง 0.0004–0.0008 m/s² · ตัวรับรถปลายราง) · หาเวลาการ์ดตัดลำแสงแบบประมาณค่าในช่วง
- ผลตรวจ: Lab 80 p หลัง/ก่อน 99.4–99.8%, มวล X คลาด 0.3–4.5% (ยิงช้า + รถหนักคลาดมากสุด) · Lab 81 เฉลี่ย e 0.963/0.780/0.651 เทียบจริง 0.957/0.770/0.644, มวล X 290 vs 286 g · โหมดวัดเองไม่มีค่าเฉลยใน DOM · มือถือ 375 px ไม่มี scroll แนวนอน
- ลงทะเบียน: labs_data (topic ใหม่ `momentum` 💥 โมเมนตัมและการชน ในกลุ่มกลศาสตร์ · รวม 81 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดใหม่ 2 การ์ด + preview vpl2-collide / vpl2-elastic · hero 53) · build หน้ารวมใหม่ · ตรวจไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/80. momentum-inelastic-collision.html`, `81. momentum-elastic-collision.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy — รอเจ้าของดู 80–81 แล้วสั่ง "อัพขึ้นเว็บ"
- ถัดไปในชุดโมเมนตัม: 79 การดล (เซนเซอร์แรง F–t) · 84 ลูกตุ้มขีปนะ · 82 · 83 · 85 · 86

### หมายเหตุ
- รถ A ที่หลังชนช้ากว่า 3.5% ของ v₁ ถือว่า “เกือบหยุด” (บันทึกได้ v_A′ = 0) · ถ้าเร็วกว่านั้นแต่การ์ดผ่านเกตไม่เต็มแผ่น ระบบไม่ให้บันทึกและบอกให้เลื่อนเกต/อัดสปริงเพิ่ม
- ควรทำแลปทีละแชต: ไฟล์ลงทะเบียน (labs_data, kp-auth, admin, หน้า VPL02) และ build ตีกันได้ถ้าสองแชตแก้พร้อมกัน

## [2026-09-17 22:40] — Lab 80 เพิ่มสวิตช์กันชน ตีนตุ๊กแก ↔ แม่เหล็ก

### ทำอะไรไปบ้าง
- เจ้าของขอให้ Lab 80 สลับเป็นการชนแบบยืดหยุ่นได้ → เพิ่มกันชน 2 แบบ: 🔗 ตีนตุ๊กแก (ติดกัน, e = 0) · 🧲 แม่เหล็ก (แยกกัน, e สุ่ม 0.95–0.99 ต่อการเปิดหน้า) · ปุ่มในแผงและแถบปุ่มใต้ภาพ (แทนปุ่มสปริง ซึ่งยังเลือกได้ในแผง) · ภาพ 3D เปลี่ยนแผ่นตีนตุ๊กแก/จานแม่เหล็กตามที่เลือก
- โหมดแม่เหล็ก: ฟอร์มมีช่อง ⑥ ทิศรถ A หลังชน (วิ่งต่อ/กระดอน/หยุด) และ ⑦ t_A · ตารางมีคอลัมน์กันชน, v_A′ มีเครื่องหมาย, e · กราฟ p–p และ Ek หลัง/ก่อน แสดงทั้งสองแบบ (วงกลม = ติดกัน, สี่เหลี่ยม = แม่เหล็ก) · กราฟ v₁/v₂ ใช้เฉพาะแถวติดกัน · m_X จากแถวแม่เหล็กใช้ m_A(v₁ − v_A′)/v₂
- คำแนะนำ 🧭 เพิ่มขั้น ⑧ ให้ลองแม่เหล็กอย่างน้อย 2 แถว · แท็บวิธีการ/ทฤษฎีเพิ่มหัวข้อกันชนแม่เหล็ก
- ผลตรวจ: ติดกัน Ek เหลือ 49.7/39.7/33.1% (ทฤษฎี 50/40/33.3) · แม่เหล็ก Ek 97.6–99.6%, e เฉลี่ย 0.991 (จริง 0.986) · p หลัง/ก่อน 99.1–99.9% · มวล X 522–526 g (จริง 521) · ไม่มี error · ไม่มีค่าเฉลยใน DOM โหมดวัดเอง
- แก้คำอธิบาย Lab 80 ใน labs_data และการ์ดหน้า VPL02 แล้ว build ใหม่

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/80. momentum-inelastic-collision.html` · `_admin/labs_data.py` · `virtual-physics-lab-02.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy 80–81

## [2026-09-17 23:10] — ปุ่ม ⚙️ ตั้งค่า / 📊 ผล บนภาพ 3D เมื่อจอแคบ (ทดลองใน Lab 80–81)

### ทำอะไรไปบ้าง
- เจ้าของอยากให้แผงขวากลายเป็นปุ่มตั้งค่าเมื่อจอแคบ ภาพ 3D จะได้เต็มจอ และกดได้ทันทีไม่ต้องเลื่อนลง
- `_shared/kp-mobile-panel.js` เพิ่มตัวเลือก opt-in (แลปอื่นไม่เปลี่ยน):
  - `canvasBtn:true` → ปุ่มลอย ⚙️ ตั้งค่า / 📊 ผล ที่มุมขวาบนของภาพหลัก (กดแล้วไม่หมุนกล้อง) · แถบปุ่มมุมมองเว้นที่ให้ไม่ทับกัน
  - `bp` > 900 และจอกว้างกว่า 900 px → แผงเลื่อนออกจากขอบขวาเป็น drawer กว้าง 390 px แทนแผ่นจากขอบล่าง · ตาราง `.sim-layout` เหลือคอลัมน์เดียว ภาพ 3D เต็มความกว้าง
- Lab 80 และ 81 ตั้ง `window.KP_MPANEL={bp:1280,canvasBtn:true}` → จอ ≤ 1280 px ซ่อนแผงขวา ใช้ปุ่มบนภาพแทน
- ทดสอบ: 1100×760 ภาพกว้าง 1074 px, กด ⚙️ แล้ว drawer เปิดจากขวา กล้องไม่หมุน · 1400 px แผงขวากลับที่เดิม ปุ่มลอยซ่อน · 375 px ปุ่มลอยไม่ทับปุ่มมุมมอง แผ่นล่างทำงานเหมือนเดิม

### ไฟล์ที่แก้
- `_shared/kp-mobile-panel.js` · `Virtual Physics Lab 02/80. …html` · `81. …html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- รอเจ้าของลองดู ถ้าชอบ ขยาย `{bp:1280,canvasBtn:true}` ไปแลปอื่น (อย่างน้อยแลป 3D ทั้งหมด)
- ยังไม่ deploy 80–81

## [2026-09-17 23:40] — แถบเครื่องมือเหนือภาพ 3D แทนปุ่มลอยทับภาพ (Lab 80–81)

### ทำอะไรไปบ้าง
- เจ้าของแจ้งว่าปุ่มมุมมอง + ⚙️/📊 ที่ลอยบนภาพบังอุปกรณ์ → ย้ายทั้งหมดไปไว้ในแถบ `#viewBar` เหนือภาพ 3D (นอกกรอบ canvas)
- `_shared/kp-mobile-panel.js` เพิ่มตัวเลือก `btnBar:'#viewBar'` → ใส่ปุ่ม ⚙️ ตั้งค่า / 📊 ผล ท้ายแถบเครื่องมือแทนการลอยทับภาพ
- จอ ≤ 900 px: ปุ่มมุมมองเป็นแถวเดียวปัดซ้าย-ขวาได้ ↺ รีเซตค่า อยู่หน้าสุด · จอ ≤ 560 px: แถวที่ 2 เป็น ⚙️/📊 เต็มความกว้าง
- ผล: แถบสูง 54 px ที่ 1100 px (แถวเดียว) · 95 px บนมือถือ 375 px (เดิม 181 px) · ไม่มีปุ่มใดทับภาพ 3D · ไม่มี scroll แนวนอน · ไม่มี error

### ไฟล์ที่แก้
- `_shared/kp-mobile-panel.js` · `Virtual Physics Lab 02/80. …html` · `81. …html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ถ้าเจ้าของชอบ: ใช้แถบเครื่องมือ + `{bp:1280,canvasBtn:true,btnBar:'#viewBar'}` กับแลป 3D อื่น
- ยังไม่ deploy 80–81

## [2026-09-17 23:55] — ปุ่ม ⚙️ ตั้งค่า แสดงเฉพาะจอเล็ก (Lab 80–81)

### ทำอะไรไปบ้าง
- เจ้าของต้องการ: จอเล็กใช้ปุ่มตั้งค่า · จอใหญ่แสดงแผงด้านข้างตามปกติ → เอา `bp:1280` ออก ใช้ค่ามาตรฐาน 900 px (`KP_MPANEL={canvasBtn:true,btnBar:'#viewBar'}`)
- ตรวจ: 1100 px แผงขวาแสดง ปุ่ม ⚙️/📊 ซ่อน · 860 px แผงซ่อน ปุ่ม ⚙️/📊 แสดงในแถบเหนือภาพ

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/80. …html` · `81. …html`

## [2026-09-18 00:15] — จัดปุ่มบนมือถือใหม่: แถบบน = รีเซต/ตั้งค่า/ผล · ความเร็ว+มุมมองอยู่บนภาพ (Lab 80–81)

### ทำอะไรไปบ้าง
- ตามที่เจ้าของสั่ง: จอ ≤ 900 px แถบเหนือภาพ 3D มี ↺ รีเซตค่า · ⚙️ ตั้งค่า · 📊 ผล แถวเดียว (สูง 55 px) · ปุ่ม 🐢 ความเร็ว, ✋ เลื่อนภาพ และปุ่มมุมมอง กลับไปอยู่บนภาพ 3D เป็นแถวเดียวปัดซ้าย-ขวาได้ที่ขอบล่าง (สูง 31 px)
- จอ > 900 px: ไม่มีแถบบน · ปุ่มความเร็ว/มุมมอง/รีเซตอยู่มุมล่างซ้ายของภาพตามเดิม · แผงขวาแสดงปกติ
- มีปุ่ม ↺ รีเซตค่า 2 ปุ่ม (ในแถบบน และบนภาพ) CSS ซ่อนตามขนาดจอ

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/80. …html` · `81. …html`

## [2026-09-18 00:25] — เอาแถบปุ่มด้านบนออก (Lab 80–81)

### ทำอะไรไปบ้าง
- เจ้าของบอกว่าปุ่ม ⚙️ ตั้งค่า / 📊 ผล มีที่แถบขอบล่างของจออยู่แล้ว → ลบแถบ `#viewBar` และ config `KP_MPANEL` ออกจาก Lab 80–81 (ใช้ค่ามาตรฐานของ kp-mobile-panel.js)
- ปุ่มบนภาพ 3D: จอกว้างอยู่มุมล่างซ้ายเหมือนเดิม · จอ ≤ 900 px เป็นแถวเดียวปัดซ้าย-ขวาได้ ↺ รีเซตค่า อยู่หน้าสุด
- ตัวเลือก `canvasBtn` / `btnBar` / drawer ใน `_shared/kp-mobile-panel.js` ยังอยู่ (ปิดไว้เป็นค่าเริ่มต้น ไม่มีแลปไหนใช้)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/80. …html` · `81. …html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy 80–81

## [2026-09-18 00:40] — deploy: Lab 80–81 ชุดโมเมนตัม

### ทำอะไรไปบ้าง
- commit 241809c (11 ไฟล์) + push main · เว็บจริงอัปเดตภายใน ~45 วินาที
- ตรวจเว็บจริง: Lab 80, Lab 81, virtual-lab.html, kp-mobile-panel.js โหลด 200 · หน้า VPL02 มี lab-81 · ยิงรถด้วยกันชนแม่เหล็กบนเว็บจริงได้ผลครบ ไม่มี console error

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ถัดไปในชุดโมเมนตัม: 79 การดล (F–t) · 84 ลูกตุ้มขีปนะ · 82 · 83 · 85 · 86

## [2026-09-18 01:30] — Lab 79 การดลและแรงดล (เซนเซอร์แรง · 3D)

### ทำอะไรไปบ้าง
- **Lab 79** — รางลม + เครื่องยิงสปริง (ชุดเดียวกับ Lab 80) ยิงรถเข้าชนเซนเซอร์แรงที่ปลายรางขวา · โฟโตเกต 1 ตัว (ลากได้) จำเวลาได้ 2 ครั้ง: ขาไป / ขากลับหลังเด้ง
- **จอเครื่องบันทึกข้อมูลในฉาก 3D**: ช่องเวลาบังแสง 2 ช่อง + กราฟแรง–เวลา (1 ms ต่อจุด, 200 ms เต็มจอ ช่องละ 10 ms, เต็มสเกล 2/5/10/20 N อัตโนมัติ, ช่องละ 1/10) วาดสดขณะชน · ปุ่ม ∫ พื้นที่ แรเงาและแสดง ∫F dt · มุมมอง 📈 จอกราฟ
- กันชน 3 แบบ: 🔩 สปริงแข็ง (k≈1500, e≈0.86) · 🌀 สปริงนิ่ม (k≈300, e≈0.79) · 🟤 ดินน้ำมัน (แรงหนืด ไม่เด้ง) · รถ 200/300/400 g และรถปริศนา X (250–550 g)
- นักเรียนกรอก t₁ t₂ F_max Δt J → ตาราง v₁ v₂ (มีเครื่องหมาย) |Δv| |Δp| J/|Δp| F เฉลี่ย F_max/F เฉลี่ย m_X · กราฟ J–Δp, F_max–Δt, J–Δv (ความชัน = มวล) · ตรวจมวล X (±5%) + คำทำนาย Δt ×2 → F เฉลี่ย ×½
- บันทึกได้ทันทีเมื่อวัดครบ (รถยังวิ่งต่อในภาพจนหยุด) ไม่ต้องรอรถกลับถึงปลายราง
- ผลตรวจ: J/|Δp| 99.3–100.5% ทุกกันชน · ความชันกราฟ J–Δp = 1.001 · มวล X 487–496 g (จริง 486–494 ในสองรอบ) · F_max/F เฉลี่ยของสปริง ≈ 1.50–1.53 (ครึ่งไซน์ π/2) · ดินน้ำมันรถ 400 g ยิงช้า Δt 96 ms อยู่ในหน้าจอ · ไม่มี error · 375 px ไม่มี scroll แนวนอน
- ลงทะเบียน: labs_data (82 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดโมเมนตัม 3 การ์ด + preview vpl2-impulse · hero 54) · build ใหม่ · ไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/79. impulse-force-sensor.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy Lab 79
- ถัดไปในชุดโมเมนตัม: 84 ลูกตุ้มขีปนะ · 82 ดีดตัวแยก · 83 ชน 2 มิติ · 85 ลูกบอลกระดอน · 86 เปลนิวตัน

## [2026-09-18 02:40] — Lab 84 ลูกตุ้มขีปนะ (3D)

### ทำอะไรไปบ้าง
- **Lab 84** — ปืนสปริงบนโต๊ะ ตั้งระยะยิง ใกล้/กลาง/ไกล · ลูกเหล็ก 66.0 g · ลูกพลาสติก 16.0 g · ลูกปริศนา X (25–55 g) · ลูกตุ้ม M 250/350 g · L = 28.0 cm
- **ตอน ข ยิงเข้าลูกตุ้ม**: ลูกบอลฝังในถ้วย ลูกตุ้มแกว่งขึ้นดันเข็มชี้สีแดงค้างที่มุมสูงสุด · โปรแทรกเตอร์ขีดละ 0.5° (มุมมอง 📐) · v = (m+M)√(2gL(1−cos θ))/m
- **ตอน ก ยิงออกขอบโต๊ะ**: ลูกตุ้มถูกเกี่ยวขึ้นพ้นทาง · ลูกตกบนกระดาษคาร์บอนที่**ลากวางเองได้** (ตกนอกกระดาษ = ไม่มีรอย) · เทปวัดบนพื้น 0–400 cm ขีดละ 1 mm เริ่มที่ลูกดิ่งใต้ปากกระบอก · รอยล่าสุดมีวงแดง · ไม้บรรทัดตั้งที่มุมโต๊ะวัด H (เส้นแดงจากปากกระบอก) · ความสูงโต๊ะสุ่มต่อการเปิดหน้า
- ปืน: พลังงานคงที่ต่อระยะยิง + ลูกสูบ 50 g → ลูกเบาเร็วกว่า · แต่ละนัดแกว่ง ±1% · จุดหมุน/เข็มชี้เสียพลังงาน 1.2%
- ตาราง ① v = R√(g/2H) + ค่าเฉลี่ยต่อ (ลูก, ระยะ) · ตาราง ② h, V, v ลูกตุ้ม, v โพรเจกไทล์, อัตราส่วน, Ek หลัง/ก่อน เทียบ m/(m+M), m_X = MV/(v−V) · กราฟ v–v, Ek หลัง/ก่อน – m/(m+M), v/V − 1 – M (ความชัน 1/m) · ตรวจมวล X (±6%) + คำทำนาย Ek หาย 79.1%
- ผลตรวจ (จำลองนักเรียนอ่านมุมปัด 0.5°): v ลูกตุ้ม/v โพรเจกไทล์ 97.3–100.8% · Ek ratio/ทฤษฎี 0.95–1.02 · มวลจากกราฟ: เหล็ก 65.8 g (66.0) พลาสติก 16.0 g (16.0) · มวล X เฉลี่ย 44.1 g (จริง 44.2) · ไม่มี error · 375 px ไม่มี scroll แนวนอน
- แก้ระหว่างทำ: ไม้บรรทัดตั้งเดิมบังลูกตุ้ม → ย้ายไปมุมหน้าโต๊ะ · ขีดไม้บรรทัดย้ายไปขอบที่เส้นแดงแตะ · ซ่อนลูกบอลหลังตกไม่ให้บังรอย
- ลงทะเบียน: labs_data (83 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดโมเมนตัม 4 การ์ด + preview vpl2-ballistic · hero 55) · build ใหม่ · ไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/84. ballistic-pendulum.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy Lab 79 และ 84
- ถัดไปในชุดโมเมนตัม: 82 ดีดตัวแยก · 83 ชน 2 มิติบนโต๊ะลม · 85 ลูกบอลกระดอน · 86 เปลนิวตัน

## [2026-09-18 03:00] — Lab 84: ลูกบอลค้างที่จุดตก

### ทำอะไรไปบ้าง
- เจ้าของบอกว่าอ่านระยะตกยาก อยากให้ลูกเหล็กค้างที่จุดตก → หลังตก ลูกบอลวางนิ่งบนกระดาษ กึ่งกลางลูกอยู่ที่ R พอดี (ไม่หายแล้ว) จนกด ↩ บรรจุใหม่ · รอยคาร์บอน + วงแดงยังอยู่ใต้ลูก
- มุมมอง 🔍 จุดตกบนพื้น: ตามตำแหน่งลูกที่เพิ่งตก · มองเกือบตั้งฉาก (ลดพาราแลกซ์) · ซูมใกล้ขึ้น
- ข้อความคำแนะนำ/ฟอร์ม/วิธีทดลอง เปลี่ยนเป็น “อ่าน R ที่กึ่งกลางลูกบอลที่ค้างอยู่”
- ตรวจ: R = 173.5 cm ลูกอยู่ x = 173.5 cm บนพื้น ภาพอ่านได้ตรงขีด

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/84. ballistic-pendulum.html`

## [2026-09-18 03:15] — deploy: Lab 79 + 84 ชุดโมเมนตัม

### ทำอะไรไปบ้าง
- commit 3752a4d (10 ไฟล์) + push main · เว็บจริงอัปเดตภายใน ~45 วินาที
- ตรวจเว็บจริง: Lab 79, Lab 84, virtual-lab.html โหลด 200 · หน้า VPL02 มี lab-84 · Lab 84 ยิงออกขอบโต๊ะแล้วลูกค้างที่ R = 173.9 cm ตรงกับตำแหน่งลูก · Lab 79 ยิงชนเซนเซอร์วัดครบ J = 0.1839 N·s · ไม่มี console error

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ชุดโมเมนตัมบนเว็บแล้ว: 79 · 80 · 81 · 84 · ที่เหลือ: 82 ดีดตัวแยก · 83 ชน 2 มิติ · 85 ลูกบอลกระดอน · 86 เปลนิวตัน

## [2026-09-18 04:00] — Lab 82 การดีดตัวแยกจากกัน (3D)

### ทำอะไรไปบ้าง
- **Lab 82** — รางลม (ชุดเดียวกับ Lab 80) · รถ A (มีสปริงแผ่น + สลักสีแดง) กับรถ B จอดชิดกันกลางราง · **ลากรถคู่** และโฟโตเกตซ้าย/ขวาได้ · กด ▶ ปลดสลัก รถแยกไปคนละทาง · ตัวรับรถที่ปลายทั้งสองข้าง
- สปริงอัด 3 ระดับ ปล่อยพลังงานคงที่ต่อระดับ (≈ 20 / 45 / 80 mJ แกว่ง ±3% ต่อหน้า ±2% ต่อครั้ง เสีย 3%) · รถ A 200/300/400 g · รถ B 200/300/400 g หรือ X (250–550 g)
- กรอก t_A (เกต 1 ครั้งที่ 1) · t_B (เกต 2 ครั้งที่ 1) → ตาราง v_A (−), v_B (+), p_A, p_B, p_A + p_B, m_X · ตาราง ② |v_B|/|v_A| เทียบ m_A/m_B, Ek_A, Ek_B, Ek รวม, ส่วนแบ่งพลังงานของ A เทียบ m_B/(m_A+m_B) · กราฟ |p_B|–|p_A|, |v_B|/|v_A| – m_A/m_B (เส้นประม่วงของรถ X), Ek รวมต่อระดับสปริง · ตรวจมวล X (±5%) + คำทำนาย A ได้ Ek 66.7%
- บันทึกได้ทันทีเมื่อรถผ่านเกตครบ · ปุ่ม ↩ ตั้งรถใหม่ล้างจอจับเวลา
- ผลตรวจ: (p_A + p_B)/|p_A| อยู่ใน ±0.3% · |v_B|/|v_A| ÷ (m_A/m_B) = 0.999–1.003 · Ek รวมคงที่ต่อระดับ (18.5 / 44.3–45.3 / 76.2–78.5 mJ) · ส่วนแบ่งพลังงานตรงทฤษฎี · มวล X 384–385 g (จริง 385) · ไม่มี error · 375 px ไม่มี scroll แนวนอน
- ลงทะเบียน: labs_data (84 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดโมเมนตัม 5 การ์ด + preview vpl2-recoil · hero 56) · build ใหม่ · ไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/82. momentum-explosion-recoil.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy Lab 82
- ที่เหลือในชุดโมเมนตัม: 83 ชน 2 มิติบนโต๊ะลม · 85 ลูกบอลกระดอน · 86 เปลนิวตัน

## [2026-09-18 05:10] — Lab 83 การชนใน 2 มิติ: ภาพแฟลชบนโต๊ะลม (3D)

### ทำอะไรไปบ้าง
- **Lab 83** — โต๊ะลม 80 × 50 cm พื้นพิมพ์ตาราง 1 cm (เส้นหนาทุก 5 cm · ตัวเลขตามขอบ · พิกัด x,y ที่จุดตัดทุก 5 cm) · ลูกยางแบน A 150 g ยิงตามแนว y = 25 cm (แรงยิง เบา/กลาง/แรง) · **ลากลูกยาง B** ให้เยื้องแนว · B 150 g / 300 g / ปริศนา X (100–350 g) · ขอบแม่เหล็ก e ≈ 0.95 (ซ่อน)
- **ภาพแฟลชทุก 0.040 s พิมพ์ลงบนพื้นโต๊ะใน 3D** หลังยิง: กากบาทกลางลูกทุกภาพ + หมายเลข A1…, A′1…, B′1… (ป้ายวางตั้งฉากกับแนวเคลื่อนที่สลับข้าง) · มุมมอง 📸 ภาพแฟลช (มองจากบน · ซ่อนขาตั้งกล้องอัตโนมัติ) · ไฟแฟลชกะพริบตอนถ่าย
- กรอกการกระจัดใน 4 ช่วงแฟลช 5 ค่า (Δx_A, Δx_A′, Δy_A′, Δx_B′, Δy_B′) → ตาราง v, มุม, Σp_x, Σp_y, มุมแยก, Ek หลัง/ก่อน, m_X (แกน y และแกน x เฉลี่ย) · กราฟ: เวกเตอร์ p ต่อหัว-ท้าย (แถวล่าสุด), Σp หลัง – p ก่อน, มุมแยก – m_B/m_A · ตรวจมวล X (±6%) + คำทำนายมุมแยก 90°
- ผลตรวจ (จำลองอ่านคลาด ±1 mm): Σp_x/p 98–102% · Σp_y/p ±2% · มุมแยกมวลเท่ากัน 85–88° · B 300 g มุมแยก 123–133° · มวล X เฉลี่ย 332 g (จริง 339) · ไม่มี error · 375 px ไม่มี scroll แนวนอน
- แก้ระหว่างทำ: ขาตั้งกล้องบังมุมมองจากบน → ซ่อนเมื่อมองชันกว่า ~66° · พื้นขาวจนมองไม่เห็นตาราง → ลด emissive เพิ่มความเข้มเส้น · ป้ายหมายเลขซ้อนกัน → วางตั้งฉากกับแนวเคลื่อนที่
- ลงทะเบียน: labs_data (85 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดโมเมนตัม 6 การ์ด + preview vpl2-strobe2d · hero 57) · build ใหม่ · ไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/83. momentum-2d-collision-strobe.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy Lab 82 และ 83
- ที่เหลือในชุดโมเมนตัม: 85 ลูกบอลกระดอน · 86 เปลนิวตัน

## [2026-09-18 06:30] — Lab 83: เปลี่ยนเป็นวัดด้วยไม้บรรทัด + โปรแทรกเตอร์

### ทำอะไรไปบ้าง
- เจ้าของเลือกให้วัดด้วยไม้บรรทัดแทนอ่านพิกัดบนตาราง และถามว่าต้องวัดมุมไหม → ต้องวัด (โมเมนตัมเป็นเวกเตอร์) จึงเพิ่มโปรแทรกเตอร์คู่กัน
- พื้นโต๊ะไม่มีตารางแล้ว (เหลือจุดรูเบาะลมจาง ๆ และเส้นประแนวยิง) เหมือนภาพแฟลชจริง
- 📏 ไม้บรรทัดใส 30 cm ขีดละ 1 mm: ลากตัวไม้ = ย้าย · ลากจุดแดงที่ปลาย = หมุนรอบขีดศูนย์ · ปล่อยแล้วขีดศูนย์ดูดติดกากบาทจุดแฟลชที่ใกล้ที่สุด (≤ 0.8 cm)
- 📐 โปรแทรกเตอร์ใสเต็มวง 0° ถึง ±180° ขีดละ 1° (เหนือแนวยิง + · ใต้แนว −) เส้นฐานขนานทิศยิงเสมอ · ลากย้าย · จุดกลางดูดติดกากบาท · เต็มวงเพราะลูก B 300 g ทำให้ A กระดอนถอยหลัง (≈ −100°)
- ปุ่มมุมมอง 🔍 ไม้บรรทัด (ตามไม้บรรทัด มองจากบน) · 🧰 เรียกเครื่องมือมาที่นี่ (ย้ายเครื่องมือมากลางภาพที่ดูอยู่)
- ช่องกรอกใหม่: ② |d_A| · ③ |d_A′| ④ θ_A′ · ⑤ |d_B′| ⑥ θ_B′ → ตารางแตกเวกเตอร์ v_x = v cos θ, v_y = v sin θ ให้ · m_X ใช้ sin/cos · ข้อความวิธีทดลอง/ทฤษฎีปรับตาม
- ผลตรวจ: จำลองอ่านคลาด ±1 mm และ ±1° → Σp_x/p 98–102% · Σp_y/p ≤ 3% · มุมแยกมวลเท่ากัน 85–88° · มวล X 128–129 g (จริง 127) · ทดสอบลากไม้บรรทัด หมุนด้วยจุดแดงได้ −52.6° (จริง −52.7°) · โปรแทรกเตอร์ดูดติด B′1 พอดี · 375 px ไม่มี scroll แนวนอน · ไม่มี error
- แก้คำอธิบายใน labs_data และการ์ดหน้า VPL02 แล้ว build ใหม่

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/83. momentum-2d-collision-strobe.html` · `_admin/labs_data.py` · `virtual-physics-lab-02.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy Lab 82 และ 83

## [2026-09-18 06:50] — Lab 83: ถาดเก็บไม้บรรทัดและโปรแทรกเตอร์นอกโต๊ะ

### ทำอะไรไปบ้าง
- เจ้าของให้วางเครื่องมือนอกโต๊ะหรือมีที่เก็บ → เพิ่ม**ถาดเครื่องมือวัด**ติดขอบหน้าโต๊ะลม (นอกพื้นโต๊ะ ไม่บังภาพแฟลช) · ไม้บรรทัดและโปรแทรกเตอร์เริ่มต้นวางบนถาด
- ลากหยิบจากถาดไปวางบนโต๊ะได้ (ขยายขอบเขตการลากให้ถึงถาด) · ปุ่ม **📥 เก็บเครื่องมือ** คืนทั้งสองชิ้นกลับถาด · ↺ รีเซตค่า ก็คืนกลับถาด · ปุ่ม 🧰 เรียกเครื่องมือมาที่นี่ ยังใช้ได้
- มุมมอง "ทั้งชุด" ถอยให้เห็นถาด · ข้อความวิธีทดลองและคำแนะนำ 🧭 บอกให้หยิบจากถาด
- ตรวจ: ลากไม้บรรทัดจากถาดไปกลางโต๊ะได้ (28.0, 17.9) · กดเก็บกลับตำแหน่งถาด · ไม่มี error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/83. momentum-2d-collision-strobe.html`

## [2026-09-18 08:10] — Lab 85 ลูกบอลกระดอน: สัมประสิทธิ์การกระดอน (3D)

### ทำอะไรไปบ้าง
- **Lab 85** — ไม้เมตรตั้ง 0–150 cm ขีดละ 1 mm (ขีดอยู่ขอบด้านลูกบอล) · ขาตั้ง + ที่จับแม่เหล็ก **ลากขึ้นลงได้** (หรือปุ่ม ⬆⬇ 5 cm) มีขีดชี้แดงที่ระดับขอบล่างลูก · ความสูงเริ่มต้นสุ่ม 98–102 cm ต้องอ่านเอง
- ลูก 5 ชนิด: ซูเปอร์บอล · กอล์ฟ · เทนนิส · ปิงปอง · ลูกปริศนา X (e สุ่มต่อการเปิดหน้า) · แรงต้านอากาศแปรตาม v² (ปิงปองมากสุด)
- หลังปล่อย: **ภาพค้าง**ที่จุดสูงสุดครั้งที่ 1–3 พร้อมเส้นเล็งแดงไปยังไม้เมตร · ปุ่ม 🔍 อ่าน วนซูม h₀ → h₁ → h₂ → h₃ · **เครื่องจับเวลาเสียงกระทบ** ในฉาก แสดง T ระหว่างการกระทบ 1→2, 2→3, 3→4 (ms)
- กรอก h₀ h₁ h₂ h₃ T₁₂ T₂₃ → ตาราง √(hₙ₊₁/hₙ) 3 ค่า, e เฉลี่ย, พลังงานหายไป 1 − e², e = T₂₃/T₁₂ · กราฟ hₙ₊₁–hₙ (ความชัน e²), ln h – n, e – h₀ · ตรวจ e ของลูก X (±0.03) + คำทำนาย h₂ = 100 × 0.9⁴ = 65.6 cm
- ผลตรวจ: ซูเปอร์บอล e ความสูง 0.870 / เวลา 0.872 (จริง 0.873) · กอล์ฟ 0.786/0.787 (0.787) · เทนนิส 0.713/0.713 (0.719) · ลูก X 0.675–0.680 (0.681) · ปิงปอง 0.804 จาก 100 cm และ 0.819 จาก 50 cm (จริง 0.838) · ลากที่จับจาก 100.3 → 60.3 cm ได้ · ไม่มีค่าเฉลยใน DOM · 375 px ไม่มี scroll แนวนอน
- แก้ระหว่างทำ: เดิมเขียนว่า e จากความสูงของปิงปองต่ำกว่า e จากเวลา แต่แบบจำลองให้สองวิธีเท่ากัน (แรงต้านลดทั้งความสูงและเวลา) → เปลี่ยนข้อความ/คำถาม/กราฟที่ 3 เป็น "e ที่วัดได้ขึ้นกับความสูงที่ปล่อย" (กราฟ e – h₀)
- ลงทะเบียน: labs_data (86 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดโมเมนตัม 7 การ์ด + preview vpl2-bounce · hero 58) · build ใหม่ · ไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/85. bouncing-ball-restitution.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ deploy Lab 82, 83, 85
- เหลือแลปสุดท้ายในชุดโมเมนตัม: 86 เปลนิวตัน

## [2026-09-18 08:40] — Lab 85: วัตถุประสงค์ชัดเจน + แผ่นกระแทก

### ทำอะไรไปบ้าง
- **วัตถุประสงค์** เขียนใหม่เป็น 5 ข้อที่วัดผลได้ ("เมื่อจบการทดลอง นักเรียนสามารถ…": คำนวณ e ของลูก 4 ชนิด · เทียบ e 2 วิธี · อธิบายพลังงานที่หายไป 1 − e² และ hₙ = h₀e²ⁿ · ทดสอบว่า e ขึ้นกับความสูงที่ปล่อย/แรงต้านอากาศ · หา e ของลูก X) · แสดงเป็นกล่อง **🎯 วัตถุประสงค์ของการทดลอง** ด้านบนแท็บการทดลอง (นอกภาพ 3D กดย่อ/ขยายได้) และในแท็บวิธีการทดลอง
- **แผ่นกระแทกหินแกรนิต** 40 × 30 × 3 cm ใต้จุดปล่อย มีเป้ากากบาทสีเหลืองกลางแผ่น (แทนฐานขาตั้งเล็ก ๆ เดิม) · ขาตั้งและไม้เมตรยึดบนแผ่น · ศูนย์ไม้เมตร = ผิวแผ่น · แขนที่จับแม่เหล็กยื่นจากขาตั้งมาตรงเหนือเป้า ลูกตกกลางแผ่นพอดี · ย้ายเครื่องจับเวลาเสียงลงพื้นนอกแผ่น
- ข้อความอุปกรณ์ในแท็บวิธีการทดลองปรับตาม
- ตรวจ: e ยังตรง (ซูเปอร์บอล 0.883/0.882 จริง 0.888 · เทนนิส 0.735/0.732 จริง 0.739 · X 0.560/0.561 จริง 0.564) · ไม่มี error

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/85. bouncing-ball-restitution.html`

## [2026-09-18 08:55] — deploy: Lab 82 · 83 · 85 ชุดโมเมนตัม

### ทำอะไรไปบ้าง
- commit 46b7b29 (11 ไฟล์) + push main · เว็บจริงอัปเดตภายใน ~45 วินาที
- ตรวจเว็บจริง: Lab 82, 83, 85 โหลด 200 · หน้า VPL02 มี lab-85 · ทดลองบนเว็บจริงครบทั้ง 3 แลป (82 วัดเวลาได้ 106.6/106.3 ms · 83 ภาพแฟลชสมบูรณ์ มีถาดเครื่องมือ · 85 T = 787/687/598 ms มีกล่องวัตถุประสงค์) · ไม่มี console error

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ชุดโมเมนตัมบนเว็บแล้ว 79–85 · เหลือ 86 เปลนิวตัน

## [2026-09-18 10:30] — Lab 86 เปลนิวตัน (Newton's Cradle 3D) — แลปสุดท้ายของชุดโมเมนตัม

### ทำอะไรไปบ้าง
- **Lab 86** — เปลลูกเหล็ก 5 ลูก (m 66.8 g · d 2.54 cm · L 25.0 cm แขวนเชือกคู่) · **ลากลูกซ้ายสุด**ขึ้นตั้งมุม (หรือปุ่ม 🔼🔽 ทีละ 1°) · ยกได้ 1–4 ลูก (เฉพาะลูกเหล็ก)
- **เครื่องมือวัด 3 อย่าง**: โปรแทรกเตอร์ซ้าย ขีดละ 0.5° + แขนชี้น้ำเงินติดลูกที่ 1 (อ่านมุมยก) · โปรแทรกเตอร์ขวา + **เข็มชี้แดงค้างมุมสูงสุด**ของลูกขวาสุด · เครื่องจับเวลาเสียงกระทบในฉาก (ช่วง 1→2, 2→3, 3→4 ms) · ระบบ**ไม่บอกตัวเลขมุม**ในโหมดวัดเอง
- **ลูกกระทบเปลี่ยนได้**: เหล็ก 66.8 · อะลูมิเนียม 23.0 · ตะกั่ว 97.0 · **ลูกปริศนา X** (สุ่ม 30–110 g เลี่ยงช่วง 58–78) · e ของเหล็กสุ่ม 0.972–0.990 ต่อการเปิดหน้า (±0.4% ต่อการชน)
- **เอนจิน**: ลูกตุ้ม 5 ตัว integrate dt 0.2 ms + แก้การชนเป็นลำดับคู่ (impulse ตาม e) + แก้ตำแหน่งกันซ้อน → ยก n ลูกได้ออก n ลูกจริง · เสียง “ดัง” นับเฉพาะการชนที่ความเร็วเข้าหากัน > 25% ของ v เข้า (ลูกที่สั่น 1–3° ไม่ถูกนับ)
- **บันทึก 5 ช่อง**: θ₀ · θ ออก · N · (ไม่บังคับ) เวลาเสียง 1→2 → ตาราง ① โมเมนตัม/พลังงาน (v, p ก่อน–หลัง, Ek ก่อน–หลัง, k = v ออก/v เข้า → e = 2k^¼ − 1) · ตาราง ② R = (v ออก/v เข้า) ÷ k = 2m₁/(m₁+m) → m₁ = mR/(2−R) · ตาราง ③ T = 2t → g = 4π²L/T²
- กราฟ: v ออก–v เข้า · p หลัง–p ก่อน (สีตามจำนวนลูกที่ยก) · R–มวลลูกกระทบ พร้อมเส้นทฤษฎีและเส้นประม่วงของลูก X ลากไปตัดหาค่ามวล
- ตรวจคำตอบ: มวล X (±10%) · คำทำนาย “ยก 2 ลูกออก 1 ลูก → Ek = 200% ของก่อนชน จึงเป็นไปไม่ได้” (±5 จุด %)
- **ตามคำสั่งเจ้าของ**: ย้ายวัตถุประสงค์ไปแท็บ 📋 วิธีการทดลอง หน้าแลปเหลือบรรทัดเดียวว่า “สิ่งที่ต้องวัด…”
- ผลตรวจ (รันจริงในหน้าเว็บ): ยก 1/2/3/4 ลูก → ออก 1/2/3/4 ลูก มุมออก 19.05/19.26/19.51/19.76° ที่มุมยก 20° · k = 0.9517 → e = 0.9754 (จริง 0.977) · อะลูมิเนียม R = 0.5127 (ทฤษฎี 0.5122) · ตะกั่ว 1.185 (1.184) · **มวล X 84.7 g (จริง 84.3 · คลาด +0.5%)** · p หลัง/ก่อน 95–98.5% · Ek 90–97% · เวลาเสียง 503–510 ms → g 9.75 ที่ 10° แต่ 9.49 ที่ 30° (คาบยาวขึ้นเมื่อมุมมาก) · ไม่มี console error
- แก้ระหว่างทำ: ทิศเชือกกลับด้าน · หน้าปัดโปรแทรกเตอร์วาดเป็นลิ่มผิด (เปลี่ยนเป็นวาดทีละองศา) · เสาหน้าบังหน้าปัด (ย้ายหน้าปัดมาไว้หน้าโครง z 7.4/7.7) · ลูกเหล็กมืด (ลด metalness + เพิ่มไฟหน้า) · ป้าย L/มวล ย้ายลงมาที่เสา · จอเครื่องจับเวลาเยื้องจากตัวเครื่อง · ปุ่มตั้งค่าเคยถูกล็อกระหว่างแกว่ง → เปลี่ยนเป็นตั้งลูกใหม่อัตโนมัติถ้าบันทึกผลแล้ว
- ลงทะเบียน: labs_data (87 แลป), kp-auth + admin VLAB_SERIES, admin LAB_LIST, หน้า VPL02 (หมวดโมเมนตัม 8 การ์ด + preview `vpl2-cradle` · hero 59) · build ใหม่ (virtual-lab.html · library.html · index.html) · ไม่มีการ์ดซ้ำ

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 02/86. newtons-cradle.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html`, `virtual-physics-lab-02.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **ยังไม่ deploy Lab 86** (รอสั่ง “อัพขึ้นเว็บ”)
- ชุดโมเมนตัม 79–86 **ครบทั้งชุดแล้ว**

### หมายเหตุ
- เวลาระหว่างเสียงกระทบ = ครึ่งคาบ ใช้หาค่า g ได้ แต่ที่มุมยกมาก g ที่ได้จะต่ำกว่าจริง (T ≈ T₀(1 + θ²/16)) — ใช้เป็นประเด็นสอนเรื่องข้อจำกัดของสูตรลูกตุ้มมุมเล็ก

## [2026-09-18 12:10] — เปิดชุดใหม่: ฟิสิกส์อะตอม (VPL04) · Lab 87 + 88

### ทำอะไรไปบ้าง
- เจ้าของเลือกชุดต่อไป = **ฟิสิกส์อะตอม** และสั่งให้ **"เข้าโฟลเดอร์ใหม่"** → สร้าง `Virtual Physics Lab 04/` ซีรีส์ `vpl04` (ยังใช้เลขแลปต่อเนื่อง 87, 88, …)
- **รองรับซีรีส์ใหม่ทั้งระบบ**: `kp-auth.js` + `_admin/admin.html` (VLAB_SERIES.vpl04 · presets member/pro/premium/anonymous · ANONYMOUS_ACCESS_FALLBACK · legacy labs loop) · `protect_new_file.py` (access prefix `vlab:vpl04:` · is_sim/is_vlab · guard redirect → virtual-lab.html) · `labs_data.py` (prefix `V4` · topic ใหม่ `atomic` ⚛️ ฟิสิกส์อะตอมและควอนตัม · group ใหม่ `modern` ⚛️ ฟิสิกส์ยุคใหม่ · SERIES 'vpl04')
- **Lab 87 สเปกโตรมิเตอร์เกรตติง** — จานสเกลวงกลม r = 30 cm ขีดละ 1° เลขทุก 10° + **เวอร์เนียร์ 10 ช่องบน 9° (0.1°)** แขนเวอร์เนียร์เยื้องจากลำกล้อง 35° ไม่ให้ตัวกล้องบัง · **ตำแหน่งศูนย์ของสเกลสุ่มต่อการเปิดหน้า** จึงต้องวัดสองข้างแล้วเฉลี่ย (หรือเทียบกับค่าอ่านแนวตรง m = 0)
  - หลอด 3 หลอด: ไฮโดรเจน · ปรอท (ทราบค่า ใช้สอบเทียบ) · **แก๊สปริศนา X** (สุ่ม He/Ne/Na) · เกรตติง 600 / 300 เส้น/mm · จอแสดง **ภาพในกล้องเล็ง** (ช่องภาพ ±1.1° มีกากบาท เส้นสเปกตรัมสีจริงตาม λ บอกลำดับ m)
  - บันทึกได้เฉพาะเมื่อมีเส้นอยู่กลางกากบาท · ตาราง ① ค่าอ่าน ② θ = (ซ้าย − ขวา)/2 → λ = d sin θ/m ③ อนุกรมบัลเมอร์ (เรียง λ → n = 3–6) → R · กราฟ sin θ – m · 1/λ – (¼ − 1/n²) · แผนภูมิเทียบเส้นแก๊ส X กับเส้นอ้างอิง 4 ชนิด
  - ตรวจ: R (±2%) · แก๊ส X (เลือก) · λ ของเส้น n = 7 → 2 (±1.5%)
  - **ผลตรวจ** (จำลองอ่านเวอร์เนียร์ 0.1°): λ ไฮโดรเจน 655.5 / 486.8 / 434.5 / 410.9 nm (จริง 656.3 / 486.1 / 434.0 / 410.2 · คลาด ≤ 0.2%) · R = 1.0965 ×10⁷ (คลาด −0.08%) · Ne ที่วัดได้ 640.5 / 613.5 / 586.4 / 539.9 (จริง 640.2 / 614.3 / 585.2 / 540.1) · ไม่มี console error
- **Lab 88 ปรากฏการณ์โฟโตอิเล็กทริก** — หลอดปรอท + รูรับแสง 25/50/100% + **วงล้อฟิลเตอร์ 6 ช่อง** (365.0 · 404.7 · 435.8 · 546.1 · 578.0 · 650 nm) + หลอดโฟโต (เห็นอิเล็กตรอนวิ่งเมื่อมีกระแส) + แผงวัดมีโวลต์มิเตอร์ 0.01 V และแอมมิเตอร์ 0.1 nA · **ลากปุ่มหมุน**ปรับ 0.00–3.00 V
  - I = I₀(1 − V/V_s) + สัญญาณรบกวน ±0.2 nA · **โลหะแคโทดปริศนาสุ่มจาก 5 ชนิด** (Cs 2.14 · Rb 2.26 · K 2.30 · Na 2.36 · Ba 2.52 eV) · ฟิลเตอร์ที่ f < f₀ ไม่มีกระแสเลยแม้เพิ่มความเข้ม (บันทึกเป็น "ต่ำกว่าขีดเริ่ม" ได้)
  - ตาราง ① λ, f, E โฟตอน, I ที่ V = 0, V_s → ความชัน h/e, W, f₀, λ₀ · ตาราง ② ผลของความเข้ม · กราฟ V_s – f (มีเส้นประแดงของฟิลเตอร์ที่ไม่มีกระแส) · I – ความเข้ม · V_s – ความเข้ม
  - ตรวจ: h (±4%) · W (±0.12 eV) · ชนิดโลหะ (เลือก)
  - **ผลตรวจ**: โลหะสุ่มได้ Cs (W 2.14) → จาก 5 จุด h = 6.612 ×10⁻³⁴ J·s (คลาด −0.21%) · W = 2.134 eV · f₀ = 5.172 ×10¹⁴ Hz (λ₀ 580 nm) · 650 nm ไม่มีกระแส ✓ · ไม่มี console error
- แก้ระหว่างทำ (Lab 87): ทิศ/รูปหน้าปัดโปรแทรกเตอร์ · เสาบังหน้าปัด · จอบังจานสเกล (ย้ายไปมุมซ้ายหน้า) · เวอร์เนียร์อ่านไม่ออกที่จานเล็ก → ขยายจานเป็น r 30 cm + เทกซ์เจอร์ 4096 + ป้ายกำกับใหม่
- ลงทะเบียน: labs_data (89 แลป) · kp-auth + admin VLAB_SERIES vpl04 (lab-87, lab-88) · admin LAB_LIST · build ใหม่ (virtual-lab.html มีกลุ่ม ⚛️ ฟิสิกส์ยุคใหม่ · library.html · index.html นับ 89)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 04/87. hydrogen-spectrum-grating.html`, `Virtual Physics Lab 04/88. photoelectric-planck.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/protect_new_file.py`, `_admin/labs_data.py` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ชุดฟิสิกส์อะตอมที่เหลือตามที่เสนอ: 89 ฟรังก์–เฮิรตซ์ · 90 e/m ของอิเล็กตรอน · 91 การเลี้ยวเบนอิเล็กตรอน · 92 สเปกตรัมรังสีเอกซ์ (แบรกก์ · มอสลีย์) · 93 การกระเจิงอนุภาคแอลฟา · 94 รังสีวัตถุดำ/กฎวีน · 95 ครึ่งชีวิตและการดูดกลืนรังสี
- **VPL04 ยังไม่มีหน้า catalog เฉพาะ** (guard redirect ไป virtual-lab.html ซึ่งมีแลปครบแล้ว) — ถ้าต้องการหน้า `virtual-physics-lab-04.html` แบบ VPL02 ต้องสร้างเพิ่ม

### หมายเหตุ
- ⚠️ **สิทธิ์ผู้เข้าชมทั่วไป**: ค่า `anonymous_access` ใน Firestore (`settings/public`) ยังเป็น `['demo:*','vlab:vpl01:*','vlab:vpl02:*']` ถ้าไม่เพิ่ม `vlab:vpl04:*` ผู้เข้าชมที่ไม่ล็อกอินจะเห็นแลป 87–88 เป็นล็อก → ต้องเข้า admin panel การ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" แล้วติ๊ก VPL04 (ค่า fallback ในโค้ดเพิ่มให้แล้ว)

## [2026-09-18 13:40] — VPL04 ต่อ: Lab 89 ฟรังก์–เฮิรตซ์ · Lab 90 e/m ของอิเล็กตรอน

### ทำอะไรไปบ้าง
- **Lab 89 การทดลองฟรังก์–เฮิรตซ์** — หลอดในเตาอบ (ด้านหน้าเปิด เห็นไส้หลอด กริด 2 วง แผ่นเก็บ และอิเล็กตรอนวิ่ง) · แผงวัดมีโวลต์มิเตอร์ 0.1 V + แอมมิเตอร์ 0.1 nA · **ลากปุ่มหมุน** ปรับ U 0–30 V
  - I(U) = A(U−0.6)^0.95 คูณด้วยหลุมเกาส์เซียนที่ U = n·ΔU + V_contact (V_contact สุ่มต่อหลอด 0.8–1.9 V · หลุมลึกขึ้นตาม n และอุณหภูมิ) · สัญญาณรบกวน ±0.25 nA · 3 อุณหภูมิ (160/180/200 °C) เปลี่ยนความสูงกระแสและความลึกของหลุม
  - บันทึกได้ทุกจุด (U, I) เพื่อเขียนกราฟ · ระบบทำเครื่องหมายอัตโนมัติว่าจุดใดเป็น**จุดต่ำสุดลำดับที่ n** · ตาราง ② หา ΔU เฉลี่ย = พลังงานกระตุ้น (eV) · λ = 1240/E · กราฟ I–U และ U_n–n (ความชัน = ΔU, จุดตัด = V_contact)
  - หลอดปรอท (ทราบค่า 4.90 eV) + **หลอดปริศนา X** สุ่มจาก Cd 3.80 / Na 2.10 / K 1.61 eV · ตรวจ: พลังงาน (±3%) · λ (±3%) · ชนิดธาตุ
  - **ผลตรวจ**: X = K → ΔU วัดได้ 1.607–1.613 V (คลาด −0.18% ถึง +0.16%) λ 771 nm ✓ · Hg 4.95 V (+1.0% — เป็นความคลาดเชิงระบบแบบเดียวกับของจริง) · ตรวจคำตอบผ่านทั้ง 3 ข้อ · ไม่มี console error
  - แก้ระหว่างทำ: จุดต่ำสุดจุดแรกไม่ถูกตรวจจับ (หลุมตื้นเกินเทียบพื้นหลังที่ชันขึ้น) → ทำหลุมลึกขึ้น + ฐานชันน้อยลง + ขยายหน้าต่างตรวจจับเป็น 0.35ΔU · เตาอบเดิมทึบมองไม่เห็นหลอด → เปลี่ยนเป็นโครง 5 ด้านเปิดหน้า + กระจกใส
- **Lab 90 e/m ของอิเล็กตรอน** — ขดเฮลม์โฮลตซ์ (N = 130 · R = 15 cm) หลอดแก้วทรงกลม ปืนอิเล็กตรอนยิงขึ้น ลำอิเล็กตรอนเรืองแสงเป็นวงกลม · แผงวัด V (100–300 V) และ I (0.60–2.40 A)
  - **ไม้บรรทัดแนวตั้ง 0–30 cm ขีดละ 1 mm + ตัวชี้เลื่อนได้ 2 อัน** (เขียว = ขอบล่าง · แดง = ขอบบน) ลากด้วยมือ · 2r = ค่าอ่านบน − ล่าง · B = (4/5)^1.5 μ₀NI/R = 0.7793 mT/A · e/m = 2V/(B²r²)
  - กราฟ r–√V (I คงที่) · r–1/I (V คงที่) · V–½(Br)² ความชัน = e/m (มีเส้นประค่ามาตรฐานเทียบ) · ตรวจ: e/m (±6%) · คำทำนาย V เป็น 4 เท่า → r เป็น 2 เท่า
  - **ผลตรวจ**: 10 จุด (V 100–300 ที่ I 1.2 A และ I 0.8–2.2 ที่ V 200) รัศมี 2.8–7.6 cm อยู่ในหลอดทุกจุด · **e/m เฉลี่ย 1.761 ×10¹¹ C/kg (คลาด +0.13%)** · ไม่มี console error
  - แก้ระหว่างทำ: แผงวัดบังวงอิเล็กตรอนในมุมมองตรงหน้า (ย้ายไปด้านขวา) · **ลำอิเล็กตรอนถูกหลอดแก้วโปร่งบัง** เพราะ depthWrite ของวัสดุโปร่งแสง → ตั้ง depthWrite:false + renderOrder · เปลี่ยนไม้บรรทัดจากแนวนอน (วัดซ้าย–ขวา ซึ่งจุดกึ่งกลางวงเลื่อนตาม r) เป็น**แนวตั้งวัดขอบล่าง–บน** ตรงกับเครื่องจริงและไม่มีพารัลแลกซ์
- ลงทะเบียน: labs_data (91 แลป) · kp-auth + admin VLAB_SERIES vpl04 (lab-87…90) · admin LAB_LIST · build ใหม่

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 04/89. franck-hertz.html`, `Virtual Physics Lab 04/90. em-ratio-helmholtz.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ชุดฟิสิกส์อะตอมที่เหลือ: 91 การเลี้ยวเบนอิเล็กตรอน · 92 สเปกตรัมรังสีเอกซ์ (แบรกก์ · มอสลีย์) · 93 การกระเจิงอนุภาคแอลฟา · 94 รังสีวัตถุดำ/กฎวีน · 95 ครึ่งชีวิตและการดูดกลืนรังสี
- ⚠️ ยังต้องติ๊ก `vlab:vpl04:*` ในการ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" ของ admin panel (Firestore settings/public) ไม่งั้นผู้ไม่ล็อกอินเห็นเป็นล็อก

## [2026-09-18 15:20] — VPL04 ต่อ: Lab 91 เลี้ยวเบนอิเล็กตรอน · Lab 92 รังสีเอกซ์ (แบรกก์ · มอสลีย์)

### ทำอะไรไปบ้าง
- **Lab 91 การเลี้ยวเบนของอิเล็กตรอน** — หลอดเลี้ยวเบน ปืนอิเล็กตรอน 2.5–5.0 kV (ลากปุ่มหมุนบนแผงวัด) · แผ่นกราไฟต์ (d₁ 0.213 · d₂ 0.123 nm) และ **ผลึกปริศนา X** (d สุ่ม 0.150–0.280 nm) · จอเรืองแสงวาดด้วย canvas texture: วงแหวนเรืองแสงตามจริง + จุดกลาง + **สเกล mm บนจอ** + เส้นเล็งเขียว/แดงลากได้
  - D = 2Lλ/d · λ = h/√(2meV) · L = 13.5 cm · ตาราง/กราฟ D–1/√V (เส้นตรงผ่านจุดกำเนิด) และ D–λ · ความชัน → h (กราไฟต์) และ → d (ผลึก X)
  - ตรวจ: h (±6%) · d ของ X (±6%) · คำทำนาย V 4 เท่า → D ครึ่งหนึ่ง
  - **ผลตรวจ**: 14 จุด → h = 6.648 ×10⁻³⁴ (คลาด +0.33%) · d ของ X = 0.176 nm (จริง 0.178 · คลาด −1.1%) · ตรวจคำตอบผ่านครบ · ไม่มี console error
- **Lab 92 สเปกตรัมรังสีเอกซ์** — หลอดเอกซ์เปลี่ยนเป้าได้ (Cu Z=29 · Mo Z=42 · **เป้าปริศนา X** สุ่ม Z) · 20/25/30/35 kV · ผลึก NaCl d = 282 pm บนแท่นหมุน คัปปลิง θ–2θ · **ลากแขนหัววัดไกเกอร์** อ่านมุมจากสเกลจานขีดละ 0.25° และอ่านอัตรานับบนแผงวัด
  - อัตรานับ = สเปกตรัมต่อเนื่องแบบ Kramers (ขอบชัดที่ λ_min) + ยอดเกาส์เซียน Kα/Kβ (σ 0.16°) · ระบบทำเครื่องหมายอัตโนมัติว่าจุดที่บันทึกเป็น Kα / Kβ / ขอบ
  - กราฟ N–θ · λ_min–1/V (ความชัน hc/e → h) · √f–Z (มอสลีย์ ลากหา Z ของเป้า X) · ตรวจ: h (±6%) · Z (±1)
  - **ผลตรวจ**: Cu Kα วัดได้ 155.5 pm (จริง 154.1) · Mo 72.6 (71.1) · h = 6.74 ×10⁻³⁴ (+1.7%) · **Z ของเป้าปริศนา 36 → หาได้ 36.1 ✓** · ไม่มี console error
  - แก้ระหว่างทำ: ยอด Kβ ของ Mo จมอยู่ในไหล่ของ Kα → ลดความกว้างยอดเหลือ 0.16° · แขนและลำกล้องบังสเกลมุม → ขยายจานสเกลเป็น r 27 cm ย้ายแถบสเกลออกนอกแนวแขน
- ลงทะเบียน: labs_data (93 แลป) · kp-auth + admin VLAB_SERIES vpl04 (lab-87…92) · admin LAB_LIST · build ใหม่

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 04/91. electron-diffraction.html`, `Virtual Physics Lab 04/92. xray-bragg-moseley.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ชุดฟิสิกส์อะตอมที่เหลือ: **93 การกระเจิงอนุภาคแอลฟา · 94 รังสีวัตถุดำ/กฎวีน · 95 ครึ่งชีวิตและการดูดกลืนรังสี**
- ⚠️ ยังต้องติ๊ก `vlab:vpl04:*` ในการ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" ของ admin panel

## [2026-09-18 15:55] — แก้บั๊ก: Lab 92 ลากแขนหัววัดด้วยมือไม่ได้

### ทำอะไรไปบ้าง
- เจ้าของถามว่า “ใช้มือปรับมุมไม่ได้เหรอ” → ตรวจพบว่า **ลูป render ของ Lab 92 ไม่ได้เรียก `stepHand(dt)`** จึงจับแขนได้ (HD.on = true) แต่ค่า θ ไม่ขยับเลย (ปุ่ม ◀ ▶ ยังใช้ได้ปกติ) · แก้โดยเพิ่ม `stepHand(dt)` ในลูป
- ไล่ตรวจการลากด้วยมือของ **ทุกแลปในชุด VPL04** ด้วยการยิง MouseEvent จริงบนภาพ 3D:
  - Lab 87 หมุนกล้องเล็ง: 0 → −4.41° ✓ · Lab 88 ปุ่มหมุน: 0 → 0.81 V ✓ · Lab 89 ปุ่มหมุน: 0 → 12.1 V ✓
  - Lab 90 ตัวชี้บนไม้บรรทัด: 6.24 → 8.32 cm ✓ · Lab 91 เส้นเล็งบนจอ: 1.42 → 2.32 cm ✓ · **Lab 92 แขนหัววัด: 4.0° → 2.7° ✓ (หลังแก้)**
- หมายเหตุรูปแบบที่ใช้ในชุดนี้: แลปที่ลากแล้วค่าขยับทันที (ปุ่มหมุน 88/89) ไม่ต้องใช้ `stepHand` · แลปที่มีความหนืด (ลากแล้วค่อย ๆ ตาม) ต้องเรียก `stepHand(dt)` ในลูปเสมอ

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/92. xray-bragg-moseley.html`

## [2026-09-18 17:10] — VPL04 ต่อ: Lab 93 กระเจิงแอลฟา · Lab 94 รังสีวัตถุดำ

### ทำอะไรไปบ้าง
- **Lab 93 การกระเจิงอนุภาคแอลฟา** — ห้องสุญญากาศ · ต้นกำเนิด Am-241 5.5 MeV · แผ่นโลหะ 1.0 µm (ทองคำ Z 79 · เงิน 47 · อะลูมิเนียม 13 · **แผ่นปริศนา X**) · **ลากแขนหัววัด** 5–150° อ่านมุมจากจานสเกลขีดละ 1° · ตั้งเวลานับ 10/30/60/300 s แล้วกด ▶ เริ่มนับ (เห็นอนุภาควิ่งและเครื่องนับเดินจริง)
  - N = A·Z²/sin⁴(θ/2) + พื้นหลัง 0.3/นาที · **จำนวนนับสุ่มแบบปัวซง** (ความคลาดเคลื่อน √N เหมือนของจริง · lam > 30 ใช้การประมาณปกติ)
  - ตาราง N·sin⁴(θ/2) (ควรคงที่) · กราฟ N–1/sin⁴(θ/2) · log N–log sin(θ/2) · N–Z² (ลากหา Z ของแผ่น X) · ตรวจ: เลขชี้กำลัง (±0.5) · Z (±6) · ระยะเข้าใกล้ที่สุด (±10%)
  - **ผลตรวจ**: ความชัน log–log = **−4.00 พอดี** · N·sin⁴(θ/2) = 1.40–1.67 (คงที่ในระดับสถิติ) · Z ปริศนา 26 → หาได้ 26.3 ✓ · d = 41.4 fm ✓
  - แก้ระหว่างทำ: พื้นหลังเดิม 0.4/วินาที กลบข้อมูลมุมใหญ่จนความชันเหลือ −2.07 → ลดพื้นหลังเป็น 0.005/วินาที และเพิ่มความแรงต้นกำเนิด · ตัวสุ่มปัวซงแบบคูณค้างเมื่ออัตรานับสูง → เพิ่มการประมาณแบบปกติ
- **Lab 94 รังสีวัตถุดำ** — ไส้หลอดทังสเตน 5 ระดับ (T 1600–2800 K) วัด V, I → R → **T = 293(R/R₀)^(1/1.2)** · เกรตติง 300 เส้น/mm ใส่/ถอดได้ · **ลากแขนเทอร์โมไพล์** อ่านมุมขีดละ 0.1° หาจุดที่สัญญาณสูงสุด → λ_max = d sin θ · ถอดเกรตติง = วัดกำลังรวม
  - ใช้**สูตรพลังค์เต็มรูป**คำนวณสัญญาณ · สัญญาณรบกวน ±0.01 mV · **แหล่งปริศนา** T สุ่ม 2600–5800 K (จำลองดาวฤกษ์) · ไส้หลอดเปลี่ยนสีตามอุณหภูมิจริง
  - กราฟ λ_max–1/T (ความชัน = b) · log P–log T (ความชัน 4) · ตรวจ: b (±5%) · เลขชี้กำลัง (±0.5) · อุณหภูมิแหล่งปริศนา (±5%)
  - **ผลตรวจ**: b = **2.905 ×10⁻³ m·K (คลาด +0.25%)** · ความชันสเตฟาน **4.04** · แหล่งปริศนา 4400 K → หาได้ 4409 K (+0.2%) ✓
  - แก้ระหว่างทำ: เดิมคูณ cos θ (ผลของแถบความยาวคลื่น) ทำให้ b คลาด −4.2% → ตัดออก (ถือว่าเทอร์โมไพล์แก้ค่าแถบแล้ว) เหลือคลาด 0.25%
- ลงทะเบียน: labs_data (95 แลป) · kp-auth + admin VLAB_SERIES vpl04 (lab-87…94) · admin LAB_LIST · build ใหม่

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 04/93. rutherford-scattering.html`, `Virtual Physics Lab 04/94. blackbody-wien.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html` + build

### ค้างไว้ที่ไหน / ต้องทำต่อ
- เหลือแลปสุดท้ายของชุด: **95 ครึ่งชีวิตและการดูดกลืนรังสี**
- เจ้าของถามระหว่างทาง: **อยากซูมเข้าไปเห็นปรากฏการณ์ระดับอะตอมในแลปเหล่านี้** — ยังไม่ได้ทำ (แผน: เพิ่มปุ่มมุมมอง 🔬 ระดับอะตอม ในแต่ละแลป)
- ⚠️ ยังต้องติ๊ก `vlab:vpl04:*` ในการ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" ของ admin panel

## [2026-09-18 17:30] — ปิด session (ย้ายไปทำต่อในแชตใหม่)

### สถานะ ณ ตอนปิด
- **ชุดโมเมนตัม VPL02 (79–86) เสร็จครบและอยู่บนเว็บทั้งหมด**
- **ชุดฟิสิกส์อะตอม VPL04 ทำแล้ว 8 แลป (87–94) อยู่บนเว็บทั้งหมด** · รวมทั้งระบบ **95 แลป**
  - 87 สเปกโตรมิเตอร์เกรตติง (Rydberg) · 88 โฟโตอิเล็กทริก (h · W) · 89 ฟรังก์–เฮิรตซ์ · 90 e/m
  - 91 เลี้ยวเบนอิเล็กตรอน · 92 รังสีเอกซ์ (แบรกก์ · มอสลีย์) · 93 กระเจิงแอลฟา · 94 รังสีวัตถุดำ (วีน · สเตฟาน)
- git สะอาด ไม่มี commit ค้าง (ล่าสุด 5ed6698) · ทุกไฟล์ผ่าน protect_new_file และมี GA

### ต้องทำต่อในแชตใหม่ (เรียงตามที่คุยกันไว้)
1. **Lab 95 ครึ่งชีวิตและการดูดกลืนรังสี** — แลปสุดท้ายของชุดฟิสิกส์อะตอม (GM counter · วัดอัตรานับตามเวลา หาครึ่งชีวิตของตัวอย่างปริศนา · อัตรานับ–ความหนาแผ่น หา μ ของ Al/Pb)
2. **มุมมอง 🔬 ระดับอะตอม** (เจ้าของขอ) — เพิ่มปุ่มมุมมองในแต่ละแลป กล้องบินเข้าไปดูปรากฏการณ์ระดับอะตอมที่ผูกกับค่าที่ตั้งไว้จริง ๆ
   - 87 อิเล็กตรอนตก n→2 คายโฟตอนสีตรงกับเส้นที่เล็ง · 88 โฟตอนดีดอิเล็กตรอน (f < f₀ = ไม่หลุด) · 89 ชนยืดหยุ่น/ไม่ยืดหยุ่นตาม U
   - 91 คลื่นอิเล็กตรอนสะท้อนระนาบอะตอม (2d sin θ) · 92 อิเล็กตรอนชั้น K หลุดแล้ว L ตกแทน (Kα) · 93 แอลฟาเบนรอบนิวเคลียสตามมุมจริง · 94 อะตอมคายโฟตอนเป็นชั้น ๆ
   - ยังไม่ได้ตัดสินใจว่าจะทำต้นแบบที่ Lab 93 ก่อน หรือทำ 95 ให้จบชุดก่อนแล้วค่อยทำมุมมองอะตอมรวดเดียว
3. ⚠️ **งานที่เจ้าของต้องทำเอง**: เข้า admin panel → การ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" → ติ๊ก **VPL04** แล้วบันทึก (Firestore `settings/public.anonymous_access`) ไม่งั้นผู้ไม่ล็อกอินเห็นแลป 87–94 เป็นล็อก

### หมายเหตุสำหรับแชตใหม่
- ไฟล์ต้นแบบที่ใช้ต่อได้เลย: `Virtual Physics Lab 04/93. rutherford-scattering.html` (แขนหมุน + จานสเกล + เครื่องนับปัวซง) และ `94. blackbody-wien.html` (สูตรพลังค์ + เกรตติง)
- รูปแบบการลากด้วยมือ: ถ้ามีความหนืด **ต้องเรียก `stepHand(dt)` ในลูป render** (เคยพลาดที่ Lab 92 มาแล้ว)
- เพิ่มแลปใหม่ใน VPL04 ต้องแก้ 3 ที่: `_admin/labs_data.py` · `VLAB_SERIES` ใน `kp-auth.js` **และ** `_admin/admin.html` (+ LAB_LIST) แล้วรัน `python3 _admin/build_virtual_lab.py`

## [2026-09-18 21:10] — VPL04 ปิดชุด: Lab 95 ครึ่งชีวิตและการดูดกลืนรังสี

### ทำอะไรไปบ้าง
- **Lab 95 ครึ่งชีวิตและการดูดกลืนรังสี** — แลปสุดท้ายของชุดฟิสิกส์อะตอม (VPL04) · หลอด GM + เครื่องนับตั้งเวลา 5/10/20/30 s · **ลากแท่นเลื่อนลิ่มดูดกลืน**ไปตามรางที่มีสเกล 0–20 mm (ขีดละ 0.25 mm) เปลี่ยนความหนาที่ลำรังสีผ่าน
  - ต้นกำเนิด 7 แบบ: Ba-137m (T½ 153 s ทราบค่า) · **ตัวอย่างปริศนา X** (T½ สุ่มจาก 72/96/128/186/240 s) · Cs-137 (γ) · Sr-90 (β) · Am-241 (α) · **แหล่งปริศนา Y** (สุ่มชนิดรังสี) · 🚫 ไม่มีต้นกำเนิด (วัดพื้นหลัง)
  - ตัวอย่างที่สลายตัวมีปุ่ม **🔄 เตรียมตัวอย่างใหม่** (isotope generator) นาฬิกาตัวอย่างเดินต่อเนื่องแม้ไม่ได้นับ · เครื่องนับรายงาน **เวลากลางช่วงนับ** ให้อ่านไปเขียนกราฟ
  - วัสดุดูดกลืน 3 ชนิด (Al ρ2.70 · Pb ρ11.35 · กระดาษ ρ0.80) · μ คำนวณจาก μ/ρ จริงแยกตามชนิดรังสี (γ 662 keV · β Sr-90/Y-90 · α) · **จำนวนนับสุ่มแบบปัวซง** (√C) · พื้นหลัง 0.42 ครั้ง/วินาที
  - ตาราง ① การสลายตัว (t, C, N, N−N_bg, ln) · ② การดูดกลืน (แหล่ง, วัสดุ, x, …) · กราฟ 3 แบบ: N–t (พร้อมเส้นประพื้นหลัง) · ln(N−N_bg)–t (ความชัน −λ) · ln(N−N_bg)–x (ความชัน −μ แยกสัญลักษณ์ตามวัสดุ)
  - ตรวจ: ครึ่งชีวิตของ X (±7%) · ความหนาครึ่งค่าของตะกั่วสำหรับ γ Cs-137 (±12%) · ชนิดรังสีของแหล่ง Y (เลือก α/β/γ)
  - **ผลตรวจ (รัน 5 ชุดข้อมูล)**: T½ ของ Ba-137m คลาด −0.5% ถึง +1.4% · T½ ของ X คลาด −2.7% ถึง +0.9% · x½ ของตะกั่ว คลาด −2% ถึง +3.9% (ค่าจริง 5.98 mm) · x½ ของอะลูมิเนียม 32.8–39.4 mm (จริง 34.5) · Sr-90 ใน Al x½ ≈ 0.37 mm · α หยุดด้วยกระดาษ 0.25 mm (3489 → 5 ครั้ง) · ตรวจคำตอบผ่านครบ 3 ข้อ · ไม่มี console error
- แก้ระหว่างทำ:
  - แผงเครื่องนับเดิมวางฝั่งเดียวกับกล้อง (z บวก) บังภาพทั้งหมด → ย้ายไปด้านหลังโต๊ะ (z = −23) หันจอกลับ 180° และมุมมอง 🎛 เครื่องนับ ใช้ az = π · ย่อขนาดแผงให้ไม่บังภาพบนจอมือถือ
  - สเกลบนรางกลับหัว (กด 0 แต่ขึ้น 20) → แก้สูตรแปลง pixel ↔ world z ของเทกซ์เจอร์ (canvas แถวบน = z ลบ ไม่ใช่ z บวก)
  - **บั๊กสำคัญ: ลากแล้วค้างห่างเป้าหมาย** — `stepHand` เดิมหน่วงจากค่า `XT` ที่ปัดเป็นขีดสเกลแล้ว ทำให้เมื่อเหลือระยะน้อยกว่าครึ่งขีด/สัมประสิทธิ์หน่วง ค่าจะไม่ขยับอีกเลย (ค้างห่างราว 1.5 mm) → แก้โดยเก็บตำแหน่งต่อเนื่องไว้ใน `HD.pos` แล้วค่อยปัดเป็น `XT`
- ลงทะเบียน: labs_data (96 แลป) · kp-auth + admin VLAB_SERIES vpl04 (lab-87…95) · admin LAB_LIST · build ใหม่ (virtual-lab.html · library.html · index.html นับ 96)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 04/95. half-life-absorption.html`
- `_admin/labs_data.py`, `kp-auth.js`, `_admin/admin.html` + build (`virtual-lab.html`, `library.html`, `index.html`)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **ชุดฟิสิกส์อะตอม VPL04 ครบแล้ว 9 แลป (87–95)** — งานต่อไปคือ **มุมมอง 🔬 ระดับอะตอม** ตามที่เจ้าของขอ (ยังไม่ได้ตัดสินใจว่าจะทำต้นแบบที่แลปไหนก่อน)
- **บั๊กเดียวกันกับ `stepHand` มีอยู่ในแลป 87–94 ด้วย** (ปัดค่าก่อนหน่วง) เช่น Lab 93 ปัดมุมเป็นองศา → ลากแล้วค้างห่างเป้าหมายได้ถึง ~8° · ยังไม่ได้แก้ รอเจ้าของสั่ง (แก้เหมือนกันทุกไฟล์: เพิ่ม `HD.pos`)

### หมายเหตุ
- ⚠️ **งานที่เจ้าของต้องทำเอง (ยังไม่ได้ทำ)**: ตรวจสอบจาก Firestore แล้วพบว่า `settings/public.anonymous_access` ปัจจุบันคือ
  `['demo:*','vlab:vpl01:*','vlab:vpl02:*','manual:vpl01:lab-1..5']` — **ยังไม่มี vpl03 และ vpl04 เลย**
  ผู้เข้าชมที่ไม่ล็อกอินจึงเข้าแลป 87–95 ไม่ได้ (บางครั้งเข้าได้เพราะ Firestore โหลดช้ากว่า guard แล้วตกไปใช้ค่า fallback ในโค้ด — ไม่แน่นอน)
  → เข้า admin panel → การ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" → ติ๊ก **VPL03 + VPL04 ทั้งชุด** แล้วบันทึก

## [2026-09-18 22:05] — แก้บั๊ก: ลากด้วยมือแล้วค่าค้างห่างเป้าหมาย (11 ไฟล์)

### ทำอะไรไปบ้าง
- **อาการ**: ลากอุปกรณ์ในภาพ 3D แล้วค่าจะ**หยุดขยับก่อนถึงตำแหน่งที่นิ้วชี้** ต้องขยับเมาส์ไปมาถึงจะเข้าใกล้ได้
- **สาเหตุ**: `stepHand()` เดิมคำนวณจากค่าที่**ปัดเป็นขีดสเกลแล้ว** (`cur = ตัวแปรสถานะ`) แล้วค่อยหน่วงแบบเอกซ์โพเนนเชียล · ระยะที่ขยับต่อเฟรม = k × ระยะที่เหลือ (k ≈ 0.06–0.08 ที่ 60 fps) เมื่อระยะที่เหลือน้อยกว่า (ครึ่งขีด ÷ k) ค่าที่ปัดแล้วจะ**ไม่เปลี่ยนอีกเลย** → เกิด dead zone
  - Lab 93 ปัดเป็นองศาเต็ม → ค้างได้ถึง **~8°** · Lab 92 ~1.6° (ในหน่วย 2θ) · Lab 94 ~0.8° · Lab 90/91 ~0.7 mm · VPL02 (72·79·80·81·82·83) ปัด 0.1 cm → ค้าง ~0.6–0.8 cm
- **วิธีแก้** (เหมือนกันทุกไฟล์): เก็บตำแหน่งต่อเนื่องไว้ใน `HD.pos` แล้วปัดเป็นขีดสเกล**เฉพาะตอนเขียนค่าจริง** · ต้นฟังก์ชันมีเงื่อนไข resync `if(!(Math.abs(HD.pos - <ค่าปัจจุบัน>) <= ครึ่งขีด)) HD.pos = <ค่าปัจจุบัน>;` เพื่อให้ยังตามค่าที่ถูกเปลี่ยนจากที่อื่นได้ (ปุ่ม ◀ ▶ · รีเซต · เปลี่ยนชิ้นที่ลาก) และไม่ต้องแก้ `hdStart()`
- **ตรวจแล้วทั้ง 11 ไฟล์**: สั่งลากไปยังเป้าหมาย 2–3 ค่า แล้วค่าเข้าเป้า**ตรงเป๊ะทุกไฟล์** (เดิมค้างห่าง) · ทดสอบ resync ที่ Lab 93: ระหว่างลากแล้วแทรกค่าจากปุ่ม (20→90) เฟรมถัดไปเดินต่อจาก 89 อย่างนุ่มนวล ไม่กระโดดกลับ · ทดสอบลากด้วย MouseEvent จริงที่ Lab 93: จับติด · เข้าเป้าที่นิ้วชี้ (63.5 → 63) · ไม่มี console error
- ไฟล์ที่**ไม่มีบั๊กนี้** (ไม่ได้แก้): 70 · 84 · 85 · 86 (ไม่ปัดค่า) · 87 (ไม่ปัดค่า) · 88 (ปุ่มหมุนตามมือทันที) · 89 (เหมือนกัน) · 95 (แก้ไปแล้วตอนสร้าง)

### ไฟล์ที่แก้
- `Virtual Physics Lab 02/` — `72. work-kinetic-energy.html` · `79. impulse-force-sensor.html` · `80. momentum-inelastic-collision.html` · `81. momentum-elastic-collision.html` · `82. momentum-explosion-recoil.html` · `83. momentum-2d-collision-strobe.html`
- `Virtual Physics Lab 04/` — `90. em-ratio-helmholtz.html` · `91. electron-diffraction.html` · `92. xray-bragg-moseley.html` · `93. rutherford-scattering.html` · `94. blackbody-wien.html`

### หมายเหตุ
- **กติกาสำหรับไฟล์ใหม่**: ถ้าลากแล้วต้องปัดค่าเป็นขีดสเกล ให้หน่วงจากตัวแปรต่อเนื่องเสมอ (`HD.pos`) แล้วค่อยปัด — อย่าหน่วงจากค่าที่ปัดแล้ว
- ⚠️ เรื่องสิทธิ์ผู้เข้าชมทั่วไป (Firestore `settings/public.anonymous_access` ยังไม่มี vpl03/vpl04) **ยังค้างอยู่เหมือนเดิม**

## [2026-09-18 23:15] — ต้นแบบมุมมอง 🔬 ระดับอะตอม (Lab 93 รัทเทอร์ฟอร์ด)

### ทำอะไรไปบ้าง
- เพิ่มปุ่มมุมมอง **🔬 ระดับอะตอม** ในแถวปุ่มบนภาพ 3D ของ Lab 93 — กดแล้วซ่อนฉากอุปกรณ์ทั้งหมดและแสดงฉากระดับนิวเคลียส (หน่วย fm) แทน
- **ผูกกับค่าที่ตั้งจริง**: วาดวิถีคูลอมบ์แบบผลักจาก θ ที่แขนหัววัดตั้งอยู่ และ Z ของแผ่นที่เลือก
  - `r(φ) = a(ε²−1)/(ε cos φ − 1)` · `ε = 1/sin(θ/2)` · `a = d/2` · `d = 2kZe²/E` · `b = a·cot(θ/2)`
  - ตรวจแล้วว่ามุมเบนออกมาตรงกับ θ ที่ตั้ง และทิศทางตรงกับตำแหน่งแขนหัววัดจริง (เข้าทาง −z ของนิวเคลียส ออกที่มุม θ ด้าน −z เหมือนสูตร `a=atan2(−z,x)` ของฉากใหญ่)
- องค์ประกอบในฉาก: นิวเคลียสเรืองแสง + ป้ายชื่อ · วิถีหลักเป็น**หลอด** (TubeGeometry — `LineBasicMaterial` ปรับความหนาไม่ได้ใน WebGL) · อนุภาคแอลฟาวิ่งวนตามวิถี (ช้าลงตอนเข้าใกล้ เร็วขึ้นตอนไกล เพราะแบ่งช่วงด้วยมุม φ เท่า ๆ กัน) · เส้นประ 3 เส้น (ลำเข้า · ทิศกระเจิง · ระยะเล็ง b) · **เส้นจาง 3 เส้นของอนุภาคที่เล็งห่างกว่า** (b × 1.9 / 3.4 / 6.0 → เบนน้อยลงมาก) · แถบคำอธิบายบอก d · b · ระยะเข้าใกล้ที่สุด
- **ไม่รั่วคำตอบ**: เลือกแผ่นปริศนา X → ใช้สเกล d สมมุติคงที่ (ภาพไม่เปลี่ยนตาม Z) ป้ายเขียน "นิวเคลียสของแผ่น X (+Ze)" และซ่อนตัวเลข Z · b · d ทั้งหมด — รูปร่างวิถีขึ้นกับ θ อย่างเดียว จึงไม่บอกค่า Z
- ทำตามกติกาเดิม: ไม่มีกล่อง HTML ทับภาพ 3D (คำอธิบายเป็นป้ายในฉาก) · ป้ายมีขนาดบนจอคงที่ทุกมุม/ทุกแผ่น (คิดขนาดเป็นหน่วยโลกแล้วหารด้วยสเกลฉาก) · ฉากถูกจัดกึ่งกลางและย่อให้พอดีเฟรมอัตโนมัติ · ↺ รีเซตค่า กลับมุมมอง "ทั้งชุด" ตามเดิม
- **ผลตรวจ**: θ = 5° (เกือบตรง) · 20° · 45° · 150° (สะท้อนกลับ) และแผ่น Au / Al / X — ภาพถูกต้องและอ่านได้ทุกกรณี · ค่าที่แสดง Au θ20°: d = 41.4 fm · b = 117.3 fm · เข้าใกล้ที่สุด 139.9 fm (ตรงกับสูตร) · สลับกลับมุมมองปกติแล้วอุปกรณ์กลับมาครบ นับและบันทึกได้ตามเดิม · ไม่มี console error
- เพิ่มคำอธิบายปุ่มนี้ในแท็บ 📋 วิธีการทดลอง และ 📐 ทฤษฎี

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/93. rutherford-scattering.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ถ้าเจ้าของโอเคกับต้นแบบนี้ → ทำมุมมองระดับอะตอมของแลปอื่นต่อ: 87 (อิเล็กตรอนตก n→2 คายโฟตอนสีตรงกับเส้นที่เล็ง) · 88 (โฟตอนดีดอิเล็กตรอน · f < f₀ ไม่หลุด) · 89 (ชนยืดหยุ่น/ไม่ยืดหยุ่นตาม U) · 91 (คลื่นอิเล็กตรอนสะท้อนระนาบอะตอม) · 92 (อิเล็กตรอนชั้น K หลุดแล้ว L ตกแทน) · 94 (อะตอมคายโฟตอนเป็นชั้น ๆ) · 95 (นิวเคลียสสลายตัว · โฟตอนถูกดูดกลืนในแผ่น)
- ⚠️ สิทธิ์ผู้เข้าชมทั่วไป (vpl03/vpl04 ใน Firestore) ยังค้างเหมือนเดิม

### หมายเหตุ
- รูปแบบที่ใช้ซ้ำได้: `P.atom` เป็นกลุ่มแยก · `setAtomMode()` สลับ `visible` ของลูกฉากทั้งหมด (ยกเว้นไฟ) · `update3D()` แยกสาขาออกมาก่อนตั้งแต่ต้นเมื่ออยู่โหมดอะตอม · `atomDirty` ตั้งเมื่อ θ/แผ่นเปลี่ยน · `hdStart()` คืน false ในโหมดอะตอมเพื่อให้ลากหมุนภาพได้เต็มที่

## [2026-09-18 23:55] — ปรับมุมมองระดับอะตอม Lab 93 ให้เป็นภาพแบบตำราแบบจำลองรัทเทอร์ฟอร์ด

### ทำอะไรไปบ้าง
- เจ้าของส่งภาพ "RUTHERFORD MODEL" (ลำอนุภาคขนานหลายเส้นยิงเข้าอะตอม ส่วนใหญ่ทะลุตรง มีเส้นเดียวเด้งกลับ · วงประขอบอะตอม · อิเล็กตรอนสีฟ้า · นิวเคลียสแดง) มาเป็นแบบ → **รื้อฉากระดับอะตอมใหม่ทั้งหมดให้เป็นแบบนั้น**
- ตอนนี้ฉากมี: **ลำอนุภาคขนาน 9 เส้น** เริ่มจากขอบซ้ายเดียวกัน มีหัวลูกศรจบนอกวงประเท่ากัน · วงประขอบเขตอะตอม · อิเล็กตรอน 6 ตัว · นิวเคลียสเรืองแสง
  - ทุกเส้นคำนวณจากสูตรจริง — ระยะเล็ง b ของแต่ละเส้นกระจายเป็นสัดส่วนของรัศมีภาพ (0.05–0.55) ทั้งสองด้านของนิวเคลียส แล้วได้มุมเบนของตัวเองจาก `θ = 2·arctan((d/2)/b)`
  - **เส้นเหลือง = เส้นที่เบนเข้าหัววัดพอดีที่มุม θ ที่ตั้งไว้** (b = (d/2)cot(θ/2)) มีอนุภาคแอลฟาวิ่งตามและเส้นประบอก b
  - เส้นที่เล็งห่างแทบไม่เบน · เส้นที่เฉียดใกล้เบนมากถึงเด้งกลับทางเดิม — เห็นข้อสรุปของรัทเทอร์ฟอร์ดในภาพเดียว
  - ตั้ง θ = 150° → เส้นเหลืองเด้งกลับไปทางซ้าย (ภาพที่ล้มแบบจำลองทอมสัน)
- แถบคำอธิบายเพิ่มหมายเหตุว่า **วงประไม่ได้ตามมาตราส่วน** (อะตอมจริงใหญ่กว่านิวเคลียส 10⁴–10⁵ เท่า) เพื่อไม่ให้เข้าใจผิด
- ยังไม่รั่วคำตอบเหมือนเดิม: แผ่นปริศนา X ใช้สเกลสมมุติคงที่ ซ่อน Z · b · d
- **ผลตรวจ**: θ = 20 · 60 · 150° และแผ่น Au / Al / X — ภาพถูกต้อง ทิศทางเบนตรงกับสูตร (ตรวจตำแหน่งหัวลูกศรของทุกเส้นเทียบมุมที่คำนวณได้) · ไม่มี console error

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/93. rutherford-scattering.html`

## [2026-09-19 00:30] — แก้ระบบสิทธิ์: สมาชิกที่ล็อกอินได้สิทธิ์ตาม role อัตโนมัติสำหรับชุดที่เพิ่มใหม่

### ทำอะไรไปบ้าง
- เจ้าของถามว่า "ในแอดมินปลดล็อคแล้วทำไมยังดูไม่ได้" → ไล่ตรวจแล้วพบว่า
  - ค่า `settings/public.anonymous_access` **ถูกต้องแล้ว** = `['demo:*','vlab:vpl01:*','vlab:vpl02:*','vlab:vpl03:*','vlab:vpl04:*']`
  - เปิดเว็บจริงแบบไม่ล็อกอิน: Lab 95 เปิดได้ · virtual-lab.html การ์ด 96 ใบ **ล็อก 0 ใบ** → ฝั่งผู้เข้าชมทั่วไปไม่มีปัญหา
  - **ต้นเหตุจริง**: การ์ด 🌐 สิทธิ์ผู้เข้าชมทั่วไป มีผลกับคนที่ **ไม่ล็อกอิน** เท่านั้น · คนที่ล็อกอินใช้ `access` ในเอกสารของตัวเอง และ `migrateAccess()` เดิม **return ค่าที่เก็บไว้ทั้งดุ้นถ้าไม่ว่าง** ไม่ดึง preset ของ role มาเติม → บัญชีที่ตั้งสิทธิ์ไว้ก่อนจะมี vpl03/vpl04 จะยังถูกล็อก **แม้เป็นบัญชี admin** (ถ้า `access` ของตัวเองระบุไว้เองและไม่มี `*`)
  - เจอด้วยว่า `setRole()` ในแอดมินเขียนแค่ฟิลด์ `role` ไม่แตะ `access` — เปลี่ยน role เฉย ๆ จึงไม่ปลดอะไรเลย
- **แก้ตามที่เจ้าของเลือก (แบบ 1)**: เพิ่ม `mergeRolePreset(access, role)` ใน `kp-auth.js` แล้วให้ `migrateAccess()` เรียกทุกครั้ง
  - ขอบเขตไหนที่ `access` เดิม**ไม่มี entry พูดถึงเลย** (ไม่มีทั้ง `vlab:vpl04:*` และ `vlab:vpl04:lab-xx`) → ถือว่ายังไม่เคยตัดสินใจ เติมให้ตาม preset ของ role
  - ขอบเขตที่มี entry อยู่แล้ว (แม้รายไอเทม) → **เคารพค่าเดิม** ไม่เติมทับ (ไม่พังการจำกัดสิทธิ์ที่ตั้งใจไว้)
  - `blocked` → `[]` เสมอ · มี `'*'` อยู่แล้ว → คงเดิม
  - ไม่เขียนทับข้อมูลใน Firestore — เป็นการคำนวณตอนอ่านเท่านั้น (ย้อนกลับได้)
- **ผลตรวจ** (ทดสอบทั้งใน Node และในหน้าเว็บจริง):
  - member เก่า `['demo:*','vlab:vpl01:*','vlab:vpl02:*']` → ได้ vpl03 + vpl04 เพิ่ม · เปิด Lab 95 ได้ ✓
  - admin ที่มี `access` ระบุเอง → ได้ `'*'` ✓ (แก้อาการ admin ถูกล็อกเอง)
  - blocked แม้มี access เต็ม → `[]` ✓
  - member ที่ตั้งใจให้เฉพาะ `vlab:vpl04:lab-87` → Lab 95 ยังล็อกอยู่ ✓ (ไม่เผลอปลดเกิน)
- เพิ่มกล่องอธิบายกติกานี้ใน modal ⚙️ แก้ไขสิทธิ์ ของแอดมิน และบันทึกกฎลง `CLAUDE.md`

### ไฟล์ที่แก้
- `kp-auth.js` — เพิ่ม `mergeRolePreset()` + เรียกใน `migrateAccess()`
- `_admin/admin.html` — กล่องอธิบายใน modal สิทธิ์
- `CLAUDE.md` — หัวข้อใหม่ "สิทธิ์ของสมาชิกที่ล็อกอิน = ค่าที่เก็บไว้ + preset ของ role"

### หมายเหตุ
- ระหว่างทดสอบเจอว่า **`kp-auth.js` ถูกเบราว์เซอร์แคชแรงมาก** (สคริปต์ไม่มี `?v=`) ทำให้โหลดของเก่าค้างอยู่ — บนเว็บจริง GitHub Pages ตั้ง max-age ~10 นาที จึงหายเองภายใน 10 นาที แต่ถ้าอยากให้แน่ใจทุกครั้งที่แก้ ควรเติม `?v=` ท้าย `kp-auth.js` ทุกไฟล์ (ยังไม่ได้ทำ — ต้องแก้ ~100 ไฟล์ + `protect_new_file.py`)
- ข้อควรระวังใหม่: จะ "ไม่ให้สิทธิ์ชุดหนึ่ง" ด้วยการเว้นว่างไม่ได้แล้ว ต้องติ๊กเฉพาะรายการที่อนุญาตอย่างน้อย 1 ข้อ หรือใช้ role `blocked`

## [2026-09-19 01:10] — เติมเลขเวอร์ชันท้าย kp-auth.js ทุกหน้า (cache busting)

### ทำอะไรไปบ้าง
- ปัญหา: `kp-auth.js` ถูกอ้างแบบไม่มีเลขเวอร์ชัน → เบราว์เซอร์ใช้สำเนาเก่าที่เก็บไว้ในเครื่อง แก้กฎสิทธิ์แล้วยังเห็นของเก่า (บน GitHub Pages ~10 นาที · ตอนทดสอบในเครื่องค้างยาวกว่านั้นมาก)
- เติม `?v=<เลข>` ท้าย URL ของ `kp-auth.js` **ทั้ง 155 จุดใน 155 ไฟล์** (ทุกระดับ path: `kp-auth.js` · `../` · `../../` · `../../../`)
  - ย้ำ: **ไม่มีไฟล์ใหม่เกิดขึ้น** — `?v=` เป็นแค่ query string เซิร์ฟเวอร์ยังส่งไฟล์เดิมตัวเดียว
- สร้าง **`_admin/bump_auth_version.py`** — รันครั้งเดียวเปลี่ยนเลขให้ทุกไฟล์
  - ไม่ใส่อาร์กิวเมนต์ = ใช้วันที่วันนี้ (ถ้าซ้ำของเดิมต่อ `-2`, `-3` ให้) · ใส่เลขเองได้ · `--check` ดูสถานะ
  - เลขปัจจุบันเก็บที่ `_admin/asset_version.txt` (ตอนนี้ `20260919`) · เพิ่มไฟล์อื่นที่อยากติดเวอร์ชันได้ที่ `TARGETS`
- แก้ **`protect_new_file.py`**: เพิ่ม issue `AUTH_VER` → ไฟล์ใหม่ได้ `?v=` อัตโนมัติ และ `--scan --fix` เติมให้ไฟล์ที่ยังขาด · `build_virtual_lab.py` เรียก protect อยู่แล้ว ไฟล์ที่ generate จึงได้เวอร์ชันติดมาเอง (ตรวจแล้ว)
- **ผลตรวจ**: เปิดหน้าจริง 3 ระดับ path (`virtual-lab.html` · VPL01 ลึก 2 ชั้น · VPL04 ลึก 1 ชั้น) — แท็กมี `?v=20260919` ครบ · ฟังก์ชันใหม่ `mergeRolePreset` โหลดมาแล้วจริง (ก่อนหน้านี้เบราว์เซอร์ยังใช้ไฟล์เก่าอยู่) · การ์ดในหน้า catalog 96 ใบ ล็อก 0 ใบ · ไม่มี console error
- บันทึกวิธีใช้ลง `CLAUDE.md` หัวข้อใหม่ "เวอร์ชันของสคริปต์ที่แชร์กัน (cache busting)"

### ไฟล์ที่แก้
- ใหม่: `_admin/bump_auth_version.py`, `_admin/asset_version.txt`
- `_admin/protect_new_file.py` — issue `AUTH_VER` + แทรกแท็กพร้อมเวอร์ชัน
- `CLAUDE.md` — วิธีใช้
- ไฟล์ HTML 155 ไฟล์ทั้งโปรเจกต์ (เติม `?v=` จุดละ 1 บรรทัด)

### หมายเหตุ
- `protect_new_file.py --scan` ยังไล่สแกนเข้าไปใน `.claude/worktrees/` (สำเนา worktree เก่าที่ค้างอยู่) ทำให้รายงาน issue เกินจริงหลายร้อยรายการ — ของโปรเจกต์จริงครบหมดแล้ว (`bump_auth_version.py --check` ยืนยัน) ถ้าจะให้เนียนควรให้ scan ข้ามโฟลเดอร์ `.claude` ด้วย (ยังไม่ได้ทำ)
- **ครั้งต่อไปที่แก้ `kp-auth.js` อย่าลืมรัน `python3 _admin/bump_auth_version.py`** ก่อน commit

## [2026-09-19 02:05] — มุมมอง 🔬 ระดับอะตอม แลปที่ 2: Lab 87 สเปกตรัมไฮโดรเจน (แบบจำลองโบร์)

### ทำอะไรไปบ้าง
- เพิ่มปุ่ม **🔬 ระดับอะตอม** ใน Lab 87 — กดแล้วเห็น **แบบจำลองโบร์ของอะตอมไฮโดรเจน**: โปรตอนตรงกลาง · วงโคจร n = 1–6 (เส้นประ) · อิเล็กตรอนโคจรอยู่วง n แล้ว**ตกลงมาที่ n = 2 พร้อมคายโฟตอนเป็นคลื่นวิ่งออกไป**
- **ผูกกับเส้นที่กล้องเล็งอยู่จริง**: λ ของเส้นนั้น → หา n ต้นทางจากอนุกรมบัลเมอร์ → วงต้นทาง/ปลายทางถูกไฮไลต์ (ฟ้า n = 2 · ม่วง n ต้นทาง) และ**สีของโฟตอนคือสีเดียวกับเส้นที่เห็นในกล้อง** (ใช้ `lamRGB` ตัวเดียวกับที่วาดในกล้อง)
- แถบคำอธิบายในฉากบอก ΔE = 1240/λ และสูตร 1/λ = R(1/2² − 1/n²) ที่ใช้หาค่า R ในตาราง ③ · มีหมายเหตุว่ารัศมีวงในภาพย่อไว้ (ของจริง r ∝ n²)
- **ไม่รั่วคำตอบ**: หลอดปรอทและ **แก๊สปริศนา X** จะไม่วาดการเปลี่ยนระดับเลย แต่ขึ้นข้อความว่าแบบจำลองโบร์ใช้กับไฮโดรเจน (อิเล็กตรอน 1 ตัว) เท่านั้น — เป็นฟิสิกส์ที่ถูกต้องและไม่บอกใบ้ชนิดแก๊ส
- **ผลตรวจ 5 สถานะ**: เล็ง 656 → n = 3 ✓ · 486 → n = 4 ✓ · 434 → n = 5 ✓ · 410 → n = 6 ✓ · เส้นกลาง m = 0 → ขึ้นข้อความอธิบายว่าเป็นแสงรวมทุกสี ✓ · ปรอท/แก๊ส X → ขึ้นข้อความแบบจำลองโบร์ใช้ไม่ได้ ✓ · สีโฟตอนตรงกับความยาวคลื่นทุกเส้น · ไม่มี console error
- แก้ระหว่างทำ: ประกาศ `lamHex` ซ้ำกับของเดิมในไฟล์ (syntax error) → ใช้ตัวเดิม · กรอบภาพเดิมคำนวณจากครึ่งล่างอย่างเดียวทำให้ฉากลอยไม่กลาง → คิด bounding box จริงทั้ง 4 ด้าน (รวมระยะที่โฟตอนวิ่ง) แล้วเลื่อนกลุ่มให้อยู่กลางภาพ · วงโคจรเส้นบางมองไม่ชัด → วาดวงแหวนทึบทับเฉพาะ 2 วงที่เกี่ยวข้อง

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/87. hydrogen-spectrum-grating.html`

### เพิ่มเติมตามที่เจ้าของขอ (รอบเดียวกัน)
- เจ้าของบอกว่า "น่าจะมีซิมูเลชันในอะตอมด้วย เช่นโฟตอนวิ่งชนอิเล็กตรอนตามทฤษฎี" → ขยายเป็น **วงจรครบรอบ**:
  ① อนุภาคพุ่งเข้ามากระตุ้น → อิเล็กตรอนกระโดดจาก n = 2 ขึ้นไปวง n · ② อยู่ที่วง n ชั่วครู่ · ③ ตกกลับ n = 2 แล้วคายโฟตอนวิ่งออกไป
- เพิ่มปุ่ม **⚡ กระตุ้น** (โผล่เฉพาะในมุมมองอะตอม) สลับ 2 กลไก:
  - **ชนด้วยอิเล็กตรอนเร็ว** — กลไกจริงในหลอดปล่อยประจุ (ค่าเริ่มต้น)
  - **ดูดกลืนโฟตอน** ที่พลังงานพอดีกับผลต่างระดับ — วาดเป็นคลื่นสีเดียวกับเส้น วิ่งเข้าหาอิเล็กตรอนแล้วหายไปตอนถูกดูดกลืน (เป็นที่มาของสเปกตรัมดูดกลืน)
- แถบคำอธิบายเล่าเป็นขั้น ① ② และบอกกลไกที่เลือกอยู่ · ตรวจแล้วทั้งสองโหมดที่ 656 และ 486 nm · ไม่มี console error

### รอบที่ 2 ของ Lab 87: วาดหลายอะตอมพร้อมกัน (ตามที่เจ้าของเสนอ)
- เจ้าของเสนอ "ให้อิเล็กตรอนสองอนุภาคที่อยู่คนละระดับได้รับแสงแล้วโดดขึ้น แล้วตกกลับคายโฟตอนคนละสี"
- **ข้อแก้ทางฟิสิกส์**: ไฮโดรเจน 1 อะตอมมีอิเล็กตรอน **1 ตัว** จึงทำเป็นอิเล็กตรอน 2 ตัวในอะตอมเดียวไม่ได้ → ทำเป็น **3 อะตอมในหลอดเดียวกัน** แทน (ตรงกับความจริงและอธิบายได้ดีกว่า)
  - อะตอมใหญ่ = เส้นที่กล้องเล็งอยู่ (มีป้าย n ครบ 6 วง) · อีก 2 อะตอมเล็กทำการเปลี่ยนระดับอื่นของบัลเมอร์ พร้อมป้าย "n = 4 → 2 · 486 nm"
  - ทั้ง 3 อะตอมเล่นวงจรกระตุ้น–กระโดด–ตกกลับ–คายโฟตอน โดย**เหลื่อมเฟสกัน** และคายโฟตอน**คนละสี**พร้อมกัน
  - แถบคำอธิบายเพิ่มบรรทัด "ในหลอดมีอะตอมมหาศาลทำพร้อมกัน สเปกตรัมจึงมีหลายเส้นในภาพเดียว" และหมายเหตุว่าไฮโดรเจนมีอิเล็กตรอน 1 ตัว
- รีแฟกเตอร์เป็นฟังก์ชัน `mkUnit()` / `setUnit()` / `stepUnit()` — ใช้วงกลมรัศมี 1 แล้วสเกลเอา จึงไม่ต้องสร้าง geometry ใหม่ทุกครั้งที่เปลี่ยนเส้น
- **ผลตรวจ 5 สถานะ**: 410 → หลัก n = 6 เพื่อนบ้าน 3,4 ✓ · 486 → หลัก n = 4 เพื่อนบ้าน 3,5 ✓ · เส้นกลาง m = 0 · ปรอท · แก๊ส X → ซ่อนอะตอมเพื่อนบ้านทั้งหมด ไม่รั่วคำตอบ ✓ · ไม่มี console error

### ค้างไว้ที่ไหน / ต้องทำต่อ
- มุมมองระดับอะตอมที่เหลือ: **88 · 89 · 91 · 92 · 94 · 95**

## [2026-09-19 03:10] — มุมมอง 🔬 ระดับอะตอม แลปที่ 3: Lab 89 ฟรังก์–เฮิรตซ์ (ชนยืดหยุ่น vs ไม่ยืดหยุ่น)

### ทำอะไรไปบ้าง
- เจ้าของเข้าใจสลับกันว่า "ชนยืดหยุ่น = ปรอทดูดพลังงานได้มาก ทำให้วัดค่าได้น้อยลง" → อธิบายว่ากลับกัน แล้วทำมุมมองให้เห็นภาพ
- เพิ่มปุ่ม **🔬 ระดับอะตอม** ใน Lab 89 — แสดง **2 สถานีเทียบกันข้าง ๆ กัน** ผูกกับ U ที่ตั้งจริง (KE ≈ U − V_contact)
  - **ซ้าย ชนแบบยืดหยุ่น**: อิเล็กตรอนเด้งเปลี่ยนทิศ **ความเร็วเท่าเดิม** · ป้ายบอก "ก่อนชน X eV → หลังชน X eV · เสียเพียง ~µeV (ราว 0.001%)" · อธิบายว่าอะตอมหนักกว่า 370,000 เท่า
  - **ขวา ชนแบบไม่ยืดหยุ่น**: เกิดเฉพาะเมื่อ KE ≥ พลังงานกระตุ้น · อะตอมวาบเป็นสีม่วงแล้วคายโฟตอน (ปรอท = 254 nm) · อิเล็กตรอน**ช้าลงฮวบ** (ความเร็วขาออก ∝ √(KE−E) เห็นได้จากระยะห่างของหางอนุภาค)
  - ถ้า U ยังต่ำกว่าเกณฑ์ → สถานีขวาขึ้น "ยังชนแบบไม่ยืดหยุ่นไม่ได้ · พลังงาน x eV < 4.90 eV" พร้อมเหตุผลว่าพลังงานเป็นระดับไม่ต่อเนื่อง ดูดครึ่ง ๆ กลาง ๆ ไม่ได้ → กระแสยังไม่ตก
- แถบล่างสรุปประเด็นที่เจ้าของถามโดยตรง: **อุณหภูมิเปลี่ยนแค่จำนวนการชน → กระแสและความลึกของหลุม แต่ระยะห่างของหลุมไม่ขยับ** · และย้ำว่า contact potential เลื่อนหลุมแรกไปทั้งชุด จึงต้องวัดระยะห่างระหว่างหลุม
- **ไม่รั่วคำตอบ**: หลอด X ไม่แสดงตัวเลขพลังงานกระตุ้น ไม่แสดง λ ของโฟตอน และไม่บอกจำนวนครั้งที่กระตุ้นได้ (ให้ไปนับหลุมในกราฟเอง) · โฟตอนของหลอด X ใช้สีกลางไม่ผูกกับ λ
- **ผลตรวจ**: U = 3.5 (KE 1.80 < 4.90 → กระตุ้นไม่ได้ ✓) · U = 9.0 (KE 7.50 → 2.60 ✓) · U = 14.0 (12.60 → 7.70 ✓) · U = 18.0 (16.30 → 11.40 · n = 3 ✓) · หลอด X ซ่อนตัวเลขครบ ✓ · ไม่มี console error ใหม่ (400 จาก Firebase มีอยู่เดิมทุกหน้า ตรวจเทียบกับ Lab 90 ที่ไม่ได้แก้แล้ว)
- แก้ระหว่างทำ: ข้อความในป้ายยาวเกินความกว้าง canvas จนถูกตัดหัวท้าย → แตกเป็นบรรทัดสั้นลงและขยาย canvas · โฟตอนที่พุ่งขึ้นมุมขวาบนหลุดกรอบภาพ → รวมระยะของโฟตอนเข้าไปในการคำนวณกรอบ
- เขียนอธิบายประเด็นยืดหยุ่น/ไม่ยืดหยุ่นเพิ่มในแท็บทฤษฎีด้วย

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/89. franck-hertz.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- มุมมองระดับอะตอมที่เหลือ: **88 · 91 · 92 · 94 · 95**

## [2026-09-19 03:50] — มุมมอง 🔬 ระดับอะตอม แลปที่ 4: Lab 88 โฟโตอิเล็กทริก

### ทำอะไรไปบ้าง
- เพิ่มปุ่ม **🔬 ระดับอะตอม** ใน Lab 88 — ภาพตัดขวางแคโทด–แอโนด ผูกกับค่าที่ตั้งจริงทั้ง 3 ตัว (ฟิลเตอร์ · ความเข้ม · V)
  - โฟตอนสีตามฟิลเตอร์วิ่งมาชนผิวโลหะ (มีผลึกอะตอมและอิเล็กตรอนอิสระในเนื้อโลหะ) เกิดประกายที่จุดชน
  - **hf ≥ W** → อิเล็กตรอนหลุดออกมาวิ่งไปหาแอโนด · **hf < W** → ไม่มีอิเล็กตรอนเลย แม้ความเข้ม 100% (ข้อความอธิบายว่า 1 โฟตอนต่อ 1 อิเล็กตรอน สะสมพลังงานจากหลายโฟตอนไม่ได้)
  - **ความต่างศักย์ต้าน V**: ถ้า V > V_s อิเล็กตรอนวิ่งไปได้แค่เศษส่วน V_s/V ของช่องว่างแล้ว**ถูกดันกลับ** (ตรงตามฟิสิกส์) → เห็นชัดว่าทำไมกระแสถึงเป็นศูนย์
  - **ความเข้ม** = จำนวนโฟตอน (1/2/3 ลำตามระดับความเข้ม) → จำนวนอิเล็กตรอนมากขึ้น แต่ระยะที่วิ่งไปได้เท่าเดิม = KE ต่อตัวไม่เปลี่ยน
- **ไม่รั่วคำตอบ**: ไม่แสดงค่า W หรือชนิดโลหะเป็นตัวเลขเลย เขียนเป็นสัญลักษณ์ KE = hf − W และบอกว่า W คือค่าที่ต้องหา
- **ผลตรวจ**: 365 nm + V 0.30 (อิเล็กตรอนถึงขั้ว ✓) · 365 nm + V 2.20 > V_s 1.257 (ไปได้ 57% แล้วกลับ ✓) · 435.8 nm + V 2.20 (ไปได้ 15% ✓) · 650 nm (hf 1.907 < W → ไม่มีอิเล็กตรอนเลย ✓) · ความเข้ม 25% → 1 ลำ / 100% → 3 ลำ ✓ · ไม่มี console error ใหม่
- แก้ระหว่างทำ: ชื่อตัวแปร `slab`/`anode` ชนกับของเดิมในไฟล์ (syntax error) → เปลี่ยนเป็น `aSlab`/`aAnode` · ข้อความในแถบยาวเกินกรอบ → ย่อให้สั้นลง
- เขียนอธิบายในแท็บทฤษฎีด้วย

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/88. photoelectric-planck.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- มุมมองระดับอะตอมที่เหลือ: **91 · 92 · 94 · 95**

## [2026-09-19 04:25] — มุมมอง 🔬 ระดับอะตอม แลปที่ 5: Lab 91 เลี้ยวเบนอิเล็กตรอน (แบรกก์)

### ทำอะไรไปบ้าง
- เพิ่มปุ่ม **🔬 ระดับอะตอม** ใน Lab 91 — ภาพการสะท้อนแบบแบรกก์จากระนาบอะตอม 3 ระนาบ ผูกกับค่าที่ตั้งจริง
  - คลื่นอิเล็กตรอน (สีฟ้า) วิ่งเข้ามา สะท้อนจากระนาบที่ 1 (จุด A) และทะลุไปสะท้อนที่ระนาบที่ 2 (จุด B) ออกไปขนานกัน (สีเหลือง) — คลื่นขาออกเฟสตรงกันเพื่อสื่อการเสริมกัน
  - เส้นตั้งฉากประ + **ส่วนสีชมพู = เส้นทางที่ต่างกัน 2d sin θ** (วาดเป็นหลอดหนาให้เห็นชัด) พร้อมป้ายกำกับ
  - แถบข้อมูลคำนวณจริง: λ = h/√(2meV) จาก V ที่ตั้ง · d ของระนาบที่เลือก · θ = arcsin(λ/2d) · และยืนยันว่า 2d sin θ = λ พอดี
  - ตรวจตัวเลข: 4.0 kV → λ 19.39 pm · กราไฟต์ d 213 pm → θ 2.61° · 2d sinθ = 19.39 pm ✓ ตรงสูตร · 2.5 kV → λ 24.53 pm ✓
- **ไม่รั่วคำตอบ**: ผลึกปริศนา X แสดง "ระยะระนาบ d = ?" และระบุว่าภาพใช้ระยะสมมุติ ไม่บอก d หรือ θ จริง
- เขียนกำกับไว้ชัดว่า**มุม θ ในภาพขยายไว้** (ของจริง 2–5°) ทั้งในฉากและในแท็บทฤษฎี

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/91. electron-diffraction.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- มุมมองระดับอะตอมที่เหลือ: **92 · 94 · 95**

## [2026-09-19 05:05] — มุมมอง 🔬 ระดับอะตอม แลปที่ 6: Lab 92 รังสีเอกซ์ (เบรมส์ชตราลุง + เส้น K)

### ทำอะไรไปบ้าง
- เพิ่มปุ่ม **🔬 ระดับอะตอม** ใน Lab 92 — แสดง **2 กระบวนการที่เกิดพร้อมกันในเป้าเดียวกัน** ผูกกับเป้าและ kV ที่ตั้งจริง
  - **ซ้าย เบรมส์ชตราลุง**: อิเล็กตรอนวิ่งเข้าใกล้นิวเคลียส เบนตามเส้นทางโค้ง แล้วคายโฟตอนตอนเฉียดใกล้ที่สุด · ป้ายบอกว่าตัวที่เสียพลังงานหมดในครั้งเดียวให้โฟตอนพลังงานสูงสุด = kV keV → λ_min (ขอบคมในกราฟ)
  - **ขวา เส้นลักษณะเฉพาะ K**: อะตอมมีชั้น K และ L (วงประพร้อมป้าย) · อิเล็กตรอนพุ่งเข้ามากระแทกอิเล็กตรอนชั้น K หลุดออก → เกิดช่องว่างสีเหลือง → อิเล็กตรอนชั้น L ตกลงมาเติม → คายโฟตอน Kα วิ่งออกไป
  - แถบล่างสรุปประเด็นสำคัญ: **ขอบคมขึ้นกับ kV เท่านั้น** (ใช้หา h) · **ยอดแหลมขึ้นกับธาตุของเป้าเท่านั้น** (ใช้หา Z ด้วยมอสลีย์)
  - มีสาขาสำหรับกรณี kV ไม่พอกระแทกอิเล็กตรอนชั้น K (ใช้ `kAllowed()` ตัวเดียวกับแบบจำลองหลัก) → ขึ้นข้อความว่าเห็นแต่สเปกตรัมต่อเนื่อง
- **ไม่รั่วคำตอบ**: ไม่แสดงตัวเลข λ_min และ λ/พลังงานของ Kα เลย (เป็นค่าที่ต้องวัดจากมุมแบรกก์) · เป้าปริศนาแสดง "เป้าปริศนา X (Z = ?)"
- **ผลตรวจ**: Cu 30 kV ✓ · Mo 20 kV ✓ · เป้า X 35 kV (ซ่อน Z ✓ · โฟตอน Kα ออกมาถูกจังหวะ) · ไม่มี console error ใหม่
- แก้ระหว่างทำ: ป้ายเป้าขึ้นว่า "เป้า เป้า X" (ชื่อซ้ำ) → แก้เป็น "เป้าปริศนา X (Z = ?)"

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/92. xray-bragg-moseley.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- มุมมองระดับอะตอมที่เหลือ: **94 · 95**

## [2026-09-19 05:45] — มุมมอง 🔬 ระดับอะตอม แลปที่ 7: Lab 94 รังสีวัตถุดำ

### ทำอะไรไปบ้าง
- เพิ่มปุ่ม **🔬 ระดับอะตอม** ใน Lab 94 — 2 ฝั่งในภาพเดียว ผูกกับแหล่ง/ระดับกำลังที่เลือกจริง
  - **ซ้าย**: ผลึกอะตอม 25 ตัวสั่นด้วยแอมพลิจูด ∝ ฟังก์ชันของ T · โฟตอนพุ่งออกแบบสุ่มทุกทิศ โดย**สุ่มความยาวคลื่นตามการแจกแจงพลังค์จริงที่อุณหภูมินั้น** (rejection sampling จากฟังก์ชัน `planck()` ตัวเดียวกับแบบจำลองหลัก) แล้วแปลงเป็นสี · อัตราการปล่อยโฟตอน ∝ T⁴ จึงเห็นชัดว่าร้อนขึ้น = โฟตอนถี่ขึ้นมาก
  - **ขวา**: เส้นโค้งพลังค์ของอุณหภูมิที่ตั้งอยู่ ระบายสีใต้กราฟตามความยาวคลื่น + เส้นประที่ยอด (λ_max) · สำหรับไส้หลอดวาด**เส้นจางของอีก 4 ระดับ**เทียบให้เห็นว่ายอดเลื่อนและพื้นที่โต
- **ไม่รั่วคำตอบ**: ไม่มีตัวเลขบนแกนกราฟ · ไม่บอก T และ λ_max · แหล่งปริศนาไม่วาดเส้นเทียบของระดับอื่น และปรับสเกลกับยอดของตัวเองจึงเทียบขนาดไม่ได้
- **ผลตรวจ**: ระดับ 1 (1600 K) กราฟแบนเตี้ย โฟตอนน้อยมาก · ระดับ 5 (2800 K) ยอดสูงและเลื่อนซ้าย โฟตอนถี่ · แหล่งปริศนา (5680 K) ยอดไปทางน้ำเงิน ไม่แสดง T ✓ · ไม่มี console error ใหม่
- แก้ระหว่างทำ: อะตอมกระโดดไปทับกราฟเพราะลืมบวกออฟเซตของสถานี (`o.x` เป็นพิกัดในสถานี ไม่ใช่พิกัดโลก) → แก้เป็น `SXA+o.x`

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/94. blackbody-wien.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- มุมมองระดับอะตอมที่เหลือ: **95** (แลปสุดท้ายของชุด)

## [2026-09-19 06:25] — มุมมองระดับอะตอมแลปสุดท้าย: Lab 95 (ครบทั้งชุด VPL04)

### ทำอะไรไปบ้าง
- เพิ่มปุ่ม **⚛️ ระดับอะตอม** ใน Lab 95 — 2 ฝั่ง แสดงว่าทั้งครึ่งชีวิตและการดูดกลืนเป็น**กระบวนการสุ่มแบบเดียวกันในเชิงคณิตศาสตร์**
  - **ซ้าย การสลายตัว**: นิวเคลียส 64 ตัว แต่ละตัวสุ่มสลายด้วยความน่าจะเป็นเท่ากันต่อเฟรม (p = 1 − 2^(−dt/T½ ในภาพ)) · ตัวที่สลายหรี่ลงและปล่อยอนุภาคออกไป · ป้ายนับ "เหลือ N / 64" แบบเรียลไทม์ · เมื่อหมดจะเริ่มใหม่อัตโนมัติ
  - **ขวา การดูดกลืน**: ต้นกำเนิด → แผ่นดูดกลืน (**ความกว้างของแผ่นในภาพ ∝ ความหนาที่ตั้งจริง**) → หลอด GM · อนุภาคแต่ละตัวสุ่มว่ารอดหรือไม่ด้วยความน่าจะเป็น e^(−μx) **จาก μ จริงของคู่ (ชนิดรังสี, วัสดุ)** · ตัวที่ถูกดูดกลืนหยุดที่ความลึกสุ่มตามการแจกแจงเลขชี้กำลังแบบตัดปลาย (สีแดง) ตัวที่รอดทะลุไปถึงหลอด (สีเขียว)
- **ไม่รั่วคำตอบ**: อัตราการสลายในภาพใช้ครึ่งชีวิตสมมุติ 6 วินาที (เขียนกำกับไว้) ไม่ผูกกับ T½ จริงของตัวอย่าง X · ไม่แสดง μ · ความหนาครึ่งค่า · T½ · และไม่ระบุชนิดรังสีของแหล่งปริศนา Y
- **ผลตรวจ**: Cs-137 + ตะกั่ว 6 mm (โอกาสรอด 0.499 → เขียว/แดงราวครึ่งต่อครึ่ง ✓) · Am-241 + กระดาษ 0.5 mm (โอกาสรอด 3.8×10⁻¹¹ → แดงทั้งหมด หยุดที่หน้าแผ่น ✓) · แหล่ง Y + ไม่มีแผ่น (ทะลุหมด ไม่บอกชนิดรังสี ✓) · แผงนับถอยหลังและรีเซ็ตเองได้ ✓ · ไม่มี console error ใหม่

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/95. half-life-absorption.html`

### 🎉 สรุป: มุมมองระดับอะตอมครบทั้งชุด VPL04 แล้ว (9 แลป)
| แลป | สิ่งที่แสดงในมุมมองอะตอม |
|---|---|
| 87 | 3 อะตอมไฮโดรเจนเล่นวงจรกระตุ้น–กระโดด–ตกกลับ–คายโฟตอนคนละสี · สลับกลไกกระตุ้นได้ |
| 88 | โฟตอนชนอิเล็กตรอนในโลหะ · ต่ำกว่าเกณฑ์ไม่หลุดเลย · V ต้านทำให้วิ่งไปได้สั้นลง |
| 89 | ชนยืดหยุ่น (เด้ง ความเร็วเท่าเดิม) เทียบชนไม่ยืดหยุ่น (เสียพลังงานเป็นก้อน) |
| 91 | การสะท้อนแบรกก์จาก 2 ระนาบ · เส้นทางต่างกัน 2d sin θ |
| 92 | เบรมส์ชตราลุง (ขอบคม) เทียบเส้นลักษณะเฉพาะ Kα (ยอดแหลม) |
| 93 | ลำอนุภาคขนานยิงเข้าอะตอม ส่วนใหญ่ทะลุตรง เส้นที่เฉียดนิวเคลียสเด้งกลับ |
| 94 | อะตอมสั่นคายโฟตอนสีตามการแจกแจงพลังค์ + เส้นโค้งพลังค์เทียบหลายอุณหภูมิ |
| 95 | นิวเคลียสสลายตัวแบบสุ่ม + อนุภาคถูกดูดกลืนในแผ่นตามความน่าจะเป็น e^(−μx) |

### หมายเหตุ / รูปแบบที่ใช้ซ้ำได้ทุกไฟล์
- `P.atom` เป็นกลุ่มแยก · `setAtomMode()` สลับ `visible` ของลูกฉากทั้งหมด (ยกเว้นไฟ) · `update3D()` แยกสาขาออกตั้งแต่ต้นเมื่ออยู่โหมดอะตอม · `atomSig` เทียบค่าที่ตั้งไว้เพื่อ rebuild · `hdStart()` คืน false ในโหมดอะตอม
- ป้ายทั้งหมดเป็น CanvasTexture วางในฉาก (ไม่มีกล่อง HTML ทับภาพ 3D) · คำนวณ bounding box แล้วเลื่อนกลุ่มให้อยู่กลางภาพและ fit กล้องอัตโนมัติ
- **กติกาสำคัญ**: ค่าที่เป็นคำตอบของแลป (ค่าปริศนาและปริมาณที่ต้องวัด) ต้องไม่ปรากฏเป็นตัวเลขในฉากอะตอม — แสดงพฤติกรรมได้ แต่ไม่บอกตัวเลข

## [2026-09-22 01:10] — แก้ปุ่มหมุน Lab 89/91 · สร้าง Lab 96–97 (การหมุน) ใน VPL01

### ทำอะไรไปบ้าง
- **ข้อ 2 (บั๊กลาก stepHand ใน 87–94)**: ตรวจแล้วแก้ไปตั้งแต่ commit 4cb4220 (2026-09-18) แต่เจอบั๊กแบบเดียวกันที่**ปุ่มหมุน (knob)** — ปัดค่าทุกครั้งที่เมาส์ขยับ หมุนช้า ๆ ค่าไม่เปลี่ยนเลย
  - Lab 89 (แรงดันเร่ง U) ต้องหมุน > 0.5° ต่อครั้งค่าถึงขยับ · Lab 91 (kV) ต้อง > 6° ต่อครั้ง
  - แก้ให้สะสมมุมใน `HD.u` แล้วค่อยปัดตอนเขียนค่า (มี resync ถ้าค่าถูกเปลี่ยนจากที่อื่น) · ทดสอบหมุน 0.2°×100 ครั้ง: Lab 89 ได้ 5.0 → 7.0 V ตรงทฤษฎี · Lab 91 3.0 → 3.2 kV ✓ · Lab 88 ปัดที่ 0.001 V ไม่มีปัญหา
- **ข้อ 4 ชุดการเคลื่อนที่แบบวงกลม ข้อ 9–10** เจ้าของเลือกใส่ **VPL01** → เลขแลปต่อจากทั้งเว็บ = **Lab 96, 97** (แบบเดียวกับ Lab 42–44 ที่อยู่ใน VPL01) · access `vlab:vpl01:lab-96/97` · topic `projectile` (วงกลม) · ม.4 · 3D ล้วน
  - **Lab 96 โมเมนต์ความเฉื่อย: คานหมุนกับตุ้มถ่วง** — ข้อ 9 เดิมเป็น "rolling race" แต่ซ้ำกับ Lab 73 (ลูกตัน/กลวงกลิ้งลงราง) จึงทำเป็นแลปวัด I แบบคลาสสิกแทน
    - ตุ้มแขวน (20–250 g) ตกดึงเชือกที่พันรอบรอกขั้นบันได (r = 1/2/3 cm) ผ่านรอกเล็กขอบโต๊ะ · คานอะลูมิเนียมมีสเกล mm + ตุ้มคู่เลื่อนได้ (ไม่มีตุ้ม / ทองเหลือง 200 g / ❓ X) · ไม้เมตรแนวดิ่ง + ประตูแสงลากได้ + ตัวจับเวลา 0.001 s
    - นักเรียนอ่าน d (เข็มแดงใต้ตุ้มบนสเกลคาน) · h (ขีดแดงประตูแสงบนไม้เมตร) · t (จอจับเวลา) → a = 2h/t², α = a/r, τ = m(g−a)r
    - กราฟ τ–α ความชัน = I จุดตัดแกน = τ_f (แรงเสียดทานที่แกน) · กราฟ I–d² ความชัน = 2M · ตรวจคำตอบ M_X และ I₀ ของคานเปล่า
    - ปริศนาสุ่มต่อการเปิดหน้า: M_X (110–330 g ไม่ใกล้ 200) · I₀ · τ_f · ถ้า mgr ไม่ชนะแรงเสียดทานสถิต คานไม่หมุน
    - ลากตุ้มบนคาน (เข้า-ออกพร้อมกันสองข้าง) และลากประตูแสงได้ (หน่วง ~0.28 s เก็บค่าต่อเนื่อง ไม่มี dead zone)
    - **ผลตรวจ**: t ตรงสูตรปิด (3.158 s) · ทดลองเต็มชุดโหมดอัตโนมัติ: I จากความชัน 0.013863 เทียบจริง 0.01386 · τ_f 2.38 vs 2.42 ×10⁻³ · M ทองเหลือง 199.8 g · M_X 259 g vs 260 g ✓ · ลากด้วยนิ้ว (375 px) ✓ · ไม่มี console error
  - **Lab 97 การอนุรักษ์โมเมนตัมเชิงมุม: วางวงแหวนบนจานหมุน**
    - จานอะลูมิเนียม 1.500 kg R 12.0 cm บนลูกปืน · ปั่นด้วยปุ่ม 🌀 หรือ**ลากขอบจานแล้วปล่อย** (ได้ความเร็วตอนปล่อย) · แขนจับวัตถุ 3 ตำแหน่ง d = 0 / 2.5 / 5.0 cm · วัตถุ: วงแหวนเหล็ก 1.400 kg · แท่งเหล็ก 0.600 kg ยาว 24 cm · ❓ วงแหวน X
    - ประตูแสงใต้ขอบจาน + **จอบันทึกคาบทุกรอบ** (0.0001 s) หยุดเองเมื่อครบ 6 รอบหลังวาง · นักเรียนต้องเลือก T₁ = รอบสุดท้ายก่อนวาง และ T₂ = รอบแรกหลังนิ่ง (ข้ามรอบที่คร่อมจังหวะวาง)
    - ฟิสิกส์: ตกจาก 3 cm → ไถล μ = 0.35 ถ่าย L จากจานไปวัตถุจนหมุนเท่ากัน · ลูกปืนมีแรงเสียดทานเล็กน้อย
    - ตาราง: L หลัง/ก่อน · Ek หลัง/ก่อน · I ทดลอง = I_จาน(T₂/T₁ − 1) เทียบสูตร · M_X · กราฟ L หลัง–L ก่อน และ I–d² (ทฤษฎีบทแกนขนาน)
    - **ผลตรวจ**: L หลัง/ก่อน 99.4–99.8% · Ek เหลือ 68% (ทฤษฎีหาย 31.2%) · แท่ง I 2.92 vs 2.88 ×10⁻³ · ความชัน I–d² 1.42 kg (จริง 1.40) · M_X 1.955 vs 1.938 kg ✓ · ลากปั่นจาน ✓
- ลงทะเบียน: `labs_data.py` · `VLAB_SERIES` vpl01 ใน kp-auth.js + admin.html · `LAB_LIST` admin · การ์ด + ภาพพรีวิว canvas (`vpl-inertia`, `vpl-angmom`) ใน virtual-physics-lab-01.html (25 → 27) · build แล้ว (หน้าแรก 98 แลป) · bump kp-auth เป็น `?v=20260922`

### ไฟล์ที่แก้
- `Virtual Physics Lab 04/89. franck-hertz.html`, `91. electron-diffraction.html` — ปุ่มหมุนสะสมค่าต่อเนื่อง
- `Virtual Physics Lab 01/Mechacnics/96. moment-of-inertia-rotating-bar.html` — ใหม่
- `Virtual Physics Lab 01/Mechacnics/97. angular-momentum-disk-ring.html` — ใหม่
- `_admin/labs_data.py`, `_admin/admin.html`, `kp-auth.js`, `virtual-physics-lab-01.html`
- สร้างใหม่จาก build: `index.html`, `virtual-lab.html`, `library.html` · ทุกไฟล์ที่โหลด kp-auth (?v=20260922)

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ✅ push ขึ้นเว็บแล้ว (2026-09-22) — ตรวจเว็บจริง: Lab 96, 97, หน้า VPL01 (การ์ดใหม่), หน้าแรก 98 แลป, ปุ่มหมุน Lab 91 ตัวใหม่ ✓
- ชุดวงกลมครบ 10 ข้อแล้ว (62–69 + 96–97)
- VPL03 หน้า catalog — พักไว้ตามที่เจ้าของสั่ง

### หมายเหตุ
- Lab 42–44 อยู่ในโฟลเดอร์ VPL01 แต่ `data-access`/guard ในไฟล์เป็น `vlab:vpl02:lab-4x` ขณะที่ labs_data เป็น `vlab:vpl01:lab-4x` และลิงก์ topbar ใช้ `../` (ควรเป็น `../../`) — ไม่ได้แก้ในรอบนี้
- ไฟล์ใหม่ใน VPL01 ต้องใช้ path `../../` (ลึก 2 ชั้น)

## [2026-09-22 03:20] — เปิดชุดใหม่ VPL05 กลศาสตร์ของไหล · Lab 98–99

### ทำอะไรไปบ้าง
- เจ้าของเลือกทำ **กลศาสตร์ของไหล** และสั่ง "เปิด 05" → โฟลเดอร์ใหม่ `Virtual Physics Lab 05/` · access `vlab:vpl05:*` · เลขแลปต่อจากทั้งเว็บ
- แผนที่เสนอ (เจ้าของยังไม่ได้ขอแก้): 98 ความดัน–ความลึก · 99 แมนอมิเตอร์/บารอมิเตอร์ · 100 เครื่องอัดไฮดรอลิก (พาสคัล) · 101 แรงลอยตัว (อาร์คิมิดีส) · 102 ไฮโดรมิเตอร์ · 103 ความตึงผิว · 104 ความหนืด (สโตกส์) · 105 สมการความต่อเนื่อง · 106 แบร์นูลลี
- **ต่อสายชุดใหม่**: `VLAB_SERIES.vpl05` + presets member/pro/premium + ANONYMOUS_ACCESS_FALLBACK + legacy loop ใน kp-auth.js และ admin.html (รวม preset "all" และค่าเริ่มต้นการ์ดผู้เข้าชม) · protect_new_file.py (access, is_sim, is_vlab, guard → virtual-lab.html) · labs_data: `V5`, topic ใหม่ `fluid` 💧 (อยู่กลุ่มกลศาสตร์), SERIES vpl05 · CLAUDE.md
- **Lab 98 ความดันในของเหลว** — ถังแก้วลึก 50 cm · ของเหลว น้ำ/น้ำเกลือ 1200/น้ำมันพืช 920/❓X · หัววัดกรวยแผ่นยางหันได้ 3 ทิศ ลากขึ้นลง-ซ้ายขวาได้ · อ่านความลึกจาก**สเกลบนก้าน (0 = กลางแผ่นยาง) ตรงระดับผิว** · เครื่องวัดความดันสัมบูรณ์ 0.01 kPa แกว่ง ±0.01 · กราฟ P–h ทุกของเหลว · ปริศนา ρ_X และ P₀ ของวัน
  - ผลตรวจ: fit ได้ ρ 1000/1198/921 และ X 1338 (จริง 1340) · P₀ 101.461 (จริง 101.46) ✓ · สเกลที่ผิวอ่าน 20.0 ตรง H=20 ✓
- **Lab 99 แมนอมิเตอร์และบารอมิเตอร์** — หลอดตัว U (น้ำ/ปรอท) + วาล์ว 3 ทาง: อากาศ / ขวด 1000 mL + กระบอกฉีดยา 20 mL (เริ่ม 10.0 mL ทุกครั้งที่ปิดวาล์ว, กฎบอยล์ + ปริมาตรที่ของเหลวเลื่อน) / ถังแก๊ส X · ของเหลวแกว่งหน่วงก่อนนิ่ง · กันดันจนล้นหลอด · บารอมิเตอร์ทอร์ริเชลลี หลอด 95 cm เอียง 0–60° (เอียงมากปรอทเต็มหลอด) · ตัวเลื่อนเส้นเล็งแดงบนไม้เมตร · สถานที่: ระดับน้ำทะเล / ดอยอินทนนท์ 2565 m / ❓X (P = P₀e^(−z/8400))
  - ผลตรวจ: ถัง X น้ำ 2.411 · ปรอท 2.399 (จริง 2.42) ✓ · สถานที่ X 82.63 (จริง 82.70) ✓ · เอียง 20° h เท่าเดิม · 40° เต็มหลอด ✓
  - แก้ระหว่างทำ: เดิมอ้างว่าจุดน้ำกับปรอทจากกระบอกฉีดยาอยู่บนเส้นเดียวกัน — ไม่จริง (ของเหลวเลื่อนทำให้ปริมาตรแก๊สเปลี่ยน ~20%) → เปลี่ยนให้เทียบน้ำกับปรอทด้วยถัง X (ความดันคงที่) แทน · ตัวเลขซ้ำที่รอยต่อสเกล (75/75, 28/28) แก้ทั้ง 98 และ 99
- build แล้ว: 100 แลป · bump kp-auth `?v=20260922-2`

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 05/98. liquid-pressure-depth.html`, `99. manometer-barometer.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/protect_new_file.py`, `_admin/labs_data.py`, `CLAUDE.md` · build: `index.html`, `virtual-lab.html`, `library.html` · ทุกไฟล์ที่โหลด kp-auth

### ค้างไว้ที่ไหน / ต้องทำต่อ
- **ยังไม่ได้ push** — รอเจ้าของดู 98–99
- **หลัง push เจ้าของต้องติ๊ก VPL05 ในการ์ด "🌐 สิทธิ์ผู้เข้าชมทั่วไป" ของแอดมิน** ไม่อย่างนั้นผู้ไม่ล็อกอินจะถูกเด้งไป virtual-lab.html (ทดสอบในเครื่องแล้วเด้งจริง เพราะ Firestore `settings/public` ยังไม่มี vpl05)
- ถัดไป: Lab 100–101

## [2026-09-22 03:40] — แก้จอเครื่องวัดความดัน Lab 98

### ทำอะไรไปบ้าง
- เจ้าของแจ้ง "เครื่องวัดความดันไม่เห็นสเกล" → จอแสดงผลถูกวางจมอยู่ในกล่อง (คำนวณตำแหน่งหน้ากล่องผิด ลืมว่ากล่องหมุน −0.2 rad และลึก 4 cm) เห็นแต่กล่องสีเทา
- ย้ายจอไปแนบหน้ากล่อง · ตรวจแล้วอ่านได้ชัด (102.75 kPa ที่ลึก 20 cm) · จอของ Lab 96/97 วางถูกอยู่แล้ว

### ไฟล์ที่แก้
- `Virtual Physics Lab 05/98. liquid-pressure-depth.html`

## [2026-09-22 04:10] — ลากอุปกรณ์ด้วยมือใน Lab 98–99

### ทำอะไรไปบ้าง
- เจ้าของขอ "ทั้งสองแลปเอามือลากอุปกรณ์การทดลอง" · ทดสอบด้วยเมาส์จริงพบว่า **ลากเร็ว ๆ แล้วปล่อย อุปกรณ์แทบไม่ขยับ** เพราะอุปกรณ์ตามมือแบบหน่วง และหยุดทันทีที่ปล่อยเมาส์
- แก้ทั้งสองแลป: ปล่อยเมาส์แล้ว**อุปกรณ์เคลื่อนต่อจนถึงจุดที่ปล่อย** (`HD.fin`) · กดปุ่มปรับค่า/เปลี่ยนของเหลว/รีเซตจะยกเลิกการเคลื่อนค้าง (`cancelHand()`) · Lab 99 ถ้าดันลูกสูบจนของเหลวจะล้นก็หยุดเอง
- Lab 99 เพิ่ม: **แตะด้ามวาล์วในภาพเพื่อหมุนวาล์ว** (เดิมเป็นปุ่มอย่างเดียว) มีระยะแตะกว้างแบบเดียวกับชิ้นอื่น · มุมมอง 💉 กระบอกฉีดยา กว้างขึ้นให้เห็นด้ามลูกสูบ · มุมเอียงหลอดเป็นค่าต่อเนื่อง (แสดง 1 ตำแหน่งทศนิยม)
- ผลตรวจด้วยการลากเมาส์จริงในเบราว์เซอร์: 98 หัววัด 10 → 23.2 cm และเลื่อนข้าง 4.7 cm (กล้องไม่หมุนตาม) · 99 แตะวาล์ว อากาศ → ขวด ✓ · ลูกสูบ 10 → 3.8 mL หลอดตัว U ตอบสนอง Δh 5 cm ✓ · เอียงหลอด 11.5° ✓ · ตัวเลื่อน 70 → 66.6 cm ✓

### ไฟล์ที่แก้
- `Virtual Physics Lab 05/98. liquid-pressure-depth.html`, `99. manometer-barometer.html`

### หมายเหตุ
- แลปเก่า (62–97) ยังใช้แบบ "หยุดทันทีที่ปล่อย" อยู่ — ถ้าเจ้าของเจอปัญหาเดียวกันให้ใช้รูปแบบ `HD.fin` นี้
- ทดสอบ Lab ใน VPL05 บนเครื่องต้องทำสำเนาชั่วคราวที่ปิด `kpPageAccess` เพราะ guard เด้งออก (ยังไม่ได้ติ๊ก VPL05) · พิกัดของเครื่องมือคลิกเป็นกรอบ 800 px ต้องหาร innerWidth/800

## [2026-09-22 05:30] — Lab 100 เครื่องอัดไฮดรอลิก · Lab 101 แรงลอยตัว (VPL05)

### ทำอะไรไปบ้าง
- push Lab 98–99 ขึ้นเว็บแล้ว (ตรวจเว็บจริง 200 ทั้งคู่ · kp-auth/admin รู้จัก vpl05)
- **สิทธิ์ผู้ชมทั่วไปยังไม่ได้ตั้ง**: Firestore `settings/public.anonymous_access` = demo + vpl01–04 (ยังไม่มี vpl05) · เบราว์เซอร์ของ Claude ไม่ได้ล็อกอิน และ Claude in Chrome ไม่ได้เชื่อมต่อ → เจ้าของต้องติ๊ก VPL05 เองในการ์ด 🌐 ของแอดมิน
- **Lab 100 หลักของพาสคัล: เครื่องอัดไฮดรอลิก** — ลูกสูบเล็ก 2/3/4 cm · ลูกสูบใหญ่ 10 cm หรือ ❓X (สุ่ม 7–14 cm) · ตุ้ม 0–40 kg (แผ่น 10/5/1 kg ซ้อน) · **ลากด้ามเครื่องวัดแรงลง** (ดึงขึ้นไม่ได้ มีวาล์วกันกลับ · แตะวาล์วเพื่อปล่อยลง) · เครื่องวัดแรงดิจิทัลมี HOLD = แรงเฉลี่ยขณะดัน (ข้าม 0.35 s แรก) · **มาตรวัดความดันแบบเข็ม 0–120 kPa ขีดละ 1 kPa** · ไม้บรรทัด d₁ (1 mm) และ d₂ (0.5 mm) · แรงเสียดทานซีล f₁ 0.4 N, f₂ 3 N ทำให้กราฟ F₁–F₂ มีจุดตัดแกนแต่ความชันยัง = A₁/A₂
  - ผลตรวจ: HOLD 8.36 N = ทฤษฎี · เข็มชี้ 25 kPa ตรง mg/A₂ · D_X จากระยะ 13.09 (จริง 13.2) · แนะนำนักเรียนใช้ความชันกราฟ (แม่นกว่า)
- **Lab 101 แรงลอยตัว: อาร์คิมิดีส** — เครื่องชั่งสปริงแบบเข็ม 0–6 N ขีดละ 0.05 N (สปริงยืด 2 cm/N · หาจุดสมดุลจริง วัตถุลอยขึ้นเมื่อได้แรงลอยตัว) · ลากแขนขาตั้ง/เครื่องชั่งลงจุ่มวัตถุ · ถ้วยยูเรกาล้นลงกระบอกตวง 100 mL ขีดละ 1 mL (ติดตามปริมาตรในถ้วยจริง: ยกออกหลังล้นแล้วระดับต่ำกว่าปาก ต้องเติมใหม่) · ตรวจจับแตะก้นถ้วย · วัตถุ อะลูมิเนียม/ทองเหลือง/❓X · ของเหลว น้ำ/น้ำเกลือ/❓Y
  - ผลตรวจ: V ที่ล้น = ปริมาตรวัตถุพอดี (75.4) · ρ_X 6340 = จริง · ρ_Y 1297 (จริง 1295) · เข็มอ่าน 1.25 N ตรง 1.256 · กระบอกตวงอ่าน 75
- ลงทะเบียน: labs_data · VLAB_SERIES.vpl05 (kp-auth + admin) · LAB_LIST · protect · bump `?v=20260922-4` · build (หน้าแรก 102 แลป)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 05/100. hydraulic-press-pascal.html`, `101. buoyancy-archimedes.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py` · build: `index.html`, `virtual-lab.html`, `library.html` · ทุกไฟล์ที่โหลด kp-auth

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ✅ push 100–101 ขึ้นเว็บแล้ว (ตรวจเว็บจริง: ทั้งสองแลป 200 · หน้าแรก 102 แลป · kp-auth มี lab-101)
- **เจ้าของต้องติ๊ก VPL05 ในการ์ด 🌐 สิทธิ์ผู้เข้าชมทั่วไป** (ตรวจได้ด้วย REST: firestore.googleapis.com/v1/projects/kp-science-f11ff/databases/(default)/documents/settings/public)
- ถัดไป: 102 ไฮโดรมิเตอร์ · 103 ความตึงผิว

### หมายเหตุ
- heredoc ของ python ที่มีตัวห้อย ₁ ₂ บางครั้งพังด้วย "Non-UTF-8 code" → เขียนสคริปต์เป็นไฟล์ใน scratchpad แทน

## [2026-09-22 06:40] — Lab 102 ไฮโดรมิเตอร์ · Lab 103 ความตึงผิว (VPL05)

### ทำอะไรไปบ้าง
- **Lab 102 ไฮโดรมิเตอร์และการลอย** — หลอดทดลองก้นกลม R 1.00 cm ยาว 22 cm (6.00 g) + ลูกตะกั่ว 2.00 g (0–20 ลูก) · สเกลกระดาษในหลอด 0 = ปลายก้น · ของเหลว น้ำ/น้ำเกลือ 1200/น้ำมัน 920/แอลกอฮอล์ 790/❓Z · **ลากหลอดกดลงหรือยกขึ้นแล้วปล่อย หลอดกระเพื่อมด้วยแรงลอยตัวจริง (+แรงหน่วง) กลับมาลอยนิ่ง** · แตะจานลูกตะกั่วเพื่อหย่อนเพิ่ม · หนักเกินจมมิด · V_จม ของก้นครึ่งทรงกลม → กราฟ h–m ตัดแกนที่ R/3
  - ผลตรวจ: fit น้ำ 999 · Z 868 (จริง 869) · จุดตัดแกน 0.31 (≈R/3) · คำทำนาย 10 ลูกในแอลกอฮอล์ = 10.81 cm ตรงค่าจำลอง
- **Lab 103 ความตึงผิว (ห่วงลวด)** — ห่วง r 1.50/2.50 cm แขวนเซนเซอร์แรง 0.1 mN (ค่าสด + PEAK) · จานบนแท่นยก **ลากขึ้นลงได้** + ปุ่มละเอียด 0.5 mm + ลดช้าอัตโนมัติ 0.5 mm/s · ฟิล์มยืดแล้วขาด F = W + γ4πr(1−(1−z/z_max)²) · **ลดเร็วเกิน ~0.6 mm/s ฟิล์มขาดก่อน ค่า PEAK ต่ำกว่าจริง** (สอนเทคนิค) · ของเหลว น้ำ 72.8/น้ำสบู่ 30/เอทานอล 22.3/❓X
  - ผลตรวจ: ลดช้าได้ ΔF = ทฤษฎีพอดี (13.72, 22.87 mN) · ลด 2 cm/s ได้ 12.14 (ต่ำ 11%) · X 40.4–40.8 (จริง 40.4)
- ลงทะเบียน labs_data · VLAB_SERIES.vpl05 · LAB_LIST · protect · bump `?v=20260922-5` · build (หน้าแรก 104 แลป)
- เช็ก Firestore อีกครั้ง: สิทธิ์ผู้ชมทั่วไป**ยังไม่มี vpl05**

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 05/102. hydrometer-flotation.html`, `103. surface-tension-ring.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py` · build + ทุกไฟล์ที่โหลด kp-auth

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ✅ push 102–103 ขึ้นเว็บแล้ว (ตรวจเว็บจริง 200 ทั้งคู่ · หน้าแรก 104 แลป) · สิทธิ์ผู้ชมทั่วไปยังไม่มี vpl05
- ถัดไป: 104 ความหนืด (สโตกส์) · 105 สมการความต่อเนื่อง · 106 แบร์นูลลี

## [2026-09-22 08:00] — Lab 104 ความหนืด · Lab 105 สมการความต่อเนื่อง (VPL05)

### ทำอะไรไปบ้าง
- **Lab 104 ความหนืด (ลูกตก · สโตกส์)** — กระบอกของเหลวสูง 50 cm สเกล mm · **ลากวงแหวนประตูแสง 2 วง** (แดง/น้ำเงิน) · แตะลูกบนถาดเพื่อปล่อย · ตัวจับเวลาเริ่มที่ประตูบน หยุดที่ประตูล่าง · ลูกเหล็ก 2–6 mm + ลูกแก้ว 4 mm · กลีเซอรีน 1.41 / น้ำมันละหุ่ง 0.99 / ❓X (ρ 910 ทราบ η สุ่ม) · ฟิสิกส์ m dv/dt = W − F_B − 6πηrv (ไม่คิดผลผนัง)
  - ผลตรวจ: v วัด = v_t ทฤษฎีทุกลูก · fit η กลีเซอรีน 1.410 · X 0.410 = จริง
- **Lab 105 สมการความต่อเนื่อง** — ท่อใส 3 ช่วง A 2.0 / B 1.0 / ❓X cm · วาล์ว 4 ระดับ (Q สุ่มต่อหน้า) · **แตะวาล์ว/บีกเกอร์/หัวฉีดสีในภาพ** · เก็บน้ำลงบีกเกอร์ 500 mL + นาฬิกาเริ่ม/หยุดตามการเก็บ → Q · ฉีดสีแล้วภาพแฟลชทุก 0.10 s เหลือรอยแหวนแดงบนท่อ · **ลากไม้บรรทัดใส 30 cm** วัดระยะรอย → v = d/(n·0.1) · ตาราง A·v เทียบ Q · กราฟ v–Q ความชัน 1/A
  - ผลตรวจ: ระยะรอยแฟลช = v·0.1 ตรงทุกช่วง · D_X 1.78 (จริง 1.77)
- ลงทะเบียน labs_data · VLAB_SERIES.vpl05 · LAB_LIST · protect · bump `?v=20260922-6` · build (หน้าแรก 106 แลป)

### ไฟล์ที่แก้
- ใหม่: `Virtual Physics Lab 05/104. viscosity-falling-ball.html`, `105. continuity-equation.html`
- `kp-auth.js`, `_admin/admin.html`, `_admin/labs_data.py` · build + ทุกไฟล์ที่โหลด kp-auth

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ push 104–105
- เหลือ 106 แบร์นูลลี (แลปสุดท้ายของชุดของไหล)
- สิทธิ์ผู้ชมทั่วไปยังไม่มี vpl05 (เจ้าของต้องติ๊กเอง)

### หมายเหตุ
- session ใหม่ preview server ดับ → `preview_start phys` ใหม่

## [2026-09-22 08:40] — Lab 105: สายน้ำไหลออกจากปลายท่อ

### ทำอะไรไปบ้าง
- เจ้าของขอ "105 อยากให้มีรูปน้ำไหลออกจากท่อ" → เดิมเป็นแท่งตรงแนวดิ่งบาง ๆ ที่ไม่ต่อกับปลายท่อ
- ทำใหม่เป็น**สายน้ำพุ่งออกจากปากท่อ X ตามแนวโพรเจกไทล์จริง** (ความเร็วปากท่อ v = Q/A_X) · **สายน้ำเล็กลงเมื่อตกเร็วขึ้น** (Av คงตัว → r ∝ 1/√v) · ลายน้ำเลื่อนไหลตามเวลา · ระลอก 2 วงตรงจุดตก · ถาดรองน้ำใต้ปากท่อ
- กดเก็บน้ำ → **บีกเกอร์เลื่อนเข้าไปรองใต้สายน้ำ** สายน้ำตกลงถึงผิวน้ำในบีกเกอร์ · นาฬิกาและปริมาตรเริ่มนับเมื่อบีกเกอร์อยู่ใต้สายน้ำแล้ว (Q ที่วัดได้ตรงค่าจริง 30.80 mL/s)
- ยกท่อสูงขึ้น (PY 12 → 16) ให้บีกเกอร์ลอดใต้ปากท่อได้ · ปรับมุมมองทั้งชุด/บีกเกอร์

### ไฟล์ที่แก้
- `Virtual Physics Lab 05/105. continuity-equation.html`

### ค้างไว้ที่ไหน / ต้องทำต่อ
- ยังไม่ได้ push 104–105 · เหลือ 106 แบร์นูลลี
