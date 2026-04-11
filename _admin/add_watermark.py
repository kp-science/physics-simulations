#!/usr/bin/env python3
"""Add diagonal watermark "KP Science" to PDF lab manuals."""
import sys, os
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
from io import BytesIO

def create_watermark_page(width, height, text="KP Science"):
    """Create a single-page PDF with diagonal watermark text."""
    buf = BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(width, height))

    c.saveState()
    # Move to center, rotate 45 degrees
    c.translate(width / 2, height / 2)
    c.rotate(45)

    # Light gray, very transparent
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.06))
    c.setFont("Helvetica-Bold", 72)
    c.drawCentredString(0, 0, text)

    # Smaller URL below
    c.setFont("Helvetica", 20)
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.05))
    c.drawCentredString(0, -40, "kp-science.github.io")

    c.restoreState()

    # Header: website link at top-right
    c.saveState()
    c.setFillColor(Color(0.45, 0.45, 0.45, alpha=0.35))
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 20, height - 18, "KP Science  |  kp-science.github.io/physics-simulations")
    c.restoreState()

    c.save()
    buf.seek(0)
    return buf


def add_watermark(input_path, output_path=None, text="KP Science"):
    """Add watermark to every page of a PDF."""
    if output_path is None:
        output_path = input_path  # overwrite

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Get page dimensions
        box = page.mediabox
        w = float(box.width)
        h = float(box.height)

        # Create watermark matching page size
        wm_buf = create_watermark_page(w, h, text)
        wm_reader = PdfReader(wm_buf)
        wm_page = wm_reader.pages[0]

        # Merge watermark under the page content
        page.merge_page(wm_page)
        writer.add_page(page)

    # Write to temp file first, then rename (safe overwrite)
    temp_path = output_path + '.tmp'
    with open(temp_path, 'wb') as f:
        writer.write(f)
    os.replace(temp_path, output_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 add_watermark.py <pdf_file_or_dir> [--all]")
        print("  --all  Process all PDFs in the directory")
        sys.exit(1)

    target = sys.argv[1]
    do_all = '--all' in sys.argv

    if os.path.isfile(target):
        print(f"Adding watermark to: {os.path.basename(target)}")
        add_watermark(target)
        print("Done!")
    elif os.path.isdir(target) and do_all:
        pdfs = sorted([f for f in os.listdir(target) if f.endswith('.pdf')])
        print(f"Adding watermark to {len(pdfs)} PDFs...\n")
        for i, fname in enumerate(pdfs, 1):
            fpath = os.path.join(target, fname)
            try:
                add_watermark(fpath)
                print(f"  [{i}/{len(pdfs)}] OK  {fname}")
            except Exception as e:
                print(f"  [{i}/{len(pdfs)}] ERR {fname}: {e}")
        print(f"\nDone!")
    else:
        print(f"Not found: {target}")
        sys.exit(1)
