"""Build skyblue-poolcare.com.

    python3 _build/build.py               # live theme -> public/
    python3 _build/build.py california    # one theme -> public/
    python3 _build/build.py --demos       # every theme -> demos/<theme>/

Writes the static site to public/. Content lives in _build/content.py.
Styles: _build/base.css + _build/skyblue.css + the theme's override file
in _build/themes/, joined into one public/assets/site.css. Only the look
changes between themes; pages and copy are identical. Forms post to GoHighLevel (see GHL-SETUP.md).
Links are relative and pages are flat .html files, so Cloudflare Pages
serves them as clean URLs (/pool-service-encino).
"""
import csv
import html
import json
import shutil
import sys
from pathlib import Path

from content import BIZ, CITIES, FAQ, POSTS, PROMISES, SERVICES, TESTIMONIALS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "public"
DEMOS = ROOT / "demos"
e = html.escape

# Demo themes for Skyblue to pick from. Same pages and copy, different look.
# Colors in every theme come from the current logo: sky blue + #7CE6F3 aqua.
THEMES = {
    "skyblue": {
        "name": "Original", "blurb": "The first build. Bright, friendly, sky-blue gradients.",
        "fonts": "family=Outfit:wght@600;700&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,800",
        "color": "#2490C8", "css": None,
    },
    "california": {
        "name": "California", "blurb": "Sunset sky, palms and sand, with bold modern type.",
        "fonts": "family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Figtree:wght@400;500;600;700",
        "color": "#FF8A5B", "css": "california.css",
    },
    "minimal": {
        "name": "Minimal", "blurb": "White space, thin lines, one blue. Nothing extra.",
        "fonts": "family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600",
        "color": "#FFFFFF", "css": "minimal.css",
    },
    "nightswim": {
        "name": "Night Swim", "blurb": "Dark navy and glowing aqua. Upscale, for Beverly Hills and the Hills.",
        "fonts": "family=Playfair+Display:wght@600;700&family=Manrope:wght@400;600;800",
        "color": "#0B1A3F", "css": "nightswim.css",
    },
}
LIVE_THEME = "skyblue"
DEMO_THEMES = ["california", "minimal", "nightswim"]
THEME, THEME_KEY = THEMES[LIVE_THEME], LIVE_THEME

# Logo from the current Webflow site. Drop the file in _build/logo.png to
# serve it locally instead (do this before launch). If the image fails to
# load, brand.js swaps in the drawn mark + wordmark.
LOGO_SRC = "https://cdn.prod.website-files.com/6779dcd512e7db5c270fcafa/678bb8a3a9998141beaf7191_SkyBlue%20Logo.png"
REGIONS = {"valley": "San Fernando Valley", "westside": "Westside & Hollywood"}

# zip -> neighborhoods, from the shared service-area list
ZIPS = {r["zip"]: r for r in csv.DictReader(open(ROOT / "data" / "service-area-zips.csv"))}

LOGO = """<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#2490C8"/>
<path d="M5 22q4-4 7.5 0t7.5 0 7.5 0 7.5 0" fill="none" stroke="#7CE6F3" stroke-width="3" stroke-linecap="round"/>
<path d="M7 28q3.3-3 6.5 0t6.5 0 6.5 0 6.5 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
<circle cx="27" cy="12" r="4" fill="#FFD25C"/></svg>"""


def page_url(slug):
    return f"{BIZ['domain']}/{slug}" if slug else BIZ["domain"] + "/"


def city_file(c):
    return f"pool-service-{c['slug']}.html"


def brand():
    src = "assets/logo.png" if (HERE / "logo.png").exists() else LOGO_SRC
    return (f'<a class="brand" href="index.html"><img class="brand-logo" src="{src}" alt="SkyBlue Pool Care" width="180" height="52">'
            f'<span class="brand-fallback">{LOGO}<span>Sky<b>Blue</b> Pool Care</span></span></a>')


