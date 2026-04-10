#!/usr/bin/env python3
"""
Fix auth modal + download button in Lab 6.1-15 simulation files.

Problem: cowork injected modal CSS/HTML/scripts inside frame-busting <script>,
breaking HTML structure. This script moves everything to correct locations.
"""
import os
import re

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "Virtual Physics Lab 01", "Mechacnics")

FILES = [
    "6.1 pendulum_timer.html",
    "6.2water-clock-simulation.html",
    "6.3 tape_timer_simulation.html",
    "7. strobe_photography_simulation.html",
    "8. straight-line-motion-simulation.html",
    "9. galileo-water-clock-simulation.html",
    "10. spinning_disc_sim.html",
    "11. air_track_simulation.html",
    "12. turntable_gravity_simulation.html",
    "13. free-fall-experiment.html",
    "14.mass_weight_simulation.html",
    "15. newtons_second_law_simulation.html",
]

# Clean frame-busting script
CLEAN_FRAME_BUST = """<script>
/* KP Science \u2014 Frame Protection */
(function(){
  try{
    if(window.self !== window.top){
      window.top.location.href = window.self.location.href;
    }
  }catch(e){
    document.documentElement.innerHTML =
      '<body style="background:#0a0e1a;color:#e2e8f0;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center;padding:20px">' +
      '<div><h1 style="color:#38bdf8">\\ud83d\\udd12 KP Science</h1>' +
      '<p>\\u0e2a\\u0e37\\u0e48\\u0e2d\\u0e19\\u0e35\\u0e49\\u0e44\\u0e21\\u0e48\\u0e2d\\u0e19\\u0e38\\u0e0d\\u0e32\\u0e15\\u0e43\\u0e2b\\u0e49\\u0e41\\u0e2a\\u0e14\\u0e07\\u0e1c\\u0e48\\u0e32\\u0e19\\u0e40\\u0e27\\u0e47\\u0e1a\\u0e44\\u0e0b\\u0e15\\u0e4c\\u0e2d\\u0e37\\u0e48\\u0e19</p>' +
      '<p><a href="../../index.html" style="color:#38bdf8">\\u2190 \\u0e01\\u0e25\\u0e31\\u0e1a\\u0e2a\\u0e39\\u0e48 KP Science</a></p></div></body>';
  }
})();
</script>"""

# Actually use readable Thai text in the frame-busting
CLEAN_FRAME_BUST = '<script>\n/* KP Science \u2014 Frame Protection */\n(function(){\n  try{\n    if(window.self !== window.top){\n      window.top.location.href = window.self.location.href;\n    }\n  }catch(e){\n    document.documentElement.innerHTML =\n      \'<body style="background:#0a0e1a;color:#e2e8f0;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center;padding:20px">\' +\n      \'<div><h1 style="color:#38bdf8">KP Science</h1>\' +\n      \'<p style="margin:1rem 0">This simulation cannot be embedded on other websites.</p>\' +\n      \'<p><a href="../../index.html" style="color:#38bdf8">Go to KP Science</a></p></div></body>\';\n  }\n})();\n</script>'

