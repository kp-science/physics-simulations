#!/usr/bin/env python3
"""ใส่ _shared/kp-real3d.js (ภาพ 3D สมจริง: แสงสะท้อน · เงา · โต๊ะไม้) ให้ไฟล์แลป 3D

ใช้:
  python3 _admin/add_real3d.py            # ทุกไฟล์ที่ใช้ three.js (ยกเว้น poe/)
  python3 _admin/add_real3d.py ไฟล์.html   # เฉพาะไฟล์ที่ระบุ
  python3 _admin/add_real3d.py --check    # ดูว่าไฟล์ไหนยังไม่มี
  python3 _admin/add_real3d.py --remove   # เอาออกทั้งหมด

แทรกต่อจากบรรทัด fallback ของ three.js ทันที (ต้องโหลดก่อนแลปสร้าง renderer)
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', 'poe', '_admin'}
FALLBACK = re.compile(r'<script>if\(typeof THREE==="undefined"\)\{ document\.write\(\'<script src="((?:\.\./)*)_shared/three\.min\.js"><\\/script>\'\); \}</script>')
TAG = '<script src="{p}_shared/kp-real3d.js"></script>'


def files_3d():
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in fs:
            if f.endswith('.html'):
                p = os.path.join(d, f)
                with open(p, encoding='utf-8') as fh:
                    if 'THREE.WebGLRenderer' in fh.read():
                        yield p


def process(path, mode):
    s = open(path, encoding='utf-8').read()
    has = 'kp-real3d.js' in s
    rel = os.path.relpath(path, ROOT)
    if mode == 'check':
        if not has:
            print('  ยังไม่มี:', rel)
        return not has
    if mode == 'remove':
        if not has:
            return False
        s2 = re.sub(r'\n?<script src="(?:\.\./)*_shared/kp-real3d\.js"></script>', '', s)
    else:
        if has:
            return False
        m = FALLBACK.search(s)
        if not m:
            print('  ⚠️ ไม่พบบรรทัดโหลด three.js:', rel)
            return False
        s2 = s[:m.end()] + '\n' + TAG.format(p=m.group(1)) + s[m.end():]
    open(path, 'w', encoding='utf-8').write(s2)
    print('  ✓', rel)
    return True


def main():
    args = sys.argv[1:]
    mode = 'check' if '--check' in args else 'remove' if '--remove' in args else 'add'
    paths = [os.path.abspath(a) for a in args if not a.startswith('--')] or list(files_3d())
    n = sum(process(p, mode) for p in sorted(paths))
    print({'check': f'ยังไม่มี {n} ไฟล์', 'remove': f'เอาออก {n} ไฟล์', 'add': f'ใส่แล้ว {n} ไฟล์'}[mode], f'(ตรวจ {len(paths)} ไฟล์)')


if __name__ == '__main__':
    main()
