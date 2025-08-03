# CofreSeguro

**Mobile-money fraud shield** — analyse SMS/text and links, score risk with an ensemble
(rules + ML + optional local LLM), and deliver bilingual financial-literacy tips.

> Built to recreate and surpass hackathon-grade mobile-money AI guards (e.g. NDZALAMA IA style demos)
> with production engineering practices.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, JWT, SQLAlchemy |
| Database | PostgreSQL (SQLite local fallback) |
| AI | Ollama/Llama optional + rule/ML fallback |
| Client | Flutter (iOS / Android / Web) |

## Quick start (backend)

```bash
cd backend
pip install -e ".[dev]"
uvicorn cofreseguro.main:app --reload --port 8080
```

## Demo credentials

| User | Password |
|------|----------|
| demo@cofreseguro.app | demo123! |
| admin@cofreseguro.app | admin123! |

## Docs

See [docs/](docs/) for architecture, threat model, and demo guide.
