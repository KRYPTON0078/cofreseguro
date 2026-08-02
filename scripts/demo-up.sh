#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
docker compose up --build -d
echo "API: http://localhost:8080/docs"
echo "Demo user: demo@cofreseguro.app / demo123!"
echo "Android emulator API_BASE=http://10.0.2.2:8080"
echo "Physical phone: use your PC LAN IP, e.g. http://192.168.x.x:8080"
