# Evaluation

Lightweight offline scoring over `datasets/en` and `datasets/pt`.

```bash
python scripts/evaluate_corpus.py
```

Reports precision/recall-style counts for fraud vs ham using the ensemble
(rules + ML + URL) without requiring Ollama.
