#!/usr/bin/env python3
"""Build and score a public-business outreach queue for Altora.

Input is a manually/API-collected CSV of public business contacts. This tool
normalizes, deduplicates, scores fit, and writes a review queue. It never sends
email or WhatsApp messages.
"""
from __future__ import annotations
import argparse, csv, re
from pathlib import Path
from urllib.parse import urlparse

FIELDS = [
    "company", "city", "vertical", "website", "public_email", "public_phone",
    "source_url", "notes", "fit_score", "recommended_offer", "status"
]
CITY_WEIGHT = {"balikpapan": 15, "samarinda": 15}
VERTICALS = {
    "logistics": (35, "Fleet management, telematics, dan command center"),
    "transport": (35, "Fleet management, telematics, dan command center"),
    "mining": (35, "AI CCTV safety, sensor, dan command center"),
    "contractor": (32, "AI CCTV safety, sensor, dan command center"),
    "warehouse": (30, "CCTV safety, smart access, dan hardware"),
    "manufacturing": (30, "HRIS, safety sensor, dan system integration"),
    "distributor": (28, "Altora POS/ERP roadmap dan software custom"),
    "retail": (25, "Altora POS roadmap, HRIS, dan software custom"),
    "f&b": (25, "Altora POS roadmap, HRIS, dan software custom"),
    "hotel": (28, "Smart access, CCTV, dan HRIS"),
    "property": (28, "Smart access, CCTV, dan sensor safety"),
    "education": (25, "HRIS, smart access, dan custom system"),
    "healthcare": (25, "HRIS, smart access, dan custom system"),
}

def norm(v: str) -> str:
    return re.sub(r"\s+", " ", (v or "").strip())

def domain(url: str) -> str:
    u = norm(url)
    if not u: return ""
    if not re.match(r"https?://", u): u = "https://" + u
    return urlparse(u).netloc.lower().removeprefix("www.")

def score(row: dict) -> tuple[int, str]:
    city = norm(row.get("city")).lower()
    vert = norm(row.get("vertical")).lower()
    base = CITY_WEIGHT.get(city, 0)
    for k, (points, offer) in VERTICALS.items():
        if k in vert:
            base += points
            suggested = offer
            break
    else:
        suggested = "Software custom, integrasi, atau konsultasi teknologi"
        base += 12
    if norm(row.get("website")): base += 10
    if norm(row.get("public_email")): base += 20
    if norm(row.get("public_phone")): base += 10
    if norm(row.get("source_url")): base += 5
    return min(base, 100), suggested

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path, default=Path("leads/outreach_queue.csv"))
    args = ap.parse_args()
    rows = list(csv.DictReader(args.input.open(encoding="utf-8-sig")))
    seen, out = set(), []
    for raw in rows:
        row = {k: norm(raw.get(k, "")) for k in FIELDS}
        if not row["company"] or row["city"].lower() not in CITY_WEIGHT: continue
        key = (domain(row["website"]) or row["public_email"].lower() or row["company"].lower(), row["city"].lower())
        if key in seen: continue
        seen.add(key)
        row["fit_score"], row["recommended_offer"] = score(row)
        row["status"] = "review"
        out.append(row)
    out.sort(key=lambda x: int(x["fit_score"]), reverse=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(out)
    print(f"Wrote {len(out)} deduplicated public-business leads to {args.out}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
