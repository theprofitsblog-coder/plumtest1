/* ==========================================================================
   DNI verification harness.

   Loads a real built page into jsdom, stubs out Ringba's remote loader (so no
   network call happens), then exercises every path dni.js has to handle:

     1. fallback stays put when Ringba never responds
     2. callback swap updates visible text AND every tel: href
     3. formatting is preserved for each punctuation pattern
     4. a callback that fires before dni.js parses is replayed from the queue
     5. stray plain-text instances of the old number are swept too

   Run:  node test/dni.test.js
   ========================================================================== */

const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.join(__dirname, "..", "public");
const dniSrc = fs.readFileSync(path.join(ROOT, "js/dni.js"), "utf8");
const FALLBACK = "(831) 532-6042";
const FALLBACK_DIGITS = "8315326042";

let pass = 0, fail = 0;
function ok(cond, label, extra) {
  if (cond) { pass++; console.log("  PASS  " + label); }
  else { fail++; console.log("  FAIL  " + label + (extra ? "  -> " + extra : "")); }
}

function loadPage(rel, url) {
  let html = fs.readFileSync(path.join(ROOT, rel), "utf8");
  // Neutralise Ringba's remote loader: jsdom would not fetch it anyway, but we
  // also do not want the stub tag id reaching anything.
  html = html.replace("sc.src = '//js.callcdn.com/js_v2/min/ringba.com.js';",
                      "sc.src = 'about:blank';");
  const dom = new JSDOM(html, {
    url: url || "https://example.test/" + rel,
    runScripts: "dangerously",
    pretendToBeVisual: true
  });
  return dom;
}

async function run(dom) {
  dom.window.eval(dniSrc);
  if (!dom.window.FMP_DNI) throw new Error("dni.js did not install");
  // dni.js defers boot() to DOMContentLoaded, exactly as it does in a browser
  await loaded(dom);
  return dom.window;
}

function loaded(dom) {
  const w = dom.window;
  if (w.document.readyState !== "loading") {
    return new Promise(r => setTimeout(r, 30));   // let the listener flush
  }
  return new Promise(r => {
    w.document.addEventListener("DOMContentLoaded", () => setTimeout(r, 30), { once: true });
    setTimeout(r, 4000);
  });
}

function dniTexts(w) {
  return Array.from(w.document.querySelectorAll(".dni"))
    .map(e => e.textContent.trim()).filter(Boolean);
}
function telHrefs(w) {
  return Array.from(w.document.querySelectorAll("a[href^='tel:']"))
    .map(a => a.getAttribute("href"));
}

// ---------------------------------------------------------------- tests ------
console.log("\n=== dni.js verification ===");

