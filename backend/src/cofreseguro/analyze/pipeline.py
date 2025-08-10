"""Ensemble fraud analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from cofreseguro.analyze.llm_ollama import enrich_with_llm
from cofreseguro.analyze.ml_scorer import score_text
from cofreseguro.analyze.rules import evaluate_rules
from cofreseguro.analyze.url_score import score_urls_in_text
from cofreseguro.literacy.tips import tip_for


@dataclass
class AnalysisResult:
    risk_score: float
    risk_level: str
    labels: list[str]
    explanation: str
    tip: str
    engine: str
    url_scores: list[dict]


def _level(score: float) -> str:
    if score >= 0.85:
        return "critical"
    if score >= 0.65:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def _explain(locale: str, labels: list[str], score: float, engine: str) -> str:
    if locale.startswith("pt"):
        return (
            f"Pontuação de risco {score:.2f} ({_level(score)}) via {engine}. "
            f"Sinais: {', '.join(labels) if labels else 'nenhum padrão forte'}."
        )
    return (
        f"Risk score {score:.2f} ({_level(score)}) via {engine}. "
        f"Signals: {', '.join(labels) if labels else 'no strong patterns'}."
    )


async def analyze_text(text: str, locale: str = "en") -> AnalysisResult:
    rule_score, hits = evaluate_rules(text, locale)
    labels = [h.label for h in hits]
    ml = score_text(text)
    url_results = score_urls_in_text(text)
    url_boost = max((u.score for u in url_results), default=0.0)
    for u in url_results:
        labels.extend(u.reasons)
    fused = min(1.0, 0.45 * rule_score + 0.35 * ml.score + 0.35 * url_boost)
    level = _level(fused)
    engine = "rules+ml+url"
    explanation = _explain(locale, labels, fused, engine)
    llm_text = await enrich_with_llm(text, locale, level)
    if llm_text:
        explanation = llm_text
        engine = "rules+ml+url+llm"
    tip = tip_for(labels, locale)
    return AnalysisResult(
        risk_score=round(fused, 4),
        risk_level=level,
        labels=sorted(set(labels)),
        explanation=explanation,
        tip=tip,
        engine=engine,
        url_scores=[{"url": u.url, "score": u.score, "reasons": u.reasons} for u in url_results],
    )
