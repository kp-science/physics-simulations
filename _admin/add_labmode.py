#!/usr/bin/env python3
"""ใส่ _shared/kp-labmode.js (🎓 โหมดสอน + 🔒 ล็อกโหมดอัตโนมัติสำหรับสมาชิก) ให้แลปที่มีปุ่มโหมดอัตโนมัติ

ใช้:
  python3 _admin/add_labmode.py            # ทุกแลปที่มี setMode('auto') ฯลฯ (ยกเว้น poe/ และ Demo/)
  python3 _admin/add_labmode.py --check    # ดูว่าไฟล์ไหนยังไม่มี

แทรกก่อน </body> ตัวสุดท้าย · ขั้นตอนโหมดสอนของแต่ละแลป = <script>window.KP_TUTOR = {...}</script>
ใส่ในไฟล์แลปเองก่อนบรรทัดนี้
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '.claude', 'node_modules', 'poe', '_admin', 'Demo'}
AUTO_RE = re.compile(r'onclick="[^"]*\b\w*Mode\w*\(\s*\'auto\'|data-(?:mode|rec)="auto"|id="mAuto"|id="rec-toggle"')


def root_rel(path):
    depth = os.path.relpath(path, ROOT).count(os.sep)
    return '../' * depth


def targets():
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in fs:
            if f.endswith('.html') and f != 'index.html':
                p = os.path.join(d, f)
                if AUTO_RE.search(open(p, encoding='utf-8').read()):
                    yield p


def main():
    check = '--check' in sys.argv
    n = 0
    paths = sorted(targets())
    for p in paths:
        s = open(p, encoding='utf-8').read()
        if 'kp-labmode.js' in s:
            continue
        n += 1
        rel = os.path.relpath(p, ROOT)
        if check:
            print('  ยังไม่มี:', rel)
            continue
        tag = f'\n<!-- KP Lab Mode (🎓 โหมดสอน · 🔒 โหมดอัตโนมัติสำหรับสมาชิก) -->\n<script src="{root_rel(p)}_shared/kp-labmode.js"></script>\n'
        i = s.rfind('</body>')
        if i < 0:
            print('  ⚠️ ไม่พบ </body>:', rel)
            continue
        open(p, 'w', encoding='utf-8').write(s[:i] + tag + s[i:])
        print('  ✓', rel)
    print(('ยังไม่มี' if check else 'ใส่แล้ว'), n, 'ไฟล์', f'(แลปที่มีโหมดอัตโนมัติ {len(paths)} ไฟล์)')


if __name__ == '__main__':
    main()
