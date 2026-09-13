#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้าง virtual-lab.html (catalog รวมทุก lab จัดตามบทเรียน สสวท.) + เขียนหมวด Virtual Lab ใน library.html ใหม่
   Usage: python3 _admin/build_virtual_lab.py"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labs_data import TOPICS, GROUPS, LABS, SERIES
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T={t[0]:t for t in TOPICS}
by_topic={t[0]:[l for l in LABS if l[5]==t[0]] for t in TOPICS}
LEVEL_KEY={'ม.4':'m4','ม.5':'m5','ม.6':'m6','ปริญญาตรี':'uni'}
esc=html.escape

def card(l):
    acc,href,num,title,desc,topic,level,series,tags=l
    t=T[topic]; clr='var(--'+t[4]+')'
    stag=SERIES[series][0]
    tag_html=''.join(f'<span class="tag tag-soft">{esc(x)}</span>' for x in tags[:2])
    return f'''      <a data-locked="true" data-access="{acc}" href="{esc(href)}" class="demo-card lab-card" data-topic="{topic}" data-level="{LEVEL_KEY[level]}" data-series="{series}" data-search="{esc((title+' '+desc+' '+' '.join(tags)+' '+num).lower())}" style="--card-accent:{clr}">
        <div class="lc-head"><span class="lc-icon">{t[1]}</span><span class="lc-num">{'Lab' if series=='vpl03' else 'Exp'} {esc(num)}</span><span class="lc-level">{esc(level)}</span><span class="lc-series">{stag}</span></div>
        <div class="dc-body"><div class="dc-title">{esc(title)}</div><p class="dc-desc">{esc(desc)}</p></div>
        <div class="dc-footer"><div class="dc-tags">{tag_html}</div><div class="dc-arrow">→</div></div>
      </a>
'''

def build_page():
    sections=''
    for g in GROUPS:
        gid,gicon,gname,tids=g
        n=sum(len(by_topic[t]) for t in tids)
        sections+=f'\n<div class="group-anchor" id="g-{gid}"><span class="ga-icon">{gicon}</span><span class="ga-name">{esc(gname)}</span><span class="ga-count">{n} การทดลอง</span></div>\n'
        for tid in tids:
            t=T[tid]; labs=by_topic[tid]
            if not labs: continue
            sections+=f'''<section class="topic-section" id="t-{tid}" data-topic="{tid}" style="--tclr:var(--{t[4]})">
  <div class="topic-header"><div class="topic-icon">{t[1]}</div><div><div class="topic-name">{esc(t[2])}</div><div class="topic-en">{esc(t[3])}</div></div><span class="topic-count" data-count>{len(labs)} การทดลอง</span></div>
  <div class="demo-grid">
{''.join(card(l) for l in labs)}  </div>
</section>
'''
    topic_chips=''.join(f'<button class="fchip" data-f="topic" data-v="{t[0]}" onclick="setFilter(this)">{t[1]} {esc(t[2])}</button>' for t in TOPICS if by_topic[t[0]])
    total=len(LABS)
    return f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KP Science — Virtual Lab ทั้งหมด จัดตามบทเรียน</title>
