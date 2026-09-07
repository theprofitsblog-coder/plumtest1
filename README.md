# FindMyPlumber — pay-per-call plumber referral site (batch 1)

A static, dependency-free multi-page site for a **pay-per-call plumber referral
service**. Visitors call the number on the page, Ringba tracks and routes the
call, the site earns per qualified call.

The site is a **referral / directory service, not a plumbing company**, and every
page says so.

```
Batch 1:  18 city pages  ·  6 Central Coast counties  ·  25 HTML files  ·  ~668 KB
QA:       0 failures, 0 warnings  ·  25 HTML files validated
DNI:      21/21 tests passing
```

---

## 1. What is here

```
findmyplumber/
├── public/                     ← THE SITE. Deploy this folder, nothing else.
│   ├── index.html              homepage + city index + search filter
│   ├── cities/*.html           18 city pages (batch 1)
│   ├── how-it-works.html
│   ├── about.html
│   ├── contact.html
│   ├── privacy-policy.html     includes the call-recording disclosure
│   ├── terms.html              states plainly: lead gen, not a contractor
│   ├── 404.html
│   ├── sitemap.xml  robots.txt
│   ├── css/site.css
│   ├── js/dni.js               Ringba adapter: href sync, queue replay, self-test
│   ├── js/city-search.js       homepage city/ZIP/county filter
│   ├── img/favicon-512.png  favicon-32.png  apple-touch-icon.png   (real PNGs)
│   └── data/cities.json        machine-readable coverage index
├── src/
│   ├── config.py               ← EDIT THIS: brand, domain, phone, Ringba ids
│   ├── cities.py               ← EDIT THIS: the per-city researched dataset
│   ├── templates.py            header/footer/phone block + RINGBA SNIPPET slot
│   ├── build.py                the generator (also holds the copy-variant pools)
│   ├── qa.py                   anti-template + integrity gate
│   └── make_favicon.py         regenerates the PNG icons
└── test/dni.test.js            jsdom harness proving the number swap works
```

Build and verify:

```bash
python3 src/build.py --qa        # regenerate public/ and run the QA gate
node test/dni.test.js            # verify Ringba DNI behaviour (needs jsdom)
python3 src/make_favicon.py      # only if you change the logo
```

Preview locally:

```bash
python3 -m http.server 8000 --bind 0.0.0.0 --directory public
```

---

## 2. BEFORE YOU GO LIVE — five things, in order

### 2.1 Point Ringba at the number that is actually on the page

Ringba's DNI replaces a **"Number to Replace"**. It must be exactly what is
printed on the page, in any punctuation pattern.

In `src/config.py`:

```python
PHONE_DISPLAY = "(831) 532-6042"   # what the page shows / what Ringba matches
PHONE_TEL     = "+18315326042"
```

In Ringba → **Manage Campaigns → your campaign → Call Tracking Tags**:

| Ringba field | Set it to |
|---|---|
| Primary Number | the number that shows when the pool is exhausted |
| **Number to Replace** | `(831) 532-6042` — same digits as `PHONE_DISPLAY` |
| Capture User Data | **ON**, then pick your Number Pool |

> Ringba recommends Number to Replace = Primary Number, so that if the script
> fails to load the call still routes to the right campaign. This build follows
> that: the fallback number on every page is a real, routed number.

### 2.2 Paste the real Ringba snippet

`src/templates.py` has a clearly marked slot:

```
<!-- ===================== BEGIN RINGBA CALL TRACKING TAG ===================== -->
...
<!-- ====================== END RINGBA CALL TRACKING TAG ======================= -->
```

Replace that whole block with the snippet Ringba generates (Campaigns → your
campaign → Call Tracking Tags → **Install Tag** → copy). **Do not modify it**,
and keep the two config lines it needs:

```js
numberClass: "dni",              // elements Ringba renders the pool number into
cb: window.__fmpDniOnNumber,     // site hook that syncs tel: links
```

Ringba's own rule: **one snippet per page**. The build enforces it and QA fails
if a page ever has two.

If you would rather not hand-edit the template, set in `src/config.py`:

```python
RINGBA_TEMPLATE_TAG_ID = "JS..."   # your ringba_com_tag value
```

and the built-in snippet becomes live as-is.

### 2.3 Prove the swap happens

Every page carries a self-test. No code changes needed:

```
https://yourdomain.com/?dnitest=mock      # simulates a pool number, no Ringba call
https://yourdomain.com/?dnitest=report    # diagnostic panel
```

The panel reports: snippet present, `ringba_com_tag` configured, callback fired,
number on page, **changed vs fallback**, and how many `tel:` links are in sync.

Then do the real test: load a city page in a browser with the snippet installed,
and confirm the displayed number is **not** `(831) 532-6042`. If it still is,
Ringba returned no pool number — check that the campaign *and* the publisher
number are both **active** (a paused/deleted either makes the snippet 404) and
that Capture User Data is on with a pool attached.

