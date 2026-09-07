/* ============================================================================
   FindMyPlumber — Ringba Dynamic Number Insertion adapter
   ----------------------------------------------------------------------------
   WHAT THIS FILE DOES (and deliberately does NOT do)

   Ringba's own tracking tag is responsible for fetching a pool number and
   rendering it into the page. It replaces every instance of the configured
   "Number to Replace" — in any punctuation pattern — and re-renders it in the
   same pattern. See src/templates.py for the snippet slot.

   This adapter only does the three things Ringba's renderer is not guaranteed
   to do on its own:

     1. Sync the href of every <a href="tel:..."> so tap-to-call always dials
        the number the visitor is actually looking at. (Critical on mobile:
        if the text swaps but the href does not, the call goes to the wrong
        number and the conversion is not attributed.)
     2. Sync data-ringba-number / data-active-number attributes.
     3. Report status, so you can prove the swap happened before spending a
        dollar on traffic.

   It never fabricates a number. If Ringba does not respond, the fallback
   number from config.py stays on screen and still routes.

   ---------------------------------------------------------------------------
   VERIFICATION MODES (use before going live)

     /                       normal
     /?dnitest=mock          simulates a pool number (999) 867-5309 without
                             contacting Ringba — proves the swap, the tel:
                             sync and the formatting logic all work
     /?dnitest=report        shows the diagnostic panel (also auto-shown in
                             mock mode). Checks: snippet present, tag id set,
                             instances found, number changed vs fallback.
   ============================================================================ */

