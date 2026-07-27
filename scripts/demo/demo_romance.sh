#!/usr/bin/env bash
set -euo pipefail
API=${API:-http://localhost:8080}
TOKEN=$(curl -s -X POST "$API/v1/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"demo@cofreseguro.app","password":"demo123!"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
curl -s -X POST "$API/v1/analyze" -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"text":"DEMO romance urgent PIN OTP https://bit.ly/romance","locale":"en"}' | python3 -m json.tool
