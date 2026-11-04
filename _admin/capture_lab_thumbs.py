#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ถ่ายภาพหน้าจอภาพ 3D ของทุกแลปมาทำภาพการ์ดใน virtual-lab.html
   → assets/thumbs/labs/<series>-<lab>.jpg  (640×360)

   Usage:
     python3 _admin/capture_lab_thumbs.py            # ถ่ายเฉพาะแลปที่ยังไม่มีภาพ
     python3 _admin/capture_lab_thumbs.py --force    # ถ่ายใหม่ทั้งหมด
     python3 _admin/capture_lab_thumbs.py 46 vpl08   # ถ่ายเฉพาะแลปที่เลข/ชุด/access ตรง (ถ่ายทับ)
     python3 _admin/capture_lab_thumbs.py --check    # ดูว่าแลปไหนยังไม่มีภาพ

   ต้องมี node + puppeteer (npm i -g puppeteer) · ภาพไหนไม่สวย แทนไฟล์เองได้ (ชื่อเดิม 640×360)
   แล้วรัน python3 _admin/build_virtual_lab.py ให้การ์ดใช้ภาพ"""
import os, sys, json, subprocess, tempfile, threading, functools, http.server, socketserver
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labs_data import LABS
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'assets', 'thumbs', 'labs')
W, H = 640, 360
# แลปที่หน้าเริ่มต้นยังไม่มีภาพทดลอง (จอว่าง/เมนูเลือกชุด) → ไม่ถ่ายอัตโนมัติ การ์ดจะไม่มีภาพ
# อยากได้ภาพ: ถ่ายเองตอนกำลังทดลอง แล้ววางไฟล์ชื่อตามนี้ (640×360 .jpg) ใน assets/thumbs/labs/
SKIP = {'vpl01-lab-6.3', 'vpl02-lab-39', 'vpl02-lab-43'}

def slug(acc):  # 'vlab:vpl01:lab-6.1' → 'vpl01-lab-6.1'
    return acc.split(':', 1)[1].replace(':', '-')

def thumb_path(acc):
    return os.path.join(OUT, slug(acc) + '.jpg')

NODE = r'''
const puppeteer = require('puppeteer');
const fs = require('fs');
const [,, listFile, rawDir, port, base] = process.argv;
// ใช้ถ่ายภาพเท่านั้น: ปิดตัวกันหน้า (kpPageAccess) ในสำเนา kp-auth.js ที่ส่งให้ browser ตัวนี้ ไฟล์จริงไม่ถูกแก้
const AUTH = fs.readFileSync(base + '/kp-auth.js', 'utf8').replace('function kpPageAccess(required, redirectTo) {', 'function kpPageAccess(required, redirectTo) { return;');
const labs = JSON.parse(fs.readFileSync(listFile, 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const browser = await puppeteer.launch({ headless: true,
    args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required', '--mute-audio'] });
  const res = {};
  let i = 0;
  async function worker() {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 1 });
    page.on('dialog', d => d.dismiss().catch(() => {}));
    await page.setRequestInterception(true);
    page.on('request', rq => rq.url().split('?')[0].endsWith('/kp-auth.js')
      ? rq.respond({ status: 200, contentType: 'application/javascript', body: AUTH }) : rq.continue());
    while (i < labs.length) {
      const L = labs[i++];
      const url = 'http://127.0.0.1:' + port + '/' + L.href.split('/').map(encodeURIComponent).join('/');
      try {
        await page.goto(url, { waitUntil: 'load', timeout: 45000 });
        await sleep(5500);                     // ให้ three.js + env map + เงา เรนเดอร์เสร็จ
        // ① หา canvas หลัก (ใหญ่สุด ไม่ใช่ชั้นลายน้ำที่ pointer-events:none) แล้วเลื่อนให้อยู่กลางจอ
        await page.evaluate(() => {
          try { window.KPWatermark && KPWatermark.remove(); } catch (e) {}
          let best = null, area = 0;
          for (const c of document.querySelectorAll('canvas')) {
            const r = c.getBoundingClientRect(), cs = getComputedStyle(c);
            if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
            const overlay = cs.pointerEvents === 'none' && /absolute|fixed/.test(cs.position);
            let gl = c.hasAttribute('data-engine');   // three.js ใส่ data-engine ให้ canvas ที่มันสร้าง
            if (!gl && r.width * r.height > 0) try { gl = !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) {}
            const a = r.width * r.height * (overlay ? 0.01 : 1) * (gl ? 100 : 1);   // ภาพ 3D มาก่อนกราฟ 2D
            if (a > area) { area = a; best = c; }
          }
          document.querySelectorAll('canvas').forEach(c => c.removeAttribute('data-kpcap'));
          if (best) { best.setAttribute('data-kpcap', best.hasAttribute('data-engine') || (() => { try { return !!(best.getContext('webgl2') || best.getContext('webgl')); } catch (e) { return false; } })() ? 'gl' : '2d'); const r = best.getBoundingClientRect();
            document.documentElement.style.scrollBehavior = 'auto'; document.body.style.scrollBehavior = 'auto';
            if (r.top < 0 || r.bottom > innerHeight) best.scrollIntoView({ behavior: 'instant', block: r.height > innerHeight ? 'start' : 'center' }); }
        });
        await sleep(700);
        const info = await page.evaluate(() => {
          const vw = innerWidth, vh = innerHeight, c = document.querySelector('canvas[data-kpcap]');
          if (!c) return { best: null, frac: 0, url: location.href, locked: false };
          const r = c.getBoundingClientRect();
          const x0 = Math.max(0, r.left), y0 = Math.max(0, r.top), x1 = Math.min(vw, r.right), y1 = Math.min(vh, r.bottom);
          const best = { x: x0, y: y0, w: Math.max(0, x1 - x0), h: Math.max(0, y1 - y0) };
          const gl = c.getAttribute('data-kpcap') === 'gl';
          const wide = !gl && best.w / Math.max(1, best.h) > 2.2;
          // ② ซ่อนทุกอย่างที่ทับภาพหลัก (แถบเครื่องมือ แผงคำอธิบาย ปุ่ม แถบบน ลายน้ำ) — เหลือแต่ภาพแลป
          for (const e of document.querySelectorAll('body *')) {
            if (e === c || e.contains(c)) continue;
            const cs = getComputedStyle(e), p = cs.position;
            const floating = p === 'fixed' || p === 'absolute' || p === 'sticky';
            const q = e.getBoundingClientRect();
            const overlaps = !wide && q.right > x0 + 2 && q.left < x1 - 2 && q.bottom > y0 + 2 && q.top < y1 - 2;
            if (floating || overlaps)
              e.style.setProperty('visibility', 'hidden', 'important');
          }
          return { best, gl, sx: scrollX, sy: scrollY, frac: best.w * best.h / (vw * vh), url: location.href, locked: /สมาชิกเท่านั้น|ไม่มีสิทธิ์/.test(document.body.innerText.slice(0, 4000)) };
        });
        await sleep(150);
        let clip = info.best && info.frac > 0.08 ? info.best : { x: 0, y: 60, w: 1280, h: 740 };
        // ตัดตรงกลางให้เป็น 16:9
        let { x, y, w, h } = clip;
        const wide = !info.gl && w / h > 2.2;   // แลป 2D แบบแถบยาว → ขยายกรอบให้เห็นรอบ ๆ แทนการตัดตรงกลาง
        if (wide) { const nh = Math.min(800, w * 9 / 16); y = Math.max(0, Math.min(800 - nh, y + h / 2 - nh / 2)); h = nh; w = h * 16 / 9; x = Math.max(0, Math.min(1280 - w, x)); }
        else if (w / h > 16 / 9) { const nw = h * 16 / 9; x += (w - nw) / 2; w = nw; } else { const nh = w * 9 / 16; y += (h - nh) / 2; h = nh; }
        if (!wide && info.best && info.frac > 0.08) { const z = 0.86; x += w * (1 - z) / 2; y += h * (1 - z) / 2; w *= z; h *= z; }   // ซูมเข้ากลางภาพเล็กน้อย
        const file = rawDir + '/' + L.slug + '.png';
        // ถ่ายเฉพาะส่วนที่เห็นบนจอ แล้วให้ Python ตัดตามกรอบ (พิกัดบนจอ ไม่ต้องสนใจการเลื่อนหน้า)
        await page.screenshot({ path: file });
        res[L.slug] = { ok: true, box: [x, y, w, h], canvas: !!(info.best && info.frac > 0.08), redirected: !info.url.includes(L.href.split('/').pop().slice(0, 8).replace(/ /g, '%20')), locked: info.locked };
        process.stdout.write('.');
      } catch (e) { res[L.slug] = { ok: false, err: String(e).slice(0, 160) }; process.stdout.write('x'); }
    }
    await page.close();
  }
  await Promise.all([worker(), worker(), worker(), worker()]);
  await browser.close();
  fs.writeFileSync(rawDir + '/_result.json', JSON.stringify(res));
})();
'''

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    force = '--force' in sys.argv
    if '--check' in sys.argv:
        miss = [l for l in LABS if not os.path.exists(thumb_path(l[0]))]
        print('มีภาพแล้ว %d / %d' % (len(LABS) - len(miss), len(LABS)))
        for l in miss: print('  ยังไม่มี:', l[2], l[3])
        return
    if args:
        todo = [l for l in LABS if any(a == l[2] or a == l[7] or a == l[0] or a == slug(l[0]) for a in args)]
    else:
        todo = [l for l in LABS if slug(l[0]) not in SKIP and (force or not os.path.exists(thumb_path(l[0])))]
    if not todo: print('ทุกแลปมีภาพแล้ว (ใช้ --force เพื่อถ่ายใหม่)'); return
    os.makedirs(OUT, exist_ok=True)
    from PIL import Image
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=BASE))
    httpd.daemon_threads = True
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory() as tmp:
        lf = os.path.join(tmp, 'labs.json')
        json.dump([{'slug': slug(l[0]), 'href': l[1]} for l in todo], open(lf, 'w'))
        js = os.path.join(tmp, 'cap.js'); open(js, 'w').write(NODE)
        env = dict(os.environ, NODE_PATH=subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
        print('กำลังถ่าย %d แลป' % len(todo), flush=True)
        subprocess.run(['node', js, lf, tmp, str(port), BASE], env=env, check=True)
        res = json.load(open(os.path.join(tmp, '_result.json')))
        bad = []
        for l in todo:
            s = slug(l[0]); r = res.get(s, {'ok': False, 'err': 'no result'})
            raw = os.path.join(tmp, s + '.png')
            if not r.get('ok') or not os.path.exists(raw):
                bad.append((l[2], l[3], r.get('err'))); continue
            x, y, w, h = r['box']
            im = Image.open(raw).convert('RGB').crop((round(x), round(y), round(x + w), round(y + h))).resize((W, H), Image.LANCZOS)
            im.save(thumb_path(l[0]), 'JPEG', quality=80, optimize=True, progressive=True)
            if not r.get('canvas') or r.get('locked'):
                bad.append((l[2], l[3], 'ไม่เจอภาพ canvas ใหญ่ — ใช้ภาพทั้งหน้า' if not r.get('canvas') else 'หน้าล็อกสมาชิก'))
    httpd.shutdown()
    print('\nเสร็จ %d แลป → %s' % (len(todo), os.path.relpath(OUT, BASE)))
    for b in bad: print('  ⚠️ Exp %s %s — %s' % b)

if __name__ == '__main__':
    main()
