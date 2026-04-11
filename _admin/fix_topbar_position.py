#!/usr/bin/env python3
"""
Fix topbar position — move from inside frame-busting script to after real <body>.
Also clean up the broken frame-busting script.
"""
import os, re, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEAN_FRAME_BUST = '''<script>
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
      '<p><a href="../../index.html" style="color:#38bdf8">Go to KP Science</a></p></div></body>';
  }
})();
</script>'''


def get_root_path(filepath):
    rel = os.path.relpath(filepath, BASE)
    depth = rel.count(os.sep)
    return '../' * depth if depth > 0 else ''


def get_topbar_html(root_path):
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


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)

    # Check if topbar is before <meta charset (= inside frame-busting)
    topbar_pos = content.find('kp-topbar')
    charset_pos = content.find('<meta charset')
    if topbar_pos == -1 or charset_pos == -1:
        return False
    if topbar_pos > charset_pos:
        # Topbar is after charset = correct position
        return False

    # Step 1: Find and replace everything from frame-busting script to <meta charset
    # with clean frame-busting
    ga_end_marker = "gtag('config', 'G-2YTJBNHP6D');"
    ga_pos = content.find(ga_end_marker)
    if ga_pos == -1:
        print(f"  SKIP {fname}: no GA config found")
        return False

    ga_script_end = content.find('</script>', ga_pos)
    if ga_script_end == -1:
        return False
    ga_script_end += len('</script>')

    charset_match = content.find('<meta charset="UTF-8">')
    if charset_match == -1:
        charset_match = content.find('<meta charset=')
    if charset_match == -1:
        print(f"  SKIP {fname}: no <meta charset>")
        return False

    # Replace the broken section with clean frame-busting
    content = content[:ga_script_end] + '\n' + CLEAN_FRAME_BUST + '\n\n' + content[charset_match:]

    # Step 2: Find the real <body> tag and add topbar after it
    body_match = re.search(r'<body[^>]*>', content)
    if body_match:
        insert_pos = body_match.end()
        # Skip whitespace
        while insert_pos < len(content) and content[insert_pos] in '\n\r\t ':
            insert_pos += 1

        # Check if topbar already exists at correct position
        if 'kp-topbar' not in content[insert_pos:insert_pos+200]:
            root_path = get_root_path(filepath)
            topbar_html = '\n' + get_topbar_html(root_path)
            content = content[:insert_pos] + topbar_html + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {fname}")
    return True


if __name__ == '__main__':
    print("=== Fixing topbar position (move out of frame-busting) ===\n")

    # Find all broken files
    files = []
    for root, dirs, fnames in os.walk(BASE):
        # Skip admin, marketing, lab-manuals
        if '_admin' in root or '_marketing' in root or 'lab-manuals' in root:
            continue
        for fn in fnames:
            if fn.endswith('.html'):
                fpath = os.path.join(root, fn)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                tp = content.find('kp-topbar')
                cs = content.find('<meta charset')
                if tp != -1 and cs != -1 and tp < cs:
                    files.append(fpath)

    print(f"Found {len(files)} broken files\n")

    count = 0
    for fpath in sorted(files):
        if fix_file(fpath):
            count += 1

    print(f"\nFixed: {count}/{len(files)}")
