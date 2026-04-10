// ============================================================
//  KP Science — Auth System v1.0
//  Firebase Authentication + Firestore quota
// ============================================================

const firebaseConfig = {
  apiKey: "AIzaSyBTtSjqno1IVku27_J0lFY2dU0y8nq9B5U",
  authDomain: "kp-science-f11ff.firebaseapp.com",
  projectId: "kp-science-f11ff",
  storageBucket: "kp-science-f11ff.firebasestorage.app",
  messagingSenderId: "352992735315",
  appId: "1:352992735315:web:c88b220ffc750862ab16a6",
  measurementId: "G-LZFF138J33"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db   = firebase.firestore();

// ── Config ────────────────────────────────────────────────
const DOWNLOAD_QUOTA = 3; // ดาวน์โหลดสูงสุดต่อเดือน

// ── State ─────────────────────────────────────────────────
let currentUser = null;

// ── Auth state listener ───────────────────────────────────
auth.onAuthStateChanged(user => {
  currentUser = user;
  updateTopbar(user);
  if (user) {
    unlockSimulations();
  } else {
    lockSimulations();
  }
});

// ── UI: Topbar ────────────────────────────────────────────
function updateTopbar(user) {
  const loginBtn  = document.getElementById('kp-login-btn');
  const userMenu  = document.getElementById('kp-user-menu');
  const userEmail = document.getElementById('kp-user-email');

  if (user) {
    if (loginBtn)  loginBtn.style.display  = 'none';
    if (userMenu)  userMenu.style.display  = 'flex';
    if (userEmail) userEmail.textContent   = user.email.split('@')[0]; // แสดงแค่ชื่อ
  } else {
    if (loginBtn)  loginBtn.style.display  = 'flex';
    if (userMenu)  userMenu.style.display  = 'none';
  }
}

// ── Lock / Unlock ─────────────────────────────────────────
function lockSimulations() {
  document.querySelectorAll('[data-locked="true"]').forEach(el => {
    el.classList.add('kp-locked');
    el.setAttribute('data-original-href', el.getAttribute('href') || '');
    el.removeAttribute('href');
    el.addEventListener('click', onLockedClick);
  });
}

function unlockSimulations() {
  document.querySelectorAll('[data-locked="true"]').forEach(el => {
    el.classList.remove('kp-locked');
    const original = el.getAttribute('data-original-href');
    if (original) el.setAttribute('href', original);
    el.removeEventListener('click', onLockedClick);
  });
}

function onLockedClick(e) {
  e.preventDefault();
  showModal('login');
}

// ── Modal ─────────────────────────────────────────────────
function showModal(tab = 'login') {
  const modal = document.getElementById('kp-auth-modal');
  if (modal) {
    modal.classList.add('open');
    switchTab(tab);
    clearErrors();
  }
}

function hideModal() {
  const modal = document.getElementById('kp-auth-modal');
  if (modal) modal.classList.remove('open');
  clearErrors();
}

function switchTab(tab) {
  document.querySelectorAll('.kp-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.kp-tab-pane').forEach(t => t.classList.remove('active'));
  const tabEl = document.getElementById('tab-' + tab);
  const paneEl = document.getElementById('pane-' + tab);
  if (tabEl)  tabEl.classList.add('active');
  if (paneEl) paneEl.classList.add('active');
}

// ── Login ─────────────────────────────────────────────────
async function kpLogin() {
  const email = document.getElementById('kp-login-email').value.trim();
  const pass  = document.getElementById('kp-login-pass').value;
  const errEl = document.getElementById('kp-login-err');

  if (!email || !pass) { errEl.textContent = 'กรุณากรอกอีเมลและรหัสผ่าน'; return; }

  try {
    errEl.textContent = 'กำลังเข้าสู่ระบบ...';
    await auth.signInWithEmailAndPassword(email, pass);
    hideModal();
  } catch(e) {
    errEl.textContent = translateError(e.code);
  }
}

// ── Register ──────────────────────────────────────────────
async function kpRegister() {
  const email = document.getElementById('kp-reg-email').value.trim();
  const pass  = document.getElementById('kp-reg-pass').value;
  const pass2 = document.getElementById('kp-reg-pass2').value;
  const errEl = document.getElementById('kp-reg-err');

  if (!email || !pass) { errEl.textContent = 'กรุณากรอกข้อมูลให้ครบ'; return; }
  if (pass !== pass2)  { errEl.textContent = 'รหัสผ่านไม่ตรงกัน'; return; }
  if (pass.length < 6) { errEl.textContent = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'; return; }

  try {
    errEl.textContent = 'กำลังสร้างบัญชี...';
    const cred = await auth.createUserWithEmailAndPassword(email, pass);

    // สร้างข้อมูลสมาชิกใน Firestore
    await db.collection('users').doc(cred.user.uid).set({
      email:              email,
      role:               'member',
      createdAt:          firebase.firestore.FieldValue.serverTimestamp(),
      downloadsThisMonth: 0,
      downloadMonth:      new Date().getMonth(),
      downloadYear:       new Date().getFullYear()
    });

    hideModal();
  } catch(e) {
    errEl.textContent = translateError(e.code);
  }
}

// ── Logout ────────────────────────────────────────────────
async function kpLogout() {
  await auth.signOut();
}

// ── Download with quota ───────────────────────────────────
async function kpDownload(fileUrl, fileName) {
  if (!currentUser) {
    showModal('login');
    return;
  }

  const userRef = db.collection('users').doc(currentUser.uid);
  const snap    = await userRef.get();

  if (!snap.exists) {
    alert('ไม่พบข้อมูลสมาชิก กรุณาติดต่อผู้ดูแล');
    return;
  }

  const data         = snap.data();
  const nowMonth     = new Date().getMonth();
  const nowYear      = new Date().getFullYear();

  // Reset quota ถ้าขึ้นเดือนหรือปีใหม่
  const sameMonth = data.downloadMonth === nowMonth && data.downloadYear === nowYear;
  const count     = sameMonth ? (data.downloadsThisMonth || 0) : 0;

  if (count >= DOWNLOAD_QUOTA) {
    showQuotaAlert(count);
    return;
  }

  // อัปเดต quota แล้วดาวน์โหลด
  await userRef.update({
    downloadsThisMonth: firebase.firestore.FieldValue.increment(sameMonth ? 1 : 1),
    downloadMonth:      nowMonth,
    downloadYear:       nowYear,
    ...(sameMonth ? {} : { downloadsThisMonth: 1 })
  });

  // trigger download
  const a = document.createElement('a');
  a.href = fileUrl;
  a.download = fileName || 'document';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  // แจ้งเตือนเหลืออีกกี่ครั้ง
  const remaining = DOWNLOAD_QUOTA - (sameMonth ? count + 1 : 1);
  if (remaining === 0) {
    alert('คุณใช้สิทธิ์ดาวน์โหลดครบแล้วในเดือนนี้ สิทธิ์จะรีเซ็ตในเดือนหน้า');
  } else {
    // silent — ไม่รบกวนผู้ใช้
  }
}

function showQuotaAlert(count) {
  const el = document.getElementById('kp-quota-alert');
  if (el) {
    el.style.display = 'flex';
    setTimeout(() => el.style.display = 'none', 4000);
  } else {
    alert(`คุณใช้สิทธิ์ดาวน์โหลดครบ ${DOWNLOAD_QUOTA} ครั้งแล้วในเดือนนี้`);
  }
}

// ── Error translation ─────────────────────────────────────
function translateError(code) {
  const map = {
    'auth/user-not-found':      'ไม่พบบัญชีนี้ในระบบ',
    'auth/wrong-password':      'รหัสผ่านไม่ถูกต้อง',
    'auth/invalid-credential':  'อีเมลหรือรหัสผ่านไม่ถูกต้อง',
    'auth/email-already-in-use':'อีเมลนี้มีบัญชีอยู่แล้ว',
    'auth/invalid-email':       'รูปแบบอีเมลไม่ถูกต้อง',
    'auth/weak-password':       'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร',
    'auth/too-many-requests':   'ลองใหม่ภายหลัง (เข้าสู่ระบบผิดหลายครั้ง)',
    'auth/network-request-failed': 'ไม่มีการเชื่อมต่ออินเทอร์เน็ต',
  };
  return map[code] || 'เกิดข้อผิดพลาด: ' + code;
}

function clearErrors() {
  ['kp-login-err','kp-reg-err'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = '';
  });
  ['kp-login-email','kp-login-pass','kp-reg-email','kp-reg-pass','kp-reg-pass2'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
}

// ── Close modal on backdrop click ─────────────────────────
document.addEventListener('click', e => {
  const modal = document.getElementById('kp-auth-modal');
  if (modal && e.target === modal) hideModal();
});

// ── Enter key support ─────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') hideModal();
});
