#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/mobile"
API_BASE="${API_BASE:-http://10.0.2.2:8080}"
flutter pub get
flutter build apk --release --dart-define=API_BASE="$API_BASE"
echo "APK: $ROOT/mobile/build/app/outputs/flutter-apk/app-release.apk"
