# Diccionarios de señales multilingüe (ES/PT) para ConversaSense AI

SIGNALS = {
    "es": {
        "fallback": [
            r"no he? entendi(do)?",
            r"no he? comprendi(do)?",
            r"disculpa,? no te entend[íi]",
            r"puedes repetir",
            r"lo siento,? no encontr[ée]"
        ],
        "apology": [
            r"lo siento",
            r"disculpa",
            r"perd[óo]n",
            r"lamento"
        ],
        "reboot": [
            r"¿qu[ée] te gustar[íi]a hacer\?",
            r"men[úu] principal",
            r"¿en qu[ée] m[áa]s puedo ayudarte\?",
            r"¿puedo ayudarte en algo m[áa]s\?"
        ],
        "capability_error": [
            r"no puedo (ayudarte|hacer eso)",
            r"no tengo (acceso|informaci[óo]n)",
            r"fuera de mi alcance"
        ],
        "profanity": [
            # Lista simplificada para el MVP
            r"mierda", r"puto", r"puta", r"pendejo", r"est[úu]pido", r"carajo"
        ],
        "negation": [
            r"\bno\b", r"nunca", r"jam[áa]s", r"tampoco"
        ],
        "escalation": [
            r"agente", r"humano", r"persona", r"hablar con alguien", r"operador"
        ]
    },
    "pt": {
        "fallback": [
            r"n[ãa]o entendi",
            r"n[ãa]o compreendi",
            r"desculpe,? n[ãa]o entendi",
            r"pode repetir",
            r"sinto muito,? n[ãa]o encontrei"
        ],
        "apology": [
            r"sinto muito",
            r"desculpe",
            r"perd[ãa]o",
            r"lamento"
        ],
        "reboot": [
            r"o que (voc[êe]|você) gostaria de fazer\?",
            r"menu principal",
            r"como posso te ajudar mais\?",
            r"posso ajudar em algo mais\?"
        ],
        "capability_error": [
            r"n[ãa]o posso (ajudar|fazer isso)",
            r"n[ãa]o tenho (acesso|informa[çc][ãa]o)"
        ],
        "profanity": [
            r"merda", r"porra", r"caralho", r"puta", r"est[úu]pido"
        ],
        "negation": [
            r"\bn[ãa]o\b", r"nunca", r"jamais", r"nem"
        ],
        "escalation": [
            r"atendente", r"humano", r"pessoa", r"falar com algu[ée]m", r"operador"
        ]
    }
}
