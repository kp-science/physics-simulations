// ============================================================
//  KP Science — Auth System v2.0
//  Firebase Authentication + Firestore + Topics Access Control
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

// Topics ทั้งหมดในระบบ
const ALL_TOPICS = ['mechanics', 'waves', 'astronomy', 'electricity', 'thermodynamics'];

// Topics ที่ได้รับเมื่อสมัครใหม่ (Free member)
const DEFAULT_TOPICS = ['mechanics'];

// ── State ─────────────────────────────────────────────────
let currentUser     = null;
let currentUserData = null; // ข้อมูลจาก Firestore

// ── Auth state listener ───────────────────────────────────
auth.onAuthStateChanged(async user => {
  currentUser = user;
  if (user) {
    // โหลดข้อมูล user จาก Firestore
    try {
      const snap = await db.collection('users').doc(user.uid).get();
      currentUserData = snap.exists ? snap.data() : null;
    } catch(e) {
      currentUserData = null;
    }
    // ── Sync watermark tier จาก Firestore → localStorage ──
    syncWatermarkTier(currentUserData);
    updateTopbar(user);
    applyTopicAccess();
  } else {
    currentUserData = null;
    // ── ลบ tier เมื่อ logout → ลายน้ำกลับมา ──
    try { localStorage.removeItem('kp_access_tier'); } catch(e){}
    if (typeof KPWatermark !== 'undefined') KPWatermark.show();
    updateTopbar(null);
    lockAll();
  }
});

// ── Watermark Tier Sync ──────────────────────────────────
function syncWatermarkTier(userData) {
  try {
    if (!userData) return;
    const tier = userData.access_tier || '';
    const role = userData.role || 'member';
    // role admin/premium หรือ access_tier ที่ตั้งไว้ → ปลดลายน้ำ
    const unlockTiers = ['pro', 'premium', 'admin'];
    if (unlockTiers.includes(tier) || unlockTiers.includes(role)) {
      localStorage.setItem('kp_access_tier', tier || role);
      if (typeof KPWatermark !== 'undefined') KPWatermark.check();
    } else {
      localStorage.removeItem('kp_access_tier');
      if (typeof KPWatermark !== 'undefined') KPWatermark.show();
    }
  } catch(e) {}
}

// ── UI: Topbar ────────────────────────────────────────────
function updateTopbar(user) {
  const loginBtn  = document.getElementById('kp-login-btn');
  const userMenu  = document.getElementById('kp-user-menu');
  const userEmail = document.getElementById('kp-user-email');

  if (user) {
    if (loginBtn)  loginBtn.style.display  = 'none';
    if (userMenu)  userMenu.style.display  = 'flex';
    if (userEmail) userEmail.textContent   = user.email.split('@')[0];
  } else {
    if (loginBtn)  loginBtn.style.display  = 'flex';
    if (userMenu)  userMenu.style.display  = 'none';
  }
}

// ── Topics Access Control ─────────────────────────────────

// กำหนด topics ที่ user เข้าถึงได้
function getUserTopics() {
  if (!currentUserData) return [];
  // admin หรือ premium เข้าได้ทุก topic
  if (currentUserData.role === 'admin' || currentUserData.role === 'premium') {
    return ALL_TOPICS;
  }
  // blocked เข้าไม่ได้เลย
  if (currentUserData.role === 'blocked') return [];
  // member ทั่วไปดูตาม topics ที่กำหนด
  return currentUserData.topics || DEFAULT_TOPICS;
}

// ใช้สิทธิ์กับทุก element ที่มี data-locked
function applyTopicAccess() {
  const allowedTopics = getUserTopics();

  document.querySelectorAll('[data-locked="true"]').forEach(el => {
    const topic = el.getAttribute('data-topic') || 'mechanics';
    if (allowedTopics.includes(topic)) {
      unlock(el);
    } else {
      lock(el);
    }
  });
}

function lockAll() {
  document.querySelectorAll('[data-locked="true"]').forEach(el => lock(el));
}

