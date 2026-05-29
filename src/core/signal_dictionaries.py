# Diccionarios de señales multilingüe (ES/PT) para ConversaSense AI
# Enriquecido mediante Gemini Deep Research y términos adicionales de alta fricción transaccional.

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
            # Vulgaridades, agresividad implícita y términos de frustración aguda (ES)
            r"mierda", r"puto", r"puta", r"pendejo", r"est[úu]pido", r"carajo",
            r"harto", r"pesimo", r"basura", r"porquer[ií]a", r"estafa", r"fraude", r"robo", r"lamentable", r"vergonzoso", r"in[uú]t[ií]l",
            r"\b(?:p[eé]s[ií]mo\s+serv[ií]c[ií]o|me\s+est[aá]n?\s+tomando\s+el\s+pelo|es\s+un\s+ch[ií]ste|vaya\s+(?:ayuda|basura|porquer[ií]a)|estafador(?:es)?|g[ií]l[ií]pollas|v[eé]te\s+a\s+fre[ií]r\s+esp[aá]rragos|una\s+polla\s+en\s+v[ií]nagre|hasta\s+los\s+(?:huevos|cojones|pelotas|catapl[ií]nes)|me\s+cago\s+en|p[ií]nche|no\s+mames|ch[ií]nga(?:r|te|\s+tu)?|val[ií][oó]\s+verga|pendejo[as]?|la\s+concha\s+de|boludo[as]?|pelotudo[as]?|h[ií]jueputa|gonorrea|huev[oó]n|carajo|m[ií]erda|por\s+la\s+puta\s+madre)\b"
        ],
        "negation": [
            # Negaciones, resignación, problemas de software y frustración pasivo-agresiva/sarcástica (ES)
            r"\bno\b", r"nunca", r"jam[áa]s", r"tampoco",
            r"no funciona", r"da error", r"no me deja", r"no entra", r"no puedo", r"falla", r"bucle", r"loop",
            r"\b(?:no\s+me\s+s[ií]rve|deja\s+as[ií]|no\s+es\s+eso|olv[ií]dalo|otra\s+vez\s+con\s+lo\s+m[ií]smo|no\s+ent[ií]endes\s+nada|as[ií]\s+no\s+se\s+puede|decepcionado[as]?|no\s+entiend[es|e]|corta\s+el\s+rollo|es\s+un\s+rollo|no\s+sirve\s+para\s+nada|me\s+rindo|ya\s+para\s+qu[eé]|deja\s+de\s+escribir|eres\s+in[uú]t[ií]l|vuelve\s+a\s+ti\s+mismo)\b",
            r"\b(?:(?:gen[ií]al|excelente|marav[ií]llosa|buen[ií]s[ií]ma|l[ií]nda|gran)\s+(?:ayuda|atenc[ií][oó]n|serv[ií]c[ií]o)\s*(?:\(sarc[aá]st[ií]co\)\s*)?|grac[ií]as\s+por\s+nada|(?:s[uú]per|gen[ií]al|excelente)\s*,\s*(?:me\s+bloquearon|me\s+estafaron|me\s+bloqueaste|no\s+func[ií]ona|un\s+desastre|otra\s+traba|otra\s+tonter[ií]a|me\s+bloqueasteis|vaya\s+jefe|qu[eé]\s+jefazo))\b"
        ],
        "escalation": [
            # Solicitudes de transferencia humana implícitas, directas y derivaciones de soporte (ES)
            r"agente", r"humano", r"persona", r"hablar con alguien", r"operador",
            r"p[aá]same con", r"transfi[eé]reme", r"derivame", r"hablar con soporte", r"ayuda humana", r"contacto telef[oó]nico",
            r"\b(?:alg[uú]i[eé]n\s+real|con\s+una\s+persona|que\s+me\s+atienda\s+alg[uú]i[eé]n|con\s+un\s+superv[ií]sor|tel[eé]fono\s+de\s+soporte|as[ií]stenc[ií]a\s+de\s+verdad|atenc[ií][oó]n\s+humana|soporte\s+humano|hablar\s+con\s+humano|con\s+un\s+humano|atenci[oó]n\s+espec[ií]al[ií]zada|atendente\s+de\s+carne\s+y\s+hueso|asesor\s+verdadero)\b"
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
            # Vulgaridades, agresividad implícita y términos de frustración aguda (PT)
            r"merda", r"porra", r"caralho", r"puta", r"est[úu]pido",
            r"harto", r"pessimo", r"lixo", r"porcaria", r"fraude", r"roubo", r"in[uú]t[ií]l", r"vergonhoso", r"lament[aá]vel",
            r"\b(?:palha[cç]ada|est[aã]o\s+me\s+t[ií]rando|que\s+p[ií]ada|p[eé]ss[ií]mo\s+serv[ií][cç]o|br[ií]ncade[ií]ra|pelas\s+barbas\s+do\s+profeta|macacos\s+me\s+mordam|f[ií]car\s+p\s+da\s+v[ií]da|merda|puta\s+que\s+par[ií]u|pqp|caralho|v[aã]o\s+se\s+foder|bosta|desgra[cç]a|f[ií]lho\s+da\s+puta|[ií]mbe[cç][ií]l|[ií]d[ií]ota)\b"
        ],
        "negation": [
            # Negaciones, resignación, problemas de software y frustración pasivo-agresiva/sarcástica (PT)
            r"\bn[ãa]o\b", r"nunca", r"jamais", r"nem",
            r"n[ãa]o funciona", r"d[aá] erro", r"n[ãa]o entra", r"n[ãa]o consigo", r"falha", r"n[ãa]o posso",
            r"\b(?:de[ií]xa\s+pra\s+l[aá]|n[aã]o\s+ad[ií]anta|esquece|de\s+novo\s+i[s|ss]o|voc[eê]\s+n[aã]o\s+entende|n[aã]o\s+serve|t[ií]rar\s+o\s+caval[ií]nho\s+da\s+chuva|ver\s+nav[ií]os|chatead[oa]|morgad[oa]|magoad[oa]|aborrec[ií]d[oa]|[ií]rr[ií]tad[oa]|abusad[oa]|zangad[oa]|enjeitad[oa]|enjoado[as]?|n[aã]o\s+func[ií]ona|des[ií]sto|canse[ií])\b",
            r"\b(?:(?:[oó]t[ií]ma?|marav[ií]lhosa?|l[ií]nda?|excelente)\s+(?:ajuda|atend[ií]mento|suporte|serv[ií][cç]o)\s*(?:\([ií]r[oó]n[ií]co\)\s*)?|obrigad[oa]\s+por\s+nada|(?:[oó]t[ií]mo|marav[ií]lha|l[ií]ndo)\s*,\s*(?:me\s+bloquearam|me\s+bloqueou|n[aã]o\s+func[ií]ona|perdi\s+meu\s+acesso|que\s+beleza)|parab[eé]ns\s+pelo\s+p[eé]ss[ií]mo)\b"
        ],
        "escalation": [
            # Solicitudes de transferencia humana implícitas, directas y derivaciones de soporte (PT)
            r"atendente", r"humano", r"pessoa", r"falar com algu[ée]m", r"operador",
            r"passa para", r"transfere", r"falar com atendente", r"falar com suporte", r"ajuda humana",
            r"\b(?:algu[eé]m\s+de\s+verdade|falar\s+com\s+pessoa|atendente\s+real|ajuda\s+humana|atend[ií]mento\s+espec[ií]al[ií]zado|falar\s+com\s+humano|atendente\s+humano|quero\s+falar\s+com\s+algu[eé]m|suporte\s+humano|quero\s+um\s+humano|n[aã]o\s+quero\s+rob[oó]|falar\s+com\s+um\s+gerente)\b"
        ]
    }
}