def head(title, desc, slug, schema=None, noindex=False):
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
{robots}<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{page_url(slug)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{page_url(slug)}">
<meta name="theme-color" content="{THEME['color']}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{THEME['fonts']}&display=swap">
<link rel="stylesheet" href="assets/site.css">
{ld}
</head>
<body class="theme-{THEME_KEY}">
"""


def nav(active=""):
    items = [("weekly-pool-service.html", "Weekly Service", "weekly"),
             ("index.html#services", "Services", "services"),
             ("service-areas.html", "Service Areas", "areas"),
             ("blog.html", "Blog", "blog"),
             ("contact.html", "Contact", "contact")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if k == active else ""}>{t}</a>' for h, t, k in items)
    return f"""<header class="site-head">
  <div class="wrap head-row">
    {brand()}
    <nav class="main-nav" aria-label="Main">{links}</nav>
    <div class="head-cta">
      <a class="head-phone" href="tel:{BIZ['phone_e164']}">{BIZ['phone']}</a>
      <a class="btn btn-primary" href="contact.html">Get a Free Quote</a>
    </div>
  </div>
</header>
<main>
"""


def footer():
    def links(region):
        return "".join(f'<li><a href="{city_file(c)}">{c["name"]}</a></li>' for c in CITIES if c["region"] == region)
    svc = "".join(f'<li><a href="{s.get("href", "index.html#services")}">{s["name"]}</a></li>' for s in SERVICES)
    return f"""</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      {brand()}
      <p>Locally owned weekly pool service for the {BIZ['region']}. A photo and full pool report after every visit.</p>
    </div>
    <div>
      <h3>Contact</h3>
      <ul class="foot-list">
        <li><a href="tel:{BIZ['phone_e164']}">{BIZ['phone']}</a></li>
        <li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
        <li>{BIZ['hours']}</li>
      </ul>
      <h3>Services</h3>
      <ul class="foot-list">{svc}</ul>
    </div>
    <div>
      <h3>San Fernando Valley</h3>
      <ul class="foot-list">{links('valley')}</ul>
    </div>
    <div>
      <h3>Westside &amp; Hollywood</h3>
      <ul class="foot-list">{links('westside')}</ul>
    </div>
  </div>
  <div class="wrap foot-base">
    <span>&copy; 2026 {BIZ['legal']}</span>
    <span><a href="service-areas.html">All service areas</a> &middot; <a href="blog.html">Blog</a> &middot; <a href="privacy.html">Privacy</a></span>
  </div>
</footer>
<div class="mobile-bar">
  <a href="tel:{BIZ['phone_e164']}">Call</a>
  <a class="mb-quote" href="contact.html">Free Quote</a>
</div>
<script src="assets/brand.js" defer></script>
<script src="assets/ghl-form.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- form

def intake_form(fid, city=None):
    p = fid
    city_opts = "".join(
        f'<option value="{c["short"]}"{" selected" if city and c["slug"] == city["slug"] else ""}>{c["name"]}</option>'
        for c in CITIES)
    svc_opts = "".join(f"<option>{s['name']}</option>" for s in SERVICES)
    page_city = city["short"] if city else ""
    return f"""<form class="intake" id="{p}-form" data-ghl-form novalidate>
  <div class="f-row">
    <div class="f-field"><label for="{p}-first">First name</label><input id="{p}-first" name="first_name" autocomplete="given-name" required></div>
    <div class="f-field"><label for="{p}-phone">Mobile phone</label><input id="{p}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
  </div>
  <div class="f-field"><label for="{p}-address">Street address</label><input id="{p}-address" name="address1" autocomplete="street-address"></div>
  <div class="f-row">
    <div class="f-field"><label for="{p}-zip">ZIP code</label><input id="{p}-zip" name="postal_code" inputmode="numeric" autocomplete="postal-code" maxlength="5" required></div>
    <div class="f-field"><label for="{p}-city">Area</label><select id="{p}-city" name="city"><option value="">Choose your area</option>{city_opts}<option>Other</option></select></div>
  </div>
  <div class="f-row">
    <div class="f-field"><label for="{p}-service">What do you need?</label><select id="{p}-service" name="service_needed"><option>Weekly Pool Service</option>{svc_opts.replace('<option>Weekly Pool Service</option>', '')}<option>Not sure yet</option></select></div>
    <div class="f-field"><label for="{p}-email">Email <span class="opt">(optional)</span></label><input id="{p}-email" name="email" type="email" autocomplete="email"></div>
  </div>
  <label class="f-consent" for="{p}-consent"><input id="{p}-consent" name="sms_consent" type="checkbox" value="yes"> <span>I agree to receive calls and text messages from SkyBlue Pool Care about my quote and service. Msg &amp; data rates may apply. Msg frequency varies. Reply STOP to opt out, HELP for help. See our <a href="privacy.html">Privacy Policy</a>.</span></label>
  <div class="hp" aria-hidden="true"><label for="{p}-website">Website</label><input id="{p}-website" name="website" tabindex="-1" autocomplete="off"></div>
  <input type="hidden" name="lead_source" value="Website">
  <input type="hidden" name="page_city" value="{page_city}">
  <input type="hidden" name="page_url" value="">
  <input type="hidden" name="utm_source" value=""><input type="hidden" name="utm_medium" value=""><input type="hidden" name="utm_campaign" value=""><input type="hidden" name="utm_term" value=""><input type="hidden" name="gclid" value="">
  <button class="btn btn-primary btn-block" type="submit">Get My Free Quote</button>
  <p class="f-status" role="status" aria-live="polite"></p>
  <p class="f-note">No contract. We reply the same business day.</p>
</form>"""


# ---------------------------------------------------------------- sections

def trust_strip():
    return '<div class="trust"><div class="wrap trust-row">' + "".join(
        f'<div class="trust-item"><strong>{a}</strong><span>{b}</span></div>' for a, b in PROMISES) + "</div></div>"


def services_section():
    cards = "".join(f"""<article class="svc">
      <h3>{f'<a href="{s["href"]}">{s["name"]}</a>' if s.get("href") else s["name"]}</h3>
      <p>{s['body']}</p>
      <ul>{''.join(f'<li>{pt}</li>' for pt in s['points'])}</ul>
    </article>""" for s in SERVICES)
    return f"""<section class="sec" id="services">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Services</p><h2>Weekly care, cleanups and repairs</h2>
    <p class="lede">One local team for the weekly cleaning and everything that breaks in between.</p></div>
    <div class="svc-grid">{cards}</div>
  </div>
</section>"""


def visit_section():
    tasks = [("Brush", "walls, steps, tile line"), ("Skim", "surface and waterline"), ("Vacuum", "floor and corners"),
             ("Baskets", "skimmer and pump emptied"), ("Chemistry", "tested and balanced"), ("Equipment", "pump, filter, heater checked")]
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in tasks)
    return f"""<section class="sec sec-visit">
  <div class="wrap visit-grid">
    <div>
      <p class="eyebrow">Every visit</p>
      <h2>A clean pool and a photo report, every week</h2>
      <p class="lede">Your tech comes the same day each week. When they leave, you get a photo and a full pool report, so you always know the work was done.</p>
      <ul class="checks">
        <li>Same day every week, no skipped cleanings</li>
        <li>Free 21-point inspection after your first service</li>
        <li>No contract, month to month</li>
      </ul>
    </div>
    <div class="report">
      <div class="report-head"><span>Pool report</span><span class="report-ok">Complete</span></div>
      <table class="report-table"><caption class="sr">What every weekly visit covers</caption>{rows}</table>
      <p class="report-foot">Sent to your phone after every visit, with photos.</p>
    </div>
  </div>
</section>"""


