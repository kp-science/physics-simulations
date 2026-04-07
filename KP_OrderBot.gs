/**
 * ═══════════════════════════════════════════════════════════
 *  KP Science — Order Management Bot (Google Apps Script)
 *  โกเมน ปาปะโถ · KP Science Simulations
 *
 *  วิธีติดตั้ง:
 *  1. เปิด Google Sheets ที่ใช้ติดตามออเดอร์
 *  2. Extensions → Apps Script → วาง code นี้ทั้งหมด
 *  3. กด Save → Run → อนุญาต Permission ครั้งแรก
 *  4. ตั้ง Trigger: Triggers → Add Trigger → onEdit → From spreadsheet → On edit
 * ═══════════════════════════════════════════════════════════
 */

// ─── CONFIG (แก้ไขตรงนี้เท่านั้น) ───────────────────────────
const CONFIG = {
  SHEET_NAME:     "📋 Orders",
  STATUS_COL:     7,   // column G = สถานะ
  NAME_COL:       3,   // column C = ชื่อ-นามสกุล
  SCHOOL_COL:     4,   // column D = โรงเรียน
  PACKAGE_COL:    5,   // column E = แพ็กเกจ
  PRICE_COL:      6,   // column F = ราคา
  CONTACT_COL:    9,   // column I = Email/Line
  CAT1_COL:       10,  // column J = หมวดที่ 1
  CAT2_COL:       11,  // column K = หมวดที่ 2
  CAT3_COL:       12,  // column L = หมวดที่ 3
  PW_SENT_COL:    13,  // column M = รหัสที่ส่ง
  SENT_FLAG_COL:  14,  // column N = ส่งแล้ว ✅
  NOTE_COL:       15,  // column O = หมายเหตุ
  HEADER_ROW:     2,

  // รหัสผ่านแต่ละหมวด (ต้องตรงกับในไฟล์ HTML)
  PASSWORDS: {
    "กลศาสตร์":     "mech-2025",
    "คลื่น":        "wave-2025",
    "ดาราศาสตร์":  "astro-2025",
    "ไฟฟ้า":        "elec-2025",
    "อุณหพลศาสตร์":"thermo-2025",
  },

  // ลิงก์แต่ละหมวด
  LINKS: {
    "กลศาสตร์":     "https://komane67.github.io/physics-simulations/mechanics.html",
    "คลื่น":        "https://komane67.github.io/physics-simulations/waves.html",
    "ดาราศาสตร์":  "https://komane67.github.io/physics-simulations/astronomy.html",
    "ไฟฟ้า":        "https://komane67.github.io/physics-simulations/electricity.html",
    "อุณหพลศาสตร์":"https://komane67.github.io/physics-simulations/thermo.html",
  },

  SENDER_NAME:    "ครูโกเมน · KP Science",
  BASE_URL:       "https://komane67.github.io/physics-simulations/",
};

// ─── TRIGGER: เมื่อแก้ไข Sheet ──────────────────────────────
function onEdit(e) {
  const sheet = e.range.getSheet();
  if (sheet.getName() !== CONFIG.SHEET_NAME) return;

  const row = e.range.getRow();
  const col = e.range.getColumn();

  // ถ้าเปลี่ยนสถานะเป็น "ชำระแล้ว" → ส่ง email อัตโนมัติ
  if (col === CONFIG.STATUS_COL && row > CONFIG.HEADER_ROW) {
    const newVal = e.value;
    if (newVal === "ชำระแล้ว") {
      sendPasswordEmail(sheet, row);
    }
  }
}