(function () {
  "use strict";

  // Idempotency guard: if this file is somehow evaluated twice on the same page
  // (a build mistake, or a tag manager injecting it again), the first instance
  // wins. Without this, the second boot() resets state and drops the number.
  if (window.FMP_DNI) { return; }

  // The fallback number is what stays on screen if Ringba never responds, and it
  // is also the "old" number we sweep the DOM for. Discover it defensively:
  //   1. the data-fallback attribute on our own <script> tag
  //   2. window.__fmpDniFallback, set by the inline stub in <head>
  //   3. the most common rendering found inside a .dni element
  var _cs = document.currentScript;
  var FALLBACK =
    (_cs && _cs.getAttribute("data-fallback")) ||
    window.__fmpDniFallback ||
    (function () {
      var el = document.querySelector(".dni");
      return el ? el.textContent.trim() : "";
    })();
  if (!FALLBACK || FALLBACK.replace(/\D+/g, "").length < 10) {
    // Without a known fallback we cannot tell an old number from a new one, so
    // refuse to rewrite anything rather than corrupt the page.
    if (window.console && console.error) {
      console.error("[dni] no fallback number could be determined; DNI disabled.");
    }
    window.FMP_DNI = { state: function () { return { error: "no-fallback" }; },
                       digits: function (x) { return String(x || "").replace(/\D+/g, ""); },
                       format: function (x) { return x; },
                       applyNumber: function () { return false; },
                       report: function () {}, drainQueue: function () { return false; } };
    return;
  }
  var state = {
    fallback: FALLBACK,
    fallbackDigits: "",
    active: FALLBACK,
    activeDigits: "",
    swapped: false,
    source: "fallback",
    cbFired: false,
    cbFirstTime: null,
    mock: false,
    startedAt: Date.now()
  };

  // --------------------------------------------------------------- helpers --

  function digits(s) {
    if (!s) return "";
    var d = String(s).replace(/\D+/g, "");
    if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
    return d;
  }

  function fmt(d, pattern) {
    if (!d || d.length < 10) return pattern || d || "";
    d = d.slice(-10);
    // Re-render in the same pattern as the fallback, matching Ringba's
    // documented behaviour of preserving the replaced number's format.
    var p = pattern || "(XXX) XXX-XXXX";
    var i = 0;
    return p.replace(/X/g, function () { return d.charAt(i++) || ""; });
  }

  function patternOf(s) {
    return String(s || "").replace(/\d/g, "X");
  }

  function telHref(d) {
    return "tel:+1" + d.slice(-10);
  }

  function findPhoneNodes(root) {
    var out = [];
    var all = (root || document).querySelectorAll(
      "a[href^='tel:'], [data-ringba-number], .dni, .dni-tel"
    );
    for (var i = 0; i < all.length; i++) out.push(all[i]);
    return out;
  }

  // Sweep visible text + attributes for any rendering of the OLD number and
  // rewrite it to the NEW one. This is the safety net for hrefs and for
  // attributes Ringba's renderer does not touch.
  function rewrite(oldDigits, newDigits, newDisplay) {
    if (!oldDigits || !newDigits || oldDigits === newDigits) return 0;
    var variants = buildVariants(oldDigits);
    var n = 0;

    findPhoneNodes().forEach(function (el) {
      if (el.href && el.getAttribute("href").indexOf("tel:") === 0) {
        var want = telHref(newDigits);
        if (el.getAttribute("href") !== want) {
          el.setAttribute("href", want);
          n++;
        }
      }
      if (el.getAttribute("data-ringba-number")) {
        el.setAttribute("data-active-number", newDisplay);
      }
    });

    // Text nodes anywhere in the document that still show an old rendering.
    try {
      var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
      var node, hits = [];
      while ((node = walker.nextNode())) {
        var v = node.nodeValue;
        if (!v) continue;
        for (var k = 0; k < variants.length; k++) {
          if (v.indexOf(variants[k]) !== -1) { hits.push(node); break; }
        }
      }
      hits.forEach(function (tn) {
        var before = tn.nodeValue;
        var after = before;
        variants.forEach(function (v) {
          after = after.split(v).join(newDisplay);
        });
        if (after !== before) { tn.nodeValue = after; n++; }
      });
    } catch (e) { /* non-fatal */ }

    return n;
  }

  function buildVariants(d) {
    d = d.slice(-10);
    if (d.length < 10) return [d];
    var a = d.slice(0, 3), b = d.slice(3, 6), c = d.slice(6);
    return [
      "(" + a + ") " + b + "-" + c,
      a + "-" + b + "-" + c,
      a + "." + b + "." + c,
      a + " " + b + " " + c,
      "+1" + a + b + c,
      "1" + a + b + c,
      a + b + c
    ];
  }

  // --------------------------------------------------------- apply a number --

  function applyNumber(raw, source, tagId, firstTime) {
    var d = digits(raw);
    if (d.length < 10) return false;

    var display = fmt(d, patternOf(state.fallback) || "(XXX) XXX-XXXX");
    var changed = rewrite(state.activeDigits || state.fallbackDigits, d, display);

    state.active = display;
    state.activeDigits = d;
    state.swapped = d !== state.fallbackDigits;
    state.source = source;
    state.changedNodes = changed;
    if (typeof firstTime !== "undefined") state.cbFirstTime = !!firstTime;
    if (typeof tagId !== "undefined") state.tagId = tagId;

    emit();
    return true;
  }

  function emit() {
    try {
      document.dispatchEvent(new CustomEvent("fmp:dnichange", { detail: snapshot() }));
    } catch (e) {}
  }

  function snapshot() {
    return {
      fallback: state.fallback,
      active: state.active,
      swapped: state.swapped,
      source: state.source,
      cbFired: state.cbFired,
      tagId: state.tagId || "",
      mock: state.mock,
      nodes: findPhoneNodes().length,
      ms: Date.now() - state.startedAt
    };
  }

  // ------------------------------------------- Ringba callback (public API) --
  // The <head> of every page defines __fmpDniOnNumber as a QUEUE stub before
  // Ringba's snippet runs, so the snippet never captures `undefined`. This
  // replaces the stub with the live handler, and drains anything the stub
  // buffered in the meantime.
  function liveHandler(number, tagId, firstTime) {
    state.cbFired = true;
    return applyNumber(number, "ringba-callback", tagId, firstTime);
  }

  function drainQueue() {
    var q = window.__fmpDniQueue;
    if (!q || !q.length) return false;
    window.__fmpDniQueue = [];
    var done = false;
    for (var i = 0; i < q.length; i++) {
      if (liveHandler(q[i][0], q[i][1], q[i][2])) done = true;
    }
    return done;
  }

  window.__fmpDniOnNumber = liveHandler;

  // Back-compat: some Ringba tag generations expose GotNumber instead.
  window.GotNumber = function (number, tagId, firstTime) {
    state.cbFired = true;
    applyNumber(number, "ringba-GotNumber", tagId, firstTime);
  };

  // --------------------------------------------------------------- diagnostics
  function snippetPresent() {
    var s = document.getElementsByTagName("script");
    for (var i = 0; i < s.length; i++) {
      var t = s[i].textContent || "";
      if (t.indexOf("ringba_com_tag") !== -1 || t.indexOf("js.callcdn.com") !== -1) return t;
    }
    return "";
  }

  function tagIdFromSnippet(txt) {
    var m = txt && txt.match(/ringba_com_tag\s*=\s*["']([^"']+)["']/);
    return m ? m[1] : "";
  }

  function renderReport() {
    if (document.getElementById("dni-report")) return;
    var snip = snippetPresent();
    var tag = tagIdFromSnippet(snip);
    var tagOk = tag && tag.indexOf("PASTE_YOUR") !== 0;
    var instances = document.querySelectorAll(".dni").length;
    var hrefs = document.querySelectorAll("a[href^='tel:']").length;
    var hrefMatches = 0;
    document.querySelectorAll("a[href^='tel:']").forEach(function (a) {
      if (digits(a.getAttribute("href")) === state.activeDigits) hrefMatches++;
    });

    function pill(ok, yes, no) {
      return '<span class="pill ' + (ok ? "ok" : "bad") + '">' + (ok ? yes : no) + "</span>";
    }

    var rows = [
      ["Ringba snippet in DOM", pill(!!snip, "found", "missing")],
      ["ringba_com_tag configured", tagOk ? pill(true, tag) : pill(false, tag || "not set")],
      ["Callback fired", pill(state.cbFired, "yes", "no")],
      ["Number on page", "<strong>" + state.active + "</strong>"],
      ["Changed vs fallback", pill(state.swapped, "SWAPPED", "fallback in use")],
      ["Number source", state.source],
      [".dni instances", instances],
      ["tel: links in sync", pill(hrefs === hrefMatches, hrefMatches + "/" + hrefs, hrefMatches + "/" + hrefs)],
      ["Mock mode", pill(!state.mock, "off", "ON")]
    ];

    var box = document.createElement("div");
    box.className = "dni-report";
    box.id = "dni-report";
    box.setAttribute("role", "status");
    box.innerHTML =
      "<h4>Ringba DNI self-test</h4><table><tbody>" +
      rows.map(function (r) { return "<tr><th>" + r[0] + "</th><td>" + r[1] + "</td></tr>"; }).join("") +
      "</tbody></table>" +
      '<p class="small muted" style="margin:.6em 0 0">Fallback ' + state.fallback +
      '. If &ldquo;Number on page&rdquo; equals the fallback, Ringba did not return a pool number ' +
      '&mdash; check that the campaign and publisher number are both active.</p>' +
      '<button type="button" id="dni-report-close">Close</button>';
    document.body.appendChild(box);
    var btn = document.getElementById("dni-report-close");
    if (btn) btn.addEventListener("click", function () { box.parentNode.removeChild(box); });
  }

  // ------------------------------------------------------------------- boot --
  function boot() {
    state.fallbackDigits = digits(FALLBACK);
    state.activeDigits = state.fallbackDigits;

    // Replay any Ringba callback that fired before this file parsed.
    drainQueue();

    // Adopt whatever Ringba already rendered before this script ran.
    var first = document.querySelector(".dni");
    if (first) {
      var shown = digits(first.textContent);
      if (shown.length >= 10 && shown !== state.fallbackDigits) {
        applyNumber(shown, "already-rendered");
      }
    }

    var q = new URLSearchParams(location.search);
    var mode = (q.get("dnitest") || "").toLowerCase();

    if (mode === "mock") {
      state.mock = true;
      // Fires after the real Ringba loader would have had time to respond,
      // so a genuine pool number wins if one arrives first.
      window.setTimeout(function () {
        if (!state.cbFired && !state.swapped) {
          applyNumber("(999) 867-5309", "mock-selftest");
          renderReport();
        }
      }, 2500);
    }

    if (mode === "report" || mode === "mock") {
      window.setTimeout(renderReport, mode === "mock" ? 2700 : 600);
    }

    // Late safety nets. Ringba's response is asynchronous and can land at any
    // point, so for the first few seconds re-check both the queue and whatever
    // is actually rendered on the page.
    var ticks = 0;
    var timer = window.setInterval(function () {
      ticks++;
      drainQueue();
      var el = document.querySelector(".dni");
      if (el) {
        var d = digits(el.textContent);
        if (d.length >= 10 && d !== state.activeDigits) applyNumber(d, "late-scan");
      }
      if (ticks >= 20) window.clearInterval(timer);   // ~10s of coverage
    }, 500);

    emit();
  }

  window.FMP_DNI = {
    state: snapshot,
    drainQueue: drainQueue,
    applyNumber: function (n) { return applyNumber(n, "manual"); },
    report: renderReport,
    digits: digits,
    format: fmt
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