> **If the number does not swap, calls are not attributed and you do not get
> paid.** Do not buy traffic before this passes.

Or run the automated harness, which exercises the same paths headlessly:

```bash
npm install jsdom && node test/dni.test.js
```

### 2.4 Set the real domain

`src/config.py` → `DOMAIN`. That drives canonical URLs, `sitemap.xml`,
`robots.txt` and all schema. Re-run `python3 src/build.py`.

`findmyplumber.com` is a placeholder — it is referenced only through `config.py`,
so nothing else needs editing.

### 2.5 Wire the contact form and the inbox

`FORM_ENDPOINT = "#"` in `config.py` is deliberately inert: the form explains
that it cannot send yet, rather than silently eating enquiries. Point it at
Formspree / Basin / a Cloudflare Worker, then remove the guard script in
`build_contact()`. Also set a real `CONTACT_EMAIL`.

---

## 3. Ringba wiring — how a phone number is built

One canonical markup, used in the header, hero, call blocks, footer and the
sticky mobile bar:

```html
<a class="dni-tel lg" href="tel:+18315326042" data-fallback="(831) 532-6042"
   data-ringba-number="true" aria-label="Call FindMyPlumber at (831) 532-6042">
  <span class="dni">(831) 532-6042</span>
</a>
```

- `.dni` is what Ringba renders the pool number into (`numberClass: "dni"`).
- The visible text is always the **fallback** number, so something sensible
  shows before the swap and if the script never loads.
- `js/dni.js` does only what Ringba's renderer is not guaranteed to do:
  1. rewrites every `href="tel:…"` so **tap-to-call dials the number on screen**
     (the highest-value fix — a swapped text node with a stale `href` sends the
     call to the wrong number and loses the attribution),
  2. keeps `data-active-number` in sync,
  3. sweeps stray plain-text renderings of the old number,
  4. buffers an early Ringba callback in `window.__fmpDniQueue` and replays it.

It never invents a number, and it refuses to rewrite anything if it cannot
determine the fallback (fails safe rather than corrupting the page).

Mobile: the number is a large tap target and there is a sticky bottom call bar
(`.sticky-call`) visible while scrolling, with `safe-area-inset` padding.

---

## 4. Honesty rules this build enforces

Baked into the copy **and** mechanically checked by `src/qa.py`:

| Rule | Enforcement |
|---|---|
| Never claim to be a licensed plumbing business | Every page: disclosure by the phone number + footer + terms §1 |
| No invented founding year / address / owner | `check_forbidden()` regexes fail the build |
| No fake testimonials, reviews, ratings, counts | No such section exists; regex fails on "testimonial", "N-star", "N,NNN customers" |
| No unverifiable response times / satisfaction rates | Answers say "response depends on the plumber and current demand" |
| Plain-language "we connect you, we are not the plumber" | `DISCLOSURE_LONG` on every city page and the footer of every page |
| Call-recording disclosure | `privacy-policy.html` §5, incl. California Penal Code §632 all-party consent |
| Every number sourced | Each city page prints its source note (Census / utility CCR / city program) |

Deliberately **omitted**: any "how many plumbers are in our network in X" claim,
any review widget, any "guaranteed arrival in 60 minutes".

---

## 5. How the anti-template problem is handled

At 100+ pages, `{{city}}` substitution is the thing that gets a site penalised or
ignored. Each city page varies on **14 independent axes**:

| Axis | Variants |
|---|---|
| Locally relevant plumbing issue (2–3 sentences, researched) | unique per city |
| Real local fact + population | unique per city |
| Neighborhoods / ZIP codes / nearby towns | unique per city |
| 3 city-specific FAQ questions | unique per city |
| Source note | unique per city |
| Intro frame | 8 |
| Referral paragraph | 8 |
| Closing line | 8 |
| Emergency paragraph | 8 |
| Generic FAQ set (3 Q&A) | **18 — one unique set per city** |
| Service-area intro + 3 sub-headings | 8 + 8 |
| "Not a price quote" note | 7 |
| Services lead-in + 8 per-card blurbs | 8 + 8 |
| Hero card heading/items, CTA label, "have ready" list + heading | 8 / 8 / 8 / 7 / 8 |
| Section order | 7 distinct layouts |
| H2 headings (area / issue / fact / call / svc / emergency / nearby / faq) | 3–5 each |

**Slot assignment is a joint graph colouring**, not a modulo rotation. Two pages
are "related" if they are in the same county, cross-link as nearby towns, or are
adjacent in the city index. Related pages are guaranteed to share **no** rotating
block in **any** pool — the assigner searches all 12 pools simultaneously. The
generic FAQ set is solved as a bipartite matching so each city gets a unique one.

The largest related-clique in batch 1 is 7 cities, which is why every pool has
≥ 7 variants. `assign_slots()` raises if you add a pool below that.

### What QA measures