// ─── ส่งอีเมลรหัสผ่าน ────────────────────────────────────────
function sendPasswordEmail(sheet, row) {
  const data = getRowData(sheet, row);

  // ตรวจว่ามี email
  if (!isValidEmail(data.contact)) {
    logNote(sheet, row, "⚠️ ไม่มี email — ส่งผ่าน Line เอง");
    return;
  }

  // สร้างรหัสผ่านตามหมวด
  const pwLines   = buildPasswordLines(data);
  const linkLines = buildLinkLines(data);

  if (pwLines.length === 0) {
    logNote(sheet, row, "⚠️ ไม่พบหมวดที่เลือก — ตรวจสอบ column J-L");
    return;
  }

  const subject = `🔑 KP Science — รหัสผ่านสำหรับ ${data.name}`;
  const body    = buildEmailBody(data, pwLines, linkLines);

  try {
    GmailApp.sendEmail(data.contact, subject, "", { htmlBody: body });
    sheet.getRange(row, CONFIG.SENT_FLAG_COL).setValue("✅");
    sheet.getRange(row, CONFIG.PW_SENT_COL).setValue(pwLines.map(l => l.pw).join(", "));
    logNote(sheet, row, `📧 ส่ง email แล้ว ${new Date().toLocaleDateString('th-TH')}`);
  } catch (err) {
    logNote(sheet, row, "❌ ส่ง email ไม่สำเร็จ: " + err.message);
  }
}

// ─── สร้าง HTML Email Body ────────────────────────────────────
function buildEmailBody(data, pwLines, linkLines) {
  const pwRows = pwLines.map(l =>
    `<tr>
       <td style="padding:8px 16px;color:#94a3b8;font-size:13px;">🔑 ${l.cat}</td>
       <td style="padding:8px 16px;font-family:monospace;font-size:16px;
                  color:#facc15;font-weight:bold;letter-spacing:2px;">${l.pw}</td>
       <td style="padding:8px 16px;"><a href="${l.link}"
           style="color:#38bdf8;font-size:12px;">เปิดลิงก์ →</a></td>
     </tr>`
  ).join('');

  return `
<!DOCTYPE html>
<html lang="th">
<body style="margin:0;padding:0;background:#06090f;font-family:'Sarabun',Arial,sans-serif;">
<div style="max-width:560px;margin:0 auto;padding:24px 16px;">

  <!-- Header -->
  <div style="background:linear-gradient(135deg,#0d1421,#111827);
              border:1px solid rgba(56,189,248,0.2);border-radius:16px;
              padding:28px 32px;text-align:center;margin-bottom:20px;">
    <div style="font-size:2rem;margin-bottom:8px;">🔬</div>
    <div style="color:#38bdf8;font-size:22px;font-weight:700;letter-spacing:1px;">KP Science</div>
    <div style="color:#94a3b8;font-size:13px;margin-top:4px;">Simulations · โรงเรียนสตรีวิทยา</div>
  </div>

  <!-- Greeting -->
  <div style="background:#0d1421;border-radius:12px;padding:20px 24px;
              border-left:4px solid #34d399;margin-bottom:16px;">
    <p style="color:#f0f4f8;font-size:15px;margin:0 0 8px;">
      สวัสดีครับ คุณ <strong style="color:#38bdf8;">${data.name}</strong> 🎉
    </p>
    <p style="color:#94a3b8;font-size:13px;margin:0;">
      ยืนยันการชำระเงินเรียบร้อยแล้วครับ — แพ็กเกจ <strong style="color:#f0f4f8;">${data.pkg}</strong>
    </p>
  </div>

  <!-- Password Table -->
  <div style="background:#0d1421;border-radius:12px;padding:20px 24px;margin-bottom:16px;
              border:1px solid rgba(56,189,248,0.15);">
    <p style="color:#38bdf8;font-size:13px;font-weight:700;
              letter-spacing:1px;text-transform:uppercase;margin:0 0 14px;">
      🔑 รหัสผ่านของคุณ
    </p>
    <table style="width:100%;border-collapse:collapse;">${pwRows}</table>
  </div>

  <!-- How to use -->
  <div style="background:#111827;border-radius:12px;padding:18px 24px;margin-bottom:16px;">
    <p style="color:#38bdf8;font-size:12px;font-weight:700;
              letter-spacing:1px;text-transform:uppercase;margin:0 0 10px;">วิธีใช้งาน</p>
    <ol style="color:#94a3b8;font-size:13px;padding-left:18px;margin:0;line-height:2;">
      <li>คลิก "เปิดลิงก์" ด้านบน หรือเปิด <a href="${CONFIG.BASE_URL}" style="color:#38bdf8;">${CONFIG.BASE_URL}</a></li>
      <li>เลือกหมวดที่ซื้อ → กรอกรหัสผ่าน → กด "เข้าใช้งาน"</li>
      <li>ใช้ได้บน PC · iPad · มือถือ ไม่ต้องติดตั้งซอฟต์แวร์</li>
    </ol>
  </div>

  <!-- Footer -->
  <div style="text-align:center;padding-top:16px;">
    <p style="color:#475569;font-size:12px;margin:0;">
      มีปัญหาการใช้งานติดต่อได้ทาง Line ที่ส่งออเดอร์มาได้เลยครับ<br>
      <span style="color:#38bdf8;">KP Science</span> · โกเมน ปาปะโถ · โรงเรียนสตรีวิทยา
    </p>
  </div>

</div>
</body>
</html>`;
}

