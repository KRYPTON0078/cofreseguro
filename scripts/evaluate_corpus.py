#!/usr/bin/env python3
"""Evaluate ensemble on EN/PT datasets."""
from __future__ import annotations
import asyncio, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))
from cofreseguro.analyze.pipeline import analyze_text

async def main() -> None:
    tp=fp=tn=fn=0
    for loc in ("en","pt"):
        for path in sorted((ROOT/"datasets"/loc).glob("sample_*.json")):
            row=json.loads(path.read_text())
            y = 1 if row.get("label")=="fraud" else 0
            res = await analyze_text(row["text"], row.get("locale","en"))
            pred = 1 if res.risk_level in {"medium","high","critical"} else 0
            if pred==1 and y==1: tp+=1
            elif pred==1 and y==0: fp+=1
            elif pred==0 and y==0: tn+=1
            else: fn+=1
    prec = tp/max(tp+fp,1); rec=tp/max(tp+fn,1)
    print({"tp":tp,"fp":fp,"tn":tn,"fn":fn,"precision":round(prec,3),"recall":round(rec,3)})

if __name__ == "__main__":
    asyncio.run(main())
