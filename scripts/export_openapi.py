#!/usr/bin/env python3
"""Export OpenAPI JSON snapshot."""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))
from cofreseguro.main import create_app
app = create_app()
out = ROOT / "docs" / "api" / "openapi.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(app.openapi(), indent=2) + "\n", encoding="utf-8")
print("wrote", out)
