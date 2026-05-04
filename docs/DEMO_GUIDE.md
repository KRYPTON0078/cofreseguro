# Demo guide

## 1. Start the API

```bash
cd backend
pip install -e ".[dev]"
uvicorn cofreseguro.main:app --reload --port 8080
```

## 2. Sign in

Use `demo@cofreseguro.app` / `demo123!` (seeded on startup).

## 3. Paste a fraud SMS

English example:

> URGENT: Your M-Pesa prize is waiting. Send your PIN now and click https://bit.ly/claim-now

Portuguese example:

> URGENTE: Ganhou um prémio M-Pesa. Envie o PIN e clique no link https://bit.ly/premio

Expect elevated `risk_level` (often `high` / `critical`), credential/phishing labels, and a tip.

## 4. Show history and tips

- `GET /v1/history` after a few analyses
- Flutter **Tips** tab for literacy content
- Optional: enable Ollama profile in Compose for narrative enrichment

## 5. Talking points

- Ensemble still works with `OLLAMA_ENABLED=false`
- EN + PT coverage for Southern/Eastern African and Lusophone users
- Behavioural risk rises as high-risk analyses accumulate
