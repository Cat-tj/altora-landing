#!/usr/bin/env python3
"""Static SEO audit for Altora. Exits non-zero only on required failures; AI-crawler access is reported as a warning."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://altora.id"


def tag(s: str, name: str, attr: str, value: str) -> str | None:
    """First <name ...> tag whose `attr` equals `value`, regardless of attribute order."""
    for m in re.finditer(rf"<{name}\b[^>]*>", s, re.I):
        if re.search(rf'\b{attr}="{re.escape(value)}"', m.group(0)):
            return m.group(0)
    return None


def content(t: str | None, attr: str = "content") -> str:
    m = re.search(rf'\b{attr}="([^"]*)"', t or "")
    return m.group(1) if m else ""


# name -> check(html) ; each returns True when the page passes
required = {
    "title": lambda s: bool(re.search(r"<title>[^<]{20,}</title>", s)),
    "description": lambda s: 70 <= len(content(tag(s, "meta", "name", "description"))) <= 240,
    "canonical": lambda s: content(tag(s, "link", "rel", "canonical"), "href") == BASE + "/",
    "robots": lambda s: content(tag(s, "meta", "name", "robots")) == "index,follow,max-image-preview:large",
    "json-ld": lambda s: '<script type="application/ld+json"' in s,
    "og-title": lambda s: bool(content(tag(s, "meta", "property", "og:title"))),
    "og-image": lambda s: content(tag(s, "meta", "property", "og:image")).startswith(BASE + "/"),
}

# Bots that decide whether AI assistants can learn about / cite Altora.
AI_BOTS = {
    "GPTBot": "Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)",
    "OAI-SearchBot": "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)",
    "ClaudeBot": "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)",
    "PerplexityBot": "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "CCBot": "CCBot/2.0 (https://commoncrawl.org/faq/)",
}
AI_ROBOTS = ("GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended", "meta-externalagent", "CCBot")


def fetch(path: str, ua: str = "AltoraSEOAudit/1.0") -> tuple[int, str]:
    req = Request(BASE + path, headers={"User-Agent": ua})
    try:
        with urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except HTTPError as err:
        return err.code, ""


def robots_blocked(robots: str) -> list[str]:
    """User-agents that robots.txt disallows from the whole site."""
    blocked, agents, in_rules = [], [], False
    for line in robots.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, val = (x.strip() for x in line.split(":", 1))
        if key.lower() == "user-agent":
            if in_rules:
                agents, in_rules = [], False
            agents.append(val)
        else:
            in_rules = True
            if key.lower() == "disallow" and val == "/":
                blocked += agents
    return blocked


def main() -> int:
    local = (ROOT / "index.html").read_text(encoding="utf-8")
    failures = [name for name, check in required.items() if not check(local)]
    warnings: list[str] = []
    sitemap = ROOT / "sitemap.xml"
    robots = ROOT / "robots.txt"
    if not sitemap.exists() or "https://altora.id/" not in sitemap.read_text(): failures.append("sitemap")
    if not robots.exists() or "Sitemap: https://altora.id/sitemap.xml" not in robots.read_text(): failures.append("robots.txt")
    local_images = re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', local)
    missing_images = sorted({p for p in local_images if not p.startswith(("http://", "https://", "data:"))
                             and not (ROOT / p.split("?", 1)[0].lstrip("/")).exists()})
    if missing_images: failures.append("missing local images: " + ", ".join(missing_images))
    live = {}
    try:
        for path in ("/", "/robots.txt", "/sitemap.xml", "/llms.txt"):
            status, body = fetch(path)
            live[path] = status
            if status != 200: failures.append(f"live {path}: HTTP {status}")
            if path == "/" and ("canonical" not in body or "application/ld+json" not in body):
                failures.append("live homepage metadata")
            if path == "/robots.txt":
                blocked = [b for b in AI_ROBOTS if b in robots_blocked(body)]
                if blocked: warnings.append("robots.txt live blocks AI crawlers: " + ", ".join(blocked))
        denied = [name for name, ua in AI_BOTS.items() if fetch("/", ua)[0] != 200]
        if denied: warnings.append("AI crawlers denied by firewall (non-200): " + ", ".join(denied))
    except (URLError, TimeoutError) as err:
        failures.append(f"live fetch: {err}")
    print("Altora SEO audit")
    print("local checks:", "PASS" if not [x for x in failures if not x.startswith("live")] else "FAIL")
    print("live status:", live)
    for w in warnings:
        print("WARN:", w)
    if failures:
        print("FAIL:")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print("PASS: title, description, canonical, robots, schema, social tags, sitemap, robots.txt, referenced images, and live endpoints.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
