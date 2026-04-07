#!/usr/bin/env python3
"""
KP Science Simulation — Domain Protection Script
=================================================
ใช้ script นี้เพื่อเพิ่ม domain check + copyright notice
ให้กับไฟล์ HTML ทุกไฟล์ใน physics-simulations/

วิธีใช้:
  python3 add_protection.py

หมายเหตุ: script นี้ idempotent (รันซ้ำได้ ไม่เพิ่ม protection ซ้ำ)
"""

import os
import re

# ─── CONFIG ───────────────────────────────────────────────
ROOT_DIR    = os.path.dirname(os.path.abspath(__file__))
OWNER       = "โกเมน ปาปะโถ"
SITE        = "komane67.github.io"
YEAR        = "2025"
MARKER      = "KP-DOMAIN-PROTECTION"   # ใช้ตรวจว่าเพิ่มแล้วหรือยัง

# ไฟล์ที่ข้ามไม่ต้องใส่ protection (admin tool, หน้าหลัก)
SKIP_FILES  = {"admin_passwords.html"}

# ─── PROTECTION CODE (injected right before </head>) ──────
PROTECTION_BLOCK = f"""
  <!-- {MARKER} — DO NOT REMOVE -->
  <!-- © {YEAR} {OWNER} · KP Science Simulation · {SITE}/physics-simulations/ -->
  <!-- ห้ามคัดลอก ดัดแปลง หรือเผยแพร่โดยไม่ได้รับอนุญาต -->
  <script>
  (function(){{
    var allowed = ['{SITE}', 'localhost', '127.0.0.1'];
    var host = location.hostname;
    if (!allowed.some(function(d){{ return host === d || host.endsWith('.' + d); }})) {{
      document.documentElement.innerHTML =
        '<body style="background:#06090f;color:#f87171;font-family:sans-serif;' +
        'display:flex;align-items:center;justify-content:center;height:100vh;' +
        'text-align:center;padding:2rem">' +
        '<div><div style="font-size:3rem">⛔</div>' +
        '<h2 style="margin:.5rem 0">ไฟล์นี้ถูกคัดลอกโดยไม่ได้รับอนุญาต</h2>' +
        '<p style="color:#94a3b8">© {YEAR} {OWNER} · KP Science Simulation</p>' +
        '<p style="color:#94a3b8">กรุณาเข้าใช้งานที่ <a href="https://{SITE}/physics-simulations/" ' +
        'style="color:#38bdf8">{SITE}/physics-simulations/</a></p></div></body>';
    }}
  }})();
  </script>"""

# ─── MAIN ──────────────────────────────────────────────────
added   = []
skipped = []
already = []

for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    # ข้ามโฟลเดอร์ .git
    dirnames[:] = [d for d in dirnames if d != '.git']

    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        if fname in SKIP_FILES:
            skipped.append(fname)
            continue

        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # ข้ามถ้ามี marker แล้ว (idempotent)
        if MARKER in content:
            already.append(os.path.relpath(fpath, ROOT_DIR))
            continue

        # แทรกก่อน </head> (หรือก่อน <body> ถ้าไม่มี </head>)
        if '</head>' in content:
            new_content = content.replace('</head>', PROTECTION_BLOCK + '\n</head>', 1)
        elif '<body' in content:
            new_content = content.replace('<body', PROTECTION_BLOCK + '\n<body', 1)
        else:
            # ไม่มี structure ปกติ — เพิ่มตอนต้นไฟล์
            new_content = PROTECTION_BLOCK + '\n' + content

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        added.append(os.path.relpath(fpath, ROOT_DIR))

# ─── REPORT ────────────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  KP Science — Domain Protection Report")
print(f"{'='*55}")
print(f"\n✅ เพิ่ม protection แล้ว ({len(added)} ไฟล์):")
for f in sorted(added):
    print(f"   + {f}")

if already:
    print(f"\n⏭  มี protection อยู่แล้ว ({len(already)} ไฟล์):")
    for f in sorted(already):
        print(f"   = {f}")

if skipped:
    print(f"\n⏩ ข้าม ({len(skipped)} ไฟล์):")
    for f in sorted(skipped):
        print(f"   - {f}")

print(f"\n{'='*55}")
print(f"  รวม: {len(added)} เพิ่ม · {len(already)} มีแล้ว · {len(skipped)} ข้าม")
print(f"{'='*55}\n")
