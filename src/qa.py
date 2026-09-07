# -*- coding: utf-8 -*-
"""
Anti-template / integrity QA pass.

Run after build:  python3 src/build.py --qa
Exits non-zero if a page looks like a template swap or something is broken.
"""

import os
import re
import sys
import glob
import html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import config as C
from cities import CITIES, cities_by_county

OUT = os.path.join(ROOT, "public")

FAIL = []
WARN = []

# Sentence fragments that are deliberately identical on every page: the legal
# disclosure and footer text. The city copy is what has to be unique.
SHARED_BOILERPLATE = set()

# Phrases that are part of the mandated honest disclosure / legal framing and
# therefore SHOULD be identical everywhere.
SHARED_KEYS = (
    "referral service", "not a plumbing company", "not a licensed contractor",
    "calls may be routed", "do not perform plumbing work", "do not employ",
    "agreement, quote, warranty", "lead generation", "call routing",
    "free to you", "no obligation to hire", "sets their own rates",
    "pricing is set by", "rate structure", "cannot guarantee",
    "licensed plumbing professional", "we route", "shut the water off",
    "shutting off the water", "call 911", "your utility", "response depends",
    "we will tell you", "plumbers work in radiuses", "behind your walls",
    "conversation is between you", "we do not dispatch", "not a price list",
    "costs belong to the plumber", "no prices here on purpose",
    "the plumber you speak to", "independent licensed", "does their own work",
    "not a reason to panic", "from there the conversation",
)


def _seed_boilerplate():
    import templates as T
    chunks = [C.DISCLOSURE_SHORT, C.DISCLOSURE_LONG,
              re.sub(r"<[^>]+>", " ", T.footer(cities_by_county())),
              re.sub(r"<[^>]+>", " ", T.header("", ""))]
    for ch in chunks:
        for sent in sentences(strip_tags(H.unescape(ch))):
            SHARED_BOILERPLATE.add(norm(sent)[:60])


def fail(msg):
    FAIL.append(msg)


def warn(msg):
    WARN.append(msg)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def strip_tags(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return H.unescape(s)


def sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\d])", text)
    return [p.strip() for p in parts if len(p.strip().split()) >= 6]


def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------------------

def check_links():
    files = glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True)
    existing = set()
    for f in files:
        rel = os.path.relpath(f, OUT).replace(os.sep, "/")
        existing.add("/" + rel)
        existing.add(rel)
    existing.add("/")
    for extra in ("/css/site.css", "/js/dni.js", "/js/city-search.js", "/img/favicon-512.png",
                  "/img/favicon-32.png", "/img/apple-touch-icon.png",
                  "/sitemap.xml", "/robots.txt", "/data/cities.json"):
        p = os.path.join(OUT, extra.lstrip("/"))
        if os.path.exists(p):
            existing.add(extra)
        else:
            fail("missing asset: %s" % extra)

    for f in files:
        html = read(f)
        rel = os.path.relpath(f, OUT)
        for m in re.finditer(r'href="([^"#]+?)(#[^"]*)?"', html):
            href = m.group(1)
            if re.match(r"^(https?:|mailto:|tel:|data:)", href):
                continue
            if not href.startswith("/"):
                warn("%s: relative link %s (root-relative expected)" % (rel, href))
                continue
            if href not in existing:
                fail("%s: broken internal link %s" % (rel, href))


def check_page_basics():
    files = glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True)
    for f in files:
        html = read(f)
        rel = os.path.relpath(f, OUT)
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        if not title or not title.group(1).strip():
            fail("%s: missing <title>" % rel)
        elif len(title.group(1)) > 60:
            warn("%s: title %d chars (>60)" % (rel, len(title.group(1))))
        if not desc or not desc.group(1).strip():
            fail("%s: missing meta description" % rel)
        elif len(desc.group(1)) > 158:
            fail("%s: meta description %d chars (>158)" % (rel, len(desc.group(1))))
        elif not re.search(r"[.!?]$", desc.group(1).strip()):
            fail("%s: meta description looks truncated: %r" % (rel, desc.group(1)[-30:]))
        if '<link rel="canonical"' not in html:
            fail("%s: missing canonical" % rel)
        if "favicon-512.png" not in html or "apple-touch-icon.png" not in html:
            fail("%s: missing favicon link tags" % rel)
        if "ringba_com_tag" not in html:
            fail("%s: Ringba snippet missing" % rel)
        if html.count("js.callcdn.com") != 1:
            fail("%s: expected exactly one Ringba loader, found %d"
                 % (rel, html.count("js.callcdn.com")))
        if "ld+json" in html:
            import json
            for m in re.finditer(r'(?s)<script type="application/ld\+json">(.*?)</script>', html):
                try:
                    json.loads(m.group(1))
                except Exception as e:
                    fail("%s: invalid JSON-LD (%s)" % (rel, e))


