# Threat model (lightweight)

## Assets

- User credentials and JWTs
- Analysis history (SMS text may contain sensitive content)
- Behavioural risk profiles
- Signing secrets (`JWT_SECRET`)

## Trust boundaries

- Mobile/web client → API (HTTPS in production; JWT bearer)
- API → database
- API → optional Ollama (local network; never required for core scoring)

## Key threats and mitigations

| Threat | Mitigation |
|--------|------------|
| Credential stuffing | Bcrypt password hashes; rate-limit at gateway in prod |
| JWT theft | Short expiry; rotate `JWT_SECRET`; HTTPS only in prod |
| Prompt injection via SMS text | LLM is optional enrichment only; rules/ML decide score |
| Data leakage in logs | Structured logs avoid full message dumps by default |
| Supply-chain / dependency risk | Pin CI Python; review critical deps |
| Over-trusting OCR | Image path clearly marks OCR unavailability |

## Out of scope

- Live M-Pesa operator API integration
- Guaranteed fraud adjudication / legal evidence chain
- Attacking real users or third-party systems

## Residual risk

Local demos ship with default secrets — change before any shared deployment.
