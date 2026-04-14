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

// ═════════════════════════════════════════════════════════
// ── Access Schema v4 (Phase 1) ───────────────────────────
// Format: "category:source:item" string-based
// Examples:
//   "demo:mechanics"           — Demo วิชากลศาสตร์
//   "demo:*"                   — Demo ทุกวิชา (bundle)
//   "vlab:vpl01:lab-16"        — Virtual Lab 01 Lab 16 (per-item)
//   "vlab:vpl01:*"             — Virtual Lab 01 ทั้ง series (bundle)
//   "manual:vpl01:*"           — คู่มือ VPL01 ทั้งหมด
//   "*"                        — Superuser (admin)
// ═════════════════════════════════════════════════════════

// รายการ lab IDs แต่ละ series (ใช้ render per-item drill-down ใน admin)
const VLAB_SERIES = {
  vpl01: {
    label: 'Virtual Lab 01',
    labs: ['lab-1','lab-2','lab-3','lab-4','lab-5','lab-6.1','lab-6.2','lab-6.3',
           'lab-7','lab-8','lab-9','lab-10','lab-11','lab-12','lab-13','lab-14',
           'lab-15','lab-16','lab-17','lab-18','lab-19','lab-20','lab-21']
  },
  vpl02: {
    label: 'Virtual Lab 02',
    labs: ['lab-30','lab-31','lab-32','lab-32b','lab-32c','lab-33','lab-33b',
           'lab-34','lab-35','lab-37']
  }
};

const ACCESS_SCHEMA = [
  // ── Phase 1 (active) ──
  {
    id: 'demo', label: 'Demo (หลักการวิทยาศาสตร์)', icon: '🎬', phase: 1,
    kind: 'subjects',
    items: [
      { id: 'mechanics',      label: 'กลศาสตร์',      icon: '⚙️' },
      { id: 'waves',          label: 'คลื่นและเสียง', icon: '🌊' },
      { id: 'astronomy',      label: 'ดาราศาสตร์',    icon: '🌌' },
      { id: 'electricity',    label: 'ไฟฟ้า',         icon: '⚡' },
      { id: 'thermodynamics', label: 'อุณหพลศาสตร์', icon: '🔥' }
    ]
  },
  {
    id: 'vlab', label: 'Virtual Lab (ฝึกทักษะ)', icon: '🧪', phase: 1,
    kind: 'series',
    items: Object.keys(VLAB_SERIES).map(k => ({ id: k, label: VLAB_SERIES[k].label, labs: VLAB_SERIES[k].labs }))
  },
  {
    id: 'manual', label: 'คู่มือ Lab', icon: '📘', phase: 1,
    kind: 'series',
    items: Object.keys(VLAB_SERIES).map(k => ({ id: k, label: VLAB_SERIES[k].label, labs: VLAB_SERIES[k].labs }))
  },
  // ── Phase 2 (placeholder) ──
  { id: 'exam',    label: 'ข้อสอบ + Simulation',     icon: '📝', phase: 2, comingSoon: true },
  { id: 'examsim', label: 'Simulation สร้างข้อสอบ',   icon: '🎯', phase: 2, comingSoon: true },
  // ── Phase 3 (placeholder) ──
  { id: 'course',  label: 'คอสออนไลน์',              icon: '📚', phase: 3, comingSoon: true }
];

// Role defaults (preset)
const ROLE_ACCESS_PRESETS = {
  blocked:  [],
  member:   ['demo:*'],
  pro:      ['demo:*', 'vlab:vpl01:*', 'manual:vpl01:*'],
  premium:  ['demo:*', 'vlab:vpl01:*', 'vlab:vpl02:*', 'manual:vpl01:*', 'manual:vpl02:*', 'exam:*'],
  ultimate: ['*'],
  admin:    ['*']
};

