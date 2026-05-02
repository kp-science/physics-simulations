# 🔥 Firebase Setup Guide — Physics Quest

> **เป้าหมาย:** ตั้งค่า Firebase project (ฟรี) เพื่อให้เกมมีระบบ login + cloud save
> **เวลาที่ใช้:** 5-10 นาที (one-time)
> **ค่าใช้จ่าย:** $0 จนถึง ~10,000 ผู้ใช้พร้อมกัน

ทำตามทีละขั้น แล้ว copy `firebaseConfig` กลับมาให้ Claude — Claude จะ integrate ให้ที่เหลือ

---

## ขั้นที่ 1 — Create Firebase Project (2 นาที)

1. เปิด **https://console.firebase.google.com** ใน browser (login ด้วย komanepapato@gmail.com)
2. กด **"Add project"** (หรือ "เพิ่มโปรเจกต์")
3. ชื่อ project: `physics-quest` (หรืออะไรก็ได้)
4. **Disable Google Analytics** (ไม่จำเป็นสำหรับตอนนี้, ลด complexity) → กด "Create project"
5. รอ ~30 วินาที → กด "Continue"

---

## ขั้นที่ 2 — Enable Authentication (2 นาที)

1. ใน Firebase console (ซ้ายมือ) → **Build** → **Authentication**
2. กด **"Get started"**
3. แท็บ **Sign-in method** → enable 2 อย่างนี้:

   **a) Google**
   - คลิก "Google" → toggle "Enable" ON
   - **Project support email:** เลือก komanepapato@gmail.com
   - กด "Save"

   **b) Email/Password**
   - คลิก "Email/Password" → toggle "Enable" ON (ตัวบน)
   - **อย่า** enable "Email link (passwordless)" — ไม่ใช้
   - กด "Save"

---

## ขั้นที่ 3 — Create Firestore Database (2 นาที)

1. ซ้ายมือ → **Build** → **Firestore Database**
2. กด **"Create database"**
3. เลือก **"Start in production mode"** (ปลอดภัยกว่า — Claude จะตั้ง security rules ให้ทีหลัง)
4. **Location:** เลือก `asia-southeast1 (Singapore)` ← สำคัญ! ใกล้ไทยที่สุด ลดความช้า
5. กด "Enable" → รอ ~30 วินาที

---

## ขั้นที่ 4 — Set Firestore Security Rules (1 นาที)

1. ในหน้า Firestore Database → แท็บ **Rules** (อยู่ด้านบน)
2. ลบ rules เดิมทั้งหมด, แทนด้วย:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Each user can only read/write their own document
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;

      // Sub-collections under user (saves, activity log later)
      match /{document=**} {
        allow read, write: if request.auth != null && request.auth.uid == uid;
      }
    }
  }
}
```

3. กด **"Publish"**

---

## ขั้นที่ 5 — Register Web App + Copy Config (3 นาที)

1. ซ้ายมือ ⚙️ (Settings icon) → **Project settings**
2. แท็บ **General** → scroll ลงไปหา **"Your apps"**
3. กดไอคอน **`</>`** (Web app)
4. **App nickname:** `physics-quest-web` → **อย่า** เลือก "Set up Firebase Hosting" → กด "Register app"
5. หน้าถัดไปจะแสดง code block สีดำ — เลื่อนหาส่วนที่ขึ้นต้นด้วย:

```js
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "physics-quest-xxxxx.firebaseapp.com",
  projectId: "physics-quest-xxxxx",
  storageBucket: "physics-quest-xxxxx.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abc123"
};
```

6. **Copy เฉพาะ object `firebaseConfig` 6-7 บรรทัดนี้** → paste กลับมาในแชท
7. กด "Continue to console" — เสร็จขั้นที่ 5

---

## ขั้นที่ 6 — Add Authorized Domain (สำหรับ GitHub Pages)

> ✅ ถ้ายังเล่นแค่ในเครื่อง (file:// หรือ localhost) ข้ามขั้นนี้ไปก่อน
> ⚠️ ถ้าต้องการ deploy ขึ้น GitHub Pages ทำตามนี้

1. Authentication → แท็บ **Settings** → **Authorized domains**
2. กด "Add domain"
3. ใส่ `komane67.github.io` → กด "Add"
4. (`localhost` มีอยู่แล้ว default — ไม่ต้องเพิ่ม)

---

## ✅ Done! Checklist

- [ ] Project created
- [ ] Google + Email/Password sign-in enabled
- [ ] Firestore created in `asia-southeast1`
- [ ] Security rules published
- [ ] Web app registered + `firebaseConfig` copied
- [ ] (optional) `komane67.github.io` added to authorized domains

**ขั้นต่อไป:** paste `firebaseConfig` 6-7 บรรทัดในแชท → Claude จะ integrate Firebase SDK เข้า engine + สร้าง login UI + cloud save ให้ทันที

---

## 🔍 Free Tier Limits (สบายใจได้)

| Resource | Free | ใช้จริง (นักเรียน 1 คนเล่น 1 ชม.) |
|---|---|---|
| Auth users | ไม่จำกัด | 1 |
| Firestore reads | 50,000/วัน | ~20 reads (login + sync) |
| Firestore writes | 20,000/วัน | ~30 writes (save game) |
| Storage | 1 GB | ~50 KB ต่อ save |

**สรุป:** รองรับ ~1,000 active นักเรียน/วันได้สบายๆ ฟรี — เกินค่อยอัพ Blaze plan ($25/เดือน Spark Plan)

---

## 🆘 Troubleshooting

**ถ้า Google sign-in ไม่ทำงานตอน test:**
- เช็คว่า `localhost` อยู่ใน Authorized domains (Authentication → Settings)

**ถ้าเห็น error "Missing or insufficient permissions":**
- Security rules ยังไม่ publish — กลับไปขั้นที่ 4

**ถ้าลืม config:**
- กลับไป Project Settings → General → Your apps → คลิกแอป → "Config"