def steps_section():
    steps = [("Free quote", "Send the form or call. We quote over the phone."),
             ("Deep first clean", "A service manager does a full initial cleaning."),
             ("21-point inspection", "Free, after your first scheduled service."),
             ("Weekly service", "Same day every week, photo report every time.")]
    lis = "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in steps)
    return f"""<section class="sec">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2>Getting started takes one call</h2></div>
    <ol class="steps">{lis}</ol>
  </div>
</section>"""


def price_section():
    return f"""<section class="sec sec-alt" id="pricing">
  <div class="wrap visit-grid">
    <div>
      <p class="eyebrow">Pricing</p>
      <h2>Weekly pool service pricing</h2>
      <p class="lede">One flat monthly price for weekly service. Your exact price depends on pool size, a spa, trees and equipment, and we'll give you a firm number before we start.</p>
    </div>
    <div class="price-card">
      <p class="eyebrow">Weekly service</p>
      <p class="price-from">from {BIZ['price_from']}<small> /month</small></p>
      <p>Includes brushing, skimming, vacuuming, baskets, water testing and balancing, an equipment check and a photo report every visit. <span class="fill">Chemicals included? Confirm.</span></p>
      <a class="btn btn-primary" href="#quote">Get my exact price</a>
    </div>
  </div>
</section>"""


def areas_section():
    blocks = ""
    for key, label in REGIONS.items():
        chips = "".join(f'<a class="city" href="{city_file(c)}">{c["name"]}</a>' for c in CITIES if c["region"] == key)
        blocks += f'<h3 class="region-head">{label}</h3><div class="city-cloud">{chips}</div>'
    return f"""<section class="sec sec-areas" id="areas">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Service areas</p><h2>Weekly routes across the Valley and the Westside</h2>
    <p class="lede">74 zip codes, from Sylmar to Santa Monica. Pick your area for local details.</p></div>
    {blocks}
    <p class="areas-more"><a href="service-areas.html">See every zip code we serve &rarr;</a></p>
  </div>
</section>"""


def reviews_section():
    cards = "".join(f'<figure class="review"><blockquote>{e(q)}</blockquote><figcaption>{n}</figcaption></figure>'
                    for q, n in TESTIMONIALS)
    cards += '<figure class="review"><blockquote><span class="fill">Paste a 5-star Google review here.</span></blockquote><figcaption><span class="fill">First name, area</span></figcaption></figure>'
    return f"""<section class="sec sec-reviews">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Reviews</p><h2>What customers say</h2>
    <p class="lede"><span class="fill">X.X stars from XX Google reviews</span></p></div>
    <div class="review-grid">{cards}</div>
  </div>
</section>"""


