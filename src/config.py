# -*- coding: utf-8 -*-
"""
Site-wide configuration for FindMyPlumber.

EDIT THE VALUES IN THIS FILE (and nothing else) to rebrand / re-point the site.
Then run:  python3 src/build.py
"""

# ---------------------------------------------------------------- identity ---
BRAND = "FindMyPlumber"
BRAND_LEGAL = "FindMyPlumber.com"
BRAND_TAGLINE = "Free plumber referrals across California's Central Coast"

# Placeholder domain. Global find/replace in public/ when the real domain is live.
DOMAIN = "findmyplumber.com"
ORIGIN = "https://" + DOMAIN          # used for canonical + sitemap URLs

CONTACT_EMAIL = "hello@" + DOMAIN      # TODO: point at a real monitored inbox

# ------------------------------------------------------------------ phone ----
# The number shown on the page BEFORE Ringba swaps it, and the number that
# still works if the Ringba script never loads. Ringba's "Number to Replace"
# must be set to exactly this number.
PHONE_RAW = "8315326042"               # E.164-ish digits, no punctuation
PHONE_DISPLAY = "(831) 532-6042"       # <-- the pattern Ringba will match/replace
PHONE_TEL = "+18315326042"

# ----------------------------------------------------------------- ringba ----
# Ringba > Manage Campaigns > your campaign > Call Tracking Tags > Install Tag.
# Paste the generated snippet BETWEEN the marker lines in src/templates.py
# (RINGBA_SNIPPET). Leave TEMPLATE_TAG_ID alone if you paste the whole snippet.
RINGBA_CAMPAIGN_ID = "PASTE_YOUR_RINGBA_CAMPAIGN_ID"
RINGBA_TEMPLATE_TAG_ID = "PASTE_YOUR_ringba_com_tag_VALUE"

# Ringba returns a 404 if the campaign or the publisher number is paused/deleted,
# so this fallback must always be a live, routed number.
RINGBA_FALLBACK_OK = True

# ------------------------------------------------------------------- misc ----
LAUNCH_DATE = "2026-09-07"             # batch 1 publish date, used in sitemap
DEFAULT_LOCALE = "en-US"
STATE_NAME = "California"
STATE_ABBR = "CA"

# Cities added in later batches get a later <lastmod> so the sitemap stays honest.
BATCH = 1

DISCLOSURE_SHORT = "Calls may be routed to a network of licensed local plumbing professionals."

DISCLOSURE_LONG = (
    "FindMyPlumber is a free referral service, not a plumbing company. We do not perform "
    "plumbing work and we are not a licensed contractor. When you call, your call may be "
    "routed to a network of independent, licensed local plumbing professionals who contact "
    "you directly. Any agreement, quote, warranty or invoice is between you and the plumber "
    "you choose to hire."
)

# Contact form endpoint. Static site, so wire this to Formspree / Basin /
# a Cloudflare Worker / your own API, then remove the JS guard in
# build_contact(). Leave as "#" to keep the form inert but honest.
FORM_ENDPOINT = "#"
