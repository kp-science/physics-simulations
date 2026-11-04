#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้างแถบ "📸 วิธีใช้แลป" ให้แลป: ภาพหน้าจอครบกระบวนการทีละขั้น พร้อมคำอธิบายและค่าที่ได้แต่ละขั้น
   → assets/guides/<ชุด>-lab-<เลข>/ (guide.json + step-N.jpg) และเพิ่มชื่อลง assets/guides/index.json

   Usage:
     python3 _admin/capture_lab_guide.py 60            # แลปเลข 60 (หรือ vpl02-lab-60)
     python3 _admin/capture_lab_guide.py --all         # ทุกแลปใน _admin/lab_guides/

   เนื้อหาขั้นตอน = _admin/lab_guides.py (กรอบเหลือง · prep ที่ตั้งสภาพแลป · คำอธิบาย · ค่าที่ได้)
   แสดงผลด้วย _shared/kp-labmode.js (เปิดแลปผ่าน http)
   ดีบัก: KPG_KEEP=<โฟลเดอร์> เก็บภาพดิบไว้ดู"""
import os, sys, json, subprocess, tempfile, threading, functools, http.server, socketserver, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labs_data import LABS
from lab_guides import GUIDES
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'assets', 'guides')
VW, VH = 1280, 800

def slug(acc): return acc.split(':', 1)[1].replace(':', '-')

NODE = r'''
const puppeteer = require('puppeteer');
const fs = require('fs');
const [,, cfgFile, outDir, port, base] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cfgFile, 'utf8'));
// ถ่ายภาพเท่านั้น: ปิดตัวกันหน้าใน kp-auth.js สำเนาที่ส่งให้ browser ตัวนี้ (ไฟล์จริงไม่ถูกแก้)
const AUTH = fs.readFileSync(base + '/kp-auth.js', 'utf8').replace('function kpPageAccess(required, redirectTo) {', 'function kpPageAccess(required, redirectTo) { return;');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--mute-audio'] });
  const page = await browser.newPage();
  page.on('dialog', d => d.dismiss().catch(() => {}));
  await page.setRequestInterception(true);
  page.on('request', rq => rq.url().split('?')[0].endsWith('/kp-auth.js')
    ? rq.respond({ status: 200, contentType: 'application/javascript', body: AUTH }) : rq.continue());
  await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 1 });
  await page.goto('http://127.0.0.1:' + port + '/' + cfg.href.split('/').map(encodeURIComponent).join('/'), { waitUntil: 'load', timeout: 60000 });
  await sleep(4500);
  await page.evaluate(src => { document.documentElement.style.scrollBehavior = 'auto'; window.alert = () => {}; window.confirm = () => true; (0, eval)(src); }, cfg.setup || '');
  const out = [];
  for (let i = 0; i < cfg.steps.length; i++) {
    const st = cfg.steps[i];
    const err = await page.evaluate(src => { try { (0, eval)(src); return null; } catch (e) { return String(e); } }, st.prep || '');
    await sleep(900);   // ให้ภาพ 3D/กราฟวาดสภาพใหม่
    const r = await page.evaluate(sels => {
      const els = sels.map(s => document.querySelector(s)).filter(e => e && e.getClientRects().length);
      if (!els.length) return null;
      els[0].scrollIntoView({ block: 'center', behavior: 'instant' });   // เลื่อนทั้งหน้าและแผงที่เลื่อนได้เอง
      const rs = els.map(e => e.getBoundingClientRect());
      const u = { y: Math.min(...rs.map(q => q.top)), b: Math.max(...rs.map(q => q.bottom)) };
      if (u.b - u.y < innerHeight && (u.y < 0 || u.b > innerHeight)) scrollBy(0, u.y - (innerHeight - (u.b - u.y)) / 2);
      return els.map(e => { const q = e.getBoundingClientRect(); return { x: q.left, y: q.top, w: q.width, h: q.height }; });
    }, [].concat(st.el || []));
    await sleep(350);
    const f = outDir + '/raw-step-' + (i + 1) + '.png';
    await page.screenshot({ path: f, captureBeyondViewport: false });
    out.push({ file: f, rects: r, err });
    process.stdout.write(err ? 'E' : (r ? 's' : '?'));
  }
  await browser.close();
  fs.writeFileSync(outDir + '/_result.json', JSON.stringify(out));
})();
'''

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def render(raw, rects, dst):
    """ทำนอกกรอบให้มืด + กรอบเหลืองมุมมน แล้วตัดรอบเป้าหมายให้เห็นบริบท"""
    from PIL import Image, ImageDraw
    im = Image.open(raw).convert('RGB')
    if rects:
        pad = 7
        boxes = [(max(0, r['x'] - pad), max(0, r['y'] - pad), min(VW, r['x'] + r['w'] + pad), min(VH, r['y'] + r['h'] + pad)) for r in rects]
        keep = [im.crop(tuple(int(v) for v in b)) for b in boxes]
        im = Image.blend(im, Image.new('RGB', im.size, (2, 6, 14)), 0.55)
        for b, k in zip(boxes, keep): im.paste(k, (int(b[0]), int(b[1])))
        d = ImageDraw.Draw(im)
        for b in boxes: d.rounded_rectangle([b[0], b[1], b[2] - 1, b[3] - 1], radius=10, outline=(250, 204, 21), width=4)
        x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
        w = min(max(x1 - x0 + 110, 540), VW); h = min(max(y1 - y0 + 110, 340), VH)   # ตัดชิดเป้าหมาย เห็นบริบทรอบ ๆ พอประมาณ
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        L = min(max(0, cx - w / 2), VW - w); T = min(max(0, cy - h / 2), VH - h)
        im = im.crop((int(L), int(T), int(L + w), int(T + h)))
    if im.width > 960: im = im.resize((960, round(im.height * 960 / im.width)), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=84, optimize=True, progressive=True)

def write_index():
    """index.json = ทุกโฟลเดอร์ที่มี guide.json (สร้างใหม่ทั้งไฟล์ → รันหลายแลปพร้อมกันได้)"""
    lst = sorted(d for d in os.listdir(OUT) if os.path.exists(os.path.join(OUT, d, 'guide.json')))
    tmp = os.path.join(OUT, '.index.%d.json' % os.getpid())
    json.dump(lst, open(tmp, 'w')); os.replace(tmp, os.path.join(OUT, 'index.json'))

def capture(lab, g, port):
    s = slug(lab[0]); d = os.path.join(OUT, s); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.startswith(('step-', 'btn-')): os.remove(os.path.join(d, f))
    with tempfile.TemporaryDirectory() as tmp:
        cf = os.path.join(tmp, 'cfg.json')
        json.dump({'href': lab[1], 'setup': g.get('setup', ''), 'steps': [{'el': x.get('el'), 'prep': x.get('prep', '')} for x in g['steps']]}, open(cf, 'w'))
        js = os.path.join(tmp, 'cap.js'); open(js, 'w').write(NODE)
        env = dict(os.environ, NODE_PATH=subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
        print('Exp %s %s ' % (lab[2], lab[3]), end='', flush=True)
        subprocess.run(['node', js, cf, tmp, str(port), BASE], env=env, check=True)
        res = json.load(open(os.path.join(tmp, '_result.json')))
        if os.environ.get('KPG_KEEP'): shutil.copytree(tmp, os.environ['KPG_KEEP'], dirs_exist_ok=True)
        steps, warn = [], []
        for n, (st, r) in enumerate(zip(g['steps'], res), 1):
            img = 'step-%d.jpg' % n
            render(r['file'], r['rects'], os.path.join(d, img))
            if r['err']: warn.append('ขั้น %d prep: %s' % (n, r['err']))
            if not r['rects']: warn.append('ขั้น %d หาเป้าหมาย %s ไม่เจอ' % (n, st.get('el')))
            steps.append({'img': img, 'title': st['title'], 'text': st['text'], 'out': st.get('out', '')})
    json.dump({'lab': lab[2], 'title': g.get('title', ''), 'steps': steps}, open(os.path.join(d, 'guide.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    write_index()
    print(' → %d ขั้น' % len(steps))
    for w in warn: print('  ⚠️ ' + w)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    want = list(GUIDES) if '--all' in sys.argv else args
    if not want: print(__doc__); return
    labs = [l for l in LABS if slug(l[0]) in GUIDES and any(a in (l[2], slug(l[0]), l[0]) for a in want)]
    if not labs: print('ยังไม่มีขั้นตอนของแลปนี้ใน _admin/lab_guides.py'); return
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=BASE))
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    for l in labs: capture(l, GUIDES[slug(l[0])], httpd.server_address[1])
    httpd.shutdown()

if __name__ == '__main__':
    main()