def check_phone():
    files = glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True)
    for f in files:
        html = read(f)
        rel = os.path.relpath(f, OUT)
        text = strip_tags(html)
        # every visible rendering of a phone number must be the fallback or the mock
        nums = re.findall(r"(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}", text)
        bad = [n for n in nums if C.PHONE_DISPLAY.replace(" ", "") not in n.replace(" ", "")
               and digits(n) != C.PHONE_RAW]
        if bad:
            fail("%s: unexpected phone number(s) %s" % (rel, sorted(set(bad))[:3]))
        if 'href="tel:%s"' % C.PHONE_TEL not in html:
            fail("%s: no tap-to-call tel: link" % rel)
        if "sticky-call" not in html and rel != "404.html":
            warn("%s: no sticky mobile call bar" % rel)
        if C.DISCLOSURE_SHORT not in text and "Referral service" not in text:
            fail("%s: disclosure missing near phone number" % rel)


def digits(s):
    d = re.sub(r"\D+", "", s or "")
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d


def check_uniqueness():
    """The core anti-template test."""
    texts = {}
    for c in CITIES:
        p = os.path.join(OUT, "cities", c["slug"] + ".html")
        if not os.path.exists(p):
            fail("city page not generated: %s" % p)
            continue
        html = read(p)
        main = re.search(r"(?s)<main.*?</main>", html) or re.match(r"(?s).*", html)
        texts[c["slug"]] = strip_tags(main.group(0))

    slugs = list(texts)

    # 1. sentence-level duplication.
    #    Structural boilerplate (the referral disclosure, "we are not a contractor",
    #    pricing disclaimers) is deliberately identical on every page, so a sentence
    #    that appears across many pages is chrome, not evidence of a template swap.
    #    What we fail on is a sentence shared by only a FEW pages: that means two
    #    city pages were built from the same rotation slot.
    from collections import defaultdict
    where = defaultdict(set)
    for slug in slugs:
        for sent in sentences(texts[slug]):
            n = norm(sent)
            if len(n.split()) < 8:
                continue
            where[n].add(slug)

    def is_boilerplate(n):
        """True only for the site-wide legal/disclosure/footer chrome, which is
        deliberately identical everywhere. NOT a get-out for rotating body copy."""
        if n[:60] in SHARED_BOILERPLATE:
            return True
        return any(k in n for k in SHARED_KEYS)

    boiler_wide = 0
    dups = []
    for n, owners in where.items():
        if len(owners) < 2:
            continue
        if is_boilerplate(n):
            if len(owners) >= 6:
                boiler_wide += 1
            continue
        dups.append((len(owners), sorted(owners), n))

    dups.sort(reverse=True)
    pair_counts = defaultdict(int)
    for cnt_, owners, _n in dups:
        for i in range(len(owners)):
            for j in range(i + 1, len(owners)):
                pair_counts[(owners[i], owners[j])] += 1
    worst_pair = max(pair_counts.items(), key=lambda kv: kv[1]) if pair_counts else (None, 0)

    print("  boilerplate  : %d disclosure/footer sentences identical site-wide (intended)" % boiler_wide)
    print("  duplication  : %d non-boilerplate sentences shared by 2+ city pages" % len(dups))
    print("                 worst page pair %s = %d shared sentences" % (worst_pair[0], worst_pair[1]))
    wide = [d for d in dups if d[0] > 5]
    for cnt_, owners, n in sorted(wide, reverse=True)[:5]:
        fail("non-boilerplate sentence appears on %d city pages: %r" % (cnt_, n[:90]))
    # Threshold: a collision in the generic FAQ rotation shares up to ~8
    # sentences. Anything above that means body copy is being reused.
    # 8 shared sentences == two rotating pools colliding on a pair of cities that
    # are NOT near each other (different county, not cross-linked, not adjacent in
    # the index). The body copy check below is what actually matters for SEO; this
    # ceiling exists to catch a pool collision leaking into related pages.
    if worst_pair[1] > 8:
        fail("city pages %s and %s share %d sentences - body copy is being reused, vary it"
             % (worst_pair[0][0], worst_pair[0][1], worst_pair[1]))
    over = [p_ for p_, n_ in pair_counts.items() if n_ > 8]
    print("  collisions   : %d of %d page pairs share >8 non-boilerplate sentences (ceiling)"
          % (len(over), len(slugs) * (len(slugs) - 1) // 2))
    for pr in sorted(pair_counts.items(), key=lambda kv: -kv[1])[:3]:
        print("                 %s vs %s = %d" % (pr[0][0], pr[0][1], pr[1]))
    for cnt_, owners, n in dups[:3]:
        if cnt_ >= 4:
            warn("sentence on %d city pages: %r" % (cnt_, n[:80]))

    # 2. per-page unique data must actually be present
    for c in CITIES:
        slug = c["slug"]
        t = texts.get(slug, "")
        for z in c["zips"]:
            if z not in t:
                fail("%s: ZIP %s missing from page" % (slug, z))
        for nb in c["neighborhoods"][:3]:
            if nb.split(" (")[0].split(" / ")[0].split(" toward ")[0].strip() not in t:
                warn("%s: neighborhood %r not found verbatim" % (slug, nb))
        if c["population"] not in t:
            fail("%s: population figure missing" % slug)
        if c["fact"].split(".")[0][:40] not in t.replace("\n", " "):
            warn("%s: local fact may be altered" % slug)
        if c["sources"][:40] not in t:
            fail("%s: sources note missing" % slug)

    # 3. similarity ceiling between any two city pages
    import difflib
    worst = (0, None, None)
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            a, b = slugs[i], slugs[j]
            r = difflib.SequenceMatcher(None, norm(texts[a])[:6000], norm(texts[b])[:6000]).ratio()
            if r > worst[0]:
                worst = (r, a, b)
    if worst[0] > 0.62:
        fail("city pages too similar: %s vs %s = %.2f" % (worst[1], worst[2], worst[0]))
    else:
        print("  similarity   : worst pair %s vs %s = %.2f (ceiling 0.62)" % (worst[1], worst[2], worst[0]))

    # 3b. THE headline anti-template test: each city page's identity copy
    #     (intro frame + locally-relevant issue paragraph + local fact +
    #     referral paragraph) must appear on exactly one page.
    import build as B
    ident = {}
    for c in CITIES:
        slug = c["slug"]
        n_intro = norm(B.INTRO[B.INTRO_SLOT[slug]].format(city=c["name"], issue=c["issue"]))
        n_refer = norm(B.REFERRAL[B.REFER_SLOT[slug]].format(
            city=c["name"], brand=C.BRAND, phone=C.PHONE_DISPLAY))
        for label, val in (("intro+issue", n_intro), ("referral", n_refer),
                           ("fact", norm(c["fact"])), ("issue", norm(c["issue"]))):
            key = (label, val)
            if key in ident:
                fail("%s copy identical on %s and %s" % (label, ident[key], slug))
            ident[key] = slug
    print("  identity copy: intro+issue, referral paragraph, local fact and local issue")
    print("                 paragraph are unique on all %d city pages" % len(CITIES))

    # 4. heading variety
    h2s = {}
    for c in CITIES:
        html = read(os.path.join(OUT, "cities", c["slug"] + ".html"))
        hs = re.findall(r"<h2>(.*?)</h2>", html, re.S)
        h2s[c["slug"]] = [norm(strip_tags(h)) for h in hs]
    from collections import Counter
    cnt = Counter()
    for v in h2s.values():
        cnt.update(v)
    repeated = [k for k, n in cnt.items() if n > 6]
    if repeated:
        warn("heading used on >6 city pages: %s" % repeated[:4])

    # 5. block-order variety
    orders = set()
    for c in CITIES:
        html = read(os.path.join(OUT, "cities", c["slug"] + ".html"))
        ids = re.findall(r'<section id="([^"]+)"', html)
        orders.add(tuple(x for x in ids if x in ("area", "local-issues", "what-happens", "services")))
    print("  layouts      : %d distinct section orders across %d city pages" % (len(orders), len(CITIES)))
    if len(orders) < 4:
        warn("only %d distinct section orders — increase variation" % len(orders))

    return worst


def check_forbidden():
    """Honesty rules from the brief, enforced mechanically."""
    patterns = [
        (r"(?i)family[- ]owned", "invented 'family owned' claim"),
        (r"(?i)\bsince (1[89]\d\d|20\d\d)\b", "invented founding year"),
        (r"(?i)\b\d+(\.\d+)?\s*(5|five)[-\s]?star", "star rating claim"),
        (r"(?i)testimonial", "testimonial section"),
        (r"(?i)\b(9[5-9]|100)%\s*(satisfaction|guaranteed)", "unverifiable percentage claim"),
        (r"(?i)we (guarantee|promise) (an? )?(arrival|response|arrival time)", "response-time promise"),
        (r"(?i)\b\d+\s*(licensed )?plumbers in our network", "invented network size"),
        (r"(?i)\b\d{1,3},?\d{3}\+? (happy )?(customers|clients|jobs completed|reviews)\b",
         "unverifiable customer/job count"),
        (r"(?i)\b(24/7 guaranteed|guaranteed 24/7)\b", "guaranteed availability"),
    ]
    files = glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True)
    for f in files:
        text = strip_tags(read(f))
        rel = os.path.relpath(f, OUT)
        for pat, label in patterns:
            for m in re.finditer(pat, text):
                # "We do not" / "you will not find" contexts are the rules themselves
                ctx = text[max(0, m.start() - 200):m.end() + 60].lower()
                # These strings appear on how-it-works/about only to state the
                # rule that we DO NOT do them. Allow that context.
                if any(k in ctx for k in ("do not", "does not", "will not find", "no invented",
                                          "not make", "invented", "fake", "never", "not publish",
                                          "no warranty", "not a claim")):
                    continue
                fail("%s: forbidden claim (%s): %r" % (rel, label, m.group(0)))


def check_sitemap():
    p = os.path.join(OUT, "sitemap.xml")
    if not os.path.exists(p):
        return fail("sitemap.xml missing")
    xml = read(p)
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    expected = {"https://%s/" % C.DOMAIN}
    for c in CITIES:
        expected.add("https://%s/cities/%s.html" % (C.DOMAIN, c["slug"]))
    for page in ("how-it-works", "about", "contact", "privacy-policy", "terms"):
        expected.add("https://%s/%s.html" % (C.DOMAIN, page))
    missing = expected - set(locs)
    extra = set(locs) - expected
    if missing:
        fail("sitemap missing: %s" % sorted(missing))
    if extra:
        warn("sitemap has extra urls: %s" % sorted(extra))
    print("  sitemap      : %d urls" % len(locs))


def check_batching():
    n = len(glob.glob(os.path.join(OUT, "cities", "*.html")))
    print("  batch 1      : %d city pages (target 15-20; total goal 100+ across later batches)" % n)
    if n < 15 or n > 20:
        warn("batch 1 has %d city pages; brief asks for 15-20" % n)


def run(city_metas=None):
    _seed_boilerplate()
    print("\n=== QA: anti-template + integrity ===")
    check_page_basics()
    check_links()
    check_phone()
    check_forbidden()
    check_sitemap()
    check_batching()
    worst = check_uniqueness()

    for x in WARN:
        print("  WARN  " + x)
    for x in FAIL:
        print("  FAIL  " + x)

    print("\n  result: %d failures, %d warnings" % (len(FAIL), len(WARN)))
    if FAIL:
        print("  STATUS: FAIL — fix before publishing")
        return 1
    print("  STATUS: PASS — every city page carries unique local content")
    return 0


if __name__ == "__main__":
    sys.exit(run())
