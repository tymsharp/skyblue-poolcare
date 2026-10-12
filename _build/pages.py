"""Build the client-facing demo preview tree (demo-host/).

    python3 _build/build.py --demos     # demos/<theme>/ first
    python3 _build/pages.py             # then demo-host/

demo-host/ is a plain static tree: the picker page and its screenshots
(from _build/previews/) plus site/<theme>/ for each demo. It is committed
as the orphan `gh-pages` branch of tymsharp/skyblue-poolcare:

    cd demo-host && git init -q -b gh-pages && git add -A \
      && git commit -q -m "Demo previews" \
      && git push -f https://github.com/tymsharp/skyblue-poolcare.git gh-pages

Hosting on Cloudflare (the branch carries a wrangler.jsonc, so no build step):

  * Workers, from any checkout of the branch:  npx wrangler deploy
    -> https://skyblue-demo.<account>.workers.dev
  * Or in the Cloudflare dashboard: Workers & Pages > Create > Pages >
    Connect to Git > tymsharp/skyblue-poolcare, production branch gh-pages,
    no build command, output directory "/".

GitHub Pages also serves the same branch at
https://tymsharp.github.io/skyblue-poolcare/ until the branch is deleted.

Every page gets a noindex tag, _headers adds X-Robots-Tag: noindex on
Cloudflare, and robots.txt disallows crawling, so the previews never
compete with the real site in search.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEMOS = ROOT / "demos"
OUT = ROOT / "demo-host"
NOINDEX = '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">'
SKIP = {"sitemap.xml", "robots.txt", "_headers", "index.html"}

HEADERS = """/*
  X-Robots-Tag: noindex, nofollow
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
"""

WRANGLER = """{
  // Cloudflare Worker serving this folder as static assets.
  // Deploy from a checkout of the gh-pages branch:  npx wrangler deploy
  "name": "skyblue-demo",
  "compatibility_date": "2026-09-01",
  "assets": { "directory": "./", "html_handling": "auto-trailing-slash" }
}
"""

ASSETSIGNORE = "wrangler.jsonc\n.assetsignore\n.git\n"


def copy_page(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix == ".html":
        html = src.read_text()
        if 'name="robots"' not in html:
            html = html.replace('<meta charset="utf-8">', NOINDEX, 1)
        dst.write_text(html)
    else:
        shutil.copy(src, dst)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for p in (HERE / "previews").iterdir():
        copy_page(p, OUT / p.name)
    n = 0
    for theme in sorted(d for d in DEMOS.iterdir() if d.is_dir()):
        for p in theme.rglob("*"):
            if p.is_file() and p.name not in SKIP or p.name == "index.html" and p.parent == theme:
                copy_page(p, OUT / "site" / theme.name / p.relative_to(theme))
                n += p.suffix == ".html"
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    (OUT / "_headers").write_text(HEADERS)
    (OUT / "wrangler.jsonc").write_text(WRANGLER)
    (OUT / ".assetsignore").write_text(ASSETSIGNORE)
    (OUT / ".nojekyll").write_text("")
    print(f"demo-host/: picker + {n} demo pages, all noindex")


if __name__ == "__main__":
    build()
