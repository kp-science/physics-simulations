/**
 * ═══════════════════════════════════════════════════════════
 *  KP Science — Watermark Overlay Module
 *
 *  Usage: <script src="/_shared/watermark.js"></script>
 *
 *  - แสดงลายน้ำ "KP Science" บน canvas ทุกอัน (default)
 *  - ซ่อนลายน้ำเมื่อผู้ใช้มีสิทธิ์ (access tier)
 *
 *  API:
 *    KPWatermark.remove()   — ซ่อนลายน้ำทันที
 *    KPWatermark.show()     — แสดงลายน้ำ
 *    KPWatermark.check()    — ตรวจสิทธิ์จาก localStorage
 *
 *  Access control:
 *    localStorage.setItem('kp_access_tier', 'pro')  → ไม่แสดง
 *    localStorage.removeItem('kp_access_tier')       → แสดง
 * ═══════════════════════════════════════════════════════════
 */
;(function () {
  'use strict';

  /* ── Config ──────────────────────────────────────────── */
  var ACCESS_KEY    = 'kp_access_tier';
  var UNLOCK_TIERS  = ['pro', 'premium', 'admin'];
  var BRAND_COLOR   = '#818cf8';
  var OPACITY       = 0.07;
  var FONT_MAIN     = 'bold 48px Sarabun, sans-serif';
  var FONT_SUB      = '18px Sarabun, sans-serif';
  var ANGLE         = -Math.PI / 6;
  var REFRESH_MS    = 3000; // re-check ทุก 3 วินาที (กรณี canvas resize)

  /* ── State ───────────────────────────────────────────── */
  var overlays  = [];   // { wrapper, overlay }
  var hidden    = false;
  var timer     = null;

  /* ── Helpers ─────────────────────────────────────────── */

  /** ตรวจสิทธิ์จาก localStorage */
  function hasAccess() {
    try {
      var tier = localStorage.getItem(ACCESS_KEY);
      return tier && UNLOCK_TIERS.indexOf(tier.toLowerCase()) !== -1;
    } catch (e) { return false; }
  }

  /** วาดลายน้ำบน overlay canvas */
  function drawWatermark(oc) {
    var ctx = oc.getContext('2d');
    var cw  = oc.width;
    var ch  = oc.height;
    ctx.clearRect(0, 0, cw, ch);

    if (hidden) return;

    ctx.save();
    ctx.globalAlpha = OPACITY;
    ctx.font        = FONT_MAIN;
    ctx.textAlign   = 'center';
    ctx.fillStyle   = BRAND_COLOR;
    ctx.translate(cw / 2, ch / 2);
    ctx.rotate(ANGLE);
    ctx.fillText('KP Science', 0, -10);
    ctx.font = FONT_SUB;
    ctx.fillText('Virtual Physics Lab', 0, 25);
    ctx.restore();
  }

  /** สร้าง overlay canvas ซ้อนบน simulation canvas */
  function attachOverlay(simCanvas) {
    // ข้ามถ้าเป็น overlay ของเราเอง
    if (simCanvas.dataset.kpWatermark === '1') return null;

    var parent = simCanvas.parentNode;
    if (!parent) return null;

    // ทำให้ parent เป็น relative (ถ้ายังไม่ใช่)
    var pos = getComputedStyle(parent).position;
    if (pos === 'static' || pos === '') {
      parent.style.position = 'relative';
    }

    var oc  = document.createElement('canvas');
    oc.dataset.kpWatermark = '1';
    oc.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none;z-index:999;';
    oc.width  = simCanvas.width  || simCanvas.offsetWidth  || 800;
    oc.height = simCanvas.height || simCanvas.offsetHeight || 500;

    parent.insertBefore(oc, simCanvas.nextSibling);
    drawWatermark(oc);

    return { target: simCanvas, overlay: oc };
  }

  /** สแกน canvas ทั้งหมดในหน้า แล้วแปะ overlay */
  function scan() {
    var canvases = document.querySelectorAll('canvas:not([data-kp-watermark="1"])');
    for (var i = 0; i < canvases.length; i++) {
      var c = canvases[i];
      // ข้ามถ้ามี overlay แล้ว
      var already = false;
      for (var j = 0; j < overlays.length; j++) {
        if (overlays[j].target === c) { already = true; break; }
      }
      if (already) continue;
      var o = attachOverlay(c);
      if (o) overlays.push(o);
    }
  }

  /** Sync ขนาด overlay กับ canvas เป้าหมาย */
  function syncSizes() {
    for (var i = 0; i < overlays.length; i++) {
      var o  = overlays[i];
      var tw = o.target.width  || o.target.offsetWidth;
      var th = o.target.height || o.target.offsetHeight;
      if (o.overlay.width !== tw || o.overlay.height !== th) {
        o.overlay.width  = tw;
        o.overlay.height = th;
        drawWatermark(o.overlay);
      }
    }
  }

  /** Refresh loop — ตรวจ canvas ใหม่ + sync ขนาด */
  function refresh() {
    if (hasAccess()) { api.remove(); return; }
    scan();
    syncSizes();
  }

  /* ── Public API ──────────────────────────────────────── */
  var api = {
    /** ซ่อนลายน้ำทันที */
    remove: function () {
      hidden = true;
      for (var i = 0; i < overlays.length; i++) {
        overlays[i].overlay.style.display = 'none';
      }
    },

    /** แสดงลายน้ำ */
    show: function () {
      hidden = false;
      for (var i = 0; i < overlays.length; i++) {
        overlays[i].overlay.style.display = '';
        drawWatermark(overlays[i].overlay);
      }
    },

    /** ตรวจสิทธิ์แล้วซ่อน/แสดงอัตโนมัติ */
    check: function () {
      if (hasAccess()) { api.remove(); }
      else             { api.show();   }
    }
  };

  window.KPWatermark = api;

  /* ── Init ────────────────────────────────────────────── */
  function init() {
    if (hasAccess()) { hidden = true; return; }
    scan();
    // Re-check เป็นระยะ (canvas อาจโหลดทีหลัง หรือ resize)
    timer = setInterval(refresh, REFRESH_MS);
  }

  // รอ DOM พร้อม
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ฟัง storage event (login/logout จากแท็บอื่น)
  window.addEventListener('storage', function (e) {
    if (e.key === ACCESS_KEY) { api.check(); }
  });

})();
