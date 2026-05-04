# CofreSeguro

**Mobile-money fraud shield** — analyse SMS/text and links, score risk with an ensemble
(rules + ML + optional local LLM), and deliver bilingual financial-literacy tips (EN + PT).

Built to recreate and surpass hackathon-grade mobile-money AI guards (NDZALAMA IA–style demos)
with production engineering practices: JWT auth, history, behavioural risk, CI, Compose, and a Helm stub.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, JWT, SQLAlchemy (async) |
| Database | PostgreSQL (SQLite local fallback) |
| AI | Ollama/Llama optional + rule/ML fallback |
| Client | Flutter (iOS / Android / Web) |
| Ops | Docker Compose, GitHub Actions, Prometheus metrics, Helm stub |

## Quick start (backend)

```bash
cd backend
pip install -e ".[dev]"
uvicorn cofreseguro.main:app --reload --port 8080
```

Or with Compose:

```bash
docker compose up --build
```

Open API docs at `http://localhost:8080/docs`.

## Demo credentials

| User | Password |
|------|----------|
| demo@cofreseguro.app | demo123! |
| admin@cofreseguro.app | admin123! |

## Try an analysis

```bash
TOKEN=$(curl -s -X POST http://localhost:8080/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@cofreseguro.app","password":"demo123!"}' | jq -r .access_token)

curl -s -X POST http://localhost:8080/v1/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"text":"URGENT: send your M-Pesa PIN to claim prize https://bit.ly/x","locale":"en"}'
```

## Flutter client

```bash
cd mobile
flutter pub get
flutter run -d chrome   # or android / ios
```

Point the API base URL at your machine (default `http://localhost:8080`).

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Why CofreSeguro](docs/WHY_COFRESEGURO.md)
- [Demo guide](docs/DEMO_GUIDE.md)
- [API reference](docs/API_REFERENCE.md)

## License

MIT — see [LICENSE](LICENSE).