def faq_section(items, title="Questions we hear a lot"):
    body = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f"""<section class="sec sec-faq">
  <div class="wrap faq-wrap">
    <div class="sec-head"><p class="eyebrow">FAQ</p><h2>{title}</h2></div>
    <div class="faq">{body}</div>
  </div>
</section>"""


def quote_section(title="Get a free weekly service quote", city=None, fid="q"):
    return f"""<section class="sec sec-quote" id="quote">
  <div class="wrap quote-grid">
    <div class="quote-copy">
      <p class="eyebrow">Free quote</p>
      <h2>{title}</h2>
      <p class="lede">Tell us where your pool is. We'll call or text the same business day with a price. No contract, no pressure.</p>
      <ul class="checks">
        <li>Photo and full pool report after every visit</li>
        <li>No skipped cleanings guarantee</li>
        <li>Free 21-point inspection after your first service</li>
      </ul>
      <p class="quote-call">Rather talk? Call <a href="tel:{BIZ['phone_e164']}">{BIZ['phone']}</a></p>
    </div>
    <div class="quote-card">{intake_form(fid, city)}</div>
  </div>
</section>"""


def page_hero(eyebrow, title, lede, crumbs):
    bc = " <span>/</span> ".join(f'<a href="{h}">{t}</a>' if h else f'<span aria-current="page">{t}</span>' for t, h in crumbs)
    return f"""<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{bc}</nav>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


# ---------------------------------------------------------------- schema

def business_schema():
    return {
        "@type": "HomeAndConstructionBusiness",
        "@id": BIZ["domain"] + "/#business",
        "name": BIZ["name"],
        "url": BIZ["domain"] + "/",
        "telephone": BIZ["phone_e164"],
        "email": BIZ["email"],
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": "Los Angeles", "addressRegion": "CA", "addressCountry": "US"},
        "areaServed": [{"@type": "Place", "name": f"{c['name']}, CA"} for c in CITIES]
                      + sorted(ZIPS),
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Pool services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"]}} for s in SERVICES]},
    }


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(strip_tags(a))}}
        for q, a in items]}


def crumbs_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": page_url(s)} for i, (t, s) in enumerate(crumbs)]}


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def graph(*nodes):
    return {"@context": "https://schema.org", "@graph": list(nodes)}


# ---------------------------------------------------------------- pages

def home():
    hero = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">San Fernando Valley &middot; Westside &middot; Hollywood</p>
      <h1>Weekly pool service, <span>with proof every visit.</span></h1>
      <p class="lede">Locally owned pool care from Sylmar to Santa Monica. Same day every week, and a photo and full pool report after every cleaning.</p>
      <div class="hero-btns"><a class="btn btn-primary" href="#quote">Get a Free Quote</a><a class="btn btn-ghost" href="tel:{BIZ['phone_e164']}">Call {BIZ['phone']}</a></div>
      <p class="hero-note">Weekly service from {BIZ['price_from']}/month &middot; No contract</p>
    </div>
    <div class="hero-card">
      <p class="hero-card-title">Quick quote</p>
      <p class="hero-card-sub">Takes about a minute.</p>
      {intake_form('h')}
    </div>
  </div>
  <div class="hero-art" aria-hidden="true"><span class="sun"></span><span class="palm p1"></span><span class="palm p2"></span></div>
  <div class="wave-band" aria-hidden="true"></div>
</section>"""
    body = (trust_strip() + services_section() + visit_section() + price_section() + areas_section()
            + reviews_section() + steps_section() + blog_teaser() + faq_section(FAQ)
            + quote_section("Prefer to tell us more? Get a quote"))
    schema = graph({**business_schema()}, faq_schema(FAQ))
    return (head("Weekly Pool Service, San Fernando Valley & Westside | SkyBlue",
                 "Weekly pool cleaning across the San Fernando Valley, Westside and Hollywood. Same day every week, photo report after every visit, no contract. Free quote.",
                 "", schema)
            + nav() + hero + body + footer())


def weekly_page():
    crumbs = [("Home", ""), ("Weekly Pool Service", "weekly-pool-service")]
    main = page_hero("Weekly pool service", "Weekly pool service in Los Angeles",
                     f"Same day every week across the {BIZ['region']}. A photo and full pool report after every visit, and no contract.",
                     [("Home", "index.html"), ("Weekly Pool Service", None)])
    main += visit_section() + price_section() + steps_section() + reviews_section() + areas_section()
    main += faq_section(FAQ, "Weekly service questions") + quote_section()
    schema = graph(
        {"@type": "Service", "serviceType": "Weekly pool cleaning", "name": "Weekly Pool Service",
         "provider": {"@id": BIZ["domain"] + "/#business", "name": BIZ["name"]},
         "areaServed": [{"@type": "Place", "name": f"{c['name']}, CA"} for c in CITIES]},
        faq_schema(FAQ), crumbs_schema(crumbs))
    return (head("Weekly Pool Service in Los Angeles | SkyBlue Pool Care",
                 "Weekly pool cleaning in the San Fernando Valley and Westside LA: brush, skim, vacuum, balance, photo report after every visit. No contract. Free quote.",
                 "weekly-pool-service", schema)
            + nav("weekly") + main + footer())