# CSS to add to main <style> block
MODAL_CSS = """
/* === Download button === */
.btn-dl-pdf{display:inline-flex;align-items:center;gap:6px;background:transparent;border:2px solid rgba(52,211,153,0.75);color:#34d399;padding:6px 18px;border-radius:20px;font-family:'Sarabun',sans-serif;font-size:0.83rem;font-weight:700;text-decoration:none;transition:all .2s;cursor:pointer}
.btn-dl-pdf:hover{background:rgba(52,211,153,0.12);border-color:#34d399}
/* === Auth Modal === */
#kp-auth-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:9999;align-items:center;justify-content:center;padding:1rem}
#kp-auth-modal.open{display:flex}
.kp-modal-box{background:#0d1421;border:1px solid rgba(255,255,255,0.12);border-radius:16px;width:100%;max-width:420px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,0.5)}
.kp-modal-head{padding:1.25rem 1.5rem 0;display:flex;justify-content:space-between;align-items:center}
.kp-modal-head h3{font-size:1.05rem;font-weight:700}
.kp-modal-close{background:none;border:none;color:var(--muted);font-size:1.2rem;cursor:pointer;padding:4px 8px;border-radius:6px;transition:.2s}
.kp-modal-close:hover{color:var(--text);background:rgba(255,255,255,0.07)}
.kp-tabs{display:flex;gap:0;padding:1rem 1.5rem 0;border-bottom:1px solid rgba(255,255,255,0.07)}
.kp-tab{background:none;border:none;color:var(--muted);font-size:.9rem;font-weight:600;padding:.5rem 1rem;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;transition:.2s;font-family:'Sarabun',sans-serif}
.kp-tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.kp-tab-pane{display:none;padding:1.5rem}
.kp-tab-pane.active{display:block}
.kp-field{margin-bottom:1rem}
.kp-field label{display:block;font-size:.8rem;color:var(--muted);margin-bottom:.35rem;font-weight:600}
.kp-field input{width:100%;background:#161b27;border:1px solid rgba(255,255,255,0.1);color:var(--text);padding:.65rem .9rem;border-radius:8px;font-family:'Sarabun',sans-serif;font-size:.9rem;outline:none;transition:.2s;box-sizing:border-box}
.kp-field input:focus{border-color:var(--accent)}
.kp-submit{width:100%;background:var(--accent);color:#06090f;border:none;padding:.75rem;border-radius:9px;font-size:.95rem;font-weight:700;cursor:pointer;transition:.2s;font-family:'Sarabun',sans-serif}
.kp-submit:hover{background:#7dd3fc}
.kp-google-btn{width:100%;display:flex;align-items:center;justify-content:center;gap:.6rem;background:#fff;color:#1f1f1f;border:none;padding:.72rem;border-radius:9px;font-size:.92rem;font-weight:600;cursor:pointer;font-family:'Sarabun',sans-serif;transition:.2s;margin-bottom:1rem}
.kp-google-btn:hover{background:#f1f1f1}
.kp-divider{display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;color:var(--muted);font-size:.78rem}
.kp-divider::before,.kp-divider::after{content:'';flex:1;height:1px;background:rgba(255,255,255,0.08)}
.kp-err{color:#f87171;font-size:.82rem;min-height:1.2rem;margin-bottom:.5rem}
.kp-switch{text-align:center;font-size:.82rem;color:var(--muted);margin-top:.75rem}
.kp-switch button{background:none;border:none;color:var(--accent);cursor:pointer;font-family:'Sarabun',sans-serif;font-weight:600}"""

# Modal HTML + scripts to insert before </body>
GOOGLE_SVG = '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'

