# -*- coding: utf-8 -*-
"""Shared HTML partials + the Ringba snippet slot."""

import config as C

# ============================================================================
# RINGBA SNIPPET
# ----------------------------------------------------------------------------
# Paste the EXACT snippet Ringba generates for your call tracking tag between
# the markers below (Ringba > Manage Campaigns > your campaign >
# Call Tracking Tags > Install Tag > copy the JavaScript).
#
# Ringba's own guidance, which this wiring respects:
#   * ONE snippet per page. Two campaigns on one page = unpredictable results.
#   * "Number to Replace" must be the number actually printed on the page,
#     i.e. config.PHONE_DISPLAY -> "(831) 532-6042".
#   * The script replaces every instance of that number regardless of
#     formatting, and re-renders it in the same pattern.
#   * If the campaign or publisher number is paused/deleted the snippet
#     returns a 404 and the fallback number stays on screen (still routed).
#
# Until you paste the real snippet, the fallback template below is used. It is
# Ringba's standard v2 loader shape with YOUR ids swapped in, plus the options
# this site needs (numberClass + callback). It is inert until you set
# RINGBA_TEMPLATE_TAG_ID in config.py.
# ============================================================================

RINGBA_SNIPPET = """
<!-- ===================== BEGIN RINGBA CALL TRACKING TAG =====================
     Replace this whole block with Ringba's generated snippet, unmodified.
     Keep exactly one snippet per page.
     =========================================================================== -->
<script>
(function(e,d) {
    //Ringba.com phone number tracking
    var ringba_com_tag = "__RINGBA_TAG_ID__";
    var _sc = d.getElementsByTagName('script'), _s = _sc[_sc.length - 1];
    e._rgba = e._rgba || { q: [] };
    e._rgba.q.push({
        tag: ringba_com_tag,
        numberClass: "dni",                 // elements Ringba renders the pool number into
        render: true,                       // Ringba writes the number itself
        cb: window.__fmpDniOnNumber,        // site-side hook: syncs tel: links + reports status
        script: _s
    });
    if (!(e._rgba.loading = !!e._rgba.loading)) {
        var sc = d.createElement('script'); sc.type = 'text/javascript'; sc.async = true;
        sc.src = '//js.callcdn.com/js_v2/min/ringba.com.js';
        var s = d.getElementsByTagName('script')[0]; s.parentNode.insertBefore(sc, s);
        e._rgba.loading = true;
    }
})(window,document);
</script>
<!-- ====================== END RINGBA CALL TRACKING TAG ======================= -->
"""


def ringba_snippet():
    return RINGBA_SNIPPET.replace("__RINGBA_TAG_ID__", C.RINGBA_TEMPLATE_TAG_ID)


# =============================================================== fragments ===

def phone_link(size="md", label=None, extra_class=""):
    """
    One canonical Ringba-ready phone element.

    Ringba replaces the text node holding PHONE_DISPLAY and re-renders it in
    the same pattern. dni.js keeps the href in sync with whatever ends up on
    screen, so tap-to-call always dials the number the visitor is looking at.
    """
    txt = label if label else C.PHONE_DISPLAY
    return (
        '<a class="dni-tel {sz} {ex}" href="tel:{tel}" data-fallback="{fb}"'
        ' data-ringba-number="true" aria-label="Call {brand} at {fb}">'
        '<span class="dni">{txt}</span></a>'
    ).format(sz=size, ex=extra_class, tel=C.PHONE_TEL, fb=C.PHONE_DISPLAY,
             brand=C.BRAND, txt=txt)


def disclosure(kind="short"):
    body = C.DISCLOSURE_SHORT if kind == "short" else C.DISCLOSURE_LONG
    return '<p class="disclosure"><span class="disclosure-flag">Referral service</span> ' + body + '</p>'


def nav(active=""):
    items = [
        ("home", "/", "Home"),
        ("how", "/how-it-works.html", "How it works"),
        ("cities", "/index.html#cities", "Cities"),
        ("about", "/about.html", "About"),
        ("contact", "/contact.html", "Contact"),
    ]
    lis = "".join(
        '<li><a href="{href}"{cls}>{label}</a></li>'.format(
            href=href, label=label,
            cls=' class="is-active" aria-current="page"' if key == active else "")
        for key, href, label in items)
    return lis


