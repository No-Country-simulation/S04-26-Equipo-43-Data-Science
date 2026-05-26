# Ejemplo: Cálculo de Coherencia de Diálogo

## Contexto
Analizar si la respuesta del bot es semánticamente cercana a la solicitud del usuario para detectar fallos de NLU.

## Entrada
- Usuario: "¿Cómo puedo cancelar mi suscripción?"
- Bot: "Lo siento, no entiendo tu pregunta. ¿Quieres saber sobre nuestros precios?"

## Proceso
1. Cargar `SentenceTransformer`.
2. Codificar ambas frases.
3. Calcular `cosine_similarity`.

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

user_msg = "¿Cómo puedo cancelar mi suscripción?"
bot_msg = "Lo siento, no entiendo tu pregunta."

emb1 = model.encode(user_msg, convert_to_tensor=True)
emb2 = model.encode(bot_msg, convert_to_tensor=True)

similarity = util.cos_sim(emb1, emb2).item()
# Resultado esperado: ~0.25 (Baja similitud)
```

## Salida Esperada
Un valor flotante entre -1 y 1. Valores cercanos a 0 indican que el bot falló en entender la intención específica.
