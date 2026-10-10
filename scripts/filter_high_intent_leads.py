#!/usr/bin/env python3
"""Create a compact, high-intent review queue from scored public OSM leads."""
from __future__ import annotations
import csv
from pathlib import Path

src=Path('leads/outreach_queue.csv')
out=Path('leads/high_intent_review_queue.csv')
priority={
 'logistics','transport','mining','contractor','warehouse','manufacturing',
 'distributor','retail','f&b','hotel','property','education','healthcare',
 'company','telecommunication','supermarket','hospital','clinic'
}
rows=list(csv.DictReader(src.open(encoding='utf-8')))
selected=[]
for r in rows:
    v=r['vertical'].lower()
    if v not in priority: continue
    if not (r['website'] or r['public_email'] or r['public_phone']): continue
    selected.append(r)
# Keep targetable prospects; outbound requires later verification that the
# channel is a company-published business channel.
selected.sort(key=lambda r:(-int(r['fit_score']), r['city'],r['company'].lower()))
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=selected[0].keys() if selected else csv.DictReader(src.open()).fieldnames)
    w.writeheader();w.writerows(selected)
print(f'Wrote {len(selected)} high-intent public listings → {out}')
for r in selected[:20]:
    print(f"{r['fit_score']:>3} | {r['city']:<10} | {r['vertical']:<15} | {r['company']}")