function lock(el) {
  if (el.classList.contains('kp-locked')) return;
  el.classList.add('kp-locked');
  const href = el.getAttribute('href');
  if (href) el.setAttribute('data-original-href', href);
  el.removeAttribute('href');
  el.addEventListener('click', onLockedClick);
}

function unlock(el) {
  el.classList.remove('kp-locked');
  const original = el.getAttribute('data-original-href');
  if (original) el.setAttribute('href', original);
  el.removeEventListener('click', onLockedClick);
}

function onLockedClick(e) {
  e.preventDefault();
  if (!currentUser) {
    showModal('login');
  } else {
    // login แล้วแต่ไม่มีสิทธิ์ topic นี้
    showTopicAlert(e.currentTarget);
  }
}

function showTopicAlert(el) {
  const topic = el.getAttribute('data-topic') || 'mechanics';
  const topicNames = {
    mechanics:      'กลศาสตร์',
    waves:          'คลื่นและเสียง',
    astronomy:      'ดาราศาสตร์',
    electricity:    'ไฟฟ้า',
    thermodynamics: 'อุณหพลศาสตร์'
  };
  const t = document.getElementById('kp-quota-alert');
  if (t) {
    t.textContent = `🔒 สิทธิ์ "${topicNames[topic] || topic}" สำหรับ Premium เท่านั้น`;
    t.style.display = 'flex';
    setTimeout(() => t.style.display = 'none', 3500);
  }
}

