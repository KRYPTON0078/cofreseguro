#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/mobile"
API_BASE="${API_BASE:-http://localhost:8080}"
flutter pub get
flutter build web --release --dart-define=API_BASE="$API_BASE"
echo "Web build: $ROOT/mobile/build/web"