def zip_chips(c):
    lis = "".join(f'<li><b>{z}</b>{e(ZIPS[z]["neighborhoods"].replace(";", ","))}</li>' for z in c["zips"])
    return f'<ul class="zip-list">{lis}</ul>'


def city_page(c):
    hoods = ", ".join(c["hoods"][:-1]) + " and " + c["hoods"][-1]
    near = [x for x in CITIES if x["region"] == c["region"] and x["slug"] != c["slug"]]
    near_html = "".join(f'<a class="city" href="{city_file(x)}">{x["name"]}</a>' for x in near)
    local = "".join(f'<article class="local"><h3>{t}</h3><p>{b}</p></article>' for t, b in c["local"])
    svc = "".join(f"<li><strong>{s['name']}.</strong> {s['short']}</li>" for s in SERVICES)
    faq_items = c["faq"] + FAQ[:4]
    slug = city_file(c)[:-5]
    crumbs = [("Home", ""), ("Service Areas", "service-areas"), (c["name"], slug)]
    title = f"Pool Service in {c['name']} | SkyBlue Pool Care"
    if len(title) > 62:
        title = f"Pool Service {c['name']} | SkyBlue"
    desc = (f"Weekly pool cleaning in {c['name']} ({', '.join(c['zips'][:3])}{' and more' if len(c['zips']) > 3 else ''}). "
            "Same day every week, photo report after every visit, no contract. Free quote.")
    main = page_hero(f"{REGIONS[c['region']]}", f"Weekly pool service in {c['name']}",
                     f"Same-day-every-week pool cleaning for {hoods}. A photo and full pool report after every visit.",
                     [("Home", "index.html"), ("Service Areas", "service-areas.html"), (c["name"], None)])
    main += f"""<section class="sec">
  <div class="wrap city-grid">
    <div class="prose">
      <h2>Pool care in {c['name']}</h2>
      <p>{c['intro']}</p>
      <h3>Weekly service in {c['short']}</h3>
      <p>Your tech comes the same day every week. They brush, skim, vacuum, empty the baskets, check the equipment, and test and balance the water. Then you get a photo and a full pool report. Weekly service starts at {BIZ['price_from']} a month, with no contract.</p>
      <h3>Other services in {c['short']}</h3>
      <ul>{svc}</ul>
    </div>
    <aside class="quote-card side-quote">
      <p class="hero-card-title">Free {c['short']} quote</p>
      {intake_form('c', c)}
    </aside>
  </div>
</section>
<section class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Local knowledge</p><h2>What {c['short']} pools need</h2></div>
    <div class="local-grid">{local}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Areas we serve</p><h2>{c['name']} zip codes and neighborhoods</h2>
    <p class="lede">Our {c['short']} routes cover these zip codes. Not sure if you're on a route? <a href="#quote">Ask with the quote form</a>.</p></div>
    {zip_chips(c)}
  </div>
</section>
{reviews_section()}
<section class="sec sec-areas">
  <div class="wrap"><div class="sec-head"><h2>Nearby service areas</h2></div><div class="city-cloud">{near_html}</div>
  <p class="areas-more"><a href="service-areas.html">All service areas &rarr;</a></p></div>
</section>
{faq_section(faq_items, f"{c['short']} pool service questions")}
{quote_section(f"Get a {c['short']} pool service quote", c, "q")}"""
    schema = graph(
        {"@type": "Service", "serviceType": "Weekly pool cleaning", "name": f"Weekly Pool Service in {c['name']}",
         "provider": {"@id": BIZ["domain"] + "/#business", "name": BIZ["name"], "telephone": BIZ["phone_e164"]},
         "areaServed": [{"@type": "Place", "name": f"{h}, CA"} for h in c["hoods"]]
                       + c["zips"]},
        faq_schema(faq_items), crumbs_schema(crumbs))
    return head(title, desc, slug, schema) + nav("areas") + main + footer()


