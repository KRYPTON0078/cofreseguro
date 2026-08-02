# Deploy on Android and PC

## 1. Start API

```bash
./scripts/demo-up.sh
# or: cd backend && uvicorn cofreseguro.main:app --host 0.0.0.0 --port 8080
```

## 2. Android APK

```bash
./scripts/build-android.sh
# Install: adb install -r mobile/build/app/outputs/flutter-apk/app-release.apk
```

In **Settings**, set API base:
- Emulator: `http://10.0.2.2:8080`
- Physical phone: `http://<your-pc-lan-ip>:8080`

## 3. PC via Web (recommended for demos)

```bash
./scripts/build-web.sh
cd mobile/build/web && python -m http.server 9090
```

Open `http://localhost:9090` and set API base to `http://localhost:8080`.

## 4. PC Linux desktop

```bash
./scripts/build-linux.sh
```

## 5. PC Windows

Download the **cofreseguro-windows** artifact from GitHub Actions, or build on Windows:

```bat
cd mobile
flutter build windows --release --dart-define=API_BASE=http://127.0.0.1:8080
```
