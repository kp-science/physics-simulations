#!/usr/bin/env python3
"""Add auth-aware download buttons + modal + lock system to Lab 16-20."""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MECH = os.path.join(BASE, "Virtual Physics Lab 01", "Mechacnics")

FILES = {
    "16. trajectories_simulation.html": ("../lab-manuals-pdf/คู่มือการทดลอง_16_trajectories.pdf", 16),
    "17. centripetal_force_simulation.html": ("../lab-manuals-pdf/คู่มือการทดลอง_17_centripetal_force.pdf", 17),
    "18. newton_third_law_simulation.html": ("../lab-manuals-pdf/คู่มือการทดลอง_18_newton_third_law.pdf", 18),
    "19.pendulum_energy_sim.html": ("../lab-manuals-pdf/คู่มือการทดลอง_19_pendulum_energy.pdf", 19),
    "20. tilted_air_track.html": ("../lab-manuals-pdf/คู่มือการทดลอง_20_tilted_air_track.pdf", 20),
}

GOOGLE_SVG = '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'

# CSS to add before </style>
DL_CSS = """
/* Download button */
.btn-dl-pdf{display:inline-flex;align-items:center;gap:6px;background:transparent;border:2px solid rgba(52,211,153,0.75);color:#34d399;padding:6px 18px;border-radius:20px;font-family:'Sarabun',sans-serif;font-size:0.83rem;font-weight:700;text-decoration:none;transition:all .2s;cursor:pointer}
.btn-dl-pdf:hover{background:rgba(52,211,153,0.12);border-color:#34d399}
/* Auth Modal */
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
.kp-switch button{background:none;border:none;color:var(--accent);cursor:pointer;font-family:'Sarabun',sans-serif;font-weight:600}
/* Download lock state */
.dl-locked{border-color:rgba(148,163,184,0.5)!important;color:#94a3b8!important}
.dl-locked:hover{border-color:rgba(148,163,184,0.7)!important;background:rgba(148,163,184,0.08)!important}
"""

def get_body_block(pdf_path, lab_num):
    return f"""
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
  if (isFree) {{ _doDl(path); }}
  else {{
    if (typeof currentUser !== 'undefined' && currentUser) {{ _doDl(path); }}
    else {{ if (typeof showModal === 'function') showModal('login'); }}
  }}
}}
function _doDl(path) {{
  if (typeof logDownload === 'function') logDownload(path);
  var a = document.createElement('a');
  a.href = path; a.download = '';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}}
</script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>
<script src="../../kp-auth.js"></script>
<script>
/* KP Download Lock \u2014 auto lock/unlock based on auth */
(function(){{
  var FREE=[1,2,3,4,5];
  function isFree(n){{return FREE.some(function(f){{return Math.abs(f-n)<0.01}})||n<1}}
  function getLabBtns(){{
    var r=[];
    document.querySelectorAll('.btn-dl-pdf,.sc-dl-btn,.lib-dl-btn').forEach(function(b){{
      var oc=b.getAttribute('onclick')||'';
      var m=oc.match(/dlPdf\\([^,]+,\\s*([\\d.]+)\\)/);
      if(m){{var n=parseFloat(m[1]);if(!isFree(n))r.push(b)}}
    }});
    return r;
  }}
  function update(user){{
    getLabBtns().forEach(function(b){{
      var t=b.textContent.replace(/^[\\u2b07\\u{{1f512}}\\u{{1f513}}]\\s*/u,'').replace(/^\u2b07\\s*/,'');
      if(user){{b.classList.remove('dl-locked');b.textContent='\\u2b07 '+t}}
      else{{b.classList.add('dl-locked');b.textContent='\\u{{1f512}} '+t}}
    }});
  }}
  update(null);
  var iv=setInterval(function(){{
    if(typeof firebase!=='undefined'&&firebase.auth){{
      clearInterval(iv);
      firebase.auth().onAuthStateChanged(update);
    }}
  }},200);
  setTimeout(function(){{clearInterval(iv)}},10000);
}})();
</script>"""

def fix_file(filepath, pdf_path, lab_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)

    if 'kp-auth-modal' in content:
        print(f"  SKIP {fname}: already has auth system")
        return False

    # 1. Add CSS before </style>
    style_end = content.find('</style>')
    if style_end == -1:
        print(f"  SKIP {fname}: no </style>")
        return False
    content = content[:style_end] + DL_CSS + '\n' + content[style_end:]

    # 2. Add download button before </nav>
    nav_end = content.find('</nav>')
    if nav_end == -1:
        print(f"  SKIP {fname}: no </nav>")
        return False
    dl_btn = f'\n  <button class="btn-dl-pdf" onclick="dlPdf(\'{pdf_path}\',{lab_num})">\u2b07 \u0e14\u0e32\u0e27\u0e19\u0e4c\u0e42\u0e2b\u0e25\u0e14\u0e04\u0e39\u0e48\u0e21\u0e37\u0e2d Lab</button>\n'
    content = content[:nav_end] + dl_btn + content[nav_end:]

    # 3. Add modal + scripts before </body>
    body_end = content.rfind('</body>')
    if body_end == -1:
        print(f"  SKIP {fname}: no </body>")
        return False
    content = content[:body_end] + get_body_block(pdf_path, lab_num) + '\n' + content[body_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {fname}")
    return True


if __name__ == '__main__':
    print("=== Adding download system to Lab 16-20 ===\n")
    count = 0
    for fname, (pdf, num) in FILES.items():
        fpath = os.path.join(MECH, fname)
        if os.path.exists(fpath):
            if fix_file(fpath, pdf, num):
                count += 1
        else:
            print(f"  MISS {fname}")
    print(f"\nDone: {count}/{len(FILES)}")
