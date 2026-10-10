#!/usr/bin/env python3
"""Collect public businesses from OpenStreetMap for Altora outreach research.

Uses Overpass only; retains organization details published in OSM. It does not
collect personal contacts and never sends messages.
"""
from __future__ import annotations
import csv, json, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT = Path("leads/osm_public_business_leads.csv")
CITIES = ["Balikpapan", "Samarinda"]
# Broad enough to identify organizations, but outreach later is limited to
# contacts expressly published by the organization.
QUERY = '''[out:json][timeout:120];
area["name"="{city}"]["boundary"="administrative"]->.a;
(
  nwr["office"](area.a);
  nwr["industrial"](area.a);
  nwr["shop"](area.a);
  nwr["tourism"~"hotel|guest_house"](area.a);
  nwr["amenity"~"hospital|clinic|school|university|college"](area.a);
  nwr["craft"](area.a);
);
out center tags;'''
FIELDS = ["company","city","vertical","website","public_email","public_phone","source_url","notes"]

def fetch(city: str) -> list[dict]:
    data = urlencode({"data": QUERY.format(city=city)}).encode()
    req = Request("https://overpass-api.de/api/interpreter", data=data, headers={"User-Agent":"AltoraLeadResearch/1.0"})
    with urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode()).get("elements", [])

def vertical(t: dict) -> str:
    return t.get("industrial") or t.get("office") or t.get("craft") or t.get("shop") or t.get("tourism") or t.get("amenity") or "business"

def main() -> int:
    all_rows, seen = [], set()
    for city in CITIES:
        for e in fetch(city):
            t = e.get("tags", {})
            name = (t.get("name") or "").strip()
            if not name: continue
            website = t.get("website") or t.get("contact:website") or ""
            email = t.get("email") or t.get("contact:email") or ""
            phone = t.get("phone") or t.get("contact:phone") or ""
            key = (name.lower(), city.lower(), website.lower())
            if key in seen: continue
            seen.add(key)
            all_rows.append({
                "company":name, "city":city, "vertical":vertical(t), "website":website,
                "public_email":email, "public_phone":phone,
                "source_url":f"https://www.openstreetmap.org/{e.get('type')}/{e.get('id')}",
                "notes":"Public business listing from OpenStreetMap; validate fit and contact channel before outreach."
            })
        time.sleep(1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(all_rows)
    print(f"Collected {len(all_rows)} public OSM business listings → {OUT}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
