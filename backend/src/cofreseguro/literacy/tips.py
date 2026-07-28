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
    "sim_swap": {
        "en": "SIM-swap alerts by SMS are often fake. Contact your operator from a trusted channel.",
        "pt": "Alertas de troca de SIM por SMS são muitas vezes falsos. Contacte o operador por canal fiável.",
    },
    "otp_forward": {
        "en": "Never forward OTPs. Anyone asking you to forward a code is a scammer.",
        "pt": "Nunca encaminhe OTPs. Quem pede para encaminhar um código é fraudulento.",
    },
    "airtime": {
        "en": "Free airtime offers that ask for PIN are scams. Top up only in the official app.",
        "pt": "Ofertas de saldo grátis que pedem PIN são fraude. Recarregue só na app oficial.",
    },
    "loan": {
        "en": "Instant loans that charge a fee before disbursement are usually traps.",
        "pt": "Empréstimos instantâneos que cobram taxa antes do desembolso são tipicamente armadilhas.",
    },
    "romance": {
        "en": "Romance pressure for money or PIN is a classic scam. Stop and verify independently.",
        "pt": "Pressão romântica por dinheiro ou PIN é fraude clássica. Pare e verifique de forma independente.",
    },
    "invoice": {
        "en": "Unexpected invoices with short links are phishing. Check bills inside official portals.",
        "pt": "Facturas inesperadas com links curtos são phishing. Confirme nas portais oficiais.",
    },
    "qr_hijack": {
        "en": "Do not scan unexpected QR codes for money moves. Prefer in-app payments.",
        "pt": "Não digitalize QR inesperados para movimentos de dinheiro. Prefira pagamentos na app.",
    },
    "family_emergency": {
        "en": "Verify family emergencies by calling known numbers, never numbers from the SMS.",
        "pt": "Confirme emergências familiares ligando para números conhecidos, nunca os do SMS.",
    },
    "job_offer": {
        "en": "Real employers do not charge registration fees by SMS or demand OTP.",
        "pt": "Empregadores reais não cobram taxa de inscrição por SMS nem pedem OTP.",
    },
    "crypto": {
        "en": "Never share seed phrases or private keys. Crypto giveaways are almost always scams.",
        "pt": "Nunca partilhe frases semente ou chaves privadas. Giveaways crypto são quase sempre fraude.",
    },
    "ussd": {
        "en": "Be careful with USSD codes from SMS. Prefer official app menus for sensitive actions.",
        "pt": "Cuidado com códigos USSD de SMS. Prefira menus oficiais da app para acções sensíveis.",
    },
    "brand_mz": {
        "en": "Mozambique brand lookalikes are common. Open the official app instead of SMS links.",
        "pt": "Imitações de marcas em Moçambique são comuns. Abra a app oficial em vez de links SMS.",
    },
    "brand_ao": {
        "en": "Angola brand lookalikes appear in SMS fraud. Verify inside the official app.",
        "pt": "Imitações de marcas em Angola aparecem em SMS. Verifique na app oficial.",
    },
    "urgency": {
        "en": "Urgency is a manipulation tactic. Pause before sending money or codes.",
        "pt": "Urgência é táctica de manipulação. Pause antes de enviar dinheiro ou códigos.",
    },
    "brand_mention": {
        "en": "Brand names in SMS do not prove legitimacy. Prefer the official app.",
        "pt": "Nomes de marca no SMS não provam legitimidade. Prefira a app oficial.",
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
