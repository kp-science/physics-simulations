#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เติม CSS กัน "แถบเลือกข้อความสีฟ้า" ตอนลากนิ้วบน iPad/มือถือ ให้ไฟล์ HTML ทุกไฟล์

ปัญหา: บน iPad ลากนิ้วในภาพ 3D / บนปุ่ม แล้ว Safari ตีความเป็นการลากเลือกข้อความ
       → ขึ้นแถบไฮไลต์สีฟ้าทับหน้าจอ

วิธีแก้: ใส่ <style id="kp-touch-css"> ก่อน </head> ปิดการเลือกข้อความเฉพาะส่วนที่ใช้ลาก
        (ภาพ · canvas · ปุ่ม · แผงควบคุม · แถบเมนู) — เนื้อหาที่ต้องคัดลอก เช่น ทฤษฎี
        วิธีทำ ตาราง ยังเลือกได้ตามปกติ และช่องกรอกตัวเลขยังพิมพ์/เลือกได้

ใช้งาน:
    python3 _admin/add_touch_css.py           # เติมให้ไฟล์ที่ยังไม่มี
    python3 _admin/add_touch_css.py --check   # ดูว่าไฟล์ไหนยังไม่มี (ไม่แก้ไฟล์)
    python3 _admin/add_touch_css.py --remove  # เอาออก
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '_preview', '.claude', 'assets'}
MARK = 'kp-touch-css'

BLOCK = """<!-- KP Touch: ลากนิ้วบน iPad/มือถือแล้วไม่ให้ขึ้นแถบเลือกข้อความสีฟ้า (ข้อความเนื้อหายังคัดลอกได้) -->
<style id="kp-touch-css">
html{-webkit-text-size-adjust:100%}
body{-webkit-tap-highlight-color:transparent}
canvas,svg,button,.btn,.btn-mini,.btn-sm,label,select,
.view3d,.view3d *,.sim-panel,.panel,.panel-section,.panel-title,.controls,.control,.ctrl,.sidebar,
.mode-btns,.viewbtns,.tabs,nav,nav *,.hud,.legend,.toolbar,.slider,.sl-row,.row-ctrl
{-webkit-user-select:none;-ms-user-select:none;user-select:none;-webkit-touch-callout:none}
input,textarea,[contenteditable]{-webkit-user-select:auto;-ms-user-select:auto;user-select:auto}
</style>
"""

REMOVE_RE = re.compile(
    r'\n?<!-- KP Touch:[^\n]*-->\n<style id="kp-touch-css">.*?</style>\n?',
    re.S)


def html_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in filenames:
            if fn.lower().endswith('.html'):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def main():
    check = '--check' in sys.argv
    remove = '--remove' in sys.argv
    files = html_files()
    done = skipped = nohead = 0
    for f in files:
        rel = os.path.relpath(f, ROOT)
        s = io.open(f, encoding='utf-8').read()
        if remove:
            if MARK not in s:
                continue
            new = REMOVE_RE.sub('\n', s)
            if new != s:
                io.open(f, 'w', encoding='utf-8').write(new)
                done += 1
                print('  − %s' % rel)
            continue
        if MARK in s:
            skipped += 1
            continue
        if check:
            print('  → %s' % rel)
            done += 1
            continue
        i = s.find('</head>')
        if i == -1:
            nohead += 1
            print('  ⚠️  ไม่มี </head> ข้ามไฟล์: %s' % rel)
            continue
        io.open(f, 'w', encoding='utf-8').write(s[:i] + BLOCK + s[i:])
        done += 1
    verb = 'ยังไม่มี' if check else ('เอาออก' if remove else 'เติมให้')
    print('\n%s %d ไฟล์ · มีอยู่แล้ว %d · ไฟล์ HTML ทั้งหมด %d%s'
          % (verb, done, skipped, len(files), (' · ไม่มี </head> %d' % nohead) if nohead else ''))


if __name__ == '__main__':
    main()
