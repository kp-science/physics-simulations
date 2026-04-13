/**
 * ═══════════════════════════════════════════════════════════
 *  KP Science — Watermark Overlay Module v2
 *
 *  Usage: <script src="/_shared/watermark.js"></script>
 *
 *  - แสดงลายน้ำ "KP Science" บน canvas หลักของ simulation
 *  - เฉพาะ canvas แรกที่มองเห็น + ใหญ่พอ (≥400px กว้าง)
 *  - ใช้ CSS display size (ไม่ใช่ attribute size) → ไม่ล้น/เยื้อง
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
  var OPACITY       = 0.12;
  var ANGLE         = -Math.PI / 6;
  var MIN_WIDTH     = 400;   // ไม่แปะ canvas เล็กกว่า 400px
  var REFRESH_MS    = 3000;

  /* ── State ───────────────────────────────────────────── */
  var overlay   = null;   // { target, canvas }
  var hidden    = false;
  var timer     = null;

  /* ── Helpers ─────────────────────────────────────────── */

  function hasAccess() {
    try {
      var tier = localStorage.getItem(ACCESS_KEY);
      return tier && UNLOCK_TIERS.indexOf(tier.toLowerCase()) !== -1;
    } catch (e) { return false; }
  }

  /** หา canvas หลักของ simulation — ตัวแรกที่มองเห็นและกว้างพอ */
  function findMainCanvas() {
    var canvases = document.querySelectorAll('canvas:not([data-kp-watermark="1"])');
    for (var i = 0; i < canvases.length; i++) {
      var c = canvases[i];
      if (c.offsetWidth >= MIN_WIDTH && c.offsetHeight > 0) {
        return c;
      }
    }
    return null;
  }

  /** คำนวณ font size ตามขนาด canvas */
  function getFontSizes(w, h) {
    var dim = Math.min(w, h);
    var main = Math.max(24, Math.min(48, dim * 0.1));
    var sub  = Math.max(12, main * 0.38);
    return { main: main, sub: sub, gap: main * 0.6 };
  }

  /** วาดลายน้ำบน overlay canvas */
  function drawWatermark(oc) {
    var ctx = oc.getContext('2d');
    var cw  = oc.width;
    var ch  = oc.height;
    ctx.clearRect(0, 0, cw, ch);

    if (hidden || cw < MIN_WIDTH) return;

    var fs = getFontSizes(cw, ch);

    ctx.save();
    ctx.globalAlpha = OPACITY;
    ctx.textAlign   = 'center';
    ctx.fillStyle   = BRAND_COLOR;
    ctx.translate(cw / 2, ch / 2);
    ctx.rotate(ANGLE);
    ctx.font = 'bold ' + Math.round(fs.main) + 'px Sarabun, sans-serif';
    ctx.fillText('KP Science', 0, -fs.gap / 2);
    ctx.font = Math.round(fs.sub) + 'px Sarabun, sans-serif';
    ctx.fillText('Virtual Physics Lab', 0, fs.gap / 2 + fs.sub * 0.3);
    ctx.restore();
  }

  /** สร้าง / อัปเดต overlay canvas ซ้อนบน simulation canvas หลัก */
  function attachOverlay(simCanvas) {
    var parent = simCanvas.parentNode;
    if (!parent) return null;

    // ทำให้ parent เป็น relative
    var pos = getComputedStyle(parent).position;
    if (pos === 'static' || pos === '') {
      parent.style.position = 'relative';
    }

    // ใช้ CSS display size (offsetWidth/Height) ไม่ใช่ attribute size
    var dw = simCanvas.offsetWidth;
    var dh = simCanvas.offsetHeight;

    var oc = document.createElement('canvas');
    oc.dataset.kpWatermark = '1';
    oc.width  = dw;
    oc.height = dh;
    // ตั้ง CSS ให้ตรงกับ display size ของ canvas เป้าหมาย
    oc.style.cssText =
      'position:absolute;top:0;left:0;pointer-events:none;z-index:999;' +
      'width:' + dw + 'px;height:' + dh + 'px;' +
      'background:transparent !important;border:none !important;';

    parent.insertBefore(oc, simCanvas.nextSibling);
    drawWatermark(oc);

    return { target: simCanvas, canvas: oc };
  }

  /** Sync ขนาด overlay กับ canvas เป้าหมาย (กรณี resize/responsive) */
  function syncSize() {
    if (!overlay) return;
    var t  = overlay.target;
    var oc = overlay.canvas;
    var dw = t.offsetWidth;
    var dh = t.offsetHeight;

    // ถ้า target หายไป (ถูกลบ) ให้ลบ overlay ด้วย
    if (!document.body.contains(t)) {
      if (oc.parentNode) oc.parentNode.removeChild(oc);
      overlay = null;
      return;
    }

    // ถ้า target ซ่อน (เช่นสลับ tab) → ซ่อน overlay
    if (dw === 0 || dh === 0) {
      oc.style.display = 'none';
      return;
    }
    oc.style.display = '';

    // Sync ขนาด
    if (oc.width !== dw || oc.height !== dh) {
      oc.width  = dw;
      oc.height = dh;
      oc.style.width  = dw + 'px';
      oc.style.height = dh + 'px';
      drawWatermark(oc);
    }
  }

  /** Refresh — หา canvas ถ้ายังไม่มี, sync ขนาด */
  function refresh() {
    if (hasAccess()) { api.remove(); return; }

    if (!overlay) {
      var main = findMainCanvas();
      if (main) {
        overlay = attachOverlay(main);
      }
    }
    syncSize();
  }

  /* ── Public API ──────────────────────────────────────── */
  var api = {
    remove: function () {
      hidden = true;
      if (overlay) overlay.canvas.style.display = 'none';
    },
    show: function () {
      hidden = false;
      if (overlay) {
        overlay.canvas.style.display = '';
        drawWatermark(overlay.canvas);
      }
    },
    check: function () {
      if (hasAccess()) { api.remove(); }
      else             { api.show();   }
    }
  };

  window.KPWatermark = api;

  /* ── Init ────────────────────────────────────────────── */
  function init() {
    if (hasAccess()) { hidden = true; return; }

    var main = findMainCanvas();
    if (main) {
      overlay = attachOverlay(main);
    }
    // Re-check เป็นระยะ (canvas อาจโหลดทีหลัง, resize, tab switch)
    timer = setInterval(refresh, REFRESH_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // defer เล็กน้อย — ให้ canvas render ก่อน
    setTimeout(init, 300);
  }

  // ฟัง storage event (login/logout จากแท็บอื่น)
  window.addEventListener('storage', function (e) {
    if (e.key === ACCESS_KEY) { api.check(); }
  });

})();
