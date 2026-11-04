# -*- coding: utf-8 -*-
"""ขั้นตอนครบกระบวนการของแต่ละแลป สำหรับ "วิธีการทดลองแบบมีภาพ" (ถ่ายภาพด้วย _admin/capture_lab_guide.py)
   หลักและขั้นตอนทำงาน: skill kp-lab-procedure (.claude/skills/kp-lab-procedure/SKILL.md)

   1 แลป = 1 ไฟล์ _admin/lab_guides/<ชุด>-lab-<เลข>.py ที่ประกาศ GUIDE = {
     'title': 'ชื่อกระบวนการ',
     'setup': 'JS ที่รันครั้งเดียวหลังโหลดแลป (ฟังก์ชันช่วย เช่น สร้างข้อมูลจากแบบจำลองฟิสิกส์ของแลป)',
     'steps': [ {
        'el':    'css selector' หรือ ['sel1', 'sel2']   (กรอบสีเหลืองในภาพ)
        'prep':  'JS ก่อนถ่ายภาพขั้นนี้ — ทำให้แลปอยู่ในสภาพของขั้นนั้น',
        'title': 'ทำอะไร (สั้น)',
        'text':  'อธิบายวิธีทำ / เหตุผล (HTML ได้)',
        'out':   'ค่าที่ได้จากขั้นนี้ (HTML ได้ · ไม่ใส่ก็ได้)',
     }, ... ] }
   ต้นแบบ: _admin/lab_guides/vpl02-lab-60.py"""
import os, importlib.util
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lab_guides')
GUIDES = {}
for f in sorted(os.listdir(DIR)):
    if f.endswith('.py') and not f.startswith('_'):
        spec = importlib.util.spec_from_file_location('g_' + f[:-3].replace('-', '_').replace('.', '_'), os.path.join(DIR, f))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        GUIDES[f[:-3]] = m.GUIDE