// Legacy topic mapping (v1 + v2 → v4)
// v1: mechanics/waves/... → demo:mechanics/demo:waves + vlab:vpl01:* (for old data-topic)
// v2: sim_demo/sim_vpl01/doc_vpl01 → demo:*/vlab:vpl01:*/manual:vpl01:*
const LEGACY_TOPIC_MAP = {
  // v1 (physics topic based)
  mechanics:      'demo:mechanics',
  waves:          'demo:waves',
  astronomy:      'demo:astronomy',
  electricity:    'demo:electricity',
  thermodynamics: 'demo:thermodynamics',
  // v2 (simulation/document based)
  sim_demo:       'demo:*',
  sim_vpl01:      'vlab:vpl01:*',
  sim_vpl02:      'vlab:vpl02:*',
  doc_vpl01:      'manual:vpl01:*',
  doc_vpl02:      'manual:vpl02:*'
};

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
      currentUserData = snap.exists ? migrateAccess(snap.data()) : null;
    } catch(e) {
      currentUserData = null;
    }
    // ── Sync watermark tier จาก Firestore → localStorage ──
    syncWatermarkTier(currentUserData);
    updateTopbar(user);
    applyAccessControl();
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

// ── Access Control (v4) ───────────────────────────────────

// Migrate user data → ensure `access` field exists
function migrateAccess(userData) {
  if (!userData) return userData;
  if (Array.isArray(userData.access) && userData.access.length) return userData;

  const access = [];
  const role = userData.role || 'member';

  // Admin/premium เสมอเข้าได้ทุกอย่าง
  if (role === 'admin' || role === 'premium') {
    return { ...userData, access: ['*'] };
  }
  if (role === 'blocked') {
    return { ...userData, access: [] };
  }

  // Derive จาก legacy topics field
  (userData.topics || []).forEach(t => {
    const mapped = LEGACY_TOPIC_MAP[t];
    if (mapped && !access.includes(mapped)) access.push(mapped);
  });

  // Derive จาก legacy labs field (granular per-lab access)
  // Note: ถ้ามี vlab:vpl01:* แล้ว ไม่ต้องเพิ่ม per-lab
  const labs = userData.labs || [];
  const hasVpl01Bundle = access.includes('vlab:vpl01:*');
  const hasVpl02Bundle = access.includes('vlab:vpl02:*');
  labs.forEach(labId => {
    const inVpl01 = VLAB_SERIES.vpl01.labs.includes(labId);
    const inVpl02 = VLAB_SERIES.vpl02.labs.includes(labId);
    if (inVpl01 && !hasVpl01Bundle) {
      const k = 'vlab:vpl01:' + labId;
      if (!access.includes(k)) access.push(k);
    } else if (inVpl02 && !hasVpl02Bundle) {
      const k = 'vlab:vpl02:' + labId;
      if (!access.includes(k)) access.push(k);
    }
  });

  // ถ้ายังไม่มีอะไรเลย → default member
  if (!access.length) access.push('demo:*');

  return { ...userData, access };
}

// Core: เช็คว่า user มีสิทธิ์ access string ที่ต้องการไหม
function hasAccess(required) {
  if (!required) return true;
  if (!currentUserData) return false;
  const userAccess = currentUserData.access || [];

  // Superuser
  if (userAccess.includes('*')) return true;
  // Exact
  if (userAccess.includes(required)) return true;
  // Wildcard parent (e.g. "vlab:vpl01:*" → covers "vlab:vpl01:lab-16")
  const parts = required.split(':');
  for (let i = parts.length - 1; i > 0; i--) {
    if (userAccess.includes(parts.slice(0, i).join(':') + ':*')) return true;
  }
  return false;
}

// คืน flat list ของทุก access ที่ user มี (expand wildcards)
function getUserAccess() {
  return (currentUserData && currentUserData.access) || [];
}

// Back-compat: code เก่าอาจเรียก getUserTopics() อยู่
function getUserTopics() { return getUserAccess(); }

// ใช้สิทธิ์กับทุก element ที่มี data-locked หรือ data-access
function applyAccessControl() {
  document.querySelectorAll('[data-locked="true"], [data-access]').forEach(el => {
    // Prefer data-access (v4), fallback to data-topic (v1/v2)
    let required = el.getAttribute('data-access');
    if (!required) {
      const legacy = el.getAttribute('data-topic') || 'demo:mechanics';
      required = LEGACY_TOPIC_MAP[legacy] || legacy;
    }
    if (hasAccess(required)) unlock(el);
    else lock(el);
  });
}

// Back-compat alias
function applyTopicAccess() { applyAccessControl(); }

