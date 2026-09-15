# -*- coding: utf-8 -*-
"""เปลี่ยนฟอนต์ทั้งเว็บจาก Sarabun → ชุด B (IBM Plex Sans Thai)
   · ข้อความบนหน้า (CSS)  : IBM Plex Sans Thai Looped, IBM Plex Sans Thai
   · ข้อความในแคนวาส (JS) : IBM Plex Sans Thai  (กว้างใกล้ Sarabun ±2% ป้ายในแคนวาสจึงไม่ล้น)
   ใช้: python3 _admin/switch_font_plex.py [--dry]"""
import os, re, sys, glob
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
DRY = '--dry' in sys.argv
CSS_FAM = 'IBM Plex Sans Thai Looped,IBM Plex Sans Thai'
JS_FAM = 'IBM Plex Sans Thai'
LINK = 'family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=IBM+Plex+Sans+Thai+Looped:wght@300;400;500;600;700'

def fix_css(t):
    return re.sub(r"""(['"]?)Sarabun\1""", CSS_FAM, t)

def fix_js(t):
    t = re.sub(r"""(['"])Sarabun\1""", lambda m: m.group(1) + JS_FAM + m.group(1), t)
    return re.sub(r'\bSarabun\b', JS_FAM, t)

def convert_html(s):
    s = re.sub(r'family=Sarabun(?::[^&"\']*)?', LINK, s)
    s = re.sub(r'font-family="([^"]*)"', lambda m: 'font-family="' + re.sub(r"'?Sarabun'?", JS_FAM, m.group(1)) + '"', s)   # SVG: แบบแผนภาพ ใช้ตัวไม่มีหัว
    out, i = [], 0
    for m in re.finditer(r'(<style[^>]*>)(.*?)(</style>)|(<script(?![^>]*\bsrc=)[^>]*>)(.*?)(</script>)', s, re.S):
        out.append(re.sub(r'style="([^"]*)"', lambda a: 'style="' + fix_css(a.group(1)) + '"', s[i:m.start()]))
        if m.group(1): out.append(m.group(1) + fix_css(m.group(2)) + m.group(3))
        else: out.append(m.group(4) + fix_js(m.group(5)) + m.group(6))
        i = m.end()
    out.append(re.sub(r'style="([^"]*)"', lambda a: 'style="' + fix_css(a.group(1)) + '"', s[i:]))
    return ''.join(out)

SKIP = ('_preview/', '_marketing/', '.claude/', 'node_modules/')
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(SKIP) and '__pristine' not in f]
changed = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    if 'Sarabun' not in s: continue
    t = convert_html(s)
    if t != s:
        changed += 1
        if not DRY: open(f, 'w', encoding='utf-8').write(t)
# ไฟล์ JS/สคริปต์สร้างหน้า
extra = {
  '_shared/kp-mobile-panel.js': lambda s: s.replace('Sarabun', CSS_FAM),            # CSS ในสตริง JS
  '_shared/watermark.js': fix_js,                                                    # วาดบนแคนวาส
  '_admin/protect_new_file.py': fix_css,                                             # TOPBAR_CSS
  '_admin/build_virtual_lab.py': lambda s: fix_css(re.sub(r'family=Sarabun(?::[^&"\']*)?', LINK, s)),
}
for f, fn in extra.items():
    s = open(f, encoding='utf-8').read(); t = fn(s)
    if t != s:
        changed += 1
        if not DRY: open(f, 'w', encoding='utf-8').write(t)
left = [f for f in files if 'Sarabun' in open(f, encoding='utf-8').read()]
print(('DRY ' if DRY else '') + 'changed %d files · still mention Sarabun: %d' % (changed, len(left)), left[:5])
