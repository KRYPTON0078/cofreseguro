# CofreSeguro

**Mobile-money fraud shield** — analyse SMS/text and links, score risk with an ensemble
(rules + ML + URL + optional local LLM), and deliver bilingual financial-literacy tips (EN + PT).

## Demo credentials

| User | Password |
|------|----------|
| demo@cofreseguro.app | demo123! |
| admin@cofreseguro.app | admin123! |

## Quick start (API)

```bash
./scripts/demo-up.sh
# API docs: http://localhost:8080/docs
```

Local without Docker:

```bash
cd backend && pip install -e ".[dev]"
uvicorn cofreseguro.main:app --host 0.0.0.0 --port 8080
```

## Show on Android + PC

See **[docs/DEPLOY_ANDROID_PC.md](docs/DEPLOY_ANDROID_PC.md)** for APK, Web, Linux, and Windows deliverables.

```bash
./scripts/build-android.sh   # APK
./scripts/build-web.sh       # PC browser demo
./scripts/build-linux.sh     # Linux desktop
```

Flutter Settings → API base URL (emulator `http://10.0.2.2:8080`).

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, JWT, SQLAlchemy, YAML policies |
| Database | PostgreSQL (Compose) / SQLite local |
| AI | Rules + fitted lite ML + URL policies + optional Ollama |
| Client | Flutter (Android / Web / Linux / Windows) |
| Ops | Docker Compose, Helm, GitHub Actions artifacts |

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Why CofreSeguro](docs/WHY_COFRESEGURO.md)
- [Demo guide](docs/DEMO_GUIDE.md)
- [Evaluation](docs/EVALUATION.md)
- [Deploy Android/PC](docs/DEPLOY_ANDROID_PC.md)
