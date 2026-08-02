"""Literacy tips keyed by fraud label."""

from __future__ import annotations

TIPS: dict[str, dict[str, str]] = {
    "credential_harvest": {
        "en": "Never share your PIN or OTP. Real operators never ask for them by SMS.",
        "pt": "Nunca partilhe o seu PIN ou OTP. Operadores reais nunca os pedem por SMS.",
    },
    "phishing": {
        "en": "Open the official app instead of tapping links in unexpected messages.",
        "pt": "Abra a aplicação oficial em vez de clicar em links de mensagens inesperadas.",
    },
    "prize_scam": {
        "en": "Unexpected prizes are usually scams. Verify through official channels.",
        "pt": "Prémios inesperados são geralmente fraudes. Confirme por canais oficiais.",
    },
    "fake_agent": {
        "en": "Confirm agent identity in the official app before paying.",
        "pt": "Confirme a identidade do agente na app oficial antes de pagar.",
    },
    "short_link": {
        "en": "Avoid shortened links in money-related SMS. Type the official site yourself.",
        "pt": "Evite links encurtados em SMS sobre dinheiro. Escreva o site oficial.",
    },
    "account_threat": {
        "en": "Fear messages about locked accounts are common bait. Verify in-app only.",
        "pt": "Mensagens de conta bloqueada são isco comum. Verifique só na app.",
    },
    "refund_scam": {
        "en": "Refunds never require your PIN. Ignore SMS that ask for codes.",
        "pt": "Reembolsos nunca pedem PIN. Ignore SMS que pedem códigos.",
    },
    "social_redirect": {
        "en": "Move conversations to official channels; ignore WhatsApp PIN requests.",
        "pt": "Use canais oficiais; ignore pedidos de PIN no WhatsApp.",
    },
    "default": {
        "en": "When in doubt, stop and verify using the official app or helpline.",
        "pt": "Em caso de dúvida, pare e verifique pela app oficial ou linha de apoio.",
    },
}


def tip_for(labels: list[str], locale: str = "en") -> str:
    lang = "pt" if locale.startswith("pt") else "en"
    for label in labels:
        if label in TIPS:
            return TIPS[label][lang]
    return TIPS["default"][lang]
