#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
  KP Science — Protect & Setup New HTML Files
  รันสคริปต์นี้ทุกครั้งที่เพิ่มไฟล์ HTML ใหม่เข้าโปรเจกต์

  Usage:
    python3 _admin/protect_new_file.py <file.html>
    python3 _admin/protect_new_file.py --scan          # สแกนหาไฟล์ที่ยังไม่ครบ
    python3 _admin/protect_new_file.py --scan --fix     # สแกน + แก้อัตโนมัติ

  สิ่งที่สคริปต์ทำ:
    1. Google Analytics (G-2YTJBNHP6D)
    2. Frame protection (ป้องกัน iframe)
    3. Domain protection (ป้องกันคัดลอก — เฉพาะ Demo/)
    4. KP Topbar (nav bar + login button)
    5. Topbar CSS
    6. Mobile layout fix (canvas order:-1)
    7. แก้ <\\!-- เป็น <!--
    8. Watermark overlay (VPL01 + VPL02 simulation files)
═══════════════════════════════════════════════════════════════
"""
import os, re, sys, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─── Lab ID extraction ───────────────────────────────────
# VPL01: "16. trajectories_simulation.html" → lab-16
# VPL01: "6.1 pendulum_timer.html" → lab-6.1
# VPL01: "6.2water-clock-simulation.html" → lab-6.2 (decimal ไม่ติด letter)
# VPL02: "32B. light-reflection.html" → lab-32b
# Regex เรียง: decimal ก่อน (กัน match ต่อ letter), fallback integer+letter
LAB_ID_RE = re.compile(r'^(\d+\.\d+|\d+[A-Za-z]?)')

def extract_lab_id(filename):
    """ดึง lab-id จากชื่อไฟล์ e.g. '32B. light-reflection.html' → 'lab-32b'"""
    m = LAB_ID_RE.match(filename)
    if not m:
        return None
    return 'lab-' + m.group(1).lower()

def get_access_string(filepath):
    """Return access string for a lab/demo file"""
    fname = os.path.basename(filepath)

    # Demo files — subject based on folder name
    if '/Demo/' in filepath:
        # เช็ค path segments เพื่อหา subject
        THAI_SUBJECT = {
            'mechanics':   'mechanics',
            'คลื่น':       'waves',
            'ดาราศาสตร์': 'astronomy',
            'แสง':         'optics',
            'แม่เหล็ก':   'magnetism'
        }
        for seg in filepath.split('/'):
            for thai, subj in THAI_SUBJECT.items():
                if thai in seg:
                    return f'demo:{subj}'
        return 'demo:mechanics'  # fallback

    # VPL files
    lab_id = extract_lab_id(fname)
    if not lab_id:
        return None
    if '/Virtual Physics Lab 01/' in filepath:
        return f'vlab:vpl01:{lab_id}'
    if '/Virtual Physics Lab 02/' in filepath:
        return f'vlab:vpl02:{lab_id}'
    return None

# ─── Templates ───────────────────────────────────────────

GA_CODE = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2YTJBNHP6D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-2YTJBNHP6D');
</script>'''

FRAME_PROTECTION = '''<script>
/* KP Science — Frame Protection */
(function(){
  try{
    if(window.self !== window.top){
      window.top.location.href = window.self.location.href;
    }
  }catch(e){
    document.documentElement.innerHTML =
      '<body style="background:#0a0e1a;color:#e2e8f0;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center;padding:20px">' +
      '<div><h1 style="color:#38bdf8">KP Science</h1>' +
      '<p style="margin:1rem 0">This simulation cannot be embedded on other websites.</p>' +
      '<p><a href="index.html" style="color:#38bdf8">Go to KP Science</a></p></div></body>';
  }
})();
</script>'''

DOMAIN_PROTECTION = '''<!-- KP-DOMAIN-PROTECTION — DO NOT REMOVE -->
  <script>
  (function(){
    var allowed = ['kp-science.github.io', 'localhost', '127.0.0.1', ''];
    var host = location.hostname;
    if (host && !allowed.some(function(d){ return host === d || host.endsWith('.' + d); })) {
      document.body.innerHTML =
        '<div style="background:#06090f;color:#f87171;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;text-align:center;padding:2rem">' +
        '<div><div style="font-size:3rem">⛔</div>' +
        '<h2 style="margin:.5rem 0">This file was copied without permission</h2>' +
        '<p style="color:#94a3b8">© 2025 KP Science Simulation</p>' +
        '<p style="color:#94a3b8">Please visit <a href="https://kp-science.github.io/physics-simulations/" style="color:#38bdf8">kp-science.github.io</a></p></div></div>';
    }
  })();
  </script>'''

TOPBAR_CSS = """
/* === KP Topbar === */
.kp-topbar{position:sticky;top:0;z-index:200;background:rgba(6,9,15,0.92);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.07);padding:0 4%;display:flex;align-items:center;height:50px;gap:1.2rem;font-family:'Sarabun',sans-serif}
.kp-topbar .tb-logo{display:flex;align-items:center;gap:.4rem;text-decoration:none;flex-shrink:0}
.kp-topbar .tb-logo-mark{width:28px;height:28px;border-radius:7px;background:linear-gradient(135deg,#38bdf8,#818cf8);display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:900;color:#06090f}
.kp-topbar .tb-logo-text{font-size:.9rem;font-weight:700}.kp-topbar .tb-kp{color:#38bdf8}.kp-topbar .tb-sc{color:#f0f4f8}
.kp-topbar .tb-links{display:flex;gap:1.2rem;margin-left:auto}
.kp-topbar .tb-links a{color:#7c8fa6;text-decoration:none;font-size:.8rem;font-weight:600;transition:.2s}
.kp-topbar .tb-links a:hover{color:#f0f4f8}
.kp-topbar .tb-cta{background:#38bdf8;color:#06090f;padding:5px 14px;border-radius:6px;font-size:.78rem;font-weight:700;text-decoration:none;transition:.2s;white-space:nowrap}
.kp-topbar .tb-cta:hover{background:#7dd3fc}
.kp-topbar .tb-login{display:flex;align-items:center;gap:.3rem;background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;padding:5px 12px;border-radius:6px;font-size:.78rem;font-weight:700;cursor:pointer;transition:.2s;font-family:inherit;white-space:nowrap}
.kp-topbar .tb-login:hover{background:rgba(56,189,248,0.2)}
.kp-topbar .tb-user{display:none;align-items:center;gap:.5rem}
.kp-topbar .tb-user-email{font-size:.75rem;color:#38bdf8;font-weight:600;max-width:100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.kp-topbar .tb-user-logout{font-size:.72rem;color:#7c8fa6;background:none;border:none;cursor:pointer;font-family:inherit}
@media(max-width:768px){.kp-topbar .tb-links{display:none}.kp-topbar .tb-cta{display:none}}
"""


def get_root_path(filepath):
    rel = os.path.relpath(filepath, BASE)
    depth = rel.count(os.sep)
    return '../' * depth if depth > 0 else ''


def get_topbar_html(root_path):
    return f'''<!-- KP Topbar -->
<nav class="kp-topbar">
  <a href="{root_path}index.html" class="tb-logo"><div class="tb-logo-mark">KP</div><div class="tb-logo-text"><span class="tb-kp">KP</span><span class="tb-sc">Science</span></div></a>
  <div class="tb-links"><a href="{root_path}index.html#demos">Demo</a><a href="{root_path}index.html#collections">Collections</a><a href="{root_path}library.html">Library</a><a href="{root_path}index.html#about">\u0e40\u0e01\u0e35\u0e48\u0e22\u0e27\u0e01\u0e31\u0e1a</a><a href="{root_path}index.html#contact">\u0e15\u0e34\u0e14\u0e15\u0e48\u0e2d</a></div>
  <a href="{root_path}index.html#demos" class="tb-cta">\U0001f3ac \u0e43\u0e0a\u0e49\u0e07\u0e32\u0e19\u0e1f\u0e23\u0e35</a>
  <button class="tb-login" id="kp-tb-login" onclick="if(typeof showModal==='function')showModal('login')">\U0001f511 \u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a</button>
  <div class="tb-user" id="kp-tb-user"><span class="tb-user-email" id="kp-tb-email"></span><button class="tb-user-logout" onclick="if(typeof kpLogout==='function')kpLogout()">\u0e2d\u0e2d\u0e01</button></div>
</nav>
'''


# ─── Check functions ─────────────────────────────────────

def check_file(filepath):
    """Check what's missing in a file. Returns list of issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    fname = os.path.basename(filepath)
    is_demo = '/Demo/' in filepath

    # 1. GA code
    if 'G-2YTJBNHP6D' not in content:
        issues.append('GA')

    # 2. Frame protection (VPL files)
    if '/Mechacnics/' in filepath and 'Frame Protection' not in content:
        issues.append('FRAME')

    # 3. Domain protection (Demo files)
    if is_demo and 'KP-DOMAIN-PROTECTION' not in content:
        issues.append('DOMAIN')

    # 4. Topbar
    if 'kp-topbar' not in content and 'class="topbar"' not in content:
        issues.append('TOPBAR')

    # 4a. Topbar HTML exists but CSS missing
    if 'kp-topbar' in content and '.kp-topbar{' not in content and '.kp-topbar {' not in content:
        issues.append('TOPBAR_CSS')

    # 4b. Topbar in wrong position (inside script)
    tp = content.find('kp-topbar')
    cs = content.find('<meta charset')
    if tp != -1 and cs != -1 and tp < cs:
        issues.append('TOPBAR_POS')

    # 5. Escaped comments
    if '<\\!--' in content:
        issues.append('COMMENT')

    # 6. Mobile order fix
    if 'grid-template-columns' in content and 'order:-1' not in content and 'order: -1' not in content:
        # Has grid layout but no mobile order fix
        issues.append('MOBILE')

    # 7. Watermark (VPL01/VPL02/Demo simulation files)
    is_sim = '/Virtual Physics Lab 01/' in filepath or '/Virtual Physics Lab 02/' in filepath or '/Demo/' in filepath
    if is_sim and 'watermark.js' not in content and fname != 'index.html':
        issues.append('WATERMARK')

    # 8. Access Guard (VPL01/VPL02/Demo files — ต้องมี firebase + kp-auth.js + kpPageAccess)
    is_vlab = '/Virtual Physics Lab 01/' in filepath or '/Virtual Physics Lab 02/' in filepath
    is_demo_sim = '/Demo/' in filepath  # Demo ก็ต้องการ page guard
    if (is_vlab or is_demo_sim) and fname != 'index.html':
        if 'firebase-app-compat' not in content:
            issues.append('FIREBASE_CDN')
        if 'kp-auth.js' not in content:
            issues.append('KP_AUTH')
        if 'kpPageAccess(' not in content:
            issues.append('ACCESS_GUARD')

    return issues


def fix_file(filepath, issues=None):
    """Fix all issues in a file."""
    if issues is None:
        issues = check_file(filepath)
    if not issues:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    root_path = get_root_path(filepath)
    changed = False

    # Fix escaped comments
    if 'COMMENT' in issues:
        content = content.replace('<\\!--', '<!--')
        changed = True

    # Add GA code
    if 'GA' in issues:
        head_pos = content.find('<head>')
        if head_pos != -1:
            content = content[:head_pos + 6] + '\n' + GA_CODE + '\n' + content[head_pos + 6:]
            changed = True

    # Add topbar CSS
    if 'TOPBAR' in issues and 'kp-topbar' not in content:
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + TOPBAR_CSS + content[style_end:]
            changed = True

        # Add topbar HTML after <body>
        head_end = content.find('</head>')
        if head_end != -1:
            body_match = re.search(r'<body[^>]*>', content[head_end:])
            if body_match:
                pos = head_end + body_match.end()
                content = content[:pos] + '\n' + get_topbar_html(root_path) + content[pos:]
                changed = True

    # Fix topbar CSS missing (HTML exists but no CSS)
    if 'TOPBAR_CSS' in issues and '.kp-topbar{' not in content and '.kp-topbar {' not in content:
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + TOPBAR_CSS + content[style_end:]
            changed = True

    # Fix topbar position
    if 'TOPBAR_POS' in issues:
        # Remove topbar from wrong position
        content = re.sub(r'<!-- KP Topbar -->.*?</nav>\s*', '', content, flags=re.DOTALL)
        # Re-insert after real <body>
        head_end = content.find('</head>')
        if head_end != -1:
            body_match = re.search(r'<body[^>]*>', content[head_end:])
            if body_match:
                pos = head_end + body_match.end()
                content = content[:pos] + '\n' + get_topbar_html(root_path) + content[pos:]
                changed = True

    # Add watermark script (VPL files)
    if 'WATERMARK' in issues and 'watermark.js' not in content:
        wm_root = get_root_path(filepath)
        wm_tag = f'\n<!-- KP Watermark -->\n<script src="{wm_root}_shared/watermark.js"></script>\n'
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + wm_tag + content[body_end:]
            changed = True

    # Add Firebase CDN + kp-auth.js + access guard (VPL01/VPL02 files)
    if 'FIREBASE_CDN' in issues and 'firebase-app-compat' not in content:
        auth_root = get_root_path(filepath)
        fb_tag = (
            f'\n<!-- KP Auth (Firebase) -->\n'
            f'<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>\n'
            f'<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>\n'
            f'<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>\n'
            f'<script src="{auth_root}kp-auth.js"></script>\n'
        )
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + fb_tag + content[body_end:]
            changed = True
    elif 'KP_AUTH' in issues and 'kp-auth.js' not in content:
        # มี firebase แล้วแต่ยังไม่มี kp-auth.js
        auth_root = get_root_path(filepath)
        auth_tag = f'\n<script src="{auth_root}kp-auth.js"></script>\n'
        # ใส่หลัง firebase-firestore
        idx = content.find('firebase-firestore-compat')
        if idx != -1:
            end_tag = content.find('</script>', idx)
            if end_tag != -1:
                content = content[:end_tag+9] + auth_tag + content[end_tag+9:]
                changed = True
        else:
            body_end = content.rfind('</body>')
            if body_end != -1:
                content = content[:body_end] + auth_tag + content[body_end:]
                changed = True

    # Add page-level access guard
    if 'ACCESS_GUARD' in issues and 'kpPageAccess(' not in content:
        access = get_access_string(filepath)
        if access:
            # redirect กลับไปหน้า listing
            if '/Virtual Physics Lab 01/' in filepath:
                listing = get_root_path(filepath) + 'virtual-physics-lab-01.html'
            elif '/Virtual Physics Lab 02/' in filepath:
                listing = get_root_path(filepath) + 'virtual-physics-lab-02.html'
            elif '/Demo/' in filepath:
                # map subject → demo listing page
                subject = access.split(':')[1] if ':' in access else 'mechanics'
                listing = get_root_path(filepath) + f'demo-{subject}.html'
            else:
                listing = get_root_path(filepath) + 'index.html'
            guard_tag = (
                f'\n<!-- KP Page Access Guard -->\n'
                f'<script>\n'
                f'  // รอให้ kp-auth.js โหลดเสร็จก่อน\n'
                f'  (function(){{\n'
                f'    var w = setInterval(function(){{\n'
                f'      if (typeof kpPageAccess === "function") {{\n'
                f'        clearInterval(w);\n'
                f'        kpPageAccess("{access}", "{listing}");\n'
                f'      }}\n'
                f'    }}, 50);\n'
                f'    setTimeout(function(){{clearInterval(w)}}, 5000);\n'
                f'  }})();\n'
                f'</script>\n'
            )
            body_end = content.rfind('</body>')
            if body_end != -1:
                content = content[:body_end] + guard_tag + content[body_end:]
                changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changed


# ─── Main ────────────────────────────────────────────────

def scan_all():
    """Scan all HTML files and report issues."""
    print("═══ KP Science — File Health Scan ═══\n")

    all_files = []
    for root, dirs, fnames in os.walk(BASE):
        # Skip folders
        skip = ['_admin', '_marketing', 'lab-manuals', 'node_modules', '.git']
        if any(s in root for s in skip):
            continue
        for fn in fnames:
            if fn.endswith('.html'):
                all_files.append(os.path.join(root, fn))

    ok_count = 0
    issue_count = 0

    for fpath in sorted(all_files):
        issues = check_file(fpath)
        rel = os.path.relpath(fpath, BASE)
        if issues:
            print(f"  ⚠️  {rel}")
            for issue in issues:
                labels = {
                    'GA': 'ขาด Google Analytics',
                    'FRAME': 'ขาด Frame Protection',
                    'DOMAIN': 'ขาด Domain Protection',
                    'TOPBAR': 'ขาด KP Topbar',
                    'TOPBAR_CSS': 'Topbar ขาด CSS',
                    'TOPBAR_POS': 'Topbar อยู่ผิดตำแหน่ง',
                    'COMMENT': 'มี <\\!-- (escaped comment)',
                    'MOBILE': 'ขาด mobile order fix',
                    'WATERMARK': 'ขาด Watermark overlay',
                    'FIREBASE_CDN': 'ขาด Firebase CDN',
                    'KP_AUTH': 'ขาด kp-auth.js',
                    'ACCESS_GUARD': 'ขาด Page Access Guard',
                }
                print(f"      → {labels.get(issue, issue)}")
            issue_count += 1
        else:
            ok_count += 1

    print(f"\n✅ OK: {ok_count}  ⚠️ Issues: {issue_count}  Total: {ok_count + issue_count}")
    return issue_count


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    if sys.argv[1] == '--scan':
        issues = scan_all()
        if '--fix' in sys.argv and issues > 0:
            print("\n═══ Auto-fixing... ═══\n")
            for root, dirs, fnames in os.walk(BASE):
                skip = ['_admin', '_marketing', 'lab-manuals', 'node_modules', '.git']
                if any(s in root for s in skip):
                    continue
                for fn in fnames:
                    if fn.endswith('.html'):
                        fpath = os.path.join(root, fn)
                        file_issues = check_file(fpath)
                        if file_issues:
                            if fix_file(fpath, file_issues):
                                rel = os.path.relpath(fpath, BASE)
                                print(f"  Fixed: {rel} ({', '.join(file_issues)})")
            print("\n═══ Re-scanning... ═══")
            scan_all()
    else:
        # Process specific file
        fpath = os.path.abspath(sys.argv[1])
        if not os.path.exists(fpath):
            print(f"File not found: {fpath}")
            sys.exit(1)

        issues = check_file(fpath)
        if not issues:
            print(f"✅ {os.path.basename(fpath)} — ครบทุกอย่างแล้ว")
        else:
            print(f"⚠️  {os.path.basename(fpath)} — ต้องแก้:")
            for i in issues:
                print(f"   → {i}")
            fix_file(fpath, issues)
            print(f"✅ แก้เสร็จแล้ว!")
