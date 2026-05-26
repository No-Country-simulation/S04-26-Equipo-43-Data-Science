# Knowledge Source: Google GenAI SDK v2 (google-genai)

**URL:** https://googleapis.github.io/python-genai/
**Fecha de Captura:** 2026-05-26

## Contenido Procesado

### Resumen Técnico
El SDK `google-genai` (v2) es la biblioteca unificada de Google para interactuar con modelos Gemini tanto en Google AI Studio como en Vertex AI. Reemplaza al antiguo `google-generativeai`.

### Sintaxis de Configuración Estructurada
Para obtener respuestas JSON garantizadas, se debe utilizar `response_mime_type` y `response_schema` dentro de `types.GenerateContentConfig`.

#### 1. Uso de Pydantic para el Esquema
```python
from pydantic import BaseModel
from google.genai import types

class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Give me information for the United States.',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=CountryInfo,
    ),
)
print(response.text)
```

#### 2. Uso de Diccionarios (JSON Schema)
```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Give me information for the United States.',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'required': [
                'name',
                'population',
                'capital',
                'continent',
                'gdp',
                'official_language',
                'total_area_sq_mi',
            ],
            'properties': {
                'name': {'type': 'STRING'},
                'population': {'type': 'INTEGER'},
                'capital': {'type': 'STRING'},
                'continent': {'type': 'STRING'},
                'gdp': {'type': 'INTEGER'},
                'official_language': {'type': 'STRING'},
                'total_area_sq_mi': {'type': 'INTEGER'},
            },
            'type': 'OBJECT',
        },
    ),
)
print(response.text)
```

### Mejores Prácticas
- Usar siempre `temperature=0.1` o menor para tareas de extracción de datos para asegurar consistencia.
- El SDK traduce automáticamente los tipos de Python/Pydantic a los tipos internos de la API (ej: `str` -> `STRING`).
- Forzar `response_mime_type='application/json'` es obligatorio cuando se usa `response_schema`.
