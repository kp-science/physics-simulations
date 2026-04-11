#!/usr/bin/env python3
"""
Fix mobile layout for all simulation files.
Add order:-1 to canvas container so it appears above controls on mobile.
"""
import os, re

MECH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "Virtual Physics Lab 01", "Mechacnics")

# (filename, canvas_container_css_selector, mobile_breakpoint_px)
FILES = [
    ("1. measuring_precision.html",        ".right-panel",  700),   # canvas in right-panel -> should be first
    ("2. vector_forces_sim.html",          ".canvas-area",  860),
    ("3. torques_simulation.html",         ".canvas-area",  768),
    ("4. force_resolution_sim.html",       ".canvas-wrap",  600),
    ("5. incline_forces.html",             ".canvas-col",   600),
    ("6.1 pendulum_timer.html",            ".sim-center",   900),
    ("6.2water-clock-simulation.html",     ".canvas-wrap",  1000),
    ("6.3 tape_timer_simulation.html",     ".sim-center",   920),
    ("7. strobe_photography_simulation.html", ".canvas-wrap", 900),
    ("8. straight-line-motion-simulation.html", ".canvas-wrap", 600),
    ("9. galileo-water-clock-simulation.html", ".sim-center", 1100),
    ("10. spinning_disc_sim.html",         ".canvas-wrap",  900),
    ("11. air_track_simulation.html",      ".canvas-wrap",  980),
    ("12. turntable_gravity_simulation.html", ".canvas-wrap", 1200),
    ("13. free-fall-experiment.html",      ".canvas-card",  1100),
    ("14.mass_weight_simulation.html",     ".canvas-wrap",  768),
    ("15. newtons_second_law_simulation.html", ".canvas-wrap", 1000),
    ("16. trajectories_simulation.html",   ".canvas-card",  1100),
    ("17. centripetal_force_simulation.html", ".canvas-wrap", 960),
    ("18. newton_third_law_simulation.html", ".canvas-wrap", 960),
    # 19 already fixed
    ("20. tilted_air_track.html",          ".canvas-wrap",  980),
]


def fix_file(filepath, canvas_cls, breakpoint):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    cls_name = canvas_cls.lstrip('.')

    # Check if already has order:-1 for this class
    if f'{cls_name}{{order:-1' in content.replace(' ', '') or f'{cls_name}{{ order:-1' in content.replace(' ', '') or f'{cls_name}{{order: -1' in content:
        print(f"  SKIP {fname}: already has order fix")
        return False

    # Strategy: find the mobile media query for this breakpoint and add the order rule
    # Look for @media(max-width:XXXpx) that contains grid-template-columns:1fr
    pattern = rf'(@media\s*\(\s*max-width\s*:\s*{breakpoint}px\s*\)\s*\{{)'

    match = re.search(pattern, content)
    if match:
        # Add canvas order rule right after the opening brace
        insert_pos = match.end()
        # Check if the class is already mentioned in this media query
        # Find the closing brace of this media query
        brace_count = 1
        i = insert_pos
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        media_block = content[insert_pos:i]

        if f'{cls_name}' in media_block and 'order' in media_block:
            print(f"  SKIP {fname}: order already in media query")
            return False

        # Insert the order rule
        rule = f'\n  {canvas_cls}{{order:-1}}'
        content = content[:insert_pos] + rule + content[insert_pos:]
    else:
        # No matching media query found — try broader search
        # Look for any mobile media query that sets grid to 1fr
        mobile_pattern = r'(@media\s*\(\s*max-width\s*:\s*\d+px\s*\)\s*\{[^}]*grid-template-columns\s*:\s*1fr)'
        matches = list(re.finditer(mobile_pattern, content))
        if matches:
            # Use the last match (most likely the main layout one)
            m = matches[-1]
            # Find the closing } of this rule inside the media query
            rule_end = content.find('}', m.end())
            if rule_end != -1:
                rule = f'\n  {canvas_cls}{{order:-1}}'
                content = content[:rule_end+1] + rule + content[rule_end+1:]
            else:
                print(f"  FAIL {fname}: couldn't find insertion point")
                return False
        else:
            print(f"  FAIL {fname}: no mobile media query found")
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {fname} ({canvas_cls} order:-1 at {breakpoint}px)")
    return True


if __name__ == '__main__':
    print("=== Fixing mobile layout (canvas above controls) ===\n")
    count = 0
    for fname, cls, bp in FILES:
        fpath = os.path.join(MECH, fname)
        if os.path.exists(fpath):
            if fix_file(fpath, cls, bp):
                count += 1
        else:
            print(f"  MISS {fname}")
    print(f"\nFixed: {count}/{len(FILES)}")
