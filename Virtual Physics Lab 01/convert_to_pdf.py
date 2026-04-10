#!/usr/bin/env python3
"""
แปลงไฟล์ DOCX คู่มือ Lab เป็น PDF
รันบน Mac โดยใช้ Microsoft Word (รองรับภาษาไทยสมบูรณ์)

วิธีใช้:
  1. เปิด Terminal
  2. cd "/Users/komanepapato/Documents/GitHub/physics-simulations/Virtual Physics Lab 01"
  3. pip3 install docx2pdf
  4. python3 convert_to_pdf.py
"""

import os
import subprocess
import sys

DOCX_DIR = os.path.join(os.path.dirname(__file__), "lab-manuals-docx")
PDF_DIR  = os.path.join(os.path.dirname(__file__), "lab-manuals-pdf")

# ไฟล์คู่มือ Lab 1–15 ที่ต้องแปลง
TARGET_LABS = [
    "คู่มือการทดลอง_1_measuring_precision.docx",
    "คู่มือการทดลอง_2_vector_forces.docx",
    "คู่มือการทดลอง_3_torques.docx",
    "คู่มือการทดลอง_4_force_resolution.docx",
    "คู่มือการทดลอง_5_incline_forces.docx",
    "คู่มือการทดลอง_6.1_timing_devices.docx",
    "คู่มือการทดลอง_6.2_water_clock.docx",
    "คู่มือการทดลอง_6.3_tape_timer.docx",
    "คู่มือการทดลอง_7_strobe_photography.docx",
    "คู่มือการทดลอง_8_straight_line_motion.docx",
    "คู่มือการทดลอง_9_galileo_water_clock.docx",
    "คู่มือการทดลอง_10_spinning_disc.docx",
    "คู่มือการทดลอง_11_air_track.docx",
    "คู่มือการทดลอง_12_turntable_gravity.docx",
    "คู่มือการทดลอง_13_free_fall.docx",
    "คู่มือการทดลอง_14_mass_weight.docx",
    "คู่มือการทดลอง_15_newtons_2nd_law.docx",
]

def check_docx2pdf():
    try:
        import docx2pdf
        return True
    except ImportError:
        return False

def install_docx2pdf():
    print("📦 กำลังติดตั้ง docx2pdf...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "docx2pdf"])
    print("✅ ติดตั้งสำเร็จ\n")

def convert_all():
    from docx2pdf import convert

    os.makedirs(PDF_DIR, exist_ok=True)

    success = 0
    failed  = []

    for filename in TARGET_LABS:
        docx_path = os.path.join(DOCX_DIR, filename)
        pdf_name  = filename.replace(".docx", ".pdf")
        pdf_path  = os.path.join(PDF_DIR, pdf_name)

        if not os.path.exists(docx_path):
            print(f"⚠️  ไม่พบไฟล์: {filename}")
            failed.append(filename)
            continue

        print(f"🔄 กำลังแปลง: {filename}")
        try:
            convert(docx_path, pdf_path)
            size_kb = os.path.getsize(pdf_path) / 1024
            print(f"   ✅ บันทึกแล้ว → {pdf_name} ({size_kb:.0f} KB)")
            success += 1
        except Exception as e:
            print(f"   ❌ ผิดพลาด: {e}")
            failed.append(filename)

    print(f"\n{'='*50}")
    print(f"✅ แปลงสำเร็จ: {success} ไฟล์")
    if failed:
        print(f"❌ ผิดพลาด:   {len(failed)} ไฟล์")
        for f in failed:
            print(f"   - {f}")
    print(f"📁 PDF อยู่ที่: {PDF_DIR}")

if __name__ == "__main__":
    print("=" * 50)
    print("🔄 KP Science — แปลงคู่มือ Lab เป็น PDF")
    print("=" * 50 + "\n")

    if not check_docx2pdf():
        install_docx2pdf()

    convert_all()
