# Why CofreSeguro

CofreSeguro keeps the spirit of NDZALAMA IA–style mobile-money fraud shields and pushes
further on reliability and product depth.

| Capability | Typical hackathon demo | CofreSeguro |
|------------|------------------------|-------------|
| Detection | Often LLM-only | Rules + ML + URL + optional LLM |
| Offline AI | Breaks if model down | Rule/ML path always works |
| Languages | Often one locale | English + Portuguese |
| Links | Rarely scored | Short-link / fragment URL scorer |
| Images | Optional OCR talk track | `/v1/analyze/image` OCR stub |
| User risk | Per-message only | Behavioural profile counters |
| SDLC | Sparse | CI, Compose, Helm stub, threat model |

## Product principles

1. **Protect first** — never force a live LLM dependency for a demo or field trial.
2. **Explain scores** — every analysis returns labels, explanation, and a literacy tip.
3. **Ship like production** — auth, persistence, metrics, and docs are first-class.