function lockAll() {
  document.querySelectorAll('[data-locked="true"], [data-access]').forEach(el => lock(el));
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
  let required = el.getAttribute('data-access');
  if (!required) {
    const legacy = el.getAttribute('data-topic') || 'demo:mechanics';
    required = LEGACY_TOPIC_MAP[legacy] || legacy;
  }
  // หาชื่อจาก ACCESS_SCHEMA
  const [catId, srcId, itemId] = required.split(':');
  let label = required;
  const cat = ACCESS_SCHEMA.find(c => c.id === catId);
  if (cat) {
    label = cat.label;
    if (srcId && srcId !== '*' && cat.items) {
      const src = cat.items.find(i => i.id === srcId);
      if (src) label += ' · ' + src.label;
      if (itemId && itemId !== '*') label += ' · ' + itemId;
    }
  }
  const t = document.getElementById('kp-quota-alert');
  if (t) {
    t.textContent = `🔒 สิทธิ์ "${label}" สำหรับสมาชิกที่ได้รับอนุญาตเท่านั้น`;
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
      access:             ROLE_ACCESS_PRESETS.member,   // v4: ['demo:*']
      topics:             ['sim_demo'],                  // legacy back-compat
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
        access:             ROLE_ACCESS_PRESETS.member,   // v4: ['demo:*']
        topics:             ['sim_demo'],                  // legacy back-compat
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
  member:   { text: 'สมาชิก',      cls: 'kp-role-member',  icon: '🆓' },
  pro:      { text: 'โปร',         cls: 'kp-role-premium', icon: '⭐' },
  premium:  { text: 'พรีเมียม',    cls: 'kp-role-premium', icon: '💎' },
  ultimate: { text: 'Ultimate',    cls: 'kp-role-admin',   icon: '🏆' },
  admin:    { text: 'ผู้ดูแล',     cls: 'kp-role-admin',   icon: '👑' },
  blocked:  { text: 'ถูกระงับ',    cls: 'kp-role-blocked', icon: '🚫' }
};

// Render section ในโปรไฟล์ของแต่ละ category ใน ACCESS_SCHEMA
function renderProfileCategory(cat) {
  const header = '<div class="kp-topic-group-head">' + cat.icon + ' ' + cat.label +
                 (cat.comingSoon ? ' <span class="kp-coming-soon">🔜 เร็วๆ นี้</span>' : '') +
                 '</div>';

  // Coming Soon → แสดงแค่ header + hint
  if (cat.comingSoon) {
    return '<div class="kp-topic-group kp-group-coming">' + header +
           '<div class="kp-coming-hint">อยู่ระหว่างพัฒนา</div></div>';
  }

  let rows = '';
  if (cat.kind === 'subjects') {
    // Demo — แสดง subjects
    rows = cat.items.map(item => {
      const ok = hasAccess(cat.id + ':' + item.id);
      return '<div class="kp-topic-row ' + (ok ? 'allowed' : 'locked') + '">' +
             '<span><span class="kp-topic-ico">' + item.icon + '</span> ' + item.label + '</span>' +
             '<span>' + (ok ? '✅' : '🔒') + '</span></div>';
    }).join('');
  } else if (cat.kind === 'series') {
    // VLab / Manual — แสดง series + นับ lab ที่เข้าถึงได้
    rows = cat.items.map(item => {
      const bundle = hasAccess(cat.id + ':' + item.id + ':*');
      const total  = (item.labs || []).length;
      let unlockedCount;
      if (bundle) {
        unlockedCount = total;
      } else {
        unlockedCount = (item.labs || []).filter(l => hasAccess(cat.id + ':' + item.id + ':' + l)).length;
      }
      const ok = unlockedCount > 0;
      const detail = bundle ? 'ทั้งหมด (' + total + ' รายการ)'
                            : (unlockedCount > 0 ? unlockedCount + '/' + total + ' รายการ'
                                                 : 'ยังไม่มีสิทธิ์');
      return '<div class="kp-topic-row ' + (ok ? 'allowed' : 'locked') + '">' +
             '<span>' + item.label + '</span>' +
             '<span class="kp-topic-detail">' + detail + ' ' + (ok ? '✅' : '🔒') + '</span></div>';
    }).join('');
  }

  return '<div class="kp-topic-group">' + header + rows + '</div>';
}


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

  // Topics (render แบบ grouped ตาม ACCESS_CATEGORIES)
  // Access (render แบบ grouped ตาม ACCESS_SCHEMA v4)
  const topicsEl = document.getElementById('kp-profile-topics');
  if (topicsEl) {
    topicsEl.innerHTML = ACCESS_SCHEMA.map(cat => renderProfileCategory(cat)).join('');
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
