# -*- coding: utf-8 -*-
"""สร้าง index.html (หน้าแรก) จาก _admin/home_template.html + _admin/labs_data.py + ไฟล์ใน Demo/
   · แลป/Demo แนะนำ: แก้ที่ FEAT / DEMOS ด้านล่าง (ภาพหน้าจออยู่ assets/thumbs/<ชื่อ>.jpg)
   · ถูกเรียกจาก build_virtual_lab.py อัตโนมัติ หรือรันเอง: python3 _admin/build_home.py"""
import os, sys, glob, html, urllib.parse
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, '_admin')); os.chdir(BASE)
import labs_data as L
from collections import Counter
esc = lambda t: html.escape(str(t), quote=True)
ROOT = ''   # index.html อยู่ที่ราก
url = lambda p: ROOT + '/'.join(urllib.parse.quote(x) for x in p.split('/'))
lab = {l[2]: l for l in L.LABS}
grp = {g[0]: g for g in L.GROUPS}
cnt = {g[0]: sum(1 for l in L.LABS if l[5] in g[3]) for g in L.GROUPS}
lvl = Counter(l[6] for l in L.LABS)
demos_all = [f for f in glob.glob('Demo/**/*.html', recursive=True) if not f.endswith('index.html')]
dcount = Counter(f.split('/')[1] for f in demos_all)
N_LAB, N_DEMO = len(L.LABS), len(demos_all)

def clean(t):
    t = t.replace('(3D)', '').strip()
    return t
ICON = {  # ไอคอนเส้น 48×48
 'mech': '<path d="M14 8h20M24 8v22"/><circle cx="24" cy="34" r="6"/><path d="M8 42h32" stroke-dasharray="2 4"/>',
 'wave': '<path d="M4 24c5-10 9-10 14 0s9 10 14 0 9-10 14 0"/><path d="M4 34c5-6 9-6 14 0s9 6 14 0 9-6 14 0" opacity=".45"/>',
 'elec': '<circle cx="15" cy="24" r="6"/><circle cx="33" cy="24" r="6"/><path d="M12 24h6M15 21v6M30 24h6"/><path d="M21 24h6" stroke-dasharray="2 3"/>',
 'astro': '<circle cx="24" cy="24" r="7"/><ellipse cx="24" cy="24" rx="19" ry="7" transform="rotate(-20 24 24)"/><circle cx="41" cy="17" r="2.5"/>',
 'demo': '<rect x="6" y="9" width="36" height="24" rx="3"/><path d="M20 16l9 5-9 5z"/><path d="M17 40h14M24 33v7"/>',
}
subjects = [
 ('mech', 'กลศาสตร์', 'การวัด · การเคลื่อนที่ · แรง · วงกลม · SHM', f'{cnt["mech"]} แลป', 'virtual-lab.html#g-mech'),
 ('wave', 'คลื่น · เสียง · แสง', 'คลื่นกล · การหักเห · ทัศนอุปกรณ์ · การแทรกสอด', f'{cnt["wave"]} แลป', 'virtual-lab.html#g-wave'),
 ('elec', 'ไฟฟ้าสถิต', 'ประจุ · สนาม · ศักย์ · ตัวเก็บประจุ', f'{cnt["elec"]} แลป', 'virtual-lab.html#g-elec'),
 ('astro', 'ดาราศาสตร์', 'เอกภพ · ดาวฤกษ์ · ดวงอาทิตย์', f'{cnt["astro"]} แลป · {dcount.get("ดาราศาสตร์",0)} Demo', 'virtual-lab.html#g-astro'),
 ('demo', 'Demo ช่วยสอน', 'ฉายประกอบการอธิบายในห้องเรียน', f'{N_DEMO} เรื่อง', 'Demo/index.html'),
]
subj_html = ''.join(f'''<a class="subj s-{k}" href="{ROOT}{href}">
  <svg viewBox="0 0 48 48" aria-hidden="true">{ICON[k]}</svg>
  <div class="subj-t"><h3>{esc(n)}</h3><p>{esc(d)}</p></div>
  <span class="subj-n">{esc(c)}</span></a>''' for k, n, d, c, href in subjects)

grades = [
 ('ม.4', 'm4', 'การวัด · การเคลื่อนที่แนวตรง · แรงและกฎนิวตัน · โพรเจกไทล์ · การเคลื่อนที่แบบวงกลม', f'{lvl["ม.4"]} แลป', f'virtual-lab.html?level=m4'),
 ('ม.5', 'm5', 'SHM · คลื่นกล · เสียง · แสงและทัศนอุปกรณ์ · ไฟฟ้าสถิต', f'{lvl["ม.5"]} แลป', f'virtual-lab.html?level=m5'),
 ('ม.6', 'm6', 'ไฟฟ้า (มิลลิแกน) · ดาราศาสตร์และจักรวาลวิทยา', f'{lvl["ม.6"]} แลป · {dcount.get("ดาราศาสตร์",0)} Demo', f'virtual-lab.html?level=m6'),
 ('มหาวิทยาลัย', 'uni', 'ปฏิบัติการฟิสิกส์ 1 · การวัดอย่างละเอียดด้วยเวอร์เนียร์และไมโครมิเตอร์ 3D', '1 แลป', 'Virtual Physics Lab 03/1. precision-measurement-3d.html'),
]
grade_html = ''.join(f'''<a class="grade" href="{url(href) if href.startswith('Virtual') else ROOT+href}">
  <span class="g-lv">{esc(g)}</span><p>{esc(d)}</p><span class="g-n">{esc(c)} <i>→</i></span></a>''' for g, k, d, c, href in grades)