def areas_page():
    blocks = ""
    for key, label in REGIONS.items():
        cards = "".join(f"""<a class="area-card" href="{city_file(c)}"><strong>{c['name']}</strong>
          <span>{', '.join(c['hoods'][:4])}</span></a>""" for c in CITIES if c["region"] == key)
        rows = "".join(
            f'<tr><td>{z}</td><td>{e(ZIPS[z]["neighborhoods"].replace(";", ","))}</td><td><a href="{city_file(c)}">{c["name"]}</a></td></tr>'
            for c in CITIES if c["region"] == key for z in c["zips"])
        blocks += f"""<h2 class="region-head">{label}</h2>
  <div class="area-grid">{cards}</div>
  <details class="zip-details"><summary>All {label} zip codes</summary>
  <table class="zip-table"><thead><tr><th>Zip</th><th>Neighborhoods</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table></details>"""
    crumbs = [("Home", ""), ("Service Areas", "service-areas")]
    main = page_hero("Service areas", "Pool service areas",
                     "Weekly routes in 74 zip codes across the San Fernando Valley, the Westside and Hollywood.",
                     [("Home", "index.html"), ("Service Areas", None)]) + f"""
<section class="sec"><div class="wrap">{blocks}
  <p class="areas-note">Don't see your zip? <a href="contact.html">Ask about your address.</a></p>
</div></section>{quote_section()}"""
    return (head("Pool Service Areas: Valley & Westside LA | SkyBlue Pool Care",
                 "SkyBlue Pool Care serves 74 zip codes: Calabasas, Woodland Hills, Encino, Tarzana, Sherman Oaks, Studio City, Northridge, Porter Ranch, Granada Hills, Burbank, Hollywood Hills, Beverly Hills, Brentwood, Santa Monica and more.",
                 "service-areas", graph(business_schema(), crumbs_schema(crumbs)))
            + nav("areas") + main + footer())


def contact_page():
    main = page_hero("Contact", "Get a free pool service quote",
                     "Tell us where your pool is. We'll call or text the same business day with a price.",
                     [("Home", "index.html"), ("Contact", None)]) + f"""
<section class="sec" id="quote"><div class="wrap quote-grid">
  <div class="quote-copy">
    <h2>Talk to a real person</h2>
    <dl class="contact-list">
      <dt>Phone</dt><dd><a href="tel:{BIZ['phone_e164']}">{BIZ['phone']}</a></dd>
      <dt>Email</dt><dd><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></dd>
      <dt>Hours</dt><dd>{BIZ['hours']}</dd>
      <dt>Service area</dt><dd><a href="service-areas.html">{BIZ['region']}</a></dd>
    </dl>
  </div>
  <div class="quote-card">{intake_form('ct')}</div>
</div></section>"""
    return (head("Get a Free Pool Service Quote | SkyBlue Pool Care",
                 "Request a free weekly pool service quote from SkyBlue Pool Care. Serving the San Fernando Valley, Westside and Hollywood.",
                 "contact", graph(business_schema()))
            + nav("contact") + main + footer())


def thanks_page():
    main = page_hero("Request received", "Thanks! We'll be in touch today.",
                     f"We reply the same business day. Need us sooner? Call {BIZ['phone']}.",
                     [("Home", "index.html"), ("Thank you", None)])
    return head("Thank You | SkyBlue Pool Care", "Your quote request was received.", "thank-you", noindex=True) + nav() + main + footer()


def not_found_page():
    main = page_hero("Page not found", "That page isn't here.",
                     "Try weekly pool service, our service areas, or get a quote.",
                     [("Home", "index.html")]) + quote_section()
    return head("Page Not Found | SkyBlue Pool Care", "Page not found.", "404", noindex=True) + nav() + main + footer()


def privacy_page():
    main = page_hero("Privacy", "Privacy Policy", "How SkyBlue Pool Care handles the information you send us.",
                     [("Home", "index.html"), ("Privacy", None)]) + f"""
<section class="sec"><div class="wrap prose legal">
  <p>Last updated October 2026.</p>
  <h2>What we collect</h2>
  <p>When you request a quote we collect your name, phone number, address, zip code, email if given, and the service you need. We also record the page you came from and ad campaign tags so we know which ads work.</p>
  <h2>How we use it</h2>
  <p>We use it to quote, schedule and service your pool, and to contact you about your service by phone, text or email.</p>
  <h2>Text messages</h2>
  <p>If you check the consent box, we may send texts about your quote and service. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. We do not sell or share your phone number or text consent with third parties or affiliates for their marketing.</p>
  <h2>Sharing</h2>
  <p>We don't sell your information. We share it only with service providers that help us run the business, such as our customer management and messaging software.</p>
  <h2>Contact</h2>
  <p>Questions or requests to delete your information: <a href="mailto:{BIZ['email']}">{BIZ['email']}</a> or <a href="tel:{BIZ['phone_e164']}">{BIZ['phone']}</a>.</p>
</div></section>"""
    return head("Privacy Policy | SkyBlue Pool Care", "SkyBlue Pool Care privacy policy.", "privacy") + nav() + main + footer()