<meta name="description" content="ห้องปฏิบัติการฟิสิกส์เสมือน {total} การทดลอง จัดตามบทเรียนฟิสิกส์ ม.ปลาย (สสวท.) — การวัด การเคลื่อนที่ แรงและกฎนิวตัน SHM คลื่น เสียง แสง ดาราศาสตร์">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700;800&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{{--bg:#06090f;--bg2:#0d1117;--bg3:#161b27;--bg4:#1c2333;--border:rgba(255,255,255,0.07);--border2:rgba(255,255,255,0.14);
--accent:#38bdf8;--accent2:#818cf8;--accent3:#34d399;--accent4:#fb923c;--accent5:#f472b6;--text:#f0f4f8;--muted:#7c8fa6;--card:#0d1421}}
*{{box-sizing:border-box;margin:0;padding:0}} html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:'Sarabun',sans-serif;line-height:1.6;min-height:100vh}}
nav.topnav{{position:sticky;top:50px;z-index:100;background:rgba(6,9,15,0.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 5%;display:flex;align-items:center;gap:1rem;height:52px}}
.nav-logo{{font-size:1rem;font-weight:700;color:var(--accent)}} .nav-logo span{{color:var(--accent2)}}
.nav-back{{margin-left:auto;color:var(--muted);text-decoration:none;font-size:.85rem}} .nav-back:hover{{color:var(--accent)}}
.hero{{padding:44px 5% 28px;background:linear-gradient(180deg,rgba(56,189,248,0.05),transparent);border-bottom:1px solid var(--border)}}
.hero-inner{{max-width:1200px;margin:0 auto}}
.hero-badge{{display:inline-flex;align-items:center;gap:.5rem;background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.22);color:var(--accent);padding:5px 16px;border-radius:20px;font-size:.78rem;font-weight:700;letter-spacing:1px;margin-bottom:1rem}}
.hero h1{{font-size:clamp(1.5rem,3.6vw,2.2rem);font-weight:800;margin-bottom:.4rem}} .hero h1 span{{color:var(--accent)}}
.hero p{{color:var(--muted);font-size:.98rem;max-width:640px;line-height:1.7}}
.series-links{{margin-top:.8rem;font-size:.82rem;color:var(--muted)}} .series-links a{{color:var(--accent);text-decoration:none;margin-left:.4rem}}
/* filter bar */
.fbar{{position:sticky;top:102px;z-index:90;background:rgba(6,9,15,0.96);backdrop-filter:blur(14px);border-bottom:1px solid var(--border);padding:.7rem 5%}}
.fbar-inner{{max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:.5rem}}
.frow{{display:flex;gap:.4rem;flex-wrap:wrap;align-items:center}}
.flabel{{font-size:.72rem;color:var(--muted);font-weight:700;min-width:54px;text-transform:uppercase;letter-spacing:.5px}}
.fchip{{background:var(--bg3);border:1px solid var(--border);color:var(--muted);padding:5px 12px;border-radius:20px;font-size:.78rem;font-weight:600;cursor:pointer;font-family:inherit;transition:.2s;white-space:nowrap}}
.fchip:hover{{border-color:var(--accent);color:var(--text)}} .fchip.active{{background:var(--accent);border-color:var(--accent);color:#06090f}}
.fsearch{{margin-left:auto;background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:8px;font-family:inherit;font-size:.85rem;min-width:220px}}
.fsearch:focus{{outline:none;border-color:var(--accent)}}
.fcount{{font-size:.78rem;color:var(--muted);font-family:'Share Tech Mono',monospace}}
/* groups / topics */
.wrap{{max-width:1200px;margin:0 auto;padding:1.6rem 5% 3rem}}
.group-anchor{{display:flex;align-items:center;gap:.7rem;margin:2.2rem 0 1rem;padding-bottom:.5rem;border-bottom:2px solid var(--border2);scroll-margin-top:170px}}
.group-anchor:first-child{{margin-top:.4rem}}
.ga-icon{{font-size:1.5rem}} .ga-name{{font-size:1.3rem;font-weight:800}} .ga-count{{margin-left:auto;font-size:.78rem;color:var(--muted);font-family:'Share Tech Mono',monospace}}
.topic-section{{margin-bottom:2rem;scroll-margin-top:170px}}
.topic-header{{display:flex;align-items:center;gap:.75rem;padding:.75rem 1rem;background:var(--bg2);border:1px solid var(--border);border-left:4px solid var(--tclr);border-radius:10px;margin-bottom:1rem}}
.topic-icon{{width:38px;height:38px;border-radius:9px;background:color-mix(in srgb,var(--tclr) 14%,transparent);display:flex;align-items:center;justify-content:center;font-size:1.1rem}}
.topic-name{{font-weight:700;font-size:1rem}} .topic-en{{font-size:.75rem;color:var(--muted)}}
.topic-count{{margin-left:auto;font-size:.73rem;font-family:'Share Tech Mono',monospace;color:var(--muted);background:var(--bg3);border:1px solid var(--border);padding:2px 10px;border-radius:20px}}
.demo-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}}
.demo-card{{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;transition:.25s;position:relative;display:flex;flex-direction:column;text-decoration:none;color:var(--text)}}
.demo-card:hover{{transform:translateY(-4px);border-color:var(--card-accent,var(--accent))}}
.demo-card:hover .dc-arrow{{background:var(--card-accent,var(--accent));color:#06090f;border-color:var(--card-accent,var(--accent))}}
.lc-head{{display:flex;align-items:center;gap:.5rem;padding:.7rem 1rem;background:linear-gradient(135deg,color-mix(in srgb,var(--card-accent) 18%,#0d1421),#0d1421);border-bottom:1px solid var(--border)}}
.lc-icon{{font-size:1.2rem}} .lc-num{{font-family:'Share Tech Mono',monospace;font-weight:800;color:var(--card-accent);font-size:.9rem}}
.lc-level{{margin-left:auto;font-size:.68rem;font-weight:700;color:var(--muted);background:var(--bg3);border:1px solid var(--border);padding:1px 8px;border-radius:10px}}
.lc-series{{font-size:.64rem;font-weight:700;color:var(--muted);border:1px dashed var(--border2);padding:1px 6px;border-radius:6px;letter-spacing:.3px}}
.dc-body{{padding:.9rem 1rem .6rem;flex:1;display:flex;flex-direction:column;gap:.35rem}}
.dc-title{{font-size:.95rem;font-weight:700;line-height:1.35}} .dc-desc{{font-size:.8rem;color:var(--muted);line-height:1.55;flex:1}}
.dc-footer{{padding:.6rem 1rem .85rem;display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border)}}
.dc-tags{{display:flex;gap:.3rem;flex-wrap:wrap}}
.tag{{display:inline-block;font-size:.66rem;font-weight:700;padding:2px 8px;border-radius:20px}}
.tag-soft{{background:rgba(255,255,255,0.05);color:var(--muted);border:1px solid var(--border)}}
.dc-arrow{{width:28px;height:28px;border-radius:50%;border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:.75rem;color:var(--muted);transition:.2s;flex-shrink:0}}
.empty{{display:none;text-align:center;color:var(--muted);padding:3rem 0}} .empty.show{{display:block}}
footer{{border-top:1px solid var(--border);padding:1.5rem 5%;text-align:center;color:var(--muted);font-size:.85rem}} footer a{{color:var(--accent);text-decoration:none}}
@media(max-width:768px){{.fbar{{top:100px}}.fsearch{{margin-left:0;width:100%}}.flabel{{min-width:100%}}.demo-grid{{grid-template-columns:1fr}}.hero{{padding:28px 5% 20px}}}}
/* === KP Access Lock Overlay === */
[data-locked="true"].kp-locked{{position:relative;pointer-events:all}}
[data-locked="true"].kp-locked::after{{content:'🔒  สมาชิกเท่านั้น';position:absolute;inset:0;background:rgba(6,9,15,0.75);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;color:var(--accent);font-weight:700;font-size:.9rem;border-radius:14px;z-index:5}}
</style>
</head>
<body>

<nav class="topnav"><div class="nav-logo">KP<span>Science</span></div><a href="index.html" class="nav-back">← กลับหน้าหลัก</a></nav>

<div class="hero"><div class="hero-inner">
  <div class="hero-badge">🧪 VIRTUAL PHYSICS LAB · จัดตามบทเรียน</div>
  <h1>ห้องปฏิบัติการฟิสิกส์เสมือน <span>ทั้งหมด {total} การทดลอง</span></h1>
  <p>เลือกจากบทเรียนฟิสิกส์ ม.ปลาย (สสวท.) ได้โดยตรง — การวัด · การเคลื่อนที่ · แรงและกฎนิวตัน · SHM · คลื่น · เสียง · แสง · ดาราศาสตร์ — เปิดได้ทันที ไม่ต้องติดตั้ง</p>
  <div class="series-links">ดูแบบชุดเดิม: <a href="virtual-physics-lab-01.html">VPL 01 กลศาสตร์</a> · <a href="virtual-physics-lab-02.html">VPL 02 คลื่น แสง เสียง</a></div>
</div></div>

<div class="fbar"><div class="fbar-inner">
  <div class="frow"><span class="flabel">กลุ่ม</span>
    <button class="fchip active" data-f="topic" data-v="all" onclick="setFilter(this)">ทั้งหมด</button>
    {''.join(f'<button class="fchip" data-f="group" data-v="{g[0]}" onclick="setFilter(this)">{g[1]} {esc(g[2])}</button>' for g in GROUPS)}
    <input class="fsearch" id="q" type="search" placeholder="🔍 ค้นหา เช่น เลนส์, นิวตัน, Exp 37" oninput="applyFilter()">
  </div>
  <div class="frow"><span class="flabel">บทเรียน</span>{topic_chips}</div>
  <div class="frow"><span class="flabel">ระดับ</span>
    <button class="fchip active" data-f="level" data-v="all" onclick="setFilter(this)">ทุกระดับ</button>
    <button class="fchip" data-f="level" data-v="m4" onclick="setFilter(this)">ม.4</button>
    <button class="fchip" data-f="level" data-v="m5" onclick="setFilter(this)">ม.5</button>
    <button class="fchip" data-f="level" data-v="m6" onclick="setFilter(this)">ม.6</button>
    <button class="fchip" data-f="level" data-v="uni" onclick="setFilter(this)">ปริญญาตรี · 3D</button>
    <span class="fcount" id="fcount">{total} / {total}</span>
  </div>
</div></div>

<div class="wrap" id="catalog">
{sections}
<div class="empty" id="empty">ไม่พบการทดลองที่ตรงกับตัวกรอง — ลองล้างตัวกรองหรือค้นคำอื่น</div>
</div>

<footer>© 2569 KP Science · <a href="index.html">หน้าหลัก</a> · <a href="library.html">Library</a> · ข้อมูล lab ทั้งหมดสร้างจาก <code>_admin/labs_data.py</code></footer>

<script>
const GROUPS={{{','.join(f'"{g[0]}":{[t for t in g[3]]}'.replace("'",'"') for g in GROUPS)}}};
const F={{topic:'all',group:null,level:'all'}};
function setFilter(btn){{
  const f=btn.dataset.f, v=btn.dataset.v;
  if(f==='group'){{ F.group=v; F.topic='all'; }} else if(f==='topic'){{ F.topic=v; F.group=null; }} else F.level=v;
  document.querySelectorAll('.fchip[data-f="topic"],.fchip[data-f="group"]').forEach(b=>b.classList.toggle('active',(F.group? (b.dataset.f==='group'&&b.dataset.v===F.group) : (b.dataset.f==='topic'&&b.dataset.v===F.topic))));
  document.querySelectorAll('.fchip[data-f="level"]').forEach(b=>b.classList.toggle('active',b.dataset.v===F.level));
  applyFilter();
  if(f==='group'||f==='topic'){{ const tgt = f==='group'? document.getElementById('g-'+v) : (v==='all'? null : document.getElementById('t-'+v)); if(tgt) tgt.scrollIntoView({{behavior:'smooth',block:'start'}}); }}
}}
function applyFilter(){{
  const q=(document.getElementById('q').value||'').trim().toLowerCase();
  let shown=0;
  document.querySelectorAll('.lab-card').forEach(c=>{{
    const okT = F.group ? GROUPS[F.group].includes(c.dataset.topic) : (F.topic==='all'||c.dataset.topic===F.topic);
    const okL = F.level==='all'||c.dataset.level===F.level;
    const okQ = !q || c.dataset.search.includes(q);
    const ok=okT&&okL&&okQ; c.style.display=ok?'':'none'; if(ok) shown++;
  }});
  document.querySelectorAll('.topic-section').forEach(s=>{{ const n=[...s.querySelectorAll('.lab-card')].filter(c=>c.style.display!=='none').length; s.style.display=n?'':'none'; s.querySelector('[data-count]').textContent=n+' การทดลอง'; }});
  document.querySelectorAll('.group-anchor').forEach(g=>{{ const gid=g.id.replace('g-',''); const n=[...document.querySelectorAll('.lab-card')].filter(c=>GROUPS[gid].includes(c.dataset.topic)&&c.style.display!=='none').length; g.style.display=n?'':'none'; g.querySelector('.ga-count').textContent=n+' การทดลอง'; }});
  document.getElementById('fcount').textContent=shown+' / {total}';
  document.getElementById('empty').classList.toggle('show',shown===0);
}}
// deep links: ?level=uni | ?topic=waves | ?group=mech | ?q=...
(function(){{
  const p=new URLSearchParams(location.search);
  if(p.get('level')){{ const b=document.querySelector('.fchip[data-f="level"][data-v="'+p.get('level')+'"]'); if(b) setFilter(b); }}
  if(p.get('topic')){{ const b=document.querySelector('.fchip[data-f="topic"][data-v="'+p.get('topic')+'"]'); if(b) setFilter(b); }}
  if(p.get('group')){{ const b=document.querySelector('.fchip[data-f="group"][data-v="'+p.get('group')+'"]'); if(b) setFilter(b); }}
  if(p.get('q')){{ document.getElementById('q').value=p.get('q'); applyFilter(); }}
}})();
</script>

<!-- KP Auth (Firebase) -->
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>
<script src="kp-auth.js"></script>
</body>
</html>
'''

def build_library_block():
    out='''  <!-- ═════ Virtual Lab (ทุกชุด · จัดตามบทเรียน สสวท.) — generated by _admin/build_virtual_lab.py ═════ -->
  <div class="lib-cat" data-cat="vlab" style="--cat-clr:var(--accent3)">
    <div class="lib-cat-header">
      <span class="lib-cat-icon">🧪</span>
      <div><span class="lib-cat-title">Virtual Physics Lab</span><span class="lib-cat-en">ทุกชุด (VPL 01 · 02 · 03) จัดตามบทเรียน — <a href="virtual-lab.html" style="color:var(--accent)">ดูแบบการ์ดพร้อมตัวกรอง →</a></span></div>
      <span class="lib-cat-count">%d files</span>
    </div>
''' % len(LABS)
    for t in TOPICS:
        labs=by_topic[t[0]]
        if not labs: continue
        out+=f'    <div class="lib-sub" id="lib-t-{t[0]}">\n      <div class="lib-sub-title">{t[1]} {esc(t[2])} · {esc(t[3])}</div>\n      <div class="lib-list">\n'
        for acc,href,num,title,desc,topic,level,series,tags in labs:
            out+=f'        <a data-locked="true" data-access="{acc}" href="{esc(href)}" class="lib-item"><span class="lib-item-dot"></span><span class="lib-item-name">{"Lab" if series=="vpl03" else "Exp"} {esc(num)}: {esc(title)} <span style="color:var(--muted);font-size:.72rem">· {esc(level)} · {SERIES[series][0]}</span></span><span class="lib-item-num">{esc(num)}</span><span class="lib-item-arr">→</span></a>\n'
        out+='      </div>\n    </div>\n'
    out+='  </div>\n\n'
    return out

if __name__=='__main__':
    open(os.path.join(BASE,'virtual-lab.html'),'w',encoding='utf-8').write(build_page())
    p=os.path.join(BASE,'library.html'); s=open(p,encoding='utf-8').read()
    start=s.find('<!-- ═════ Virtual Physics Lab 01'); 
    if start<0: start=s.find('<!-- ═════ Virtual Lab (ทุกชุด')
    if start<0: start=s.find('<div class="lib-cat" data-cat="vlab"')
    end=s.find('<!-- ═══════════════════════════════════════════════════════\n       🎬 DEMOS')
    assert start>0 and end>start, (start,end)
    s=s[:start]+build_library_block()+'\n'+s[end:]
    open(p,'w',encoding='utf-8').write(s)
    print('built virtual-lab.html (%d labs) + library.html lab block' % len(LABS))
    os.system('python3 "%s" virtual-lab.html' % os.path.join(BASE,'_admin','protect_new_file.py'))   # GA + topbar