FEAT = [('69', 'lab-69'), ('55', 'lab-55'), ('52', 'lab-52'), ('65', 'lab-65'), ('60', 'lab-60'), ('46', 'lab-46'), ('37', 'lab-37'), ('13', 'lab-13')]
TOPIC_G = {t: g[0] for g in L.GROUPS for t in g[3]}
def feat_card(n, img):
    l = lab[n]; is3d = '3D' in l[3]; new = l[7] == 'vpl02' and n.isdigit() and 54 <= int(n) <= 69
    tg = TOPIC_G[l[5]]
    return (f'<a class="tcard" href="{url(l[1])}"><div class="thumb s-{tg}"><img src="{ROOT}assets/thumbs/{img}.jpg" alt="" loading="lazy" onerror="this.remove()">'
            + ('<span class="rib">ใหม่</span>' if new else '') + '</div>'
            f'<div class="tc-body"><div class="tc-meta"><span>Lab {esc(n)}</span><span>{esc(l[6])}{" · 3D" if is3d else ""}</span></div>'
            f'<h3>{esc(clean(l[3]))}</h3><p>{esc(l[4])}</p></div></a>')
feat_html = ''.join(feat_card(n, i) for n, i in FEAT)

DEMOS = [('Demo/แม่เหล็ก/magnetic_field_sim_3.html', 'demo-magnet', 'สนามแม่เหล็กของแท่งแม่เหล็ก 2 แท่ง', 'แม่เหล็ก'),
         ('Demo/คลื่น/waves_simulation.html', 'demo-waves', 'คลื่นกล: สันคลื่น ท้องคลื่น และความยาวคลื่น', 'คลื่น'),
         ('Demo/ดาราศาสตร์/galaxy_rotation.html', 'demo-galaxy', 'กราฟการหมุนของกาแล็กซีกับสสารมืด', 'ดาราศาสตร์'),
         ('Demo/mechanics/โปรเจคไทล์/monkey_gun-3.html', 'demo-monkey', 'ยิงลิงที่ปล่อยตัวจากกิ่งไม้', 'กลศาสตร์'),
         ('Demo/ดาราศาสตร์/cosmic_timeline.html', 'demo-timeline', '6 ยุคของเอกภพ', 'ดาราศาสตร์'),
         ('Demo/ดาราศาสตร์/stellar_parallax.html', 'demo-parallax', 'พารัลแลกซ์ของดาว d = 1/p', 'ดาราศาสตร์')]
DG = {'แม่เหล็ก': 'elec', 'คลื่น': 'wave', 'ดาราศาสตร์': 'astro', 'กลศาสตร์': 'mech'}
demo_html = ''.join(f'<a class="tcard" href="{url(h)}"><div class="thumb s-{DG[s]}"><img src="{ROOT}assets/thumbs/{i}.jpg" alt="" loading="lazy" onerror="this.remove()"></div>'
                    f'<div class="tc-body"><div class="tc-meta"><span>{esc(s)}</span><span>Demo</span></div><h3>{esc(t)}</h3></div></a>' for h, i, t, s in DEMOS)

hero_imgs = ''.join(f'<figure class="shot shot-{k}"><img src="{ROOT}assets/thumbs/{i}.jpg" alt="" onerror="this.remove()"><figcaption>Lab {n} · {esc(clean(lab[n][3]).split(":")[0])}</figcaption></figure>'
                    for k, (n, i) in enumerate([('69', 'lab-69'), ('52', 'lab-52'), ('55', 'lab-55')]))

tpl = open(os.path.join(BASE, '_admin', 'home_template.html'), encoding='utf-8').read()
for k, v in {'SUBJECTS': subj_html, 'GRADES': grade_html, 'FEATURED': feat_html, 'DEMOS': demo_html, 'HERO': hero_imgs,
             'N_LAB': N_LAB, 'N_DEMO': N_DEMO, 'ROOT': ROOT}.items():
    tpl = tpl.replace('{{' + k + '}}', str(v))
open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8').write(tpl)
print('built index.html · %d แลป · %d Demo' % (N_LAB, N_DEMO))
missing = [i for _, i in FEAT] + [d[1] for d in DEMOS]
missing = [i for i in missing if not os.path.exists(os.path.join(BASE, 'assets', 'thumbs', i + '.jpg'))]
if missing: print('⚠️ ไม่พบภาพหน้าจอ:', missing)
