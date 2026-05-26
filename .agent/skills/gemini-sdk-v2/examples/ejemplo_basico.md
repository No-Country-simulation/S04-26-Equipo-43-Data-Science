# Ejemplo: Clasificación Estructurada de Texto

## Contexto
Deseamos analizar un mensaje de chat y obtener una clasificación JSON con confianza y etiquetas.

## Entrada
Un mensaje de usuario: "¡Esto es un desastre, mi pedido no llega y nadie responde!"

## Proceso
1. Inicializar cliente con API Key.
2. Definir clase Pydantic `Classification`.
3. Llamar a `generate_content` con el esquema definido.

```python
from google import genai
from google.genai import types
from pydantic import BaseModel

class Classification(BaseModel):
    is_frustrated: bool
    confidence: float
    reasoning: str

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Analiza este mensaje: '¡Esto es un desastre!'",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Classification
    )
)

print(response.text)
```

## Salida Esperada
```json
{
    "is_frustrated": true,
    "confidence": 0.98,
    "reasoning": "El usuario utiliza exclamaciones y lenguaje negativo ('desastre')."
}
```
