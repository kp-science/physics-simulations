#!/usr/bin/env python3
"""
Add lock icon system to download buttons.
- Lab 1-5: always show ⬇ (free)
- Lab 6+: show 🔒 if not logged in, ⬇ if logged in
"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MECH = os.path.join(BASE, "Virtual Physics Lab 01", "Mechacnics")

# CSS for locked state
LOCK_CSS = """
/* Download lock state */
.dl-locked{border-color:rgba(148,163,184,0.5)!important;color:#94a3b8!important}
.dl-locked:hover{border-color:rgba(148,163,184,0.7)!important;background:rgba(148,163,184,0.08)!important}"""

# JS that auto-detects download buttons and toggles lock/unlock based on auth
LOCK_JS = """<script>
/* KP Download Lock — auto lock/unlock based on auth */
(function(){
  var FREE=[1,2,3,4,5];
  function isFree(n){return FREE.some(function(f){return Math.abs(f-n)<0.01})||n<1}
  function getLabBtns(){
    var r=[];
    document.querySelectorAll('.btn-dl-pdf,.sc-dl-btn,.lib-dl-btn').forEach(function(b){
      var oc=b.getAttribute('onclick')||'';
      var m=oc.match(/dlPdf\\([^,]+,\\s*([\\d.]+)\\)/);
      if(m){var n=parseFloat(m[1]);if(!isFree(n))r.push(b)}
    });
    return r;
  }
  function update(user){
    getLabBtns().forEach(function(b){
      var t=b.textContent.replace(/^[\\u2b07\\u{1f512}\\u{1f513}]\\s*/u,'').replace(/^⬇\\s*/,'');
      if(user){b.classList.remove('dl-locked');b.textContent='⬇ '+t}
      else{b.classList.add('dl-locked');b.textContent='\\u{1f512} '+t}
    });
  }
  update(null);
  var iv=setInterval(function(){
    if(typeof firebase!=='undefined'&&firebase.auth){
      clearInterval(iv);
      firebase.auth().onAuthStateChanged(update);
    }
  },200);
  setTimeout(function(){clearInterval(iv)},10000);
})();
</script>"""


def add_lock_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fname = os.path.basename(filepath)
    changed = False

    # Skip if already has lock system
    if 'KP Download Lock' in content:
        print(f"  SKIP {fname}: already has lock system")
        return False

    # Step 1: Add lock CSS to <style> block
    # Find the main </style> tag (after <meta charset)
    charset_pos = content.find('<meta charset')
    if charset_pos == -1:
        charset_pos = 0

    style_end = content.find('</style>', charset_pos)
    if style_end != -1 and '.dl-locked' not in content:
        content = content[:style_end] + LOCK_CSS + '\n' + content[style_end:]
        changed = True

    # Step 2: Add lock JS after kp-auth.js (or before </body> if no kp-auth)
    if 'kp-auth.js' in content:
        # Insert right after kp-auth.js script tag
        auth_pos = content.rfind('kp-auth.js')
        script_end = content.find('>', auth_pos)
        if script_end != -1:
            # Find the end of that </script> tag
            close_tag = content.find('</script>', script_end)
            if close_tag == -1:
                close_tag = script_end
            else:
                close_tag += len('</script>')
            content = content[:close_tag] + '\n' + LOCK_JS + content[close_tag:]
            changed = True
    else:
        # No kp-auth.js — insert before </body>
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + LOCK_JS + '\n' + content[body_end:]
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK   {fname}")
        return True
    else:
        print(f"  NOOP {fname}")
        return False


# Files to update
SIM_FILES = [
    "6.1 pendulum_timer.html",
    "6.2water-clock-simulation.html",
    "6.3 tape_timer_simulation.html",
    "7. strobe_photography_simulation.html",
    "8. straight-line-motion-simulation.html",
    "9. galileo-water-clock-simulation.html",
    "10. spinning_disc_sim.html",
    "11. air_track_simulation.html",
    "12. turntable_gravity_simulation.html",
    "13. free-fall-experiment.html",
    "14.mass_weight_simulation.html",
    "15. newtons_second_law_simulation.html",
]

PAGE_FILES = [
    os.path.join(BASE, "virtual-physics-lab-01.html"),
    os.path.join(BASE, "library.html"),
]

if __name__ == '__main__':
    print("=== Adding lock system ===\n")

    count = 0
    print("Simulation files:")
    for fname in SIM_FILES:
        fpath = os.path.join(MECH, fname)
        if os.path.exists(fpath):
            if add_lock_to_file(fpath):
                count += 1
        else:
            print(f"  MISS {fname}")

    print("\nPage files:")
    for fpath in PAGE_FILES:
        if os.path.exists(fpath):
            if add_lock_to_file(fpath):
                count += 1
        else:
            print(f"  MISS {os.path.basename(fpath)}")

    print(f"\nUpdated: {count} files")