# ---------------------------------------------------------------- blog

def post_file(p):
    return f"blog-{p['slug']}.html"


def post_card(p):
    return f"""<article class="post-card">
      <p class="post-meta"><span class="tag">{p['tag']}</span> <time datetime="{p['date']}">{p['date_h']}</time></p>
      <h3><a href="{post_file(p)}">{p['title']}</a></h3>
      <p>{p['desc']}</p>
      <span class="post-read">{p['read']}</span>
    </article>"""


def blog_teaser():
    cards = "".join(post_card(p) for p in POSTS[:3])
    return f"""<section class="sec sec-blog">
  <div class="wrap">
    <div class="sec-head row-head"><div><p class="eyebrow">Pool care tips</p><h2>From the blog</h2></div>
    <a class="link-more" href="blog.html">All articles &rarr;</a></div>
    <div class="post-grid">{cards}</div>
  </div>
</section>"""


def render_body(blocks):
    out = []
    for kind, val in blocks:
        if kind == "ul":
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in val) + "</ul>")
        else:
            out.append(f"<{kind}>{val}</{kind}>")
    return "\n".join(out)


def blog_index():
    feat, rest = POSTS[0], POSTS[1:]
    crumbs = [("Home", ""), ("Blog", "blog")]
    main = page_hero("Blog", "Pool care tips for Los Angeles owners",
                     "Straight answers on pricing, water chemistry and keeping your pool clear through a Valley summer.",
                     [("Home", "index.html"), ("Blog", None)]) + f"""
<section class="sec"><div class="wrap">
  <article class="post-feature">
    <p class="post-meta"><span class="tag">{feat['tag']}</span> <time datetime="{feat['date']}">{feat['date_h']}</time> &middot; {feat['read']}</p>
    <h2><a href="{post_file(feat)}">{feat['title']}</a></h2>
    <p class="lede">{feat['desc']}</p>
    <a class="btn btn-ghost" href="{post_file(feat)}">Read the article</a>
  </article>
  <div class="post-grid">{''.join(post_card(p) for p in rest)}</div>
</div></section>"""
    schema = graph({"@type": "Blog", "name": f"{BIZ['name']} Blog", "url": page_url("blog"),
                    "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"],
                                  "url": page_url(post_file(p)[:-5])} for p in POSTS]},
                   crumbs_schema(crumbs))
    return (head("Pool Care Blog for Los Angeles Owners | SkyBlue Pool Care",
                 "Pool care tips for San Fernando Valley and Westside homeowners: pricing, hard water, heat waves, winter care.",
                 "blog", schema) + nav("blog") + main + footer())


def post_page(p):
    slug = post_file(p)[:-5]
    others = "".join(post_card(x) for x in POSTS if x["slug"] != p["slug"])
    crumbs = [("Home", ""), ("Blog", "blog"), (p["title"], slug)]
    schema = graph({"@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
                    "datePublished": p["date"], "dateModified": p["date"], "mainEntityOfPage": page_url(slug),
                    "author": {"@type": "Organization", "name": BIZ["name"]},
                    "publisher": {"@id": BIZ["domain"] + "/#business", "name": BIZ["name"]}},
                   crumbs_schema(crumbs))
    main = f"""<article class="article">
  <header class="page-hero">
    <div class="wrap narrow">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> <span>/</span> <a href="blog.html">Blog</a></nav>
      <p class="post-meta"><span class="tag">{p['tag']}</span> <time datetime="{p['date']}">{p['date_h']}</time> &middot; {p['read']}</p>
      <h1>{p['title']}</h1>
      <p class="lede">{p['desc']}</p>
    </div>
  </header>
  <div class="wrap narrow prose">{render_body(p['body'])}
    <aside class="inline-cta"><p><strong>Want this handled for you?</strong> Weekly service with a photo report after every visit.</p><a class="btn btn-primary" href="contact.html">Get a Free Quote</a></aside>
  </div>
</article>
<section class="sec sec-blog"><div class="wrap"><div class="sec-head"><h2>More pool tips</h2></div><div class="post-grid">{others}</div></div></section>"""
    title = f"{p['title']} | SkyBlue"
    return head(title, p["desc"], slug, schema) + nav("blog") + main + footer()


# ---------------------------------------------------------------- build

def sitemap(slugs):
    rows = "".join(f"<url><loc>{page_url(s)}</loc></url>" for s in slugs)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{rows}</urlset>\n'


HEADERS = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable
/sitemap.xml
  Cache-Control: public, max-age=3600
/robots.txt
  Cache-Control: public, max-age=3600
