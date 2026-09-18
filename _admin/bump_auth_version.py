# -*- coding: utf-8 -*-
"""เปลี่ยนเลขเวอร์ชันท้าย URL ของสคริปต์ที่แชร์กันทั้งเว็บ (cache busting)

ทำไมต้องมี: เบราว์เซอร์เก็บสำเนาไฟล์ .js ไว้ในเครื่อง พอเราแก้ไฟล์แล้วอัปขึ้นเว็บ
เครื่องที่เคยเข้ามาแล้วอาจยังใช้สำเนาเก่าอยู่ (GitHub Pages ~10 นาที)
การเติม ?v=<เลข> ทำให้เบราว์เซอร์มองว่าเป็น URL ใหม่ จึงโหลดไฟล์ใหม่ทันที
— ไฟล์บนเซิร์ฟเวอร์ยังมีตัวเดียวเหมือนเดิม ?v= เป็นแค่ป้ายห้อยท้าย URL

วิธีใช้:
    python3 _admin/bump_auth_version.py            # ใช้วันที่วันนี้ (ถ้าซ้ำของเดิมจะต่อ -2, -3 ให้)
    python3 _admin/bump_auth_version.py 20260920   # กำหนดเลขเอง
    python3 _admin/bump_auth_version.py --check    # ดูเฉย ๆ ว่าตอนนี้เป็นเลขอะไร / ไฟล์ไหนยังไม่มี

เพิ่มไฟล์ที่ต้องติดเวอร์ชันได้ที่ TARGETS
"""
import io, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER_FILE = os.path.join(ROOT, '_admin', 'asset_version.txt')
TARGETS = ['kp-auth.js']
SKIP_DIRS = {'.git', 'node_modules', '_preview', '.claude'}


def current_version():
    try:
        v = io.open(VER_FILE, encoding='utf-8').read().strip()
        return v or '1'
    except IOError:
        return '1'


def next_version(cur):
    today = datetime.date.today().strftime('%Y%m%d')
    if not cur.startswith(today):
        return today
    m = re.match(r'^(\d{8})(?:-(\d+))?$', cur)
    n = int(m.group(2) or 1) + 1 if m else 2
    return today + '-' + str(n)


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower().endswith('.html'):
                yield os.path.join(dirpath, fn)


def apply_version(content, version):
    """เติม/แก้ ?v= ให้ทุก target — คืน (เนื้อหาใหม่, จำนวนแท็กที่แตะ)"""
    n = 0
    for name in TARGETS:
        pat = re.compile(r'(src=")([^"]*?)' + re.escape(name) + r'(?:\?v=[^"]*)?(")')
        content, k = pat.subn(lambda m: m.group(1) + m.group(2) + name + '?v=' + version + m.group(3), content)
        n += k
    return content, n


def main():
    args = [a for a in sys.argv[1:]]
    cur = current_version()

    if '--check' in args:
        print('เวอร์ชันปัจจุบัน: ' + cur)
        missing = []
        for f in html_files():
            c = io.open(f, encoding='utf-8').read()
            for name in TARGETS:
                if re.search(r'src="[^"]*' + re.escape(name) + r'"', c):
                    missing.append(os.path.relpath(f, ROOT)); break
        if missing:
            print('ยังไม่มี ?v= (%d ไฟล์):' % len(missing))
            for f in missing[:20]:
                print('   - ' + f)
            if len(missing) > 20:
                print('   ... และอีก %d ไฟล์' % (len(missing) - 20))
        else:
            print('ทุกไฟล์มี ?v= ครบแล้ว ✅')
        return 0

    version = args[0] if args and not args[0].startswith('-') else next_version(cur)
    changed_files = 0
    total_tags = 0
    for f in html_files():
        c = io.open(f, encoding='utf-8').read()
        new, n = apply_version(c, version)
        total_tags += n
        if new != c:
            io.open(f, 'w', encoding='utf-8').write(new)
            changed_files += 1
    io.open(VER_FILE, 'w', encoding='utf-8').write(version + '\n')
    print('เวอร์ชันใหม่: %s (เดิม %s)' % (version, cur))
    print('แก้ไฟล์ HTML %d ไฟล์ · แท็กทั้งหมด %d จุด · เป้าหมาย: %s' % (changed_files, total_tags, ', '.join(TARGETS)))
    print('อย่าลืม commit + push เพื่อให้เบราว์เซอร์ทุกเครื่องได้ไฟล์ใหม่ทันที')
    return 0


if __name__ == '__main__':
    sys.exit(main())
