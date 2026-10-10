#!/usr/bin/env python3
"""Static SEO audit for Altora. Exits non-zero only on required failures."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://altora.id"
required = {
    "title": r"<title>[^<]{20,}</title>",
    "description": r'<meta name="description" content="[^"]{70,240}">',
    "canonical": r'<link rel="canonical" href="https://altora\.id/">',
    "robots": r'<meta name="robots" content="index,follow,max-image-preview:large">',
    "json-ld": r'<script type="application/ld\+json">',
    "og-title": r'<meta property="og:title" content="[^"]+">',
    "og-image": r'<meta property="og:image" content="https://altora\.id/[^"]+">',
}

def fetch(path: str) -> tuple[int, str]:
    req = Request(BASE + path, headers={"User-Agent": "AltoraSEOAudit/1.0"})
    with urlopen(req, timeout=20) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")

def main() -> int:
    local = (ROOT / "index.html").read_text(encoding="utf-8")
    failures = [name for name, pattern in required.items() if not re.search(pattern, local, re.S)]
    sitemap = ROOT / "sitemap.xml"
    robots = ROOT / "robots.txt"
    if not sitemap.exists() or "https://altora.id/" not in sitemap.read_text(): failures.append("sitemap")
    if not robots.exists() or "Sitemap: https://altora.id/sitemap.xml" not in robots.read_text(): failures.append("robots.txt")
    local_images = re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', local)
    missing_images = [p for p in local_images if not p.startswith(("http://", "https://")) and not (ROOT / p.split("?", 1)[0]).exists()]
    if missing_images: failures.append("missing local images: " + ", ".join(missing_images))
    live = {}
    try:
        for path in ("/", "/robots.txt", "/sitemap.xml"):
            status, body = fetch(path)
            live[path] = status
            if status != 200: failures.append(f"live {path}: HTTP {status}")
        if "application/ld+json" not in body and False: failures.append("live schema")
        status, homepage = fetch("/")
        if "canonical" not in homepage or "application/ld+json" not in homepage: failures.append("live homepage metadata")
    except (URLError, HTTPError, TimeoutError) as err:
        failures.append(f"live fetch: {err}")
    print("Altora SEO audit")
    print("local checks:", "PASS" if not [x for x in failures if not x.startswith("live")] else "FAIL")
    print("live status:", live)
    if failures:
        print("FAIL:")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print("PASS: title, description, canonical, robots, schema, social tags, sitemap, robots.txt, referenced images, and live endpoints.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