MODAL_HTML = f'''
<!-- KP Auth Modal -->
<div id="kp-auth-modal">
  <div class="kp-modal-box">
    <div class="kp-modal-head">
      <h3>\U0001f511 KP Science \u2014 \u0e2a\u0e21\u0e32\u0e0a\u0e34\u0e01</h3>
      <button class="kp-modal-close" onclick="hideModal()">\u2715</button>
    </div>
    <div class="kp-tabs">
      <button class="kp-tab active" id="tab-login" onclick="switchTab('login')">\u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a</button>
      <button class="kp-tab" id="tab-register" onclick="switchTab('register')">\u0e2a\u0e21\u0e31\u0e04\u0e23\u0e2a\u0e21\u0e32\u0e0a\u0e34\u0e01</button>
    </div>
    <div class="kp-tab-pane active" id="pane-login">
      <button class="kp-google-btn" onclick="kpLoginGoogle()">
        {GOOGLE_SVG}
        \u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a\u0e14\u0e49\u0e27\u0e22 Google
      </button>
      <div class="kp-divider">\u0e2b\u0e23\u0e37\u0e2d</div>
      <div class="kp-field"><label>\u0e2d\u0e35\u0e40\u0e21\u0e25</label><input type="email" id="kp-login-email" placeholder="your@email.com" /></div>
      <div class="kp-field"><label>\u0e23\u0e2b\u0e31\u0e2a\u0e1c\u0e48\u0e32\u0e19</label><input type="password" id="kp-login-pass" placeholder="\u2022\u2022\u2022\u2022\u2022\u2022" onkeydown="if(event.key==='Enter')kpLogin()" /></div>
      <div class="kp-err" id="kp-login-err"></div>
      <button class="kp-submit" onclick="kpLogin()">\u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a</button>
      <div class="kp-switch">\u0e22\u0e31\u0e07\u0e44\u0e21\u0e48\u0e21\u0e35\u0e1a\u0e31\u0e0d\u0e0a\u0e35? <button onclick="switchTab('register')">\u0e2a\u0e21\u0e31\u0e04\u0e23\u0e1f\u0e23\u0e35</button></div>
    </div>
    <div class="kp-tab-pane" id="pane-register">
      <button class="kp-google-btn" onclick="kpLoginGoogle()">
        {GOOGLE_SVG}
        \u0e2a\u0e21\u0e31\u0e04\u0e23\u0e14\u0e49\u0e27\u0e22 Google
      </button>
      <div class="kp-divider">\u0e2b\u0e23\u0e37\u0e2d\u0e2a\u0e21\u0e31\u0e04\u0e23\u0e14\u0e49\u0e27\u0e22\u0e2d\u0e35\u0e40\u0e21\u0e25</div>
      <div class="kp-field"><label>\u0e2d\u0e35\u0e40\u0e21\u0e25</label><input type="email" id="kp-reg-email" placeholder="your@email.com" /></div>
      <div class="kp-field"><label>\u0e23\u0e2b\u0e31\u0e2a\u0e1c\u0e48\u0e32\u0e19</label><input type="password" id="kp-reg-pass" placeholder="\u0e2d\u0e22\u0e48\u0e32\u0e07\u0e19\u0e49\u0e2d\u0e22 6 \u0e15\u0e31\u0e27\u0e2d\u0e31\u0e01\u0e29\u0e23" /></div>
      <div class="kp-field"><label>\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19\u0e23\u0e2b\u0e31\u0e2a\u0e1c\u0e48\u0e32\u0e19</label><input type="password" id="kp-reg-pass2" placeholder="\u2022\u2022\u2022\u2022\u2022\u2022" onkeydown="if(event.key==='Enter')kpRegister()" /></div>
      <div class="kp-err" id="kp-reg-err"></div>
      <button class="kp-submit" onclick="kpRegister()">\u0e2a\u0e21\u0e31\u0e04\u0e23\u0e2a\u0e21\u0e32\u0e0a\u0e34\u0e01\u0e1f\u0e23\u0e35</button>
      <div class="kp-switch">\u0e21\u0e35\u0e1a\u0e31\u0e0d\u0e0a\u0e35\u0e41\u0e25\u0e49\u0e27? <button onclick="switchTab('login')">\u0e40\u0e02\u0e49\u0e32\u0e2a\u0e39\u0e48\u0e23\u0e30\u0e1a\u0e1a</button></div>
    </div>
  </div>
</div>

<script>
function dlPdf(path, labNum) {{
  var FREE_LABS = [1, 2, 3, 4, 5];
  var num = parseFloat(labNum) || 0;
  var isFree = FREE_LABS.some(function(n){{ return Math.abs(n - num) < 0.01; }}) || num < 1;
  if (isFree) {{
    _doDl(path);
  }} else {{
    if (typeof currentUser !== 'undefined' && currentUser) {{
      _doDl(path);
    }} else {{
      if (typeof showModal === 'function') showModal('login');
    }}
  }}
}}
function _doDl(path) {{
  var a = document.createElement('a');
  a.href = path; a.download = '';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}}
</script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>
<script src="../../kp-auth.js"></script>'''


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)

    # Step 1: Find and replace the broken frame-busting section
    # Pattern: from the frame-busting <script> to <meta charset="UTF-8">
    # The broken section starts after GA script and ends just before <meta charset

    # Find the start marker: the frame-busting script
    # It can start with either:
    # - <script>\n/* KP Science — Frame Protection */ (after meta CSP tags)
    # We need to find everything from the frame-busting script to <meta charset

    # Strategy: find <meta charset="UTF-8"> and replace everything between
    # the last </script> of GA and <meta charset with clean frame-busting

    # Find the GA closing tag position
    ga_end = content.find("gtag('config', 'G-2YTJBNHP6D');")
    if ga_end == -1:
        print(f"  SKIP {fname}: GA config not found")
        return False
    ga_script_end = content.find('</script>', ga_end)
    if ga_script_end == -1:
        print(f"  SKIP {fname}: GA </script> not found")
        return False
    ga_script_end += len('</script>')

    # Find <meta charset="UTF-8">
    meta_charset = content.find('<meta charset="UTF-8">')
    if meta_charset == -1:
        print(f"  SKIP {fname}: <meta charset> not found")
        return False

    # The section between GA script end and meta charset is the broken part
    broken_section = content[ga_script_end:meta_charset]

    # Build clean replacement
    clean_replacement = '\n' + CLEAN_FRAME_BUST + '\n\n'

    # Replace broken section
    content = content[:ga_script_end] + clean_replacement + content[meta_charset:]

    # Step 2: Add modal CSS to main <style> block (if not already there)
    if '#kp-auth-modal' not in content.split('<meta charset')[1].split('</style>')[0]:
        # Find the closing </style> of the main style block
        style_start = content.find('<style>', content.find('<meta charset'))
        if style_start == -1:
            print(f"  SKIP {fname}: main <style> not found")
            return False
        style_end = content.find('</style>', style_start)
        if style_end == -1:
            print(f"  SKIP {fname}: </style> not found")
            return False

        # Insert modal CSS before </style>
        content = content[:style_end] + MODAL_CSS + '\n' + content[style_end:]

    # Step 3: Add modal HTML + scripts before </body> (if not already there)
    # First check if modal HTML already exists in the correct location (after main content)
    body_end = content.rfind('</body>')
    if body_end == -1:
        print(f"  SKIP {fname}: </body> not found")
        return False

    # Check if kp-auth-modal already exists in the page body (not in frame-busting)
    main_content = content[content.find('<meta charset'):]
    if 'id="kp-auth-modal"' not in main_content:
        content = content[:body_end] + MODAL_HTML + '\n' + content[body_end:]
    else:
        print(f"  INFO {fname}: modal HTML already in correct location")

    # Step 4: Remove any stray content from broken injection
    # Look for orphaned </body>'; or })(); between frame-busting and meta charset
    # This should already be handled by Step 1's replacement

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {fname}")
    return True


