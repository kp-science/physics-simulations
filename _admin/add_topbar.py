#!/usr/bin/env python3
"""
Add unified KP Science topbar to all simulation + page files.
Topbar includes: logo, nav links, "ทดลองฟรี" CTA, login/user menu.
Removes old "← กลับหน้าแรก" back button since topbar replaces it.
"""
import os, re, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CSS for topbar (injected into <style>)
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

def get_topbar_html(root_path):
    """Generate topbar HTML with correct relative paths."""
    return f'''<!-- KP Topbar -->
<nav class="kp-topbar">
  <a href="{root_path}index.html" class="tb-logo">
    <div class="tb-logo-mark">KP</div>
    <div class="tb-logo-text"><span class="tb-kp">KP</span><span class="tb-sc">Science</span></div>
  </a>
  <div class="tb-links">
    <a href="{root_path}index.html#demos">Demo</a>
    <a href="{root_path}index.html#collections">Collections</a>
    <a href="{root_path}library.html">Library</a>
    <a href="{root_path}index.html#about">\u0e40\u0e01\u0e35\u0e48\u0e22\u0e27\u0e01\u0e31\u0e1a</a>
    <a href="{root_path}index.html#contact">\u0e15\u0e34\u0e14\u0e15\u0e48\u0e2d</a>
  </div>
  <a href="{root_path}index.html#demos" class="tb-cta">\U0001f3ac \u0e17\u0e14\u0e25\u0e2d\u0e07\u0e1f\u0e23\u0e35</a>
  <button class="tb-login" id="kp-tb-login" onclick="if(typeof showModal==='function')showModal('login')">\U0001f511 \u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a</button>
  <div class="tb-user" id="kp-tb-user">
    <span class="tb-user-email" id="kp-tb-email"></span>
    <button class="tb-user-logout" onclick="if(typeof kpLogout==='function')kpLogout()">\u0e2d\u0e2d\u0e01</button>
  </div>
</nav>
'''

# JS to toggle login/user display based on auth state
TOPBAR_JS = """<script>
/* KP Topbar auth toggle */
(function(){
  var iv=setInterval(function(){
    if(typeof firebase!=='undefined'&&firebase.auth){
      clearInterval(iv);
      firebase.auth().onAuthStateChanged(function(u){
        var lb=document.getElementById('kp-tb-login');
        var um=document.getElementById('kp-tb-user');
        var em=document.getElementById('kp-tb-email');
        if(!lb||!um) return;
        if(u){lb.style.display='none';um.style.display='flex';if(em)em.textContent=u.email.split('@')[0];}
        else{lb.style.display='flex';um.style.display='none';}
      });
    }
  },300);
  setTimeout(function(){clearInterval(iv)},10000);
})();
</script>"""


def get_root_path(filepath):
    """Calculate relative path to project root from file location."""
    rel = os.path.relpath(filepath, BASE)
    depth = rel.count(os.sep)
    if depth == 0:
        return ''
    return '../' * depth


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)

    # Skip if already has topbar
    if 'kp-topbar' in content:
        print(f"  SKIP {fname}: already has topbar")
        return False

    root_path = get_root_path(filepath)
    changed = False

    # 1. Add topbar CSS before </style>
    style_end = content.find('</style>')
    if style_end != -1:
        content = content[:style_end] + TOPBAR_CSS + content[style_end:]
        changed = True
    else:
        print(f"  WARN {fname}: no </style> found, skipping CSS")

    # 2. Add topbar HTML after <body> (before any other content)
    body_match = re.search(r'<body[^>]*>', content)
    if body_match:
        insert_pos = body_match.end()
        # Skip whitespace/newlines
        while insert_pos < len(content) and content[insert_pos] in '\n\r\t ':
            insert_pos += 1
        topbar_html = '\n' + get_topbar_html(root_path)
        content = content[:insert_pos] + topbar_html + content[insert_pos:]
        changed = True
    else:
        print(f"  WARN {fname}: no <body> found")

    # 3. Remove old back button (← กลับหน้าแรก) since topbar replaces it
    # Remove the <a> tag
    content = re.sub(
        r'<a[^>]*class="kp-back-btn"[^>]*>.*?</a>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove the CSS for kp-back-btn (but keep if it's used elsewhere)
    content = re.sub(
        r'\.kp-back-btn\s*\{[^}]*\}\s*',
        '',
        content
    )
    content = re.sub(
        r'\.kp-back-btn:hover\s*\{[^}]*\}\s*',
        '',
        content
    )
    content = re.sub(
        r'@media[^{]*\{[^}]*\.kp-back-btn[^}]*\}\s*\}',
        '',
        content
    )

    # 4. Add topbar auth JS before </body> (if kp-auth.js is loaded)
    if 'kp-auth.js' in content and 'KP Topbar auth' not in content:
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + TOPBAR_JS + '\n' + content[body_end:]

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK   {fname}")
        return True
    return False


if __name__ == '__main__':
    print("=== Adding KP Topbar to all files ===\n")

    # Collect all files to update
    files = []

    # VPL simulations
    vpl_dir = os.path.join(BASE, "Virtual Physics Lab 01", "Mechacnics")
    files.extend(sorted(glob.glob(os.path.join(vpl_dir, "*.html"))))

    # Demo simulations
    demo_dir = os.path.join(BASE, "Demo", "mechanics")
    for root, dirs, fnames in os.walk(demo_dir):
        for fn in sorted(fnames):
            if fn.endswith('.html'):
                files.append(os.path.join(root, fn))

    # Main pages (skip index.html which already has its own topbar)
    for pg in ['mechanics.html', 'course.html', 'plane_mirror_reflection.html']:
        fp = os.path.join(BASE, pg)
        if os.path.exists(fp):
            files.append(fp)

    # Also add to VPL page and library if they don't have it
    # (They already have a different topbar class, skip them)

    count = 0
    for fpath in files:
        if os.path.exists(fpath):
            if fix_file(fpath):
                count += 1

    print(f"\nDone: {count} files updated")