// ── Modal ─────────────────────────────────────────────────
function showModal(tab = 'login') {
  const modal = document.getElementById('kp-auth-modal');
  if (modal) {
    // ถ้าเปิดแท็บ login/register ปกติ → แสดง login+register tabs, ซ่อน profile
    if (tab !== 'profile') {
      const tabLogin   = document.getElementById('tab-login');
      const tabReg     = document.getElementById('tab-register');
      const tabProfile = document.getElementById('tab-profile');
      if (tabLogin)   tabLogin.style.display   = 'block';
      if (tabReg)     tabReg.style.display     = 'block';
      if (tabProfile) tabProfile.style.display = 'none';
    }
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
  const tabEl  = document.getElementById('tab-' + tab);
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

    await db.collection('users').doc(cred.user.uid).set({
      email:              email,
      role:               'member',
      topics:             DEFAULT_TOPICS,   // mechanics เท่านั้นตอนสมัคร
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

// ── Google Sign-In ────────────────────────────────────────
async function kpLoginGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  try {
    const result = await auth.signInWithPopup(provider);
    const user   = result.user;

    // ถ้า login ครั้งแรก → สร้าง user doc ใน Firestore
    const userRef = db.collection('users').doc(user.uid);
    const snap    = await userRef.get();
    if (!snap.exists) {
      await userRef.set({
        email:              user.email,
        role:               'member',
        topics:             DEFAULT_TOPICS,
        createdAt:          firebase.firestore.FieldValue.serverTimestamp(),
        downloadsThisMonth: 0,
        downloadMonth:      new Date().getMonth(),
        downloadYear:       new Date().getFullYear()
      });
    }
    hideModal();
  } catch(e) {
    if (e.code === 'auth/popup-closed-by-user') return;
    const errEl = document.getElementById('kp-login-err') || document.getElementById('kp-reg-err');
    if (errEl) errEl.textContent = translateError(e.code);
  }
}

// ── Logout ────────────────────────────────────────────────
async function kpLogout() {
  await auth.signOut();
}

// ── Profile ───────────────────────────────────────────────
const ROLE_LABELS = {
  member:  { text: 'สมาชิก',      cls: 'kp-role-member',  icon: '🆓' },
  premium: { text: 'พรีเมียม',    cls: 'kp-role-premium', icon: '💎' },
  admin:   { text: 'ผู้ดูแล',     cls: 'kp-role-admin',   icon: '👑' },
  blocked: { text: 'ถูกระงับ',    cls: 'kp-role-blocked', icon: '🚫' }
};

const TOPIC_LABELS = {
  mechanics:      { name: 'กลศาสตร์',       icon: '⚙️' },
  waves:          { name: 'คลื่นและเสียง',   icon: '🌊' },
  astronomy:      { name: 'ดาราศาสตร์',      icon: '🌌' },
  electricity:    { name: 'ไฟฟ้า',          icon: '⚡' },
  thermodynamics: { name: 'อุณหพลศาสตร์',   icon: '🔥' }
};

async function showProfile() {
  if (!currentUser) { showModal('login'); return; }

  // ถ้าข้อมูลยังไม่โหลด → โหลดใหม่
  if (!currentUserData) {
    try {
      const snap = await db.collection('users').doc(currentUser.uid).get();
      currentUserData = snap.exists ? snap.data() : null;
    } catch(e) { currentUserData = null; }
  }

  renderProfile();

  // เปิด modal + สลับไปแท็บ profile
  const tabProfile = document.getElementById('tab-profile');
  if (tabProfile) tabProfile.style.display = 'block';
  const tabLogin = document.getElementById('tab-login');
  const tabReg   = document.getElementById('tab-register');
  if (tabLogin) tabLogin.style.display = 'none';
  if (tabReg)   tabReg.style.display   = 'none';

  showModal('profile');
}

function renderProfile() {
  if (!currentUser) return;
  const d = currentUserData || {};

  // Avatar
  const avatarEl = document.getElementById('kp-profile-avatar');
  if (avatarEl) {
    const photo = currentUser.photoURL;
    if (photo) {
      avatarEl.innerHTML = '<img src="' + photo + '" alt="avatar" onerror="this.parentNode.textContent=this.parentNode.getAttribute(\'data-initial\')||\'?\'">';
    } else {
      const initial = (currentUser.displayName || currentUser.email || '?').trim().charAt(0).toUpperCase();
      avatarEl.setAttribute('data-initial', initial);
      avatarEl.textContent = initial;
    }
  }

  // Name + Email
  const nameEl  = document.getElementById('kp-profile-name');
  const emailEl = document.getElementById('kp-profile-email');
  if (nameEl)  nameEl.textContent  = currentUser.displayName || (currentUser.email || '').split('@')[0] || 'สมาชิก';
  if (emailEl) emailEl.textContent = currentUser.email || '—';

  // Role badge
  const roleKey = d.role || 'member';
  const role    = ROLE_LABELS[roleKey] || ROLE_LABELS.member;
  const roleEl  = document.getElementById('kp-profile-role');
  if (roleEl) {
    roleEl.className = 'kp-role-badge ' + role.cls;
    roleEl.textContent = role.icon + ' ' + role.text;
  }

  // Topics
  const allowed = getUserTopics();
  const topicsEl = document.getElementById('kp-profile-topics');
  if (topicsEl) {
    topicsEl.innerHTML = ALL_TOPICS.map(t => {
      const info = TOPIC_LABELS[t] || { name: t, icon: '📘' };
      const ok = allowed.includes(t);
      return '<div class="kp-topic-row ' + (ok ? 'allowed' : 'locked') + '">' +
             '<span><span class="kp-topic-ico">' + info.icon + '</span> ' + info.name + '</span>' +
             '<span>' + (ok ? '✅' : '🔒') + '</span>' +
             '</div>';
    }).join('');
  }

  // Watermark status
  const wmEl = document.getElementById('kp-profile-watermark');
  if (wmEl) {
    const unlockTiers = ['pro', 'premium', 'admin'];
    const unlocked = unlockTiers.includes(d.access_tier) || unlockTiers.includes(roleKey);
    wmEl.textContent = unlocked ? 'ซ่อนอยู่' : 'แสดงอยู่';
    wmEl.className = 'kp-stat-value ' + (unlocked ? 'ok' : 'warn');
  }

  // Downloads
  const dlEl = document.getElementById('kp-profile-downloads');
  if (dlEl) {
    const nowMonth = new Date().getMonth();
    const nowYear  = new Date().getFullYear();
    const sameMonth = d.downloadMonth === nowMonth && d.downloadYear === nowYear;
    const used = sameMonth ? (d.downloadsThisMonth || 0) : 0;
    const quota = d.downloadQuota != null ? d.downloadQuota : DOWNLOAD_QUOTA;
    const isUnlimited = quota < 0;
    if (isUnlimited) {
      dlEl.textContent = used + ' / ไม่จำกัด';
      dlEl.className = 'kp-stat-value ok';
    } else {
      dlEl.textContent = used + ' / ' + quota + ' ครั้ง';
      dlEl.className = 'kp-stat-value ' + (used >= quota ? 'warn' : '');
    }
  }

  // Joined date
  const jEl = document.getElementById('kp-profile-joined');
  if (jEl) {
    let dateStr = '—';
    try {
      if (d.createdAt && d.createdAt.toDate) {
        const dt = d.createdAt.toDate();
        dateStr = dt.toLocaleDateString('th-TH', { year:'numeric', month:'short', day:'numeric' });
      } else if (currentUser.metadata && currentUser.metadata.creationTime) {
        const dt = new Date(currentUser.metadata.creationTime);
        dateStr = dt.toLocaleDateString('th-TH', { year:'numeric', month:'short', day:'numeric' });
      }
    } catch(e) {}
    jEl.textContent = dateStr;
  }
}

// ── Download with quota ───────────────────────────────────
async function kpDownload(fileUrl, fileName) {
  if (!currentUser) { showModal('login'); return; }

  const userRef = db.collection('users').doc(currentUser.uid);
  const snap    = await userRef.get();
  if (!snap.exists) { alert('ไม่พบข้อมูลสมาชิก'); return; }

  const data     = snap.data();
  const nowMonth = new Date().getMonth();
  const nowYear  = new Date().getFullYear();
  const sameMonth = data.downloadMonth === nowMonth && data.downloadYear === nowYear;
  const count     = sameMonth ? (data.downloadsThisMonth || 0) : 0;
  const userQuota = data.downloadQuota || DOWNLOAD_QUOTA; // per-user quota from admin
  const isUnlimited = userQuota < 0;

  if (!isUnlimited && count >= userQuota) {
    const t = document.getElementById('kp-quota-alert');
    if (t) {
      t.textContent = `⚠️ คุณใช้สิทธิ์ดาวน์โหลดครบ ${userQuota} ครั้งแล้วในเดือนนี้`;
      t.style.display = 'flex';
      setTimeout(() => t.style.display = 'none', 4000);
    }
    return;
  }

  await userRef.update({
    downloadsThisMonth: firebase.firestore.FieldValue.increment(1),
    downloadMonth:      nowMonth,
    downloadYear:       nowYear,
    ...(sameMonth ? {} : { downloadsThisMonth: 1 })
  });

  const a = document.createElement('a');
  a.href = fileUrl;
  a.download = fileName || 'document';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  // Log download
  logDownload(fileName || fileUrl);
}

// ── Download Log ─────────────────────────────────────────
function logDownload(fileName) {
  if (!currentUser) return;
  try {
    db.collection('download_logs').add({
      userId: currentUser.uid,
      email: currentUser.email,
      fileName: fileName,
      timestamp: firebase.firestore.FieldValue.serverTimestamp()
    });
  } catch(e) { console.error('logDownload error:', e); }
}

// ── Error translation ─────────────────────────────────────
function translateError(code) {
  const map = {
    'auth/user-not-found':         'ไม่พบบัญชีนี้ในระบบ',
    'auth/wrong-password':         'รหัสผ่านไม่ถูกต้อง',
    'auth/invalid-credential':     'อีเมลหรือรหัสผ่านไม่ถูกต้อง',
    'auth/email-already-in-use':   'อีเมลนี้มีบัญชีอยู่แล้ว',
    'auth/invalid-email':          'รูปแบบอีเมลไม่ถูกต้อง',
    'auth/weak-password':          'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร',
    'auth/too-many-requests':      'ลองใหม่ภายหลัง (เข้าสู่ระบบผิดหลายครั้ง)',
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

// ── Backdrop & Escape ─────────────────────────────────────
document.addEventListener('click', e => {
  const modal = document.getElementById('kp-auth-modal');
  if (modal && e.target === modal) hideModal();
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') hideModal();
});