def verify_file(filepath):
    """Verify the fixed file has correct structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    errors = []

    # Check frame-busting is clean (no modal CSS inside it)
    fb_start = content.find('/* KP Science')
    fb_end = content.find('</script>', fb_start) if fb_start != -1 else -1
    if fb_start != -1 and fb_end != -1:
        fb_section = content[fb_start:fb_end]
        if 'kp-auth-modal' in fb_section:
            errors.append("modal code still inside frame-busting script")
        if 'btn-dl-pdf' in fb_section:
            errors.append("btn-dl-pdf CSS still inside frame-busting script")

    # Check modal CSS is in main <style>
    main_style_start = content.find('<style>', content.find('<meta charset'))
    main_style_end = content.find('</style>', main_style_start) if main_style_start != -1 else -1
    if main_style_start != -1 and main_style_end != -1:
        main_style = content[main_style_start:main_style_end]
        if '#kp-auth-modal' not in main_style:
            errors.append("modal CSS missing from main <style>")
        if '.btn-dl-pdf' not in main_style:
            errors.append("btn-dl-pdf CSS missing from main <style>")
        if '.kp-divider::before' not in main_style:
            errors.append("kp-divider pseudo-elements missing")

    # Check modal HTML exists before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        pre_body = content[body_end-200:body_end]
        if 'kp-auth.js' not in pre_body:
            errors.append("kp-auth.js not found before </body>")

    # Check dlPdf function exists outside frame-busting
    after_charset = content[content.find('<meta charset'):]
    if 'function dlPdf' not in after_charset:
        errors.append("dlPdf function not found in page content")

    # Check download button in nav
    if 'btn-dl-pdf' not in after_charset.split('</nav>')[0] if '</nav>' in after_charset else '':
        # Try to find it differently
        if 'class="btn-dl-pdf"' not in after_charset:
            errors.append("download button not found in nav")

    if errors:
        print(f"  FAIL {fname}: {'; '.join(errors)}")
        return False
    else:
        print(f"  PASS {fname}")
        return True


if __name__ == '__main__':
    print("=== Fixing 12 Lab files ===\n")

    fixed = 0
    for fname in FILES:
        fpath = os.path.join(BASE, fname)
        if not os.path.exists(fpath):
            print(f"  MISS {fname}")
            continue
        if fix_file(fpath):
            fixed += 1

    print(f"\nFixed: {fixed}/{len(FILES)}\n")

    print("=== Verifying ===\n")
    passed = 0
    for fname in FILES:
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath) and verify_file(fpath):
            passed += 1

    print(f"\nPassed: {passed}/{len(FILES)}")