def header(active="", sub=""):
    return """
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="/">
      <img src="/img/favicon-32.png" width="32" height="32" alt="">
      <span class="brand-text">{brand}<em>{sub}</em></span>
    </a>
    <nav class="site-nav" aria-label="Main navigation"><ul>{nav}</ul></nav>
    <div class="head-cta">
      {phone}
      <span class="head-cta-note">Free referral &middot; talk to a local pro</span>
    </div>
  </div>
</header>
""".format(brand=C.BRAND, sub=sub, nav=nav(active), phone=phone_link("sm"))


def footer(city_groups, active_city=None):
    from cities import CITIES

    cols = []
    for county, cities in city_groups.items():
        if not cities:
            continue
        lis = "".join(
            '<li><a href="/cities/{slug}.html">{name}</a></li>'.format(
                slug=c["slug"], name=c["name"]) for c in cities)
        cols.append('<div class="f-col"><h3>{county}</h3><ul>{lis}</ul></div>'.format(
            county=county.replace(" County", " Co."), lis=lis))

    return """
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="f-col f-brand">
        <h3>{brand}</h3>
        <p>A free referral service that connects you with licensed local plumbing
           professionals across California's Central Coast. We are not a plumbing
           company and we do not perform plumbing work.</p>
        <p style="margin:12px 0">{phone}</p>
        <p class="foot-disclosure">{disclosure}</p>
      </div>
      <div class="f-cities">{cols}</div>
    </div>

    <div class="foot-nav">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/how-it-works.html">How it works</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
        <li><a href="/privacy-policy.html">Privacy policy</a></li>
        <li><a href="/terms.html">Terms of service</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
      </ul>
    </div>

    <div class="foot-legal">
      <p><strong>Disclosure:</strong> {long_disclosure}</p>
      <p>&copy; {year} {legal}. All rights reserved. Contractor licensing, insurance,
         pricing and workmanship are the sole responsibility of the independent plumbing
         professional you choose to hire. Nothing on this site is a guarantee of price,
         availability or response time.</p>
    </div>
  </div>
</footer>

<a class="sticky-call" href="tel:{tel}">
  <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z"/></svg>
  <span class="sticky-label">Call now</span>
  <span class="dni sticky-num">{phone_display}</span>
</a>
""".format(brand=C.BRAND, cols="".join(cols), disclosure=C.DISCLOSURE_SHORT,
           long_disclosure=C.DISCLOSURE_LONG, year="2026", legal=C.BRAND_LEGAL,
           tel=C.PHONE_TEL, phone_display=C.PHONE_DISPLAY, phone=phone_link("sm"))


def sticky_call_note():
    """Hidden duplicate of the display number so Ringba's text sweep has an
    extra instance to replace; kept out of the visual flow."""
    return ('<span class="dni dni-ghost" aria-hidden="true">' + C.PHONE_DISPLAY + '</span>')


# ================================================================== heads =====

def head(title, description, path, extra_schema="", extra_head="", robots="index,follow"):
    url = C.ORIGIN + "/" + path.lstrip("/") if path != "/" else C.ORIGIN + "/"
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{brand}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#0E2B45">
<link rel="icon" type="image/png" sizes="512x512" href="/img/favicon-512.png">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/css/site.css">
<script>
/* Defined inline BEFORE Ringba's snippet so the callback reference in the
   snippet is never undefined. Queued calls are replayed by /js/dni.js. */
window.__fmpDniQueue = [];
window.__fmpDniFallback = "{phone_display}";
window.__fmpDniOnNumber = function (n, t, f) {{ window.__fmpDniQueue.push([n, t, f]); }};
</script>
{ringba}
<script src="/js/dni.js" defer data-fallback="{phone_display}"></script>
{extra_head}
{schema}
</head>""".format(title=title, desc=description, robots=robots, url=url,
                 brand=C.BRAND, ringba=ringba_snippet(), extra_head=extra_head,
                 phone_display=C.PHONE_DISPLAY, schema=extra_schema)


def ld(obj):
    import json
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'


def page_end(extra_scripts=""):
    """Closing scripts, injected before </body>."""
    return "".join('<script src="%s" defer></script>' % src for src in extra_scripts)
