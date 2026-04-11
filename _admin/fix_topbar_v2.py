#!/usr/bin/env python3
"""
Fix topbar position v2 — completely rebuild frame-busting and re-insert topbar.
Strategy:
1. Remove ALL topbar HTML from file (wherever it is)
2. Replace everything between GA script and <meta charset with clean frame-busting
3. Find real <body> tag and insert topbar after it
"""
import os, re, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEAN_FB = '<script>\n/* KP Science \u2014 Frame Protection */\n(function(){\n  try{\n    if(window.self !== window.top){\n      window.top.location.href = window.self.location.href;\n    }\n  }catch(e){\n    document.documentElement.innerHTML =\n      \'<body style="background:#0a0e1a;color:#e2e8f0;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center;padding:20px">\' +\n      \'<div><h1 style="color:#38bdf8">KP Science</h1>\' +\n      \'<p style="margin:1rem 0">This simulation cannot be embedded on other websites.</p>\' +\n      \'<p><a href="../../index.html" style="color:#38bdf8">Go to KP Science</a></p></div></body>\';\n  }\n})();\n</script>'


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

    # Step 1: Remove ALL topbar HTML blocks (wherever they are)
    content = re.sub(
        r'<!-- KP Topbar -->\s*<nav class="kp-topbar">.*?</nav>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # Step 2: Fix frame-busting — replace everything between GA </script> and <meta charset
    ga_marker = "gtag('config', 'G-2YTJBNHP6D');"
    ga_pos = content.find(ga_marker)
    if ga_pos == -1:
        print(f"  SKIP {fname}: no GA")
        return False

    ga_script_end = content.find('</script>', ga_pos)
    if ga_script_end == -1:
        print(f"  SKIP {fname}: no GA </script>")
        return False
    ga_script_end += len('</script>')

    charset_pos = content.find('<meta charset')
    if charset_pos == -1:
        print(f"  SKIP {fname}: no charset")
        return False

    # Only replace if there's frame-busting between GA and charset
    between = content[ga_script_end:charset_pos]
    if 'Frame Protection' in between or 'frame' in between.lower() or 'kp-topbar' in between or len(between.strip()) > 20:
        content = content[:ga_script_end] + '\n' + CLEAN_FB + '\n\n' + content[charset_pos:]

    # Step 3: Find real <body> tag and insert topbar
    body_match = re.search(r'<body[^>]*>', content)
    if body_match:
        insert_pos = body_match.end()
        root_path = get_root_path(filepath)
        topbar = '\n' + get_topbar_html(root_path)
        content = content[:insert_pos] + topbar + content[insert_pos:]
    else:
        print(f"  WARN {fname}: no <body>")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {fname}")
    return True


if __name__ == '__main__':
    print("=== Fix topbar position v2 ===\n")

    # Find ALL files with topbar before <meta charset
    files = []
    for root, dirs, fnames in os.walk(BASE):
        if '_admin' in root or '_marketing' in root or 'lab-manuals' in root:
            continue
        for fn in fnames:
            if not fn.endswith('.html'):
                continue
            fpath = os.path.join(root, fn)
            with open(fpath, 'r', encoding='utf-8') as f:
                c = f.read()
            tp = c.find('kp-topbar')
            cs = c.find('<meta charset')
            if tp != -1 and cs != -1 and tp < cs:
                files.append(fpath)

    print(f"Found {len(files)} broken files\n")
    count = 0
    for fpath in sorted(files):
        if fix_file(fpath):
            count += 1

    print(f"\nFixed: {count}/{len(files)}")

    # Verify
    print("\n=== Verify ===")
    still_broken = 0
    for fpath in sorted(files):
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()
        tp = c.find('kp-topbar')
        cs = c.find('<meta charset')
        if tp != -1 and cs != -1 and tp < cs:
            print(f"  STILL BROKEN: {os.path.basename(fpath)}")
            still_broken += 1
    if still_broken == 0:
        print("  All files OK!")