(async function main() {

  // 1. fallback untouched
  {
    const w = await run(loadPage("cities/salinas.html"));
    const t = dniTexts(w);
    ok(t.length >= 4, "page exposes >=4 .dni number slots (" + t.length + ")");
    ok(t.every(x => x.replace(/\D/g, "").slice(-10) === FALLBACK_DIGITS),
       "all slots show the fallback number before Ringba responds",
       JSON.stringify(t.slice(0, 4)));
    ok(telHrefs(w).every(h => h === "tel:+1" + FALLBACK_DIGITS),
       "all tel: hrefs point at the fallback");
    const st = w.FMP_DNI.state();
    ok(st.swapped === false && st.source === "fallback", "state reports fallback / not swapped");
    const n = w.document.querySelectorAll(".sticky-call").length;
    ok(n === 1, "exactly one sticky mobile call bar (" + n + ")");
}

  // 2. callback swap
  {
    const w = await run(loadPage("cities/santa-maria.html"));
    w.__fmpDniOnNumber("(415) 555-0199", "JStest123", true);
    const t = dniTexts(w);
    ok(t.every(x => x.replace(/\D/g, "").slice(-10) === "4155550199"),
       "every .dni slot swapped to the pool number", JSON.stringify(t.slice(0, 4)));
    ok(telHrefs(w).every(h => h === "tel:+14155550199"),
       "every tel: href re-pointed at the pool number",
       JSON.stringify([...new Set(telHrefs(w))]));
    ok(t[0] === "(415) 555-0199", "fallback punctuation pattern preserved", t[0]);
    const st = w.FMP_DNI.state();
    ok(st.swapped && st.cbFired && st.tagId === "JStest123",
       "state reports swapped, callback fired, tagId captured");
    const a = w.document.querySelector("[data-ringba-number]");
    ok(a && a.getAttribute("data-active-number") === "(415) 555-0199",
       "data-active-number attribute kept in sync");
    const body = w.document.body.textContent;
    ok(body.indexOf(FALLBACK_DIGITS) === -1 && body.indexOf("532-6042") === -1,
       "no stale fallback rendering left in visible text");
}

  // 3. formatting patterns
  {
    const w = await run(loadPage("index.html"));
    const cases = [
      ["4155550199", "(415) 555-0199"],
      ["+14155550199", "(415) 555-0199"],
      ["1 (415) 555-0199", "(415) 555-0199"],
      ["415.555.0199", "(415) 555-0199"]
    ];
    let allOk = true, detail = "";
    for (const [input, expected] of cases) {
      const got = w.FMP_DNI.format(w.FMP_DNI.digits(input), "(XXX) XXX-XXXX");
      if (got !== expected) { allOk = false; detail += input + "->" + got + " "; }
    }
    ok(allOk, "digits()/format() normalise all Ringba return patterns", detail);
}

  // 4. queued callback replay (Ringba can respond before dni.js parses)
  {
    const dom2 = new JSDOM(fs.readFileSync(path.join(ROOT, "cities/santa-cruz.html"), "utf8")
      .replace("sc.src = '//js.callcdn.com/js_v2/min/ringba.com.js';", "sc.src='about:blank';"),
      { url: "https://example.test/x", runScripts: "dangerously" });
    await loaded(dom2);                       // let the page's own inline stub run
    ok(typeof dom2.window.__fmpDniOnNumber === "function",
       "inline <head> stub defined __fmpDniOnNumber before Ringba's snippet");
    // simulate Ringba answering BEFORE dni.js has parsed: it hits the stub queue
    dom2.window.__fmpDniOnNumber("(650) 555-0142", "JSqueued", true);
    ok(Array.isArray(dom2.window.__fmpDniQueue) && dom2.window.__fmpDniQueue.length === 1,
       "stub buffered the early callback in the queue");
    const sc = dom2.window.document.createElement("script");
    sc.textContent = dniSrc;
    dom2.window.document.body.appendChild(sc);
    await new Promise(r => setTimeout(r, 80));   // let boot() run
    const w2 = dom2.window;
    const t = Array.from(w2.document.querySelectorAll(".dni")).map(e => e.textContent.trim());
    ok(t.every(x => x.replace(/\D/g, "").slice(-10) === "6505550142"),
       "queued callback replayed on boot", JSON.stringify(t.slice(0, 3)));
    const hrefs = Array.from(w2.document.querySelectorAll("a[href^='tel:']"))
      .map(a => a.getAttribute("href"));
    ok(hrefs.every(h => h === "tel:+16505550142"), "queued replay also fixed tel: hrefs");
}

  // 5. stray text sweep
  {
    const w = await run(loadPage("cities/monterey.html"));
    const p = w.document.createElement("p");
    p.textContent = "Or call 831-532-6042 or (831) 532-6042 any time.";
    p.className = "dni";
    w.document.body.appendChild(p);
    w.__fmpDniOnNumber("(925) 555-0177", "JSsweep", true);
    const txt = w.document.body.textContent;
    ok(txt.indexOf("831-532-6042") === -1 && txt.indexOf("(831) 532-6042") === -1,
       "stray plain-text renderings of the old number were swept",
       txt.match(/831[\s.\-)]*532[\s.\-]*6042/g) ? "leftover found" : "");
    ok(p.textContent.indexOf("(925) 555-0177") !== -1, "swept text uses the fallback pattern");
}

  // 6. every page: exactly one Ringba snippet, one sticky bar, disclosure present
  {
    const files = [];
    (function walk(d) {
      for (const e of fs.readdirSync(d, { withFileTypes: true })) {
        const p = path.join(d, e.name);
        if (e.isDirectory()) walk(p);
        else if (e.name.endsWith(".html")) files.push(p);
      }
    })(ROOT);
    let snippetOk = true, discOk = true, telOk = true, n = 0;
    for (const f of files) {
      const h = fs.readFileSync(f, "utf8");
      n++;
      if ((h.match(/var ringba_com_tag\s*=/g) || []).length !== 1) snippetOk = false;
      if ((h.match(/js\.callcdn\.com/g) || []).length !== 1) snippetOk = false;
      if (h.indexOf("Calls may be routed to a network of licensed local plumbing professionals.") === -1)
        discOk = false;
      if (h.indexOf('href="tel:+18315326042"') === -1) telOk = false;
    }
    ok(snippetOk, "exactly one Ringba snippet on all " + n + " pages");
    ok(discOk, "referral disclosure present on all " + n + " pages");
    ok(telOk, "tap-to-call fallback link present on all " + n + " pages");
}

console.log("\n  " + pass + " passed, " + fail + " failed");
console.log(fail ? "  STATUS: FAIL" : "  STATUS: PASS — swap, href sync, formatting and replay all work");
process.exit(fail ? 1 : 0);

})();
