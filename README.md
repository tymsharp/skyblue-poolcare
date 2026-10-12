# skyblue-poolcare.com

Static site for SkyBlue Pool Care. Same pattern as bjgdigital.com: plain HTML, one CSS file, deployed on Cloudflare Pages. Lead forms post into GoHighLevel.

## Pages (25)
- Home, Weekly Pool Service, Service Areas, Contact, Privacy, Thank You (noindex), 404.
- Blog index plus 4 posts, `blog-<slug>.html` (pricing, hard water, heat-wave green pools, winter service). Posts live in `POSTS` in `_build/content.py`; add one there and rebuild.
- 15 city pages, `pool-service-<city>.html`. All 74 service-area zips are listed on the city page that covers them. No per-zip pages, on purpose (doorway-page risk).
  - Valley: Calabasas & West Hills, Woodland Hills, Encino & Lake Balboa, Tarzana, Sherman Oaks & Van Nuys, Studio City & Toluca Lake, Northridge & Chatsworth, Porter Ranch & Granada Hills, Burbank.
  - Westside: Hollywood Hills & Los Feliz, West Hollywood, Beverly Hills & Bel Air, Brentwood & Pacific Palisades, Santa Monica & Venice, Culver City & Mar Vista.

## Edit and build
- Content: `_build/content.py` (business facts, services, FAQ, city pages and their zips).
- Layout: `_build/build.py`. Styles: `_build/base.css` + `_build/skyblue.css`.
- Zip neighborhoods: `data/service-area-zips.csv`.
```
python3 _build/build.py
```
Writes `public/`. Commit `public/` too, so Cloudflare needs no build step.

## Deploy on Cloudflare Pages
1. Workers & Pages > Create > Pages > Connect to Git > this repo.
2. Framework preset **None**. Build command **empty**. Output directory **`public`**.
3. Custom domain `skyblue-poolcare.com`, plus `www` with a 301 redirect rule to the apex.
4. Search Console: add the domain, submit `/sitemap.xml`, request indexing on the 15 city pages.

## Before launch (yellow `class="fill"` in the HTML)
- **Weekly starting price** (`price_from` in content.py) and whether chemicals are included.
- **One phone number.** Main site uses (310) 421-8863, the GHL page uses (213) 668-6131. Pick one; it must match the Google Business Profile.
- **Google rating and review count**, plus 1 real Google review per area if possible.
- **License and insurance** line, and hours (set to Mon to Sat 7 to 5 as a guess).
- Logo: the header uses a drawn wave mark. Swap in the real logo if wanted.
- GHL webhook URL: see `GHL-SETUP.md`.
- Testimonials (Daisy S., Steven W.) and claims (photo report, no skipped cleanings, 21-point inspection, no contract, 35+ years combined) come from Skyblue's current site.