// ─── Helper: ดึงข้อมูลแถว ─────────────────────────────────────
function getRowData(sheet, row) {
  const get = (col) => sheet.getRange(row, col).getValue();
  return {
    name:    get(CONFIG.NAME_COL)    || "",
    school:  get(CONFIG.SCHOOL_COL)  || "",
    pkg:     get(CONFIG.PACKAGE_COL) || "",
    price:   get(CONFIG.PRICE_COL)   || 0,
    contact: get(CONFIG.CONTACT_COL) || "",
    cat1:    get(CONFIG.CAT1_COL)    || "",
    cat2:    get(CONFIG.CAT2_COL)    || "",
    cat3:    get(CONFIG.CAT3_COL)    || "",
  };
}

// ─── Helper: สร้างรายการรหัสผ่าน ──────────────────────────────
function buildPasswordLines(data) {
  const cats = [data.cat1, data.cat2, data.cat3].filter(c => c !== "");
  return cats.map(cat => ({
    cat:  cat,
    pw:   CONFIG.PASSWORDS[cat] || "N/A",
    link: CONFIG.LINKS[cat]     || CONFIG.BASE_URL,
  }));
}

function buildLinkLines(data) {
  return buildPasswordLines(data).map(l => l.link);
}

// ─── Helper: ตรวจ email ──────────────────────────────────────
function isValidEmail(str) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str);
}

// ─── Helper: บันทึกหมายเหตุ ─────────────────────────────────
function logNote(sheet, row, msg) {
  const cell = sheet.getRange(row, CONFIG.NOTE_COL);
  const existing = cell.getValue();
  cell.setValue(existing ? existing + " | " + msg : msg);
}

// ─── รันด้วยตนเอง: ส่งรหัสให้ทุกออเดอร์ที่ชำระแล้วแต่ยังไม่ส่ง ──
function sendAllPending() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
  const last  = sheet.getLastRow();
  let count   = 0;

  for (let row = CONFIG.HEADER_ROW + 1; row <= last; row++) {
    const status = sheet.getRange(row, CONFIG.STATUS_COL).getValue();
    const sent   = sheet.getRange(row, CONFIG.SENT_FLAG_COL).getValue();
    if (status === "ชำระแล้ว" && sent !== "✅") {
      sendPasswordEmail(sheet, row);
      count++;
      Utilities.sleep(1000); // ป้องกัน rate limit
    }
  }

  SpreadsheetApp.getUi().alert(`✅ ส่ง email เรียบร้อย ${count} รายการ`);
}

// ─── สร้าง Menu ในหน้า Spreadsheet ──────────────────────────
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("🔬 KP Science")
    .addItem("📧 ส่งรหัสให้ทุกออเดอร์ที่ค้างอยู่", "sendAllPending")
    .addItem("📊 รีเฟรช Dashboard", "refreshDashboard")
    .addToUi();
}

function refreshDashboard() {
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName("📊 Dashboard").getRange("A1").activate();
  SpreadsheetApp.getUi().alert("✅ Dashboard อัพเดทแล้ว");
}