"""


def build(theme=LIVE_THEME, out=OUT):
    global THEME, THEME_KEY
    THEME, THEME_KEY = THEMES[theme], theme
    css = (HERE / "base.css").read_text() + "\n" + (HERE / "skyblue.css").read_text()
    if THEME["css"]:
        css += "\n" + (HERE / "themes" / THEME["css"]).read_text()
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    (out / "assets" / "site.css").write_text(css)
    shutil.copy(HERE / "brand.js", out / "assets" / "brand.js")
    if (HERE / "logo.png").exists():
        shutil.copy(HERE / "logo.png", out / "assets" / "logo.png")
    shutil.copy(HERE / "ghl-form.js", out / "assets" / "ghl-form.js")
    (out / "assets" / "favicon.svg").write_text(LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
    pages = {"index.html": home(), "weekly-pool-service.html": weekly_page(), "service-areas.html": areas_page(),
             "contact.html": contact_page(), "thank-you.html": thanks_page(), "404.html": not_found_page(),
             "privacy.html": privacy_page()}
    for c in CITIES:
        pages[city_file(c)] = city_page(c)
    pages["blog.html"] = blog_index()
    for p in POSTS:
        pages[post_file(p)] = post_page(p)
    for name, src in pages.items():
        (out / name).write_text(src)
    indexable = (["", "weekly-pool-service", "service-areas", "contact", "blog"] + [city_file(c)[:-5] for c in CITIES]
                 + [post_file(p)[:-5] for p in POSTS])
    (out / "sitemap.xml").write_text(sitemap(indexable))
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BIZ['domain']}/sitemap.xml\n")
    (out / "_headers").write_text(HEADERS)
    print(f"{out.relative_to(ROOT)}/ ({theme}): {len(pages)} pages, {len(CITIES)} city pages, {len(POSTS)} posts, {sum(len(c['zips']) for c in CITIES)} zips")


def build_demos():
    if DEMOS.exists():
        shutil.rmtree(DEMOS)
    for key in DEMO_THEMES:
        build(key, DEMOS / key)
    (DEMOS / "index.html").write_text(demo_index())


def demo_index():
    cards = "".join(f"""<a class="d-card" href="{k}/index.html">
  <span class="d-swatch d-{k}"></span>
  <strong>{t['name']}</strong><span>{t['blurb']}</span></a>""" for k, t in ((k, THEMES[k]) for k in DEMO_THEMES))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SkyBlue Site Demos</title><meta name="robots" content="noindex">
<style>
:root{{--bg:#F4F8FB;--card:#fff;--ink:#0A2236;--muted:#4A6478;--line:#D8EAF2}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0B1620;--card:#13222F;--ink:#E7F2F8;--muted:#9FB6C6;--line:#24384A}}}}
:root[data-theme="dark"]{{--bg:#0B1620;--card:#13222F;--ink:#E7F2F8;--muted:#9FB6C6;--line:#24384A}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:1040px;margin:0 auto;padding:48px 16px}}h1{{font-size:clamp(1.7rem,4vw,2.4rem);margin:0 0 6px;text-wrap:balance}}
p{{color:var(--muted);margin:0 0 28px;max-width:62ch}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))}}
.d-card{{display:flex;flex-direction:column;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 14px 18px;color:inherit;text-decoration:none;transition:transform .15s}}
.d-card:hover{{transform:translateY(-2px)}}.d-card span:last-child{{color:var(--muted);font-size:.92rem}}
.d-swatch{{height:120px;border-radius:9px;margin-bottom:8px}}
.d-skyblue{{background:linear-gradient(180deg,#E3F7FC,#A7E3F2 70%,#0E7FB8 70%)}}
.d-california{{background:radial-gradient(circle at 70% 42%,#FFD25C 0 14%,transparent 15%),linear-gradient(180deg,#FFB38A,#FFD9B0 55%,#7CE6F3 55%,#2BA7D6)}}
.d-minimal{{background:linear-gradient(90deg,#fff 0 62%,#0E7FB8 62% 64%,#fff 64%);border:1px solid #E5E9EC}}
.d-nightswim{{background:radial-gradient(ellipse at 50% 110%,#7CE6F3 0,transparent 55%),linear-gradient(180deg,#06182A,#0B2B45)}}
.note{{margin-top:28px;font-size:.9rem}}
</style></head><body><main>
<h1>SkyBlue Pool Care site demos</h1>
<p>Same pages and copy in every version. Only the look changes. Yellow highlights are placeholders for Zach's details (price, rating, license, hours).</p>
<div class="grid">{cards}</div>
<p class="note">Each demo is the full site: home, weekly service, service areas, blog, contact and {len(CITIES)} city pages.</p>
</main></body></html>
"""


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else LIVE_THEME
    build_demos() if arg == "--demos" else build(arg)
