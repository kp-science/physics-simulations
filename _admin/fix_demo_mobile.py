#!/usr/bin/env python3
"""Fix mobile layout for Demo/mechanics simulation files — canvas above controls."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "Demo", "mechanics")

# (filepath relative to BASE, canvas_container_class, breakpoint)
# Only files where controls appear BEFORE canvas in HTML/grid order
FILES = [
    # Controls LEFT (small px), Canvas RIGHT (1fr) → canvas pushed down on mobile
    ("การเคลื่อนที่แนวตรง/stone_ab_simulation.html",    ".canvas-area", 900),
    ("กฎนิวตัน/sliding_weights_triangle.html",           ".canvas-area", 880),
    ("กฎนิวตัน/incline_forces_v7.html",                  ".canvas-col",  680),
    ("โปรเจคไทล์/air_table_parabolas.html",              ".canvas-wrap", 920),
    ("เวกเตอร์/bulldozer_moving_sheet.html",             ".canvas-wrap", 940),
    # Files with controls-right but worth checking
    ("กฎนิวตัน/guinea_feather.html",                     ".canvas-wrap", 860),
    ("กฎนิวตัน/Demo_01-10_Rolling_Ball_Incline.html",    ".canvas-col",  900),
    ("กฎนิวตัน/inertia02_v2_1.html",                     ".sim-main",    700),
    ("โปรเจคไทล์/vertical_gun_car.html",                 "#cvw",         768),
    ("เวกเตอร์/demo_01-09_upgraded.html",                ".canvas-wrap", 780),
    ("โปรเจคไทล์/demo02_01_shooter_dropper.html",        ".canvas-area", 800),
    ("กฎนิวตัน/atwood_machine.html",                     ".canvas-col",  860),
    ("เวกเตอร์/Demo_01-09_Bulldozer_Moving_Sheet.html",  ".canvas-wrap", 768),
]


def fix_file(filepath, canvas_cls, breakpoint):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    cls_clean = canvas_cls.lstrip('.').lstrip('#')

    # Check if already has order fix
    if 'order:-1' in content.replace(' ', '') and cls_clean in content:
        # Check if order:-1 is associated with our class
        if re.search(rf'{re.escape(canvas_cls)}\s*\{{[^}}]*order\s*:\s*-1', content):
            print(f"  SKIP {fname}: already has order fix")
            return False

    # Find the mobile media query
    pattern = rf'(@media\s*\(\s*max-width\s*:\s*{breakpoint}px\s*\)\s*\{{)'
    match = re.search(pattern, content)

    if match:
        insert_pos = match.end()
        rule = f'\n  {canvas_cls}{{order:-1}}'
        content = content[:insert_pos] + rule + content[insert_pos:]
    else:
        # Try finding any media query close to the breakpoint (±100px)
        for bp_try in range(breakpoint - 100, breakpoint + 101, 10):
            pattern2 = rf'(@media\s*\(\s*max-width\s*:\s*{bp_try}px\s*\)\s*\{{)'
            match2 = re.search(pattern2, content)
            if match2:
                insert_pos = match2.end()
                rule = f'\n  {canvas_cls}{{order:-1}}'
                content = content[:insert_pos] + rule + content[insert_pos:]
                print(f"  OK   {fname} ({canvas_cls} order:-1 at {bp_try}px instead of {breakpoint}px)")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

        # Last resort: add new media query before </style>
        style_end = content.rfind('</style>')
        if style_end != -1:
            rule = f'\n@media(max-width:{breakpoint}px){{{canvas_cls}{{order:-1}}}}\n'
            content = content[:style_end] + rule + content[style_end:]
        else:
            print(f"  FAIL {fname}: no </style> found")
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {fname} ({canvas_cls} order:-1 at {breakpoint}px)")
    return True


if __name__ == '__main__':
    print("=== Fixing Demo/mechanics mobile layout ===\n")
    count = 0
    for rel_path, cls, bp in FILES:
        fpath = os.path.join(BASE, rel_path)
        if os.path.exists(fpath):
            if fix_file(fpath, cls, bp):
                count += 1
        else:
            print(f"  MISS {rel_path}")
    print(f"\nFixed: {count}/{len(FILES)}")
