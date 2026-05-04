# Architecture

CofreSeguro analyses suspicious mobile-money messages and returns a risk score, labels,
explanation, and a financial-literacy tip — in English or Portuguese.

```text
Flutter client
    |  JWT
    v
FastAPI (auth / analyze / history / metrics)
    |
    +-- Rule engine (EN + PT patterns)
    +-- Lightweight ML scorer
    +-- URL reputation scorer
    +-- OCR stub (image paste path)
    +-- Optional Ollama/Llama enrichment
    +-- Behavioural risk profile updater
    |
    v
PostgreSQL (or SQLite locally)
```

## Request path

1. Client authenticates via `POST /v1/auth/login` and receives a JWT.
2. Client submits text (or image) to `POST /v1/analyze`.
3. Ensemble fuses rule hits, ML score, and URL boost into `risk_score` / `risk_level`.
4. Result is persisted; behavioural counters update; tip is selected from literacy bank.
5. History is available at `GET /v1/history`.

## Design choices

- **Ensemble over LLM-only** — works when Ollama is offline (`OLLAMA_ENABLED=false`).
- **SQLite fallback** — zero-infra local demos; Compose uses Postgres 16.
- **Bilingual rules** — PT patterns plus EN fallback for mixed messages.
- **Metrics** — Prometheus text at `/metrics` for scrape-friendly ops demos.