```
identity copy: intro+issue, referral paragraph, local fact and local issue
               paragraph are unique on all 18 city pages
similarity   : worst pair 0.31 (ceiling 0.62)
layouts      : 7 distinct section orders across 18 city pages
collisions   : 0 of 153 page pairs share >8 non-boilerplate sentences
boilerplate  : 4 disclosure/footer sentences identical site-wide (intended)
```

Plus: every internal link resolves, all ZIPs/population/source notes are present
on their own page, titles ≤ 60 chars, meta descriptions ≤ 158 and not truncated,
JSON-LD parses, exactly one Ringba snippet per page, no unexpected phone numbers
anywhere, sitemap matches the generated set.

```bash
python3 src/build.py --qa     # exits non-zero on failure
```

---

## 6. Publishing pace — read this before batch 2

The brief is 100+ cities. **Do not publish them in one batch on a new domain.**

| Batch | When | What |
|---|---|---|
| **1 (this build)** | launch | 18 city pages + homepage + legal + sitemap |
| 2 | ~2–3 weeks later, once batch 1 is crawled and indexed | next 15–20 cities |
| 3+ | every 2–3 weeks | 15–20 more, same standard per page |

Practical notes:

- Submit `sitemap.xml` in Search Console at launch. Watch coverage before adding
  the next batch — if pages are not getting indexed, adding more does not help.
- Get a handful of real inbound links and a Google Business Profile for the
  referral service before batch 2.
- Only publish a city page when you can write the researched local detail for it.
  A thin page is worse than no page.
- Each batch: append to `src/cities.py`, run `python3 src/build.py --qa`, deploy
  **only the new/changed files**, and give the new URLs their own `<lastmod>`.

---

## 7. Adding cities (batch 2 and beyond)

1. Append a dict to `src/cities.py`. Every field is required:

```python
dict(
    slug="fresno", name="Fresno", county="Fresno County",
    population="542,107", pop_note="2020 U.S. Census",
    zips=["93701", ...],                    # real USPS ZIPs
    neighborhoods=["Tower District", ...],  # real, checkable names
    nearby=["Clovis", "Madera", ...],       # include other covered cities to cross-link
    landmarks=["..."],
    fact=("One true, specific sentence: region, landmark, population."),
    sources=("Where the numbers came from — Census, utility CCR, city program page."),
    issue=("2–3 sentences on a plumbing issue genuinely more common HERE: "
           "hard water, pre-1970 cast iron/Orangeburg, expansive clay, salt air, "
           "flood history, wells and septic. Researched, not generic."),
    services=[...8 items...],               # localise them: softeners, well pumps, laterals
    faq=[("Q about this city?", "Honest A.") × 3],
)
```

2. Run the build. `assign_slots()` recolours automatically; QA fails if a pool is
   now too small for the enlarged clique — add variants to that pool in
   `src/build.py`.

3. Run `node test/dni.test.js` and `python3 src/build.py --qa`.

### Sourcing the local detail (what to actually look up)

- **Water hardness** → the utility's annual Consumer Confidence Report, or the
  district's "water hardness" page. Batch 1 used: Cal Water (Salinas 254 ppm ≈
  15 gpg, Salinas Hills ≈ 320 ppm), City of Santa Maria Utilities (groundwater
  420–730 mg/L = 25–43 gpg, typical blend 250 mg/L = 15 gpg), Monterey Water
  System CCR (169 ppm avg), Soquel Creek WD (150–370 ppm), Scotts Valley WD
  (230 ppm), San Lorenzo Valley WD (46 ppm, soft), Valley Water (county
  groundwater > 250 mg/L).
- **Housing age / pipe material** → city historic context statements, sewer
  lateral ordinance staff reports. (Santa Cruz: pre-1970 homes commonly clay
  tile, cast iron or Orangeburg; lateral ordinance effective 26 Jun 2018;
  ~16,000 private laterals, ~160 miles of public main.)
- **Municipal programs** → point-of-sale lateral / septic / well inspection
  ordinances. These make excellent, genuinely useful FAQ content.
- **Population** → 2020 Decennial Census (census.gov). Attribute it on the page.
- **ZIPs and neighborhoods** → USPS and city/county sources. Never invent a
  neighborhood name.

---

## 8. Known placeholders

| Where | What |
|---|---|
| `config.py` `RINGBA_TEMPLATE_TAG_ID` | `PASTE_YOUR_ringba_com_tag_VALUE` |
| `config.py` `DOMAIN` | `findmyplumber.com` (placeholder) |
| `config.py` `CONTACT_EMAIL` | `hello@findmyplumber.com` |
| `config.py` `FORM_ENDPOINT` | `#` — form is inert and says so |
| `templates.py` `RINGBA_SNIPPET` | Ringba-shaped loader awaiting your tag id |

The site is fully functional with all of these in place: the fallback number is
real and routed, so calls work before Ringba is configured — they just are not
attributed.
